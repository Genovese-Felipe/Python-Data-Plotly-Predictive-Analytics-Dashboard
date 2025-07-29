"""
Construction Project Dashboard - Data Generation Script
====================================================

This script generates realistic synthetic data for a construction project monitoring dashboard.
Uses only pandas and numpy as required.

Business Context:
- Construction company with 30+ active projects  
- Project types: Engineering & Non-Residential, Commercial Building, Infrastructure
- Budget range: $100K - $1M+ per project
- Key metrics: Completion %, Budget utilization, Resource allocation, Timeline performance
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Set random seed for reproducible results
np.random.seed(42)

# Configuration
NUM_PROJECTS = 30
DATA_DIR = '../data'

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

def generate_projects_master():
    """Generate master project information"""
    
    project_ids = [f'Project_{i}' for i in range(1, NUM_PROJECTS + 1)]
    
    # Project types based on construction industry
    project_types = ['Engineering & Non-Residential', 'Commercial Building', 'Infrastructure']
    
    # Project managers
    managers = ['Project Manager_A', 'Project Manager_B', 'Project Manager_C', 
                'Project Manager_D', 'Project Manager_E']
    
    # Generate start dates over past 2 years
    start_dates = pd.date_range(
        start='2022-01-01', 
        end='2024-01-01', 
        periods=NUM_PROJECTS
    )
    
    projects_master = pd.DataFrame({
        'project_id': project_ids,
        'name': [f'Construction Project {i}' for i in range(1, NUM_PROJECTS + 1)],
        'type': np.random.choice(project_types, NUM_PROJECTS, p=[0.4, 0.35, 0.25]),
        'manager': np.random.choice(managers, NUM_PROJECTS),
        'start_date': start_dates,
        'budget': np.random.uniform(100000, 1000000, NUM_PROJECTS).round(0).astype(int),
        'duration_days': np.random.randint(180, 1500, NUM_PROJECTS)  # 6 months to 4+ years
    })
    
    return projects_master

def generate_project_status(projects_master):
    """Generate current project status and progress"""
    
    project_ids = projects_master['project_id'].tolist()
    
    # Status distribution: 40% completed, 50% in progress, 10% not started
    statuses = np.random.choice(
        ['Completed', 'In Progress', 'Not Started'], 
        NUM_PROJECTS, 
        p=[0.4, 0.5, 0.1]
    )
    
    # Completion percentages based on status
    completion_percent = []
    budget_used = []
    days_used = []
    
    for i, status in enumerate(statuses):
        budget = projects_master.iloc[i]['budget']
        duration = projects_master.iloc[i]['duration_days']
        
        if status == 'Completed':
            completion = 100
            budget_variance = np.random.uniform(0.8, 1.2)  # ±20% variance
            days_variance = np.random.uniform(0.9, 1.1)    # ±10% variance
        elif status == 'In Progress':
            completion = np.random.randint(20, 95)
            budget_variance = np.random.uniform(0.7, 1.3)  # Wider variance for ongoing
            days_variance = np.random.uniform(0.8, 1.2)
        else:  # Not Started
            completion = 0
            budget_variance = np.random.uniform(0.0, 0.1)  # Minimal spending
            days_variance = np.random.uniform(0.0, 0.1)
        
        completion_percent.append(completion)
        budget_used.append(int(budget * budget_variance))
        days_used.append(int(duration * days_variance))
    
    project_status = pd.DataFrame({
        'project_id': project_ids,
        'status': statuses,
        'completion_percent': completion_percent,
        'budget_used': budget_used,
        'days_used': days_used
    })
    
    return project_status

def generate_project_stages():
    """Generate project stage information for sunburst chart"""
    
    # Construction project stages
    stages = ['Plan', 'Design', 'Pre-construct', 'Construct', 'Close-out']
    
    project_stages = []
    
    for project_num in range(1, NUM_PROJECTS + 1):
        project_id = f'Project_{project_num}'
        
        # Each project can be in multiple stages or completed stages
        num_stages = np.random.randint(1, 4)  # 1-3 active/completed stages
        project_stage_list = np.random.choice(stages, num_stages, replace=False)
        
        for stage_num, stage in enumerate(project_stage_list, 1):
            project_stages.append({
                'project_id': project_id,
                'stage': stage,
                'stage_number': stage_num
            })
    
    return pd.DataFrame(project_stages)

def generate_budget_variance():
    """Generate budget tracking data for trend analysis"""
    
    budget_data = []
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    for project_num in range(1, NUM_PROJECTS + 1):
        project_id = f'Project_{project_num}'
        
        # Generate monthly budget tracking for active projects
        num_months = np.random.randint(3, 12)  # 3-12 months of data
        selected_months = np.random.choice(months, num_months, replace=False)
        
        base_budget = np.random.uniform(50000, 200000)  # Monthly budget
        
        for month in selected_months:
            variance = np.random.uniform(-0.3, 0.4)  # -30% to +40% variance
            
            budget_data.append({
                'project_id': project_id,
                'month': month,
                'planned_budget': base_budget,
                'actual_budget': base_budget * (1 + variance),
                'variance': base_budget * variance
            })
    
    return pd.DataFrame(budget_data)

def generate_resources():
    """Generate resource allocation data"""
    
    resource_types = ['Engineers', 'Architects', 'Project Managers', 'Contractors', 'Supervisors']
    
    resources_data = []
    
    for project_num in range(1, NUM_PROJECTS + 1):
        project_id = f'Project_{project_num}'
        
        # Each project uses 2-4 resource types
        num_resource_types = np.random.randint(2, 5)
        used_resources = np.random.choice(resource_types, num_resource_types, replace=False)
        
        for resource_type in used_resources:
            planned = np.random.randint(2, 20)  # 2-20 people planned
            variance = np.random.uniform(0.7, 1.3)  # ±30% variance
            actual = max(1, int(planned * variance))  # At least 1 person
            
            resources_data.append({
                'project_id': project_id,
                'resource_type': resource_type,
                'planned_resources': planned,
                'actual_resources': actual
            })
    
    return pd.DataFrame(resources_data)

def generate_workload():
    """Generate workload and timeline data"""
    
    workload_data = []
    
    for project_num in range(1, NUM_PROJECTS + 1):
        project_id = f'Project_{project_num}'
        
        # Generate workload breakdown
        total_hours = np.random.randint(1000, 10000)  # Total project hours
        completion_rate = np.random.uniform(0.2, 0.9)  # 20-90% complete
        
        completed_hours = int(total_hours * completion_rate)
        remaining_hours = total_hours - completed_hours
        
        # Some projects might have overdue work
        overdue_hours = np.random.randint(0, int(remaining_hours * 0.3)) if remaining_hours > 0 else 0
        remaining_hours = max(0, remaining_hours - overdue_hours)
        
        workload_data.append({
            'project_id': project_id,
            'completed_hours': completed_hours,
            'remaining_hours': remaining_hours,
            'overdue_hours': overdue_hours,
            'total_hours': total_hours
        })
    
    return pd.DataFrame(workload_data)

def main():
    """Main function to generate all datasets"""
    
    print("🏗️ Generating Construction Project Dashboard Data...")
    print(f"📊 Creating data for {NUM_PROJECTS} projects...")
    
    # Generate all datasets
    projects_master = generate_projects_master()
    project_status = generate_project_status(projects_master)
    project_stages = generate_project_stages()
    budget_variance = generate_budget_variance()
    resources = generate_resources()
    workload = generate_workload()
    
    # Save to CSV files
    datasets = {
        'projects_master.csv': projects_master,
        'project_status.csv': project_status,
        'project_stages.csv': project_stages,
        'budget_variance.csv': budget_variance,
        'resources.csv': resources,
        'workload.csv': workload
    }
    
    for filename, df in datasets.items():
        filepath = os.path.join(DATA_DIR, filename)
        df.to_csv(filepath, index=False)
        print(f"✅ Saved {filename}: {len(df)} records")
    
    print(f"\n🎯 Data generation complete!")
    print(f"📁 Files saved to: {DATA_DIR}/")
    print(f"📈 Ready for dashboard visualization!")
    
    # Display sample data
    print(f"\n📋 Sample Projects Master Data:")
    print(projects_master.head())
    
    print(f"\n📋 Sample Project Status Data:")  
    print(project_status.head())

if __name__ == "__main__":
    main()
