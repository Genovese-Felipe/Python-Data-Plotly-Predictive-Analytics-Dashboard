"""
An interactive dashboard for a comparative analysis of productivity tools.

This script uses Plotly and Dash to create a feature-rich dashboard that
visualizes data about various productivity tools. It includes multiple charts
for ranking, criteria comparison, pricing, use cases, and market analysis,
all presented in a professional and interactive layout.
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from dash import Dash, dcc, html, dash_table
import dash_bootstrap_components as dbc
from datetime import datetime
import os

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
        dict: A dictionary of pandas DataFrames.
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
    
    return summary[['Ranking', 'tool_name', 'category', 'Score', 'Price']]


# Initialize Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
data = load_data()

# App layout
app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1("🔧 Productivity Tools Comparative Analysis", className="text-center my-4"), width=12)),
    dbc.Row([
        dbc.Col(dbc.Card(dcc.Graph(figure=create_ranking_chart(data))), width=12, className="mb-4"),
        dbc.Col(dbc.Card(dcc.Graph(figure=create_radar_chart(data))), width=12, className="mb-4"),
        dbc.Col(dash_table.DataTable(
            data=create_summary_table(data).to_dict('records'),
            columns=[{"name": i, "id": i} for i in create_summary_table(data).columns],
        ), width=12, className="mb-4"),
    ])
], fluid=True)


if __name__ == "__main__":
    print("🚀 Starting interactive dashboard...")
    app.run_server(debug=True)