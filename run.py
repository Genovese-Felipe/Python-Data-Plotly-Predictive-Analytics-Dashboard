#!/usr/bin/env python3
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
    print("\n🛑 Dashboard stopped")
