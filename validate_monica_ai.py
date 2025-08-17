#!/usr/bin/env python3
"""
Monica AI System Validation Script
=================================

Comprehensive validation to ensure the Monica AI System is properly 
implemented and all components work correctly.
"""

import sys
import traceback

def validate_imports():
    """Validate all core imports work correctly."""
    print("🔍 Validating imports...")
    
    try:
        # Core imports
        from Monica_AI_System import BotManager, APIIntegrationFramework, PromptSystem, PlatformManager
        print("   ✅ Main package imports successful")
        
        # Module-specific imports
        from Monica_AI_System.core import BotManager as CoreBotManager
        from Monica_AI_System.capabilities import KnowledgeManager, WritingAssistant
        from Monica_AI_System.integrations import PlatformManager as IntegrationPlatformManager
        from Monica_AI_System.config import get_config
        print("   ✅ Submodule imports successful")
        
        # Dashboard integration
        from Monica_AI_System.dashboard_integration import integrate_monica_with_dashboard
        print("   ✅ Dashboard integration import successful")
        
        return True
    except Exception as e:
        print(f"   ❌ Import error: {e}")
        traceback.print_exc()
        return False

def validate_basic_functionality():
    """Test basic functionality of core components."""
    print("🧪 Validating basic functionality...")
    
    try:
        from Monica_AI_System.core.bot_manager import BotManager
        from Monica_AI_System.core.api_integration import APIIntegrationFramework
        from Monica_AI_System.core.prompt_system import PromptSystem
        
        # Test BotManager
        bot_manager = BotManager()
        bot_id = bot_manager.create_bot(
            name="Validation Bot",
            role="General Assistant",
            description="Test bot for validation",
            capabilities=["General assistance", "Question answering"],
            knowledge_domains=["General knowledge", "Basic support"],
            owner_id="validator"
        )
        print("   ✅ Bot creation successful")
        
        # Test API Framework
        api_framework = APIIntegrationFramework()
        status = api_framework.get_api_status()
        print(f"   ✅ API framework status: {len(status)} APIs available")
        
        # Test Prompt System
        prompt_system = PromptSystem()
        templates = prompt_system.list_templates()
        print(f"   ✅ Prompt system: {len(templates)} templates available")
        
        return True
    except Exception as e:
        print(f"   ❌ Functionality error: {e}")
        traceback.print_exc()
        return False

def validate_dashboard():
    """Test dashboard integration."""
    print("🎯 Validating dashboard integration...")
    
    try:
        import dash
        from Monica_AI_System.dashboard_integration import integrate_monica_with_dashboard
        
        # Create test app
        app = dash.Dash(__name__)
        
        # Test integration
        integrate_monica_with_dashboard(app)
        print("   ✅ Dashboard integration successful")
        
        return True
    except Exception as e:
        print(f"   ❌ Dashboard error: {e}")
        traceback.print_exc()
        return False

def validate_requirements():
    """Check if requirements are satisfied."""
    print("📦 Validating requirements...")
    
    required_packages = [
        ('dash', 'dash'), 
        ('plotly', 'plotly'), 
        ('pandas', 'pandas'), 
        ('numpy', 'numpy'), 
        ('scikit-learn', 'sklearn')
    ]
    
    missing = []
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"   ✅ {package_name}")
        except ImportError:
            missing.append(package_name)
            print(f"   ❌ {package_name} - missing")
    
    if missing:
        print(f"   ⚠️  Missing packages: {', '.join(missing)}")
        print("   📝 Run: pip install -r requirements.txt")
        return False
    
    return True

def main():
    """Run comprehensive validation."""
    print("🚀 Monica AI System Validation")
    print("=" * 50)
    
    validations = [
        ("Requirements", validate_requirements),
        ("Imports", validate_imports),
        ("Basic Functionality", validate_basic_functionality),
        ("Dashboard Integration", validate_dashboard)
    ]
    
    results = []
    for name, validation_func in validations:
        try:
            result = validation_func()
            results.append((name, result))
            print()
        except Exception as e:
            print(f"❌ {name} validation failed: {e}")
            results.append((name, False))
            print()
    
    # Summary
    print("📊 Validation Summary")
    print("-" * 30)
    
    all_passed = True
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{name:20} {status}")
        if not passed:
            all_passed = False
    
    print()
    if all_passed:
        print("🎉 All validations passed! Monica AI System is ready to use.")
        print("🚀 Run: python final_dashboard.py")
        return 0
    else:
        print("⚠️  Some validations failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())