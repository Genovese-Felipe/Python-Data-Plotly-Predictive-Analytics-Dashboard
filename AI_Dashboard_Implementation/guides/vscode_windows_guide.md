# VS Code Windows PC Implementation Guide
# Professional Dashboard Development with GitHub Copilot

## 🖥️ Windows PC Setup Instructions

### 1. Prerequisites Installation

#### Install Python
```batch
# Download Python from python.org (3.8 or higher)
# During installation, check "Add Python to PATH"
# Verify installation in Command Prompt:
python --version
pip --version
```

#### Install Git for Windows
```batch
# Download from git-scm.com
# Use default settings during installation
# Verify in Command Prompt:
git --version
```

#### Install VS Code
```batch
# Download from code.visualstudio.com
# Install with default settings
# Launch VS Code
```

### 2. VS Code Extensions Setup

#### Essential Extensions
```json
{
  "recommendations": [
    "ms-python.python",
    "GitHub.copilot",
    "GitHub.copilot-chat",
    "ms-python.vscode-pylance",
    "ms-toolsai.jupyter",
    "ms-vscode.vscode-json",
    "bradlc.vscode-tailwindcss",
    "formulahendry.auto-rename-tag"
  ]
}
```

#### Install via Command Palette (Ctrl+Shift+P)
```
ext install ms-python.python
ext install GitHub.copilot
ext install GitHub.copilot-chat
ext install ms-python.vscode-pylance
ext install ms-toolsai.jupyter
```

### 3. Project Setup

#### Clone Repository
```batch
# Open Command Prompt or PowerShell
# Navigate to desired directory
cd C:\Development

# Clone repository
git clone https://github.com/your-username/Python-Data-Plotly-Predictive-Analytics-Dashboard.git
cd Python-Data-Plotly-Predictive-Analytics-Dashboard
```

#### Open in VS Code
```batch
# From project directory
code .

# Or open VS Code first, then:
# File > Open Folder > Select project directory
```

### 4. Python Environment Setup

#### Create Virtual Environment
```batch
# In VS Code Terminal (Ctrl+`)
python -m venv dashboard_env

# Activate virtual environment
# PowerShell:
dashboard_env\Scripts\Activate.ps1

# Command Prompt:
dashboard_env\Scripts\activate.bat

# Verify activation (should show (dashboard_env) in prompt)
```

#### Install Dependencies
```batch
# With virtual environment activated
pip install --upgrade pip
pip install dash plotly pandas numpy

# Verify installations
python -c "import dash, plotly, pandas, numpy; print('✅ All libraries installed')"
```

### 5. VS Code Configuration

#### Create .vscode/settings.json
```json
{
    "python.defaultInterpreterPath": "./dashboard_env/Scripts/python.exe",
    "python.terminal.activateEnvironment": true,
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "python.formatting.blackArgs": ["--line-length", "100"],
    "files.autoSave": "afterDelay",
    "files.autoSaveDelay": 1000,
    "github.copilot.enable": {
        "*": true,
        "python": true,
        "markdown": true
    }
}
```

#### Create .vscode/launch.json for Debugging
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Run Dashboard",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}\\AI_Dashboard_Implementation\\scripts\\viz.py",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}\\AI_Dashboard_Implementation\\scripts"
        },
        {
            "name": "Generate Data",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}\\AI_Dashboard_Implementation\\scripts\\data_gen.py",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}\\AI_Dashboard_Implementation\\scripts"
        }
    ]
}
```

### 6. Development Workflow

#### Generate Data
```batch
# Navigate to scripts directory
cd AI_Dashboard_Implementation\scripts

# Run data generation
python data_gen.py
```

#### Develop Dashboard
```batch
# Open viz.py in VS Code
# Use Copilot for code assistance
# Run dashboard
python viz.py

# Access at http://localhost:8050
```

#### Using GitHub Copilot

##### Copilot Shortcuts
```
Ctrl+I          - Inline chat
Ctrl+Shift+I    - Copilot chat panel
Tab             - Accept suggestion
Ctrl+→          - Accept word
Alt+]           - Next suggestion
Alt+[           - Previous suggestion
```

##### Effective Copilot Prompts
```python
# Comment-based prompts for Copilot
# "Create a bar chart showing budget vs actual spending"
# "Add filter dropdown for project managers"
# "Implement responsive design for mobile devices"
# "Create KPI card component with gradient background"
```

### 7. Debugging and Testing

#### Debug Configuration
```python
# Use VS Code debugger
# Set breakpoints by clicking left margin
# Press F5 to start debugging
# Use F10 (step over), F11 (step into), F12 (step out)

# Example debug session:
if __name__ == "__main__":
    print("🐛 Debug: Starting dashboard...")
    dashboard = ConstructionDashboard()  # Set breakpoint here
    dashboard.run_server(debug=True)
```

#### Testing Scripts
```batch
# Test data generation
python -m pytest tests/ -v

# Test dashboard components
python -c "from viz import ConstructionDashboard; d = ConstructionDashboard(); print('✅ Dashboard initialized')"
```

### 8. Git Integration

#### Configure Git
```batch
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

#### VS Code Git Workflow
```
1. Use Source Control panel (Ctrl+Shift+G)
2. Stage changes by clicking +
3. Write commit message
4. Commit with Ctrl+Enter
5. Push with ... menu > Push
```

#### Branch Management
```batch
# Create feature branch
git checkout -b feature/new-chart-type

# Make changes, commit
git add .
git commit -m "add: new resource allocation chart"

# Push branch
git push origin feature/new-chart-type

# Create pull request on GitHub
```

### 9. Performance Optimization

#### Windows-Specific Optimizations
```python
# Add to beginning of viz.py for Windows performance
import os
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Use multiprocessing for data processing
import multiprocessing
multiprocessing.set_start_method('spawn', force=True)
```

#### Memory Management
```python
# Monitor memory usage
import psutil
print(f"Memory usage: {psutil.virtual_memory().percent}%")

# Optimize pandas operations
pd.options.mode.chained_assignment = None  # Disable warnings
```

### 10. Deployment Preparation

#### Create Requirements File
```batch
# Generate requirements.txt
pip freeze > requirements.txt

# Or create manually:
echo dash==3.2.0 > requirements.txt
echo plotly==6.2.0 >> requirements.txt
echo pandas==2.3.1 >> requirements.txt
echo numpy==2.3.2 >> requirements.txt
```

#### Build Distribution
```batch
# Create distribution package
mkdir dist
copy AI_Dashboard_Implementation\outputs\dashboard.html dist\
copy AI_Dashboard_Implementation\data\*.csv dist\data\
```

### 11. Advanced VS Code Features

#### Jupyter Notebook Integration
```python
# Create .ipynb files for data exploration
# Use #%% to create cells in .py files
# Run cells with Shift+Enter

#%% Data Analysis Cell
import pandas as pd
df = pd.read_csv('data/projects_master.csv')
df.head()

#%% Visualization Cell
import plotly.express as px
fig = px.bar(df, x='project_type', y='budget_allocated')
fig.show()
```

#### Code Snippets
```json
// Create .vscode/snippets.json
{
    "Dash App Structure": {
        "prefix": "dash-app",
        "body": [
            "app = dash.Dash(__name__)",
            "",
            "app.layout = html.Div([",
            "    $1",
            "])",
            "",
            "@app.callback(",
            "    Output('$2', 'figure'),",
            "    Input('$3', 'value')",
            ")",
            "def update_$4($5):",
            "    $6",
            "    return fig",
            "",
            "if __name__ == '__main__':",
            "    app.run_server(debug=True)"
        ]
    }
}
```

### 12. File Structure Management

#### Recommended Windows File Structure
```
C:\Development\Python-Data-Plotly-Predictive-Analytics-Dashboard\
├── AI_Dashboard_Implementation\
│   ├── scripts\
│   │   ├── data_gen.py
│   │   └── viz.py
│   ├── data\
│   │   ├── projects_master.csv
│   │   ├── resources.csv
│   │   └── ...
│   ├── outputs\
│   │   └── dashboard.html
│   └── guides\
├── .vscode\
│   ├── settings.json
│   ├── launch.json
│   └── tasks.json
├── dashboard_env\          # Virtual environment
├── requirements.txt
└── README.md
```

### 13. Troubleshooting Windows Issues

#### Common Problems and Solutions

##### Path Issues
```batch
# If Python not found
set PATH=%PATH%;C:\Python39\;C:\Python39\Scripts\

# Use forward slashes in Python
import os
data_path = os.path.join('..', 'data', 'file.csv')
```

##### Permission Issues
```batch
# Run VS Code as Administrator if needed
# Right-click VS Code > Run as administrator

# Or change file permissions
icacls "C:\Development" /grant Users:F /t
```

##### Port Conflicts
```python
# Use different port if 8050 is busy
app.run_server(debug=True, port=8051)

# Or kill existing processes
taskkill /f /im python.exe
```

### 14. Backup and Sync

#### OneDrive Integration
```batch
# Move project to OneDrive for backup
move C:\Development\Dashboard C:\Users\%USERNAME%\OneDrive\Development\

# Create symbolic link
mklink /D C:\Development\Dashboard C:\Users\%USERNAME%\OneDrive\Development\Dashboard
```

#### GitHub Sync
```batch
# Auto-sync with GitHub
git config --global push.autoSetupRemote true

# Use VS Code auto-sync
# File > Preferences > Settings > Git: Auto Fetch > true
```

## ✅ Windows Development Checklist

- [ ] Python installed and in PATH
- [ ] Git installed and configured
- [ ] VS Code with extensions installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed
- [ ] Project opened in VS Code
- [ ] GitHub Copilot configured
- [ ] Data generation script runs
- [ ] Dashboard visualization works
- [ ] Debugging configuration set up
- [ ] Git repository connected
- [ ] HTML export successful

## 🚀 Next Steps for Windows Development

1. **Configure auto-deployment** to GitHub Pages
2. **Set up automated testing** with pytest
3. **Create batch scripts** for common tasks
4. **Implement CI/CD pipeline** with GitHub Actions
5. **Add desktop application** with tkinter
6. **Create installer** with PyInstaller

---

**💡 Windows-Specific Pro Tips:**
- Use PowerShell for better terminal experience
- Enable Windows Subsystem for Linux (WSL) for Unix commands
- Use Windows Terminal for better development experience
- Configure Windows Defender exclusions for development folders
- Use VSCode Remote-WSL for hybrid development