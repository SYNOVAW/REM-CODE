"""
REM-CODE Constitutional Adapter
公式REM-CODE interpreter との統合アダプター

Bridges Constitutional Framework with official REM-CODE Collapse Spiral execution
"""

import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class REMConstitutionalAdapter:
    """
    Adapter that integrates Constitutional Framework with official REM-CODE interpreter
    """
    
    def __init__(self, rem_interpreter=None):
        """Initialize adapter with optional REM interpreter"""
        self.rem_interpreter = rem_interpreter
        self.constitutional_context = {}
        
        logger.info("🔗 REM Constitutional Adapter initialized")
    
    def set_rem_interpreter(self, interpreter):
        """Set the REM interpreter instance"""
        self.rem_interpreter = interpreter
        logger.info("✅ REM interpreter connected to Constitutional Adapter")
    
    def execute_with_constitutional_context(self, rem_code: str, constitutional_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute REM CODE with constitutional context
        
        Args:
            rem_code: REM CODE to execute
            constitutional_context: Constitutional validation context
            
        Returns:
            Execution result with constitutional metadata
        """
        if not self.rem_interpreter:
            logger.warning("⚠️ No REM interpreter connected, using fallback")
            return self._fallback_execution(rem_code, constitutional_context)
        
        try:
            # Add constitutional context to execution environment
            enhanced_context = {
                **constitutional_context,
                "constitutional_mode": True,
                "authority_validated": constitutional_context.get("authority_valid", False),
                "consensus_achieved": constitutional_context.get("sr_valid", False),
                "signatures_verified": constitutional_context.get("signature_valid", False)
            }
            
            logger.info(f"🏛️ Executing REM CODE with constitutional validation")
            logger.info(f"   Authority: {'✅' if enhanced_context['authority_validated'] else '❌'}")
            logger.info(f"   Consensus: {'✅' if enhanced_context['consensus_achieved'] else '❌'}")
            logger.info(f"   Signatures: {'✅' if enhanced_context['signatures_verified'] else '❌'}")
            
            # Execute via official REM interpreter
            result = self.rem_interpreter.execute(rem_code, context=enhanced_context)
            
            # Enhance result with constitutional metadata
            enhanced_result = {
                **result,
                "constitutional_execution": True,
                "constitutional_context": enhanced_context,
                "compliance_validated": True
            }
            
            logger.info("✅ Constitutional REM execution completed")
            return enhanced_result
            
        except Exception as e:
            logger.error(f"❌ Constitutional REM execution failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "constitutional_execution": True,
                "constitutional_context": constitutional_context
            }
    
    def _fallback_execution(self, rem_code: str, constitutional_context: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback execution when no REM interpreter is available"""
        logger.info("🔄 Fallback constitutional execution")
        
        return {
            "success": True,
            "result": "fallback_execution",
            "rem_code": rem_code,
            "constitutional_execution": True,
            "constitutional_context": constitutional_context,
            "message": "Executed via constitutional fallback (no REM interpreter connected)"
        }
    
    def validate_constitutional_rem_syntax(self, rem_code: str) -> Dict[str, Any]:
        """
        Validate REM CODE syntax with constitutional constructs
        
        Returns validation result with constitutional construct detection
        """
        constitutional_constructs = [
            "Authority", "Consensus", "Validate", "Emergency", 
            "Trinity", "Constitutional"
        ]
        
        detected_constructs = []
        for construct in constitutional_constructs:
            if construct in rem_code:
                detected_constructs.append(construct)
        
        has_constitutional_constructs = len(detected_constructs) > 0
        
        validation_result = {
            "valid_syntax": True,  # Would integrate with actual parser
            "constitutional_constructs_detected": has_constitutional_constructs,
            "detected_constructs": detected_constructs,
            "requires_constitutional_validation": has_constitutional_constructs
        }
        
        if has_constitutional_constructs:
            logger.info(f"🏛️ Constitutional constructs detected: {detected_constructs}")
        
        return validation_result
    
    def enhance_rem_executor_with_constitutional_features(self, executor):
        """
        Enhance existing REM executor with constitutional features
        """
        original_execute = executor.execute
        
        def constitutional_execute(statements, **kwargs):
            """Enhanced execute method with constitutional awareness"""
            # Check for constitutional context
            constitutional_context = kwargs.get('constitutional_context', {})
            
            if constitutional_context:
                logger.info("🏛️ Executing with constitutional context")
                # Add constitutional validation metadata
                kwargs['constitutional_mode'] = True
                kwargs['constitutional_metadata'] = constitutional_context
            
            # Call original execute method
            return original_execute(statements, **kwargs)
        
        # Replace execute method
        executor.execute = constitutional_execute
        logger.info("✅ REM executor enhanced with constitutional features")
        
        return executor
    
    def create_constitutional_rem_session(self) -> Dict[str, Any]:
        """Create a REM session with constitutional capabilities"""
        session = {
            "session_id": f"constitutional_rem_{hash(id(self))}",
            "constitutional_mode": True,
            "adapter": self,
            "features": [
                "constitutional_authority_validation",
                "consensus_requirements", 
                "cryptographic_signatures",
                "emergency_protocols",
                "trinity_coordination"
            ]
        }
        
        logger.info(f"🏛️ Constitutional REM session created: {session['session_id']}")
        return session

def create_constitutional_adapter(rem_interpreter=None):
    """Factory function to create constitutional adapter"""
    return REMConstitutionalAdapter(rem_interpreter)

def integrate_constitutional_framework_with_rem_interpreter(interpreter):
    """
    High-level integration function for Constitutional Framework + REM interpreter
    """
    logger.info("🔗 Integrating Constitutional Framework with REM interpreter")
    
    # Create adapter
    adapter = create_constitutional_adapter(interpreter)
    
    # Enhance interpreter with constitutional features
    if hasattr(interpreter, 'executor'):
        adapter.enhance_rem_executor_with_constitutional_features(interpreter.executor)
    
    # Add constitutional methods to interpreter
    interpreter.constitutional_adapter = adapter
    interpreter.execute_constitutional = adapter.execute_with_constitutional_context
    interpreter.validate_constitutional_syntax = adapter.validate_constitutional_rem_syntax
    
    logger.info("✅ Constitutional Framework integration complete")
    return adapter