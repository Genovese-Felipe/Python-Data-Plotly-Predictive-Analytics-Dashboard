"""
A data generation script for an advanced performance analytics dashboard.

This script creates a rich, synthetic dataset for analyzing project performance
in-depth. It generates multiple interconnected CSV files covering project details,
milestones, financials, resources, and quality metrics.
"""

import pandas as pd
import numpy as np
import datetime as dt
import random
import os

# Ensure reproducibility
np.random.seed(42)
random.seed(42)


def generate_advanced_projects_data(n_projects=150):
    """
    Generates and saves a comprehensive set of advanced project performance data.

    This function creates five interconnected DataFrames with detailed metrics
    for an advanced analytics dashboard. The datasets include:
    1.  df_projects: Core project data with performance and risk scores.
    2.  df_milestones: Project milestones with planned vs. actual dates.
    3.  df_financial: Monthly financial tracking with planned vs. actual spend.
    4.  df_resources: Detailed resource allocation and costs.
    5.  df_quality: Quality scores across various dimensions.

    Args:
        n_projects (int, optional): The number of projects to generate. Defaults to 150.

    Returns:
        tuple: A tuple of the five generated pandas DataFrames.
    """
    data_dir = os.path.join(os.path.dirname(__file__), '../data')
    os.makedirs(data_dir, exist_ok=True)

    # Project master data
    project_categories = ['Software Development', 'Digital Transformation', 'Data Analytics', 'AI/ML Implementation', 'Cloud Migration']
    projects_data = {
        'project_id': [f'ADV-{i:04d}' for i in range(1, n_projects + 1)],
        'project_name': [f'{cat} Project {i:03d}' for i, cat in enumerate(np.random.choice(project_categories, n_projects), 1)],
        'category': np.random.choice(project_categories, n_projects),
        'start_date': [dt.datetime(2023, 6, 1) + dt.timedelta(days=random.randint(0, 400)) for _ in range(n_projects)],
        'planned_duration_days': np.random.randint(60, 450, n_projects),
        'budget_usd': np.random.randint(50000, 1500000, n_projects),
        'complexity_score': np.random.randint(1, 11, n_projects),
        'risk_score': np.random.randint(1, 11, n_projects)
    }
    df_projects = pd.DataFrame(projects_data)
    df_projects['planned_end_date'] = df_projects.apply(lambda row: row['start_date'] + dt.timedelta(days=row['planned_duration_days']), axis=1)

    # Project status and progress
    today = dt.datetime.now()
    df_projects['status'] = df_projects.apply(lambda row: 'Not Started' if row['start_date'] > today else 'Completed' if row['planned_end_date'] < today else 'In Progress', axis=1)
    df_projects['progress_percent'] = df_projects.apply(lambda row: 100 if row['status'] == 'Completed' else 0 if row['status'] == 'Not Started' else min(99, int(((today - row['start_date']).days / row['planned_duration_days']) * 100)), axis=1)
    df_projects['schedule_variance_days'] = df_projects.apply(lambda row: int((row['progress_percent'] / 100 * row['planned_duration_days']) - (today - row['start_date']).days) if row['status'] == 'In Progress' else 0, axis=1)
    df_projects['actual_cost_usd'] = df_projects['budget_usd'] * (1 + (df_projects['complexity_score'] - 5) / 10 * np.random.uniform(-0.1, 0.2))

    # Milestones data
    milestones_data = []
    for _, project in df_projects.iterrows():
        for i in range(5):
            milestones_data.append({
                'project_id': project['project_id'],
                'milestone_name': f'Milestone {i+1}',
                'planned_date': project['start_date'] + dt.timedelta(days=int(project['planned_duration_days'] * (i+1)/5))
            })
    df_milestones = pd.DataFrame(milestones_data)

    # Financial data
    financial_data = []
    for _, project in df_projects.iterrows():
        for i in range(12):
            financial_data.append({
                'project_id': project['project_id'],
                'month': (project['start_date'] + dt.timedelta(days=30*i)).strftime('%Y-%m'),
                'planned_spend': project['budget_usd'] / 12,
                'actual_spend': project['budget_usd'] / 12 * np.random.uniform(0.8, 1.2)
            })
    df_financial = pd.DataFrame(financial_data)

    # Resources data
    resources_data = []
    resource_types = ['Senior Dev', 'Junior Dev', 'PM', 'QA', 'DevOps']
    for _, project in df_projects.iterrows():
        for r_type in resource_types:
            resources_data.append({
                'project_id': project['project_id'],
                'resource_type': r_type,
                'planned_hours': np.random.randint(100, 500),
                'actual_hours': np.random.randint(80, 600)
            })
    df_resources = pd.DataFrame(resources_data)

    # Quality metrics
    quality_metrics_data = []
    for _, project in df_projects.iterrows():
        quality_metrics_data.append({
            'project_id': project['project_id'],
            'code_quality_score': np.random.randint(70, 100),
            'test_coverage_pct': np.random.randint(80, 100),
            'customer_satisfaction': np.random.randint(1, 6)
        })
    df_quality = pd.DataFrame(quality_metrics_data)

    # Save datasets
    data_dir = os.path.join(os.path.dirname(__file__), '../data')
    df_projects.to_csv(os.path.join(data_dir, 'projects_advanced.csv'), index=False)
    df_milestones.to_csv(os.path.join(data_dir, 'milestones_advanced.csv'), index=False)
    df_financial.to_csv(os.path.join(data_dir, 'financial_advanced.csv'), index=False)
    df_resources.to_csv(os.path.join(data_dir, 'resources_advanced.csv'), index=False)
    df_quality.to_csv(os.path.join(data_dir, 'quality_metrics.csv'), index=False)
    
    print("Advanced project performance data generated successfully!")
    print(f"- Projects: {len(df_projects)} records")
    print(f"- Milestones: {len(df_milestones)} records")
    print(f"- Financial: {len(df_financial)} records")
    print(f"- Resources: {len(df_resources)} records")
    print(f"- Quality Metrics: {len(df_quality)} records")
    
    return df_projects, df_milestones, df_financial, df_resources, df_quality


if __name__ == "__main__":
    generate_advanced_projects_data(150)
    print("\nAdvanced performance analytics data generation completed successfully!")