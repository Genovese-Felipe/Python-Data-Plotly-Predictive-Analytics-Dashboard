"""
An advanced performance analytics dashboard for strategic project management.

This script uses Plotly and Dash to create a sophisticated, interactive dashboard
for in-depth analysis of a project portfolio. It includes advanced KPIs,
automated executive insights, and a variety of complex visualizations to track
performance, financials, risk, and quality.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import os
import sys

# Advanced color scheme for a professional look
ADVANCED_COLORS = {
    'primary': '#2E86AB', 'secondary': '#A23B72', 'accent': '#F18F01',
    'success': '#32A251', 'warning': '#FF6B35', 'danger': '#E74C3C',
    'info': '#17A2B8', 'light': '#F8F9FA', 'dark': '#2C3E50',
    'purple': '#8E44AD', 'teal': '#1ABC9C'
}


def load_advanced_data():
    """
    Loads advanced performance analytics data from CSV files.

    Returns:
        tuple: A tuple of pandas DataFrames.
    """
    try:
        data_path = os.path.join(os.path.dirname(__file__), '../data')
        df_projects = pd.read_csv(os.path.join(data_path, 'projects_advanced.csv'), parse_dates=['start_date', 'planned_end_date', 'actual_end_date'])
        df_milestones = pd.read_csv(os.path.join(data_path, 'milestones_advanced.csv'), parse_dates=['planned_date', 'actual_date'])
        df_financial = pd.read_csv(os.path.join(data_path, 'financial_advanced.csv'), parse_dates=['month'])
        df_resources = pd.read_csv(os.path.join(data_path, 'resources_advanced.csv'))
        df_quality = pd.read_csv(os.path.join(data_path, 'quality_metrics.csv'), parse_dates=['measurement_date'])
        print("Advanced data loaded successfully.")
        return df_projects, df_milestones, df_financial, df_resources, df_quality
    except FileNotFoundError:
        print("Advanced data files not found. Please run the corresponding data generation script.")
        sys.exit(1)


def create_advanced_kpi_card(title, value, change=None, icon=None, color='primary', subtitle=None):
    """
    Creates an advanced, styled KPI card.

    Args:
        title (str): The title of the KPI.
        value (str): The value to display.
        change (str, optional): The change from a previous period.
        icon (str, optional): The Font Awesome icon name.
        color (str, optional): The color theme.
        subtitle (str, optional): A subtitle for the KPI.

    Returns:
        dbc.Card: A styled KPI card component.
    """
    card_content = [
        html.H6(title, className="text-muted", style={'textTransform': 'uppercase'}),
        html.H2(value, style={'color': ADVANCED_COLORS[color]}),
        html.P(subtitle, className="text-muted") if subtitle else ""
    ]
    if change:
        change_color = 'green' if float(change.strip('%+-')) > 0 else 'red'
        card_content.append(html.P(f"{change} vs last period", style={'color': change_color}))
    return dbc.Card(dbc.CardBody(card_content), className="shadow-sm")


def generate_executive_insights(df_projects, df_financial=None, df_quality=None):
    """
    Generates automated, executive-level insights from the data.

    Args:
        df_projects (pd.DataFrame): The main projects DataFrame.
        df_financial (pd.DataFrame, optional): The financial data.
        df_quality (pd.DataFrame, optional): The quality metrics data.

    Returns:
        list: A list of Dash components with insights.
    """
    if df_projects.empty:
        return [html.P("No data available to generate insights.", className="text-muted")]
    
    insights = []
    # Portfolio Health Score
    health_score = (df_projects['progress_percent'].mean() + (1 - (df_projects['risk_score'].mean() / 10)) * 100) / 2
    insights.append(html.P(f"Portfolio Health Score: {health_score:.1f}/100"))
    
    # Budget Performance
    budget_variance = ((df_projects['actual_cost_usd'].sum() - df_projects['budget_usd'].sum()) / df_projects['budget_usd'].sum()) * 100
    insights.append(html.P(f"Budget Performance: {budget_variance:.1f}% variance"))
    
    return insights


# Load data and initialize app
df_projects, df_milestones, df_financial, df_resources, df_quality = load_advanced_data()
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])
server = app.server

# App layout
app.layout = dbc.Container(fluid=True, children=[
    html.H1("🚀 Advanced Performance Analytics", className="my-4 text-center"),
    dbc.Row([
        dbc.Col(create_advanced_kpi_card("Portfolio Size", f"{len(df_projects)}", "+15%", "briefcase"), width=3),
        dbc.Col(create_advanced_kpi_card("Total Investment", f"${df_projects['budget_usd'].sum()/1e6:.1f}M", "+22%", "dollar-sign", "success"), width=3),
        dbc.Col(create_advanced_kpi_card("Completion Rate", f"{(len(df_projects[df_projects['status'] == 'Completed'])/len(df_projects))*100:.1f}%", "+8%", "check-circle", "teal"), width=3),
        dbc.Col(create_advanced_kpi_card("Expected ROI", f"{df_projects['expected_roi_pct'].mean():.0f}%", "+12%", "chart-line", "accent"), width=3),
    ], className="mb-4"),
    dbc.Row([
        dbc.Col(dcc.Graph(id='performance-matrix'), width=8),
        dbc.Col(dcc.Graph(id='category-sunburst'), width=4)
    ])
])


@callback(
    [Output('performance-matrix', 'figure'),
     Output('category-sunburst', 'figure')],
    [Input('performance-matrix', 'id')] # Dummy input to trigger callback
)
def update_advanced_charts(_):
    """
    Updates all charts in the advanced analytics dashboard.

    Args:
        _ : A dummy input to trigger the callback on load.

    Returns:
        tuple: A tuple of updated Plotly figure objects.
    """
    # Performance Matrix
    fig_matrix = px.scatter(
        df_projects, x='schedule_variance_days', y='budget_variance_pct',
        size='budget_usd', color='priority', hover_name='project_name',
        labels={'schedule_variance_days': 'Schedule Variance (Days)', 'budget_variance_pct': 'Budget Variance (%)'}
    )
    
    # Category Sunburst
    fig_sunburst = px.sunburst(
        df_projects, path=['category', 'priority'], values='budget_usd',
        title="Portfolio Distribution by Category and Priority"
    )
    
    return fig_matrix, fig_sunburst


if __name__ == '__main__':
    print("Starting Advanced Performance Analytics Dashboard...")
    app.run_server(debug=True)