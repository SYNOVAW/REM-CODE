#!/usr/bin/env python3
"""
REM-CODE Functions Manager Tests
Covers REMFunctionManager and global function APIs
"""
import pytest
from functions.functions import (
    REMFunctionManager, get_global_manager, define_function, call_function,
    list_functions, generate_ast, generate_zine, save_memory
)

def test_manager_init_and_memory():
    manager = REMFunctionManager()
    assert isinstance(manager, REMFunctionManager)
    manager.save_memory()
    manager.load_memory()
    assert isinstance(manager.functions, dict)

def test_define_and_list_function():
    manager = REMFunctionManager()
    result = manager.define_function("test_func", ["def test_func():", "    return 42"])
    assert "test_func" in manager.functions
    funcs = manager.list_functions()
    assert "test_func" in funcs

def test_call_function():
    manager = REMFunctionManager()
    manager.define_function("test_func2", ["def test_func2():", "    return 99"])
    result = manager.call_function("test_func2", sr_value=0.8)
    assert isinstance(result, list)

def test_generate_ast():
    manager = REMFunctionManager()
    manager.define_function("test_func3", ["def test_func3():", "    return 1"])
    ast = manager.generate_ast("test_func3")
    assert isinstance(ast, dict)

def test_generate_zine():
    manager = REMFunctionManager()
    manager.define_function("test_func4", ["def test_func4():", "    return 2"])
    zine = manager.generate_zine("test_func4")
    assert zine is None or isinstance(zine, str)

def test_delete_function():
    manager = REMFunctionManager()
    manager.define_function("test_func5", ["def test_func5():", "    return 3"])
    msg = manager.delete_function("test_func5")
    assert "deleted" in msg or "not found" in msg

def test_search_functions():
    manager = REMFunctionManager()
    manager.define_function("searchable_func", ["def searchable_func():", "    return 4"])
    results = manager.search_functions("searchable")
    assert any("searchable_func" in r for r in results)

def test_get_function_stats():
    manager = REMFunctionManager()
    stats = manager.get_function_stats()
    assert isinstance(stats, dict)

def test_export_import_functions(tmp_path):
    manager = REMFunctionManager()
    manager.define_function("export_func", ["def export_func():", "    return 5"])
    export_path = tmp_path / "exported.json"
    msg = manager.export_functions(str(export_path))
    assert "exported" in msg or "Exported" in msg
    msg2 = manager.import_functions(str(export_path), overwrite=True)
    assert "imported" in msg2 or "Imported" in msg2

def test_global_manager_and_apis():
    gm = get_global_manager()
    assert isinstance(gm, REMFunctionManager)
    define_function("global_func", ["def global_func():", "    return 6"])
    funcs = list_functions()
    assert "global_func" in funcs
    ast = generate_ast("global_func")
    assert isinstance(ast, (dict, list))
    zine = generate_zine("global_func")
    assert zine is None or isinstance(zine, str)
    call_result = call_function("global_func", sr_value=0.7)
    assert isinstance(call_result, list)
    save_memory() 