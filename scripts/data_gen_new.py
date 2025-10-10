"""
A data generation script for the construction project dashboard.

This script creates several CSV files containing synthetic data that mimics
real-world construction project management scenarios. The generated data covers
project metadata, status, budget, resources, and workload.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Configuration
NUM_PROJECTS = 30
DATA_DIR = os.path.join(os.path.dirname(__file__), '../data')


def generate_projects_master():
    """
    Generates the master project information DataFrame.

    Returns:
        pd.DataFrame: A DataFrame containing the master project data.
    """
    np.random.seed(42)
    project_ids = [f'Project_{i}' for i in range(1, NUM_PROJECTS + 1)]
    project_types = ['Engineering & Non-Residential', 'Commercial Building', 'Infrastructure']
    managers = ['Project Manager_A', 'Project Manager_B', 'Project Manager_C', 'Project Manager_D', 'Project Manager_E']
    start_dates = pd.to_datetime(pd.date_range(start='2022-01-01', end='2024-01-01', periods=NUM_PROJECTS))
    
    return pd.DataFrame({
        'project_id': project_ids,
        'name': [f'Construction Project {i}' for i in range(1, NUM_PROJECTS + 1)],
        'type': np.random.choice(project_types, NUM_PROJECTS, p=[0.4, 0.35, 0.25]),
        'manager': np.random.choice(managers, NUM_PROJECTS),
        'start_date': start_dates,
        'budget': np.random.uniform(100000, 1000000, NUM_PROJECTS).round(0).astype(int),
        'duration_days': np.random.randint(180, 1500, NUM_PROJECTS)
    })


def generate_project_status(projects_master):
    """
    Generates project status data, including completion and budget spending.

    Args:
        projects_master (pd.DataFrame): The master projects DataFrame.

    Returns:
        pd.DataFrame: A DataFrame with project status details.
    """
    np.random.seed(42)
    statuses = np.random.choice(['Completed', 'In Progress', 'Not Started'], NUM_PROJECTS, p=[0.4, 0.5, 0.1])
    data = []
    for i, row in projects_master.iterrows():
        status = statuses[i]
        completion = 100 if status == 'Completed' else 0 if status == 'Not Started' else np.random.randint(20, 95)
        budget_variance = np.random.uniform(0.8, 1.2) if status == 'Completed' else np.random.uniform(0.0, 0.1) if status == 'Not Started' else np.random.uniform(0.7, 1.3)
        days_variance = np.random.uniform(0.9, 1.1) if status == 'Completed' else np.random.uniform(0.0, 0.1) if status == 'Not Started' else np.random.uniform(0.8, 1.2)
        
        data.append({
            'project_id': row['project_id'], 'status': status, 'completion_percent': completion,
            'budget_used': int(row['budget'] * budget_variance),
            'days_used': int(row['duration_days'] * days_variance)
        })
    return pd.DataFrame(data)


def generate_project_stages():
    """
    Generates data for the different stages of each project.

    Returns:
        pd.DataFrame: A DataFrame mapping projects to their current stage.
    """
    np.random.seed(42)
    stages = ['Plan', 'Design', 'Pre-construct', 'Construct', 'Close-out']
    project_stages = []
    for project_num in range(1, NUM_PROJECTS + 1):
        project_id = f'Project_{project_num}'
        num_stages = np.random.randint(1, 4)
        project_stage_list = np.random.choice(stages, num_stages, replace=False)
        for stage_num, stage in enumerate(project_stage_list, 1):
            project_stages.append({'project_id': project_id, 'stage': stage, 'stage_number': stage_num})
    return pd.DataFrame(project_stages)


def generate_budget_variance():
    """
    Generates monthly budget variance data for each project.

    Returns:
        pd.DataFrame: A DataFrame with planned vs. actual budget data.
    """
    np.random.seed(42)
    budget_data = []
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    for project_num in range(1, NUM_PROJECTS + 1):
        project_id = f'Project_{project_num}'
        num_months = np.random.randint(3, 12)
        selected_months = np.random.choice(months, num_months, replace=False)
        base_budget = np.random.uniform(50000, 200000)
        for month in selected_months:
            variance = np.random.uniform(-0.3, 0.4)
            budget_data.append({
                'project_id': project_id, 'month': month,
                'planned_budget': base_budget,
                'actual_budget': base_budget * (1 + variance),
                'variance': base_budget * variance
            })
    return pd.DataFrame(budget_data)


def generate_resources():
    """
    Generates data on planned vs. actual resource allocation.

    Returns:
        pd.DataFrame: A DataFrame detailing resource utilization.
    """
    np.random.seed(42)
    resource_types = ['Engineers', 'Architects', 'Project Managers', 'Contractors', 'Supervisors']
    resources_data = []
    for project_num in range(1, NUM_PROJECTS + 1):
        project_id = f'Project_{project_num}'
        num_resource_types = np.random.randint(2, 5)
        used_resources = np.random.choice(resource_types, num_resource_types, replace=False)
        for resource_type in used_resources:
            planned = np.random.randint(2, 20)
            actual = max(1, int(planned * np.random.uniform(0.7, 1.3)))
            resources_data.append({
                'project_id': project_id, 'resource_type': resource_type,
                'planned_resources': planned, 'actual_resources': actual
            })
    return pd.DataFrame(resources_data)


def generate_workload():
    """
    Generates workload data, including completed, remaining, and overdue hours.

    Returns:
        pd.DataFrame: A DataFrame with workload breakdown for each project.
    """
    np.random.seed(42)
    workload_data = []
    for project_num in range(1, NUM_PROJECTS + 1):
        project_id = f'Project_{project_num}'
        total_hours = np.random.randint(1000, 10000)
        completion_rate = np.random.uniform(0.2, 0.9)
        completed_hours = int(total_hours * completion_rate)
        remaining_hours = total_hours - completed_hours
        overdue_hours = np.random.randint(0, int(remaining_hours * 0.3)) if remaining_hours > 0 else 0
        workload_data.append({
            'project_id': project_id,
            'completed_hours': completed_hours,
            'remaining_hours': max(0, remaining_hours - overdue_hours),
            'overdue_hours': overdue_hours,
            'total_hours': total_hours
        })
    return pd.DataFrame(workload_data)


def main():
    """
    Main function to generate all datasets and save them to CSV files.
    """
    print("🏗️ Generating Construction Project Dashboard Data...")
    os.makedirs(DATA_DIR, exist_ok=True)

    projects_master = generate_projects_master()
    datasets = {
        'projects_master.csv': projects_master,
        'project_status.csv': generate_project_status(projects_master),
        'project_stages.csv': generate_project_stages(),
        'budget_variance.csv': generate_budget_variance(),
        'resources.csv': generate_resources(),
        'workload.csv': generate_workload()
    }

    for filename, df in datasets.items():
        filepath = os.path.join(DATA_DIR, filename)
        df.to_csv(filepath, index=False)
        print(f"✅ Saved {filename} with {len(df)} records to {filepath}")

    print(f"\n🎯 Data generation complete! Files saved to: {DATA_DIR}/")


if __name__ == "__main__":
    main()