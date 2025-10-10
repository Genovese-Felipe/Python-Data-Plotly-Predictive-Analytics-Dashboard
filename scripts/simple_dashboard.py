"""
A simple, interactive dashboard for visualizing project status and progress.

This script creates a web-based dashboard using Plotly and Dash that displays
a pie chart for project status and a bar chart for project progress. It includes
an interactive dropdown to filter the projects by their status.
"""
import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np

# Generate simple data for testing
np.random.seed(42)
df = pd.DataFrame({
    'project': [f'Proj_{i}' for i in range(1, 11)],
    'status': np.random.choice(['Completed', 'In Progress', 'On Hold'], 10),
    'progress': np.random.randint(20, 100, 10)
})

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout of the dashboard
app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1("📊 Simple Dashboard", className="text-center mb-4 text-primary"), width=12)),
    dbc.Row(dbc.Col(dbc.Card(dbc.CardBody([
        html.H5("Status Filter", className="card-title"),
        dcc.Dropdown(
            id='status-filter',
            options=[{'label': s, 'value': s} for s in df['status'].unique()],
            value=df['status'].unique().tolist(),
            multi=True
        )
    ])), width=12), className="mb-4"),
    
    dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody(dcc.Graph(id='status-chart'))), width=6),
        dbc.Col(dbc.Card(dbc.CardBody(dcc.Graph(id='progress-chart'))), width=6)
    ], className="mb-4"),
    
    dbc.Row(dbc.Col(html.Div(id='data-info', className="text-center text-muted"), width=12))
    
], fluid=True)


@app.callback(
    [Output('status-chart', 'figure'),
     Output('progress-chart', 'figure'),
     Output('data-info', 'children')],
    [Input('status-filter', 'value')]
)
def update_charts(selected_status):
    """
    Updates the charts and info text based on the selected project statuses.

    This callback function is triggered when the user changes the selection in the
    status filter dropdown. It filters the data and regenerates the pie and bar charts.

    Args:
        selected_status (list): A list of project statuses selected by the user.

    Returns:
        tuple: A tuple containing the updated figures for the status and progress
               charts, and a string with info about the displayed data.
    """
    filtered_df = df[df['status'].isin(selected_status)] if selected_status else df

    # Status Pie Chart
    status_counts = filtered_df['status'].value_counts()
    fig_status = px.pie(
        values=status_counts.values,
        names=status_counts.index,
        title="Status Distribution",
        color_discrete_sequence=['#28a745', '#007bff', '#ffc107']
    )

    # Progress Bar Chart
    fig_progress = px.bar(
        filtered_df,
        x='project',
        y='progress',
        title="Progress by Project",
        color='progress',
        color_continuous_scale='RdYlGn'
    )

    info = f"📊 Showing {len(filtered_df)} of {len(df)} projects"
    
    return fig_status, fig_progress, info


if __name__ == '__main__':
    print("🚀 Simple Dashboard Started!")
    print("🌐 Access: http://localhost:8050")
    print("💡 Test the filters to see the interactivity")
    app.run_server(debug=True)