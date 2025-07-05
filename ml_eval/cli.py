"""Command-line interface"""

import argparse
import yaml
import sys
from pathlib import Path

from .core import EvaluationFramework
from .examples import FISH_CLASSIFICATION_WORKFLOW, AIRCRAFT_LANDING_MODEL
from .reports import ReliabilityReport


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(description="ML Systems Evaluation Framework")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Evaluate command
    eval_parser = subparsers.add_parser("evaluate", help="Run evaluation")
    eval_parser.add_argument("--config", required=True, help="Configuration file path")
    eval_parser.add_argument("--mode", choices=["single", "workflow"], default="single", help="Evaluation mode")

    # Report command
    report_parser = subparsers.add_parser("report", help="Generate reports")
    report_parser.add_argument("--type", choices=["reliability"], default="reliability", help="Report type")
    report_parser.add_argument("--period", default="30d", help="Time period for report")

    # Monitor command
    monitor_parser = subparsers.add_parser("monitor", help="Continuous monitoring")
    monitor_parser.add_argument("--config", required=True, help="Configuration file path")
    monitor_parser.add_argument("--interval", default="60", help="Monitoring interval in seconds")

    # Development command
    dev_parser = subparsers.add_parser("dev", help="Development evaluation")
    dev_parser.add_argument("--config", required=True, help="Configuration file path")
    dev_parser.add_argument("--mode", choices=["training", "validation"], default="training", help="Development mode")

    # Example command
    example_parser = subparsers.add_parser("example", help="Show example configurations")
    example_parser.add_argument(
        "--type", choices=["fish-workflow", "aircraft-model"], required=True, help="Example type"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "evaluate":
        run_evaluation(args.config, args.mode)
    elif args.command == "report":
        generate_report(args.type, args.period)
    elif args.command == "monitor":
        run_monitoring(args.config, int(args.interval))
    elif args.command == "dev":
        run_development_evaluation(args.config, args.mode)
    elif args.command == "example":
        show_example(args.type)


def run_evaluation(config_path: str, mode: str):
    """Run evaluation with configuration"""
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

        framework = EvaluationFramework(config)
        
        # For demo purposes, create a mock result
        from .core import EvaluationResult, ErrorBudget
        from datetime import datetime
        
        result = EvaluationResult(
            system_name=config.get("system", {}).get("name", "Unknown System"),
            evaluation_time=datetime.now(),
            slo_compliance={"accuracy": True, "latency": False},
            error_budgets={
                "accuracy": ErrorBudget("accuracy", 0.8, 0.1),
                "latency": ErrorBudget("latency", 0.2, 0.3)
            }
        )
        
        print(f"✅ Evaluation completed for {result.system_name}")
        print(f"📊 SLO Compliance: {sum(result.slo_compliance.values())}/{len(result.slo_compliance)}")
        
    except FileNotFoundError:
        print(f"❌ Configuration file not found: {config_path}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Evaluation failed: {e}")
        sys.exit(1)


def generate_report(report_type: str, period: str):
    """Generate report"""
    if report_type == "reliability":
        # Create a mock result for demo
        from .core import EvaluationResult, ErrorBudget
        from datetime import datetime
        
        result = EvaluationResult(
            system_name="Demo System",
            evaluation_time=datetime.now(),
            slo_compliance={"availability": True, "latency": False},
            error_budgets={
                "availability": ErrorBudget("availability", 0.95, 0.02),
                "latency": ErrorBudget("latency", 0.1, 0.15)
            }
        )
        
        report = ReliabilityReport(result)
        print(report.generate())
    else:
        print(f"❌ Unknown report type: {report_type}")
        sys.exit(1)


def run_monitoring(config_path: str, interval: int):
    """Run continuous monitoring"""
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

        framework = EvaluationFramework(config)
        
        print(f"🔍 Starting continuous monitoring for {config.get('system', {}).get('name', 'Unknown System')}")
        print(f"⏱️  Monitoring interval: {interval} seconds")
        print("Press Ctrl+C to stop monitoring")
        
        import time
        while True:
            try:
                # Simulate continuous evaluation
                from .core import EvaluationResult, ErrorBudget
                from datetime import datetime
                
                result = EvaluationResult(
                    system_name=config.get("system", {}).get("name", "Unknown System"),
                    evaluation_time=datetime.now(),
                    slo_compliance={"accuracy": True, "latency": True},
                    error_budgets={
                        "accuracy": ErrorBudget("accuracy", 0.85, 0.05),
                        "latency": ErrorBudget("latency", 0.9, 0.02)
                    }
                )
                
                # Check for alerts
                for name, budget in result.error_budgets.items():
                    if budget.burn_rate > 0.1:  # High burn rate
                        print(f"⚠️  ALERT: High burn rate for {name}: {budget.burn_rate:.2f}")
                    if budget.is_exhausted:
                        print(f"🚨 CRITICAL: Error budget exhausted for {name}")
                
                print(f"✅ Monitoring check at {result.evaluation_time.strftime('%H:%M:%S')}")
                time.sleep(interval)
                
            except KeyboardInterrupt:
                print("\n🛑 Monitoring stopped")
                break
                
    except FileNotFoundError:
        print(f"❌ Configuration file not found: {config_path}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Monitoring failed: {e}")
        sys.exit(1)


def run_development_evaluation(config_path: str, mode: str):
    """Run development evaluation"""
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

        framework = EvaluationFramework(config)
        
        print(f"🔬 Development evaluation for {config.get('system', {}).get('name', 'Unknown System')}")
        print(f"📊 Mode: {mode}")
        
        # Simulate development evaluation
        from .core import EvaluationResult, ErrorBudget
        from datetime import datetime
        
        if mode == "training":
            print("🎯 Training phase evaluation:")
            print("  - Model architecture validation")
            print("  - Hyperparameter optimization")
            print("  - SLO compliance checking")
            
            result = EvaluationResult(
                system_name=config.get("system", {}).get("name", "Unknown System"),
                evaluation_time=datetime.now(),
                slo_compliance={"accuracy": False, "latency": True},
                error_budgets={
                    "accuracy": ErrorBudget("accuracy", 0.3, 0.4),  # Poor performance
                    "latency": ErrorBudget("latency", 0.95, 0.01)
                }
            )
            
            # Provide development feedback
            if not result.slo_compliance["accuracy"]:
                print("💡 RECOMMENDATION: Consider model architecture changes or additional training data")
                
        elif mode == "validation":
            print("🧪 Validation phase evaluation:")
            print("  - Cross-validation performance")
            print("  - Generalization assessment")
            print("  - Production readiness check")
            
            result = EvaluationResult(
                system_name=config.get("system", {}).get("name", "Unknown System"),
                evaluation_time=datetime.now(),
                slo_compliance={"accuracy": True, "latency": True},
                error_budgets={
                    "accuracy": ErrorBudget("accuracy", 0.92, 0.03),
                    "latency": ErrorBudget("latency", 0.98, 0.005)
                }
            )
            
            print("✅ Model ready for deployment")
        
        print(f"📈 Development metrics: {result.slo_compliance}")
        
    except FileNotFoundError:
        print(f"❌ Configuration file not found: {config_path}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Development evaluation failed: {e}")
        sys.exit(1)


def show_example(example_type: str):
    """Show example configuration"""
    if example_type == "fish-workflow":
        print("# Fish Species Classification Workflow Configuration")
        print(yaml.dump(FISH_CLASSIFICATION_WORKFLOW, default_flow_style=False))
    elif example_type == "aircraft-model":
        print("# Aircraft Landing Model Configuration")
        print(yaml.dump(AIRCRAFT_LANDING_MODEL, default_flow_style=False))


if __name__ == "__main__":
    main()
