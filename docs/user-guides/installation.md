# 📦 Installation Guide

This guide provides detailed installation instructions for the ML Systems Evaluation Framework.

## 🔧 Prerequisites

- 🐍 Python 3.11 or higher
- 📦 UV package manager (https://astral.sh/uv/)
- 📥 Git (for cloning the repository)

## 🚀 Installation Methods

### 📋 Method 1: Development Installation (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd ml-systems-evaluation

# Install dependencies and the framework
uv sync --group dev

# (Optional) Activate the UV-managed virtual environment
uv shell
```

### 🏭 Method 2: Production Installation

```bash
# Clone the repository
git clone <repository-url>
cd ml-systems-evaluation

# Install only main dependencies (no dev tools)
uv sync --group main
```

### 🐳 Method 3: Docker Installation

```bash
# Build the Docker image
docker build -t ml-systems-evaluation .

# Run the container
docker run -it ml-systems-evaluation ml-eval --help
```

## ✅ Verification

After installation, verify that everything is working:

```bash
# Check version
ml-eval --version

# Check available commands
ml-eval --help

# List available templates
ml-eval templates list
```

## ⚙️ Configuration

### 🌍 Environment Variables

Set these environment variables for your environment:

```bash
export ML_EVAL_CONFIG_PATH=/path/to/your/config
export ML_EVAL_LOG_LEVEL=INFO
export ML_EVAL_DATA_DIR=/path/to/data
```

### 📦 UV Configuration
If you're using UV, you can configure it for your project:

```bash
# Set Python version
uv python --use 3.11

# Add additional dependencies if needed
uv add package-name

# View dependency tree
uv tree

# Update dependencies
uv update
```

## 🔧 Troubleshooting

### ❌ Common Issues

**🚨 Issue**: "Command not found: ml-eval"
- **✅ Solution**: Ensure UV environment is activated: `uv shell`

**🚨 Issue**: "Module not found"
- **✅ Solution**: Reinstall dependencies: `uv sync`

**🚨 Issue**: "Permission denied"
- **✅ Solution**: Check file permissions or use `sudo` if necessary

### 🆘 Getting Help

- 📖 Check the [Quick Start Guide](getting-started.md) for basic setup
- ⚙️ Review [Configuration Guide](configuration.md) for detailed options
- 🖥️ Consult the [CLI Reference](cli-reference.md) for command details 