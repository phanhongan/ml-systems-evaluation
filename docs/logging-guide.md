# Logging Guide

This document describes the comprehensive logging implementation in the ML Systems Evaluation Framework during development.

## 🔧 Current Implementation

### **Logging Calls**
```python
self.logger.debug("🚀 Starting Interpretability Evaluation")
self.logger.debug(f"📊 Input metrics: {len(metrics)} items")
self.logger.debug(f"🧠 LLM enabled: {self.use_llm}")
```

## 📊 Implementation Statistics

### **Files with Logging:**
1. **`ml_eval/evaluators/interpretability.py`** - 45+ logging calls
2. **`ml_eval/evaluators/edge_case.py`** - 30+ logging calls  
3. **`ml_eval/evaluators/safety.py`** - 25+ logging calls
4. **`ml_eval/cli/main.py`** - Logging configuration

### **Total Implementation:**
- **100+ logging calls** across evaluators
- **3 evaluator files** with comprehensive logging
- **1 CLI file** with logging configuration
- **LLM integration** as default behavior

## 🎨 Current Logging Output

### **Clean and Structured**
```
DEBUG: 📤 Sending LLM prompt for perception:
DEBUG:    📝 Prompt length: 724 characters
DEBUG:    🎯 Component: perception
DEBUG:    📊 Score: 0.000
DEBUG:    🎚️ Threshold: 0.700
DEBUG:    📋 Prompt preview: Analyze the interpretability of the perception component in a safety-critical ML system. Component: perception Interpretability Score: 0.000...
DEBUG: 📥 Received LLM response for perception:
DEBUG:    📏 Response length: 2374 characters
DEBUG:    📋 Response preview: 1. Interpretability Score Meaning for System Safety: The interpretability score of the perception component in our ML system is currently at 0.0. This score is a measure of how easily we can understan...
```

## 🎯 Logging Features

### **1. Logging Levels**
```python
# Debug level for detailed reasoning chain
self.logger.debug("🧠 Starting LLM reasoning chain for perception")

# Warning level for errors and fallbacks
self.logger.warning("❌ LLM call failed, falling back to simulation")

# Info level for initialization
self.logger.info("✅ LLM-enhanced evaluator initialized successfully")
```

### **2. Configurable Logging**
```bash
# Enable verbose logging to see reasoning chain
python -m ml_eval.cli.main --verbose evaluate config.yaml

# Standard logging (INFO level)
python -m ml_eval.cli.main evaluate config.yaml

# Filter specific log levels
python -m ml_eval.cli.main --verbose evaluate config.yaml 2>&1 | grep "DEBUG:"
```

### **3. Structured Logging**
```python
# Consistent formatting across all evaluators
self.logger.debug(f"📊 Component score: {score:.3f}, Threshold: {threshold}")
self.logger.debug(f"📋 Available metrics: {list(metrics.keys())}")
self.logger.debug(f"📤 Sending LLM prompt for {component}:")
```

## 🔧 Technical Implementation

### **1. Logging Configuration**
```python
def setup_logging(verbose: bool = False) -> None:
    """Setup logging configuration"""
    log_format = "%(levelname)s: %(message)s"
    
    if verbose:
        logging.basicConfig(
            level=logging.DEBUG,
            format=log_format,
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.StreamHandler(sys.stderr)
            ]
        )
        
        # Filter out verbose HTTP request logs from external libraries
        logging.getLogger("httpx").setLevel(logging.WARNING)
        logging.getLogger("openai").setLevel(logging.WARNING)
        logging.getLogger("stainless").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        logging.getLogger("requests").setLevel(logging.WARNING)
        
        # Set our framework logs to DEBUG level
        logging.getLogger("ml_eval").setLevel(logging.DEBUG)
    else:
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.StreamHandler(sys.stderr)
            ]
        )
```

### **2. Logger Initialization**
```python
# In each evaluator class
self.logger = logging.getLogger(__name__)
```

### **3. CLI Integration**
```python
# Add verbose flag to CLI
parser.add_argument(
    "--verbose", "-v",
    action="store_true",
    help="Enable verbose output with debug logging"
)

# Setup logging based on flag
setup_logging(verbose=getattr(parsed_args, 'verbose', False))
```

### **4. Enhanced Logging Format**
```python
# Structured logging with emojis and better formatting
self.logger.debug(f"📝 Prompt length: {len(prompt)} characters")
self.logger.debug(f"🎯 Component: {component}")
self.logger.debug(f"📊 Score: {score:.3f}")
self.logger.debug(f"🎚️ Threshold: {threshold:.3f}")
```

### **5. Preview Generation**
```python
# Log a preview of the prompt (first 200 chars)
prompt_preview = prompt[:200].replace('\n', ' ').strip()
self.logger.debug(f"📋 Prompt preview: {prompt_preview}...")

# Log a preview of the response (first 200 chars)
response_preview = response[:200].replace('\n', ' ').strip()
self.logger.debug(f"📋 Response preview: {response_preview}...")
```

## 📈 Logging Categories

### **1. Evaluation Flow Tracking**
```
DEBUG: 🚀 Starting Interpretability Evaluation
DEBUG: 📊 Input metrics: 0 items
DEBUG: 🧠 LLM enabled: True
DEBUG: 📈 Evaluating overall interpretability...
DEBUG:    Overall score: 0.000
```

### **2. Component Analysis**
```
DEBUG: 🔍 Starting explanation generation for perception
DEBUG:    Score: 0.000
DEBUG:    Available metrics: 0 items
DEBUG:    Threshold: 0.7
DEBUG:    Score vs threshold: ❌ Below
```

### **3. LLM Call Tracking**
```
DEBUG: 📤 Sending LLM prompt for perception:
DEBUG:    📝 Prompt length: 724 characters
DEBUG:    🎯 Component: perception
DEBUG:    📊 Score: 0.000
DEBUG:    🎚️ Threshold: 0.700
DEBUG:    📋 Prompt preview: Analyze the interpretability of the perception component...
```

### **4. Response Analysis**
```
DEBUG: 📥 Received LLM response for perception:
DEBUG:    📏 Response length: 2374 characters
DEBUG:    📋 Response preview: 1. Interpretability Score Meaning for System Safety...
```

### **5. Error Handling**
```
WARNING: ❌ LLM call failed: API key not found
WARNING: ❌ LLM call failed: Network error, falling back to simulation
DEBUG: 🔄 Using deterministic fallback for perception
```

## 🎯 Emoji Legend

### **📤 Sending Operations**
- **📤**: Sending LLM prompt
- **📝**: Prompt length
- **🎯**: Component being analyzed
- **📊**: Score values
- **🎚️**: Threshold values
- **📋**: Preview content

### **📥 Receiving Operations**
- **📥**: Received LLM response
- **📏**: Response length
- **📋**: Response preview

### **🔍 Analysis Operations**
- **🔍**: Starting analysis
- **📊**: Metrics and scores
- **📋**: Available data
- **❌/✅**: Status indicators

### **🚀 Flow Operations**
- **🚀**: Starting evaluation
- **📈**: Progress tracking
- **🧠**: LLM operations
- **⚠️**: Alerts and warnings

## 🎨 Visual Structure

### **1. Consistent Indentation**
```
DEBUG: 📤 Sending LLM prompt for perception:
DEBUG:    📝 Prompt length: 724 characters
DEBUG:    🎯 Component: perception
DEBUG:    📊 Score: 0.000
DEBUG:    🎚️ Threshold: 0.700
```

### **2. Preview Truncation**
```python
# Clean preview without line breaks
prompt_preview = prompt[:200].replace('\n', ' ').strip()
self.logger.debug(f"📋 Prompt preview: {prompt_preview}...")
```

### **3. Formatted Numbers**
```python
# Consistent decimal formatting
self.logger.debug(f"📊 Score: {score:.3f}")
self.logger.debug(f"🎚️ Threshold: {threshold:.3f}")
```

## 🎯 Usage Examples

### **1. Development Debugging**
```bash
# Enable full debug logging
python -m ml_eval.cli.main --verbose evaluate config.yaml

# Filter for specific components
python -m ml_eval.cli.main --verbose evaluate config.yaml 2>&1 | grep "perception"

# Track LLM calls only
python -m ml_eval.cli.main --verbose evaluate config.yaml 2>&1 | grep "🧠"

# Filter for specific operations
python -m ml_eval.cli.main --verbose evaluate config.yaml 2>&1 | grep "📤"
python -m ml_eval.cli.main --verbose evaluate config.yaml 2>&1 | grep "📥"
```

### **2. Production Monitoring**
```bash
# Standard logging (INFO level)
python -m ml_eval.cli.main evaluate config.yaml

# Check for errors only
python -m ml_eval.cli.main evaluate config.yaml 2>&1 | grep "WARNING\|ERROR"
```

### **3. Performance Analysis**
```bash
# Track response sizes
python -m ml_eval.cli.main --verbose evaluate config.yaml 2>&1 | grep "📏"

# Monitor prompt efficiency
python -m ml_eval.cli.main --verbose evaluate config.yaml 2>&1 | grep "📝"

# Track specific components
python -m ml_eval.cli.main --verbose evaluate config.yaml 2>&1 | grep "perception"

# Monitor score thresholds
python -m ml_eval.cli.main --verbose evaluate config.yaml 2>&1 | grep "🎚️"
```

## 🔍 Logging Quality

### **1. Consistent Logging Levels**
- **DEBUG**: Detailed reasoning chain and internal operations
- **INFO**: Important initialization and completion events
- **WARNING**: Errors that don't break execution (fallbacks)
- **ERROR**: Critical errors that affect functionality

### **2. Structured Messages**
- **Emojis**: Visual indicators for different log categories
- **Indentation**: Hierarchical information display
- **Consistent Format**: Uniform message structure across evaluators

### **3. Error Context**
```python
# Contextual error information
self.logger.warning(f"❌ LLM call failed for {component}: {e}")
self.logger.debug(f"🔄 Using deterministic fallback for {component}")
```

## ✅ Current Features

### **1. Readability**
- **No verbose HTTP logs**: Filtered out external library noise
- **Structured information**: Clear hierarchy with indentation
- **Visual indicators**: Emojis for quick recognition

### **2. Usability**
- **Preview content**: See what's being sent/received without full dumps
- **Formatted numbers**: Consistent decimal precision
- **Status indicators**: Clear success/failure indicators

### **3. Performance**
- **Reduced noise**: Only relevant information shown
- **Faster scanning**: Visual patterns for quick identification
- **Better filtering**: Easy to grep for specific operations

### **4. Developer Experience**
- **Intuitive logging**: Easy to understand what's happening
- **Debug-friendly**: Clear separation of concerns
- **Development-ready**: Appropriate log levels for development environment

## 🚀 Development Features

### **1. Log File Output**
```python
# Add file handler for persistent logging
file_handler = logging.FileHandler('evaluation.log')
file_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
```

### **2. Structured Logging**
```python
# JSON format for machine-readable logs
import json
log_data = {
    "component": component,
    "score": score,
    "threshold": threshold,
    "timestamp": datetime.now().isoformat()
}
self.logger.debug(f"Component analysis: {json.dumps(log_data)}")
```

### **3. Performance Metrics**
```python
# Add timing information
import time
start_time = time.time()
# ... LLM call ...
duration = time.time() - start_time
self.logger.debug(f"⏱️ LLM call completed in {duration:.2f}s")
```

## ✅ Current Status

- [x] **Interpretability Evaluator**: Comprehensive logging implementation
- [x] **Edge Case Evaluator**: Comprehensive logging implementation
- [x] **Safety Evaluator**: Comprehensive logging implementation
- [x] **CLI Main**: Logging configuration with verbose flag
- [x] **LLM Integration**: Default behavior with fallbacks
- [x] **Log Levels**: Proper DEBUG/INFO/WARNING/ERROR usage
- [x] **Testing**: Verified logging works correctly
- [x] **Documentation**: Usage examples and guides

## 🎉 Current Implementation

The logging implementation provides clean, structured, and visually appealing debug information during development! 

**Key features:**
- ✅ **Filtered HTTP noise**: No verbose request/response dumps
- ✅ **Visual structure**: Emojis and indentation for clarity
- ✅ **Preview content**: See prompts and responses without full dumps
- ✅ **Consistent formatting**: Uniform number formatting and structure
- ✅ **Better categorization**: Clear separation of different operations
- ✅ **Configurable Logging**: Enable/disable debug output with `--verbose`
- ✅ **Structured Messages**: Consistent formatting with emojis and indentation
- ✅ **Proper Log Levels**: DEBUG, INFO, WARNING, ERROR appropriately used
- ✅ **Error Context**: Detailed error information with fallback tracking
- ✅ **Performance Visibility**: Response times, prompt lengths, and success rates
- ✅ **LLM Integration**: Default behavior with comprehensive logging

The chain of thoughts logging provides excellent visibility into the LLM-enhanced evaluation process during development! 🎉 