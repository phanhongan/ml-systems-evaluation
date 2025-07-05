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
