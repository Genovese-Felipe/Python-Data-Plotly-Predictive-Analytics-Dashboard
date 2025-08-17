"""
Advanced Data Analytics Module
Python Data Plotly Predictive Analytics Dashboard

This module provides comprehensive data analysis capabilities including:
- Statistical analysis and data profiling
- Machine learning model implementations
- Advanced data preprocessing utilities
- Time series analysis
- Data validation and quality assessment
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import accuracy_score, mean_squared_error, classification_report
from sklearn.cluster import KMeans
from scipy import stats
import warnings
warnings.filterwarnings('ignore')


class DataProfiler:
    """Comprehensive data profiling and analysis class."""
    
    def __init__(self, dataframe):
        """
        Initialize the DataProfiler with a pandas DataFrame.
        
        Args:
            dataframe (pd.DataFrame): The dataset to profile
        """
        self.df = dataframe.copy()
        self.profile = {}
        
    def generate_profile(self):
        """Generate comprehensive data profile."""
        self.profile = {
            'basic_info': self._basic_info(),
            'missing_values': self._missing_values_analysis(),
            'numerical_summary': self._numerical_summary(),
            'categorical_summary': self._categorical_summary(),
            'data_types': self._data_types_analysis(),
            'correlation_analysis': self._correlation_analysis(),
            'outlier_detection': self._outlier_detection()
        }
        return self.profile
    
    def _basic_info(self):
        """Basic dataset information."""
        return {
            'shape': self.df.shape,
            'memory_usage': self.df.memory_usage(deep=True).sum(),
            'columns': list(self.df.columns),
            'dtypes': self.df.dtypes.to_dict()
        }
    
    def _missing_values_analysis(self):
        """Analyze missing values."""
        missing = self.df.isnull().sum()
        missing_percent = (missing / len(self.df)) * 100
        return {
            'total_missing': missing.sum(),
            'missing_by_column': missing.to_dict(),
            'missing_percentage': missing_percent.to_dict(),
            'complete_rows': len(self.df) - len(self.df[self.df.isnull().any(axis=1)])
        }
    
    def _numerical_summary(self):
        """Statistical summary for numerical columns."""
        numerical_cols = self.df.select_dtypes(include=[np.number]).columns
        summary = {}
        
        for col in numerical_cols:
            summary[col] = {
                'mean': self.df[col].mean(),
                'median': self.df[col].median(),
                'std': self.df[col].std(),
                'min': self.df[col].min(),
                'max': self.df[col].max(),
                'q25': self.df[col].quantile(0.25),
                'q75': self.df[col].quantile(0.75),
                'skewness': stats.skew(self.df[col].dropna()),
                'kurtosis': stats.kurtosis(self.df[col].dropna())
            }
        
        return summary
    
    def _categorical_summary(self):
        """Summary for categorical columns."""
        categorical_cols = self.df.select_dtypes(include=['object', 'category']).columns
        summary = {}
        
        for col in categorical_cols:
            summary[col] = {
                'unique_count': self.df[col].nunique(),
                'unique_values': self.df[col].unique().tolist()[:20],  # First 20 unique values
                'value_counts': self.df[col].value_counts().head(10).to_dict(),
                'mode': self.df[col].mode().iloc[0] if not self.df[col].mode().empty else None
            }
        
        return summary
    
    def _data_types_analysis(self):
        """Analyze data types and suggest optimizations."""
        type_analysis = {}
        
        for col in self.df.columns:
            dtype = str(self.df[col].dtype)
            unique_count = self.df[col].nunique()
            null_count = self.df[col].isnull().sum()
            
            type_analysis[col] = {
                'current_type': dtype,
                'unique_values': unique_count,
                'null_values': null_count,
                'suggested_type': self._suggest_optimal_type(col, dtype, unique_count)
            }
        
        return type_analysis
    
    def _suggest_optimal_type(self, column, current_type, unique_count):
        """Suggest optimal data type for memory efficiency."""
        if 'int' in current_type:
            max_val = self.df[column].max()
            min_val = self.df[column].min()
            
            if min_val >= 0:
                if max_val < 256:
                    return 'uint8'
                elif max_val < 65536:
                    return 'uint16'
                elif max_val < 4294967296:
                    return 'uint32'
            else:
                if -128 <= min_val and max_val < 128:
                    return 'int8'
                elif -32768 <= min_val and max_val < 32768:
                    return 'int16'
                elif -2147483648 <= min_val and max_val < 2147483648:
                    return 'int32'
        
        elif 'float' in current_type:
            return 'float32' if self.df[column].max() < 3.4e38 else 'float64'
        
        elif current_type == 'object' and unique_count < len(self.df) * 0.5:
            return 'category'
        
        return current_type
    
    def _correlation_analysis(self):
        """Analyze correlations between numerical variables."""
        numerical_df = self.df.select_dtypes(include=[np.number])
        
        if len(numerical_df.columns) < 2:
            return {'message': 'Insufficient numerical columns for correlation analysis'}
        
        correlation_matrix = numerical_df.corr()
        
        # Find strong correlations
        strong_correlations = []
        for i in range(len(correlation_matrix.columns)):
            for j in range(i+1, len(correlation_matrix.columns)):
                corr_value = correlation_matrix.iloc[i, j]
                if abs(corr_value) > 0.7:
                    strong_correlations.append({
                        'variable1': correlation_matrix.columns[i],
                        'variable2': correlation_matrix.columns[j],
                        'correlation': corr_value
                    })
        
        return {
            'correlation_matrix': correlation_matrix.to_dict(),
            'strong_correlations': strong_correlations
        }
    
    def _outlier_detection(self):
        """Detect outliers using IQR method."""
        numerical_cols = self.df.select_dtypes(include=[np.number]).columns
        outliers = {}
        
        for col in numerical_cols:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outlier_indices = self.df[(self.df[col] < lower_bound) | (self.df[col] > upper_bound)].index
            
            outliers[col] = {
                'count': len(outlier_indices),
                'percentage': (len(outlier_indices) / len(self.df)) * 100,
                'lower_bound': lower_bound,
                'upper_bound': upper_bound
            }
        
        return outliers


class MachineLearningPipeline:
    """Complete ML pipeline for classification and regression tasks."""
    
    def __init__(self, data, target_column):
        """
        Initialize ML pipeline.
        
        Args:
            data (pd.DataFrame): The dataset
            target_column (str): Name of the target variable
        """
        self.data = data.copy()
        self.target = target_column
        self.features = None
        self.X = None
        self.y = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.models = {}
        self.predictions = {}
        self.metrics = {}
        
    def preprocess_data(self, test_size=0.2, random_state=42):
        """Preprocess the data for ML training."""
        # Separate features and target
        self.y = self.data[self.target]
        self.X = self.data.drop(columns=[self.target])
        
        # Handle categorical variables
        categorical_cols = self.X.select_dtypes(include=['object', 'category']).columns
        for col in categorical_cols:
            le = LabelEncoder()
            self.X[col] = le.fit_transform(self.X[col].astype(str))
        
        # Handle missing values
        self.X = self.X.fillna(self.X.mean())
        
        # Split the data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=test_size, random_state=random_state
        )
        
        # Scale features
        self.scaler = StandardScaler()
        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.X_test_scaled = self.scaler.transform(self.X_test)
        
        return {
            'train_shape': self.X_train.shape,
            'test_shape': self.X_test.shape,
            'features': list(self.X.columns)
        }
    
    def train_classification_models(self):
        """Train multiple classification models."""
        # Random Forest
        rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
        rf_model.fit(self.X_train_scaled, self.y_train)
        self.models['random_forest'] = rf_model
        
        # Logistic Regression
        lr_model = LogisticRegression(random_state=42, max_iter=1000)
        lr_model.fit(self.X_train_scaled, self.y_train)
        self.models['logistic_regression'] = lr_model
        
        return list(self.models.keys())
    
    def train_regression_models(self):
        """Train multiple regression models."""
        # Random Forest Regressor
        rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
        rf_model.fit(self.X_train_scaled, self.y_train)
        self.models['random_forest_regressor'] = rf_model
        
        # Linear Regression
        lr_model = LinearRegression()
        lr_model.fit(self.X_train_scaled, self.y_train)
        self.models['linear_regression'] = lr_model
        
        return list(self.models.keys())
    
    def evaluate_models(self):
        """Evaluate all trained models."""
        for model_name, model in self.models.items():
            predictions = model.predict(self.X_test_scaled)
            self.predictions[model_name] = predictions
            
            # Determine if classification or regression
            if hasattr(model, 'predict_proba'):  # Classification
                accuracy = accuracy_score(self.y_test, predictions)
                report = classification_report(self.y_test, predictions, output_dict=True)
                
                self.metrics[model_name] = {
                    'accuracy': accuracy,
                    'classification_report': report
                }
            else:  # Regression
                mse = mean_squared_error(self.y_test, predictions)
                rmse = np.sqrt(mse)
                
                self.metrics[model_name] = {
                    'mse': mse,
                    'rmse': rmse,
                    'r2_score': model.score(self.X_test_scaled, self.y_test)
                }
        
        return self.metrics
    
    def get_feature_importance(self):
        """Get feature importance for tree-based models."""
        importance_data = {}
        
        for model_name, model in self.models.items():
            if hasattr(model, 'feature_importances_'):
                importance_dict = dict(zip(self.X.columns, model.feature_importances_))
                # Sort by importance
                importance_data[model_name] = dict(
                    sorted(importance_dict.items(), key=lambda x: x[1], reverse=True)
                )
        
        return importance_data


class TimeSeriesAnalyzer:
    """Time series analysis and forecasting utilities."""
    
    def __init__(self, data, date_column, value_column):
        """
        Initialize time series analyzer.
        
        Args:
            data (pd.DataFrame): The dataset
            date_column (str): Name of the date column
            value_column (str): Name of the value column
        """
        self.data = data.copy()
        self.date_col = date_column
        self.value_col = value_column
        self._prepare_data()
        
    def _prepare_data(self):
        """Prepare time series data."""
        self.data[self.date_col] = pd.to_datetime(self.data[self.date_col])
        self.data = self.data.sort_values(self.date_col)
        self.data.set_index(self.date_col, inplace=True)
        
    def decompose_series(self):
        """Decompose time series into trend, seasonal, and residual components."""
        from statsmodels.tsa.seasonal import seasonal_decompose
        
        decomposition = seasonal_decompose(
            self.data[self.value_col].dropna(), 
            model='additive', 
            period=12  # Assuming monthly data
        )
        
        return {
            'trend': decomposition.trend.dropna().to_dict(),
            'seasonal': decomposition.seasonal.dropna().to_dict(),
            'residual': decomposition.resid.dropna().to_dict()
        }
    
    def calculate_moving_averages(self, windows=[7, 30, 90]):
        """Calculate moving averages for different windows."""
        ma_data = {}
        
        for window in windows:
            ma_data[f'MA_{window}'] = self.data[self.value_col].rolling(window=window).mean().to_dict()
        
        return ma_data
    
    def detect_anomalies(self, threshold=2):
        """Detect anomalies using z-score method."""
        z_scores = np.abs(stats.zscore(self.data[self.value_col].dropna()))
        anomalies = self.data[z_scores > threshold]
        
        return {
            'anomaly_count': len(anomalies),
            'anomaly_dates': anomalies.index.strftime('%Y-%m-%d').tolist(),
            'anomaly_values': anomalies[self.value_col].tolist()
        }


class DataQualityAssessment:
    """Comprehensive data quality assessment tools."""
    
    def __init__(self, dataframe):
        """Initialize with a pandas DataFrame."""
        self.df = dataframe.copy()
        
    def assess_quality(self):
        """Perform comprehensive data quality assessment."""
        assessment = {
            'completeness': self._assess_completeness(),
            'consistency': self._assess_consistency(),
            'validity': self._assess_validity(),
            'accuracy': self._assess_accuracy(),
            'uniqueness': self._assess_uniqueness()
        }
        
        # Calculate overall score
        scores = [assessment[key]['score'] for key in assessment if 'score' in assessment[key]]
        assessment['overall_score'] = np.mean(scores) if scores else 0
        
        return assessment
    
    def _assess_completeness(self):
        """Assess data completeness."""
        total_cells = self.df.shape[0] * self.df.shape[1]
        missing_cells = self.df.isnull().sum().sum()
        completeness_score = ((total_cells - missing_cells) / total_cells) * 100
        
        return {
            'score': completeness_score,
            'total_cells': total_cells,
            'missing_cells': missing_cells,
            'details': self.df.isnull().sum().to_dict()
        }
    
    def _assess_consistency(self):
        """Assess data consistency."""
        consistency_issues = []
        
        # Check for mixed data types in object columns
        for col in self.df.select_dtypes(include=['object']).columns:
            unique_types = set(type(x).__name__ for x in self.df[col].dropna())
            if len(unique_types) > 1:
                consistency_issues.append(f"Mixed types in {col}: {unique_types}")
        
        # Check for case inconsistencies
        for col in self.df.select_dtypes(include=['object']).columns:
            values = self.df[col].dropna().astype(str)
            lower_count = values.str.islower().sum()
            upper_count = values.str.isupper().sum()
            mixed_case = len(values) - lower_count - upper_count
            
            if mixed_case > 0 and lower_count > 0 and upper_count > 0:
                consistency_issues.append(f"Inconsistent case in {col}")
        
        consistency_score = max(0, 100 - len(consistency_issues) * 10)
        
        return {
            'score': consistency_score,
            'issues': consistency_issues
        }
    
    def _assess_validity(self):
        """Assess data validity."""
        validity_issues = []
        
        # Check for negative values in columns that shouldn't have them
        numerical_cols = self.df.select_dtypes(include=[np.number]).columns
        for col in numerical_cols:
            if col.lower() in ['age', 'price', 'count', 'quantity']:
                negative_count = (self.df[col] < 0).sum()
                if negative_count > 0:
                    validity_issues.append(f"Negative values in {col}: {negative_count}")
        
        # Check for outliers
        for col in numerical_cols:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = ((self.df[col] < (Q1 - 1.5 * IQR)) | 
                       (self.df[col] > (Q3 + 1.5 * IQR))).sum()
            
            if outliers > len(self.df) * 0.1:  # More than 10% outliers
                validity_issues.append(f"High outlier percentage in {col}: {outliers/len(self.df)*100:.1f}%")
        
        validity_score = max(0, 100 - len(validity_issues) * 15)
        
        return {
            'score': validity_score,
            'issues': validity_issues
        }
    
    def _assess_accuracy(self):
        """Assess data accuracy (basic checks)."""
        accuracy_issues = []
        
        # Check for impossible dates
        date_cols = self.df.select_dtypes(include=['datetime64']).columns
        for col in date_cols:
            future_dates = (self.df[col] > pd.Timestamp.now()).sum()
            very_old_dates = (self.df[col] < pd.Timestamp('1900-01-01')).sum()
            
            if future_dates > 0:
                accuracy_issues.append(f"Future dates in {col}: {future_dates}")
            if very_old_dates > 0:
                accuracy_issues.append(f"Very old dates in {col}: {very_old_dates}")
        
        accuracy_score = max(0, 100 - len(accuracy_issues) * 20)
        
        return {
            'score': accuracy_score,
            'issues': accuracy_issues
        }
    
    def _assess_uniqueness(self):
        """Assess data uniqueness."""
        duplicate_rows = self.df.duplicated().sum()
        uniqueness_score = ((len(self.df) - duplicate_rows) / len(self.df)) * 100
        
        # Check for columns that should be unique
        uniqueness_issues = []
        for col in self.df.columns:
            if col.lower() in ['id', 'email', 'phone', 'username']:
                duplicates = self.df[col].duplicated().sum()
                if duplicates > 0:
                    uniqueness_issues.append(f"Duplicates in {col}: {duplicates}")
        
        return {
            'score': uniqueness_score,
            'duplicate_rows': duplicate_rows,
            'issues': uniqueness_issues
        }


# Utility functions for common data operations
def optimize_dataframe_memory(df):
    """Optimize DataFrame memory usage by converting to optimal data types."""
    optimized_df = df.copy()
    
    for col in optimized_df.columns:
        col_type = optimized_df[col].dtype
        
        if col_type != 'object':
            c_min = optimized_df[col].min()
            c_max = optimized_df[col].max()
            
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    optimized_df[col] = optimized_df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    optimized_df[col] = optimized_df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    optimized_df[col] = optimized_df[col].astype(np.int32)
            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    optimized_df[col] = optimized_df[col].astype(np.float32)
        else:
            if optimized_df[col].nunique() / len(optimized_df) < 0.5:
                optimized_df[col] = optimized_df[col].astype('category')
    
    return optimized_df


def generate_synthetic_data(n_samples=1000, n_features=10, problem_type='classification'):
    """Generate synthetic data for testing ML pipelines."""
    from sklearn.datasets import make_classification, make_regression
    
    if problem_type == 'classification':
        X, y = make_classification(
            n_samples=n_samples,
            n_features=n_features,
            n_informative=n_features//2,
            n_redundant=0,
            random_state=42
        )
    else:
        X, y = make_regression(
            n_samples=n_samples,
            n_features=n_features,
            noise=0.1,
            random_state=42
        )
    
    # Create DataFrame
    feature_names = [f'feature_{i}' for i in range(n_features)]
    df = pd.DataFrame(X, columns=feature_names)
    df['target'] = y
    
    return df


if __name__ == "__main__":
    # Example usage and testing
    print("Advanced Data Analytics Module - Testing")
    print("=" * 50)
    
    # Generate sample data
    sample_data = generate_synthetic_data(1000, 8, 'classification')
    print(f"Generated sample data: {sample_data.shape}")
    
    # Test DataProfiler
    profiler = DataProfiler(sample_data)
    profile = profiler.generate_profile()
    print(f"Data profiling completed: {len(profile)} sections analyzed")
    
    # Test ML Pipeline
    ml_pipeline = MachineLearningPipeline(sample_data, 'target')
    ml_pipeline.preprocess_data()
    models = ml_pipeline.train_classification_models()
    metrics = ml_pipeline.evaluate_models()
    print(f"ML models trained: {models}")
    
    # Test Data Quality Assessment
    quality_assessor = DataQualityAssessment(sample_data)
    quality_report = quality_assessor.assess_quality()
    print(f"Data quality score: {quality_report['overall_score']:.2f}/100")
    
    print("All tests completed successfully!")