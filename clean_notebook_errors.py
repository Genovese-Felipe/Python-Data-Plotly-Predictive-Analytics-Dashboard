#!/usr/bin/env python3
"""
A script to clean up specific error outputs from Jupyter notebooks.

This utility scans specified Jupyter notebook files and removes any output cells
that contain errors related to the deprecated `update_xaxis` method, which helps
in maintaining clean and error-free notebooks in the repository.
"""

import json
import os

def clean_notebook_errors(notebook_path):
    """
    Cleans `update_xaxis` error outputs from a single Jupyter notebook file.

    This function reads a notebook, iterates through its cells, and removes any
    output that contains the specified error text. The cleaned notebook is then
    written back to the original file.

    Args:
        notebook_path (str): The full path to the Jupyter notebook file.

    Returns:
        bool: True if any errors were cleaned, False otherwise.
    """
    print(f"Cleaning errors from {notebook_path}...")
    
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"  Error reading notebook: {e}")
        return False

    cleaned_cells_count = 0
    
    for cell in notebook.get('cells', []):
        if cell.get('cell_type') == 'code' and 'outputs' in cell:
            original_output_count = len(cell['outputs'])
            # Filter out outputs containing the specific error message
            cell['outputs'] = [
                output for output in cell['outputs']
                if 'update_xaxis' not in str(output.get('traceback', []))
            ]
            
            if len(cell['outputs']) < original_output_count:
                cleaned_cells_count += 1
                print(f"  Removed {original_output_count - len(cell['outputs'])} error outputs from a cell.")
    
    # Write the cleaned content back to the file
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)
    
    if cleaned_cells_count > 0:
        print(f"  Cleaned {cleaned_cells_count} cells in {notebook_path}.")
        return True
    return False

def main():
    """
    Main function to orchestrate the cleanup of specified notebooks.

    This function defines a list of notebooks to be cleaned, iterates through them,
    and calls the `clean_notebook_errors` function for each one. It provides a
    summary of the cleanup process.
    """
    repo_root = os.path.dirname(os.path.abspath(__file__))
    notebooks_to_clean = [
        'Dashboard_Working.ipynb',
        'versao_finalizada_almost_there/Dashboard_Working.ipynb'
    ]
    
    total_cleaned_notebooks = 0
    for notebook_name in notebooks_to_clean:
        notebook_path = os.path.join(repo_root, notebook_name)
        if os.path.exists(notebook_path):
            if clean_notebook_errors(notebook_path):
                total_cleaned_notebooks += 1
        else:
            print(f"Notebook not found: {notebook_path}")
    
    print(f"\n✅ Cleaned {total_cleaned_notebooks} notebooks.")

if __name__ == '__main__':
    main()