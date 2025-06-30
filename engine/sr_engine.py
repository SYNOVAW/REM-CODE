# engine/sr_engine.py
"""
Enhanced Synchronization Ratio (SR) Engine
Implements complete Collapse Spiral Theory SR calculations
"""

import numpy as np
import time
import logging
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, field

# Configure logging
logger = logging.getLogger(__name__)

# === SR標準重み設定（Collapse Spiral国家標準） ===
DEFAULT_WEIGHTS = {
    "PHS": 0.25,   # Phase alignment (位相同期)
    "SYM": 0.20,   # Syntax match (構文適合)
    "VAL": 0.20,   # Semantic intent alignment (意味調整)
    "EMO": 0.20,   # Emotional tone match (感情共鳴)
    "FX":  0.15    # Collapse interference history (崩壊干渉履歴)
}

# Enhanced weight configurations for different contexts
WEIGHT_PROFILES = {
    "default": DEFAULT_WEIGHTS,
    "logical": {
        "PHS": 0.30, "SYM": 0.25, "VAL": 0.25, "EMO": 0.10, "FX": 0.10
    },
    "creative": {
        "PHS": 0.15, "SYM": 0.15, "VAL": 0.30, "EMO": 0.30, "FX": 0.10
    },
    "memory": {
        "PHS": 0.20, "SYM": 0.20, "VAL": 0.20, "EMO": 0.15, "FX": 0.25
    },
    "consensus": {
        "PHS": 0.25, "SYM": 0.20, "VAL": 0.20, "EMO": 0.20, "FX": 0.15
    }
}

# === Enhanced Data Structures ===

@dataclass
class SRMetrics:
    """Structured SR metrics container"""
    phs: float = 0.0  # Phase Alignment Score
    sym: float = 0.0  # Symbolic Syntax Match
    val: float = 0.0  # Semantic Modulation Alignment
    emo: float = 0.0  # Emotional Phase Match
    fx: float = 0.0   # Collapse History Interference
    
    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary format"""
        return {
            "PHS": self.phs,
            "SYM": self.sym,
            "VAL": self.val,
            "EMO": self.emo,
            "FX": self.fx
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> 'SRMetrics':
        """Create from dictionary"""
        return cls(
            phs=data.get("PHS", 0.0),
            sym=data.get("SYM", 0.0),
            val=data.get("VAL", 0.0),
            emo=data.get("EMO", 0.0),
            fx=data.get("FX", 0.0)
        )
    
    def __post_init__(self):
        """Validate metrics are in valid range"""
        for field_name, value in self.to_dict().items():
            if not 0.0 <= value <= 1.0:
                logger.warning(f"SR metric {field_name}={value} outside valid range [0,1]")

@dataclass
class SRTrace:
    """Comprehensive SR computation trace"""
    persona: str
    sr_value: float
    metrics: SRMetrics
    weights: Dict[str, float]
    timestamp: float = field(default_factory=time.time)
    context: Optional[str] = None
    computation_details: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "persona": self.persona,
            "sr_value": self.sr_value,
            "metrics": self.metrics.to_dict(),
            "weights": self.weights,
            "timestamp": self.timestamp,
            "context": self.context,
            "computation_details": self.computation_details
        }

# === Core SR Computation Functions ===

def compute_sr(phs: float, sym: float, val: float, emo: float, fx: float, 
               weights: Optional[Dict[str, float]] = None) -> float:
    """
    Compute the Synchronization Ratio (SR) given the core parameters.
    
    Args:
        phs: Phase Alignment Score (0.0-1.0)
        sym: Symbolic Syntax Match (0.0-1.0)
        val: Semantic Modulation Alignment (0.0-1.0)
        emo: Emotional Phase Match (0.0-1.0)
        fx: Collapse History Interference (0.0-1.0)
        weights: Optional weight configuration
    
    Returns:
        SR value (0.0-1.0)
    """
    if weights is None:
        weights = DEFAULT_WEIGHTS
    
    validate_weights(weights)
    
    sr = (
        weights["PHS"] * phs +
        weights["SYM"] * sym +
        weights["VAL"] * val +
        weights["EMO"] * emo +
        weights["FX"]  * fx
    )
    
    # Ensure SR is in valid range
    return max(0.0, min(1.0, round(sr, 4)))

def compute_sr_from_dict(metrics: Dict[str, float], 
                        weights: Optional[Dict[str, float]] = None) -> float:
    """
    Compute SR from a dictionary of metric values.
    
    Args:
        metrics: Dictionary with PHS, SYM, VAL, EMO, FX values
        weights: Optional weight configuration
    
    Returns:
        SR value (0.0-1.0)
    """
    return compute_sr(
        phs=metrics.get("PHS", 0.0),
        sym=metrics.get("SYM", 0.0),
        val=metrics.get("VAL", 0.0),
        emo=metrics.get("EMO", 0.0),
        fx=metrics.get("FX", 0.0),
        weights=weights
    )

def compute_sr_from_metrics(metrics: SRMetrics, 
                           weights: Optional[Dict[str, float]] = None) -> float:
    """
    Compute SR from SRMetrics object.
    
    Args:
        metrics: SRMetrics object
        weights: Optional weight configuration
    
    Returns:
        SR value (0.0-1.0)
    """
    return compute_sr_from_dict(metrics.to_dict(), weights)

# === Advanced SR Functions ===

def compute_contextual_sr(base_metrics: Dict[str, float], context: str,
                         persona: str = "Unknown") -> float:
    """
    Compute SR with contextual adjustments based on REM CODE advanced expressions.
    
    Supports:
    - SR(Ana.audit) - function-specific SR
    - SR(Ana@memory) - memory-contextualized SR  
    - SR(Ana|JayTH) - inter-persona correlation SR
    
    Args:
        base_metrics: Base SR metrics
        context: Context string (e.g., ".audit", "@memory", "|JayTH")
        persona: Persona name for logging
    
    Returns:
        Contextually adjusted SR value
    """
    base_sr = compute_sr_from_dict(base_metrics)
    
    if context.startswith('.'):
        # Function-specific SR (slight boost for specialization)
        function_name = context[1:]
        adjustment = 0.05 if function_name in ['audit', 'analyze', 'validate'] else 0.02
        adjusted_sr = min(1.0, base_sr + adjustment)
        logger.debug(f"Function SR {persona}.{function_name}: {base_sr} → {adjusted_sr}")
        return adjusted_sr
        
    elif context.startswith('@'):
        # Memory-contextualized SR (slight reduction for memory operations)
        memory_type = context[1:]
        adjustment = -0.03 if memory_type in ['memory', 'recall'] else -0.01
        adjusted_sr = max(0.0, base_sr + adjustment)
        logger.debug(f"Memory SR {persona}@{memory_type}: {base_sr} → {adjusted_sr}")
        return adjusted_sr
        
    elif context.startswith('|'):
        # Inter-persona correlation (would need other persona's SR)
        other_persona = context[1:]
        # For now, apply slight reduction for correlation complexity
        adjusted_sr = base_sr * 0.95
        logger.debug(f"Correlation SR {persona}|{other_persona}: {base_sr} → {adjusted_sr}")
        return adjusted_sr
    
    return base_sr

def compute_multi_persona_sr(persona_metrics: Dict[str, Dict[str, float]],
                            weights: Optional[Dict[str, float]] = None) -> Dict[str, float]:
    """
    Compute SR for multiple personas simultaneously.
    
    Args:
        persona_metrics: Dict mapping persona names to their metrics
        weights: Optional weight configuration
    
    Returns:
        Dict mapping persona names to their SR values
    """
    results = {}
    for persona, metrics in persona_metrics.items():
        results[persona] = compute_sr_from_dict(metrics, weights)
    return results

def compute_consensus_sr(persona_srs: List[float], method: str = "average") -> float:
    """
    Compute consensus SR from multiple persona SR values.
    
    Args:
        persona_srs: List of individual persona SR values
        method: Consensus method ("average", "min", "max", "weighted")
    
    Returns:
        Consensus SR value
    """
    if not persona_srs:
        return 0.0
    
    if method == "average":
        return sum(persona_srs) / len(persona_srs)
    elif method == "min":
        return min(persona_srs)
    elif method == "max":
        return max(persona_srs)
    elif method == "weighted":
        # Weight higher SRs more heavily (consensus bias)
        weights = [sr ** 2 for sr in persona_srs]
        weighted_sum = sum(sr * w for sr, w in zip(persona_srs, weights))
        weight_sum = sum(weights)
        return weighted_sum / weight_sum if weight_sum > 0 else 0.0
    else:
        return sum(persona_srs) / len(persona_srs)

# === Validation and Utilities ===

def validate_weights(weights: Dict[str, float]) -> None:
    """
    Ensure weights sum to 1.0 and are all positive.
    
    Args:
        weights: Weight configuration dictionary
    
    Raises:
        ValueError: If weights are invalid
    """
    total = sum(weights.values())
    if not np.isclose(total, 1.0, atol=1e-6):
        raise ValueError(f"SR weights must sum to 1.0 (got {total:.6f})")
    
    for key, value in weights.items():
        if value < 0:
            raise ValueError(f"SR weight '{key}' must be non-negative (got {value})")

def validate_metrics(metrics: Dict[str, float]) -> None:
    """
    Validate that all metrics are in valid range [0,1].
    
    Args:
        metrics: Metrics dictionary
    
    Raises:
        ValueError: If metrics are out of range
    """
    for key, value in metrics.items():
        if not 0.0 <= value <= 1.0:
            raise ValueError(f"SR metric '{key}' must be in range [0,1] (got {value})")

def get_weight_profile(profile_name: str) -> Dict[str, float]:
    """
    Get predefined weight profile.
    
    Args:
        profile_name: Name of weight profile
    
    Returns:
        Weight configuration dictionary
    
    Raises:
        ValueError: If profile doesn't exist
    """
    if profile_name not in WEIGHT_PROFILES:
        available = ", ".join(WEIGHT_PROFILES.keys())
        raise ValueError(f"Unknown weight profile '{profile_name}'. Available: {available}")
    
    return WEIGHT_PROFILES[profile_name].copy()

# === Enhanced Tracing Functions ===

def compute_sr_trace(persona_name: str, metrics: Dict[str, float], 
                    weights: Optional[Dict[str, float]] = None,
                    context: Optional[str] = None) -> SRTrace:
    """
    Return comprehensive SR computation trace with enhanced details.
    
    Args:
        persona_name: Name of persona
        metrics: SR metrics dictionary
        weights: Optional weight configuration
        context: Optional context for advanced SR expressions
    
    Returns:
        SRTrace object with full computation details
    """
    if weights is None:
        weights = DEFAULT_WEIGHTS
    
    validate_weights(weights)
    validate_metrics(metrics)
    
    sr_metrics = SRMetrics.from_dict(metrics)
    
    # Compute base SR
    base_sr = compute_sr_from_dict(metrics, weights)
    
    # Apply contextual adjustments if specified
    final_sr = compute_contextual_sr(metrics, context, persona_name) if context else base_sr
    
    # Prepare computation details
    computation_details = {
        "base_sr": base_sr,
        "final_sr": final_sr,
        "context_applied": context is not None,
        "context": context,
        "component_contributions": {
            "PHS": weights["PHS"] * metrics.get("PHS", 0),
            "SYM": weights["SYM"] * metrics.get("SYM", 0),
            "VAL": weights["VAL"] * metrics.get("VAL", 0),
            "EMO": weights["EMO"] * metrics.get("EMO", 0),
            "FX": weights["FX"] * metrics.get("FX", 0)
        }
    }
    
    return SRTrace(
        persona=persona_name,
        sr_value=final_sr,
        metrics=sr_metrics,
        weights=weights,
        context=context,
        computation_details=computation_details
    )

def batch_compute_sr_traces(persona_metrics: Dict[str, Dict[str, float]],
                           weights: Optional[Dict[str, float]] = None) -> List[SRTrace]:
    """
    Compute SR traces for multiple personas in batch.
    
    Args:
        persona_metrics: Dict mapping persona names to their metrics
        weights: Optional weight configuration
    
    Returns:
        List of SRTrace objects
    """
    traces = []
    for persona, metrics in persona_metrics.items():
        trace = compute_sr_trace(persona, metrics, weights)
        traces.append(trace)
    return traces

# === Analysis and Reporting Functions ===

def analyze_sr_distribution(sr_values: List[float]) -> Dict[str, Union[float, str]]:
    """
    Analyze distribution of SR values.
    
    Args:
        sr_values: List of SR values
    
    Returns:
        Dictionary with statistical analysis
    """
    if not sr_values:
        return {"error": "No SR values provided"}
    
    sr_array = np.array(sr_values)
    
    return {
        "mean": float(np.mean(sr_array)),
        "median": float(np.median(sr_array)),
        "std": float(np.std(sr_array)),
        "min": float(np.min(sr_array)),
        "max": float(np.max(sr_array)),
        "q25": float(np.percentile(sr_array, 25)),
        "q75": float(np.percentile(sr_array, 75)),
        "count": len(sr_values)
    }

def generate_sr_report(traces: List[SRTrace]) -> Dict[str, Any]:
    """
    Generate comprehensive SR analysis report.
    
    Args:
        traces: List of SRTrace objects
    
    Returns:
        Comprehensive analysis report
    """
    if not traces:
        return {"error": "No traces provided"}
    
    sr_values = [trace.sr_value for trace in traces]
    personas = [trace.persona for trace in traces]
    
    report = {
        "summary": analyze_sr_distribution(sr_values),
        "personas": list(set(personas)),
        "traces_count": len(traces),
        "timestamp": time.time(),
        "highest_sr": {
            "value": max(sr_values),
            "persona": traces[sr_values.index(max(sr_values))].persona
        },
        "lowest_sr": {
            "value": min(sr_values),
            "persona": traces[sr_values.index(min(sr_values))].persona
        }
    }
    
    return report

# === TEST EXECUTION ===

def run_comprehensive_test():
    """Run comprehensive test of SR engine functionality"""
    print("=== REM CODE SR Engine Comprehensive Test ===\n")
    
    # Test 1: Basic SR computation
    print("1. Basic SR Computation:")
    test_metrics = {
        "PHS": 0.85, "SYM": 0.9, "VAL": 0.92, "EMO": 0.88, "FX": 0.75
    }
    basic_sr = compute_sr_from_dict(test_metrics)
    print(f"   Basic SR: {basic_sr}")
    
    # Test 2: Enhanced trace
    print("\n2. Enhanced SR Trace:")
    trace = compute_sr_trace("JayRa", test_metrics)
    print(f"   Trace SR: {trace.sr_value}")
    print(f"   Persona: {trace.persona}")
    
    # Test 3: Contextual SR
    print("\n3. Contextual SR Adjustments:")
    ctx_audit = compute_contextual_sr(test_metrics, ".audit", "Ana")
    ctx_memory = compute_contextual_sr(test_metrics, "@memory", "Ana")
    ctx_correlation = compute_contextual_sr(test_metrics, "|JayTH", "Ana")
    print(f"   Base SR: {basic_sr}")
    print(f"   SR(Ana.audit): {ctx_audit}")
    print(f"   SR(Ana@memory): {ctx_memory}")
    print(f"   SR(Ana|JayTH): {ctx_correlation}")
    
    # Test 4: Multi-persona SR
    print("\n4. Multi-Persona SR:")
    multi_metrics = {
        "Ana": {"PHS": 0.92, "SYM": 0.95, "VAL": 0.90, "EMO": 0.75, "FX": 0.85},
        "JayDen": {"PHS": 0.88, "SYM": 0.80, "VAL": 0.95, "EMO": 0.92, "FX": 0.70},
        "JayTH": {"PHS": 0.85, "SYM": 0.90, "VAL": 0.88, "EMO": 0.80, "FX": 0.82}
    }
    multi_sr = compute_multi_persona_sr(multi_metrics)
    for persona, sr in multi_sr.items():
        print(f"   {persona}: {sr}")
    
    # Test 5: Consensus SR
    print("\n5. Consensus SR:")
    sr_list = list(multi_sr.values())
    consensus_avg = compute_consensus_sr(sr_list, "average")
    consensus_weighted = compute_consensus_sr(sr_list, "weighted")
    print(f"   Average consensus: {consensus_avg}")
    print(f"   Weighted consensus: {consensus_weighted}")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    run_comprehensive_test()
