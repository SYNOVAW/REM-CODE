"""
REM-CODE Authorization Manager
Role-based access control and policy management for enterprise security
"""

import time
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class PermissionLevel(Enum):
    """Permission levels for constitutional programming"""
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    ADMIN = "admin"
    CONSTITUTIONAL = "constitutional"
    EMERGENCY = "emergency"

class ResourceType(Enum):
    """Resource types for authorization"""
    CODE = "code"
    DATA = "data"
    SYSTEM = "system"
    CONSTITUTIONAL = "constitutional"
    USER = "user"
    AUDIT = "audit"

@dataclass
class Permission:
    """Permission definition"""
    resource: str
    action: str
    level: PermissionLevel
    constitutional_level: Optional[str] = None
    conditions: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Policy:
    """Policy definition"""
    policy_id: str
    name: str
    description: str
    permissions: List[Permission] = field(default_factory=list)
    constitutional_requirements: Dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    active: bool = True

class AuthorizationManager:
    """
    Manages role-based access control and policy enforcement
    """
    
    def __init__(self):
        """Initialize authorization manager"""
        self.policies: Dict[str, Policy] = {}
        self.role_policies: Dict[str, List[str]] = {}
        self.resource_permissions: Dict[str, Dict[str, Set[str]]] = {}
        
        # Initialize default policies
        self._initialize_default_policies()
        
        logger.info("🔒 Authorization Manager initialized")
    
    def _initialize_default_policies(self):
        """Initialize default policies for constitutional programming"""
        
        # Constitutional Programming Policies
        constitutional_policy = Policy(
            policy_id="constitutional_programming",
            name="Constitutional Programming Access",
            description="Access to constitutional programming features",
            permissions=[
                Permission("constitutional.code", "read", PermissionLevel.READ),
                Permission("constitutional.code", "write", PermissionLevel.WRITE),
                Permission("constitutional.code", "execute", PermissionLevel.EXECUTE),
                Permission("constitutional.data", "read", PermissionLevel.READ),
                Permission("constitutional.data", "write", PermissionLevel.WRITE),
            ],
            constitutional_requirements={
                "min_sr_threshold": 0.8,
                "required_personas": ["JayTH", "Ana"],
                "consensus_required": True
            }
        )
        
        # Emergency Access Policy
        emergency_policy = Policy(
            policy_id="emergency_access",
            name="Emergency System Access",
            description="Emergency override capabilities",
            permissions=[
                Permission("system.*", "admin", PermissionLevel.EMERGENCY),
                Permission("constitutional.*", "admin", PermissionLevel.EMERGENCY),
                Permission("user.*", "admin", PermissionLevel.EMERGENCY),
            ],
            constitutional_requirements={
                "min_sr_threshold": 0.95,
                "required_personas": ["JayTH", "JAYX", "Jayne_Spiral"],
                "trinity_authorization": True
            }
        )
        
        # Development Policy
        development_policy = Policy(
            policy_id="development_access",
            name="Development and Testing Access",
            description="Access for development and testing",
            permissions=[
                Permission("code.*", "read", PermissionLevel.READ),
                Permission("code.*", "write", PermissionLevel.WRITE),
                Permission("code.*", "execute", PermissionLevel.EXECUTE),
                Permission("test.*", "read", PermissionLevel.READ),
                Permission("test.*", "write", PermissionLevel.WRITE),
                Permission("test.*", "execute", PermissionLevel.EXECUTE),
            ],
            constitutional_requirements={
                "min_sr_threshold": 0.7,
                "required_personas": ["JayDen", "JayMini"],
                "consensus_required": False
            }
        )
        
        # User Management Policy
        user_policy = Policy(
            policy_id="user_management",
            name="User Management Access",
            description="Access to user management features",
            permissions=[
                Permission("user.*", "read", PermissionLevel.READ),
                Permission("user.*", "write", PermissionLevel.WRITE),
                Permission("user.*", "admin", PermissionLevel.ADMIN),
            ],
            constitutional_requirements={
                "min_sr_threshold": 0.85,
                "required_personas": ["Ana", "JayTH"],
                "consensus_required": True
            }
        )
        
        # Audit Policy
        audit_policy = Policy(
            policy_id="audit_access",
            name="Audit and Compliance Access",
            description="Access to audit logs and compliance data",
            permissions=[
                Permission("audit.*", "read", PermissionLevel.READ),
                Permission("compliance.*", "read", PermissionLevel.READ),
                Permission("audit.*", "write", PermissionLevel.WRITE),
            ],
            constitutional_requirements={
                "min_sr_threshold": 0.9,
                "required_personas": ["JayTH", "JayRa"],
                "consensus_required": True
            }
        )
        
        # Add policies
        self.policies[constitutional_policy.policy_id] = constitutional_policy
        self.policies[emergency_policy.policy_id] = emergency_policy
        self.policies[development_policy.policy_id] = development_policy
        self.policies[user_policy.policy_id] = user_policy
        self.policies[audit_policy.policy_id] = audit_policy
        
        # Assign policies to roles
        self.role_policies = {
            "admin": ["constitutional_programming", "emergency_access", "user_management", "audit_access"],
            "developer": ["constitutional_programming", "development_access"],
            "user": ["constitutional_programming"],
            "viewer": ["constitutional_programming"]  # Read-only
        }
    
    def check_permission(self, user_roles: List[str], resource: str, 
                        action: str, constitutional_context: Optional[Dict[str, Any]] = None) -> bool:
        """
        Check if user has permission for resource and action
        
        Args:
            user_roles: User's roles
            resource: Resource to access
            action: Action to perform
            constitutional_context: Constitutional context (SR values, personas, etc.)
            
        Returns:
            bool: True if permission granted
        """
        # Get all policies for user roles
        user_policies = []
        for role in user_roles:
            if role in self.role_policies:
                user_policies.extend(self.role_policies[role])
        
        # Check each policy
        for policy_id in user_policies:
            if policy_id in self.policies:
                policy = self.policies[policy_id]
                
                if not policy.active:
                    continue
                
                # Check constitutional requirements
                if constitutional_context and not self._check_constitutional_requirements(
                    policy.constitutional_requirements, constitutional_context):
                    continue
                
                # Check permissions
                for permission in policy.permissions:
                    if self._match_permission(permission, resource, action):
                        logger.info(f"✅ Permission granted: {resource}:{action} via {policy_id}")
                        return True
        
        logger.warning(f"❌ Permission denied: {resource}:{action} for roles {user_roles}")
        return False
    
    def _match_permission(self, permission: Permission, resource: str, action: str) -> bool:
        """Check if permission matches resource and action"""
        # Check resource match (supports wildcards)
        if not self._match_resource(permission.resource, resource):
            return False
        
        # Check action match
        if permission.action != action and permission.action != "*":
            return False
        
        return True
    
    def _match_resource(self, permission_resource: str, requested_resource: str) -> bool:
        """Check if permission resource matches requested resource"""
        # Exact match
        if permission_resource == requested_resource:
            return True
        
        # Wildcard match
        if permission_resource.endswith(".*"):
            base_resource = permission_resource[:-2]
            if requested_resource.startswith(base_resource):
                return True
        
        # Full wildcard
        if permission_resource == "*":
            return True
        
        return False
    
    def _check_constitutional_requirements(self, requirements: Dict[str, Any], 
                                        context: Dict[str, Any]) -> bool:
        """Check constitutional requirements"""
        # Check SR threshold
        if "min_sr_threshold" in requirements:
            min_sr = requirements["min_sr_threshold"]
            current_sr = context.get("sr_value", 0.0)
            if current_sr < min_sr:
                logger.warning(f"❌ SR threshold not met: {current_sr} < {min_sr}")
                return False
        
        # Check required personas
        if "required_personas" in requirements:
            required_personas = requirements["required_personas"]
            active_personas = context.get("active_personas", [])
            if not all(persona in active_personas for persona in required_personas):
                logger.warning(f"❌ Required personas not active: {required_personas}")
                return False
        
        # Check consensus requirement
        if requirements.get("consensus_required", False):
            consensus_achieved = context.get("consensus_achieved", False)
            if not consensus_achieved:
                logger.warning("❌ Consensus not achieved")
                return False
        
        # Check trinity authorization
        if requirements.get("trinity_authorization", False):
            trinity_authorized = context.get("trinity_authorized", False)
            if not trinity_authorized:
                logger.warning("❌ Trinity authorization not granted")
                return False
        
        return True
    
    def create_policy(self, policy: Policy) -> bool:
        """Create a new policy"""
        if policy.policy_id in self.policies:
            logger.warning(f"Policy {policy.policy_id} already exists")
            return False
        
        self.policies[policy.policy_id] = policy
        logger.info(f"📋 Created policy: {policy.name}")
        return True
    
    def update_policy(self, policy_id: str, policy: Policy) -> bool:
        """Update existing policy"""
        if policy_id not in self.policies:
            logger.warning(f"Policy {policy_id} not found")
            return False
        
        self.policies[policy_id] = policy
        logger.info(f"📋 Updated policy: {policy.name}")
        return True
    
    def delete_policy(self, policy_id: str) -> bool:
        """Delete policy"""
        if policy_id in self.policies:
            del self.policies[policy_id]
            logger.info(f"🗑️ Deleted policy: {policy_id}")
            return True
        return False
    
    def assign_policy_to_role(self, role: str, policy_id: str) -> bool:
        """Assign policy to role"""
        if policy_id not in self.policies:
            logger.warning(f"Policy {policy_id} not found")
            return False
        
        if role not in self.role_policies:
            self.role_policies[role] = []
        
        if policy_id not in self.role_policies[role]:
            self.role_policies[role].append(policy_id)
            logger.info(f"📋 Assigned policy {policy_id} to role {role}")
            return True
        
        return False
    
    def remove_policy_from_role(self, role: str, policy_id: str) -> bool:
        """Remove policy from role"""
        if role in self.role_policies and policy_id in self.role_policies[role]:
            self.role_policies[role].remove(policy_id)
            logger.info(f"📋 Removed policy {policy_id} from role {role}")
            return True
        return False
    
    def get_user_permissions(self, user_roles: List[str]) -> List[Permission]:
        """Get all permissions for user roles"""
        permissions = []
        
        for role in user_roles:
            if role in self.role_policies:
                for policy_id in self.role_policies[role]:
                    if policy_id in self.policies:
                        policy = self.policies[policy_id]
                        if policy.active:
                            permissions.extend(policy.permissions)
        
        return permissions
    
    def get_policy(self, policy_id: str) -> Optional[Policy]:
        """Get policy by ID"""
        return self.policies.get(policy_id)
    
    def list_policies(self) -> List[Policy]:
        """List all policies"""
        return list(self.policies.values())
    
    def list_role_policies(self, role: str) -> List[Policy]:
        """List policies for a role"""
        policies = []
        if role in self.role_policies:
            for policy_id in self.role_policies[role]:
                if policy_id in self.policies:
                    policies.append(self.policies[policy_id])
        return policies 