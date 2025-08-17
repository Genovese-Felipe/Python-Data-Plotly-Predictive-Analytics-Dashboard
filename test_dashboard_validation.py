#!/usr/bin/env python3
"""
Comprehensive Dashboard Validation Test Suite

This test suite validates that all dashboard files are free from common Plotly API errors
and ensures they can run without exceptions. Multiple verifications are performed to
prevent issues from recurring.

Tests include:
1. Syntax validation for all Python files
2. Import validation for all dashboard modules  
3. Plotly API method validation
4. Dashboard execution tests
5. Common error pattern detection
"""

import ast
import os
import sys
import re
import importlib.util
import json
from typing import List, Dict, Tuple, Any
import subprocess
import tempfile
import time

class DashboardValidator:
    """Comprehensive validator for dashboard files with multiple verification levels"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.success_count = 0
        self.repo_root = os.path.dirname(os.path.abspath(__file__))
        
        # Common Plotly API errors to detect
        self.plotly_api_errors = [
            r'\.update_xaxis\(',  # Should be update_xaxes
            r'\.update_yaxis\(',  # Should be update_yaxes  
            r'\.run_server\(',    # Should be run() in newer Dash versions
            r'\.plotly_chart\(',  # Should be plotly_chart() in Streamlit, not Dash
        ]
        
        # Files to validate
        self.dashboard_files = [
            'working_dashboard.py',
            'final_dashboard.py',
            'simple_dashboard.py',
            'test_dash.py',
            'scripts/viz.py',
            'scripts/enhanced_viz.py',
        ]
        
        # Jupyter notebooks to validate
        self.notebook_files = [
            'Dashboard_Working.ipynb',
            'versao_finalizada_almost_there/Dashboard_Working.ipynb',
        ]

    def log_error(self, message: str, file_path: str = "", line_num: int = 0):
        """Log an error with context"""
        error_msg = f"❌ ERROR: {message}"
        if file_path:
            error_msg += f" in {file_path}"
        if line_num:
            error_msg += f" at line {line_num}"
        self.errors.append(error_msg)
        print(error_msg)

    def log_warning(self, message: str, file_path: str = "", line_num: int = 0):
        """Log a warning with context"""
        warning_msg = f"⚠️  WARNING: {message}"
        if file_path:
            warning_msg += f" in {file_path}"
        if line_num:
            warning_msg += f" at line {line_num}"
        self.warnings.append(warning_msg)
        print(warning_msg)

    def log_success(self, message: str):
        """Log a successful validation"""
        self.success_count += 1
        success_msg = f"✅ {message}"
        print(success_msg)

    def validate_syntax(self, file_path: str) -> bool:
        """Validate Python syntax using AST parsing"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            ast.parse(content)
            self.log_success(f"Syntax validation passed for {file_path}")
            return True
            
        except SyntaxError as e:
            self.log_error(f"Syntax error: {e}", file_path, e.lineno)
            return False
        except Exception as e:
            self.log_error(f"Failed to read/parse file: {e}", file_path)
            return False

    def validate_plotly_api(self, file_path: str) -> bool:
        """Validate Plotly API usage patterns"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            errors_found = False
            lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                for pattern in self.plotly_api_errors:
                    if re.search(pattern, line):
                        errors_found = True
                        
                        # Provide specific guidance for each error
                        if 'update_xaxis' in pattern:
                            self.log_error(f"Found deprecated 'update_xaxis', should be 'update_xaxes'", file_path, line_num)
                        elif 'update_yaxis' in pattern:
                            self.log_error(f"Found deprecated 'update_yaxis', should be 'update_yaxes'", file_path, line_num)
                        elif 'run_server' in pattern:
                            self.log_error(f"Found deprecated 'run_server', should be 'run'", file_path, line_num)
                        elif 'plotly_chart' in pattern:
                            self.log_error(f"Found 'plotly_chart' (Streamlit), should use dcc.Graph in Dash", file_path, line_num)
            
            if not errors_found:
                self.log_success(f"Plotly API validation passed for {file_path}")
                return True
            else:
                return False
                
        except Exception as e:
            self.log_error(f"Failed to validate Plotly API usage: {e}", file_path)
            return False

    def validate_imports(self, file_path: str) -> bool:
        """Validate that all imports are available"""
        try:
            spec = importlib.util.spec_from_file_location("test_module", file_path)
            if spec is None:
                self.log_error(f"Could not load module spec", file_path)
                return False
            
            # Try to import without executing the main block
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Extract only import statements and function definitions
            lines = content.split('\n')
            import_lines = []
            for line in lines:
                stripped = line.strip()
                if (stripped.startswith('import ') or 
                    stripped.startswith('from ') or
                    stripped.startswith('def ') or
                    stripped.startswith('class ') or
                    stripped == '' or
                    stripped.startswith('#')):
                    import_lines.append(line)
                elif 'if __name__' in line:
                    break
            
            # Create temporary file with just imports and definitions
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp:
                tmp.write('\n'.join(import_lines))
                tmp_path = tmp.name
            
            try:
                spec = importlib.util.spec_from_file_location("test_imports", tmp_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                self.log_success(f"Import validation passed for {file_path}")
                return True
                
            finally:
                os.unlink(tmp_path)
                
        except ImportError as e:
            self.log_error(f"Import error: {e}", file_path)
            return False
        except Exception as e:
            self.log_error(f"Failed to validate imports: {e}", file_path)
            return False

    def validate_notebook_json(self, notebook_path: str) -> bool:
        """Validate that Jupyter notebook is valid JSON and check for API errors"""
        try:
            with open(notebook_path, 'r', encoding='utf-8') as f:
                notebook = json.load(f)
            
            # Check notebook structure
            if 'cells' not in notebook:
                self.log_error("Invalid notebook structure: missing 'cells'", notebook_path)
                return False
            
            # Check for API errors in code cells
            errors_found = False
            for cell_idx, cell in enumerate(notebook['cells']):
                if cell.get('cell_type') == 'code' and 'source' in cell:
                    cell_content = '\n'.join(cell['source'])
                    
                    for pattern in self.plotly_api_errors:
                        if re.search(pattern, cell_content):
                            errors_found = True
                            self.log_error(f"Found API error in notebook cell {cell_idx + 1}", notebook_path)
            
            if not errors_found:
                self.log_success(f"Notebook validation passed for {notebook_path}")
                return True
            else:
                return False
                
        except json.JSONDecodeError as e:
            self.log_error(f"Invalid JSON in notebook: {e}", notebook_path)
            return False
        except Exception as e:
            self.log_error(f"Failed to validate notebook: {e}", notebook_path)
            return False

    def test_dashboard_execution(self, file_path: str) -> bool:
        """Test that a dashboard file can be imported and basic objects created"""
        try:
            # Skip actual execution to avoid port conflicts, just test import
            print(f"🧪 Testing dashboard execution for {file_path}...")
            
            # Use subprocess to test the file in isolation
            cmd = [sys.executable, '-c', f"""
import sys
import os
sys.path.insert(0, '{self.repo_root}')

# Import the module
file_path = '{file_path}'
if not os.path.exists(file_path):
    print(f"File not found: {{file_path}}")
    sys.exit(1)

# Try to import and create basic objects
try:
    import importlib.util
    spec = importlib.util.spec_from_file_location("test_dashboard", file_path)
    module = importlib.util.module_from_spec(spec)
    
    # Mock the app.run call to prevent server startup
    import dash
    original_run = dash.Dash.run
    dash.Dash.run = lambda self, *args, **kwargs: None
    
    spec.loader.exec_module(module)
    print("SUCCESS: Dashboard module imported successfully")
    
except Exception as e:
    print(f"ERROR: {{e}}")
    sys.exit(1)
"""]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and "SUCCESS" in result.stdout:
                self.log_success(f"Dashboard execution test passed for {file_path}")
                return True
            else:
                self.log_error(f"Dashboard execution test failed: {result.stderr}", file_path)
                return False
                
        except subprocess.TimeoutExpired:
            self.log_error(f"Dashboard execution test timed out", file_path)
            return False
        except Exception as e:
            self.log_error(f"Failed to test dashboard execution: {e}", file_path)
            return False

    def run_comprehensive_validation(self) -> Dict[str, Any]:
        """Run all validation tests and return summary"""
        print("🔍 Starting Comprehensive Dashboard Validation...")
        print("=" * 60)
        
        results = {
            'total_files': 0,
            'passed_files': 0,
            'failed_files': 0,
            'error_count': 0,
            'warning_count': 0,
            'test_results': {}
        }
        
        # Test Python files
        for file_path in self.dashboard_files:
            full_path = os.path.join(self.repo_root, file_path)
            if not os.path.exists(full_path):
                self.log_warning(f"File not found, skipping: {file_path}")
                continue
                
            results['total_files'] += 1
            file_passed = True
            
            print(f"\n📄 Validating: {file_path}")
            print("-" * 40)
            
            # Run all validation tests
            tests = [
                ('Syntax', lambda: self.validate_syntax(full_path)),
                ('Imports', lambda: self.validate_imports(full_path)),
                ('Plotly API', lambda: self.validate_plotly_api(full_path)),
                ('Execution', lambda: self.test_dashboard_execution(full_path)),
            ]
            
            test_results = {}
            for test_name, test_func in tests:
                try:
                    test_passed = test_func()
                    test_results[test_name] = test_passed
                    if not test_passed:
                        file_passed = False
                except Exception as e:
                    self.log_error(f"{test_name} test failed with exception: {e}", file_path)
                    test_results[test_name] = False
                    file_passed = False
            
            results['test_results'][file_path] = test_results
            
            if file_passed:
                results['passed_files'] += 1
                print(f"✅ {file_path} - ALL TESTS PASSED")
            else:
                results['failed_files'] += 1
                print(f"❌ {file_path} - SOME TESTS FAILED")
        
        # Test Jupyter notebooks
        for notebook_path in self.notebook_files:
            full_path = os.path.join(self.repo_root, notebook_path)
            if not os.path.exists(full_path):
                self.log_warning(f"Notebook not found, skipping: {notebook_path}")
                continue
                
            results['total_files'] += 1
            print(f"\n📓 Validating notebook: {notebook_path}")
            print("-" * 40)
            
            if self.validate_notebook_json(full_path):
                results['passed_files'] += 1
                print(f"✅ {notebook_path} - VALIDATION PASSED")
            else:
                results['failed_files'] += 1
                print(f"❌ {notebook_path} - VALIDATION FAILED")
        
        # Summary
        results['error_count'] = len(self.errors)
        results['warning_count'] = len(self.warnings)
        
        print("\n" + "=" * 60)
        print("📊 VALIDATION SUMMARY")
        print("=" * 60)
        print(f"Total files tested: {results['total_files']}")
        print(f"Files passed: {results['passed_files']}")
        print(f"Files failed: {results['failed_files']}")
        print(f"Total errors: {results['error_count']}")
        print(f"Total warnings: {results['warning_count']}")
        print(f"Success rate: {results['passed_files']}/{results['total_files']} ({100*results['passed_files']/max(1,results['total_files']):.1f}%)")
        
        if results['error_count'] == 0:
            print("\n🎉 ALL VALIDATIONS PASSED! No critical errors found.")
        else:
            print(f"\n⚠️  {results['error_count']} critical errors need to be fixed.")
        
        return results

def main():
    """Main test function"""
    validator = DashboardValidator()
    results = validator.run_comprehensive_validation()
    
    # Return appropriate exit code
    if results['error_count'] > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == '__main__':
    main()