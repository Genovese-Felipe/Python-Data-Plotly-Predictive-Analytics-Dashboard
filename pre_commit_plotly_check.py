#!/usr/bin/env python3
"""
Pre-commit Hook for Plotly API Validation

This script validates that code changes don't introduce common Plotly API errors.
It can be used as a git pre-commit hook or run manually against specific files.

Usage:
    - As a pre-commit hook (no arguments): Validates staged files.
    - Manually: python pre_commit_plotly_check.py [file1.py] [file2.ipynb] ...
"""

import os
import re
import sys
import subprocess
from typing import List, Tuple

class PlotlyPreCommitValidator:
    """A validator to check for deprecated Plotly API usage in Python and notebook files."""

    def __init__(self):
        """Initializes the validator."""
        self.errors_found: List[Tuple[str, int, str, str, str]] = []
        self.api_patterns: List[Tuple[str, str, str]] = [
            (r'\.update_xaxis\(', 'update_xaxis', 'update_xaxes'),
            (r'\.update_yaxis\(', 'update_yaxis', 'update_yaxes'),
            (r'\.run_server\(', 'run_server', 'run'),
        ]
        self.file_patterns: List[str] = ['*.py', '*.ipynb']

    def get_staged_files(self) -> List[str]:
        """
        Gets the list of staged Python and notebook files from git.

        Returns:
            A list of file paths.
        """
        try:
            result = subprocess.run(
                ['git', 'diff', '--cached', '--name-only'],
                capture_output=True, text=True, check=True
            )
            files = result.stdout.strip().split('\n')
            return [
                f for f in files if f and any(f.endswith(ext) for ext in ['.py', '.ipynb'])
            ]
        except (FileNotFoundError, subprocess.CalledProcessError):
            # Fallback for non-git environments or if git command fails
            return self.get_all_relevant_files()

    def get_all_relevant_files(self) -> List[str]:
        """
        Gets all relevant Python and notebook files in the repository.

        Returns:
            A list of all found file paths.
        """
        all_files = []
        for root, _, filenames in os.walk('.'):
            if '.git' in root or '.vscode' in root:
                continue
            for filename in filenames:
                if any(filename.endswith(ext) for ext in ['.py', '.ipynb']):
                    all_files.append(os.path.join(root, filename))
        return all_files

    def check_file(self, file_path: str) -> List[Tuple[int, str, str, str]]:
        """
        Checks a single file for deprecated API calls.

        Args:
            file_path: The path to the file to check.

        Returns:
            A list of tuples, each containing error details.
        """
        errors = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # For notebooks, we check the content as a single block
            if file_path.endswith('.ipynb'):
                lines = [content] # Check the whole file content
            else:
                lines = content.split('\n')

            for line_num, line in enumerate(lines, 1):
                for pattern, old_method, new_method in self.api_patterns:
                    if re.search(pattern, line):
                        errors.append((line_num, line.strip(), old_method, new_method))
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
        return errors

    def validate_files(self, files_to_check: List[str]) -> bool:
        """
        Validates a list of files for API errors.

        Args:
            files_to_check: A list of file paths to validate.

        Returns:
            True if all files are valid, False otherwise.
        """
        if not files_to_check:
            print("✅ No relevant files to check.")
            return True

        print(f"🔍 Checking {len(files_to_check)} files for Plotly API errors...")
        all_valid = True
        for file_path in files_to_check:
            if not os.path.exists(file_path):
                continue
            
            errors = self.check_file(file_path)
            if errors:
                all_valid = False
                print(f"\n❌ Found errors in {file_path}:")
                for line_num, line, old, new in errors:
                    message = f"  - Line {line_num}: Found '{old}', should be '{new}'."
                    print(message)
                    self.errors_found.append((file_path, line_num, line, old, new))
        return all_valid

    def print_summary(self, is_valid: bool):
        """
        Prints a summary of the validation results.

        Args:
            is_valid: A boolean indicating if all checks passed.
        """
        if is_valid:
            print("\n✅ All checked files passed Plotly API validation!")
        else:
            print(f"\n❌ Found {len(self.errors_found)} Plotly API errors.")
            print("   Please fix the issues listed above and try again.")

def main():
    """
    Main function to run the validation process.

    It determines which files to check (either from command-line arguments or
    from git staged files) and then runs the validator.
    """
    validator = PlotlyPreCommitValidator()
    
    # If file paths are passed as arguments, use them.
    # Otherwise, get staged files for pre-commit hook functionality.
    args = sys.argv[1:]
    if args:
        files_to_check = args
        print("Running validation on specified files...")
    else:
        print("Running validation on staged files...")
        files_to_check = validator.get_staged_files()

    is_valid = validator.validate_files(files_to_check)
    validator.print_summary(is_valid)
    
    if not is_valid:
        print("\n🚫 Commit blocked due to API errors.")
        sys.exit(1)
    else:
        print("\n✅ Validation passed. Ready to commit!")
        sys.exit(0)

if __name__ == '__main__':
    main()