# scripts/viz.py - Construction Project Management Dashboard Visualization
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import datetime as dt
import os
import sys

# Orange corporate theme colors (matching construction reference)
COLORS = {
    'primary': '#FF6B35',      # Orange primary
    'secondary': '#FF8C69',    # Light orange
    'accent': '#FF4500',       # Dark orange
    'success': '#28a745',
    'warning': '#ffc107',
    'danger': '#dc3545',
    'info': '#17a2b8',
    'light': '#f8f9fa',
    'dark': '#343a40',
    'white': '#ffffff'
}

def load_data():
    """Load construction project data from CSV files"""
    try:
        df_projects_master = pd.read_csv('data/projects_master.csv')
        df_project_status = pd.read_csv('data/project_status.csv')
        df_project_stages = pd.read_csv('data/project_stages.csv')
        df_budget_variance = pd.read_csv('data/budget_variance.csv')
        df_resources = pd.read_csv('data/resources.csv')
        df_workload = pd.read_csv('data/workload.csv')
        
        # Convert date columns
        df_projects_master['start_date'] = pd.to_datetime(df_projects_master['start_date'])
        df_projects_master['planned_end_date'] = pd.to_datetime(df_projects_master['planned_end_date'])
        
        return df_projects_master, df_project_status, df_project_stages, df_budget_variance, df_resources, df_workload
        
    except FileNotFoundError:
        print("Data files not found. Running data generation...")
        sys.path.insert(0, 'scripts')
        from data_gen import generate_construction_projects
        return generate_construction_projects(30)

def create_gauge_chart(value, title, range_max=100, color=COLORS['primary']):
    """Create a gauge chart for KPIs"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title, 'font': {'size': 16, 'color': COLORS['dark']}},
        delta = {'reference': range_max * 0.8},
        gauge = {
            'axis': {'range': [None, range_max], 'tickcolor': COLORS['dark']},
            'bar': {'color': color},
            'steps': [
                {'range': [0, range_max * 0.5], 'color': COLORS['light']},
                {'range': [range_max * 0.5, range_max * 0.8], 'color': '#E0E0E0'}
            ],
            'threshold': {
                'line': {'color': COLORS['danger'], 'width': 4},
                'thickness': 0.75,
                'value': range_max * 0.9
            }
        }
    ))
    
    fig.update_layout(
        height=250,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor='white',
        font={'color': COLORS['dark'], 'family': 'Segoe UI'}
    )
    return fig

def create_donut_chart(data, values, names, title, colors=None):
    """Create a donut chart"""
    if colors is None:
        colors = [COLORS['primary'], COLORS['secondary'], COLORS['accent'], COLORS['warning']]
    
    fig = px.pie(
        values=values, 
        names=names,
        hole=0.4,
        color_discrete_sequence=colors
    )
    
    fig.update_traces(
        textposition='outside',
        textinfo='percent+label',
        marker=dict(line=dict(color='white', width=2)),
        hovertemplate='<b>%{label}</b><br>%{value}<br>%{percent}<extra></extra>'
    )
    
    fig.update_layout(
        title={'text': title, 'x': 0.5, 'font': {'size': 16, 'color': COLORS['dark']}},
        height=250,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor='white',
        font={'color': COLORS['dark'], 'family': 'Segoe UI'},
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    return fig

def create_combination_chart(df_budget):
    """Create combination chart for budget variance (bars + line)"""
    # Aggregate monthly data
    monthly_data = df_budget.groupby('month').agg({
        'actual_budget': 'sum',
        'planned_budget': 'sum'
    }).reset_index()
    
    monthly_data['variance_pct'] = ((monthly_data['actual_budget'] - monthly_data['planned_budget']) / monthly_data['planned_budget'] * 100)
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add bars for budget amounts
    fig.add_trace(
        go.Bar(x=monthly_data['month'], y=monthly_data['planned_budget'], 
               name='Planned Budget', marker_color=COLORS['primary'], opacity=0.7),
        secondary_y=False,
    )
    
    fig.add_trace(
        go.Bar(x=monthly_data['month'], y=monthly_data['actual_budget'], 
               name='Actual Budget', marker_color=COLORS['accent'], opacity=0.7),
        secondary_y=False,
    )
    
    # Add variance line
    fig.add_trace(
        go.Scatter(x=monthly_data['month'], y=monthly_data['variance_pct'],
                   mode='lines+markers', name='Variance %', 
                   line=dict(color=COLORS['danger'], width=3),
                   marker=dict(size=8)),
        secondary_y=True,
    )
    
    # Update y-axes titles
    fig.update_yaxes(title_text="Budget Amount ($)", secondary_y=False, titlefont=dict(color=COLORS['dark']))
    fig.update_yaxes(title_text="Variance (%)", secondary_y=True, titlefont=dict(color=COLORS['danger']))
    
    fig.update_layout(
        title={'text': 'Budget Variance', 'x': 0.5, 'font': {'size': 16, 'color': COLORS['dark']}},
        height=300,
        margin=dict(l=40, r=40, t=40, b=40),
        paper_bgcolor='white',
        barmode='group',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        font={'color': COLORS['dark'], 'family': 'Segoe UI'}
    )
    
    return fig

# Initialize Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])
server = app.server

# Load data
df_projects_master, df_project_status, df_project_stages, df_budget_variance, df_resources, df_workload = load_data()

# Merge data for easier access
df_main = df_projects_master.merge(df_project_status, on='project_id').merge(df_project_stages, on='project_id')

# Calculate KPIs
total_projects = len(df_main)
total_budget = df_main['budget'].sum()
avg_completion = df_main['completion_percent'].mean()
projects_on_track = len(df_main[df_main['completion_percent'] >= 80])
utilization_ratio = df_main['budget_used'].sum() / df_main['budget'].sum() * 100

# Define app layout
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.H1("Construction Project Monitoring Dashboard", 
                   className="text-center mb-0", 
                   style={'color': COLORS['primary'], 'fontWeight': 'bold'}),
            html.P("Executive Overview of Project Portfolio Performance", 
                   className="text-center text-muted mb-4")
        ])
    ], className="mb-4"),
    
    # Project Selector
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Project Portfolio Filter", className="card-title"),
                    dcc.Dropdown(
                        id='project-selector',
                        options=[{'label': 'All Projects', 'value': 'all'}] + 
                                [{'label': f"{row['project_id']}: {row['name']}", 'value': row['project_id']} 
                                 for _, row in df_projects_master.iterrows()],
                        value='all',
                        className="mb-3"
                    ),
                    html.Div([
                        html.Strong("Portfolio Summary: "),
                        f"{total_projects} Active Projects | Total Budget: ${total_budget:,.0f}"
                    ])
                ])
            ], className="shadow-sm")
        ])
    ], className="mb-4"),
    
    # KPI Cards Row
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Total Projects", className="card-title text-muted"),
                    html.H2(f"{total_projects}", className="text-primary", style={'fontWeight': 'bold'}),
                    html.Small("+3 this month", className="text-success")
                ])
            ], className="text-center shadow-sm h-100")
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Total Budget", className="card-title text-muted"),
                    html.H2(f"${total_budget/1e6:.1f}M", className="text-primary", style={'fontWeight': 'bold'}),
                    html.Small("+12% vs planned", className="text-success")
                ])
            ], className="text-center shadow-sm h-100")
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Avg Completion", className="card-title text-muted"),
                    html.H2(f"{avg_completion:.1f}%", className="text-primary", style={'fontWeight': 'bold'}),
                    html.Small("-2% vs target", className="text-warning")
                ])
            ], className="text-center shadow-sm h-100")
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("On Track", className="card-title text-muted"),
                    html.H2(f"{projects_on_track}/{total_projects}", className="text-primary", style={'fontWeight': 'bold'}),
                    html.Small("80%+ completion", className="text-info")
                ])
            ], className="text-center shadow-sm h-100")
        ], width=3)
    ], className="mb-4"),
    
    # Main Dashboard Grid
    dbc.Row([
        # Left Column
        dbc.Col([
            # Project Work Status (Donut)
            dbc.Card([
                dbc.CardHeader([
                    html.H5("Project Work Status", className="mb-0", style={'fontWeight': 'bold'})
                ]),
                dbc.CardBody([
                    dcc.Graph(id='work-status-donut', config={'displayModeBar': False})
                ])
            ], className="shadow-sm mb-4"),
            
            # Projects by Stage (Pie)
            dbc.Card([
                dbc.CardHeader([
                    html.H5("Projects by Stage", className="mb-0", style={'fontWeight': 'bold'})
                ]),
                dbc.CardBody([
                    dcc.Graph(id='stage-pie', config={'displayModeBar': False})
                ])
            ], className="shadow-sm")
        ], width=4),
        
        # Center Column
        dbc.Col([
            # Project Completion Gauge
            dbc.Card([
                dbc.CardHeader([
                    html.H5("Project Completion", className="mb-0", style={'fontWeight': 'bold'})
                ]),
                dbc.CardBody([
                    dcc.Graph(id='completion-gauge', config={'displayModeBar': False})
                ])
            ], className="shadow-sm mb-4"),
            
            # Utilized Duration Gauge
            dbc.Card([
                dbc.CardHeader([
                    html.H5("Utilized Duration", className="mb-0", style={'fontWeight': 'bold'})
                ]),
                dbc.CardBody([
                    dcc.Graph(id='duration-gauge', config={'displayModeBar': False})
                ])
            ], className="shadow-sm")
        ], width=4),
        
        # Right Column
        dbc.Col([
            # Budget Variance (Combination Chart)
            dbc.Card([
                dbc.CardHeader([
                    html.H5("Budget Variance", className="mb-0", style={'fontWeight': 'bold'})
                ]),
                dbc.CardBody([
                    dcc.Graph(id='budget-combination', config={'displayModeBar': False}, style={'height': '540px'})
                ])
            ], className="shadow-sm")
        ], width=4)
    ], className="mb-4"),
    
    # Bottom Row
    dbc.Row([
        # Actual vs Planned Resources
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5("Actual vs Planned Resources", className="mb-0", style={'fontWeight': 'bold'})
                ]),
                dbc.CardBody([
                    dcc.Graph(id='resources-bar', config={'displayModeBar': False})
                ])
            ], className="shadow-sm")
        ], width=6),
        
        # Workload (Stacked Horizontal Bar)
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5("Workload Distribution", className="mb-0", style={'fontWeight': 'bold'})
                ]),
                dbc.CardBody([
                    dcc.Graph(id='workload-bar', config={'displayModeBar': False})
                ])
            ], className="shadow-sm")
        ], width=6)
    ], className="mb-4"),
    
    # Footer
    html.Hr(),
    html.P("Construction Project Monitoring Dashboard | Executive Level | Real-time Data", 
           className="text-center text-muted small")
    
], fluid=True, style={'backgroundColor': COLORS['light']})

# Callbacks for interactivity
@callback(
    [Output('work-status-donut', 'figure'),
     Output('stage-pie', 'figure'),
     Output('completion-gauge', 'figure'),
     Output('duration-gauge', 'figure'),
     Output('budget-combination', 'figure'),
     Output('resources-bar', 'figure'),
     Output('workload-bar', 'figure')],
    [Input('project-selector', 'value')]
)
def update_charts(selected_project):
    # Filter data based on selection
    if selected_project == 'all':
        filtered_main = df_main
        filtered_budget = df_budget_variance
        filtered_resources = df_resources
        filtered_workload = df_workload
    else:
        filtered_main = df_main[df_main['project_id'] == selected_project]
        filtered_budget = df_budget_variance[df_budget_variance['project_id'] == selected_project]
        filtered_resources = df_resources[df_resources['project_id'] == selected_project]
        filtered_workload = df_workload[df_workload['project_id'] == selected_project]
    
    # 1. Work Status Donut
    status_counts = filtered_main['status'].value_counts()
    work_status_fig = create_donut_chart(
        None, status_counts.values, status_counts.index, 
        "Project Work Status",
        [COLORS['success'], COLORS['warning'], COLORS['danger'], COLORS['info']]
    )
    
    # 2. Stage Pie Chart
    stage_counts = filtered_main['stage'].value_counts()
    stage_fig = create_donut_chart(
        None, stage_counts.values, stage_counts.index,
        "Projects by Stage",
        [COLORS['primary'], COLORS['secondary'], COLORS['accent'], COLORS['warning'], COLORS['info']]
    )
    
    # 3. Completion Gauge
    avg_completion = filtered_main['completion_percent'].mean()
    completion_gauge = create_gauge_chart(avg_completion, "Avg Completion %", 100, COLORS['primary'])
    
    # 4. Duration Gauge
    avg_duration_used = (filtered_main['days_used'] / filtered_main['duration_days'] * 100).mean()
    duration_gauge = create_gauge_chart(avg_duration_used, "Duration Utilized %", 100, COLORS['accent'])
    
    # 5. Budget Combination Chart
    budget_combination_fig = create_combination_chart(filtered_budget)
    
    # 6. Resources Bar Chart
    resources_agg = filtered_resources.groupby('resource_type').agg({
        'actual_resources': 'sum',
        'planned_resources': 'sum'
    }).reset_index()
    
    resources_fig = go.Figure()
    resources_fig.add_trace(go.Bar(
        x=resources_agg['resource_type'],
        y=resources_agg['planned_resources'],
        name='Planned',
        marker_color=COLORS['primary'],
        opacity=0.7
    ))
    resources_fig.add_trace(go.Bar(
        x=resources_agg['resource_type'],
        y=resources_agg['actual_resources'],
        name='Actual',
        marker_color=COLORS['accent'],
        opacity=0.7
    ))
    
    resources_fig.update_layout(
        title={'text': 'Actual vs Planned Resources', 'x': 0.5, 'font': {'size': 16, 'color': COLORS['dark']}},
        barmode='group',
        height=300,
        margin=dict(l=40, r=40, t=40, b=40),
        paper_bgcolor='white',
        font={'color': COLORS['dark'], 'family': 'Segoe UI'},
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
    )
    
    # 7. Workload Stacked Horizontal Bar
    workload_agg = filtered_workload.agg({
        'completed_hours': 'sum',
        'remaining_hours': 'sum',
        'overdue_hours': 'sum'
    })
    
    workload_fig = go.Figure()
    workload_fig.add_trace(go.Bar(
        x=[workload_agg['completed_hours']],
        y=['Project Hours'],
        name='Completed',
        orientation='h',
        marker_color=COLORS['success']
    ))
    workload_fig.add_trace(go.Bar(
        x=[workload_agg['remaining_hours']],
        y=['Project Hours'],
        name='Remaining',
        orientation='h',
        marker_color=COLORS['warning']
    ))
    workload_fig.add_trace(go.Bar(
        x=[workload_agg['overdue_hours']],
        y=['Project Hours'],
        name='Overdue',
        orientation='h',
        marker_color=COLORS['danger']
    ))
    
    workload_fig.update_layout(
        title={'text': 'Workload Distribution', 'x': 0.5, 'font': {'size': 16, 'color': COLORS['dark']}},
        barmode='stack',
        height=300,
        margin=dict(l=40, r=40, t=40, b=40),
        paper_bgcolor='white',
        font={'color': COLORS['dark'], 'family': 'Segoe UI'},
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        xaxis_title="Hours"
    )
    
    return work_status_fig, stage_fig, completion_gauge, duration_gauge, budget_combination_fig, resources_fig, workload_fig

# Custom CSS styling
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Construction Project Monitoring Dashboard</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                font-family: 'Segoe UI', Roboto, sans-serif;
                background-color: #f8f9fa;
            }
            .card {
                border: none;
                border-radius: 8px;
            }
            .shadow-sm {
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1) !important;
            }
            .card-header {
                background-color: white;
                border-bottom: 1px solid #dee2e6;
                font-weight: bold;
            }
            h1, h2, h3, h4, h5 {
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

if __name__ == '__main__':
    # Ensure output directory exists
    if not os.path.exists('outputs'):
        os.makedirs('outputs')
    
    # For development, run the server
    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        app.run(debug=True, port=8050)
    else:
        # Generate static HTML
        print("Generating static HTML dashboard...")
        
        # Save the dashboard HTML
        html_content = app.index_string.format(
            metas='<meta charset="UTF-8">',
            title='Construction Project Monitoring Dashboard',
            favicon='',
            css='',
            app_entry='<div>Dashboard generated successfully. Run with debug flag to view interactively.</div>',
            config='',
            scripts='',
            renderer=''
        )
        
        with open('outputs/dashboard.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("Dashboard HTML saved to outputs/dashboard.html")
        print("To run interactively, use: python scripts/viz.py debug")