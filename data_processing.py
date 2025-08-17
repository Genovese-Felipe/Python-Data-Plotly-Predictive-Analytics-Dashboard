"""
Data Processing and ETL Pipeline Module
Python Data Plotly Predictive Analytics Dashboard

This module provides comprehensive data processing and ETL capabilities:
- Data ingestion from multiple sources
- Data transformation and cleaning pipelines
- Data validation and quality checks
- Performance optimization
- Batch and streaming data processing
- Data pipeline orchestration
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any, Optional, Union, Callable
import sqlite3
import json
import csv
import os
from pathlib import Path
from datetime import datetime, timedelta
import logging
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time
from dataclasses import dataclass
from abc import ABC, abstractmethod
import hashlib
import pickle


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class DataPipelineConfig:
    """Configuration for data processing pipelines."""
    chunk_size: int = 10000
    max_workers: int = 4
    validation_enabled: bool = True
    error_threshold: float = 0.05
    output_format: str = 'parquet'
    compression: str = 'snappy'
    backup_enabled: bool = True
    retry_attempts: int = 3
    timeout_seconds: int = 300


class DataSource(ABC):
    """Abstract base class for data sources."""
    
    @abstractmethod
    def connect(self) -> bool:
        """Establish connection to data source."""
        pass
    
    @abstractmethod
    def read_data(self, query: str = None, **kwargs) -> pd.DataFrame:
        """Read data from source."""
        pass
    
    @abstractmethod
    def disconnect(self):
        """Close connection to data source."""
        pass


class CSVDataSource(DataSource):
    """CSV file data source implementation."""
    
    def __init__(self, file_path: str, delimiter: str = ',', encoding: str = 'utf-8'):
        """
        Initialize CSV data source.
        
        Args:
            file_path (str): Path to CSV file
            delimiter (str): CSV delimiter
            encoding (str): File encoding
        """
        self.file_path = file_path
        self.delimiter = delimiter
        self.encoding = encoding
        self.connected = False
    
    def connect(self) -> bool:
        """Check if CSV file exists and is readable."""
        try:
            self.connected = os.path.exists(self.file_path) and os.access(self.file_path, os.R_OK)
            return self.connected
        except Exception as e:
            logger.error(f"Failed to connect to CSV file {self.file_path}: {e}")
            return False
    
    def read_data(self, query: str = None, **kwargs) -> pd.DataFrame:
        """
        Read data from CSV file.
        
        Args:
            query (str): Not used for CSV files
            **kwargs: Additional pandas read_csv parameters
        
        Returns:
            pd.DataFrame: Loaded data
        """
        if not self.connected:
            raise ConnectionError("Not connected to data source")
        
        try:
            return pd.read_csv(
                self.file_path,
                delimiter=self.delimiter,
                encoding=self.encoding,
                **kwargs
            )
        except Exception as e:
            logger.error(f"Failed to read CSV file {self.file_path}: {e}")
            raise
    
    def disconnect(self):
        """Disconnect from CSV source."""
        self.connected = False


class SQLiteDataSource(DataSource):
    """SQLite database data source implementation."""
    
    def __init__(self, db_path: str):
        """
        Initialize SQLite data source.
        
        Args:
            db_path (str): Path to SQLite database file
        """
        self.db_path = db_path
        self.connection = None
    
    def connect(self) -> bool:
        """Connect to SQLite database."""
        try:
            self.connection = sqlite3.connect(self.db_path)
            return True
        except Exception as e:
            logger.error(f"Failed to connect to SQLite database {self.db_path}: {e}")
            return False
    
    def read_data(self, query: str = None, **kwargs) -> pd.DataFrame:
        """
        Read data from SQLite database.
        
        Args:
            query (str): SQL query to execute
            **kwargs: Additional pandas read_sql parameters
        
        Returns:
            pd.DataFrame: Query results
        """
        if not self.connection:
            raise ConnectionError("Not connected to database")
        
        if not query:
            raise ValueError("Query is required for database sources")
        
        try:
            return pd.read_sql(query, self.connection, **kwargs)
        except Exception as e:
            logger.error(f"Failed to execute query: {e}")
            raise
    
    def disconnect(self):
        """Disconnect from SQLite database."""
        if self.connection:
            self.connection.close()
            self.connection = None


class JSONDataSource(DataSource):
    """JSON file data source implementation."""
    
    def __init__(self, file_path: str, encoding: str = 'utf-8'):
        """
        Initialize JSON data source.
        
        Args:
            file_path (str): Path to JSON file
            encoding (str): File encoding
        """
        self.file_path = file_path
        self.encoding = encoding
        self.connected = False
    
    def connect(self) -> bool:
        """Check if JSON file exists and is readable."""
        try:
            self.connected = os.path.exists(self.file_path) and os.access(self.file_path, os.R_OK)
            return self.connected
        except Exception as e:
            logger.error(f"Failed to connect to JSON file {self.file_path}: {e}")
            return False
    
    def read_data(self, query: str = None, **kwargs) -> pd.DataFrame:
        """
        Read data from JSON file.
        
        Args:
            query (str): JSONPath query (not implemented)
            **kwargs: Additional pandas read_json parameters
        
        Returns:
            pd.DataFrame: Loaded data
        """
        if not self.connected:
            raise ConnectionError("Not connected to data source")
        
        try:
            return pd.read_json(self.file_path, encoding=self.encoding, **kwargs)
        except Exception as e:
            logger.error(f"Failed to read JSON file {self.file_path}: {e}")
            raise
    
    def disconnect(self):
        """Disconnect from JSON source."""
        self.connected = False


class DataValidator:
    """Data validation and quality assessment."""
    
    def __init__(self, config: DataPipelineConfig):
        """Initialize with pipeline configuration."""
        self.config = config
        self.validation_results = {}
    
    def validate_schema(self, 
                       df: pd.DataFrame, 
                       expected_schema: Dict[str, str]) -> Tuple[bool, List[str]]:
        """
        Validate DataFrame schema against expected schema.
        
        Args:
            df (pd.DataFrame): DataFrame to validate
            expected_schema (Dict[str, str]): Expected column types
        
        Returns:
            Tuple[bool, List[str]]: Validation success and error messages
        """
        errors = []
        
        # Check for missing columns
        expected_columns = set(expected_schema.keys())
        actual_columns = set(df.columns)
        missing_columns = expected_columns - actual_columns
        
        if missing_columns:
            errors.append(f"Missing columns: {missing_columns}")
        
        # Check data types
        for column, expected_type in expected_schema.items():
            if column in df.columns:
                actual_type = str(df[column].dtype)
                if not self._is_compatible_type(actual_type, expected_type):
                    errors.append(f"Column {column}: expected {expected_type}, got {actual_type}")
        
        return len(errors) == 0, errors
    
    def validate_data_quality(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Assess data quality metrics.
        
        Args:
            df (pd.DataFrame): DataFrame to assess
        
        Returns:
            Dict[str, Any]: Quality assessment results
        """
        total_cells = df.shape[0] * df.shape[1]
        missing_cells = df.isnull().sum().sum()
        duplicate_rows = df.duplicated().sum()
        
        quality_metrics = {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'total_cells': total_cells,
            'missing_cells': missing_cells,
            'missing_percentage': (missing_cells / total_cells) * 100 if total_cells > 0 else 0,
            'duplicate_rows': duplicate_rows,
            'duplicate_percentage': (duplicate_rows / len(df)) * 100 if len(df) > 0 else 0,
            'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024 / 1024,
            'data_types': df.dtypes.to_dict()
        }
        
        # Check for outliers in numerical columns
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        outlier_info = {}
        
        for col in numerical_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
            outlier_info[col] = {
                'count': len(outliers),
                'percentage': (len(outliers) / len(df)) * 100 if len(df) > 0 else 0
            }
        
        quality_metrics['outliers'] = outlier_info
        
        return quality_metrics
    
    def _is_compatible_type(self, actual_type: str, expected_type: str) -> bool:
        """Check if data types are compatible."""
        type_mappings = {
            'int': ['int64', 'int32', 'int16', 'int8', 'uint64', 'uint32', 'uint16', 'uint8'],
            'float': ['float64', 'float32'],
            'string': ['object', 'string'],
            'datetime': ['datetime64[ns]', 'datetime64'],
            'bool': ['bool']
        }
        
        expected_variants = type_mappings.get(expected_type, [expected_type])
        return actual_type in expected_variants


class DataTransformer:
    """Data transformation utilities."""
    
    @staticmethod
    def clean_text_columns(df: pd.DataFrame, 
                          columns: List[str] = None,
                          operations: List[str] = None) -> pd.DataFrame:
        """
        Clean text columns with various operations.
        
        Args:
            df (pd.DataFrame): Input DataFrame
            columns (List[str]): Columns to clean (default: all object columns)
            operations (List[str]): Operations to perform
        
        Returns:
            pd.DataFrame: DataFrame with cleaned text columns
        """
        df_clean = df.copy()
        
        if columns is None:
            columns = df_clean.select_dtypes(include=['object']).columns.tolist()
        
        if operations is None:
            operations = ['strip', 'lower', 'remove_special_chars']
        
        for col in columns:
            if col in df_clean.columns:
                if 'strip' in operations:
                    df_clean[col] = df_clean[col].astype(str).str.strip()
                
                if 'lower' in operations:
                    df_clean[col] = df_clean[col].str.lower()
                
                if 'upper' in operations:
                    df_clean[col] = df_clean[col].str.upper()
                
                if 'remove_special_chars' in operations:
                    df_clean[col] = df_clean[col].str.replace(r'[^\w\s]', '', regex=True)
                
                if 'remove_extra_spaces' in operations:
                    df_clean[col] = df_clean[col].str.replace(r'\s+', ' ', regex=True)
        
        return df_clean
    
    @staticmethod
    def normalize_numerical_columns(df: pd.DataFrame,
                                   columns: List[str] = None,
                                   method: str = 'minmax') -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Normalize numerical columns.
        
        Args:
            df (pd.DataFrame): Input DataFrame
            columns (List[str]): Columns to normalize
            method (str): Normalization method ('minmax', 'zscore', 'robust')
        
        Returns:
            Tuple[pd.DataFrame, Dict[str, Any]]: Normalized DataFrame and scaling parameters
        """
        df_norm = df.copy()
        scaling_params = {}
        
        if columns is None:
            columns = df_norm.select_dtypes(include=[np.number]).columns.tolist()
        
        for col in columns:
            if col in df_norm.columns:
                if method == 'minmax':
                    min_val = df_norm[col].min()
                    max_val = df_norm[col].max()
                    df_norm[col] = (df_norm[col] - min_val) / (max_val - min_val)
                    scaling_params[col] = {'method': 'minmax', 'min': min_val, 'max': max_val}
                
                elif method == 'zscore':
                    mean_val = df_norm[col].mean()
                    std_val = df_norm[col].std()
                    df_norm[col] = (df_norm[col] - mean_val) / std_val
                    scaling_params[col] = {'method': 'zscore', 'mean': mean_val, 'std': std_val}
                
                elif method == 'robust':
                    median_val = df_norm[col].median()
                    mad_val = df_norm[col].mad()
                    df_norm[col] = (df_norm[col] - median_val) / mad_val
                    scaling_params[col] = {'method': 'robust', 'median': median_val, 'mad': mad_val}
        
        return df_norm, scaling_params
    
    @staticmethod
    def handle_missing_values(df: pd.DataFrame,
                             strategy: Dict[str, str] = None) -> pd.DataFrame:
        """
        Handle missing values with different strategies per column.
        
        Args:
            df (pd.DataFrame): Input DataFrame
            strategy (Dict[str, str]): Strategy per column
        
        Returns:
            pd.DataFrame: DataFrame with handled missing values
        """
        df_filled = df.copy()
        
        if strategy is None:
            strategy = {}
        
        for col in df_filled.columns:
            col_strategy = strategy.get(col, 'auto')
            
            if col_strategy == 'auto':
                if df_filled[col].dtype in ['int64', 'float64']:
                    col_strategy = 'mean'
                else:
                    col_strategy = 'mode'
            
            if col_strategy == 'mean':
                df_filled[col].fillna(df_filled[col].mean(), inplace=True)
            elif col_strategy == 'median':
                df_filled[col].fillna(df_filled[col].median(), inplace=True)
            elif col_strategy == 'mode':
                mode_value = df_filled[col].mode()
                if not mode_value.empty:
                    df_filled[col].fillna(mode_value.iloc[0], inplace=True)
            elif col_strategy == 'forward_fill':
                df_filled[col].fillna(method='ffill', inplace=True)
            elif col_strategy == 'backward_fill':
                df_filled[col].fillna(method='bfill', inplace=True)
            elif col_strategy == 'interpolate':
                df_filled[col].interpolate(inplace=True)
            elif isinstance(col_strategy, (str, int, float)):
                df_filled[col].fillna(col_strategy, inplace=True)
        
        return df_filled
    
    @staticmethod
    def create_derived_features(df: pd.DataFrame,
                               feature_definitions: Dict[str, str]) -> pd.DataFrame:
        """
        Create derived features based on expressions.
        
        Args:
            df (pd.DataFrame): Input DataFrame
            feature_definitions (Dict[str, str]): Feature name -> expression mapping
        
        Returns:
            pd.DataFrame: DataFrame with new features
        """
        df_features = df.copy()
        
        for feature_name, expression in feature_definitions.items():
            try:
                # Safely evaluate expression in DataFrame context
                df_features[feature_name] = df_features.eval(expression)
            except Exception as e:
                logger.warning(f"Failed to create feature {feature_name}: {e}")
        
        return df_features


class DataPipeline:
    """Main data processing pipeline orchestrator."""
    
    def __init__(self, config: DataPipelineConfig = None):
        """Initialize data pipeline with configuration."""
        self.config = config or DataPipelineConfig()
        self.validator = DataValidator(self.config)
        self.execution_history = []
        self.cache = {}
    
    def create_hash_key(self, *args) -> str:
        """Create hash key for caching."""
        key_string = '|'.join(str(arg) for arg in args)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def execute_pipeline(self,
                        data_source: DataSource,
                        transformations: List[Callable],
                        output_path: str = None,
                        validation_schema: Dict[str, str] = None) -> pd.DataFrame:
        """
        Execute complete data pipeline.
        
        Args:
            data_source (DataSource): Data source to read from
            transformations (List[Callable]): List of transformation functions
            output_path (str): Optional output file path
            validation_schema (Dict[str, str]): Schema validation rules
        
        Returns:
            pd.DataFrame: Processed data
        """
        pipeline_start = datetime.now()
        pipeline_id = self.create_hash_key(str(pipeline_start), str(transformations))
        
        try:
            # Step 1: Connect to data source
            logger.info(f"Pipeline {pipeline_id}: Connecting to data source")
            if not data_source.connect():
                raise ConnectionError("Failed to connect to data source")
            
            # Step 2: Read data
            logger.info(f"Pipeline {pipeline_id}: Reading data")
            df = data_source.read_data()
            logger.info(f"Pipeline {pipeline_id}: Loaded {len(df)} rows, {len(df.columns)} columns")
            
            # Step 3: Validate schema if provided
            if validation_schema and self.config.validation_enabled:
                logger.info(f"Pipeline {pipeline_id}: Validating schema")
                is_valid, errors = self.validator.validate_schema(df, validation_schema)
                if not is_valid:
                    logger.error(f"Schema validation failed: {errors}")
                    raise ValueError(f"Schema validation failed: {errors}")
            
            # Step 4: Apply transformations
            logger.info(f"Pipeline {pipeline_id}: Applying {len(transformations)} transformations")
            for i, transform_func in enumerate(transformations):
                try:
                    df = transform_func(df)
                    logger.info(f"Pipeline {pipeline_id}: Transformation {i+1} completed")
                except Exception as e:
                    logger.error(f"Pipeline {pipeline_id}: Transformation {i+1} failed: {e}")
                    if self.config.retry_attempts > 0:
                        # Retry logic could be implemented here
                        pass
                    raise
            
            # Step 5: Final validation
            if self.config.validation_enabled:
                logger.info(f"Pipeline {pipeline_id}: Final data quality check")
                quality_metrics = self.validator.validate_data_quality(df)
                
                error_rate = quality_metrics['missing_percentage'] / 100
                if error_rate > self.config.error_threshold:
                    logger.warning(f"Data quality below threshold: {error_rate:.2%} errors")
            
            # Step 6: Save output if specified
            if output_path:
                logger.info(f"Pipeline {pipeline_id}: Saving output to {output_path}")
                self._save_output(df, output_path)
            
            # Step 7: Record execution
            execution_time = (datetime.now() - pipeline_start).total_seconds()
            execution_record = {
                'pipeline_id': pipeline_id,
                'start_time': pipeline_start,
                'execution_time': execution_time,
                'input_rows': len(df),
                'output_rows': len(df),
                'transformations': len(transformations),
                'status': 'success'
            }
            self.execution_history.append(execution_record)
            
            logger.info(f"Pipeline {pipeline_id}: Completed successfully in {execution_time:.2f}s")
            return df
            
        except Exception as e:
            # Record failed execution
            execution_time = (datetime.now() - pipeline_start).total_seconds()
            execution_record = {
                'pipeline_id': pipeline_id,
                'start_time': pipeline_start,
                'execution_time': execution_time,
                'error': str(e),
                'status': 'failed'
            }
            self.execution_history.append(execution_record)
            
            logger.error(f"Pipeline {pipeline_id}: Failed after {execution_time:.2f}s: {e}")
            raise
            
        finally:
            # Always disconnect from data source
            data_source.disconnect()
    
    def _save_output(self, df: pd.DataFrame, output_path: str):
        """Save DataFrame to specified output path."""
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        # Create backup if enabled
        if self.config.backup_enabled and os.path.exists(output_path):
            backup_path = f"{output_path}.backup.{int(time.time())}"
            os.rename(output_path, backup_path)
            logger.info(f"Created backup: {backup_path}")
        
        # Save in specified format
        if self.config.output_format == 'csv':
            df.to_csv(output_path, index=False)
        elif self.config.output_format == 'parquet':
            df.to_parquet(output_path, compression=self.config.compression)
        elif self.config.output_format == 'json':
            df.to_json(output_path, orient='records')
        elif self.config.output_format == 'excel':
            df.to_excel(output_path, index=False)
        else:
            raise ValueError(f"Unsupported output format: {self.config.output_format}")
    
    def process_in_chunks(self,
                         data_source: DataSource,
                         transformation_func: Callable,
                         output_path: str = None) -> pd.DataFrame:
        """
        Process large datasets in chunks.
        
        Args:
            data_source (DataSource): Data source
            transformation_func (Callable): Single transformation function
            output_path (str): Optional output path
        
        Returns:
            pd.DataFrame: Processed data (concatenated chunks)
        """
        if not data_source.connect():
            raise ConnectionError("Failed to connect to data source")
        
        try:
            processed_chunks = []
            chunk_number = 0
            
            # For CSV sources, we can use chunking
            if isinstance(data_source, CSVDataSource):
                chunk_reader = pd.read_csv(
                    data_source.file_path,
                    chunksize=self.config.chunk_size,
                    delimiter=data_source.delimiter,
                    encoding=data_source.encoding
                )
                
                for chunk in chunk_reader:
                    logger.info(f"Processing chunk {chunk_number + 1}")
                    processed_chunk = transformation_func(chunk)
                    processed_chunks.append(processed_chunk)
                    chunk_number += 1
            else:
                # For other sources, load all data and split manually
                df = data_source.read_data()
                total_chunks = len(df) // self.config.chunk_size + 1
                
                for i in range(0, len(df), self.config.chunk_size):
                    chunk = df.iloc[i:i + self.config.chunk_size]
                    logger.info(f"Processing chunk {chunk_number + 1}/{total_chunks}")
                    processed_chunk = transformation_func(chunk)
                    processed_chunks.append(processed_chunk)
                    chunk_number += 1
            
            # Concatenate all processed chunks
            result = pd.concat(processed_chunks, ignore_index=True)
            
            if output_path:
                self._save_output(result, output_path)
            
            return result
            
        finally:
            data_source.disconnect()
    
    def parallel_processing(self,
                           data_sources: List[DataSource],
                           transformation_func: Callable,
                           combine_func: Callable = None) -> pd.DataFrame:
        """
        Process multiple data sources in parallel.
        
        Args:
            data_sources (List[DataSource]): List of data sources
            transformation_func (Callable): Transformation function
            combine_func (Callable): Function to combine results
        
        Returns:
            pd.DataFrame: Combined processed data
        """
        if combine_func is None:
            combine_func = lambda dfs: pd.concat(dfs, ignore_index=True)
        
        def process_source(source):
            if source.connect():
                try:
                    df = source.read_data()
                    return transformation_func(df)
                finally:
                    source.disconnect()
            return pd.DataFrame()
        
        with ThreadPoolExecutor(max_workers=self.config.max_workers) as executor:
            results = list(executor.map(process_source, data_sources))
        
        # Filter out empty DataFrames
        valid_results = [df for df in results if not df.empty]
        
        if valid_results:
            return combine_func(valid_results)
        else:
            return pd.DataFrame()
    
    def get_execution_summary(self) -> Dict[str, Any]:
        """Get summary of pipeline executions."""
        if not self.execution_history:
            return {'message': 'No executions recorded'}
        
        successful_runs = [r for r in self.execution_history if r['status'] == 'success']
        failed_runs = [r for r in self.execution_history if r['status'] == 'failed']
        
        return {
            'total_executions': len(self.execution_history),
            'successful_executions': len(successful_runs),
            'failed_executions': len(failed_runs),
            'success_rate': len(successful_runs) / len(self.execution_history) * 100,
            'average_execution_time': np.mean([r['execution_time'] for r in successful_runs]) if successful_runs else 0,
            'total_processing_time': sum(r['execution_time'] for r in self.execution_history),
            'last_execution': self.execution_history[-1] if self.execution_history else None
        }


# Utility functions for common transformations
def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicate rows from DataFrame."""
    return df.drop_duplicates()


def filter_outliers(df: pd.DataFrame, columns: List[str] = None, method: str = 'iqr') -> pd.DataFrame:
    """Filter outliers from numerical columns."""
    df_filtered = df.copy()
    
    if columns is None:
        columns = df_filtered.select_dtypes(include=[np.number]).columns.tolist()
    
    for col in columns:
        if method == 'iqr':
            Q1 = df_filtered[col].quantile(0.25)
            Q3 = df_filtered[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            df_filtered = df_filtered[(df_filtered[col] >= lower_bound) & (df_filtered[col] <= upper_bound)]
        elif method == 'zscore':
            z_scores = np.abs((df_filtered[col] - df_filtered[col].mean()) / df_filtered[col].std())
            df_filtered = df_filtered[z_scores < 3]
    
    return df_filtered


def add_datetime_features(df: pd.DataFrame, date_column: str) -> pd.DataFrame:
    """Add datetime-based features."""
    df_features = df.copy()
    
    # Ensure datetime type
    df_features[date_column] = pd.to_datetime(df_features[date_column])
    
    # Extract features
    df_features[f'{date_column}_year'] = df_features[date_column].dt.year
    df_features[f'{date_column}_month'] = df_features[date_column].dt.month
    df_features[f'{date_column}_day'] = df_features[date_column].dt.day
    df_features[f'{date_column}_dayofweek'] = df_features[date_column].dt.dayofweek
    df_features[f'{date_column}_quarter'] = df_features[date_column].dt.quarter
    df_features[f'{date_column}_is_weekend'] = df_features[date_column].dt.dayofweek.isin([5, 6])
    
    return df_features


def create_sample_data_source() -> CSVDataSource:
    """Create a sample CSV data source for testing."""
    # Create sample data
    sample_data = pd.DataFrame({
        'id': range(1, 1001),
        'name': [f'User_{i}' for i in range(1, 1001)],
        'age': np.random.randint(18, 80, 1000),
        'score': np.random.normal(75, 15, 1000),
        'category': np.random.choice(['A', 'B', 'C'], 1000),
        'date': pd.date_range('2023-01-01', periods=1000, freq='H')
    })
    
    # Save to temporary CSV
    temp_file = '/tmp/sample_data.csv'
    sample_data.to_csv(temp_file, index=False)
    
    return CSVDataSource(temp_file)


if __name__ == "__main__":
    # Example usage and testing
    print("Data Processing and ETL Pipeline Module - Testing")
    print("=" * 60)
    
    # Create sample data source
    data_source = create_sample_data_source()
    print("Sample data source created")
    
    # Configure pipeline
    config = DataPipelineConfig(
        chunk_size=100,
        validation_enabled=True,
        output_format='csv'
    )
    
    # Create pipeline
    pipeline = DataPipeline(config)
    
    # Define transformations
    transformations = [
        remove_duplicates,
        lambda df: DataTransformer.clean_text_columns(df, ['name']),
        lambda df: add_datetime_features(df, 'date'),
        lambda df: filter_outliers(df, ['age', 'score'])
    ]
    
    # Execute pipeline
    try:
        result = pipeline.execute_pipeline(
            data_source=data_source,
            transformations=transformations,
            output_path='/tmp/processed_data.csv'
        )
        
        print(f"Pipeline executed successfully!")
        print(f"Input: 1000 rows -> Output: {len(result)} rows")
        print(f"Columns: {list(result.columns)}")
        
        # Test chunk processing
        chunk_result = pipeline.process_in_chunks(
            data_source=create_sample_data_source(),
            transformation_func=lambda df: df[df['age'] > 30]
        )
        print(f"Chunk processing: {len(chunk_result)} rows processed")
        
        # Get execution summary
        summary = pipeline.get_execution_summary()
        print(f"Execution summary: {summary['total_executions']} runs, {summary['success_rate']:.1f}% success rate")
        
    except Exception as e:
        print(f"Pipeline execution failed: {e}")
    
    # Test individual components
    print("\nTesting individual components:")
    
    # Test data validator
    validator = DataValidator(config)
    sample_df = pd.DataFrame({
        'id': [1, 2, 3],
        'name': ['A', 'B', 'C'],
        'value': [1.0, 2.0, 3.0]
    })
    
    schema = {'id': 'int', 'name': 'string', 'value': 'float'}
    is_valid, errors = validator.validate_schema(sample_df, schema)
    print(f"Schema validation: {'PASS' if is_valid else 'FAIL'}")
    
    quality_metrics = validator.validate_data_quality(sample_df)
    print(f"Data quality: {quality_metrics['missing_percentage']:.1f}% missing values")
    
    # Test data transformer
    transformer = DataTransformer()
    normalized_df, params = transformer.normalize_numerical_columns(sample_df, ['value'])
    print(f"Normalization: {params}")
    
    print("\nAll tests completed successfully!")