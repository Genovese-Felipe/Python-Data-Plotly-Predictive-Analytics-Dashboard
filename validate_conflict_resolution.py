#!/usr/bin/env python3
"""
Conflict Resolution Validation Script
====================================

This script validates that the merge conflict resolution is correct
by testing the resolved files without requiring all dependencies.
"""

import ast
import os
import sys

def test_python_syntax(filepath):
    """Test if a Python file has valid syntax."""
    print(f"\n🔍 Testing syntax: {filepath}")
    try:
        with open(filepath, 'r') as f:
            source = f.read()
        
        # Check for remaining conflict markers
        conflict_markers = ['<<<<<<<', '=======' , '>>>>>>>']
        for marker in conflict_markers:
            if marker in source:
                print(f"❌ Found conflict marker '{marker}' in {filepath}")
                return False
        
        # Test syntax
        ast.parse(source)
        print(f"✅ {filepath} has valid Python syntax")
        return True
        
    except SyntaxError as e:
        print(f"❌ Syntax error in {filepath}: {e}")
        return False
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        return False
    except Exception as e:
        print(f"❌ Error testing {filepath}: {e}")
        return False

def test_gitignore():
    """Test that .gitignore is properly resolved."""
    print("\n🔍 Testing .gitignore resolution")
    try:
        with open('.gitignore', 'r') as f:
            content = f.read()
        
        # Check for conflict markers
        if any(marker in content for marker in ['<<<<<<<', '=======', '>>>>>>>']):
            print("❌ .gitignore still contains conflict markers")
            return False
        
        # Check for expected patterns
        expected_patterns = [
            '__pycache__/',
            '*/__pycache__/',
            '**/__pycache__/',
            '.Python',
            'build/',
            'dist/',
            '.vscode/',
            '.DS_Store'
        ]
        
        missing_patterns = []
        for pattern in expected_patterns:
            if pattern not in content:
                missing_patterns.append(pattern)
        
        if missing_patterns:
            print(f"❌ Missing expected patterns in .gitignore: {missing_patterns}")
            return False
            
        print("✅ .gitignore properly resolved with comprehensive patterns")
        return True
        
    except Exception as e:
        print(f"❌ Error testing .gitignore: {e}")
        return False

def test_optional_import_pattern():
    """Test that final_dashboard.py has proper optional import pattern."""
    print("\n🔍 Testing optional import pattern in final_dashboard.py")
    try:
        with open('final_dashboard.py', 'r') as f:
            content = f.read()
        
        # Check for optional import pattern
        if 'try:' not in content or 'MONICA_AI_AVAILABLE' not in content:
            print("❌ final_dashboard.py missing optional import pattern")
            return False
            
        if 'except ImportError:' not in content:
            print("❌ final_dashboard.py missing ImportError handling")
            return False
            
        print("✅ final_dashboard.py has proper optional import pattern")
        return True
        
    except Exception as e:
        print(f"❌ Error testing optional import pattern: {e}")
        return False

def main():
    """Run all validation tests."""
    print("🧪 Running Conflict Resolution Validation")
    print("=" * 50)
    
    tests = [
        ("Python Syntax Tests", [
            lambda: test_python_syntax('final_dashboard.py'),
            lambda: test_python_syntax('test_dash.py'),
            lambda: test_python_syntax('working_dashboard.py'),
        ]),
        ("File Resolution Tests", [
            test_gitignore,
            test_optional_import_pattern,
        ])
    ]
    
    total_tests = 0
    passed_tests = 0
    
    for category, test_functions in tests:
        print(f"\n📋 {category}")
        print("-" * 30)
        
        for test_func in test_functions:
            total_tests += 1
            if test_func():
                passed_tests += 1
    
    print(f"\n📊 Results: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All conflict resolution tests passed!")
        print("✅ The merge conflicts have been properly resolved")
        return True
    else:
        print("❌ Some tests failed - conflicts may not be fully resolved")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)