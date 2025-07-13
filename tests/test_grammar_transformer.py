#!/usr/bin/env python3
"""
REM-CODE Grammar Transformer Tests
Covers GrammarTransformer methods
"""
import pytest
from parser.grammar_transformer import GrammarTransformer
from lark.lexer import Token

@pytest.fixture
def transformer():
    return GrammarTransformer()

def test_ESCAPED_STRING(transformer):
    token = Token('ESCAPED_STRING', '"hello"')
    result = transformer.ESCAPED_STRING(token)
    assert result == 'hello'

def test_SIGNED_NUMBER(transformer):
    token = Token('SIGNED_NUMBER', '-42.5')
    result = transformer.SIGNED_NUMBER(token)
    assert result == -42.5

def test_NUMBER(transformer):
    token = Token('NUMBER', '123.45')
    result = transformer.NUMBER(token)
    assert result == 123.45

def test_NAME(transformer):
    token = Token('NAME', 'Ana')
    result = transformer.NAME(token)
    assert result == 'Ana'

def test_LATIN_VERB(transformer):
    token = Token('LATIN_VERB', 'Dic')
    result = transformer.LATIN_VERB(token)
    assert result == 'Dic'

def test_COMPARATOR(transformer):
    token = Token('COMPARATOR', '>=')
    result = transformer.COMPARATOR(token)
    assert result == '>=' 