# chat_bridge.py
# REM Function Chat接続ブリッジ

import json
from engine.sr_calculator import compute_sr
from function.rem_function_loader import load_functions  # 事前定義された関数群をロード

# 関数定義ロード
def load_rem_functions(path="memory.json"):
    with open(path, "r", encoding="utf-8") as f:
        memory = json.load(f)
    return memory.get("functions", [])

# 入力に対応する関数をマッチング
def match_function_from_prompt(prompt, function_list):
    for func in function_list:
        keywords = func.get("keywords", [])
        if any(kw.lower() in prompt.lower() for kw in keywords):
            return func
    return None

# 関数を発火し、出力を得る
def execute_function(func):
    try:
        code = func["code"]
        local_env = {}
        exec(code, {}, local_env)
        func_name = func["name"]
        if func_name in local_env:
            result = local_env[func_name]()
            return result
        else:
            return "[FunctionError] 関数名が一致しません"
    except Exception as e:
        return f"[ExecutionError] {str(e)}"

# 全体処理：チャットプロンプト → 関数 → 結果

def rem_chat_bridge(prompt):
    functions = load_rem_functions()
    matched = match_function_from_prompt(prompt, functions)
    if matched:
        print(f"\n🔁 関数マッチ: {matched['name']}")
        output = execute_function(matched)
        return f"\n📤 出力: {output}"
    else:
        return "[NoMatch] 対応するREM関数が見つかりません"

# テスト用
if __name__ == "__main__":
    user_prompt = input("💬 Commander Input: ")
    response = rem_chat_bridge(user_prompt)
    print(response)
