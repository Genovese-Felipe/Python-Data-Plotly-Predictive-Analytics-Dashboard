import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Gerar dados de exemplo
np.random.seed(42)
n_samples = 1000

# Dataset de vendas
dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
sales_data = []

for i, date in enumerate(dates):
    daily_sales = np.random.poisson(50) + np.sin(i/30) * 10 + np.random.normal(0, 5)
    sales_data.append({
        'data': date,
        'vendas': max(0, daily_sales),
        'produto': np.random.choice(['Produto A', 'Produto B', 'Produto C']),
        'regiao': np.random.choice(['Norte', 'Sul', 'Leste', 'Oeste']),
        'vendedor': np.random.choice(['João', 'Maria', 'Pedro', 'Ana', 'Carlos'])
    })

df = pd.DataFrame(sales_data)

# Criar aplicação Dash
app = dash.Dash(__name__)

# Layout da aplicação
app.layout = html.Div([
    html.H1("📊 Dashboard de Vendas - Python Analytics", 
            style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': 30}),
    
    # Cards de KPI
    html.Div([
        html.Div([
            html.H3(f"{df['vendas'].sum():,.0f}", style={'color': '#e74c3c', 'margin': 0}),
            html.P("Total de Vendas", style={'margin': 0})
        ], className="kpi-card", style={
            'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px',
            'boxShadow': '0 4px 6px rgba(0,0,0,0.1)', 'textAlign': 'center',
            'width': '23%', 'display': 'inline-block', 'margin': '1%'
        }),
        
        html.Div([
            html.H3(f"{df['data'].dt.year.nunique()}", style={'color': '#3498db', 'margin': 0}),
            html.P("Ano de Dados", style={'margin': 0})
        ], style={
            'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px',
            'boxShadow': '0 4px 6px rgba(0,0,0,0.1)', 'textAlign': 'center',
            'width': '23%', 'display': 'inline-block', 'margin': '1%'
        }),
        
        html.Div([
            html.H3(f"{df['vendedor'].nunique()}", style={'color': '#2ecc71', 'margin': 0}),
            html.P("Vendedores", style={'margin': 0})
        ], style={
            'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px',
            'boxShadow': '0 4px 6px rgba(0,0,0,0.1)', 'textAlign': 'center',
            'width': '23%', 'display': 'inline-block', 'margin': '1%'
        }),
        
        html.Div([
            html.H3(f"{df['vendas'].mean():.1f}", style={'color': '#f39c12', 'margin': 0}),
            html.P("Média Diária", style={'margin': 0})
        ], style={
            'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px',
            'boxShadow': '0 4px 6px rgba(0,0,0,0.1)', 'textAlign': 'center',
            'width': '23%', 'display': 'inline-block', 'margin': '1%'
        })
    ], style={'marginBottom': '30px'}),
    
    # Filtros
    html.Div([
        html.Div([
            html.Label("Selecione o Produto:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='produto-dropdown',
                options=[{'label': 'Todos', 'value': 'todos'}] + 
                        [{'label': prod, 'value': prod} for prod in df['produto'].unique()],
                value='todos',
                style={'marginBottom': '20px'}
            )
        ], style={'width': '48%', 'display': 'inline-block'}),
        
        html.Div([
            html.Label("Selecione a Região:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='regiao-dropdown',
                options=[{'label': 'Todas', 'value': 'todas'}] + 
                        [{'label': reg, 'value': reg} for reg in df['regiao'].unique()],
                value='todas'
            )
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ], style={'marginBottom': '30px'}),
    
    # Gráficos
    html.Div([
        html.Div([
            dcc.Graph(id='vendas-tempo')
        ], style={'width': '50%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Graph(id='vendas-produto')
        ], style={'width': '50%', 'float': 'right', 'display': 'inline-block'})
    ]),
    
    html.Div([
        html.Div([
            dcc.Graph(id='vendas-regiao')
        ], style={'width': '50%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Graph(id='vendas-vendedor')
        ], style={'width': '50%', 'float': 'right', 'display': 'inline-block'})
    ])
    
], style={'padding': '20px', 'backgroundColor': '#ecf0f1'})

# Callbacks
@app.callback(
    [Output('vendas-tempo', 'figure'),
     Output('vendas-produto', 'figure'),
     Output('vendas-regiao', 'figure'),
     Output('vendas-vendedor', 'figure')],
    [Input('produto-dropdown', 'value'),
     Input('regiao-dropdown', 'value')]
)
def update_graphs(produto_selecionado, regiao_selecionada):
    # Filtrar dados
    df_filtrado = df.copy()
    
    if produto_selecionado != 'todos':
        df_filtrado = df_filtrado[df_filtrado['produto'] == produto_selecionado]
    
    if regiao_selecionada != 'todas':
        df_filtrado = df_filtrado[df_filtrado['regiao'] == regiao_selecionada]
    
    # Gráfico de vendas ao longo do tempo
    vendas_tempo = df_filtrado.groupby('data')['vendas'].sum().reset_index()
    fig_tempo = px.line(vendas_tempo, x='data', y='vendas', 
                       title='📈 Vendas ao Longo do Tempo',
                       labels={'vendas': 'Vendas', 'data': 'Data'})
    fig_tempo.update_traces(line_color='#e74c3c')
    fig_tempo.update_layout(plot_bgcolor='white')
    
    # Gráfico de vendas por produto
    vendas_produto = df_filtrado.groupby('produto')['vendas'].sum().reset_index()
    fig_produto = px.bar(vendas_produto, x='produto', y='vendas',
                        title='🛍️ Vendas por Produto',
                        labels={'vendas': 'Vendas', 'produto': 'Produto'},
                        color='vendas', color_continuous_scale='viridis')
    fig_produto.update_layout(plot_bgcolor='white')
    
    # Gráfico de vendas por região
    vendas_regiao = df_filtrado.groupby('regiao')['vendas'].sum().reset_index()
    fig_regiao = px.pie(vendas_regiao, values='vendas', names='regiao',
                       title='🗺️ Distribuição por Região')
    
    # Gráfico de vendas por vendedor
    vendas_vendedor = df_filtrado.groupby('vendedor')['vendas'].sum().reset_index()
    fig_vendedor = px.bar(vendas_vendedor, x='vendedor', y='vendas',
                         title='👥 Performance por Vendedor',
                         labels={'vendas': 'Vendas', 'vendedor': 'Vendedor'},
                         color='vendas', color_continuous_scale='plasma')
    fig_vendedor.update_layout(plot_bgcolor='white')
    
    return fig_tempo, fig_produto, fig_regiao, fig_vendedor

if __name__ == '__main__':
    print("🚀 Iniciando Dashboard de Vendas...")
    print("🌐 Acesse: http://localhost:8050")
    print("⚡ Dashboard rodando com dados simulados")
    app.run(debug=True, host='0.0.0.0', port=8050)
