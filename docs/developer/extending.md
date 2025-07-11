# Extending the Framework

This guide explains how to extend the ML Systems Evaluation Framework with custom components.

## Overview

The framework is designed to be extensible, allowing you to create custom components that integrate with the existing system. All custom components follow a consistent interface pattern.

## How to Create Custom Components

### Step 1: Choose Your Component Type
- **Collectors**: For gathering data from new sources
- **Evaluators**: For analyzing data with custom logic
- **Reports**: For generating custom output formats

### Step 2: Create Your Implementation
1. **Import the base class** from the appropriate module
2. **Extend the base class** and implement required methods
3. **Add your custom logic** in the implementation methods
4. **Handle errors appropriately** and add logging

### Step 3: Register Your Component
1. **Create a configuration** that references your component type
2. **Import your component** in your application
3. **The framework will automatically discover** and instantiate your component

### Step 4: Test Your Component
1. **Write unit tests** for your component
2. **Test with sample data** to ensure it works correctly
3. **Validate integration** with the framework

## Practical Example: Creating a Custom Collector

Here's a step-by-step example of creating a custom database collector:

### 1. Create Your Collector Class

```python
# my_collectors.py
from ml_eval.collectors.base import BaseCollector
from ml_eval.core.config import MetricData
from typing import Dict, Any
from datetime import datetime

class DatabaseCollector(BaseCollector):
    """Custom collector for database metrics."""
    
    def collect(self) -> Dict[str, list[MetricData]]:
        """Collect metrics from database."""
        # Your custom collection logic here
        metric = MetricData(
            timestamp=datetime.now(),
            value=0.95,  # Your metric value
            metadata={'source': 'database'}
        )
        return {'custom_metric': [metric]}
    
    def health_check(self) -> bool:
        """Check if data source is healthy."""
        return True  # Your health check logic
```

### 2. Create Configuration

```yaml
# config.yaml
system:
  name: "My System"
  type: "custom"

collectors:
  - name: "database_collector"
    type: "custom"
```

### 3. Use Your Custom Component

```python
# main.py
import my_collectors  # Import your custom component
from ml_eval.core.framework import EvaluationFramework

framework = EvaluationFramework(config)
result = framework.evaluate()
```

## Custom Collectors

### Overview

Collectors are responsible for gathering data from various sources. You can create custom collectors to handle specific data sources or collection methods.

### Base Interface

See [`ml_eval/collectors/base.py`](../../ml_eval/collectors/base.py) for the actual `BaseCollector` interface.

### Implementation Examples

See these real collector implementations for reference:
- [`ml_eval/collectors/online.py`](../../ml_eval/collectors/online.py) - Real-time data collection
- [`ml_eval/collectors/offline.py`](../../ml_eval/collectors/offline.py) - Historical data collection
- [`ml_eval/collectors/environmental.py`](../../ml_eval/collectors/environmental.py) - Environmental monitoring
- [`ml_eval/collectors/regulatory.py`](../../ml_eval/collectors/regulatory.py) - Compliance monitoring

## Custom Evaluators

### Overview

Evaluators analyze collected data and produce evaluation results. You can create custom evaluators for specific analysis needs.

### Base Interface

See [`ml_eval/evaluators/base.py`](../../ml_eval/evaluators/base.py) for the actual `BaseEvaluator` interface.

### Implementation Examples

See these real evaluator implementations for reference:
- [`ml_eval/evaluators/reliability.py`](../../ml_eval/evaluators/reliability.py) - Reliability evaluation
- [`ml_eval/evaluators/safety.py`](../../ml_eval/evaluators/safety.py) - Safety-critical evaluation
- [`ml_eval/evaluators/performance.py`](../../ml_eval/evaluators/performance.py) - Performance metrics
- [`ml_eval/evaluators/compliance.py`](../../ml_eval/evaluators/compliance.py) - Regulatory compliance
- [`ml_eval/evaluators/drift.py`](../../ml_eval/evaluators/drift.py) - Data drift detection

## Custom Reports

### Overview

Reports generate output from evaluation results. You can create custom reports for specific stakeholder needs.

### Base Interface

See [`ml_eval/reports/base.py`](../../ml_eval/reports/base.py) for the actual `BaseReport` interface.

### Implementation Examples

See these real report implementations for reference:
- [`ml_eval/reports/reliability.py`](../../ml_eval/reports/reliability.py) - Reliability reports
- [`ml_eval/reports/safety.py`](../../ml_eval/reports/safety.py) - Safety reports
- [`ml_eval/reports/compliance.py`](../../ml_eval/reports/compliance.py) - Compliance reports
- [`ml_eval/reports/business.py`](../../ml_eval/reports/business.py) - Business impact reports

## Custom Templates

### Overview

Templates provide pre-configured setups for different use cases. You can create custom templates for your specific industry or requirements.

### Example Template

```yaml
# custom_template.yaml
system:
  name: "Custom System"
  type: "custom"

collectors:
  - name: "custom_collector"
    type: "custom"

evaluators:
  - name: "custom_evaluator"
    type: "custom"

reports:
  - name: "custom_report"
    type: "custom"
```

### Template Integration

See [`ml_eval/templates/factory.py`](../../ml_eval/templates/factory.py) for how templates are implemented and [`ml_eval/examples/registry.py`](../../ml_eval/examples/registry.py) for example patterns.

## Configuration Integration

### Using Custom Components

Once you've created your custom components, you can use them in your configurations by setting the `type` field to `"custom"`:

```yaml
# config.yaml
collectors:
  - name: "my_collector"
    type: "custom"

evaluators:
  - name: "my_evaluator"
    type: "custom"
```

### Loading Custom Components

```python
import your_custom_components  # Import your custom components
# The framework will automatically discover and use them
```

This guide provides a practical approach to extending the ML Systems Evaluation Framework with custom components, enabling you to adapt the framework to your specific needs while maintaining compatibility with the existing system.
