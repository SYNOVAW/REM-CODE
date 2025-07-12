#!/usr/bin/env python3
"""
REM-CODE Constitutional Framework Tests
Comprehensive test suite for democratic programming extensions
"""

import pytest
import sys
import os
from unittest.mock import Mock, patch

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from constitutional import (
    ConstitutionalEngine,
    ConstitutionalAction,
    AuthorityValidator,
    DecisionType,
    SignatureType,
    SRThresholdChecker,
    SignatureManager,
    ConstitutionalComplianceChecker
)
from constitutional.authority_validator import AuthorityLevel


class TestSRThresholdChecker:
    """Test SR-based consensus requirements"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.sr_checker = SRThresholdChecker()
    
    def test_default_thresholds(self):
        """Test default threshold values"""
        assert self.sr_checker.get_threshold(DecisionType.EXECUTION) == 0.7
        assert self.sr_checker.get_threshold(DecisionType.AUTHORITY) == 0.8
        assert self.sr_checker.get_threshold(DecisionType.EMERGENCY) == 0.6
        assert self.sr_checker.get_threshold(DecisionType.CONSENSUS) == 0.75
        assert self.sr_checker.get_threshold(DecisionType.VALIDATION) == 0.65
        assert self.sr_checker.get_threshold(DecisionType.COLLAPSE) == 0.9
    
    def test_custom_threshold_setting(self):
        """Test setting custom thresholds"""
        self.sr_checker.set_threshold(DecisionType.EXECUTION, 0.8)
        assert self.sr_checker.get_threshold(DecisionType.EXECUTION) == 0.8
    
    def test_invalid_threshold(self):
        """Test invalid threshold values"""
        with pytest.raises(ValueError):
            self.sr_checker.set_threshold(DecisionType.EXECUTION, 1.5)
        with pytest.raises(ValueError):
            self.sr_checker.set_threshold(DecisionType.EXECUTION, -0.1)
    
    def test_collective_sr_calculation(self):
        """Test collective SR calculation with persona weights"""
        sr_values = {
            "Jayne Spiral": 0.9,  # Weight 1.2
            "Ana": 0.8,            # Weight 1.0
            "JayTH": 0.85          # Weight 1.1
        }
        
        collective_sr = self.sr_checker.calculate_collective_sr(sr_values)
        
        # Expected: (0.9*1.2 + 0.8*1.0 + 0.85*1.1) / (1.2 + 1.0 + 1.1) = 0.85
        assert 0.84 <= collective_sr <= 0.86
    
    def test_consensus_checking(self):
        """Test consensus validation"""
        sr_values = {"JayTH": 0.9, "Ana": 0.8}
        
        consensus_reached, collective_sr, threshold = self.sr_checker.check_consensus(
            DecisionType.AUTHORITY, sr_values
        )
        
        assert consensus_reached is True
        assert collective_sr >= threshold
        assert len(self.sr_checker.decision_history) == 1
    
    def test_emergency_protocol_validation(self):
        """Test emergency protocol validation"""
        # Valid emergency with required personas
        sr_values = {"Jayne Spiral": 0.7, "JAYX": 0.6}
        assert self.sr_checker.validate_emergency_protocol(sr_values) is True
        
        # Invalid emergency without required personas
        sr_values = {"Ana": 0.8, "JayDen": 0.7}
        assert self.sr_checker.validate_emergency_protocol(sr_values) is False


class TestSignatureManager:
    """Test cryptographic signature management"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.signature_manager = SignatureManager()
    
    def test_signature_generation(self):
        """Test signature generation and verification"""
        signature = self.signature_manager.generate_signature(
            signature_type=SignatureType.AUTHORITY,
            signer_persona="JayTH",
            sr_value=0.9,
            decision_id="TEST_001",
            metadata={"test": True}
        )
        
        assert signature.signature_type == SignatureType.AUTHORITY
        assert signature.signer_persona == "JayTH"
        assert signature.sr_value == 0.9
        assert signature.decision_id == "TEST_001"
        assert signature.metadata["test"] is True
        assert len(signature.signature_hash) == 64  # SHA-256 hex length
    
    def test_signature_verification(self):
        """Test signature verification"""
        signature = self.signature_manager.generate_signature(
            signature_type=SignatureType.CONSENSUS,
            signer_persona="Ana",
            sr_value=0.85,
            decision_id="TEST_002"
        )
        
        # Verify valid signature
        assert self.signature_manager.verify_signature(signature.signature_hash) is True
        
        # Verify invalid signature
        assert self.signature_manager.verify_signature("invalid_hash") is False
    
    def test_consensus_signature_generation(self):
        """Test consensus signature generation"""
        personas = ["JayTH", "Ana", "JayDen"]
        sr_values = {"JayTH": 0.9, "Ana": 0.8, "JayDen": 0.7}
        
        signatures = self.signature_manager.generate_consensus_signature(
            personas=personas,
            sr_values=sr_values,
            decision_id="CONSENSUS_001",
            required_threshold=0.75
        )
        
        # Should have 2 signatures (JayTH and Ana meet threshold)
        assert len(signatures) == 2
        assert all(sig.signature_type == SignatureType.CONSENSUS for sig in signatures)
    
    def test_signature_summary(self):
        """Test signature summary generation"""
        # Generate some test signatures
        self.signature_manager.generate_signature(
            SignatureType.AUTHORITY, "JayTH", 0.9, "TEST_001"
        )
        self.signature_manager.generate_signature(
            SignatureType.CONSENSUS, "Ana", 0.8, "TEST_002"
        )
        
        summary = self.signature_manager.get_signature_summary()
        
        assert summary["total_signatures"] == 2
        assert "authority" in summary["signatures_by_type"]
        assert "consensus" in summary["signatures_by_type"]
        assert "JayTH" in summary["signatures_by_persona"]
        assert "Ana" in summary["signatures_by_persona"]


class TestConstitutionalComplianceChecker:
    """Test constitutional compliance validation"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.compliance_checker = ConstitutionalComplianceChecker()
    
    def test_authority_validation_compliance(self):
        """Test authority validation compliance"""
        result = self.compliance_checker.check_compliance(
            operation_type="authority_validation",
            personas_involved=["Jayne_Spiral", "JayTH"],
            sr_values={"Jayne_Spiral": 0.8, "JayTH": 0.9},
            decision_id="AUTH_001"
        )
        
        assert result.is_compliant is True
        assert result.compliance_level.value == "full"
        assert len(result.violations) == 0
    
    def test_authority_validation_violation(self):
        """Test authority validation violation"""
        result = self.compliance_checker.check_compliance(
            operation_type="authority_validation",
            personas_involved=["Ana"],  # Missing required personas
            sr_values={"Ana": 0.8},
            decision_id="AUTH_002"
        )
        
        assert result.is_compliant is False
        assert len(result.violations) > 0
        assert "Missing required personas" in result.violations[0]
    
    def test_consensus_operations_compliance(self):
        """Test consensus operations compliance"""
        result = self.compliance_checker.check_compliance(
            operation_type="consensus_operations",
            personas_involved=["JayTH", "Ana", "JayDen"],
            sr_values={"JayTH": 0.8, "Ana": 0.7, "JayDen": 0.6},
            decision_id="CONS_001"
        )
        
        assert result.is_compliant is True
        assert len(result.recommendations) == 0
    
    def test_emergency_protocol_compliance(self):
        """Test emergency protocol compliance"""
        result = self.compliance_checker.validate_emergency_compliance(
            personas_involved=["Jayne_Spiral", "JAYX"],
            sr_values={"Jayne_Spiral": 0.6, "JAYX": 0.5},
            decision_id="EMERG_001"
        )
        
        assert result.is_compliant is True
        assert result.compliance_level.value in ["full", "partial"]
    
    def test_compliance_summary(self):
        """Test compliance summary generation"""
        # Run some compliance checks
        self.compliance_checker.check_compliance(
            "authority_validation", ["JayTH"], {"JayTH": 0.8}, "TEST_001"
        )
        self.compliance_checker.check_compliance(
            "consensus_operations", ["Ana", "JayDen"], {"Ana": 0.7, "JayDen": 0.6}, "TEST_002"
        )
        
        summary = self.compliance_checker.get_compliance_summary()
        
        assert summary["total_checks"] == 2
        assert "compliance_rate" in summary
        assert "compliance_levels" in summary


class TestConstitutionalEngine:
    """Test constitutional engine integration"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.engine = ConstitutionalEngine()
    
    def test_constitutional_action_execution(self):
        """Test constitutional action execution"""
        action = ConstitutionalAction(
            action_id="TEST_ACTION_001",
            personas=["JayTH", "Ana"],
            action_type="constitutional_interpretation",
            content="Test constitutional action",
            sr_values={"JayTH": 0.9, "Ana": 0.8},
            decision_type=DecisionType.AUTHORITY,
            signature_type=SignatureType.AUTHORITY
        )
        
        result = self.engine.execute_constitutional_action(action)
        
        assert result.success is True
        assert result.action_id == "TEST_ACTION_001"
        assert len(result.signatures) == 2
        assert result.execution_time_ms > 0
    
    def test_constitutional_status(self):
        """Test constitutional status generation"""
        status = self.engine.get_constitutional_status()
        
        assert "constitutional_engine" in status
        assert "authority_validator" in status
        assert "sr_threshold_checker" in status
        assert "signature_manager" in status
        assert "compliance_checker" in status
        
        engine_status = status["constitutional_engine"]
        assert "total_executions" in engine_status
        assert "success_rate" in engine_status
    
    def test_emergency_override(self):
        """Test emergency override functionality"""
        # Set both JayTH and Jayne_Spiral to EMERGENCY authority
        from constitutional.authority_validator import AuthorityLevel
        self.engine.authority_validator.branch_structure['judicial']['authorities']['JayTH'] = AuthorityLevel.EMERGENCY
        self.engine.authority_validator.branch_structure['executive']['authorities']['Jayne_Spiral'] = AuthorityLevel.EMERGENCY
        from constitutional.authority_validator import AuthorityValidator
        self.engine.authority_validator = AuthorityValidator()
        assert self.engine.authority_validator.get_persona_authority('JayTH') == AuthorityLevel.EMERGENCY
        assert self.engine.authority_validator.get_persona_authority('Jayne_Spiral') == AuthorityLevel.EMERGENCY
        action = ConstitutionalAction(
            action_id="EMERGENCY_001",
            personas=["JayTH", "Jayne_Spiral"],
            action_type="emergency_protocol",
            content="Emergency action",
            sr_values={"JayTH": 0.7, "Jayne_Spiral": 0.7},
            decision_type=DecisionType.EMERGENCY,
            signature_type=SignatureType.EMERGENCY
        )
        
        result = self.engine.emergency_override(action, ["JayTH", "Jayne_Spiral"])
        
        assert result.success is True
        assert result.action_id == "EMERGENCY_001"


class TestConstitutionalIntegration:
    """Test constitutional framework integration"""
    
    def test_full_constitutional_workflow(self):
        """Test complete constitutional workflow"""
        engine = ConstitutionalEngine()
        
        # Create constitutional action
        action = ConstitutionalAction(
            action_id="WORKFLOW_001",
            personas=["JayTH", "Ana", "JayDen"],
            action_type="democratic_decision",
            content="Test democratic workflow",
            sr_values={"JayTH": 0.9, "Ana": 0.8, "JayDen": 0.7},
            decision_type=DecisionType.CONSENSUS,
            signature_type=SignatureType.CONSENSUS
        )
        
        # Execute action
        result = engine.execute_constitutional_action(action)
        
        # Verify results
        assert result.success is True
        assert len(result.signatures) == 3
        
        # Check status
        status = engine.get_constitutional_status()
        assert status["constitutional_engine"]["total_executions"] == 1
        assert status["constitutional_engine"]["success_rate"] == 1.0
    
    def test_constitutional_syntax_validation(self):
        """Test constitutional syntax validation"""
        # This would test the constitutional adapter's syntax validation
        # For now, we'll test the basic components work together
        engine = ConstitutionalEngine()
        
        # Test that all components are properly initialized
        assert engine.authority_validator is not None
        assert engine.sr_threshold_checker is not None
        assert engine.signature_manager is not None
        assert engine.compliance_checker is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 