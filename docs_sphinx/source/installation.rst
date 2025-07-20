Installation Guide
=================

This guide covers how to install the ML Systems Evaluation Framework and its dependencies.

.. note::
   For a more detailed installation guide with troubleshooting and advanced configuration,
   see the :doc:`../docs/user-guides/installation` guide in the Markdown documentation.

Prerequisites
------------

* Python 3.11 or higher
* pip or uv package manager
* Git (for development)

Installation Methods
-------------------

Using pip
~~~~~~~~~

.. code-block:: bash

   # Install from PyPI
   pip install ml-systems-evaluation

   # Install with development dependencies
   pip install ml-systems-evaluation[dev]

Using uv (Recommended)
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Install using uv
   uv add ml-systems-evaluation

   # Install with development dependencies
   uv add --group dev ml-systems-evaluation

From Source
~~~~~~~~~~

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/phanhongan/ml-systems-evaluation.git
   cd ml-systems-evaluation

   # Install in development mode
   uv sync --group dev
   uv run pip install -e .

Dependencies
-----------

Core Dependencies
~~~~~~~~~~~~~~~~

* `PyYAML <https://pyyaml.org/>`_ - Configuration file parsing
* `requests <https://requests.readthedocs.io/>`_ - HTTP client for API calls
* `click <https://click.palletsprojects.com/>`_ - Command-line interface
* `aiohttp <https://aiohttp.readthedocs.io/>`_ - Async HTTP client
* `openai <https://platform.openai.com/docs>`_ - OpenAI API integration
* `anthropic <https://docs.anthropic.com/>`_ - Anthropic API integration
* `python-dotenv <https://github.com/theskumar/python-dotenv>`_ - Environment variable management
* `numpy <https://numpy.org/>`_ - Numerical computing

Development Dependencies
~~~~~~~~~~~~~~~~~~~~~~~

* `pytest <https://pytest.org/>`_ - Testing framework
* `pytest-cov <https://pytest-cov.readthedocs.io/>`_ - Coverage reporting
* `pytest-mock <https://pytest-mock.readthedocs.io/>`_ - Mocking utilities
* `pytest-asyncio <https://pytest-asyncio.readthedocs.io/>`_ - Async test support
* `ruff <https://docs.astral.sh/ruff/>`_ - Code formatting and linting

Verification
-----------

After installation, verify that the framework is working correctly:

.. code-block:: bash

   # Check installation
   ml-eval --version

   # Run a quick test
   ml-eval evaluate --help

   # Test with a basic configuration
   ml-eval evaluate --config examples/templates/basic-system.yaml

Configuration
------------

The framework uses YAML configuration files. See the :doc:`configuration` guide for detailed configuration options.

Environment Variables
-------------------

Set up environment variables for API access:

.. code-block:: bash

   # OpenAI API
   export OPENAI_API_KEY="your-openai-api-key"

   # Anthropic API
   export ANTHROPIC_API_KEY="your-anthropic-api-key"

   # Optional: Custom API endpoints
   export OPENAI_API_BASE="https://api.openai.com/v1"
   export ANTHROPIC_API_BASE="https://api.anthropic.com"

Troubleshooting
--------------

Common Issues
~~~~~~~~~~~~

**Import Errors**: Ensure you're using Python 3.11+ and have all dependencies installed.

**API Key Errors**: Verify your API keys are set correctly in environment variables.

**Configuration Errors**: Check that your YAML configuration files are valid.

**Permission Errors**: Ensure you have write permissions in the installation directory.

Getting Help
-----------

* Check the :doc:`getting-started` guide for quick setup
* Review the :doc:`configuration` guide for detailed configuration options
* See the :doc:`user-guides/cli-reference` for command-line usage
* Report issues on the `GitHub repository <https://github.com/phanhongan/ml-systems-evaluation>`_ 