# Configuration Management Strategy

## Overview

This document outlines the strategy for managing example configurations and potential future template systems in the ML Systems Evaluation Framework.

## Current Implementation

The framework has TWO configuration systems:

### 1. Internal Default Configurations (Config Factory + TemplateManager)
- **Location**: `ml_eval/templates/files/` with minimal default YAML files
- **Implementation**: Config Factory uses TemplateManager to load basic defaults
- **Reality**: Files are very minimal (5-10 lines) with just basic default values
- **Usage**: Used internally by the framework for component creation with fallback to hardcoded configs

### 2. Example Configurations (User-Facing)
- **Example Location**: `examples/industries/` with industry-specific subdirectories  
- **CLI Support**: `ml-eval create-config` command for basic configuration generation
- **User Workflow**: Copy and customize existing example configurations

### Current Structure

**Internal Default Configurations:**
```
ml_eval/templates/files/
├── collectors/          # Minimal default configs (5-10 lines each)
├── evaluators/          # Minimal default configs (5-10 lines each)  
├── reports/             # Minimal default configs (5-10 lines each)
└── industries/          # Industry-specific templates (more comprehensive)
```

**User-Facing Examples:**
```
examples/industries/
├── aviation/            # Aviation industry examples
├── manufacturing/       # Manufacturing industry examples  
├── maritime/            # Maritime industry examples
├── semiconductor/       # Semiconductor industry examples
├── aquaculture/         # Aquaculture industry examples
└── cybersecurity/       # Cybersecurity industry examples
```

### Current Workflows

**Internal Default Configuration Usage (Framework Code):**
```python
# Config Factory loads minimal defaults then applies user settings
from ml_eval.config import ConfigFactory

factory = ConfigFactory()

# Loads minimal defaults from base-collector_online.yaml (just 6 lines)
# Then merges with user-provided endpoint
collector_config = factory.create_collector_config("online", endpoint="http://...")

# Loads minimal defaults from base-evaluator_performance.yaml (just 9 lines)  
# Then merges with user-provided thresholds
evaluator_config = factory.create_evaluator_config("performance", thresholds={...})
```

**User Workflow (Copy Examples):**
```bash
# Copy existing example
cp examples/industries/manufacturing/predictive-maintenance.yaml my-config.yaml

# Create new configuration
ml-eval create-config --output my-config.yaml --system-name "My System"

# Customize and use
nano my-config.yaml
ml-eval run my-config.yaml
```

## Future Template System (Planned Features)

### Phase 1: 🔄 Enhanced Configuration Management

- ✅ **TemplateManager**: Already exists and loads minimal defaults from `ml_eval/templates/files/`
- ✅ **Config Factory**: Already uses TemplateManager for loading basic defaults
- 🔄 **Rich Template Files**: Replace minimal defaults with comprehensive templates
- 🔄 **CLI Commands**: `ml-eval template` commands for template management
- 🔄 **Enhanced Validation**: Advanced template validation and error checking

### Phase 2: 🔄 AI-Powered Templates (Future)

- 🔄 LLM-powered template generation and customization
- 🔄 Natural language template creation and modification
- 🔄 Intelligent template validation and error correction
- 🔄 Template marketplace/registry for community contributions
- 🔄 Template sharing and distribution ecosystem

### Planned Template Structure (Future)

```
ml_eval/templates/files/
├── collectors/          # Data collection configurations
├── evaluators/          # Evaluation method configurations  
├── reports/             # Report generation configurations
└── industries/          # Industry-specific templates
```

## Migration Strategy

### From Current (Examples) to Future (Templates)

1. **Phase 1**: Maintain current example system while building template infrastructure
2. **Phase 2**: Migrate examples to formal template system
3. **Phase 3**: Add AI-powered features and template marketplace

### Backward Compatibility

- Current example configurations will remain supported
- Migration tools will be provided when template system is ready
- Users can continue using current workflow

## Conclusion

**Current State**: The framework has a dual-system approach:

**Internal Default Configuration System (Config Factory):**
- **Minimal default loading** from `ml_eval/templates/files/` (5-10 lines per file)
- **Basic defaults** for collectors, evaluators, reports (not comprehensive templates)
- **Programmatic API** for framework components
- **Fallback to hardcoded configs** when files don't exist or are insufficient

**User-Facing Examples:**
- **Simple workflow** using standard file operations
- **Industry-specific examples** for 6 industries  
- **Basic configuration generation** via `create-config` command

**Future Vision**: Build a comprehensive template system with:
- **Rich template files** replacing the current minimal defaults
- **CLI template commands** for template management (`ml-eval template list`, `use`, etc.)
- **AI-powered generation** and customization via LLM integration
- **Template marketplace** for sharing community templates
- **Unified user experience** bridging internal defaults and user examples

This strategy builds upon the existing Config Factory infrastructure but requires creating comprehensive templates to replace the current minimal default files. 