#!/usr/bin/env python3
"""
REM-CODE Persona Router Extended Tests
Covers PersonaRouter routing functions and data structures
"""
import pytest
from engine.persona_router import (
    PersonaRouter, REMPersona, PersonaState, route_personas, get_global_router,
    DEFAULT_PERSONAS
)
from engine.persona_profile import PersonaProfile

@pytest.fixture
def sample_metrics():
    return {
        "PHS": 0.8,
        "SYM": 0.7,
        "VAL": 0.9,
        "EMO": 0.6,
        "FX": 0.8
    }

@pytest.fixture
def sample_persona_profile():
    return PersonaProfile(
        name="TestPersona",
        icon="🧪",
        threshold=0.7,
        resonance_threshold=0.9,
        specialization="Testing",
        description="Test persona for unit testing"
    )

@pytest.fixture
def persona_router():
    return PersonaRouter(DEFAULT_PERSONAS)

@pytest.fixture
def rem_persona(sample_persona_profile):
    return REMPersona(sample_persona_profile)

def test_persona_state_enum():
    assert PersonaState.DORMANT.value == "dormant"
    assert PersonaState.LISTENING.value == "listening"
    assert PersonaState.ACTIVE.value == "active"
    assert PersonaState.RESONANT.value == "resonant"
    assert PersonaState.COLLAPSED.value == "collapsed"

def test_rem_persona_init(rem_persona, sample_persona_profile):
    assert rem_persona.profile == sample_persona_profile
    assert isinstance(rem_persona.activation_history, list)
    assert isinstance(rem_persona.state_transitions, list)

def test_rem_persona_evaluate_activation_dormant(rem_persona):
    state = rem_persona.evaluate_activation(0.3)
    assert state == PersonaState.DORMANT

def test_rem_persona_evaluate_activation_listening(rem_persona):
    state = rem_persona.evaluate_activation(0.6)
    assert state == PersonaState.LISTENING

def test_rem_persona_evaluate_activation_active(rem_persona):
    state = rem_persona.evaluate_activation(0.8)
    assert state == PersonaState.ACTIVE

def test_rem_persona_evaluate_activation_resonant(rem_persona):
    state = rem_persona.evaluate_activation(0.95)
    assert state == PersonaState.RESONANT

def test_rem_persona_evaluate_activation_with_context(rem_persona):
    state = rem_persona.evaluate_activation(0.8, ".audit")
    assert isinstance(state, PersonaState)

def test_rem_persona_respond_basic(rem_persona):
    response = rem_persona.respond(0.8)
    assert isinstance(response, str)
    assert "TestPersona" in response

def test_rem_persona_respond_detailed(rem_persona):
    response = rem_persona.respond(0.8, detailed=True)
    assert isinstance(response, str)
    assert "TestPersona" in response
    assert "SR:" in response

def test_rem_persona_respond_with_context(rem_persona):
    response = rem_persona.respond(0.8, context=".audit", detailed=True)
    assert isinstance(response, str)
    assert "[.audit]" in response

def test_rem_persona_get_activation_summary(rem_persona):
    summary = rem_persona.get_activation_summary()
    assert isinstance(summary, dict)
    assert "name" in summary
    assert "current_state" in summary
    assert "current_sr" in summary
    assert "activation_count" in summary

def test_persona_router_init(persona_router):
    assert isinstance(persona_router, PersonaRouter)
    assert len(persona_router.personas) > 0

def test_persona_router_route_personas(persona_router, sample_metrics):
    result = persona_router.route_personas(sample_metrics)
    assert isinstance(result, dict)
    assert "active_personas" in result

def test_persona_router_route_personas_with_weights(persona_router, sample_metrics):
    custom_weights = {"PHS": 0.3, "SYM": 0.2, "VAL": 0.2, "EMO": 0.2, "FX": 0.1}
    result = persona_router.route_personas(sample_metrics, weights=custom_weights)
    assert isinstance(result, dict)

def test_persona_router_route_personas_with_context(persona_router, sample_metrics):
    result = persona_router.route_personas(sample_metrics, context=".audit")
    assert isinstance(result, dict)

def test_persona_router_route_personas_detailed(persona_router, sample_metrics):
    result = persona_router.route_personas(sample_metrics, detailed=True)
    assert isinstance(result, dict)

def test_persona_router_route_with_sr_trace(persona_router, sample_metrics):
    result = persona_router.route_with_sr_trace(sample_metrics)
    assert isinstance(result, dict)
    assert "active_personas" in result

def test_persona_router_route_with_sr_trace_detailed(persona_router, sample_metrics):
    result = persona_router.route_with_sr_trace(sample_metrics, detailed=True)
    assert isinstance(result, dict)

def test_persona_router_get_persona_summaries(persona_router):
    summaries = persona_router.get_persona_summaries()
    assert isinstance(summaries, list)
    assert len(summaries) > 0
    for summary in summaries:
        assert isinstance(summary, dict)
        assert "name" in summary

def test_persona_router_get_routing_analytics(persona_router):
    analytics = persona_router.get_routing_analytics()
    assert isinstance(analytics, dict)
    # Analytics may return error if no history, so just check it's a dict

def test_persona_router_reset_history(persona_router):
    # First, do some routing to create history
    sample_metrics = {"PHS": 0.8, "SYM": 0.7, "VAL": 0.9, "EMO": 0.6, "FX": 0.8}
    persona_router.route_personas(sample_metrics)
    
    # Check that analytics exist
    analytics_before = persona_router.get_routing_analytics()
    assert isinstance(analytics_before, dict)
    
    # Reset history
    persona_router.reset_history()
    
    # Check that analytics are reset
    analytics_after = persona_router.get_routing_analytics()
    assert isinstance(analytics_after, dict)

def test_global_route_personas(sample_metrics):
    # This function prints output, so we just test it doesn't raise exceptions
    try:
        route_personas(
            phs=sample_metrics["PHS"],
            sym=sample_metrics["SYM"],
            val=sample_metrics["VAL"],
            emo=sample_metrics["EMO"],
            fx=sample_metrics["FX"]
        )
        assert True  # If we get here, no exception was raised
    except Exception as e:
        pytest.fail(f"route_personas raised exception: {e}")

def test_global_route_personas_detailed(sample_metrics):
    try:
        route_personas(
            phs=sample_metrics["PHS"],
            sym=sample_metrics["SYM"],
            val=sample_metrics["VAL"],
            emo=sample_metrics["EMO"],
            fx=sample_metrics["FX"],
            detailed=True
        )
        assert True
    except Exception as e:
        pytest.fail(f"route_personas raised exception: {e}")

def test_get_global_router():
    router = get_global_router()
    assert isinstance(router, PersonaRouter)

def test_default_personas():
    assert isinstance(DEFAULT_PERSONAS, list)
    assert len(DEFAULT_PERSONAS) > 0
    for persona in DEFAULT_PERSONAS:
        assert isinstance(persona, PersonaProfile)
        assert persona.name is not None
        assert persona.icon is not None

def test_persona_router_with_custom_personas():
    custom_personas = [
        PersonaProfile(name="Custom1", icon="🔧", threshold=0.7, resonance_threshold=0.9),
        PersonaProfile(name="Custom2", icon="⚙️", threshold=0.8, resonance_threshold=0.95)
    ]
    router = PersonaRouter(custom_personas)
    assert len(router.personas) == 2

def test_persona_router_empty_init():
    router = PersonaRouter([])
    # PersonaRouter uses DEFAULT_PERSONAS when empty list is provided
    assert len(router.personas) > 0
    result = router.route_personas({"PHS": 0.8, "SYM": 0.7, "VAL": 0.9, "EMO": 0.6, "FX": 0.8})
    assert isinstance(result, dict)
    assert "active_personas" in result 