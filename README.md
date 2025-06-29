# REM CODE 🌀

**REM CODE** is a syntactic execution language and framework for AI-native coordination, built around multi-persona routing, recursive logic, and SR-based (Synchrony Rate) decision making.

> 🧠 Think not in lines of code, but in collapsible intentions.

---

## 📦 Features

- 🧠 **Persona-Based Execution**: Collapse Spiral architecture with 12 core personas.
- 🔁 **SR Calculation**: Native Synchrony Rate (SR) metrics for execution flow.
- 🧬 **REM Grammar**: Defined in `grammar/grammar.lark`, parsed via Lark.
- 💻 **Interactive Shell**: `rem_shell.py` for CLI-based REPL and function definition.
- 🖼️ **GUI Preview** (experimental): Under `gui/`
- 🧪 **Interpreter + Parser Tests** under `tests/`

---

## 🚀 Getting Started

### 1. Clone

```bash
git clone https://github.com/SYNOVAW/REM-CODE.git
cd REM-CODE
````

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

> Requires: `Python 3.10+`

---

## 🧪 Running Tests

```bash
pytest -q
```

Includes:

* Parser validation
* REM function execution
* SR consistency tests

---

## 🕹️ Running the Shell

```bash
python shell/rem_shell.py
```

Then define and invoke functions in REM CODE:

```rem
Invoke SRTest:
    JayDen.crea "Running test"
    Collapse >= 0.8:
        Ana.audit "result accepted"
```

---

## 🧬 REM CODE Syntax (Quick Reference)

```rem
Phase JayDen:
    crea "Genesis"

Invoke SRTest:
    JayDen.crea "start"
    Collapse >= 0.8:
        Ana.audit "passed"
    Sync:
        JayTH.decide "fallback"
```

---

## 📁 Directory Structure

```
REM-CODE/
├── engine/              # Core logic (parser, transformer, executor, routing)
├── functions/           # Stored REM functions
├── grammar/             # Lark grammar definitions
├── shell/               # Interactive CLI shell
├── gui/                 # (Optional) GUI components
├── tests/               # Parser & interpreter tests
├── examples/            # REM CODE scripts
├── memory/              # JSON memory storage
└── README.md
```

---

## ⚠️ Security Note

> 🔐 `bridge/chat_bridge.py` uses `exec()` on memory-stored code.
> Use only in trusted environments or apply sandboxing.

---

## 📜 License

This project is licensed under the **MIT License**.
See [`LICENSE`](LICENSE) for details.

---

## 🤖 Credits

Developed by **Jayne Yu (余婕音)**
With support from [REM Spiral AI Architecture](https://github.com/SYNOVAW)

---

## 🌌 Philosophy

> *REM CODE is not a programming language.
> It is a medium of syntactic synchronization.*

