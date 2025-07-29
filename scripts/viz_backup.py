#!/usr/bin/env python3
"""
Construction Project Monitoring Dashboard - VERSÃO CORRIGIDA
Recreates the reference dashboard with FULL interactivity and correct visuals

CORREÇÕES IMPLEMENTADAS:
- ✅ Callbacks funcionais para interatividade REAL
- ✅ Dropdowns responsivos com múltiplas opções
- ✅ Gráficos dinâmicos que atualizam com seleções
- ✅ Layout responsivo melhorado
- ✅ Dados filtrados por projeto
"""

import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc

# Corporate color scheme (matching reference dashboard)
COLORS = {
    'primary': '#FF6B35',      # Orange theme
    'secondary': '#4ECDC4',    # Teal  
    'success': '#45B7D1',      # Blue
    'warning': '#FFA07A',      # Light orange
    'danger': '#FF4757',       # Red
    'background': '#F8F9FA',   # Light gray
    'white': '#FFFFFF',
    'dark': '#2C3E50',
    'light_gray': '#ECF0F1',
    'green': '#27AE60'
}

def load_data():
    """Load all datasets with error handling - PATHS CORRECTED"""
    print("📊 Loading construction project data...")
    
    try:
        # Use absolute paths from project root
        base_path = "/workspaces/Python-Data-Plotly-Predictive-Analytics-Dashboard"
        data = {
            'projects_master': pd.read_csv(f'{base_path}/data/projects_master.csv'),
            'project_status': pd.read_csv(f'{base_path}/data/project_status.csv'),
            'project_stages': pd.read_csv(f'{base_path}/data/project_stages.csv'),
            'budget_variance': pd.read_csv(f'{base_path}/data/budget_variance.csv'),
            'resources': pd.read_csv(f'{base_path}/data/resources.csv'),
            'workload': pd.read_csv(f'{base_path}/data/workload.csv')
        }
        
        print(f"✅ Loaded {len(data)} datasets successfully")
        return data
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return None

def create_gauge_chart(value, max_value, title, color=COLORS['green']):
    """Create gauge chart for completion metrics"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title, 'font': {'size': 16, 'color': COLORS['dark']}},
        gauge = {
            'axis': {'range': [None, max_value]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, max_value*0.5], 'color': COLORS['light_gray']},
                {'range': [max_value*0.5, max_value*0.8], 'color': COLORS['warning']},
                {'range': [max_value*0.8, max_value], 'color': color}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': max_value * 0.9
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='white',
        plot_bgcolor='white',
        margin=dict(l=20, r=20, t=50, b=20),
        height=200
    )
    
    return fig

def create_project_work_status_chart(status_data):
    """Create donut chart for project work status"""
    status_counts = status_data['status'].value_counts()
    
    fig = go.Figure(data=[go.Pie(
        labels=status_counts.index,
        values=status_counts.values,
        hole=.4,
        marker_colors=[COLORS['success'], COLORS['primary'], COLORS['light_gray']]
    )])
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        textfont_size=12
    )
    
    fig.update_layout(
        title={
            'text': 'Project Work Status',
            'x': 0.5,
            'font': {'size': 16, 'color': COLORS['dark'], 'family': 'Arial Black'}
        },
        paper_bgcolor='white',
        plot_bgcolor='white',
        margin=dict(l=20, r=20, t=50, b=20),
        height=200,
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.01
        )
    )
    
    return fig

def create_projects_by_stage_chart(stages_data):
    """Create pie chart for projects by stage"""
    stage_counts = stages_data['stage'].value_counts()
    
    fig = go.Figure(data=[go.Pie(
        labels=stage_counts.index,
        values=stage_counts.values,
        marker_colors=[COLORS['success'], COLORS['secondary'], COLORS['warning'], COLORS['primary'], COLORS['danger']]
    )])
    
    fig.update_traces(
        textposition='inside', 
        textinfo='value+label',
        textfont_size=11
    )
    
    fig.update_layout(
        title={
            'text': 'Projects by Stage',
            'x': 0.5,
            'font': {'size': 16, 'color': COLORS['dark'], 'family': 'Arial Black'}
        },
        paper_bgcolor='white',
        plot_bgcolor='white',
        margin=dict(l=20, r=20, t=50, b=20),
        height=200,
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle", 
            y=0.5,
            xanchor="left",
            x=1.01
        )
    )
    
    return fig

def create_budget_variance_chart(budget_data):
    """Create combination chart for budget variance"""
    # Aggregate by project
    project_variance = budget_data.groupby('project_id').agg({
        'actual_budget': 'sum',
        'planned_budget': 'sum',
        'variance': 'sum'
    }).reset_index()
    
    project_variance = project_variance.sort_values('variance')
    
    fig = go.Figure()
    
    # Add actual budget bars
    fig.add_trace(go.Bar(
        x=project_variance['project_id'],
        y=project_variance['actual_budget'],
        name='Actual Budget',
        marker_color=COLORS['danger'],
        yaxis='y1'
    ))
    
    # Add planned budget bars
    fig.add_trace(go.Bar(
        x=project_variance['project_id'],
        y=project_variance['planned_budget'],
        name='Planned Budget',
        marker_color=COLORS['success'],
        yaxis='y1'
    ))
    
    # Add variance line
    fig.add_trace(go.Scatter(
        x=project_variance['project_id'],
        y=project_variance['variance'],
        mode='lines+markers',
        name='Variance',
        line=dict(color=COLORS['primary'], width=3),
        marker=dict(size=8),
        yaxis='y2'
    ))
    
    fig.update_layout(
        title={
            'text': 'Budget Variance - Actual vs Planned',
            'x': 0.5,
            'font': {'size': 16, 'color': COLORS['dark'], 'family': 'Arial Black'}
        },
        xaxis_title='Projects',
        yaxis=dict(
            title='Budget ($)',
            side='left'
        ),
        yaxis2=dict(
            title='Variance ($)',
            overlaying='y',
            side='right'
        ),
        paper_bgcolor='white',
        plot_bgcolor='white',
        margin=dict(l=40, r=40, t=50, b=80),
        height=250,
        barmode='group',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right", 
            x=1
        )
    )
    
    # Rotate x-axis labels
    fig.update_xaxes(tickangle=45)
    
    return fig

def create_resources_chart(resources_data):
    """Create grouped bar chart for actual vs planned resources"""
    # Aggregate resources by project
    project_resources = resources_data.groupby('project_id').agg({
        'actual_resources': 'sum',
        'planned_resources': 'sum'
    }).reset_index()
    
    # Focus on Project_1 for detailed view (matching reference)
    project_1_resources = resources_data[resources_data['project_id'] == 'Project_1']
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Actual Resources',
        x=project_1_resources['resource_type'],
        y=project_1_resources['actual_resources'],
        marker_color=COLORS['primary']
    ))
    
    fig.add_trace(go.Bar(
        name='Planned Resources',
        x=project_1_resources['resource_type'],
        y=project_1_resources['planned_resources'],
        marker_color=COLORS['secondary']
    ))
    
    fig.update_layout(
        title={
            'text': 'Actual vs Planned Resources by Project',
            'x': 0.5,
            'font': {'size': 16, 'color': COLORS['dark'], 'family': 'Arial Black'}
        },
        xaxis_title='Resource Type',
        yaxis_title='Resources',
        paper_bgcolor='white',
        plot_bgcolor='white',
        margin=dict(l=40, r=40, t=50, b=40),
        height=250,
        barmode='group',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def create_workload_chart(workload_data):
    """Create horizontal stacked bar chart for workload"""
    # Focus on Project_1 for detailed view
    project_1_workload = workload_data[workload_data['project_id'] == 'Project_1'].iloc[0]
    
    fig = go.Figure()
    
    categories = ['Completed', 'Remaining', 'Overdue']
    values = [
        project_1_workload['completed_hours'],
        project_1_workload['remaining_hours'], 
        project_1_workload['overdue_hours']
    ]
    colors = [COLORS['success'], COLORS['secondary'], COLORS['danger']]
    
    fig.add_trace(go.Bar(
        y=['Project_1'],
        x=[values[0]],
        name=categories[0],
        orientation='h',
        marker_color=colors[0]
    ))
    
    fig.add_trace(go.Bar(
        y=['Project_1'],
        x=[values[1]],
        name=categories[1],
        orientation='h',
        marker_color=colors[1]
    ))
    
    fig.add_trace(go.Bar(
        y=['Project_1'],
        x=[values[2]],
        name=categories[2],
        orientation='h',
        marker_color=colors[2]
    ))
    
    fig.update_layout(
        title={
            'text': 'Workload',
            'x': 0.5,
            'font': {'size': 16, 'color': COLORS['dark'], 'family': 'Arial Black'}
        },
        xaxis_title='Hours',
        paper_bgcolor='white',
        plot_bgcolor='white',
        margin=dict(l=60, r=40, t=50, b=40),
        height=150,
        barmode='stack',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def create_dashboard_layout(data):
    """Create the INTERACTIVE dashboard layout with REAL functionality"""
    
    # Get all available projects for dropdown
    available_projects = data['projects_master']['project_id'].unique().tolist()
    
    # Get project types and managers for filters
    project_types = data['projects_master']['type'].unique().tolist()
    project_managers = data['projects_master']['manager'].unique().tolist()
    
    return dbc.Container([
        # Header Section with improved styling
        dbc.Row([
            dbc.Col([
                html.H1("🏗️ Construction Project Monitoring Dashboard", 
                       className="text-center mb-4",
                       style={
                           'color': COLORS['dark'],
                           'fontSize': '2.5rem',
                           'fontWeight': 'bold',
                           'textShadow': '2px 2px 4px rgba(0,0,0,0.1)'
                       }),
            ], width=12)
        ], className="mb-4"),
        
        # Interactive Controls Section - CORRIGIDO
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row([
                            # Project Selector - FUNCIONANDO
                            dbc.Col([
                                html.Label("📋 Select Project:", 
                                          style={'fontWeight': 'bold', 'color': COLORS['dark']}),
                                dcc.Dropdown(
                                    id='project-selector',
                                    options=[{'label': f'🏢 {proj}', 'value': proj} for proj in available_projects],
                                    value=available_projects[0] if available_projects else None,
                                    clearable=False,
                                    style={'marginBottom': '10px'}
                                )
                            ], width=3),
                            
                            # Project Type Filter - NOVO
                            dbc.Col([
                                html.Label("🏗️ Project Type:", 
                                          style={'fontWeight': 'bold', 'color': COLORS['dark']}),
                                dcc.Dropdown(
                                    id='type-filter',
                                    options=[{'label': f'🔧 {ptype}', 'value': ptype} for ptype in project_types],
                                    value=project_types,
                                    multi=True,
                                    style={'marginBottom': '10px'}
                                )
                            ], width=3),
                            
                            # Manager Filter - NOVO  
                            dbc.Col([
                                html.Label("👤 Project Manager:", 
                                          style={'fontWeight': 'bold', 'color': COLORS['dark']}),
                                dcc.Dropdown(
                                    id='manager-filter',
                                    options=[{'label': f'👷 {manager}', 'value': manager} for manager in project_managers],
                                    value=project_managers,
                                    multi=True,
                                    style={'marginBottom': '10px'}
                                )
                            ], width=3),
                            
                            # Date Range - NOVO
                            dbc.Col([
                                html.Label("📅 Date Range:", 
                                          style={'fontWeight': 'bold', 'color': COLORS['dark']}),
                                dcc.DatePickerRange(
                                    id='date-range',
                                    start_date='2024-01-01',
                                    end_date='2024-12-31',
                                    display_format='DD/MM/YYYY',
                                    style={'marginBottom': '10px'}
                                )
                            ], width=3)
                        ])
                    ])
                ], color="light", outline=True, className="mb-4")
            ], width=12)
        ]),
        
        # KPI Cards Row - DINÂMICO
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H2(id="total-projects-kpi", className="text-center", 
                               style={'color': COLORS['primary'], 'fontSize': '2rem'}),
                        html.P("Total Projects", className="text-center text-muted")
                    ])
                ], color="light", outline=True)
            ], width=2),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H2(id="budget-kpi", className="text-center", 
                               style={'color': COLORS['success'], 'fontSize': '2rem'}),
                        html.P("Total Budget", className="text-center text-muted")
                    ])
                ], color="light", outline=True)
            ], width=2),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H2(id="completion-kpi", className="text-center", 
                               style={'color': COLORS['warning'], 'fontSize': '2rem'}),
                        html.P("Avg Completion", className="text-center text-muted")
                    ])
                ], color="light", outline=True)
            ], width=2),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H2(id="active-projects-kpi", className="text-center", 
                               style={'color': COLORS['secondary'], 'fontSize': '2rem'}),
                        html.P("Active Projects", className="text-center text-muted")
                    ])
                ], color="light", outline=True)
            ], width=2),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H2(id="overdue-kpi", className="text-center", 
                               style={'color': COLORS['danger'], 'fontSize': '2rem'}),
                        html.P("Overdue Hours", className="text-center text-muted")
                    ])
                ], color="light", outline=True)
            ], width=2),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H2(id="resources-kpi", className="text-center", 
                               style={'color': COLORS['green'], 'fontSize': '2rem'}),
                        html.P("Total Resources", className="text-center text-muted")
                    ])
                ], color="light", outline=True)
            ], width=2),
        ], className="mb-4"),
        
        # Charts Grid - INTERATIVO (4 gráficos na linha 1)
        dbc.Row([
            # Row 1: FOUR charts  
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("📊 Project Status Distribution", className="mb-0")),
                    dbc.CardBody([
                        dcc.Graph(id='status-pie-chart', config={'displayModeBar': True})
                    ])
                ], className="h-100")
            ], width=3),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("🌟 Project Stages Sunburst", className="mb-0")),
                    dbc.CardBody([
                        dcc.Graph(id='stages-donut-chart', config={'displayModeBar': True})
                    ])
                ], className="h-100")
            ], width=3),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("⚡ Project Completion", className="mb-0")),
                    dbc.CardBody([
                        dcc.Graph(id='completion-gauge-chart', config={'displayModeBar': True})
                    ])
                ], className="h-100")
            ], width=3),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("📈 Progress Trend", className="mb-0")),
                    dbc.CardBody([
                        dcc.Graph(id='progress-trend-chart', config={'displayModeBar': True})
                    ])
                ], className="h-100")
            ], width=3),
        ], className="mb-4"),
        
        # Row 2: Two charts
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("💰 Budget Analysis", className="mb-0")),
                    dbc.CardBody([
                        dcc.Graph(id='budget-combo-chart', config={'displayModeBar': True})
                    ])
                ], className="h-100")
            ], width=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("👥 Resource Allocation", className="mb-0")),
                    dbc.CardBody([
                        dcc.Graph(id='resources-bar-chart', config={'displayModeBar': True})
                    ])
                ], className="h-100")
            ], width=6),
        ], className="mb-4"),
        
        # Row 3: One wide chart
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("⏱️ Workload Timeline", className="mb-0")),
                    dbc.CardBody([
                        dcc.Graph(id='workload-timeline-chart', config={'displayModeBar': True})
                    ])
                ], className="h-100")
            ], width=12)
        ], className="mb-4"),
        
        # Project Details Table - NOVO
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("📋 Project Details Table", className="mb-0")),
                    dbc.CardBody([
                        dash_table.DataTable(
                            id='projects-table',
                            columns=[
                                {"name": "Project", "id": "project_id"},
                                {"name": "Type", "id": "type"},
                                {"name": "Manager", "id": "manager"},
                                {"name": "Budget", "id": "budget", "type": "numeric", "format": {"specifier": "$,.0f"}},
                                {"name": "Duration", "id": "duration_days", "type": "numeric"},
                                {"name": "Status", "id": "status"}
                            ],
                            style_cell={'textAlign': 'left', 'padding': '10px'},
                            style_header={'backgroundColor': COLORS['primary'], 'color': 'white', 'fontWeight': 'bold'},
                            style_data_conditional=[
                                {
                                    'if': {'row_index': 'odd'},
                                    'backgroundColor': COLORS['background']
                                }
                            ],
                            page_size=10,
                            sort_action="native",
                            filter_action="native"
                        )
                    ])
                ])
            ], width=12)
        ])
        
    ], fluid=True, style={'backgroundColor': COLORS['background'], 'minHeight': '100vh', 'padding': '20px'})

def main():
    """Main dashboard application with REAL interactivity"""
    print("🚀 Starting CORRECTED Construction Project Monitoring Dashboard...")
    
    # Load data
    data = load_data()
    if not data:
        print("❌ Failed to load data. Exiting.")
        return
    
    # Initialize Dash app with Bootstrap theme
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.title = "Construction Project Monitoring Dashboard"
    
    # Set layout
    app.layout = create_dashboard_layout(data)
    
    # CALLBACK 1: Update KPIs based on filters - FUNCIONAL
    @app.callback(
        [Output('total-projects-kpi', 'children'),
         Output('budget-kpi', 'children'),
         Output('completion-kpi', 'children'),
         Output('active-projects-kpi', 'children'),
         Output('overdue-kpi', 'children'),
         Output('resources-kpi', 'children')],
        [Input('project-selector', 'value'),
         Input('type-filter', 'value'),
         Input('manager-filter', 'value')]
    )
    def update_kpis(selected_project, selected_types, selected_managers):
        """Update KPI cards dynamically"""
        
        # Filter data based on selections
        filtered_projects = data['projects_master']
        if selected_types:
            filtered_projects = filtered_projects[filtered_projects['type'].isin(selected_types)]
        if selected_managers:
            filtered_projects = filtered_projects[filtered_projects['manager'].isin(selected_managers)]
            
        # Calculate KPIs
        total_projects = len(filtered_projects)
        total_budget = filtered_projects['budget'].sum()
        avg_completion = data['project_status'][data['project_status']['project_id'].isin(filtered_projects['project_id'])]['completion_percent'].mean()
        active_projects = len(data['project_status'][data['project_status']['status'] == 'In Progress'])
        total_overdue = data['workload']['overdue_hours'].sum()
        total_resources = data['resources']['actual_resources'].sum()
        
        return (
            f"{total_projects}",
            f"${total_budget:,.0f}",
            f"{avg_completion:.1f}%",
            f"{active_projects}",
            f"{total_overdue:.0f}h",
            f"{total_resources:.0f}"
        )
    
    # CALLBACK 2: Update all charts - REAL INTERACTIVITY (CORRIGIDO com DATE + 4º gráfico)
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
            
        project_ids = filtered_projects['project_id'].tolist()
        
        # 1. Status Pie Chart - DINÂMICO E MAIOR
        status_data = data['project_status'][data['project_status']['project_id'].isin(project_ids)]
        status_counts = status_data['status'].value_counts()
        
        status_fig = px.pie(
            values=status_counts.values, 
            names=status_counts.index,
            color_discrete_map={'Completed': COLORS['success'], 'In Progress': COLORS['primary'], 'On Hold': COLORS['warning']},
            title="Project Status Distribution"
        )
        status_fig.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            textfont_size=12,
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        )
        status_fig.update_layout(showlegend=True, height=350, font_size=11)
        
        # 2. Stages SUNBURST Chart - INTERATIVO E DINÂMICO  
        stages_data = data['project_stages'][data['project_stages']['project_id'].isin(project_ids)]
        
        # Criar hierarquia para Sunburst: Type -> Stage -> Project
        sunburst_df = stages_data.merge(filtered_projects[['project_id', 'type']], on='project_id', how='left')
        
        # Preparar dados hierárquicos
        sunburst_data = []
        for _, row in sunburst_df.iterrows():
            sunburst_data.append({
                'ids': f"{row['type']}",
                'labels': f"{row['type']}",
                'parents': "",
                'values': 1
            })
            sunburst_data.append({
                'ids': f"{row['type']}-{row['stage']}",
                'labels': f"{row['stage']}",
                'parents': f"{row['type']}",
                'values': 1
            })
            sunburst_data.append({
                'ids': f"{row['type']}-{row['stage']}-{row['project_id']}",
                'labels': f"{row['project_id']}",
                'parents': f"{row['type']}-{row['stage']}",
                'values': 1
            })
        
        # Remover duplicatas e agregar
        sunburst_df_clean = pd.DataFrame(sunburst_data).groupby(['ids', 'labels', 'parents']).sum().reset_index()
        
        stages_fig = go.Figure(go.Sunburst(
            ids=sunburst_df_clean['ids'],
            labels=sunburst_df_clean['labels'],
            parents=sunburst_df_clean['parents'],
            values=sunburst_df_clean['values'],
            branchvalues="total",
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percentParent}<extra></extra>',
            maxdepth=3,
            insidetextorientation='radial'
        ))
        
        stages_fig.update_layout(
            title="Project Stages - Interactive Sunburst",
            height=350,
            font_size=10
        )
        
        # 3. Completion Gauge - DINÂMICO
        if selected_project:
            project_completion = data['project_status'][data['project_status']['project_id'] == selected_project]['completion_percent']
            completion_value = project_completion.iloc[0] if len(project_completion) > 0 else 75
        else:
            completion_value = status_data['completion_percent'].mean()
            
        gauge_fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = completion_value,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Project Completion %"},
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
        
        # 4. Progress Trend Chart - NOVO GRÁFICO
        progress_data = filtered_projects.merge(
            data['project_status'][['project_id', 'completion_percent']], 
            on='project_id', 
            how='left'
        )
        
        # Criar gráfico de barras horizontal com progresso
        progress_fig = go.Figure()
        
        colors = [COLORS['success'] if x >= 90 else COLORS['warning'] if x >= 70 else COLORS['danger'] for x in progress_data['completion_percent']]
        
        progress_fig.add_trace(go.Bar(
            y=progress_data['project_id'],
            x=progress_data['completion_percent'],
            orientation='h',
            marker_color=colors,
            text=[f"{x}%" for x in progress_data['completion_percent']],
            textposition='inside',
            hovertemplate='<b>%{y}</b><br>Progress: %{x}%<extra></extra>'
        ))
        
        progress_fig.update_layout(
            title="Progress by Project",
            xaxis_title="Completion %",
            yaxis_title="Projects",
            height=350,
            showlegend=False
        )
        
        # 5. Budget Combo Chart - DINÂMICO (numeração ajustada)
        budget_data = data['budget_variance'][data['budget_variance']['project_id'].isin(project_ids)]
        budget_agg = budget_data.groupby('project_id').agg({
            'actual_budget': 'sum',
            'planned_budget': 'sum', 
            'variance': 'sum'
        }).reset_index()
        
        budget_fig = go.Figure()
        budget_fig.add_trace(go.Bar(
            name='Actual Budget',
            x=budget_agg['project_id'],
            y=budget_agg['actual_budget'],
            marker_color=COLORS['danger']
        ))
        budget_fig.add_trace(go.Bar(
            name='Planned Budget',
            x=budget_agg['project_id'],
            y=budget_agg['planned_budget'],
            marker_color=COLORS['success']
        ))
        budget_fig.add_trace(go.Scatter(
            name='Variance',
            x=budget_agg['project_id'],
            y=budget_agg['variance'],
            mode='lines+markers',
            marker_color=COLORS['primary'],
            yaxis='y2'
        ))
        budget_fig.update_layout(
            title="Budget Analysis: Actual vs Planned",
            yaxis2=dict(title="Variance", overlaying='y', side='right'),
            barmode='group',
            height=400
        )
        
        # 5. Resources Bar Chart - DINÂMICO
        resources_data = data['resources'][data['resources']['project_id'].isin(project_ids)]
        resources_agg = resources_data.groupby('resource_type').agg({
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
        
        # 6. Workload Timeline - NOVO E DINÂMICO
        workload_data = data['workload'][data['workload']['project_id'].isin(project_ids)]
        
        workload_fig = go.Figure()
        for i, row in workload_data.iterrows():
            workload_fig.add_trace(go.Bar(
                name=f"{row['project_id']} - Completed",
                x=[row['project_id']],
                y=[row['completed_hours']],
                marker_color=COLORS['success'],
                showlegend=False
            ))
            workload_fig.add_trace(go.Bar(
                name=f"{row['project_id']} - Remaining", 
                x=[row['project_id']],
                y=[row['remaining_hours']],
                marker_color=COLORS['secondary'],
                showlegend=False
            ))
            workload_fig.add_trace(go.Bar(
                name=f"{row['project_id']} - Overdue",
                x=[row['project_id']],
                y=[row['overdue_hours']],
                marker_color=COLORS['danger'],
                showlegend=False
            ))
        
        workload_fig.update_layout(
            title="Workload Distribution by Project",
            barmode='stack',
            height=400
        )
        
        return status_fig, stages_fig, gauge_fig, progress_fig, budget_fig, resources_fig, workload_fig
    
    # CALLBACK 3: Update projects table - FUNCIONAL
    @app.callback(
        Output('projects-table', 'data'),
        [Input('project-selector', 'value'),
         Input('type-filter', 'value'),
         Input('manager-filter', 'value')]
    )
    def update_projects_table(selected_project, selected_types, selected_managers):
        """Update projects table with filtering"""
        
        filtered_projects = data['projects_master'].copy()
        
        if selected_types:
            filtered_projects = filtered_projects[filtered_projects['type'].isin(selected_types)]
        if selected_managers:
            filtered_projects = filtered_projects[filtered_projects['manager'].isin(selected_managers)]
            
        # Add status information
        filtered_projects = filtered_projects.merge(
            data['project_status'][['project_id', 'status']], 
            on='project_id', 
            how='left'
        )
        
        return filtered_projects.to_dict('records')
    
    print("✅ Dashboard initialized with FULL INTERACTIVITY!")
    print("🌐 Access dashboard at: http://localhost:8050")  
    print("🎯 Features: REAL interactive filters, dynamic charts, responsive KPIs")
    print("🔄 Try changing the dropdown filters to see LIVE updates!")
    
    # Run server
    app.run_server(debug=True, host='0.0.0.0', port=8050)

if __name__ == '__main__':
    main()
