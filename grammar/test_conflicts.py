#!/usr/bin/env python3
"""
Test script to check for Reduce/Reduce conflicts in REM-CODE grammar
"""

from pathlib import Path
from lark import Lark
import sys
import os

def test_grammar_conflicts():
    """Test if grammar has reduce/reduce conflicts"""
    
    # Load grammar
    grammar_path = Path(__file__).parent / "grammar.lark"
    print(f"🔍 Loading grammar from: {grammar_path}")
    
    try:
        with open(grammar_path, "r", encoding="utf-8") as f:
            grammar = f.read()
        print("✅ Grammar loaded successfully")
    except FileNotFoundError:
        print(f"❌ Grammar file not found")
        return False
    
    # Test parser creation (this will reveal conflicts)
    try:
        parser = Lark(grammar, parser="lalr", debug=True)
        print("✅ Parser created successfully - NO CONFLICTS!")
        
        # Test simple parsing
        test_code = """
Authority JayLoid requires Constitutional:
    JayLoid.Cogita "test"
    set threshold = SR current_value
    Collapse SR(JayLoid) >= 0.8:
        JayLoid.Activa "high sr action"
"""
        
        print("\n🧪 Testing parse...")
        try:
            tree = parser.parse(test_code)
            print("✅ Parse test successful!")
            return True
        except Exception as e:
            print(f"❌ Parse test failed: {e}")
            return False
            
    except Exception as e:
        if "reduce/reduce" in str(e).lower() or "conflict" in str(e).lower():
            print(f"❌ REDUCE/REDUCE CONFLICT DETECTED: {e}")
        else:
            print(f"❌ Parser creation failed: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Testing REM-CODE Grammar for Conflicts...")
    success = test_grammar_conflicts()
    
    if success:
        print("\n🎉 Grammar is CONFLICT-FREE and ready!")
    else:
        print("\n💥 Grammar has conflicts that need fixing")
    
    sys.exit(0 if success else 1)