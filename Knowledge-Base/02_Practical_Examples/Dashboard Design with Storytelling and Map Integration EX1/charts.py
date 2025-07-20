import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

def create_sunburst_chart(sales_df, department_filter='all'):
    """Cria gráfico Sunburst hierárquico de vendas por categoria"""
    
    # Filtrar dados se necessário
    if department_filter != 'all':
        # Mapear departamentos para categorias
        dept_mapping = {
            'sales': ['Eletrônicos', 'Roupas'],
            'marketing': ['Casa & Jardim', 'Livros'],
            'operations': ['Esportes'],
            'finance': ['Eletrônicos', 'Casa & Jardim']
        }
        if department_filter in dept_mapping:
            sales_df = sales_df[sales_df['category'].isin(dept_mapping[department_filter])]
    
    # Agregar dados por categoria e subcategoria
    category_totals = sales_df.groupby('category')['total_revenue'].sum().reset_index()
    subcategory_totals = sales_df.groupby(['category', 'subcategory'])['total_revenue'].sum().reset_index()
    
    # Preparar dados para o sunburst
    labels = ['Vendas Totais'] + category_totals['category'].tolist()
    parents = [''] + ['Vendas Totais'] * len(category_totals)
    values = [category_totals['total_revenue'].sum()] + category_totals['total_revenue'].tolist()
    
    # Adicionar subcategorias
    for _, row in subcategory_totals.iterrows():
        labels.append(row['subcategory'])
        parents.append(row['category'])
        values.append(row['total_revenue'])
    
    fig = go.Figure(go.Sunburst(
        labels=labels,
        parents=parents,
        values=values,
        branchvalues="total",
        hovertemplate='<b>%{label}</b><br>Receita: R$ %{value:,.0f}<br>Percentual: %{percentParent}<extra></extra>',
        maxdepth=3,
        insidetextorientation='radial'
    ))
    
    fig.update_layout(
        title="Hierarquia de Vendas por Categoria",
        font_size=12,
        margin=dict(t=50, l=0, r=0, b=0),
        height=400
    )
    
    return fig

def create_bubble_chart(products_df):
    """Cria gráfico Bubble de performance de produtos"""
    
    fig = px.scatter(
        products_df,
        x='sales_volume',
        y='profit_margin',
        size='total_revenue',
        color='customer_satisfaction',
        hover_name='product',
        hover_data={
            'sales_volume': ':,',
            'profit_margin': ':.1f',
            'total_revenue': ':,.0f',
            'customer_satisfaction': ':.1f'
        },
        labels={
            'sales_volume': 'Volume de Vendas (unidades)',
            'profit_margin': 'Margem de Lucro (%)',
            'customer_satisfaction': 'Satisfação do Cliente',
            'total_revenue': 'Receita Total (R$)'
        },
        color_continuous_scale='Viridis',
        size_max=60
    )
    
    fig.update_layout(
        title="Análise de Performance por Produto",
        xaxis_title="Volume de Vendas (unidades)",
        yaxis_title="Margem de Lucro (%)",
        height=400,
        margin=dict(t=50, l=50, r=50, b=50)
    )
    
    return fig

def create_area_chart(sales_df):
    """Cria gráfico de área com tendências de receita"""
    
    # Agregar dados por mês
    sales_df['month'] = pd.to_datetime(sales_df['date']).dt.to_period('M')
    monthly_data = sales_df.groupby('month').agg({
        'total_revenue': 'sum',
        'quantity': 'sum'
    }).reset_index()
    
    # Converter período para string para plotagem
    monthly_data['month_str'] = monthly_data['month'].astype(str)
    
    # Calcular meta (110% da receita real com variação)
    monthly_data['target'] = monthly_data['total_revenue'] * 1.1 * (1 + np.random.uniform(-0.1, 0.1, len(monthly_data)))
    
    fig = go.Figure()
    
    # Área da receita real
    fig.add_trace(go.Scatter(
        x=monthly_data['month_str'],
        y=monthly_data['total_revenue'],
        fill='tonexty',
        mode='lines+markers',
        name='Receita Real',
        line=dict(color='#3b82f6', width=2),
        fillcolor='rgba(59, 130, 246, 0.3)',
        hovertemplate='<b>Receita Real</b><br>Mês: %{x}<br>Valor: R$ %{y:,.0f}<extra></extra>'
    ))
    
    # Linha da meta
    fig.add_trace(go.Scatter(
        x=monthly_data['month_str'],
        y=monthly_data['target'],
        mode='lines+markers',
        name='Meta',
        line=dict(color='#10b981', width=2, dash='dash'),
        hovertemplate='<b>Meta</b><br>Mês: %{x}<br>Valor: R$ %{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title="Tendências de Receita Mensal",
        xaxis_title="Mês",
        yaxis_title="Receita (R$)",
        height=400,
        margin=dict(t=50, l=50, r=50, b=50),
        hovermode='x unified'
    )
    
    return fig

def create_stacked_bar_chart(sales_df):
    """Cria gráfico de barras empilhadas por canal e período"""
    
    # Agregar dados por trimestre e canal
    sales_df['quarter'] = pd.to_datetime(sales_df['date']).dt.to_period('Q')
    quarterly_data = sales_df.groupby(['quarter', 'channel'])['total_revenue'].sum().reset_index()
    quarterly_data['quarter_str'] = quarterly_data['quarter'].astype(str)
    
    # Pivot para ter canais como colunas
    pivot_data = quarterly_data.pivot(index='quarter_str', columns='channel', values='total_revenue').fillna(0)
    
    fig = go.Figure()
    
    colors = ['#3b82f6', '#10b981', '#8b5cf6', '#f59e0b']
    
    for i, channel in enumerate(pivot_data.columns):
        fig.add_trace(go.Bar(
            name=channel,
            x=pivot_data.index,
            y=pivot_data[channel],
            marker_color=colors[i % len(colors)],
            hovertemplate=f'<b>{channel}</b><br>Trimestre: %{{x}}<br>Receita: R$ %{{y:,.0f}}<extra></extra>'
        ))
    
    fig.update_layout(
        title="Vendas por Canal e Trimestre",
        xaxis_title="Trimestre",
        yaxis_title="Receita (R$)",
        barmode='stack',
        height=400,
        margin=dict(t=50, l=50, r=50, b=50)
    )
    
    return fig

def create_flow_chart(funnel_df, sources_df):
    """Cria gráfico Sankey (Flow) do funil de conversão"""
    
    # Preparar dados para o Sankey
    # Nós: estágios do funil + fontes de leads
    node_labels = sources_df['source'].tolist() + funnel_df['stage'].tolist()
    
    # Links: das fontes para leads, e entre estágios do funil
    source_indices = []
    target_indices = []
    values = []
    
    # Links das fontes para "Leads"
    leads_index = len(sources_df) + 1  # Índice de "Leads" na lista combinada
    for i, row in sources_df.iterrows():
        source_indices.append(i)  # Índice da fonte
        target_indices.append(leads_index)  # Índice de "Leads"
        values.append(row['leads'])
    
    # Links entre estágios do funil
    for i in range(len(funnel_df) - 1):
        source_indices.append(len(sources_df) + i)
        target_indices.append(len(sources_df) + i + 1)
        values.append(funnel_df.iloc[i + 1]['count'])
    
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=node_labels,
            color=["#3b82f6", "#10b981", "#8b5cf6", "#f59e0b", "#ef4444", "#06b6d4"] * 3
        ),
        link=dict(
            source=source_indices,
            target=target_indices,
            value=values,
            color=["rgba(59, 130, 246, 0.3)"] * len(values)
        )
    )])
    
    fig.update_layout(
        title="Fluxo de Conversão de Clientes",
        font_size=10,
        height=400,
        margin=dict(t=50, l=0, r=0, b=0)
    )
    
    return fig

def create_map_chart(sales_df):
    """Cria mapa interativo de vendas por região"""
    
    # Agregar dados por região
    regional_data = sales_df.groupby(['region', 'latitude', 'longitude']).agg({
        'total_revenue': 'sum',
        'quantity': 'sum'
    }).reset_index()
    
    # Calcular tamanho dos pontos baseado na receita
    regional_data['size'] = (regional_data['total_revenue'] / regional_data['total_revenue'].max()) * 50 + 10
    
    fig = px.scatter_mapbox(
        regional_data,
        lat='latitude',
        lon='longitude',
        size='size',
        color='total_revenue',
        hover_name='region',
        hover_data={
            'total_revenue': ':,.0f',
            'quantity': ':,',
            'latitude': False,
            'longitude': False,
            'size': False
        },
        color_continuous_scale='Viridis',
        size_max=30,
        zoom=3,
        center=dict(lat=-14.2350, lon=-51.9253),
        mapbox_style='open-street-map',
        labels={
            'total_revenue': 'Receita Total (R$)',
            'quantity': 'Quantidade Vendida'
        }
    )
    
    fig.update_layout(
        title="Distribuição Geográfica de Vendas",
        height=400,
        margin=dict(t=50, l=0, r=0, b=0)
    )
    
    return fig

