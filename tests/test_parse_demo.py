#!/usr/bin/env python3
"""
REM-CODE Parse Demo Tests
Covers load_grammar, load_demo, parse_demo_code
"""
import pytest
import os
from parser import parse_demo

@pytest.fixture
def grammar_path():
    return "grammar/grammar.lark"

@pytest.fixture
def demo_path():
    return "examples/demo1.remc"

def test_load_grammar(grammar_path):
    grammar = parse_demo.load_grammar(grammar_path)
    assert isinstance(grammar, str)
    assert len(grammar) > 0

def test_load_demo(demo_path):
    code = parse_demo.load_demo(demo_path)
    assert isinstance(code, str)
    assert len(code) > 0

def test_parse_demo_code(monkeypatch, grammar_path, demo_path):
    # monkeypatch the file paths to ensure test isolation
    monkeypatch.setattr(parse_demo, "GRAMMAR_FILE", grammar_path)
    monkeypatch.setattr(parse_demo, "DEMO_FILE", demo_path)
    # Should not raise
    parse_demo.parse_demo_code() 