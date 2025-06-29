import pathlib
import sys
import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

try:
    import numpy  # noqa: F401
    import lark  # noqa: F401
except ImportError:
    pytest.skip("Required module missing", allow_module_level=True)

from engine.interpreter import REMInterpreter

def test_run_demo():
    base = pathlib.Path(__file__).resolve().parents[1]
    code_path = base / 'examples' / 'demo1.remc'
    code = code_path.read_text(encoding='utf-8')
    interpreter = REMInterpreter()
    results = interpreter.run_rem_code(code)
    assert isinstance(results, list)
    assert results

