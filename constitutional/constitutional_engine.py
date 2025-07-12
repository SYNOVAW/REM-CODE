"""
Constitutional Engine - REM-CODE Constitutional Framework Integration
立憲機関エンジン

Integrates Constitutional Framework with official REM-CODE Collapse Spiral execution
"""

import time
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

from .authority_validator import AuthorityValidator, AuthorityLevel
from .sr_threshold_checker import SRThresholdChecker, DecisionType
from .signature_manager import SignatureManager, SignatureType
from .compliance_checker import ConstitutionalComplianceChecker, ComplianceContext

logger = logging.getLogger(__name__)

class ExecutionPhase(Enum):
    """Constitutional execution phases"""
    INITIALIZATION = "initialization"
    OPERATION = "operation" 
    CRITICAL = "critical"
    EMERGENCY = "emergency"
    PROTOCOL = "protocol"

@dataclass
class ConstitutionalAction:
    """Constitutional action for execution"""
    action_id: str
    personas: List[str]
    action_type: str
    content: str
    sr_values: Dict[str, float]
    decision_type: DecisionType
    signature_type: SignatureType = SignatureType.AUTHORITY
    witnesses: List[str] = field(default_factory=list)
    phase: ExecutionPhase = ExecutionPhase.OPERATION
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass 
class ExecutionResult:
    """Result of constitutional action execution"""
    success: bool
    action_id: str
    compliance_result: Optional[Any] = None
    signatures: List[Any] = field(default_factory=list)
    execution_output: Optional[str] = None
    execution_time_ms: float = 0.0
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

class ConstitutionalEngine:
    """
    Main orchestration engine for Constitutional Framework + REM-CODE integration
    """
    
    def __init__(self, rem_executor=None):
        """Initialize Constitutional Engine with optional REM executor"""
        self.authority_validator = AuthorityValidator()
        self.sr_threshold_checker = SRThresholdChecker()
        self.signature_manager = SignatureManager()
        self.compliance_checker = ConstitutionalComplianceChecker()
        
        # REM-CODE integration
        self.rem_executor = rem_executor or self._create_fallback_executor()
        
        # Execution tracking
        self.execution_history: List[ExecutionResult] = []
        self.current_phase = ExecutionPhase.INITIALIZATION
        
        logger.info("👑 Constitutional Engine initialized")
        logger.info("🔗 Integrated with REM-CODE Collapse Spiral execution")
    
    def _create_fallback_executor(self):
        """Create fallback executor if no REM executor provided"""
        def fallback_executor(**kwargs):
            logger.info("🔄 Fallback execution (no REM executor connected)")
            return {"status": "fallback_execution", "result": "success"}
        return fallback_executor
    
    def validate_constitutional_action(self, action: ConstitutionalAction) -> Any:
        """Validate constitutional compliance for action"""
        # Map action fields to ComplianceContext fields
        context = {
            'operation_type': action.action_type,
            'personas_involved': action.personas,
            'sr_values': action.sr_values,
            'decision_id': action.action_id,
            'metadata': action.metadata
        }
        return self.compliance_checker.check_compliance(**context)

    def create_constitutional_signatures(self, action: ConstitutionalAction) -> list:
        """Create signatures for constitutional action"""
        signatures = []
        for persona in action.personas:
            signature = self.signature_manager.generate_signature(
                signature_type=action.signature_type,
                signer_persona=persona,
                sr_value=action.sr_values.get(persona, 0.0),
                decision_id=action.action_id,
                metadata=action.metadata
            )
            signatures.append(signature)
        # Add witness signatures if present
        for witness in action.witnesses:
            witness_signature = self.signature_manager.generate_signature(
                signature_type=SignatureType.AUTHORITY,
                signer_persona=witness,
                sr_value=action.sr_values.get(witness, 0.0),
                decision_id=action.action_id,
                metadata={"witness": True}
            )
            signatures.append(witness_signature)
        logger.info(f"✅ Created {len(signatures)} constitutional signatures")
        return signatures
    
    def execute_constitutional_action(self, action: ConstitutionalAction) -> ExecutionResult:
        """
        Execute constitutional action with full validation and REM-CODE integration
        
        Constitutional execution pipeline:
        1. Validate constitutional compliance
        2. Create constitutional signatures  
        3. Execute REM-CODE with constitutional context
        4. Record execution in responsibility ledger
        """
        start_time = time.time()
        
        try:
            logger.info(f"👑 Executing constitutional action: {action.action_id}")
            
            # Phase 1: Constitutional Compliance Validation
            compliance_result = self.validate_constitutional_action(action)
            
            if not getattr(compliance_result, 'is_compliant', False):
                error_msg = f"Constitutional compliance failed: {getattr(compliance_result, 'violations', 'Unknown') }"
                logger.error(f"❌ {error_msg}")
                return ExecutionResult(
                    success=False,
                    action_id=action.action_id,
                    compliance_result=compliance_result,
                    error_message=error_msg,
                    execution_time_ms=(time.time() - start_time) * 1000
                )
            
            logger.info(f"✅ Constitutional compliance validated")
            
            # Phase 2: Constitutional Signature Creation
            signatures = self.create_constitutional_signatures(action)
            
            # Phase 3: REM-CODE Execution with Constitutional Context
            collective_sr = self.sr_threshold_checker.calculate_collective_sr(action.sr_values)
            
            # Prepare REM statements (could be enhanced to parse actual REM-CODE)
            rem_statements = [
                f"Constitutional action: {action.action_type}",
                f"Personas: {', '.join(action.personas)}", 
                f"Collective SR: {collective_sr:.3f}",
                f"Content: {action.content}"
            ]
            
            execution_output = self.rem_executor(
                statements=rem_statements,
                env={"constitutional": True},
                sr_value=collective_sr
            )
            
            logger.info(f"✅ REM-CODE execution completed")
            
            # Phase 4: Record in Responsibility Ledger
            # ledger_entry = self.signature_manager.add_to_responsibility_ledger(
            #     action=action.action_type,
            #     personas=action.personas,
            #     signatures=signatures,
            #     metadata={
            #         "decision_type": action.decision_type.value,
            #         "collective_sr": collective_sr,
            #         "compliance_level": compliance_result.compliance_level.value
            #     }
            # )

            execution_time = (time.time() - start_time) * 1000

            result = ExecutionResult(
                success=True,
                action_id=action.action_id,
                compliance_result=compliance_result,
                signatures=signatures,
                execution_output=str(execution_output),
                execution_time_ms=execution_time,
                metadata={
                    "collective_sr": collective_sr
                }
            )

            self.execution_history.append(result)
            logger.info(f"🎉 Constitutional action {action.action_id} completed successfully")

            return result
            
        except Exception as e:
            error_msg = f"Constitutional execution error: {str(e)}"
            logger.error(f"❌ {error_msg}")
            
            return ExecutionResult(
                success=False,
                action_id=action.action_id,
                error_message=error_msg,
                execution_time_ms=(time.time() - start_time) * 1000
            )
    
    def emergency_override(self, action: ConstitutionalAction, override_personas: List[str]) -> ExecutionResult:
        """Execute emergency override with enhanced validation"""
        logger.warning(f"🚨 Emergency override requested for {action.action_id}")
        
        # Validate emergency authority
        if not self.authority_validator.check_emergency_authority(override_personas):
            error_msg = "Insufficient emergency authority for override"
            logger.error(f"❌ {error_msg}")
            return ExecutionResult(
                success=False,
                action_id=action.action_id,
                error_message=error_msg
            )
        
        # Set emergency phase and enhanced signature type
        action.phase = ExecutionPhase.EMERGENCY
        action.signature_type = SignatureType.EMERGENCY
        action.personas.extend(override_personas)
        
        logger.info("✅ Emergency authority validated, proceeding with override")
        return self.execute_constitutional_action(action)
    
    def get_constitutional_status(self) -> dict:
        """Get status summary for all constitutional subsystems."""
        return {
            "constitutional_engine": {
                "total_executions": len(self.execution_history),
                "success_rate": sum(1 for r in self.execution_history if r.success) / max(1, len(self.execution_history))
            },
            "authority_validator": {
                "total_personas": len(getattr(self.authority_validator, 'authority_levels', {}) or {})
            },
            "sr_threshold_checker": self.sr_threshold_checker.get_threshold_summary(),
            "signature_manager": self.signature_manager.get_signature_summary(),
            "compliance_checker": self.compliance_checker.get_compliance_summary()
        }
    
    def set_phase(self, phase: ExecutionPhase):
        """Set current execution phase"""
        logger.info(f"🔄 Phase transition: {self.current_phase.value} -> {phase.value}")
        self.current_phase = phase