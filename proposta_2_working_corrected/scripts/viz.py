"""
An interactive dashboard for analyzing project performance.

This script uses Plotly and Dash to create a comprehensive dashboard with
KPIs, automated insights, and a variety of interactive charts for deep-diving
into project performance metrics.
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import datetime as dt
import os
import sys

# Global settings - Professional color palette
COLOR_PALETTE = {
    'primary': '#3366cc', 'secondary': '#dc3912', 'success': '#109618',
    'danger': '#cb3d3d', 'warning': '#ff9900', 'info': '#0099c6',
    'light': '#f9f9f9', 'dark': '#333333', 'text': '#505050'
}


def load_data():
    """
    Loads and preprocesses the project data from CSV files.

    If the data files are not found, it attempts to generate them by calling
    the data generation scripts.

    Returns:
        tuple: A tuple of pandas DataFrames for each dataset.
    """
    try:
        data_path = os.path.join(os.path.dirname(__file__), '../data')
        df_projects = pd.read_csv(os.path.join(data_path, 'projects.csv'))
        df_milestones = pd.read_csv(os.path.join(data_path, 'project_milestones.csv'))
        df_financials = pd.read_csv(os.path.join(data_path, 'monthly_financials.csv'))
        df_resources = pd.read_csv(os.path.join(data_path, 'project_resources.csv'))

        for col in ['start_date', 'planned_completion_date', 'actual_completion_date']:
            df_projects[col] = pd.to_datetime(df_projects[col])
        df_milestones['planned_date'] = pd.to_datetime(df_milestones['planned_date'])
        df_financials['date'] = pd.to_datetime(df_financials['date'])

        print("Data loaded successfully.")
        return df_projects, df_milestones, df_financials, df_resources
    except FileNotFoundError:
        print("Data files not found. Generating new data...")
        from data_gen import generate_project_data, generate_resource_data
        df_projects, df_milestones, df_financials = generate_project_data(200)
        df_resources = generate_resource_data(df_projects)
        return df_projects, df_milestones, df_financials, df_resources


def create_kpi_card(title, value, change=None, icon=None, color='primary'):
    """
    Creates a styled card for displaying a Key Performance Indicator (KPI).

    Args:
        title (str): The title of the KPI.
        value (str): The value of the KPI.
        change (str, optional): The change from the previous period.
        icon (str, optional): The Font Awesome icon name.
        color (str, optional): The color theme for the card.

    Returns:
        dbc.Card: A styled KPI card component.
    """
    card_content = [
        html.Div([
            html.Div([
                html.H4(title, className="card-title text-muted"),
                html.H2(value, className="card-value", style={'color': COLOR_PALETTE[color]})
            ], className="col-9"),
            html.Div(html.I(className=f"fa fa-{icon} fa-3x text-{color}"), className="col-3 text-right")
        ], className="row")
    ]
    if change:
        card_content.append(html.Div(f"{change} vs. previous period", className="small text-muted"))
    return dbc.Card(dbc.CardBody(card_content), className="kpi-card h-100 shadow-sm")


# Load data and initialize app
df_projects, df_milestones, df_financials, df_resources = load_data()
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY, dbc.icons.FONT_AWESOME])
server = app.server

# App layout
app.layout = dbc.Container(fluid=True, children=[
    html.H1("Project Performance Dashboard", className="my-4"),
    dbc.Row([
        dbc.Col(dcc.DatePickerRange(id='date-filter', start_date=df_projects['start_date'].min(), end_date=df_projects['actual_completion_date'].max()), width=4),
        dbc.Col(dcc.Dropdown(id='type-filter', options=[{'label': t, 'value': t} for t in df_projects['project_type'].unique()], multi=True, placeholder="Filter by Type"), width=4),
        dbc.Col(dcc.Dropdown(id='region-filter', options=[{'label': r, 'value': r} for r in df_projects['region'].unique()], multi=True, placeholder="Filter by Region"), width=4),
    ]),
    dbc.Row([
        dbc.Col(create_kpi_card("Total Projects", f"{len(df_projects)}", "+12%", "clipboard-list"), width=3),
        dbc.Col(create_kpi_card("Total Value", f"${df_projects['budget'].sum()/1e6:.1f}M", "+8.3%", "dollar-sign", "success"), width=3),
        dbc.Col(create_kpi_card("On-Time Projects", f"{sum(df_projects['delay_days'] == 0) / len(df_projects) * 100:.1f}%", "-2.5%", "calendar-check", "info"), width=3),
        dbc.Col(create_kpi_card("Avg. Satisfaction", f"{df_projects['satisfaction_cliente'].mean():.1f}/10", "+0.8", "smile", "warning"), width=3)
    ], className="my-4"),
    dbc.Row([
        dbc.Col(dcc.Graph(id='portfolio-trend-chart'), width=8),
        dbc.Col(dcc.Graph(id='status-chart'), width=4),
    ])
])


@callback(
    [Output('portfolio-trend-chart', 'figure'),
     Output('status-chart', 'figure')],
    [Input('date-filter', 'start_date'),
     Input('date-filter', 'end_date'),
     Input('type-filter', 'value'),
     Input('region-filter', 'value')]
)
def update_charts(start_date, end_date, types, regions):
    """
    Updates the dashboard charts based on the selected filters.

    Args:
        start_date (str): The start date of the date range.
        end_date (str): The end date of the date range.
        types (list): A list of selected project types.
        regions (list): A list of selected regions.

    Returns:
        tuple: A tuple of updated Plotly figure objects.
    """
    filtered_df = df_projects.copy()
    if start_date and end_date:
        filtered_df = filtered_df[(filtered_df['start_date'] >= start_date) & (filtered_df['planned_completion_date'] <= end_date)]
    if types:
        filtered_df = filtered_df[filtered_df['project_type'].isin(types)]
    if regions:
        filtered_df = filtered_df[filtered_df['region'].isin(regions)]

    # Portfolio Trend Chart
    if filtered_df.empty:
        fig_trend = px.line(title="No data available for selected filters")
    else:
        df_trend = filtered_df.groupby(filtered_df['start_date'].dt.to_period('M')).size().reset_index(name='count')
        df_trend['start_date'] = df_trend['start_date'].dt.to_timestamp()
        fig_trend = px.line(df_trend, x='start_date', y='count', title='Portfolio Evolution Over Time')

    # Status Chart
    if filtered_df.empty:
        fig_status = px.pie(title="No data available")
    else:
        status_counts = filtered_df['status'].value_counts()
        fig_status = px.pie(status_counts, values='count', names=status_counts.index, title='Project Status Distribution')
    
    return fig_trend, fig_status


if __name__ == '__main__':
    app.run_server(debug=True)