"""
A simple test dashboard using the Iris dataset.

This script creates a basic Dash application to display a scatter plot and a
histogram of the Iris dataset. It serves as a simple example or test case for
a Dash dashboard.
"""

import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd

# Load the sample Iris dataset
df = px.data.iris()

app = dash.Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div([
    html.H1("🌸 Iris Dashboard - Test", style={'textAlign': 'center'}),

    html.P(f"Dataset loaded with {len(df)} samples",
           style={'textAlign': 'center', 'fontSize': '18px'}),

    dcc.Graph(
        figure=px.scatter(df, x="sepal_width", y="sepal_length",
                         color="species", title="Sepal Analysis")
    ),

    dcc.Graph(
        figure=px.histogram(df, x="petal_length", color="species",
                           title="Petal Length Distribution")
    )
])

if __name__ == '__main__':
    print("🚀 Starting Dash server...")
    print("📊 Dashboard available at: http://localhost:8050")
    app.run_server(debug=True)