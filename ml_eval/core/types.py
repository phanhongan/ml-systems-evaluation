"""Type definitions for ML Systems Evaluation Framework"""

from enum import Enum


class CriticalityLevel(Enum):
    """Criticality levels for ML systems"""

    OPERATIONAL = "operational"
    BUSINESS_CRITICAL = "business_critical"
    SAFETY_CRITICAL = "safety_critical"


class ComplianceStandard(Enum):
    """Compliance standards for ML systems"""

    # Aviation
    DO_178C = "DO-178C"
    DO_254 = "DO-254"
    ARP4754A = "ARP4754A"

    # Maritime
    SOLAS = "SOLAS"
    COLREGS = "COLREGS"

    # Manufacturing
    ISO_13485 = "ISO-13485"
    FDA_510K = "FDA-510K"

    # Energy
    IEC_61508 = "IEC-61508"
    ISO_13849 = "ISO-13849"


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
    MARITIME = "maritime"
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

    # Maritime
    COLLISION_AVOIDANCE = "collision_avoidance"
    NAVIGATION_SAFETY = "navigation_safety"
