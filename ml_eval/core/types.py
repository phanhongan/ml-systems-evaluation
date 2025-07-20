"""Type definitions for ML Systems Evaluation Framework"""

from enum import Enum


class CriticalityLevel(Enum):
    """Criticality levels for ML systems"""

    OPERATIONAL = "operational"
    BUSINESS_CRITICAL = "business_critical"
    SAFETY_CRITICAL = "safety_critical"


class ComplianceStandard(Enum):
    """Industry compliance standards"""

    # Aviation safety standards
    DO_178C = "DO-178C"  # Software Considerations in Airborne Systems
    DO_254 = "DO-254"  # Hardware Considerations in Airborne Systems
    ARP4754A = "ARP4754A"  # Guidelines for Development of Civil Aircraft and Systems
    FAA = "FAA"  # Federal Aviation Administration
    EASA = "EASA"  # European Aviation Safety Agency
    ICAO = "ICAO"  # International Civil Aviation Organization

    # Maritime safety standards
    COLREGs = "COLREGs"  # International Regulations for Preventing Collisions at Sea
    IMO = "IMO Guidelines"  # International Maritime Organization Guidelines

    # Energy standards
    NERC = "NERC"  # North American Electric Reliability Corporation
    FERC = "FERC"  # Federal Energy Regulatory Commission

    # Manufacturing standards
    ISO_9001 = "ISO-9001"  # Quality Management Systems
    ISO_14001 = "ISO-14001"  # Environmental Management Systems

    # General standards
    GDPR = "GDPR"  # Data privacy
    NONE = "none"


class EvaluationMode(Enum):
    """Evaluation modes"""

    VALIDATION = "validation"
    SINGLE = "single"
    CONTINUOUS = "continuous"
    WORKFLOW = "workflow"
    INTERPRETABILITY = "interpretability"
    EDGE_CASE = "edge_case"
    FMEA = "fmea"


class ReportType(Enum):
    """Report types"""

    RELIABILITY = "reliability"
    SAFETY = "safety"
    COMPLIANCE = "compliance"
    BUSINESS_IMPACT = "business_impact"
    TREND = "trend"
    INCIDENT = "incident"
    INTERPRETABILITY = "interpretability"
    EDGE_CASE = "edge_case"


class IndustryType(Enum):
    """Supported industries"""

    MANUFACTURING = "manufacturing"
    AVIATION = "aviation"
    ENERGY = "energy"
    MARITIME = "maritime"
    AQUACULTURE = "aquaculture"
    CUSTOM = "custom"


class TemplateType(Enum):
    """Template types per industry"""

    # Manufacturing
    PREDICTIVE_MAINTENANCE = "predictive_maintenance"
    DEMAND_FORECASTING = "demand_forecasting"

    # Aviation
    SAFETY_DECISION = "safety_decision"
    FLIGHT_CONTROL = "flight_control"

    # Energy
    GRID_OPTIMIZATION = "grid_optimization"
    DEMAND_PREDICTION = "demand_prediction"

    # Maritime
    COLLISION_AVOIDANCE = "collision_avoidance"
    NAVIGATION_SYSTEM = "navigation_system"

    # Aquaculture
    SPECIES_CLASSIFICATION = "species_classification"
    ENVIRONMENTAL_MONITORING = "environmental_monitoring"
