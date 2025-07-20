Configuration Guide
==================

This guide explains how to configure the ML Systems Evaluation Framework for your specific use case.

Configuration Overview
--------------------

The framework uses YAML configuration files to define evaluation parameters, collectors, evaluators, and reports. Configuration files are organized hierarchically and support inheritance and overrides.

Basic Configuration Structure
---------------------------

.. code-block:: yaml

   # Basic configuration structure
   system:
     name: "my-ml-system"
     version: "1.0.0"
     description: "Description of the ML system"

   collectors:
     - name: "performance-collector"
       type: "online"
       config:
         endpoint: "http://localhost:8000/metrics"
         interval: 60

   evaluators:
     - name: "performance-evaluator"
       type: "performance"
       config:
         metrics: ["accuracy", "latency", "throughput"]
         thresholds:
           accuracy: 0.95
           latency: 100

   reports:
     - name: "performance-report"
       type: "business"
       config:
         format: "html"
         output_dir: "./reports"

Configuration Templates
---------------------

The framework provides several pre-configured templates for different use cases:

Basic System Template
~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   # examples/templates/basic-system.yaml
   system:
     name: "basic-ml-system"
     version: "1.0.0"

   collectors:
     - name: "basic-collector"
       type: "offline"
       config:
         data_path: "./data"

   evaluators:
     - name: "basic-evaluator"
       type: "performance"
       config:
         metrics: ["accuracy"]

   reports:
     - name: "basic-report"
       type: "business"

Safety-Critical Template
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   # examples/templates/safety-critical.yaml
   system:
     name: "safety-critical-system"
     version: "1.0.0"
     safety_level: "critical"

   collectors:
     - name: "safety-collector"
       type: "online"
       config:
         monitoring_interval: 30

   evaluators:
     - name: "safety-evaluator"
       type: "safety"
       config:
         safety_metrics: ["failure_rate", "response_time"]
         critical_thresholds:
           failure_rate: 0.001
           response_time: 50

   reports:
     - name: "safety-report"
       type: "safety"

Industry-Specific Configurations
------------------------------

Aviation Configuration
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   # examples/industries/aviation/aircraft-landing.yaml
   system:
     name: "aircraft-landing-system"
     industry: "aviation"
     safety_level: "critical"

   collectors:
     - name: "flight-data-collector"
       type: "online"
       config:
         data_sources: ["radar", "gps", "sensors"]
         sampling_rate: 10

   evaluators:
     - name: "landing-safety-evaluator"
       type: "safety"
       config:
         safety_metrics: ["landing_accuracy", "approach_speed"]
         critical_thresholds:
           landing_accuracy: 0.99
           approach_speed: 150

   reports:
     - name: "aviation-safety-report"
       type: "safety"

Manufacturing Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   # examples/industries/manufacturing/predictive-maintenance.yaml
   system:
     name: "predictive-maintenance-system"
     industry: "manufacturing"

   collectors:
     - name: "sensor-data-collector"
       type: "online"
       config:
         sensors: ["temperature", "vibration", "pressure"]
         collection_interval: 60

   evaluators:
     - name: "maintenance-evaluator"
       type: "performance"
       config:
         metrics: ["prediction_accuracy", "false_alarm_rate"]
         thresholds:
           prediction_accuracy: 0.90
           false_alarm_rate: 0.05

   reports:
     - name: "manufacturing-report"
       type: "business"

Environment Variables
-------------------

The framework supports environment variables for sensitive configuration:

.. code-block:: bash

   # API Configuration
   export OPENAI_API_KEY="your-api-key"
   export ANTHROPIC_API_KEY="your-api-key"

   # Database Configuration
   export DATABASE_URL="postgresql://user:pass@localhost/db"

   # Custom Endpoints
   export METRICS_ENDPOINT="http://localhost:8000/metrics"
   export ALERTING_WEBHOOK="https://hooks.slack.com/..."

Configuration Inheritance
-----------------------

You can create base configurations and extend them:

.. code-block:: yaml

   # base-config.yaml
   system:
     name: "base-system"
     version: "1.0.0"

   collectors:
     - name: "base-collector"
       type: "offline"

   evaluators:
     - name: "base-evaluator"
       type: "performance"

   # extended-config.yaml
   extends: "base-config.yaml"

   system:
     name: "extended-system"
     description: "Extended system with additional features"

   evaluators:
     - name: "additional-evaluator"
       type: "safety"
       config:
         safety_metrics: ["reliability"]

Validation
---------

The framework validates configuration files before execution:

.. code-block:: bash

   # Validate configuration
   ml-eval validate --config my-config.yaml

   # Check configuration syntax
   ml-eval check --config my-config.yaml

Advanced Configuration
--------------------

Custom Collectors
~~~~~~~~~~~~~~~~

.. code-block:: yaml

   collectors:
     - name: "custom-collector"
       type: "custom"
       class: "my_module.CustomCollector"
       config:
         custom_param: "value"

Custom Evaluators
~~~~~~~~~~~~~~~~

.. code-block:: yaml

   evaluators:
     - name: "custom-evaluator"
       type: "custom"
       class: "my_module.CustomEvaluator"
       config:
         custom_metrics: ["metric1", "metric2"]

Custom Reports
~~~~~~~~~~~~~

.. code-block:: yaml

   reports:
     - name: "custom-report"
       type: "custom"
       class: "my_module.CustomReport"
       config:
         output_format: "pdf"
         template: "custom_template.html"

Configuration Best Practices
--------------------------

1. **Use Templates**: Start with existing templates and customize as needed
2. **Environment Variables**: Store sensitive data in environment variables
3. **Validation**: Always validate configurations before deployment
4. **Documentation**: Document custom configurations and their purposes
5. **Version Control**: Keep configurations in version control
6. **Testing**: Test configurations in development before production

Configuration Examples
--------------------

See the `examples/ <https://github.com/phanhongan/ml-systems-evaluation/tree/main/examples>`_ directory for complete configuration examples for different industries and use cases.

Next Steps
----------

* Read the :doc:`getting-started` guide to run your first evaluation
* Check the :doc:`user-guides/cli-reference` for command-line options
* Review :doc:`user-guides/example-configurations` for more examples 