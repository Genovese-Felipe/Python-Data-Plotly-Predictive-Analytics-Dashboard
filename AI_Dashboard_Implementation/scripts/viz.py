"""
A professional visualization script for the construction project dashboard.

This script uses Plotly and Dash to create a comprehensive and interactive
dashboard for monitoring construction projects. It includes a variety of
visualizations, KPI cards, and interactive filters to provide a detailed
overview of a project portfolio.
"""

import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
import sys

# Add the parent directory to the path to allow imports from the 'scripts' directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Professional color palette
COLOR_PALETTE = {
    'primary': '#3498db', 'secondary': '#2ecc71', 'success': '#27ae60',
    'warning': '#f39c12', 'danger': '#e74c3c', 'info': '#17a2b8',
    'dark': '#2c3e50', 'light': '#ecf0f1'
}


class ConstructionDashboard:
    """
    A class to create and manage the construction project dashboard.

    This class encapsulates all the functionality for the dashboard, including
    data loading, KPI calculations, chart creation, and layout setup.
    """

    def __init__(self):
        """Initializes the dashboard, loads data, and sets up the layout."""
        self.load_data()
        self.app = dash.Dash(__name__)
        self.setup_layout()
        self.setup_callbacks()

    def load_data(self):
        """Loads all necessary data from CSV files."""
        data_path = os.path.join(os.path.dirname(__file__), '../data')
        try:
            self.projects_df = pd.read_csv(f'{data_path}/projects_master.csv', parse_dates=['start_date', 'end_date'])
            self.resources_df = pd.read_csv(f'{data_path}/resources.csv')
            self.workload_df = pd.read_csv(f'{data_path}/workload.csv')
            self.budget_df = pd.read_csv(f'{data_path}/budget_variance.csv', parse_dates=['date'])
            print("✅ All data files loaded successfully.")
        except FileNotFoundError as e:
            print(f"❌ Error loading data: {e}. Please run the data generation script.")
            # Create empty dataframes to prevent crashes
            self.projects_df = pd.DataFrame()
            self.resources_df = pd.DataFrame()
            self.workload_df = pd.DataFrame()
            self.budget_df = pd.DataFrame()

    def calculate_kpis(self):
        """
        Calculates Key Performance Indicators (KPIs) from the loaded data.

        Returns:
            dict: A dictionary of calculated KPIs.
        """
        if self.projects_df.empty:
            return {
                'total_projects': 0, 'active_projects': 0, 'total_budget': 0,
                'budget_utilization': 0, 'avg_completion': 0
            }
        
        total_projects = len(self.projects_df)
        active_projects = len(self.projects_df[self.projects_df['status'] == 'In Progress'])
        total_budget = self.projects_df['budget_allocated'].sum()
        budget_utilization = (self.projects_df['budget_spent'].sum() / total_budget) * 100 if total_budget > 0 else 0
        avg_completion = self.projects_df['completion_percentage'].mean()
        
        return {
            'total_projects': total_projects, 'active_projects': active_projects,
            'total_budget': total_budget, 'budget_utilization': budget_utilization,
            'avg_completion': avg_completion
        }

    def create_kpi_cards(self):
        """
        Creates the KPI cards section of the dashboard.

        Returns:
            html.Div: A Div component containing the KPI cards.
        """
        kpis = self.calculate_kpis()
        card_style = {'padding': '20px', 'textAlign': 'center', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'}
        
        return html.Div([
            html.Div(f"Total Projects: {kpis['total_projects']}", style=card_style),
            html.Div(f"Active Projects: {kpis['active_projects']}", style=card_style),
            html.Div(f"Budget Utilization: {kpis['budget_utilization']:.1f}%", style=card_style),
            html.Div(f"Avg Completion: {kpis['avg_completion']:.1f}%", style=card_style),
        ], style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr 1fr 1fr', 'gap': '20px', 'margin': '20px'})

    def create_project_status_chart(self):
        """
        Creates a pie chart for the project status distribution.

        Returns:
            go.Figure: A Plotly figure object.
        """
        if self.projects_df.empty: return go.Figure()
        status_counts = self.projects_df['status'].value_counts()
        return px.pie(status_counts, values=status_counts.values, names=status_counts.index, title="Project Status Distribution")

    def create_budget_performance_chart(self):
        """
        Creates a bar chart comparing allocated vs. spent budget by project type.

        Returns:
            go.Figure: A Plotly figure object.
        """
        if self.projects_df.empty: return go.Figure()
        budget_summary = self.projects_df.groupby('project_type').agg({'budget_allocated': 'sum', 'budget_spent': 'sum'}).reset_index()
        return px.bar(budget_summary, x='project_type', y=['budget_allocated', 'budget_spent'], barmode='group', title="Budget vs. Spending by Type")

    def setup_layout(self):
        """Sets up the main layout of the dashboard."""
        self.app.layout = html.Div([
            html.H1("🏗️ Construction Project Management Dashboard", style={'textAlign': 'center', 'padding': '20px'}),
            dcc.Dropdown(
                id='project-type-filter',
                options=[{'label': t, 'value': t} for t in self.projects_df['project_type'].unique()],
                value=self.projects_df['project_type'].unique().tolist(),
                multi=True,
                style={'margin': '20px'}
            ),
            html.Div(id='kpi-cards'),
            dcc.Graph(id='status-chart'),
            dcc.Graph(id='budget-performance-chart'),
        ])

    def setup_callbacks(self):
        """Sets up the callbacks for dashboard interactivity."""
        @self.app.callback(
            [Output('kpi-cards', 'children'),
             Output('status-chart', 'figure'),
             Output('budget-performance-chart', 'figure')],
            [Input('project-type-filter', 'value')]
        )
        def update_dashboard(selected_types):
            """
            Updates all dashboard components based on selected filters.

            Args:
                selected_types (list): The list of selected project types.

            Returns:
                tuple: A tuple containing the updated KPI cards and chart figures.
            """
            original_df = self.projects_df.copy()
            if selected_types:
                self.projects_df = self.projects_df[self.projects_df['project_type'].isin(selected_types)]
            
            kpi_cards = self.create_kpi_cards()
            status_chart = self.create_project_status_chart()
            budget_chart = self.create_budget_performance_chart()
            
            self.projects_df = original_df  # Restore original df
            return kpi_cards, status_chart, budget_chart

    def run_server(self, debug=True, port=8050):
        """
        Runs the Dash server for the interactive dashboard.

        Args:
            debug (bool, optional): Whether to run the server in debug mode.
            port (int, optional): The port to run the server on.
        """
        print(f"🚀 Starting Construction Dashboard server on http://localhost:{port}")
        self.app.run_server(debug=debug, port=port)


if __name__ == "__main__":
    dashboard = ConstructionDashboard()
    dashboard.run_server()