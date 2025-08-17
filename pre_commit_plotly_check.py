#!/usr/bin/env python3
"""
Pre-commit Hook for Plotly API Validation

This script validates that code changes don't introduce common Plotly API errors.
It can be used as a git pre-commit hook or run manually before commits.

Usage:
    python pre_commit_plotly_check.py
    
Or install as git hook:
    cp pre_commit_plotly_check.py .git/hooks/pre-commit
    chmod +x .git/hooks/pre-commit
"""

import os
import re
import sys
import subprocess
from typing import List, Tuple

class PlotlyPreCommitValidator:
    """Pre-commit validator for Plotly API usage"""
    
    def __init__(self):
        self.errors_found = []
        
        # Define common Plotly API errors
        self.api_patterns = [
            (r'\.update_xaxis\(', 'update_xaxis', 'update_xaxes'),
            (r'\.update_yaxis\(', 'update_yaxis', 'update_yaxes'),
            (r'\.run_server\(', 'run_server', 'run'),
            (r'app\.run_server\(', 'app.run_server', 'app.run'),
        ]
        
        # File patterns to check
        self.file_patterns = ['*.py', '*.ipynb']
    
    def get_staged_files(self) -> List[str]:
        """Get list of staged files from git"""
        try:
            result = subprocess.run(
                ['git', 'diff', '--cached', '--name-only'],
                capture_output=True, text=True
            )
            
            if result.returncode == 0:
                files = result.stdout.strip().split('\n')
                return [f for f in files if f and any(
                    f.endswith(pattern.replace('*', '')) 
                    for pattern in self.file_patterns
                )]
            else:
                # If not in a git repo, check all relevant files
                return self.get_all_relevant_files()
                
        except FileNotFoundError:
            # Git not available, check all files
            return self.get_all_relevant_files()
    
    def get_all_relevant_files(self) -> List[str]:
        """Get all relevant files in the repository"""
        files = []
        for root, dirs, filenames in os.walk('.'):
            # Skip hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for filename in filenames:
                if any(filename.endswith(pattern.replace('*', '')) for pattern in self.file_patterns):
                    files.append(os.path.join(root, filename))
        
        return files
    
    def check_file(self, file_path: str) -> List[Tuple[int, str, str, str]]:
        """Check a single file for API errors"""
        errors = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                for pattern, old_method, new_method in self.api_patterns:
                    if re.search(pattern, line):
                        errors.append((line_num, line.strip(), old_method, new_method))
            
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
        
        return errors
    
    def validate_all_files(self) -> bool:
        """Validate all staged files"""
        files_to_check = self.get_staged_files()
        
        if not files_to_check:
            print("✅ No relevant files to check")
            return True
        
        print(f"🔍 Checking {len(files_to_check)} files for Plotly API errors...")
        
        all_valid = True
        
        for file_path in files_to_check:
            if not os.path.exists(file_path):
                continue
                
            errors = self.check_file(file_path)
            
            if errors:
                all_valid = False
                print(f"\n❌ {file_path}:")
                
                for line_num, line_content, old_method, new_method in errors:
                    print(f"  Line {line_num}: Found '{old_method}', should be '{new_method}'")
                    print(f"    {line_content}")
                    
                self.errors_found.extend(errors)
        
        return all_valid
    
    def print_summary(self, valid: bool):
        """Print validation summary"""
        if valid:
            print("\n✅ All files passed Plotly API validation!")
            print("📝 No deprecated API calls found.")
        else:
            print(f"\n❌ Found {len(self.errors_found)} Plotly API errors!")
            print("\n🔧 How to fix:")
            print("  • Replace 'update_xaxis' with 'update_xaxes'")
            print("  • Replace 'update_yaxis' with 'update_yaxes'")
            print("  • Replace 'run_server' with 'run'")
            print("\n📖 For more help, see:")
            print("  • Plotly documentation: https://plotly.com/python/")
            print("  • Dash documentation: https://dash.plotly.com/")

def main():
    """Main validation function"""
    validator = PlotlyPreCommitValidator()
    
    print("🚀 Plotly API Pre-commit Validation")
    print("=" * 40)
    
    valid = validator.validate_all_files()
    validator.print_summary(valid)
    
    if not valid:
        print("\n🚫 Commit blocked due to API errors. Please fix and try again.")
        sys.exit(1)
    else:
        print("\n✅ Validation passed. Ready to commit!")
        sys.exit(0)

if __name__ == '__main__':
    main()