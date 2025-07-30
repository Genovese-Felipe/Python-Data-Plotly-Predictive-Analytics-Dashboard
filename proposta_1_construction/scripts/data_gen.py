# scripts/data_gen.py - Construction Project Management Dashboard Data Generation
import pandas as pd
import numpy as np
import datetime as dt
import random
import os

# Ensure reproducibility
np.random.seed(42)
random.seed(42)

def generate_construction_projects(n_projects=30):
    """
    Generate construction project data for executive dashboard
    
    Parameters:
    -----------
    n_projects : int
        Number of construction projects to generate
        
    Returns:
    --------
    tuple
        DataFrames for projects master, status, stages, budget variance, resources, workload
    """
    
    # Ensure data directory exists
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Project types and their characteristics
    project_types = ['Residential Complex', 'Commercial Building', 'Industrial Facility', 'Infrastructure']
    construction_stages = ['Planning', 'Design', 'Pre-construction', 'Construction', 'Final']
    
    # Generate master project data
    projects_master = {
        'project_id': [f'PROJ-{i:03d}' for i in range(1, n_projects + 1)],
        'name': [f'Construction Project {i:03d}' for i in range(1, n_projects + 1)],
        'type': np.random.choice(project_types, n_projects),
        'manager': [f'Manager {chr(65 + i % 10)}' for i in range(n_projects)],
        'start_date': [dt.datetime(2023, 1, 1) + dt.timedelta(days=random.randint(0, 365)) 
                      for _ in range(n_projects)],
        'budget': np.random.randint(500000, 5000000, n_projects),
        'duration_days': np.random.randint(90, 730, n_projects)
    }
    
    df_projects_master = pd.DataFrame(projects_master)
    
    # Calculate planned end dates
    df_projects_master['planned_end_date'] = df_projects_master.apply(
        lambda row: row['start_date'] + dt.timedelta(days=row['duration_days']), axis=1
    )
    
    # Generate project status data
    status_data = []
    for _, project in df_projects_master.iterrows():
        # Determine current status based on dates
        today = dt.datetime.now()
        if project['start_date'] > today:
            status = 'Not Started'
            completion = 0
        elif project['planned_end_date'] < today:
            status = np.random.choice(['Completed', 'Delayed'], p=[0.7, 0.3])
            completion = 100 if status == 'Completed' else np.random.randint(85, 99)
        else:
            status = 'In Progress'
            # Calculate expected completion based on time elapsed
            days_elapsed = (today - project['start_date']).days
            expected_progress = min(95, (days_elapsed / project['duration_days']) * 100)
            completion = max(5, expected_progress + np.random.randint(-10, 15))
        
        # Calculate budget utilization
        if status == 'Not Started':
            budget_used = 0
        else:
            budget_used = project['budget'] * (completion / 100) * np.random.uniform(0.8, 1.2)
        
        # Calculate days used
        days_used = max(0, (today - project['start_date']).days) if status != 'Not Started' else 0
        
        status_data.append({
            'project_id': project['project_id'],
            'status': status,
            'completion_percent': completion,
            'budget_used': budget_used,
            'days_used': days_used
        })
    
    df_project_status = pd.DataFrame(status_data)
    
    # Generate project stages data
    stages_data = []
    for _, project in df_projects_master.iterrows():
        project_completion = df_project_status[
            df_project_status['project_id'] == project['project_id']
        ]['completion_percent'].iloc[0]
        
        # Determine which stage each project is in
        if project_completion == 0:
            current_stage = 'Planning'
            stage_number = 1
        elif project_completion < 20:
            current_stage = 'Design'
            stage_number = 2
        elif project_completion < 40:
            current_stage = 'Pre-construction'
            stage_number = 3
        elif project_completion < 95:
            current_stage = 'Construction'
            stage_number = 4
        else:
            current_stage = 'Final'
            stage_number = 5
        
        stages_data.append({
            'project_id': project['project_id'],
            'stage': current_stage,
            'stage_number': stage_number
        })
    
    df_project_stages = pd.DataFrame(stages_data)
    
    # Generate budget variance data (monthly tracking)
    budget_variance_data = []
    for _, project in df_projects_master.iterrows():
        start_date = project['start_date']
        end_date = project['planned_end_date']
        
        # Generate monthly data points
        current_date = start_date.replace(day=1)
        monthly_budget = project['budget'] / ((end_date - start_date).days / 30.44)  # Average days per month
        
        month_count = 0
        while current_date <= dt.datetime.now() and current_date <= end_date and month_count < 24:
            # Calculate actual vs planned budget for this month
            planned_budget = monthly_budget
            
            # Add some variance to actual budget
            variance_factor = np.random.uniform(0.7, 1.3)
            actual_budget = planned_budget * variance_factor
            
            budget_variance_data.append({
                'project_id': project['project_id'],
                'month': current_date.strftime('%Y-%m'),
                'actual_budget': actual_budget,
                'planned_budget': planned_budget
            })
            
            # Move to next month
            if current_date.month == 12:
                current_date = current_date.replace(year=current_date.year + 1, month=1)
            else:
                current_date = current_date.replace(month=current_date.month + 1)
            
            month_count += 1
    
    df_budget_variance = pd.DataFrame(budget_variance_data)
    
    # Generate resources data
    resource_types = ['Human Resources', 'Equipment', 'Materials']
    resources_data = []
    
    for _, project in df_projects_master.iterrows():
        for resource_type in resource_types:
            # Calculate resource allocation based on project type and size
            if project['type'] == 'Residential Complex':
                base_allocation = {'Human Resources': 0.4, 'Equipment': 0.2, 'Materials': 0.4}
            elif project['type'] == 'Commercial Building':
                base_allocation = {'Human Resources': 0.35, 'Equipment': 0.25, 'Materials': 0.4}
            elif project['type'] == 'Industrial Facility':
                base_allocation = {'Human Resources': 0.3, 'Equipment': 0.35, 'Materials': 0.35}
            else:  # Infrastructure
                base_allocation = {'Human Resources': 0.25, 'Equipment': 0.4, 'Materials': 0.35}
            
            planned_resources = project['budget'] * base_allocation[resource_type]
            actual_resources = planned_resources * np.random.uniform(0.8, 1.2)
            
            resources_data.append({
                'project_id': project['project_id'],
                'actual_resources': actual_resources,
                'planned_resources': planned_resources,
                'resource_type': resource_type
            })
    
    df_resources = pd.DataFrame(resources_data)
    
    # Generate workload data
    workload_data = []
    for _, project in df_projects_master.iterrows():
        # Calculate work hours based on project size and completion
        total_estimated_hours = project['duration_days'] * 8 * np.random.randint(5, 25)  # 5-25 people working 8 hours/day
        
        completion_pct = df_project_status[
            df_project_status['project_id'] == project['project_id']
        ]['completion_percent'].iloc[0]
        
        completed_hours = total_estimated_hours * (completion_pct / 100)
        remaining_hours = max(0, total_estimated_hours - completed_hours)
        
        # Calculate overdue hours (if project is behind schedule)
        if completion_pct < 100 and dt.datetime.now() > project['planned_end_date']:
            overdue_factor = min(0.3, (dt.datetime.now() - project['planned_end_date']).days / 365)
            overdue_hours = total_estimated_hours * overdue_factor
        else:
            overdue_hours = 0
        
        workload_data.append({
            'project_id': project['project_id'],
            'completed_hours': completed_hours,
            'remaining_hours': remaining_hours,
            'overdue_hours': overdue_hours
        })
    
    df_workload = pd.DataFrame(workload_data)
    
    # Save all datasets
    df_projects_master.to_csv('data/projects_master.csv', index=False)
    df_project_status.to_csv('data/project_status.csv', index=False)
    df_project_stages.to_csv('data/project_stages.csv', index=False)
    df_budget_variance.to_csv('data/budget_variance.csv', index=False)
    df_resources.to_csv('data/resources.csv', index=False)
    df_workload.to_csv('data/workload.csv', index=False)
    
    print(f"Generated construction project data:")
    print(f"- Projects Master: {len(df_projects_master)} projects")
    print(f"- Project Status: {len(df_project_status)} status records")
    print(f"- Project Stages: {len(df_project_stages)} stage records")
    print(f"- Budget Variance: {len(df_budget_variance)} monthly records")
    print(f"- Resources: {len(df_resources)} resource allocations")
    print(f"- Workload: {len(df_workload)} workload records")
    
    return df_projects_master, df_project_status, df_project_stages, df_budget_variance, df_resources, df_workload

if __name__ == "__main__":
    # Generate all data
    df_projects_master, df_project_status, df_project_stages, df_budget_variance, df_resources, df_workload = generate_construction_projects(30)
    print("\nConstruction project data generation completed successfully!")