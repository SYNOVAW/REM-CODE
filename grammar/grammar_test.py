#!/usr/bin/env python3
"""
Grammar Test for REM-CODE Lite
Test the fixed grammar for Reduce/Reduce conflicts
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from lark import Lark, LarkError
    LARK_AVAILABLE = True
except ImportError:
    LARK_AVAILABLE = False

def test_grammar():
    """Test REM-CODE grammar for conflicts"""
    if not LARK_AVAILABLE:
        print("❌ Lark parser not available")
        return False
    
    # Load grammar
    try:
        with open('grammar/grammar.lark', 'r') as f:
            grammar_content = f.read()
        
        # Create parser
        parser = Lark(grammar_content, start='start', parser='lalr')
        print("✅ Grammar loaded successfully - no Reduce/Reduce conflicts!")
        
        # Test basic constitutional constructs
        test_cases = [
            # Basic authority
            '''Authority JayTH requires Constitutional:
    JayTH.Cogita "test"
    Sign "Test #001" by JayTH Reason "Test signature"''',
            
            # SR expression (fixed syntax)
            '''Collapse SR(JayTH) >= 0.8:
    JayTH.Activa "high sr action"''',
            
            # SR variable (fixed syntax)  
            '''set threshold = SR current_value
Collapse SR threshold >= 0.9:
    JayTH.Declara "threshold exceeded"''',
            
            # Consensus
            '''Consensus SR >= 0.8 by JayTH, Ana:
    JayTH.Coordina "consensus action"
    Ana.Verificare "consensus validation"''',
            
            # Emergency
            '''Emergency trinity authorization:
    JayTH.Vigila "emergency situation"
    Ana.Protege "system integrity"'''
        ]
        
        print("\n🧪 Testing constitutional constructs:")
        for i, test_case in enumerate(test_cases, 1):
            try:
                result = parser.parse(test_case)
                print(f"✅ Test {i}: Parse successful")
            except LarkError as e:
                print(f"❌ Test {i}: Parse failed - {e}")
                return False
        
        print("\n🎉 All grammar tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Grammar test failed: {e}")
        return False

def main():
    """Main test runner"""
    print("🔍 Testing REM-CODE Grammar for conflicts...")
    success = test_grammar()
    
    if success:
        print("\n✅ Grammar is conflict-free and ready for production!")
    else:
        print("\n❌ Grammar has issues that need fixing")
    
    return success

if __name__ == "__main__":
    main()