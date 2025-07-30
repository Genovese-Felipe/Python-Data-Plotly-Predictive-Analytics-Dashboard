#!/usr/bin/env python3
"""
Setup script for Python Data Plotly Predictive Analytics Dashboard
================================================================

This script sets up the dashboard environment and generates sample data.
Run this after cloning the repository to get everything working.
"""

import subprocess
import sys
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version}")
    return True

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "-r", "requirements.txt"
        ])
        print("✅ Packages installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install packages: {e}")
        return False

def generate_sample_data():
    """Generate sample data for the dashboard"""
    print("📊 Generating sample data...")
    try:
        subprocess.check_call([
            sys.executable, "scripts/data_gen_new.py"
        ])
        print("✅ Sample data generated successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to generate data: {e}")
        return False

def test_dashboard():
    """Test dashboard components"""
    print("🧪 Testing dashboard components...")
    try:
        subprocess.check_call([
            sys.executable, "test_setup.py"
        ])
        print("✅ Dashboard test passed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Dashboard test failed: {e}")
        return False

def create_run_script():
    """Create a simple run script"""
    script_content = '''#!/usr/bin/env python3
"""
Simple script to run the dashboard
"""
import subprocess
import sys

print("🚀 Starting Construction Project Dashboard...")
print("📊 Access the dashboard at: http://localhost:8050")
print("⏹️  Press Ctrl+C to stop")

try:
    subprocess.run([sys.executable, "scripts/viz_new.py"])
except KeyboardInterrupt:
    print("\\n🛑 Dashboard stopped")
'''
    
    with open('run.py', 'w') as f:
        f.write(script_content)
    
    # Make it executable on Unix systems
    if os.name != 'nt':
        os.chmod('run.py', 0o755)
    
    print("✅ Created run.py script")

def main():
    """Main setup function"""
    print("🏗️ Python Data Plotly Predictive Analytics Dashboard Setup")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        return 1
    
    # Install requirements
    if not install_requirements():
        return 1
    
    # Generate sample data
    if not generate_sample_data():
        return 1
    
    # Test dashboard
    if not test_dashboard():
        return 1
    
    # Create run script
    create_run_script()
    
    print("\n🎉 Setup complete!")
    print("\n📋 Next steps:")
    print("1. Run the dashboard: python run.py")
    print("2. Open your browser to: http://localhost:8050")
    print("3. Explore the interactive dashboard")
    
    print("\n📁 Project structure:")
    print("├── data/          # Generated CSV data files")
    print("├── scripts/       # Python scripts for data generation and visualization")
    print("├── outputs/       # Generated HTML dashboard files")
    print("├── requirements.txt # Python package dependencies")
    print("├── run.py         # Simple script to start the dashboard")
    print("└── test_setup.py  # Test script to validate setup")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())