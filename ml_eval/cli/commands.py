"""CLI commands for ML Systems Evaluation Framework"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict

from ..config.factory import ConfigFactory
from ..core.framework import EvaluationFramework


def run_evaluation_command(args: argparse.Namespace) -> int:
    """Run evaluation with the specified configuration"""
    try:
        # Load configuration
        factory = ConfigFactory()
        config = factory.create_config(args.config)

        # Initialize framework
        framework = EvaluationFramework(config)

        # Run evaluation
        results = framework.evaluate()

        # Convert EvaluationResult to dictionary for JSON serialization
        def convert_to_dict(obj: Any) -> Any:
            """Recursively convert objects to dictionaries for JSON serialization"""
            if hasattr(obj, "__dict__"):
                # Convert object to dictionary
                result = {}
                for key, value in obj.__dict__.items():
                    if key.startswith("_"):  # Skip private attributes
                        continue
                    result[key] = convert_to_dict(value)
                return result
            elif isinstance(obj, (list, tuple)):
                return [convert_to_dict(item) for item in obj]
            elif isinstance(obj, dict):
                return {key: convert_to_dict(value) for key, value in obj.items()}
            elif hasattr(obj, "isoformat"):  # Handle datetime objects
                return obj.isoformat()
            else:
                return obj

        results_dict = convert_to_dict(results)

        # Output results
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, "w") as f:
                json.dump(results_dict, f, indent=2, default=str)

            print(f"Results saved to {output_path}")
        else:
            print(json.dumps(results_dict, indent=2, default=str))

        return 0

    except Exception as e:
        print(f"Error running evaluation: {e}", file=sys.stderr)
        return 1


def validate_config_command(args: argparse.Namespace) -> int:
    """Validate configuration file"""
    try:
        factory = ConfigFactory()
        config = factory.create_config(args.config)

        print("Configuration is valid!")
        print(f"System: {config.get('system', {}).get('name', 'Unknown')}")
        print(f"Collectors: {len(config.get('collectors', []))}")
        print(f"Evaluators: {len(config.get('evaluators', []))}")
        print(f"Reports: {len(config.get('reports', []))}")

        return 0

    except Exception as e:
        # Try to extract and print validator errors if available
        from ..config.validator import ConfigValidator
        import yaml

        try:
            with open(args.config, "r") as f:
                config_data = yaml.safe_load(f)
            validator = ConfigValidator()
            validator.validate_config(config_data)
            errors = validator.get_errors()
            warnings = validator.get_warnings()
            if errors:
                print("Validation errors:")
                for err in errors:
                    print(f"  - {err}")
            if warnings:
                print("Validation warnings:")
                for warn in warnings:
                    print(f"  - {warn}")
        except Exception as inner:
            print(f"(Additionally failed to extract validation errors: {inner})")
        print(f"Configuration validation failed: {e}", file=sys.stderr)
        return 1


def list_collectors_command(args: argparse.Namespace) -> int:
    """List available collectors"""
    try:
        factory = ConfigFactory()
        config = factory.create_config(args.config)

        collectors = config.get("collectors", [])

        if not collectors:
            print("No collectors configured")
            return 0

        print("Configured collectors:")
        for i, collector in enumerate(collectors, 1):
            collector_type = collector.get("type", "unknown")
            name = collector.get("name", f"collector_{i}")
            print(f"  {i}. {name} ({collector_type})")

        return 0

    except Exception as e:
        print(f"Error listing collectors: {e}", file=sys.stderr)
        return 1


def list_evaluators_command(args: argparse.Namespace) -> int:
    """List available evaluators"""
    try:
        factory = ConfigFactory()
        config = factory.create_config(args.config)

        evaluators = config.get("evaluators", [])

        if not evaluators:
            print("No evaluators configured")
            return 0

        print("Configured evaluators:")
        for i, evaluator in enumerate(evaluators, 1):
            evaluator_type = evaluator.get("type", "unknown")
            name = evaluator.get("name", f"evaluator_{i}")
            print(f"  {i}. {name} ({evaluator_type})")

        return 0

    except Exception as e:
        print(f"Error listing evaluators: {e}", file=sys.stderr)
        return 1


def list_reports_command(args: argparse.Namespace) -> int:
    """List available reports"""
    try:
        factory = ConfigFactory()
        config = factory.create_config(args.config)

        reports = config.get("reports", [])

        if not reports:
            print("No reports configured")
            return 0

        print("Configured reports:")
        for i, report in enumerate(reports, 1):
            report_type = report.get("type", "unknown")
            name = report.get("name", f"report_{i}")
            print(f"  {i}. {name} ({report_type})")

        return 0

    except Exception as e:
        print(f"Error listing reports: {e}", file=sys.stderr)
        return 1


def collect_data_command(args: argparse.Namespace) -> int:
    """Collect data using configured collectors"""
    try:
        factory = ConfigFactory()
        config = factory.create_config(args.config)

        # Initialize framework
        framework = EvaluationFramework(config)

        # Collect data using internal method
        data = framework._collect_all_metrics()

        # Output data
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, "w") as f:
                json.dump(data, f, indent=2, default=str)

            print(f"Data saved to {output_path}")
        else:
            print(json.dumps(data, indent=2, default=str))

        return 0

    except Exception as e:
        print(f"Error collecting data: {e}", file=sys.stderr)
        return 1


def evaluate_metrics_command(args: argparse.Namespace) -> int:
    """Evaluate metrics using configured evaluators"""
    try:
        factory = ConfigFactory()
        config = factory.create_config(args.config)

        # Initialize framework
        framework = EvaluationFramework(config)

        # Load data if provided
        data = {}
        if args.data:
            with open(args.data, "r") as f:
                data = json.load(f)

        # Evaluate metrics using internal method
        results = framework._run_all_evaluations(data)

        # Output results
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, "w") as f:
                json.dump(results, f, indent=2, default=str)

            print(f"Results saved to {output_path}")
        else:
            print(json.dumps(results, indent=2, default=str))

        return 0

    except Exception as e:
        print(f"Error evaluating metrics: {e}", file=sys.stderr)
        return 1


def generate_reports_command(args: argparse.Namespace) -> int:
    """Generate reports using configured report generators"""
    try:
        factory = ConfigFactory()
        config = factory.create_config(args.config)

        # Initialize framework
        framework = EvaluationFramework(config)

        # Load results if provided
        results = {}
        if args.results:
            with open(args.results, "r") as f:
                results = json.load(f)

        # Generate reports
        reports = framework.generate_reports(results)

        # Output reports
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, "w") as f:
                json.dump(reports, f, indent=2, default=str)

            print(f"Reports saved to {output_path}")
        else:
            print(json.dumps(reports, indent=2, default=str))

        return 0

    except Exception as e:
        print(f"Error generating reports: {e}", file=sys.stderr)
        return 1


def health_check_command(args: argparse.Namespace) -> int:
    """Perform health check on configured components"""
    try:
        factory = ConfigFactory()
        config = factory.create_config(args.config)

        # Initialize framework
        framework = EvaluationFramework(config)

        # Perform health check
        health_status = framework.health_check()

        # Output results
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, "w") as f:
                json.dump(health_status, f, indent=2, default=str)

            print(f"Health check results saved to {output_path}")
        else:
            print(json.dumps(health_status, indent=2, default=str))

        # Return appropriate exit code
        if health_status.get("overall_healthy", False):
            return 0
        else:
            return 1

    except Exception as e:
        print(f"Error performing health check: {e}", file=sys.stderr)
        return 1


def create_config_command(args: argparse.Namespace) -> int:
    """Create a new configuration file"""
    try:
        # Create basic configuration
        config: Dict[str, Any] = {
            "system": {
                "name": args.system_name,
                "type": args.system_type,
                "criticality": args.criticality,
            },
            "collectors": [],
            "evaluators": [],
            "reports": [],
        }

        # Add industry-specific defaults if specified
        if args.industry:
            system_config = config["system"]
            if isinstance(system_config, dict):
                system_config["industry"] = args.industry

        # Save configuration
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w") as f:
            json.dump(config, f, indent=2)

        print(f"Configuration created at {output_path}")
        return 0

    except Exception as e:
        print(f"Error creating configuration: {e}", file=sys.stderr)
        return 1
