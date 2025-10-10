"""
A visualization script for the construction project management dashboard.

This script loads the construction project data and creates a comprehensive,
interactive dashboard using Plotly and Dash. It includes a variety of charts
and KPIs to provide an executive overview of project portfolio performance.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, html, dcc, Input, Output
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

    If the data files are not found, it attempts to generate them by running
    the 'data_gen.py' script.

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
        
        df_projects_master['start_date'] = pd.to_datetime(df_projects_master['start_date'])
        df_projects_master['planned_end_date'] = pd.to_datetime(df_projects_master['planned_end_date'])
        
        return df_projects_master, df_project_status, df_project_stages, df_budget_variance, df_resources, df_workload
    except FileNotFoundError:
        print("Data files not found. Running data generation...")
        from data_gen import generate_construction_projects
        return generate_construction_projects(30)


def create_gauge_chart(value, title, range_max=100, color=COLORS['primary']):
    """
    Creates a gauge chart for KPIs.

    Args:
        value (float): The value to display on the gauge.
        title (str): The title of the gauge.
        range_max (int, optional): The maximum value of the gauge range. Defaults to 100.
        color (str, optional): The color of the gauge bar. Defaults to COLORS['primary'].

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


def create_combination_chart(df_budget):
    """
    Creates a combination bar and line chart for budget variance.

    Args:
        df_budget (pd.DataFrame): The DataFrame containing budget data.

    Returns:
        go.Figure: A Plotly figure object.
    """
    monthly_data = df_budget.groupby('month').agg({'actual_budget': 'sum', 'planned_budget': 'sum'}).reset_index()
    monthly_data['variance_pct'] = ((monthly_data['actual_budget'] - monthly_data['planned_budget']) / monthly_data['planned_budget'] * 100)
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=monthly_data['month'], y=monthly_data['planned_budget'], name='Planned Budget'), secondary_y=False)
    fig.add_trace(go.Bar(x=monthly_data['month'], y=monthly_data['actual_budget'], name='Actual Budget'), secondary_y=False)
    fig.add_trace(go.Scatter(x=monthly_data['month'], y=monthly_data['variance_pct'], name='Variance %'), secondary_y=True)
    
    fig.update_layout(title={'text': 'Budget Variance', 'x': 0.5}, height=300, barmode='group')
    return fig


# Load data and initialize app
df_projects_master, df_project_status, df_project_stages, df_budget_variance, df_resources, df_workload = load_data()
df_main = df_projects_master.merge(df_project_status, on='project_id').merge(df_project_stages, on='project_id')

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Define app layout
app.layout = dbc.Container(fluid=True, children=[
    html.H1("Construction Project Monitoring Dashboard", className="text-center my-4"),
    dcc.Dropdown(
        id='project-selector',
        options=[{'label': 'All Projects', 'value': 'all'}] + [{'label': f"{r['project_id']}: {r['name']}", 'value': r['project_id']} for _, r in df_projects_master.iterrows()],
        value='all',
        className="mb-4"
    ),
    dbc.Row([
        dbc.Col(dcc.Graph(id='work-status-donut'), width=4),
        dbc.Col(dcc.Graph(id='completion-gauge'), width=4),
        dbc.Col(dcc.Graph(id='budget-combination'), width=4),
    ])
])


@app.callback(
    [Output('work-status-donut', 'figure'),
     Output('completion-gauge', 'figure'),
     Output('budget-combination', 'figure')],
    [Input('project-selector', 'value')]
)
def update_charts(selected_project):
    """
    Updates the dashboard charts based on the selected project.

    Args:
        selected_project (str): The ID of the selected project, or 'all'.

    Returns:
        tuple: A tuple of updated Plotly figure objects.
    """
    if selected_project == 'all':
        filtered_main = df_main
        filtered_budget = df_budget_variance
    else:
        filtered_main = df_main[df_main['project_id'] == selected_project]
        filtered_budget = df_budget_variance[df_budget_variance['project_id'] == selected_project]

    status_counts = filtered_main['status'].value_counts()
    work_status_fig = create_donut_chart(status_counts.values, status_counts.index, "Project Work Status")
    
    avg_completion = filtered_main['completion_percent'].mean()
    completion_gauge = create_gauge_chart(avg_completion, "Avg Completion %")
    
    budget_combination_fig = create_combination_chart(filtered_budget)
    
    return work_status_fig, completion_gauge, budget_combination_fig


if __name__ == '__main__':
    app.run_server(debug=True)