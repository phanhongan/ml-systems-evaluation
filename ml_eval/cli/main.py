"""Main CLI entry point for ML Systems Evaluation Framework"""

import argparse
import sys


def create_parser() -> argparse.ArgumentParser:
    """Create the main argument parser"""
    parser = argparse.ArgumentParser(
        description="ML Systems Evaluation Framework CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ml-eval run config.yaml
  ml-eval validate config.yaml
  ml-eval collect config.yaml --output data.json
  ml-eval evaluate config.yaml --data data.json --output results.json
  ml-eval report config.yaml --results results.json --output reports.json
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Run evaluation command
    run_parser = subparsers.add_parser("run", help="Run complete evaluation pipeline")
    run_parser.add_argument("config", help="Configuration file path")
    run_parser.add_argument(
        "--output", help="Output file for results (default: stdout)"
    )

    # Validate configuration command
    validate_parser = subparsers.add_parser(
        "validate", help="Validate configuration file"
    )
    validate_parser.add_argument("config", help="Configuration file path")

    # List components commands
    list_collectors_parser = subparsers.add_parser(
        "list-collectors", help="List configured collectors"
    )
    list_collectors_parser.add_argument("config", help="Configuration file path")

    list_evaluators_parser = subparsers.add_parser(
        "list-evaluators", help="List configured evaluators"
    )
    list_evaluators_parser.add_argument("config", help="Configuration file path")

    list_reports_parser = subparsers.add_parser(
        "list-reports", help="List configured reports"
    )
    list_reports_parser.add_argument("config", help="Configuration file path")

    # Collect data command
    collect_parser = subparsers.add_parser(
        "collect", help="Collect data using configured collectors"
    )
    collect_parser.add_argument("config", help="Configuration file path")
    collect_parser.add_argument(
        "--output", help="Output file for collected data (default: stdout)"
    )

    # Evaluate metrics command
    evaluate_parser = subparsers.add_parser(
        "evaluate", help="Evaluate metrics using configured evaluators"
    )
    evaluate_parser.add_argument("config", help="Configuration file path")
    evaluate_parser.add_argument("--data", help="Input data file (optional)")
    evaluate_parser.add_argument(
        "--output", help="Output file for results (default: stdout)"
    )

    # Generate reports command
    report_parser = subparsers.add_parser(
        "report", help="Generate reports using configured report generators"
    )
    report_parser.add_argument("config", help="Configuration file path")
    report_parser.add_argument("--results", help="Input results file (optional)")
    report_parser.add_argument(
        "--output", help="Output file for reports (default: stdout)"
    )

    # Health check command
    health_parser = subparsers.add_parser(
        "health", help="Perform health check on configured components"
    )
    health_parser.add_argument("config", help="Configuration file path")
    health_parser.add_argument(
        "--output", help="Output file for health check results (default: stdout)"
    )

    # Create configuration command
    create_parser = subparsers.add_parser(
        "create-config", help="Create a new configuration file"
    )
    create_parser.add_argument("--output", required=True, help="Output file path")
    create_parser.add_argument("--system-name", required=True, help="System name")
    create_parser.add_argument(
        "--system-type",
        default="single_model",
        choices=["single_model", "workflow", "ensemble"],
        help="System type (default: single_model)",
    )
    create_parser.add_argument(
        "--criticality",
        default="operational",
        choices=["operational", "business_critical", "safety_critical"],
        help="System criticality level (default: operational)",
    )
    create_parser.add_argument("--industry", help="Industry type (optional)")

    return parser


def main(args: list[str] | None = None) -> int:
    """Main CLI entry point"""
    parser = create_parser()
    parsed_args = parser.parse_args(args)

    if not parsed_args.command:
        parser.print_help()
        return 1

    # Import commands here to avoid circular imports
    from .commands import (
        collect_data_command,
        create_config_command,
        evaluate_metrics_command,
        generate_reports_command,
        health_check_command,
        list_collectors_command,
        list_evaluators_command,
        list_reports_command,
        run_evaluation_command,
        validate_config_command,
    )

    # Route to appropriate command handler
    command_handlers = {
        "run": run_evaluation_command,
        "validate": validate_config_command,
        "list-collectors": list_collectors_command,
        "list-evaluators": list_evaluators_command,
        "list-reports": list_reports_command,
        "collect": collect_data_command,
        "evaluate": evaluate_metrics_command,
        "report": generate_reports_command,
        "health": health_check_command,
        "create-config": create_config_command,
    }

    handler = command_handlers.get(parsed_args.command)
    if handler:
        return handler(parsed_args)
    else:
        print(f"Unknown command: {parsed_args.command}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())


cli = main
