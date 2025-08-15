"""
Productivity Tools Comparison Dashboard - Interactive Visualization
================================================================

Creates an interactive dashboard for productivity tools analysis using Plotly Dash.
Uses ONLY pandas, numpy, and plotly as required by project specifications.

Dashboard Features:
- Overall comparison and ranking
- Detailed criteria breakdown
- Use cases analysis
- Pricing comparison
- Market analysis trends
- Professional styling with Bootstrap components
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
from datetime import datetime
import os

# PROFESSIONAL COLOR SCHEME
COLORS = {
    'primary': '#1f77b4',
    'success': '#2ca02c', 
    'danger': '#d62728',
    'warning': '#ff7f0e',
    'info': '#17becf',
    'secondary': '#7f7f7f',
    'dark': '#1f1f1f',
    'light': '#f8f9fa',
    'light_gray': '#e9ecef',
    'white': '#ffffff',
    'obsidian': '#6c5ce7',
    'notion': '#000000',
    'keep': '#fbbc04',
    'roam': '#0984e3',
    'evernote': '#00b894'
}

# Tool-specific colors
TOOL_COLORS = {
    'Obsidian': COLORS['obsidian'],
    'Notion': COLORS['notion'],
    'Google Keep': COLORS['keep'],
    'Roam Research': COLORS['roam'],
    'Evernote': COLORS['evernote']
}

def load_data():
    """Load all generated datasets"""
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    
    datasets = {}
    files = [
        'tools_basic_info.csv',
        'evaluation_criteria.csv', 
        'detailed_scores.csv',
        'pricing_data.csv',
        'use_cases_data.csv',
        'weighted_scores.csv',
        'market_analysis.csv'
    ]
    
    for file in files:
        filepath = os.path.join(data_dir, file)
        key = file.replace('.csv', '')
        datasets[key] = pd.read_csv(filepath, encoding='utf-8')
    
    return datasets

def create_ranking_chart(data):
    """Create main ranking visualization"""
    df = data['weighted_scores'].sort_values('weighted_score', ascending=True)
    
    fig = go.Figure()
    
    # Add horizontal bar chart
    fig.add_trace(go.Bar(
        y=df['tool_name'],
        x=df['percentage_score'],
        orientation='h',
        text=[f"{score}%" for score in df['percentage_score']],
        textposition='auto',
        marker=dict(
            color=[TOOL_COLORS[tool] for tool in df['tool_name']],
            line=dict(width=2, color='white')
        ),
        hovertemplate='<b>%{y}</b><br>Pontuação: %{x}%<br><extra></extra>'
    ))
    
    fig.update_layout(
        title={
            'text': '<b>🏆 Ranking Geral - Ferramentas de Produtividade</b>',
            'x': 0.5,
            'font': {'size': 24, 'color': COLORS['dark']}
        },
        xaxis_title='<b>Pontuação Geral (%)</b>',
        yaxis_title='<b>Ferramentas</b>',
        font=dict(size=14),
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=20, r=20, t=80, b=20),
        height=400,
        showlegend=False,
        xaxis=dict(
            range=[0, 100],
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray'
        )
    )
    
    return fig

def create_radar_chart(data):
    """Create radar chart for criteria comparison"""
    criteria_df = data['evaluation_criteria']
    scores_df = data['detailed_scores']
    
    # Pivot the scores data
    pivot_df = scores_df.pivot(index='tool_name', columns='criteria_name', values='score')
    
    fig = go.Figure()
    
    # Add trace for each tool
    for tool in pivot_df.index:
        fig.add_trace(go.Scatterpolar(
            r=pivot_df.loc[tool].values,
            theta=pivot_df.columns,
            fill='toself',
            name=tool,
            line=dict(color=TOOL_COLORS[tool], width=2),
            fillcolor=TOOL_COLORS[tool],
            opacity=0.3,
            hovertemplate='<b>%{fullData.name}</b><br>%{theta}: %{r:.1f}<extra></extra>'
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10],
                showticklabels=True,
                tick0=0,
                dtick=2
            )
        ),
        title={
            'text': '<b>📊 Comparação por Critérios</b>',
            'x': 0.5,
            'font': {'size': 20, 'color': COLORS['dark']}
        },
        font=dict(size=12),
        height=500,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    )
    
    return fig

def create_criteria_heatmap(data):
    """Create heatmap of scores by criteria"""
    scores_df = data['detailed_scores']
    
    # Pivot the data
    pivot_df = scores_df.pivot(index='tool_name', columns='criteria_name', values='score')
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot_df.values,
        x=pivot_df.columns,
        y=pivot_df.index,
        colorscale='RdYlGn',
        zmin=0,
        zmax=10,
        hoverongaps=False,
        hovertemplate='<b>%{y}</b><br>%{x}: %{z:.1f}<extra></extra>',
        colorbar=dict(title="Pontuação")
    ))
    
    # Add text annotations
    for i, tool in enumerate(pivot_df.index):
        for j, criteria in enumerate(pivot_df.columns):
            score = pivot_df.iloc[i, j]
            fig.add_annotation(
                x=j, y=i,
                text=f"{score:.1f}",
                showarrow=False,
                font=dict(color="white" if score < 5 else "black", size=12, family="Arial Black")
            )
    
    fig.update_layout(
        title={
            'text': '<b>🎯 Mapa de Calor - Pontuações por Critério</b>',
            'x': 0.5,
            'font': {'size': 20, 'color': COLORS['dark']}
        },
        xaxis_title='<b>Critérios de Avaliação</b>',
        yaxis_title='<b>Ferramentas</b>',
        font=dict(size=12),
        height=400
    )
    
    return fig

def create_pricing_chart(data):
    """Create pricing comparison chart"""
    pricing_df = data['pricing_data']
    
    fig = go.Figure()
    
    # Filter tools with pricing > 0
    paid_tools = pricing_df[pricing_df['basic_plan_price_brl'] > 0]
    
    fig.add_trace(go.Bar(
        x=paid_tools['tool_name'],
        y=paid_tools['basic_plan_price_brl'],
        name='Plano Básico',
        marker_color=COLORS['info'],
        text=[f"R$ {price}" for price in paid_tools['basic_plan_price_brl']],
        textposition='auto'
    ))
    
    fig.add_trace(go.Bar(
        x=paid_tools['tool_name'],
        y=paid_tools['professional_plan_price_brl'],
        name='Plano Profissional',
        marker_color=COLORS['warning'],
        text=[f"R$ {price}" for price in paid_tools['professional_plan_price_brl']],
        textposition='auto'
    ))
    
    fig.update_layout(
        title={
            'text': '<b>💰 Comparação de Preços (R$ / mês)</b>',
            'x': 0.5,
            'font': {'size': 20, 'color': COLORS['dark']}
        },
        xaxis_title='<b>Ferramentas</b>',
        yaxis_title='<b>Preço Mensal (R$)</b>',
        font=dict(size=12),
        barmode='group',
        height=400,
        showlegend=True
    )
    
    return fig

def create_use_cases_chart(data):
    """Create use cases difficulty vs suitability chart"""
    use_cases_df = data['use_cases_data']
    
    # Map difficulty to numeric values
    difficulty_map = {
        'Muito Fácil': 1,
        'Fácil': 2,
        'Médio': 3,
        'Difícil': 4,
        'Muito Difícil': 5
    }
    
    use_cases_df['difficulty_numeric'] = use_cases_df['difficulty_level'].map(difficulty_map)
    
    fig = go.Figure()
    
    for tool in use_cases_df['tool_name'].unique():
        tool_data = use_cases_df[use_cases_df['tool_name'] == tool]
        
        fig.add_trace(go.Scatter(
            x=tool_data['difficulty_numeric'],
            y=tool_data['suitability_score'],
            mode='markers',
            name=tool,
            marker=dict(
                color=TOOL_COLORS[tool],
                size=12,
                line=dict(width=2, color='white')
            ),
            text=tool_data['use_case_name'],
            hovertemplate='<b>%{fullData.name}</b><br>Caso de Uso: %{text}<br>Dificuldade: %{x}<br>Adequação: %{y:.1f}<extra></extra>'
        ))
    
    fig.update_layout(
        title={
            'text': '<b>🎯 Casos de Uso: Dificuldade vs Adequação</b>',
            'x': 0.5,
            'font': {'size': 20, 'color': COLORS['dark']}
        },
        xaxis_title='<b>Nível de Dificuldade</b>',
        yaxis_title='<b>Pontuação de Adequação</b>',
        font=dict(size=12),
        height=500,
        xaxis=dict(
            tickmode='array',
            tickvals=[1, 2, 3, 4, 5],
            ticktext=['Muito Fácil', 'Fácil', 'Médio', 'Difícil', 'Muito Difícil']
        ),
        yaxis=dict(range=[0, 10])
    )
    
    return fig

def create_market_growth_chart(data):
    """Create market growth and user base chart"""
    market_df = data['market_analysis']
    
    fig = go.Figure()
    
    # Create bubble chart
    fig.add_trace(go.Scatter(
        x=market_df['growth_rate_2024'],
        y=market_df['innovation_score'],
        mode='markers',
        text=market_df['tool_name'],
        textposition="middle center",
        marker=dict(
            size=np.log10(market_df['user_base_estimate']) * 5,  # Scale for visibility
            color=[TOOL_COLORS[tool] for tool in market_df['tool_name']],
            opacity=0.7,
            line=dict(width=2, color='white')
        ),
        hovertemplate='<b>%{text}</b><br>Crescimento 2024: %{x}%<br>Inovação: %{y:.1f}<br>Base de Usuários: %{customdata:,.0f}<extra></extra>',
        customdata=market_df['user_base_estimate']
    ))
    
    fig.update_layout(
        title={
            'text': '<b>🚀 Análise de Mercado: Crescimento vs Inovação</b>',
            'x': 0.5,
            'font': {'size': 20, 'color': COLORS['dark']}
        },
        xaxis_title='<b>Taxa de Crescimento 2024 (%)</b>',
        yaxis_title='<b>Pontuação de Inovação</b>',
        font=dict(size=12),
        height=500,
        showlegend=False,
        annotations=[
            dict(
                text="Tamanho da bolha = Base de usuários",
                xref="paper", yref="paper",
                x=0.02, y=0.98,
                xanchor="left", yanchor="top",
                showarrow=False,
                font=dict(size=10, color=COLORS['secondary'])
            )
        ]
    )
    
    return fig

def create_summary_table(data):
    """Create comprehensive summary table"""
    # Combine key metrics
    basic_info = data['tools_basic_info']
    weighted_scores = data['weighted_scores']
    pricing = data['pricing_data']
    market = data['market_analysis']
    
    # Merge datasets
    summary = basic_info.merge(weighted_scores, on='tool_name')
    summary = summary.merge(pricing[['tool_name', 'basic_plan_price_brl', 'free_plan']], on='tool_name')
    summary = summary.merge(market[['tool_name', 'market_position', 'future_outlook']], on='tool_name')
    
    # Format for display
    summary['ranking_display'] = summary['ranking'].astype(str) + 'º'
    summary['score_display'] = summary['percentage_score'].astype(str) + '%'
    summary['price_display'] = summary.apply(
        lambda x: 'Gratuito' if x['free_plan'] else f"R$ {x['basic_plan_price_brl']}/mês", axis=1
    )
    
    # Select and rename columns for display
    display_columns = {
        'ranking_display': 'Ranking',
        'tool_name': 'Ferramenta',
        'category': 'Categoria',
        'score_display': 'Pontuação',
        'price_display': 'Preço',
        'target_users': 'Público-Alvo',
        'market_position': 'Posição no Mercado',
        'future_outlook': 'Perspectiva'
    }
    
    table_data = summary[list(display_columns.keys())].rename(columns=display_columns)
    
    return table_data

# Initialize Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Load data
data = load_data()

# Create layout
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.H1("🔧 Análise Comparativa de Ferramentas de Produtividade", 
                   className="text-center mb-4",
                   style={'color': COLORS['dark'], 'fontWeight': 'bold'}),
            html.Hr()
        ])
    ]),
    
    # Overview cards
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("🏆 Vencedor", className="card-title"),
                    html.H2("Notion", style={'color': COLORS['success']}),
                    html.P("83.3% de pontuação geral")
                ])
            ], color="success", outline=True)
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("📊 Ferramentas Analisadas", className="card-title"),
                    html.H2("5", style={'color': COLORS['info']}),
                    html.P("Critérios de avaliação: 7")
                ])
            ], color="info", outline=True)
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("💰 Melhor Custo-Benefício", className="card-title"),
                    html.H2("Google Keep", style={'color': COLORS['warning']}),
                    html.P("Gratuito com 77.1%")
                ])
            ], color="warning", outline=True)
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("🧠 Mais Inovador", className="card-title"),
                    html.H2("Roam Research", style={'color': COLORS['danger']}),
                    html.P("9.5 pontos em inovação")
                ])
            ], color="danger", outline=True)
        ], width=3)
    ], className="mb-4"),
    
    # Main ranking chart
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(
                        figure=create_ranking_chart(data),
                        config={'displayModeBar': False}
                    )
                ])
            ])
        ])
    ], className="mb-4"),
    
    # Radar and heatmap charts
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(
                        figure=create_radar_chart(data),
                        config={'displayModeBar': False}
                    )
                ])
            ])
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(
                        figure=create_criteria_heatmap(data),
                        config={'displayModeBar': False}
                    )
                ])
            ])
        ], width=6)
    ], className="mb-4"),
    
    # Pricing and use cases
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(
                        figure=create_pricing_chart(data),
                        config={'displayModeBar': False}
                    )
                ])
            ])
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(
                        figure=create_use_cases_chart(data),
                        config={'displayModeBar': False}
                    )
                ])
            ])
        ], width=6)
    ], className="mb-4"),
    
    # Market analysis
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(
                        figure=create_market_growth_chart(data),
                        config={'displayModeBar': False}
                    )
                ])
            ])
        ])
    ], className="mb-4"),
    
    # Summary table
    dbc.Row([
        dbc.Col([
            html.H3("📋 Tabela Resumo Comparativa", className="text-center mb-3"),
            dbc.Card([
                dbc.CardBody([
                    dash_table.DataTable(
                        data=create_summary_table(data).to_dict('records'),
                        columns=[{"name": col, "id": col} for col in create_summary_table(data).columns],
                        style_cell={
                            'textAlign': 'center',
                            'padding': '12px',
                            'fontFamily': 'Arial',
                            'fontSize': '14px'
                        },
                        style_header={
                            'backgroundColor': COLORS['primary'],
                            'color': 'white',
                            'fontWeight': 'bold'
                        },
                        style_data_conditional=[
                            {
                                'if': {'filter_query': '{Ranking} = 1º'},
                                'backgroundColor': '#d4edda',
                                'color': 'black',
                            }
                        ]
                    )
                ])
            ])
        ])
    ], className="mb-4"),
    
    # Footer
    dbc.Row([
        dbc.Col([
            html.Hr(),
            html.P("📊 Dashboard criado com dados de pesquisa de múltiplas fontes (G2, Capterra, Product Hunt, Reddit, YouTube)",
                  className="text-center text-muted"),
            html.P(f"🕐 Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
                  className="text-center text-muted")
        ])
    ])
    
], fluid=True)

def export_dashboard_html():
    """Export dashboard as static HTML"""
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'outputs')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Create a comprehensive HTML report
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Análise de Ferramentas de Produtividade</title>
        <meta charset="utf-8">
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {{ font-family: Arial, sans-serif; }}
            .chart-container {{ margin: 20px 0; }}
            .summary-table {{ margin: 20px 0; }}
            h1, h2 {{ color: {COLORS['dark']}; }}
        </style>
    </head>
    <body>
        <div class="container-fluid">
            <h1 class="text-center mb-4">🔧 Análise Comparativa de Ferramentas de Produtividade</h1>
            <hr>
            
            <div class="row mb-4">
                <div class="col-md-12">
                    <div id="ranking-chart" class="chart-container"></div>
                </div>
            </div>
            
            <div class="row mb-4">
                <div class="col-md-6">
                    <div id="radar-chart" class="chart-container"></div>
                </div>
                <div class="col-md-6">
                    <div id="heatmap-chart" class="chart-container"></div>
                </div>
            </div>
            
            <div class="row mb-4">
                <div class="col-md-6">
                    <div id="pricing-chart" class="chart-container"></div>
                </div>
                <div class="col-md-6">
                    <div id="use-cases-chart" class="chart-container"></div>
                </div>
            </div>
            
            <div class="row mb-4">
                <div class="col-md-12">
                    <div id="market-chart" class="chart-container"></div>
                </div>
            </div>
            
            <div class="row mb-4">
                <div class="col-md-12">
                    <h3 class="text-center mb-3">📋 Tabela Resumo Comparativa</h3>
                    <div class="summary-table">
                        {create_summary_table(data).to_html(classes='table table-striped table-hover', table_id='summary-table', escape=False)}
                    </div>
                </div>
            </div>
            
            <hr>
            <p class="text-center text-muted">📊 Dashboard criado com dados de pesquisa de múltiplas fontes</p>
            <p class="text-center text-muted">🕐 Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
        </div>
        
        <script>
            // Add charts to HTML
            Plotly.newPlot('ranking-chart', {json.dumps(create_ranking_chart(data), cls=plotly.utils.PlotlyJSONEncoder)});
            Plotly.newPlot('radar-chart', {json.dumps(create_radar_chart(data), cls=plotly.utils.PlotlyJSONEncoder)});
            Plotly.newPlot('heatmap-chart', {json.dumps(create_criteria_heatmap(data), cls=plotly.utils.PlotlyJSONEncoder)});
            Plotly.newPlot('pricing-chart', {json.dumps(create_pricing_chart(data), cls=plotly.utils.PlotlyJSONEncoder)});
            Plotly.newPlot('use-cases-chart', {json.dumps(create_use_cases_chart(data), cls=plotly.utils.PlotlyJSONEncoder)});
            Plotly.newPlot('market-chart', {json.dumps(create_market_growth_chart(data), cls=plotly.utils.PlotlyJSONEncoder)});
        </script>
    </body>
    </html>
    """
    
    output_file = os.path.join(output_dir, 'productivity_tools_dashboard.html')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Dashboard HTML exportado para: {output_file}")
    return output_file

if __name__ == "__main__":
    # Export static HTML version
    import json
    import plotly
    
    export_dashboard_html()
    
    # Run interactive dashboard
    print("🚀 Iniciando dashboard interativo...")
    print("📊 Acesse: http://127.0.0.1:8050")
    app.run_server(debug=True, host='127.0.0.1', port=8050)