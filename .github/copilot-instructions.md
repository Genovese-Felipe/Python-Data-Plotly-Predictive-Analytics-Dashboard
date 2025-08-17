# Python Data Plotly Predictive Analytics Dashboard
Professional construction project management dashboard built with Python, Plotly, and Dash. Features interactive visualizations, real-time analytics, and automated GitHub Pages deployment.

**ALWAYS follow these instructions exactly. Only fallback to additional search and context gathering if the information in these instructions is incomplete or found to be in error.**

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively
- Bootstrap, build, and test the repository:
  - `python --version` -- verify Python 3.8+ is installed
  - `pip install pandas numpy plotly dash dash-bootstrap-components` -- takes 40 seconds. NEVER CANCEL. Set timeout to 60+ minutes.
  - `cd AI_Dashboard_Implementation/scripts` -- ALWAYS use this directory for main functionality
  - `python data_gen.py` -- generates construction project data, takes 3 seconds
  - `python viz.py` -- creates dashboard, takes 5 seconds. Choose option 2 for HTML export.
- Full test suite:
  - `python validate_monica_ai.py` -- validates system integration, takes 10 seconds
  - `python test_dashboard_validation.py` -- comprehensive dashboard validation, takes 60 seconds. NEVER CANCEL. Set timeout to 90+ minutes.
- Run the interactive dashboard:
  - ALWAYS run the bootstrapping steps first.
  - `cd AI_Dashboard_Implementation/scripts && python viz.py` -- choose option 1 for server mode
  - Dashboard available at: http://localhost:8050
  - Debug mode: Enabled by default

## Validation
- Always manually validate any new code by generating data and testing dashboard export.
- ALWAYS run through at least one complete end-to-end scenario after making changes:
  1. Generate fresh data: `python data_gen.py`
  2. Export dashboard: `python viz.py` (option 2)
  3. Verify HTML file created in `../outputs/dashboard.html`
  4. Test interactive mode: `python viz.py` (option 1) and access http://localhost:8050
- You can build and run the application locally, and the dashboard works in browser preview.
- Always run `python validate_monica_ai.py` and `python test_dashboard_validation.py` before you are done or the CI (.github/workflows/pages.yml) will fail.

## Common tasks
The following are outputs from frequently run commands. Reference them instead of viewing, searching, or running bash commands to save time.

### Repo root
ls -a [repo-root]
.
..
.git
.github
.gitignore
AI_Dashboard_Implementation
AI_Knowledge_Extraction_System
Monica_AI_System
README.md
requirements.txt
requirements_processing.txt
scripts
outputs
data
docs

### Primary working directory
cd AI_Dashboard_Implementation
ls -la
data/
guides/
outputs/
scripts/

### Data generation output
cd AI_Dashboard_Implementation/scripts && python data_gen.py
🏗️ Construction Dashboard Data Generation
📊 Generating projects master data... ✅ Generated 25 projects
🔧 Generating resources data... ✅ Generated 200 resource entries
👥 Generating workload data... ✅ Generated 300 workload entries
💰 Generating budget variance data... ✅ Generated 183 budget tracking entries
📈 Generating project stages data... ✅ Generated 175 project stage entries
📋 Generating project status data... ✅ Generated 1625 daily status entries
✅ Data generation completed successfully!

### Dashboard export output
python viz.py (option 2)
🏗️ Construction Project Management Dashboard
✅ All data files loaded successfully
✅ Dashboard exported to ../outputs/dashboard.html

### pip install requirements.txt
pip install pandas numpy plotly dash dash-bootstrap-components
Installing packages... (takes 40 seconds)
Successfully installed dash-3.2.0 plotly-6.3.0 pandas-2.3.1 numpy-2.3.2 dash-bootstrap-components-2.0.3

## Build and Deployment Timing
- **CRITICAL**: Set appropriate timeouts for all commands. DO NOT use default timeouts.
- **NEVER CANCEL BUILDS OR LONG-RUNNING COMMANDS**.
- Dependencies installation: Takes 40 seconds. NEVER CANCEL. Set timeout to 120+ seconds.
- Data generation: Takes 3 seconds. Safe with default timeout.
- Dashboard creation: Takes 5 seconds. Safe with default timeout.
- Full validation suite: Takes 60 seconds. NEVER CANCEL. Set timeout to 90+ minutes.
- GitHub Actions deployment: Takes 2-3 minutes. NEVER CANCEL. Automatic timeout handling.

## Repository Structure Overview
- **AI_Dashboard_Implementation/**: Main working directory with functional dashboard
  - `scripts/data_gen.py`: Generates realistic construction project data (2508 data points)
  - `scripts/viz.py`: Creates interactive Dash dashboard with HTML export
  - `data/`: Generated CSV files (projects_master.csv, resources.csv, etc.)
  - `outputs/`: Generated dashboard.html file for GitHub Pages
- **scripts/**: Legacy dashboard implementations (some have syntax errors)
- **Monica_AI_System/**: AI-powered knowledge processing system
- **docs/**: Documentation and archived project files
- **.github/workflows/pages.yml**: Automated GitHub Pages deployment

## Key Validation Commands
```bash
# Comprehensive system validation
python validate_monica_ai.py        # 10 seconds
python test_dashboard_validation.py # 60 seconds - NEVER CANCEL

# Quick validation workflow
cd AI_Dashboard_Implementation/scripts
python data_gen.py                  # 3 seconds
python viz.py                       # 5 seconds, choose option 2
ls -la ../outputs/dashboard.html    # Verify file exists
```

## Dependency Requirements
```python
# Core requirements (install time: 40 seconds)
pandas>=2.3.1
numpy>=2.3.2  
plotly>=6.3.0
dash>=3.2.0
dash-bootstrap-components>=2.0.3

# Additional for full functionality (install time: 10 seconds)
scikit-learn>=1.7.1
scipy>=1.16.1
```

## Development Environment Setup
1. **Python Version**: Requires Python 3.8+ (tested with 3.12.3)
2. **Package Manager**: Uses pip (tested with 24.0)
3. **Virtual Environment**: Recommended but not required
4. **Operating System**: Linux/Ubuntu (GitHub Actions), Windows/macOS supported locally

## Troubleshooting Common Issues
- **Missing outputs directory**: Run `mkdir -p AI_Dashboard_Implementation/outputs`
- **Import errors**: Install missing packages with `pip install [package]`
- **Deprecated API warnings**: Use AI_Dashboard_Implementation scripts (newer versions)
- **Server connection errors**: Check port 8050 availability for interactive mode

## GitHub Pages Deployment
- **Automatic**: Deploys on push to main branch when files in data/, scripts/, outputs/, docs/ change
- **Manual**: Use workflow_dispatch trigger in GitHub Actions
- **Access**: Live site at https://genovese-felipe.github.io/Python-Data-Plotly-Predictive-Analytics-Dashboard/
- **Assets**: Dashboard files copied to docs/assets/dashboards/

## Performance Optimization Notes
- Data generation creates 2508 data points across 6 datasets
- Dashboard HTML output size: ~69KB (compressed interactive format)
- Interactive mode supports real-time updates and filtering
- GitHub Pages deployment includes automatic Jekyll build process