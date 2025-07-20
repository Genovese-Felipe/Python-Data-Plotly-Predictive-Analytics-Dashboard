import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd

# Dados de exemplo simples
df = px.data.iris()

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("🌸 Dashboard Íris - Teste", style={'textAlign': 'center'}),
    
    html.P(f"Dataset carregado com {len(df)} amostras", 
           style={'textAlign': 'center', 'fontSize': '18px'}),
    
    dcc.Graph(
        figure=px.scatter(df, x="sepal_width", y="sepal_length", 
                         color="species", title="Análise das Sépalas")
    ),
    
    dcc.Graph(
        figure=px.histogram(df, x="petal_length", color="species",
                           title="Distribuição do Comprimento das Pétalas")
    )
])

if __name__ == '__main__':
    print("🚀 Servidor Dash iniciando...")
    print("📊 Dashboard disponível em: http://localhost:8050")
    app.run_server(debug=True, host='0.0.0.0', port=8050)
