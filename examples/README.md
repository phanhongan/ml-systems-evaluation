# ML Systems Evaluation Examples

This directory contains example configurations demonstrating how to use the ML Systems Evaluation framework across different industries and use cases.

## 📁 Directory Structure

### Industry Examples (`industries/`)
Ready-to-use configurations organized by industry:

- **[Aquaculture](./industries/aquaculture/)**: Species classification and environmental monitoring
- **[Aviation](./industries/aviation/)**: Safety-critical aircraft systems  
- **[Cybersecurity](./industries/cybersecurity/)**: AI-driven security operations, alert triage, and incident response
- **[Energy](./industries/energy/)**: Energy optimization recommendations and cost reduction
- **[Manufacturing](./industries/manufacturing/)**: Predictive maintenance and demand forecasting
- **[Maritime](./industries/maritime/)**: Collision avoidance and navigation safety
- **[Semiconductor](./industries/semiconductor/)**: Digital twins and yield prediction

Each industry directory contains:
- Example YAML configuration files
- README.md with usage instructions  
- Industry-specific implementation examples (when applicable)

### Templates (`templates/`)
General-purpose configuration templates:
- **basic-system.yaml**: Basic system configuration template
- **business-critical.yaml**: Business-critical system template with cost optimization  
- **safety-critical.yaml**: Safety-critical system template with zero-tolerance requirements

### Tutorials (`tutorials/`)
Step-by-step guides and learning resources:
- **getting-started/**: Beginner-friendly tutorials
- **custom-evaluators/**: How to create custom evaluators
- **advanced-configuration/**: Configuration patterns

## 🚀 Getting Started

**New to the framework?** See the guides:

- **[📋 Example Configurations Guide](../docs/user-guides/example-configurations.md)** - Detailed guide on how to use these examples
- **[🚀 Getting Started Guide](../docs/user-guides/getting-started.md)** - Basic setup and first evaluation  
- **[⚙️ Configuration Reference](../docs/user-guides/configuration.md)** - Complete YAML syntax reference

## 🤝 Contributing

When adding new examples:
- Follow naming conventions: kebab-case for YAML files, snake_case for Python files
- Organize by industry in the appropriate subdirectory  
- Include a README.md file for each industry directory
- Provide both configuration examples (YAML) and implementation examples (Python) when applicable

For detailed contribution guidelines, see the [Extending the Framework](../docs/developer/extending.md) guide.
