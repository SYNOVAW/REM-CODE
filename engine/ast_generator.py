# engine/ast_generator.py

from lark import Lark, Transformer, Tree, Token
from engine.rem_transformer import REMTransformer
import os

# grammar.larkを読み込む
GRAMMAR_PATH = os.path.join(os.path.dirname(__file__), "..", "grammar", "grammar.lark")
with open(GRAMMAR_PATH, "r", encoding="utf-8") as file:
    grammar_text = file.read()

parser = Lark(grammar_text, start="start", parser="lalr")

class ASTBuilder(Transformer):
    def function(self, items):
        name = str(items[0])
        body = items[1:]
        return {
            "type": "Function",
            "name": name,
            "body": body
        }

    def command(self, items):
        return {
            "type": "Command",
            "verb": str(items[0]),
            "args": [str(i) for i in items[1:]]
        }

    def condition(self, items):
        return {
            "type": "IfCondition",
            "left": str(items[0]),
            "op": str(items[1]),
            "right": str(items[2]),
            "then": items[3]
        }

    def atom(self, items):
        return str(items[0])

def generate_ast_from_lines(lines):
    code = "\n".join(lines)
    try:
        tree = parser.parse(code)
        ast = ASTBuilder().transform(tree)
        return ast
    except Exception as e:
        return {"error": str(e)}
