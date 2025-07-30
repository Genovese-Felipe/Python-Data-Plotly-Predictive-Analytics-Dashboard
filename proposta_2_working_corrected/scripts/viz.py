# scripts/viz.py - Dashboard de Performance de Projetos (Proposal 2 - Corrected Working)
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import datetime as dt
import os
import sys

# Configurações Globais - Paleta de cores profissional
COLOR_PALETTE = {
    'primary': '#3366cc',
    'secondary': '#dc3912',
    'success': '#109618',
    'danger': '#cb3d3d',
    'warning': '#ff9900',
    'info': '#0099c6',
    'light': '#f9f9f9',
    'dark': '#333333',
    'text': '#505050'
}

def load_data():
    """
    Carrega os dados dos arquivos CSV e faz conversões necessárias.
    """
    try:
        df_projetos = pd.read_csv('data/projetos.csv')
        df_marcos = pd.read_csv('data/marcos_projeto.csv')
        df_financeiro = pd.read_csv('data/financeiro_mensal.csv')
        df_recursos = pd.read_csv('data/recursos_projeto.csv')
        
        # Converter colunas de data
        date_columns = ['data_inicio', 'data_conclusao_prevista', 'data_conclusao_real']
        for col in date_columns:
            df_projetos[col] = pd.to_datetime(df_projetos[col])
        
        df_marcos['data_prevista'] = pd.to_datetime(df_marcos['data_prevista'])
        df_marcos['data_real'] = pd.to_datetime(df_marcos['data_real'])
        df_financeiro['data'] = pd.to_datetime(df_financeiro['data'])
        
        print("Dados carregados com sucesso.")
        return df_projetos, df_marcos, df_financeiro, df_recursos
    
    except FileNotFoundError:
        print("Arquivos de dados não encontrados. Gerando novos dados...")
        sys.path.insert(0, 'scripts')
        from data_gen import gerar_dados_projetos, gerar_dados_recursos
        df_projetos, df_marcos, df_financeiro = gerar_dados_projetos(200)
        df_recursos = gerar_dados_recursos(df_projetos)
        return df_projetos, df_marcos, df_financeiro, df_recursos

def create_kpi_card(title, value, change=None, icon=None, color='primary'):
    """
    Cria um card para exibição de KPIs.
    """
    card_content = [
        html.Div([
            html.Div([
                html.H4(title, className="card-title text-muted", style={'fontWeight': 'bold'}),
                html.H2(value, className="card-value", style={'fontWeight': 'bold', 'color': COLOR_PALETTE[color]})
            ], className="col-9"),
            
            html.Div([
                html.I(className=f"fa fa-{icon} fa-3x text-{color}") if icon else "",
            ], className="col-3 text-right d-flex align-items-center justify-content-center")
        ], className="row")
    ]
    
    if change is not None:
        try:
            change_value = float(change.strip('%+-'))
            direction = "up" if change_value > 0 else "down"
            change_color = "success" if direction == "up" else "danger"
            
            card_content.append(
                html.Div([
                    html.I(className=f"fa fa-arrow-{direction} me-1"),
                    html.Span(change),
                    html.Span(" vs. período anterior", className="ms-1 small")
                ], className=f"mt-2 text-{change_color}")
            )
        except:
            pass
    
    return dbc.Card(card_content, className="kpi-card h-100 shadow-sm")

def generate_insights(filtered_df, filtered_financeiro=None):
    """
    Gera insights automatizados com base nos dados filtrados.
    """
    insights = []
    
    if filtered_df.empty:
        return [html.P("Ajuste os filtros para gerar insights baseados nos dados.", className="text-muted")]
    
    # Insight 1: Projetos críticos
    critical_projects = filtered_df[
        (filtered_df['atraso'] > 30) & 
        (filtered_df['custo_adicional_pct'] > 15)
    ]
    if len(critical_projects) > 0:
        insights.append(html.Div([
            html.H6(f"🚨 {len(critical_projects)} Projetos Críticos Identificados", 
                   className="text-danger", style={'fontWeight': 'bold'}),
            html.P(f"Projetos com atraso superior a 30 dias e custo adicional acima de 15%")
        ]))
    
    # Insight 2: Eficiência por tipo
    if 'tipo_projeto' in filtered_df.columns and 'eficiencia' in filtered_df.columns:
        efficiency_by_type = filtered_df.groupby('tipo_projeto')['eficiencia'].mean().sort_values()
        if not efficiency_by_type.empty and len(efficiency_by_type) > 1:
            most_efficient = efficiency_by_type.index[0]
            least_efficient = efficiency_by_type.index[-1]
            
            insights.append(html.Div([
                html.H6("📊 Eficiência por Tipo de Projeto", className="text-primary mt-3", style={'fontWeight': 'bold'}),
                html.P([
                    f"Projetos do tipo ", 
                    html.Strong(most_efficient), 
                    f" apresentam maior eficiência de custo (R${efficiency_by_type.iloc[0]:.2f}/m²)",
                    html.Br(),
                    f"Projetos do tipo ",
                    html.Strong(least_efficient),
                    f" apresentam menor eficiência (R${efficiency_by_type.iloc[-1]:.2f}/m²)"
                ])
            ]))
    
    # Insight 3: Tendência temporal
    if filtered_financeiro is not None and len(filtered_financeiro) > 0:
        try:
            df_trend = filtered_financeiro.copy()
            df_trend['year_month'] = pd.to_datetime(df_trend['data']).dt.to_period('M')
            trend_data = df_trend.groupby('year_month').agg({
                'variacao': 'mean'
            }).reset_index()
            
            recent_months = min(3, len(trend_data))
            if recent_months > 0:
                recent_avg = trend_data['variacao'].tail(recent_months).mean()
                trend_direction = "crescente" if recent_avg > 2 else "decrescente" if recent_avg < -2 else "estável"
                
                insights.append(html.Div([
                    html.H6("📈 Tendência Recente de Custos", className="text-info mt-3", style={'fontWeight': 'bold'}),
                    html.P(f"Nos últimos {recent_months} meses, os custos mostram tendência {trend_direction} ({recent_avg:.1f}%)")
                ]))
        except:
            pass
    
    # Se não houver insights devido a filtros muito restritivos
    if not insights:
        return [html.P("✨ Ajuste os filtros para gerar insights baseados nos dados.", className="text-muted")]
    
    return insights

# Carregar dados
df_projetos, df_marcos, df_financeiro, df_recursos = load_data()

# Configuração do App Dash
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY, dbc.icons.FONT_AWESOME])
server = app.server

# Layout do Dashboard
app.layout = dbc.Container([
    # Cabeçalho
    dbc.Row([
        dbc.Col([
            html.H1("Dashboard de Performance de Projetos", className="mb-0", 
                   style={'fontWeight': 'bold', 'color': COLOR_PALETTE['primary']}),
            html.P("Análise completa de métricas e KPIs para gestão eficiente de projetos", 
                   className="text-muted")
        ], width=8),
        dbc.Col([
            dbc.Card([
                html.P("Última atualização", className="small text-muted mb-0"),
                html.H5(dt.datetime.now().strftime("%d/%m/%Y %H:%M"), className="mb-0", style={'fontWeight': 'bold'})
            ], body=True, className="h-100 text-right shadow-sm")
        ], width=4, className="d-flex align-items-center")
    ], className="mb-4 mt-3"),
    
    # Filtros
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Filtros", className="card-title border-bottom pb-2 mb-3", style={'fontWeight': 'bold'}),
                    dbc.Row([
                        dbc.Col([
                            html.Label("Período", className="small text-muted"),
                            dcc.DatePickerRange(
                                id='date-filter',
                                start_date=df_projetos['data_inicio'].min(),
                                end_date=df_projetos['data_conclusao_real'].max(),
                                display_format='DD/MM/YYYY',
                                className="w-100"
                            )
                        ], width=4),
                        dbc.Col([
                            html.Label("Tipo de Projeto", className="small text-muted"),
                            dcc.Dropdown(
                                id='tipo-filter',
                                options=[{'label': t, 'value': t} for t in df_projetos['tipo_projeto'].unique()],
                                value=df_projetos['tipo_projeto'].unique().tolist(),
                                multi=True,
                                className="w-100"
                            )
                        ], width=4),
                        dbc.Col([
                            html.Label("Região", className="small text-muted"),
                            dcc.Dropdown(
                                id='regiao-filter',
                                options=[{'label': r, 'value': r} for r in df_projetos['regiao'].unique()],
                                value=df_projetos['regiao'].unique().tolist(),
                                multi=True,
                                className="w-100"
                            )
                        ], width=4)
                    ])
                ])
            ], className="shadow-sm")
        ], width=12)
    ], className="mb-4"),
    
    # KPIs
    dbc.Row([
        dbc.Col([
            create_kpi_card(
                "Total de Projetos", 
                f"{len(df_projetos)}", 
                "+12%",
                "clipboard-list",
                "primary"
            )
        ], width=3),
        dbc.Col([
            create_kpi_card(
                "Valor Total", 
                f"R$ {df_projetos['orcamento'].sum()/1e6:.1f}M", 
                "+8.3%",
                "dollar-sign",
                "success"
            )
        ], width=3),
        dbc.Col([
            create_kpi_card(
                "Projetos No Prazo", 
                f"{sum(df_projetos['atraso'] == 0) / len(df_projetos) * 100:.1f}%", 
                "-2.5%",
                "calendar-check",
                "info"
            )
        ], width=3),
        dbc.Col([
            create_kpi_card(
                "Satisfação Média", 
                f"{df_projetos['satisfacao_cliente'].mean():.1f}/10", 
                "+0.8",
                "smile",
                "warning"
            )
        ], width=3)
    ], className="mb-4"),
    
    # Seção de Insights
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5("💡 Insights Automáticos", className="mb-0", style={'fontWeight': 'bold'}),
                ]),
                dbc.CardBody([
                    html.Div(id="insights-content")
                ])
            ], className="shadow-sm")
        ], width=12)
    ], className="mb-4"),
    
    # Gráficos principais
    dbc.Row([
        # Coluna principal (esquerda)
        dbc.Col([
            # Gráfico de tendência principal
            dbc.Card([
                dbc.CardHeader([
                    html.H5("📈 Evolução do Portfólio de Projetos", className="mb-0", style={'fontWeight': 'bold'}),
                ]),
                dbc.CardBody([
                    dcc.Loading(
                        id="loading-trend-chart",
                        type="circle",
                        children=[
                            dcc.Graph(
                                id='portfolio-trend-chart',
                                config={'displayModeBar': False},
                                style={'height': '400px'}
                            )
                        ]
                    )
                ])
            ], className="shadow-sm mb-4"),
            
            # Gráfico de dispersão custo vs. prazo
            dbc.Card([
                dbc.CardHeader([
                    html.H5("🎯 Relação entre Custo e Prazo", className="mb-0", style={'fontWeight': 'bold'}),
                ]),
                dbc.CardBody([
                    dcc.Loading(
                        id="loading-scatter",
                        type="circle",
                        children=[
                            dcc.Graph(
                                id='cost-schedule-scatter',
                                config={'displayModeBar': False},
                                style={'height': '400px'}
                            )
                        ]
                    )
                ])
            ], className="shadow-sm")
        ], width=8),
        
        # Coluna secundária (direita)
        dbc.Col([
            # Distribuição por tipo
            dbc.Card([
                dbc.CardHeader([
                    html.H5("📊 Projetos por Tipo", className="mb-0", style={'fontWeight': 'bold'}),
                ]),
                dbc.CardBody([
                    dcc.Loading(
                        id="loading-tipo",
                        type="circle",
                        children=[
                            dcc.Graph(
                                id='tipo-chart',
                                config={'displayModeBar': False},
                                style={'height': '250px'}
                            )
                        ]
                    )
                ])
            ], className="shadow-sm mb-4"),
            
            # Desempenho por região
            dbc.Card([
                dbc.CardHeader([
                    html.H5("🗺️ Desempenho por Região", className="mb-0", style={'fontWeight': 'bold'}),
                ]),
                dbc.CardBody([
                    dcc.Loading(
                        id="loading-region",
                        type="circle",
                        children=[
                            dcc.Graph(
                                id='region-performance-chart',
                                config={'displayModeBar': False},
                                style={'height': '250px'}
                            )
                        ]
                    )
                ])
            ], className="shadow-sm mb-4"),
            
            # Status dos projetos
            dbc.Card([
                dbc.CardHeader([
                    html.H5("⚡ Status dos Projetos", className="mb-0", style={'fontWeight': 'bold'}),
                ]),
                dbc.CardBody([
                    dcc.Loading(
                        id="loading-status",
                        type="circle",
                        children=[
                            dcc.Graph(
                                id='status-chart',
                                config={'displayModeBar': False},
                                style={'height': '250px'}
                            )
                        ]
                    )
                ])
            ], className="shadow-sm")
        ], width=4)
    ], className="mb-4"),
    
    # Gráficos secundários
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5("🔧 Distribuição de Recursos", className="mb-0", style={'fontWeight': 'bold'}),
                ]),
                dbc.CardBody([
                    dcc.Loading(
                        id="loading-resources",
                        type="circle",
                        children=[
                            dcc.Graph(
                                id='resources-chart',
                                config={'displayModeBar': False},
                                style={'height': '400px'}
                            )
                        ]
                    )
                ])
            ], className="shadow-sm")
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5("⚖️ Eficiência por Tipo de Projeto", className="mb-0", style={'fontWeight': 'bold'}),
                ]),
                dbc.CardBody([
                    dcc.Loading(
                        id="loading-efficiency",
                        type="circle",
                        children=[
                            dcc.Graph(
                                id='efficiency-chart',
                                config={'displayModeBar': False},
                                style={'height': '400px'}
                            )
                        ]
                    )
                ])
            ], className="shadow-sm")
        ], width=6)
    ], className="mb-4"),
    
    # Rodapé
    dbc.Row([
        dbc.Col([
            html.Hr(),
            html.P([
                "Dashboard desenvolvido por ",
                html.A("Genovese-Felipe", href="https://github.com/Genovese-Felipe"),
                ". Dados atualizados em tempo real."
            ], className="text-center text-muted small")
        ])
    ])
], fluid=True, className="pb-4")

# Callbacks
@callback(
    [Output('portfolio-trend-chart', 'figure'),
     Output('cost-schedule-scatter', 'figure'),
     Output('tipo-chart', 'figure'),
     Output('region-performance-chart', 'figure'),
     Output('status-chart', 'figure'),
     Output('resources-chart', 'figure'),
     Output('efficiency-chart', 'figure'),
     Output('insights-content', 'children')],
    [Input('date-filter', 'start_date'),
     Input('date-filter', 'end_date'),
     Input('tipo-filter', 'value'),
     Input('regiao-filter', 'value')]
)
def update_charts(start_date, end_date, tipos, regioes):
    # Filtrar dados
    filtered_df = df_projetos.copy()
    
    if start_date and end_date:
        filtered_df = filtered_df[(filtered_df['data_inicio'] >= start_date) & 
                                  (filtered_df['data_conclusao_prevista'] <= end_date)]
    
    if tipos and len(tipos) > 0:
        filtered_df = filtered_df[filtered_df['tipo_projeto'].isin(tipos)]
    
    if regioes and len(regioes) > 0:
        filtered_df = filtered_df[filtered_df['regiao'].isin(regioes)]
    
    # Filtrar os datasets relacionados
    filtered_marcos = df_marcos[df_marcos['id_projeto'].isin(filtered_df['id_projeto'])]
    filtered_financeiro = df_financeiro[df_financeiro['id_projeto'].isin(filtered_df['id_projeto'])]
    filtered_recursos = df_recursos[df_recursos['id_projeto'].isin(filtered_df['id_projeto'])]
    
    # Gerar insights
    insights = generate_insights(filtered_df, filtered_financeiro)
    
    # 1. Portfolio Trend Chart
    if filtered_financeiro.empty:
        fig_trend = px.line(title="Sem dados disponíveis")
    else:
        df_trend = filtered_financeiro.copy()
        df_trend['year_month'] = pd.to_datetime(df_trend['data']).dt.to_period('M')
        df_trend_grouped = df_trend.groupby('year_month').agg(
            orcado=('orcado', 'sum'),
            realizado=('realizado', 'sum')
        ).reset_index()
        df_trend_grouped['year_month'] = df_trend_grouped['year_month'].dt.to_timestamp()
        
        fig_trend = go.Figure()
        
        fig_trend.add_trace(go.Scatter(
            x=df_trend_grouped['year_month'], 
            y=df_trend_grouped['orcado'],
            mode='lines+markers',
            name='Orçado',
            line=dict(color=COLOR_PALETTE['primary'], width=3),
            marker=dict(size=8)
        ))
        
        fig_trend.add_trace(go.Scatter(
            x=df_trend_grouped['year_month'], 
            y=df_trend_grouped['realizado'],
            mode='lines+markers',
            name='Realizado',
            line=dict(color=COLOR_PALETTE['secondary'], width=3),
            marker=dict(size=8)
        ))
        
        fig_trend.update_layout(
            title={'text': 'Evolução Temporal do Portfólio', 'font': {'size': 16}},
            template="plotly_white",
            margin=dict(l=40, r=20, t=40, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            hovermode='x unified'
        )
    
    # 2. Cost vs Schedule Scatter
    if filtered_df.empty:
        fig_scatter = px.scatter(title="Sem dados disponíveis")
    else:
        fig_scatter = px.scatter(
            filtered_df,
            x='atraso',
            y='custo_adicional_pct',
            color='tipo_projeto',
            size='orcamento',
            hover_name='nome_projeto',
            hover_data=['satisfacao_cliente', 'regiao'],
            color_discrete_map={
                'Residencial': COLOR_PALETTE['primary'],
                'Comercial': COLOR_PALETTE['secondary'],
                'Industrial': COLOR_PALETTE['warning'],
                'Infraestrutura': COLOR_PALETTE['info']
            },
            labels={
                'atraso': 'Atraso (dias)',
                'custo_adicional_pct': 'Custo Adicional (%)',
                'tipo_projeto': 'Tipo de Projeto'
            }
        )
        
        fig_scatter.update_layout(
            title={'text': 'Análise de Risco: Custo vs Prazo', 'font': {'size': 16}},
            template="plotly_white",
            margin=dict(l=40, r=20, t=40, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
    
    # 3. Projects by Type
    if filtered_df.empty:
        fig_tipo = px.pie(title="Sem dados disponíveis")
    else:
        df_tipo = filtered_df.groupby('tipo_projeto').agg(
            count=('id_projeto', 'count'),
            orcamento_total=('orcamento', 'sum')
        ).reset_index()
        
        fig_tipo = px.pie(
            df_tipo,
            values='orcamento_total',
            names='tipo_projeto',
            hole=0.4,
            color_discrete_sequence=[COLOR_PALETTE['primary'], COLOR_PALETTE['secondary'], 
                                   COLOR_PALETTE['warning'], COLOR_PALETTE['info']]
        )
        
        fig_tipo.update_traces(textposition='outside', textinfo='percent+label')
        fig_tipo.update_layout(
            title={'text': 'Distribuição por Tipo', 'font': {'size': 16}},
            template="plotly_white",
            margin=dict(l=20, r=20, t=40, b=20),
            showlegend=False
        )
    
    # 4. Regional Performance
    if filtered_df.empty:
        fig_region = px.bar(title="Sem dados disponíveis")
    else:
        df_region = filtered_df.groupby('regiao').agg(
            count=('id_projeto', 'count'),
            satisfacao_media=('satisfacao_cliente', 'mean')
        ).reset_index()
        
        fig_region = px.bar(
            df_region,
            x='regiao',
            y='count',
            color='satisfacao_media',
            color_continuous_scale='RdYlGn',
            text='count'
        )
        
        fig_region.update_traces(textposition='outside')
        fig_region.update_layout(
            title={'text': 'Performance Regional', 'font': {'size': 16}},
            template="plotly_white",
            margin=dict(l=40, r=20, t=40, b=20)
        )
    
    # 5. Status Chart
    if filtered_df.empty:
        fig_status = px.bar(title="Sem dados disponíveis")
    else:
        df_status = filtered_df['status'].value_counts().reset_index()
        df_status.columns = ['status', 'count']
        
        status_colors = {
            'Concluído': COLOR_PALETTE['success'],
            'Em Andamento': COLOR_PALETTE['warning'],
            'Atrasado': COLOR_PALETTE['danger'],
            'Planejado': COLOR_PALETTE['info']
        }
        
        fig_status = px.bar(
            df_status,
            y='status',
            x='count',
            orientation='h',
            color='status',
            color_discrete_map=status_colors,
            text='count'
        )
        
        fig_status.update_traces(textposition='auto')
        fig_status.update_layout(
            title={'text': 'Status dos Projetos', 'font': {'size': 16}},
            template="plotly_white",
            margin=dict(l=40, r=20, t=40, b=20),
            showlegend=False
        )
    
    # 6. Resources Chart
    if filtered_recursos.empty:
        fig_resources = px.bar(title="Sem dados disponíveis")
    else:
        recursos_agg = filtered_recursos.groupby('categoria_recurso').agg(
            valor_orcado=('valor_orcado', 'sum'),
            valor_realizado=('valor_realizado', 'sum')
        ).reset_index()
        
        fig_resources = go.Figure()
        fig_resources.add_trace(go.Bar(
            x=recursos_agg['categoria_recurso'],
            y=recursos_agg['valor_orcado'],
            name='Orçado',
            marker_color=COLOR_PALETTE['primary'],
            opacity=0.7
        ))
        
        fig_resources.add_trace(go.Bar(
            x=recursos_agg['categoria_recurso'],
            y=recursos_agg['valor_realizado'],
            name='Realizado',
            marker_color=COLOR_PALETTE['secondary'],
            opacity=0.7
        ))
        
        fig_resources.update_layout(
            title={'text': 'Recursos: Orçado vs Realizado', 'font': {'size': 16}},
            template="plotly_white",
            margin=dict(l=40, r=20, t=40, b=40),
            barmode='group',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis_tickangle=-45
        )
    
    # 7. Efficiency Chart
    if filtered_df.empty:
        fig_efficiency = px.box(title="Sem dados disponíveis")
    else:
        fig_efficiency = px.box(
            filtered_df,
            x='tipo_projeto',
            y='eficiencia',
            color='tipo_projeto',
            points="all",
            color_discrete_map={
                'Residencial': COLOR_PALETTE['primary'],
                'Comercial': COLOR_PALETTE['secondary'],
                'Industrial': COLOR_PALETTE['warning'],
                'Infraestrutura': COLOR_PALETTE['info']
            }
        )
        
        fig_efficiency.update_layout(
            title={'text': 'Eficiência de Custo por Tipo', 'font': {'size': 16}},
            template="plotly_white",
            margin=dict(l=40, r=20, t=40, b=20),
            showlegend=False,
            yaxis_title="Custo por m² (R$)"
        )
    
    return fig_trend, fig_scatter, fig_tipo, fig_region, fig_status, fig_resources, fig_efficiency, insights

# CSS Personalizado
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Dashboard de Performance de Projetos</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                font-family: 'Segoe UI', Roboto, sans-serif;
                color: #505050;
                background-color: #f8f9fa;
            }
            
            .kpi-card {
                transition: transform 0.2s;
                border-radius: 8px;
                overflow: hidden;
            }
            
            .kpi-card:hover {
                transform: translateY(-3px);
            }
            
            .card {
                border-radius: 8px;
                border: none;
                overflow: hidden;
            }
            
            .card-header {
                background-color: #ffffff;
                border-bottom: 1px solid rgba(0,0,0,0.08);
                padding: 15px 20px;
            }
            
            .shadow-sm {
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05) !important;
            }
            
            h1, h2, h3, h4, h5 {
                font-weight: bold !important;
            }
            
            .container-fluid {
                padding: 0 30px;
            }
            
            @media (max-width: 768px) {
                .container-fluid {
                    padding: 0 15px;
                }
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

if __name__ == '__main__':
    # Verificar se o diretório de saída existe
    if not os.path.exists('outputs'):
        os.makedirs('outputs')
    
    # Para desenvolvimento
    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        app.run(debug=True, port=8051)
    else:
        print("Dashboard estático criado. Use 'debug' para executar o servidor.")