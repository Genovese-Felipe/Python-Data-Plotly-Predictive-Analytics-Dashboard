#!/usr/bin/env python3
"""
Test script for the organized dashboard version
===============================================

This script validates that the organized version works correctly.
"""

import os
import sys
import pandas as pd

def test_file_structure():
    """Test that all expected files exist in the organized structure."""
    print("🔍 Testing file structure...")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    expected_files = [
        'README.md',
        'Dashboard_Working.ipynb',
        'scripts/viz_new.py',
        'scripts/data_gen_final.py',
        'data/projects_master.csv',
        'data/project_status.csv',
        'data/project_stages.csv',
        'data/budget_variance.csv',
        'data/resources.csv',
        'data/workload.csv',
        'documentacao/PROJECT_COMPLETION_REPORT.md',
        'documentacao/PULL_REQUEST_ALMOST_THERE.md',
        'documentacao/FINAL_STATUS_CHECK.md',
        'documentacao/PROJETO_FINALIZADO.md'
    ]
    
    missing_files = []
    for file_path in expected_files:
        full_path = os.path.join(base_dir, file_path)
        if not os.path.exists(full_path):
            missing_files.append(file_path)
        else:
            print(f"   ✅ {file_path}")
    
    if missing_files:
        print(f"   ❌ Missing files: {missing_files}")
        return False
    
    print("   ✅ All expected files present!")
    return True

def test_data_loading():
    """Test that data files can be loaded correctly."""
    print("\n📊 Testing data loading...")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, 'data')
    
    csv_files = [
        'projects_master.csv',
        'project_status.csv', 
        'project_stages.csv',
        'budget_variance.csv',
        'resources.csv',
        'workload.csv'
    ]
    
    total_records = 0
    for csv_file in csv_files:
        file_path = os.path.join(data_dir, csv_file)
        try:
            df = pd.read_csv(file_path)
            record_count = len(df)
            total_records += record_count
            print(f"   ✅ {csv_file}: {record_count} records")
        except Exception as e:
            print(f"   ❌ {csv_file}: Error loading - {e}")
            return False
    
    print(f"   📈 Total records loaded: {total_records}")
    return True

def test_script_imports():
    """Test that the Python scripts can be imported without errors."""
    print("\n🐍 Testing script imports...")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    scripts_dir = os.path.join(base_dir, 'scripts')
    
    # Add scripts directory to path
    sys.path.insert(0, scripts_dir)
    
    try:
        # Test imports without running the scripts
        import importlib.util
        
        # Test data_gen_final
        spec = importlib.util.spec_from_file_location(
            "data_gen_final", 
            os.path.join(scripts_dir, "data_gen_final.py")
        )
        data_gen_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(data_gen_module)
        print("   ✅ data_gen_final.py imports successfully")
        
        # Test viz_new (just check it can be parsed)
        with open(os.path.join(scripts_dir, "viz_new.py"), 'r') as f:
            code = f.read()
            compile(code, "viz_new.py", "exec")
        print("   ✅ viz_new.py syntax is valid")
        
    except Exception as e:
        print(f"   ❌ Import error: {e}")
        return False
    
    return True

def main():
    """Run all tests."""
    print("🚀 Testing Organized Dashboard Version")
    print("=" * 50)
    
    all_tests_passed = True
    
    # Run tests
    all_tests_passed &= test_file_structure()
    all_tests_passed &= test_data_loading() 
    all_tests_passed &= test_script_imports()
    
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("🎉 All tests passed! The organized version is working correctly.")
        print("\n📋 To run the dashboard:")
        print("   cd versao_finalizada_almost_there")
        print("   python scripts/viz_new.py")
        print("   # Access: http://localhost:8050")
    else:
        print("❌ Some tests failed. Please check the issues above.")
    
    return all_tests_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)