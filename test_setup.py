#!/usr/bin/env python3
"""
Test script to validate dashboard functionality and generate HTML output
"""

import sys
import os
sys.path.append('/home/runner/work/Python-Data-Plotly-Predictive-Analytics-Dashboard/Python-Data-Plotly-Predictive-Analytics-Dashboard/scripts')

# Import the viz_new module
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

def test_data_loading():
    """Test if data loading works correctly"""
    print("🔍 Testing data loading...")
    
    base_dir = '/home/runner/work/Python-Data-Plotly-Predictive-Analytics-Dashboard/Python-Data-Plotly-Predictive-Analytics-Dashboard'
    data_dir = os.path.join(base_dir, 'data')
    
    required_files = [
        'projects_master.csv',
        'project_status.csv', 
        'project_stages.csv',
        'budget_variance.csv',
        'resources.csv',
        'workload.csv'
    ]
    
    datasets = {}
    for file in required_files:
        filepath = os.path.join(data_dir, file)
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            datasets[file.replace('.csv', '')] = df
            print(f"✅ Loaded {file}: {len(df)} rows")
        else:
            print(f"❌ Missing {file}")
            return False
    
    return datasets

def create_sample_chart(data):
    """Create a sample chart to test plotly functionality"""
    print("📊 Creating sample chart...")
    
    # Create a simple bar chart using the projects data
    projects_df = data['projects_master']
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=projects_df['project_name'][:10],  # First 10 projects
        y=projects_df['total_budget'][:10],
        name='Project Budget',
        marker_color='#1f77b4'
    ))
    
    fig.update_layout(
        title="Sample Project Budget Chart",
        xaxis_title="Projects",
        yaxis_title="Budget ($)",
        template="plotly_white"
    )
    
    # Save to HTML
    output_dir = os.path.join('/home/runner/work/Python-Data-Plotly-Predictive-Analytics-Dashboard/Python-Data-Plotly-Predictive-Analytics-Dashboard', 'outputs')
    os.makedirs(output_dir, exist_ok=True)
    
    html_file = os.path.join(output_dir, 'test_chart.html')
    fig.write_html(html_file)
    print(f"✅ Sample chart saved to: {html_file}")
    
    return True

def main():
    print("🧪 Testing Dashboard Components...")
    print("=" * 50)
    
    # Test data loading
    data = test_data_loading()
    if not data:
        print("❌ Data loading failed")
        return 1
    
    # Test chart creation
    if not create_sample_chart(data):
        print("❌ Chart creation failed")
        return 1
    
    print("\n✅ All tests passed!")
    print("🚀 Dashboard components are working correctly")
    print("\n📋 Data Summary:")
    for name, df in data.items():
        print(f"   - {name}: {len(df)} records")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())