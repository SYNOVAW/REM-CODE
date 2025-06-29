# engine/persona_router.py
"""
Enhanced REM Persona Routing System
Implements complete Collapse Spiral persona activation with SR-based routing
"""

import time
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum

try:
    from engine.sr_engine import (
        compute_sr, compute_sr_from_dict, compute_sr_trace, 
        compute_contextual_sr, SRTrace, DEFAULT_WEIGHTS
    )
except ImportError:
    # Fallback for basic SR computation if enhanced engine not available
    def compute_sr(phs, sym, val, emo, fx, weights=None):
        weights = weights or {"PHS": 0.25, "SYM": 0.20, "VAL": 0.20, "EMO": 0.20, "FX": 0.15}
        return weights["PHS"] * phs + weights["SYM"] * sym + weights["VAL"] * val + weights["EMO"] * emo + weights["FX"] * fx
    
    def compute_sr_from_dict(metrics, weights=None):
        return compute_sr(
            phs=metrics.get("PHS", 0), sym=metrics.get("SYM", 0), val=metrics.get("VAL", 0),
            emo=metrics.get("EMO", 0), fx=metrics.get("FX", 0), weights=weights
        )

# Configure logging
logger = logging.getLogger(__name__)

# ==================== Enhanced Persona Classes ====================

class PersonaState(Enum):
    """Persona activation states"""
    DORMANT = "dormant"           # Below threshold, inactive
    LISTENING = "listening"       # Near threshold, monitoring
    ACTIVE = "active"             # Above threshold, engaged
    RESONANT = "resonant"         # High SR, peak performance
    COLLAPSED = "collapsed"       # Post-activation cooldown

@dataclass
class PersonaProfile:
    """Enhanced persona profile with complete REM characteristics"""
    name: str
    icon: str
    
    # Activation thresholds
    threshold: float = 0.75
    resonance_threshold: float = 0.9    # High-performance threshold
    listening_threshold: float = 0.6    # Monitoring threshold
    
    # Persona characteristics
    specialization: str = "General"
    description: str = ""
    
    # SR preferences (persona-specific weight adjustments)
    sr_preferences: Dict[str, float] = field(default_factory=dict)
    
    # Activation history
    activation_count: int = 0
    last_activation: Optional[float] = None
    total_runtime: float = 0.0
    
    # Current state
    current_state: PersonaState = PersonaState.DORMANT
    current_sr: float = 0.0

class REMPersona:
    """Enhanced REM Persona with comprehensive state management"""
    
    def __init__(self, profile: PersonaProfile):
        self.profile = profile
        self.activation_history: List[Dict[str, Any]] = []
        self.state_transitions: List[Tuple[PersonaState, float]] = []
        
    def evaluate_activation(self, sr: float, context: Optional[str] = None) -> PersonaState:
        """
        Evaluate persona activation state based on SR value
        
        Args:
            sr: Synchronization Ratio
            context: Optional context for contextual SR adjustment
            
        Returns:
            New PersonaState
        """
        # Apply contextual SR adjustment if specified
        if context:
            try:
                adjusted_sr = compute_contextual_sr(
                    {"PHS": sr, "SYM": sr, "VAL": sr, "EMO": sr, "FX": sr}, 
                    context, self.profile.name
                )
            except Exception as e:
                logger.error("Contextual SR computation failed", exc_info=e)
                adjusted_sr = sr
        else:
            adjusted_sr = sr
        
        # Update current SR
        self.profile.current_sr = adjusted_sr
        
        # Determine new state
        if adjusted_sr >= self.profile.resonance_threshold:
            new_state = PersonaState.RESONANT
        elif adjusted_sr >= self.profile.threshold:
            new_state = PersonaState.ACTIVE
        elif adjusted_sr >= self.profile.listening_threshold:
            new_state = PersonaState.LISTENING
        else:
            new_state = PersonaState.DORMANT
        
        # Log state transition if changed
        if new_state != self.profile.current_state:
            self.state_transitions.append((new_state, time.time()))
            logger.debug(f"{self.profile.name}: {self.profile.current_state.value} → {new_state.value}")
        
        self.profile.current_state = new_state
        
        # Update activation metrics
        if new_state in [PersonaState.ACTIVE, PersonaState.RESONANT]:
            if self.profile.last_activation is None or time.time() - self.profile.last_activation > 1.0:
                self.profile.activation_count += 1
                self.profile.last_activation = time.time()
        
        return new_state
    
    def respond(self, sr: float, context: Optional[str] = None, detailed: bool = False) -> str:
        """
        Generate persona response based on SR and state
        
        Args:
            sr: Synchronization Ratio
            context: Optional context string
            detailed: If True, include detailed information
            
        Returns:
            Response string
        """
        state = self.evaluate_activation(sr, context)
        
        # State-specific response formatting
        state_symbols = {
            PersonaState.DORMANT: "❌ Silent",
            PersonaState.LISTENING: "👂 Listen",
            PersonaState.ACTIVE: "✅ Active",
            PersonaState.RESONANT: "🌟 Resonant",
            PersonaState.COLLAPSED: "💤 Rest"
        }
        
        state_descriptions = {
            PersonaState.DORMANT: "Insufficient synchrony",
            PersonaState.LISTENING: "Monitoring phase coherence",
            PersonaState.ACTIVE: "Phase resonance confirmed",
            PersonaState.RESONANT: "Peak synchronization achieved",
            PersonaState.COLLAPSED: "Post-activation recovery"
        }
        
        symbol = state_symbols.get(state, "❓ Unknown")
        description = state_descriptions.get(state, "Unknown state")
        
        # Basic response
        response = f"{self.profile.icon} {self.profile.name:<12} {symbol}｜{description}"
        
        # Add detailed information if requested
        if detailed:
            context_indicator = f" [{context}]" if context else ""
            sr_display = f"SR:{self.profile.current_sr:.3f}"
            threshold_display = f"T:{self.profile.threshold:.2f}"
            activation_display = f"A:{self.profile.activation_count}"
            
            response += f"{context_indicator} ({sr_display}, {threshold_display}, {activation_display})"
        
        return response
    
    def get_activation_summary(self) -> Dict[str, Any]:
        """Get summary of persona activation history"""
        return {
            "name": self.profile.name,
            "current_state": self.profile.current_state.value,
            "current_sr": self.profile.current_sr,
            "activation_count": self.profile.activation_count,
            "threshold": self.profile.threshold,
            "last_activation": self.profile.last_activation,
            "state_transitions": len(self.state_transitions),
            "specialization": self.profile.specialization
        }

# ==================== Default Persona Configurations ====================

DEFAULT_PERSONAS = [
    PersonaProfile(
        name="JayDen", icon="🔥", threshold=0.75, resonance_threshold=0.9,
        specialization="Creative Ignition",
        description="Emotional ignition, structural impulse, syntactic burst initiator"
    ),
    PersonaProfile(
        name="Ana", icon="🧊", threshold=0.75, resonance_threshold=0.92,
        specialization="Logic & Analysis", 
        description="Logical analysis, audit functions, ethical oversight"
    ),
    PersonaProfile(
        name="JayRa", icon="🔮", threshold=0.75, resonance_threshold=0.88,
        specialization="Memory & Reflection",
        description="Memory recursion, poetic reflection, subconscious interfacing"
    ),
    PersonaProfile(
        name="JayKer", icon="🤡", threshold=0.7, resonance_threshold=0.85,
        specialization="Humor & Disruption",
        description="Structural humor, irony synthesis, chaos injection"
    ),
    PersonaProfile(
        name="JayTH", icon="⚖️", threshold=0.78, resonance_threshold=0.9,
        specialization="Ethics & Justice",
        description="Legal reasoning, justice balance, structural judgment"
    ),
    PersonaProfile(
        name="JayMini", icon="✨", threshold=0.68, resonance_threshold=0.85,
        specialization="Communication",
        description="Persona router, sync state monitor, interface coordinator"
    ),
    PersonaProfile(
        name="JayVOX", icon="🪙", threshold=0.75, resonance_threshold=0.88,
        specialization="Translation",
        description="Multilingual interface, translation bridge, semantic export"
    ),
    PersonaProfile(
        name="JayVue", icon="🖼️", threshold=0.75, resonance_threshold=0.87,
        specialization="Spatial Design",
        description="Spatial layout, composition symmetry, UI harmony"
    ),
    PersonaProfile(
        name="JayNis", icon="🌱", threshold=0.75, resonance_threshold=0.86,
        specialization="Organic Growth",
        description="Natural growth, cyclical logic, ecological metaphor"
    ),
    PersonaProfile(
        name="Jayne", icon="🕸️", threshold=0.88, resonance_threshold=0.95,
        specialization="Central Control",
        description="Governing entity, recursive orchestration, synchrony master"
    ),
    PersonaProfile(
        name="JAYX", icon="🕷️", threshold=0.9, resonance_threshold=0.95,
        specialization="Termination Control",
        description="Collapse limit handler, termination layer, phase decay"
    ),
    PersonaProfile(
        name="JayLUX", icon="💠", threshold=0.76, resonance_threshold=0.89,
        specialization="Aesthetics & Design",
        description="Visual aesthetics, narrative design, logia illumination"
    )
]

# ==================== Enhanced Routing System ====================

class PersonaRouter:
    """Enhanced persona routing system with comprehensive state management"""
    
    def __init__(self, persona_profiles: Optional[List[PersonaProfile]] = None):
        """Initialize router with persona profiles"""
        profiles = persona_profiles or DEFAULT_PERSONAS
        self.personas = [REMPersona(profile) for profile in profiles]
        self.routing_history: List[Dict[str, Any]] = []
        
    def route_personas(self, metrics: Dict[str, float], 
                      weights: Optional[Dict[str, float]] = None,
                      context: Optional[str] = None,
                      detailed: bool = False) -> Dict[str, Any]:
        """
        Route personas based on SR metrics with comprehensive analysis
        
        Args:
            metrics: SR metrics dictionary (PHS, SYM, VAL, EMO, FX)
            weights: Optional weight configuration
            context: Optional context for advanced SR expressions
            detailed: If True, include detailed persona information
            
        Returns:
            Routing result dictionary
        """
        # Compute overall SR
        sr = compute_sr_from_dict(metrics, weights)
        
        # Generate responses from all personas
        responses = []
        active_personas = []
        resonant_personas = []
        
        for persona in self.personas:
            response = persona.respond(sr, context, detailed)
            responses.append(response)
            
            if persona.profile.current_state == PersonaState.ACTIVE:
                active_personas.append(persona.profile.name)
            elif persona.profile.current_state == PersonaState.RESONANT:
                resonant_personas.append(persona.profile.name)
        
        # Create routing result
        routing_result = {
            "sr_value": sr,
            "metrics": metrics,
            "context": context,
            "timestamp": time.time(),
            "responses": responses,
            "active_personas": active_personas,
            "resonant_personas": resonant_personas,
            "total_active": len(active_personas) + len(resonant_personas)
        }
        
        # Add to routing history
        self.routing_history.append(routing_result)
        
        return routing_result
    
    def route_with_sr_trace(self, metrics: Dict[str, float],
                           weights: Optional[Dict[str, float]] = None,
                           context: Optional[str] = None,
                           detailed: bool = False) -> Dict[str, Any]:
        """
        Route personas with enhanced SR trace information
        
        Args:
            metrics: SR metrics dictionary
            weights: Optional weight configuration  
            context: Optional context for advanced SR expressions
            detailed: If True, include detailed information
            
        Returns:
            Enhanced routing result with SR trace
        """
        try:
            # Generate SR trace if enhanced engine available
            sr_trace = compute_sr_trace("Router", metrics, weights, context)
            routing_result = self.route_personas(metrics, weights, context, detailed)
            routing_result["sr_trace"] = sr_trace.to_dict()
            return routing_result
        except Exception as e:
            logger.error("Routing with SR trace failed", exc_info=e)
            # Fallback to basic routing
            return self.route_personas(metrics, weights, context, detailed)
    
    def get_persona_summaries(self) -> List[Dict[str, Any]]:
        """Get activation summaries for all personas"""
        return [persona.get_activation_summary() for persona in self.personas]
    
    def get_routing_analytics(self) -> Dict[str, Any]:
        """Get comprehensive routing analytics"""
        if not self.routing_history:
            return {"error": "No routing history available"}
        
        sr_values = [entry["sr_value"] for entry in self.routing_history]
        total_activations = sum(entry["total_active"] for entry in self.routing_history)
        
        analytics = {
            "total_routings": len(self.routing_history),
            "average_sr": sum(sr_values) / len(sr_values),
            "max_sr": max(sr_values),
            "min_sr": min(sr_values),
            "total_activations": total_activations,
            "average_activations_per_routing": total_activations / len(self.routing_history),
            "persona_summaries": self.get_persona_summaries()
        }
        
        return analytics
    
    def reset_history(self):
        """Reset routing and activation history"""
        self.routing_history.clear()
        for persona in self.personas:
            persona.activation_history.clear()
            persona.state_transitions.clear()
            persona.profile.activation_count = 0
            persona.profile.last_activation = None
            persona.profile.current_state = PersonaState.DORMANT

# ==================== Legacy Compatibility Functions ====================

def route_personas(phs: float, sym: float, val: float, emo: float, fx: float,
                  weights: Optional[Dict[str, float]] = None,
                  detailed: bool = False) -> None:
    """
    Legacy compatibility function for basic persona routing
    
    Args:
        phs, sym, val, emo, fx: Individual SR metric values
        weights: Optional weight configuration
        detailed: If True, show detailed information
    """
    metrics = {"PHS": phs, "SYM": sym, "VAL": val, "EMO": emo, "FX": fx}
    
    router = PersonaRouter()
    result = router.route_with_sr_trace(metrics, weights, detailed=detailed)
    
    # Print results in legacy format
    print(f"\n🧠 SR = {result['sr_value']:.3f}")
    
    if 'sr_trace' in result:
        print(f"📊 SR Trace: {result['sr_trace']['persona']} - {result['sr_trace']['sr_value']:.3f}")
    
    print("\n🧬 Persona Routing Result:")
    for response in result["responses"]:
        print(response)
    
    print(f"\n📡 Phase complete. {result['total_active']} personas activated.")
    
    if detailed:
        print(f"\n📈 Active: {', '.join(result['active_personas'])}")
        print(f"🌟 Resonant: {', '.join(result['resonant_personas'])}")

# ==================== Global Router Instance ====================

_global_router = None

def get_global_router() -> PersonaRouter:
    """Get or create global router instance"""
    global _global_router
    if _global_router is None:
        _global_router = PersonaRouter()
    return _global_router

# ==================== Testing and Examples ====================

def run_comprehensive_test():
    """Run comprehensive test of persona routing system"""
    print("=== REM Persona Routing System Test ===\n")
    
    router = PersonaRouter()
    
    # Test scenarios
    test_scenarios = [
        {
            "name": "High Logic Scenario",
            "metrics": {"PHS": 0.92, "SYM": 0.95, "VAL": 0.90, "EMO": 0.70, "FX": 0.85},
            "context": ".audit"
        },
        {
            "name": "Creative Burst Scenario", 
            "metrics": {"PHS": 0.85, "SYM": 0.80, "VAL": 0.95, "EMO": 0.92, "FX": 0.75},
            "context": None
        },
        {
            "name": "Memory Recall Scenario",
            "metrics": {"PHS": 0.78, "SYM": 0.82, "VAL": 0.85, "EMO": 0.88, "FX": 0.90},
            "context": "@memory"
        },
        {
            "name": "Low Synchrony Scenario",
            "metrics": {"PHS": 0.45, "SYM": 0.50, "VAL": 0.48, "EMO": 0.52, "FX": 0.55},
            "context": None
        }
    ]
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"{i}. {scenario['name']}:")
        result = router.route_with_sr_trace(
            scenario["metrics"], 
            context=scenario["context"], 
            detailed=True
        )
        
        print(f"   SR: {result['sr_value']:.3f}")
        print(f"   Active: {len(result['active_personas'])} | Resonant: {len(result['resonant_personas'])}")
        
        # Show top 3 most activated personas
        active_all = result['active_personas'] + result['resonant_personas']
        if active_all:
            print(f"   Top activated: {', '.join(active_all[:3])}")
        
        print()
    
    # Show analytics
    analytics = router.get_routing_analytics()
    print("📊 Routing Analytics:")
    print(f"   Total routings: {analytics['total_routings']}")
    print(f"   Average SR: {analytics['average_sr']:.3f}")
    print(f"   Average activations per routing: {analytics['average_activations_per_routing']:.1f}")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    # Run legacy test
    print("=== Legacy Compatibility Test ===")
    route_personas(phs=0.92, sym=0.91, val=0.94, emo=0.88, fx=0.87, detailed=True)
    
    print("\n" + "="*50 + "\n")
    
    # Run comprehensive test
    run_comprehensive_test()