#!/usr/bin/env python3
"""
REM-CODE REM Executor Extended Tests
Covers REMExecutor execution methods and global functions
"""
import pytest
from engine.rem_executor import (
    REMExecutor, REMExecutionContext, create_executor, create_context,
    execute, execute_function, compare, flatten_statements
)

@pytest.fixture
def context():
    return REMExecutionContext()

@pytest.fixture
def executor(context):
    return REMExecutor(context)

def test_execution_context_init(context):
    assert isinstance(context, REMExecutionContext)
    assert isinstance(context.variables, dict)
    assert isinstance(context.functions, dict)
    assert isinstance(context.personas, dict)

def test_execution_context_log(context):
    context.log("Test message")
    assert "Test message" in context.execution_log

def test_execution_context_add_signature(context):
    context.add_signature("Test content", "Ana", "Test reason")
    assert len(context.signature_log) == 1
    assert context.signature_log[0]["content"] == "Test content"

def test_execution_context_set_persona_sr(context):
    context.set_persona_sr("Ana", 0.8)
    assert context.persona_sr["Ana"] == 0.8

def test_execution_context_get_persona_sr(context):
    context.set_persona_sr("Ana", 0.8)
    sr = context.get_persona_sr("Ana")
    assert sr == 0.8

def test_execution_context_get_persona_sr_with_context(context):
    context.set_persona_sr("Ana", 0.8)
    context.set_persona_sr("JayTH", 0.9)
    
    # Test function-specific SR
    sr_audit = context.get_persona_sr("Ana", ".audit")
    assert sr_audit > 0.8
    
    # Test memory-contextualized SR
    sr_memory = context.get_persona_sr("Ana", "@memory")
    assert sr_memory < 0.8
    
    # Test inter-persona correlation
    sr_corr = context.get_persona_sr("Ana", "|JayTH")
    assert 0.8 <= sr_corr <= 0.9

def test_executor_init(executor):
    assert isinstance(executor, REMExecutor)
    assert executor.context is not None

def test_executor_execute_phase(executor):
    statements = [("phase", "TestPhase", [("simple_call", "print", ["Hello"])])]
    result = executor.execute(statements)
    assert isinstance(result, list)
    assert len(result) > 0

def test_executor_execute_invoke(executor):
    statements = [("invoke", ["Ana", "JayDen"], [("simple_call", "print", ["Hi"])])]
    result = executor.execute(statements)
    assert isinstance(result, list)
    assert len(result) > 0

def test_executor_execute_collapse(executor):
    statements = [("collapse", ("sr_condition", "Ana", ">", 0.5), [("simple_call", "print", ["Collapse"])])]
    result = executor.execute(statements)
    assert isinstance(result, list)

def test_executor_execute_elapse(executor):
    statements = [("elapse", ("sr_condition", "Ana", ">", 0.5), [("simple_call", "print", ["Elapse"])])]
    result = executor.execute(statements)
    assert isinstance(result, list)

def test_executor_execute_sync(executor):
    statements = [("sync", [("simple_call", "print", ["Sync"])])]
    result = executor.execute(statements)
    assert isinstance(result, list)

def test_executor_execute_cocollapse(executor):
    statements = [("cocollapse", ["Ana", "JayDen"], ("sr_condition", "Ana", ">", 0.5), [("simple_call", "print", ["CoCollapse"])])]
    result = executor.execute(statements)
    assert isinstance(result, list)

def test_executor_execute_persona_call(executor):
    statements = [("persona_call", "Ana", "Dic", ["Hello from Ana"])]
    result = executor.execute(statements)
    assert isinstance(result, list)

def test_executor_execute_latin_call(executor):
    statements = [("latin_call", "Dic", ["Hello"])]
    result = executor.execute(statements)
    assert isinstance(result, list)

def test_executor_execute_simple_call(executor):
    statements = [("simple_call", "print", ["Hello"])]
    result = executor.execute(statements)
    assert isinstance(result, list)

def test_executor_execute_set(executor):
    statements = [("set", "x", 42)]
    result = executor.execute(statements)
    assert isinstance(result, list)
    assert executor.context.variables["x"] == 42

def test_executor_execute_use(executor):
    executor.context.variables["x"] = 42
    statements = [("use", "x")]
    result = executor.execute(statements)
    assert isinstance(result, list)

def test_executor_execute_store(executor):
    statements = [("store", "key", "value")]
    result = executor.execute(statements)
    assert isinstance(result, list)

def test_executor_execute_sign(executor):
    statements = [("sign", "content", "Ana", "reason")]
    result = executor.execute(statements)
    assert isinstance(result, list)

def test_executor_execute_cosign(executor):
    statements = [("cosign", ["Ana", "JayDen"], "content")]
    result = executor.execute(statements)
    assert isinstance(result, list)

def test_executor_execute_reason(executor):
    statements = [("reason", "Ana", "reason")]
    result = executor.execute(statements)
    assert isinstance(result, list)

def test_executor_execute_recall(executor):
    statements = [("recall", "key")]
    result = executor.execute(statements)
    assert isinstance(result, list)

def test_executor_execute_memoryset(executor):
    statements = [("memoryset", "key", "value")]
    result = executor.execute(statements)
    assert isinstance(result, list)

def test_executor_execute_phase_transition(executor):
    statements = [("phase_transition", "NewPhase")]
    result = executor.execute(statements)
    assert isinstance(result, list)

def test_executor_execute_describe(executor):
    statements = [("describe", "content")]
    result = executor.execute(statements)
    assert isinstance(result, list)

def test_executor_execute_narrate(executor):
    statements = [("narrate", "content")]
    result = executor.execute(statements)
    assert isinstance(result, list)

def test_executor_execute_visualize(executor):
    statements = [("visualize", "content")]
    result = executor.execute(statements)
    assert isinstance(result, list)

def test_executor_execute_function_def(executor):
    statements = [("function_def", "test_func", ["param"], [("simple_call", "print", ["Hello"])])]
    result = executor.execute(statements)
    assert isinstance(result, list)

def test_executor_evaluate_sr_condition(executor):
    # Test SR condition evaluation
    condition = ("sr_condition", "Ana", ">", 0.5)
    result = executor._evaluate_sr_condition(condition)
    assert isinstance(result, bool)

def test_executor_evaluate_sr_expression(executor):
    # Test SR expression evaluation
    sr_expr = ("sr_expr", "Ana", None)
    result = executor._evaluate_sr_expression(sr_expr)
    assert isinstance(result, float)

def test_executor_compare_values(executor):
    assert executor._compare_values(0.8, ">", 0.5) is True
    assert executor._compare_values(0.3, "<", 0.5) is True
    assert executor._compare_values(0.5, "==", 0.5) is True

def test_executor_resolve_value(executor):
    assert executor._resolve_value(42) == 42
    assert executor._resolve_value("test") == "test"
    assert executor._resolve_value(None) is None

def test_global_create_executor():
    executor = create_executor()
    assert isinstance(executor, REMExecutor)

def test_global_create_context():
    context = create_context()
    assert isinstance(context, REMExecutionContext)

def test_global_execute():
    statements = [("simple_call", "print", ["Hello"])]
    result = execute(statements)
    assert isinstance(result, list)

def test_global_execute_function():
    lines = ["print('Hello')"]
    result = execute_function(lines, 0.8)
    assert isinstance(result, list)

def test_global_compare():
    assert compare(0.8, ">", 0.5) is True
    assert compare(0.3, "<", 0.5) is True
    assert compare(0.5, "==", 0.5) is True

def test_global_flatten_statements():
    nested = [("phase", "Test", [("simple_call", "print", ["Hello"])])]
    flattened = flatten_statements(nested)
    assert isinstance(flattened, list) 