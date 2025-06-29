# engine/rem_transformer.py
"""
Improved REM CODE Transformer
Combines the simplicity of tuple-based AST with enhanced REM CODE feature support
"""

from lark import Transformer, v_args
from typing import Union, List, Tuple, Any, Optional
import logging

logger = logging.getLogger(__name__)

class REMTransformer(Transformer):
    """
    Enhanced REM CODE Transformer with comprehensive Collapse Spiral support
    
    Returns tuple-based AST for simplicity while supporting all REM CODE features
    """
    
    def __init__(self):
        super().__init__()
        self.persona_registry = set()
        self.phase_registry = set()
        self.variable_registry = set()
        self._current_phase = None
        
    # ===== Core Structure =====
    
    def start(self, items):
        """Root node: list of all top-level statements"""
        result = list(items)
        logger.debug(f"Parsed {len(result)} top-level statements")
        return result

    def phase_block(self, items):
        """Phase block: ('phase', name, [statements])"""
        phase_name = str(items[0])
        statements = list(items[1:])
        
        self.phase_registry.add(phase_name)
        self._current_phase = phase_name
        
        logger.debug(f"Phase '{phase_name}' with {len(statements)} statements")
        return ("phase", phase_name, statements)

    def invoke_block(self, items):
        """Invoke block: ('invoke', [personas], [statements])"""
        personas = items[0] if isinstance(items[0], list) else [items[0]]
        statements = list(items[1:]) if len(items) > 1 else []
        
        # Register personas
        for persona in personas:
            self.persona_registry.add(str(persona))
            
        return ("invoke", personas, statements)

    def function_def(self, items):
        """Function definition: ('function_def', name, [params], [statements])"""
        name = str(items[0])
        
        # Handle optional parameters
        if len(items) > 1 and isinstance(items[1], list):
            params = items[1]
            statements = list(items[2:])
        else:
            params = []
            statements = list(items[1:])
            
        return ("function_def", name, params, statements)

    # ===== Enhanced Collapse Spiral Logic =====
    
    def collapse_block(self, items):
        """
        Enhanced collapse block with Elapse and Sync support
        ('collapse', condition, statements, elapse_blocks, sync_block)
        """
        condition = items[0]
        remaining_items = items[1:]
        
        main_statements = []
        elapse_blocks = []
        sync_block = None
        
        # Separate different types of blocks
        for item in remaining_items:
            if isinstance(item, tuple):
                if item[0] == "elapse":
                    elapse_blocks.append(item)
                elif item[0] == "sync":
                    if sync_block is None:
                        sync_block = item
                    else:
                        logger.warning("Multiple sync blocks found, using last one")
                        sync_block = item
                else:
                    main_statements.append(item)
            else:
                main_statements.append(item)
        
        # Build comprehensive collapse structure
        result = ("collapse", condition, main_statements)
        if elapse_blocks:
            result = result + (elapse_blocks,)
        if sync_block:
            result = result + (sync_block,)
            
        return result

    def elapse_block(self, items):
        """Elapse block: ('elapse', condition, [statements])"""
        condition = items[0]
        statements = list(items[1:])
        return ("elapse", condition, statements)

    def sync_block(self, items):
        """Sync block: ('sync', [statements])"""
        statements = list(items)
        return ("sync", statements)

    def cocollapse_block(self, items):
        """Multi-persona collapse: ('cocollapse', [personas], condition, [statements])"""
        personas = items[0] if isinstance(items[0], list) else [items[0]]
        condition = items[1]
        statements = list(items[2:])
        
        # Register personas
        for persona in personas:
            self.persona_registry.add(str(persona))
            
        return ("cocollapse", personas, condition, statements)

    # ===== Enhanced SR Conditions =====
    
    def sr_condition(self, items):
        """SR condition: ('sr_condition', expression, operator, value)"""
        expression = items[0]
        operator = str(items[1])
        value = float(items[2])
        return ("sr_condition", expression, operator, value)

    def sr_expression(self, items):
        """
        Enhanced SR expression supporting:
        - SR(Ana) -> ('sr_expr', 'Ana', None)
        - SR(Ana.audit) -> ('sr_expr', 'Ana', 'audit')
        - SR(Ana@memory) -> ('sr_expr', 'Ana', '@memory')
        - SR(Ana|JayTH) -> ('sr_expr', 'Ana', '|JayTH')
        """
        if len(items) == 1:
            # Simple SR(persona)
            persona = str(items[0])
            return ("sr_expr", persona, None)
        elif len(items) >= 2:
            # Complex SR expressions
            persona = str(items[0])
            context = str(items[1])
            
            # Detect context type
            if '.' in context:
                return ("sr_expr", persona, f".{context}")
            elif '@' in context or context.startswith('@'):
                return ("sr_expr", persona, f"@{context.lstrip('@')}")
            elif '|' in context or context.startswith('|'):
                return ("sr_expr", persona, f"|{context.lstrip('|')}")
            else:
                return ("sr_expr", persona, context)
        
        return ("sr_expr", str(items[0]), None)

    # ===== Commands =====
    
    def persona_command(self, items):
        """Persona command: ('persona_call', persona, verb, [args])"""
        persona = str(items[0])
        verb = str(items[1])
        args = list(items[2:]) if len(items) > 2 else []
        
        self.persona_registry.add(persona)
        return ("persona_call", persona, verb, args)

    def latin_command(self, items):
        """Latin command: ('latin_call', verb, [args])"""
        verb = str(items[0])
        args = list(items[1:]) if len(items) > 1 else []
        return ("latin_call", verb, args)

    def simple_command(self, items):
        """Simple command: ('simple_call', name, [args])"""
        name = str(items[0])
        args = list(items[1:]) if len(items) > 1 else []
        return ("simple_call", name, args)

    # ===== Variable Operations =====
    
    def set_command(self, items):
        """Set command: ('set', variable, value)"""
        variable = str(items[0])
        value = items[1]
        
        self.variable_registry.add(variable)
        return ("set", variable, value)

    def use_command(self, items):
        """Use command: ('use', variable)"""
        variable = str(items[0])
        return ("use", variable)

    def store_command(self, items):
        """Store command: ('store', variable, command)"""
        variable = str(items[0])
        command = items[1]
        
        self.variable_registry.add(variable)
        return ("store", variable, command)

    # ===== Signature & Attribution =====
    
    def sign_block(self, items):
        """Sign block: ('sign', content, persona, reason)"""
        if len(items) >= 3:
            content = str(items[0])
            persona = str(items[1])
            reason = str(items[2])
        else:
            content = str(items[0]) if len(items) > 0 else ""
            persona = str(items[1]) if len(items) > 1 else ""
            reason = ""
            
        return ("sign", content, persona, reason)

    def cosign_block(self, items):
        """CoSign block: ('cosign', content, [personas])"""
        content = str(items[0])
        personas = items[1] if isinstance(items[1], list) else [str(items[1])]
        return ("cosign", content, personas)

    def reason_block(self, items):
        """Reason block: ('reason', reason)"""
        reason = str(items[0])
        return ("reason", reason)

    # ===== Memory & Transitions =====
    
    def recall_block(self, items):
        """
        Recall block: ('recall', content, target) or ('recall_from_memory', content, target)
        """
        if len(items) == 2:
            # Simple recall
            content = str(items[0])
            target = str(items[1])
            return ("recall", content, target)
        elif len(items) >= 3:
            # Recall from memory
            content = str(items[0])
            target = str(items[-1])  # Last item is target
            return ("recall_from_memory", content, target)
        else:
            return ("recall", str(items[0]), "")

    def memoryset_block(self, items):
        """Memory set: ('memoryset', variable, content)"""
        variable = str(items[0])
        content = str(items[1])
        
        self.variable_registry.add(variable)
        return ("memoryset", variable, content)

    def phase_transition(self, items):
        """
        Phase transition: ('phase_transition', target) or ('phase_transition_with', target, sr_expr)
        """
        target = str(items[0])
        
        if len(items) > 1:
            sr_expr = items[1]
            return ("phase_transition_with", target, sr_expr)
        else:
            return ("phase_transition", target)

    # ===== Narrative Commands =====
    
    def describe_command(self, items):
        """Describe command: ('describe', name, content)"""
        name = str(items[0])
        content = str(items[1]) if len(items) > 1 else ""
        return ("describe", name, content)

    def narrate_command(self, items):
        """Narrate command: ('narrate', name, content)"""
        name = str(items[0])
        content = str(items[1]) if len(items) > 1 else ""
        return ("narrate", name, content)

    def visualize_command(self, items):
        """Visualize command: ('visualize', name, content)"""
        name = str(items[0])
        content = str(items[1]) if len(items) > 1 else ""
        return ("visualize", name, content)

    # ===== Helper Methods =====
    
    def persona_list(self, items):
        """Convert items to persona list"""
        personas = [str(item) for item in items]
        for persona in personas:
            self.persona_registry.add(persona)
        return personas

    def param_list(self, items):
        """Convert items to parameter list"""
        return [str(item) for item in items]

    def arg_list(self, items):
        """Return arguments as-is"""
        return list(items)

    # ===== Terminal Handlers =====
    
    def ESCAPED_STRING(self, s):
        """Remove quotes from strings"""
        return str(s)[1:-1]

    def NAME(self, name):
        """Convert to string"""
        return str(name)

    def SIGNED_NUMBER(self, token):
        """Convert to float"""
        return float(token)
        
    def NUMBER(self, token):
        """Convert to float"""
        return float(token)

    def LATIN_VERB(self, token):
        """Convert to string"""
        return str(token)

    def COMPARATOR(self, token):
        """Convert to string"""
        return str(token)

    # ===== Debug Information =====
    
    def get_analysis_info(self):
        """Return analysis information for debugging"""
        return {
            "personas": list(self.persona_registry),
            "phases": list(self.phase_registry),
            "variables": list(self.variable_registry),
            "current_phase": self._current_phase
        }

    def reset_state(self):
        """Reset transformer state"""
        self.persona_registry.clear()
        self.phase_registry.clear()
        self.variable_registry.clear()
        self._current_phase = None

# ===== Factory Function =====

def create_rem_transformer() -> REMTransformer:
    """Factory function to create REM transformer"""
    return REMTransformer()

# ===== Utility Functions =====

def analyze_ast(ast: List[Tuple], transformer: REMTransformer = None):
    """Analyze AST and return insights"""
    if transformer is None:
        transformer = REMTransformer()
    
    def count_node_types(nodes, counts=None):
        if counts is None:
            counts = {}
        
        for node in nodes:
            if isinstance(node, tuple) and len(node) > 0:
                node_type = node[0]
                counts[node_type] = counts.get(node_type, 0) + 1
                
                # Recursively count nested nodes
                for item in node[1:]:
                    if isinstance(item, list):
                        count_node_types(item, counts)
        
        return counts
    
    node_counts = count_node_types(ast)
    analysis_info = transformer.get_analysis_info()
    
    return {
        "node_counts": node_counts,
        "total_nodes": sum(node_counts.values()),
        **analysis_info
    }
