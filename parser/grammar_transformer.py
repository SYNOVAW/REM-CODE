# rem-code/parser/grammar_transformer.py

from lark import Lark
from engine.rem_transformer import REMTransformer
import os

GRAMMAR_PATH = os.path.join(os.path.dirname(__file__), "..", "grammar", "grammar.lark")

def load_grammar():
    with open(GRAMMAR_PATH, "r", encoding="utf-8") as f:
        return f.read()

def parse_lines(lines, sr_value=0.0):
    grammar = load_grammar()
    parser = Lark(grammar, parser="lalr", start="start")

    code = "\n".join(lines)
    print(f">>> Parsing code:\n{code}")
    
    tree = parser.parse(code)
    print(">>> Parsed Tree:\n", tree.pretty())  # 🌲 構文木確認

    # ✅ Transformerを通して AST を tuple に変換
    transformer = REMTransformer(sr_value=sr_value)
    ast = transformer.transform(tree)

    print(">>> Transformed AST:", ast)  # ✅ tuple化されたAST

    # デバッグ: ASTの詳細分析
    print(">>> AST Analysis:")
    if isinstance(ast, list):
        for i, item in enumerate(ast):
            print(f"  [{i}] {type(item).__name__}: {item}")
            if isinstance(item, tuple) and len(item) >= 2:
                print(f"      Action: {item[0]}, Target: {item[1]}")

    assert isinstance(ast, list), f"Transformer failed to flatten AST, got {type(ast)}"

    return ast