# LLM Integration Guide

This guide shows how LLM integration works in the ML Systems Evaluation Framework.

## 🏗️ Architecture Overview

### Hybrid Deterministic + LLM Approach

The framework uses a **hybrid architecture** that combines:
- **Deterministic evaluation**: Traditional quantitative metrics and threshold checking
- **LLM-enhanced analysis**: Intelligent natural language explanations and contextual reasoning

### LLM Components

1. **LLMAssistantEngine**: Configuration generation, troubleshooting, documentation
2. **LLMAnalysisEngine**: Pattern recognition, anomaly detection, correlation analysis
3. **Evaluator-specific LLM integration**: Domain-specific intelligent analysis

## 🔧 Implementation Options

### **Option 1: Direct Provider Integration**

```python
# In ml_eval/evaluators/interpretability.py
def _call_llm(self, prompt: str, context: dict[str, Any]) -> str:
    """Make LLM call using provider directly"""
    try:
        import asyncio
        
        async def make_llm_call():
            # Access provider directly from config
            from ..llm.providers import create_llm_provider
            
            provider_config = self.llm_config.get("provider_config", {})
            provider = create_llm_provider(
                self.llm_config.get("provider", "openai"), 
                provider_config
            )
            
            response = await provider.generate_response(
                prompt=prompt,
                context=context,
                temperature=0.1
            )
            return response
        
        # Run async call
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(make_llm_call())
        finally:
            loop.close()
            
    except Exception as e:
        self.logger.warning(f"LLM call failed: {e}")
        return self._generate_fallback_explanation(context)
```

### **Option 2: Enhanced LLM Assistant**

```python
# In ml_eval/llm/assistant.py - Add this method
async def generate_explanation(self, prompt: str, context: dict[str, Any]) -> str:
    """Generate explanation using LLM"""
    try:
        response = await self.provider.generate_response(
            prompt=prompt,
            context=context,
            temperature=0.1
        )
        return response
    except Exception as e:
        self.logger.error(f"LLM explanation generation failed: {e}")
        return "Error generating explanation"
```

### **Option 3: Configuration-Driven Approach**

```yaml
# In your config file
evaluators:
  - type: "interpretability"
    config:
      use_llm: true
      llm:
        provider: "openai"
        provider_config:
          api_key: "${OPENAI_API_KEY}"
          model: "gpt-4"
          temperature: 0.1
          max_tokens: 1000
```

## 🚀 Step-by-Step Implementation

### **1. Update the Evaluator**

```python
# In ml_eval/evaluators/interpretability.py
def _generate_component_explanation(self, component: str, metrics: dict[str, Any], score: float) -> str:
    """Generate natural language explanation for a component"""
    try:
        # Build context and prompt
        context = {
            "component": component,
            "score": score,
            "metrics": {k: v for k, v in metrics.items() if k.startswith(f"{component}_")},
            "threshold": self.thresholds.get(f"{component}_interpretability", 0.7),
        }
        
        prompt = f"""
        Analyze the interpretability of the {component} component in a safety-critical ML system.
        
        Component: {component}
        Interpretability Score: {score:.3f}
        Threshold: {context['threshold']}
        Component Metrics: {context['metrics']}
        
        Generate a natural language explanation that:
        1. Explains what this score means for system safety
        2. Identifies potential risks if below threshold
        3. Suggests specific improvements if needed
        4. Uses clear, non-technical language for stakeholders
        
        Focus on safety implications and regulatory compliance.
        """
        
        # Make LLM call with fallback
        if self.use_llm and self.llm_assistant:
            return self._call_llm(prompt, context)
        else:
            return self._generate_simulated_explanation(context)
            
    except Exception as e:
        return f"Error generating explanation for {component}: {e!s}"
```

### **2. Implement LLM Call**

```python
def _call_llm(self, prompt: str, context: dict[str, Any]) -> str:
    """Make LLM call"""
    try:
        import asyncio
        
        async def make_llm_call():
            from ..llm.providers import create_llm_provider
            
            # Create provider from config
            provider_config = self.llm_config.get("provider_config", {})
            provider = create_llm_provider(
                self.llm_config.get("provider", "openai"), 
                provider_config
            )
            
            # Make the call
            response = await provider.generate_response(
                prompt=prompt,
                context=context,
                temperature=self.llm_config.get("temperature", 0.1)
            )
            return response
        
        # Execute async call
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(make_llm_call())
        finally:
            loop.close()
            
    except Exception as e:
        self.logger.warning(f"LLM call failed: {e}, falling back to simulation")
        return self._generate_simulated_explanation(context)
```

### **3. Add Configuration Options**

```python
# In ml_eval/evaluators/interpretability.py - Update __init__
def __init__(self, config: dict[str, Any]):
    super().__init__(config)
    self.logger = logging.getLogger(__name__)
    
    # LLM configuration
    self.use_llm = config.get("use_llm", True)
    self.llm_config = config.get("llm", {})
    
    # Initialize LLM components
    self.llm_assistant = None
    self.llm_analyzer = None
    
    if self.use_llm:
        try:
            from ..llm import LLMAssistantEngine, LLMAnalysisEngine
            self.llm_assistant = LLMAssistantEngine(self.llm_config)
            self.llm_analyzer = LLMAnalysisEngine(self.llm_config)
            self.logger.info("✅ LLM integration enabled")
                
        except Exception as e:
            self.logger.warning(f"❌ LLM initialization failed: {e}")
```

## 🎯 Implemented LLM-Enhanced Evaluators

### 1. InterpretabilityEvaluator

**Capabilities:**
- ✅ **Natural language explanations** for model decisions
- ✅ **Decision transparency analysis** with contextual reasoning
- ✅ **Feature importance narratives** explaining feature significance
- ✅ **Cross-component reasoning** linking perception → planning → control
- ✅ **Safety justifications** for regulatory compliance

**Example Output:**
```json
{
  "llm_enhanced": {
    "natural_language_explanations": {
      "perception": "The perception component demonstrates good interpretability (score: 0.85), meeting the safety threshold of 0.7. This means the system can adequately explain its perception decisions to regulators and stakeholders, which is crucial for safety-critical applications."
    },
    "decision_transparency_analysis": {
      "transparency_patterns": ["Strong decision transparency across all components"],
      "improvement_areas": [],
      "best_practices": ["Maintain current transparency standards"]
    }
  }
}
```

### 2. EdgeCaseEvaluator

**Capabilities:**
- ✅ **Intelligent edge case generation** based on domain knowledge
- ✅ **Failure pattern analysis** with correlation insights
- ✅ **Scenario reasoning** for complex edge case scenarios
- ✅ **Adaptive stress testing** based on learned patterns
- ✅ **Safety margin analysis** for critical scenarios

**Example Output:**
```json
{
  "llm_enhanced": {
    "intelligent_edge_case_generation": {
      "generated_scenarios": [
        "Targeted stress test for perception system (current score: 0.65)",
        "Low visibility perception testing",
        "Sensor occlusion scenarios"
      ],
      "boundary_conditions": [
        "Test system behavior at maximum sensor range",
        "Validate performance under minimum visibility conditions"
      ]
    }
  }
}
```

### 3. SafetyEvaluator

**Capabilities:**
- ✅ **Intelligent FMEA analysis** with contextual risk assessment
- ✅ **Dynamic risk assessment** with adaptive thresholds
- ✅ **Safety margin optimization** based on environmental factors
- ✅ **Emergency procedure enhancement** with intelligent recommendations
- ✅ **Compliance reasoning** for complex regulatory requirements

**Example Output:**
```json
{
  "llm_enhanced": {
    "intelligent_fmea_analysis": {
      "failure_mode_insights": [
        "High-risk failure mode detected: sensor_failure_rate (probability: 0.15)"
      ],
      "mitigation_strategies": [
        "Implement sensor redundancy and fusion for sensor_failure_rate"
      ],
      "risk_prioritization": {
        "critical_failures": ["sensor_failure_rate"],
        "moderate_risks": ["communication_failure_rate"]
      }
    }
  }
}
```

## 🔧 Configuration Examples

### **LLM Configuration**
```yaml
evaluators:
  - type: "interpretability"
    config:
      use_llm: true
      llm:
        provider: "openai"
        provider_config:
          api_key: "${OPENAI_API_KEY}"
          model: "gpt-4"
          temperature: 0.1
          max_tokens: 1000
```

### **LLM Disabled Configuration**
```yaml
evaluators:
  - type: "interpretability"
    config:
      use_llm: false  # Disable LLM entirely
      thresholds:
        overall_interpretability: 0.7
```

## 🚨 Error Handling and Fallbacks

### **1. API Key Issues**
```python
def _validate_llm_config(self) -> bool:
    """Validate LLM configuration"""
    if not self.use_llm:
        return False
        
    provider_config = self.llm_config.get("provider_config", {})
    api_key = provider_config.get("api_key") or os.environ.get("OPENAI_API_KEY")
    
    if not api_key:
        self.logger.warning("❌ No API key found, falling back to simulation")
        return False
        
    return True
```

### **2. Network Issues**
```python
def _test_llm_connectivity(self) -> bool:
    """Test LLM API connectivity"""
    try:
        import asyncio
        
        async def test_connection():
            from ..llm.providers import create_llm_provider
            
            provider = create_llm_provider("openai", self.llm_config.get("provider_config", {}))
            response = await provider.generate_response("Test", {}, temperature=0.1)
            return len(response) > 0
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(test_connection())
        finally:
            loop.close()
            
    except Exception as e:
        self.logger.warning(f"❌ LLM connectivity test failed: {e}")
        return False
```

### **3. Rate Limiting**
```python
def _handle_rate_limiting(self, retry_count: int = 0) -> str:
    """Handle rate limiting with exponential backoff"""
    if retry_count >= 3:
        return self._generate_simulated_explanation(context)
    
    wait_time = 2 ** retry_count  # Exponential backoff
    time.sleep(wait_time)
    
    return self._call_llm_with_retry(prompt, context, retry_count + 1)
```

### **4. Graceful Degradation**
```python
if self.use_llm:
    try:
        # LLM-enhanced analysis
        llm_result = await self.llm_assistant.analyze(metrics)
        return llm_result
    except Exception as e:
        self.logger.warning(f"LLM analysis failed: {e}, falling back to deterministic evaluation")
        return self.deterministic_analysis(metrics)
else:
    return self.deterministic_analysis(metrics)
```

## 📊 Performance Considerations

### **Caching Strategy**
- **LLM responses cached** to avoid redundant API calls
- **Deterministic results cached** for comparison
- **Configurable cache TTL** for different analysis types

### **Async Processing**
- **Non-blocking LLM calls** for real-time evaluation
- **Parallel processing** of multiple evaluators
- **Timeout handling** for long-running analyses

## 🔒 Security and Privacy

### **Data Handling**
- **No sensitive data sent to LLM** without explicit configuration
- **Local processing option** for sensitive systems
- **Data anonymization** for external LLM providers

### **API Key Management**
- **Environment variable configuration**
- **Secure key storage** in configuration
- **Key rotation support**

## 📊 Performance Comparison

| Aspect | Simulation | LLM Integration |
|--------|------------|----------|
| **Speed** | ✅ Instant | ⚠️ 1-5 seconds |
| **Cost** | ✅ Free | ❌ $0.01-0.10 per call |
| **Reliability** | ✅ 100% | ⚠️ Network dependent |
| **Quality** | ⚠️ Basic | ✅ Rich and contextual |
| **Consistency** | ✅ Perfect | ⚠️ Variable |

## 🎯 Best Practices

### **1. Development Workflow**
```bash
# Use simulation for development
export LLM_MODE=simulation

# Use LLM for production testing
export LLM_MODE=llm
export OPENAI_API_KEY=your-key-here
```

### **2. Testing Strategy**
```python
# Test both modes
def test_llm_modes():
    # Test simulation mode
    config_sim = {"use_llm": False}
    evaluator_sim = InterpretabilityEvaluator(config_sim)
    
    # Test LLM mode
    config_llm = {"use_llm": True, "llm": {"provider_config": {"api_key": "test"}}}
    evaluator_llm = InterpretabilityEvaluator(config_llm)
```

### **3. Monitoring and Logging**
```python
# Add comprehensive logging
def _log_llm_usage(self, mode: str, success: bool, duration: float):
    self.logger.info(f"LLM call: mode={mode}, success={success}, duration={duration:.2f}s")
```

## 🔍 Troubleshooting

### **Common Issues:**

1. **API Key Not Found**
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

2. **Network Connectivity**
   ```bash
   curl -H "Authorization: Bearer $OPENAI_API_KEY" https://api.openai.com/v1/models
   ```

3. **Rate Limiting**
   ```python
   # Add exponential backoff
   time.sleep(2 ** retry_count)
   ```

4. **Invalid Response**
   ```python
   # Add response validation
   if not response or len(response.strip()) < 10:
       return self._generate_fallback_explanation(context)
   ```

## 🚀 Usage Examples

### **Basic LLM-Enhanced Evaluation**
```bash
python -m ml_eval.cli.main evaluate examples/llm-enhanced-demo.yaml
```

### **Configuration with LLM**
```yaml
evaluators:
  - type: "interpretability"
    config:
      use_llm: true
      llm:
        provider: "openai"
```

This guide provides a complete path for LLM integration while maintaining safety and reliability. 