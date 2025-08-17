"""
Dashboard Utilities Module
Python Data Plotly Predictive Analytics Dashboard

This module provides comprehensive utilities for dashboard creation including:
- Data processing and transformation utilities
- Chart generation helpers
- Dashboard layout management
- Configuration management
- Performance optimization tools
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
from datetime import datetime, timedelta
import json
from typing import Dict, List, Tuple, Any, Optional
import os
from pathlib import Path


class DashboardConfig:
    """Configuration management for dashboard applications."""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize dashboard configuration.
        
        Args:
            config_file (str, optional): Path to configuration file
        """
        self.config = self._load_default_config()
        if config_file and os.path.exists(config_file):
            self._load_config_file(config_file)
    
    def _load_default_config(self) -> Dict[str, Any]:
        """Load default dashboard configuration."""
        return {
            'theme': {
                'primary_color': '#2E86AB',
                'secondary_color': '#A23B72',
                'accent_color': '#F18F01',
                'background_color': '#FAFBFC',
                'text_color': '#2D3748',
                'font_family': 'Inter, Arial, sans-serif',
                'font_size': 14
            },
            'layout': {
                'sidebar_width': 250,
                'header_height': 60,
                'margin': 20,
                'border_radius': 8,
                'card_shadow': '0 4px 15px rgba(0,0,0,0.08)'
            },
            'charts': {
                'height': 400,
                'template': 'plotly_white',
                'color_sequence': px.colors.qualitative.Set2,
                'show_legend': True,
                'animation': True
            },
            'data': {
                'cache_timeout': 300,  # 5 minutes
                'max_rows': 10000,
                'chunk_size': 1000
            },
            'performance': {
                'enable_caching': True,
                'compress_responses': True,
                'lazy_loading': True
            }
        }
    
    def _load_config_file(self, config_file: str):
        """Load configuration from file."""
        try:
            with open(config_file, 'r') as f:
                file_config = json.load(f)
            self._deep_update(self.config, file_config)
        except Exception as e:
            print(f"Warning: Could not load config file {config_file}: {e}")
    
    def _deep_update(self, base_dict: Dict, update_dict: Dict):
        """Deep update dictionary."""
        for key, value in update_dict.items():
            if key in base_dict and isinstance(base_dict[key], dict) and isinstance(value, dict):
                self._deep_update(base_dict[key], value)
            else:
                base_dict[key] = value
    
    def get(self, key_path: str, default=None):
        """
        Get configuration value using dot notation.
        
        Args:
            key_path (str): Dot-separated path to config value
            default: Default value if key not found
        """
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, key_path: str, value: Any):
        """
        Set configuration value using dot notation.
        
        Args:
            key_path (str): Dot-separated path to config value
            value: Value to set
        """
        keys = key_path.split('.')
        config = self.config
        
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        config[keys[-1]] = value


class DataProcessor:
    """Advanced data processing utilities for dashboard applications."""
    
    @staticmethod
    def clean_dataframe(df: pd.DataFrame, 
                       remove_duplicates: bool = True,
                       handle_missing: str = 'drop',
                       date_columns: List[str] = None) -> pd.DataFrame:
        """
        Clean and preprocess DataFrame.
        
        Args:
            df (pd.DataFrame): Input DataFrame
            remove_duplicates (bool): Whether to remove duplicate rows
            handle_missing (str): How to handle missing values ('drop', 'fill', 'interpolate')
            date_columns (List[str]): List of columns to convert to datetime
        
        Returns:
            pd.DataFrame: Cleaned DataFrame
        """
        df_clean = df.copy()
        
        # Remove duplicates
        if remove_duplicates:
            df_clean = df_clean.drop_duplicates()
        
        # Handle missing values
        if handle_missing == 'drop':
            df_clean = df_clean.dropna()
        elif handle_missing == 'fill':
            # Fill numerical columns with mean, categorical with mode
            for col in df_clean.columns:
                if df_clean[col].dtype in ['int64', 'float64']:
                    df_clean[col].fillna(df_clean[col].mean(), inplace=True)
                else:
                    df_clean[col].fillna(df_clean[col].mode().iloc[0] if not df_clean[col].mode().empty else 'Unknown', inplace=True)
        elif handle_missing == 'interpolate':
            df_clean = df_clean.interpolate()
        
        # Convert date columns
        if date_columns:
            for col in date_columns:
                if col in df_clean.columns:
                    df_clean[col] = pd.to_datetime(df_clean[col], errors='coerce')
        
        return df_clean
    
    @staticmethod
    def aggregate_data(df: pd.DataFrame, 
                      group_by: List[str], 
                      agg_dict: Dict[str, str]) -> pd.DataFrame:
        """
        Aggregate data by specified columns.
        
        Args:
            df (pd.DataFrame): Input DataFrame
            group_by (List[str]): Columns to group by
            agg_dict (Dict[str, str]): Aggregation dictionary {column: function}
        
        Returns:
            pd.DataFrame: Aggregated DataFrame
        """
        return df.groupby(group_by).agg(agg_dict).reset_index()
    
    @staticmethod
    def create_time_series(df: pd.DataFrame, 
                          date_column: str, 
                          value_column: str,
                          frequency: str = 'D') -> pd.DataFrame:
        """
        Create time series from DataFrame.
        
        Args:
            df (pd.DataFrame): Input DataFrame
            date_column (str): Name of date column
            value_column (str): Name of value column
            frequency (str): Resampling frequency ('D', 'W', 'M', 'Y')
        
        Returns:
            pd.DataFrame: Time series DataFrame
        """
        df_ts = df.copy()
        df_ts[date_column] = pd.to_datetime(df_ts[date_column])
        df_ts = df_ts.set_index(date_column)
        
        return df_ts[value_column].resample(frequency).sum().reset_index()


class ChartFactory:
    """Factory class for creating various types of charts."""
    
    def __init__(self, config: DashboardConfig):
        """
        Initialize chart factory with configuration.
        
        Args:
            config (DashboardConfig): Dashboard configuration
        """
        self.config = config
        
    def create_line_chart(self, df: pd.DataFrame, 
                         x_column: str, 
                         y_column: str,
                         color_column: str = None,
                         title: str = None) -> go.Figure:
        """Create an interactive line chart."""
        fig = px.line(
            df, 
            x=x_column, 
            y=y_column,
            color=color_column,
            title=title or f"{y_column} over {x_column}",
            template=self.config.get('charts.template'),
            color_discrete_sequence=self.config.get('charts.color_sequence')
        )
        
        self._apply_chart_styling(fig)
        return fig
    
    def create_bar_chart(self, df: pd.DataFrame,
                        x_column: str,
                        y_column: str,
                        color_column: str = None,
                        title: str = None,
                        orientation: str = 'v') -> go.Figure:
        """Create an interactive bar chart."""
        fig = px.bar(
            df,
            x=x_column,
            y=y_column,
            color=color_column,
            title=title or f"{y_column} by {x_column}",
            template=self.config.get('charts.template'),
            color_discrete_sequence=self.config.get('charts.color_sequence'),
            orientation=orientation
        )
        
        self._apply_chart_styling(fig)
        return fig
    
    def create_scatter_plot(self, df: pd.DataFrame,
                           x_column: str,
                           y_column: str,
                           size_column: str = None,
                           color_column: str = None,
                           title: str = None) -> go.Figure:
        """Create an interactive scatter plot."""
        fig = px.scatter(
            df,
            x=x_column,
            y=y_column,
            size=size_column,
            color=color_column,
            title=title or f"{y_column} vs {x_column}",
            template=self.config.get('charts.template'),
            color_discrete_sequence=self.config.get('charts.color_sequence')
        )
        
        self._apply_chart_styling(fig)
        return fig
    
    def create_pie_chart(self, df: pd.DataFrame,
                        values_column: str,
                        names_column: str,
                        title: str = None) -> go.Figure:
        """Create an interactive pie chart."""
        fig = px.pie(
            df,
            values=values_column,
            names=names_column,
            title=title or f"Distribution of {values_column}",
            template=self.config.get('charts.template'),
            color_discrete_sequence=self.config.get('charts.color_sequence')
        )
        
        self._apply_chart_styling(fig)
        return fig
    
    def create_histogram(self, df: pd.DataFrame,
                        x_column: str,
                        color_column: str = None,
                        bins: int = 30,
                        title: str = None) -> go.Figure:
        """Create an interactive histogram."""
        fig = px.histogram(
            df,
            x=x_column,
            color=color_column,
            nbins=bins,
            title=title or f"Distribution of {x_column}",
            template=self.config.get('charts.template'),
            color_discrete_sequence=self.config.get('charts.color_sequence')
        )
        
        self._apply_chart_styling(fig)
        return fig
    
    def create_box_plot(self, df: pd.DataFrame,
                       x_column: str = None,
                       y_column: str = None,
                       color_column: str = None,
                       title: str = None) -> go.Figure:
        """Create an interactive box plot."""
        fig = px.box(
            df,
            x=x_column,
            y=y_column,
            color=color_column,
            title=title or f"Box Plot of {y_column or x_column}",
            template=self.config.get('charts.template'),
            color_discrete_sequence=self.config.get('charts.color_sequence')
        )
        
        self._apply_chart_styling(fig)
        return fig
    
    def create_heatmap(self, df: pd.DataFrame,
                      x_column: str,
                      y_column: str,
                      z_column: str,
                      title: str = None) -> go.Figure:
        """Create an interactive heatmap."""
        pivot_df = df.pivot(index=y_column, columns=x_column, values=z_column)
        
        fig = px.imshow(
            pivot_df,
            title=title or f"Heatmap of {z_column}",
            template=self.config.get('charts.template'),
            color_continuous_scale='Blues'
        )
        
        self._apply_chart_styling(fig)
        return fig
    
    def create_sunburst_chart(self, df: pd.DataFrame,
                             path_columns: List[str],
                             values_column: str,
                             title: str = None) -> go.Figure:
        """Create an interactive sunburst chart."""
        fig = px.sunburst(
            df,
            path=path_columns,
            values=values_column,
            title=title or "Sunburst Chart",
            template=self.config.get('charts.template'),
            color_discrete_sequence=self.config.get('charts.color_sequence')
        )
        
        self._apply_chart_styling(fig)
        return fig
    
    def create_treemap(self, df: pd.DataFrame,
                      path_columns: List[str],
                      values_column: str,
                      title: str = None) -> go.Figure:
        """Create an interactive treemap."""
        fig = px.treemap(
            df,
            path=path_columns,
            values=values_column,
            title=title or "Treemap",
            template=self.config.get('charts.template'),
            color_discrete_sequence=self.config.get('charts.color_sequence')
        )
        
        self._apply_chart_styling(fig)
        return fig
    
    def create_3d_scatter(self, df: pd.DataFrame,
                         x_column: str,
                         y_column: str,
                         z_column: str,
                         color_column: str = None,
                         size_column: str = None,
                         title: str = None) -> go.Figure:
        """Create a 3D scatter plot."""
        fig = px.scatter_3d(
            df,
            x=x_column,
            y=y_column,
            z=z_column,
            color=color_column,
            size=size_column,
            title=title or f"3D Scatter: {x_column}, {y_column}, {z_column}",
            template=self.config.get('charts.template'),
            color_discrete_sequence=self.config.get('charts.color_sequence')
        )
        
        self._apply_chart_styling(fig)
        return fig
    
    def create_correlation_matrix(self, df: pd.DataFrame,
                                 title: str = None) -> go.Figure:
        """Create a correlation matrix heatmap."""
        # Select only numerical columns
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        corr_matrix = df[numerical_cols].corr()
        
        fig = px.imshow(
            corr_matrix,
            title=title or "Correlation Matrix",
            template=self.config.get('charts.template'),
            color_continuous_scale='RdBu',
            aspect='auto'
        )
        
        # Add correlation values as text
        fig.update_traces(text=np.around(corr_matrix.values, decimals=2), texttemplate='%{text}')
        
        self._apply_chart_styling(fig)
        return fig
    
    def _apply_chart_styling(self, fig: go.Figure):
        """Apply consistent styling to charts."""
        fig.update_layout(
            height=self.config.get('charts.height'),
            font_family=self.config.get('theme.font_family'),
            font_size=self.config.get('theme.font_size'),
            plot_bgcolor=self.config.get('theme.background_color'),
            paper_bgcolor=self.config.get('theme.background_color'),
            showlegend=self.config.get('charts.show_legend')
        )
        
        # Update axis styling
        fig.update_xaxes(
            gridcolor='rgba(0,0,0,0.1)',
            zeroline=False
        )
        fig.update_yaxes(
            gridcolor='rgba(0,0,0,0.1)',
            zeroline=False
        )


class KPICalculator:
    """Calculate various Key Performance Indicators (KPIs)."""
    
    @staticmethod
    def calculate_growth_rate(current_value: float, previous_value: float) -> float:
        """Calculate growth rate between two values."""
        if previous_value == 0:
            return 0
        return ((current_value - previous_value) / previous_value) * 100
    
    @staticmethod
    def calculate_moving_average(data: List[float], window: int) -> List[float]:
        """Calculate moving average for a given window."""
        return [np.mean(data[max(0, i-window+1):i+1]) for i in range(len(data))]
    
    @staticmethod
    def calculate_variance(data: List[float]) -> float:
        """Calculate variance of data."""
        return np.var(data)
    
    @staticmethod
    def calculate_trend(data: List[float]) -> str:
        """Determine trend direction of data."""
        if len(data) < 2:
            return "Insufficient data"
        
        first_half = np.mean(data[:len(data)//2])
        second_half = np.mean(data[len(data)//2:])
        
        if second_half > first_half * 1.05:
            return "Increasing"
        elif second_half < first_half * 0.95:
            return "Decreasing"
        else:
            return "Stable"
    
    @staticmethod
    def calculate_conversion_rate(conversions: int, total_visitors: int) -> float:
        """Calculate conversion rate."""
        if total_visitors == 0:
            return 0
        return (conversions / total_visitors) * 100


class DashboardLayout:
    """Utilities for creating dashboard layouts."""
    
    def __init__(self, config: DashboardConfig):
        """Initialize with dashboard configuration."""
        self.config = config
    
    def create_card_style(self) -> Dict[str, str]:
        """Create CSS style for dashboard cards."""
        return {
            'backgroundColor': self.config.get('theme.background_color'),
            'border': f'1px solid {self.config.get("theme.border_color", "#E2E8F0")}',
            'borderRadius': f'{self.config.get("layout.border_radius")}px',
            'boxShadow': self.config.get('layout.card_shadow'),
            'padding': f'{self.config.get("layout.margin")}px',
            'margin': f'{self.config.get("layout.margin")}px',
            'fontFamily': self.config.get('theme.font_family')
        }
    
    def create_header_style(self) -> Dict[str, str]:
        """Create CSS style for dashboard header."""
        return {
            'backgroundColor': self.config.get('theme.primary_color'),
            'color': 'white',
            'height': f'{self.config.get("layout.header_height")}px',
            'padding': '0 20px',
            'display': 'flex',
            'alignItems': 'center',
            'fontSize': '24px',
            'fontWeight': 'bold',
            'fontFamily': self.config.get('theme.font_family')
        }
    
    def create_sidebar_style(self) -> Dict[str, str]:
        """Create CSS style for dashboard sidebar."""
        return {
            'backgroundColor': self.config.get('theme.background_color'),
            'width': f'{self.config.get("layout.sidebar_width")}px',
            'height': '100vh',
            'border': f'1px solid {self.config.get("theme.border_color", "#E2E8F0")}',
            'padding': f'{self.config.get("layout.margin")}px',
            'fontFamily': self.config.get('theme.font_family')
        }


class PerformanceOptimizer:
    """Performance optimization utilities for dashboards."""
    
    @staticmethod
    def optimize_dataframe_for_display(df: pd.DataFrame, max_rows: int = 1000) -> pd.DataFrame:
        """Optimize DataFrame for display by sampling if too large."""
        if len(df) > max_rows:
            return df.sample(n=max_rows, random_state=42)
        return df
    
    @staticmethod
    def cache_data(data: Any, cache_key: str, cache_dir: str = ".cache") -> str:
        """Cache data to disk for faster loading."""
        cache_path = Path(cache_dir)
        cache_path.mkdir(exist_ok=True)
        
        file_path = cache_path / f"{cache_key}.json"
        
        if isinstance(data, pd.DataFrame):
            data.to_json(file_path, orient='records')
        else:
            with open(file_path, 'w') as f:
                json.dump(data, f)
        
        return str(file_path)
    
    @staticmethod
    def load_cached_data(cache_key: str, cache_dir: str = ".cache") -> Any:
        """Load cached data from disk."""
        cache_path = Path(cache_dir) / f"{cache_key}.json"
        
        if cache_path.exists():
            try:
                with open(cache_path, 'r') as f:
                    return json.load(f)
            except Exception:
                # Try loading as DataFrame
                try:
                    return pd.read_json(cache_path, orient='records')
                except Exception:
                    return None
        return None
    
    @staticmethod
    def is_cache_valid(cache_key: str, cache_timeout: int = 300, cache_dir: str = ".cache") -> bool:
        """Check if cached data is still valid."""
        cache_path = Path(cache_dir) / f"{cache_key}.json"
        
        if cache_path.exists():
            cache_time = cache_path.stat().st_mtime
            return (datetime.now().timestamp() - cache_time) < cache_timeout
        
        return False


class DataExporter:
    """Export data and charts in various formats."""
    
    @staticmethod
    def export_to_csv(df: pd.DataFrame, filename: str):
        """Export DataFrame to CSV."""
        df.to_csv(filename, index=False)
    
    @staticmethod
    def export_to_excel(df: pd.DataFrame, filename: str, sheet_name: str = 'Data'):
        """Export DataFrame to Excel."""
        df.to_excel(filename, sheet_name=sheet_name, index=False)
    
    @staticmethod
    def export_chart_to_html(fig: go.Figure, filename: str):
        """Export Plotly chart to HTML."""
        fig.write_html(filename)
    
    @staticmethod
    def export_chart_to_image(fig: go.Figure, filename: str, format: str = 'png'):
        """Export Plotly chart to image."""
        fig.write_image(filename, format=format)
    
    @staticmethod
    def create_dashboard_report(data_dict: Dict[str, pd.DataFrame], 
                               charts_dict: Dict[str, go.Figure],
                               output_file: str = 'dashboard_report.html'):
        """Create a comprehensive dashboard report."""
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Dashboard Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .section { margin: 30px 0; }
                .chart { margin: 20px 0; }
                table { border-collapse: collapse; width: 100%; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
            </style>
        </head>
        <body>
            <h1>Dashboard Report</h1>
            <p>Generated on: {date}</p>
        """.format(date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        # Add data tables
        for name, df in data_dict.items():
            html_content += f"""
            <div class="section">
                <h2>Data: {name}</h2>
                {df.head(10).to_html(classes='data-table')}
                <p>Showing first 10 rows of {len(df)} total rows.</p>
            </div>
            """
        
        # Add charts
        for name, fig in charts_dict.items():
            chart_html = fig.to_html(include_plotlyjs='cdn', div_id=f'chart_{name}')
            html_content += f"""
            <div class="section">
                <h2>Chart: {name}</h2>
                <div class="chart">{chart_html}</div>
            </div>
            """
        
        html_content += """
        </body>
        </html>
        """
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)


# Utility functions
def create_sample_data(n_rows: int = 1000) -> pd.DataFrame:
    """Create sample data for testing dashboard components."""
    np.random.seed(42)
    
    dates = pd.date_range(start='2023-01-01', periods=n_rows, freq='D')
    categories = ['A', 'B', 'C', 'D', 'E']
    regions = ['North', 'South', 'East', 'West']
    
    data = {
        'date': np.random.choice(dates, n_rows),
        'category': np.random.choice(categories, n_rows),
        'region': np.random.choice(regions, n_rows),
        'value': np.random.normal(100, 20, n_rows),
        'quantity': np.random.poisson(10, n_rows),
        'price': np.random.gamma(2, 50, n_rows)
    }
    
    return pd.DataFrame(data)


def validate_data_for_chart(df: pd.DataFrame, chart_type: str, required_columns: List[str]) -> bool:
    """Validate that DataFrame has required columns for chart type."""
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        print(f"Warning: Missing columns for {chart_type}: {missing_columns}")
        return False
    
    return True


if __name__ == "__main__":
    # Example usage and testing
    print("Dashboard Utilities Module - Testing")
    print("=" * 50)
    
    # Test configuration
    config = DashboardConfig()
    print(f"Primary color: {config.get('theme.primary_color')}")
    
    # Create sample data
    sample_data = create_sample_data(500)
    print(f"Created sample data: {sample_data.shape}")
    
    # Test chart factory
    chart_factory = ChartFactory(config)
    
    # Create various charts
    line_chart = chart_factory.create_line_chart(
        sample_data, 'date', 'value', 'category'
    )
    
    bar_chart = chart_factory.create_bar_chart(
        sample_data.groupby('category')['value'].sum().reset_index(),
        'category', 'value'
    )
    
    scatter_plot = chart_factory.create_scatter_plot(
        sample_data, 'quantity', 'price', color_column='category'
    )
    
    print("Charts created successfully:")
    print("- Line chart")
    print("- Bar chart") 
    print("- Scatter plot")
    
    # Test KPI calculations
    values = sample_data['value'].tolist()
    growth_rate = KPICalculator.calculate_growth_rate(values[-1], values[0])
    trend = KPICalculator.calculate_trend(values)
    
    print(f"\nKPI Analysis:")
    print(f"Growth rate: {growth_rate:.2f}%")
    print(f"Trend: {trend}")
    
    # Test data processing
    processed_data = DataProcessor.clean_dataframe(sample_data)
    print(f"Data processed: {processed_data.shape}")
    
    print("\nAll tests completed successfully!")