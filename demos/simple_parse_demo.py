#!/usr/bin/env python3
"""
Simple REM-CODE Parser Demo
Fixed version that should work reliably
"""

from pathlib import Path
from lark import Lark
import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from parser.grammar_transformer import GrammarTransformer
import json

def simple_parse_demo():
    """Simple demo that works"""
    
    # Get the correct paths
    demo_dir = Path(__file__).resolve().parent
    project_root = demo_dir.parent
    
    # Load grammar
    grammar_path = project_root / "grammar" / "grammar.lark"
    print(f"🔍 Loading grammar from: {grammar_path}")
    
    try:
        with open(grammar_path, "r", encoding="utf-8") as f:
            grammar = f.read()
        print("✅ Grammar loaded successfully")
    except FileNotFoundError:
        print(f"❌ Grammar file not found at: {grammar_path}")
        return
    
    # Create parser
    try:
        parser = Lark(grammar, parser="lalr", transformer=GrammarTransformer())
        print("✅ Parser created successfully")
    except Exception as e:
        print(f"❌ Parser creation failed: {e}")
        return
    
    # Test with simple REM-CODE
    simple_code = """
Authority JayLoid requires Constitutional:
    JayLoid.Cogita "Hello REM Nation"
    Sign "First test" by JayLoid Reason "Testing parser"
"""
    
    print("\n🧪 Testing with simple REM-CODE:")
    print(simple_code)
    
    try:
        tree = parser.parse(simple_code)
        print("✅ Parse successful!")
        print("\n📋 Parse result:")
        print(json.dumps(tree, indent=2, ensure_ascii=False))
        return tree
    except Exception as e:
        print(f"❌ Parse failed: {e}")
        return None

if __name__ == "__main__":
    simple_parse_demo()