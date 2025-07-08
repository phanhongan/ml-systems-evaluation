"""Template management for ML Systems Evaluation Framework"""

from pathlib import Path
from typing import Any

# Remove TemplateFactory import

__all__ = ["TemplateManager"]


class TemplateManager:
    """Manages external YAML-based templates"""

    def __init__(self, template_dir: str | None = None):
        self.template_dir = (
            Path(template_dir) if template_dir else Path(__file__).parent / "files"
        )
        # Remove self.factory = TemplateFactory()

    def get_template(self, industry: str, template_type: str) -> dict[str, Any]:
        """Get template from external YAML file"""
        external_template = self._load_external_template(industry, template_type)
        if external_template:
            return external_template

        raise ValueError(
            f"Template not found for industry: {industry}, type: {template_type}"
        )

    def _load_external_template(
        self, industry: str, template_type: str
    ) -> dict[str, Any] | None:
        """Load template from external YAML file"""
        template_path = self.template_dir / f"{industry}-{template_type}.yaml"

        if not template_path.exists():
            return None

        try:
            import yaml

            with open(template_path) as f:
                return yaml.safe_load(f)
        except Exception:
            return None

    def list_available_templates(self) -> list[str]:
        """List all available external YAML templates"""
        templates = []

        # Add external templates
        if self.template_dir.exists():
            for template_file in self.template_dir.glob("*.yaml"):
                templates.append(template_file.stem)

        return templates

    def create_template_file(
        self, _industry: str, _template_type: str, _output_path: str | None = None
    ) -> str:
        """Create external template file (deprecated - all templates are now external)"""
        raise ValueError(
            "All templates are now external YAML files. Use existing templates or create new ones manually."
        )
