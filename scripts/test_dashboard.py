import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.H1("🚀 Test Dashboard", className="text-center mb-4"),
    html.P("Se você vê esta mensagem, o dashboard está funcionando!", className="text-center"),
    dbc.Alert("Dashboard carregado com sucesso!", color="success")
])

if __name__ == '__main__':
    print("🚀 Starting test dashboard...")
    print("📍 Access: http://localhost:8050")
    app.run_server(debug=True, host='0.0.0.0', port=8050)
