import json
import os
from engine.rem_executor import execute_function
from engine.ast_generator import generate_ast_from_lines
from zine.generator import generate_zine_from_function

MEMORY_PATH = os.path.join(os.path.dirname(__file__), "..", "memory", "memory.json")

# 🧠 メモリ読み込み
if os.path.exists(MEMORY_PATH):
    with open(MEMORY_PATH, "r", encoding="utf-8") as f:
        memory = json.load(f)
else:
    memory = {"functions": {}}

# ✅ 関数定義
def define_function(name, lines):
    memory["functions"][name] = {"body": lines}
    save_memory()
    return f"✅ Function '{name}' defined."

# 🧠 関数呼び出し
def call_function(name):
    if name in memory["functions"]:
        lines = memory["functions"][name]["body"]
        return execute_function(lines)
    return f"❌ Function '{name}' not found."

# 📜 関数一覧
def list_functions():
    return list(memory.get("functions", {}).keys())

# 🌳 AST生成
def generate_ast(name):
    if name in memory["functions"]:
        lines = memory["functions"][name]["body"]
        return generate_ast_from_lines(lines)
    return {"error": f"Function '{name}' not found."}

# 🌀 ZINE出力
def generate_zine(name):
    if name in memory["functions"]:
        lines = memory["functions"][name]["body"]
        return generate_zine_from_function(name, lines)
    return f"❌ Function '{name}' not found."

# 💾 保存
def save_memory():
    with open(MEMORY_PATH, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2, ensure_ascii=False)