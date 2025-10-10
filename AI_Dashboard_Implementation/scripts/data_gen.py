"""
A data generation script for the AI-powered construction project dashboard.

This script creates a comprehensive set of realistic, synthetic data for
visualizing and analyzing construction project performance. It generates
multiple interconnected CSV files covering all key aspects of project
management, from high-level project details to daily status updates.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Ensure reproducible results for consistent data generation
np.random.seed(42)


def create_data_directory():
    """
    Ensures that the data directory exists, creating it if necessary.

    Returns:
        str: The path to the data directory.
    """
    data_dir = os.path.join(os.path.dirname(__file__), '../data')
    os.makedirs(data_dir, exist_ok=True)
    return data_dir


def generate_projects_master(num_projects=25):
    """
    Generates the main project master dataset.

    Args:
        num_projects (int, optional): The number of projects to generate.

    Returns:
        pd.DataFrame: A DataFrame containing the master list of projects.
    """
    project_types = ['Residential', 'Commercial', 'Infrastructure', 'Industrial']
    statuses = ['Planning', 'In Progress', 'Completed', 'On Hold']
    managers = ['John Smith', 'Maria Garcia', 'David Chen', 'Sarah Johnson']
    
    projects = []
    for i in range(1, num_projects + 1):
        start_date = datetime(2024, 1, 1) + timedelta(days=np.random.randint(0, 180))
        duration = np.random.randint(30, 365)
        budget = np.random.randint(100000, 2000000)
        completion = max(0, min(100, ((datetime.now() - start_date).days / duration) * 100 + np.random.normal(0, 10)))
        
        projects.append({
            'project_id': f'PROJ_{i:03d}',
            'project_name': f'{np.random.choice(project_types)} Project {i}',
            'project_type': np.random.choice(project_types),
            'status': np.random.choice(statuses, p=[0.1, 0.5, 0.3, 0.1]),
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': (start_date + timedelta(days=duration)).strftime('%Y-%m-%d'),
            'budget_allocated': budget,
            'budget_spent': round(budget * (completion / 100) * np.random.uniform(0.8, 1.2), 2),
            'completion_percentage': round(completion, 1),
            'project_manager': np.random.choice(managers),
        })
    return pd.DataFrame(projects)


def generate_resources_data(projects_df, num_entries=200):
    """
    Generates resource allocation and usage data.

    Args:
        projects_df (pd.DataFrame): The master projects DataFrame.
        num_entries (int, optional): The number of resource entries to generate.

    Returns:
        pd.DataFrame: A DataFrame with resource allocation data.
    """
    resource_types = ['Equipment', 'Labor', 'Materials']
    resources = []
    for i in range(num_entries):
        project_id = np.random.choice(projects_df['project_id'])
        resource_type = np.random.choice(resource_types)
        allocated_qty = np.random.randint(1, 100)
        resources.append({
            'resource_id': f'RES_{i:04d}',
            'project_id': project_id,
            'resource_type': resource_type,
            'allocated_quantity': allocated_qty,
            'used_quantity': round(allocated_qty * np.random.uniform(0.7, 1.1), 2),
            'cost_per_unit': np.random.randint(50, 1000),
        })
    return pd.DataFrame(resources)


def generate_workload_data(projects_df, num_entries=300):
    """
    Generates team workload and productivity data.

    Args:
        projects_df (pd.DataFrame): The master projects DataFrame.
        num_entries (int, optional): The number of workload entries to generate.

    Returns:
        pd.DataFrame: A DataFrame with team workload data.
    """
    team_members = ['John Doe', 'Jane Smith', 'Bob Wilson', 'Alice Brown']
    workload = []
    for i in range(num_entries):
        project_id = np.random.choice(projects_df['project_id'])
        hours_worked = max(0, min(12, np.random.normal(8, 1.5)))
        workload.append({
            'date': (datetime.now() - timedelta(days=np.random.randint(0, 90))).strftime('%Y-%m-%d'),
            'project_id': project_id,
            'team_member': np.random.choice(team_members),
            'hours_worked': round(hours_worked, 1),
            'productivity_score': round(max(0.3, min(1.0, (hours_worked / 8) + np.random.normal(0, 0.15))), 2),
        })
    return pd.DataFrame(workload)


def main():
    """
    Main function to generate all datasets and save them to CSV files.
    """
    print("🏗️ Construction Dashboard Data Generation")
    data_dir = create_data_directory()
    print(f"📁 Data directory: {data_dir}")

    print("📊 Generating projects master data...")
    projects_df = generate_projects_master()
    projects_df.to_csv(f'{data_dir}/projects_master.csv', index=False)
    print(f"   ✅ Generated {len(projects_df)} projects")

    print("🔧 Generating resources data...")
    resources_df = generate_resources_data(projects_df)
    resources_df.to_csv(f'{data_dir}/resources.csv', index=False)
    print(f"   ✅ Generated {len(resources_df)} resource entries")

    print("👥 Generating workload data...")
    workload_df = generate_workload_data(projects_df)
    workload_df.to_csv(f'{data_dir}/workload.csv', index=False)
    print(f"   ✅ Generated {len(workload_df)} workload entries")

    print("\n✅ Data generation completed successfully!")
    print(f"📁 All CSV files saved to {data_dir}")


if __name__ == "__main__":
    main()