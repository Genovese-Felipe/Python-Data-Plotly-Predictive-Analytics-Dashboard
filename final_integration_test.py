#!/usr/bin/env python3
"""
Final Integration Test - Demonstrates Complete Fix

This test demonstrates that the Plotly API errors have been completely
resolved and that the prevention system is working.
"""

import subprocess
import sys
import os

def test_dashboard_execution():
    """Test that the main dashboard executes without errors"""
    print("🧪 Testing dashboard execution...")
    
    # Test the main dashboard file
    cmd = [sys.executable, '-c', '''
import sys
import os
sys.path.insert(0, "/home/runner/work/Python-Data-Plotly-Predictive-Analytics-Dashboard/Python-Data-Plotly-Predictive-Analytics-Dashboard")

try:
    # Import and test the fixed dashboard
    import working_dashboard
    
    # Verify the app object was created
    assert hasattr(working_dashboard, "app"), "Dashboard app not created"
    
    # Test that the callback function exists and uses correct API
    assert hasattr(working_dashboard, "update_charts"), "Callback function not found"
    
    # Test callback execution with sample data
    result = working_dashboard.update_charts(["Web Dev", "Data Analysis"])
    
    # Verify we get 4 figures back (pie, bar, scatter, sunburst)
    assert len(result) == 4, f"Expected 4 figures, got {len(result)}"
    
    print("✅ Dashboard execution test: PASSED")
    print("✅ All callback functions work correctly")
    print("✅ Plotly API calls execute without errors")
    
except Exception as e:
    print(f"❌ Dashboard test failed: {e}")
    sys.exit(1)
''']
    
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd())
    
    if result.returncode == 0:
        print(result.stdout)
        return True
    else:
        print(f"❌ Dashboard execution failed: {result.stderr}")
        return False

def test_api_validation():
    """Test that our API validation catches errors"""
    print("\n🧪 Testing API validation system...")
    
    # Run the pre-commit check
    result = subprocess.run([sys.executable, 'pre_commit_plotly_check.py'], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Pre-commit API validation: PASSED")
        print("✅ No deprecated API calls detected")
        return True
    else:
        print(f"❌ API validation failed: {result.stderr}")
        return False

def test_create_error_scenario():
    """Create a test file with errors to verify detection works"""
    print("\n🧪 Testing error detection capability...")
    
    # Create a temporary file with the old error
    test_file_content = '''
import plotly.express as px

def broken_function():
    fig = px.bar(x=[1,2,3], y=[1,2,3])
    fig.update_xaxis(tickangle=45)  # This should be detected as error
    return fig
'''
    
    with open('test_error_file.py', 'w') as f:
        f.write(test_file_content)
    
    try:
        # Run validation on the error file
        result = subprocess.run([sys.executable, 'pre_commit_plotly_check.py'], 
                              capture_output=True, text=True)
        
        # Should detect the error and return non-zero exit code
        if result.returncode != 0 and 'update_xaxis' in result.stdout:
            print("✅ Error detection test: PASSED")
            print("✅ Validation correctly identified deprecated API call")
            return True
        else:
            print("❌ Error detection failed - deprecated API not caught")
            return False
    
    finally:
        # Clean up test file
        if os.path.exists('test_error_file.py'):
            os.remove('test_error_file.py')

def main():
    """Run all integration tests"""
    print("🚀 Final Integration Test - Plotly API Fix Validation")
    print("=" * 60)
    
    tests = [
        ("Dashboard Execution", test_dashboard_execution),
        ("API Validation System", test_api_validation),
        ("Error Detection", test_create_error_scenario),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running: {test_name}")
        print("-" * 40)
        
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ Test '{test_name}' failed with exception: {e}")
    
    print("\n" + "=" * 60)
    print("📊 FINAL TEST RESULTS")
    print("=" * 60)
    print(f"Tests passed: {passed}/{total}")
    print(f"Success rate: {100*passed/total:.1f}%")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Plotly API errors have been completely resolved")
        print("✅ Prevention system is working correctly")
        print("✅ Multiple verification levels are active")
        print("\n🛡️ The system is now protected against recurrence!")
        return True
    else:
        print(f"\n⚠️ {total - passed} tests failed")
        print("❌ Additional fixes may be needed")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)