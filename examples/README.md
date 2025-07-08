# ML Systems Evaluation Examples

This directory contains comprehensive examples demonstrating how to use the ML Systems Evaluation framework across different industries and use cases.

## Directory Structure

### Industry Examples (`industries/`)
Ready-to-use configurations organized by industry:

- **[Aviation](./industries/aviation/)**: Safety-critical aircraft systems
- **[Maritime](./industries/maritime/)**: Collision avoidance and navigation safety
- **[Manufacturing](./industries/manufacturing/)**: Predictive maintenance and demand forecasting
- **[Semiconductor](./industries/semiconductor/)**: Digital twins and yield prediction
- **[Aquaculture](./industries/aquaculture/)**: Species classification and environmental monitoring

### Templates (`templates/`)
General-purpose configuration templates for different system types:
- **basic-system.yaml**: Basic system configuration template
- **business-critical.yaml**: Business-critical system template with cost optimization
- **safety-critical.yaml**: Safety-critical system template with zero-tolerance requirements

### Tutorials (`tutorials/`)
Step-by-step guides and learning resources:
- **getting-started/**: Beginner-friendly tutorials
- **custom-evaluators/**: How to create custom evaluators
- **advanced-configuration/**: Advanced configuration patterns

## Quick Start

1. **Choose your industry**: Navigate to the relevant industry directory above
2. **Select an example**: Each industry directory contains specific examples with detailed READMEs
3. **Customize**: Modify the configuration to match your requirements
4. **Run**: Use the ML Systems Evaluation framework to evaluate your system

## Contributing

When adding new examples:
- Follow naming conventions: kebab-case for YAML files, snake_case for Python files
- Organize by industry in the appropriate subdirectory
- Include a README.md file for each industry directory
- Provide both configuration examples (YAML) and implementation examples (Python)
