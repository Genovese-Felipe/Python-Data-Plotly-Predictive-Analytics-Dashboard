import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np

# Dados simples para teste
np.random.seed(42)
df = pd.DataFrame({
    'projeto': [f'Proj_{i}' for i in range(1, 11)],
    'status': np.random.choice(['Concluído', 'Em Andamento', 'Pausado'], 10),
    'progresso': np.random.randint(20, 100, 10)
})

# App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout
app.layout = dbc.Container([
    
    dbc.Row([
        dbc.Col([
            html.H1("📊 Dashboard Simplificado", className="text-center mb-4 text-primary"),
            html.Hr()
        ], width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Filtro de Status", className="card-title"),
                    dcc.Dropdown(
                        id='status-filter',
                        options=[{'label': s, 'value': s} for s in df['status'].unique()],
                        value=df['status'].unique().tolist(),
                        multi=True
                    )
                ])
            ])
        ], width=12)
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='grafico-status')
                ])
            ])
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='grafico-progresso')
                ])
            ])
        ], width=6)
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            html.Div(id='info-dados', className="text-center text-muted")
        ], width=12)
    ])
    
], fluid=True)

# Callbacks
@app.callback(
    [Output('grafico-status', 'figure'),
     Output('grafico-progresso', 'figure'),
     Output('info-dados', 'children')],
    [Input('status-filter', 'value')]
)
def update_charts(selected_status):
    
    filtered_df = df[df['status'].isin(selected_status)] if selected_status else df
    
    # Gráfico de Status
    status_counts = filtered_df['status'].value_counts()
    fig_status = px.pie(
        values=status_counts.values,
        names=status_counts.index,
        title="Distribuição por Status",
        color_discrete_sequence=['#28a745', '#007bff', '#ffc107']
    )
    
    # Gráfico de Progresso
    fig_progress = px.bar(
        filtered_df,
        x='projeto',
        y='progresso',
        title="Progresso por Projeto",
        color='progresso',
        color_continuous_scale='RdYlGn'
    )
    
    info = f"📊 Mostrando {len(filtered_df)} de {len(df)} projetos"
    
    return fig_status, fig_progress, info

if __name__ == '__main__':
    print("🚀 Dashboard Simplificado Iniciado!")
    print("🌐 Acesse: http://localhost:8050")
    print("💡 Teste os filtros para ver a interatividade")
    app.run_server(debug=True, host='0.0.0.0', port=8050)
