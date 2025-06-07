# rem_code/functions.py

from engine.persona_router import route_personas

def define_function(name, body):
    # Stores function definition in memory (in-memory dict for now)
    if "functions" not in memory:
        memory["functions"] = {}
    memory["functions"][name] = body
    return f"Function '{name}' defined."

def call_function(name):
    if "functions" not in memory or name not in memory["functions"]:
        return f"Function '{name}' not found."
    body = memory["functions"][name]
    output = []
    for line in body:
        output.append(execute_line(line))
    return "\n".join(output)

def execute_line(line):
    # Basic REM CODE execution engine (very limited)
    if line.startswith("say "):
        return line[4:].strip('"')
    if line.startswith("route_personas"):
        return route_personas()
    return f"Unknown command: {line}"

# Mock memory for testing
memory = {}
