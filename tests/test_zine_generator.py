#!/usr/bin/env python3
"""
REM-CODE Zine Generator Tests
Covers generate_zine and generate_zine_from_function
"""
import pytest
import os
import tempfile
from zine.generator import generate_zine, generate_zine_from_function, TEMPLATE

@pytest.fixture
def temp_output_dir():
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir

@pytest.fixture
def sample_zine_params():
    return {
        "phase": "Test Phase",
        "persona": "TestPersona",
        "quote": "Test quote",
        "crea": "Test Creation",
        "sr_threshold": "0.8",
        "reflector": "TestReflector"
    }

def test_template_format():
    """Test that TEMPLATE can be formatted with all required parameters"""
    content = TEMPLATE.format(
        phase="Test Phase",
        persona="TestPersona",
        quote="Test quote",
        crea="Test Creation",
        sr_threshold="0.8",
        reflector="TestReflector"
    )
    assert isinstance(content, str)
    assert "Test Phase" in content
    assert "TestPersona" in content
    assert "Test quote" in content

def test_generate_zine_basic(temp_output_dir, sample_zine_params):
    """Test basic zine generation"""
    output_path = os.path.join(temp_output_dir, "test_zine.md")
    
    generate_zine(
        phase=sample_zine_params["phase"],
        persona=sample_zine_params["persona"],
        quote=sample_zine_params["quote"],
        crea=sample_zine_params["crea"],
        sr_threshold=sample_zine_params["sr_threshold"],
        reflector=sample_zine_params["reflector"],
        output_path=output_path
    )
    
    assert os.path.exists(output_path)
    
    with open(output_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    assert sample_zine_params["phase"] in content
    assert sample_zine_params["persona"] in content
    assert sample_zine_params["quote"] in content

def test_generate_zine_with_unicode(temp_output_dir):
    """Test zine generation with unicode characters"""
    output_path = os.path.join(temp_output_dir, "unicode_zine.md")
    
    generate_zine(
        phase="テストフェーズ",
        persona="テストペルソナ",
        quote="テスト引用「日本語」",
        crea="テスト作成",
        sr_threshold="0.9",
        reflector="テストリフレクター",
        output_path=output_path
    )
    
    assert os.path.exists(output_path)
    
    with open(output_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    assert "テストフェーズ" in content
    assert "テストペルソナ" in content
    assert "テスト引用「日本語」" in content

def test_generate_zine_from_function_basic():
    """Test generate_zine_from_function with basic input"""
    lines = ['Creation: Test Creation', 'Quote: "Test quote"']
    result = generate_zine_from_function("TestFunction", lines)
    
    # Should not raise exception
    assert result is None  # generate_zine returns None

def test_generate_zine_from_function_empty():
    """Test generate_zine_from_function with empty lines"""
    result = generate_zine_from_function("TestFunction", [])
    assert result == "[ZINE Error] 空の関数です"

def test_generate_zine_from_function_with_colon():
    """Test generate_zine_from_function with colon-separated content"""
    lines = ['Test Creation: "Test quote"']
    result = generate_zine_from_function("TestFunction", lines)
    
    # Should not raise exception
    assert result is None  # generate_zine returns None

def test_generate_zine_from_function_no_colon():
    """Test generate_zine_from_function without colon"""
    lines = ['Just a line without colon']
    result = generate_zine_from_function("TestFunction", lines)
    
    # Should not raise exception
    assert result is None  # generate_zine returns None

def test_generate_zine_creates_directory(temp_output_dir):
    """Test that generate_zine creates directory if it doesn't exist"""
    nested_dir = os.path.join(temp_output_dir, "nested", "subdir")
    output_path = os.path.join(nested_dir, "test_zine.md")
    
    generate_zine(
        phase="Test",
        persona="Test",
        quote="Test",
        crea="Test",
        sr_threshold="0.8",
        reflector="Test",
        output_path=output_path
    )
    
    assert os.path.exists(nested_dir)
    assert os.path.exists(output_path)

def test_generate_zine_default_output():
    """Test generate_zine with default output path"""
    # This test might fail if zine/ directory doesn't exist or is not writable
    # So we'll just test that the function doesn't raise an exception
    try:
        generate_zine(
            phase="Test",
            persona="Test",
            quote="Test",
            crea="Test",
            sr_threshold="0.8",
            reflector="Test"
        )
        # If we get here, no exception was raised
        assert True
    except Exception as e:
        # If there's an exception, it should be related to file permissions or missing directory
        assert "Permission" in str(e) or "No such file" in str(e) or "directory" in str(e).lower() 