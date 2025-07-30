#!/usr/bin/env python3
"""
Dashboard Execution Script
==========================

Simple script to run the Construction Project Monitoring Dashboard.
"""

import os
import sys
import subprocess

def main():
    """Main execution function."""
    print("🚀 Starting Construction Project Monitoring Dashboard")
    print("=" * 60)
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dashboard_script = os.path.join(script_dir, 'scripts', 'viz_new.py')
    
    if not os.path.exists(dashboard_script):
        print("❌ Dashboard script not found at:", dashboard_script)
        return 1
    
    print("📂 Working directory:", script_dir)
    print("🔧 Dashboard script:", dashboard_script)
    print("📍 Will be available at: http://localhost:8050")
    print()
    print("⏳ Loading dashboard... (this may take a few seconds)")
    print("💡 Press Ctrl+C to stop the dashboard")
    print("-" * 60)
    
    try:
        # Change to the script directory and run the dashboard
        os.chdir(script_dir)
        subprocess.run([sys.executable, dashboard_script])
    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped by user")
        return 0
    except Exception as e:
        print(f"\n❌ Error running dashboard: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())