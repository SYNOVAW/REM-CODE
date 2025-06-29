from pathlib import Path
from lark import Lark
from engine.rem_transformer import REMTransformer
import json

BASE_DIR = Path(__file__).resolve().parent


def parse_remc(file_path: str):
    """Parse a REMC file using the bundled grammar."""
    grammar_path = BASE_DIR / "grammar" / "grammar.lark"
    with open(grammar_path, "r", encoding="utf-8") as f:
        grammar = f.read()

    parser = Lark(grammar, parser="lalr", transformer=REMTransformer())
    
    code_path = Path(file_path)
    if not code_path.is_absolute():
        code_path = BASE_DIR / code_path
    with open(code_path, "r", encoding="utf-8") as f:
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
