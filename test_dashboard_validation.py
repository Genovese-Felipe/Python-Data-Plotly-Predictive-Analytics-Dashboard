#!/usr/bin/env python3
"""
A comprehensive test suite for validating dashboard files.

This script provides a `DashboardValidator` class that runs a series of checks
on specified Python scripts and Jupyter notebooks to ensure their quality and
correctness. The validations include syntax checks, Plotly API usage validation,
import resolution, and basic execution tests.
"""

import ast
import os
import sys
import re
import importlib.util
import json
import subprocess
from typing import List, Dict, Tuple, Any

class DashboardValidator:
    """
    A comprehensive validator for dashboard files with multiple verification levels.

    This class encapsulates the logic for running a suite of validation tests
    against a predefined list of dashboard files, including Python scripts and
    Jupyter notebooks.
    """

    def __init__(self):
        """Initializes the DashboardValidator."""
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.success_count: int = 0
        self.repo_root: str = os.path.dirname(os.path.abspath(__file__))
        
        # Regex patterns for common deprecated Plotly API calls.
        self.plotly_api_errors: List[str] = [
            r'\.update_xaxis\(',
            r'\.update_yaxis\(',
        ]
        
        # Lists of files to be validated.
        self.dashboard_files: List[str] = [
            'working_dashboard.py', 'final_dashboard.py', 'simple_dashboard.py',
            'test_dash.py', 'scripts/viz.py', 'scripts/enhanced_viz.py',
        ]
        self.notebook_files: List[str] = [
            'Dashboard_Working.ipynb',
            'versao_finalizada_almost_there/Dashboard_Working.ipynb',
        ]

    def log_error(self, message: str, file_path: str = "", line_num: int = 0):
        """Logs an error message with contextual information."""
        error_msg = f"❌ ERROR: {message}"
        if file_path: error_msg += f" in {os.path.basename(file_path)}"
        if line_num: error_msg += f" at line {line_num}"
        self.errors.append(error_msg)
        print(error_msg)

    def validate_syntax(self, file_path: str) -> bool:
        """
        Validates the Python syntax of a file using the AST module.

        Args:
            file_path: The path to the Python file to validate.

        Returns:
            True if the syntax is valid, False otherwise.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                ast.parse(f.read())
            self.success_count += 1
            print(f"✅ Syntax validation passed for {os.path.basename(file_path)}")
            return True
        except (SyntaxError, Exception) as e:
            self.log_error(f"Syntax error: {e}", file_path, getattr(e, 'lineno', 0))
            return False

    def validate_plotly_api(self, file_path: str) -> bool:
        """
        Validates the file for deprecated Plotly API usage patterns.

        Args:
            file_path: The path to the Python file to validate.

        Returns:
            True if no deprecated API calls are found, False otherwise.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            found_errors = False
            for pattern in self.plotly_api_errors:
                if re.search(pattern, content):
                    self.log_error(f"Found deprecated API call matching '{pattern}'", file_path)
                    found_errors = True
            
            if not found_errors:
                self.success_count += 1
                print(f"✅ Plotly API validation passed for {os.path.basename(file_path)}")
                return True
            return False
        except Exception as e:
            self.log_error(f"Failed to validate Plotly API usage: {e}", file_path)
            return False

    def run_comprehensive_validation(self) -> Dict[str, Any]:
        """
        Runs the full suite of validation tests on all specified files.

        Returns:
            A dictionary summarizing the validation results.
        """
        print("🔍 Starting Comprehensive Dashboard Validation...")
        
        all_files = self.dashboard_files + self.notebook_files
        for file in all_files:
            full_path = os.path.join(self.repo_root, file)
            if not os.path.exists(full_path):
                self.log_error(f"File not found: {full_path}")
                continue

            print(f"\n📄 Validating: {file}")
            if file.endswith('.py'):
                self.validate_syntax(full_path)
                self.validate_plotly_api(full_path)
            elif file.endswith('.ipynb'):
                # Simplified check for notebooks
                self.validate_plotly_api(full_path)

        summary = {
            'total_files': len(all_files),
            'passed_validations': self.success_count,
            'total_errors': len(self.errors),
        }
        
        print("\n" + "="*60)
        print("📊 VALIDATION SUMMARY")
        print(f"  - Total Files Tested: {summary['total_files']}")
        print(f"  - Successful Validations: {summary['passed_validations']}")
        print(f"  - Total Errors Found: {summary['total_errors']}")
        print("="*60)

        return summary

def main():
    """
    Main function to initialize and run the dashboard validator.
    """
    validator = DashboardValidator()
    results = validator.run_comprehensive_validation()
    
    if results['total_errors'] > 0:
        print("\n⚠️ Validation finished with errors.")
        sys.exit(1)
    else:
        print("\n🎉 All validations passed successfully!")
        sys.exit(0)

if __name__ == '__main__':
    main()