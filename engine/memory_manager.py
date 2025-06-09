import json
import os

MEMORY_FILE = "memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {"functions": []}
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_memory(memory_data):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory_data, f, ensure_ascii=False, indent=2)

def add_function(name, code_lines, persona="JayDen", sr_threshold=0.85, tags=None):
    if tags is None:
        tags = []
    memory = load_memory()
    new_function = {
        "name": name,
        "code": code_lines,
        "persona": persona,
        "sr_threshold": sr_threshold,
        "tags": tags
    }
    # 関数名の重複を防ぐ（上書き）
    memory["functions"] = [f for f in memory["functions"] if f["name"] != name]
    memory["functions"].append(new_function)
    save_memory(memory)

def list_functions():
    memory = load_memory()
    return [f["name"] for f in memory.get("functions", [])]

def get_function_by_name(name):
    memory = load_memory()
    for func in memory.get("functions", []):
        if func["name"] == name:
            return func
    return None
