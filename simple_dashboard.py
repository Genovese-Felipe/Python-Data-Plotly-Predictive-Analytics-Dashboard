"""
A simple sales dashboard built with Plotly and Dash.

This script creates an interactive dashboard for visualizing sales data.
It includes Key Performance Indicators (KPIs), filters for product and region,
and several charts that update dynamically based on user selections.
"""
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Generate sample data
np.random.seed(42)
n_samples = 1000

# Sales dataset
dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
sales_data = []

for i, date in enumerate(dates):
    daily_sales = np.random.poisson(50) + np.sin(i/30) * 10 + np.random.normal(0, 5)
    sales_data.append({
        'date': date,
        'sales': max(0, daily_sales),
        'product': np.random.choice(['Product A', 'Product B', 'Product C']),
        'region': np.random.choice(['North', 'South', 'East', 'West']),
        'seller': np.random.choice(['John', 'Maria', 'Peter', 'Ana', 'Carlos'])
    })

df = pd.DataFrame(sales_data)

# Create Dash application
app = dash.Dash(__name__)

# Application layout
app.layout = html.Div([
    html.H1("📊 Sales Dashboard - Python Analytics",
            style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': 30}),

    # KPI cards
    html.Div([
        html.Div([
            html.H3(f"{df['sales'].sum():,.0f}", style={'color': '#e74c3c', 'margin': 0}),
            html.P("Total Sales", style={'margin': 0})
        ], className="kpi-card", style={
            'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px',
            'boxShadow': '0 4px 6px rgba(0,0,0,0.1)', 'textAlign': 'center',
            'width': '23%', 'display': 'inline-block', 'margin': '1%'
        }),

        html.Div([
            html.H3(f"{df['date'].dt.year.nunique()}", style={'color': '#3498db', 'margin': 0}),
            html.P("Year of Data", style={'margin': 0})
        ], style={
            'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px',
            'boxShadow': '0 4px 6px rgba(0,0,0,0.1)', 'textAlign': 'center',
            'width': '23%', 'display': 'inline-block', 'margin': '1%'
        }),

        html.Div([
            html.H3(f"{df['seller'].nunique()}", style={'color': '#2ecc71', 'margin': 0}),
            html.P("Sellers", style={'margin': 0})
        ], style={
            'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px',
            'boxShadow': '0 4px 6px rgba(0,0,0,0.1)', 'textAlign': 'center',
            'width': '23%', 'display': 'inline-block', 'margin': '1%'
        }),

        html.Div([
            html.H3(f"{df['sales'].mean():.1f}", style={'color': '#f39c12', 'margin': 0}),
            html.P("Daily Average", style={'margin': 0})
        ], style={
            'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px',
            'boxShadow': '0 4px 6px rgba(0,0,0,0.1)', 'textAlign': 'center',
            'width': '23%', 'display': 'inline-block', 'margin': '1%'
        })
    ], style={'marginBottom': '30px'}),

    # Filters
    html.Div([
        html.Div([
            html.Label("Select Product:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='product-dropdown',
                options=[{'label': 'All', 'value': 'all'}] +
                        [{'label': prod, 'value': prod} for prod in df['product'].unique()],
                value='all',
                style={'marginBottom': '20px'}
            )
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            html.Label("Select Region:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='region-dropdown',
                options=[{'label': 'All', 'value': 'all'}] +
                        [{'label': reg, 'value': reg} for reg in df['region'].unique()],
                value='all'
            )
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ], style={'marginBottom': '30px'}),

    # Charts
    html.Div([
        html.Div([
            dcc.Graph(id='sales-time')
        ], style={'width': '50%', 'display': 'inline-block'}),

        html.Div([
            dcc.Graph(id='sales-product')
        ], style={'width': '50%', 'float': 'right', 'display': 'inline-block'})
    ]),

    html.Div([
        html.Div([
            dcc.Graph(id='sales-region')
        ], style={'width': '50%', 'display': 'inline-block'}),

        html.Div([
            dcc.Graph(id='sales-seller')
        ], style={'width': '50%', 'float': 'right', 'display': 'inline-block'})
    ])

], style={'padding': '20px', 'backgroundColor': '#ecf0f1'})


@app.callback(
    [Output('sales-time', 'figure'),
     Output('sales-product', 'figure'),
     Output('sales-region', 'figure'),
     Output('sales-seller', 'figure')],
    [Input('product-dropdown', 'value'),
     Input('region-dropdown', 'value')]
)
def update_graphs(selected_product, selected_region):
    """
    Update the dashboard graphs based on user-selected filters.

    This function is triggered when the user selects a product or region from the
    dropdown menus. It filters the data and regenerates the charts.

    Args:
        selected_product (str): The product selected by the user.
        selected_region (str): The region selected by the user.

    Returns:
        tuple: A tuple containing the updated figures for all charts.
    """
    filtered_df = df.copy()

    if selected_product != 'all':
        filtered_df = filtered_df[filtered_df['product'] == selected_product]

    if selected_region != 'all':
        filtered_df = filtered_df[filtered_df['region'] == selected_region]

    # Sales over time chart
    sales_time = filtered_df.groupby('date')['sales'].sum().reset_index()
    fig_time = px.line(sales_time, x='date', y='sales',
                       title='📈 Sales Over Time',
                       labels={'sales': 'Sales', 'date': 'Date'})
    fig_time.update_traces(line_color='#e74c3c')
    fig_time.update_layout(plot_bgcolor='white')

    # Sales by product chart
    sales_product = filtered_df.groupby('product')['sales'].sum().reset_index()
    fig_product = px.bar(sales_product, x='product', y='sales',
                         title='🛍️ Sales by Product',
                         labels={'sales': 'Sales', 'product': 'Product'},
                         color='sales', color_continuous_scale='viridis')
    fig_product.update_layout(plot_bgcolor='white')

    # Sales by region chart
    sales_region = filtered_df.groupby('region')['sales'].sum().reset_index()
    fig_region = px.pie(sales_region, values='sales', names='region',
                        title='🗺️ Distribution by Region')

    # Sales by seller chart
    sales_seller = filtered_df.groupby('seller')['sales'].sum().reset_index()
    fig_seller = px.bar(sales_seller, x='seller', y='sales',
                          title='👥 Performance by Seller',
                          labels={'sales': 'Sales', 'seller': 'Seller'},
                          color='sales', color_continuous_scale='plasma')
    fig_seller.update_layout(plot_bgcolor='white')

    return fig_time, fig_product, fig_region, fig_seller


if __name__ == '__main__':
    print("🚀 Starting Sales Dashboard...")
    print("🌐 Access: http://localhost:8050")
    print("⚡ Dashboard running with simulated data")
    app.run_server(debug=True)