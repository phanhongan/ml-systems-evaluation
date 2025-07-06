"""Unit tests for CLI module"""

import pytest
from unittest.mock import Mock, patch, call
import sys
import argparse
from io import StringIO

from ml_eval.cli.main import create_parser, main
from ml_eval.cli.commands import (
    template_command,
    quickstart_command,
    example_command,
    dev_command,
    evaluate_command,
    monitor_command,
    report_command
)


class TestCLIParser:
    """Test CLI argument parsing"""
    
    def test_template_command_parser(self):
        """Test template command argument parsing"""
        parser = create_parser()
        args = parser.parse_args([
            "template",
            "--industry", "manufacturing",
            "--type", "quality_control",
            "--output", "config.yaml"
        ])
        
        assert args.command == "template"
        assert args.industry == "manufacturing"
        assert args.type == "quality_control"
        assert args.output == "config.yaml"
        
    def test_quickstart_command_parser(self):
        """Test quickstart command argument parsing"""
        parser = create_parser()
        args = parser.parse_args([
            "quickstart",
            "--industry", "aviation"
        ])
        
        assert args.command == "quickstart"
        assert args.industry == "aviation"
        
    def test_evaluate_command_parser(self):
        """Test evaluate command argument parsing"""
        parser = create_parser()
        args = parser.parse_args([
            "evaluate",
            "--config", "system.yaml",
            "--mode", "single",
            "--output", "results.json"
        ])
        
        assert args.command == "evaluate"
        assert args.config == "system.yaml"
        assert args.mode == "single"
        assert args.output == "results.json"
        
    def test_monitor_command_parser(self):
        """Test monitor command argument parsing"""
        parser = create_parser()
        args = parser.parse_args([
            "monitor",
            "--config", "system.yaml",
            "--interval", "300",
            "--duration", "3600"
        ])
        
        assert args.command == "monitor"
        assert args.config == "system.yaml"
        assert args.interval == 300
        assert args.duration == 3600
        
    def test_report_command_parser(self):
        """Test report command argument parsing"""
        parser = create_parser()
        args = parser.parse_args([
            "report",
            "--type", "reliability",
            "--period", "30d",
            "--output", "report.json"
        ])
        
        assert args.command == "report"
        assert args.type == "reliability"
        assert args.period == "30d"
        assert args.output == "report.json"


class TestCLICommands:
    """Test CLI command execution"""
    
    @patch('ml_eval.cli.commands._generate_template')
    def test_template_command(self, mock_generate):
        """Test template command execution"""
        parser = create_parser()
        args = parser.parse_args([
            "template",
            "--industry", "manufacturing",
            "--type", "quality_control"
        ])
    
        # Mock the internal function
        mock_generate.return_value = 0
    
        # Execute command
        result = template_command(args)
    
        # Verify internal function was called
        mock_generate.assert_called_once_with("manufacturing", "quality_control", None)
        assert result == 0
        
    @patch('ml_eval.cli.commands._show_quickstart')
    def test_quickstart_command(self, mock_show):
        """Test quickstart command execution"""
        parser = create_parser()
        args = parser.parse_args([
            "quickstart",
            "--industry", "aviation"
        ])
    
        # Mock the internal function
        mock_show.return_value = 0
    
        # Execute command
        result = quickstart_command(args)
    
        # Verify internal function was called
        mock_show.assert_called_once_with("aviation")
        assert result == 0
        
    @patch('ml_eval.cli.commands._show_example')
    def test_example_command(self, mock_show):
        """Test example command execution"""
        parser = create_parser()
        args = parser.parse_args([
            "example",
            "--type", "aviation_safety"
        ])
    
        # Mock the internal function
        mock_show.return_value = 0
    
        # Execute command
        result = example_command(args)
    
        # Verify internal function was called
        mock_show.assert_called_once_with("aviation_safety", False)
        assert result == 0
        
    @patch('ml_eval.cli.commands._run_development')
    def test_dev_command(self, mock_run):
        """Test dev command execution"""
        parser = create_parser()
        args = parser.parse_args([
            "dev",
            "--config", "system.yaml",
            "--mode", "validation"
        ])
    
        # Mock the internal function
        mock_run.return_value = 0
    
        # Execute command
        result = dev_command(args)
    
        # Verify internal function was called
        mock_run.assert_called_once_with("system.yaml", "validation", False)
        assert result == 0
        
    @patch('ml_eval.cli.commands._run_evaluation')
    def test_evaluate_command(self, mock_run):
        """Test evaluate command execution"""
        parser = create_parser()
        args = parser.parse_args([
            "evaluate",
            "--config", "system.yaml",
            "--mode", "single"
        ])
    
        # Mock the internal function
        mock_run.return_value = 0
    
        # Execute command
        result = evaluate_command(args)
    
        # Verify internal function was called
        mock_run.assert_called_once_with("system.yaml", "single", None)
        assert result == 0
        
    @patch('ml_eval.cli.commands._run_monitoring')
    def test_monitor_command(self, mock_run):
        """Test monitor command execution"""
        parser = create_parser()
        args = parser.parse_args([
            "monitor",
            "--config", "system.yaml",
            "--interval", "300"
        ])
    
        # Mock the internal function
        mock_run.return_value = 0
    
        # Execute command
        result = monitor_command(args)
    
        # Verify internal function was called
        mock_run.assert_called_once_with("system.yaml", 300, None)
        assert result == 0
        
    @patch('ml_eval.cli.commands._generate_report')
    def test_report_command(self, mock_generate):
        """Test report command execution"""
        parser = create_parser()
        args = parser.parse_args([
            "report",
            "--type", "reliability",
            "--period", "30d"
        ])
    
        # Mock the internal function
        mock_generate.return_value = 0
    
        # Execute command
        result = report_command(args)
    
        # Verify internal function was called
        mock_generate.assert_called_once_with("reliability", "30d", None)
        assert result == 0


class TestCLIIntegration:
    """Test CLI integration and error handling"""
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_cli_main_help(self, mock_stdout):
        """Test CLI main help output"""
        with pytest.raises(SystemExit) as exc_info:
            main(["--help"])
        
        # Help should exit with code 0
        assert exc_info.value.code == 0
        
        # Should contain help text
        output = mock_stdout.getvalue()
        assert "ML Systems Evaluation Framework" in output
        assert "template" in output
        assert "evaluate" in output
        
    @patch('sys.stdout', new_callable=StringIO)
    def test_cli_main_version(self, mock_stdout):
        """Test CLI main version output"""
        with pytest.raises(SystemExit) as exc_info:
            main(["--version"])
        
        # Version should exit with code 0
        assert exc_info.value.code == 0
        
        # Should contain version text
        output = mock_stdout.getvalue()
        assert "ML Systems Evaluation Framework v0.1.0" in output
        
    def test_cli_main_no_command(self):
        """Test CLI main with no command"""
        # Should exit with error when no command provided
        with pytest.raises(SystemExit) as exc_info:
            main([])
        
        # Should exit with error code
        assert exc_info.value.code == 2
        
    @patch('ml_eval.cli.commands._generate_template')
    def test_cli_main_template_command(self, mock_generate):
        """Test CLI main template command"""
        mock_generate.return_value = 0
    
        result = main(["template", "--industry", "manufacturing", "--type", "quality_control"])
    
        # Should call internal function
        mock_generate.assert_called_once_with("manufacturing", "quality_control", None)
        assert result == 0
        
    @patch('ml_eval.cli.commands._run_evaluation')
    def test_cli_main_evaluate_command(self, mock_run):
        """Test CLI main evaluate command"""
        mock_run.return_value = 0
    
        result = main(["evaluate", "--config", "system.yaml", "--mode", "single"])
    
        # Should call internal function
        mock_run.assert_called_once_with("system.yaml", "single", None)
        assert result == 0
        
    def test_cli_argument_validation(self):
        """Test CLI argument validation"""
        parser = create_parser()
        
        # Test invalid industry
        with pytest.raises(SystemExit):
            parser.parse_args(["template", "--industry", "invalid", "--type", "test"])
            
        # Test invalid mode
        with pytest.raises(SystemExit):
            parser.parse_args(["evaluate", "--config", "test.yaml", "--mode", "invalid"])
            
        # Test missing required arguments
        with pytest.raises(SystemExit):
            parser.parse_args(["template", "--industry", "manufacturing"])
            
    def test_cli_verbose_logging(self):
        """Test CLI verbose logging setup"""
        parser = create_parser()
        args = parser.parse_args(["--verbose", "template", "--industry", "manufacturing", "--type", "test"])
        
        assert args.verbose is True
        
    def test_cli_command_help(self):
        """Test CLI command help"""
        parser = create_parser()
        
        # Test template command help
        with pytest.raises(SystemExit):
            parser.parse_args(["template", "--help"])
            
        # Test evaluate command help
        with pytest.raises(SystemExit):
            parser.parse_args(["evaluate", "--help"])
            
    def test_cli_invalid_arguments(self):
        """Test CLI invalid argument handling"""
        parser = create_parser()
        
        # Test invalid command
        with pytest.raises(SystemExit):
            parser.parse_args(["invalid_command"])
            
        # Test invalid subcommand arguments
        with pytest.raises(SystemExit):
            parser.parse_args(["template", "--invalid_arg", "value"])
            
    def test_cli_default_values(self):
        """Test CLI default argument values"""
        parser = create_parser()
        
        # Test evaluate command defaults
        args = parser.parse_args(["evaluate", "--config", "system.yaml"])
        assert args.mode == "single"
        
        # Test monitor command defaults
        args = parser.parse_args(["monitor", "--config", "system.yaml"])
        assert args.interval == 300
        assert args.duration is None
        
        # Test report command defaults
        args = parser.parse_args(["report", "--type", "reliability"])
        assert args.period == "30d"
        
    def test_cli_command_coverage(self):
        """Test that all commands are covered by parser"""
        parser = create_parser()
        
        # Test all available commands
        commands = ["template", "quickstart", "example", "dev", "evaluate", "monitor", "report"]
        
        for command in commands:
            # Should not raise SystemExit for valid commands
            try:
                args = parser.parse_args([command, "--help"])
            except SystemExit:
                # Help is expected to exit
                pass
            except Exception as e:
                pytest.fail(f"Command {command} failed: {e}")
                
    def test_cli_error_handling(self):
        """Test CLI error handling"""
        # Test with invalid arguments
        with pytest.raises(SystemExit):
            main(["invalid", "arguments"])
            
        # Test with missing required arguments
        with pytest.raises(SystemExit):
            main(["template"])
            
        # Test with invalid option values
        with pytest.raises(SystemExit):
            main(["template", "--industry", "invalid", "--type", "test"]) 