# ENHANCED VISUALIZATION SCRIPT - IMPROVED INTERACTIVE DASHBOARD
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
from datetime import datetime, timedelta
from functools import lru_cache

# PROFESSIONAL COLOR SCHEME
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

# ENHANCED DATA GENERATION WITH TOOLTIP SUPPORT
def generate_enhanced_data():
    """Generate comprehensive data with enhanced tooltip information"""
    
    np.random.seed(42)
    
    # Projects Master Data with Enhanced Fields
    project_ids = [f'PROJ_{i:03d}' for i in range(1, 31)]
    projects_master = pd.DataFrame({
        'project_id': project_ids,
        'project_name': [f'Construction Project {i}' for i in range(1, 31)],
        'type': np.random.choice(['Residential', 'Commercial', 'Infrastructure', 'Industrial', 'Public Works'], 30),
        'manager': np.random.choice(['John Smith', 'Maria Garcia', 'David Wilson', 'Sarah Johnson', 'Michael Brown'], 30),
        'start_date': pd.date_range(start='2023-01-01', periods=30, freq='15D')[:30],
        'end_date': pd.date_range(start='2024-01-01', periods=30, freq='20D')[:30],
        'priority': np.random.choice(['High', 'Medium', 'Low'], 30),
        'total_budget': np.random.uniform(50000, 500000, 30).round(2),
        'location': np.random.choice(['Downtown', 'Suburbs', 'Industrial District', 'Waterfront', 'City Center'], 30),
        'contractor': np.random.choice(['BuildCorp Ltd', 'Mega Construction', 'Elite Builders', 'ProBuild Inc', 'Urban Development'], 30)
    })
    
    # Enhanced Project Status with Additional Metrics
    project_status = pd.DataFrame({
        'project_id': project_ids,
        'status': np.random.choice(['Completed', 'In Progress', 'On Hold', 'Planning'], 30, p=[0.3, 0.4, 0.1, 0.2]),
        'completion_percent': np.random.uniform(20, 100, 30).round(1),
        'last_updated': pd.date_range(start='2024-01-01', periods=30, freq='D'),
        'quality_score': np.random.uniform(7.0, 10.0, 30).round(1),
        'safety_incidents': np.random.randint(0, 5, 30),
        'days_ahead_behind': np.random.randint(-30, 15, 30)
    })
    
    # Enhanced Project Stages with Detailed Information
    stages = ['Planning', 'Foundation', 'Structure', 'MEP Installation', 'Finishing', 'Inspection']
    project_stages = []
    for project in project_ids[:20]:  # 20 projects for variety
        for stage in np.random.choice(stages, np.random.randint(3, 6), replace=False):
            project_stages.append({
                'project_id': project,
                'stage': stage,
                'status': np.random.choice(['Completed', 'In Progress', 'Pending', 'Delayed']),
                'hours_spent': np.random.randint(50, 500),
                'planned_hours': np.random.randint(100, 600),
                'cost': np.random.uniform(5000, 50000),
                'workers_assigned': np.random.randint(3, 15)
            })
    project_stages = pd.DataFrame(project_stages)
    
    # Enhanced Budget Variance with Detailed Breakdown
    budget_variance = []
    for project in project_ids:
        budget = projects_master[projects_master['project_id'] == project]['total_budget'].iloc[0]
        actual = budget * np.random.uniform(0.8, 1.3)
        variance_pct = ((actual - budget) / budget) * 100
        budget_variance.append({
            'project_id': project,
            'planned_budget': budget,
            'actual_budget': actual,
            'variance': actual - budget,
            'variance_percent': variance_pct,
            'month': np.random.choice(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']),
            'category': np.random.choice(['Materials', 'Labor', 'Equipment', 'Overhead']),
            'approval_status': np.random.choice(['Approved', 'Pending', 'Rejected'], p=[0.7, 0.2, 0.1])
        })
    budget_variance = pd.DataFrame(budget_variance)
    
    # Enhanced Resources with Skills and Availability
    resource_types = ['Civil Engineers', 'Architects', 'Project Managers', 'Construction Workers', 'Equipment Operators', 'Quality Inspectors']
    resources = []
    for project in project_ids[:25]:  # 25 projects
        for resource_type in np.random.choice(resource_types, np.random.randint(3, 5), replace=False):
            planned = np.random.randint(3, 15)
            actual = np.random.randint(1, 18)
            efficiency = (actual / planned) * np.random.uniform(0.8, 1.2)
            resources.append({
                'project_id': project,
                'resource_type': resource_type,
                'planned_resources': planned,
                'actual_resources': actual,
                'efficiency_score': efficiency,
                'cost_per_hour': np.random.uniform(25, 150),
                'allocation_date': pd.date_range(start='2024-01-01', periods=1, freq='D')[0],
                'skill_level': np.random.choice(['Junior', 'Mid', 'Senior', 'Expert'])
            })
    resources = pd.DataFrame(resources)
    
    # Enhanced Workload with Performance Metrics
    workload = []
    for project in project_ids:
        completed = np.random.randint(100, 800)
        remaining = np.random.randint(50, 400)
        overdue = np.random.randint(0, 100)
        productivity = completed / (completed + remaining + overdue)
        workload.append({
            'project_id': project,
            'completed_hours': completed,
            'remaining_hours': remaining,
            'overdue_hours': overdue,
            'productivity_index': productivity,
            'team_size': np.random.randint(5, 25),
            'overtime_hours': np.random.randint(0, 200),
            'milestone_completion': np.random.randint(60, 100)
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

# ENHANCED VISUALIZATION FUNCTIONS WITH COMPREHENSIVE TOOLTIPS
def create_enhanced_charts(data):
    """Create enhanced charts with comprehensive tooltips and interactivity"""
    
    # 1. ENHANCED STATUS PIE CHART
    status_counts = data['project_status']['status'].value_counts()
    merged_status = data['projects_master'].merge(data['project_status'], on='project_id')
    
    status_fig = go.Figure(data=[go.Pie(
        labels=status_counts.index,
        values=status_counts.values,
        hole=0.3,
        hovertemplate=
        '<b>Status: %{label}</b><br>' +
        'Projects: %{value}<br>' +
        'Percentage: %{percent}<br>' +
        'Total Budget: $%{customdata:,.0f}<extra></extra>',
        customdata=[merged_status[merged_status['status'] == status]['total_budget'].sum() 
                   for status in status_counts.index],
        marker=dict(
            colors=[COLORS['success'], COLORS['primary'], COLORS['warning'], COLORS['secondary']],
            line=dict(color='#FFFFFF', width=2)
        ),
        textinfo='label+percent',
        textposition='inside',
        textfont=dict(size=12, color='white')
    )])
    
    status_fig.update_layout(
        title={
            'text': '<b>Project Status Distribution</b>',
            'x': 0.5,
            'font': {'size': 16, 'color': COLORS['dark']}
        },
        height=400,
        showlegend=True,
        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.01),
        margin=dict(t=60, b=20, l=20, r=120)
    )
    
    # 2. ENHANCED SUNBURST CHART
    stages_data = data['project_stages']
    sunburst_data = []
    
    # Create hierarchical data for sunburst
    for _, row in stages_data.iterrows():
        project_info = data['projects_master'][data['projects_master']['project_id'] == row['project_id']].iloc[0]
        sunburst_data.append({
            'ids': f"{row['project_id']}-{row['stage']}",
            'labels': row['stage'],
            'parents': row['project_id'],
            'values': row['hours_spent'],
            'customdata': {
                'project_name': project_info['project_name'],
                'manager': project_info['manager'],
                'status': row['status'],
                'workers': row['workers_assigned'],
                'cost': row['cost'],
                'efficiency': (row['hours_spent'] / row['planned_hours']) * 100 if row['planned_hours'] > 0 else 0
            }
        })
    
    # Add project parents
    for proj in stages_data['project_id'].unique():
        project_info = data['projects_master'][data['projects_master']['project_id'] == proj].iloc[0]
        total_hours = stages_data[stages_data['project_id'] == proj]['hours_spent'].sum()
        sunburst_data.append({
            'ids': proj,
            'labels': proj,
            'parents': "",
            'values': total_hours,
            'customdata': {
                'project_name': project_info['project_name'],
                'manager': project_info['manager'],
                'type': project_info['type'],
                'budget': project_info['total_budget'],
                'location': project_info['location']
            }
        })
    
    sunburst_df = pd.DataFrame(sunburst_data)
    
    stages_fig = go.Figure(go.Sunburst(
        ids=sunburst_df['ids'],
        labels=sunburst_df['labels'],
        parents=sunburst_df['parents'],
        values=sunburst_df['values'],
        branchvalues="total",
        hovertemplate=
        '<b>%{label}</b><br>' +
        'Hours Spent: %{value:,.0f}<br>' +
        'Percentage of Parent: %{percentParent}<br>' +
        'Percentage of Total: %{percentRoot}<br>' +
        '<extra></extra>',
        maxdepth=2,
        insidetextorientation='radial'
    ))
    
    stages_fig.update_layout(
        title={
            'text': '<b>Project Stages - Interactive Hierarchy</b>',
            'x': 0.5,
            'font': {'size': 16, 'color': COLORS['dark']}
        },
        height=450,
        font_size=11,
        margin=dict(t=60, b=20, l=20, r=20)
    )
    
    # 3. ENHANCED GAUGE CHART
    avg_completion = data['project_status']['completion_percent'].mean()
    projects_on_track = len(data['project_status'][data['project_status']['completion_percent'] >= 80])
    total_projects = len(data['project_status'])
    
    gauge_fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=avg_completion,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={
            'text': '<b>Average Project Completion</b><br><span style="font-size:12px">Target: 85%</span>',
            'font': {'size': 14}
        },
        delta={'reference': 85, 'valueformat': '.1f'},
        number={'suffix': '%', 'font': {'size': 40}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': COLORS['primary'], 'thickness': 0.8},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 50], 'color': COLORS['danger']},
                {'range': [50, 85], 'color': COLORS['warning']},
                {'range': [85, 100], 'color': COLORS['success']}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    gauge_fig.add_annotation(
        text=f"Projects on Track: {projects_on_track}/{total_projects}",
        x=0.5, y=0.1,
        showarrow=False,
        font=dict(size=12, color=COLORS['dark'])
    )
    
    gauge_fig.update_layout(
        height=350,
        margin=dict(t=60, b=60, l=20, r=20)
    )
    
    # 4. ENHANCED BAR CHART - PROJECT PROGRESS
    progress_data = data['project_status'].merge(data['projects_master'], on='project_id')
    progress_data = progress_data.sort_values('completion_percent', ascending=True).head(15)
    
    # Color coding based on status and completion
    colors = []
    for _, row in progress_data.iterrows():
        if row['completion_percent'] >= 90:
            colors.append(COLORS['success'])
        elif row['completion_percent'] >= 70:
            colors.append(COLORS['warning'])
        else:
            colors.append(COLORS['danger'])
    
    progress_fig = go.Figure(data=[go.Bar(
        y=progress_data['project_name'],
        x=progress_data['completion_percent'],
        orientation='h',
        marker_color=colors,
        hovertemplate=
        '<b>%{y}</b><br>' +
        'Progress: %{x}%<br>' +
        'Status: %{customdata[0]}<br>' +
        'Manager: %{customdata[1]}<br>' +
        'Type: %{customdata[2]}<br>' +
        'Budget: $%{customdata[3]:,.0f}<br>' +
        'Days Ahead/Behind: %{customdata[4]:+d}<br>' +
        '<extra></extra>',
        customdata=progress_data[['status', 'manager', 'type', 'total_budget', 'days_ahead_behind']].values,
        text=[f"{x:.1f}%" for x in progress_data['completion_percent']],
        textposition='inside',
        textfont=dict(color='white', size=10)
    )])
    
    progress_fig.update_layout(
        title={
            'text': '<b>Project Progress Overview (Top 15)</b>',
            'x': 0.5,
            'font': {'size': 16, 'color': COLORS['dark']}
        },
        xaxis_title="Completion Percentage",
        yaxis_title="Projects",
        height=500,
        margin=dict(t=60, b=40, l=200, r=40),
        xaxis=dict(range=[0, 105])
    )
    
    # 5. ENHANCED COMBO CHART - BUDGET ANALYSIS
    budget_agg = data['budget_variance'].groupby('project_id').agg({
        'actual_budget': 'sum',
        'planned_budget': 'sum',
        'variance': 'sum',
        'variance_percent': 'mean'
    }).reset_index().head(12)
    
    # Merge with project info
    budget_agg = budget_agg.merge(data['projects_master'], on='project_id')
    
    combo_fig = go.Figure()
    
    # Planned Budget Bars
    combo_fig.add_trace(go.Bar(
        name='Planned Budget',
        x=budget_agg['project_id'],
        y=budget_agg['planned_budget'],
        marker_color=COLORS['success'],
        hovertemplate=
        '<b>%{x}</b><br>' +
        'Planned: $%{y:,.0f}<br>' +
        'Project: %{customdata[0]}<br>' +
        'Manager: %{customdata[1]}<br>' +
        '<extra></extra>',
        customdata=budget_agg[['project_name', 'manager']].values,
        opacity=0.8
    ))
    
    # Actual Budget Bars
    combo_fig.add_trace(go.Bar(
        name='Actual Budget',
        x=budget_agg['project_id'],
        y=budget_agg['actual_budget'],
        marker_color=COLORS['danger'],
        hovertemplate=
        '<b>%{x}</b><br>' +
        'Actual: $%{y:,.0f}<br>' +
        'Variance: %{customdata[0]:+.1f}%<br>' +
        'Type: %{customdata[1]}<br>' +
        '<extra></extra>',
        customdata=budget_agg[['variance_percent', 'type']].values,
        opacity=0.8
    ))
    
    # Variance Line
    combo_fig.add_trace(go.Scatter(
        name='Variance %',
        x=budget_agg['project_id'],
        y=budget_agg['variance_percent'] * 1000,  # Scale for visibility
        mode='lines+markers',
        marker=dict(color=COLORS['primary'], size=8),
        line=dict(width=3),
        yaxis='y2',
        hovertemplate=
        '<b>%{x}</b><br>' +
        'Variance: %{customdata:+.1f}%<br>' +
        '<extra></extra>',
        customdata=budget_agg['variance_percent'].values
    ))
    
    combo_fig.update_layout(
        title={
            'text': '<b>Budget Analysis: Planned vs Actual (Top 12)</b>',
            'x': 0.5,
            'font': {'size': 16, 'color': COLORS['dark']}
        },
        xaxis_title="Project ID",
        yaxis_title="Budget Amount ($)",
        yaxis2=dict(
            title="Variance Percentage (%)",
            overlaying='y',
            side='right',
            tickformat='.1f'
        ),
        barmode='group',
        height=450,
        legend=dict(x=0.02, y=0.98),
        margin=dict(t=60, b=60, l=60, r=80)
    )
    
    # 6. ENHANCED SCATTER PLOT - RESOURCE EFFICIENCY
    resources_analysis = data['resources'].groupby('project_id').agg({
        'efficiency_score': 'mean',
        'planned_resources': 'sum',
        'actual_resources': 'sum',
        'cost_per_hour': 'mean'
    }).reset_index()
    
    resources_analysis = resources_analysis.merge(data['projects_master'], on='project_id')
    resources_analysis = resources_analysis.merge(
        data['project_status'][['project_id', 'completion_percent']], on='project_id'
    )
    
    # Size based on total budget, color based on project type
    type_colors = {
        'Residential': COLORS['primary'],
        'Commercial': COLORS['success'], 
        'Infrastructure': COLORS['warning'],
        'Industrial': COLORS['danger'],
        'Public Works': COLORS['info']
    }
    
    scatter_fig = go.Figure()
    
    for ptype in resources_analysis['type'].unique():
        type_data = resources_analysis[resources_analysis['type'] == ptype]
        
        scatter_fig.add_trace(go.Scatter(
            x=type_data['efficiency_score'],
            y=type_data['completion_percent'],
            mode='markers',
            name=ptype,
            marker=dict(
                size=type_data['total_budget'] / 10000,  # Scale for bubble size
                color=type_colors.get(ptype, COLORS['secondary']),
                opacity=0.7,
                line=dict(width=1, color='white')
            ),
            hovertemplate=
            '<b>%{customdata[0]}</b><br>' +
            'Efficiency Score: %{x:.2f}<br>' +
            'Completion: %{y:.1f}%<br>' +
            'Type: ' + ptype + '<br>' +
            'Budget: $%{customdata[1]:,.0f}<br>' +
            'Manager: %{customdata[2]}<br>' +
            'Resources Planned: %{customdata[3]}<br>' +
            'Resources Actual: %{customdata[4]}<br>' +
            '<extra></extra>',
            customdata=type_data[['project_name', 'total_budget', 'manager', 
                                 'planned_resources', 'actual_resources']].values
        ))
    
    scatter_fig.update_layout(
        title={
            'text': '<b>Resource Efficiency vs Project Completion</b>',
            'x': 0.5,
            'font': {'size': 16, 'color': COLORS['dark']}
        },
        xaxis_title="Resource Efficiency Score",
        yaxis_title="Project Completion (%)",
        height=450,
        showlegend=True,
        legend=dict(x=0.02, y=0.98),
        margin=dict(t=60, b=60, l=60, r=40)
    )
    
    return {
        'status_fig': status_fig,
        'stages_fig': stages_fig,
        'gauge_fig': gauge_fig,
        'progress_fig': progress_fig,
        'combo_fig': combo_fig,
        'scatter_fig': scatter_fig
    }

# ENHANCED DASHBOARD LAYOUT WITH ADVANCED CONTROLS
def create_enhanced_layout(data):
    """Create enhanced dashboard layout with comprehensive controls"""
    
    # Create all charts
    charts = create_enhanced_charts(data)
    
    # Control Panel
    controls_panel = dbc.Card([
        dbc.CardHeader([
            html.H5("🎛️ Dashboard Controls", className="mb-0 text-primary")
        ]),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Label("Project Status Filter:", className="fw-bold"),
                    dcc.Dropdown(
                        id='status-filter',
                        options=[{'label': 'All Status', 'value': 'all'}] + 
                               [{'label': status, 'value': status} 
                                for status in data['project_status']['status'].unique()],
                        value='all',
                        placeholder="Select Project Status",
                        clearable=False
                    )
                ], md=3),
                dbc.Col([
                    html.Label("Project Type Filter:", className="fw-bold"),
                    dcc.Dropdown(
                        id='type-filter',
                        options=[{'label': 'All Types', 'value': 'all'}] + 
                               [{'label': ptype, 'value': ptype} 
                                for ptype in data['projects_master']['type'].unique()],
                        value='all',
                        placeholder="Select Project Type",
                        clearable=False
                    )
                ], md=3),
                dbc.Col([
                    html.Label("Priority Filter:", className="fw-bold"),
                    dcc.Dropdown(
                        id='priority-filter',
                        options=[{'label': 'All Priorities', 'value': 'all'}] + 
                               [{'label': priority, 'value': priority} 
                                for priority in data['projects_master']['priority'].unique()],
                        value='all',
                        placeholder="Select Priority",
                        clearable=False
                    )
                ], md=3),
                dbc.Col([
                    html.Label("Dashboard View:", className="fw-bold"),
                    dbc.Switch(
                        id='advanced-view-toggle',
                        label="Advanced Analytics",
                        value=False
                    ),
                    html.Br(),
                    dbc.Button(
                        "🔄 Refresh Data",
                        id='refresh-button',
                        color="primary",
                        size="sm",
                        className="mt-2"
                    )
                ], md=3)
            ])
        ])
    ], className="mb-4")
    
    # KPI Cards Row
    kpi_cards = dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(f"{len(data['projects_master'])}", className="text-primary mb-0"),
                    html.P("Total Projects", className="mb-0 text-muted")
                ])
            ], className="text-center h-100")
        ], md=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(f"${data['projects_master']['total_budget'].sum():,.0f}", className="text-success mb-0"),
                    html.P("Total Budget", className="mb-0 text-muted")
                ])
            ], className="text-center h-100")
        ], md=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(f"{data['project_status']['completion_percent'].mean():.1f}%", className="text-info mb-0"),
                    html.P("Avg Completion", className="mb-0 text-muted")
                ])
            ], className="text-center h-100")
        ], md=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(f"{len(data['project_status'][data['project_status']['status'] == 'Completed'])}", className="text-warning mb-0"),
                    html.P("Completed", className="mb-0 text-muted")
                ])
            ], className="text-center h-100")
        ], md=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(f"{data['project_status']['days_ahead_behind'].mean():+.0f}", className="text-secondary mb-0"),
                    html.P("Days Avg Variance", className="mb-0 text-muted")
                ])
            ], className="text-center h-100")
        ], md=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(id="live-timestamp", className="text-dark mb-0"),
                    html.P("Last Updated", className="mb-0 text-muted")
                ])
            ], className="text-center h-100")
        ], md=2)
    ], className="mb-4")
    
    # Main Charts Layout
    main_layout = html.Div([
        # Header
        dbc.Row([
            dbc.Col([
                html.H1("🏗️ Construction Project Monitoring Dashboard", 
                       className="text-center mb-4 text-primary"),
                html.P("Advanced Analytics & Real-time Project Tracking", 
                      className="text-center text-muted mb-4")
            ])
        ]),
        
        # Controls
        controls_panel,
        
        # KPI Cards
        kpi_cards,
        
        # Charts Row 1
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(
                            id='status-chart',
                            figure=charts['status_fig'],
                            config={'displayModeBar': True, 'displaylogo': False}
                        )
                    ])
                ])
            ], md=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(
                            id='gauge-chart',
                            figure=charts['gauge_fig'],
                            config={'displayModeBar': True, 'displaylogo': False}
                        )
                    ])
                ])
            ], md=6)
        ], className="mb-4"),
        
        # Charts Row 2
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(
                            id='sunburst-chart',
                            figure=charts['stages_fig'],
                            config={'displayModeBar': True, 'displaylogo': False}
                        )
                    ])
                ])
            ], md=12)
        ], className="mb-4"),
        
        # Charts Row 3
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(
                            id='progress-chart',
                            figure=charts['progress_fig'],
                            config={'displayModeBar': True, 'displaylogo': False}
                        )
                    ])
                ])
            ], md=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(
                            id='scatter-chart',
                            figure=charts['scatter_fig'],
                            config={'displayModeBar': True, 'displaylogo': False}
                        )
                    ])
                ])
            ], md=6)
        ], className="mb-4"),
        
        # Charts Row 4
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(
                            id='combo-chart',
                            figure=charts['combo_fig'],
                            config={'displayModeBar': True, 'displaylogo': False}
                        )
                    ])
                ])
            ], md=12)
        ], className="mb-4"),
        
        # Interval component for live updates
        dcc.Interval(
            id='interval-component',
            interval=30*1000,  # Update every 30 seconds
            n_intervals=0
        ),
        
        # Store components for data sharing
        dcc.Store(id='filtered-data'),
        dcc.Store(id='original-data')
    ])
    
    return main_layout

# ENHANCED CALLBACK FUNCTIONS
def register_enhanced_callbacks(app, data):
    """Register enhanced callbacks with comprehensive interactivity"""
    
    # Store original data
    @app.callback(
        Output('original-data', 'data'),
        Input('refresh-button', 'n_clicks'),
        prevent_initial_call=False
    )
    def store_original_data(n_clicks):
        return {
            'projects_master': data['projects_master'].to_dict('records'),
            'project_status': data['project_status'].to_dict('records'),
            'project_stages': data['project_stages'].to_dict('records'),
            'budget_variance': data['budget_variance'].to_dict('records'),
            'resources': data['resources'].to_dict('records'),
            'workload': data['workload'].to_dict('records')
        }
    
    # Filter data based on controls
    @app.callback(
        Output('filtered-data', 'data'),
        [Input('status-filter', 'value'),
         Input('type-filter', 'value'),
         Input('priority-filter', 'value'),
         Input('original-data', 'data')]
    )
    def filter_data(status_filter, type_filter, priority_filter, original_data):
        if not original_data:
            return {}
        
        # Convert back to DataFrames
        filtered_data = {}
        for key, value in original_data.items():
            filtered_data[key] = pd.DataFrame(value)
        
        # Apply filters to projects_master
        projects_mask = pd.Series([True] * len(filtered_data['projects_master']))
        
        if type_filter != 'all':
            projects_mask &= (filtered_data['projects_master']['type'] == type_filter)
        
        if priority_filter != 'all':
            projects_mask &= (filtered_data['projects_master']['priority'] == priority_filter)
        
        filtered_projects = filtered_data['projects_master'][projects_mask]['project_id'].tolist()
        
        # Apply status filter to project_status
        status_mask = pd.Series([True] * len(filtered_data['project_status']))
        if status_filter != 'all':
            status_mask &= (filtered_data['project_status']['status'] == status_filter)
        
        filtered_status_projects = filtered_data['project_status'][status_mask]['project_id'].tolist()
        
        # Get intersection of filtered projects
        final_projects = list(set(filtered_projects) & set(filtered_status_projects))
        
        # Filter all datasets
        for key in filtered_data:
            if 'project_id' in filtered_data[key].columns:
                filtered_data[key] = filtered_data[key][
                    filtered_data[key]['project_id'].isin(final_projects)
                ]
        
        # Convert back to records for storage
        return {key: df.to_dict('records') for key, df in filtered_data.items()}
    
    # Update all charts based on filtered data
    @app.callback(
        [Output('status-chart', 'figure'),
         Output('gauge-chart', 'figure'),
         Output('sunburst-chart', 'figure'),
         Output('progress-chart', 'figure'),
         Output('scatter-chart', 'figure'),
         Output('combo-chart', 'figure')],
        [Input('filtered-data', 'data'),
         Input('advanced-view-toggle', 'value')]
    )
    def update_all_charts(filtered_data, advanced_view):
        if not filtered_data or not any(filtered_data.values()):
            # Return empty figures
            empty_fig = go.Figure().add_annotation(
                text="No data available for current filters",
                x=0.5, y=0.5, showarrow=False
            )
            return [empty_fig] * 6
        
        # Convert back to DataFrames
        data_dict = {key: pd.DataFrame(value) for key, value in filtered_data.items()}
        
        # Create charts with filtered data
        charts = create_enhanced_charts(data_dict)
        
        return (
            charts['status_fig'],
            charts['gauge_fig'], 
            charts['stages_fig'],
            charts['progress_fig'],
            charts['scatter_fig'],
            charts['combo_fig']
        )
    
    # Update live timestamp
    @app.callback(
        Output('live-timestamp', 'children'),
        Input('interval-component', 'n_intervals')
    )
    def update_timestamp(n):
        return datetime.now().strftime("%H:%M:%S")

# MAIN APPLICATION SETUP
def create_enhanced_app():
    """Create and configure the enhanced Dash application"""
    
    # Generate enhanced data
    data = generate_enhanced_data()
    
    # Initialize Dash app with Bootstrap theme
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    
    # Set app layout
    app.layout = dbc.Container([
        create_enhanced_layout(data)
    ], fluid=True)
    
    # Register callbacks
    register_enhanced_callbacks(app, data)
    
    return app, data

# EXPORT FUNCTIONALITY
def export_enhanced_dashboard():
    """Export enhanced dashboard to HTML file"""
    
    app, data = create_enhanced_app()
    
    # Generate charts for export
    charts = create_enhanced_charts(data)
    
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Enhanced Construction Project Monitoring Dashboard</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f8f9fa;
                margin: 0;
                padding: 20px;
            }}
            .dashboard-header {{
                background: linear-gradient(135deg, #007bff, #0056b3);
                color: white;
                padding: 30px;
                margin-bottom: 30px;
                border-radius: 15px;
                text-align: center;
                box-shadow: 0 10px 30px rgba(0,123,255,0.3);
            }}
            .chart-container {{
                background: white;
                padding: 20px;
                margin-bottom: 25px;
                border-radius: 15px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                border: 1px solid #e9ecef;
            }}
            .kpi-card {{
                background: white;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                box-shadow: 0 3px 10px rgba(0,0,0,0.1);
                margin-bottom: 20px;
                border-left: 4px solid #007bff;
            }}
            .kpi-value {{
                font-size: 2.5rem;
                font-weight: bold;
                color: #007bff;
                margin: 0;
            }}
            .kpi-label {{
                color: #6c757d;
                margin: 0;
                font-size: 0.9rem;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
            .dashboard-info {{
                background: #e7f1ff;
                padding: 15px;
                border-radius: 10px;
                border-left: 5px solid #007bff;
                margin-bottom: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="container-fluid">
            <!-- Header -->
            <div class="dashboard-header">
                <h1 class="display-4 mb-3">🏗️ Construction Project Monitoring Dashboard</h1>
                <p class="lead mb-0">Enhanced Analytics & Real-time Project Tracking System</p>
                <small>Generated on {datetime.now().strftime("%B %d, %Y at %H:%M:%S")}</small>
            </div>
            
            <!-- Dashboard Info -->
            <div class="dashboard-info">
                <h5><i class="bi bi-info-circle"></i> Dashboard Overview</h5>
                <p class="mb-0">This interactive dashboard provides comprehensive insights into construction project performance, 
                including status tracking, budget analysis, resource allocation, and progress monitoring across all active projects.</p>
            </div>
            
            <!-- KPI Cards -->
            <div class="row mb-4">
                <div class="col-md-2">
                    <div class="kpi-card">
                        <h4 class="kpi-value">{len(data['projects_master'])}</h4>
                        <p class="kpi-label">Total Projects</p>
                    </div>
                </div>
                <div class="col-md-2">
                    <div class="kpi-card">
                        <h4 class="kpi-value">${data['projects_master']['total_budget'].sum():,.0f}</h4>
                        <p class="kpi-label">Total Budget</p>
                    </div>
                </div>
                <div class="col-md-2">
                    <div class="kpi-card">
                        <h4 class="kpi-value">{data['project_status']['completion_percent'].mean():.1f}%</h4>
                        <p class="kpi-label">Avg Completion</p>
                    </div>
                </div>
                <div class="col-md-2">
                    <div class="kpi-card">
                        <h4 class="kpi-value">{len(data['project_status'][data['project_status']['status'] == 'Completed'])}</h4>
                        <p class="kpi-label">Completed</p>
                    </div>
                </div>
                <div class="col-md-2">
                    <div class="kpi-card">
                        <h4 class="kpi-value">{len(data['project_status'][data['project_status']['status'] == 'In Progress'])}</h4>
                        <p class="kpi-label">In Progress</p>
                    </div>
                </div>
                <div class="col-md-2">
                    <div class="kpi-card">
                        <h4 class="kpi-value">{data['project_status']['days_ahead_behind'].mean():+.0f}</h4>
                        <p class="kpi-label">Days Variance</p>
                    </div>
                </div>
            </div>
            
            <!-- Charts Row 1 -->
            <div class="row">
                <div class="col-md-6">
                    <div class="chart-container">
                        <div id="status-chart">{charts['status_fig'].to_html(include_plotlyjs=False, div_id="status-chart")}</div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="chart-container">
                        <div id="gauge-chart">{charts['gauge_fig'].to_html(include_plotlyjs=False, div_id="gauge-chart")}</div>
                    </div>
                </div>
            </div>
            
            <!-- Charts Row 2 -->
            <div class="row">
                <div class="col-md-12">
                    <div class="chart-container">
                        <div id="sunburst-chart">{charts['stages_fig'].to_html(include_plotlyjs=False, div_id="sunburst-chart")}</div>
                    </div>
                </div>
            </div>
            
            <!-- Charts Row 3 -->
            <div class="row">
                <div class="col-md-6">
                    <div class="chart-container">
                        <div id="progress-chart">{charts['progress_fig'].to_html(include_plotlyjs=False, div_id="progress-chart")}</div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="chart-container">
                        <div id="scatter-chart">{charts['scatter_fig'].to_html(include_plotlyjs=False, div_id="scatter-chart")}</div>
                    </div>
                </div>
            </div>
            
            <!-- Charts Row 4 -->
            <div class="row">
                <div class="col-md-12">
                    <div class="chart-container">
                        <div id="combo-chart">{charts['combo_fig'].to_html(include_plotlyjs=False, div_id="combo-chart")}</div>
                    </div>
                </div>
            </div>
            
            <!-- Footer -->
            <div class="text-center mt-5 mb-3">
                <p class="text-muted">
                    <small>Enhanced Construction Project Dashboard | Interactive Analytics Platform | 
                    Built with Python, Plotly & Dash</small>
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Save to file
    with open('outputs/enhanced_dashboard.html', 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    return html_template

# EXECUTION
if __name__ == "__main__":
    # Export enhanced dashboard
    export_enhanced_dashboard()
    print("✅ Enhanced dashboard exported to outputs/enhanced_dashboard.html")
    
    # Create and run interactive app
    app, data = create_enhanced_app()
    print("🚀 Starting enhanced interactive dashboard...")
    print("📊 Dashboard available at: http://localhost:8050")
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=8050)
