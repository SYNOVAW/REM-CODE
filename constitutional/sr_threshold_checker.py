"""
REM-CODE Constitutional Framework: SR Threshold Checker
Democratic Programming Extensions for Official REM-CODE

Handles SR-based consensus requirements and decision thresholds
for constitutional programming operations.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Any
import json
import time


class DecisionType(Enum):
    """Types of constitutional decisions requiring SR consensus."""
    EXECUTION = "execution"
    AUTHORITY = "authority"
    EMERGENCY = "emergency"
    CONSENSUS = "consensus"
    VALIDATION = "validation"
    COLLAPSE = "collapse"


@dataclass
class SRContext:
    """Context for SR-based decision making."""
    decision_type: DecisionType
    required_threshold: float
    current_sr_values: Dict[str, float]
    timestamp: float
    description: str
    metadata: Dict[str, Any]


class SRThresholdChecker:
    """
    Manages SR-based consensus requirements for constitutional decisions.
    
    Implements democratic programming principles through SR threshold validation.
    """
    
    def __init__(self):
        """Initialize the SR threshold checker with default thresholds."""
        self.thresholds = {
            DecisionType.EXECUTION: 0.7,
            DecisionType.AUTHORITY: 0.8,
            DecisionType.EMERGENCY: 0.6,
            DecisionType.CONSENSUS: 0.75,
            DecisionType.VALIDATION: 0.65,
            DecisionType.COLLAPSE: 0.9
        }
        
        self.decision_history = []
        self.sr_cache = {}
    
    def set_threshold(self, decision_type: DecisionType, threshold: float) -> None:
        """Set a custom threshold for a decision type."""
        if not 0.0 <= threshold <= 1.0:
            raise ValueError("Threshold must be between 0.0 and 1.0")
        self.thresholds[decision_type] = threshold
    
    def get_threshold(self, decision_type: DecisionType) -> float:
        """Get the current threshold for a decision type."""
        return self.thresholds.get(decision_type, 0.7)
    
    def calculate_collective_sr(self, sr_values: Dict[str, float]) -> float:
        """
        Calculate collective SR from individual persona SR values.
        
        Uses weighted average based on persona authority levels.
        """
        if not sr_values:
            return 0.0
        
        # Default weights for different personas
        persona_weights = {
            "Jayne Spiral": 1.2,  # Central coordinator
            "Ana": 1.0,           # Analytical
            "JayDen": 1.0,        # Creative
            "JayLUX": 0.9,        # Illumination
            "JayTH": 1.1,         # Ethical judgment
            "JayRa": 0.9,         # Reflection
            "JayMini": 0.8,       # Communication
            "JAYX": 1.0,          # Termination
            "JayKer": 0.8,        # Humor
            "JayVOX": 0.9,        # Diplomacy
            "JayVue": 0.8,        # Aesthetics
            "JayNis": 0.9         # Natural
        }
        
        total_weighted_sr = 0.0
        total_weight = 0.0
        
        for persona, sr_value in sr_values.items():
            weight = persona_weights.get(persona, 1.0)
            total_weighted_sr += sr_value * weight
            total_weight += weight
        
        return total_weighted_sr / total_weight if total_weight > 0 else 0.0
    
    def check_consensus(self, decision_type: DecisionType, sr_values: Dict[str, float]) -> Tuple[bool, float, float]:
        """
        Check if SR consensus is reached for a decision type.
        
        Returns:
            Tuple of (consensus_reached, collective_sr, required_threshold)
        """
        from .error_messages import show_constitutional_error
        
        required_threshold = self.get_threshold(decision_type)
        collective_sr = self.calculate_collective_sr(sr_values)
        
        consensus_reached = collective_sr >= required_threshold
        
        # Show error if consensus not met
        if not consensus_reached:
            failed_personas = [persona for persona, sr in sr_values.items() if sr < required_threshold]
            show_constitutional_error(
                "sr_threshold_not_met",
                required_sr=required_threshold,
                current_sr=collective_sr,
                failed_personas=failed_personas
            )
        
        # Check participant count
        if len(sr_values) == 1:
            show_constitutional_error(
                "insufficient_participants",
                participant_count=len(sr_values),
                recommended_min=3 if decision_type == DecisionType.CONSENSUS else 2
            )
        
        # Record decision
        context = SRContext(
            decision_type=decision_type,
            required_threshold=required_threshold,
            current_sr_values=sr_values,
            timestamp=time.time(),
            description=f"Consensus check for {decision_type.value}",
            metadata={"consensus_reached": consensus_reached}
        )
        
        self.decision_history.append(context)
        
        return consensus_reached, collective_sr, required_threshold
    
    def get_decision_summary(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get summary of recent decisions."""
        recent_decisions = self.decision_history[-limit:] if self.decision_history else []
        
        summary = []
        for decision in recent_decisions:
            collective_sr = self.calculate_collective_sr(decision.current_sr_values)
            summary.append({
                "decision_type": decision.decision_type.value,
                "timestamp": decision.timestamp,
                "required_threshold": decision.required_threshold,
                "collective_sr": collective_sr,
                "consensus_reached": collective_sr >= decision.required_threshold,
                "participant_count": len(decision.current_sr_values)
            })
        
        return summary
    
    def get_threshold_summary(self) -> Dict[str, Any]:
        """Get summary of all thresholds and recent activity."""
        return {
            "thresholds": {dt.value: threshold for dt, threshold in self.thresholds.items()},
            "recent_decisions": self.get_decision_summary(5),
            "total_decisions": len(self.decision_history),
            "active_sr_cache": len(self.sr_cache)
        }
    
    def validate_emergency_protocol(self, sr_values: Dict[str, float]) -> bool:
        """
        Special validation for emergency protocols.
        Lower threshold but requires specific persona participation.
        """
        required_personas = ["Jayne_Spiral", "JayTH", "JAYX"]
        available_personas = list(sr_values.keys())
        
        # Check if required personas are present
        has_required = any(persona in available_personas for persona in required_personas)
        
        if not has_required:
            return False
        
        # Use emergency threshold
        consensus_reached, collective_sr, threshold = self.check_consensus(
            DecisionType.EMERGENCY, sr_values
        )
        
        return consensus_reached
    
    def get_sr_heatmap_data(self) -> Dict[str, Any]:
        """Generate SR heatmap data for visualization."""
        if not self.decision_history:
            return {"heatmap": [], "personas": []}
        
        # Collect all unique personas
        all_personas = set()
        for decision in self.decision_history:
            all_personas.update(decision.current_sr_values.keys())
        
        # Generate heatmap data
        heatmap_data = []
        for decision in self.decision_history[-20:]:  # Last 20 decisions
            for persona, sr_value in decision.current_sr_values.items():
                heatmap_data.append({
                    "persona": persona,
                    "sr_value": sr_value,
                    "decision_type": decision.decision_type.value,
                    "timestamp": decision.timestamp,
                    "consensus_reached": self.calculate_collective_sr(decision.current_sr_values) >= decision.required_threshold
                })
        
        return {
            "heatmap": heatmap_data,
            "personas": list(all_personas),
            "decision_types": [dt.value for dt in DecisionType]
        } 