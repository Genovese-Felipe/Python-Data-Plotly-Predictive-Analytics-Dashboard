#!/usr/bin/env python3
"""A runner script for launching the main construction dashboard.

This script provides a convenient way to start the project's main data
visualization dashboard. It ensures that the dashboard is run from the correct
project directory and executes the primary visualization script.

The dashboard itself is defined in `scripts/viz_new.py`.
"""

import subprocess
import sys
import os


def main():
    """Sets up the environment and runs the dashboard script.

    This function changes the current working directory to the project root
    and then executes the `scripts/viz_new.py` script as a subprocess.
    It handles potential errors and user interruptions gracefully.

    Returns:
        An integer status code (0 for success, 1 for failure).
    """
    try:
        # Mudar para o diretório do projeto
        os.chdir("/workspaces/Python-Data-Plotly-Predictive-Analytics-Dashboard")

        # Executar o dashboard
        print("🚀 Iniciando dashboard com layout de 4 linhas...")
        print("📊 Dashboard URL: http://127.0.0.1:8050")
        print("⏹️  Pressione Ctrl+C para parar")

        # Executar viz_new.py
        subprocess.run([sys.executable, "scripts/viz_new.py"], check=True)

    except KeyboardInterrupt:
        print("\n🛑 Dashboard interrompido pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao executar dashboard: {e}")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
