"""
Monica AI Dashboard Integration
==============================

Integrates Monica AI Bot System with the existing Plotly dashboard,
providing a comprehensive web interface for:
- Bot management and creation
- API integration configuration  
- Knowledge management
- Writing assistance
- Platform integrations
- Real-time analytics and monitoring
"""

import dash
from dash import dcc, html, Input, Output, State, dash_table, callback
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any

# Import Monica AI components
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Monica_AI_System.core.bot_manager import BotManager
from Monica_AI_System.core.api_integration import APIIntegrationFramework
from Monica_AI_System.core.prompt_system import PromptSystem
from Monica_AI_System.capabilities.knowledge_manager import KnowledgeManager
from Monica_AI_System.capabilities.writing_assistant import WritingAssistant
from Monica_AI_System.integrations.platform_manager import PlatformManager
from Monica_AI_System.config.settings import get_config

class MonicaDashboard:
    """
    Main dashboard integration for Monica AI system.
    
    Provides comprehensive web interface for managing all aspects
    of the Monica AI bot system within the existing Plotly dashboard.
    """
    
    def __init__(self, app: dash.Dash):
        self.app = app
        self.bot_manager = BotManager()
        self.api_framework = APIIntegrationFramework()
        self.prompt_system = PromptSystem()
        self.knowledge_manager = KnowledgeManager()
        self.writing_assistant = WritingAssistant()
        self.platform_manager = PlatformManager()
        
        # Dashboard state
        self.current_user = "default_user"
        self.dashboard_data = {}
        
        # Setup callbacks
        self._setup_callbacks()
    
    def get_layout(self) -> html.Div:
        """Get the complete Monica AI dashboard layout."""
        
        return html.Div([
            # Header
            html.Div([
                html.H1("🤖 Monica AI Bot System", 
                       style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '30px'}),
                html.P("Comprehensive AI assistant platform with multi-platform integration",
                       style={'textAlign': 'center', 'color': '#7f8c8d', 'fontSize': '18px'})
            ], style={'padding': '20px', 'backgroundColor': '#ecf0f1', 'marginBottom': '20px'}),
            
            # Navigation Tabs
            dcc.Tabs(id='monica-tabs', value='overview', children=[
                dcc.Tab(label='📊 Overview', value='overview'),
                dcc.Tab(label='🤖 Bot Management', value='bots'),
                dcc.Tab(label='🔌 API Integration', value='apis'),
                dcc.Tab(label='📝 Prompt System', value='prompts'),
                dcc.Tab(label='📚 Knowledge Base', value='knowledge'),
                dcc.Tab(label='✍️ Writing Assistant', value='writing'),
                dcc.Tab(label='🌐 Platform Integration', value='platforms'),
                dcc.Tab(label='📈 Analytics', value='analytics')
            ], style={'marginBottom': '20px'}),
            
            # Content Area
            html.Div(id='monica-content', children=self._get_overview_content()),
            
            # Hidden stores for state management
            dcc.Store(id='monica-store', data={}),
            dcc.Interval(id='monica-interval', interval=30000, n_intervals=0)  # 30 second updates
        ])
    
    def _get_overview_content(self) -> html.Div:
        """Get overview dashboard content."""
        
        # Get system statistics
        bot_stats = self._get_bot_statistics()
        api_stats = self._get_api_statistics()
        knowledge_stats = self._get_knowledge_statistics()
        
        return html.Div([
            # System Status Cards
            html.Div([
                # Active Bots Card
                html.Div([
                    html.H3("Active Bots", style={'color': '#3498db'}),
                    html.H2(str(bot_stats['active_bots']), style={'color': '#2c3e50', 'margin': '10px 0'}),
                    html.P(f"Total: {bot_stats['total_bots']}", style={'color': '#7f8c8d'})
                ], className='overview-card', style=self._get_card_style()),
                
                # API Integrations Card
                html.Div([
                    html.H3("API Integrations", style={'color': '#2ecc71'}),
                    html.H2(str(api_stats['active_apis']), style={'color': '#2c3e50', 'margin': '10px 0'}),
                    html.P(f"Available: {api_stats['total_apis']}", style={'color': '#7f8c8d'})
                ], className='overview-card', style=self._get_card_style()),
                
                # Knowledge Documents Card  
                html.Div([
                    html.H3("Knowledge Documents", style={'color': '#e74c3c'}),
                    html.H2(str(knowledge_stats['total_documents']), style={'color': '#2c3e50', 'margin': '10px 0'}),
                    html.P(f"Size: {knowledge_stats['total_size_mb']:.1f} MB", style={'color': '#7f8c8d'})
                ], className='overview-card', style=self._get_card_style()),
                
                # System Health Card
                html.Div([
                    html.H3("System Health", style={'color': '#f39c12'}),
                    html.H2("98.5%", style={'color': '#2c3e50', 'margin': '10px 0'}),
                    html.P("All systems operational", style={'color': '#7f8c8d'})
                ], className='overview-card', style=self._get_card_style())
            ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '30px'}),
            
            # Quick Actions
            html.Div([
                html.H3("Quick Actions", style={'marginBottom': '20px'}),
                html.Div([
                    html.Button("Create New Bot", id='btn-create-bot', 
                               className='btn btn-primary', style=self._get_button_style('#3498db')),
                    html.Button("Upload Knowledge", id='btn-upload-knowledge',
                               className='btn btn-success', style=self._get_button_style('#2ecc71')),
                    html.Button("Generate Content", id='btn-generate-content',
                               className='btn btn-info', style=self._get_button_style('#e67e22')),
                    html.Button("API Settings", id='btn-api-settings',
                               className='btn btn-warning', style=self._get_button_style('#f39c12'))
                ], style={'display': 'flex', 'gap': '15px'})
            ], style={'marginBottom': '30px'}),
            
            # Recent Activity Chart
            html.Div([
                html.H3("Recent Activity", style={'marginBottom': '20px'}),
                dcc.Graph(id='activity-chart', figure=self._get_activity_chart())
            ], style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})
        ])
    
    def _get_bot_management_content(self) -> html.Div:
        """Get bot management interface."""
        
        user_bots = self.bot_manager.list_user_bots(self.current_user)
        
        return html.Div([
            # Bot Creation Form
            html.Div([
                html.H3("Create New Bot", style={'marginBottom': '20px'}),
                html.Div([
                    html.Div([
                        html.Label("Bot Name"),
                        dcc.Input(id='bot-name', type='text', placeholder='Enter bot name',
                                 style={'width': '100%', 'padding': '8px', 'marginBottom': '10px'})
                    ], style={'width': '48%', 'display': 'inline-block'}),
                    
                    html.Div([
                        html.Label("Role"),
                        dcc.Dropdown(
                            id='bot-role',
                            options=[{'label': role, 'value': role} for role in get_config('bot')['available_roles']],
                            placeholder='Select role',
                            style={'marginBottom': '10px'}
                        )
                    ], style={'width': '48%', 'float': 'right'})
                ], style={'marginBottom': '15px'}),
                
                html.Div([
                    html.Label("Description"),
                    dcc.Textarea(id='bot-description', placeholder='Describe your bot\'s purpose...',
                                style={'width': '100%', 'height': '80px', 'padding': '8px', 'marginBottom': '10px'})
                ]),
                
                html.Div([
                    html.Div([
                        html.Label("Communication Style"),
                        dcc.Dropdown(
                            id='bot-style',
                            options=[{'label': style, 'value': style} for style in get_config('bot')['communication_styles']],
                            value='Professional',
                            style={'marginBottom': '10px'}
                        )
                    ], style={'width': '32%', 'display': 'inline-block'}),
                    
                    html.Div([
                        html.Label("Difficulty Level"),
                        dcc.Dropdown(
                            id='bot-difficulty',
                            options=[{'label': level, 'value': level} for level in get_config('bot')['difficulty_levels']],
                            value='Intermediate',
                            style={'marginBottom': '10px'}
                        )
                    ], style={'width': '32%', 'display': 'inline-block', 'marginLeft': '2%'}),
                    
                    html.Div([
                        html.Label("Capabilities"),
                        dcc.Dropdown(
                            id='bot-capabilities',
                            options=[
                                {'label': 'Data Analysis', 'value': 'data_analysis'},
                                {'label': 'Code Generation', 'value': 'code_generation'},
                                {'label': 'Content Writing', 'value': 'content_writing'},
                                {'label': 'Research', 'value': 'research'},
                                {'label': 'Email Processing', 'value': 'email_processing'}
                            ],
                            multi=True,
                            style={'marginBottom': '10px'}
                        )
                    ], style={'width': '32%', 'float': 'right'})
                ], style={'marginBottom': '15px'}),
                
                html.Button("Create Bot", id='btn-submit-bot', 
                           style=self._get_button_style('#3498db'))
            ], style=self._get_form_style()),
            
            # Existing Bots Table
            html.Div([
                html.H3("Your Bots", style={'marginBottom': '20px'}),
                self._get_bots_table(user_bots)
            ], style={'marginTop': '30px'})
        ])
    
    def _get_api_integration_content(self) -> html.Div:
        """Get API integration management interface."""
        
        api_status = self.api_framework.get_api_status()
        
        return html.Div([
            # API Status Overview
            html.Div([
                html.H3("API Integration Status", style={'marginBottom': '20px'}),
                self._get_api_status_cards(api_status)
            ]),
            
            # API Configuration
            html.Div([
                html.H3("Configure API Credentials", style={'marginBottom': '20px', 'marginTop': '30px'}),
                html.Div([
                    html.Div([
                        html.Label("Select API"),
                        dcc.Dropdown(
                            id='api-selector',
                            options=[
                                {'label': 'Gmail API', 'value': 'gmail_api'},
                                {'label': 'YouTube API', 'value': 'youtube_api'},
                                {'label': 'GitHub API', 'value': 'github_api'},
                                {'label': 'Twitter API', 'value': 'twitter_api'},
                                {'label': 'News API', 'value': 'news_api'}
                            ],
                            placeholder='Select an API to configure'
                        )
                    ], style={'width': '48%', 'display': 'inline-block'}),
                    
                    html.Div([
                        html.Label("API Key/Token"),
                        dcc.Input(id='api-key', type='password', placeholder='Enter API key',
                                 style={'width': '100%', 'padding': '8px'})
                    ], style={'width': '48%', 'float': 'right'})
                ], style={'marginBottom': '15px'}),
                
                html.Button("Save Credentials", id='btn-save-api',
                           style=self._get_button_style('#2ecc71'))
            ], style=self._get_form_style())
        ])
    
    def _get_knowledge_management_content(self) -> html.Div:
        """Get knowledge management interface."""
        
        knowledge_stats = self.knowledge_manager.get_knowledge_statistics(self.current_user)
        
        return html.Div([
            # Knowledge Upload
            html.Div([
                html.H3("Upload Knowledge", style={'marginBottom': '20px'}),
                html.Div([
                    dcc.Upload(
                        id='knowledge-upload',
                        children=html.Div([
                            'Drag and Drop or ',
                            html.A('Select Files')
                        ]),
                        style={
                            'width': '100%', 'height': '60px', 'lineHeight': '60px',
                            'borderWidth': '1px', 'borderStyle': 'dashed',
                            'borderRadius': '5px', 'textAlign': 'center',
                            'margin': '10px', 'backgroundColor': '#f8f9fa'
                        },
                        multiple=True
                    )
                ]),
                
                html.Div([
                    html.Div([
                        html.Label("Tags"),
                        dcc.Input(id='knowledge-tags', placeholder='Enter tags (comma-separated)',
                                 style={'width': '100%', 'padding': '8px'})
                    ], style={'width': '48%', 'display': 'inline-block'}),
                    
                    html.Div([
                        html.Label("Category"),
                        dcc.Dropdown(
                            id='knowledge-category',
                            options=[
                                {'label': 'Technical', 'value': 'technical'},
                                {'label': 'Business', 'value': 'business'},
                                {'label': 'Academic', 'value': 'academic'},
                                {'label': 'Personal', 'value': 'personal'}
                            ],
                            placeholder='Select category'
                        )
                    ], style={'width': '48%', 'float': 'right'})
                ], style={'marginTop': '15px'})
            ], style=self._get_form_style()),
            
            # Knowledge Statistics
            html.Div([
                html.H3("Knowledge Base Statistics", style={'marginBottom': '20px'}),
                self._get_knowledge_stats_display(knowledge_stats)
            ], style={'marginTop': '30px'})
        ])
    
    def _get_card_style(self) -> Dict[str, str]:
        """Get card styling."""
        return {
            'backgroundColor': 'white',
            'padding': '20px',
            'borderRadius': '8px',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
            'textAlign': 'center',
            'width': '22%'
        }
    
    def _get_button_style(self, color: str) -> Dict[str, str]:
        """Get button styling."""
        return {
            'backgroundColor': color,
            'color': 'white',
            'padding': '10px 20px',
            'border': 'none',
            'borderRadius': '5px',
            'cursor': 'pointer',
            'fontSize': '14px'
        }
    
    def _get_form_style(self) -> Dict[str, str]:
        """Get form styling."""
        return {
            'backgroundColor': 'white',
            'padding': '20px',
            'borderRadius': '8px',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
        }
    
    def _get_bot_statistics(self) -> Dict[str, Any]:
        """Get bot statistics."""
        user_bots = self.bot_manager.list_user_bots(self.current_user)
        active_bots = self.bot_manager.get_active_bots(self.current_user)
        
        return {
            'total_bots': len(user_bots),
            'active_bots': len(active_bots),
            'bot_types': {},
            'usage_stats': {}
        }
    
    def _get_api_statistics(self) -> Dict[str, Any]:
        """Get API statistics."""
        api_status = self.api_framework.get_api_status()
        active_apis = sum(1 for status in api_status.values() if status.get('auth_configured', False))
        
        return {
            'total_apis': len(api_status),
            'active_apis': active_apis,
            'usage_stats': {}
        }
    
    def _get_knowledge_statistics(self) -> Dict[str, Any]:
        """Get knowledge statistics."""
        stats = self.knowledge_manager.get_knowledge_statistics(self.current_user)
        
        return {
            'total_documents': stats.get('total_documents', 0),
            'total_size_mb': stats.get('total_content_length', 0) / (1024 * 1024),
            'categories': stats.get('domain_distribution', {})
        }
    
    def _get_activity_chart(self) -> go.Figure:
        """Generate activity chart."""
        
        # Mock activity data
        dates = pd.date_range(start=datetime.now() - timedelta(days=7), end=datetime.now(), freq='D')
        bot_activity = [5, 8, 12, 15, 20, 18, 25]
        api_calls = [50, 75, 100, 120, 150, 140, 180]
        knowledge_uploads = [2, 3, 1, 4, 2, 3, 5]
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=['Bot Interactions', 'API Calls', 'Knowledge Uploads', 'System Performance'],
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Bot activity
        fig.add_trace(
            go.Scatter(x=dates, y=bot_activity, name='Bot Interactions', line=dict(color='#3498db')),
            row=1, col=1
        )
        
        # API calls
        fig.add_trace(
            go.Bar(x=dates, y=api_calls, name='API Calls', marker_color='#2ecc71'),
            row=1, col=2
        )
        
        # Knowledge uploads
        fig.add_trace(
            go.Scatter(x=dates, y=knowledge_uploads, name='Uploads', 
                      mode='markers+lines', marker=dict(color='#e74c3c', size=8)),
            row=2, col=1
        )
        
        # System performance
        performance = [98.5, 99.1, 97.8, 98.9, 99.5, 98.2, 99.0]
        fig.add_trace(
            go.Scatter(x=dates, y=performance, name='Uptime %', 
                      fill='tonexty', fillcolor='rgba(241, 196, 15, 0.3)',
                      line=dict(color='#f39c12')),
            row=2, col=2
        )
        
        fig.update_layout(
            height=500,
            showlegend=False,
            title_text="Monica AI System Activity Dashboard"
        )
        
        return fig
    
    def _get_bots_table(self, bots: List) -> dash_table.DataTable:
        """Generate bots table."""
        
        if not bots:
            return html.P("No bots created yet. Create your first bot above!")
        
        # Convert bots to table data
        table_data = []
        for bot in bots:
            table_data.append({
                'Name': bot.name,
                'Role': bot.role,
                'Status': 'Active' if bot.is_active else 'Inactive',
                'Created': bot.created_at[:10],
                'Interactions': bot.usage_stats.get('total_interactions', 0),
                'Success Rate': f"{bot.usage_stats.get('user_satisfaction', 0):.1f}/5.0"
            })
        
        return dash_table.DataTable(
            data=table_data,
            columns=[
                {"name": "Name", "id": "Name"},
                {"name": "Role", "id": "Role"},
                {"name": "Status", "id": "Status"},
                {"name": "Created", "id": "Created"},
                {"name": "Interactions", "id": "Interactions"},
                {"name": "Success Rate", "id": "Success Rate"}
            ],
            style_cell={'textAlign': 'left', 'padding': '10px'},
            style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
            style_data_conditional=[
                {
                    'if': {'filter_query': '{Status} = Active'},
                    'backgroundColor': '#d5f4e6',
                    'color': 'black',
                }
            ]
        )
    
    def _get_api_status_cards(self, api_status: Dict) -> html.Div:
        """Generate API status cards."""
        
        cards = []
        for api_name, status in list(api_status.items())[:6]:  # Show first 6
            status_color = '#2ecc71' if status.get('auth_configured', False) else '#e74c3c'
            status_text = 'Configured' if status.get('auth_configured', False) else 'Not Configured'
            
            card = html.Div([
                html.H4(status.get('name', api_name), style={'margin': '0 0 10px 0'}),
                html.P(status_text, style={'color': status_color, 'fontWeight': 'bold'}),
                html.P(f"Usage: {status.get('current_usage', 0)}/{status.get('rate_limit', 100)}")
            ], style={
                'backgroundColor': 'white',
                'padding': '15px',
                'borderRadius': '5px',
                'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                'textAlign': 'center',
                'width': '15%',
                'margin': '10px'
            })
            cards.append(card)
        
        return html.Div(cards, style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'space-between'})
    
    def _get_knowledge_stats_display(self, stats: Dict) -> html.Div:
        """Display knowledge statistics."""
        
        return html.Div([
            html.Div([
                html.H4("Documents", style={'color': '#3498db'}),
                html.H3(str(stats.get('total_documents', 0)))
            ], style=self._get_card_style()),
            
            html.Div([
                html.H4("Total Size", style={'color': '#2ecc71'}),
                html.H3(f"{stats.get('total_content_length', 0) / 1024:.1f} KB")
            ], style=self._get_card_style()),
            
            html.Div([
                html.H4("Categories", style={'color': '#e74c3c'}),
                html.H3(str(len(stats.get('domain_distribution', {}))))
            ], style=self._get_card_style()),
            
            html.Div([
                html.H4("Relations", style={'color': '#f39c12'}),
                html.H3(str(stats.get('total_relationships', 0)))
            ], style=self._get_card_style())
        ], style={'display': 'flex', 'justifyContent': 'space-between'})
    
    def _setup_callbacks(self):
        """Setup dashboard callbacks."""
        
        @self.app.callback(
            Output('monica-content', 'children'),
            Input('monica-tabs', 'value')
        )
        def update_content(active_tab):
            if active_tab == 'overview':
                return self._get_overview_content()
            elif active_tab == 'bots':
                return self._get_bot_management_content()
            elif active_tab == 'apis':
                return self._get_api_integration_content()
            elif active_tab == 'knowledge':
                return self._get_knowledge_management_content()
            else:
                return html.Div([
                    html.H3(f"{active_tab.title()} Interface"),
                    html.P("This feature is coming soon!")
                ])

def integrate_monica_with_dashboard(existing_app: dash.Dash) -> dash.Dash:
    """
    Integrate Monica AI system with existing dashboard.
    
    Args:
        existing_app: Existing Dash application
        
    Returns:
        Enhanced Dash application with Monica AI features
    """
    
    # Create Monica dashboard instance
    monica_dashboard = MonicaDashboard(existing_app)
    
    # Add Monica AI tab to existing layout
    original_layout = existing_app.layout
    
    # Enhanced layout with Monica AI integration
    enhanced_layout = html.Div([
        # Navigation between original dashboard and Monica AI
        dcc.Tabs(id='main-navigation', value='original', children=[
            dcc.Tab(label='📊 Analytics Dashboard', value='original'),
            dcc.Tab(label='🤖 Monica AI System', value='monica')
        ], style={'marginBottom': '20px'}),
        
        # Content area
        html.Div(id='main-content', children=original_layout)
    ])
    
    # Update app layout
    existing_app.layout = enhanced_layout
    
    # Add navigation callback
    @existing_app.callback(
        Output('main-content', 'children'),
        Input('main-navigation', 'value')
    )
    def update_main_content(active_tab):
        if active_tab == 'monica':
            return monica_dashboard.get_layout()
        else:
            return original_layout
    
    return existing_app