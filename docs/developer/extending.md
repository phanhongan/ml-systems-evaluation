# Extending the Framework

This guide explains how to extend the ML Systems Evaluation Framework with custom components, including collectors, evaluators, reports, and data sources.

## Overview

The framework is designed to be highly extensible, allowing you to create custom components that integrate seamlessly with the existing system. All custom components follow a consistent interface pattern and can be easily integrated into your configurations.

## Extension Points

### 1. Custom Collectors
### 2. Custom Evaluators
### 3. Custom Reports
### 4. Custom Data Sources
### 5. Custom Templates

## Custom Collectors

### Overview

Collectors are responsible for gathering data from various sources. You can create custom collectors to handle specific data sources or collection methods.

### Base Collector Interface

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import pandas as pd

class BaseCollector(ABC):
    """Base class for all collectors."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the collector with configuration."""
        self.config = config
        self.name = config.get('name', 'unnamed_collector')
        self.data_source = config.get('data_source')
        self.metrics = config.get('metrics', [])
    
    @abstractmethod
    def collect(self, start_date: Optional[str] = None, 
                end_date: Optional[str] = None) -> pd.DataFrame:
        """Collect data from the configured source."""
        pass
    
    @abstractmethod
    def validate_connection(self) -> bool:
        """Validate connection to the data source."""
        pass
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get metadata about the collected data."""
        return {
            'collector_name': self.name,
            'data_source': self.data_source,
            'metrics': self.metrics,
            'collection_timestamp': pd.Timestamp.now().isoformat()
        }
```

### Example: Custom Database Collector

```python
import pandas as pd
import sqlalchemy as sa
from ml_eval.collectors.base import BaseCollector

class CustomDatabaseCollector(BaseCollector):
    """Custom collector for a specific database schema."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.connection_string = config['connection']
        self.table_name = config['table']
        self.engine = None
    
    def validate_connection(self) -> bool:
        """Test database connection."""
        try:
            self.engine = sa.create_engine(self.connection_string)
            with self.engine.connect() as conn:
                conn.execute(sa.text("SELECT 1"))
            return True
        except Exception as e:
            print(f"Connection validation failed: {e}")
            return False
    
    def collect(self, start_date: Optional[str] = None, 
                end_date: Optional[str] = None) -> pd.DataFrame:
        """Collect data from the database."""
        if not self.engine:
            self.engine = sa.create_engine(self.connection_string)
        
        # Build query based on configuration
        query = f"SELECT * FROM {self.table_name}"
        conditions = []
        
        if start_date:
            conditions.append(f"timestamp >= '{start_date}'")
        if end_date:
            conditions.append(f"timestamp <= '{end_date}'")
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        # Execute query
        df = pd.read_sql(query, self.engine)
        
        # Add metadata
        df['_collector_name'] = self.name
        df['_collection_timestamp'] = pd.Timestamp.now()
        
        return df
```

### Example: Custom API Collector

```python
import requests
import pandas as pd
from ml_eval.collectors.base import BaseCollector

class CustomAPICollector(BaseCollector):
    """Custom collector for REST API endpoints."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_url = config['url']
        self.headers = config.get('headers', {})
        self.auth_token = config.get('auth_token')
    
    def validate_connection(self) -> bool:
        """Test API connection."""
        try:
            headers = self.headers.copy()
            if self.auth_token:
                headers['Authorization'] = f"Bearer {self.auth_token}"
            
            response = requests.get(f"{self.api_url}/health", headers=headers)
            return response.status_code == 200
        except Exception as e:
            print(f"API connection validation failed: {e}")
            return False
    
    def collect(self, start_date: Optional[str] = None, 
                end_date: Optional[str] = None) -> pd.DataFrame:
        """Collect data from the API."""
        headers = self.headers.copy()
        if self.auth_token:
            headers['Authorization'] = f"Bearer {self.auth_token}"
        
        # Build request parameters
        params = {}
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date
        
        # Make API request
        response = requests.get(self.api_url, headers=headers, params=params)
        response.raise_for_status()
        
        # Convert response to DataFrame
        data = response.json()
        df = pd.DataFrame(data)
        
        # Add metadata
        df['_collector_name'] = self.name
        df['_collection_timestamp'] = pd.Timestamp.now()
        
        return df
```

### Registering Custom Collectors

```python
from ml_eval.collectors.registry import CollectorRegistry

# Register your custom collector
CollectorRegistry.register('custom_database', CustomDatabaseCollector)
CollectorRegistry.register('custom_api', CustomAPICollector)
```

## Custom Evaluators

### Overview

Evaluators analyze collected data and produce evaluation results. You can create custom evaluators for specific analysis needs.

### Base Evaluator Interface

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, List
import pandas as pd

class BaseEvaluator(ABC):
    """Base class for all evaluators."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the evaluator with configuration."""
        self.config = config
        self.name = config.get('name', 'unnamed_evaluator')
        self.thresholds = config.get('thresholds', {})
    
    @abstractmethod
    def evaluate(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Evaluate the provided data."""
        pass
    
    @abstractmethod
    def get_metrics(self) -> List[str]:
        """Get list of metrics this evaluator produces."""
        pass
    
    def check_thresholds(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Check results against configured thresholds."""
        threshold_results = {}
        
        for metric, value in results.items():
            if metric in self.thresholds:
                threshold = self.thresholds[metric]
                threshold_results[metric] = {
                    'value': value,
                    'threshold': threshold,
                    'status': 'pass' if value >= threshold else 'fail'
                }
        
        return threshold_results
```

### Example: Custom Performance Evaluator

```python
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from ml_eval.evaluators.base import BaseEvaluator

class CustomPerformanceEvaluator(BaseEvaluator):
    """Custom performance evaluator for specific metrics."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.prediction_column = config.get('prediction_column', 'prediction')
        self.actual_column = config.get('actual_column', 'actual')
        self.metrics = config.get('metrics', ['accuracy', 'precision', 'recall', 'f1'])
    
    def evaluate(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Evaluate performance metrics."""
        if self.prediction_column not in data.columns or self.actual_column not in data.columns:
            raise ValueError(f"Required columns {self.prediction_column} and {self.actual_column} not found")
        
        y_true = data[self.actual_column]
        y_pred = data[self.prediction_column]
        
        results = {}
        
        if 'accuracy' in self.metrics:
            results['accuracy'] = accuracy_score(y_true, y_pred)
        
        if 'precision' in self.metrics:
            results['precision'] = precision_score(y_true, y_pred, average='weighted')
        
        if 'recall' in self.metrics:
            results['recall'] = recall_score(y_true, y_pred, average='weighted')
        
        if 'f1' in self.metrics:
            results['f1_score'] = f1_score(y_true, y_pred, average='weighted')
        
        # Add threshold checking
        threshold_results = self.check_thresholds(results)
        
        return {
            'metrics': results,
            'threshold_results': threshold_results,
            'evaluator_name': self.name
        }
    
    def get_metrics(self) -> List[str]:
        """Get list of metrics this evaluator produces."""
        return self.metrics
```

### Example: Custom Drift Evaluator

```python
import pandas as pd
import numpy as np
from scipy import stats
from ml_eval.evaluators.base import BaseEvaluator

class CustomDriftEvaluator(BaseEvaluator):
    """Custom drift detection evaluator."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.features = config.get('features', [])
        self.baseline_data = config.get('baseline_data')
        self.detection_method = config.get('detection_method', 'ks_test')
        self.sensitivity = config.get('sensitivity', 0.05)
    
    def evaluate(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Evaluate data drift."""
        if not self.baseline_data:
            raise ValueError("Baseline data is required for drift detection")
        
        drift_results = {}
        
        for feature in self.features:
            if feature not in data.columns:
                continue
            
            current_data = data[feature].dropna()
            baseline_data = self.baseline_data[feature].dropna()
            
            if self.detection_method == 'ks_test':
                statistic, p_value = stats.ks_2samp(baseline_data, current_data)
                drift_detected = p_value < self.sensitivity
                drift_score = 1 - p_value
            elif self.detection_method == 'chi_square':
                # Implement chi-square test for categorical data
                pass
            else:
                raise ValueError(f"Unknown detection method: {self.detection_method}")
            
            drift_results[feature] = {
                'drift_detected': drift_detected,
                'drift_score': drift_score,
                'p_value': p_value,
                'statistic': statistic
            }
        
        # Overall drift assessment
        overall_drift = any(result['drift_detected'] for result in drift_results.values())
        overall_score = np.mean([result['drift_score'] for result in drift_results.values()])
        
        return {
            'drift_results': drift_results,
            'overall_drift_detected': overall_drift,
            'overall_drift_score': overall_score,
            'evaluator_name': self.name
        }
    
    def get_metrics(self) -> List[str]:
        """Get list of metrics this evaluator produces."""
        return ['drift_score', 'drift_detected']
```

### Registering Custom Evaluators

```python
from ml_eval.evaluators.registry import EvaluatorRegistry

# Register your custom evaluators
EvaluatorRegistry.register('custom_performance', CustomPerformanceEvaluator)
EvaluatorRegistry.register('custom_drift', CustomDriftEvaluator)
```

## Custom Reports

### Overview

Reports generate output from evaluation results. You can create custom reports for specific stakeholder needs.

### Base Report Interface

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import pandas as pd

class BaseReport(ABC):
    """Base class for all reports."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the report with configuration."""
        self.config = config
        self.name = config.get('name', 'unnamed_report')
        self.format = config.get('format', 'html')
        self.output_path = config.get('output_path', './reports/')
    
    @abstractmethod
    def generate(self, evaluation_results: Dict[str, Any], 
                data: Optional[pd.DataFrame] = None) -> str:
        """Generate the report."""
        pass
    
    @abstractmethod
    def get_supported_formats(self) -> List[str]:
        """Get list of supported output formats."""
        pass
```

### Example: Custom Business Report

```python
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from ml_eval.reports.base import BaseReport

class CustomBusinessReport(BaseReport):
    """Custom business report with executive summary."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.include_charts = config.get('include_charts', True)
        self.include_recommendations = config.get('include_recommendations', True)
        self.executive_summary = config.get('executive_summary', True)
    
    def generate(self, evaluation_results: Dict[str, Any], 
                data: Optional[pd.DataFrame] = None) -> str:
        """Generate the business report."""
        html_content = []
        
        # Executive Summary
        if self.executive_summary:
            html_content.append(self._generate_executive_summary(evaluation_results))
        
        # Key Metrics
        html_content.append(self._generate_metrics_section(evaluation_results))
        
        # Charts
        if self.include_charts and data is not None:
            html_content.append(self._generate_charts_section(data, evaluation_results))
        
        # Recommendations
        if self.include_recommendations:
            html_content.append(self._generate_recommendations_section(evaluation_results))
        
        return '\n'.join(html_content)
    
    def _generate_executive_summary(self, results: Dict[str, Any]) -> str:
        """Generate executive summary section."""
        summary = """
        <h2>Executive Summary</h2>
        <div class="executive-summary">
            <p>This report provides a comprehensive analysis of the ML system performance.</p>
            <ul>
        """
        
        # Add key findings
        for metric, data in results.get('metrics', {}).items():
            status = data.get('status', 'unknown')
            value = data.get('value', 0)
            summary += f"<li>{metric.title()}: {value:.3f} ({status})</li>"
        
        summary += "</ul></div>"
        return summary
    
    def _generate_metrics_section(self, results: Dict[str, Any]) -> str:
        """Generate metrics section."""
        metrics_html = """
        <h2>Key Performance Metrics</h2>
        <table class="metrics-table">
            <thead>
                <tr><th>Metric</th><th>Value</th><th>Threshold</th><th>Status</th></tr>
            </thead>
            <tbody>
        """
        
        for metric, data in results.get('threshold_results', {}).items():
            value = data.get('value', 0)
            threshold = data.get('threshold', 0)
            status = data.get('status', 'unknown')
            status_class = 'pass' if status == 'pass' else 'fail'
            
            metrics_html += f"""
                <tr>
                    <td>{metric.title()}</td>
                    <td>{value:.3f}</td>
                    <td>{threshold:.3f}</td>
                    <td class="{status_class}">{status.upper()}</td>
                </tr>
            """
        
        metrics_html += "</tbody></table>"
        return metrics_html
    
    def _generate_charts_section(self, data: pd.DataFrame, 
                                results: Dict[str, Any]) -> str:
        """Generate charts section."""
        charts_html = "<h2>Performance Charts</h2>"
        
        # Create performance trend chart
        if 'timestamp' in data.columns:
            fig = px.line(data, x='timestamp', y='accuracy', 
                         title='Accuracy Over Time')
            charts_html += f"<div>{fig.to_html()}</div>"
        
        # Create metrics comparison chart
        metrics_data = []
        for metric, data in results.get('metrics', {}).items():
            metrics_data.append({
                'metric': metric,
                'value': data.get('value', 0)
            })
        
        if metrics_data:
            df_metrics = pd.DataFrame(metrics_data)
            fig = px.bar(df_metrics, x='metric', y='value', 
                        title='Performance Metrics Comparison')
            charts_html += f"<div>{fig.to_html()}</div>"
        
        return charts_html
    
    def _generate_recommendations_section(self, results: Dict[str, Any]) -> str:
        """Generate recommendations section."""
        recommendations = []
        
        # Analyze results and generate recommendations
        for metric, data in results.get('threshold_results', {}).items():
            if data.get('status') == 'fail':
                recommendations.append(f"Improve {metric} performance to meet threshold")
        
        if not recommendations:
            recommendations.append("System performance is meeting all targets")
        
        recommendations_html = """
        <h2>Recommendations</h2>
        <ul class="recommendations">
        """
        
        for rec in recommendations:
            recommendations_html += f"<li>{rec}</li>"
        
        recommendations_html += "</ul>"
        return recommendations_html
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported output formats."""
        return ['html', 'pdf']
```

### Registering Custom Reports

```python
from ml_eval.reports.registry import ReportRegistry

# Register your custom report
ReportRegistry.register('custom_business', CustomBusinessReport)
```

## Custom Data Sources

### Overview

Data sources provide access to different types of data. You can create custom data sources for specific data formats or systems.

### Base Data Source Interface

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import pandas as pd

class BaseDataSource(ABC):
    """Base class for all data sources."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the data source with configuration."""
        self.config = config
        self.name = config.get('name', 'unnamed_source')
        self.type = config.get('type', 'custom')
    
    @abstractmethod
    def connect(self) -> bool:
        """Establish connection to the data source."""
        pass
    
    @abstractmethod
    def get_data(self, query_params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        """Retrieve data from the source."""
        pass
    
    @abstractmethod
    def get_schema(self) -> Dict[str, Any]:
        """Get schema information for the data source."""
        pass
    
    def test_connection(self) -> Dict[str, Any]:
        """Test the connection and return status."""
        try:
            success = self.connect()
            schema = self.get_schema() if success else {}
            return {
                'success': success,
                'schema': schema,
                'error': None if success else 'Connection failed'
            }
        except Exception as e:
            return {
                'success': False,
                'schema': {},
                'error': str(e)
            }
```

### Example: Custom File Data Source

```python
import pandas as pd
import json
from pathlib import Path
from ml_eval.data_sources.base import BaseDataSource

class CustomFileDataSource(BaseDataSource):
    """Custom data source for specific file formats."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.file_path = config['path']
        self.file_format = config.get('format', 'csv')
        self.encoding = config.get('encoding', 'utf-8')
    
    def connect(self) -> bool:
        """Check if file exists and is accessible."""
        return Path(self.file_path).exists()
    
    def get_data(self, query_params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        """Read data from file."""
        if self.file_format == 'csv':
            return pd.read_csv(self.file_path, encoding=self.encoding)
        elif self.file_format == 'json':
            return pd.read_json(self.file_path, encoding=self.encoding)
        elif self.file_format == 'parquet':
            return pd.read_parquet(self.file_path)
        elif self.file_format == 'excel':
            return pd.read_excel(self.file_path)
        else:
            raise ValueError(f"Unsupported file format: {self.file_format}")
    
    def get_schema(self) -> Dict[str, Any]:
        """Get schema information."""
        try:
            df = self.get_data()
            return {
                'columns': list(df.columns),
                'dtypes': df.dtypes.to_dict(),
                'shape': df.shape,
                'file_path': self.file_path,
                'file_format': self.file_format
            }
        except Exception as e:
            return {
                'error': str(e),
                'file_path': self.file_path,
                'file_format': self.file_format
            }
```

### Registering Custom Data Sources

```python
from ml_eval.data_sources.registry import DataSourceRegistry

# Register your custom data source
DataSourceRegistry.register('custom_file', CustomFileDataSource)
```

## Custom Templates

### Overview

Templates provide pre-configured setups for different use cases. You can create custom templates for your specific industry or requirements.

### Template Structure

```yaml
# custom_template.yaml
template:
  name: "Custom Industry Template"
  version: "1.0.0"
  description: "Custom template for specific industry needs"
  industry: "custom"
  author: "Your Name"
  tags: ["custom", "industry-specific"]

system:
  name: "Custom System"
  type: "custom"
  criticality: "business-critical"

data_sources:
  - name: "custom_data_source"
    type: "custom_file"
    path: "/path/to/data"
    format: "csv"

collectors:
  - name: "custom_collector"
    type: "custom_database"
    data_source: "custom_data_source"
    metrics: ["custom_metric1", "custom_metric2"]

evaluators:
  - name: "custom_evaluator"
    type: "custom_performance"
    thresholds:
      custom_metric1: 0.95
      custom_metric2: 0.90

reports:
  - name: "custom_report"
    type: "custom_business"
    format: "html"
    output_path: "./reports/"

slo:
  custom_metric1: 0.95
  custom_metric2: 0.90
```

### Creating Template Package

```python
from ml_eval.templates.base import BaseTemplate

class CustomTemplate(BaseTemplate):
    """Custom template for specific industry."""
    
    def __init__(self):
        super().__init__()
        self.name = "Custom Industry Template"
        self.version = "1.0.0"
        self.industry = "custom"
        self.description = "Custom template for specific industry needs"
    
    def get_configuration(self, customizations: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get the template configuration."""
        config = {
            'system': {
                'name': 'Custom System',
                'type': 'custom',
                'criticality': 'business-critical'
            },
            'data_sources': [
                {
                    'name': 'custom_data_source',
                    'type': 'custom_file',
                    'path': '/path/to/data',
                    'format': 'csv'
                }
            ],
            'collectors': [
                {
                    'name': 'custom_collector',
                    'type': 'custom_database',
                    'data_source': 'custom_data_source',
                    'metrics': ['custom_metric1', 'custom_metric2']
                }
            ],
            'evaluators': [
                {
                    'name': 'custom_evaluator',
                    'type': 'custom_performance',
                    'thresholds': {
                        'custom_metric1': 0.95,
                        'custom_metric2': 0.90
                    }
                }
            ],
            'reports': [
                {
                    'name': 'custom_report',
                    'type': 'custom_business',
                    'format': 'html',
                    'output_path': './reports/'
                }
            ],
            'slo': {
                'custom_metric1': 0.95,
                'custom_metric2': 0.90
            }
        }
        
        # Apply customizations
        if customizations:
            config = self._apply_customizations(config, customizations)
        
        return config
    
    def validate_configuration(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate the template configuration."""
        errors = []
        warnings = []
        
        # Add validation logic here
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
```

### Registering Custom Templates

```python
from ml_eval.templates.registry import TemplateRegistry

# Register your custom template
TemplateRegistry.register('custom_industry', CustomTemplate)
```

## Configuration Integration

### Using Custom Components

Once you've created and registered your custom components, you can use them in your configurations:

```yaml
# config_with_custom_components.yaml
system:
  name: "System with Custom Components"
  type: "custom"
  criticality: "business-critical"

data_sources:
  - name: "custom_data"
    type: "custom_file"
    path: "/path/to/data.csv"
    format: "csv"

collectors:
  - name: "custom_collector"
    type: "custom_database"
    data_source: "custom_data"
    metrics: ["custom_metric1", "custom_metric2"]

evaluators:
  - name: "custom_evaluator"
    type: "custom_performance"
    thresholds:
      custom_metric1: 0.95
      custom_metric2: 0.90

reports:
  - name: "custom_report"
    type: "custom_business"
    format: "html"
    output_path: "./reports/"

slo:
  custom_metric1: 0.95
  custom_metric2: 0.90
```

### Loading Custom Components

```python
# Load your custom components
import your_custom_components

# The components will be automatically registered when imported
# Or register them manually:
from ml_eval.collectors.registry import CollectorRegistry
from ml_eval.evaluators.registry import EvaluatorRegistry
from ml_eval.reports.registry import ReportRegistry

CollectorRegistry.register('custom_database', your_custom_components.CustomDatabaseCollector)
EvaluatorRegistry.register('custom_performance', your_custom_components.CustomPerformanceEvaluator)
ReportRegistry.register('custom_business', your_custom_components.CustomBusinessReport)
```

## Best Practices

### 1. Component Design
- Follow the established interface patterns
- Implement proper error handling
- Add comprehensive logging
- Include input validation

### 2. Testing
- Write unit tests for your components
- Test with sample data
- Validate error conditions
- Test integration with the framework

### 3. Documentation
- Document your component's purpose and usage
- Include configuration examples
- Provide troubleshooting guidance
- Add code comments

### 4. Performance
- Optimize for large datasets
- Implement efficient data processing
- Use appropriate data structures
- Consider memory usage

### 5. Security
- Validate all inputs
- Handle sensitive data appropriately
- Implement proper authentication
- Follow security best practices

## Distribution

### Packaging Custom Components

```python
# setup.py for your custom components
from setuptools import setup, find_packages

setup(
    name="ml-eval-custom-components",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "ml-eval>=1.0.0",
        "pandas>=1.3.0",
        "numpy>=1.20.0",
        "scikit-learn>=1.0.0",
        "plotly>=5.0.0"
    ],
    entry_points={
        "ml_eval.collectors": [
            "custom_database = your_package.collectors:CustomDatabaseCollector",
            "custom_api = your_package.collectors:CustomAPICollector",
        ],
        "ml_eval.evaluators": [
            "custom_performance = your_package.evaluators:CustomPerformanceEvaluator",
            "custom_drift = your_package.evaluators:CustomDriftEvaluator",
        ],
        "ml_eval.reports": [
            "custom_business = your_package.reports:CustomBusinessReport",
        ],
    }
)
```

### Installing Custom Components

```bash
# Install your custom components
pip install your-custom-components-package

# The components will be automatically available
ml-eval evaluate --config config_with_custom_components.yaml
```

This guide provides a comprehensive approach to extending the ML Systems Evaluation Framework with custom components, enabling you to adapt the framework to your specific needs while maintaining compatibility with the existing system. 