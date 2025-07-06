"""Configuration loading utilities for ML Systems Evaluation"""

import os
import yaml
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

from ..core.types import IndustryType, SystemType, CriticalityLevel


class ConfigLoader:
    """Configuration loader with validation for Industrial AI systems"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.supported_formats = ['.yaml', '.yml', '.json']
        
    def load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from file with validation"""
        try:
            path = Path(config_path)
            
            if not path.exists():
                raise FileNotFoundError(f"Configuration file not found: {config_path}")
                
            if path.suffix not in self.supported_formats:
                raise ValueError(f"Unsupported file format: {path.suffix}")
                
            with open(path, 'r', encoding='utf-8') as f:
                if path.suffix in ['.yaml', '.yml']:
                    config = yaml.safe_load(f)
                elif path.suffix == '.json':
                    config = json.load(f)
                else:
                    raise ValueError(f"Unsupported file format: {path.suffix}")
                    
            # Validate and normalize configuration
            config = self._normalize_config(config)
            self._validate_basic_structure(config)
            
            self.logger.info(f"Successfully loaded configuration from {config_path}")
            return config
            
        except Exception as e:
            self.logger.error(f"Failed to load configuration from {config_path}: {e}")
            raise
            
    def _normalize_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize configuration structure"""
        # Ensure required top-level sections exist
        if 'system' not in config:
            config['system'] = {}
            
        if 'slos' not in config:
            config['slos'] = {}
            
        if 'collectors' not in config:
            config['collectors'] = []
            
        if 'evaluators' not in config:
            config['evaluators'] = []
            
        # Set defaults for system configuration
        system = config['system']
        system.setdefault('name', 'Unknown System')
        system.setdefault('type', 'single_model')
        system.setdefault('criticality', 'operational')
        
        return config
        
    def _validate_basic_structure(self, config: Dict[str, Any]):
        """Validate basic configuration structure"""
        required_sections = ['system', 'slos']
        missing_sections = [section for section in required_sections if section not in config]
        
        if missing_sections:
            raise ValueError(f"Missing required configuration sections: {missing_sections}")
            
        # Validate system configuration
        system = config['system']
        if not isinstance(system, dict):
            raise ValueError("System configuration must be a dictionary")
            
        # Validate SLOs
        slos = config['slos']
        if not isinstance(slos, dict):
            raise ValueError("SLOs configuration must be a dictionary")
            
        # Validate collectors
        collectors = config.get('collectors', [])
        if not isinstance(collectors, list):
            raise ValueError("Collectors configuration must be a list")
            
        # Validate evaluators
        evaluators = config.get('evaluators', [])
        if not isinstance(evaluators, list):
            raise ValueError("Evaluators configuration must be a list")
            
    def load_template(self, industry: str, template_type: str) -> Dict[str, Any]:
        """Load industry-specific template configuration"""
        try:
            # This would load from template files
            # For now, return a basic template structure
            template = self._get_basic_template(industry, template_type)
            self.logger.info(f"Loaded template for {industry}/{template_type}")
            return template
            
        except Exception as e:
            self.logger.error(f"Failed to load template {industry}/{template_type}: {e}")
            raise
            
    def _get_basic_template(self, industry: str, template_type: str) -> Dict[str, Any]:
        """Get basic template structure for industry and type"""
        # This is a simplified template - in practice, these would be loaded from files
        templates = {
            'manufacturing': {
                'quality_control': {
                    'system': {
                        'name': 'Manufacturing Quality Control System',
                        'type': 'workflow',
                        'criticality': 'business_critical'
                    },
                    'slos': {
                        'defect_detection_accuracy': {
                            'target': 0.98,
                            'window': '24h',
                            'error_budget': 0.02,
                            'description': 'Accuracy in detecting manufacturing defects'
                        },
                        'prediction_latency': {
                            'target': 100,
                            'window': '1h',
                            'error_budget': 0.05,
                            'description': 'Time to predict quality issues (ms)'
                        }
                    },
                    'collectors': [
                        {
                            'type': 'online',
                            'endpoint': 'http://manufacturing-metrics:9090'
                        }
                    ],
                    'evaluators': [
                        {
                            'type': 'reliability',
                            'error_budget_window': '30d'
                        }
                    ]
                }
            },
            'aviation': {
                'safety_decision': {
                    'system': {
                        'name': 'Aviation Safety Decision System',
                        'type': 'single_model',
                        'criticality': 'safety_critical'
                    },
                    'slos': {
                        'decision_accuracy': {
                            'target': 0.9999,
                            'window': '24h',
                            'error_budget': 0.0001,
                            'description': 'Accuracy of safety-critical decisions',
                            'compliance_standard': 'DO-178C',
                            'safety_critical': True
                        },
                        'response_time': {
                            'target': 50,
                            'window': '1h',
                            'error_budget': 0.01,
                            'description': 'Decision response time (ms)',
                            'safety_critical': True
                        }
                    },
                    'collectors': [
                        {
                            'type': 'online',
                            'endpoint': 'http://aviation-system:8080/metrics'
                        }
                    ],
                    'evaluators': [
                        {
                            'type': 'reliability',
                            'error_budget_window': '7d'
                        },
                        {
                            'type': 'safety',
                            'compliance_standards': ['DO-178C']
                        }
                    ]
                }
            }
        }
        
        if industry in templates and template_type in templates[industry]:
            return templates[industry][template_type]
        else:
            raise ValueError(f"Template not found: {industry}/{template_type}")
            
    def save_config(self, config: Dict[str, Any], output_path: str):
        """Save configuration to file"""
        try:
            path = Path(output_path)
            
            # Ensure directory exists
            path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(path, 'w', encoding='utf-8') as f:
                if path.suffix in ['.yaml', '.yml']:
                    yaml.dump(config, f, default_flow_style=False, indent=2)
                elif path.suffix == '.json':
                    json.dump(config, f, indent=2)
                else:
                    raise ValueError(f"Unsupported output format: {path.suffix}")
                    
            self.logger.info(f"Configuration saved to {output_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to save configuration to {output_path}: {e}")
            raise 