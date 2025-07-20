#!/usr/bin/env python3
"""
Build and serve Sphinx documentation for ML Systems Evaluation Framework.

This script provides convenient commands for building, serving, and managing
the Sphinx documentation.
"""

import argparse
import os
import subprocess
import sys
import webbrowser
from pathlib import Path


def run_command(cmd, cwd=None, check=True):
    """Run a command and return the result."""
    try:
        result = subprocess.run(
            cmd, 
            cwd=cwd, 
            check=check, 
            capture_output=True, 
            text=True
        )
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {' '.join(cmd)}")
        print(f"Error: {e}")
        return e


def build_docs(clean=False, fast=False, full=False):
    """Build the Sphinx documentation."""
    docs_dir = Path(__file__).parent
    
    if clean:
        print("Cleaning build artifacts...")
        run_command(["make", "clean-all"], cwd=docs_dir)
    
    if fast:
        print("Building documentation (fast mode)...")
        result = run_command(["uv", "run", "make", "html-fast"], cwd=docs_dir)
    elif full:
        print("Building documentation (full mode with warnings)...")
        result = run_command(["uv", "run", "make", "html-full"], cwd=docs_dir)
    else:
        print("Building documentation...")
        result = run_command(["uv", "run", "make", "html"], cwd=docs_dir)
    
    if result.returncode == 0:
        print("✅ Documentation built successfully!")
        print(f"📁 HTML files are in: {docs_dir}/build/html/")
        return True
    else:
        print("❌ Documentation build failed!")
        return False


def serve_docs(port=8000, open_browser=True):
    """Serve the documentation locally."""
    docs_dir = Path(__file__).parent
    html_dir = docs_dir / "build" / "html"
    
    if not html_dir.exists():
        print("❌ Documentation not built. Building first...")
        if not build_docs():
            return False
    
    print(f"🌐 Serving documentation at http://localhost:{port}")
    print("Press Ctrl+C to stop the server")
    
    if open_browser:
        webbrowser.open(f"http://localhost:{port}")
    
    try:
        run_command(
            ["python", "-m", "http.server", str(port)], 
            cwd=html_dir, 
            check=False
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped.")


def check_links():
    """Check for broken links in the documentation."""
    docs_dir = Path(__file__).parent
    print("🔍 Checking links...")
    result = run_command(["uv", "run", "make", "check"], cwd=docs_dir)
    
    if result.returncode == 0:
        print("✅ Link check completed successfully!")
    else:
        print("❌ Link check found issues!")
        print(result.stdout)
        print(result.stderr)


def spell_check():
    """Run spell checking on the documentation."""
    docs_dir = Path(__file__).parent
    print("📝 Running spell check...")
    result = run_command(["uv", "run", "make", "spelling"], cwd=docs_dir)
    
    if result.returncode == 0:
        print("✅ Spell check completed successfully!")
    else:
        print("❌ Spell check found issues!")
        print(result.stdout)
        print(result.stderr)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Build and serve Sphinx documentation"
    )
    parser.add_argument(
        "command",
        choices=["build", "serve", "check", "spell", "clean"],
        help="Command to run"
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Clean build artifacts before building"
    )
    parser.add_argument(
        "--fast",
        action="store_true",
        help="Build with parallel processing"
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Build with full error checking"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for serving documentation (default: 8000)"
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Don't open browser when serving"
    )
    
    args = parser.parse_args()
    
    if args.command == "build":
        build_docs(clean=args.clean, fast=args.fast, full=args.full)
    elif args.command == "serve":
        serve_docs(port=args.port, open_browser=not args.no_browser)
    elif args.command == "check":
        check_links()
    elif args.command == "spell":
        spell_check()
    elif args.command == "clean":
        docs_dir = Path(__file__).parent
        run_command(["uv", "run", "make", "clean-all"], cwd=docs_dir)
        print("🧹 Build artifacts cleaned!")


if __name__ == "__main__":
    main() 