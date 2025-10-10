#!/usr/bin/env python3
"""
An execution script to launch the construction project monitoring dashboard.

This script provides a convenient way to run the main dashboard application,
`viz_new.py`, ensuring that it is executed from the correct directory context.
"""

import os
import sys
import subprocess

def main():
    """
    Sets up the environment and runs the main dashboard visualization script.

    This function locates the `viz_new.py` script within the 'scripts'
    subdirectory, changes the current working directory to ensure all relative
    paths in the visualization script work correctly, and then executes it as
    a subprocess. It also handles user interruptions and other potential errors.

    Returns:
        int: An exit code (0 for success, 1 for failure).
    """
    print("🚀 Starting Construction Project Monitoring Dashboard...")
    print("=" * 60)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    dashboard_script = os.path.join(script_dir, 'scripts', 'viz_new.py')

    if not os.path.exists(dashboard_script):
        print(f"❌ Dashboard script not found at: {dashboard_script}")
        return 1

    print(f"📂 Working directory: {script_dir}")
    print(f"🔧 Dashboard script: {dashboard_script}")
    print("📍 Dashboard will be available at: http://localhost:8050")
    print("\n⏳ Loading dashboard... (this may take a few seconds)")
    print("💡 Press Ctrl+C to stop the dashboard")
    print("-" * 60)

    try:
        # Change to the script's directory to ensure correct relative path handling
        os.chdir(script_dir)
        subprocess.run([sys.executable, os.path.join('scripts', 'viz_new.py')], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped by user.")
        return 0
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"\n❌ Error running dashboard: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())