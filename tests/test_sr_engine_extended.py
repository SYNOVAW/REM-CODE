#!/usr/bin/env python3
"""
REM-CODE SR Engine Extended Tests
Covers SR computation functions and data structures
"""
import pytest
from engine.sr_engine import (
    compute_sr, compute_sr_from_dict, compute_sr_from_metrics,
    compute_contextual_sr, compute_multi_persona_sr, compute_consensus_sr,
    validate_weights, validate_metrics, get_weight_profile,
    compute_sr_trace, batch_compute_sr_traces, analyze_sr_distribution,
    generate_sr_report, SRMetrics, SRTrace, DEFAULT_WEIGHTS, WEIGHT_PROFILES
)

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
def sample_sr_metrics():
    return SRMetrics(phs=0.8, sym=0.7, val=0.9, emo=0.6, fx=0.8)

@pytest.fixture
def multi_persona_metrics():
    return {
        "Ana": {"PHS": 0.8, "SYM": 0.7, "VAL": 0.9, "EMO": 0.6, "FX": 0.8},
        "JayDen": {"PHS": 0.9, "SYM": 0.8, "VAL": 0.7, "EMO": 0.8, "FX": 0.7},
        "JayTH": {"PHS": 0.7, "SYM": 0.9, "VAL": 0.8, "EMO": 0.7, "FX": 0.9}
    }

def test_sr_metrics_creation(sample_sr_metrics):
    assert sample_sr_metrics.phs == 0.8
    assert sample_sr_metrics.sym == 0.7
    assert sample_sr_metrics.val == 0.9
    assert sample_sr_metrics.emo == 0.6
    assert sample_sr_metrics.fx == 0.8

def test_sr_metrics_to_dict(sample_sr_metrics):
    data = sample_sr_metrics.to_dict()
    assert data["PHS"] == 0.8
    assert data["SYM"] == 0.7
    assert data["VAL"] == 0.9
    assert data["EMO"] == 0.6
    assert data["FX"] == 0.8

def test_sr_metrics_from_dict(sample_metrics):
    metrics = SRMetrics.from_dict(sample_metrics)
    assert metrics.phs == 0.8
    assert metrics.sym == 0.7
    assert metrics.val == 0.9
    assert metrics.emo == 0.6
    assert metrics.fx == 0.8

def test_compute_sr_basic():
    sr = compute_sr(0.8, 0.7, 0.9, 0.6, 0.8)
    assert isinstance(sr, float)
    assert 0.0 <= sr <= 1.0

def test_compute_sr_with_weights():
    custom_weights = {"PHS": 0.3, "SYM": 0.2, "VAL": 0.2, "EMO": 0.2, "FX": 0.1}
    sr = compute_sr(0.8, 0.7, 0.9, 0.6, 0.8, custom_weights)
    assert isinstance(sr, float)
    assert 0.0 <= sr <= 1.0

def test_compute_sr_from_dict(sample_metrics):
    sr = compute_sr_from_dict(sample_metrics)
    assert isinstance(sr, float)
    assert 0.0 <= sr <= 1.0

def test_compute_sr_from_metrics(sample_sr_metrics):
    sr = compute_sr_from_metrics(sample_sr_metrics)
    assert isinstance(sr, float)
    assert 0.0 <= sr <= 1.0

def test_compute_contextual_sr_function():
    base_metrics = {"PHS": 0.8, "SYM": 0.7, "VAL": 0.9, "EMO": 0.6, "FX": 0.8}
    sr = compute_contextual_sr(base_metrics, ".audit", "Ana")
    assert isinstance(sr, float)
    assert 0.0 <= sr <= 1.0

def test_compute_contextual_sr_memory():
    base_metrics = {"PHS": 0.8, "SYM": 0.7, "VAL": 0.9, "EMO": 0.6, "FX": 0.8}
    sr = compute_contextual_sr(base_metrics, "@memory", "Ana")
    assert isinstance(sr, float)
    assert 0.0 <= sr <= 1.0

def test_compute_contextual_sr_correlation():
    base_metrics = {"PHS": 0.8, "SYM": 0.7, "VAL": 0.9, "EMO": 0.6, "FX": 0.8}
    sr = compute_contextual_sr(base_metrics, "|JayTH", "Ana")
    assert isinstance(sr, float)
    assert 0.0 <= sr <= 1.0

def test_compute_multi_persona_sr(multi_persona_metrics):
    result = compute_multi_persona_sr(multi_persona_metrics)
    assert isinstance(result, dict)
    assert "Ana" in result
    assert "JayDen" in result
    assert "JayTH" in result
    for sr in result.values():
        assert 0.0 <= sr <= 1.0

def test_compute_consensus_sr_average():
    sr_values = [0.8, 0.7, 0.9]
    consensus = compute_consensus_sr(sr_values, "average")
    assert isinstance(consensus, float)
    assert 0.0 <= consensus <= 1.0

def test_compute_consensus_sr_weighted():
    sr_values = [0.8, 0.7, 0.9]
    consensus = compute_consensus_sr(sr_values, "weighted")
    assert isinstance(consensus, float)
    assert 0.0 <= consensus <= 1.0

def test_validate_weights():
    valid_weights = {"PHS": 0.25, "SYM": 0.20, "VAL": 0.20, "EMO": 0.20, "FX": 0.15}
    validate_weights(valid_weights)  # Should not raise exception

def test_validate_metrics():
    valid_metrics = {"PHS": 0.8, "SYM": 0.7, "VAL": 0.9, "EMO": 0.6, "FX": 0.8}
    validate_metrics(valid_metrics)  # Should not raise exception

def test_get_weight_profile():
    default_profile = get_weight_profile("default")
    assert isinstance(default_profile, dict)
    assert "PHS" in default_profile
    
    logical_profile = get_weight_profile("logical")
    assert isinstance(logical_profile, dict)
    assert "PHS" in logical_profile

def test_compute_sr_trace(sample_metrics):
    trace = compute_sr_trace("Ana", sample_metrics)
    assert isinstance(trace, SRTrace)
    assert trace.persona == "Ana"
    assert 0.0 <= trace.sr_value <= 1.0

def test_compute_sr_trace_with_context(sample_metrics):
    trace = compute_sr_trace("Ana", sample_metrics, context=".audit")
    assert isinstance(trace, SRTrace)
    assert trace.context == ".audit"

def test_batch_compute_sr_traces(multi_persona_metrics):
    traces = batch_compute_sr_traces(multi_persona_metrics)
    assert isinstance(traces, list)
    assert len(traces) == 3
    for trace in traces:
        assert isinstance(trace, SRTrace)

def test_analyze_sr_distribution():
    sr_values = [0.8, 0.7, 0.9, 0.6, 0.8]
    analysis = analyze_sr_distribution(sr_values)
    assert isinstance(analysis, dict)
    assert "mean" in analysis
    assert "std" in analysis

def test_generate_sr_report():
    traces = [
        SRTrace("Ana", 0.8, SRMetrics(0.8, 0.7, 0.9, 0.6, 0.8), DEFAULT_WEIGHTS),
        SRTrace("JayDen", 0.9, SRMetrics(0.9, 0.8, 0.7, 0.8, 0.7), DEFAULT_WEIGHTS)
    ]
    report = generate_sr_report(traces)
    assert isinstance(report, dict)
    assert "summary" in report

def test_sr_trace_to_dict():
    trace = SRTrace("Ana", 0.8, SRMetrics(0.8, 0.7, 0.9, 0.6, 0.8), DEFAULT_WEIGHTS)
    data = trace.to_dict()
    assert isinstance(data, dict)
    assert data["persona"] == "Ana"
    assert data["sr_value"] == 0.8

def test_default_weights():
    assert isinstance(DEFAULT_WEIGHTS, dict)
    assert "PHS" in DEFAULT_WEIGHTS
    assert "SYM" in DEFAULT_WEIGHTS
    assert "VAL" in DEFAULT_WEIGHTS
    assert "EMO" in DEFAULT_WEIGHTS
    assert "FX" in DEFAULT_WEIGHTS

def test_weight_profiles():
    assert isinstance(WEIGHT_PROFILES, dict)
    assert "default" in WEIGHT_PROFILES
    assert "logical" in WEIGHT_PROFILES
    assert "creative" in WEIGHT_PROFILES
    assert "memory" in WEIGHT_PROFILES
    assert "consensus" in WEIGHT_PROFILES 