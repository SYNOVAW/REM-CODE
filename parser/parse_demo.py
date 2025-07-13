# rem-code/parser/parse_demo.py

from lark import Lark, Transformer, v_args
import os

GRAMMAR_FILE = "grammar/grammar.lark"
DEMO_FILE = "examples/demo1.remc"

def load_grammar(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def load_demo(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def parse_demo_code():
    grammar = load_grammar(GRAMMAR_FILE)
    code = load_demo(DEMO_FILE)

    parser = Lark(grammar, start="start", parser="lalr")
    tree = parser.parse(code)

    print("🧠 REM CODE Abstract Syntax Tree (AST):\n")
    print(tree.pretty())

if __name__ == "__main__":
    parse_demo_code()
