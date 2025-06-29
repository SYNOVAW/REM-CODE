
# engine/grammar_transformer.py
"""
Minimal Grammar Transformer for REM CODE
Only handles necessary transformations, letting Lark handle the rest automatically
"""

from lark import Transformer, v_args

@v_args(inline=True)
class GrammarTransformer(Transformer):
    """
    Minimal transformer that only handles transformations that actually need processing.
    Most tokens are handled automatically by Lark.
    """
    
    # ===== String Processing =====
    def ESCAPED_STRING(self, token):
        """Remove surrounding quotes from strings"""
        return str(token)[1:-1]
    
    # ===== Number Processing =====
    def SIGNED_NUMBER(self, token):
        """Convert string numbers to float"""
        return float(token)
    
    def NUMBER(self, token):
        """Convert string numbers to float"""
        return float(token)
    
    # ===== Token Conversion (only where needed) =====
    def NAME(self, token):
        """Ensure names are strings"""
        return str(token)
    
    def LATIN_VERB(self, token):
        """Ensure Latin verbs are strings"""
        return str(token)
    
    def COMPARATOR(self, token):
        """Ensure operators are strings"""
        return str(token)