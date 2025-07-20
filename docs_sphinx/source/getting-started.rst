Getting Started
==============

This guide will help you get up and running with the ML Systems Evaluation Framework quickly.

Quick Start
-----------

1. **Install the Framework**

   .. code-block:: bash

      # Using uv (recommended)
      uv add ml-systems-evaluation

      # Or using pip
      pip install ml-systems-evaluation

2. **Set Up Environment Variables**

   .. code-block:: bash

      # For LLM-enhanced evaluations
      export OPENAI_API_KEY="your-openai-api-key"
      export ANTHROPIC_API_KEY="your-anthropic-api-key"

3. **Run Your First Evaluation**

   .. code-block:: bash

      # Run a basic evaluation
      ml-eval evaluate --config examples/templates/basic-system.yaml

      # Run an industry-specific evaluation
      ml-eval evaluate --config examples/industries/aviation/aircraft-landing.yaml

Your First Evaluation
--------------------

Let's create a simple evaluation for a basic ML system:

1. **Create a Configuration File**

   Create a file named `my-first-evaluation.yaml`:

   .. code-block:: yaml

      system:
        name: "my-first-ml-system"
        version: "1.0.0"
        description: "A simple ML system for demonstration"

      collectors:
        - name: "basic-data-collector"
          type: "offline"
          config:
            data_path: "./sample_data.csv"
            features: ["feature1", "feature2", "feature3"]
            target: "target"

      evaluators:
        - name: "performance-evaluator"
          type: "performance"
          config:
            metrics: ["accuracy", "precision", "recall"]
            thresholds:
              accuracy: 0.85
              precision: 0.80
              recall: 0.75

      reports:
        - name: "basic-report"
          type: "business"
          config:
            format: "html"
            output_dir: "./reports"

2. **Run the Evaluation**

   .. code-block:: bash

      ml-eval evaluate --config my-first-evaluation.yaml

3. **View Results**

   Check the generated report in the `./reports` directory.

Understanding the Framework
-------------------------

The ML Systems Evaluation Framework consists of several key components:

Collectors
~~~~~~~~~

Collectors gather data from various sources:

* **Offline Collectors**: Process static datasets
* **Online Collectors**: Real-time data collection
* **Environmental Collectors**: System environment data
* **Regulatory Collectors**: Compliance-related data

Example collector configuration:

.. code-block:: yaml

   collectors:
     - name: "my-collector"
       type: "online"
       config:
         endpoint: "http://localhost:8000/metrics"
         interval: 60  # seconds
         timeout: 30

Evaluators
~~~~~~~~~~

Evaluators analyze the collected data and assess system performance:

* **Performance Evaluators**: Accuracy, latency, throughput
* **Safety Evaluators**: Failure rates, safety metrics
* **Compliance Evaluators**: Regulatory requirements
* **Reliability Evaluators**: System reliability metrics

Example evaluator configuration:

.. code-block:: yaml

   evaluators:
     - name: "my-evaluator"
       type: "performance"
       config:
         metrics: ["accuracy", "latency"]
         thresholds:
           accuracy: 0.95
           latency: 100  # milliseconds

Reports
~~~~~~~

Reports generate output for stakeholders:

* **Business Reports**: Executive summaries
* **Technical Reports**: Detailed technical analysis
* **Compliance Reports**: Regulatory documentation
* **Safety Reports**: Safety-critical assessments

Example report configuration:

.. code-block:: yaml

   reports:
     - name: "my-report"
       type: "business"
       config:
         format: "html"
         output_dir: "./reports"
         include_charts: true

Industry-Specific Evaluations
----------------------------

The framework provides pre-configured evaluations for various industries:

Aviation
~~~~~~~~

.. code-block:: bash

   # Aircraft landing system evaluation
   ml-eval evaluate --config examples/industries/aviation/aircraft-landing.yaml

Manufacturing
~~~~~~~~~~~~

.. code-block:: bash

   # Predictive maintenance evaluation
   ml-eval evaluate --config examples/industries/manufacturing/predictive-maintenance.yaml

Energy
~~~~~~

.. code-block:: bash

   # Energy optimization evaluation
   ml-eval evaluate --config examples/industries/energy/energy-optimization-recommendations.yaml

Maritime
~~~~~~~~

.. code-block:: bash

   # Collision avoidance evaluation
   ml-eval evaluate --config examples/industries/maritime/collision-avoidance.yaml

Advanced Features
----------------

LLM-Enhanced Evaluations
~~~~~~~~~~~~~~~~~~~~~~~

Enable LLM-enhanced evaluations for more sophisticated analysis:

.. code-block:: yaml

   evaluators:
     - name: "llm-enhanced-evaluator"
       type: "llm_enhanced"
       config:
         provider: "openai"
         model: "gpt-4"
         analysis_type: "edge_case"
         prompt_template: "custom_prompt.txt"

Real-time Monitoring
~~~~~~~~~~~~~~~~~~~

Set up continuous monitoring:

.. code-block:: bash

   # Start monitoring
   ml-eval monitor --config my-monitoring-config.yaml

   # Check monitoring status
   ml-eval status

Custom Evaluators
~~~~~~~~~~~~~~~~

Create custom evaluators for specific requirements:

.. code-block:: python

   # custom_evaluator.py
   from ml_eval.evaluators.base import BaseEvaluator

   class CustomEvaluator(BaseEvaluator):
       def evaluate(self, data):
           # Your custom evaluation logic
           return {"custom_metric": 0.95}

Command Line Interface
---------------------

The framework provides a comprehensive CLI:

.. code-block:: bash

   # Basic commands
   ml-eval --help
   ml-eval evaluate --help
   ml-eval monitor --help

   # Configuration management
   ml-eval validate --config my-config.yaml
   ml-eval check --config my-config.yaml

   # Monitoring and alerts
   ml-eval monitor --config monitoring.yaml
   ml-eval alerts --config alerts.yaml

Next Steps
----------

1. **Explore Examples**: Check the `examples/` directory for more configurations
2. **Read User Guides**: See :doc:`user-guides/first-evaluation` for detailed walkthroughs
3. **Configure Monitoring**: Set up continuous monitoring with :doc:`user-guides/monitoring`
4. **Customize Evaluators**: Learn to create custom evaluators in :doc:`developer/extending`
5. **Industry Guides**: Explore industry-specific guides in the :doc:`industries` section

Troubleshooting
--------------

Common Issues and Solutions:

**Configuration Errors**
   - Validate your YAML syntax
   - Check that all required fields are present
   - Verify file paths and permissions

**API Key Issues**
   - Ensure environment variables are set correctly
   - Check API key permissions and quotas
   - Verify API endpoints are accessible

**Data Collection Issues**
   - Check data source connectivity
   - Verify data format and schema
   - Ensure sufficient permissions

**Performance Issues**
   - Monitor system resources
   - Check network connectivity
   - Review evaluation intervals

Getting Help
-----------

* **Documentation**: This guide and related documentation
* **Examples**: Check the `examples/` directory
* **GitHub Issues**: Report bugs and request features
* **Community**: Join discussions and ask questions 