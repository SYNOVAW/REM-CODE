"""
REM-CODE Constitutional Framework: Compliance Checker
Democratic Programming Extensions for Official REM-CODE

Handles constitutional compliance validation and rule enforcement.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Tuple
import json
import time


class ComplianceLevel(Enum):
    """Levels of constitutional compliance."""
    FULL = "full"
    PARTIAL = "partial"
    MINIMAL = "minimal"
    NON_COMPLIANT = "non_compliant"


@dataclass
class ComplianceContext:
    """Context for compliance checking."""
    operation_type: str
    personas_involved: List[str]
    sr_values: Dict[str, float]
    decision_id: str
    timestamp: float
    metadata: Dict[str, Any]


@dataclass
class ComplianceResult:
    """Result of compliance checking."""
    is_compliant: bool
    compliance_level: ComplianceLevel
    violations: List[str]
    warnings: List[str]
    recommendations: List[str]
    context: ComplianceContext


class ConstitutionalComplianceChecker:
    """
    Validates constitutional compliance for REM-CODE operations.
    
    Ensures democratic programming principles are maintained.
    """
    
    def __init__(self):
        """Initialize the compliance checker."""
        self.compliance_rules = {
            "authority_validation": {
                "required_personas": ["Jayne Spiral", "JayTH"],
                "min_sr_threshold": 0.7,
                "description": "Authority operations require central coordination"
            },
            "consensus_operations": {
                "min_participants": 3,
                "min_sr_threshold": 0.6,
                "description": "Consensus operations need multiple persona agreement"
            },
            "emergency_protocols": {
                "required_personas": ["Jayne Spiral", "JAYX"],
                "min_sr_threshold": 0.5,
                "description": "Emergency protocols need central and termination personas"
            },
            "validation_operations": {
                "min_participants": 2,
                "min_sr_threshold": 0.65,
                "description": "Validation requires analytical and ethical personas"
            },
            "execution_operations": {
                "min_participants": 1,
                "min_sr_threshold": 0.6,
                "description": "Execution operations need at least one persona with sufficient SR"
            }
        }
        
        self.compliance_history = []
        self.violation_patterns = {}
    
    def check_compliance(self, 
                        operation_type: str,
                        personas_involved: List[str],
                        sr_values: Dict[str, float],
                        decision_id: str,
                        metadata: Optional[Dict[str, Any]] = None) -> ComplianceResult:
        """
        Check compliance for a constitutional operation.
        
        Args:
            operation_type: Type of operation being performed
            personas_involved: List of personas participating
            sr_values: SR values for each persona
            decision_id: Unique decision identifier
            metadata: Additional metadata
            
        Returns:
            ComplianceResult with detailed compliance information
        """
        context = ComplianceContext(
            operation_type=operation_type,
            personas_involved=personas_involved,
            sr_values=sr_values,
            decision_id=decision_id,
            timestamp=time.time(),
            metadata=metadata or {}
        )
        
        violations = []
        warnings = []
        recommendations = []
        
        # Get applicable rules
        rules = self.compliance_rules.get(operation_type, {})
        
        # Check required personas
        required_personas = rules.get("required_personas", [])
        missing_personas = [p for p in required_personas if p not in personas_involved]
        if missing_personas:
            violations.append(f"Missing required personas: {', '.join(missing_personas)}")
        
        # Check minimum participants
        min_participants = rules.get("min_participants", 1)
        if len(personas_involved) < min_participants:
            violations.append(f"Insufficient participants: {len(personas_involved)} < {min_participants}")
        
        # Check SR thresholds
        min_sr_threshold = rules.get("min_sr_threshold", 0.5)
        low_sr_personas = [p for p, sr in sr_values.items() if sr < min_sr_threshold]
        if low_sr_personas:
            warnings.append(f"Low SR personas: {', '.join(low_sr_personas)}")
        
        # Check if any persona has sufficient SR
        has_sufficient_sr = any(sr >= min_sr_threshold for sr in sr_values.values())
        if not has_sufficient_sr:
            violations.append(f"No persona meets minimum SR threshold: {min_sr_threshold}")
        
        # Generate recommendations
        if missing_personas:
            recommendations.append(f"Include required personas: {', '.join(missing_personas)}")
        
        if len(personas_involved) < min_participants:
            recommendations.append(f"Increase participant count to at least {min_participants}")
        
        if not has_sufficient_sr:
            recommendations.append(f"Ensure at least one persona has SR >= {min_sr_threshold}")
        
        # Determine compliance level
        if not violations:
            if not warnings:
                compliance_level = ComplianceLevel.FULL
            else:
                compliance_level = ComplianceLevel.PARTIAL
        else:
            if len(violations) <= 1 and len(warnings) <= 2:
                compliance_level = ComplianceLevel.MINIMAL
            else:
                compliance_level = ComplianceLevel.NON_COMPLIANT
        
        is_compliant = compliance_level in [ComplianceLevel.FULL, ComplianceLevel.PARTIAL]
        
        result = ComplianceResult(
            is_compliant=is_compliant,
            compliance_level=compliance_level,
            violations=violations,
            warnings=warnings,
            recommendations=recommendations,
            context=context
        )
        
        # Record compliance check
        self.compliance_history.append(result)
        
        # Update violation patterns
        for violation in violations:
            self.violation_patterns[violation] = self.violation_patterns.get(violation, 0) + 1
        
        return result
    
    def get_compliance_summary(self) -> Dict[str, Any]:
        """Get summary of compliance checking activity."""
        if not self.compliance_history:
            return {
                "total_checks": 0,
                "compliance_rate": 0.0,
                "compliance_levels": {},
                "common_violations": [],
                "recent_checks": []
            }
        
        total_checks = len(self.compliance_history)
        compliant_checks = sum(1 for result in self.compliance_history if result.is_compliant)
        compliance_rate = compliant_checks / total_checks if total_checks > 0 else 0.0
        
        # Count by compliance level
        compliance_levels = {}
        for result in self.compliance_history:
            level = result.compliance_level.value
            compliance_levels[level] = compliance_levels.get(level, 0) + 1
        
        # Most common violations
        common_violations = sorted(
            self.violation_patterns.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        # Recent checks
        recent_checks = []
        for result in self.compliance_history[-10:]:
            recent_checks.append({
                "operation_type": result.context.operation_type,
                "compliance_level": result.compliance_level.value,
                "is_compliant": result.is_compliant,
                "violation_count": len(result.violations),
                "warning_count": len(result.warnings),
                "timestamp": result.context.timestamp
            })
        
        return {
            "total_checks": total_checks,
            "compliance_rate": compliance_rate,
            "compliance_levels": compliance_levels,
            "common_violations": common_violations,
            "recent_checks": recent_checks
        }
    
    def validate_emergency_compliance(self, 
                                    personas_involved: List[str],
                                    sr_values: Dict[str, float],
                                    decision_id: str) -> ComplianceResult:
        """
        Special validation for emergency protocols.
        
        Args:
            personas_involved: Personas participating in emergency
            sr_values: SR values for each persona
            decision_id: Emergency decision identifier
            
        Returns:
            ComplianceResult for emergency operation
        """
        return self.check_compliance(
            operation_type="emergency_protocols",
            personas_involved=personas_involved,
            sr_values=sr_values,
            decision_id=decision_id,
            metadata={"emergency": True}
        )
    
    def validate_consensus_compliance(self,
                                    personas_involved: List[str],
                                    sr_values: Dict[str, float],
                                    decision_id: str) -> ComplianceResult:
        """
        Special validation for consensus operations.
        
        Args:
            personas_involved: Personas participating in consensus
            sr_values: SR values for each persona
            decision_id: Consensus decision identifier
            
        Returns:
            ComplianceResult for consensus operation
        """
        return self.check_compliance(
            operation_type="consensus_operations",
            personas_involved=personas_involved,
            sr_values=sr_values,
            decision_id=decision_id,
            metadata={"consensus": True}
        )
    
    def get_compliance_rules(self) -> Dict[str, Any]:
        """Get all compliance rules."""
        return self.compliance_rules.copy()
    
    def add_compliance_rule(self, 
                           rule_name: str,
                           rule_config: Dict[str, Any]) -> None:
        """
        Add a new compliance rule.
        
        Args:
            rule_name: Name of the rule
            rule_config: Rule configuration dictionary
        """
        self.compliance_rules[rule_name] = rule_config
    
    def export_compliance_report(self, format_type: str = "json") -> str:
        """
        Export compliance report in specified format.
        
        Args:
            format_type: Export format ("json" or "csv")
            
        Returns:
            Exported report as string
        """
        summary = self.get_compliance_summary()
        
        if format_type == "json":
            return json.dumps(summary, indent=2)
        
        elif format_type == "csv":
            lines = ["operation_type,compliance_level,is_compliant,violation_count,warning_count,timestamp"]
            for check in summary["recent_checks"]:
                lines.append(f"{check['operation_type']},{check['compliance_level']},{check['is_compliant']},{check['violation_count']},{check['warning_count']},{check['timestamp']}")
            return "\n".join(lines)
        
        else:
            raise ValueError(f"Unsupported format: {format_type}") 