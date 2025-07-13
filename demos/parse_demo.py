from pathlib import Path
from lark import Lark
import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from parser.grammar_transformer import GrammarTransformer
import json

BASE_DIR = Path(__file__).resolve().parent


def parse_remc(file_path: str):
    """Parse a REMC file using the bundled grammar."""
    grammar_path = BASE_DIR.parent / "grammar" / "grammar.lark"
    with open(grammar_path, "r", encoding="utf-8") as f:
        grammar = f.read()

    parser = Lark(grammar, parser="lalr", transformer=GrammarTransformer())
    
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
