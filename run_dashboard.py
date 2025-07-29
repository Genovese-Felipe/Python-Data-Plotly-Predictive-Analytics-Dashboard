#!/usr/bin/env python3
"""
Script para executar o dashboard seguindo as especificações do projeto
"""

import subprocess
import sys
import os

def main():
    try:
        # Mudar para o diretório do projeto
        os.chdir('/workspaces/Python-Data-Plotly-Predictive-Analytics-Dashboard')
        
        # Executar o dashboard
        print("🚀 Iniciando dashboard com layout de 4 linhas...")
        print("📊 Dashboard URL: http://127.0.0.1:8050")
        print("⏹️  Pressione Ctrl+C para parar")
        
        # Executar viz_new.py
        subprocess.run([sys.executable, 'scripts/viz_new.py'], check=True)
        
    except KeyboardInterrupt:
        print("\n🛑 Dashboard interrompido pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao executar dashboard: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
