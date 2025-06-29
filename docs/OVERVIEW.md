# 📦 REM-CODE Repository Overview

The **REM-CODE** repository hosts an experimental framework for **persona-based execution** using the **REM code language**. Its core components include:

---

## 🧠 Core Components

### • Parser and Grammar  
Lark-based parsing logic defined in [`grammar/grammar.lark`](../grammar/grammar.lark). Syntax supports `Phase`, `Invoke`, and `command` blocks.

### • Engine  
Modules in [`engine/`](../engine/) manage:
- Code execution (`interpreter.py`, `rem_executor.py`)
- Synchronization Rate computation (`sr_engine.py`)
- Persona routing (`persona_router.py`)
- Memory persistence (`memory_manager.py`)

### • Interactive Shell  
CLI environment in [`shell/rem_shell.py`](../shell/rem_shell.py), supporting:
- Real-time REM CODE interpretation
- SR calculation display
- Memory and function introspection

### • Examples and Tests  
- [`examples/`](../examples/) includes demonstration REM CODE files  
- [`tests/`](../tests/) validates parsing, execution, and SR behavior  
  *(requires `lark`, `numpy`)*

---

## 🛠️ Ongoing Improvements

Open tasks are defined in [`agent_task.json`](../agent_task.json), including:

- Replacing `bare except:` blocks
- Aligning example syntax with grammar
- Pinning dependency versions in `requirements.txt`
- Hardening `exec()` use in `chat_bridge.py`
- Consolidating logging setup

---

## 👥 Persona Engine (AGENTS)

The [`AGENTS.md`](../AGENTS.md) file outlines:

- How **personas** (e.g., JayDen, Ana, JayRa) participate in execution
- How **SR (Synchrony Rate)** guides persona routing
- Guidelines for **safe execution**, especially around memory storage and `exec()` calls

---

## ✅ Goal

The REM-CODE framework interprets and executes **REM CODE**—a custom, high-level language based on **persona-driven logic** and recursive execution models. It blends:

- Symbolic language parsing
- Weighted decision-making via SR
- Memory-aware action handling

---

> ⚠️ To fully evaluate behavior:
> - Install dependencies: `pip install -r requirements.txt`  
> - Run tests: `pytest tests/`  
> - Follow open issues and progress in `agent_task.json`
