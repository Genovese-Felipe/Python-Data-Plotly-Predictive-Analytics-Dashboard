#!/usr/bin/env python3
"""
A validation script for the Monica AI System.

This script runs a comprehensive suite of checks to ensure that the Monica AI
System is properly installed, configured, and all its core components are
functioning as expected. It validates imports, basic functionality, dashboard
integration, and package requirements.
"""

import sys
import traceback
import importlib

def validate_imports():
    """
    Validates that all core and submodule imports for the Monica AI system work correctly.

    This function attempts to import all the main classes and functions from the
    `Monica_AI_System` to ensure the project structure is intact and all
    modules are accessible.

    Returns:
        bool: True if all imports are successful, False otherwise.
    """
    print("🔍 Validating imports...")
    try:
        from Monica_AI_System.core.bot_manager import BotManager
        from Monica_AI_System.core.api_integration import APIIntegrationFramework
        from Monica_AI_System.core.prompt_system import PromptSystem
        from Monica_AI_System.capabilities.knowledge_manager import KnowledgeManager
        from Monica_AI_System.dashboard_integration import integrate_monica_with_dashboard
        print("   ✅ All core component imports are successful.")
        return True
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        traceback.print_exc()
        return False

def validate_basic_functionality():
    """
    Tests the basic functionality of the core components of the Monica AI system.

    This function instantiates the main classes and calls simple methods on them
    to ensure they initialize without errors and are operational.

    Returns:
        bool: True if basic functionality tests pass, False otherwise.
    """
    print("🧪 Validating basic functionality...")
    try:
        from Monica_AI_System.core.bot_manager import BotManager
        from Monica_AI_System.core.api_integration import APIIntegrationFramework
        from Monica_AI_System.core.prompt_system import PromptSystem

        bot_manager = BotManager()
        bot_manager.create_bot(name="ValidationBot", role="Validator")
        print("   ✅ BotManager instantiation and bot creation successful.")

        api_framework = APIIntegrationFramework()
        api_framework.get_api_status()
        print("   ✅ APIIntegrationFramework instantiation and status check successful.")

        prompt_system = PromptSystem()
        prompt_system.list_templates()
        print("   ✅ PromptSystem instantiation and template listing successful.")
        
        return True
    except Exception as e:
        print(f"   ❌ Functionality error: {e}")
        traceback.print_exc()
        return False

def validate_dashboard_integration():
    """
    Tests the integration of the Monica AI system with a Dash application.

    This function creates a dummy Dash app and passes it to the integration
    function to ensure that the integration logic does not raise any exceptions.

    Returns:
        bool: True if the dashboard integration test passes, False otherwise.
    """
    print("🎯 Validating dashboard integration...")
    try:
        import dash
        from Monica_AI_System.dashboard_integration import integrate_monica_with_dashboard
        
        app = dash.Dash(__name__)
        integrate_monica_with_dashboard(app)
        print("   ✅ Dashboard integration function executed successfully.")
        return True
    except Exception as e:
        print(f"   ❌ Dashboard integration error: {e}")
        traceback.print_exc()
        return False

def validate_requirements():
    """
    Checks if all required Python packages are installed in the environment.

    This function iterates through a list of required packages and attempts to
    import them to verify their availability.

    Returns:
        bool: True if all requirements are met, False otherwise.
    """
    print("📦 Validating requirements...")
    required_packages = [
        ('dash', 'dash'), ('plotly', 'plotly'), ('pandas', 'pandas'),
        ('numpy', 'numpy'), ('scikit-learn', 'sklearn')
    ]
    missing = []
    for package_name, import_name in required_packages:
        try:
            importlib.import_module(import_name)
            print(f"   ✅ {package_name}")
        except ImportError:
            missing.append(package_name)
            print(f"   ❌ {package_name} - MISSING")
    
    if missing:
        print(f"\n   ⚠️  Missing packages: {', '.join(missing)}")
        print("   📝 Please run: pip install -r requirements.txt")
        return False
    return True

def main():
    """
    Runs the comprehensive validation suite for the Monica AI system.

    This function orchestrates the execution of all validation checks and prints
    a summary of the results. It returns an exit code based on whether all
    validations passed.

    Returns:
        int: An exit code (0 for success, 1 for failure).
    """
    print("🚀 Monica AI System Validation")
    print("=" * 50)
    
    validations = [
        ("Requirements", validate_requirements),
        ("Imports", validate_imports),
        ("Basic Functionality", validate_basic_functionality),
        ("Dashboard Integration", validate_dashboard_integration)
    ]
    
    results = []
    for name, validation_func in validations:
        print(f"\n--- Running: {name} ---")
        passed = validation_func()
        results.append((name, passed))

    print("\n" + "=" * 50)
    print("📊 Validation Summary")
    print("-" * 50)
    
    all_passed = all(passed for _, passed in results)
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{name:25} {status}")
    
    print("-" * 50)
    if all_passed:
        print("\n🎉 All validations passed! Monica AI System is ready.")
        return 0
    else:
        print("\n⚠️ Some validations failed. Please review the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())