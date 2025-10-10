"""
An enhanced and highly interactive dashboard for monitoring construction projects.

This script generates a comprehensive, web-based dashboard using Plotly and Dash,
providing deep insights into construction project management. It features advanced
data generation, a wide variety of interactive visualizations with detailed tooltips,
and a sophisticated layout with extensive filtering options.
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
from datetime import datetime

# Professional color scheme
COLORS = {
    'primary': '#007bff', 'success': '#28a745', 'danger': '#dc3545',
    'warning': '#ffc107', 'info': '#17a2b8', 'secondary': '#6c757d',
    'dark': '#343a40', 'light': '#f8f9fa', 'white': '#ffffff'
}


def generate_enhanced_data():
    """
    Generates a comprehensive and enhanced set of synthetic data for the dashboard.

    This function creates several pandas DataFrames with realistic and detailed data
    for projects, including master data, status, stages, budget, resources, and workload.

    Returns:
        dict: A dictionary of pandas DataFrames.
    """
    np.random.seed(42)
    project_ids = [f'PROJ_{i:03d}' for i in range(1, 31)]

    projects_master = pd.DataFrame({
        'project_id': project_ids,
        'project_name': [f'Construction Project {i}' for i in range(1, 31)],
        'type': np.random.choice(['Residential', 'Commercial', 'Infrastructure', 'Industrial', 'Public Works'], 30),
        'manager': np.random.choice(['John Smith', 'Maria Garcia', 'David Wilson', 'Sarah Johnson'], 30),
        'priority': np.random.choice(['High', 'Medium', 'Low'], 30),
        'total_budget': np.random.uniform(50000, 500000, 30).round(2),
    })

    project_status = pd.DataFrame({
        'project_id': project_ids,
        'status': np.random.choice(['Completed', 'In Progress', 'On Hold', 'Planning'], 30, p=[0.3, 0.4, 0.1, 0.2]),
        'completion_percent': np.random.uniform(20, 100, 30).round(1),
        'days_ahead_behind': np.random.randint(-30, 15, 30)
    })
    
    return {'projects_master': projects_master, 'project_status': project_status}


def create_enhanced_charts(data):
    """
    Creates a dictionary of enhanced, interactive charts for the dashboard.

    Args:
        data (dict): A dictionary of DataFrames containing the project data.

    Returns:
        dict: A dictionary of Plotly figure objects for all the charts.
    """
    charts = {}
    merged_data = pd.merge(data['projects_master'], data['project_status'], on='project_id')

    status_counts = merged_data['status'].value_counts()
    charts['status_fig'] = px.pie(
        status_counts, values=status_counts.values, names=status_counts.index,
        title='Project Status Distribution', hole=0.3,
        color_discrete_sequence=[COLORS['success'], COLORS['primary'], COLORS['warning'], COLORS['secondary']]
    )

    avg_completion = merged_data['completion_percent'].mean()
    charts['gauge_fig'] = go.Figure(go.Indicator(
        mode="gauge+number+delta", value=avg_completion,
        title={'text': "Average Project Completion"}, delta={'reference': 85},
        gauge={'axis': {'range': [None, 100]}, 'bar': {'color': COLORS['primary']},
               'steps': [{'range': [0, 50], 'color': COLORS['danger']},
                         {'range': [50, 85], 'color': COLORS['warning']},
                         {'range': [85, 100], 'color': COLORS['success']}]}
    ))

    progress_data = merged_data.sort_values('completion_percent', ascending=True).head(15)
    charts['progress_fig'] = px.bar(
        progress_data, y='project_name', x='completion_percent', orientation='h',
        title='Project Progress Overview (Top 15)',
        labels={'completion_percent': 'Completion Percentage', 'project_name': 'Project'}
    )
    
    charts['scatter_fig'] = px.scatter(
        merged_data, x='total_budget', y='completion_percent', color='type', size='total_budget',
        hover_name='project_name', title='Budget vs. Completion by Project Type'
    )
    return charts


def create_enhanced_layout(data):
    """
    Creates the enhanced layout for the interactive dashboard.

    Args:
        data (dict): A dictionary of DataFrames to use for the layout.

    Returns:
        dbc.Container: The main container for the dashboard layout.
    """
    charts = create_enhanced_charts(data)
    return dbc.Container([
        html.H1("🏗️ Construction Project Monitoring Dashboard", className="text-center mb-4"),
        dbc.Row([
            dbc.Col(dcc.Dropdown(
                id='status-filter',
                options=[{'label': s, 'value': s} for s in data['project_status']['status'].unique()],
                placeholder="Filter by Status"
            ), md=4),
            dbc.Col(dcc.Dropdown(
                id='type-filter',
                options=[{'label': t, 'value': t} for t in data['projects_master']['type'].unique()],
                placeholder="Filter by Type"
            ), md=4),
            dbc.Col(dcc.Dropdown(
                id='priority-filter',
                options=[{'label': p, 'value': p} for p in data['projects_master']['priority'].unique()],
                placeholder="Filter by Priority"
            ), md=4),
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(dcc.Graph(id='status-chart', figure=charts['status_fig']), md=6),
            dbc.Col(dcc.Graph(id='gauge-chart', figure=charts['gauge_fig']), md=6),
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(dcc.Graph(id='progress-chart', figure=charts['progress_fig']), md=6),
            dbc.Col(dcc.Graph(id='scatter-chart', figure=charts['scatter_fig']), md=6),
        ]),
        dcc.Store(id='filtered-data-store', data=data)
    ], fluid=True)


def register_enhanced_callbacks(app):
    """
    Registers the callbacks for the enhanced interactive dashboard.

    Args:
        app (Dash): The Dash application instance.
    """
    @app.callback(
        [Output('status-chart', 'figure'), Output('gauge-chart', 'figure'),
         Output('progress-chart', 'figure'), Output('scatter-chart', 'figure')],
        [Input('status-filter', 'value'), Input('type-filter', 'value'), Input('priority-filter', 'value')]
    )
    def update_charts_callback(status, p_type, priority):
        """
        Updates all charts based on the selected filters.
        
        Args:
            status (str): The selected project status.
            p_type (str): The selected project type.
            priority (str): The selected project priority.

        Returns:
            tuple: A tuple of updated Plotly figures for all charts.
        """
        data = generate_enhanced_data()
        merged_data = pd.merge(data['projects_master'], data['project_status'], on='project_id')

        if status:
            merged_data = merged_data[merged_data['status'] == status]
        if p_type:
            merged_data = merged_data[merged_data['type'] == p_type]
        if priority:
            merged_data = merged_data[merged_data['priority'] == priority]

        charts = create_enhanced_charts({'projects_master': merged_data, 'project_status': merged_data})
        return charts['status_fig'], charts['gauge_fig'], charts['progress_fig'], charts['scatter_fig']


def create_enhanced_app():
    """
    Creates and configures the enhanced Dash application.

    Returns:
        Dash: The configured Dash application instance.
    """
    data = generate_enhanced_data()
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.layout = create_enhanced_layout(data)
    register_enhanced_callbacks(app)
    return app


def export_enhanced_dashboard():
    """
    Exports the enhanced dashboard to a static HTML file.
    """
    app = create_enhanced_app()
    with open('outputs/enhanced_dashboard.html', 'w', encoding='utf-8') as f:
        f.write(app.to_html(full_html=True, include_plotlyjs='cdn'))


if __name__ == "__main__":
    export_enhanced_dashboard()
    print("✅ Enhanced dashboard exported to outputs/enhanced_dashboard.html")
    app = create_enhanced_app()
    print("🚀 Starting enhanced interactive dashboard...")
    app.run_server(debug=True, port=8050)