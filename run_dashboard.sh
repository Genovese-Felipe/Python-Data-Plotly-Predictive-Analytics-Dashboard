#!/bin/bash
echo "🚀 Iniciando Dashboard..."
echo "📁 Diretório atual: $(pwd)"
echo "🐍 Python: $(python --version)"

cd /workspaces/Python-Data-Plotly-Predictive-Analytics-Dashboard

echo "📊 Executando dashboard..."
python scripts/viz.py
