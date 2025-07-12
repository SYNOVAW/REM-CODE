"""
REM-CODE Constitutional Framework: Signature Manager
Democratic Programming Extensions for Official REM-CODE

Handles cryptographic signatures and accountability for constitutional operations.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
import hashlib
import json
import time
import base64


class SignatureType(Enum):
    """Types of constitutional signatures."""
    AUTHORITY = "authority"
    CONSENSUS = "consensus"
    EMERGENCY = "emergency"
    VALIDATION = "validation"
    EXECUTION = "execution"


@dataclass
class ConstitutionalSignature:
    """Represents a constitutional signature with metadata."""
    signature_type: SignatureType
    signer_persona: str
    sr_value: float
    timestamp: float
    signature_hash: str
    metadata: Dict[str, Any]
    decision_id: str


class SignatureManager:
    """
    Manages cryptographic signatures for constitutional operations.
    
    Provides accountability and non-repudiation for democratic programming decisions.
    """
    
    def __init__(self):
        """Initialize the signature manager."""
        self.signatures = []
        self.signature_cache = {}
        self.verification_history = []
    
    def generate_signature(self, 
                          signature_type: SignatureType,
                          signer_persona: str,
                          sr_value: float,
                          decision_id: str,
                          metadata: Optional[Dict[str, Any]] = None,
                          action_name: str = "",
                          reasoning: str = "") -> ConstitutionalSignature:
        """
        Generate a constitutional signature for a decision.
        
        Args:
            signature_type: Type of signature
            signer_persona: Persona making the signature
            sr_value: SR value at time of signing
            decision_id: Unique identifier for the decision
            metadata: Additional metadata
            action_name: Name of the action being signed
            reasoning: Reasoning for the signature
            
        Returns:
            ConstitutionalSignature object
        """
        from .error_messages import show_constitutional_error
        
        # Validate signature requirements
        if not action_name:
            show_constitutional_error(
                "missing_signature",
                action=decision_id or "unnamed_action",
                persona=signer_persona
            )
            
        if reasoning and len(reasoning.strip()) < 10:
            show_constitutional_error(
                "insufficient_reasoning",
                reasoning=reasoning
            )
        
        timestamp = time.time()
        
        # Create signature data
        signature_data = {
            "type": signature_type.value,
            "persona": signer_persona,
            "sr_value": sr_value,
            "timestamp": timestamp,
            "decision_id": decision_id,
            "action_name": action_name,
            "reasoning": reasoning,
            "metadata": {**(metadata or {}), "action_name": action_name, "reasoning": reasoning}
        }
        
        # Generate hash
        data_string = json.dumps(signature_data, sort_keys=True)
        signature_hash = hashlib.sha256(data_string.encode()).hexdigest()
        
        # Create signature object
        signature = ConstitutionalSignature(
            signature_type=signature_type,
            signer_persona=signer_persona,
            sr_value=sr_value,
            timestamp=timestamp,
            signature_hash=signature_hash,
            metadata={
                **(metadata or {}),
                "action_name": action_name,
                "reasoning": reasoning
            },
            decision_id=decision_id
        )
        
        # Store signature
        self.signatures.append(signature)
        self.signature_cache[signature_hash] = signature
        
        return signature
    
    def verify_signature(self, signature_hash: str) -> bool:
        """
        Verify a signature hash.
        
        Args:
            signature_hash: Hash to verify
            
        Returns:
            True if signature is valid and found
        """
        if signature_hash in self.signature_cache:
            signature = self.signature_cache[signature_hash]
            
            # Recreate signature data (must match generation exactly)
            signature_data = {
                "type": signature.signature_type.value,
                "persona": signature.signer_persona,
                "sr_value": signature.sr_value,
                "timestamp": signature.timestamp,
                "decision_id": signature.decision_id,
                "action_name": signature.metadata.get("action_name", ""),
                "reasoning": signature.metadata.get("reasoning", ""),
                "metadata": signature.metadata
            }
            
            # Verify hash
            data_string = json.dumps(signature_data, sort_keys=True)
            expected_hash = hashlib.sha256(data_string.encode()).hexdigest()
            
            is_valid = expected_hash == signature_hash
            
            # Record verification
            self.verification_history.append({
                "signature_hash": signature_hash,
                "timestamp": time.time(),
                "valid": is_valid,
                "signature_type": signature.signature_type.value,
                "signer_persona": signature.signer_persona
            })
            
            return is_valid
        
        return False
    
    def get_signatures_by_decision(self, decision_id: str) -> List[ConstitutionalSignature]:
        """Get all signatures for a specific decision."""
        return [sig for sig in self.signatures if sig.decision_id == decision_id]
    
    def get_signatures_by_persona(self, persona: str) -> List[ConstitutionalSignature]:
        """Get all signatures by a specific persona."""
        return [sig for sig in self.signatures if sig.signer_persona == persona]
    
    def get_signatures_by_type(self, signature_type: SignatureType) -> List[ConstitutionalSignature]:
        """Get all signatures of a specific type."""
        return [sig for sig in self.signatures if sig.signature_type == signature_type]
    
    def get_signature_summary(self) -> Dict[str, Any]:
        """Get summary of all signatures."""
        if not self.signatures:
            return {
                "total_signatures": 0,
                "signatures_by_type": {},
                "signatures_by_persona": {},
                "recent_signatures": []
            }
        
        # Count by type
        signatures_by_type = {}
        for sig_type in SignatureType:
            signatures_by_type[sig_type.value] = len(self.get_signatures_by_type(sig_type))
        
        # Count by persona
        signatures_by_persona = {}
        for sig in self.signatures:
            persona = sig.signer_persona
            signatures_by_persona[persona] = signatures_by_persona.get(persona, 0) + 1
        
        # Recent signatures
        recent_signatures = sorted(self.signatures, key=lambda x: x.timestamp, reverse=True)[:10]
        recent_data = []
        for sig in recent_signatures:
            recent_data.append({
                "type": sig.signature_type.value,
                "persona": sig.signer_persona,
                "sr_value": sig.sr_value,
                "timestamp": sig.timestamp,
                "decision_id": sig.decision_id
            })
        
        return {
            "total_signatures": len(self.signatures),
            "signatures_by_type": signatures_by_type,
            "signatures_by_persona": signatures_by_persona,
            "recent_signatures": recent_data,
            "verification_count": len(self.verification_history)
        }
    
    def generate_consensus_signature(self, 
                                   personas: List[str],
                                   sr_values: Dict[str, float],
                                   decision_id: str,
                                   required_threshold: float) -> List[ConstitutionalSignature]:
        """
        Generate consensus signatures from multiple personas.
        
        Args:
            personas: List of personas participating
            sr_values: SR values for each persona
            decision_id: Decision identifier
            required_threshold: Required SR threshold for consensus
            
        Returns:
            List of valid signatures
        """
        signatures = []
        
        for persona in personas:
            if persona in sr_values:
                sr_value = sr_values[persona]
                
                # Only sign if SR is above threshold
                if sr_value >= required_threshold:
                    signature = self.generate_signature(
                        signature_type=SignatureType.CONSENSUS,
                        signer_persona=persona,
                        sr_value=sr_value,
                        decision_id=decision_id,
                        metadata={"consensus_threshold": required_threshold}
                    )
                    signatures.append(signature)
        
        return signatures
    
    def export_signatures(self, format_type: str = "json") -> str:
        """
        Export signatures in specified format.
        
        Args:
            format_type: Export format ("json" or "csv")
            
        Returns:
            Exported data as string
        """
        if format_type == "json":
            data = []
            for sig in self.signatures:
                data.append({
                    "type": sig.signature_type.value,
                    "persona": sig.signer_persona,
                    "sr_value": sig.sr_value,
                    "timestamp": sig.timestamp,
                    "signature_hash": sig.signature_hash,
                    "decision_id": sig.decision_id,
                    "metadata": sig.metadata
                })
            return json.dumps(data, indent=2)
        
        elif format_type == "csv":
            lines = ["type,persona,sr_value,timestamp,signature_hash,decision_id"]
            for sig in self.signatures:
                lines.append(f"{sig.signature_type.value},{sig.signer_persona},{sig.sr_value},{sig.timestamp},{sig.signature_hash},{sig.decision_id}")
            return "\n".join(lines)
        
        else:
            raise ValueError(f"Unsupported format: {format_type}")
    
    def get_verification_stats(self) -> Dict[str, Any]:
        """Get verification statistics."""
        if not self.verification_history:
            return {"total_verifications": 0, "successful_verifications": 0, "success_rate": 0.0}
        
        total = len(self.verification_history)
        successful = sum(1 for v in self.verification_history if v["valid"])
        success_rate = successful / total if total > 0 else 0.0
        
        return {
            "total_verifications": total,
            "successful_verifications": successful,
            "success_rate": success_rate,
            "recent_verifications": self.verification_history[-10:]
        } 