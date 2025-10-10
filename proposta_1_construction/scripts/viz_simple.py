"""
A static visualization script for the construction project management dashboard.

This script loads the construction project data and creates a static,
non-interactive dashboard using Plotly and Dash. It is designed to provide a
snapshot of the project portfolio performance.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import sys
import os

# Orange corporate theme colors
COLORS = {
    'primary': '#FF6B35', 'secondary': '#FF8C69', 'accent': '#FF4500',
    'success': '#28a745', 'warning': '#ffc107', 'danger': '#dc3545',
    'info': '#17a2b8', 'light': '#f8f9fa', 'dark': '#343a40'
}


def load_data():
    """
    Loads the construction project data from CSV files.

    If the data files are not found, it prints an error and exits.

    Returns:
        tuple: A tuple of pandas DataFrames for each dataset.
    """
    try:
        data_path = os.path.join(os.path.dirname(__file__), '../data')
        df_projects_master = pd.read_csv(os.path.join(data_path, 'projects_master.csv'))
        df_project_status = pd.read_csv(os.path.join(data_path, 'project_status.csv'))
        df_project_stages = pd.read_csv(os.path.join(data_path, 'project_stages.csv'))
        df_budget_variance = pd.read_csv(os.path.join(data_path, 'budget_variance.csv'))
        df_resources = pd.read_csv(os.path.join(data_path, 'resources.csv'))
        df_workload = pd.read_csv(os.path.join(data_path, 'workload.csv'))
        
        return df_projects_master, df_project_status, df_project_stages, df_budget_variance, df_resources, df_workload
    except FileNotFoundError:
        print("Data files not found. Please run data_gen.py first.")
        sys.exit(1)


def create_gauge_chart(value, title, range_max=100, color=COLORS['primary']):
    """
    Creates a gauge chart for KPIs.

    Args:
        value (float): The value to display on the gauge.
        title (str): The title of the gauge.
        range_max (int, optional): The maximum value of the gauge range.
        color (str, optional): The color of the gauge bar.

    Returns:
        go.Figure: A Plotly figure object.
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=value,
        title={'text': title},
        gauge={'axis': {'range': [None, range_max]}, 'bar': {'color': color}}
    ))
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=20))
    return fig


def create_donut_chart(values, names, title, colors=None):
    """
    Creates a donut chart.

    Args:
        values (list): The values for the chart segments.
        names (list): The names of the chart segments.
        title (str): The title of the chart.
        colors (list, optional): A list of colors for the segments.

    Returns:
        go.Figure: A Plotly figure object.
    """
    fig = px.pie(values=values, names=names, hole=0.4, color_discrete_sequence=colors)
    fig.update_layout(title={'text': title, 'x': 0.5}, height=250, showlegend=True)
    return fig


# Load data and create charts
df_projects_master, df_project_status, df_project_stages, df_budget_variance, df_resources, df_workload = load_data()
df_main = df_projects_master.merge(df_project_status, on='project_id').merge(df_project_stages, on='project_id')

status_counts = df_main['status'].value_counts()
work_status_fig = create_donut_chart(status_counts.values, status_counts.index, "Project Work Status")

stage_counts = df_main['stage'].value_counts()
stage_fig = create_donut_chart(stage_counts.values, stage_counts.index, "Projects by Stage")

avg_completion = df_main['completion_percent'].mean()
completion_gauge = create_gauge_chart(avg_completion, "Project Completion %")

# Initialize and define app layout
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container(fluid=True, children=[
    html.H1("Construction Project Dashboard (Static)", className="text-center my-4"),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=work_status_fig), width=4),
        dbc.Col(dcc.Graph(figure=stage_fig), width=4),
        dbc.Col(dcc.Graph(figure=completion_gauge), width=4),
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)