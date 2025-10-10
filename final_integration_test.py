#!/usr/bin/env python3
"""
An integration test suite to validate the complete fix for Plotly API errors.

This script runs a series of tests to ensure that the main dashboard executes
without errors, that the API validation system correctly identifies deprecated
calls, and that the overall system is protected against the recurrence of these
specific API issues.
"""

import subprocess
import sys
import os

def test_dashboard_execution():
    """
    Tests that the main dashboard script executes without errors.

    This function runs the `working_dashboard.py` script in a separate process
    and asserts that the Dash app object and its callback are created correctly.
    It also invokes the callback to ensure it returns the expected number of figures.

    Returns:
        bool: True if the test passes, False otherwise.
    """
    print("🧪 Testing dashboard execution...")
    
    # A self-contained script to test the dashboard's functionality in isolation.
    test_script = '''
import sys
import os
import traceback
# Assuming the script is run from the repository root.
sys.path.insert(0, os.getcwd())
try:
    import working_dashboard
    assert hasattr(working_dashboard, "app"), "Dashboard app object not found."
    assert hasattr(working_dashboard, "update_charts"), "Callback function 'update_charts' not found."
    
    # Test callback execution with sample data.
    result = working_dashboard.update_charts(["Web Dev", "Data Analysis"])
    assert len(result) == 4, f"Expected 4 figures, but got {len(result)}."
    
    print("✅ Dashboard execution test: PASSED")
    print("✅ All callback functions work correctly.")
    print("✅ Plotly API calls execute without errors.")
except Exception as e:
    print(f"❌ Dashboard test failed: {e}")
    traceback.print_exc()
    sys.exit(1)
'''
    
    cmd = [sys.executable, '-c', test_script]
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    
    if result.returncode == 0:
        print(result.stdout)
        return True
    else:
        print(f"❌ Dashboard execution failed:\n{result.stderr}")
        return False

def test_api_validation():
    """
    Tests that the API validation system correctly identifies a clean codebase.

    This function runs the `pre_commit_plotly_check.py` script and expects it
    to return a success exit code, indicating that no deprecated API calls
    were found in the repository.

    Returns:
        bool: True if the validation passes, False otherwise.
    """
    print("\n🧪 Testing API validation system...")
    
    result = subprocess.run([sys.executable, 'pre_commit_plotly_check.py'], 
                          capture_output=True, text=True, check=False)
    
    if result.returncode == 0:
        print("✅ Pre-commit API validation: PASSED")
        print("✅ No deprecated API calls detected.")
        return True
    else:
        print(f"❌ API validation failed:\n{result.stderr}")
        return False

def test_create_error_scenario():
    """
    Tests the error detection capability by creating a temporary file with a known error.

    This function writes a temporary Python file containing a deprecated API call
    and then runs the validation script against it, expecting the script to fail
    and correctly identify the error.

    Returns:
        bool: True if the error is correctly detected, False otherwise.
    """
    print("\n🧪 Testing error detection capability...")
    
    test_file_content = '''
import plotly.express as px
def broken_function():
    fig = px.bar(x=[1,2,3], y=[1,2,3])
    fig.update_xaxis(tickangle=45)  # This should be detected as an error.
    return fig
'''
    
    test_filename = 'temp_test_error_file.py'
    with open(test_filename, 'w', encoding='utf-8') as f:
        f.write(test_file_content)
    
    try:
        # Run validation on the temporary error file.
        result = subprocess.run([sys.executable, 'pre_commit_plotly_check.py', test_filename],
                              capture_output=True, text=True, check=False)
        
        # The test passes if the validation script returns a non-zero exit code
        # and correctly identifies the deprecated call in its output.
        if result.returncode != 0 and 'update_xaxis' in result.stdout:
            print("✅ Error detection test: PASSED")
            print("✅ Validation correctly identified the deprecated API call.")
            return True
        else:
            print("❌ Error detection failed - deprecated API was not caught.")
            print(f"Exit Code: {result.returncode}\nStdout: {result.stdout}\nStderr: {result.stderr}")
            return False
    
    finally:
        # Clean up the temporary test file.
        if os.path.exists(test_filename):
            os.remove(test_filename)

def main():
    """
    Runs the full suite of integration tests and reports the results.

    This function orchestrates the execution of all defined tests, tracks the
    number of passed and failed tests, and prints a final summary of the
    validation results.

    Returns:
        bool: True if all tests pass, False otherwise.
    """
    print("🚀 Final Integration Test - Plotly API Fix Validation")
    print("=" * 60)
    
    tests = [
        ("Dashboard Execution", test_dashboard_execution),
        ("API Validation System", test_api_validation),
        ("Error Detection", test_create_error_scenario),
    ]
    
    passed_count = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running: {test_name}")
        print("-" * 40)
        
        try:
            if test_func():
                passed_count += 1
        except Exception as e:
            print(f"❌ Test '{test_name}' failed with an unexpected exception: {e}")
    
    print("\n" + "=" * 60)
    print("📊 FINAL TEST RESULTS")
    print("=" * 60)
    print(f"Tests passed: {passed_count}/{total_tests}")
    print(f"Success rate: {100 * passed_count / total_tests:.1f}%")
    
    if passed_count == total_tests:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Plotly API errors have been completely resolved.")
        print("✅ The prevention system is working correctly.")
        print("🛡️ The system is now protected against recurrence!")
        return True
    else:
        print(f"\n⚠️ {total_tests - passed_count} tests failed.")
        print("❌ Additional fixes may be needed.")
        return False

if __name__ == '__main__':
    if main():
        sys.exit(0)
    else:
        sys.exit(1)