"""
A data generation script for a performance-focused projects dashboard.

This script creates several CSV files with simulated data to model various
aspects of project performance, including project details, milestones,
financials, and resource allocation.
"""

import pandas as pd
import numpy as np
import datetime as dt
import random
import os

# Ensure reproducibility
np.random.seed(42)
random.seed(42)


def generate_project_data(n_projects=200):
    """
    Generates simulated data for project performance analysis.

    This function creates and saves three DataFrames:
    1.  df_projects: Core project details, status, and performance metrics.
    2.  df_milestones: Project milestones with planned and actual dates.
    3.  df_financials: Monthly financial data, including budget and actuals.

    Args:
        n_projects (int, optional): The number of projects to generate. Defaults to 200.

    Returns:
        tuple: A tuple containing the three generated pandas DataFrames.
    """
    data_dir = os.path.join(os.path.dirname(__file__), '../data')
    os.makedirs(data_dir, exist_ok=True)

    project_types = ['Residential', 'Commercial', 'Industrial', 'Infrastructure']
    regions = ['North', 'South', 'East', 'West', 'Central']

    # Generate basic project data
    projects_data = {
        'project_id': [f'PROJ-{i:04d}' for i in range(1, n_projects + 1)],
        'project_name': [f'Project {t} {i:03d}' for i, t in enumerate(np.random.choice(project_types, n_projects), 1)],
        'project_type': np.random.choice(project_types, n_projects),
        'region': np.random.choice(regions, n_projects),
        'manager': [f'Manager {chr(65 + i % 15)}' for i in range(n_projects)],
        'start_date': [dt.datetime(2023, 1, 1) + dt.timedelta(days=random.randint(0, 365)) for _ in range(n_projects)],
        'planned_duration': np.random.randint(30, 365, n_projects),
        'budget': np.random.randint(100000, 2000000, n_projects),
        'complexity': np.random.choice(['Low', 'Medium', 'High', 'Very High'], n_projects, p=[0.2, 0.4, 0.3, 0.1])
    }
    df_projects = pd.DataFrame(projects_data)
    df_projects['planned_completion_date'] = df_projects.apply(lambda row: row['start_date'] + dt.timedelta(days=row['planned_duration']), axis=1)

    # Determine status and progress
    today = dt.datetime.now()
    df_projects['status'] = df_projects.apply(lambda row: 'Planned' if row['start_date'] > today else np.random.choice(['Completed', 'Delayed'], p=[0.7, 0.3]) if row['planned_completion_date'] < today else 'In Progress', axis=1)
    df_projects['progress'] = df_projects.apply(lambda row: 100 if row['status'] == 'Completed' else np.random.randint(70, 95) if row['status'] == 'Delayed' else 0, axis=1)
    df_projects['delay_days'] = df_projects.apply(lambda row: np.random.randint(15, 60) if row['status'] == 'Delayed' else 0, axis=1)
    df_projects['actual_completion_date'] = df_projects.apply(lambda row: row['planned_completion_date'] + dt.timedelta(days=row['delay_days']), axis=1)
    df_projects['cost_overrun_pct'] = df_projects.apply(lambda row: np.random.randint(5, 25) if row['delay_days'] > 0 else np.random.randint(0, 10), axis=1)
    df_projects['actual_cost'] = df_projects['budget'] * (1 + df_projects['cost_overrun_pct'] / 100)

    # Generate milestones
    milestones_data = []
    milestone_types = ['Initiation', 'Planning', 'Execution', 'Monitoring', 'Closure']
    for _, project in df_projects.iterrows():
        for i, m_type in enumerate(milestone_types):
            milestones_data.append({
                'project_id': project['project_id'],
                'milestone_name': f'{m_type} - {project["project_name"]}',
                'milestone_type': m_type,
                'planned_date': project['start_date'] + dt.timedelta(days=int((i / 4) * project['planned_duration']))
            })
    df_milestones = pd.DataFrame(milestones_data)

    # Generate monthly financials
    financial_data = []
    for _, project in df_projects.iterrows():
        if project['status'] == 'Planned': continue
        start_date = project['start_date']
        end_date = min(project['actual_completion_date'], today)
        num_months = (end_date.year - start_date.year) * 12 + end_date.month - start_date.month
        monthly_budget = project['budget'] / max(1, num_months)
        for i in range(num_months + 1):
            current_date = start_date + dt.timedelta(days=30*i)
            if current_date > end_date: break
            financial_data.append({
                'project_id': project['project_id'],
                'date': current_date.strftime('%Y-%m-01'),
                'budgeted': monthly_budget,
                'actual': monthly_budget * (1 + np.random.uniform(-0.2, 0.3)),
            })
    df_financials = pd.DataFrame(financial_data)

    # Save datasets
    df_projects.to_csv(os.path.join(data_dir, 'projects.csv'), index=False)
    df_milestones.to_csv(os.path.join(data_dir, 'project_milestones.csv'), index=False)
    df_financials.to_csv(os.path.join(data_dir, 'monthly_financials.csv'), index=False)

    print("Project performance data generated successfully!")
    print(f"- Projects: {len(df_projects)} records")
    print(f"- Milestones: {len(df_milestones)} records")
    print(f"- Financials: {len(df_financials)} records")
    
    return df_projects, df_milestones, df_financials


def generate_resource_data(df_projects):
    """
    Generates data about the resources used in the projects.

    Args:
        df_projects (pd.DataFrame): The main projects DataFrame.

    Returns:
        pd.DataFrame: A DataFrame with resource allocation data.
    """
    data_dir = os.path.join(os.path.dirname(__file__), '../data')
    resource_categories = ['Human Resources', 'Equipment', 'Materials', 'Software', 'Consulting', 'Infrastructure']
    resources_data = []
    
    for _, project in df_projects.iterrows():
        n_categories = random.randint(3, len(resource_categories))
        selected_cats = random.sample(resource_categories, n_categories)
        distribution = np.random.dirichlet(np.ones(n_categories)) * 100
        
        for i, category in enumerate(selected_cats):
            budgeted_value = project['budget'] * (distribution[i] / 100)
            actual_value = budgeted_value * (1 + project['cost_overrun_pct'] / 100 * np.random.uniform(0.5, 1.5))
            resources_data.append({
                'project_id': project['project_id'],
                'resource_category': category,
                'budgeted_value': budgeted_value,
                'actual_value': actual_value
            })
    
    df_resources = pd.DataFrame(resources_data)
    df_resources.to_csv(os.path.join(data_dir, 'project_resources.csv'), index=False)
    print(f"- Resources: {len(df_resources)} records")
    return df_resources


if __name__ == "__main__":
    print("Generating all performance project data...")
    df_projects, _, _ = generate_project_data(200)
    generate_resource_data(df_projects)
    print("\nData generation for performance projects completed successfully!")