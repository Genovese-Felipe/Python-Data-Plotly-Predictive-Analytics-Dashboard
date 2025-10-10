#!/usr/bin/env python3
"""
A script to generate a static HTML dashboard for GitHub Pages.

This utility creates a self-contained HTML file with embedded Plotly charts,
showcasing a professional construction project management dashboard. It generates
its own sample data and is designed for easy deployment on static hosting
platforms like GitHub Pages.
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_static_dashboard():
    """
    Generates a static Plotly figure containing multiple dashboard charts.

    This function first creates a synthetic dataset for construction projects
    and then uses this data to build a multi-plot figure with subplots for
    various project metrics, such as status, budget, completion, and resources.

    Returns:
        go.Figure: A Plotly figure object containing the complete dashboard layout.
    """
    np.random.seed(42)
    
    # Professional color palette
    colors = {
        'primary': '#2563eb', 'secondary': '#64748b', 'success': '#059669',
        'warning': '#d97706', 'danger': '#dc2626', 'info': '#0891b2',
        'dark': '#1e293b'
    }
    
    # Generate sample construction project data
    projects_data = [{
        'project_id': f'PROJ_{i:03d}',
        'project_name': f'Construction Project {i}',
        'status': np.random.choice(['Completed', 'In Progress', 'Planning', 'On Hold'], p=[0.4, 0.35, 0.15, 0.1]),
        'completion': np.random.randint(20, 100),
        'budget_allocated': np.random.randint(100000, 2000000),
        'project_type': np.random.choice(['Residential', 'Commercial', 'Infrastructure', 'Industrial']),
        'manager': np.random.choice(['John Smith', 'Maria Garcia', 'David Chen', 'Sarah Johnson']),
    } for i in range(1, 26)]
    df = pd.DataFrame(projects_data)
    df['budget_spent'] = df.apply(lambda row: int(row['budget_allocated'] * (row['completion'] / 100) * np.random.uniform(0.8, 1.2)), axis=1)

    # Create subplots for the dashboard
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Project Status Distribution', 'Budget Performance by Type', 'Project Completion Progress', 'Resource Allocation'),
        specs=[[{"type": "pie"}, {"type": "bar"}], [{"type": "scatter"}, {"type": "heatmap"}]]
    )
    
    # 1. Project Status Pie Chart
    status_counts = df['status'].value_counts()
    fig.add_trace(go.Pie(labels=status_counts.index, values=status_counts.values, marker_colors=[colors['success'], colors['warning'], colors['info'], colors['danger']]), row=1, col=1)
    
    # 2. Budget Performance Bar Chart
    budget_by_type = df.groupby('project_type').agg({'budget_allocated': 'sum', 'budget_spent': 'sum'}).reset_index()
    fig.add_trace(go.Bar(x=budget_by_type['project_type'], y=budget_by_type['budget_allocated'], name='Allocated', marker_color=colors['primary']), row=1, col=2)
    fig.add_trace(go.Bar(x=budget_by_type['project_type'], y=budget_by_type['budget_spent'], name='Spent', marker_color=colors['warning']), row=1, col=2)
    
    # 3. Project Completion Scatter Plot
    fig.add_trace(go.Scatter(x=df['budget_allocated'], y=df['completion'], mode='markers', text=df['project_name']), row=2, col=1)
    
    # 4. Resource Allocation Heatmap
    manager_type_matrix = df.groupby(['manager', 'project_type']).size().unstack(fill_value=0)
    fig.add_trace(go.Heatmap(z=manager_type_matrix.values, x=manager_type_matrix.columns, y=manager_type_matrix.index, colorscale='Blues'), row=2, col=2)
    
    fig.update_layout(title_text='<b>🏗️ Construction Project Management Dashboard</b>', height=800, showlegend=False)
    return fig

def create_index_html():
    """
    Creates the complete HTML structure for the static dashboard page.

    This function generates the main dashboard figure and embeds it into a
    fully structured and styled HTML document, ready for deployment.

    Returns:
        str: The complete HTML content as a string.
    """
    dashboard_fig = generate_static_dashboard()
    dashboard_html = dashboard_fig.to_html(include_plotlyjs='cdn', full_html=False)
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Construction Project Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {{ background-color: #f8f9fa; }}
        .container {{ max-width: 1200px; margin-top: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <div class="card-body">
                {dashboard_html}
            </div>
        </div>
    </div>
</body>
</html>"""
    return html_content

if __name__ == "__main__":
    print("Generating static dashboard HTML...")
    html_content = create_index_html()
    
    # Save the generated HTML to a file
    with open('docs/index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ Static dashboard generated successfully!")
    print("📄 Created: docs/index.html")
    print("🌐 Ready for GitHub Pages deployment.")