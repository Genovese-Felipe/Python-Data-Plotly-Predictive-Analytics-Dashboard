import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os

# Importar funções de gráficos
from charts import (
    create_sunburst_chart, 
    create_bubble_chart, 
    create_area_chart, 
    create_stacked_bar_chart, 
    create_flow_chart, 
    create_map_chart
)

# Carregar dados
@callback(
    Output('data-store', 'data'),
    Input('data-store', 'id')
)
def load_data(_):
    """Carrega todos os dados necessários"""
    try:
        sales_df = pd.read_csv('/home/ubuntu/dashboard-dash-analytics/src/data/sales_data.csv')
        funnel_df = pd.read_csv('/home/ubuntu/dashboard-dash-analytics/src/data/funnel_data.csv')
        sources_df = pd.read_csv('/home/ubuntu/dashboard-dash-analytics/src/data/lead_sources.csv')
        products_df = pd.read_csv('/home/ubuntu/dashboard-dash-analytics/src/data/product_performance.csv')
        
        return {
            'sales': sales_df.to_dict('records'),
            'funnel': funnel_df.to_dict('records'),
            'sources': sources_df.to_dict('records'),
            'products': products_df.to_dict('records')
        }
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        return {}

# Inicializar a aplicação Dash
app = dash.Dash(__name__, external_stylesheets=['/assets/style.css'])
server = app.server

# Configurar o layout responsivo
app.layout = html.Div([
    # Store para dados
    dcc.Store(id='data-store'),
    
    # Header
    html.Div([
        html.Div([
            html.H1("Dashboard Analytics", className="header-title"),
            html.P("Visualização Interativa de Dados Empresariais", className="header-subtitle"),
        ]),
        html.Div([
            html.Span("⚡ Tempo Real", className="badge"),
            html.Button("Exportar Dados", className="export-btn")
        ], className="header-actions")
    ], className="header"),
    
    # Filtros Globais
    html.Div([
        html.Div([
            html.Label("Filtrar por Departamento:", className="filter-label"),
            dcc.Dropdown(
                id='department-filter',
                options=[
                    {'label': 'Todos', 'value': 'all'},
                    {'label': 'Vendas', 'value': 'sales'},
                    {'label': 'Marketing', 'value': 'marketing'},
                    {'label': 'Operações', 'value': 'operations'},
                    {'label': 'Financeiro', 'value': 'finance'}
                ],
                value='all',
                className="filter-dropdown"
            )
        ]),
        html.Div([
            html.Label("Período:", className="filter-label"),
            dcc.DatePickerRange(
                id='date-range',
                start_date=datetime.now() - timedelta(days=365),
                end_date=datetime.now(),
                className="date-picker"
            )
        ])
    ], className="filters-container"),
    
    # KPIs
    html.Div([
        html.Div([
            html.H3(id="kpi-revenue", className="kpi-value"),
            html.P("Receita Total", className="kpi-label"),
            html.P(id="kpi-revenue-change", className="kpi-change positive")
        ], className="kpi-card kpi-blue"),
        
        html.Div([
            html.H3(id="kpi-customers", className="kpi-value"),
            html.P("Novos Clientes", className="kpi-label"),
            html.P(id="kpi-customers-change", className="kpi-change positive")
        ], className="kpi-card kpi-green"),
        
        html.Div([
            html.H3(id="kpi-conversion", className="kpi-value"),
            html.P("Taxa de Conversão", className="kpi-label"),
            html.P(id="kpi-conversion-change", className="kpi-change positive")
        ], className="kpi-card kpi-purple"),
        
        html.Div([
            html.H3(id="kpi-ticket", className="kpi-value"),
            html.P("Ticket Médio", className="kpi-label"),
            html.P(id="kpi-ticket-change", className="kpi-change positive")
        ], className="kpi-card kpi-orange")
    ], className="kpis-container"),
    
    # Grid de Gráficos
    html.Div([
        # Linha 1: Sunburst + Area Chart
        html.Div([
            html.Div([
                html.H3("Hierarquia de Vendas por Categoria", className="chart-title"),
                html.P("Distribuição hierárquica das vendas por categoria e subcategoria", className="chart-subtitle"),
                dcc.Graph(id='sunburst-chart', className="chart")
            ], className="chart-container"),
            
            html.Div([
                html.H3("Tendências de Receita", className="chart-title"),
                html.P("Evolução da receita ao longo dos últimos 12 meses", className="chart-subtitle"),
                dcc.Graph(id='area-chart', className="chart")
            ], className="chart-container")
        ], className="chart-row"),
        
        # Linha 2: Bubble Chart + Map
        html.Div([
            html.Div([
                html.H3("Análise de Performance por Produto", className="chart-title"),
                html.P("Relação entre volume de vendas, margem de lucro e satisfação do cliente", className="chart-subtitle"),
                dcc.Graph(id='bubble-chart', className="chart")
            ], className="chart-container"),
            
            html.Div([
                html.H3("Distribuição Geográfica", className="chart-title"),
                html.P("Vendas por região do Brasil", className="chart-subtitle"),
                dcc.Graph(id='map-chart', className="chart")
            ], className="chart-container")
        ], className="chart-row"),
        
        # Linha 3: Stacked Bar + Flow Chart
        html.Div([
            html.Div([
                html.H3("Vendas por Canal e Período", className="chart-title"),
                html.P("Comparação de vendas por canal de distribuição ao longo do tempo", className="chart-subtitle"),
                dcc.Graph(id='stacked-bar-chart', className="chart")
            ], className="chart-container"),
            
            html.Div([
                html.H3("Fluxo de Conversão", className="chart-title"),
                html.P("Jornada do cliente desde o primeiro contato até a compra", className="chart-subtitle"),
                dcc.Graph(id='flow-chart', className="chart")
            ], className="chart-container")
        ], className="chart-row")
    ], className="charts-grid")
], className="dashboard-container")

# Callbacks para atualizar KPIs
@callback(
    [Output('kpi-revenue', 'children'),
     Output('kpi-revenue-change', 'children'),
     Output('kpi-customers', 'children'),
     Output('kpi-customers-change', 'children'),
     Output('kpi-conversion', 'children'),
     Output('kpi-conversion-change', 'children'),
     Output('kpi-ticket', 'children'),
     Output('kpi-ticket-change', 'children')],
    [Input('data-store', 'data'),
     Input('department-filter', 'value'),
     Input('date-range', 'start_date'),
     Input('date-range', 'end_date')]
)
def update_kpis(data, department_filter, start_date, end_date):
    """Atualiza os KPIs baseado nos filtros"""
    if not data or 'sales' not in data:
        return "R$ 0", "0%", "0", "0%", "0%", "0%", "R$ 0", "0%"
    
    sales_df = pd.DataFrame(data['sales'])
    
    # Filtrar por data
    if start_date and end_date:
        sales_df['date'] = pd.to_datetime(sales_df['date'])
        sales_df = sales_df[
            (sales_df['date'] >= start_date) & 
            (sales_df['date'] <= end_date)
        ]
    
    # Filtrar por departamento
    if department_filter != 'all':
        dept_mapping = {
            'sales': ['Eletrônicos', 'Roupas'],
            'marketing': ['Casa & Jardim', 'Livros'],
            'operations': ['Esportes'],
            'finance': ['Eletrônicos', 'Casa & Jardim']
        }
        if department_filter in dept_mapping:
            sales_df = sales_df[sales_df['category'].isin(dept_mapping[department_filter])]
    
    # Calcular KPIs
    total_revenue = sales_df['total_revenue'].sum()
    total_customers = sales_df['quantity'].sum()  # Aproximação
    avg_ticket = total_revenue / total_customers if total_customers > 0 else 0
    conversion_rate = 3.2  # Valor fixo para demonstração
    
    # Formatação
    revenue_formatted = f"R$ {total_revenue/1000000:.1f}M" if total_revenue >= 1000000 else f"R$ {total_revenue/1000:.0f}K"
    customers_formatted = f"{total_customers:,.0f}".replace(',', '.')
    conversion_formatted = f"{conversion_rate:.1f}%"
    ticket_formatted = f"R$ {avg_ticket:.0f}"
    
    return (
        revenue_formatted, "↗ +12% vs mês anterior",
        customers_formatted, "↗ +8% vs mês anterior", 
        conversion_formatted, "↗ +0.4% vs mês anterior",
        ticket_formatted, "↗ +5% vs mês anterior"
    )

# Callbacks para gráficos
@callback(
    Output('sunburst-chart', 'figure'),
    [Input('data-store', 'data'),
     Input('department-filter', 'value')]
)
def update_sunburst(data, department_filter):
    if not data or 'sales' not in data:
        return go.Figure()
    
    sales_df = pd.DataFrame(data['sales'])
    return create_sunburst_chart(sales_df, department_filter)

@callback(
    Output('bubble-chart', 'figure'),
    Input('data-store', 'data')
)
def update_bubble(data):
    if not data or 'products' not in data:
        return go.Figure()
    
    products_df = pd.DataFrame(data['products'])
    return create_bubble_chart(products_df)

@callback(
    Output('area-chart', 'figure'),
    [Input('data-store', 'data'),
     Input('department-filter', 'value')]
)
def update_area(data, department_filter):
    if not data or 'sales' not in data:
        return go.Figure()
    
    sales_df = pd.DataFrame(data['sales'])
    return create_area_chart(sales_df)

@callback(
    Output('stacked-bar-chart', 'figure'),
    [Input('data-store', 'data'),
     Input('department-filter', 'value')]
)
def update_stacked_bar(data, department_filter):
    if not data or 'sales' not in data:
        return go.Figure()
    
    sales_df = pd.DataFrame(data['sales'])
    return create_stacked_bar_chart(sales_df)

@callback(
    Output('flow-chart', 'figure'),
    Input('data-store', 'data')
)
def update_flow(data):
    if not data or 'funnel' not in data or 'sources' not in data:
        return go.Figure()
    
    funnel_df = pd.DataFrame(data['funnel'])
    sources_df = pd.DataFrame(data['sources'])
    return create_flow_chart(funnel_df, sources_df)

@callback(
    Output('map-chart', 'figure'),
    [Input('data-store', 'data'),
     Input('department-filter', 'value')]
)
def update_map(data, department_filter):
    if not data or 'sales' not in data:
        return go.Figure()
    
    sales_df = pd.DataFrame(data['sales'])
    return create_map_chart(sales_df)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050, debug=True)

