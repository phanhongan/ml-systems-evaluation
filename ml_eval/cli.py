"""Command-line interface for Industrial ML Systems Evaluation"""

import argparse
import sys

from .cli_commands import (
    run_evaluation,
    generate_report,
    run_monitoring,
    run_development_evaluation,
    generate_template,
    show_example,
    show_quickstart
)


def create_parser() -> argparse.ArgumentParser:
    """Create the main CLI parser"""
    parser = argparse.ArgumentParser(
        description="Industrial ML Systems Evaluation Framework - Built for ML Engineers in Manufacturing, Aviation, Energy, and other Industrial Sectors",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples for Industrial ML Engineers:

  # Quick start - evaluate your production ML system
  ml-eval evaluate --config production-system.yaml --mode single

  # Monitor your manufacturing quality control system
  ml-eval monitor --config quality-control.yaml --interval 300

  # Generate compliance report for aviation safety system
  ml-eval report --type reliability --period 7d

  # Development testing for new model
  ml-eval dev --config new-model.yaml --mode validation

  # List available templates
  ml-eval template --industry manufacturing --type list
  
  # Get specific template
  ml-eval template --industry manufacturing --type quality_control
  ml-eval template --industry aviation --type safety_decision
  ml-eval template --industry energy --type grid_optimization
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command parsers
    _add_evaluate_parser(subparsers)
    _add_report_parser(subparsers)
    _add_monitor_parser(subparsers)
    _add_dev_parser(subparsers)
    _add_template_parser(subparsers)
    _add_example_parser(subparsers)
    _add_quickstart_parser(subparsers)
    
    return parser


def _add_evaluate_parser(subparsers):
    """Add evaluate command parser"""
    eval_parser = subparsers.add_parser(
        "evaluate", 
        help="Evaluate production ML system performance and compliance"
    )
    eval_parser.add_argument(
        "--config", 
        required=True, 
        help="Configuration file path (YAML format)"
    )
    eval_parser.add_argument(
        "--mode", 
        choices=["single", "workflow"], 
        default="single", 
        help="Evaluation mode: single (one model) or workflow (pipeline)"
    )
    eval_parser.add_argument(
        "--output", 
        help="Output file for detailed results (JSON format)"
    )


def _add_report_parser(subparsers):
    """Add report command parser"""
    report_parser = subparsers.add_parser(
        "report", 
        help="Generate compliance and reliability reports"
    )
    report_parser.add_argument(
        "--type", 
        choices=["reliability", "compliance", "safety", "business"], 
        default="reliability", 
        help="Report type for different stakeholders"
    )
    report_parser.add_argument(
        "--period", 
        default="30d", 
        help="Time period for report (e.g., 7d, 30d, 90d)"
    )
    report_parser.add_argument(
        "--format", 
        choices=["text", "json", "html"], 
        default="text", 
        help="Output format for reports"
    )


def _add_monitor_parser(subparsers):
    """Add monitor command parser"""
    monitor_parser = subparsers.add_parser(
        "monitor", 
        help="Continuous monitoring for production systems"
    )
    monitor_parser.add_argument(
        "--config", 
        required=True, 
        help="Configuration file path"
    )
    monitor_parser.add_argument(
        "--interval", 
        default="60", 
        help="Monitoring interval in seconds (default: 60)"
    )
    monitor_parser.add_argument(
        "--alerts", 
        help="Alert configuration file for notifications"
    )


def _add_dev_parser(subparsers):
    """Add development command parser"""
    dev_parser = subparsers.add_parser(
        "dev", 
        help="Development and testing evaluation"
    )
    dev_parser.add_argument(
        "--config", 
        required=True, 
        help="Configuration file path"
    )
    dev_parser.add_argument(
        "--mode", 
        choices=["training", "validation", "testing"], 
        default="training", 
        help="Development phase"
    )
    dev_parser.add_argument(
        "--strict", 
        action="store_true", 
        help="Enable strict safety checks for critical systems"
    )


def _add_template_parser(subparsers):
    """Add template command parser"""
    template_parser = subparsers.add_parser(
        "template", 
        help="Get industry-specific configuration templates"
    )
    template_parser.add_argument(
        "--industry", 
        choices=["manufacturing", "aviation", "energy"], 
        required=True, 
        help="Your industry sector"
    )
    template_parser.add_argument(
        "--type", 
        help="Specific template type (use 'list' to see available types, omit for default)"
    )
    template_parser.add_argument(
        "--output", 
        help="Output file for template (default: prints to console)"
    )


def _add_example_parser(subparsers):
    """Add example command parser"""
    example_parser = subparsers.add_parser(
        "example", 
        help="Show example configurations for learning"
    )
    example_parser.add_argument(
        "--type", 
        choices=["fish-workflow", "aircraft-model", "manufacturing"], 
        required=True, 
        help="Example type"
    )
    example_parser.add_argument(
        "--detailed", 
        action="store_true", 
        help="Show detailed explanation with each section"
    )


def _add_quickstart_parser(subparsers):
    """Add quickstart command parser"""
    quick_parser = subparsers.add_parser(
        "quickstart", 
        help="Quick start guide for your first evaluation"
    )
    quick_parser.add_argument(
        "--industry", 
        choices=["manufacturing", "aviation", "energy"], 
        help="Your industry for tailored guidance"
    )


def main():
    """CLI entry point for Industrial ML Systems Evaluation"""
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        print("\n💡 Need help getting started? Try: ml-eval quickstart")
        sys.exit(1)

    # Route commands to their implementations
    if args.command == "evaluate":
        run_evaluation(args.config, args.mode, args.output)
    elif args.command == "report":
        generate_report(args.type, args.period, args.format)
    elif args.command == "monitor":
        run_monitoring(args.config, int(args.interval), args.alerts)
    elif args.command == "dev":
        run_development_evaluation(args.config, args.mode, args.strict)
    elif args.command == "template":
        generate_template(args.industry, args.output, args.type)
    elif args.command == "example":
        show_example(args.type, args.detailed)
    elif args.command == "quickstart":
        show_quickstart(args.industry)


if __name__ == "__main__":
    main()
