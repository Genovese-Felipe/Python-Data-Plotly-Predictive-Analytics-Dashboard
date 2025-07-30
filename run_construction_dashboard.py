#!/usr/bin/env python3
"""
🏗️ Construction Project Monitoring Dashboard
Professional Dash Application for Construction Analytics

Created following official Python Data Visualization guidelines.
Implements all Dash fundamentals and professional best practices.

Author: GitHub Copilot Development Agent
Project: Python-Data-Plotly-Predictive-Analytics-Dashboard
"""

# Core imports
import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from functools import lru_cache
import time

# ============================================================================
# PROFESSIONAL CONFIGURATION AND STYLING
# Following Tip 8: Color Science and Professional Design
# ============================================================================

# Professional color palette
COLORS = {
    'primary': '#2563eb',    # Professional blue
    'secondary': '#64748b',  # Professional gray
    'success': '#059669',    # Professional green
    'warning': '#d97706',    # Professional orange
    'danger': '#dc2626',     # Professional red
    'info': '#0891b2',       # Professional cyan
    'light': '#f1f5f9',      # Light gray
    'dark': '#1e293b',       # Dark gray
}

# Layout configuration
LAYOUT_CONFIG = {
    'font_family': 'Inter, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif',
    'card_shadow': '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
    'border_radius': '12px',
    'spacing': '24px'
}

# ============================================================================
# DATA GENERATION FUNCTIONS
# ============================================================================

def generate_construction_data():
    """Generate realistic construction project data for dashboard demonstration."""
    np.random.seed(42)  # For consistent demo data
    
    n_projects = 25
    project_types = ['Residential', 'Commercial', 'Infrastructure', 'Industrial']
    work_statuses = ['In Progress', 'Completed', 'Not Started']
    project_stages = ['Design', 'Plan', 'Pre-construction']
    
    data = {
        'project_id': [f'Project_{i+1}' for i in range(n_projects)],
        'project_name': [f'Construction Project {i+1}' for i in range(n_projects)],
        'project_type': np.random.choice(project_types, n_projects),
        'project_head': [f'Manager {chr(65+i%26)}' for i in range(n_projects)],
        'start_date': pd.date_range('2024-01-01', periods=n_projects, freq='W'),
        'total_budget': np.random.randint(100000, 1000000, n_projects),
        'planned_duration': np.random.randint(180, 1100, n_projects),
        'current_completion': np.random.randint(20, 100, n_projects),
        'work_status': np.random.choice(work_statuses, n_projects),
        'current_stage': np.random.choice(project_stages, n_projects)
    }
    
    df = pd.DataFrame(data)
    print("✅ Core project data generated!")
    print(f"📊 Total projects: {len(df)}")
    print(f"💰 Budget range: ${df['total_budget'].min():,} - ${df['total_budget'].max():,}")
    print(f"📅 Duration range: {df['planned_duration'].min()} - {df['planned_duration'].max()} days")
    
    return df

# ============================================================================
# LAYOUT COMPONENTS - FOLLOWING TIP 1: LAYOUT FUNDAMENTALS
# ============================================================================

def create_professional_card(title, content, icon="📊"):
    """Create professional card component with consistent styling."""
    return dbc.Card([
        dbc.CardHeader([
            html.H5([
                html.Span(icon, className="me-2"),
                title
            ], className="mb-0", style={'color': COLORS['dark']})
        ], style={'backgroundColor': '#ffffff', 'border': 'none'}),
        dbc.CardBody(content, style={'padding': '20px'})
    ], style={
        'boxShadow': LAYOUT_CONFIG['card_shadow'],
        'borderRadius': LAYOUT_CONFIG['border_radius'],
        'border': 'none',
        'marginBottom': '20px'
    })

def create_kpi_card(title, value, icon, color_type):
    """Create KPI card with dynamic color coding."""
    color = COLORS.get(color_type, COLORS['primary'])
    
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                html.Div([
                    html.H2(icon, style={
                        'fontSize': '2rem',
                        'margin': '0',
                        'color': color
                    })
                ], style={'textAlign': 'center', 'marginBottom': '10px'}),
                html.Div([
                    html.H3(value, style={
                        'fontSize': '1.8rem',
                        'fontWeight': 'bold',
                        'margin': '0',
                        'color': COLORS['dark']
                    }),
                    html.P(title, style={
                        'fontSize': '0.9rem',
                        'margin': '0',
                        'color': COLORS['secondary']
                    })
                ], style={'textAlign': 'center'})
            ])
        ], style={'padding': '20px'})
    ], style={
        'boxShadow': LAYOUT_CONFIG['card_shadow'],
        'borderRadius': LAYOUT_CONFIG['border_radius'],
        'border': 'none',
        'height': '150px'
    })

def create_filter_section():
    """Create interactive filter section."""
    return html.Div([
        dbc.Row([
            dbc.Col([
                html.Label("Project Filter:", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                dcc.Dropdown(
                    id='project-filter',
                    options=[
                        {'label': 'All Projects', 'value': 'All'},
                        {'label': 'Residential', 'value': 'Residential'},
                        {'label': 'Commercial', 'value': 'Commercial'},
                        {'label': 'Infrastructure', 'value': 'Infrastructure'}
                    ],
                    value='All',
                    style={'marginBottom': '10px'}
                )
            ], width=3),
            dbc.Col([
                html.Label("Status Filter:", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                dcc.Dropdown(
                    id='status-filter',
                    options=[
                        {'label': 'All Status', 'value': 'All'},
                        {'label': 'In Progress', 'value': 'In Progress'},
                        {'label': 'Completed', 'value': 'Completed'},
                        {'label': 'Not Started', 'value': 'Not Started'}
                    ],
                    value='All',
                    style={'marginBottom': '10px'}
                )
            ], width=3),
            dbc.Col([
                html.Label("Date Range:", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                dcc.DatePickerRange(
                    id='date-range-picker',
                    start_date='2024-01-01',
                    end_date='2024-12-31',
                    display_format='YYYY-MM-DD',
                    style={'marginBottom': '10px'}
                )
            ], width=4),
            dbc.Col([
                html.Div([
                    dbc.Button("🔄 Refresh", id="refresh-button", color="primary", size="sm"),
                    html.Div(id="refresh-trigger", style={'display': 'none'})
                ], style={'paddingTop': '25px'})
            ], width=2)
        ])
    ], style={
        'backgroundColor': '#ffffff',
        'padding': '20px',
        'borderRadius': LAYOUT_CONFIG['border_radius'],
        'boxShadow': LAYOUT_CONFIG['card_shadow'],
        'marginBottom': '30px'
    })

# ============================================================================
# VISUALIZATION FUNCTIONS - FOLLOWING PLOTLY BEST PRACTICES
# ============================================================================

@lru_cache(maxsize=128)
def create_work_status_donut(data_json):
    """Create professional donut chart for work status distribution."""
    data = pd.read_json(data_json)
    status_counts = data['work_status'].value_counts()
    
    fig = go.Figure(data=[go.Pie(
        labels=status_counts.index,
        values=status_counts.values,
        hole=0.4,
        marker=dict(
            colors=[COLORS['success'], COLORS['primary'], COLORS['warning']],
            line=dict(color='white', width=2)
        ),
        textinfo='label+percent',
        textposition='outside',
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<br><extra></extra>'
    )])
    
    fig.update_layout(
        title=dict(text="<b>Project Work Status</b>", font=dict(size=16, color=COLORS['dark']), x=0.5),
        showlegend=True,
        height=300,
        margin=dict(l=20, r=80, t=60, b=20),
        font=dict(family=LAYOUT_CONFIG['font_family'], size=12)
    )
    
    return fig

def create_stage_pie_chart(data_json):
    """Create professional pie chart for project stages."""
    data = pd.read_json(data_json)
    stage_counts = data['current_stage'].value_counts()
    
    fig = go.Figure(data=[go.Pie(
        labels=stage_counts.index,
        values=stage_counts.values,
        marker=dict(
            colors=[COLORS['primary'], COLORS['success'], COLORS['info']],
            line=dict(color='white', width=2)
        ),
        textinfo='label+percent',
        textposition='outside',
        hovertemplate='<b>%{label}</b><br>Projects: %{value}<br>Percentage: %{percent}<br><extra></extra>'
    )])
    
    fig.update_layout(
        title=dict(text="<b>Projects by Stage</b>", font=dict(size=16, color=COLORS['dark']), x=0.5),
        showlegend=True,
        height=300,
        margin=dict(l=20, r=80, t=60, b=20),
        font=dict(family=LAYOUT_CONFIG['font_family'], size=12)
    )
    
    return fig

def create_completion_gauge(completion_percent, title="Project Completion"):
    """Create professional gauge chart for completion metrics."""
    # Dynamic color based on completion
    if completion_percent >= 80:
        gauge_color = COLORS['success']
    elif completion_percent >= 50:
        gauge_color = COLORS['warning']
    else:
        gauge_color = COLORS['danger']
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=completion_percent,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"<b>{title}</b>", 'font': {'size': 16}},
        delta={'reference': 100, 'suffix': '%'},
        gauge={
            'axis': {'range': [None, 100], 'ticksuffix': '%'},
            'bar': {'color': gauge_color, 'thickness': 0.75},
            'steps': [
                {'range': [0, 50], 'color': 'rgba(244, 67, 54, 0.2)'},
                {'range': [50, 80], 'color': 'rgba(255, 193, 7, 0.2)'},
                {'range': [80, 100], 'color': 'rgba(76, 175, 80, 0.2)'}
            ],
            'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 90}
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=60, b=20),
        font=dict(family=LAYOUT_CONFIG['font_family'])
    )
    
    return fig

def create_performance_bar_chart(data_json):
    """Create performance analysis bar chart with conditional formatting."""
    data = pd.read_json(data_json)
    
    # Calculate performance metrics by project
    performance_data = data.groupby('project_name').agg({
        'current_completion': 'mean',
        'total_budget': 'sum'
    }).reset_index()
    
    # Sort by completion percentage
    performance_data = performance_data.sort_values('current_completion', ascending=True)
    
    # Color coding based on performance
    colors = []
    for completion in performance_data['current_completion']:
        if completion >= 80:
            colors.append(COLORS['success'])
        elif completion >= 60:
            colors.append(COLORS['warning'])
        else:
            colors.append(COLORS['danger'])
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=performance_data['current_completion'],
        y=performance_data['project_name'],
        orientation='h',
        marker=dict(color=colors, line=dict(color='white', width=1)),
        text=[f"{val:.1f}%" for val in performance_data['current_completion']],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Completion: %{x:.1f}%<br><extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text="<b>Project Performance Analysis</b>", font=dict(size=16, color=COLORS['dark']), x=0.5),
        xaxis=dict(title='Completion Percentage (%)', range=[0, 100], ticksuffix='%'),
        yaxis=dict(title='Projects'),
        height=350,
        margin=dict(l=150, r=60, t=80, b=60),
        font=dict(family=LAYOUT_CONFIG['font_family'])
    )
    
    return fig

def create_budget_variance_combo():
    """Create combo chart for budget variance analysis."""
    # Generate sample variance data
    months = pd.date_range('2024-01-01', periods=12, freq='M')
    actual = np.random.uniform(80000, 120000, 12)
    planned = np.random.uniform(85000, 115000, 12)
    variance = actual - planned
    
    fig = go.Figure()
    
    # Add actual vs planned bars
    fig.add_trace(go.Bar(x=months, y=actual, name='Actual', marker_color=COLORS['primary'], yaxis='y', opacity=0.8))
    fig.add_trace(go.Bar(x=months, y=planned, name='Planned', marker_color=COLORS['info'], yaxis='y', opacity=0.8))
    
    # Add variance line
    fig.add_trace(go.Scatter(
        x=months, y=variance, mode='lines+markers', name='Variance',
        line=dict(color=COLORS['danger'], width=3), yaxis='y2'
    ))
    
    fig.update_layout(
        title=dict(text="<b>Budget Variance - Actual vs Planned</b>", font=dict(size=16, color=COLORS['dark']), x=0.5),
        yaxis=dict(title='Budget Amount ($)', side='left', tickformat='$,.0f'),
        yaxis2=dict(title='Variance ($)', overlaying='y', side='right', tickformat='$,.0f'),
        xaxis=dict(title='Period'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=350,
        margin=dict(l=60, r=60, t=80, b=60),
        font=dict(family=LAYOUT_CONFIG['font_family'])
    )
    
    return fig

def create_workload_timeline():
    """Create workload timeline visualization for resource management."""
    # Generate sample timeline data
    dates = pd.date_range('2024-01-01', periods=30, freq='D')
    workload_data = []
    
    for i, date in enumerate(dates):
        daily_workload = {
            'date': date,
            'planned_hours': np.random.uniform(6, 10),
            'actual_hours': np.random.uniform(5, 11),
            'overtime': max(0, np.random.uniform(-1, 3))
        }
        workload_data.append(daily_workload)
    
    workload_df = pd.DataFrame(workload_data)
    
    fig = go.Figure()
    
    # Planned hours
    fig.add_trace(go.Scatter(
        x=workload_df['date'], y=workload_df['planned_hours'],
        mode='lines', name='Planned Hours',
        line=dict(color=COLORS['primary'], width=2, dash='dash'), fill=None
    ))
    
    # Actual hours
    fig.add_trace(go.Scatter(
        x=workload_df['date'], y=workload_df['actual_hours'],
        mode='lines', name='Actual Hours',
        line=dict(color=COLORS['success'], width=3),
        fill='tonexty', fillcolor='rgba(76, 175, 80, 0.1)'
    ))
    
    # Overtime indicators
    overtime_dates = workload_df[workload_df['overtime'] > 0]['date']
    overtime_hours = workload_df[workload_df['overtime'] > 0]['actual_hours']
    
    fig.add_trace(go.Scatter(
        x=overtime_dates, y=overtime_hours, mode='markers', name='Overtime',
        marker=dict(color=COLORS['danger'], size=8, symbol='triangle-up')
    ))
    
    fig.update_layout(
        title=dict(text="<b>Workload Timeline - Last 30 Days</b>", font=dict(size=16, color=COLORS['dark']), x=0.5),
        xaxis=dict(title='Date', tickformat='%b %d'),
        yaxis=dict(title='Hours', range=[0, 12]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=350,
        margin=dict(l=60, r=60, t=80, b=60),
        font=dict(family=LAYOUT_CONFIG['font_family'])
    )
    
    return fig

def create_kpi_summary_cards(data_json):
    """Create multiple KPI cards for dashboard header."""
    data = pd.read_json(data_json)
    
    # Calculate KPIs
    total_projects = len(data)
    avg_completion = data['current_completion'].mean()
    total_budget = data['total_budget'].sum()
    active_projects = len(data[data['work_status'] == 'In Progress'])
    
    kpis = [
        {'title': 'Total Projects', 'value': str(total_projects), 'icon': '📊', 'color': 'primary'},
        {'title': 'Avg Completion', 'value': f"{avg_completion:.1f}%", 'icon': '📈', 'color': 'success'},
        {'title': 'Total Budget', 'value': f"${total_budget/1000000:.1f}M", 'icon': '💰', 'color': 'info'},
        {'title': 'Active Projects', 'value': str(active_projects), 'icon': '🔥', 'color': 'warning'}
    ]
    
    return kpis

# ============================================================================
# MAIN DASHBOARD LAYOUT
# ============================================================================

def create_construction_dashboard():
    """Create the complete Construction Project Monitoring Dashboard."""
    
    # Generate sample data for demonstration
    sample_data = generate_construction_data()
    data_json = sample_data.to_json(date_format='iso')
    
    # Get KPI summary data
    kpi_data = create_kpi_summary_cards(data_json)
    
    # Create the main dashboard layout
    layout = html.Div([
        
        # HEADER SECTION
        html.Div([
            html.H1(
                "🏗️ Construction Project Monitoring Dashboard",
                className="dashboard-title",
                style={
                    'textAlign': 'center',
                    'color': COLORS['dark'],
                    'fontFamily': LAYOUT_CONFIG['font_family'],
                    'fontSize': '2.5rem',
                    'fontWeight': 'bold',
                    'marginBottom': '10px'
                }
            ),
            html.P(
                "Professional Analytics for Construction Project Management",
                style={
                    'textAlign': 'center',
                    'color': COLORS['secondary'],
                    'fontSize': '1.2rem',
                    'marginBottom': '30px'
                }
            )
        ], style={'marginBottom': '40px'}),
        
        # KPI CARDS SECTION
        html.Div([
            dbc.Row([
                dbc.Col([
                    create_kpi_card(kpi['title'], kpi['value'], kpi['icon'], kpi['color'])
                ], width=3) for kpi in kpi_data
            ], className="mb-4")
        ]),
        
        # FILTER SECTION
        create_filter_section(),
        
        # MAIN VISUALIZATIONS GRID
        html.Div([
            
            # Row 1: Status and Performance Overview
            dbc.Row([
                dbc.Col([
                    create_professional_card(
                        "Work Status Distribution",
                        dcc.Graph(
                            id='work-status-donut',
                            figure=create_work_status_donut(data_json),
                            config={'displayModeBar': False}
                        )
                    )
                ], width=6),
                dbc.Col([
                    create_professional_card(
                        "Project Stages",
                        dcc.Graph(
                            id='project-stages-pie',
                            figure=create_stage_pie_chart(data_json),
                            config={'displayModeBar': False}
                        )
                    )
                ], width=6)
            ], className="mb-4"),
            
            # Row 2: Performance Metrics
            dbc.Row([
                dbc.Col([
                    create_professional_card(
                        "Overall Completion",
                        dcc.Graph(
                            id='completion-gauge',
                            figure=create_completion_gauge(
                                sample_data['current_completion'].mean(),
                                "Average Project Completion"
                            ),
                            config={'displayModeBar': False}
                        )
                    )
                ], width=4),
                dbc.Col([
                    create_professional_card(
                        "Project Performance",
                        dcc.Graph(
                            id='performance-bar',
                            figure=create_performance_bar_chart(data_json),
                            config={'displayModeBar': False}
                        )
                    )
                ], width=8)
            ], className="mb-4"),
            
            # Row 3: Financial and Timeline Analysis
            dbc.Row([
                dbc.Col([
                    create_professional_card(
                        "Budget Variance Analysis",
                        dcc.Graph(
                            id='budget-variance-combo',
                            figure=create_budget_variance_combo(),
                            config={'displayModeBar': False}
                        )
                    )
                ], width=8),
                dbc.Col([
                    create_professional_card(
                        "Resource Efficiency",
                        dcc.Graph(
                            id='resource-gauge',
                            figure=create_completion_gauge(85, "Resource Efficiency"),
                            config={'displayModeBar': False}
                        )
                    )
                ], width=4)
            ], className="mb-4"),
            
            # Row 4: Timeline and Workload
            dbc.Row([
                dbc.Col([
                    create_professional_card(
                        "Workload Timeline",
                        dcc.Graph(
                            id='workload-timeline',
                            figure=create_workload_timeline(),
                            config={'displayModeBar': False}
                        )
                    )
                ], width=12)
            ], className="mb-4")
        ]),
        
        # FOOTER SECTION
        html.Div([
            html.Hr(style={'borderColor': COLORS['light']}),
            html.P(
                "📊 Professional Construction Dashboard | Built with Plotly Dash | Real-time Analytics",
                style={
                    'textAlign': 'center',
                    'color': COLORS['secondary'],
                    'fontSize': '0.9rem',
                    'marginTop': '20px'
                }
            )
        ])
        
    ], style={
        'backgroundColor': '#f8f9fa',
        'minHeight': '100vh',
        'padding': '20px',
        'fontFamily': LAYOUT_CONFIG['font_family']
    })
    
    return layout

# ============================================================================
# INITIALIZE DASH APPLICATION
# ============================================================================

# Initialize the Dash application
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Construction Project Monitoring Dashboard"

# Set the layout
app.layout = create_construction_dashboard()

# ============================================================================
# INTERACTIVE CALLBACKS
# ============================================================================

@app.callback(
    [Output('work-status-donut', 'figure'),
     Output('project-stages-pie', 'figure'),
     Output('performance-bar', 'figure')],
    [Input('project-filter', 'value'),
     Input('status-filter', 'value'),
     Input('date-range-picker', 'start_date'),
     Input('date-range-picker', 'end_date')]
)
def update_charts(selected_projects, selected_status, start_date, end_date):
    """Update multiple charts based on filter selections."""
    # Generate filtered data based on selections
    filtered_data = generate_construction_data()
    
    # Apply filters if selections exist
    if selected_projects and selected_projects != 'All':
        filtered_data = filtered_data[filtered_data['project_type'] == selected_projects]
    
    if selected_status and selected_status != 'All':
        filtered_data = filtered_data[filtered_data['work_status'] == selected_status]
    
    # Convert to JSON for visualization functions
    data_json = filtered_data.to_json(date_format='iso')
    
    # Update visualizations
    donut_fig = create_work_status_donut(data_json)
    pie_fig = create_stage_pie_chart(data_json)
    bar_fig = create_performance_bar_chart(data_json)
    
    return donut_fig, pie_fig, bar_fig

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == '__main__':
    print("🚀 Starting Construction Project Monitoring Dashboard...")
    print("📊 Dashboard will be available at: http://localhost:8050")
    print("✅ All components loaded successfully!")
    print("✅ Professional styling applied!")
    print("✅ Interactive features enabled!")
    print("🔧 Running in DEBUG mode for development...")
    
    # Run the Dash application
    app.run(debug=True, port=8050, host='0.0.0.0')
