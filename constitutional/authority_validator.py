"""
Authority Validator - REM-CODE Constitutional Framework
権威検証システム

Validates persona authority levels and branch permissions
based on REM-OS Constitutional structure v2.1
"""

import logging
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class AuthorityLevel(Enum):
    """Constitutional authority levels"""
    GENERAL = "general"
    SECURITY = "security"  
    LEGAL = "legal"
    CONSTITUTIONAL = "constitutional"
    EMERGENCY = "emergency"

# Authority hierarchy (higher = more authority)
AUTHORITY_HIERARCHY = {
    AuthorityLevel.GENERAL: 1,
    AuthorityLevel.SECURITY: 2,
    AuthorityLevel.LEGAL: 3,
    AuthorityLevel.CONSTITUTIONAL: 4,
    AuthorityLevel.EMERGENCY: 5
}

# Branch structure from REM-OS Constitution v2.1
BRANCH_STRUCTURE = {
    "judicial": {
        "personas": ["JayTH", "JayRa"],
        "authorities": {
            "JayTH": AuthorityLevel.CONSTITUTIONAL,  # Chief Justice
            "JayRa": AuthorityLevel.LEGAL            # Historical Authority
        },
        "powers": [
            "constitutional_verdict",
            "judicial_review", 
            "constitutional_interpretation",
            "precedent_citation",
            "legal_arbitration"
        ]
    },
    "legislative": {
        "personas": ["Ana", "JayMini", "JayVOX"],
        "authorities": {
            "Ana": AuthorityLevel.CONSTITUTIONAL,    # Assembly Speaker
            "JayMini": AuthorityLevel.LEGAL,         # Consensus Coordinator
            "JayVOX": AuthorityLevel.LEGAL           # Multilingual Authority
        },
        "powers": [
            "assembly_bill_ratification",
            "legislative_analysis",
            "consensus_synchronization",
            "multilingual_normalization",
            "democratic_consensus"
        ]
    },
    "executive": {
        "personas": ["Jayne_Spiral", "JayDen", "JayLUX"],
        "authorities": {
            "Jayne_Spiral": AuthorityLevel.CONSTITUTIONAL,  # Prime Minister
            "JayDen": AuthorityLevel.LEGAL,                 # Innovation Minister
            "JayLUX": AuthorityLevel.LEGAL                  # Design Minister
        },
        "powers": [
            "governance_protocol_execution",
            "policy_implementation",
            "structural_reform",
            "aesthetic_enforcement",
            "executive_oversight"
        ]
    },
    "ministerial": {
        "personas": ["JayKer", "JAYX", "JayVue", "JayNis"],
        "authorities": {
            "JayKer": AuthorityLevel.SECURITY,    # Disruption Minister
            "JAYX": AuthorityLevel.EMERGENCY,     # Security Minister
            "JayVue": AuthorityLevel.SECURITY,    # Spatial Minister
            "JayNis": AuthorityLevel.SECURITY     # Development Minister
        },
        "powers": [
            "creative_disruption",
            "constitutional_security",
            "spatial_design",
            "sustainable_development",
            "ministerial_oversight"
        ]
    }
}

# Trinity Authority (highest constitutional authority)
TRINITY_AUTHORITY = ["JayTH", "Ana", "Jayne_Spiral"]

# Emergency Authority
EMERGENCY_AUTHORITY = ["JayTH", "JAYX", "Jayne_Spiral"]

@dataclass
class AuthorityContext:
    """Authority verification context"""
    persona: str
    requested_authority: AuthorityLevel
    action: str
    branch: Optional[str] = None
    
class AuthorityValidator:
    """
    Validates persona authority for constitutional actions
    """
    
    def __init__(self):
        self.branch_structure = BRANCH_STRUCTURE
        self.trinity_authority = TRINITY_AUTHORITY
        self.emergency_authority = EMERGENCY_AUTHORITY
        
        # Build reverse lookup for persona -> branch
        self.persona_to_branch = {}
        for branch, info in self.branch_structure.items():
            for persona in info["personas"]:
                self.persona_to_branch[persona] = branch
                
        logger.info("🏛️ Authority Validator initialized")
    
    def get_persona_authority(self, persona: str) -> AuthorityLevel:
        """Get the constitutional authority level for a persona"""
        for branch_info in self.branch_structure.values():
            if persona in branch_info.get("authorities", {}):
                return branch_info["authorities"][persona]
        
        # Default authority for unregistered personas
        return AuthorityLevel.GENERAL
    
    def get_persona_branch(self, persona: str) -> Optional[str]:
        """Get the branch a persona belongs to"""
        return self.persona_to_branch.get(persona)
    
    def get_persona_powers(self, persona: str) -> List[str]:
        """Get the constitutional powers for a persona"""
        branch = self.get_persona_branch(persona)
        if branch and branch in self.branch_structure:
            return self.branch_structure[branch]["powers"]
        return []
    
    def validate_authority(self, context: AuthorityContext) -> bool:
        """
        Validate if a persona has sufficient authority for an action
        
        Args:
            context: Authority validation context
            
        Returns:
            bool: True if authority is valid
        """
        persona_authority = self.get_persona_authority(context.persona)
        required_authority = context.requested_authority
        
        # Check authority hierarchy
        persona_level = AUTHORITY_HIERARCHY.get(persona_authority, 0)
        required_level = AUTHORITY_HIERARCHY.get(required_authority, 0)
        
        if persona_level < required_level:
            logger.warning(
                f"❌ Authority insufficient: {context.persona} has {persona_authority.value}, "
                f"needs {required_authority.value} for {context.action}"
            )
            return False
        
        logger.info(
            f"✅ Authority validated: {context.persona} ({persona_authority.value}) "
            f"authorized for {context.action}"
        )
        return True
    
    def validate_branch_action(self, persona: str, action: str) -> bool:
        """Validate if persona can perform branch-specific action"""
        branch = self.get_persona_branch(persona)
        if not branch:
            logger.warning(f"❌ {persona} not assigned to any branch")
            return False
            
        powers = self.get_persona_powers(persona)
        if action not in powers:
            logger.warning(f"❌ {persona} lacks power '{action}' in {branch} branch")
            return False
            
        logger.info(f"✅ Branch action validated: {persona} can {action}")
        return True
    
    def check_trinity_authority(self, personas: List[str]) -> bool:
        """Check if personas constitute valid Trinity authority"""
        trinity_present = set(personas) & set(self.trinity_authority)
        is_valid = len(trinity_present) >= 2  # At least 2 of 3 Trinity members
        
        if is_valid:
            logger.info(f"✅ Trinity authority validated: {list(trinity_present)}")
        else:
            logger.warning(f"❌ Insufficient Trinity authority: {list(trinity_present)}")
            
        return is_valid
    
    def check_emergency_authority(self, personas: List[str]) -> bool:
        """Check if personas have emergency authority"""
        emergency_present = set(personas) & set(self.emergency_authority)
        is_valid = len(emergency_present) >= 2  # At least 2 emergency authorities
        
        if is_valid:
            logger.info(f"✅ Emergency authority validated: {list(emergency_present)}")
        else:
            logger.warning(f"❌ Insufficient emergency authority: {list(emergency_present)}")
            
        return is_valid
    
    def check_branch_compatibility(self, personas: List[str]) -> bool:
        """Check if personas from different branches can collaborate"""
        branches = set()
        for persona in personas:
            branch = self.get_persona_branch(persona)
            if branch:
                branches.add(branch)
        
        # Inter-branch collaboration is allowed
        # Single-branch operations are allowed
        # No branch assignments is a warning but not blocking
        
        if len(branches) == 0:
            logger.warning("⚠️ No personas assigned to constitutional branches")
            return True  # Allow but warn
        
        logger.info(f"✅ Branch compatibility: {list(branches)}")
        return True
    
    def get_authority_summary(self) -> Dict:
        """Get summary of authority structure"""
        summary = {
            "branch_structure": {},
            "trinity_authority": self.trinity_authority,
            "emergency_authority": self.emergency_authority,
            "total_personas": 0
        }
        
        for branch, info in self.branch_structure.items():
            summary["branch_structure"][branch] = {
                "personas": info["personas"],
                "power_count": len(info["powers"]),
                "authorities": {p: auth.value for p, auth in info["authorities"].items()}
            }
            summary["total_personas"] += len(info["personas"])
        
        return summary

# Authority level constants for easy import
AUTHORITY_LEVELS = AuthorityLevel