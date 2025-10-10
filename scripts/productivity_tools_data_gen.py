"""
A data generation script for the productivity tools comparison dashboard.

This script creates several CSV files containing synthetic data for a detailed
comparative analysis of productivity tools. The data is based on simulated
research and covers basic info, evaluation criteria, scores, pricing,
use cases, and market analysis.
"""

import pandas as pd
import numpy as np
import os

# Set random seed for reproducible results
np.random.seed(42)


def create_data_folder():
    """
    Ensures that the data directory exists, creating it if necessary.

    Returns:
        str: The path to the data directory.
    """
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    os.makedirs(data_dir, exist_ok=True)
    return data_dir


def generate_tools_basic_info():
    """
    Generates a DataFrame with basic information about each productivity tool.

    Returns:
        pd.DataFrame: A DataFrame containing basic details for each tool.
    """
    tools_data = {
        'tool_name': ['Obsidian', 'Notion', 'Google Keep', 'Roam Research', 'Evernote'],
        'category': ['Knowledge Management', 'All-in-One Workspace', 'Quick Notes', 'Networked Thought', 'Digital Notebook'],
        'founded_year': [2020, 2016, 2013, 2019, 2008],
        'primary_focus': ['Personal Knowledge Management', 'Team Collaboration', 'Quick Capture', 'Research & Analysis', 'Document Organization'],
    }
    return pd.DataFrame(tools_data)


def generate_evaluation_criteria():
    """
    Generates a DataFrame with the evaluation criteria and their weights.

    Returns:
        pd.DataFrame: A DataFrame defining the criteria for the analysis.
    """
    criteria_data = {
        'criteria_id': ['ease_of_use', 'features', 'collaboration', 'performance', 'price_value', 'mobile_experience', 'data_organization'],
        'criteria_name': ['Ease of Use', 'Features', 'Collaboration', 'Performance', 'Price/Value', 'Mobile Experience', 'Data Organization'],
        'weight_percentage': [20, 25, 15, 15, 10, 10, 5],
        'description': [
            'Learning curve, intuitive interface, onboarding, documentation',
            'Available features, flexibility, advanced capabilities, extensibility',
            'Sharing, real-time editing, access control, comments',
            'Speed, synchronization, stability, scalability',
            'Cost-benefit, available plans, free limits, transparency',
            'Native app, mobile features, synchronization, touch usability',
            'Structuring, search, categorization, backup/export'
        ]
    }
    return pd.DataFrame(criteria_data)


def generate_detailed_scores():
    """
    Generates detailed, research-based scores for each tool across all criteria.

    Returns:
        pd.DataFrame: A DataFrame with detailed scores for each tool.
    """
    tool_scores = {
        'Obsidian': {'ease_of_use': 6.2, 'features': 9.1, 'collaboration': 4.3, 'performance': 8.7, 'price_value': 9.5, 'mobile_experience': 7.1, 'data_organization': 9.3},
        'Notion': {'ease_of_use': 7.8, 'features': 9.4, 'collaboration': 9.2, 'performance': 6.8, 'price_value': 7.5, 'mobile_experience': 8.2, 'data_organization': 8.9},
        'Google Keep': {'ease_of_use': 9.3, 'features': 5.2, 'collaboration': 6.7, 'performance': 9.1, 'price_value': 10.0, 'mobile_experience': 9.4, 'data_organization': 4.8},
        'Roam Research': {'ease_of_use': 4.9, 'features': 8.8, 'collaboration': 5.4, 'performance': 6.3, 'price_value': 4.2, 'mobile_experience': 5.8, 'data_organization': 9.6},
        'Evernote': {'ease_of_use': 7.2, 'features': 7.1, 'collaboration': 6.1, 'performance': 6.9, 'price_value': 5.8, 'mobile_experience': 7.8, 'data_organization': 7.4}
    }
    scores_data = []
    criteria_map = generate_evaluation_criteria().set_index('criteria_id')['criteria_name'].to_dict()
    for tool, scores in tool_scores.items():
        for criteria_id, score in scores.items():
            scores_data.append({'tool_name': tool, 'criteria_id': criteria_id, 'criteria_name': criteria_map[criteria_id], 'score': score})
    return pd.DataFrame(scores_data)


def generate_pricing_data():
    """
    Generates a DataFrame with pricing information for each tool.

    Returns:
        pd.DataFrame: A DataFrame containing pricing details.
    """
    pricing_data = {
        'tool_name': ['Obsidian', 'Notion', 'Google Keep', 'Roam Research', 'Evernote'],
        'free_plan': [True, True, True, False, True],
        'basic_plan_price_usd': [0, 8, 0, 15, 7.99],
        'basic_plan_price_brl': [0, 42, 0, 79, 42],
    }
    return pd.DataFrame(pricing_data)


def generate_use_cases_data():
    """
    Generates a DataFrame categorizing use cases for each tool.

    Returns:
        pd.DataFrame: A DataFrame with suitability scores for various use cases.
    """
    use_cases = {
        'Obsidian': [('Advanced', 'Zettelkasten', 9.8), ('Professional', 'Knowledge Base', 9.5)],
        'Notion': [('Cotidiano', 'Personal Planner', 8.8), ('Professional', 'Project Management', 9.3)],
        'Google Keep': [('Cotidiano', 'Quick Notes', 9.7), ('Cotidiano', 'Shopping Lists', 9.5)],
        'Roam Research': [('Advanced', 'Conceptual Analysis', 9.6), ('Professional', 'Qualitative Research', 9.7)],
        'Evernote': [('Cotidiano', 'Web Clipping', 9.4), ('Professional', 'Documentation', 8.5)]
    }
    use_cases_data = []
    for tool, cases in use_cases.items():
        for category, name, score in cases:
            use_cases_data.append({'tool_name': tool, 'use_case_category': category, 'use_case_name': name, 'suitability_score': score})
    return pd.DataFrame(use_cases_data)


def calculate_weighted_scores():
    """
    Calculates the final weighted scores and rankings for each tool.

    Returns:
        pd.DataFrame: A DataFrame with the final weighted scores and rankings.
    """
    criteria_df = generate_evaluation_criteria()
    scores_df = generate_detailed_scores()
    
    weighted_scores = []
    for tool in scores_df['tool_name'].unique():
        tool_scores = scores_df[scores_df['tool_name'] == tool]
        total_weighted_score = 0
        for _, criteria in criteria_df.iterrows():
            score = tool_scores[tool_scores['criteria_id'] == criteria['criteria_id']]['score'].iloc[0]
            total_weighted_score += score * (criteria['weight_percentage'] / 100)
        weighted_scores.append({'tool_name': tool, 'weighted_score': round(total_weighted_score, 2), 'percentage_score': round(total_weighted_score * 10, 1)})
    
    weighted_df = pd.DataFrame(weighted_scores).sort_values('weighted_score', ascending=False)
    weighted_df['ranking'] = range(1, len(weighted_df) + 1)
    return weighted_df


def generate_market_analysis():
    """
    Generates a DataFrame with market analysis and trends data.

    Returns:
        pd.DataFrame: A DataFrame containing market analysis for each tool.
    """
    market_data = {
        'tool_name': ['Obsidian', 'Notion', 'Google Keep', 'Roam Research', 'Evernote'],
        'market_position': ['Niche Specialist', 'Emerging Leader', 'Mainstream', 'Academic Niche', 'Traditional Leader'],
        'future_outlook': ['Very Positive', 'Positive', 'Stable', 'Uncertain', 'Negative']
    }
    return pd.DataFrame(market_data)


def main():
    """
    Main function to generate all data files and save them to the data directory.
    """
    print("🚀 Starting data generation for productivity tools analysis...")
    data_dir = create_data_folder()
    print(f"📁 Data directory: {data_dir}")

    datasets = {
        'tools_basic_info.csv': generate_tools_basic_info(),
        'evaluation_criteria.csv': generate_evaluation_criteria(),
        'detailed_scores.csv': generate_detailed_scores(),
        'pricing_data.csv': generate_pricing_data(),
        'use_cases_data.csv': generate_use_cases_data(),
        'weighted_scores.csv': calculate_weighted_scores(),
        'market_analysis.csv': generate_market_analysis()
    }

    for filename, dataframe in datasets.items():
        filepath = os.path.join(data_dir, filename)
        dataframe.to_csv(filepath, index=False, encoding='utf-8')
        print(f"✅ Saved: {filename} ({len(dataframe)} records)")

    print("\n✨ Data generation completed successfully!")


if __name__ == "__main__":
    main()