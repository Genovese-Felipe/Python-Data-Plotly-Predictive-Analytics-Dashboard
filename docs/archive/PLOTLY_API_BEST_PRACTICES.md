# 🛡️ Plotly/Dash API Best Practices & Error Prevention Guide

## 🚨 Common API Errors and Their Fixes

### ❌ **Error: `'Figure' object has no attribute 'update_xaxis'`**

**Problem:** Using singular form instead of plural form for axis updates.

```python
# ❌ WRONG - Will cause AttributeError
bar_fig.update_xaxis(tickangle=45)
bar_fig.update_yaxis(title="Values")

# ✅ CORRECT - Use plural forms
bar_fig.update_xaxes(tickangle=45)
bar_fig.update_yaxes(title="Values")
```

### ❌ **Error: `'Dash' object has no attribute 'run_server'`**

**Problem:** Using deprecated `run_server` method in newer Dash versions.

```python
# ❌ WRONG - Deprecated in Dash 3.x+
app.run_server(debug=True, host='0.0.0.0', port=8050)

# ✅ CORRECT - Use run method
app.run(debug=True, host='0.0.0.0', port=8050)
```

## 🔧 Prevention Strategies

### 1. **Use Pre-commit Hooks**

Install the validation script as a git hook:

```bash
# Copy the pre-commit script
cp pre_commit_plotly_check.py .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

# Now git will automatically check for API errors before commits
git commit -m "Fix dashboard"
```

### 2. **Regular Validation**

Run comprehensive validation regularly:

```bash
# Check all dashboard files
python test_dashboard_validation.py

# Check only for API errors (quick)
python pre_commit_plotly_check.py
```

### 3. **Code Review Checklist**

Before committing any dashboard code, verify:

- [ ] All `update_xaxis` calls changed to `update_xaxes`
- [ ] All `update_yaxis` calls changed to `update_yaxes`
- [ ] All `run_server` calls changed to `run`
- [ ] No Streamlit functions used in Dash code
- [ ] All imports are available and correct

### 4. **IDE Configuration**

Configure your IDE to highlight these patterns:

```json
// VS Code settings.json
{
  "editor.codeActionsOnSave": {
    "source.fixAll": true
  },
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true
}
```

## 📖 Reference Documentation

### Plotly Figure API

```python
import plotly.express as px
import plotly.graph_objects as go

# Creating figures
fig = px.bar(df, x='category', y='value')

# ✅ Correct axis updates
fig.update_xaxes(tickangle=45, title="Categories")
fig.update_yaxes(title="Values", range=[0, 100])

# ✅ Layout updates
fig.update_layout(
    title="My Dashboard",
    showlegend=True,
    height=400
)
```

### Dash App Structure

```python
import dash
from dash import dcc, html, Input, Output

# ✅ Correct app initialization
app = dash.Dash(__name__)

# ✅ Layout definition
app.layout = html.Div([
    dcc.Graph(id='my-graph'),
    # ... other components
])

# ✅ Callback definition
@app.callback(
    Output('my-graph', 'figure'),
    Input('my-dropdown', 'value')
)
def update_graph(selected_value):
    # Create and return figure
    return fig

# ✅ Correct app run
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
```

## 🧪 Testing Guidelines

### Unit Testing Dashboard Components

```python
import unittest
from dash.testing.application_runners import import_app

class TestDashboard(unittest.TestCase):
    def setUp(self):
        self.app = import_app('working_dashboard')
    
    def test_app_runs(self):
        """Test that the app starts without errors"""
        # This would be expanded with actual dash.testing
        self.assertIsNotNone(self.app)
    
    def test_no_deprecated_api(self):
        """Test that no deprecated API calls exist"""
        # Run our validation script
        import subprocess
        result = subprocess.run(['python', 'pre_commit_plotly_check.py'], 
                              capture_output=True)
        self.assertEqual(result.returncode, 0)

if __name__ == '__main__':
    unittest.main()
```

## 🔍 Debugging Tips

### 1. **Check Plotly Version Compatibility**

```python
import plotly
import dash

print(f"Plotly version: {plotly.__version__}")
print(f"Dash version: {dash.__version__}")

# Ensure compatibility:
# Plotly >= 5.0.0
# Dash >= 2.0.0
```

### 2. **Validate Figure Objects**

```python
def validate_figure(fig):
    """Validate that a figure is properly constructed"""
    if not hasattr(fig, 'data'):
        raise ValueError("Invalid figure: missing data")
    
    if not hasattr(fig, 'layout'):
        raise ValueError("Invalid figure: missing layout")
    
    return True

# Use in callbacks
@app.callback(Output('graph', 'figure'), Input('dropdown', 'value'))
def update_graph(value):
    fig = create_my_figure(value)
    validate_figure(fig)  # Will catch issues early
    return fig
```

### 3. **Error Logging**

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.callback(Output('graph', 'figure'), Input('dropdown', 'value'))
def update_graph(value):
    try:
        logger.info(f"Updating graph with value: {value}")
        fig = create_figure(value)
        
        # ✅ Use correct API
        fig.update_xaxes(tickangle=45)
        
        logger.info("Graph updated successfully")
        return fig
    
    except Exception as e:
        logger.error(f"Error updating graph: {e}")
        # Return empty figure or error message
        return go.Figure()
```

## 📋 Maintenance Schedule

1. **Weekly:** Run `python test_dashboard_validation.py`
2. **Before releases:** Run full test suite
3. **After Plotly/Dash updates:** Check for new deprecations
4. **Monthly:** Review and update this guide

## 🆘 Troubleshooting Common Issues

| Error | Cause | Solution |
|-------|--------|----------|
| `AttributeError: 'Figure' object has no attribute 'update_xaxis'` | Using singular form | Change to `update_xaxes` |
| `ObsoleteAttributeException: app.run_server has been replaced` | Using deprecated method | Change to `app.run` |
| `ImportError: No module named 'dash_core_components'` | Old import style | Use `from dash import dcc` |
| `CallbackException: callback never fired` | Incorrect component IDs | Check ID matching between layout and callbacks |

---

**💡 Remember:** When in doubt, check the official documentation at [dash.plotly.com](https://dash.plotly.com) and [plotly.com/python](https://plotly.com/python).