from lark import Lark
from engine.rem_transformer import REMTransformer
import json

def parse_remc(file_path):
    # 文法読み込み
    with open("grammar/grammar.lark", "r", encoding="utf-8") as f:
        grammar = f.read()

    parser = Lark(grammar, parser="lalr", transformer=REMTransformer())
    
    # コード読み込み
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    try:
        tree = parser.parse(code)
        print("✅ Parse successful.")
        print(json.dumps(tree, indent=2, ensure_ascii=False))
        return tree
    except Exception as e:
        print("❌ Parse error:", e)

if __name__ == "__main__":
    parse_remc("examples/demo1.remc")
