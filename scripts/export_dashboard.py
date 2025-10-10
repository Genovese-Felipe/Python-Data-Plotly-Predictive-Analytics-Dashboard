"""
A script to generate a static HTML dashboard for productivity tools analysis.

This script loads data about various productivity tools, creates several
visualizations using Plotly, and exports a single, self-contained HTML file
with the complete dashboard.
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.utils
from datetime import datetime
import os
import json

# Professional color scheme
COLORS = {
    'primary': '#1f77b4', 'success': '#2ca02c', 'danger': '#d62728',
    'warning': '#ff7f0e', 'info': '#17becf', 'secondary': '#7f7f7f',
    'dark': '#1f1f1f', 'light': '#f8f9fa', 'white': '#ffffff',
    'obsidian': '#6c5ce7', 'notion': '#000000', 'keep': '#fbbc04',
    'roam': '#0984e3', 'evernote': '#00b894'
}

TOOL_COLORS = {
    'Obsidian': COLORS['obsidian'], 'Notion': COLORS['notion'],
    'Google Keep': COLORS['keep'], 'Roam Research': COLORS['roam'],
    'Evernote': COLORS['evernote']
}


def load_data():
    """
    Loads all necessary datasets from the data directory.

    Returns:
        dict: A dictionary of pandas DataFrames, with keys corresponding to the filenames.
    """
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    datasets = {}
    files = [
        'tools_basic_info.csv', 'evaluation_criteria.csv', 'detailed_scores.csv',
        'pricing_data.csv', 'use_cases_data.csv', 'weighted_scores.csv',
        'market_analysis.csv'
    ]
    for file in files:
        filepath = os.path.join(data_dir, file)
        key = file.replace('.csv', '')
        datasets[key] = pd.read_csv(filepath, encoding='utf-8')
    return datasets


def create_ranking_chart(data):
    """
    Creates the main ranking visualization as a horizontal bar chart.

    Args:
        data (dict): The dictionary of dataframes, requiring 'weighted_scores'.

    Returns:
        go.Figure: A Plotly figure object for the ranking chart.
    """
    df = data['weighted_scores'].sort_values('weighted_score', ascending=True)
    fig = px.bar(
        df, y='tool_name', x='percentage_score', orientation='h',
        text=df['percentage_score'].apply(lambda x: f'{x}%'),
        color='tool_name', color_discrete_map=TOOL_COLORS,
        title='<b>🏆 Overall Ranking - Productivity Tools</b>',
        labels={'percentage_score': '<b>Overall Score (%)</b>', 'tool_name': '<b>Tools</b>'}
    )
    fig.update_layout(showlegend=False, height=400, plot_bgcolor='white')
    return fig


def create_radar_chart(data):
    """
    Creates a radar chart for comparing tools across different criteria.

    Args:
        data (dict): The dictionary of dataframes, requiring 'detailed_scores'.

    Returns:
        go.Figure: A Plotly figure object for the radar chart.
    """
    pivot_df = data['detailed_scores'].pivot(index='tool_name', columns='criteria_name', values='score')
    fig = go.Figure()
    for tool in pivot_df.index:
        fig.add_trace(go.Scatterpolar(
            r=pivot_df.loc[tool].values, theta=pivot_df.columns,
            fill='toself', name=tool, line_color=TOOL_COLORS.get(tool)
        ))
    fig.update_layout(
        title='<b>📊 Comparison by Criteria</b>',
        polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
        showlegend=True, height=500
    )
    return fig


def create_criteria_heatmap(data):
    """
    Creates a heatmap of scores by criteria for a detailed comparison.

    Args:
        data (dict): The dictionary of dataframes, requiring 'detailed_scores'.

    Returns:
        go.Figure: A Plotly figure object for the heatmap.
    """
    pivot_df = data['detailed_scores'].pivot(index='tool_name', columns='criteria_name', values='score')
    fig = px.imshow(
        pivot_df, text_auto=True, aspect="auto",
        color_continuous_scale='RdYlGn',
        title='<b>🎯 Heatmap - Scores by Criteria</b>',
        labels=dict(x="<b>Evaluation Criteria</b>", y="<b>Tools</b>", color="Score")
    )
    fig.update_layout(height=400)
    return fig


def create_pricing_chart(data):
    """
    Creates a bar chart to compare the pricing of different tools.

    Args:
        data (dict): The dictionary of dataframes, requiring 'pricing_data'.

    Returns:
        go.Figure: A Plotly figure object for the pricing chart.
    """
    pricing_df = data['pricing_data'][data['pricing_data']['basic_plan_price_brl'] > 0]
    fig = px.bar(
        pricing_df, x='tool_name', y='basic_plan_price_brl',
        color='tool_name', color_discrete_map=TOOL_COLORS,
        title='<b>💰 Pricing Comparison (BRL / month)</b>',
        labels={'basic_plan_price_brl': '<b>Monthly Price (BRL)</b>', 'tool_name': '<b>Tools</b>'}
    )
    fig.update_layout(showlegend=False, height=400)
    return fig


def create_summary_table(data):
    """
    Creates a comprehensive summary table of all tools.

    Args:
        data (dict): The dictionary of dataframes.

    Returns:
        pd.DataFrame: A formatted DataFrame for display.
    """
    summary = pd.merge(data['tools_basic_info'], data['weighted_scores'], on='tool_name')
    summary = pd.merge(summary, data['pricing_data'][['tool_name', 'basic_plan_price_brl', 'free_plan']], on='tool_name')
    summary = pd.merge(summary, data['market_analysis'][['tool_name', 'market_position', 'future_outlook']], on='tool_name')
    
    summary['Ranking'] = summary['ranking'].astype(str) + 'º'
    summary['Score'] = summary['percentage_score'].astype(str) + '%'
    summary['Price'] = summary.apply(lambda x: 'Free' if x['free_plan'] else f"R$ {x['basic_plan_price_brl']}/month", axis=1)
    
    return summary[['Ranking', 'tool_name', 'category', 'Score', 'Price', 'target_users', 'market_position', 'future_outlook']]


def export_dashboard_html():
    """
    Exports the complete dashboard as a single, static HTML file.
    """
    print("🚀 Loading data...")
    data = load_data()
    
    print("📊 Creating visualizations...")
    charts = {
        'ranking_chart': create_ranking_chart(data),
        'radar_chart': create_radar_chart(data),
        'heatmap_chart': create_criteria_heatmap(data),
        'pricing_chart': create_pricing_chart(data),
    }
    summary_table_html = create_summary_table(data).to_html(classes='table table-striped', index=False)

    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'outputs')
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate HTML content
    html_content = f"""
    <html>
        <head>
            <title>Productivity Tools Analysis</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            <div class="container">
                <h1 class="text-center my-4">Productivity Tools Comparative Analysis</h1>
                <div class="row">
                    <div class="col-12 my-3">{charts['ranking_chart'].to_html(full_html=False, include_plotlyjs=False)}</div>
                    <div class="col-md-6 my-3">{charts['radar_chart'].to_html(full_html=False, include_plotlyjs=False)}</div>
                    <div class="col-md-6 my-3">{charts['heatmap_chart'].to_html(full_html=False, include_plotlyjs=False)}</div>
                    <div class="col-12 my-3">{charts['pricing_chart'].to_html(full_html=False, include_plotlyjs=False)}</div>
                    <div class="col-12 my-3"><h2>Summary Table</h2>{summary_table_html}</div>
                </div>
            </div>
        </body>
    </html>
    """
    
    output_file = os.path.join(output_dir, 'productivity_tools_dashboard.html')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Dashboard HTML exported to: {output_file}")


if __name__ == "__main__":
    export_dashboard_html()
    print("\n🎉 Dashboard created successfully!")
    print("📝 To view, open the HTML file in any browser.")