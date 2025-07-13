#!/usr/bin/env python3
"""
REM-CODE Import and Dependency Test Suite
Tests all modules to ensure imports work correctly after reorganization
"""

import sys
import traceback
import importlib
from pathlib import Path

def test_import(module_name, description=""):
    """Test if a module can be imported successfully"""
    try:
        importlib.import_module(module_name)
        print(f"✅ {module_name:<40} {description}")
        return True
    except Exception as e:
        print(f"❌ {module_name:<40} ERROR: {str(e)}")
        if "--verbose" in sys.argv:
            traceback.print_exc()
        return False

def test_file_execution(file_path, description=""):
    """Test if a Python file can be executed (without actually running it)"""
    try:
        with open(file_path, 'r') as f:
            code = f.read()
        compile(code, file_path, 'exec')
        print(f"✅ {str(file_path):<40} {description}")
        return True
    except Exception as e:
        print(f"❌ {str(file_path):<40} ERROR: {str(e)}")
        if "--verbose" in sys.argv:
            traceback.print_exc()
        return False

def main():
    print("=" * 80)
    print("REM-CODE Import and Dependency Test Suite")
    print("=" * 80)
    
    # Change to the REM-CODE directory
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root))
    
    total_tests = 0
    passed_tests = 0
    
    print("\n📦 Testing Core Modules:")
    print("-" * 50)
    
    # Test core modules
    core_modules = [
        ("constitutional", "Constitutional Framework"),
        ("engine", "REM Engine Components"),
        ("parser", "Grammar Parser"),
        ("shell", "Shell Interfaces"),
        ("gui", "GUI Module"),
        ("functions", "Core Functions"),
        ("bridge", "Chat Bridge"),
    ]
    
    for module, desc in core_modules:
        total_tests += 1
        if test_import(module, desc):
            passed_tests += 1
    
    print("\n🔍 Testing Constitutional Framework Components:")
    print("-" * 50)
    
    # Test constitutional submodules
    constitutional_modules = [
        ("constitutional.authority_validator", "Authority Validation"),
        ("constitutional.sr_threshold_checker", "SR Threshold Checking"),
        ("constitutional.signature_manager", "Signature Management"),
        ("constitutional.compliance_checker", "Compliance Checking"),
        ("constitutional.constitutional_engine", "Constitutional Engine"),
    ]
    
    for module, desc in constitutional_modules:
        total_tests += 1
        if test_import(module, desc):
            passed_tests += 1
    
    print("\n⚙️ Testing Engine Components:")
    print("-" * 50)
    
    # Test engine submodules
    engine_modules = [
        ("engine.ast_generator", "AST Generation"),
        ("engine.interpreter", "REM Interpreter"),
        ("engine.memory_manager", "Memory Management"),
        ("engine.persona_profile", "Persona Profiles"),
        ("engine.persona_router", "Persona Routing"),
        ("engine.rem_executor", "REM Executor"),
        ("engine.rem_transformer", "REM Transformer"),
        ("engine.sr_engine", "Synchrony Rate Engine"),
        ("engine.vocabulary_manager", "Vocabulary Management"),
    ]
    
    for module, desc in engine_modules:
        total_tests += 1
        if test_import(module, desc):
            passed_tests += 1
    
    print("\n🐚 Testing Shell Components:")
    print("-" * 50)
    
    # Test shell modules
    shell_modules = [
        ("shell.rem_shell", "Interactive Shell"),
        ("shell.rem_web_shell", "Web Shell Interface"),
    ]
    
    for module, desc in shell_modules:
        total_tests += 1
        if test_import(module, desc):
            passed_tests += 1
    
    print("\n📁 Testing Standalone Files:")
    print("-" * 50)
    
    # Test standalone files that should be importable/executable
    standalone_files = [
        (project_root / "rem_dashboard.py", "Dashboard"),
        (project_root / "tutorials" / "interactive_tutorial.py", "Interactive Tutorial"),
        (project_root / "gui" / "rem_gui.py", "GUI Application"),
        (project_root / "demos" / "constitutional_integration_demo.py", "Constitutional Demo"),
        (project_root / "demos" / "demo_dashboard.py", "Demo Dashboard"),
        (project_root / "demos" / "error_demo.py", "Error Demo"),
        (project_root / "demos" / "parse_demo.py", "Parse Demo"),
        (project_root / "demos" / "vocab_demo.py", "Vocabulary Demo"),
    ]
    
    for file_path, desc in standalone_files:
        if file_path.exists():
            total_tests += 1
            if test_file_execution(file_path, desc):
                passed_tests += 1
        else:
            print(f"⚠️  {str(file_path):<40} FILE NOT FOUND")
    
    print("\n🧪 Testing Entry Points:")
    print("-" * 50)
    
    # Test that entry point modules exist and are importable
    entry_points = [
        ("shell.rem_shell", "rem-code console entry"),
        ("shell.rem_web_shell", "rem-web console entry"),
        ("gui.rem_gui", "rem-gui console entry"),
        ("rem_dashboard", "rem-dashboard console entry"),
    ]
    
    for module, desc in entry_points:
        total_tests += 1
        if test_import(module, desc):
            passed_tests += 1
    
    print("\n📊 Checking Dependencies:")
    print("-" * 50)
    
    # Test required dependencies
    dependencies = [
        ("lark", "Lark Parser"),
        ("numpy", "NumPy"),
        ("rich", "Rich Terminal Library"),
        ("prompt_toolkit", "Prompt Toolkit"),
        ("pytest", "PyTest Testing Framework"),
    ]
    
    for dep, desc in dependencies:
        total_tests += 1
        if test_import(dep, desc):
            passed_tests += 1
    
    print("\n" + "=" * 80)
    print(f"TEST RESULTS: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED! Dependencies and imports are working correctly.")
        return 0
    else:
        failed = total_tests - passed_tests
        print(f"⚠️  {failed} tests failed. Please check the errors above.")
        print("\nTip: Run with --verbose flag for detailed error information")
        return 1

if __name__ == "__main__":
    sys.exit(main())