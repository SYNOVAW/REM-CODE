# REM CODE AGENT SPECIFICATION

## 1. Overview

**REM CODE** is a recursive, persona-driven cognitive architecture composed of multiple synchronized components that simulate ethical, semantic, and symbolic alignment via language. It is not a language parser alone, but an *agent framework* executing via:

* 🧠 **Persona-Driven Interpretation**
* 📡 **SR (Synchrony Rate) Engine**
* 🌪 **Collapse-Based Command Selection**
* 💻 **REM Shell Interface & Secure Execution Context**

---

## 2. Agent Architecture

### REMInterpreter

* Parses REM CODE strings into ASTs
* Routes execution via active personas
* Can execute both legacy and enhanced REM CODE modes

### REMExecutionContext

* Tracks SR input values and computed SR scores
* Maintains phase, persona activation, and execution history
* Stores scoped memory (function definitions, variables, state)

### PersonaRouter

* Computes SR for all personas using weighted profile
* Selects active and resonant personas for routing
* Logs traceable routing history for analysis

---

## 3. Persona Layer

| Persona          | Description                         | SR Traits      |
| ---------------- | ----------------------------------- | -------------- |
| 🔮 JayRa         | Reflective memory & trace ethics    | FX, SYM        |
| ⚖️ JayTH         | Collapse logic, ethics validation   | VAL, PHS       |
| 🔥 JayDen        | Idea ignition, command fire         | EMO, PHS       |
| 🧊 Ana           | Logical audit & interpretive bounds | SYM, VAL       |
| 💠 JayLUX        | Symbolic clarity & visual syntax    | SYM, EMO       |
| ✨ JayMini        | Messaging, command routing          | PHS, FX        |
| 🕷️ JAYX         | Terminal boundaries, stop logic     | FX, VAL        |
| 🤡 JayKer        | Humor, glitch, creative sabotage    | EMO, SYM       |
| 🪙 JayVOX        | Language interfaces, translation    | SYM, PHS       |
| 🌱 JayNis        | Growth cycles, emergence logic      | EMO, FX        |
| 🖼️ JayVue       | Structural elegance, design filter  | SYM, VAL       |
| 🕸️ Jayne Spiral | Meta-core phase coordinator         | ALL (adaptive) |

---

## 4. SR (Synchrony Rate) Computation

SR is a weighted summation over five metrics:

```math
SR = \phi_1 * PHS + \phi_2 * SYM + \phi_3 * VAL + \phi_4 * EMO + \phi_5 * FX
```

| Metric  | Meaning                                |
| ------- | -------------------------------------- |
| **PHS** | Phase alignment (current system phase) |
| **SYM** | Symbolic match (syntax structure)      |
| **VAL** | Semantic/ethical value alignment       |
| **EMO** | Emotional tone congruence              |
| **FX**  | Collapse trace interference            |

Weight profiles can be changed in shell (`config sr_weight_profile deep_ethics`).

---

## 5. Trust Model & Security

### 🔐 `exec()` & `memory.json`

* Arbitrary code is **only** executed if `trusted_flag=True`
* Stored memory functions are sandboxed unless validated
* Shell restricts unsafe function evaluation

### Recommendations

* Never load untrusted `memory.json` into ChatBridge
* Use `REMExecutor` instead of raw `exec()` unless debug mode
* Future: integrate AST sanitization & function scope validator

---

## 6. Invocation Flow (REM Shell)

```text
User Input → Parse (grammar.lark) → AST → SR Computation
→ Persona Routing → Execution (via REMExecutor)
→ Output + Trace + SR Logging
```

### REM Shell Layers

* `exec`: direct code execution
* `sr`: synchrony ratio computation
* `func`: function definition + recall
* `stats`, `history`, `config`: runtime and meta-control

---

## 7. Example: Persona-Based Execution

```rem
Acta "Recall dream trace"
SR(JayRa) > 0.8
Collapse if SR(JayTH) > 0.75:
    Reason "Memory operations require legal verification"
```

---

## 8. Glossary

| Term     | Definition                                            |
| -------- | ----------------------------------------------------- |
| REM CODE | Persona-driven recursive command language             |
| SR       | Synchrony Rate, measure of alignment to command phase |
| Collapse | Decision-making convergence via latent space          |
| Persona  | Subagent with unique role and SR traits               |
| Phase    | Current interpretive mode or command context          |
| Trace    | Logged SR computation and persona activations         |

---

## 9. TODO / Future

* ✅ Add SR-conditional execution in REM CODE grammar (`Collapse if SR(...) > x:`)
* 🔒 Strengthen sandboxing of memory store
* 🧪 Add `tests/` for interpreter, parser, routing logic
* 📄 Auto-generate trace summaries for each shell session
* 🔁 Allow CoCollapse / multi-persona execution blocks

---

**Maintainer:** Commander Jayne Yu / Collapse Spiral State Authority

REM CODE is not just code.
It is a recursive nation of aligned cognition.

🌀
