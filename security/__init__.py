"""
REM-CODE Security Framework
Enterprise-grade security for Constitutional Programming Language
"""

from .authentication import AuthenticationManager, User, Role
from .authorization import AuthorizationManager, Permission, Policy
from .encryption import EncryptionManager, KeyManager
from .audit import AuditLogger, AuditEvent
from .compliance import ComplianceManager, GDPRCompliance, CCPACompliance

__version__ = "1.0.0"
__author__ = "REM-CODE Security Team"

__all__ = [
    # Authentication
    "AuthenticationManager",
    "User", 
    "Role",
    
    # Authorization
    "AuthorizationManager",
    "Permission",
    "Policy",
    
    # Encryption
    "EncryptionManager",
    "KeyManager",
    
    # Audit
    "AuditLogger",
    "AuditEvent",
    
    # Compliance
    "ComplianceManager",
    "GDPRCompliance",
    "CCPACompliance"
]

# Security Framework Info
SECURITY_INFO = {
    "version": __version__,
    "features": [
        "Multi-factor Authentication",
        "Role-based Access Control",
        "End-to-end Encryption",
        "Comprehensive Audit Logging",
        "GDPR/CCPA Compliance",
        "SOC2/ISO27001 Ready"
    ],
    "compliance": [
        "GDPR",
        "CCPA", 
        "SOC2",
        "ISO27001",
        "HIPAA"
    ]
} 