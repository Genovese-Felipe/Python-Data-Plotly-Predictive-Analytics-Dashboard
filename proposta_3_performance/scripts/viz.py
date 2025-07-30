# scripts/viz.py - Advanced Performance Analytics Dashboard (Proposal 3)
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import datetime as dt
import os
import sys

# Advanced color scheme - Professional gradient palette
ADVANCED_COLORS = {
    'primary': '#2E86AB',      # Deep blue
    'secondary': '#A23B72',    # Deep pink
    'accent': '#F18F01',       # Orange
    'success': '#32A251',      # Green
    'warning': '#FF6B35',      # Orange-red
    'danger': '#E74C3C',       # Red
    'info': '#17A2B8',         # Cyan
    'light': '#F8F9FA',        # Light gray
    'dark': '#2C3E50',         # Dark blue-gray
    'purple': '#8E44AD',       # Purple
    'teal': '#1ABC9C'          # Teal
}

def load_advanced_data():
    """Load advanced performance analytics data from CSV files"""
    try:
        df_projects = pd.read_csv('data/projects_advanced.csv')
        df_milestones = pd.read_csv('data/milestones_advanced.csv')
        df_financial = pd.read_csv('data/financial_advanced.csv')
        df_resources = pd.read_csv('data/resources_advanced.csv')
        df_quality = pd.read_csv('data/quality_metrics.csv')
        
        # Convert date columns
        date_columns_projects = ['start_date', 'planned_end_date', 'actual_end_date']
        for col in date_columns_projects:
            df_projects[col] = pd.to_datetime(df_projects[col])
        
        df_milestones['planned_date'] = pd.to_datetime(df_milestones['planned_date'])
        df_milestones['actual_date'] = pd.to_datetime(df_milestones['actual_date'])
        df_financial['month'] = pd.to_datetime(df_financial['month'])
        df_quality['measurement_date'] = pd.to_datetime(df_quality['measurement_date'])
        
        print("Advanced data loaded successfully.")
        return df_projects, df_milestones, df_financial, df_resources, df_quality
        
    except FileNotFoundError:
        print("Advanced data files not found. Generating new data...")
        sys.path.insert(0, 'scripts')
        from data_gen import generate_advanced_projects_data
        return generate_advanced_projects_data(150)

def create_advanced_kpi_card(title, value, change=None, icon=None, color='primary', subtitle=None):
    """Create an advanced KPI card with enhanced styling"""
    card_content = [
        html.Div([
            html.Div([
                html.H6(title, className="card-title text-muted mb-1", 
                       style={'fontWeight': '600', 'fontSize': '12px', 'textTransform': 'uppercase'}),
                html.H2(value, className="card-value mb-0", 
                       style={'fontWeight': 'bold', 'color': ADVANCED_COLORS[color], 'fontSize': '28px'}),
                html.Small(subtitle, className="text-muted") if subtitle else ""
            ], className="col-8"),
            
            html.Div([
                html.I(className=f"fa fa-{icon} fa-2x", 
                      style={'color': ADVANCED_COLORS[color], 'opacity': '0.7'}) if icon else "",
            ], className="col-4 text-right d-flex align-items-center justify-content-center")
        ], className="row align-items-center")
    ]
    
    if change is not None:
        try:
            change_value = float(change.strip('%+-'))
            direction = "up" if change_value > 0 else "down"
            change_color = ADVANCED_COLORS['success'] if direction == "up" else ADVANCED_COLORS['danger']
            
            card_content.append(
                html.Div([
                    html.I(className=f"fa fa-arrow-{direction} me-2", style={'color': change_color}),
                    html.Span(change, style={'color': change_color, 'fontWeight': '600'}),
                    html.Span(" from last period", className="ms-1 small text-muted")
                ], className="mt-3", style={'fontSize': '11px'})
            )
        except:
            pass
    
    return dbc.Card(
        card_content, 
        className="h-100",
        style={
            'border': 'none',
            'borderRadius': '12px',
            'background': 'linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%)',
            'boxShadow': '0 4px 20px rgba(0,0,0,0.08)',
            'transition': 'transform 0.2s ease-in-out',
            'padding': '20px'
        }
    )

def generate_executive_insights(df_projects, df_financial=None, df_quality=None):
    """Generate executive-level insights with advanced analytics"""
    insights = []
    
    if df_projects.empty:
        return [html.P("🔍 No data available for insight generation.", className="text-muted")]
    
    # Insight 1: Portfolio Health Score
    completed_projects = len(df_projects[df_projects['status'] == 'Completed'])
    delayed_projects = len(df_projects[df_projects['status'] == 'Delayed'])
    avg_progress = df_projects['progress_percent'].mean()
    
    health_score = (completed_projects / len(df_projects)) * 40 + \
                   (1 - delayed_projects / len(df_projects)) * 30 + \
                   (avg_progress / 100) * 30
    
    health_color = ADVANCED_COLORS['success'] if health_score > 70 else \
                   ADVANCED_COLORS['warning'] if health_score > 50 else ADVANCED_COLORS['danger']
    
    insights.append(
        dbc.Card([
            dbc.CardBody([
                html.Div([
                    html.H5("📊 Portfolio Health Score", className="mb-2", 
                           style={'fontWeight': 'bold', 'color': ADVANCED_COLORS['dark']}),
                    html.H3(f"{health_score:.1f}/100", 
                           style={'color': health_color, 'fontWeight': 'bold'}),
                    html.P(f"Based on {completed_projects} completed, {delayed_projects} delayed projects", 
                           className="text-muted mb-0")
                ])
            ])
        ], className="mb-3", style={'borderLeft': f'4px solid {health_color}'})
    )
    
    # Insight 2: Budget Performance
    total_planned = df_projects['budget_usd'].sum()
    total_actual = df_projects['actual_cost_usd'].sum()
    budget_variance = ((total_actual - total_planned) / total_planned) * 100
    
    budget_status = "under budget" if budget_variance < 0 else "over budget"
    budget_color = ADVANCED_COLORS['success'] if budget_variance < 0 else ADVANCED_COLORS['danger']
    
    insights.append(
        dbc.Card([
            dbc.CardBody([
                html.Div([
                    html.H5("💰 Budget Performance", className="mb-2", 
                           style={'fontWeight': 'bold', 'color': ADVANCED_COLORS['dark']}),
                    html.H4(f"{abs(budget_variance):.1f}% {budget_status}", 
                           style={'color': budget_color, 'fontWeight': 'bold'}),
                    html.P(f"${total_actual/1e6:.1f}M actual vs ${total_planned/1e6:.1f}M planned", 
                           className="text-muted mb-0")
                ])
            ])
        ], className="mb-3", style={'borderLeft': f'4px solid {budget_color}'})
    )
    
    # Insight 3: Risk Analysis
    high_risk_projects = len(df_projects[df_projects['risk_score'] > 7])
    critical_delayed = len(df_projects[
        (df_projects['priority'] == 'Critical') & 
        (df_projects['schedule_variance_days'] < -10)
    ])
    
    if high_risk_projects > 0 or critical_delayed > 0:
        insights.append(
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.H5("⚠️ Risk Alert", className="mb-2", 
                               style={'fontWeight': 'bold', 'color': ADVANCED_COLORS['danger']}),
                        html.P([
                            f"🔴 {high_risk_projects} high-risk projects identified",
                            html.Br(),
                            f"🚨 {critical_delayed} critical projects behind schedule"
                        ], className="mb-0")
                    ])
                ])
            ], className="mb-3", style={'borderLeft': f'4px solid {ADVANCED_COLORS["danger"]}'})
        )
    
    # Insight 4: Quality Trends
    if df_quality is not None and not df_quality.empty:
        avg_quality = df_quality['score'].mean()
        quality_color = ADVANCED_COLORS['success'] if avg_quality > 8 else \
                       ADVANCED_COLORS['warning'] if avg_quality > 6 else ADVANCED_COLORS['danger']
        
        insights.append(
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.H5("✨ Quality Metrics", className="mb-2", 
                               style={'fontWeight': 'bold', 'color': ADVANCED_COLORS['dark']}),
                        html.H4(f"{avg_quality:.1f}/10", 
                               style={'color': quality_color, 'fontWeight': 'bold'}),
                        html.P("Average quality score across all dimensions", 
                               className="text-muted mb-0")
                    ])
                ])
            ], className="mb-3", style={'borderLeft': f'4px solid {quality_color}'})
        )
    
    return insights

# Load data
df_projects, df_milestones, df_financial, df_resources, df_quality = load_advanced_data()

# Initialize Dash app with advanced theme
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])
server = app.server

# Calculate key metrics
total_projects = len(df_projects)
total_budget = df_projects['budget_usd'].sum()
completed_projects = len(df_projects[df_projects['status'] == 'Completed'])
avg_roi = df_projects['expected_roi_pct'].mean()

# Advanced layout with modern design
app.layout = dbc.Container([
    # Modern Header
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H1("🚀 Advanced Performance Analytics", 
                       style={'fontWeight': 'bold', 'color': ADVANCED_COLORS['dark'], 
                             'fontSize': '36px', 'marginBottom': '8px'}),
                html.P("Executive Dashboard for Strategic Project Portfolio Management", 
                       style={'color': ADVANCED_COLORS['dark'], 'fontSize': '16px', 'opacity': '0.8'})
            ], style={'textAlign': 'center'})
        ])
    ], className="mb-5", style={'paddingTop': '20px'}),
    
    # Executive Summary Cards
    dbc.Row([
        dbc.Col([
            create_advanced_kpi_card(
                "Portfolio Size", 
                f"{total_projects}", 
                "+15%",
                "briefcase",
                "primary",
                "Active Projects"
            )
        ], width=3),
        dbc.Col([
            create_advanced_kpi_card(
                "Total Investment", 
                f"${total_budget/1e6:.1f}M", 
                "+22%",
                "dollar-sign",
                "success",
                "USD Budget"
            )
        ], width=3),
        dbc.Col([
            create_advanced_kpi_card(
                "Completion Rate", 
                f"{(completed_projects/total_projects)*100:.1f}%", 
                "+8%",
                "check-circle",
                "teal",
                "Delivered"
            )
        ], width=3),
        dbc.Col([
            create_advanced_kpi_card(
                "Expected ROI", 
                f"{avg_roi:.0f}%", 
                "+12%",
                "chart-line",
                "accent",
                "Average"
            )
        ], width=3)
    ], className="mb-5"),
    
    # Advanced Filters
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("🎛️ Analytics Filters", className="mb-3", 
                           style={'fontWeight': 'bold', 'color': ADVANCED_COLORS['dark']}),
                    dbc.Row([
                        dbc.Col([
                            html.Label("Project Category", className="fw-bold text-muted mb-1"),
                            dcc.Dropdown(
                                id='category-filter',
                                options=[{'label': cat, 'value': cat} for cat in df_projects['category'].unique()],
                                value=df_projects['category'].unique().tolist(),
                                multi=True,
                                style={'fontSize': '14px'}
                            )
                        ], width=4),
                        dbc.Col([
                            html.Label("Business Unit", className="fw-bold text-muted mb-1"),
                            dcc.Dropdown(
                                id='business-unit-filter',
                                options=[{'label': unit, 'value': unit} for unit in df_projects['business_unit'].unique()],
                                value=df_projects['business_unit'].unique().tolist(),
                                multi=True,
                                style={'fontSize': '14px'}
                            )
                        ], width=4),
                        dbc.Col([
                            html.Label("Priority Level", className="fw-bold text-muted mb-1"),
                            dcc.Dropdown(
                                id='priority-filter',
                                options=[{'label': p, 'value': p} for p in df_projects['priority'].unique()],
                                value=df_projects['priority'].unique().tolist(),
                                multi=True,
                                style={'fontSize': '14px'}
                            )
                        ], width=4)
                    ])
                ])
            ], style={'borderRadius': '12px', 'border': 'none', 'boxShadow': '0 2px 10px rgba(0,0,0,0.05)'})
        ])
    ], className="mb-4"),
    
    # Executive Insights Section
    dbc.Row([
        dbc.Col([
            html.H4("🧠 Executive Insights", className="mb-3", 
                   style={'fontWeight': 'bold', 'color': ADVANCED_COLORS['dark']}),
            html.Div(id="executive-insights")
        ], width=12)
    ], className="mb-4"),
    
    # Advanced Analytics Grid
    dbc.Row([
        # Left Column - Strategic Charts
        dbc.Col([
            # Portfolio Performance Matrix
            dbc.Card([
                dbc.CardHeader([
                    html.H5("📈 Portfolio Performance Matrix", className="mb-0", 
                           style={'fontWeight': 'bold', 'color': ADVANCED_COLORS['dark']})
                ]),
                dbc.CardBody([
                    dcc.Loading(
                        children=[dcc.Graph(id='performance-matrix', config={'displayModeBar': False})],
                        type="circle",
                        color=ADVANCED_COLORS['primary']
                    )
                ])
            ], className="mb-4", style={'borderRadius': '12px', 'border': 'none', 'boxShadow': '0 4px 15px rgba(0,0,0,0.08)'}),
            
            # Financial Trends
            dbc.Card([
                dbc.CardHeader([
                    html.H5("💰 Financial Performance Trends", className="mb-0", 
                           style={'fontWeight': 'bold', 'color': ADVANCED_COLORS['dark']})
                ]),
                dbc.CardBody([
                    dcc.Loading(
                        children=[dcc.Graph(id='financial-trends', config={'displayModeBar': False})],
                        type="circle",
                        color=ADVANCED_COLORS['primary']
                    )
                ])
            ], style={'borderRadius': '12px', 'border': 'none', 'boxShadow': '0 4px 15px rgba(0,0,0,0.08)'})
        ], width=8),
        
        # Right Column - KPI Charts
        dbc.Col([
            # Category Distribution
            dbc.Card([
                dbc.CardHeader([
                    html.H5("🎯 Project Categories", className="mb-0", 
                           style={'fontWeight': 'bold', 'color': ADVANCED_COLORS['dark']})
                ]),
                dbc.CardBody([
                    dcc.Loading(
                        children=[dcc.Graph(id='category-sunburst', config={'displayModeBar': False})],
                        type="circle",
                        color=ADVANCED_COLORS['primary']
                    )
                ])
            ], className="mb-4", style={'borderRadius': '12px', 'border': 'none', 'boxShadow': '0 4px 15px rgba(0,0,0,0.08)'}),
            
            # Risk vs Value Matrix
            dbc.Card([
                dbc.CardHeader([
                    html.H5("⚖️ Risk vs Value", className="mb-0", 
                           style={'fontWeight': 'bold', 'color': ADVANCED_COLORS['dark']})
                ]),
                dbc.CardBody([
                    dcc.Loading(
                        children=[dcc.Graph(id='risk-value-matrix', config={'displayModeBar': False})],
                        type="circle",
                        color=ADVANCED_COLORS['primary']
                    )
                ])
            ], style={'borderRadius': '12px', 'border': 'none', 'boxShadow': '0 4px 15px rgba(0,0,0,0.08)'})
        ], width=4)
    ], className="mb-4"),
    
    # Bottom Analytics Row
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5("🔧 Resource Utilization Analysis", className="mb-0", 
                           style={'fontWeight': 'bold', 'color': ADVANCED_COLORS['dark']})
                ]),
                dbc.CardBody([
                    dcc.Loading(
                        children=[dcc.Graph(id='resource-analysis', config={'displayModeBar': False})],
                        type="circle",
                        color=ADVANCED_COLORS['primary']
                    )
                ])
            ], style={'borderRadius': '12px', 'border': 'none', 'boxShadow': '0 4px 15px rgba(0,0,0,0.08)'})
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5("📊 Quality Metrics Dashboard", className="mb-0", 
                           style={'fontWeight': 'bold', 'color': ADVANCED_COLORS['dark']})
                ]),
                dbc.CardBody([
                    dcc.Loading(
                        children=[dcc.Graph(id='quality-radar', config={'displayModeBar': False})],
                        type="circle",
                        color=ADVANCED_COLORS['primary']
                    )
                ])
            ], style={'borderRadius': '12px', 'border': 'none', 'boxShadow': '0 4px 15px rgba(0,0,0,0.08)'})
        ], width=6)
    ], className="mb-4"),
    
    # Footer
    html.Hr(style={'margin': '40px 0'}),
    html.Div([
        html.P([
            "🚀 Advanced Performance Analytics Dashboard | Powered by ",
            html.A("Genovese-Felipe", href="https://github.com/Genovese-Felipe", 
                  style={'color': ADVANCED_COLORS['primary'], 'textDecoration': 'none'}),
            " | Real-time Executive Intelligence"
        ], className="text-center text-muted", style={'fontSize': '14px'})
    ])
    
], fluid=True, style={'backgroundColor': '#FAFBFC', 'paddingBottom': '40px'})

# Advanced Callbacks
@callback(
    [Output('performance-matrix', 'figure'),
     Output('financial-trends', 'figure'),
     Output('category-sunburst', 'figure'),
     Output('risk-value-matrix', 'figure'),
     Output('resource-analysis', 'figure'),
     Output('quality-radar', 'figure'),
     Output('executive-insights', 'children')],
    [Input('category-filter', 'value'),
     Input('business-unit-filter', 'value'),
     Input('priority-filter', 'value')]
)
def update_advanced_charts(categories, business_units, priorities):
    # Filter data
    filtered_df = df_projects.copy()
    
    if categories and len(categories) > 0:
        filtered_df = filtered_df[filtered_df['category'].isin(categories)]
    
    if business_units and len(business_units) > 0:
        filtered_df = filtered_df[filtered_df['business_unit'].isin(business_units)]
    
    if priorities and len(priorities) > 0:
        filtered_df = filtered_df[filtered_df['priority'].isin(priorities)]
    
    # Filter related datasets
    filtered_financial = df_financial[df_financial['project_id'].isin(filtered_df['project_id'])]
    filtered_resources = df_resources[df_resources['project_id'].isin(filtered_df['project_id'])]
    filtered_quality = df_quality[df_quality['project_id'].isin(filtered_df['project_id'])]
    
    # Generate executive insights
    insights = generate_executive_insights(filtered_df, filtered_financial, filtered_quality)
    
    # 1. Performance Matrix (Budget vs Schedule)
    if filtered_df.empty:
        fig_matrix = go.Figure().add_annotation(text="No data available", x=0.5, y=0.5)
    else:
        fig_matrix = px.scatter(
            filtered_df,
            x='schedule_variance_days',
            y='budget_variance_pct',
            size='budget_usd',
            color='priority',
            hover_name='project_name',
            hover_data=['category', 'business_unit', 'progress_percent'],
            color_discrete_map={
                'Critical': ADVANCED_COLORS['danger'],
                'High': ADVANCED_COLORS['warning'],
                'Medium': ADVANCED_COLORS['info'],
                'Low': ADVANCED_COLORS['success']
            },
            labels={
                'schedule_variance_days': 'Schedule Variance (Days)',
                'budget_variance_pct': 'Budget Variance (%)',
                'priority': 'Priority'
            }
        )
        
        # Add quadrant lines
        fig_matrix.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
        fig_matrix.add_vline(x=0, line_dash="dash", line_color="gray", opacity=0.5)
        
        fig_matrix.update_layout(
            template="plotly_white",
            height=400,
            margin=dict(l=20, r=20, t=20, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
        )
    
    # 2. Financial Trends
    if filtered_financial.empty:
        fig_financial = go.Figure().add_annotation(text="No financial data available", x=0.5, y=0.5)
    else:
        monthly_financial = filtered_financial.groupby('month').agg({
            'planned_spend': 'sum',
            'actual_spend': 'sum'
        }).reset_index()
        
        fig_financial = go.Figure()
        
        fig_financial.add_trace(go.Scatter(
            x=monthly_financial['month'],
            y=monthly_financial['planned_spend'],
            mode='lines+markers',
            name='Planned Spend',
            line=dict(color=ADVANCED_COLORS['primary'], width=3),
            marker=dict(size=8)
        ))
        
        fig_financial.add_trace(go.Scatter(
            x=monthly_financial['month'],
            y=monthly_financial['actual_spend'],
            mode='lines+markers',
            name='Actual Spend',
            line=dict(color=ADVANCED_COLORS['secondary'], width=3),
            marker=dict(size=8)
        ))
        
        fig_financial.update_layout(
            template="plotly_white",
            height=400,
            margin=dict(l=20, r=20, t=20, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
            yaxis_title="Spend ($)",
            xaxis_title="Month"
        )
    
    # 3. Category Sunburst
    if filtered_df.empty:
        fig_sunburst = go.Figure().add_annotation(text="No data available", x=0.5, y=0.5)
    else:
        # Create hierarchy: Category -> Priority -> Projects
        sunburst_data = []
        for _, row in filtered_df.iterrows():
            sunburst_data.append({
                'ids': row['project_id'],
                'labels': row['project_name'][:20],
                'parents': f"{row['category']} - {row['priority']}",
                'values': row['budget_usd']
            })
            
        # Add category-priority combinations
        for cat in filtered_df['category'].unique():
            for priority in filtered_df['priority'].unique():
                subset = filtered_df[(filtered_df['category'] == cat) & (filtered_df['priority'] == priority)]
                if not subset.empty:
                    sunburst_data.append({
                        'ids': f"{cat} - {priority}",
                        'labels': priority,
                        'parents': cat,
                        'values': subset['budget_usd'].sum()
                    })
        
        # Add categories
        for cat in filtered_df['category'].unique():
            subset = filtered_df[filtered_df['category'] == cat]
            sunburst_data.append({
                'ids': cat,
                'labels': cat,
                'parents': "",
                'values': subset['budget_usd'].sum()
            })
        
        sunburst_df = pd.DataFrame(sunburst_data)
        
        fig_sunburst = go.Figure(go.Sunburst(
            ids=sunburst_df['ids'],
            labels=sunburst_df['labels'],
            parents=sunburst_df['parents'],
            values=sunburst_df['values'],
            branchvalues="total",
            maxdepth=2
        ))
        
        fig_sunburst.update_layout(
            template="plotly_white",
            height=350,
            margin=dict(l=20, r=20, t=20, b=20)
        )
    
    # 4. Risk vs Value Matrix
    if filtered_df.empty:
        fig_risk_value = go.Figure().add_annotation(text="No data available", x=0.5, y=0.5)
    else:
        fig_risk_value = px.scatter(
            filtered_df,
            x='risk_score',
            y='business_value_score',
            size='budget_usd',
            color='category',
            hover_name='project_name',
            color_discrete_sequence=px.colors.qualitative.Set3,
            labels={
                'risk_score': 'Risk Score (1-10)',
                'business_value_score': 'Business Value (1-10)'
            }
        )
        
        fig_risk_value.update_layout(
            template="plotly_white",
            height=350,
            margin=dict(l=20, r=20, t=20, b=20),
            showlegend=False
        )
    
    # 5. Resource Analysis
    if filtered_resources.empty:
        fig_resources = go.Figure().add_annotation(text="No resource data available", x=0.5, y=0.5)
    else:
        resource_summary = filtered_resources.groupby('resource_type').agg({
            'planned_hours': 'sum',
            'actual_hours': 'sum'
        }).reset_index()
        
        fig_resources = go.Figure()
        
        fig_resources.add_trace(go.Bar(
            x=resource_summary['resource_type'],
            y=resource_summary['planned_hours'],
            name='Planned Hours',
            marker_color=ADVANCED_COLORS['primary'],
            opacity=0.7
        ))
        
        fig_resources.add_trace(go.Bar(
            x=resource_summary['resource_type'],
            y=resource_summary['actual_hours'],
            name='Actual Hours',
            marker_color=ADVANCED_COLORS['accent'],
            opacity=0.7
        ))
        
        fig_resources.update_layout(
            template="plotly_white",
            height=350,
            margin=dict(l=20, r=20, t=20, b=40),
            barmode='group',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
            xaxis_tickangle=-45,
            xaxis_title="Resource Type",
            yaxis_title="Hours"
        )
    
    # 6. Quality Radar Chart
    if filtered_quality.empty:
        fig_quality = go.Figure().add_annotation(text="No quality data available", x=0.5, y=0.5)
    else:
        quality_avg = filtered_quality.groupby('quality_dimension').agg({
            'score': 'mean',
            'target_score': 'mean'
        }).reset_index()
        
        fig_quality = go.Figure()
        
        fig_quality.add_trace(go.Scatterpolar(
            r=quality_avg['score'],
            theta=quality_avg['quality_dimension'],
            fill='toself',
            name='Actual Score',
            line_color=ADVANCED_COLORS['primary']
        ))
        
        fig_quality.add_trace(go.Scatterpolar(
            r=quality_avg['target_score'],
            theta=quality_avg['quality_dimension'],
            fill='toself',
            name='Target Score',
            line_color=ADVANCED_COLORS['success'],
            opacity=0.6
        ))
        
        fig_quality.update_layout(
            template="plotly_white",
            height=350,
            margin=dict(l=20, r=20, t=20, b=20),
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )
            ),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
        )
    
    return fig_matrix, fig_financial, fig_sunburst, fig_risk_value, fig_resources, fig_quality, insights

# Custom CSS for advanced styling
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Advanced Performance Analytics Dashboard</title>
        {%favicon%}
        {%css%}
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
            
            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                background-attachment: fixed;
                color: #2C3E50;
            }
            
            .container-fluid {
                background: #FAFBFC;
                border-radius: 20px;
                margin: 20px;
                padding: 30px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            }
            
            .card:hover {
                transform: translateY(-2px);
                transition: all 0.3s ease;
            }
            
            h1, h2, h3, h4, h5, h6 {
                font-weight: 600 !important;
            }
            
            .dash-loading {
                margin-top: 50px;
            }
            
            .Select__control {
                border: 1px solid #E2E8F0 !important;
                border-radius: 8px !important;
                box-shadow: none !important;
            }
            
            .Select__control:hover {
                border-color: #2E86AB !important;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

if __name__ == '__main__':
    # Ensure output directory exists
    if not os.path.exists('outputs'):
        os.makedirs('outputs')
    
    # For development
    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        app.run(debug=True, port=8052)
    else:
        print("Advanced analytics dashboard created. Use 'debug' flag to run server.")