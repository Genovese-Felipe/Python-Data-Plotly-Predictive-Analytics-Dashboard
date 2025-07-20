import dash
from dash import dcc, html
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from components.dashboard_layout import create_layout

app = dash.Dash(__name__)
server = app.server

app.layout = create_layout()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)

