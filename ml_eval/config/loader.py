"""Configuration loader for ML Systems Evaluation Framework"""

import json
import logging
from pathlib import Path
from typing import Any

import yaml


class ConfigLoader:
    """Load configuration from various file formats"""

    def __init__(self) -> None:
        """Initialize configuration loader"""
        self.logger = logging.getLogger(__name__)
        self.supported_formats = [".yaml", ".yml", ".json"]
        self.template_dir = Path(__file__).parent.parent / "templates"

    def load_config(self, config_path: str) -> dict[str, Any]:
        """Load configuration from file or directory"""
        path = Path(config_path)

        if path.is_file():
            return self._load_single_file(path)
        elif path.is_dir():
            return self._load_directory(path)
        else:
            raise FileNotFoundError(f"Configuration path not found: {config_path}")

    def load_template(self, template_name: str) -> dict[str, Any]:
        """Load configuration template by name"""
        template_path = self.template_dir / f"{template_name}.yaml"

        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_name}")

        return self._load_single_file(template_path)

    def _load_single_file(self, file_path: Path) -> dict[str, Any]:
        """Load configuration from a single file"""
        if not file_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {file_path}")

        file_extension = file_path.suffix.lower()

        if file_extension not in self.supported_formats:
            raise ValueError(
                f"Unsupported file format: {file_extension}. "
                f"Supported formats: {self.supported_formats}"
            )

        try:
            with open(file_path, encoding="utf-8") as f:
                if file_extension in [".yaml", ".yml"]:
                    return yaml.safe_load(f) or {}
                elif file_extension == ".json":
                    return json.load(f)
                else:
                    raise ValueError(f"Unsupported file format: {file_extension}")

        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in {file_path}: {e}") from e
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {file_path}: {e}") from e
        except Exception as e:
            raise ValueError(
                f"Failed to load configuration from {file_path}: {e}"
            ) from e

    def _load_directory(self, dir_path: Path) -> dict[str, Any]:
        """Load configuration from a directory (merge all config files)"""
        config: dict[str, Any] = {}

        # Find all configuration files in the directory
        config_files = []
        for file_path in dir_path.iterdir():
            if (
                file_path.is_file()
                and file_path.suffix.lower() in self.supported_formats
            ):
                config_files.append(file_path)

        # Sort files to ensure consistent loading order
        config_files.sort(key=lambda x: x.name)

        # Load and merge all configuration files
        for file_path in config_files:
            try:
                file_config = self._load_single_file(file_path)
                config = self._merge_configs(config, file_config)
            except Exception as e:
                raise ValueError(
                    f"Failed to load configuration from {file_path}: {e}"
                ) from e

        return config

    def _merge_configs(
        self, base_config: dict[str, Any], new_config: dict[str, Any]
    ) -> dict[str, Any]:
        """Merge two configuration dictionaries"""
        merged = base_config.copy()

        for key, value in new_config.items():
            if (
                key in merged
                and isinstance(merged[key], dict)
                and isinstance(value, dict)
            ):
                # Recursively merge nested dictionaries
                merged[key] = self._merge_configs(merged[key], value)
            else:
                # Overwrite or add the value
                merged[key] = value

        return merged

    def list_templates(self) -> list[str]:
        """List available configuration templates"""
        templates = []

        if self.template_dir.exists():
            for template_file in self.template_dir.glob("*.yaml"):
                templates.append(template_file.stem)

        return templates

    def validate_file_format(self, file_path: str) -> bool:
        """Validate if a file has a supported configuration format"""
        path = Path(file_path)
        return path.suffix.lower() in self.supported_formats

    def get_file_info(self, file_path: str) -> dict[str, Any]:
        """Get information about a configuration file"""
        path = Path(file_path)

        if not path.exists():
            return {"error": "File not found"}

        info = {
            "path": str(path),
            "size": path.stat().st_size,
            "format": path.suffix.lower(),
            "supported": path.suffix.lower() in self.supported_formats,
        }

        if info["supported"]:
            try:
                config = self._load_single_file(path)
                info["valid"] = True
                info["keys"] = list(config.keys()) if isinstance(config, dict) else []
            except Exception as e:
                info["valid"] = False
                info["error"] = str(e)

        return info
