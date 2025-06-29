# engine/ast_generator.py

from lark import Lark, Transformer, Tree, Token
from engine.rem_transformer import REMTransformer
import os

# grammar.larkを読み込む
GRAMMAR_PATH = os.path.join(os.path.dirname(__file__), "..", "grammar", "grammar.lark")
with open(GRAMMAR_PATH, "r", encoding="utf-8") as file:
    grammar_text = file.read()

parser = Lark(grammar_text, start="start", parser="lalr")

def generate_ast_from_lines(lines):
    code = "\n".join(lines)
    try:
        tree = parser.parse(code)
        print(f">>> Raw Parse Tree:\n{tree.pretty()}")
        
        # REMTransformerを直接使用
        transformer = REMTransformer()
        ast = transformer.transform(tree)
        print(f">>> Transformed AST: {ast}")
        
        # ASTの各要素をテスト実行
        print(f">>> Testing execution...")
        if isinstance(ast, list):
            for i, item in enumerate(ast):
                print(f">>> Item {i}: {item}")
                if isinstance(item, tuple):
                    if item[0] == "call":
                        print(f">>>   -> Command: {item[1]} with args: {item[2]}")
                    elif item[0] == "invoke":
                        print(f">>>   -> Invoke: {item[1]}")
                elif isinstance(item, Tree):
                    print(f">>>   -> Tree: {item.data} with children: {item.children}")
        
        return ast
    except Exception as e:
        print(f">>> Parse Error: {e}")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}