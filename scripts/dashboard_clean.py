"""
A clean and comprehensive project analytics dashboard.

This script creates a professional, interactive dashboard for project analytics
using Plotly and Dash. It includes synthetic data generation, a variety of
visualizations, and interactive filters to provide detailed insights into
project performance, budget, and resource allocation.
"""
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc

# Configuration and Styling
COLORS = {
    'primary': '#007bff', 'success': '#28a745', 'danger': '#dc3545',
    'warning': '#ffc107', 'info': '#17a2b8', 'secondary': '#6c757d',
    'dark': '#343a40', 'light': '#f8f9fa', 'white': '#ffffff'
}


def generate_synthetic_data():
    """
    Generates a comprehensive set of synthetic data for the dashboard.

    This function creates several pandas DataFrames with realistic data for
    projects, including master data, status, stages, budget, resources, and workload.

    Returns:
        dict: A dictionary of pandas DataFrames.
    """
    np.random.seed(42)
    project_ids = [f'PROJ_{i:03d}' for i in range(1, 31)]

    projects_master = pd.DataFrame({
        'project_id': project_ids,
        'project_name': [f'Project {i}' for i in range(1, 31)],
        'type': np.random.choice(['Web Development', 'Data Analysis', 'Mobile App', 'Infrastructure', 'Research'], 30),
        'manager': np.random.choice(['John Smith', 'Maria Garcia', 'David Wilson', 'Sarah Johnson'], 30),
        'start_date': pd.to_datetime(pd.date_range(start='2023-01-01', periods=30, freq='15D')),
        'priority': np.random.choice(['High', 'Medium', 'Low'], 30),
        'total_budget': np.random.uniform(50000, 500000, 30).round(2)
    })
    
    project_status = pd.DataFrame({
        'project_id': project_ids,
        'status': np.random.choice(['Completed', 'In Progress', 'On Hold'], 30, p=[0.4, 0.5, 0.1]),
        'completion_percent': np.random.uniform(20, 100, 30).round(1)
    })
    
    return {'projects_master': projects_master, 'project_status': project_status}


# Load Data
data = generate_synthetic_data()

# App Initialization
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout
app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1("📊 Project Analytics Dashboard", className="text-center mb-4"), width=12)),
    dbc.Row([
        dbc.Col(dcc.Dropdown(id='project-selector',
                             options=[{'label': 'All Projects', 'value': 'all'}] +
                                     [{'label': pid, 'value': pid} for pid in data['projects_master']['project_id']],
                             value='all', placeholder="Select a project..."), md=4),
        dbc.Col(dcc.Dropdown(id='type-filter',
                             options=[{'label': t, 'value': t} for t in data['projects_master']['type'].unique()],
                             multi=True, placeholder="Filter by type..."), md=4),
        dbc.Col(dcc.Dropdown(id='manager-filter',
                             options=[{'label': m, 'value': m} for m in data['projects_master']['manager'].unique()],
                             multi=True, placeholder="Filter by manager..."), md=4),
    ], className="mb-4"),
    dbc.Row([
        dbc.Col(dcc.Graph(id='status-pie-chart'), md=6),
        dbc.Col(dcc.Graph(id='completion-gauge-chart'), md=6),
    ], className="mb-4"),
    dbc.Row([
        dbc.Col(dash_table.DataTable(
            id='projects-table',
            columns=[{"name": i, "id": i} for i in pd.merge(data['projects_master'], data['project_status'], on='project_id').columns],
            page_size=10,
            sort_action="native",
            filter_action="native"
        ), width=12)
    ]),
], fluid=True)


@app.callback(
    [Output('status-pie-chart', 'figure'),
     Output('completion-gauge-chart', 'figure'),
     Output('projects-table', 'data')],
    [Input('project-selector', 'value'),
     Input('type-filter', 'value'),
     Input('manager-filter', 'value')]
)
def update_dashboard(selected_project, selected_types, selected_managers):
    """
    Updates all charts and the table based on user-selected filters.

    Args:
        selected_project (str): The selected project ID.
        selected_types (list): A list of selected project types.
        selected_managers (list): A list of selected project managers.

    Returns:
        tuple: A tuple of updated figures and data for the dashboard components.
    """
    filtered_projects = data['projects_master'].copy()

    if selected_project and selected_project != 'all':
        filtered_projects = filtered_projects[filtered_projects['project_id'] == selected_project]
    if selected_types:
        filtered_projects = filtered_projects[filtered_projects['type'].isin(selected_types)]
    if selected_managers:
        filtered_projects = filtered_projects[filtered_projects['manager'].isin(selected_managers)]

    project_ids = filtered_projects['project_id'].tolist()
    status_data = data['project_status'][data['project_status']['project_id'].isin(project_ids)]

    # Status Pie Chart
    status_counts = status_data['status'].value_counts()
    status_fig = px.pie(
        values=status_counts.values, names=status_counts.index,
        title="Project Status Distribution",
        color_discrete_map={'Completed': COLORS['success'], 'In Progress': COLORS['primary'], 'On Hold': COLORS['warning']}
    )

    # Completion Gauge
    avg_completion = status_data['completion_percent'].mean() if not status_data.empty else 0
    gauge_fig = go.Figure(go.Indicator(
        mode="gauge+number", value=avg_completion,
        title={'text': "Average Project Completion %"},
        gauge={'axis': {'range': [None, 100]}, 'bar': {'color': COLORS['primary']}}
    ))

    # Table data
    table_data = pd.merge(filtered_projects, status_data, on='project_id').to_dict('records')

    return status_fig, gauge_fig, table_data


if __name__ == '__main__':
    print("🚀 Starting Dashboard...")
    print("🌐 Access: http://localhost:8050")
    app.run_server(debug=True)