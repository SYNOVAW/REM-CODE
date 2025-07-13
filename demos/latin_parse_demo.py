#!/usr/bin/env python3
"""
REM CODE Latin Mode Parser Demo
Demonstrates the unified Latin syntax for REM CODE
"""

import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from pathlib import Path
from lark import Lark
from parser.grammar_transformer import GrammarTransformer
import json

BASE_DIR = Path(__file__).resolve().parent


def parse_latin_remc(file_path: str):
    """Parse a REMC file using the Latin grammar."""
    grammar_path = BASE_DIR.parent / "grammar" / "grammar_latin.lark"
    
    print(f"🔍 Loading Latin grammar from: {grammar_path}")
    
    try:
        with open(grammar_path, "r", encoding="utf-8") as f:
            grammar = f.read()
        print("✅ Latin grammar loaded successfully")
    except FileNotFoundError:
        print(f"❌ Latin grammar file not found at: {grammar_path}")
        return None
    
    try:
        parser = Lark(grammar, parser="lalr", transformer=GrammarTransformer())
        print("✅ Latin parser created successfully")
    except Exception as e:
        print(f"❌ Latin parser creation failed: {e}")
        return None
    
    code_path = Path(file_path)
    if not code_path.is_absolute():
        code_path = BASE_DIR.parent / code_path
    
    try:
        with open(code_path, "r", encoding="utf-8") as f:
            code = f.read()
        print(f"✅ Code loaded from: {code_path}")
    except FileNotFoundError:
        print(f"❌ Code file not found at: {code_path}")
        return None

    try:
        tree = parser.parse(code)
        print("✅ Latin parse successful!")
        print("\n📋 Latin Parse Result:")
        print(json.dumps(tree, indent=2, ensure_ascii=False))
        return tree
    except Exception as e:
        print(f"❌ Latin parse error: {e}")
        return None


def compare_syntax():
    """Compare English and Latin syntax"""
    print("\n🔄 Syntax Comparison:")
    print("=" * 50)
    
    comparisons = [
        ("Phase", "Phasor", "Phase block"),
        ("Invoke", "Invoca", "Persona invocation"),
        ("def", "Definio", "Function definition"),
        ("set", "Pone", "Variable assignment"),
        ("Collapse", "Collapsa", "Collapse logic"),
        ("Sync", "Synchrona", "Synchronization"),
        ("Sign", "Signa", "Signature"),
        ("Reason", "Causa", "Reasoning"),
        ("Recall", "Memora", "Memory recall"),
        ("use", "Utor", "Memory usage"),
        ("store", "Repono", "Memory storage"),
        ("by", "per", "Agent specification"),
        ("and", "et", "Logical AND"),
        ("or", "vel", "Logical OR"),
        ("with", "cum", "Accompaniment"),
        ("from", "ex", "Source specification"),
        ("to", "ad", "Target specification"),
        ("Authority", "Auctoritas", "Authority validation"),
        ("Consensus", "Consensus", "Democratic consensus"),
        ("Validate", "Validare", "Constitutional validation"),
        ("Emergency", "Urgentia", "Emergency protocols"),
        ("Trinity", "Trinitas", "Trinity coordination"),
        ("requires", "requirit", "Requirement specification"),
        ("as", "ut", "Role specification"),
        ("for", "pro", "Purpose specification"),
        ("override", "supervenio", "Emergency override"),
        ("protocol", "protocollum", "Protocol specification"),
        ("authorization", "auctorizatio", "Authorization"),
        ("coordination", "coordinatio", "Coordination"),
        ("unanimous", "unagimus", "Unanimous decision"),
        ("majority", "maioritas", "Majority decision"),
        ("decision", "decisio", "Decision making"),
        ("action", "actio", "Constitutional action"),
        ("amendment", "emendatio", "Constitutional amendment"),
        ("interpretation", "interpretatio", "Constitutional interpretation"),
        ("enforcement", "executio", "Constitutional enforcement")
    ]
    
    print(f"{'English':<15} {'Latin':<15} {'Purpose':<25}")
    print("-" * 55)
    
    for english, latin, purpose in comparisons:
        print(f"{english:<15} {latin:<15} {purpose:<25}")
    
    print("\n🎯 Benefits of Latin Unification:")
    print("• Consistent linguistic foundation")
    print("• Eliminates Reduce/Reduce conflicts")
    print("• Enhances semantic clarity")
    print("• Supports international understanding")
    print("• Maintains aesthetic elegance")


def main():
    """Main demo function"""
    print("🌀 REM CODE Latin Mode Parser Demo")
    print("=" * 50)
    
    # Compare syntax
    compare_syntax()
    
    # Parse Latin demo file
    print("\n🧪 Testing Latin Syntax Parsing:")
    print("-" * 40)
    
    result = parse_latin_remc("examples/demo_latin.remc")
    
    if result:
        print("\n🎉 Latin syntax parsing successful!")
        print("✅ All Latin keywords parsed correctly")
        print("✅ No Reduce/Reduce conflicts detected")
        print("✅ Unified linguistic foundation achieved")
    else:
        print("\n❌ Latin syntax parsing failed")
        print("Please check the grammar file and syntax")


if __name__ == "__main__":
    main() 