"""Main CLI entry point for ML Systems Evaluation Framework"""

import sys
import logging
import click
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
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )

@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    invoke_without_command=True
)
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
@click.version_option("0.1.0", prog_name="ML Systems Evaluation Framework")
@click.pass_context
def cli(ctx, verbose):
    setup_logging(verbose)
    ctx.ensure_object(dict)
    ctx.obj['VERBOSE'] = verbose
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())
        ctx.exit(2)

@cli.command(help="Generate industry-specific configuration templates")
@click.option('--industry', '-i', required=True, type=click.Choice(["manufacturing", "aviation", "energy", "healthcare", "financial", "automotive"]), help="Target industry for template")
@click.option('--type', '-t', required=True, help="Template type (use 'list' to see available types)")
@click.option('--output', '-o', help="Output file path (default: stdout)")
@click.pass_context
def template(ctx, industry, type, output):
    class Args: pass
    args = Args()
    args.industry = industry
    args.type = type
    args.output = output
    sys.exit(template_command(args))

@cli.command(help="Get started with industry-specific examples")
@click.option('--industry', '-i', required=True, type=click.Choice(["manufacturing", "aviation", "energy", "healthcare", "financial", "automotive"]), help="Target industry for quickstart")
@click.pass_context
def quickstart(ctx, industry):
    class Args: pass
    args = Args()
    args.industry = industry
    sys.exit(quickstart_command(args))

@cli.command(help="Show detailed examples and use cases")
@click.option('--type', '-t', required=True, help="Example type to show")
@click.option('--detailed', '-d', is_flag=True, help="Show detailed example with configuration")
@click.pass_context
def example(ctx, type, detailed):
    class Args: pass
    args = Args()
    args.type = type
    args.detailed = detailed
    sys.exit(example_command(args))

@cli.command(help="Development and validation tools")
@click.option('--config', '-c', required=True, help="Configuration file path")
@click.option('--mode', '-m', type=click.Choice(["validation", "test", "simulation"]), default="validation", show_default=True, help="Development mode")
@click.option('--strict', '-s', is_flag=True, help="Enable strict validation")
@click.pass_context
def dev(ctx, config, mode, strict):
    class Args: pass
    args = Args()
    args.config = config
    args.mode = mode
    args.strict = strict
    sys.exit(dev_command(args))

@cli.command(help="Run evaluation on ML system")
@click.option('--config', '-c', required=True, help="Configuration file path")
@click.option('--mode', '-m', type=click.Choice(["single", "continuous", "workflow"]), default="single", show_default=True, help="Evaluation mode")
@click.option('--output', '-o', help="Output file path for results")
@click.pass_context
def evaluate(ctx, config, mode, output):
    class Args: pass
    args = Args()
    args.config = config
    args.mode = mode
    args.output = output
    sys.exit(evaluate_command(args))

@cli.command(help="Continuous monitoring of ML system")
@click.option('--config', '-c', required=True, help="Configuration file path")
@click.option('--interval', '-i', type=int, default=300, show_default=True, help="Monitoring interval in seconds")
@click.option('--duration', '-d', type=int, help="Monitoring duration in seconds (default: run indefinitely)")
@click.pass_context
def monitor(ctx, config, interval, duration):
    class Args: pass
    args = Args()
    args.config = config
    args.interval = interval
    args.duration = duration
    sys.exit(monitor_command(args))

@cli.command(help="Generate evaluation reports")
@click.option('--type', '-t', required=True, type=click.Choice(["reliability", "safety", "compliance", "business_impact", "trend", "incident"]), help="Report type")
@click.option('--period', '-p', default="30d", show_default=True, help="Report period (e.g., 7d, 30d, 90d)")
@click.option('--output', '-o', help="Output file path for report")
@click.pass_context
def report(ctx, type, period, output):
    class Args: pass
    args = Args()
    args.type = type
    args.period = period
    args.output = output
    sys.exit(report_command(args))

if __name__ == "__main__":
    cli() 