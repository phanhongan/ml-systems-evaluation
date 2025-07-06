"""Main CLI entry point for ML Systems Evaluation Framework"""

import sys
import argparse
import logging
from typing import Optional

from .commands import (
    template_command,
    quickstart_command,
    example_command,
    dev_command,
    evaluate_command,
    monitor_command,
    report_command
)


def setup_logging(verbose: bool = False):
    """Setup logging configuration"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )


def create_parser() -> argparse.ArgumentParser:
    """Create the main argument parser"""
    parser = argparse.ArgumentParser(
        prog="ml-eval",
        description="ML Systems Evaluation Framework - Industrial AI Reliability Assessment",
        epilog="""
Examples:
  ml-eval template --industry manufacturing --type quality_control
  ml-eval quickstart --industry aviation
  ml-eval evaluate --config system.yaml --mode single
  ml-eval monitor --config system.yaml --interval 300
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="ML Systems Evaluation Framework v0.1.0"
    )
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(
        dest="command",
        help="Available commands",
        metavar="COMMAND"
    )
    
    # Template command
    template_parser = subparsers.add_parser(
        "template",
        help="Generate industry-specific configuration templates"
    )
    template_parser.add_argument(
        "--industry", "-i",
        required=True,
        choices=["manufacturing", "aviation", "energy", "healthcare", "financial", "automotive"],
        help="Target industry for template"
    )
    template_parser.add_argument(
        "--type", "-t",
        required=True,
        help="Template type (use 'list' to see available types)"
    )
    template_parser.add_argument(
        "--output", "-o",
        help="Output file path (default: stdout)"
    )
    
    # Quickstart command
    quickstart_parser = subparsers.add_parser(
        "quickstart",
        help="Get started with industry-specific examples"
    )
    quickstart_parser.add_argument(
        "--industry", "-i",
        required=True,
        choices=["manufacturing", "aviation", "energy", "healthcare", "financial", "automotive"],
        help="Target industry for quickstart"
    )
    
    # Example command
    example_parser = subparsers.add_parser(
        "example",
        help="Show detailed examples and use cases"
    )
    example_parser.add_argument(
        "--type", "-t",
        required=True,
        help="Example type to show"
    )
    example_parser.add_argument(
        "--detailed", "-d",
        action="store_true",
        help="Show detailed example with configuration"
    )
    
    # Development command
    dev_parser = subparsers.add_parser(
        "dev",
        help="Development and validation tools"
    )
    dev_parser.add_argument(
        "--config", "-c",
        required=True,
        help="Configuration file path"
    )
    dev_parser.add_argument(
        "--mode", "-m",
        choices=["validation", "test", "simulation"],
        default="validation",
        help="Development mode"
    )
    dev_parser.add_argument(
        "--strict", "-s",
        action="store_true",
        help="Enable strict validation"
    )
    
    # Evaluate command
    evaluate_parser = subparsers.add_parser(
        "evaluate",
        help="Run evaluation on ML system"
    )
    evaluate_parser.add_argument(
        "--config", "-c",
        required=True,
        help="Configuration file path"
    )
    evaluate_parser.add_argument(
        "--mode", "-m",
        choices=["single", "continuous", "workflow"],
        default="single",
        help="Evaluation mode"
    )
    evaluate_parser.add_argument(
        "--output", "-o",
        help="Output file path for results"
    )
    
    # Monitor command
    monitor_parser = subparsers.add_parser(
        "monitor",
        help="Continuous monitoring of ML system"
    )
    monitor_parser.add_argument(
        "--config", "-c",
        required=True,
        help="Configuration file path"
    )
    monitor_parser.add_argument(
        "--interval", "-i",
        type=int,
        default=300,
        help="Monitoring interval in seconds"
    )
    monitor_parser.add_argument(
        "--duration", "-d",
        type=int,
        help="Monitoring duration in seconds (default: run indefinitely)"
    )
    
    # Report command
    report_parser = subparsers.add_parser(
        "report",
        help="Generate evaluation reports"
    )
    report_parser.add_argument(
        "--type", "-t",
        choices=["reliability", "safety", "compliance", "business_impact", "trend", "incident"],
        required=True,
        help="Report type"
    )
    report_parser.add_argument(
        "--period", "-p",
        default="30d",
        help="Report period (e.g., 7d, 30d, 90d)"
    )
    report_parser.add_argument(
        "--output", "-o",
        help="Output file path for report"
    )
    
    return parser


def main(args: Optional[list] = None) -> int:
    """Main CLI entry point"""
    parser = create_parser()
    parsed_args = parser.parse_args(args)
    
    # Setup logging
    setup_logging(parsed_args.verbose)
    logger = logging.getLogger(__name__)
    
    try:
        if not parsed_args.command:
            parser.print_help()
            return 0
            
        # Route to appropriate command handler
        if parsed_args.command == "template":
            return template_command(parsed_args)
        elif parsed_args.command == "quickstart":
            return quickstart_command(parsed_args)
        elif parsed_args.command == "example":
            return example_command(parsed_args)
        elif parsed_args.command == "dev":
            return dev_command(parsed_args)
        elif parsed_args.command == "evaluate":
            return evaluate_command(parsed_args)
        elif parsed_args.command == "monitor":
            return monitor_command(parsed_args)
        elif parsed_args.command == "report":
            return report_command(parsed_args)
        else:
            logger.error(f"Unknown command: {parsed_args.command}")
            return 1
            
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        return 130
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        if parsed_args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main()) 