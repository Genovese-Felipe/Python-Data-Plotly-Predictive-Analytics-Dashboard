"""
Construction Project Dashboard - Data Generation Script
========================================================

This script generates realistic construction project data for dashboard visualization.
Uses only pandas and numpy as required by project guidelines.

Data Story: Construction company managing multiple projects with:
- Project portfolio tracking
- Resource allocation monitoring  
- Budget performance analysis
- Team productivity measurement
- Timeline management

Generated datasets:
- projects_master.csv: Main project information
- resources.csv: Resource allocation and usage
- workload.csv: Team workload and productivity
- budget_variance.csv: Budget tracking over time
- project_stages.csv: Project milestone tracking
- project_status.csv: Daily status updates
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Set random seed for reproducible results
np.random.seed(42)

def create_data_directory():
    """Create data directory if it doesn't exist"""
    data_dir = '../data'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    return data_dir

def generate_projects_master(num_projects=25):
    """Generate main project dataset"""
    
    project_types = ['Residential', 'Commercial', 'Infrastructure', 'Industrial']
    statuses = ['Planning', 'In Progress', 'Completed', 'On Hold', 'Review']
    managers = ['John Smith', 'Maria Garcia', 'David Chen', 'Sarah Johnson', 'Mike Brown', 'Lisa Davis']
    clients = ['ABC Corp', 'Metro City', 'Green Development', 'Tech Solutions', 'Urban Planning', 
               'Future Builders', 'Smart Homes Inc', 'City Council', 'Regional Authority']
    
    projects = []
    
    for i in range(1, num_projects + 1):
        # Generate realistic project dates
        start_date = datetime(2024, 1, 1) + timedelta(days=np.random.randint(0, 180))
        duration = np.random.randint(30, 365)  # Project duration in days
        end_date = start_date + timedelta(days=duration)
        
        # Budget ranges by project type
        project_type = np.random.choice(project_types)
        if project_type == 'Infrastructure':
            budget_base = np.random.randint(500000, 2000000)
        elif project_type == 'Commercial':
            budget_base = np.random.randint(200000, 800000)
        elif project_type == 'Industrial':
            budget_base = np.random.randint(300000, 1200000)
        else:  # Residential
            budget_base = np.random.randint(100000, 500000)
            
        # Calculate realistic completion based on time elapsed
        days_elapsed = min((datetime.now() - start_date).days, duration)
        base_completion = max(0, min(100, (days_elapsed / duration) * 100))
        
        # Add some variance to completion percentage
        completion = max(0, min(100, base_completion + np.random.normal(0, 10)))
        
        # Budget spent correlates with completion but has variance
        budget_spent = budget_base * (completion / 100) * np.random.uniform(0.8, 1.2)
        budget_spent = min(budget_spent, budget_base * 1.1)  # Don't exceed 110% of budget
        
        projects.append({
            'project_id': f'PROJ_{i:03d}',
            'project_name': f'{project_type} Project {i}',
            'project_type': project_type,
            'status': np.random.choice(statuses, p=[0.1, 0.4, 0.3, 0.1, 0.1]),
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'budget_allocated': budget_base,
            'budget_spent': round(budget_spent, 2),
            'completion_percentage': round(completion, 1),
            'project_manager': np.random.choice(managers),
            'client': np.random.choice(clients),
            'priority': np.random.choice(['High', 'Medium', 'Low'], p=[0.2, 0.6, 0.2]),
            'team_size': np.random.randint(3, 15),
            'location': f'Site {i}',
            'contract_value': round(budget_base * np.random.uniform(1.05, 1.25), 2)
        })
    
    return pd.DataFrame(projects)

def generate_resources_data(projects_df, num_entries=200):
    """Generate resource allocation and usage data"""
    
    resource_types = ['Equipment', 'Labor', 'Materials']
    equipment_names = ['Excavator', 'Crane', 'Bulldozer', 'Mixer', 'Pump', 'Generator']
    labor_names = ['Construction Worker', 'Engineer', 'Supervisor', 'Electrician', 'Plumber', 'Carpenter']
    material_names = ['Concrete', 'Steel', 'Lumber', 'Pipes', 'Electrical', 'Insulation']
    
    resources = []
    
    for i in range(num_entries):
        project_id = np.random.choice(projects_df['project_id'])
        resource_type = np.random.choice(resource_types)
        
        if resource_type == 'Equipment':
            resource_name = np.random.choice(equipment_names)
            cost_per_unit = np.random.randint(200, 1000)
            allocated_qty = np.random.randint(1, 5)
        elif resource_type == 'Labor':
            resource_name = np.random.choice(labor_names)
            cost_per_unit = np.random.randint(150, 500)  # Daily rate
            allocated_qty = np.random.randint(2, 20)
        else:  # Materials
            resource_name = np.random.choice(material_names)
            cost_per_unit = np.random.randint(50, 300)
            allocated_qty = np.random.randint(10, 100)
        
        used_qty = allocated_qty * np.random.uniform(0.7, 1.1)
        
        # Generate date within project timeline
        project_start = datetime.strptime(
            projects_df[projects_df['project_id'] == project_id]['start_date'].iloc[0], 
            '%Y-%m-%d'
        )
        random_days = np.random.randint(0, 90)
        resource_date = project_start + timedelta(days=random_days)
        
        resources.append({
            'resource_id': f'RES_{i:04d}',
            'project_id': project_id,
            'resource_type': resource_type,
            'resource_name': resource_name,
            'allocated_quantity': allocated_qty,
            'used_quantity': round(used_qty, 2),
            'cost_per_unit': cost_per_unit,
            'total_cost': round(used_qty * cost_per_unit, 2),
            'date': resource_date.strftime('%Y-%m-%d'),
            'efficiency_score': round(np.random.uniform(0.8, 1.0), 2)
        })
    
    return pd.DataFrame(resources)

def generate_workload_data(projects_df, num_entries=300):
    """Generate team workload and productivity data"""
    
    team_members = ['John Doe', 'Jane Smith', 'Bob Wilson', 'Alice Brown', 'Charlie Davis',
                   'Eva Martinez', 'Frank Lee', 'Grace Wang', 'Henry Taylor', 'Ivy Chen',
                   'Jack Anderson', 'Kate Moore', 'Leo Garcia', 'Mia Johnson', 'Noah Kim']
    
    task_types = ['Construction', 'Planning', 'Quality Control', 'Documentation', 
                 'Coordination', 'Safety Inspection', 'Material Handling']
    
    workload = []
    
    for i in range(num_entries):
        project_id = np.random.choice(projects_df['project_id'])
        
        # Generate date within project timeline
        project_start = datetime.strptime(
            projects_df[projects_df['project_id'] == project_id]['start_date'].iloc[0], 
            '%Y-%m-%d'
        )
        random_days = np.random.randint(0, 120)
        work_date = project_start + timedelta(days=random_days)
        
        # Realistic working hours (higher on weekdays)
        if work_date.weekday() < 5:  # Weekday
            hours_worked = np.random.normal(8, 1.5)
        else:  # Weekend
            hours_worked = np.random.normal(4, 2)
        
        hours_worked = max(0, min(12, hours_worked))  # Cap at 12 hours
        
        # Productivity score correlates with hours worked but has variance
        base_productivity = min(1.0, hours_worked / 8)
        productivity_score = max(0.3, min(1.0, base_productivity + np.random.normal(0, 0.15)))
        
        workload.append({
            'date': work_date.strftime('%Y-%m-%d'),
            'project_id': project_id,
            'team_member': np.random.choice(team_members),
            'hours_worked': round(hours_worked, 1),
            'task_type': np.random.choice(task_types),
            'productivity_score': round(productivity_score, 2),
            'overtime_hours': max(0, round(hours_worked - 8, 1)),
            'efficiency_rating': np.random.choice(['Excellent', 'Good', 'Average', 'Needs Improvement'], 
                                                p=[0.2, 0.5, 0.25, 0.05])
        })
    
    return pd.DataFrame(workload)

def generate_budget_variance_data(projects_df):
    """Generate budget tracking over time"""
    
    budget_data = []
    
    for _, project in projects_df.iterrows():
        start_date = datetime.strptime(project['start_date'], '%Y-%m-%d')
        current_date = start_date
        cumulative_spent = 0
        
        # Generate monthly budget tracking
        while current_date <= datetime.now() and current_date <= datetime.strptime(project['end_date'], '%Y-%m-%d'):
            # Monthly spending based on project progress
            monthly_budget = project['budget_allocated'] / 12  # Assume 12 month projects on average
            
            # Add variance to monthly spending
            variance_factor = np.random.uniform(0.7, 1.3)
            monthly_spent = monthly_budget * variance_factor
            cumulative_spent += monthly_spent
            
            # Don't exceed total project budget by too much
            if cumulative_spent > project['budget_allocated'] * 1.1:
                monthly_spent = max(0, project['budget_allocated'] * 1.1 - (cumulative_spent - monthly_spent))
                cumulative_spent = project['budget_allocated'] * 1.1
            
            budget_data.append({
                'project_id': project['project_id'],
                'date': current_date.strftime('%Y-%m-%d'),
                'planned_budget': round(monthly_budget, 2),
                'actual_spent': round(monthly_spent, 2),
                'cumulative_planned': round((current_date - start_date).days / 365 * project['budget_allocated'], 2),
                'cumulative_actual': round(cumulative_spent, 2),
                'variance_percentage': round(((cumulative_spent - (current_date - start_date).days / 365 * project['budget_allocated']) / project['budget_allocated']) * 100, 2)
            })
            
            current_date += timedelta(days=30)  # Monthly updates
    
    return pd.DataFrame(budget_data)

def generate_project_stages_data(projects_df):
    """Generate project milestone/stage tracking"""
    
    stages = ['Initiation', 'Planning', 'Design', 'Procurement', 'Construction', 'Testing', 'Handover']
    
    stages_data = []
    
    for _, project in projects_df.iterrows():
        start_date = datetime.strptime(project['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(project['end_date'], '%Y-%m-%d')
        total_duration = (end_date - start_date).days
        
        stage_duration = total_duration / len(stages)
        
        for i, stage in enumerate(stages):
            stage_start = start_date + timedelta(days=int(i * stage_duration))
            stage_end = start_date + timedelta(days=int((i + 1) * stage_duration))
            
            # Calculate stage completion based on overall project progress
            stage_progress = max(0, min(100, 
                (project['completion_percentage'] - i * (100/len(stages))) / (100/len(stages)) * 100
            ))
            
            stages_data.append({
                'project_id': project['project_id'],
                'stage_name': stage,
                'stage_order': i + 1,
                'planned_start': stage_start.strftime('%Y-%m-%d'),
                'planned_end': stage_end.strftime('%Y-%m-%d'),
                'actual_start': stage_start.strftime('%Y-%m-%d') if stage_progress > 0 else None,
                'completion_percentage': round(stage_progress, 1),
                'status': 'Completed' if stage_progress >= 100 else 'In Progress' if stage_progress > 0 else 'Not Started',
                'milestone_met': np.random.choice([True, False], p=[0.8, 0.2]) if stage_progress > 50 else False
            })
    
    return pd.DataFrame(stages_data)

def generate_project_status_data(projects_df, days_back=90):
    """Generate daily project status updates"""
    
    status_data = []
    
    for _, project in projects_df.iterrows():
        start_date = datetime.strptime(project['start_date'], '%Y-%m-%d')
        current_date = max(start_date, datetime.now() - timedelta(days=days_back))
        
        while current_date <= datetime.now():
            # Skip weekends for status updates
            if current_date.weekday() < 5:
                # Calculate daily progress
                days_since_start = (current_date - start_date).days
                project_duration = (datetime.strptime(project['end_date'], '%Y-%m-%d') - start_date).days
                
                expected_progress = min(100, (days_since_start / project_duration) * 100)
                actual_progress = expected_progress + np.random.normal(0, 5)
                actual_progress = max(0, min(100, actual_progress))
                
                # Risk assessment
                if actual_progress < expected_progress - 10:
                    risk_level = 'High'
                elif actual_progress < expected_progress - 5:
                    risk_level = 'Medium'
                else:
                    risk_level = 'Low'
                
                status_data.append({
                    'project_id': project['project_id'],
                    'date': current_date.strftime('%Y-%m-%d'),
                    'expected_progress': round(expected_progress, 1),
                    'actual_progress': round(actual_progress, 1),
                    'progress_variance': round(actual_progress - expected_progress, 1),
                    'risk_level': risk_level,
                    'team_size_today': project['team_size'] + np.random.randint(-2, 3),
                    'weather_impact': np.random.choice(['None', 'Minor', 'Moderate', 'Severe'], p=[0.7, 0.2, 0.08, 0.02]),
                    'quality_score': round(np.random.uniform(0.7, 1.0), 2)
                })
            
            current_date += timedelta(days=1)
    
    return pd.DataFrame(status_data)

def main():
    """Main function to generate all datasets"""
    
    print("🏗️ Construction Dashboard Data Generation")
    print("=" * 50)
    
    # Create data directory
    data_dir = create_data_directory()
    print(f"📁 Data directory: {data_dir}")
    
    # Generate main projects dataset
    print("📊 Generating projects master data...")
    projects_df = generate_projects_master()
    projects_df.to_csv(f'{data_dir}/projects_master.csv', index=False)
    print(f"   ✅ Generated {len(projects_df)} projects")
    
    # Generate resources data
    print("🔧 Generating resources data...")
    resources_df = generate_resources_data(projects_df)
    resources_df.to_csv(f'{data_dir}/resources.csv', index=False)
    print(f"   ✅ Generated {len(resources_df)} resource entries")
    
    # Generate workload data
    print("👥 Generating workload data...")
    workload_df = generate_workload_data(projects_df)
    workload_df.to_csv(f'{data_dir}/workload.csv', index=False)
    print(f"   ✅ Generated {len(workload_df)} workload entries")
    
    # Generate budget variance data
    print("💰 Generating budget variance data...")
    budget_df = generate_budget_variance_data(projects_df)
    budget_df.to_csv(f'{data_dir}/budget_variance.csv', index=False)
    print(f"   ✅ Generated {len(budget_df)} budget tracking entries")
    
    # Generate project stages data
    print("📈 Generating project stages data...")
    stages_df = generate_project_stages_data(projects_df)
    stages_df.to_csv(f'{data_dir}/project_stages.csv', index=False)
    print(f"   ✅ Generated {len(stages_df)} project stage entries")
    
    # Generate project status data
    print("📋 Generating project status data...")
    status_df = generate_project_status_data(projects_df)
    status_df.to_csv(f'{data_dir}/project_status.csv', index=False)
    print(f"   ✅ Generated {len(status_df)} daily status entries")
    
    # Summary
    print("\n📈 Data Generation Summary:")
    print(f"   • Projects: {len(projects_df)}")
    print(f"   • Resources: {len(resources_df)}")
    print(f"   • Workload entries: {len(workload_df)}")
    print(f"   • Budget tracking: {len(budget_df)}")
    print(f"   • Project stages: {len(stages_df)}")
    print(f"   • Status updates: {len(status_df)}")
    print(f"   • Total data points: {len(projects_df) + len(resources_df) + len(workload_df) + len(budget_df) + len(stages_df) + len(status_df)}")
    
    print("\n✅ Data generation completed successfully!")
    print("📁 All CSV files saved to ../data/ directory")
    
    # Display sample data
    print("\n📊 Sample Projects Data:")
    print(projects_df.head(3).to_string())

if __name__ == "__main__":
    main()