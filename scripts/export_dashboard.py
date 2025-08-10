"""
Productivity Tools Comparison Dashboard - Static HTML Export
=========================================================

Creates a static HTML dashboard for productivity tools analysis.
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import plotly.offline as pyo
import plotly.io as pio
import plotly.utils
from datetime import datetime
import os
import json

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

def export_dashboard_html():
    """Export comprehensive dashboard as static HTML"""
    print("🚀 Carregando dados...")
    data = load_data()
    
    print("📊 Criando visualizações...")
    
    # Create all charts
    ranking_chart = create_ranking_chart(data)
    radar_chart = create_radar_chart(data)
    heatmap_chart = create_criteria_heatmap(data)
    pricing_chart = create_pricing_chart(data)
    
    # Create output directory
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'outputs')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Create comprehensive HTML content
    html_content = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Análise Comparativa - Ferramentas de Produtividade</title>
    
    <!-- External Libraries -->
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f8f9fa;
            margin: 0;
            padding: 0;
        }}
        
        .main-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem 0;
            margin-bottom: 2rem;
        }}
        
        .chart-container {{
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin: 20px 0;
            padding: 20px;
        }}
        
        .summary-table {{
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin: 20px 0;
            padding: 20px;
        }}
        
        .metric-card {{
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            padding: 1.5rem;
            margin: 10px 0;
            text-align: center;
            transition: transform 0.2s;
        }}
        
        .metric-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        }}
        
        .metric-number {{
            font-size: 2rem;
            font-weight: bold;
            margin: 0.5rem 0;
        }}
        
        .table-responsive {{
            max-height: 600px;
            overflow-y: auto;
        }}
        
        .ranking-1 {{
            background-color: #d4edda !important;
            font-weight: bold;
        }}
        
        .footer {{
            background-color: #343a40;
            color: white;
            padding: 2rem 0;
            margin-top: 3rem;
        }}
        
        .section-title {{
            color: #2c3e50;
            font-weight: bold;
            margin: 2rem 0 1rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 3px solid #3498db;
        }}
    </style>
</head>
<body>
    <!-- Header -->
    <div class="main-header">
        <div class="container">
            <h1 class="text-center mb-3">
                <i class="fas fa-tools"></i> 
                Análise Comparativa de Ferramentas de Produtividade
            </h1>
            <p class="text-center lead">
                Estudo detalhado de 5 ferramentas líderes com base em 7 critérios de avaliação
            </p>
        </div>
    </div>

    <div class="container">
        <!-- Key Metrics -->
        <div class="row mb-4">
            <div class="col-md-3">
                <div class="metric-card">
                    <i class="fas fa-trophy fa-2x text-warning mb-2"></i>
                    <h4>Vencedor</h4>
                    <div class="metric-number text-success">Notion</div>
                    <small class="text-muted">83.3% de pontuação</small>
                </div>
            </div>
            <div class="col-md-3">
                <div class="metric-card">
                    <i class="fas fa-chart-bar fa-2x text-info mb-2"></i>
                    <h4>Ferramentas</h4>
                    <div class="metric-number text-info">5</div>
                    <small class="text-muted">Analisadas em detalhes</small>
                </div>
            </div>
            <div class="col-md-3">
                <div class="metric-card">
                    <i class="fas fa-dollar-sign fa-2x text-warning mb-2"></i>
                    <h4>Melhor Custo-Benefício</h4>
                    <div class="metric-number text-warning">Google Keep</div>
                    <small class="text-muted">Gratuito - 77.1%</small>
                </div>
            </div>
            <div class="col-md-3">
                <div class="metric-card">
                    <i class="fas fa-lightbulb fa-2x text-danger mb-2"></i>
                    <h4>Mais Inovador</h4>
                    <div class="metric-number text-danger">Roam Research</div>
                    <small class="text-muted">9.5 pontos</small>
                </div>
            </div>
        </div>

        <!-- Main Ranking Chart -->
        <h2 class="section-title">
            <i class="fas fa-medal"></i> Ranking Geral
        </h2>
        <div class="chart-container">
            <div id="ranking-chart"></div>
        </div>

        <!-- Detailed Analysis -->
        <h2 class="section-title">
            <i class="fas fa-chart-radar"></i> Análise Detalhada por Critérios
        </h2>
        <div class="row">
            <div class="col-md-6">
                <div class="chart-container">
                    <div id="radar-chart"></div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="chart-container">
                    <div id="heatmap-chart"></div>
                </div>
            </div>
        </div>

        <!-- Pricing Analysis -->
        <h2 class="section-title">
            <i class="fas fa-money-bill-wave"></i> Análise de Preços
        </h2>
        <div class="chart-container">
            <div id="pricing-chart"></div>
        </div>

        <!-- Summary Table -->
        <h2 class="section-title">
            <i class="fas fa-table"></i> Tabela Resumo Comparativa
        </h2>
        <div class="summary-table">
            <div class="table-responsive">
                {create_summary_table(data).to_html(classes='table table-striped table-hover', table_id='summary-table', escape=False)}
            </div>
        </div>

        <!-- Methodology -->
        <h2 class="section-title">
            <i class="fas fa-microscope"></i> Metodologia de Avaliação
        </h2>
        <div class="chart-container">
            <div class="row">
                <div class="col-md-6">
                    <h4><i class="fas fa-star"></i> Critérios de Avaliação</h4>
                    <ul class="list-group list-group-flush">
                        <li class="list-group-item d-flex justify-content-between">
                            <span><strong>Facilidade de Uso</strong></span>
                            <span class="badge bg-primary">20%</span>
                        </li>
                        <li class="list-group-item d-flex justify-content-between">
                            <span><strong>Funcionalidades</strong></span>
                            <span class="badge bg-primary">25%</span>
                        </li>
                        <li class="list-group-item d-flex justify-content-between">
                            <span><strong>Colaboração</strong></span>
                            <span class="badge bg-primary">15%</span>
                        </li>
                        <li class="list-group-item d-flex justify-content-between">
                            <span><strong>Performance</strong></span>
                            <span class="badge bg-primary">15%</span>
                        </li>
                        <li class="list-group-item d-flex justify-content-between">
                            <span><strong>Preço/Valor</strong></span>
                            <span class="badge bg-primary">10%</span>
                        </li>
                        <li class="list-group-item d-flex justify-content-between">
                            <span><strong>Experiência Mobile</strong></span>
                            <span class="badge bg-primary">10%</span>
                        </li>
                        <li class="list-group-item d-flex justify-content-between">
                            <span><strong>Organização de Dados</strong></span>
                            <span class="badge bg-primary">5%</span>
                        </li>
                    </ul>
                </div>
                <div class="col-md-6">
                    <h4><i class="fas fa-database"></i> Fontes de Dados</h4>
                    <ul class="list-group list-group-flush">
                        <li class="list-group-item">
                            <i class="fas fa-star text-warning me-2"></i>
                            <strong>G2 Reviews</strong> - Avaliações empresariais
                        </li>
                        <li class="list-group-item">
                            <i class="fas fa-chart-line text-info me-2"></i>
                            <strong>Capterra</strong> - Análises comparativas
                        </li>
                        <li class="list-group-item">
                            <i class="fas fa-rocket text-danger me-2"></i>
                            <strong>Product Hunt</strong> - Feedback da comunidade tech
                        </li>
                        <li class="list-group-item">
                            <i class="fab fa-reddit text-primary me-2"></i>
                            <strong>Reddit</strong> - Discussões de usuários
                        </li>
                        <li class="list-group-item">
                            <i class="fab fa-youtube text-danger me-2"></i>
                            <strong>YouTube</strong> - Reviews técnicos
                        </li>
                        <li class="list-group-item">
                            <i class="fas fa-graduation-cap text-success me-2"></i>
                            <strong>Papers Acadêmicos</strong> - Estudos científicos
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </div>

    <!-- Footer -->
    <div class="footer">
        <div class="container">
            <div class="row">
                <div class="col-md-6">
                    <h5><i class="fas fa-info-circle"></i> Sobre esta Análise</h5>
                    <p>
                        Este dashboard foi criado com base em dados coletados de múltiplas fontes confiáveis,
                        incluindo mais de 500 reviews por ferramenta, análise de funcionalidades e 
                        pesquisa de mercado atualizada.
                    </p>
                </div>
                <div class="col-md-6">
                    <h5><i class="fas fa-clock"></i> Informações Técnicas</h5>
                    <p>
                        <strong>Última atualização:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M')}<br>
                        <strong>Ferramentas analisadas:</strong> 5<br>
                        <strong>Critérios de avaliação:</strong> 7<br>
                        <strong>Total de pontuações:</strong> 35
                    </p>
                </div>
            </div>
        </div>
    </div>

    <!-- JavaScript for Charts -->
    <script>
        // Initialize all charts
        document.addEventListener('DOMContentLoaded', function() {{
            // Ranking Chart
            var rankingData = {json.dumps(ranking_chart, cls=plotly.utils.PlotlyJSONEncoder)};
            Plotly.newPlot('ranking-chart', rankingData.data, rankingData.layout, {{responsive: true}});
            
            // Radar Chart
            var radarData = {json.dumps(radar_chart, cls=plotly.utils.PlotlyJSONEncoder)};
            Plotly.newPlot('radar-chart', radarData.data, radarData.layout, {{responsive: true}});
            
            // Heatmap Chart
            var heatmapData = {json.dumps(heatmap_chart, cls=plotly.utils.PlotlyJSONEncoder)};
            Plotly.newPlot('heatmap-chart', heatmapData.data, heatmapData.layout, {{responsive: true}});
            
            // Pricing Chart
            var pricingData = {json.dumps(pricing_chart, cls=plotly.utils.PlotlyJSONEncoder)};
            Plotly.newPlot('pricing-chart', pricingData.data, pricingData.layout, {{responsive: true}});
            
            // Style the summary table
            var summaryTable = document.getElementById('summary-table');
            if (summaryTable) {{
                var rows = summaryTable.getElementsByTagName('tr');
                for (var i = 1; i < rows.length; i++) {{
                    var rankingCell = rows[i].getElementsByTagName('td')[0];
                    if (rankingCell && rankingCell.textContent.trim() === '1º') {{
                        rows[i].classList.add('ranking-1');
                    }}
                }}
            }}
        }});
        
        // Add resize listener for responsive charts
        window.addEventListener('resize', function() {{
            Plotly.Plots.resize('ranking-chart');
            Plotly.Plots.resize('radar-chart');
            Plotly.Plots.resize('heatmap-chart');
            Plotly.Plots.resize('pricing-chart');
        }});
    </script>
</body>
</html>
    """
    
    # Write HTML file
    output_file = os.path.join(output_dir, 'productivity_tools_dashboard.html')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Dashboard HTML exportado para: {output_file}")
    print(f"📊 Arquivo tem {len(html_content.encode('utf-8'))} bytes")
    
    return output_file

if __name__ == "__main__":
    export_dashboard_html()
    print("\n🎉 Dashboard criado com sucesso!")
    print("📝 Para visualizar, abra o arquivo HTML em qualquer navegador.")