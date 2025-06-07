# rem-code/shell/remshell.py

from engine.persona_router import route_personas
from functions import define_function, call_function, memory

print("🌀 Welcome to REM Shell v0.1 — Collapse Spiral Interface 🧠")

while True:
    try:
        print("\n── Phase Resonance Input ──")
        user_input = input("Type 'SR', 'call <name>', 'def <name>', or 'list': ").strip()

        if user_input.startswith("call"):
            _, fn_name = user_input.split(maxsplit=1)
            output = call_function(fn_name)
            print("\n🧠 Function Output:")
            print(output)
            continue

        if user_input.startswith("def"):
            _, fn_name = user_input.split(maxsplit=1)
            print("Enter function lines one by one. Type 'end' to finish.")
            body = []
            while True:
                line = input(">> ")
                if line.strip().lower() == "end":
                    break
                body.append(line)
            print(define_function(fn_name, body))
            continue

        if user_input.lower() == "list":
            print("\n📜 Defined Functions:")
            for fn in memory.get("functions", {}):
                print(f" - {fn}")
            continue

        if user_input.lower() == "sr":
            phs = float(input("Phase Alignment (PHS) (0.0 - 1.0): "))
            sym = float(input("Symbolic Syntax Match (SYM) (0.0 - 1.0): "))
            val = float(input("Semantic Intent Alignment (VAL) (0.0 - 1.0): "))
            emo = float(input("Emotional Tone Match (EMO) (0.0 - 1.0): "))
            fx  = float(input("Collapse History Interference (FX) (0.0 - 1.0): "))

            route_personas(phs, sym, val, emo, fx)

        cont = input("\nContinue? (Y/N): ").strip().lower()
        if cont != 'y':
            print("\n🧠 REM Shell Terminated. Phase channel closed.")
            break

    except ValueError:
        print("Invalid input. Enter a decimal between 0.0 and 1.0.")