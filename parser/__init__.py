"""
REM-CODE Parser Module
Grammar parsing and transformation components
"""

# Import main parser components
try:
    from .grammar_transformer import GrammarTransformer
except ImportError:
    # Graceful degradation if dependencies not available
    pass

__all__ = ['GrammarTransformer']