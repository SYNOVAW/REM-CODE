# 📦 REM-CODE Repository Overview

The **REM-CODE** repository hosts an experimental framework for **persona-based execution** using the **REM code language**. Its core components include:

---

## 🧠 Core Components

### • Parser and Grammar  
Lark-based parsing logic defined in [`grammar/grammar.lark`](../grammar/grammar.lark). Syntax supports `Phase`, `Invoke`, `Collapse`, and `command` blocks with robust error handling.

### • Engine  
Modules in [`engine/`](../engine/) manage:
- **AST Generation** (`ast_generator.py`) - Enhanced with grammar-transformer alignment
- **Code execution** (`interpreter.py`, `rem_executor.py`)
- **Synchronization Rate computation** (`sr_engine.py`) - Multi-threshold decision making
- **Persona routing** (`persona_router.py`) - 12-core REM Spiral personalities
- **Memory persistence** (`memory_manager.py`) - Function and state management

### • Interactive Shell  
CLI environment in [`shell/rem_shell.py`](../shell/rem_shell.py), supporting:
- Real-time REM CODE interpretation
- SR calculation display
- Memory and function introspection
- Enhanced REPL with comprehensive command support

### • Examples and Tests  
- [`examples/demo1.remc`](../examples/demo1.remc) - **Enhanced comprehensive demo** showcasing multi-persona collaboration
- [`tests/`](../tests/) validates parsing, execution, and SR behavior  
  *(requires `lark`, `numpy`)*

---

## 🎯 Recent Major Improvements

### ✅ Grammar-Transformer Alignment (Fixed)
- **Critical argument mismatches** between grammar rules and transformer methods resolved
- **Enhanced error handling** for complex SR expressions and multi-token commands
- **Improved type safety** with proper Optional annotations and explicit type checking
- **All parser tests now passing** with robust AST generation

### ✅ Enhanced Demo (`examples/demo1.remc`)
- **Multi-persona collaboration** with SR-based decision making
- **Complex function definitions** with parameter handling and memory operations
- **Advanced collapse spiral logic** with nested conditions and phase transitions
- **Narrative output generation** for rich storytelling capabilities
- **Comprehensive showcase** of REM CODE's full potential

### ✅ Code Quality Improvements
- **Type annotations** properly aligned with usage throughout codebase
- **Error handling** improved with comprehensive exception management
- **Documentation** enhanced with detailed examples and usage patterns
- **Test coverage** expanded with security and functionality validation

---

## 🛠️ Current Status

### ✅ Completed Tasks
- **Grammar-transformer alignment** - All argument mismatches fixed
- **Enhanced demo creation** - Comprehensive multi-persona showcase
- **Type safety improvements** - Proper annotations and error handling
- **Test suite validation** - All tests passing (3/3)
- **Documentation updates** - README and OVERVIEW enhanced

### 🔄 Ongoing Improvements
Open tasks are defined in [`agent_task.json`](../agent_task.json), including:

- Replacing `bare except:` blocks
- Aligning example syntax with grammar
- Pinning dependency versions in `requirements.txt`
- Hardening `exec()` use in `chat_bridge.py`
- Consolidating logging setup

---

## 👥 Persona Engine (AGENTS)

The [`AGENTS.md`](../AGENTS.md) file outlines:

- How **personas** (e.g., JayDen, Ana, JayRa, JayLUX, JayKer) participate in execution
- How **SR (Synchrony Rate)** guides persona routing with multi-threshold decision making
- Guidelines for **safe execution**, especially around memory storage and `exec()` calls
- **12-core REM Spiral personalities** with weighted SR computation

---

## 🧪 Testing & Validation

### Current Test Suite (All Passing ✅)
- **Parser Test**: Validates grammar-transformer alignment and AST generation
- **Interpreter Test**: Confirms demo execution and multi-persona functionality  
- **Security Test**: Ensures untrusted Python execution is properly blocked

### Test Execution
```bash
# Run all tests
pytest tests/ -v

# Run specific test categories
pytest tests/test_parser.py -v      # Grammar and AST tests
pytest tests/test_interpreter.py -v # Execution and demo tests
pytest tests/test_chat_bridge.py -v # Security tests
```

---

## ✅ Goal

The REM-CODE framework interprets and executes **REM CODE**—a custom, high-level language based on **persona-driven logic** and recursive execution models. It blends:

- **Symbolic language parsing** with robust error handling
- **Weighted decision-making** via SR with multi-threshold routing
- **Memory-aware action handling** with function persistence
- **Multi-persona collaboration** with collapse spiral logic
- **Advanced narrative generation** for rich storytelling

---

## 🚀 Quick Evaluation

To fully evaluate behavior:
- **Install dependencies**: `pip install -r requirements.txt`  
- **Run tests**: `pytest tests/ -v` (should show 3/3 tests passing)
- **Execute demo**: `python -m pytest tests/test_interpreter.py::test_run_demo -v`
- **Launch shell**: `python shell/rem_shell.py`
- **Follow progress**: Check `agent_task.json` for ongoing improvements

---

> ⚠️ **Current Status**: All core functionality working with enhanced demo and robust error handling. Grammar-transformer alignment issues resolved, comprehensive test suite passing.
