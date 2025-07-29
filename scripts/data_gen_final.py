"""
Construction Project Monitoring Dashboard - Data Generation Script
================================================================

Generates realistic synthetic data for construction project monitoring dashboard.
Uses ONLY pandas and numpy as required by project specifications.

Business Context (from your detailed description):
- Construction company with 30+ active projects
- Project Types: Engineering & Non-Residential, Commercial Building, Infrastructure  
- Project Managers working on multiple projects
- Budget range: $100K - $1M+ per project
- Key metrics: Work Progress Breakdown, Project Stages, Budget Variance, Resource Utilization, Workload

Data Story Framework:
1. Projects Master - Basic project information and metadata
2. Project Status - Current completion status and progress metrics
3. Project Stages - Stage distribution (Plan, Design, Pre-construction, Construction, Closeout)
4. Budget Variance - Actual vs Planned budget tracking
5. Resources - Actual vs Planned resource allocation
6. Workload - Completed/Remaining/Overdue task breakdown
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
    """
    Generate master project information
    Following the detailed dashboard specification with 30 projects
    """
    
    project_ids = [f'Project_{i}' for i in range(1, NUM_PROJECTS + 1)]
    
    # Project types exactly as specified in your description
    project_types = [
        'Engineering & Non-Residential',
        'Commercial Building', 
        'Infrastructure'
    ]
    
    # Project managers (Project Heads) - some work on multiple projects
    project_managers = [
        'John Smith',
        'Maria Garcia', 
        'David Wilson',
        'Sarah Johnson',
        'Michael Brown'
    ]
    
    # Generate realistic start dates spanning 2+ years
    start_dates = pd.date_range(
        start='2022-01-01', 
        end='2024-01-01', 
        periods=NUM_PROJECTS
    )
    
    # Generate end dates based on realistic construction durations
    duration_days = np.random.randint(180, 1500, NUM_PROJECTS)  # 6 months to 4+ years
    end_dates = [start + timedelta(days=int(duration)) for start, duration in zip(start_dates, duration_days)]
    
    projects_master = pd.DataFrame({
        'project_id': project_ids,
        'project_name': [f'Construction Project {i}' for i in range(1, NUM_PROJECTS + 1)],
        'project_type': np.random.choice(project_types, NUM_PROJECTS, p=[0.4, 0.35, 0.25]),
        'project_head': np.random.choice(project_managers, NUM_PROJECTS),
        'start_date': start_dates,
        'end_date': end_dates,
        'total_budget': np.random.uniform(100000, 1000000, NUM_PROJECTS).round(0).astype(int),
        'duration_days': duration_days
    })
    
    return projects_master

def generate_project_status(projects_master):
    """
    Generate project status data for Work Progress Breakdown
    Following your specification:
    - 🟢 Completed: 50% 
    - 🔵 Not Started: 40%
    - 🟡 In Progress: 10%
    """
    
    project_ids = projects_master['project_id'].tolist()
    
    # Status distribution as per your description
    statuses = np.random.choice(
        ['Completed', 'Not Started', 'In Progress'], 
        NUM_PROJECTS, 
        p=[0.5, 0.4, 0.1]  # Exactly as specified in your description
    )
    
    # Generate completion percentages, budget used, and days used based on status
    completion_percent = []
    amount_spent = []
    days_used = []
    
    for i, status in enumerate(statuses):
        total_budget = projects_master.iloc[i]['total_budget']
        duration = projects_master.iloc[i]['duration_days']
        
        if status == 'Completed':
            completion = 100
            # Completed projects have spent between 80-120% of budget (variance)
            budget_variance = np.random.uniform(0.8, 1.2)
            days_variance = np.random.uniform(0.9, 1.1)
        elif status == 'In Progress':
            completion = np.random.randint(20, 95)
            # In progress projects vary more widely
            budget_variance = np.random.uniform(0.6, 1.4)
            days_variance = np.random.uniform(0.7, 1.3)
        else:  # Not Started
            completion = 0
            # Not started projects have minimal spending
            budget_variance = np.random.uniform(0.0, 0.05)
            days_variance = np.random.uniform(0.0, 0.05)
        
        completion_percent.append(completion)
        amount_spent.append(int(total_budget * budget_variance))
        days_used.append(int(duration * days_variance))
    
    project_status = pd.DataFrame({
        'project_id': project_ids,
        'status': statuses,
        'completion_percent': completion_percent,
        'amount_spent': amount_spent,
        'days_used': days_used
    })
    
    return project_status

def generate_project_stages():
    """
    Generate project stages data for "Projects by Stage" pie chart
    Following your specification:
    - Plan: 12 projects
    - Design: 8 projects  
    - Pre-construction: 4 projects
    - Construction: 3 projects
    - Closeout: 2 projects
    """
    
    # Exact distribution from your description
    stages_distribution = {
        'Plan': 13,  # Adjusted to total 30
        'Design': 8, 
        'Pre-construction': 4,
        'Construction': 3,
        'Closeout': 2
    }
    
    project_stages = []
    project_counter = 1
    
    for stage, count in stages_distribution.items():
        for _ in range(count):
            project_stages.append({
                'project_id': f'Project_{project_counter}',
                'stage': stage,
                'stage_number': list(stages_distribution.keys()).index(stage) + 1
            })
            project_counter += 1
    
    return pd.DataFrame(project_stages)

def generate_budget_variance():
    """
    Generate budget variance data for "Budget Variance Cross-Project Financial Monitoring"
    Shows Actual vs Planned Budgets across filtered projects
    """
    
    budget_data = []
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    for project_num in range(1, NUM_PROJECTS + 1):
        project_id = f'Project_{project_num}'
        
        # Generate monthly budget tracking data
        num_months = np.random.randint(6, 12)  # 6-12 months of data
        selected_months = np.random.choice(months, num_months, replace=False)
        
        # Base monthly budget
        base_planned = np.random.randint(20000, 80000)  # Monthly planned budget
        
        for month in selected_months:
            # Add some monthly variation to planned budget
            planned = base_planned + np.random.randint(-5000, 15000)
            
            # Actual budget with variance (key for your dashboard)
            variance_factor = np.random.uniform(0.7, 1.4)  # 70%-140% of planned
            actual = int(planned * variance_factor)
            
            budget_data.append({
                'project_id': project_id,
                'month': month,
                'planned_budget': planned,
                'actual_budget': actual,
                'variance': actual - planned
            })
    
    return pd.DataFrame(budget_data)

def generate_resources():
    """
    Generate resource allocation data for "Actual vs Planned Resources Utilization"
    Shows personnel allocation vs initial estimates
    """
    
    resource_types = ['Engineers', 'Architects', 'Project Managers', 'Contractors', 'Supervisors']
    resources_data = []
    
    for project_num in range(1, NUM_PROJECTS + 1):
        project_id = f'Project_{project_num}'
        
        # Each project uses 3-5 resource types
        num_resource_types = np.random.randint(3, 6)
        used_resources = np.random.choice(resource_types, num_resource_types, replace=False)
        
        for resource_type in used_resources:
            # Generate planned vs actual resources
            planned = np.random.randint(5, 30)  # 5-30 people planned
            actual = int(planned * np.random.uniform(0.8, 1.3))  # 80%-130% variance
            
            resources_data.append({
                'project_id': project_id,
                'resource_type': resource_type,
                'planned_resources': planned,
                'actual_resources': actual
            })
    
    return pd.DataFrame(resources_data)

def generate_workload():
    """
    Generate workload data for "Workload by Project/Filter"
    Shows task completion breakdown:
    - ✅ Completed Tasks: ~201 resources
    - 🟠 Remaining Workload: ~100  
    - 🔴 Overdue: ~50
    """
    
    workload_data = []
    
    for project_num in range(1, NUM_PROJECTS + 1):
        project_id = f'Project_{project_num}'
        
        # Generate realistic workload distribution
        total_hours = np.random.randint(1000, 5000)
        
        # Percentages based on your description
        completed_pct = np.random.uniform(0.3, 0.8)  # 30-80% completed
        overdue_pct = np.random.uniform(0.05, 0.2)   # 5-20% overdue
        remaining_pct = 1 - completed_pct - overdue_pct
        
        completed_hours = int(total_hours * completed_pct)
        overdue_hours = int(total_hours * overdue_pct)
        remaining_hours = total_hours - completed_hours - overdue_hours
        
        workload_data.append({
            'project_id': project_id,
            'completed_hours': completed_hours,
            'remaining_hours': remaining_hours,
            'overdue_hours': overdue_hours,
            'total_hours': total_hours
        })
    
    return pd.DataFrame(workload_data)

def main():
    """
    Main function to generate all datasets following your detailed specification
    """
    
    print("🏗️ Construction Project Monitoring Dashboard - Data Generation")
    print("=" * 65)
    print(f"📊 Generating data for {NUM_PROJECTS} construction projects...")
    print()
    
    # Generate all datasets following exact specifications
    print("1️⃣ Generating Projects Master Data...")
    projects_master = generate_projects_master()
    
    print("2️⃣ Generating Project Status (Work Progress Breakdown)...")
    project_status = generate_project_status(projects_master)
    
    print("3️⃣ Generating Project Stages (Plan/Design/Pre-construction/etc)...")
    project_stages = generate_project_stages()
    
    print("4️⃣ Generating Budget Variance (Actual vs Planned)...")
    budget_variance = generate_budget_variance()
    
    print("5️⃣ Generating Resource Allocation (Actual vs Planned)...")
    resources = generate_resources()
    
    print("6️⃣ Generating Workload Distribution (Completed/Remaining/Overdue)...")
    workload = generate_workload()
    
    # Save to CSV files as required by project specifications
    datasets = {
        'projects_master.csv': projects_master,
        'project_status.csv': project_status,
        'project_stages.csv': project_stages,
        'budget_variance.csv': budget_variance,
        'resources.csv': resources,
        'workload.csv': workload
    }
    
    print()
    print("💾 Saving datasets to CSV files...")
    for filename, df in datasets.items():
        filepath = os.path.join(DATA_DIR, filename)
        df.to_csv(filepath, index=False)
        print(f"   ✅ {filename}: {len(df)} records")
    
    print()
    print("🎯 Data generation completed successfully!")
    print(f"📁 All files saved to: {DATA_DIR}/")
    print("📈 Ready for dashboard visualization in viz.py")
    print()
    
    # Display sample data for verification
    print("📋 Sample Projects Master Data:")
    print(projects_master.head())
    print()
    
    print("📋 Sample Project Status Distribution:")
    status_counts = project_status['status'].value_counts()
    for status, count in status_counts.items():
        percentage = (count / len(project_status)) * 100
        print(f"   {status}: {count} projects ({percentage:.1f}%)")
    print()
    
    print("📋 Sample Project Stages Distribution:")
    stage_counts = project_stages['stage'].value_counts()
    for stage, count in stage_counts.items():
        print(f"   {stage}: {count} projects")

if __name__ == "__main__":
    main()
