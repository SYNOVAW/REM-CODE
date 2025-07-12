"""
REM-CODE Constitutional Framework v2.4
Democratic Programming Extensions for Official REM-CODE

Integrates Constitutional Programming capabilities with 
the official Collapse Spiral computation model.
"""

from .authority_validator import AuthorityValidator, AuthorityLevel, AuthorityContext
from .sr_threshold_checker import SRThresholdChecker, DecisionType, SRContext  
from .signature_manager import SignatureManager, SignatureType, ConstitutionalSignature
from .compliance_checker import ConstitutionalComplianceChecker, ComplianceContext, ComplianceResult
from .constitutional_engine import ConstitutionalEngine, ConstitutionalAction, ExecutionResult

__version__ = "2.4.0"
__author__ = "Constitutional Enhancement Project"

__all__ = [
    # Core Components
    "AuthorityValidator",
    "SRThresholdChecker", 
    "SignatureManager",
    "ConstitutionalComplianceChecker",
    "ConstitutionalEngine",
    
    # Data Classes
    "AuthorityLevel",
    "AuthorityContext", 
    "DecisionType",
    "SRContext",
    "SignatureType",
    "ConstitutionalSignature",
    "ComplianceContext",
    "ComplianceResult", 
    "ConstitutionalAction",
    "ExecutionResult"
]

# Constitutional Framework Integration Info
CONSTITUTIONAL_INFO = {
    "version": __version__,
    "compatible_with": "REM-CODE v2.3+",
    "features": [
        "Democratic Authority Validation",
        "SR-based Consensus Requirements",
        "Cryptographic Accountability",
        "Constitutional Compliance Checking",
        "Emergency Protocol Management",
        "Multi-Persona Coordination"
    ],
    "grammar_extensions": [
        "authority_block",
        "consensus_block", 
        "validate_block",
        "emergency_block",
        "trinity_block",
        "constitutional_block"
    ]
}