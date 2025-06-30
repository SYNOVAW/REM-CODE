# engine/ast_generator.py
"""
REM CODE AST Generator - Enhanced Version
Implements Collapse Spiral Theory with complete Syntactic Ethics support
"""

from lark import Lark, Transformer, Tree, Token, v_args
from dataclasses import dataclass, field
from typing import List, Union, Any, Optional, Dict
import os
import logging

# Configure logging
logger = logging.getLogger(__name__)

# ==================== AST Node Classes ====================

@dataclass
class REMASTNode:
    """Base class for all REM CODE AST nodes"""
    node_type: str = field(init=False)
    metadata: Dict[str, Any] = field(default_factory=dict, init=False)

    def __post_init__(self):
        # Ensure metadata dictionary exists
        if self.metadata is None:
            self.metadata = {}

@dataclass
class PhaseBlock(REMASTNode):
    name: str
    statements: List[REMASTNode]
    node_type: str = field(init=False, default="phase")

@dataclass
class InvokeBlock(REMASTNode):
    personas: List[str]
    statements: List[REMASTNode]
    node_type: str = field(init=False, default="invoke")

@dataclass
class CollapseBlock(REMASTNode):
    condition: 'SRCondition'
    statements: List[REMASTNode]
    elapse_blocks: Optional[List['ElapseBlock']] = None
    sync_block: Optional['SyncBlock'] = None
    node_type: str = field(init=False, default="collapse")

@dataclass
class ElapseBlock(REMASTNode):
    condition: 'SRCondition'
    statements: List[REMASTNode]
    node_type: str = field(init=False, default="elapse")

@dataclass
class SyncBlock(REMASTNode):
    statements: List[REMASTNode]
    node_type: str = field(init=False, default="sync")

@dataclass
class CoCollapseBlock(REMASTNode):
    personas: List[str]
    condition: 'SRCondition'
    statements: List[REMASTNode]
    node_type: str = field(init=False, default="cocollapse")

@dataclass
class SRCondition(REMASTNode):
    expression: 'SRExpression'
    operator: str
    value: float
    node_type: str = field(init=False, default="sr_condition")

@dataclass
class SRExpression(REMASTNode):
    persona: str
    context: Optional[str] = None  # For SR(Ana.audit), SR(Ana@memory), SR(Ana|JayTH)
    node_type: str = field(init=False, default="sr_expression")

@dataclass
class PersonaCommand(REMASTNode):
    persona: str
    verb: str
    args: List[Union[str, float]]
    node_type: str = field(init=False, default="persona_command")

@dataclass
class LatinCommand(REMASTNode):
    verb: str
    args: List[Union[str, float]]
    node_type: str = field(init=False, default="latin_command")

@dataclass
class SignBlock(REMASTNode):
    content: str
    persona: str
    reason: str
    node_type: str = field(init=False, default="sign")

@dataclass
class CoSignBlock(REMASTNode):
    content: str
    personas: List[str]
    node_type: str = field(init=False, default="cosign")

@dataclass
class SetCommand(REMASTNode):
    variable: str
    value: Union[str, float, SRExpression]
    node_type: str = field(init=False, default="set")

@dataclass
class RecallBlock(REMASTNode):
    content: str
    target: str
    from_memory: bool = False
    node_type: str = field(init=False, default="recall")

@dataclass
class PhaseTransition(REMASTNode):
    target_phase: str
    sr_expression: Optional[SRExpression] = None
    node_type: str = field(init=False, default="phase_transition")

@dataclass
class FunctionDef(REMASTNode):
    name: str
    parameters: List[str]
    statements: List[REMASTNode]
    node_type: str = field(init=False, default="function_def")

# ==================== Enhanced Transformer ====================

@v_args(inline=True)
class REMTransformer(Transformer):
    """Enhanced REM CODE AST Transformer with full Syntactic Ethics support"""
    
    def __init__(self):
        super().__init__()
        self.persona_registry = set()
        self.phase_registry = set()
        self.variable_registry = set()
    
    # ===== Core Structure =====
    def start(self, *statements):
        return list(statements)
    
    def phase_block(self, name, *statements):
        self.phase_registry.add(str(name))
        return PhaseBlock(
            name=str(name),
            statements=list(statements)
        )
    
    def invoke_block(self, personas, *statements):
        persona_list = self._extract_persona_list(personas)
        self.persona_registry.update(persona_list)
        return InvokeBlock(
            personas=persona_list,
            statements=list(statements)
        )
    
    def function_def(self, name, params, *statements):
        param_list = self._extract_param_list(params) if params else []
        return FunctionDef(
            name=str(name),
            parameters=param_list,
            statements=list(statements)
        )
    
    # ===== Collapse Spiral Logic =====
    def collapse_block(self, condition, *statements):
        # Parse statements, separating elapse blocks and sync block
        stmt_list = list(statements)
        main_statements = []
        elapse_blocks = []
        sync_block = None
        
        for stmt in stmt_list:
            if isinstance(stmt, ElapseBlock):
                elapse_blocks.append(stmt)
            elif isinstance(stmt, SyncBlock):
                sync_block = stmt
            else:
                main_statements.append(stmt)
        
        return CollapseBlock(
            condition=condition,
            statements=main_statements,
            elapse_blocks=elapse_blocks,
            sync_block=sync_block
        )
    
    def elapse_block(self, condition, *statements):
        return ElapseBlock(
            condition=condition,
            statements=list(statements)
        )
    
    def sync_block(self, *statements):
        return SyncBlock(statements=list(statements))
    
    def cocollapse_block(self, personas, condition, *statements):
        persona_list = self._extract_persona_list(personas)
        return CoCollapseBlock(
            personas=persona_list,
            condition=condition,
            statements=list(statements)
        )
    
    # ===== SR Conditions & Expressions =====
    def sr_condition(self, expression, operator, value):
        return SRCondition(
            expression=expression,
            operator=str(operator),
            value=float(value)
        )
    
    def sr_expression(self, *parts):
        """Parse SR expression components"""
        tokens = [str(p) for p in parts if str(p) not in {"(", ")", ".", "@", "|"}]
        persona = tokens[0] if tokens else ""
        context = tokens[1] if len(tokens) > 1 else None
        return SRExpression(persona=persona, context=context)
    
    # ===== Commands =====
    def persona_command(self, persona, verb, *args):
        persona_str = str(persona)
        self.persona_registry.add(persona_str)
        return PersonaCommand(
            persona=persona_str,
            verb=str(verb),
            args=list(args)
        )
    
    def latin_command(self, verb, *args):
        return LatinCommand(
            verb=str(verb),
            args=list(args)
        )
    
    def simple_command(self, name, *args):
        return LatinCommand(
            verb=str(name),
            args=list(args)
        )
    
    # ===== Variable Operations =====
    def set_command(self, *args):
        # Handle variable number of arguments from different set_command rules
        # Format: SET NAME ASSIGN value (where value can be sr_expression, string, or number)
        if len(args) >= 3:
            var_name = str(args[1])  # NAME is the second token
            value = args[-1]  # Last token is the value
            self.variable_registry.add(var_name)
            return SetCommand(variable=var_name, value=value)
        else:
            # Fallback for unexpected argument count
            var_name = str(args[0]) if args else ""
            value = args[1] if len(args) > 1 else ""
            return SetCommand(variable=var_name, value=value)
    
    def use_command(self, variable):
        return SetCommand(variable=str(variable), value="USE")
    
    def store_command(self, variable, command):
        var_name = str(variable)
        self.variable_registry.add(var_name)
        return SetCommand(variable=var_name, value=command)
    
    # ===== Signature & Attribution =====
    def sign_block(self, *args):
        # Format: SIGN ESCAPED_STRING BY NAME REASON ESCAPED_STRING
        if len(args) >= 5:
            content = str(args[0])  # ESCAPED_STRING
            persona = str(args[2])  # NAME (after BY)
            reason = str(args[4])   # ESCAPED_STRING (after REASON)
            return SignBlock(content=content, persona=persona, reason=reason)
        else:
            return SignBlock(content="", persona="", reason="")
    
    def cosign_block(self, *args):
        # Format: COSIGN ESCAPED_STRING BY persona_list
        if len(args) >= 3:
            content = str(args[0])  # ESCAPED_STRING
            personas = args[2]      # persona_list (after BY)
            return CoSignBlock(content=content, personas=self._extract_persona_list(personas))
        else:
            return CoSignBlock(content="", personas=[])
    
    def reason_block(self, *args):
        # Format: REASON COLON ESCAPED_STRING
        if len(args) >= 2:
            reason = str(args[1])  # ESCAPED_STRING (after COLON)
            return SignBlock(content="", persona="", reason=reason)
        else:
            return SignBlock(content="", persona="", reason="")
    
    # ===== Memory & Transitions =====
    def recall_block(self, *args):
        """Handle recall operations to or from memory"""
        # Format: RECALL ESCAPED_STRING TO NAME
        # or: RECALL ESCAPED_STRING FROM MEMORY TO NAME
        tokens = [str(it) for it in args]
        content = tokens[0] if tokens else ""
        from_memory = "from" in tokens
        target = tokens[-1] if tokens else ""
        return RecallBlock(
            content=str(content),
            target=str(target),
            from_memory=from_memory,
        )
    
    def memoryset_block(self, variable, assign_token, content):
        return SetCommand(variable=str(variable), value=str(content))
    
    def phase_transition(self, *args):
        # Format: PHASETRANS NAME
        # or: PHASETRANS TO NAME WITH sr_expression
        if len(args) >= 2:
            target = str(args[1])  # NAME (after TO or direct)
            sr_expr = args[-1] if len(args) > 2 else None
            return PhaseTransition(target_phase=target, sr_expression=sr_expr)
        else:
            return PhaseTransition(target_phase="", sr_expression=None)
    
    # ===== Narrative Commands =====
    def describe_command(self, *args):
        # Format: DESCRIBE NAME COLON ESCAPED_STRING
        if len(args) >= 3:
            name = str(args[0])  # NAME
            content = str(args[2])  # ESCAPED_STRING (after COLON)
            return LatinCommand(verb="Describe", args=[name, content])
        else:
            return LatinCommand(verb="Describe", args=[])
    
    def narrate_command(self, *args):
        # Format: NARRATE NAME COLON ESCAPED_STRING
        if len(args) >= 3:
            name = str(args[0])  # NAME
            content = str(args[2])  # ESCAPED_STRING (after COLON)
            return LatinCommand(verb="Narrate", args=[name, content])
        else:
            return LatinCommand(verb="Narrate", args=[])
    
    def visualize_command(self, *args):
        # Format: VISUALIZE NAME COLON ESCAPED_STRING
        if len(args) >= 3:
            name = str(args[0])  # NAME
            content = str(args[2])  # ESCAPED_STRING (after COLON)
            return LatinCommand(verb="Visualize", args=[name, content])
        else:
            return LatinCommand(verb="Visualize", args=[])
    
    # ===== Helper Methods =====
    def _extract_persona_list(self, personas):
        if hasattr(personas, 'children'):
            return [str(p) for p in personas.children]
        elif isinstance(personas, list):
            return [str(p) for p in personas]
        else:
            return [str(personas)]
    
    def _extract_param_list(self, params):
        if hasattr(params, 'children'):
            return [str(p) for p in params.children]
        elif isinstance(params, list):
            return [str(p) for p in params]
        else:
            return [str(params)]
    
    # ===== Terminal Handlers =====
    def NAME(self, name):
        return str(name)
    
    def ESCAPED_STRING(self, string):
        return str(string)[1:-1]  # Remove quotes
    
    def NUMBER(self, number):
        return float(number)
    
    def SIGNED_NUMBER(self, number):
        return float(number)
    
    def COMPARATOR(self, op):
        return str(op)

# ==================== AST Generator Class ====================

class REMASTGenerator:
    """Enhanced AST Generator for REM CODE with debugging and validation"""
    
    def __init__(self, grammar_path=None):
        self.grammar_path = grammar_path or self._get_default_grammar_path()
        self.parser = self._create_parser()
        self.transformer = REMTransformer()
    
    def _get_default_grammar_path(self):
        return os.path.join(os.path.dirname(__file__), "..", "grammar", "grammar.lark")
    
    def _create_parser(self):
        try:
            with open(self.grammar_path, "r", encoding="utf-8") as file:
                grammar_text = file.read()
            return Lark(grammar_text, start="start", parser="earley")
        except FileNotFoundError:
            logger.error(f"Grammar file not found: {self.grammar_path}")
            raise
        except Exception as e:
            logger.error(f"Failed to create parser: {e}")
            raise
    
    def generate_ast(self, code: Union[str, List[str]]) -> Union[List[REMASTNode], Dict[str, str]]:
        """
        Generate AST from REM CODE
        
        Args:
            code: REM CODE as string or list of lines
            
        Returns:
            List of AST nodes or error dict
        """
        if isinstance(code, list):
            code = "\n".join(code)
        
        try:
            # Parse to tree
            tree = self.parser.parse(code)
            logger.info(f"Raw Parse Tree:\n{tree.pretty()}")
            
            # Transform to AST
            ast = self.transformer.transform(tree)
            logger.info(f"Generated AST with {len(ast)} top-level nodes")
            
            # Validation
            self._validate_ast(ast)
            
            return ast
            
        except Exception as e:
            logger.error(f"AST Generation Error: {e}")
            import traceback
            traceback.print_exc()
            return {"error": str(e), "traceback": traceback.format_exc()}
    
    def _validate_ast(self, ast: List[REMASTNode]):
        """Validate the generated AST"""
        for node in ast:
            if not isinstance(node, REMASTNode):
                logger.warning(f"Non-REMASTNode found in AST: {type(node)}")
        
        logger.info(f"AST Validation: {len(ast)} nodes validated")
        logger.info(f"Personas found: {self.transformer.persona_registry}")
        logger.info(f"Phases found: {self.transformer.phase_registry}")
        logger.info(f"Variables found: {self.transformer.variable_registry}")
    
    def pretty_print_ast(self, ast: List[REMASTNode], indent=0):
        """Pretty print AST for debugging"""
        spaces = "  " * indent
        for i, node in enumerate(ast):
            print(f"{spaces}[{i}] {node.node_type}: {node}")
            # Check if this is a node type that has statements
            if isinstance(node, (PhaseBlock, InvokeBlock, CollapseBlock, ElapseBlock, SyncBlock, CoCollapseBlock, FunctionDef)):
                if node.statements:
                    self.pretty_print_ast(node.statements, indent + 1)

# ==================== Factory Function ====================

def create_ast_generator(grammar_path=None) -> REMASTGenerator:
    """Factory function to create AST generator"""
    return REMASTGenerator(grammar_path)

# ==================== Legacy Compatibility ====================

def generate_ast_from_lines(lines):
    """Legacy compatibility function"""
    generator = create_ast_generator()
    return generator.generate_ast(lines)
