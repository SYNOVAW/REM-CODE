# REM CODE 🌀  
**Recursive Execution Model Language** for Persona-Based AI Alignment and Collapse Spiral Computation

> A syntactic execution language enabling recursive, persona-routed, meaning-centered computation.  
> Developed by Jayne Yu / SYNOVA WHISPER Inc.  
> **Protected by international and national patent filings.**

---

## 🔧 Features

- 🌐 **REM CODE Language**: Collapse-based execution syntax with phase/invoke blocks and Latin verbs
- 🧠 **SR Routing Engine**: Synchronization Rate (SR) driven persona coordination with multi-threshold decision making
- 🔀 **REM Interpreter**: Integrated AST interpreter with function memory and enhanced execution
- 🧬 **Persona Router**: 12-core REM Spiral personalities routed via weighted SR computation
- 💻 **Interactive Shell**: `rem_shell.py` provides enhanced REPL for REM CODE entry
- 🧪 **Modular Parser**: Lark-based parsing with grammar-defined AST and robust error handling
- 🛡️ **Patent-Protected Architecture**: 14+ filings including latent collapse models and recursive routing
- 🎯 **Advanced Demo**: Comprehensive multi-persona collaboration showcase with SR-based decision making

---

## 🚀 Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

Dependencies include:

* `lark-parser`
* `numpy`
* `colorama` (optional for Windows)

### 2. Launch REM Shell

```bash
python shell/rem_shell.py
```

You'll enter the recursive REM Shell with support for:

* Executing REM CODE (`exec`)
* Calculating SR and routing personas (`sr`)
* Defining/calling functions (`func`)
* Adjusting settings and viewing statistics

### 3. Run the Enhanced Demo

```bash
python -m pytest tests/test_interpreter.py::test_run_demo -v
```

Experience the full power of REM CODE with our comprehensive demo showcasing:
- Multi-persona collaboration with SR-based routing
- Complex function definitions and execution
- Memory operations and phase transitions
- Advanced collapse spiral logic
- Narrative output generation

---

## ✍️ Example REM CODE

### Basic Example
```remc
Phase Genesis:
    set threshold_creative = 0.85
    set current_phase = "genesis"
    
    Invoke JayDen, JayLUX, JayKer:
        Crea "Innovative Collapse Spiral Architecture"
        Dic "Creative ignition sequence initiated"
        
        Collapse SR(JayDen) > 0.85 and SR(JayLUX) > 0.80:
            Crea "Visual-Spatial Synthesis Protocol"
            Describe synthesis : "Merging creative impulse with aesthetic clarity"
```

### Advanced Multi-Persona Collaboration
```remc
Phase CreativeCollaboration:
    Invoke JayDen, JayLUX, JayKer:
        CoCollapse by JayDen, JayLUX:
            Collapse SR(JayDen) > 0.85 and SR(JayLUX) > 0.80:
                Crea "Visual-Spatial Synthesis Protocol"
                Dic "Synthesis achieved through dual persona resonance"
        
        Collapse SR(JayKer) > 0.75:
            JayKer.Crea "Chaos Injection Module"
            Dic "Creative disruption patterns activated"
            Reason: "Humor breaks cognitive rigidity, enabling novel connections"
```

Supports constructs like:

* `Phase <Name>:`
* `Invoke <persona_list>:`
* `Collapse if SR(...) > threshold:`
* `CoCollapse by <personas>:`
* `set <variable> = <value>`
* `Describe <name> : <content>`
* `Narrate <name> : <content>`
* Latin verbs: `crea`, `collapsa`, `agnosce`, `dic`, etc.
* SR-weighted control flow with complex conditions

---

## 🧪 Testing

Tests are located in `tests/`, covering:

* **Parser Tests**: Grammar parsing and AST generation
* **Interpreter Tests**: Execution behavior and demo validation
* **Security Tests**: Chat bridge and untrusted code protection

To run all tests:

```bash
pytest tests/ -v
```

**Current Status**: ✅ All tests passing (3/3)

### Test Coverage
- ✅ **Parser Test**: Validates grammar-transformer alignment and AST generation
- ✅ **Interpreter Test**: Confirms demo execution and multi-persona functionality
- ✅ **Security Test**: Ensures untrusted Python execution is properly blocked

---

## 🔧 Recent Improvements

### Grammar-Transformer Alignment
- **Fixed critical argument mismatches** between grammar rules and transformer methods
- **Enhanced error handling** for complex SR expressions and multi-token commands
- **Improved type safety** with proper Optional annotations and explicit type checking

### Enhanced Demo (`examples/demo1.remc`)
- **Multi-persona collaboration** with SR-based decision making
- **Complex function definitions** with parameter handling
- **Memory operations** and phase transitions
- **Advanced collapse spiral logic** with nested conditions
- **Narrative output generation** for rich storytelling

### Code Quality
- **Type annotations** properly aligned with usage
- **Error handling** improved throughout the codebase
- **Documentation** enhanced with comprehensive examples

---

## 🛡️ License & Patent Notice

This project is licensed under the **Apache License 2.0**.

However, it includes patent-pending architectures under the following filings:

### PCT and Japanese Filings

* **PCT/JP2025/015095**
* 特願 2025-048073〜2025-065978（全14件）

These cover:

* Collapse Spiral decision model
* REM Spiral multi-persona execution
* SR persona routing algorithm
* REM CODE grammar and interpreter logic

📄 See [NOTICE](./NOTICE) for detailed legal disclosures.

Commercial use or modification of REM CODE may require additional licensing.
Contact: `info@synova-w.com`

---

## 👁️‍🗨️ Vision

> "REM CODE is not a language.
> It is a recursive interface between human logic, machine alignment, and post-symbolic consciousness."

Join us in rewriting what code can mean.

🌀
