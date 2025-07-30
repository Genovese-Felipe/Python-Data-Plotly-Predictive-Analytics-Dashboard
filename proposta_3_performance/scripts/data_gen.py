# scripts/data_gen.py - Advanced Performance Analytics Dashboard (Proposal 3)
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
    Generate advanced project data for performance analytics dashboard
    
    Parameters:
    -----------
    n_projects : int
        Number of projects to generate
        
    Returns:
    --------
    tuple
        DataFrames for projects, milestones, financial, resources, quality metrics
    """
    
    # Ensure data directory exists
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Advanced project categories
    project_categories = ['Software Development', 'Digital Transformation', 'Data Analytics', 'AI/ML Implementation', 'Cloud Migration']
    business_units = ['Technology', 'Finance', 'Operations', 'Marketing', 'HR']
    priority_levels = ['Critical', 'High', 'Medium', 'Low']
    
    # Time ranges
    start_date_base = dt.datetime(2023, 6, 1)
    end_date = dt.datetime(2025, 12, 31)
    
    # Generate master project data
    projects_data = {
        'project_id': [f'ADV-{i:04d}' for i in range(1, n_projects + 1)],
        'project_name': [f'{cat} Project {i:03d}' for i, cat in enumerate(np.random.choice(project_categories, n_projects), 1)],
        'category': np.random.choice(project_categories, n_projects),
        'business_unit': np.random.choice(business_units, n_projects),
        'priority': np.random.choice(priority_levels, n_projects, p=[0.1, 0.3, 0.5, 0.1]),
        'project_manager': [f'PM {chr(65 + i % 20)}' for i in range(n_projects)],
        'start_date': [start_date_base + dt.timedelta(days=random.randint(0, 400)) for _ in range(n_projects)],
        'planned_duration_days': np.random.randint(60, 450, n_projects),
        'budget_usd': np.random.randint(50000, 1500000, n_projects),
        'complexity_score': np.random.randint(1, 11, n_projects),  # 1-10 scale
        'team_size': np.random.randint(3, 25, n_projects)
    }
    
    df_projects = pd.DataFrame(projects_data)
    
    # Calculate planned end dates
    df_projects['planned_end_date'] = df_projects.apply(
        lambda row: row['start_date'] + dt.timedelta(days=row['planned_duration_days']), axis=1
    )
    
    # Determine current status and actual metrics
    today = dt.datetime.now()
    
    def calculate_project_status(row):
        if row['start_date'] > today:
            return 'Not Started'
        elif row['planned_end_date'] < today:
            return np.random.choice(['Completed', 'Delayed'], p=[0.75, 0.25])
        else:
            return 'In Progress'
    
    df_projects['status'] = df_projects.apply(calculate_project_status, axis=1)
    
    # Calculate progress percentage
    def calculate_progress(row):
        if row['status'] == 'Not Started':
            return np.random.randint(0, 5)
        elif row['status'] == 'Completed':
            return 100
        elif row['status'] == 'Delayed':
            return np.random.randint(75, 98)
        else:  # In Progress
            days_elapsed = (today - row['start_date']).days
            expected_progress = min(95, (days_elapsed / row['planned_duration_days']) * 100)
            actual_progress = max(5, expected_progress + np.random.randint(-20, 25))
            return min(98, actual_progress)
    
    df_projects['progress_percent'] = df_projects.apply(calculate_progress, axis=1)
    
    # Calculate schedule variance (days ahead/behind)
    def calculate_schedule_variance(row):
        if row['status'] == 'Not Started':
            return 0
        days_elapsed = (today - row['start_date']).days
        expected_progress = (days_elapsed / row['planned_duration_days']) * 100
        actual_progress = row['progress_percent']
        progress_variance = actual_progress - expected_progress
        schedule_variance_days = int((progress_variance / 100) * row['planned_duration_days'])
        return schedule_variance_days
    
    df_projects['schedule_variance_days'] = df_projects.apply(calculate_schedule_variance, axis=1)
    
    # Calculate actual end date
    df_projects['actual_end_date'] = df_projects.apply(
        lambda row: row['planned_end_date'] - dt.timedelta(days=row['schedule_variance_days']) 
        if row['status'] == 'Completed' else row['planned_end_date'], axis=1
    )
    
    # Calculate budget variance
    def calculate_budget_variance(row):
        if row['status'] == 'Not Started':
            return 0
        # Budget variance correlates with complexity and schedule variance
        base_variance = (row['complexity_score'] / 10) * 0.2  # Up to 20% for high complexity
        schedule_impact = abs(row['schedule_variance_days']) / row['planned_duration_days'] * 0.15
        total_variance = (base_variance + schedule_impact) * np.random.uniform(0.5, 1.5)
        return min(0.5, total_variance)  # Cap at 50% variance
    
    df_projects['budget_variance_pct'] = df_projects.apply(calculate_budget_variance, axis=1)
    df_projects['actual_cost_usd'] = df_projects['budget_usd'] * (1 + df_projects['budget_variance_pct'])
    
    # Calculate ROI and business value
    df_projects['expected_roi_pct'] = np.random.randint(15, 150, n_projects)  # Expected ROI 15-150%
    df_projects['business_value_score'] = np.random.randint(1, 11, n_projects)  # 1-10 scale
    df_projects['risk_score'] = np.random.randint(1, 11, n_projects)  # 1-10 scale (10 = high risk)
    
    # Quality metrics
    df_projects['quality_score'] = np.random.randint(6, 11, n_projects)  # 6-10 scale
    df_projects['stakeholder_satisfaction'] = np.random.randint(5, 11, n_projects)  # 5-10 scale
    
    # Generate milestone data
    milestones_data = []
    milestone_types = ['Initiation', 'Planning Complete', 'Design Approved', 'Development Complete', 
                      'Testing Complete', 'Deployment', 'Go-Live', 'Project Closure']
    
    for _, project in df_projects.iterrows():
        n_milestones = random.randint(4, 7)
        project_duration = (project['actual_end_date'] - project['start_date']).days
        
        for i in range(n_milestones):
            milestone_date = project['start_date'] + dt.timedelta(
                days=int((i / (n_milestones - 1)) * project_duration)
            )
            
            milestone_type = milestone_types[min(i, len(milestone_types) - 1)]
            
            # Determine if milestone is completed
            is_completed = milestone_date <= today
            
            # Add some variance to actual completion
            actual_date = milestone_date
            if is_completed:
                variance_days = np.random.randint(-5, 15)  # Can be early or late
                actual_date = milestone_date + dt.timedelta(days=variance_days)
            
            milestones_data.append({
                'project_id': project['project_id'],
                'milestone_name': f'{milestone_type} - {project["project_name"]}',
                'milestone_type': milestone_type,
                'planned_date': milestone_date,
                'actual_date': actual_date if is_completed else None,
                'status': 'Completed' if is_completed else 'Pending',
                'importance_score': np.random.randint(1, 6)  # 1-5 scale
            })
    
    df_milestones = pd.DataFrame(milestones_data)
    
    # Generate financial tracking data (monthly)
    financial_data = []
    
    for _, project in df_projects.iterrows():
        if project['status'] == 'Not Started':
            continue
            
        start_month = project['start_date'].replace(day=1)
        end_month = min(today, project['actual_end_date']).replace(day=1)
        
        # Calculate monthly budget distribution
        total_months = max(1, ((project['actual_end_date'] - project['start_date']).days / 30.44))
        monthly_budget = project['budget_usd'] / total_months
        
        current_month = start_month
        month_counter = 0
        
        while current_month <= end_month and month_counter < 36:  # Limit to 3 years
            # Calculate actual spend with some variance
            progress_factor = min(1.0, month_counter / total_months)
            base_spend = monthly_budget * (1 + np.random.uniform(-0.3, 0.5))
            
            # Add project complexity impact
            complexity_multiplier = 1 + (project['complexity_score'] / 10) * 0.2
            actual_spend = base_spend * complexity_multiplier
            
            financial_data.append({
                'project_id': project['project_id'],
                'month': current_month,
                'planned_spend': monthly_budget,
                'actual_spend': actual_spend,
                'cumulative_planned': monthly_budget * (month_counter + 1),
                'cumulative_actual': None  # Will calculate later
            })
            
            # Move to next month
            if current_month.month == 12:
                current_month = current_month.replace(year=current_month.year + 1, month=1)
            else:
                current_month = current_month.replace(month=current_month.month + 1)
            
            month_counter += 1
    
    df_financial = pd.DataFrame(financial_data)
    
    # Calculate cumulative actual spend
    for project_id in df_financial['project_id'].unique():
        project_financial = df_financial[df_financial['project_id'] == project_id].sort_values('month')
        cumulative_actual = project_financial['actual_spend'].cumsum()
        df_financial.loc[df_financial['project_id'] == project_id, 'cumulative_actual'] = cumulative_actual.values
    
    # Generate resource allocation data
    resource_types = ['Senior Developers', 'Junior Developers', 'Project Managers', 'Business Analysts', 
                     'Data Scientists', 'DevOps Engineers', 'QA Engineers', 'UX/UI Designers']
    
    resources_data = []
    
    for _, project in df_projects.iterrows():
        # Determine which resource types this project needs
        n_resource_types = random.randint(3, 6)
        project_resources = random.sample(resource_types, n_resource_types)
        
        for resource_type in project_resources:
            # Calculate allocation based on project characteristics
            base_allocation = np.random.randint(1, 8)  # 1-7 people
            
            # Adjust based on project size and complexity
            if project['team_size'] > 15:
                base_allocation = int(base_allocation * 1.5)
            if project['complexity_score'] > 7:
                base_allocation = int(base_allocation * 1.2)
            
            planned_hours = base_allocation * 40 * (project['planned_duration_days'] / 7)  # 40h/week
            actual_hours = planned_hours * np.random.uniform(0.8, 1.3)
            
            resources_data.append({
                'project_id': project['project_id'],
                'resource_type': resource_type,
                'planned_allocation': base_allocation,
                'actual_allocation': base_allocation * np.random.uniform(0.8, 1.2),
                'planned_hours': planned_hours,
                'actual_hours': actual_hours,
                'hourly_rate': np.random.randint(50, 200)  # $50-200/hour
            })
    
    df_resources = pd.DataFrame(resources_data)
    
    # Generate quality metrics data
    quality_metrics_data = []
    quality_dimensions = ['Code Quality', 'User Experience', 'Performance', 'Security', 'Maintainability']
    
    for _, project in df_projects.iterrows():
        for dimension in quality_dimensions:
            # Quality varies by project type and complexity
            base_score = np.random.randint(6, 10)
            if project['complexity_score'] > 8:
                base_score = max(5, base_score - 1)  # More complex projects may have lower quality
            
            quality_metrics_data.append({
                'project_id': project['project_id'],
                'quality_dimension': dimension,
                'score': base_score,
                'measurement_date': today - dt.timedelta(days=random.randint(0, 30)),
                'target_score': np.random.randint(8, 10)
            })
    
    df_quality = pd.DataFrame(quality_metrics_data)
    
    # Save all datasets
    df_projects.to_csv('data/projects_advanced.csv', index=False)
    df_milestones.to_csv('data/milestones_advanced.csv', index=False)
    df_financial.to_csv('data/financial_advanced.csv', index=False)
    df_resources.to_csv('data/resources_advanced.csv', index=False)
    df_quality.to_csv('data/quality_metrics.csv', index=False)
    
    print(f"Advanced project performance data generated successfully!")
    print(f"- Projects: {len(df_projects)} records")
    print(f"- Milestones: {len(df_milestones)} records")
    print(f"- Financial: {len(df_financial)} records")
    print(f"- Resources: {len(df_resources)} records")
    print(f"- Quality Metrics: {len(df_quality)} records")
    
    return df_projects, df_milestones, df_financial, df_resources, df_quality

if __name__ == "__main__":
    # Generate all advanced data
    df_projects, df_milestones, df_financial, df_resources, df_quality = generate_advanced_projects_data(150)
    print("\nAdvanced performance analytics data generation completed successfully!")