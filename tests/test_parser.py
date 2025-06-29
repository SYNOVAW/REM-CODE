import pathlib
import sys
import pytest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
pytest.importorskip('lark')
from engine.ast_generator import create_ast_generator

def test_parse_demo():
    code = pathlib.Path('examples/demo1.remc').read_text(encoding='utf-8')
    generator = create_ast_generator()
    ast = generator.generate_ast(code)
    assert isinstance(ast, list)
    assert len(ast) > 0

