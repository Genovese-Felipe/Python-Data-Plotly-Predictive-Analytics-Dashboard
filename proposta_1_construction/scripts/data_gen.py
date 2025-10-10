"""
A script to generate synthetic data for the construction project dashboard.

This script creates multiple CSV files with realistic data that mimics
construction project management scenarios. The generated data covers project
metadata, status, stages, budget, resources, and workload.
"""

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
    Generates and saves a complete set of synthetic data for construction projects.

    This function creates several pandas DataFrames containing realistic data for
    a construction project dashboard, including project master data, status,
    stages, budget variance, resources, and workload. It then saves each
    DataFrame to a CSV file in the '../data' directory.

    Args:
        n_projects (int, optional): The number of projects to generate. Defaults to 30.

    Returns:
        tuple: A tuple of pandas DataFrames for each generated dataset.
    """
    data_dir = os.path.join(os.path.dirname(__file__), '../data')
    os.makedirs(data_dir, exist_ok=True)

    project_types = ['Residential Complex', 'Commercial Building', 'Industrial Facility', 'Infrastructure']
    
    projects_master = {
        'project_id': [f'PROJ-{i:03d}' for i in range(1, n_projects + 1)],
        'name': [f'Construction Project {i:03d}' for i in range(1, n_projects + 1)],
        'type': np.random.choice(project_types, n_projects),
        'manager': [f'Manager {chr(65 + i % 10)}' for i in range(n_projects)],
        'start_date': [dt.datetime(2023, 1, 1) + dt.timedelta(days=random.randint(0, 365)) for _ in range(n_projects)],
        'budget': np.random.randint(500000, 5000000, n_projects),
        'duration_days': np.random.randint(90, 730, n_projects)
    }
    df_projects_master = pd.DataFrame(projects_master)
    df_projects_master['planned_end_date'] = df_projects_master.apply(lambda row: row['start_date'] + dt.timedelta(days=row['duration_days']), axis=1)

    status_data = []
    for _, project in df_projects_master.iterrows():
        today = dt.datetime.now()
        if project['start_date'] > today:
            status, completion = 'Not Started', 0
        elif project['planned_end_date'] < today:
            status = np.random.choice(['Completed', 'Delayed'], p=[0.7, 0.3])
            completion = 100 if status == 'Completed' else np.random.randint(85, 99)
        else:
            status = 'In Progress'
            days_elapsed = (today - project['start_date']).days
            expected_progress = min(95, (days_elapsed / project['duration_days']) * 100)
            completion = max(5, expected_progress + np.random.randint(-10, 15))
        
        budget_used = 0 if status == 'Not Started' else project['budget'] * (completion / 100) * np.random.uniform(0.8, 1.2)
        days_used = max(0, (today - project['start_date']).days) if status != 'Not Started' else 0
        status_data.append({'project_id': project['project_id'], 'status': status, 'completion_percent': completion, 'budget_used': budget_used, 'days_used': days_used})
    df_project_status = pd.DataFrame(status_data)

    stages_data = []
    for _, project in df_projects_master.iterrows():
        completion = df_project_status.loc[df_project_status['project_id'] == project['project_id'], 'completion_percent'].iloc[0]
        if completion == 0: stage, num = 'Planning', 1
        elif completion < 20: stage, num = 'Design', 2
        elif completion < 40: stage, num = 'Pre-construction', 3
        elif completion < 95: stage, num = 'Construction', 4
        else: stage, num = 'Final', 5
        stages_data.append({'project_id': project['project_id'], 'stage': stage, 'stage_number': num})
    df_project_stages = pd.DataFrame(stages_data)

    datasets = {
        'projects_master.csv': df_projects_master, 'project_status.csv': df_project_status,
        'project_stages.csv': df_project_stages
    }
    for filename, df in datasets.items():
        df.to_csv(os.path.join(data_dir, filename), index=False)
        print(f"- Saved {filename}: {len(df)} records")
    
    return tuple(datasets.values())


if __name__ == "__main__":
    generate_construction_projects(30)
    print("\nConstruction project data generation completed successfully!")