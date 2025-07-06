# Testing Guide

This guide provides comprehensive testing strategies and best practices for the ML Systems Evaluation Framework, including unit testing, integration testing, and end-to-end testing.

## Testing Strategy

The framework follows a multi-layered testing approach to ensure reliability, performance, and correctness.

### Testing Pyramid

```
                    E2E Tests
                ┌─────────────┐
                │   (Few)     │
                └─────────────┘
            Integration Tests
        ┌─────────────────────┐
        │     (Some)          │
        └─────────────────────┘
            Unit Tests
    ┌─────────────────────────────┐
    │         (Many)              │
    └─────────────────────────────┘
```

## Unit Testing

### Overview

Unit tests focus on testing individual components in isolation. Each component should have comprehensive unit tests covering all functionality.

### Test Structure

```python
import pytest
import pandas as pd
from unittest.mock import Mock, patch
from ml_eval.collectors.base import BaseCollector
from ml_eval.evaluators.base import BaseEvaluator

class TestCustomCollector:
    """Test suite for custom collector."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.config = {
            'name': 'test_collector',
            'data_source': 'test_source',
            'metrics': ['metric1', 'metric2']
        }
        self.collector = CustomCollector(self.config)
    
    def test_initialization(self):
        """Test collector initialization."""
        assert self.collector.name == 'test_collector'
        assert self.collector.data_source == 'test_source'
        assert self.collector.metrics == ['metric1', 'metric2']
    
    def test_validate_connection_success(self):
        """Test successful connection validation."""
        with patch('sqlalchemy.create_engine') as mock_engine:
            mock_conn = Mock()
            mock_engine.return_value.connect.return_value.__enter__.return_value = mock_conn
            
            result = self.collector.validate_connection()
            
            assert result is True
            mock_conn.execute.assert_called_once()
    
    def test_validate_connection_failure(self):
        """Test failed connection validation."""
        with patch('sqlalchemy.create_engine') as mock_engine:
            mock_engine.side_effect = Exception("Connection failed")
            
            result = self.collector.validate_connection()
            
            assert result is False
    
    def test_collect_data(self):
        """Test data collection."""
        test_data = pd.DataFrame({
            'metric1': [1, 2, 3],
            'metric2': [4, 5, 6],
            'timestamp': pd.date_range('2024-01-01', periods=3)
        })
        
        with patch.object(self.collector, '_execute_query', return_value=test_data):
            result = self.collector.collect()
            
            assert isinstance(result, pd.DataFrame)
            assert len(result) == 3
            assert '_collector_name' in result.columns
            assert '_collection_timestamp' in result.columns
    
    def test_collect_data_with_date_range(self):
        """Test data collection with date range."""
        start_date = '2024-01-01'
        end_date = '2024-01-31'
        
        with patch.object(self.collector, '_execute_query') as mock_query:
            self.collector.collect(start_date=start_date, end_date=end_date)
            
            # Verify query was called with date conditions
            mock_query.assert_called_once()
            call_args = mock_query.call_args[0][0]
            assert 'timestamp >= \'2024-01-01\'' in call_args
            assert 'timestamp <= \'2024-01-31\'' in call_args
    
    def test_get_metadata(self):
        """Test metadata generation."""
        metadata = self.collector.get_metadata()
        
        assert metadata['collector_name'] == 'test_collector'
        assert metadata['data_source'] == 'test_source'
        assert metadata['metrics'] == ['metric1', 'metric2']
        assert 'collection_timestamp' in metadata
```

### Test Configuration

```python
# conftest.py
import pytest
import pandas as pd
from datetime import datetime, timedelta

@pytest.fixture
def sample_data():
    """Provide sample data for testing."""
    return pd.DataFrame({
        'accuracy': [0.95, 0.92, 0.88, 0.94, 0.91],
        'precision': [0.93, 0.90, 0.87, 0.92, 0.89],
        'recall': [0.94, 0.91, 0.86, 0.93, 0.90],
        'timestamp': pd.date_range('2024-01-01', periods=5)
    })

@pytest.fixture
def sample_config():
    """Provide sample configuration for testing."""
    return {
        'system': {
            'name': 'Test System',
            'type': 'manufacturing',
            'criticality': 'business-critical'
        },
        'data_sources': [
            {
                'name': 'test_database',
                'type': 'database',
                'connection': 'sqlite:///test.db'
            }
        ],
        'collectors': [
            {
                'name': 'test_collector',
                'type': 'offline',
                'data_source': 'test_database',
                'metrics': ['accuracy', 'precision', 'recall']
            }
        ],
        'evaluators': [
            {
                'name': 'test_evaluator',
                'type': 'performance',
                'thresholds': {
                    'accuracy': 0.90,
                    'precision': 0.85,
                    'recall': 0.80
                }
            }
        ],
        'reports': [
            {
                'name': 'test_report',
                'type': 'business',
                'format': 'html',
                'output_path': './test_reports/'
            }
        ],
        'slo': {
            'accuracy': 0.90,
            'precision': 0.85,
            'recall': 0.80
        }
    }

@pytest.fixture
def mock_database():
    """Provide mock database connection."""
    with patch('sqlalchemy.create_engine') as mock_engine:
        mock_conn = Mock()
        mock_engine.return_value.connect.return_value.__enter__.return_value = mock_conn
        yield mock_engine, mock_conn
```

### Testing Custom Components

```python
class TestCustomEvaluator:
    """Test suite for custom evaluator."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.config = {
            'name': 'test_evaluator',
            'thresholds': {
                'accuracy': 0.90,
                'precision': 0.85
            }
        }
        self.evaluator = CustomEvaluator(self.config)
    
    def test_evaluation_with_passing_metrics(self):
        """Test evaluation with metrics above thresholds."""
        data = pd.DataFrame({
            'prediction': [1, 0, 1, 0, 1],
            'actual': [1, 0, 1, 0, 1]
        })
        
        results = self.evaluator.evaluate(data)
        
        assert results['metrics']['accuracy'] == 1.0
        assert results['threshold_results']['accuracy']['status'] == 'pass'
    
    def test_evaluation_with_failing_metrics(self):
        """Test evaluation with metrics below thresholds."""
        data = pd.DataFrame({
            'prediction': [1, 0, 1, 0, 0],
            'actual': [1, 0, 1, 0, 1]
        })
        
        results = self.evaluator.evaluate(data)
        
        assert results['metrics']['accuracy'] == 0.8
        assert results['threshold_results']['accuracy']['status'] == 'fail'
    
    def test_get_metrics(self):
        """Test metrics list generation."""
        metrics = self.evaluator.get_metrics()
        
        assert 'accuracy' in metrics
        assert 'precision' in metrics
```

## Integration Testing

### Overview

Integration tests verify that components work together correctly and that the overall system functions as expected.

### Test Structure

```python
class TestDataCollectionIntegration:
    """Integration tests for data collection workflow."""
    
    def test_collector_evaluator_integration(self, sample_config, sample_data):
        """Test integration between collector and evaluator."""
        # Set up collector
        collector_config = sample_config['collectors'][0]
        collector = CollectorFactory.create(collector_config)
        
        # Mock data collection
        with patch.object(collector, 'collect', return_value=sample_data):
            collected_data = collector.collect()
        
        # Set up evaluator
        evaluator_config = sample_config['evaluators'][0]
        evaluator = EvaluatorFactory.create(evaluator_config)
        
        # Evaluate collected data
        results = evaluator.evaluate(collected_data)
        
        # Verify results
        assert 'metrics' in results
        assert 'threshold_results' in results
        assert len(results['metrics']) > 0
    
    def test_full_evaluation_workflow(self, sample_config):
        """Test complete evaluation workflow."""
        # Create evaluation framework
        framework = MLEvalFramework(sample_config)
        
        # Mock data collection
        with patch.object(framework.collectors[0], 'collect') as mock_collect:
            mock_collect.return_value = sample_data
            
            # Run evaluation
            results = framework.evaluate()
            
            # Verify results
            assert results['status'] == 'completed'
            assert 'evaluations' in results
            assert len(results['evaluations']) > 0
    
    def test_configuration_validation_integration(self, sample_config):
        """Test configuration validation integration."""
        # Test valid configuration
        validator = ConfigurationValidator()
        result = validator.validate(sample_config)
        
        assert result['valid'] is True
        assert len(result['errors']) == 0
        
        # Test invalid configuration
        invalid_config = sample_config.copy()
        invalid_config['data_sources'][0]['connection'] = 'invalid_connection'
        
        result = validator.validate(invalid_config)
        
        assert result['valid'] is False
        assert len(result['errors']) > 0
```

### Database Integration Testing

```python
class TestDatabaseIntegration:
    """Integration tests for database operations."""
    
    @pytest.fixture(autouse=True)
    def setup_database(self):
        """Set up test database."""
        self.engine = create_engine('sqlite:///:memory:')
        self.create_test_tables()
        yield
        self.engine.dispose()
    
    def create_test_tables(self):
        """Create test tables."""
        with self.engine.connect() as conn:
            conn.execute(text("""
                CREATE TABLE quality_measurements (
                    id INTEGER PRIMARY KEY,
                    accuracy REAL,
                    precision REAL,
                    recall REAL,
                    timestamp DATETIME
                )
            """))
            
            # Insert test data
            test_data = [
                (1, 0.95, 0.92, 0.94, '2024-01-01 10:00:00'),
                (2, 0.92, 0.90, 0.91, '2024-01-01 11:00:00'),
                (3, 0.88, 0.87, 0.86, '2024-01-01 12:00:00')
            ]
            
            conn.execute(text("""
                INSERT INTO quality_measurements 
                (id, accuracy, precision, recall, timestamp)
                VALUES (?, ?, ?, ?, ?)
            """), test_data)
            conn.commit()
    
    def test_database_collector_integration(self):
        """Test database collector with real database."""
        config = {
            'name': 'test_db_collector',
            'type': 'database',
            'connection': 'sqlite:///:memory:',
            'table': 'quality_measurements',
            'metrics': ['accuracy', 'precision', 'recall']
        }
        
        collector = DatabaseCollector(config)
        
        # Test connection
        assert collector.validate_connection() is True
        
        # Test data collection
        data = collector.collect()
        
        assert isinstance(data, pd.DataFrame)
        assert len(data) == 3
        assert 'accuracy' in data.columns
        assert 'precision' in data.columns
        assert 'recall' in data.columns
```

## End-to-End Testing

### Overview

End-to-end tests verify that the complete system works correctly from start to finish, including all components and external dependencies.

### Test Structure

```python
class TestEndToEndWorkflow:
    """End-to-end tests for complete workflows."""
    
    def test_complete_evaluation_workflow(self, tmp_path):
        """Test complete evaluation workflow from config to report."""
        # Create test configuration
        config_path = tmp_path / "test_config.yaml"
        config = {
            'system': {
                'name': 'E2E Test System',
                'type': 'manufacturing',
                'criticality': 'business-critical'
            },
            'data_sources': [
                {
                    'name': 'test_file',
                    'type': 'file',
                    'path': str(tmp_path / "test_data.csv"),
                    'format': 'csv'
                }
            ],
            'collectors': [
                {
                    'name': 'test_collector',
                    'type': 'offline',
                    'data_source': 'test_file',
                    'metrics': ['accuracy', 'precision', 'recall']
                }
            ],
            'evaluators': [
                {
                    'name': 'test_evaluator',
                    'type': 'performance',
                    'thresholds': {
                        'accuracy': 0.90,
                        'precision': 0.85,
                        'recall': 0.80
                    }
                }
            ],
            'reports': [
                {
                    'name': 'test_report',
                    'type': 'business',
                    'format': 'html',
                    'output_path': str(tmp_path / "reports")
                }
            ],
            'slo': {
                'accuracy': 0.90,
                'precision': 0.85,
                'recall': 0.80
            }
        }
        
        # Write configuration file
        with open(config_path, 'w') as f:
            yaml.dump(config, f)
        
        # Create test data
        test_data = pd.DataFrame({
            'accuracy': [0.95, 0.92, 0.88, 0.94, 0.91],
            'precision': [0.93, 0.90, 0.87, 0.92, 0.89],
            'recall': [0.94, 0.91, 0.86, 0.93, 0.90],
            'timestamp': pd.date_range('2024-01-01', periods=5)
        })
        
        test_data.to_csv(tmp_path / "test_data.csv", index=False)
        
        # Run evaluation
        result = run_evaluation(str(config_path))
        
        # Verify results
        assert result['status'] == 'completed'
        assert result['evaluations']['test_evaluator']['status'] == 'completed'
        
        # Check report generation
        report_files = list((tmp_path / "reports").glob("*.html"))
        assert len(report_files) > 0
    
    def test_cli_integration(self, tmp_path):
        """Test CLI integration."""
        # Create test configuration and data
        config_path = tmp_path / "cli_test_config.yaml"
        # ... setup configuration and data ...
        
        # Test CLI commands
        result = subprocess.run([
            'ml-eval', 'evaluate', '--config', str(config_path)
        ], capture_output=True, text=True)
        
        assert result.returncode == 0
        assert 'Evaluation completed' in result.stdout
    
    def test_api_integration(self):
        """Test API integration."""
        # Start test server
        with TestClient(app) as client:
            # Test configuration creation
            response = client.post("/config", json={
                "name": "API Test Config",
                "type": "manufacturing",
                "criticality": "business-critical"
            })
            
            assert response.status_code == 200
            config_id = response.json()["id"]
            
            # Test evaluation
            response = client.post("/evaluate", json={
                "config_id": config_id,
                "evaluator_name": "performance_evaluator"
            })
            
            assert response.status_code == 200
            evaluation_id = response.json()["id"]
            
            # Test results retrieval
            response = client.get(f"/evaluate/{evaluation_id}/results")
            
            assert response.status_code == 200
            assert "metrics" in response.json()
```

## Performance Testing

### Overview

Performance tests verify that the system meets performance requirements under various load conditions.

### Test Structure

```python
class TestPerformance:
    """Performance tests for the framework."""
    
    def test_large_dataset_processing(self):
        """Test processing of large datasets."""
        # Generate large test dataset
        large_data = pd.DataFrame({
            'accuracy': np.random.random(100000),
            'precision': np.random.random(100000),
            'recall': np.random.random(100000),
            'timestamp': pd.date_range('2024-01-01', periods=100000, freq='1min')
        })
        
        # Test collector performance
        start_time = time.time()
        collector = OfflineCollector({
            'name': 'performance_test_collector',
            'type': 'offline',
            'batch_size': 10000
        })
        
        result = collector.collect_data(large_data)
        end_time = time.time()
        
        # Verify performance requirements
        processing_time = end_time - start_time
        assert processing_time < 60  # Should complete within 60 seconds
        assert len(result) == 100000
    
    def test_concurrent_evaluations(self):
        """Test concurrent evaluation performance."""
        configs = [self.create_test_config(i) for i in range(10)]
        
        start_time = time.time()
        
        # Run evaluations concurrently
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [
                executor.submit(run_evaluation, config)
                for config in configs
            ]
            results = [future.result() for future in futures]
        
        end_time = time.time()
        
        # Verify all evaluations completed successfully
        assert all(result['status'] == 'completed' for result in results)
        
        # Verify performance requirements
        total_time = end_time - start_time
        assert total_time < 300  # Should complete within 5 minutes
    
    def test_memory_usage(self):
        """Test memory usage under load."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # Process large dataset
        large_data = pd.DataFrame({
            'data': np.random.random(1000000)
        })
        
        evaluator = PerformanceEvaluator({
            'name': 'memory_test_evaluator',
            'type': 'performance'
        })
        
        result = evaluator.evaluate(large_data)
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Verify memory usage is reasonable (less than 1GB increase)
        assert memory_increase < 1024 * 1024 * 1024
```

## Security Testing

### Overview

Security tests verify that the system handles sensitive data appropriately and is protected against common security vulnerabilities.

### Test Structure

```python
class TestSecurity:
    """Security tests for the framework."""
    
    def test_sensitive_data_handling(self):
        """Test handling of sensitive data."""
        config = {
            'data_sources': [
                {
                    'name': 'sensitive_db',
                    'type': 'database',
                    'connection': 'postgresql://user:password@localhost/db',
                    'encryption': True
                }
            ]
        }
        
        # Verify connection string is not logged
        with patch('logging.info') as mock_log:
            framework = MLEvalFramework(config)
            framework.initialize()
            
            # Check that sensitive data is not logged
            log_calls = mock_log.call_args_list
            for call in log_calls:
                assert 'password' not in str(call)
    
    def test_input_validation(self):
        """Test input validation and sanitization."""
        malicious_config = {
            'data_sources': [
                {
                    'name': 'malicious_source',
                    'type': 'database',
                    'connection': "'; DROP TABLE users; --"
                }
            ]
        }
        
        # Verify malicious input is rejected
        validator = ConfigurationValidator()
        result = validator.validate(malicious_config)
        
        assert result['valid'] is False
        assert len(result['errors']) > 0
    
    def test_authentication(self):
        """Test authentication mechanisms."""
        # Test API authentication
        with TestClient(app) as client:
            # Test without authentication
            response = client.get("/config")
            assert response.status_code == 401
            
            # Test with valid authentication
            headers = {"Authorization": "Bearer valid_token"}
            response = client.get("/config", headers=headers)
            assert response.status_code == 200
    
    def test_data_encryption(self):
        """Test data encryption at rest and in transit."""
        sensitive_data = {
            'user_id': '12345',
            'credit_card': '4111111111111111',
            'ssn': '123-45-6789'
        }
        
        # Test encryption
        encrypted_data = encrypt_sensitive_data(sensitive_data)
        decrypted_data = decrypt_sensitive_data(encrypted_data)
        
        assert decrypted_data == sensitive_data
        assert 'credit_card' not in str(encrypted_data)
        assert 'ssn' not in str(encrypted_data)
```

## Test Automation

### CI/CD Integration

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run unit tests
      run: |
        pytest tests/unit/ -v --cov=ml_eval --cov-report=xml
    
    - name: Run integration tests
      run: |
        pytest tests/integration/ -v
    
    - name: Run performance tests
      run: |
        pytest tests/performance/ -v --benchmark-only
    
    - name: Upload coverage
      uses: codecov/codecov-action@v1
      with:
        file: ./coverage.xml
```

### Test Configuration

```python
# pytest.ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --strict-markers
    --disable-warnings
    --cov=ml_eval
    --cov-report=html
    --cov-report=term-missing
markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
    performance: Performance tests
    security: Security tests
    slow: Slow running tests
```

## Best Practices

### 1. Test Organization
- Organize tests by component and type
- Use descriptive test names
- Group related tests in classes
- Use fixtures for common setup

### 2. Test Data Management
- Use realistic test data
- Create reusable test fixtures
- Clean up test data after tests
- Use separate test databases

### 3. Mocking and Stubbing
- Mock external dependencies
- Use realistic mock responses
- Test error conditions
- Verify mock interactions

### 4. Performance Considerations
- Run performance tests regularly
- Monitor test execution time
- Use appropriate test data sizes
- Test under realistic conditions

### 5. Security Testing
- Test input validation
- Verify authentication
- Check data encryption
- Test access controls

### 6. Continuous Testing
- Automate test execution
- Integrate with CI/CD
- Monitor test coverage
- Track test metrics

This testing guide provides a comprehensive approach to ensuring the reliability and quality of the ML Systems Evaluation Framework through thorough testing at all levels. 