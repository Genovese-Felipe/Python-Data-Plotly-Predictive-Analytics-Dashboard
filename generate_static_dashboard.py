#!/usr/bin/env python3
"""
Static Dashboard Generator for GitHub Pages
Creates a static HTML version of the construction dashboard that can be served via GitHub Pages
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_static_dashboard():
    """Generate a static HTML dashboard for GitHub Pages"""
    
    # Set random seed for reproducible results
    np.random.seed(42)
    
    # Professional color palette
    colors = {
        'primary': '#2563eb',
        'secondary': '#64748b', 
        'success': '#059669',
        'warning': '#d97706',
        'danger': '#dc2626',
        'info': '#0891b2',
        'light': '#f1f5f9',
        'dark': '#1e293b',
    }
    
    # Generate sample construction project data
    projects_data = []
    for i in range(1, 26):
        projects_data.append({
            'project_id': f'PROJ_{i:03d}',
            'project_name': f'Construction Project {i}',
            'status': np.random.choice(['Completed', 'In Progress', 'Planning', 'On Hold'], 
                                    p=[0.4, 0.35, 0.15, 0.1]),
            'completion': np.random.randint(20, 100),
            'budget_allocated': np.random.randint(100000, 2000000),
            'budget_spent': 0,
            'project_type': np.random.choice(['Residential', 'Commercial', 'Infrastructure', 'Industrial']),
            'manager': np.random.choice(['John Smith', 'Maria Garcia', 'David Chen', 'Sarah Johnson', 'Mike Wilson']),
            'start_date': datetime.now() - timedelta(days=np.random.randint(30, 365)),
            'estimated_end': datetime.now() + timedelta(days=np.random.randint(30, 180)),
            'team_size': np.random.randint(5, 25),
            'location': np.random.choice(['Downtown', 'Suburbs', 'Industrial Zone', 'Waterfront', 'City Center'])
        })
    
    # Calculate budget spent based on completion
    for project in projects_data:
        project['budget_spent'] = int(project['budget_allocated'] * (project['completion'] / 100) * np.random.uniform(0.8, 1.2))
    
    df = pd.DataFrame(projects_data)
    
    # Create subplots for the dashboard
    fig = make_subplots(
        rows=3, cols=2,
        subplot_titles=(
            'Project Status Distribution',
            'Budget Performance by Type', 
            'Project Completion Progress',
            'Resource Allocation Analysis',
            'Project Timeline Overview',
            'Budget Variance Analysis'
        ),
        specs=[
            [{"type": "pie"}, {"type": "bar"}],
            [{"type": "scatter"}, {"type": "heatmap"}],
            [{"type": "bar"}, {"type": "scatter"}]
        ],
        vertical_spacing=0.12,
        horizontal_spacing=0.1
    )
    
    # 1. Project Status Distribution (Pie Chart)
    status_counts = df['status'].value_counts()
    fig.add_trace(
        go.Pie(
            labels=status_counts.index,
            values=status_counts.values,
            marker_colors=[colors['success'], colors['warning'], colors['info'], colors['danger']],
            textinfo='label+percent',
            textfont_size=12,
            showlegend=True
        ),
        row=1, col=1
    )
    
    # 2. Budget Performance by Type (Bar Chart)
    budget_by_type = df.groupby('project_type').agg({
        'budget_allocated': 'sum',
        'budget_spent': 'sum'
    }).reset_index()
    
    fig.add_trace(
        go.Bar(
            x=budget_by_type['project_type'],
            y=budget_by_type['budget_allocated'],
            name='Allocated',
            marker_color=colors['primary'],
            opacity=0.8
        ),
        row=1, col=2
    )
    
    fig.add_trace(
        go.Bar(
            x=budget_by_type['project_type'],
            y=budget_by_type['budget_spent'],
            name='Spent',
            marker_color=colors['warning'],
            opacity=0.8
        ),
        row=1, col=2
    )
    
    # 3. Project Completion Progress (Scatter Plot)
    fig.add_trace(
        go.Scatter(
            x=df['budget_allocated'],
            y=df['completion'],
            mode='markers',
            marker=dict(
                size=df['team_size'],
                color=df['completion'],
                colorscale='Viridis',
                colorbar=dict(title="Completion %"),
                opacity=0.7,
                line=dict(width=1, color='white')
            ),
            text=df['project_name'],
            name='Projects',
            showlegend=False
        ),
        row=2, col=1
    )
    
    # 4. Resource Allocation Analysis (Heatmap)
    # Create a matrix of managers vs project types
    manager_type_matrix = df.groupby(['manager', 'project_type']).size().unstack(fill_value=0)
    
    fig.add_trace(
        go.Heatmap(
            z=manager_type_matrix.values,
            x=manager_type_matrix.columns,
            y=manager_type_matrix.index,
            colorscale='Blues',
            showscale=False,
            text=manager_type_matrix.values,
            texttemplate="%{text}",
            textfont={"size": 10}
        ),
        row=2, col=2
    )
    
    # 5. Project Timeline Overview (Bar Chart)
    timeline_data = df.groupby('status')['team_size'].sum().reset_index()
    fig.add_trace(
        go.Bar(
            x=timeline_data['status'],
            y=timeline_data['team_size'],
            marker_color=[colors['success'], colors['warning'], colors['info'], colors['danger']],
            name='Team Size',
            showlegend=False,
            text=timeline_data['team_size'],
            textposition='auto'
        ),
        row=3, col=1
    )
    
    # 6. Budget Variance Analysis (Scatter Plot)
    df['budget_variance'] = ((df['budget_spent'] - df['budget_allocated']) / df['budget_allocated']) * 100
    
    fig.add_trace(
        go.Scatter(
            x=df['completion'],
            y=df['budget_variance'],
            mode='markers',
            marker=dict(
                size=10,
                color=df['budget_variance'],
                colorscale='RdYlBu_r',
                opacity=0.7,
                line=dict(width=1, color='white')
            ),
            text=df['project_name'],
            name='Budget Variance',
            showlegend=False
        ),
        row=3, col=2
    )
    
    # Update layout
    fig.update_layout(
        title={
            'text': '<b>🏗️ Construction Project Management Dashboard - Professional Analytics</b>',
            'x': 0.5,
            'font': {'size': 24}
        },
        height=1200,
        font={'family': 'Arial, sans-serif'},
        paper_bgcolor='white',
        plot_bgcolor='white',
        showlegend=True
    )
    
    # Update x and y axis titles
    fig.update_xaxes(title_text="Project Type", row=1, col=2)
    fig.update_yaxes(title_text="Budget ($)", row=1, col=2)
    
    fig.update_xaxes(title_text="Budget Allocated ($)", row=2, col=1)
    fig.update_yaxes(title_text="Completion (%)", row=2, col=1)
    
    fig.update_xaxes(title_text="Project Type", row=2, col=2)
    fig.update_yaxes(title_text="Manager", row=2, col=2)
    
    fig.update_xaxes(title_text="Project Status", row=3, col=1)
    fig.update_yaxes(title_text="Total Team Size", row=3, col=1)
    
    fig.update_xaxes(title_text="Completion (%)", row=3, col=2)
    fig.update_yaxes(title_text="Budget Variance (%)", row=3, col=2)
    
    return fig

def create_index_html():
    """Create the main index.html file for GitHub Pages"""
    
    # Generate the dashboard
    dashboard_fig = generate_static_dashboard()
    
    # Convert to HTML
    dashboard_html = dashboard_fig.to_html(
        include_plotlyjs='cdn',
        config={'displayModeBar': True, 'responsive': True}
    )
    
    # Create a more comprehensive HTML structure
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Construction Project Management Dashboard - Professional Analytics with Python, Plotly, and Predictive Analytics">
    <meta name="author" content="Felipe Genovese">
    <title>Construction Project Management Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            margin: 0;
            padding: 20px 0;
        }}
        .header {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            text-align: center;
        }}
        .dashboard-container {{
            background: rgba(255, 255, 255, 0.98);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            margin-bottom: 30px;
        }}
        .footer {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            text-align: center;
            margin-top: 30px;
        }}
        .badge-custom {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 8px 16px;
            border-radius: 25px;
            margin: 5px;
            display: inline-block;
        }}
        h1 {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 700;
            margin-bottom: 20px;
        }}
        .feature-list {{
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="container-fluid">
        <div class="header">
            <h1 class="display-4">🏗️ Construction Project Management Dashboard</h1>
            <p class="lead">Professional Analytics with Python, Plotly & Predictive Analytics</p>
            <div class="feature-list">
                <span class="badge-custom">📊 Interactive Visualizations</span>
                <span class="badge-custom">🎨 Professional Design</span>
                <span class="badge-custom">📱 Responsive Layout</span>
                <span class="badge-custom">⚡ Real-time Analytics</span>
                <span class="badge-custom">🔍 Predictive Insights</span>
            </div>
        </div>
        
        <div class="dashboard-container">
            {dashboard_html.split('<body>')[1].split('</body>')[0]}
        </div>
        
        <div class="footer">
            <h5>🚀 Technology Stack</h5>
            <p><strong>Python</strong> • <strong>Plotly</strong> • <strong>Pandas</strong> • <strong>NumPy</strong> • <strong>Bootstrap</strong></p>
            <p class="text-muted">Built with professional data visualization best practices and responsive design</p>
            <p class="text-muted">
                <a href="https://github.com/Genovese-Felipe/Python-Data-Plotly-Predictive-Analytics-Dashboard" target="_blank" class="text-decoration-none">
                    📂 View Source Code on GitHub
                </a>
            </p>
        </div>
    </div>
</body>
</html>"""
    
    return html_content

if __name__ == "__main__":
    # Generate the static dashboard HTML
    html_content = create_index_html()
    
    # Save as index.html
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ Static dashboard generated successfully!")
    print("📄 Created: index.html")
    print("🌐 Ready for GitHub Pages deployment!")