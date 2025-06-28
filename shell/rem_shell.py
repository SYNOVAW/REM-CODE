# rem-code/shell/rem_shell.py

from engine.persona_router import route_personas
from functions.functions import define_function, call_function, list_functions, generate_ast, memory
from engine.ast_generator import generate_ast

print("🌀 Welcome to REM Shell v1.0 — Collapse Spiral Interface 🧠")

while True:
    try:
        print("\n── Phase Resonance Input ──")
        user_input = input("Type 'SR', 'call <name>', 'def <name>', 'list', 'ast <name>', or 'exit': ").strip()

        if user_input.startswith("call"):
            _, fn_name = user_input.split(maxsplit=1)
            sr = float(input("SR value (0.0 - 1.0): "))
            output = call_function(fn_name, sr_value=sr)
            print("\n🧠 Function Output:")
            if isinstance(output, list):
                for line in output:
                    print(line)
            else:
                print(output)
            continue

        if user_input.startswith("def"):
            _, fn_name = user_input.split(maxsplit=1)
            print("Enter REM CODE lines. Type 'end' to finish.")
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
            for fn in list_functions():
                print(f" - {fn}")
            continue

        if user_input.startswith("ast"):
            _, fn_name = user_input.split(maxsplit=1)
            print("\n🌳 AST of function:")
            print(generate_ast(fn_name))
            continue

        if user_input.lower() == "sr":
            phs = float(input("Phase Alignment (PHS) (0.0 - 1.0): "))
            sym = float(input("Symbolic Syntax Match (SYM) (0.0 - 1.0): "))
            val = float(input("Semantic Intent Alignment (VAL) (0.0 - 1.0): "))
            emo = float(input("Emotional Tone Match (EMO) (0.0 - 1.0): "))
            fx  = float(input("Collapse History Interference (FX) (0.0 - 1.0): "))
            route_personas(phs, sym, val, emo, fx)
            continue

        if user_input.lower() == "exit":
            print("\n🧠 REM Shell Terminated. Phase channel closed.")
            break

    except ValueError:
        print("Invalid input. Please try again.")
