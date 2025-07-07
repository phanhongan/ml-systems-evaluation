# 📦 Installation Guide

This guide provides detailed installation instructions for the ML Systems Evaluation Framework.

## 🔧 Prerequisites

- 🐍 Python 3.9 or higher
- 📦 Poetry package manager (https://python-poetry.org/)
- 📥 Git (for cloning the repository)

## 🚀 Installation Methods

### 📋 Method 1: Development Installation (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd ml-systems-evaluation

# Install dependencies and the framework
poetry install

# (Optional) Activate the Poetry-managed virtual environment
poetry shell
```

### 🏭 Method 2: Production Installation

```bash
# Clone the repository
git clone <repository-url>
cd ml-systems-evaluation

# Install only main dependencies (no dev tools)
poetry install --only main
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

### 📦 Poetry Configuration

If you're using Poetry, you can configure it for your project:

```bash
# Set Python version
poetry env use python3.9

# Add dependencies if needed
poetry add pandas numpy scikit-learn

# Show installed packages
poetry show
```

## 🔧 Troubleshooting

### ❌ Common Issues

**🚨 Issue**: "Command not found: ml-eval"
- **✅ Solution**: Ensure Poetry environment is activated: `poetry shell`

**🚨 Issue**: "Module not found"
- **✅ Solution**: Reinstall dependencies: `poetry install`

**🚨 Issue**: "Permission denied"
- **✅ Solution**: Check file permissions or use `sudo` if necessary

### 🆘 Getting Help

- 📖 Check the [Quick Start Guide](getting-started.md) for basic setup
- ⚙️ Review [Configuration Guide](configuration.md) for detailed options
- 🖥️ Consult the [CLI Reference](cli-reference.md) for command details 