#!/usr/bin/env python3
"""Test runner for ML Systems Evaluation Framework"""

import sys
import os
import argparse
import subprocess
from pathlib import Path


def run_tests(test_type=None, verbose=False, coverage=False):
    """Run tests with specified options"""

    # Get the project root directory
    project_root = Path(__file__).parent.parent
    tests_dir = project_root / "tests"

    # Build pytest command
    cmd = ["python", "-m", "pytest"]

    if verbose:
        cmd.append("-v")

    if coverage:
        cmd.extend(["--cov=ml_eval", "--cov-report=html", "--cov-report=term"])

    # Add test directory
    cmd.append(str(tests_dir))

    # Add specific test type if specified
    if test_type:
        if test_type == "unit":
            cmd.extend(["-k", "not integration"])
        elif test_type == "integration":
            cmd.extend(["-k", "integration"])
        elif test_type == "core":
            cmd.append(str(tests_dir / "test_core.py"))
        elif test_type == "collectors":
            cmd.append(str(tests_dir / "test_collectors.py"))
        elif test_type == "evaluators":
            cmd.append(str(tests_dir / "test_evaluators.py"))
        elif test_type == "cli":
            cmd.append(str(tests_dir / "test_cli.py"))
        elif test_type == "reports":
            cmd.append(str(tests_dir / "test_reports.py"))
        else:
            print(f"Unknown test type: {test_type}")
            return 1

    # Run tests
    print(f"Running tests: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=project_root)

    return result.returncode


def main():
    """Main test runner function"""
    parser = argparse.ArgumentParser(
        description="Test runner for ML Systems Evaluation Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_tests.py                    # Run all tests
  python run_tests.py --type unit       # Run unit tests only
  python run_tests.py --type integration # Run integration tests only
  python run_tests.py --type core       # Run core tests only
  python run_tests.py --verbose         # Run with verbose output
  python run_tests.py --coverage        # Run with coverage report
        """,
    )

    parser.add_argument(
        "--type",
        "-t",
        choices=[
            "unit",
            "integration",
            "core",
            "collectors",
            "evaluators",
            "cli",
            "reports",
        ],
        help="Type of tests to run",
    )

    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output"
    )

    parser.add_argument(
        "--coverage", "-c", action="store_true", help="Generate coverage report"
    )

    args = parser.parse_args()

    # Run tests
    exit_code = run_tests(
        test_type=args.type, verbose=args.verbose, coverage=args.coverage
    )

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
