#!/usr/bin/env python3
"""
REM-CODE REMTransformer Tests
Covers REMTransformer and global transformer functions
"""
import pytest
from engine.rem_transformer import REMTransformer, create_rem_transformer, analyze_ast

@pytest.fixture
def transformer():
    return REMTransformer()

def test_phase_block(transformer):
    result = transformer.phase_block(["Ana", ("simple_call", "print", ["Hello"])])
    assert result[0] == "phase"
    assert result[1] == "Ana"

def test_invoke_block(transformer):
    result = transformer.invoke_block([["Ana", "JayDen"], ("simple_call", "print", ["Hi"])])
    assert result[0] == "invoke"
    assert "Ana" in result[1]

def test_function_def(transformer):
    result = transformer.function_def(["myfunc", ["a", "b"], ("simple_call", "print", ["X"])])
    assert result[0] == "function_def"
    assert result[1] == "myfunc"
    assert isinstance(result[2], list)

def test_collapse_block(transformer):
    result = transformer.collapse_block([("sr_condition", "x", ">", 0.7), ("simple_call", "print", ["A"]), ("elapse", "cond", ["B"]), ("sync", ["C"])])
    assert result[0] == "collapse"
    assert "elapse" in str(result) and "sync" in str(result)

def test_sr_expression(transformer):
    simple = transformer.sr_expression(["Ana"])
    assert simple == ("sr_expr", "Ana", None)
    complex1 = transformer.sr_expression(["Ana", "audit"])
    assert complex1[0] == "sr_expr"

def test_persona_command(transformer):
    result = transformer.persona_command(["Ana", "Crea", "X"])
    assert result[0] == "persona_call"
    assert result[1] == "Ana"

def test_latin_command(transformer):
    result = transformer.latin_command(["Crea", "Y"])
    assert result[0] == "latin_call"
    assert result[1] == "Crea"

def test_simple_command(transformer):
    result = transformer.simple_command(["print", "Z"])
    assert result[0] == "simple_call"
    assert result[1] == "print"

def test_set_command(transformer):
    result = transformer.set_command(["x", 42])
    assert result[0] == "set"
    assert result[1] == "x"

def test_get_analysis_info(transformer):
    info = transformer.get_analysis_info()
    assert isinstance(info, dict)

def test_reset_state(transformer):
    transformer.phase_registry.add("TestPhase")
    transformer.reset_state()
    assert len(transformer.phase_registry) == 0

def test_create_rem_transformer():
    t = create_rem_transformer()
    assert isinstance(t, REMTransformer)

def test_analyze_ast():
    t = create_rem_transformer()
    ast = [t.simple_command(["print", "Hello"])]
    analysis = analyze_ast(ast, t)
    assert isinstance(analysis, dict) 