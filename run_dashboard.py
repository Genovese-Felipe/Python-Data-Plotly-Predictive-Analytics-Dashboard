#!/usr/bin/env python3
"""
A runner script to launch the main project dashboard.

This script is designed to execute the primary dashboard visualization script,
`scripts/viz_new.py`, which contains the full dashboard layout with four rows
of charts and components.
"""

import subprocess
import sys
import os

def main():
    """
    Executes the main dashboard script.

    This function changes the current working directory to the project root,
    prints a message to the console, and then runs the `scripts/viz_new.py`
    script as a subprocess.

    Returns:
        int: 0 on successful execution, 1 on error.
    """
    try:
        # Change to the project's root directory
        # This ensures that the script can be run from any location
        project_root = os.path.dirname(os.path.abspath(__file__))
        os.chdir(project_root)

        # Execute the dashboard script
        print("🚀 Starting dashboard with a 4-row layout...")
        print("📊 Dashboard URL: http://127.0.0.1:8050")
        print("⏹️  Press Ctrl+C to stop")

        # Run viz_new.py
        subprocess.run([sys.executable, 'scripts/viz_new.py'], check=True)

    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped by user")
    except Exception as e:
        print(f"❌ Error running dashboard: {e}")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())