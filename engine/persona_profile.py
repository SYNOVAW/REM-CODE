"""Persona profile dataclass shared by REM components."""

from dataclasses import dataclass, field
from typing import Dict, Optional, Any

from .sr_engine import compute_sr_from_dict, DEFAULT_WEIGHTS


@dataclass
class PersonaProfile:
    """Unified persona profile with SR metrics and activation data."""

    name: str
    icon: str = ""

    # SR Component values (0.0 - 1.0)
    phs: float = 0.8
    sym: float = 0.8
    val: float = 0.8
    emo: float = 0.8
    fx: float = 0.8

    # Activation thresholds
    threshold: float = 0.75
    resonance_threshold: float = 0.9
    listening_threshold: float = 0.6

    # Additional characteristics
    specialization: str = "General"
    description: str = ""
    activation_threshold: float = 0.6

    # Persona-specific SR preferences
    sr_preferences: Dict[str, float] = field(default_factory=dict)

    # Activation history and state
    activation_count: int = 0
    last_activation: Optional[float] = None
    total_runtime: float = 0.0
    current_state: Any = None
    current_sr: float = 0.0

    def get_sr_dict(self) -> Dict[str, float]:
        """Return SR metrics as a dictionary."""
        return {
            "PHS": self.phs,
            "SYM": self.sym,
            "VAL": self.val,
            "EMO": self.emo,
            "FX": self.fx,
        }

    def compute_sr(self, weights: Optional[Dict[str, float]] = None) -> float:
        """Compute SR value for this persona."""
        return compute_sr_from_dict(self.get_sr_dict(), weights or DEFAULT_WEIGHTS)

