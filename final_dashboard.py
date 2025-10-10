"""A professional project management dashboard using Plotly Dash.

This script creates and runs a standalone Dash web application that provides an
interactive dashboard for monitoring project status, budget, and other key
metrics. The dashboard features multiple interconnected charts, filtering
capabilities, and a data table.

The data is synthetically generated for demonstration purposes.

To run the dashboard, execute this script from the command line:
    $ python final_dashboard.py

The dashboard will be available at http://127.0.0.1:8050/ by default.
"""

import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# --- Data Generation ---
# In a real-world application, this data would be loaded from a database,
# API, or file. For this demo, we generate a synthetic dataset.
np.random.seed(42)
projects = []
for i in range(1, 21):
    projects.append({
        'project_id': f'PROJ_{i:03d}',
        'project_name': f'Project {i}',
        'status': np.random.choice(['Completed', 'In Progress', 'On Hold']),
        'completion': np.random.randint(20, 100),
        'budget': np.random.randint(50000, 500000),
        'type': np.random.choice(['Web Dev', 'Data Analysis', 'Mobile', 'Infrastructure']),
        'manager': np.random.choice(['John', 'Maria', 'David', 'Sarah'])
    })

df = pd.DataFrame(projects)

# Initialize app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("📊 Project Dashboard", style={'textAlign': 'center', 'marginBottom': '30px'}),
    
    # Filters
    html.Div([
        html.Div([
            html.Label("Project Type:"),
            dcc.Dropdown(
                id='type-filter',
                options=[{'label': t, 'value': t} for t in df['type'].unique()],
                value=df['type'].unique().tolist(),
                multi=True
            )
        ], style={'width': '48%', 'display': 'inline-block'}),
        
        html.Div([
            html.Label("Manager:"),
            dcc.Dropdown(
                id='manager-filter',
                options=[{'label': m, 'value': m} for m in df['manager'].unique()],
                value=df['manager'].unique().tolist(),
                multi=True
            )
        ], style={'width': '48%', 'float': 'right'})
    ], style={'marginBottom': '30px'}),
    
    # Charts Row 1
    html.Div([
        html.Div([
            dcc.Graph(id='status-pie')
        ], style={'width': '50%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Graph(id='sunburst-chart')
        ], style={'width': '50%', 'display': 'inline-block'})
    ]),
    
    # Charts Row 2
    html.Div([
        html.Div([
            dcc.Graph(id='completion-bar')
        ], style={'width': '50%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Graph(id='budget-scatter')
        ], style={'width': '50%', 'display': 'inline-block'})
    ]),
    
    # Data Table
    html.Div([
        html.H3("Projects Table"),
        dash_table.DataTable(
            id='projects-table',
            columns=[
                {"name": "ID", "id": "project_id"},
                {"name": "Name", "id": "project_name"},
                {"name": "Status", "id": "status"},
                {"name": "Completion %", "id": "completion"},
                {"name": "Budget", "id": "budget", "type": "numeric", "format": {"specifier": "$,.0f"}},
                {"name": "Type", "id": "type"},
                {"name": "Manager", "id": "manager"}
            ],
            style_cell={'textAlign': 'left'},
            style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
            page_size=10
        )
    ], style={'marginTop': '30px'})
])

# Callback
@app.callback(
    [Output('status-pie', 'figure'),
     Output('completion-bar', 'figure'),
     Output('budget-scatter', 'figure'),
     Output('sunburst-chart', 'figure'),
     Output('projects-table', 'data')],
    [Input('type-filter', 'value'),
     Input('manager-filter', 'value')]
)
def update_dashboard(selected_types, selected_managers):
    """Updates all dashboard components in response to filter changes.

    This callback function is triggered whenever the user changes the
    selection in the 'Project Type' or 'Manager' dropdowns. It filters the
    main DataFrame and regenerates all the charts and the data table.

    Args:
        selected_types (list): A list of project types selected by the user.
        selected_managers (list): A list of managers selected by the user.

    Returns:
        tuple: A tuple containing the updated figures for the pie chart,
        bar chart, scatter plot, sunburst chart, and the data for the
        projects table.
    """
    # Filter data
    filtered_df = df[
        (df["type"].isin(selected_types)) & (df["manager"].isin(selected_managers))
    ]
    
    if filtered_df.empty:
        filtered_df = df  # Show all if no filters match
    
    # 1. Status Pie Chart
    status_counts = filtered_df['status'].value_counts()
    pie_fig = px.pie(
        values=status_counts.values,
        names=status_counts.index,
        title="Project Status Distribution"
    )
    
    # 2. Completion Bar Chart
    bar_fig = px.bar(
        filtered_df.head(10),
        x='project_id',
        y='completion',
        color='status',
        title="Project Completion Progress"
    )
    
    # 3. Budget Scatter
    scatter_fig = px.scatter(
        filtered_df,
        x='completion',
        y='budget',
        color='status',
        title="Budget vs Completion"
    )
    
    # 4. Sunburst Chart
    sunburst_fig = go.Figure(go.Sunburst(
        labels=['All Projects'] + filtered_df['type'].unique().tolist() + filtered_df['project_name'].tolist(),
        parents=[''] + ['All Projects'] * len(filtered_df['type'].unique()) + filtered_df['type'].tolist(),
        values=[1] + [1] * len(filtered_df['type'].unique()) + filtered_df['completion'].tolist(),
        branchvalues="total",
    ))
    sunburst_fig.update_layout(title="Project Hierarchy - Sunburst")
    
    return pie_fig, bar_fig, scatter_fig, sunburst_fig, filtered_df.to_dict('records')