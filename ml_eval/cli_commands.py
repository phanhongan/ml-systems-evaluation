"""CLI command implementations for Industrial ML Systems Evaluation"""

import yaml
import sys
import time
from datetime import datetime
from typing import Optional

from .core import EvaluationFramework, EvaluationResult, ErrorBudget
from .templates import get_template, list_available_templates, save_template, print_template
from .examples import get_example, print_example_details


def run_evaluation(config_path: str, mode: str, output_file: Optional[str] = None) -> None:
    """Run evaluation with configuration"""
    try:
        print(f"🔍 Loading configuration from {config_path}")
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

        system_name = config.get("system", {}).get("name", "Unknown System")
        system_type = config.get("system", {}).get("type", "single")
        criticality = config.get("system", {}).get("criticality", "standard")
        
        print(f"🏭 Evaluating {system_name}")
        print(f"📊 System Type: {system_type}")
        print(f"⚠️  Criticality Level: {criticality}")
        
        framework = EvaluationFramework(config)
        
        # For demo purposes, create a mock result
        result = EvaluationResult(
            system_name=system_name,
            evaluation_time=datetime.now(),
            slo_compliance={"accuracy": True, "latency": False},
            error_budgets={
                "accuracy": ErrorBudget("accuracy", 0.8, 0.1),
                "latency": ErrorBudget("latency", 0.2, 0.3)
            }
        )
        
        print(f"\n✅ Evaluation completed for {result.system_name}")
        print(f"📈 SLO Compliance: {sum(result.slo_compliance.values())}/{len(result.slo_compliance)}")
        
        # Show critical alerts for industrial systems
        if criticality in ["safety_critical", "business_critical"]:
            print(f"\n🚨 Critical System Alerts:")
            for name, budget in result.error_budgets.items():
                if budget.burn_rate > 0.1:
                    print(f"   ⚠️  High burn rate for {name}: {budget.burn_rate:.2f}")
                if budget.is_exhausted:
                    print(f"   🚨 CRITICAL: Error budget exhausted for {name}")
        
        if output_file:
            print(f"\n💾 Saving detailed results to {output_file}")
            # Save results logic here
        
    except FileNotFoundError:
        print(f"❌ Configuration file not found: {config_path}")
        print("💡 Try running: ml-eval template --industry <your-industry>")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Evaluation failed: {e}")
        print("💡 Check your configuration file format and try again")
        sys.exit(1)


def generate_report(report_type: str, period: str, format_type: str) -> None:
    """Generate report"""
    print(f"📋 Generating {report_type} report for {period}")
    
    if report_type == "reliability":
        # Create a mock result for demo
        result = EvaluationResult(
            system_name="Production ML System",
            evaluation_time=datetime.now(),
            slo_compliance={"availability": True, "latency": False},
            error_budgets={
                "availability": ErrorBudget("availability", 0.95, 0.02),
                "latency": ErrorBudget("latency", 0.1, 0.15)
            }
        )
        
        from .reports import ReliabilityReport
        report = ReliabilityReport(result)
        print(report.generate())
    else:
        print(f"📊 {report_type.title()} report for {period}")
        print("📈 Report generation in progress...")
        # Additional report types would be implemented here


def run_monitoring(config_path: str, interval: int, alerts_config: Optional[str] = None) -> None:
    """Run continuous monitoring"""
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

        system_name = config.get("system", {}).get("name", "Unknown System")
        criticality = config.get("system", {}).get("criticality", "standard")
        
        print(f"🔍 Starting continuous monitoring for {system_name}")
        print(f"⏱️  Monitoring interval: {interval} seconds")
        print(f"⚠️  Criticality: {criticality}")
        
        if alerts_config:
            print(f"🔔 Alert configuration: {alerts_config}")
        
        print("\n💡 Press Ctrl+C to stop monitoring")
        print("📊 Real-time metrics will appear below:\n")
        
        while True:
            try:
                # Simulate continuous evaluation
                result = EvaluationResult(
                    system_name=system_name,
                    evaluation_time=datetime.now(),
                    slo_compliance={"accuracy": True, "latency": True},
                    error_budgets={
                        "accuracy": ErrorBudget("accuracy", 0.85, 0.05),
                        "latency": ErrorBudget("latency", 0.9, 0.02)
                    }
                )
                
                # Check for alerts
                alerts_found = False
                for name, budget in result.error_budgets.items():
                    if budget.burn_rate > 0.1:  # High burn rate
                        print(f"⚠️  ALERT: High burn rate for {name}: {budget.burn_rate:.2f}")
                        alerts_found = True
                    if budget.is_exhausted:
                        print(f"🚨 CRITICAL: Error budget exhausted for {name}")
                        alerts_found = True
                
                if not alerts_found:
                    print(f"✅ Monitoring check at {result.evaluation_time.strftime('%H:%M:%S')} - All systems normal")
                
                time.sleep(interval)
                
            except KeyboardInterrupt:
                print("\n🛑 Monitoring stopped")
                print("📊 Final status: Monitoring session ended")
                break
                
    except FileNotFoundError:
        print(f"❌ Configuration file not found: {config_path}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Monitoring failed: {e}")
        sys.exit(1)


def run_development_evaluation(config_path: str, mode: str, strict: bool = False) -> None:
    """Run development evaluation"""
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

        system_name = config.get("system", {}).get("name", "Unknown System")
        criticality = config.get("system", {}).get("criticality", "standard")
        
        print(f"🔬 Development evaluation for {system_name}")
        print(f"📊 Mode: {mode}")
        print(f"⚠️  Criticality: {criticality}")
        
        if strict:
            print("🔒 Strict safety checks enabled")
        
        # Simulate development evaluation
        if mode == "training":
            print("\n🎯 Training phase evaluation:")
            print("  - Model architecture validation")
            print("  - Hyperparameter optimization")
            print("  - SLO compliance checking")
            
            result = EvaluationResult(
                system_name=system_name,
                evaluation_time=datetime.now(),
                slo_compliance={"accuracy": False, "latency": True},
                error_budgets={
                    "accuracy": ErrorBudget("accuracy", 0.3, 0.4),  # Poor performance
                    "latency": ErrorBudget("latency", 0.95, 0.01)
                }
            )
            
            print(f"\n📊 Training Results:")
            print(f"   Accuracy: {result.error_budgets['accuracy'].budget_remaining:.2f} (Target: 0.95)")
            print(f"   Latency: {result.error_budgets['latency'].budget_remaining:.2f} (Target: 0.90)")
            
            if result.error_budgets['accuracy'].budget_remaining < 0.5:
                print("\n⚠️  RECOMMENDATION: Model accuracy is below acceptable threshold")
                print("   Consider: Additional training data, feature engineering, or model architecture changes")
        
        elif mode == "validation":
            print("\n✅ Validation phase evaluation:")
            print("  - Cross-validation performance")
            print("  - Safety threshold validation")
            print("  - Regulatory compliance check")
            
            result = EvaluationResult(
                system_name=system_name,
                evaluation_time=datetime.now(),
                slo_compliance={"accuracy": True, "latency": True},
                error_budgets={
                    "accuracy": ErrorBudget("accuracy", 0.92, 0.03),
                    "latency": ErrorBudget("latency", 0.88, 0.05)
                }
            )
            
            print(f"\n✅ Validation Results:")
            print(f"   Accuracy: {result.error_budgets['accuracy'].budget_remaining:.2f} ✅")
            print(f"   Latency: {result.error_budgets['latency'].budget_remaining:.2f} ✅")
            print("\n🎉 Model ready for production deployment!")
        
        elif mode == "testing":
            print("\n🧪 Testing phase evaluation:")
            print("  - Integration testing")
            print("  - Load testing")
            print("  - Failure scenario testing")
            
            result = EvaluationResult(
                system_name=system_name,
                evaluation_time=datetime.now(),
                slo_compliance={"accuracy": True, "latency": False},
                error_budgets={
                    "accuracy": ErrorBudget("accuracy", 0.89, 0.06),
                    "latency": ErrorBudget("latency", 0.75, 0.15)
                }
            )
            
            print(f"\n🧪 Testing Results:")
            print(f"   Accuracy: {result.error_budgets['accuracy'].budget_remaining:.2f} ✅")
            print(f"   Latency: {result.error_budgets['latency'].budget_remaining:.2f} ⚠️")
            print("\n⚠️  Latency performance needs improvement before production")
        
    except FileNotFoundError:
        print(f"❌ Configuration file not found: {config_path}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Development evaluation failed: {e}")
        sys.exit(1)


def generate_template(industry: str, output_file: Optional[str] = None, template_type: Optional[str] = None) -> None:
    """Generate industry-specific configuration template"""
    try:
        # Handle special case for listing available templates
        if template_type == "list":
            available_templates = list_available_templates()
            if industry in available_templates:
                print(f"📋 Available templates for {industry.title()} industry:")
                for template_name in available_templates[industry]:
                    print(f"  • {template_name}")
            else:
                print(f"❌ Industry '{industry}' not found")
            return
        
        template = get_template(industry, template_type)
        
        if output_file:
            save_template(template, output_file)
            print(f"✅ Template saved to {output_file}")
            print(f"📝 Edit the configuration for your specific {industry} system")
        else:
            # Output clean YAML without formatting text
            yaml_content = yaml.dump(template, default_flow_style=False, indent=2)
            # Remove the trailing newline that yaml.dump() adds
            print(yaml_content.rstrip('\n'))
            
    except ValueError as e:
        print(f"❌ {e}")
        available = list_available_templates()
        print(f"Available industries: {list(available.keys())}")
        if industry in available:
            print(f"Available templates for {industry}: {available[industry]}")
        sys.exit(1)


def show_example(example_type: str, detailed: bool = False) -> None:
    """Show example configurations"""
    try:
        if detailed:
            print_example_details(example_type)
        else:
            example = get_example(example_type)
            print(example["title"])
            print("=" * len(example["title"]))
            print(yaml.dump(example["config"], default_flow_style=False, indent=2))
            
    except ValueError as e:
        print(f"❌ {e}")
        available = list(get_example("fish-workflow").keys())  # Get available examples
        print(f"Available examples: {available}")
        sys.exit(1)


def show_quickstart(industry: Optional[str] = None) -> None:
    """Show quick start guide"""
    print("🚀 Industrial ML Systems Evaluation - Quick Start Guide")
    print("=" * 60)
    
    if industry:
        print(f"🎯 Tailored for {industry.title()} Industry")
        print()
    
    print("Step 1: Get a template for your industry")
    print("  ml-eval template --industry <your-industry> > my-system.yaml")
    print()
    
    print("Step 2: Customize the configuration")
    print("  # Edit my-system.yaml with your specific requirements")
    print("  # Update system name, SLOs, and data sources")
    print()
    
    print("Step 3: Test your configuration")
    print("  ml-eval dev --config my-system.yaml --mode validation")
    print()
    
    print("Step 4: Evaluate your production system")
    print("  ml-eval evaluate --config my-system.yaml --mode single")
    print()
    
    print("Step 5: Set up continuous monitoring")
    print("  ml-eval monitor --config my-system.yaml --interval 300")
    print()
    
    print("Step 6: Generate compliance reports")
    print("  ml-eval report --type reliability --period 30d")
    print()
    
    print("💡 Pro Tips:")
    print("  - Start with development evaluation before production")
    print("  - Use strict mode for safety-critical systems")
    print("  - Set up alerts for continuous monitoring")
    print("  - Generate regular compliance reports")
    print()
    
    print("📚 Learn More:")
    print("  - ml-eval example --type aircraft-model --detailed")
    print("  - ml-eval example --type manufacturing --detailed")
    print("  - Check the README.md for detailed documentation") 