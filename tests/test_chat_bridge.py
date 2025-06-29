import pathlib
import sys
import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

try:
    import numpy  # noqa: F401
    import lark  # noqa: F401
except ImportError:
    pytest.skip("Required module missing", allow_module_level=True)

from bridge.chat_bridge import REMChatBridge, REMFunction, ChatContext

def test_untrusted_python_execution_blocked():
    bridge = REMChatBridge(trusted=False)
    func = REMFunction(name="test_func", description="", code="def test_func():\n    return 'ok'")
    context = ChatContext()
    result = bridge.execute_rem_function(func, context)
    assert not result["success"]
    assert result["error"] == "Untrusted mode: Python execution disabled"

