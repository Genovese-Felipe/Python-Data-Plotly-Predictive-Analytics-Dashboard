"""
A complete project management dashboard built with Plotly and Dash.

This script generates a professional dashboard with interactive visualizations
for project analytics, including project status, completion progress, and budget analysis.
It features multiple interconnected components, such as filters, charts, and a data table,
that update dynamically based on user input.
"""
import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Generate simple data
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
    """
    Update the dashboard components based on user-selected filters.

    This callback function is triggered when the user changes the values in the
    project type or manager dropdowns. It filters the main DataFrame and
    regenerates all the charts and the data table.

    Args:
        selected_types (list): A list of project types selected by the user.
        selected_managers (list): A list of project managers selected by the user.

    Returns:
        tuple: A tuple containing the updated figures for the charts and the
               data for the projects table.
    """
    filtered_df = df[
        (df['type'].isin(selected_types)) & 
        (df['manager'].isin(selected_managers))
    ]
    
    if filtered_df.empty:
        filtered_df = df.copy()

    status_counts = filtered_df['status'].value_counts()
    pie_fig = px.pie(
        values=status_counts.values,
        names=status_counts.index,
        title="Project Status Distribution"
    )
    
    bar_fig = px.bar(
        filtered_df.head(10),
        x='project_id',
        y='completion',
        color='status',
        title="Project Completion Progress"
    )
    
    scatter_fig = px.scatter(
        filtered_df,
        x='completion',
        y='budget',
        color='status',
        title="Budget vs Completion"
    )
    
    sunburst_fig = go.Figure(go.Sunburst(
        labels=['All Projects'] + filtered_df['type'].unique().tolist() + filtered_df['project_name'].tolist(),
        parents=[''] + ['All Projects'] * len(filtered_df['type'].unique()) + filtered_df['type'].tolist(),
        values=np.ones(len(filtered_df['type'].unique()) + len(filtered_df['project_name']) + 1),
        branchvalues="total",
    ))
    sunburst_fig.update_layout(title="Project Hierarchy - Sunburst")
    
    return pie_fig, bar_fig, scatter_fig, sunburst_fig, filtered_df.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)