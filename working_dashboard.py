import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Simple data generation
np.random.seed(42)
n_projects = 20

df = pd.DataFrame({
    'project_id': [f'PROJ_{i:03d}' for i in range(1, n_projects+1)],
    'project_name': [f'Project {i}' for i in range(1, n_projects+1)],
    'status': np.random.choice(['Completed', 'In Progress', 'On Hold'], n_projects),
    'completion': np.random.randint(20, 100, n_projects),
    'budget': np.random.randint(50000, 500000, n_projects),
    'type': np.random.choice(['Web Dev', 'Data Analysis', 'Mobile', 'Infrastructure'], n_projects)
})

# Initialize app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Project Dashboard", style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '30px'}),
    
    html.Div([
        html.Label("Select Project Type:"),
        dcc.Dropdown(
            id='type-dropdown',
            options=[{'label': t, 'value': t} for t in df['type'].unique()],
            value=df['type'].unique().tolist(),
            multi=True
        )
    ], style={'width': '48%', 'display': 'inline-block', 'marginBottom': '20px'}),
    
    html.Div([
        dcc.Graph(id='status-pie'),
        dcc.Graph(id='completion-bar'),
        dcc.Graph(id='budget-scatter'),
        dcc.Graph(id='sunburst-chart')
    ])
])

# Callbacks
@app.callback(
    [Output('status-pie', 'figure'),
     Output('completion-bar', 'figure'),
     Output('budget-scatter', 'figure'),
     Output('sunburst-chart', 'figure')],
    [Input('type-dropdown', 'value')]
)
def update_charts(selected_types):
    filtered_df = df[df['type'].isin(selected_types)]
    
    # Status Pie Chart
    status_counts = filtered_df['status'].value_counts()
    pie_fig = px.pie(values=status_counts.values, names=status_counts.index, 
                     title="Project Status Distribution")
    
    # Completion Bar Chart
    bar_fig = px.bar(filtered_df, x='project_id', y='completion', 
                     title="Project Completion %", color='status')
    bar_fig.update_xaxes(tickangle=45)
    
    # Budget Scatter
    scatter_fig = px.scatter(filtered_df, x='completion', y='budget', 
                           color='status', size='budget',
                           hover_data=['project_name'],
                           title="Budget vs Completion")
    
    # Sunburst Chart
    sunburst_data = []
    for _, row in filtered_df.iterrows():
        sunburst_data.append({
            'ids': row['project_id'],
            'labels': row['project_name'],
            'parents': row['type'],
            'values': row['completion']
        })
    
    for ptype in filtered_df['type'].unique():
        sunburst_data.append({
            'ids': ptype,
            'labels': ptype,
            'parents': '',
            'values': 0
        })
    
    sunburst_df = pd.DataFrame(sunburst_data)
    
    sunburst_fig = go.Figure(go.Sunburst(
        ids=sunburst_df['ids'],
        labels=sunburst_df['labels'],
        parents=sunburst_df['parents'],
        values=sunburst_df['values'],
        branchvalues="total"
    ))
    sunburst_fig.update_layout(title="Project Stages - Sunburst")
    
    return pie_fig, bar_fig, scatter_fig, sunburst_fig

if __name__ == '__main__':
    print("🚀 Dashboard starting at http://localhost:8050")
    app.run(debug=True, host='0.0.0.0', port=8050)
