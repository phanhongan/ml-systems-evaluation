"""Type definitions for ML Systems Evaluation Framework"""

from enum import Enum


class SystemType(Enum):
    """Types of ML systems supported by the framework"""

    SINGLE_MODEL = "single_model"
    WORKFLOW = "workflow"
    PIPELINE = "pipeline"
    DISTRIBUTED = "distributed"


class CriticalityLevel(Enum):
    """Criticality levels for ML systems"""

    SAFETY_CRITICAL = "safety_critical"
    BUSINESS_CRITICAL = "business_critical"
    OPERATIONAL = "operational"
    EXPERIMENTAL = "experimental"


class ComplianceStandard(Enum):
    """Industry compliance standards"""

    DO_178C = "DO-178C"  # Aviation safety
    ISO_26262 = "ISO-26262"  # Automotive safety
    IEC_61508 = "IEC-61508"  # Industrial safety
    FDA_510K = "FDA-510K"  # Medical devices
    SOX = "SOX"  # Financial compliance
    GDPR = "GDPR"  # Data privacy
    NONE = "none"


class EvaluationMode(Enum):
    """Evaluation modes"""

    VALIDATION = "validation"
    SINGLE = "single"
    CONTINUOUS = "continuous"
    WORKFLOW = "workflow"


class ReportType(Enum):
    """Report types"""

    RELIABILITY = "reliability"
    SAFETY = "safety"
    COMPLIANCE = "compliance"
    BUSINESS_IMPACT = "business_impact"
    TREND = "trend"
    INCIDENT = "incident"


class IndustryType(Enum):
    """Supported industries"""

    MANUFACTURING = "manufacturing"
    AVIATION = "aviation"
    ENERGY = "energy"
    HEALTHCARE = "healthcare"
    FINANCIAL = "financial"
    AUTOMOTIVE = "automotive"
    CUSTOM = "custom"


class TemplateType(Enum):
    """Template types per industry"""

    # Manufacturing
    QUALITY_CONTROL = "quality_control"
    PREDICTIVE_MAINTENANCE = "predictive_maintenance"

    # Aviation
    SAFETY_DECISION = "safety_decision"
    FLIGHT_CONTROL = "flight_control"

    # Energy
    GRID_OPTIMIZATION = "grid_optimization"
    DEMAND_PREDICTION = "demand_prediction"

    # Healthcare
    MEDICAL_DIAGNOSIS = "medical_diagnosis"
    PATIENT_MONITORING = "patient_monitoring"

    # Financial
    FRAUD_DETECTION = "fraud_detection"
    RISK_ASSESSMENT = "risk_assessment"

    # Automotive
    AUTONOMOUS_DRIVING = "autonomous_driving"
    VEHICLE_SAFETY = "vehicle_safety"
