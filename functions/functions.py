# rem-code/functions/functions.py

import json
import os
from engine.rem_executor import execute_function
from parser.grammar_transformer import parse_lines  # ← 変更: 統一されたパーサーを使用
from zine.generator import generate_zine_from_function

# 🧠 メモリファイルパス
MEMORY_PATH = os.path.join(os.path.dirname(__file__), "..", "memory", "memory.json")

# 🧠 メモリ読み込み（永続化）
if os.path.exists(MEMORY_PATH):
    with open(MEMORY_PATH, "r", encoding="utf-8") as f:
        memory = json.load(f)
else:
    memory = {"functions": {}}

# ✅ 関数定義（新規登録 or 上書き）
def define_function(name, lines):
    memory["functions"][name] = {"body": lines}
    save_memory()
    return f"✅ Function '{name}' defined."

# 🧠 関数呼び出し
def call_function(name, sr_value=0.0):
    if name in memory["functions"]:
        lines = memory["functions"][name]["body"]
        
        # ✅ 安全性追加: strだったらsplitして修正
        if isinstance(lines, str):
            lines = lines.strip().split("\n")

        return execute_function(lines, sr_value=sr_value)
    return f"❌ Function '{name}' not found."

# 📜 関数一覧取得
def list_functions():
    return list(memory.get("functions", {}).keys())

# 🌳 AST生成（構文木） - 統一されたパーサーを使用
def generate_ast(name):
    if name in memory["functions"]:
        lines = memory["functions"][name]["body"]
        try:
            return parse_lines(lines)  # ← 変更: generate_ast_from_lines → parse_lines
        except Exception as e:
            return {"error": f"Parse error: {str(e)}"}
    return {"error": f"Function '{name}' not found."}

# 新しい関数: 直接ライン配列からAST生成
def generate_ast_from_lines(lines):
    """generate_ast_from_lines関数の互換性維持のためのラッパー"""
    try:
        return parse_lines(lines)
    except Exception as e:
        return {"error": f"Parse error: {str(e)}"}

# 🌀 REM ZINE出力
def generate_zine(name):
    if name in memory["functions"]:
        lines = memory["functions"][name]["body"]
        return generate_zine_from_function(name, lines)
    return f"❌ Function '{name}' not found."

# 💾 メモリ保存（永続化）
def save_memory():
    with open(MEMORY_PATH, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2, ensure_ascii=False)