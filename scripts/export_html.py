#!/usr/bin/env python3
"""
A script to export the construction project monitoring dashboard to a static HTML file.

This script loads the project data, generates all the necessary visualizations by
calling functions from an external 'viz' script, and then embeds them into a
single, self-contained HTML file.
"""

import os
import sys
import pandas as pd
import plotly.offline as pyo

# Add parent directory to path to import visualization functions
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import functions from a compatible visualization script
# Note: This script depends on a version of 'viz.py' containing these specific functions.
from scripts.viz_backup import (
    load_data, create_gauge_chart, create_project_work_status_chart,
    create_projects_by_stage_chart, create_budget_variance_chart,
    create_resources_chart, create_workload_chart, COLORS
)


def generate_html_dashboard():
    """
    Generates a complete HTML dashboard with all visualizations embedded.

    This function orchestrates the entire export process. It loads the data,
    creates all the chart figures, and then constructs a final HTML document
    with the charts embedded within a styled layout.

    Returns:
        bool: True if the export was successful, False otherwise.
    """
    print("🔄 Starting HTML export process...")

    # Load data
    data = load_data()
    if not data:
        print("❌ Failed to load data. Cannot export.")
        return False

    # Create all visualizations
    print("📊 Creating visualizations...")
    work_status_fig = create_project_work_status_chart(data['project_status'])
    projects_stage_fig = create_projects_by_stage_chart(data['project_stages'])
    completion_gauge_fig = create_gauge_chart(100, 100, "Project Completion", COLORS.get('green', '#28a745'))
    budget_variance_fig = create_budget_variance_chart(data['budget_variance'])
    resources_fig = create_resources_chart(data['resources'])
    workload_fig = create_workload_chart(data['workload'])

    # Get project data for header info
    print("🏗️ Building HTML structure...")
    projects_master = data['projects_master']
    project_status = data['project_status']
    selected_project = projects_master[projects_master['project_id'] == 'Project_1'].iloc[0]
    selected_status = project_status[project_status['project_id'] == 'Project_1'].iloc[0]

    # Generate individual chart HTML elements
    work_status_html = pyo.plot(work_status_fig, include_plotlyjs=False, output_type='div')
    projects_stage_html = pyo.plot(projects_stage_fig, include_plotlyjs=False, output_type='div')
    completion_gauge_html = pyo.plot(completion_gauge_fig, include_plotlyjs=False, output_type='div')
    budget_variance_html = pyo.plot(budget_variance_fig, include_plotlyjs=False, output_type='div')
    resources_html = pyo.plot(resources_fig, include_plotlyjs=False, output_type='div')
    workload_html = pyo.plot(workload_fig, include_plotlyjs=False, output_type='div')

    # Create final HTML with embedded charts
    final_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Construction Project Dashboard</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #F8F9FA; }}
            .header, .project-info, .chart-container, .footer {{
                background-color: white; padding: 20px; margin-bottom: 20px;
                border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .charts-grid {{ display: grid; grid-gap: 15px; }}
            .chart-row-3 {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); grid-gap: 15px; }}
            .chart-row-2 {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); grid-gap: 15px; }}
        </style>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    </head>
    <body>
        <div class="header"><h1>Construction Project Monitoring Dashboard</h1></div>
        <div class="project-info">
            <h3>Project Information</h3>
            <p><strong>Project:</strong> {selected_project['project_id']}</p>
            <p><strong>Type:</strong> {selected_project['type']}</p>
            <p><strong>Manager:</strong> {selected_project['manager']}</p>
        </div>
        <div class="charts-grid">
            <div class="chart-row-3">
                <div class="chart-container">{work_status_html}</div>
                <div class="chart-container">{projects_stage_html}</div>
                <div class="chart-container">{completion_gauge_html}</div>
            </div>
            <div class="chart-row-2">
                <div class="chart-container">{budget_variance_html}</div>
                <div class="chart-container">{resources_html}</div>
            </div>
            <div class="chart-row-1"><div class="chart-container">{workload_html}</div></div>
        </div>
        <div class="footer"><p>Dashboard generated on {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}</p></div>
    </body>
    </html>
    """

    # Write to file
    output_path = 'outputs/dashboard.html'
    os.makedirs('outputs', exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_html)

    print("✅ Dashboard exported successfully!")
    print(f"📁 File location: {os.path.abspath(output_path)}")
    return True


if __name__ == '__main__':
    generate_html_dashboard()