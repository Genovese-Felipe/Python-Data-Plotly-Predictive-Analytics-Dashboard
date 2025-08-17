#!/usr/bin/env python3
"""
Notebook Error Cleanup Script

This script removes error outputs from Jupyter notebooks that contain
the old update_xaxis errors.
"""

import json
import re
import os

def clean_notebook_errors(notebook_path):
    """Clean error outputs from a Jupyter notebook"""
    print(f"Cleaning errors from {notebook_path}...")
    
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    cleaned_cells = 0
    
    for cell in notebook.get('cells', []):
        if cell.get('cell_type') == 'code' and 'outputs' in cell:
            # Filter out outputs that contain the old API errors
            original_count = len(cell['outputs'])
            cell['outputs'] = [
                output for output in cell['outputs']
                if not any(
                    'update_xaxis' in str(output.get('text', '')) or
                    'update_xaxis' in str(output.get('traceback', []))
                    for text_part in output.get('text', [])
                )
            ]
            
            new_count = len(cell['outputs'])
            if new_count < original_count:
                cleaned_cells += 1
                print(f"  Removed {original_count - new_count} error outputs from a cell")
    
    # Write back the cleaned notebook
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)
    
    print(f"  Cleaned {cleaned_cells} cells in {notebook_path}")
    return cleaned_cells > 0

def main():
    """Main cleanup function"""
    repo_root = os.path.dirname(os.path.abspath(__file__))
    notebooks = [
        'Dashboard_Working.ipynb',
        'versao_finalizada_almost_there/Dashboard_Working.ipynb'
    ]
    
    total_cleaned = 0
    for notebook in notebooks:
        notebook_path = os.path.join(repo_root, notebook)
        if os.path.exists(notebook_path):
            if clean_notebook_errors(notebook_path):
                total_cleaned += 1
        else:
            print(f"Notebook not found: {notebook_path}")
    
    print(f"\n✅ Cleaned {total_cleaned} notebooks")

if __name__ == '__main__':
    main()