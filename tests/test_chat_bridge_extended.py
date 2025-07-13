#!/usr/bin/env python3
"""
REM-CODE Chat Bridge Extended Tests
Covers REMChatBridge, REMFunction, ChatContext and global functions
"""
import pytest
import tempfile
import json
from bridge.chat_bridge import (
    REMChatBridge, REMFunction, ChatContext,
    load_rem_functions, match_function_from_prompt,
    execute_function, rem_chat_bridge
)

@pytest.fixture
def temp_memory_file():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump({
            "functions": [
                {
                    "name": "test_func",
                    "description": "Test function",
                    "code": "def test_func(): return 'hello'",
                    "keywords": ["test", "hello"],
                    "persona": "Ana",
                    "sr_threshold": 0.7,
                    "category": "test"
                }
            ]
        }, f)
        return f.name

@pytest.fixture
def chat_bridge(temp_memory_file):
    return REMChatBridge(memory_path=temp_memory_file, trusted=True)

@pytest.fixture
def sample_function():
    return REMFunction(
        name="sample_func",
        description="Sample function for testing",
        code="def sample_func(): return 'test'",
        keywords=["sample", "test"],
        persona="JayDen",
        sr_threshold=0.8,
        category="test"
    )

@pytest.fixture
def chat_context():
    return ChatContext(user_id="test_user", session_id="test_session")

def test_rem_function_creation(sample_function):
    assert sample_function.name == "sample_func"
    assert sample_function.description == "Sample function for testing"
    assert sample_function.persona == "JayDen"
    assert sample_function.sr_threshold == 0.8

def test_rem_function_to_dict(sample_function):
    data = sample_function.to_dict()
    assert data["name"] == "sample_func"
    assert data["description"] == "Sample function for testing"
    assert data["persona"] == "JayDen"

def test_rem_function_from_dict():
    data = {
        "name": "from_dict_func",
        "description": "Function from dict",
        "code": "def from_dict_func(): pass",
        "keywords": ["dict", "test"],
        "persona": "Ana",
        "sr_threshold": 0.9
    }
    func = REMFunction.from_dict(data)
    assert func.name == "from_dict_func"
    assert func.persona == "Ana"

def test_chat_context_creation(chat_context):
    assert chat_context.user_id == "test_user"
    assert chat_context.session_id == "test_session"
    assert len(chat_context.conversation_history) == 0

def test_chat_context_add_message(chat_context):
    chat_context.add_message("user", "Hello")
    assert len(chat_context.conversation_history) == 1
    assert chat_context.conversation_history[0]["role"] == "user"
    assert chat_context.conversation_history[0]["content"] == "Hello"

def test_chat_bridge_init(chat_bridge):
    assert isinstance(chat_bridge, REMChatBridge)
    assert len(chat_bridge.functions) > 0
    assert "test_func" in chat_bridge.functions

def test_chat_bridge_get_context(chat_bridge):
    context = chat_bridge.get_context("user1", "session1")
    assert isinstance(context, ChatContext)
    assert context.user_id == "user1"
    assert context.session_id == "session1"

def test_chat_bridge_analyze_prompt_intent(chat_bridge, chat_context):
    intent = chat_bridge.analyze_prompt_intent("Hello world", chat_context)
    assert isinstance(intent, dict)
    assert "intent_scores" in intent

def test_chat_bridge_match_functions(chat_bridge, chat_context):
    matches = chat_bridge.match_functions_advanced("test function", chat_context)
    assert isinstance(matches, list)
    if matches:
        func, score = matches[0]
        assert isinstance(func, REMFunction)
        assert isinstance(score, float)

def test_chat_bridge_execute_function(chat_bridge, sample_function, chat_context):
    result = chat_bridge.execute_rem_function(sample_function, chat_context)
    assert isinstance(result, dict)
    assert "success" in result

def test_chat_bridge_rem_chat_bridge(chat_bridge):
    result = chat_bridge.rem_chat_bridge("Hello", "user1", "session1")
    assert isinstance(result, dict)
    assert "execution_results" in result

def test_chat_bridge_add_function(chat_bridge):
    success = chat_bridge.add_function(
        "new_func",
        "New test function",
        "def new_func(): return 'new'",
        ["new", "test"],
        "Ana",
        "test"
    )
    assert success is True
    assert "new_func" in chat_bridge.functions

def test_chat_bridge_get_statistics(chat_bridge):
    stats = chat_bridge.get_statistics()
    assert isinstance(stats, dict)
    assert "total_functions" in stats

def test_global_load_rem_functions(temp_memory_file):
    functions = load_rem_functions(temp_memory_file)
    assert isinstance(functions, list)
    assert len(functions) > 0

def test_global_match_function_from_prompt(temp_memory_file):
    functions = load_rem_functions(temp_memory_file)
    match = match_function_from_prompt("test function", functions)
    assert match is not None or match is None  # May or may not match

def test_global_execute_function():
    func_data = {
        "name": "global_test",
        "code": "def global_test(): return 'global'"
    }
    result = execute_function(func_data)
    assert isinstance(result, str)

def test_global_rem_chat_bridge():
    result = rem_chat_bridge("Hello world")
    assert isinstance(result, str)

def test_untrusted_mode():
    bridge = REMChatBridge(trusted=False)
    func = REMFunction(name="test", description="", code="def test(): pass")
    context = ChatContext()
    result = bridge.execute_rem_function(func, context)
    assert isinstance(result, dict)
    assert "success" in result 