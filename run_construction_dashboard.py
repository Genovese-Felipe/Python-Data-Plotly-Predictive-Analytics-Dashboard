#!/usr/bin/env python3
"""
A professional and interactive dashboard for monitoring construction projects.

This script creates a comprehensive web-based dashboard using Plotly and Dash,
designed to provide real-time analytics and insights into construction project
management. It features a variety of visualizations, including KPIs, charts,
and timelines, all of which are dynamically updated based on user-selected
filters.

The dashboard adheres to professional design principles, with a clean layout,
a consistent color scheme, and responsive components.
"""

import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# Professional color palette
COLORS = {
    'primary': '#2563eb',
    'secondary': '#64748b',
    'success': '#059669',
    'warning': '#d97706',
    'danger': '#dc2626',
    'info': '#0891b2',
    'light': '#f1f5f9',
    'dark': '#1e293b',
}

# Layout configuration
LAYOUT_CONFIG = {
    'font_family': 'Inter, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif',
    'card_shadow': '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
    'border_radius': '12px',
    'spacing': '24px'
}


def generate_construction_data():
    """
    Generates a sample DataFrame of construction project data.

    This function creates a realistic dataset for demonstration purposes,
    including project details such as type, budget, duration, and status.

    Returns:
        pd.DataFrame: A DataFrame containing the generated project data.
    """
    np.random.seed(42)
    n_projects = 25
    project_types = ['Residential', 'Commercial', 'Infrastructure', 'Industrial']
    work_statuses = ['In Progress', 'Completed', 'Not Started']
    project_stages = ['Design', 'Plan', 'Pre-construction']

    data = {
        'project_id': [f'Project_{i+1}' for i in range(n_projects)],
        'project_name': [f'Construction Project {i+1}' for i in range(n_projects)],
        'project_type': np.random.choice(project_types, n_projects),
        'project_head': [f'Manager {chr(65+i%26)}' for i in range(n_projects)],
        'start_date': pd.to_datetime(pd.date_range('2024-01-01', periods=n_projects, freq='W')),
        'total_budget': np.random.randint(100000, 1000000, n_projects),
        'planned_duration': np.random.randint(180, 1100, n_projects),
        'current_completion': np.random.randint(20, 100, n_projects),
        'work_status': np.random.choice(work_statuses, n_projects),
        'current_stage': np.random.choice(project_stages, n_projects)
    }
    return pd.DataFrame(data)


def create_professional_card(title, content, icon="📊"):
    """
    Creates a styled card component for the dashboard layout.

    Args:
        title (str): The title of the card.
        content (dash.development.base_component.Component): The content of the card.
        icon (str, optional): The icon to display next to the title. Defaults to "📊".

    Returns:
        dbc.Card: A styled card component.
    """
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
    """
    Creates a Key Performance Indicator (KPI) card.

    Args:
        title (str): The title of the KPI.
        value (str): The value of the KPI.
        icon (str): The icon for the KPI.
        color_type (str): The color type to use for styling.

    Returns:
        dbc.Card: A styled KPI card.
    """
    color = COLORS.get(color_type, COLORS['primary'])
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                html.H2(icon, style={'fontSize': '2rem', 'color': color}),
                html.H3(value, style={'fontWeight': 'bold', 'color': COLORS['dark']}),
                html.P(title, style={'color': COLORS['secondary']})
            ], style={'textAlign': 'center'})
        ])
    ], style={
        'boxShadow': LAYOUT_CONFIG['card_shadow'],
        'borderRadius': LAYOUT_CONFIG['border_radius'],
        'border': 'none',
        'height': '150px'
    })


def create_filter_section(df):
    """
    Creates the filter section of the dashboard.

    Args:
        df (pd.DataFrame): The DataFrame to use for populating filter options.

    Returns:
        html.Div: A Div component containing all the filters.
    """
    return html.Div([
        dbc.Row([
            dbc.Col(dcc.Dropdown(
                id='project-filter',
                options=[{'label': 'All Projects', 'value': 'All'}] +
                        [{'label': p_type, 'value': p_type} for p_type in df['project_type'].unique()],
                value='All',
                placeholder="Filter by Project Type"
            ), width=3),
            dbc.Col(dcc.Dropdown(
                id='status-filter',
                options=[{'label': 'All Status', 'value': 'All'}] +
                        [{'label': status, 'value': status} for status in df['work_status'].unique()],
                value='All',
                placeholder="Filter by Status"
            ), width=3),
            dbc.Col(dcc.DatePickerRange(
                id='date-range-picker',
                start_date=df['start_date'].min().date(),
                end_date=df['start_date'].max().date(),
                display_format='YYYY-MM-DD'
            ), width=4),
        ])
    ], style={
        'backgroundColor': '#ffffff',
        'padding': '20px',
        'borderRadius': LAYOUT_CONFIG['border_radius'],
        'boxShadow': LAYOUT_CONFIG['card_shadow'],
        'marginBottom': '30px'
    })


def create_work_status_donut(df):
    """
    Creates a donut chart for work status distribution.

    Args:
        df (pd.DataFrame): The DataFrame containing project data.

    Returns:
        go.Figure: A Plotly figure object.
    """
    status_counts = df['work_status'].value_counts()
    fig = px.pie(
        status_counts,
        values=status_counts.values,
        names=status_counts.index,
        hole=0.4,
        title="Project Work Status",
        color_discrete_sequence=[COLORS['success'], COLORS['primary'], COLORS['warning']]
    )
    fig.update_layout(showlegend=True, font_family=LAYOUT_CONFIG['font_family'])
    return fig


def create_stage_pie_chart(df):
    """
    Creates a pie chart for project stages.

    Args:
        df (pd.DataFrame): The DataFrame containing project data.

    Returns:
        go.Figure: A Plotly figure object.
    """
    stage_counts = df['current_stage'].value_counts()
    fig = px.pie(
        stage_counts,
        values=stage_counts.values,
        names=stage_counts.index,
        title="Projects by Stage",
        color_discrete_sequence=[COLORS['primary'], COLORS['success'], COLORS['info']]
    )
    fig.update_layout(showlegend=True, font_family=LAYOUT_CONFIG['font_family'])
    return fig


def create_completion_gauge(completion_percent, title="Project Completion"):
    """
    Creates a gauge chart for completion metrics.

    Args:
        completion_percent (float): The overall completion percentage.
        title (str, optional): The title of the gauge. Defaults to "Project Completion".

    Returns:
        go.Figure: A Plotly figure object.
    """
    gauge_color = COLORS['success'] if completion_percent >= 80 else COLORS['warning'] if completion_percent >= 50 else COLORS['danger']
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=completion_percent,
        title={'text': title},
        gauge={'axis': {'range': [None, 100]}, 'bar': {'color': gauge_color}}
    ))
    fig.update_layout(font_family=LAYOUT_CONFIG['font_family'])
    return fig


def create_performance_bar_chart(df):
    """
    Creates a bar chart to analyze project performance.

    Args:
        df (pd.DataFrame): The DataFrame containing project data.

    Returns:
        go.Figure: A Plotly figure object.
    """
    performance_data = df.groupby('project_name')['current_completion'].mean().sort_values()
    fig = px.bar(
        performance_data,
        x=performance_data.values,
        y=performance_data.index,
        orientation='h',
        title="Project Performance Analysis",
        labels={'x': 'Completion Percentage (%)', 'y': 'Projects'},
        color=performance_data.values,
        color_continuous_scale='Viridis'
    )
    fig.update_layout(font_family=LAYOUT_CONFIG['font_family'])
    return fig


def create_budget_variance_combo(df):
    """
    Creates a combo chart for budget variance analysis.

    Args:
        df (pd.DataFrame): The DataFrame to use for the chart.

    Returns:
        go.Figure: A Plotly figure object.
    """
    df['actual_cost'] = df['total_budget'] * (df['current_completion'] / 100.0) * np.random.uniform(0.9, 1.1, len(df))
    df['variance'] = df['actual_cost'] - df['total_budget']
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['project_name'], y=df['total_budget'], name='Budget', marker_color=COLORS['primary']))
    fig.add_trace(go.Bar(x=df['project_name'], y=df['actual_cost'], name='Actual Cost', marker_color=COLORS['info']))
    fig.add_trace(go.Scatter(x=df['project_name'], y=df['variance'], name='Variance', yaxis='y2', line=dict(color=COLORS['danger'])))
    
    fig.update_layout(
        title="Budget Variance - Actual vs Planned",
        yaxis={'title': 'Amount ($)'},
        yaxis2={'title': 'Variance ($)', 'overlaying': 'y', 'side': 'right'},
        font_family=LAYOUT_CONFIG['font_family']
    )
    return fig


def create_kpi_summary_cards(df):
    """
    Creates a list of KPI card data for the dashboard header.

    Args:
        df (pd.DataFrame): The DataFrame to calculate KPIs from.

    Returns:
        list: A list of dictionaries, where each dictionary represents a KPI card.
    """
    total_projects = len(df)
    avg_completion = df['current_completion'].mean()
    total_budget = df['total_budget'].sum()
    active_projects = len(df[df['work_status'] == 'In Progress'])

    kpis = [
        {'title': 'Total Projects', 'value': str(total_projects), 'icon': '📊', 'color': 'primary'},
        {'title': 'Avg Completion', 'value': f"{avg_completion:.1f}%", 'icon': '📈', 'color': 'success'},
        {'title': 'Total Budget', 'value': f"${total_budget/1000000:.1f}M", 'icon': '💰', 'color': 'info'},
        {'title': 'Active Projects', 'value': str(active_projects), 'icon': '🔥', 'color': 'warning'}
    ]
    return kpis


# Initialize the Dash application
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Construction Project Monitoring Dashboard"

# Generate data and create the layout
df_initial = generate_construction_data()
app.layout = html.Div([
    html.H1("🏗️ Construction Project Monitoring Dashboard", style={'textAlign': 'center', 'color': COLORS['dark']}),
    html.P("Professional Analytics for Construction Project Management", style={'textAlign': 'center', 'color': COLORS['secondary']}),
    dbc.Row([dbc.Col(create_kpi_card(kpi['title'], kpi['value'], kpi['icon'], kpi['color']), width=3) for kpi in create_kpi_summary_cards(df_initial)]),
    create_filter_section(df_initial),
    dbc.Row([
        dbc.Col(create_professional_card("Work Status Distribution", dcc.Graph(id='work-status-donut')), width=6),
        dbc.Col(create_professional_card("Project Stages", dcc.Graph(id='project-stages-pie')), width=6),
    ]),
    dbc.Row([
        dbc.Col(create_professional_card("Overall Completion", dcc.Graph(id='completion-gauge')), width=4),
        dbc.Col(create_professional_card("Project Performance", dcc.Graph(id='performance-bar')), width=8),
    ]),
    dbc.Row([
        dbc.Col(create_professional_card("Budget Variance Analysis", dcc.Graph(id='budget-variance-combo')), width=12),
    ]),
], style={'backgroundColor': '#f8f9fa', 'padding': '20px', 'fontFamily': LAYOUT_CONFIG['font_family']})


@app.callback(
    [Output('work-status-donut', 'figure'),
     Output('project-stages-pie', 'figure'),
     Output('performance-bar', 'figure'),
     Output('completion-gauge', 'figure'),
     Output('budget-variance-combo', 'figure')],
    [Input('project-filter', 'value'),
     Input('status-filter', 'value'),
     Input('date-range-picker', 'start_date'),
     Input('date-range-picker', 'end_date')]
)
def update_charts(selected_project, selected_status, start_date, end_date):
    """
    Updates the dashboard charts based on the selected filters.

    This callback is triggered when any of the filter values change. It filters
    the data and regenerates all the charts in the dashboard.

    Args:
        selected_project (str): The selected project type.
        selected_status (str): The selected work status.
        start_date (str): The start date of the date range.
        end_date (str): The end date of the date range.

    Returns:
        tuple: A tuple of updated Plotly figure objects for all the charts.
    """
    filtered_df = df_initial.copy()

    if selected_project and selected_project != 'All':
        filtered_df = filtered_df[filtered_df['project_type'] == selected_project]
    
    if selected_status and selected_status != 'All':
        filtered_df = filtered_df[filtered_df['work_status'] == selected_status]

    if start_date and end_date:
        filtered_df = filtered_df[
            (filtered_df['start_date'] >= pd.to_datetime(start_date)) &
            (filtered_df['start_date'] <= pd.to_datetime(end_date))
        ]

    donut_fig = create_work_status_donut(filtered_df)
    pie_fig = create_stage_pie_chart(filtered_df)
    bar_fig = create_performance_bar_chart(filtered_df)
    gauge_fig = create_completion_gauge(filtered_df['current_completion'].mean())
    budget_fig = create_budget_variance_combo(filtered_df)

    return donut_fig, pie_fig, bar_fig, gauge_fig, budget_fig


if __name__ == '__main__':
    print("🚀 Starting Construction Project Monitoring Dashboard...")
    print("📊 Dashboard available at: http://localhost:8050")
    app.run_server(debug=True)