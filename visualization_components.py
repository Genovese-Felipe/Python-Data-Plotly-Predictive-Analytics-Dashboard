"""
Data Visualization and Chart Components Module
Python Data Plotly Predictive Analytics Dashboard

This module provides comprehensive chart components and visualization utilities:
- Advanced chart types and configurations
- Interactive dashboard components
- Real-time data visualization
- Custom plotting functions
- Chart styling and theming
- Export and sharing utilities
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any, Optional, Union
import colorsys
from datetime import datetime, timedelta
import math


class AdvancedChartComponents:
    """Advanced chart components for sophisticated data visualization."""
    
    def __init__(self, color_palette: Optional[List[str]] = None):
        """
        Initialize with optional custom color palette.
        
        Args:
            color_palette (List[str], optional): Custom color palette
        """
        self.color_palette = color_palette or self._generate_color_palette()
        self.default_layout = self._create_default_layout()
    
    def _generate_color_palette(self, n_colors: int = 12) -> List[str]:
        """Generate a harmonious color palette."""
        colors = []
        for i in range(n_colors):
            hue = i / n_colors
            saturation = 0.7
            lightness = 0.6
            rgb = colorsys.hls_to_rgb(hue, lightness, saturation)
            hex_color = '#{:02x}{:02x}{:02x}'.format(
                int(rgb[0] * 255),
                int(rgb[1] * 255),
                int(rgb[2] * 255)
            )
            colors.append(hex_color)
        return colors
    
    def _create_default_layout(self) -> Dict[str, Any]:
        """Create default layout configuration."""
        return {
            'template': 'plotly_white',
            'font': {'family': 'Inter, Arial, sans-serif', 'size': 12},
            'title': {'font': {'size': 18, 'family': 'Inter, Arial, sans-serif'}},
            'showlegend': True,
            'hovermode': 'closest',
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'paper_bgcolor': 'rgba(0,0,0,0)'
        }
    
    def create_advanced_line_chart(self, 
                                  df: pd.DataFrame,
                                  x_column: str,
                                  y_columns: List[str],
                                  title: str = "Advanced Line Chart",
                                  show_markers: bool = True,
                                  smooth_lines: bool = False,
                                  fill_area: bool = False) -> go.Figure:
        """
        Create an advanced line chart with multiple y-series.
        
        Args:
            df (pd.DataFrame): Data source
            x_column (str): X-axis column name
            y_columns (List[str]): List of Y-axis column names
            title (str): Chart title
            show_markers (bool): Whether to show markers on lines
            smooth_lines (bool): Whether to smooth lines
            fill_area (bool): Whether to fill area under lines
        
        Returns:
            go.Figure: Configured Plotly figure
        """
        fig = go.Figure()
        
        for i, col in enumerate(y_columns):
            mode = 'lines+markers' if show_markers else 'lines'
            line_shape = 'spline' if smooth_lines else 'linear'
            fill_mode = 'tonexty' if fill_area and i > 0 else 'tozeroy' if fill_area else None
            
            fig.add_trace(go.Scatter(
                x=df[x_column],
                y=df[col],
                mode=mode,
                name=col,
                line=dict(
                    color=self.color_palette[i % len(self.color_palette)],
                    shape=line_shape,
                    width=2
                ),
                fill=fill_mode,
                fillcolor=self.color_palette[i % len(self.color_palette)] + '20',
                hovertemplate=f'<b>{col}</b><br>' +
                             f'{x_column}: %{{x}}<br>' +
                             f'{col}: %{{y}}<br>' +
                             '<extra></extra>'
            ))
        
        fig.update_layout(
            title=title,
            xaxis_title=x_column,
            yaxis_title='Value',
            **self.default_layout
        )
        
        return fig
    
    def create_multi_axis_chart(self,
                               df: pd.DataFrame,
                               x_column: str,
                               left_y_columns: List[str],
                               right_y_columns: List[str],
                               title: str = "Multi-Axis Chart") -> go.Figure:
        """
        Create a chart with multiple y-axes.
        
        Args:
            df (pd.DataFrame): Data source
            x_column (str): X-axis column name
            left_y_columns (List[str]): Columns for left y-axis
            right_y_columns (List[str]): Columns for right y-axis
            title (str): Chart title
        
        Returns:
            go.Figure: Configured Plotly figure
        """
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Add left y-axis traces
        for i, col in enumerate(left_y_columns):
            fig.add_trace(
                go.Scatter(
                    x=df[x_column],
                    y=df[col],
                    name=col,
                    line=dict(color=self.color_palette[i % len(self.color_palette)])
                ),
                secondary_y=False
            )
        
        # Add right y-axis traces
        for i, col in enumerate(right_y_columns):
            fig.add_trace(
                go.Scatter(
                    x=df[x_column],
                    y=df[col],
                    name=col,
                    line=dict(color=self.color_palette[(i + len(left_y_columns)) % len(self.color_palette)])
                ),
                secondary_y=True
            )
        
        # Update layout
        fig.update_layout(title=title, **self.default_layout)
        fig.update_xaxes(title_text=x_column)
        fig.update_yaxes(title_text="Left Y-Axis", secondary_y=False)
        fig.update_yaxes(title_text="Right Y-Axis", secondary_y=True)
        
        return fig
    
    def create_candlestick_chart(self,
                                df: pd.DataFrame,
                                date_column: str,
                                open_column: str,
                                high_column: str,
                                low_column: str,
                                close_column: str,
                                volume_column: str = None,
                                title: str = "Candlestick Chart") -> go.Figure:
        """
        Create a financial candlestick chart.
        
        Args:
            df (pd.DataFrame): Financial data
            date_column (str): Date column name
            open_column (str): Opening price column
            high_column (str): High price column
            low_column (str): Low price column
            close_column (str): Closing price column
            volume_column (str, optional): Volume column name
            title (str): Chart title
        
        Returns:
            go.Figure: Configured Plotly figure
        """
        if volume_column:
            fig = make_subplots(
                rows=2, cols=1,
                shared_xaxes=True,
                vertical_spacing=0.03,
                row_heights=[0.7, 0.3],
                subplot_titles=('Price', 'Volume')
            )
            
            # Add candlestick
            fig.add_trace(
                go.Candlestick(
                    x=df[date_column],
                    open=df[open_column],
                    high=df[high_column],
                    low=df[low_column],
                    close=df[close_column],
                    name="Price"
                ),
                row=1, col=1
            )
            
            # Add volume
            fig.add_trace(
                go.Bar(
                    x=df[date_column],
                    y=df[volume_column],
                    name="Volume",
                    marker_color='rgba(158,202,225,0.6)'
                ),
                row=2, col=1
            )
        else:
            fig = go.Figure()
            fig.add_trace(
                go.Candlestick(
                    x=df[date_column],
                    open=df[open_column],
                    high=df[high_column],
                    low=df[low_column],
                    close=df[close_column],
                    name="Price"
                )
            )
        
        fig.update_layout(title=title, xaxis_rangeslider_visible=False, **self.default_layout)
        return fig
    
    def create_bubble_chart(self,
                           df: pd.DataFrame,
                           x_column: str,
                           y_column: str,
                           size_column: str,
                           color_column: str = None,
                           text_column: str = None,
                           title: str = "Bubble Chart") -> go.Figure:
        """
        Create an interactive bubble chart.
        
        Args:
            df (pd.DataFrame): Data source
            x_column (str): X-axis column
            y_column (str): Y-axis column
            size_column (str): Bubble size column
            color_column (str, optional): Color grouping column
            text_column (str, optional): Text label column
            title (str): Chart title
        
        Returns:
            go.Figure: Configured Plotly figure
        """
        fig = px.scatter(
            df,
            x=x_column,
            y=y_column,
            size=size_column,
            color=color_column,
            text=text_column,
            title=title,
            color_discrete_sequence=self.color_palette
        )
        
        if text_column:
            fig.update_traces(textposition='middle center')
        
        fig.update_layout(**self.default_layout)
        return fig
    
    def create_waterfall_chart(self,
                              categories: List[str],
                              values: List[float],
                              title: str = "Waterfall Chart") -> go.Figure:
        """
        Create a waterfall chart to show cumulative effects.
        
        Args:
            categories (List[str]): Category names
            values (List[float]): Values for each category
            title (str): Chart title
        
        Returns:
            go.Figure: Configured Plotly figure
        """
        cumulative = [0]
        for val in values[:-1]:
            cumulative.append(cumulative[-1] + val)
        
        fig = go.Figure()
        
        # Add bars for each category
        for i, (cat, val) in enumerate(zip(categories, values)):
            color = self.color_palette[i % len(self.color_palette)]
            
            if i == 0:  # Starting value
                fig.add_trace(go.Bar(
                    x=[cat],
                    y=[val],
                    name=cat,
                    marker_color=color
                ))
            elif i == len(categories) - 1:  # Final value
                fig.add_trace(go.Bar(
                    x=[cat],
                    y=[cumulative[i] + val],
                    name=cat,
                    marker_color=color
                ))
            else:  # Intermediate values
                fig.add_trace(go.Bar(
                    x=[cat],
                    y=[val],
                    base=cumulative[i],
                    name=cat,
                    marker_color=color
                ))
        
        fig.update_layout(
            title=title,
            showlegend=False,
            **self.default_layout
        )
        
        return fig
    
    def create_radar_chart(self,
                          df: pd.DataFrame,
                          categories: List[str],
                          values_columns: List[str],
                          title: str = "Radar Chart") -> go.Figure:
        """
        Create a radar/spider chart.
        
        Args:
            df (pd.DataFrame): Data source
            categories (List[str]): Category names for radar axes
            values_columns (List[str]): Value columns for different series
            title (str): Chart title
        
        Returns:
            go.Figure: Configured Plotly figure
        """
        fig = go.Figure()
        
        for i, col in enumerate(values_columns):
            fig.add_trace(go.Scatterpolar(
                r=df[col],
                theta=categories,
                fill='toself',
                name=col,
                line_color=self.color_palette[i % len(self.color_palette)]
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, df[values_columns].max().max()]
                )
            ),
            title=title,
            **self.default_layout
        )
        
        return fig
    
    def create_funnel_chart(self,
                           stages: List[str],
                           values: List[float],
                           title: str = "Funnel Chart") -> go.Figure:
        """
        Create a funnel chart for conversion analysis.
        
        Args:
            stages (List[str]): Funnel stage names
            values (List[float]): Values for each stage
            title (str): Chart title
        
        Returns:
            go.Figure: Configured Plotly figure
        """
        fig = go.Figure()
        
        fig.add_trace(go.Funnel(
            y=stages,
            x=values,
            textinfo="value+percent initial",
            marker=dict(
                color=self.color_palette[:len(stages)],
                line=dict(color="white", width=2)
            )
        ))
        
        fig.update_layout(title=title, **self.default_layout)
        return fig
    
    def create_gauge_chart(self,
                          value: float,
                          title: str = "Gauge Chart",
                          min_value: float = 0,
                          max_value: float = 100,
                          threshold_ranges: List[Tuple[float, float, str]] = None) -> go.Figure:
        """
        Create a gauge chart for KPI display.
        
        Args:
            value (float): Current value
            title (str): Chart title
            min_value (float): Minimum gauge value
            max_value (float): Maximum gauge value
            threshold_ranges (List[Tuple[float, float, str]]): Color ranges
        
        Returns:
            go.Figure: Configured Plotly figure
        """
        if threshold_ranges is None:
            threshold_ranges = [
                (min_value, max_value * 0.5, "red"),
                (max_value * 0.5, max_value * 0.8, "yellow"),
                (max_value * 0.8, max_value, "green")
            ]
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=value,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': title},
            delta={'reference': max_value * 0.8},
            gauge={
                'axis': {'range': [None, max_value]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [start, end], 'color': color}
                    for start, end, color in threshold_ranges
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': max_value * 0.9
                }
            }
        ))
        
        fig.update_layout(**self.default_layout)
        return fig


class InteractiveComponents:
    """Interactive dashboard components and widgets."""
    
    @staticmethod
    def create_range_selector_buttons() -> List[Dict[str, Any]]:
        """Create time range selector buttons."""
        return [
            dict(count=1, label="1D", step="day", stepmode="backward"),
            dict(count=7, label="7D", step="day", stepmode="backward"),
            dict(count=30, label="30D", step="day", stepmode="backward"),
            dict(count=90, label="3M", step="day", stepmode="backward"),
            dict(count=365, label="1Y", step="day", stepmode="backward"),
            dict(step="all", label="All")
        ]
    
    @staticmethod
    def add_range_selector(fig: go.Figure) -> go.Figure:
        """Add range selector to a time series chart."""
        fig.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=InteractiveComponents.create_range_selector_buttons()
                ),
                rangeslider=dict(visible=True),
                type="date"
            )
        )
        return fig
    
    @staticmethod
    def add_crossfilter_selections(fig: go.Figure) -> go.Figure:
        """Add crossfilter capability to chart."""
        fig.update_layout(
            dragmode='select',
            selectdirection='diagonal'
        )
        fig.update_traces(
            selected_marker=dict(color='red'),
            unselected_marker=dict(color='lightgray', opacity=0.3)
        )
        return fig
    
    @staticmethod
    def create_dropdown_controls(options: List[Tuple[str, str]]) -> Dict[str, Any]:
        """
        Create dropdown control configuration.
        
        Args:
            options (List[Tuple[str, str]]): List of (label, value) tuples
        
        Returns:
            Dict[str, Any]: Dropdown configuration
        """
        return {
            'buttons': [
                dict(
                    label=label,
                    method="update",
                    args=[{"visible": [val == value for val in [opt[1] for opt in options]]}]
                )
                for label, value in options
            ],
            'direction': "down",
            'showactive': True,
            'x': 1.15,
            'xanchor': "left",
            'y': 1.02,
            'yanchor': "top"
        }
    
    @staticmethod
    def add_play_button(fig: go.Figure, frames: List[go.Frame]) -> go.Figure:
        """Add animation play button to chart."""
        fig.frames = frames
        fig.update_layout(
            updatemenus=[
                dict(
                    type="buttons",
                    buttons=[
                        dict(label="Play",
                             method="animate",
                             args=[None, {"frame": {"duration": 500, "redraw": True},
                                         "transition": {"duration": 300}}]),
                        dict(label="Pause",
                             method="animate",
                             args=[[None], {"frame": {"duration": 0, "redraw": True},
                                          "mode": "immediate",
                                          "transition": {"duration": 0}}])
                    ],
                    direction="left",
                    pad={"r": 10, "t": 87},
                    showactive=False,
                    x=0.1,
                    xanchor="right",
                    y=0,
                    yanchor="top"
                )
            ]
        )
        return fig


class ChartStyling:
    """Advanced chart styling and theming utilities."""
    
    @staticmethod
    def apply_dark_theme(fig: go.Figure) -> go.Figure:
        """Apply dark theme to chart."""
        fig.update_layout(
            template="plotly_dark",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='#2d3748',
            font=dict(color='white')
        )
        return fig
    
    @staticmethod
    def apply_minimal_theme(fig: go.Figure) -> go.Figure:
        """Apply minimal theme to chart."""
        fig.update_layout(
            template="simple_white",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False, zeroline=False),
            yaxis=dict(showgrid=False, zeroline=False)
        )
        return fig
    
    @staticmethod
    def apply_corporate_theme(fig: go.Figure, 
                            primary_color: str = "#1f77b4",
                            secondary_color: str = "#ff7f0e") -> go.Figure:
        """Apply corporate theme with brand colors."""
        fig.update_layout(
            template="plotly_white",
            colorway=[primary_color, secondary_color],
            title_font=dict(size=20, color=primary_color),
            font=dict(family="Arial, sans-serif")
        )
        return fig
    
    @staticmethod
    def add_watermark(fig: go.Figure, text: str, opacity: float = 0.1) -> go.Figure:
        """Add watermark to chart."""
        fig.add_annotation(
            text=text,
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            xanchor='center', yanchor='middle',
            showarrow=False,
            font=dict(size=40, color="gray"),
            opacity=opacity
        )
        return fig
    
    @staticmethod
    def add_logo(fig: go.Figure, 
                logo_path: str, 
                x: float = 0.02, 
                y: float = 0.98) -> go.Figure:
        """Add logo to chart."""
        fig.add_layout_image(
            dict(
                source=logo_path,
                xref="paper", yref="paper",
                x=x, y=y,
                sizex=0.1, sizey=0.1,
                xanchor="left", yanchor="top"
            )
        )
        return fig


class RealTimeCharts:
    """Real-time chart updates and streaming data visualization."""
    
    def __init__(self, max_points: int = 100):
        """
        Initialize real-time chart manager.
        
        Args:
            max_points (int): Maximum number of points to display
        """
        self.max_points = max_points
        self.data_buffer = []
    
    def create_streaming_line_chart(self, 
                                   initial_data: pd.DataFrame,
                                   x_column: str,
                                   y_column: str,
                                   title: str = "Real-Time Data") -> go.Figure:
        """Create a chart optimized for real-time updates."""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=initial_data[x_column],
            y=initial_data[y_column],
            mode='lines+markers',
            name='Live Data',
            line=dict(color='#2E86AB', width=2)
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title=x_column,
            yaxis_title=y_column,
            template="plotly_white",
            showlegend=False,
            xaxis=dict(type='date'),
            yaxis=dict(autorange=True)
        )
        
        return fig
    
    def update_streaming_data(self, fig: go.Figure, new_data_point: Dict[str, Any]):
        """Update streaming chart with new data point."""
        self.data_buffer.append(new_data_point)
        
        # Keep only the last max_points
        if len(self.data_buffer) > self.max_points:
            self.data_buffer = self.data_buffer[-self.max_points:]
        
        # Update figure
        x_values = [point['x'] for point in self.data_buffer]
        y_values = [point['y'] for point in self.data_buffer]
        
        fig.data[0].x = x_values
        fig.data[0].y = y_values
        
        return fig


class ExportUtilities:
    """Utilities for exporting and sharing charts."""
    
    @staticmethod
    def export_chart_config(fig: go.Figure) -> Dict[str, Any]:
        """Export chart configuration for later reconstruction."""
        return {
            'data': [trace.to_plotly_json() for trace in fig.data],
            'layout': fig.layout.to_plotly_json(),
            'config': fig.to_dict().get('config', {})
        }
    
    @staticmethod
    def create_chart_from_config(config: Dict[str, Any]) -> go.Figure:
        """Create chart from exported configuration."""
        fig = go.Figure()
        
        for trace_config in config['data']:
            fig.add_trace(go.Scatter(trace_config))
        
        fig.update_layout(config['layout'])
        
        return fig
    
    @staticmethod
    def create_responsive_html(fig: go.Figure, 
                             title: str = "Interactive Chart",
                             include_plotlyjs: str = 'cdn') -> str:
        """Create responsive HTML with mobile optimization."""
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{title}</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{ 
                    margin: 0; 
                    padding: 20px; 
                    font-family: Arial, sans-serif;
                    background-color: #f8f9fa;
                }}
                .chart-container {{
                    width: 100%;
                    max-width: 1200px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    padding: 20px;
                }}
                @media (max-width: 768px) {{
                    body {{ padding: 10px; }}
                    .chart-container {{ padding: 15px; }}
                }}
            </style>
        </head>
        <body>
            <div class="chart-container">
                {fig.to_html(include_plotlyjs=include_plotlyjs, div_id="chart")}
            </div>
        </body>
        </html>
        """
        return html_template


# Utility functions for chart creation
def create_comparison_chart(data_dict: Dict[str, pd.DataFrame],
                          x_column: str,
                          y_column: str,
                          chart_type: str = 'line') -> go.Figure:
    """
    Create a comparison chart from multiple datasets.
    
    Args:
        data_dict (Dict[str, pd.DataFrame]): Dictionary of datasets
        x_column (str): X-axis column name
        y_column (str): Y-axis column name
        chart_type (str): Type of chart ('line', 'bar', 'scatter')
    
    Returns:
        go.Figure: Comparison chart
    """
    fig = go.Figure()
    colors = px.colors.qualitative.Set1
    
    for i, (name, df) in enumerate(data_dict.items()):
        if chart_type == 'line':
            fig.add_trace(go.Scatter(
                x=df[x_column],
                y=df[y_column],
                mode='lines+markers',
                name=name,
                line=dict(color=colors[i % len(colors)])
            ))
        elif chart_type == 'bar':
            fig.add_trace(go.Bar(
                x=df[x_column],
                y=df[y_column],
                name=name,
                marker_color=colors[i % len(colors)]
            ))
        elif chart_type == 'scatter':
            fig.add_trace(go.Scatter(
                x=df[x_column],
                y=df[y_column],
                mode='markers',
                name=name,
                marker=dict(color=colors[i % len(colors)])
            ))
    
    fig.update_layout(
        title=f"{chart_type.title()} Comparison Chart",
        xaxis_title=x_column,
        yaxis_title=y_column,
        template="plotly_white"
    )
    
    return fig


def calculate_chart_statistics(df: pd.DataFrame, value_column: str) -> Dict[str, float]:
    """Calculate basic statistics for chart annotation."""
    return {
        'mean': df[value_column].mean(),
        'median': df[value_column].median(),
        'std': df[value_column].std(),
        'min': df[value_column].min(),
        'max': df[value_column].max(),
        'q25': df[value_column].quantile(0.25),
        'q75': df[value_column].quantile(0.75)
    }


def add_statistical_annotations(fig: go.Figure, 
                              stats: Dict[str, float],
                              show_mean: bool = True,
                              show_median: bool = False) -> go.Figure:
    """Add statistical reference lines to chart."""
    if show_mean:
        fig.add_hline(
            y=stats['mean'],
            line_dash="dash",
            line_color="red",
            annotation_text=f"Mean: {stats['mean']:.2f}"
        )
    
    if show_median:
        fig.add_hline(
            y=stats['median'],
            line_dash="dot",
            line_color="blue",
            annotation_text=f"Median: {stats['median']:.2f}"
        )
    
    return fig


if __name__ == "__main__":
    # Example usage and testing
    print("Data Visualization and Chart Components Module - Testing")
    print("=" * 60)
    
    # Create sample data
    dates = pd.date_range(start='2023-01-01', periods=100, freq='D')
    sample_data = pd.DataFrame({
        'date': dates,
        'value1': np.random.normal(100, 15, 100).cumsum(),
        'value2': np.random.normal(80, 12, 100).cumsum(),
        'value3': np.random.normal(120, 20, 100).cumsum(),
        'category': np.random.choice(['A', 'B', 'C'], 100),
        'size': np.random.uniform(10, 50, 100)
    })
    
    # Test advanced chart components
    chart_components = AdvancedChartComponents()
    
    # Create various advanced charts
    line_chart = chart_components.create_advanced_line_chart(
        sample_data, 'date', ['value1', 'value2', 'value3'],
        title="Multi-Series Line Chart",
        show_markers=True,
        smooth_lines=True
    )
    
    radar_data = pd.DataFrame({
        'metrics': [8, 7, 6, 9, 5, 8],
        'benchmark': [7, 8, 7, 8, 6, 7]
    })
    
    radar_chart = chart_components.create_radar_chart(
        radar_data,
        ['Speed', 'Quality', 'Cost', 'Innovation', 'Flexibility', 'Reliability'],
        ['metrics', 'benchmark'],
        title="Performance Radar Chart"
    )
    
    # Test gauge chart
    gauge_chart = chart_components.create_gauge_chart(
        value=75,
        title="Performance Score",
        max_value=100
    )
    
    # Test waterfall chart
    waterfall_chart = chart_components.create_waterfall_chart(
        ['Start', 'Increase 1', 'Increase 2', 'Decrease 1', 'End'],
        [100, 20, 15, -10, 125],
        title="Value Flow Analysis"
    )
    
    print("Charts created successfully:")
    print("- Advanced line chart with multiple series")
    print("- Radar chart for performance metrics")
    print("- Gauge chart for KPI display")
    print("- Waterfall chart for flow analysis")
    
    # Test real-time charts
    real_time_manager = RealTimeCharts(max_points=50)
    streaming_chart = real_time_manager.create_streaming_line_chart(
        sample_data.head(20), 'date', 'value1'
    )
    
    print("- Real-time streaming chart initialized")
    
    # Test export utilities
    export_utils = ExportUtilities()
    chart_config = export_utils.export_chart_config(line_chart)
    reconstructed_chart = export_utils.create_chart_from_config(chart_config)
    
    print("- Chart export and reconstruction tested")
    
    # Test chart statistics
    stats = calculate_chart_statistics(sample_data, 'value1')
    annotated_chart = add_statistical_annotations(line_chart, stats)
    
    print(f"- Chart statistics calculated: Mean = {stats['mean']:.2f}")
    
    print("\nAll advanced chart components tested successfully!")