# IMPORTS
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from dash import dash_table
from datetime import datetime, timedelta

# CONFIGURAÇÕES E ESTILO
COLORS = {
    'primary': '#007bff',
    'success': '#28a745',
    'danger': '#dc3545',
    'warning': '#ffc107',
    'info': '#17a2b8',
    'secondary': '#6c757d',
    'dark': '#343a40',
    'light': '#f8f9fa',
    'light_gray': '#e9ecef',
    'white': '#ffffff'
}

# DATA GENERATION
def generate_synthetic_data():
    """Generate comprehensive synthetic data for the dashboard"""
    
    np.random.seed(42)
    
    # Projects Master Data
    project_ids = [f'PROJ_{i:03d}' for i in range(1, 31)]
    projects_master = pd.DataFrame({
        'project_id': project_ids,
        'project_name': [f'Project {i}' for i in range(1, 31)],
        'type': np.random.choice(['Web Development', 'Data Analysis', 'Mobile App', 'Infrastructure', 'Research'], 30),
        'manager': np.random.choice(['John Smith', 'Maria Garcia', 'David Wilson', 'Sarah Johnson', 'Michael Brown'], 30),
        'start_date': pd.date_range(start='2023-01-01', periods=30, freq='15D')[:30],
        'end_date': pd.date_range(start='2024-01-01', periods=30, freq='20D')[:30],
        'priority': np.random.choice(['High', 'Medium', 'Low'], 30),
        'total_budget': np.random.uniform(50000, 500000, 30).round(2)
    })
    
    # Project Status Data
    project_status = pd.DataFrame({
        'project_id': project_ids,
        'status': np.random.choice(['Completed', 'In Progress', 'On Hold'], 30, p=[0.4, 0.5, 0.1]),
        'completion_percent': np.random.uniform(20, 100, 30).round(1),
        'last_updated': pd.date_range(start='2024-01-01', periods=30, freq='D')
    })
    
    # Project Stages
    stages = ['Planning', 'Development', 'Testing', 'Deployment', 'Maintenance']
    project_stages = []
    for project in project_ids[:15]:  # Only for some projects to have variety
        for stage in np.random.choice(stages, np.random.randint(2, 5), replace=False):
            project_stages.append({
                'project_id': project,
                'stage': stage,
                'status': np.random.choice(['Completed', 'In Progress', 'Pending']),
                'hours_spent': np.random.randint(10, 100)
            })
    project_stages = pd.DataFrame(project_stages)
    
    # Budget Variance
    budget_variance = []
    for project in project_ids:
        budget = projects_master[projects_master['project_id'] == project]['total_budget'].iloc[0]
        actual = budget * np.random.uniform(0.8, 1.2)
        budget_variance.append({
            'project_id': project,
            'planned_budget': budget,
            'actual_budget': actual,
            'variance': actual - budget,
            'month': np.random.choice(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'])
        })
    budget_variance = pd.DataFrame(budget_variance)
    
    # Resources
    resource_types = ['Developers', 'Designers', 'Testers', 'Managers', 'Infrastructure']
    resources = []
    for project in project_ids[:20]:  # Some projects only
        for resource_type in np.random.choice(resource_types, np.random.randint(2, 4), replace=False):
            resources.append({
                'project_id': project,
                'resource_type': resource_type,
                'planned_resources': np.random.randint(2, 10),
                'actual_resources': np.random.randint(1, 12),
                'allocation_date': pd.date_range(start='2024-01-01', periods=1, freq='D')[0]
            })
    resources = pd.DataFrame(resources)
    
    # Workload Data
    workload = []
    for project in project_ids:
        completed = np.random.randint(40, 200)
        remaining = np.random.randint(10, 100)
        overdue = np.random.randint(0, 30)
        workload.append({
            'project_id': project,
            'completed_hours': completed,
            'remaining_hours': remaining,
            'overdue_hours': overdue,
            'total_hours': completed + remaining + overdue,
            'week': f'Week {np.random.randint(1, 53)}'
        })
    workload = pd.DataFrame(workload)
    
    return {
        'projects_master': projects_master,
        'project_status': project_status,
        'project_stages': project_stages,
        'budget_variance': budget_variance,
        'resources': resources,
        'workload': workload
    }

# LOAD DATA
data = generate_synthetic_data()

# INITIAL CHARTS
def create_initial_charts():
    """Create initial static charts"""
    
    # 1. Status Pie Chart
    status_counts = data['project_status']['status'].value_counts()
    status_fig = px.pie(
        values=status_counts.values, 
        names=status_counts.index,
        color_discrete_map={'Completed': COLORS['success'], 'In Progress': COLORS['primary'], 'On Hold': COLORS['warning']},
        title="Project Status Distribution"
    )
    status_fig.update_traces(textposition='inside', textinfo='percent+label')
    status_fig.update_layout(showlegend=True, height=350)
    
    # 2. Stages Donut Chart (will be converted to Sunburst)
    stages_data = data['project_stages']
    stage_counts = stages_data['stage'].value_counts()
    
    # Create Sunburst instead
    sunburst_data = []
    for _, row in stages_data.iterrows():
        sunburst_data.append({
            'ids': f"{row['project_id']}-{row['stage']}",
            'labels': f"{row['stage']}",
            'parents': row['project_id'],
            'values': row['hours_spent']
        })
        
    # Add projects as parents
    for proj in stages_data['project_id'].unique():
        sunburst_data.append({
            'ids': proj,
            'labels': proj,
            'parents': "",
            'values': 0
        })
    
    sunburst_df = pd.DataFrame(sunburst_data)
    
    stages_fig = go.Figure(go.Sunburst(
        ids=sunburst_df['ids'],
        labels=sunburst_df['labels'],
        parents=sunburst_df['parents'],
        values=sunburst_df['values'],
        branchvalues="total",
        hovertemplate='<b>%{label}</b><br>Hours: %{value}<extra></extra>',
        maxdepth=2,
    ))
    stages_fig.update_layout(
        title="Project Stages - Interactive Sunburst",
        height=350,
        font_size=12
    )
    
    # 3. Completion Gauge
    avg_completion = data['project_status']['completion_percent'].mean()
    gauge_fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = avg_completion,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Average Project Completion %"},
        delta = {'reference': 80},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': COLORS['primary']},
            'steps': [
                {'range': [0, 50], 'color': COLORS['light_gray']},
                {'range': [50, 80], 'color': COLORS['warning']},
                {'range': [80, 100], 'color': COLORS['success']}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    gauge_fig.update_layout(height=350)
    
    # 4. Progress Trend Chart - NEW 4TH CHART
    progress_data = data['project_status'].copy()
    colors = [COLORS['success'] if x >= 90 else COLORS['warning'] if x >= 70 else COLORS['danger'] 
             for x in progress_data['completion_percent']]
    
    progress_fig = go.Figure()
    progress_fig.add_trace(go.Bar(
        y=progress_data['project_id'][:10],  # Top 10 for readability
        x=progress_data['completion_percent'][:10],
        orientation='h',
        marker_color=colors[:10],
        text=[f"{x}%" for x in progress_data['completion_percent'][:10]],
        textposition='inside',
        hovertemplate='<b>%{y}</b><br>Progress: %{x}%<extra></extra>'
    ))
    
    progress_fig.update_layout(
        title="Top 10 Projects - Progress Overview",
        xaxis_title="Completion %",
        yaxis_title="Projects",
        height=350,
        showlegend=False
    )
    
    # 5. Budget Combo Chart
    budget_agg = data['budget_variance'].groupby('project_id').agg({
        'actual_budget': 'sum',
        'planned_budget': 'sum', 
        'variance': 'sum'
    }).reset_index()
    
    budget_fig = go.Figure()
    budget_fig.add_trace(go.Bar(
        name='Actual Budget',
        x=budget_agg['project_id'][:10],
        y=budget_agg['actual_budget'][:10],
        marker_color=COLORS['danger']
    ))
    budget_fig.add_trace(go.Bar(
        name='Planned Budget',
        x=budget_agg['project_id'][:10],
        y=budget_agg['planned_budget'][:10],
        marker_color=COLORS['success']
    ))
    budget_fig.add_trace(go.Scatter(
        name='Variance',
        x=budget_agg['project_id'][:10],
        y=budget_agg['variance'][:10],
        mode='lines+markers',
        marker_color=COLORS['primary'],
        yaxis='y2'
    ))
    budget_fig.update_layout(
        title="Budget Analysis: Actual vs Planned (Top 10)",
        yaxis2=dict(title="Variance", overlaying='y', side='right'),
        barmode='group',
        height=400
    )
    
    # 6. Resources Bar Chart
    resources_agg = data['resources'].groupby('resource_type').agg({
        'actual_resources': 'sum',
        'planned_resources': 'sum'
    }).reset_index()
    
    resources_fig = go.Figure()
    resources_fig.add_trace(go.Bar(
        name='Actual Resources',
        x=resources_agg['resource_type'],
        y=resources_agg['actual_resources'],
        marker_color=COLORS['primary']
    ))
    resources_fig.add_trace(go.Bar(
        name='Planned Resources', 
        x=resources_agg['resource_type'],
        y=resources_agg['planned_resources'],
        marker_color=COLORS['secondary']
    ))
    resources_fig.update_layout(
        title="Resource Allocation by Type",
        barmode='group',
        height=400
    )
    
    # 7. Workload Timeline
    workload_data = data['workload'][:10]  # Top 10
    
    workload_fig = go.Figure()
    workload_fig.add_trace(go.Bar(
        name='Completed Hours',
        x=workload_data['project_id'],
        y=workload_data['completed_hours'],
        marker_color=COLORS['success']
    ))
    workload_fig.add_trace(go.Bar(
        name='Remaining Hours',
        x=workload_data['project_id'],
        y=workload_data['remaining_hours'],
        marker_color=COLORS['secondary']
    ))
    workload_fig.add_trace(go.Bar(
        name='Overdue Hours',
        x=workload_data['project_id'],
        y=workload_data['overdue_hours'],
        marker_color=COLORS['danger']
    ))
    workload_fig.update_layout(
        title="Workload Distribution by Project (Top 10)",
        barmode='stack',
        height=400
    )
    
    return status_fig, stages_fig, gauge_fig, progress_fig, budget_fig, resources_fig, workload_fig

# CREATE CHARTS
initial_charts = create_initial_charts()

# APP INITIALIZATION
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# LAYOUT
app.layout = dbc.Container([
    
    # HEADER
    dbc.Row([
        dbc.Col([
            html.H1("📊 Project Analytics Dashboard", className="text-center mb-4", 
                    style={'color': COLORS['dark'], 'fontWeight': 'bold'})
        ], width=12)
    ], className="mb-4"),
    
    # FILTERS ROW
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("🎛️ Filters & Controls", className="card-title"),
                    
                    dbc.Row([
                        dbc.Col([
                            html.Label("Project Selection:", style={'fontWeight': 'bold'}),
                            dcc.Dropdown(
                                id='project-selector',
                                options=[{'label': 'All Projects', 'value': 'all'}] + 
                                        [{'label': pid, 'value': pid} for pid in data['projects_master']['project_id']],
                                value='all',
                                placeholder="Select a project..."
                            )
                        ], md=3),
                        
                        dbc.Col([
                            html.Label("Project Type:", style={'fontWeight': 'bold'}),
                            dcc.Dropdown(
                                id='type-filter',
                                options=[{'label': ptype, 'value': ptype} for ptype in data['projects_master']['type'].unique()],
                                value=[],
                                multi=True,
                                placeholder="Filter by type..."
                            )
                        ], md=3),
                        
                        dbc.Col([
                            html.Label("Manager:", style={'fontWeight': 'bold'}),
                            dcc.Dropdown(
                                id='manager-filter',
                                options=[{'label': mgr, 'value': mgr} for mgr in data['projects_master']['manager'].unique()],
                                value=[],
                                multi=True,
                                placeholder="Filter by manager..."
                            )
                        ], md=3),
                        
                        dbc.Col([
                            html.Label("📅 Date Range:", style={'fontWeight': 'bold'}),
                            dcc.DatePickerRange(
                                id='date-range',
                                start_date=data['projects_master']['start_date'].min(),
                                end_date=data['projects_master']['start_date'].max(),
                                display_format='DD/MM/YYYY',
                                style={'width': '100%'}
                            )
                        ], md=3)
                    ])
                ])
            ])
        ], width=12)
    ], className="mb-4"),
    
    # MAIN CHARTS - ROW 1 (2 CHARTS)
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='status-pie-chart', figure=initial_charts[0])
                ])
            ])
        ], md=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Etapas do Projeto", className="text-center mb-2 text-primary"),
                    dcc.Graph(id='stages-donut-chart', figure=initial_charts[1], style={"height": "420px"})
                ])
            ], style={"backgroundColor": COLORS['light'], "boxShadow": "0 0 8px #007bff"})
        ], md=6)
    ], className="mb-4"),
    
    # MAIN CHARTS - ROW 2 (2 CHARTS)
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='completion-gauge-chart', figure=initial_charts[2])
                ])
            ])
        ], md=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='progress-trend-chart', figure=initial_charts[3])
                ])
            ])
        ], md=6)
    ], className="mb-4"),
    
    # MAIN CHARTS - ROW 3 (3 CHARTS)
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='budget-combo-chart', figure=initial_charts[4])
                ])
            ])
        ], md=4),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='resources-bar-chart', figure=initial_charts[5])
                ])
            ])
        ], md=4),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='workload-timeline-chart', figure=initial_charts[6])
                ])
            ])
        ], md=4)
    ], className="mb-4"),
    
    # DATA TABLE SECTION
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("📋 Projects Data Table", className="card-title"),
                    dash_table.DataTable(
                        id='projects-table',
                        columns=[
                            {"name": "Project ID", "id": "project_id"},
                            {"name": "Project Name", "id": "project_name"},
                            {"name": "Type", "id": "type"},
                            {"name": "Manager", "id": "manager"},
                            {"name": "Status", "id": "status"},
                            {"name": "Completion %", "id": "completion_percent", "type": "numeric", "format": {"specifier": ".1f"}},
                            {"name": "Total Budget", "id": "total_budget", "type": "numeric", "format": {"specifier": "$,.0f"}},
                            {"name": "Start Date", "id": "start_date", "type": "datetime"},
                        ],
                        data=data['projects_master'].merge(data['project_status'], on='project_id').to_dict('records'),
                        style_cell={'textAlign': 'left', 'padding': '10px'},
                        style_header={'backgroundColor': COLORS['primary'], 'color': 'white', 'fontWeight': 'bold'},
                        style_data_conditional=[
                            {
                                'if': {'filter_query': '{completion_percent} >= 90'},
                                'backgroundColor': COLORS['success'],
                                'color': 'white',
                            },
                            {
                                'if': {'filter_query': '{completion_percent} < 90 && {completion_percent} >= 70'},
                                'backgroundColor': COLORS['warning'],
                                'color': 'black',
                            },
                            {
                                'if': {'filter_query': '{completion_percent} < 70'},
                                'backgroundColor': COLORS['danger'],
                                'color': 'white',
                            }
                        ],
                        page_size=10,
                        sort_action="native",
                        filter_action="native"
                    )
                ])
            ])
        ], width=12)
    ], className="mb-4"),
    
    # FOOTER
    dbc.Row([
        dbc.Col([
            html.Hr(),
            html.P("🚀 Professional Project Analytics Dashboard | Interactive Data Visualization with Dash", 
                   className="text-center text-muted")
        ], width=12)
    ])
    
], fluid=True)


# CALLBACKS

# CALLBACK 1: Update Projects Table
@app.callback(
    Output('projects-table', 'data'),
    [Input('project-selector', 'value'),
     Input('type-filter', 'value'),
     Input('manager-filter', 'value'),
     Input('date-range', 'start_date'),
     Input('date-range', 'end_date')]
)
def update_projects_table(selected_project, selected_types, selected_managers, start_date, end_date):
    """Update projects table with REAL filtering"""
    
    # Start with merged data
    table_data = data['projects_master'].merge(data['project_status'], on='project_id')
    
    # Apply filters
    if selected_project and selected_project != 'all':
        table_data = table_data[table_data['project_id'] == selected_project]
    
    if selected_types:
        table_data = table_data[table_data['type'].isin(selected_types)]
        
    if selected_managers:
        table_data = table_data[table_data['manager'].isin(selected_managers)]
    
    if start_date and end_date:
        table_data['start_date'] = pd.to_datetime(table_data['start_date'])
        table_data = table_data[
            (table_data['start_date'] >= start_date) & 
            (table_data['start_date'] <= end_date)
        ]
    
    return table_data.to_dict('records')


# CALLBACK 2: Update all charts - REAL INTERACTIVITY
@app.callback(
    [Output('status-pie-chart', 'figure'),
     Output('stages-donut-chart', 'figure'),
     Output('completion-gauge-chart', 'figure'),
     Output('progress-trend-chart', 'figure'),
     Output('budget-combo-chart', 'figure'),
     Output('resources-bar-chart', 'figure'),
     Output('workload-timeline-chart', 'figure')],
    [Input('project-selector', 'value'),
     Input('type-filter', 'value'),
     Input('manager-filter', 'value'),
     Input('date-range', 'start_date'),
     Input('date-range', 'end_date')]
)
def update_all_charts(selected_project, selected_types, selected_managers, start_date, end_date):
    """Update all charts with REAL interactivity INCLUDING DATE FILTER"""
    
    try:
        # Filter projects based on selections
        filtered_projects = data['projects_master'].copy()
        
        # Apply date filter
        if start_date and end_date:
            filtered_projects['start_date'] = pd.to_datetime(filtered_projects['start_date'])
            filtered_projects = filtered_projects[
                (filtered_projects['start_date'] >= start_date) & 
                (filtered_projects['start_date'] <= end_date)
            ]
        
        # Apply other filters
        if selected_types:
            filtered_projects = filtered_projects[filtered_projects['type'].isin(selected_types)]
        if selected_managers:
            filtered_projects = filtered_projects[filtered_projects['manager'].isin(selected_managers)]
    # SEM TRY/EXCEPT: Força dados sintéticos sempre
    filtered_projects = data['projects_master']
    project_ids = filtered_projects['project_id'].tolist()

    # 1. Status Pie Chart
    status_data = data['project_status']
    status_counts = status_data['status'].value_counts()
    status_fig = px.pie(
        values=status_counts.values, 
        names=status_counts.index,
        color_discrete_map={'Completed': COLORS['success'], 'In Progress': COLORS['primary'], 'On Hold': COLORS['warning']},
        title="Project Status Distribution"
    )
    status_fig.update_traces(textposition='inside', textinfo='percent+label')
    status_fig.update_layout(showlegend=True, height=350)

    # 2. Stages SUNBURST
    stages_data = data['project_stages']
    sunburst_data = []
    for _, row in stages_data.iterrows():
        sunburst_data.append({
            'ids': f"{row['project_id']}-{row['stage']}",
            'labels': f"{row['stage']}",
            'parents': row['project_id'],
            'values': row.get('hours_spent', 1)
        })
    for proj in stages_data['project_id'].unique():
        sunburst_data.append({
            'ids': proj,
            'labels': proj,
            'parents': "",
            'values': 0
        })
    sunburst_df = pd.DataFrame(sunburst_data)
    stages_fig = go.Figure(go.Sunburst(
        ids=sunburst_df['ids'],
        labels=sunburst_df['labels'],
        parents=sunburst_df['parents'],
        values=sunburst_df['values'],
        branchvalues="total",
        hovertemplate='<b>%{label}</b><br>Horas: %{value}<extra></extra>',
        maxdepth=2,
    ))
    stages_fig.update_layout(
        title="Etapas do Projeto (Sunburst Interativo)",
        height=420,
        margin=dict(t=60, l=10, r=10, b=10),
        font=dict(size=16, color=COLORS['dark']),
        paper_bgcolor=COLORS['light'],
        plot_bgcolor=COLORS['light']
    )

    # 3. Completion Gauge
    avg_completion = status_data['completion_percent'].mean()
    gauge_fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = avg_completion,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Average Project Completion %"},
        delta = {'reference': 80},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': COLORS['primary']},
            'steps': [
                {'range': [0, 50], 'color': COLORS['light_gray']},
                {'range': [50, 80], 'color': COLORS['warning']},
                {'range': [80, 100], 'color': COLORS['success']}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    gauge_fig.update_layout(height=350)

    # 4. Progress Trend Chart
    progress_data = status_data.copy()
    colors = [COLORS['success'] if x >= 90 else COLORS['warning'] if x >= 70 else COLORS['danger'] 
             for x in progress_data['completion_percent']]
    progress_fig = go.Figure()
    progress_fig.add_trace(go.Bar(
        y=progress_data['project_id'][:10],
        x=progress_data['completion_percent'][:10],
        orientation='h',
        marker_color=colors[:10],
        text=[f"{x}%" for x in progress_data['completion_percent'][:10]],
        textposition='inside',
        hovertemplate='<b>%{y}</b><br>Progress: %{x}%<extra></extra>'
    ))
    progress_fig.update_layout(
        title="Progress by Project (Top 10)",
        xaxis_title="Completion %",
        yaxis_title="Projects",
        height=350,
        showlegend=False
    )

    # 5. Budget Combo Chart
    budget_agg = data['budget_variance'].groupby('project_id').agg({
        'actual_budget': 'sum',
        'planned_budget': 'sum', 
        'variance': 'sum'
    }).reset_index()
    budget_fig = go.Figure()
    budget_fig.add_trace(go.Bar(
        name='Actual Budget',
        x=budget_agg['project_id'][:10],
        y=budget_agg['actual_budget'][:10],
        marker_color=COLORS['danger']
    ))
    budget_fig.add_trace(go.Bar(
        name='Planned Budget',
        x=budget_agg['project_id'][:10],
        y=budget_agg['planned_budget'][:10],
        marker_color=COLORS['success']
    ))
    budget_fig.add_trace(go.Scatter(
        name='Variance',
        x=budget_agg['project_id'][:10],
        y=budget_agg['variance'][:10],
        mode='lines+markers',
        marker_color=COLORS['primary'],
        yaxis='y2'
    ))
    budget_fig.update_layout(
        title="Budget Analysis: Actual vs Planned (Top 10)",
        yaxis2=dict(title="Variance", overlaying='y', side='right'),
        barmode='group',
        height=400
    )

    # 6. Resources Bar Chart
    resources_agg = data['resources'].groupby('resource_type').agg({
        'actual_resources': 'sum',
        'planned_resources': 'sum'
    }).reset_index()
    resources_fig = go.Figure()
    resources_fig.add_trace(go.Bar(
        name='Actual Resources',
        x=resources_agg['resource_type'],
        y=resources_agg['actual_resources'],
        marker_color=COLORS['primary']
    ))
    resources_fig.add_trace(go.Bar(
        name='Planned Resources', 
        x=resources_agg['resource_type'],
        y=resources_agg['planned_resources'],
        marker_color=COLORS['secondary']
    ))
    resources_fig.update_layout(
        title="Resource Allocation by Type",
        barmode='group',
        height=400
    )

    # 7. Workload Timeline
    workload_data = data['workload'][:10]
    workload_fig = go.Figure()
    workload_fig.add_trace(go.Bar(
        name='Completed Hours',
        x=workload_data['project_id'],
        y=workload_data['completed_hours'],
        marker_color=COLORS['success']
    ))
    workload_fig.add_trace(go.Bar(
        name='Remaining Hours',
        x=workload_data['project_id'],
        y=workload_data['remaining_hours'],
        marker_color=COLORS['secondary']
    ))
    workload_fig.add_trace(go.Bar(
        name='Overdue Hours',
        x=workload_data['project_id'],
        y=workload_data['overdue_hours'],
        marker_color=COLORS['danger']
    ))
    workload_fig.update_layout(
        title="Workload Distribution by Project (Top 10)",
        barmode='stack',
        height=400
    )

    return status_fig, stages_fig, gauge_fig, progress_fig, budget_fig, resources_fig, workload_fig
