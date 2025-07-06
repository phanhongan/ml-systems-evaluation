"""Drift evaluator for ML Systems Evaluation"""

from typing import Dict, List, Any
from datetime import datetime

from .base import BaseEvaluator


class DriftEvaluator(BaseEvaluator):
    """Evaluate data and model drift with business impact assessment"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.drift_thresholds = config.get("drift_thresholds", {})
        self.business_impact_thresholds = config.get("business_impact_thresholds", {})
        
    def get_required_metrics(self) -> List[str]:
        """Get required metrics for drift evaluation"""
        return list(self.drift_thresholds.keys())
        
    def evaluate(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate data and model drift"""
        if not self.validate_metrics(metrics):
            return {"error": "Missing required drift metrics"}
            
        results = {
            "drift_metrics": {},
            "business_impact": {},
            "drift_alerts": [],
            "overall_drift_score": 0.0,
            "alerts": []
        }
        
        # Evaluate drift metrics
        for metric_name, threshold in self.drift_thresholds.items():
            if metric_name in metrics:
                drift_result = self._evaluate_drift_metric(metric_name, threshold, metrics[metric_name])
                results["drift_metrics"][metric_name] = drift_result
                
        # Assess business impact
        results["business_impact"] = self._assess_business_impact(results["drift_metrics"])
        
        # Calculate overall drift score
        if results["drift_metrics"]:
            total_drift = sum(metric.get("drift_score", 0) for metric in results["drift_metrics"].values())
            results["overall_drift_score"] = total_drift / len(results["drift_metrics"])
            
        # Generate drift alerts
        results["drift_alerts"] = self._generate_drift_alerts(results["drift_metrics"])
        
        # Generate overall alerts
        results["alerts"] = self._generate_overall_alerts(results)
        
        return results
        
    def _evaluate_drift_metric(self, metric_name: str, threshold: Dict[str, Any], current_value: float) -> Dict[str, Any]:
        """Evaluate a single drift metric"""
        warning_threshold = threshold.get("warning", 0.1)
        critical_threshold = threshold.get("critical", 0.3)
        
        # Calculate drift score (0-1, where 0 is no drift, 1 is maximum drift)
        drift_score = min(1.0, current_value / critical_threshold) if critical_threshold > 0 else 0.0
        
        # Determine drift level
        if drift_score >= critical_threshold:
            level = "critical"
        elif drift_score >= warning_threshold:
            level = "warning"
        else:
            level = "normal"
            
        return {
            "value": current_value,
            "threshold": threshold,
            "drift_score": drift_score,
            "level": level,
            "timestamp": datetime.now().isoformat()
        }
        
    def _assess_business_impact(self, drift_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Assess business impact of drift"""
        impact_score = 0.0
        impact_details = []
        
        for metric_name, metric_data in drift_metrics.items():
            drift_score = metric_data.get("drift_score", 0)
            level = metric_data.get("level", "normal")
            
            # Calculate business impact based on drift level
            if level == "critical":
                impact_score += 0.5
                impact_details.append(f"Critical drift in {metric_name}: High business impact")
            elif level == "warning":
                impact_score += 0.2
                impact_details.append(f"Warning drift in {metric_name}: Moderate business impact")
                
        return {
            "impact_score": min(1.0, impact_score),
            "impact_details": impact_details,
            "recommendations": self._generate_business_recommendations(drift_metrics)
        }
        
    def _generate_business_recommendations(self, drift_metrics: Dict[str, Any]) -> List[str]:
        """Generate business recommendations based on drift"""
        recommendations = []
        
        critical_drifts = [name for name, data in drift_metrics.items() if data.get("level") == "critical"]
        warning_drifts = [name for name, data in drift_metrics.items() if data.get("level") == "warning"]
        
        if critical_drifts:
            recommendations.append(f"Immediate model retraining required due to critical drift in: {', '.join(critical_drifts)}")
            
        if warning_drifts:
            recommendations.append(f"Monitor drift trends in: {', '.join(warning_drifts)}")
            
        if not critical_drifts and not warning_drifts:
            recommendations.append("No significant drift detected. Continue monitoring.")
            
        return recommendations
        
    def _generate_drift_alerts(self, drift_metrics: Dict[str, Any]) -> List[str]:
        """Generate drift-specific alerts"""
        alerts = []
        
        for metric_name, metric_data in drift_metrics.items():
            level = metric_data.get("level", "normal")
            drift_score = metric_data.get("drift_score", 0)
            
            if level == "critical":
                alerts.append(f"CRITICAL DRIFT: {metric_name} at {drift_score:.2%} - Immediate action required")
            elif level == "warning":
                alerts.append(f"DRIFT WARNING: {metric_name} at {drift_score:.2%} - Monitor closely")
                
        return alerts
        
    def _generate_overall_alerts(self, results: Dict[str, Any]) -> List[str]:
        """Generate overall alerts"""
        alerts = []
        
        # Check overall drift score
        overall_score = results["overall_drift_score"]
        if overall_score > 0.5:
            alerts.append(f"High overall drift score: {overall_score:.2%}")
            
        # Check business impact
        business_impact = results["business_impact"]
        impact_score = business_impact.get("impact_score", 0)
        if impact_score > 0.3:
            alerts.append(f"Significant business impact from drift: {impact_score:.2%}")
            
        # Add drift alerts
        alerts.extend(results["drift_alerts"])
        
        return alerts 