#!/usr/bin/env python3
"""
Export Construction Project Monitoring Dashboard to HTML
Generates static HTML version with all visualizations embedded
"""

import os
import sys
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.offline as pyo

# Add parent directory to path to import viz functions
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import functions from viz.py
from scripts.viz import (
    load_data, create_gauge_chart, create_project_work_status_chart,
    create_projects_by_stage_chart, create_budget_variance_chart,
    create_resources_chart, create_workload_chart, COLORS
)

def generate_html_dashboard():
    """Generate complete HTML dashboard with all visualizations"""
    
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
    completion_gauge_fig = create_gauge_chart(100, 100, "Project Completion", COLORS['green'])
    budget_variance_fig = create_budget_variance_chart(data['budget_variance'])
    resources_fig = create_resources_chart(data['resources'])
    workload_fig = create_workload_chart(data['workload'])
    
    # Get project data for header info
    print("🏗️ Building HTML structure...")
    projects_master = data['projects_master']
    project_status = data['project_status']
    selected_project = projects_master[projects_master['project_id'] == 'Project_1'].iloc[0]
    selected_status = project_status[project_status['project_id'] == 'Project_1'].iloc[0]
    
    # Save HTML file
    output_path = 'outputs/dashboard.html'
    os.makedirs('outputs', exist_ok=True)
    
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
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Construction Project Monitoring Dashboard</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #F8F9FA;
            }}
            .header {{
                background-color: white;
                padding: 20px;
                margin-bottom: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .header h1 {{
                color: #2C3E50;
                font-size: 28px;
                font-weight: bold;
                margin: 0;
            }}
            .project-info {{
                background-color: white;
                padding: 20px;
                margin-bottom: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                display: flex;
                align-items: center;
                flex-wrap: wrap;
                gap: 20px;
            }}
            .project-details {{
                flex: 1;
                min-width: 300px;
            }}
            .kpi-cards {{
                display: flex;
                gap: 15px;
                flex-wrap: wrap;
            }}
            .kpi-card {{
                background-color: #ECF0F1;
                padding: 15px;
                border-radius: 8px;
                text-align: center;
                min-width: 120px;
            }}
            .kpi-value {{
                color: #FF6B35;
                font-size: 24px;
                font-weight: bold;
                margin: 0;
            }}
            .kpi-label {{
                font-size: 12px;
                margin: 5px 0 0 0;
                color: #666;
            }}
            .charts-grid {{
                display: grid;
                grid-gap: 15px;
                margin-bottom: 20px;
            }}
            .chart-row-3 {{
                display: grid;
                grid-template-columns: 1fr 1fr 1fr;
                grid-gap: 15px;
            }}
            .chart-row-2 {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                grid-gap: 15px;
            }}
            .chart-row-1 {{
                display: grid;
                grid-template-columns: 1fr;
                grid-gap: 15px;
            }}
            .chart-container {{
                background-color: white;
                padding: 15px;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .footer {{
                background-color: white;
                padding: 15px;
                margin-top: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                text-align: center;
                color: #666;
                font-size: 12px;
            }}
            @media (max-width: 768px) {{
                .chart-row-3, .chart-row-2 {{
                    grid-template-columns: 1fr;
                }}
                .project-info {{
                    flex-direction: column;
                }}
                .kpi-cards {{
                    justify-content: center;
                }}
            }}
        </style>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    </head>
    <body>
        <!-- Header -->
        <div class="header">
            <h1>Construction Project Monitoring Dashboard</h1>
        </div>
        
        <!-- Project Info -->
        <div class="project-info">
            <div class="project-details">
                <h3 style="color: #2C3E50; margin-top: 0;">Project Information</h3>
                <p><strong>Project:</strong> {selected_project['project_id']}</p>
                <p><strong>Type:</strong> {selected_project['type']}</p>
                <p><strong>Manager:</strong> {selected_project['manager']}</p>
                <p><strong>Start Date:</strong> {selected_project['start_date']}</p>
                <p><strong>Duration:</strong> {selected_project['duration_days']} days</p>
            </div>
            
            <div class="kpi-cards">
                <div class="kpi-card">
                    <div class="kpi-value">{selected_status['completion_percent']}%</div>
                    <div class="kpi-label">Completion Rate</div>
                </div>
                
                <div class="kpi-card">
                    <div class="kpi-value">${selected_project['budget']:,}</div>
                    <div class="kpi-label">Total Budget</div>
                </div>
                
                <div class="kpi-card">
                    <div class="kpi-value">{selected_project['duration_days']}</div>
                    <div class="kpi-label">Days Duration</div>
                </div>
            </div>
        </div>
        
        <!-- Charts Grid -->
        <div class="charts-grid">
            <!-- Row 1: Three charts -->
            <div class="chart-row-3">
                <div class="chart-container">
                    {work_status_html}
                </div>
                <div class="chart-container">
                    {projects_stage_html}
                </div>
                <div class="chart-container">
                    {completion_gauge_html}
                </div>
            </div>
            
            <!-- Row 2: Two charts -->
            <div class="chart-row-2">
                <div class="chart-container">
                    {budget_variance_html}
                </div>
                <div class="chart-container">
                    {resources_html}
                </div>
            </div>
            
            <!-- Row 3: One chart -->
            <div class="chart-row-1">
                <div class="chart-container">
                    {workload_html}
                </div>
            </div>
        </div>
        
        <!-- Footer -->
        <div class="footer">
            <p><strong>Construction Project Monitoring Dashboard</strong> | Generated on {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>Interactive dashboard with 6 visualizations • Corporate orange theme • Responsive design</p>
            <p>Featuring: Project status tracking, budget variance analysis, resource management, and workload monitoring</p>
        </div>
    </body>
    </html>
    """
    
    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print(f"✅ Dashboard exported successfully!")
    print(f"📁 File location: {os.path.abspath(output_path)}")
    print(f"📊 Features: 6 interactive visualizations, responsive design, corporate styling")
    print(f"🎨 Theme: Orange corporate color scheme with professional layout")
    
    return True

if __name__ == '__main__':
    generate_html_dashboard()
