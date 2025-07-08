#!/usr/bin/env python3
"""
Semiconductor Etching Digital Twins Example

This example demonstrates how to use the ML Systems Evaluation framework
for semiconductor etching digital twins, including equipment monitoring,
yield prediction, and quality control for etching processes.
"""

import asyncio
import json
import logging
import os
from datetime import datetime, timedelta
from typing import Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EtchingDigitalTwin:
    """Digital twin for semiconductor etching processes."""

    def __init__(self, config_path: str):
        """Initialize the digital twin with configuration."""
        self.config = self._load_config(config_path)
        self.equipment_states = {}
        self.process_parameters = {}
        self.quality_metrics = {}
        self.alerts = []

    def _load_config(self, config_path: str) -> dict[str, Any]:
        """Load configuration from YAML file."""
        import yaml

        with open(config_path) as f:
            return yaml.safe_load(f)

    async def simulate_etch_process(
        self, wafer_id: str, etch_type: str
    ) -> dict[str, Any]:
        """Simulate etching process with digital twin monitoring."""
        logger.info(
            f"Starting etch process for wafer {wafer_id}, etch type: {etch_type}"
        )

        # Initialize process parameters
        process_params = self._get_etch_parameters(etch_type)
        equipment_status = self._get_equipment_status(etch_type)

        # Simulate process execution with real-time monitoring
        results = {
            "wafer_id": wafer_id,
            "etch_type": etch_type,
            "start_time": datetime.now().isoformat(),
            "process_parameters": process_params,
            "equipment_status": equipment_status,
            "quality_metrics": {},
            "alerts": [],
        }

        # Simulate etch process steps
        for step in self._get_etch_steps(etch_type):
            step_result = await self._execute_etch_step(step, process_params)
            results["quality_metrics"].update(step_result["quality_metrics"])
            results["alerts"].extend(step_result["alerts"])

            # Update digital twin state
            self._update_digital_twin_state(step_result)

        results["end_time"] = datetime.now().isoformat()
        results["yield_prediction"] = self._predict_etch_yield(results)

        logger.info(
            f"Completed etch process for {wafer_id}, predicted yield: {results['yield_prediction']:.2%}"
        )
        return results

    def _get_etch_parameters(self, etch_type: str) -> dict[str, float]:
        """Get etch process parameters for the specified etch type."""
        base_params = {
            "temperature": 25.0,
            "pressure": 760.0,
            "gas_flow": 100.0,
            "rf_power": 300.0,
            "dc_bias": -50.0,
        }

        # Adjust parameters based on etch type
        if etch_type == "plasma_etch":
            base_params.update(
                {
                    "etch_rate": 100.0,
                    "selectivity": 10.0,
                    "uniformity": 0.95,
                    "profile_control": 0.90,
                }
            )
        elif etch_type == "wet_etch":
            base_params.update(
                {
                    "chemical_concentration": 0.1,
                    "ph_level": 7.0,
                    "agitation_speed": 500.0,
                    "etch_rate": 50.0,
                    "uniformity": 0.98,
                }
            )
        elif etch_type == "dry_etch":
            base_params.update(
                {
                    "etch_rate": 80.0,
                    "anisotropy": 0.85,
                    "uniformity": 0.92,
                    "gas_flow": 150.0,
                }
            )
        elif etch_type == "reactive_ion_etch":
            base_params.update(
                {
                    "etch_rate": 120.0,
                    "selectivity": 15.0,
                    "anisotropy": 0.90,
                    "uniformity": 0.94,
                    "ion_current": 2.0,
                }
            )

        return base_params

    def _get_equipment_status(self, etch_type: str) -> dict[str, Any]:
        """Get equipment status for the specified etch type."""
        equipment_map = {
            "plasma_etch": "plasma_etch_chamber",
            "wet_etch": "wet_etch_tank",
            "dry_etch": "dry_etch_chamber",
            "reactive_ion_etch": "rie_chamber",
        }

        equipment_id = equipment_map.get(etch_type, "unknown")
        return {
            "equipment_id": equipment_id,
            "status": "operational",
            "runtime_hours": 1000,
            "maintenance_due": False,
            "last_calibration": datetime.now() - timedelta(days=7),
        }

    def _get_etch_steps(self, etch_type: str) -> list[str]:
        """Get etch process steps for the specified etch type."""
        step_map = {
            "plasma_etch": [
                "wafer_load",
                "chamber_pump",
                "gas_introduction",
                "plasma_ignition",
                "etch_process",
                "chamber_clean",
                "wafer_unload",
            ],
            "wet_etch": [
                "wafer_load",
                "chemical_preparation",
                "immersion",
                "agitation",
                "rinse",
                "dry",
                "wafer_unload",
            ],
            "dry_etch": [
                "wafer_load",
                "chamber_pump",
                "gas_introduction",
                "etch_process",
                "chamber_clean",
                "wafer_unload",
            ],
            "reactive_ion_etch": [
                "wafer_load",
                "chamber_pump",
                "gas_introduction",
                "ion_acceleration",
                "etch_process",
                "chamber_clean",
                "wafer_unload",
            ],
        }
        return step_map.get(etch_type, ["wafer_load", "etch_process", "wafer_unload"])

    async def _execute_etch_step(
        self, step: str, params: dict[str, float]
    ) -> dict[str, Any]:
        """Execute a single etch process step with monitoring."""
        logger.info(f"Executing etch step: {step}")

        # Simulate process execution time
        await asyncio.sleep(0.1)

        # Generate quality metrics
        quality_metrics = self._generate_etch_quality_metrics(params)

        # Check for alerts
        alerts = self._check_etch_alerts(params, quality_metrics)

        return {"step": step, "quality_metrics": quality_metrics, "alerts": alerts}

    def _generate_etch_quality_metrics(
        self, params: dict[str, float]
    ) -> dict[str, float]:
        """Generate quality metrics for the etch process step."""
        import random

        # Base quality metrics for etching
        metrics = {
            "uniformity": random.uniform(0.92, 0.98),
            "defect_density": random.uniform(0.001, 0.008),
            "etch_rate": random.uniform(80, 120),
            "selectivity": random.uniform(8, 15),
            "anisotropy": random.uniform(0.80, 0.95),
            "profile_control": random.uniform(0.85, 0.95),
        }

        # Adjust metrics based on process parameters
        if params.get("temperature", 25) > 30:
            metrics["uniformity"] *= 0.95
        if params.get("pressure", 760) > 800:
            metrics["defect_density"] *= 1.2
        if params.get("rf_power", 300) > 400:
            metrics["etch_rate"] *= 1.1
        if params.get("dc_bias", -50) < -100:
            metrics["anisotropy"] *= 1.05

        return metrics

    def _check_etch_alerts(
        self, params: dict[str, float], metrics: dict[str, float]
    ) -> list[dict[str, Any]]:
        """Check for alerts based on etch process parameters and quality metrics."""
        alerts = []

        # Temperature excursion alert
        if params.get("temperature", 25) > 30:
            alerts.append(
                {
                    "type": "temperature_excursion",
                    "severity": "medium",
                    "message": f"Temperature {params['temperature']}°C exceeds normal range",
                    "timestamp": datetime.now().isoformat(),
                }
            )

        # Defect density alert
        if metrics.get("defect_density", 0) > 0.006:
            alerts.append(
                {
                    "type": "high_defect_density",
                    "severity": "high",
                    "message": f"Defect density {metrics['defect_density']:.4f} exceeds threshold",
                    "timestamp": datetime.now().isoformat(),
                }
            )

        # Etch rate alert
        if metrics.get("etch_rate", 100) > 130:
            alerts.append(
                {
                    "type": "high_etch_rate",
                    "severity": "medium",
                    "message": f"Etch rate {metrics['etch_rate']:.1f} nm/min exceeds specification",
                    "timestamp": datetime.now().isoformat(),
                }
            )

        # Equipment failure prediction
        if self._predict_equipment_failure(params):
            alerts.append(
                {
                    "type": "equipment_failure_imminent",
                    "severity": "critical",
                    "message": "Etch equipment failure predicted within 24 hours",
                    "timestamp": datetime.now().isoformat(),
                }
            )

        return alerts

    def _predict_equipment_failure(self, params: dict[str, float]) -> bool:
        """Predict equipment failure based on parameters."""
        import random

        # Simple failure prediction logic
        failure_probability = 0.01  # Base probability

        # Increase probability based on operating conditions
        if params.get("temperature", 25) > 35:
            failure_probability += 0.05
        if params.get("rf_power", 300) > 500:
            failure_probability += 0.1
        if params.get("runtime_hours", 0) > 2000:
            failure_probability += 0.02

        return random.random() < failure_probability

    def _update_digital_twin_state(self, step_result: dict[str, Any]):
        """Update digital twin state with process results."""
        # Update equipment states
        if "equipment_status" in step_result:
            self.equipment_states.update(step_result["equipment_status"])

        # Update process parameters
        if "process_parameters" in step_result:
            self.process_parameters.update(step_result["process_parameters"])

        # Update quality metrics
        if "quality_metrics" in step_result:
            self.quality_metrics.update(step_result["quality_metrics"])

        # Store alerts
        if "alerts" in step_result:
            self.alerts.extend(step_result["alerts"])

    def _predict_etch_yield(self, results: dict[str, Any]) -> float:
        """Predict etch yield based on process results."""
        import random

        # Base yield prediction
        base_yield = 0.95

        # Adjust based on quality metrics
        quality_metrics = results.get("quality_metrics", {})

        if quality_metrics.get("uniformity", 1.0) < 0.95:
            base_yield *= 0.98
        if quality_metrics.get("defect_density", 0) > 0.005:
            base_yield *= 0.95
        if quality_metrics.get("selectivity", 10) < 8:
            base_yield *= 0.97
        if quality_metrics.get("anisotropy", 0.9) < 0.85:
            base_yield *= 0.96

        # Add some randomness
        yield_variation = random.uniform(-0.02, 0.02)
        final_yield = base_yield + yield_variation

        return max(0.0, min(1.0, final_yield))

    def get_digital_twin_summary(self) -> dict[str, Any]:
        """Get a summary of the digital twin state."""
        return {
            "equipment_states": self.equipment_states,
            "process_parameters": self.process_parameters,
            "quality_metrics": self.quality_metrics,
            "active_alerts": len(
                [a for a in self.alerts if a["severity"] in ["high", "critical"]]
            ),
            "total_alerts": len(self.alerts),
            "timestamp": datetime.now().isoformat(),
        }


async def main():
    """Main function to demonstrate etching digital twins."""
    logger.info("Starting Semiconductor Etching Digital Twins Example")

    # Initialize digital twin
    config_path = os.path.join(
        os.path.dirname(__file__), "semiconductor-etching-digital-twins.yaml"
    )
    digital_twin = EtchingDigitalTwin(config_path)

    # Simulate multiple etch processes
    etch_processes = [
        ("WAFER_001", "plasma_etch"),
        ("WAFER_002", "wet_etch"),
        ("WAFER_003", "dry_etch"),
        ("WAFER_004", "reactive_ion_etch"),
    ]

    results = []
    for wafer_id, etch_type in etch_processes:
        result = await digital_twin.simulate_etch_process(wafer_id, etch_type)
        results.append(result)

        # Print results
        print(f"\n=== Wafer {wafer_id} Etch Results ===")
        print(f"Etch Type: {etch_type}")
        print(f"Predicted Yield: {result['yield_prediction']:.2%}")
        print(f"Quality Metrics: {json.dumps(result['quality_metrics'], indent=2)}")
        print(f"Alerts: {len(result['alerts'])}")

        if result["alerts"]:
            for alert in result["alerts"]:
                print(f"  - {alert['severity'].upper()}: {alert['message']}")

    # Get digital twin summary
    summary = digital_twin.get_digital_twin_summary()
    print("\n=== Etching Digital Twin Summary ===")
    print(f"Active Alerts: {summary['active_alerts']}")
    print(f"Total Alerts: {summary['total_alerts']}")
    print(f"Equipment States: {len(summary['equipment_states'])}")
    print(f"Process Parameters: {len(summary['process_parameters'])}")

    logger.info("Semiconductor Etching Digital Twins Example completed")


if __name__ == "__main__":
    asyncio.run(main())
