# engine/rem_executor.py
"""
Enhanced REM CODE Executor
Supports full Collapse Spiral Theory and Syntactic Ethics framework
Compatible with the improved REMTransformer AST structure
"""

import logging
import random
import time
from typing import Dict, List, Union, Any, Optional, Tuple
from dataclasses import dataclass, field

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==================== Execution Context ====================

@dataclass
class REMExecutionContext:
    """Enhanced execution context with persona, phase, and SR tracking"""
    
    # Environment variables
    variables: Dict[str, Any] = field(default_factory=dict)
    
    # Function registry
    functions: Dict[str, Any] = field(default_factory=dict)
    
    # Persona registry and state
    personas: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    active_personas: List[str] = field(default_factory=list)
    
    # Phase management
    current_phase: Optional[str] = None
    phase_history: List[str] = field(default_factory=list)
    
    # SR (Synchrony Rate) management
    global_sr: float = 0.0
    persona_sr: Dict[str, float] = field(default_factory=dict)
    
    # Execution metadata
    execution_log: List[str] = field(default_factory=list)
    signature_log: List[Dict[str, Any]] = field(default_factory=list)
    
    def log(self, message: str):
        """Add message to execution log"""
        self.execution_log.append(message)
        logger.debug(message)
    
    def add_signature(self, content: str, persona: str, reason: str = ""):
        """Add signature for accountability"""
        signature = {
            "content": content,
            "persona": persona,
            "reason": reason,
            "timestamp": time.time(),
            "phase": self.current_phase
        }
        self.signature_log.append(signature)
        self.log(f"🔏 Signed by {persona}: {content}")
    
    def set_persona_sr(self, persona: str, sr_value: float):
        """Set SR value for specific persona"""
        self.persona_sr[persona] = sr_value
        self.log(f"📊 SR({persona}) = {sr_value}")
    
    def get_persona_sr(self, persona: str, context: str = None) -> float:
        """Get SR value for persona with optional context"""
        if context:
            # Handle advanced SR expressions
            if context.startswith('.'):
                # SR(Ana.audit) - function-specific SR
                base_sr = self.persona_sr.get(persona, 0.0)
                return min(base_sr + 0.1, 1.0)  # Slight boost for specific functions
            elif context.startswith('@'):
                # SR(Ana@memory) - memory-contextualized SR
                base_sr = self.persona_sr.get(persona, 0.0)
                return base_sr * 0.9  # Slight reduction for memory operations
            elif context.startswith('|'):
                # SR(Ana|JayTH) - inter-persona correlation
                other_persona = context[1:]
                sr1 = self.persona_sr.get(persona, 0.0)
                sr2 = self.persona_sr.get(other_persona, 0.0)
                return (sr1 + sr2) / 2  # Average correlation
        
        return self.persona_sr.get(persona, self.global_sr)

# ==================== Global Registry ====================

# Global function registry for backward compatibility
function_registry = {}

# Global execution context
global_context = REMExecutionContext()

# ==================== Core Executor ====================

class REMExecutor:
    """Enhanced REM CODE Executor with full Collapse Spiral support"""
    
    def __init__(self, context: Optional[REMExecutionContext] = None):
        self.context = context or REMExecutionContext()
        
        # Initialize default personas with random SR values
        default_personas = ["Ana", "JayDen", "JayTH", "JayRa", "JayLUX", "JayMini", 
                          "JAYX", "JayKer", "JayVOX", "JayVue", "JayNis", "Jayne"]
        
        for persona in default_personas:
            self.context.persona_sr[persona] = random.uniform(0.6, 0.9)
            self.context.personas[persona] = {"active": True, "history": []}
    
    def execute(self, statements: List[Any], sr_override: Optional[float] = None) -> List[str]:
        """
        Execute REM CODE statements with full Collapse Spiral support
        
        Args:
            statements: List of parsed AST nodes (tuples or objects)
            sr_override: Override global SR value for testing
            
        Returns:
            List of execution results
        """
        if sr_override is not None:
            self.context.global_sr = sr_override
            
        output = []
        
        self.context.log(f"🎯 Executing {len(statements)} statements")
        
        for i, stmt in enumerate(statements):
            self.context.log(f"[{i}] Processing: {stmt}")
            
            try:
                result = self._execute_statement(stmt)
                if result:
                    if isinstance(result, list):
                        output.extend(result)
                    else:
                        output.append(str(result))
                        
            except Exception as e:
                error_msg = f"❌ Error executing statement {i}: {e}"
                self.context.log(error_msg)
                output.append(error_msg)
                logger.error(f"Execution error: {e}", exc_info=True)
        
        return output
    
    def _execute_statement(self, stmt: Any) -> Union[str, List[str], None]:
        """Execute a single statement"""
        
        if isinstance(stmt, tuple) and len(stmt) > 0:
            return self._execute_tuple(stmt)
        elif hasattr(stmt, 'node_type'):
            return self._execute_ast_node(stmt)
        else:
            return f"⚠️ Unknown statement type: {type(stmt)}"
    
    def _execute_tuple(self, stmt: Tuple) -> Union[str, List[str], None]:
        """Execute tuple-based AST nodes"""
        kind = stmt[0]
        
        if kind == 'phase':
            return self._execute_phase(stmt)
        elif kind == 'invoke':
            return self._execute_invoke(stmt)
        elif kind == 'function_def':
            return self._execute_function_def(stmt)
        elif kind == 'collapse':
            return self._execute_collapse(stmt)
        elif kind == 'elapse':
            return self._execute_elapse(stmt)
        elif kind == 'sync':
            return self._execute_sync(stmt)
        elif kind == 'cocollapse':
            return self._execute_cocollapse(stmt)
        elif kind == 'persona_call':
            return self._execute_persona_call(stmt)
        elif kind == 'latin_call':
            return self._execute_latin_call(stmt)
        elif kind == 'simple_call':
            return self._execute_simple_call(stmt)
        elif kind == 'set':
            return self._execute_set(stmt)
        elif kind == 'use':
            return self._execute_use(stmt)
        elif kind == 'store':
            return self._execute_store(stmt)
        elif kind == 'sign':
            return self._execute_sign(stmt)
        elif kind == 'cosign':
            return self._execute_cosign(stmt)
        elif kind == 'reason':
            return self._execute_reason(stmt)
        elif kind == 'recall':
            return self._execute_recall(stmt)
        elif kind == 'recall_from_memory':
            return self._execute_recall_from_memory(stmt)
        elif kind == 'memoryset':
            return self._execute_memoryset(stmt)
        elif kind == 'phase_transition':
            return self._execute_phase_transition(stmt)
        elif kind == 'phase_transition_with':
            return self._execute_phase_transition_with(stmt)
        elif kind == 'describe':
            return self._execute_describe(stmt)
        elif kind == 'narrate':
            return self._execute_narrate(stmt)
        elif kind == 'visualize':
            return self._execute_visualize(stmt)
        else:
            return f"⚠️ Unknown tuple kind: {kind}"
    
    # ===== Phase Management =====
    
    def _execute_phase(self, stmt: Tuple) -> List[str]:
        """Execute phase block: ('phase', name, statements)"""
        _, name, statements = stmt
        
        old_phase = self.context.current_phase
        self.context.current_phase = str(name)
        self.context.phase_history.append(str(name))
        
        output = [f"🌐 Phase: {name}"]
        self.context.log(f"Entering phase: {name}")
        
        # Execute phase statements
        phase_output = self.execute(statements)
        output.extend(phase_output)
        
        # Restore previous phase
        self.context.current_phase = old_phase
        
        return output
    
    def _execute_invoke(self, stmt: Tuple) -> List[str]:
        """Execute invoke block: ('invoke', personas, statements)"""
        _, personas, statements = stmt
        
        if isinstance(personas, str):
            personas = [personas]
        
        output = [f"🚀 Invoke: {', '.join(personas)}"]
        
        # Activate personas
        for persona in personas:
            if persona not in self.context.active_personas:
                self.context.active_personas.append(persona)
            self.context.log(f"Activated persona: {persona}")
        
        # Execute statements if provided
        if statements:
            invoke_output = self.execute(statements)
            output.extend(invoke_output)
        
        return output
    
    # ===== Collapse Spiral Logic =====
    
    def _execute_collapse(self, stmt: Tuple) -> List[str]:
        """
        Execute collapse block with full Collapse Spiral support
        ('collapse', condition, statements) or 
        ('collapse', condition, statements, elapse_blocks, sync_block)
        """
        condition = stmt[1]
        main_statements = stmt[2]
        elapse_blocks = stmt[3] if len(stmt) > 3 else []
        sync_block = stmt[4] if len(stmt) > 4 else None
        
        output = []
        
        # Evaluate collapse condition
        if self._evaluate_sr_condition(condition):
            output.append(f"🌀 Collapse: Condition met - executing main block")
            collapse_output = self.execute(main_statements)
            output.extend(collapse_output)
        else:
            # Try elapse blocks
            elapse_matched = False
            for elapse_block in elapse_blocks:
                if isinstance(elapse_block, tuple) and elapse_block[0] == 'elapse':
                    elapse_condition = elapse_block[1]
                    if self._evaluate_sr_condition(elapse_condition):
                        output.append(f"⏳ Elapse: Condition met - executing elapse block")
                        elapse_output = self.execute(elapse_block[2])
                        output.extend(elapse_output)
                        elapse_matched = True
                        break
            
            # If no elapse matched, use sync block
            if not elapse_matched and sync_block:
                output.append(f"🔄 Sync: Executing fallback block")
                if isinstance(sync_block, tuple) and sync_block[0] == 'sync':
                    sync_output = self.execute(sync_block[1])
                    output.extend(sync_output)
        
        return output
    
    def _execute_elapse(self, stmt: Tuple) -> List[str]:
        """Execute elapse block: ('elapse', condition, statements)"""
        _, condition, statements = stmt
        
        output = []
        if self._evaluate_sr_condition(condition):
            output.append(f"⏳ Elapse: Condition met")
            elapse_output = self.execute(statements)
            output.extend(elapse_output)
        else:
            output.append(f"⏳ Elapse: Condition not met - skipping")
        
        return output
    
    def _execute_sync(self, stmt: Tuple) -> List[str]:
        """Execute sync block: ('sync', statements)"""
        _, statements = stmt
        
        output = [f"🔄 Sync: Executing synchronization block"]
        sync_output = self.execute(statements)
        output.extend(sync_output)
        
        return output
    
    def _execute_cocollapse(self, stmt: Tuple) -> List[str]:
        """Execute multi-persona collapse: ('cocollapse', personas, condition, statements)"""
        _, personas, condition, statements = stmt
        
        output = [f"🤝 CoCollapse: Multi-persona consensus with {', '.join(personas)}"]
        
        # Check if all personas meet the condition
        if self._evaluate_sr_condition(condition):
            output.append(f"✅ Consensus reached - executing CoCollapse block")
            cocollapse_output = self.execute(statements)
            output.extend(cocollapse_output)
        else:
            output.append(f"❌ Consensus not reached - skipping CoCollapse block")
        
        return output
    
    # ===== Commands =====
    
    def _execute_persona_call(self, stmt: Tuple) -> str:
        """Execute persona command: ('persona_call', persona, verb, args)"""
        _, persona, verb, args = stmt
        
        self.context.log(f"Persona {persona} executing {verb}")
        
        # Process arguments
        resolved_args = [self._resolve_value(arg) for arg in args]
        
        # Execute the command
        if verb == "Dic":
            message = str(resolved_args[0]) if resolved_args else "[No message]"
            return f"{persona}: {message}"
        elif verb == "Crea":
            message = str(resolved_args[0]) if resolved_args else "[No creation]"
            return f"{persona} creates: {message}"
        elif verb == "Acta":
            message = str(resolved_args[0]) if resolved_args else "[No action]"
            return f"{persona} acts: {message}"
        else:
            return f"{persona}.{verb}({', '.join(map(str, resolved_args))})"
    
    def _execute_latin_call(self, stmt: Tuple) -> str:
        """Execute Latin command: ('latin_call', verb, args)"""
        _, verb, args = stmt
        
        resolved_args = [self._resolve_value(arg) for arg in args]
        
        if verb == "Dic":
            return str(resolved_args[0]) if resolved_args else "[No message]"
        elif verb == "Acta":
            return f"Action: {resolved_args[0]}" if resolved_args else "Action: [undefined]"
        elif verb == "Crea":
            return f"Created: {resolved_args[0]}" if resolved_args else "Created: [undefined]"
        else:
            return f"{verb}({', '.join(map(str, resolved_args))})"
    
    def _execute_simple_call(self, stmt: Tuple) -> str:
        """Execute simple command: ('simple_call', name, args)"""
        _, name, args = stmt
        
        resolved_args = [self._resolve_value(arg) for arg in args]
        return f"{name}({', '.join(map(str, resolved_args))})"
    
    # ===== Variable Operations =====
    
    def _execute_set(self, stmt: Tuple) -> str:
        """Execute set command: ('set', variable, value)"""
        _, variable, value = stmt
        
        resolved_value = self._resolve_value(value)
        self.context.variables[variable] = resolved_value
        
        return f"Set {variable} = {resolved_value}"
    
    def _execute_use(self, stmt: Tuple) -> str:
        """Execute use command: ('use', variable)"""
        _, variable = stmt
        
        value = self.context.variables.get(variable, f"[undefined: {variable}]")
        return f"Using {variable}: {value}"
    
    def _execute_store(self, stmt: Tuple) -> str:
        """Execute store command: ('store', variable, command)"""
        _, variable, command = stmt
        
        # Execute the command and store result
        result = self._execute_statement(command)
        self.context.variables[variable] = result
        
        return f"Stored result in {variable}: {result}"
    
    # ===== Signature & Attribution =====
    
    def _execute_sign(self, stmt: Tuple) -> str:
        """Execute sign block: ('sign', content, persona, reason)"""
        _, content, persona, reason = stmt
        
        self.context.add_signature(content, persona, reason)
        return f"🔏 Signed by {persona}: {content} (Reason: {reason})"
    
    def _execute_cosign(self, stmt: Tuple) -> str:
        """Execute cosign block: ('cosign', content, personas)"""
        _, content, personas = stmt
        
        for persona in personas:
            self.context.add_signature(content, persona, "CoSign consensus")
        
        return f"🔏 CoSigned by {', '.join(personas)}: {content}"
    
    def _execute_reason(self, stmt: Tuple) -> str:
        """Execute reason block: ('reason', reason)"""
        _, reason = stmt
        return f"💭 Reason: {reason}"
    
    # ===== Memory Operations =====
    
    def _execute_recall(self, stmt: Tuple) -> str:
        """Execute recall: ('recall', content, target)"""
        _, content, target = stmt
        
        self.context.variables[target] = content
        return f"📋 Recalled '{content}' to {target}"
    
    def _execute_recall_from_memory(self, stmt: Tuple) -> str:
        """Execute recall from memory: ('recall_from_memory', content, target)"""
        _, content, target = stmt
        
        # Simulate memory retrieval
        recalled_value = f"Memory[{content}]"
        self.context.variables[target] = recalled_value
        return f"📋 Recalled from memory '{content}' to {target}"
    
    def _execute_memoryset(self, stmt: Tuple) -> str:
        """Execute memoryset: ('memoryset', variable, content)"""
        _, variable, content = stmt
        
        self.context.variables[variable] = content
        return f"💾 Memory set {variable} = {content}"
    
    # ===== Phase Transitions =====
    
    def _execute_phase_transition(self, stmt: Tuple) -> str:
        """Execute phase transition: ('phase_transition', target)"""
        _, target = stmt
        
        old_phase = self.context.current_phase
        self.context.current_phase = target
        self.context.phase_history.append(target)
        
        return f"🚀 Phase transition: {old_phase} → {target}"
    
    def _execute_phase_transition_with(self, stmt: Tuple) -> str:
        """Execute conditional phase transition: ('phase_transition_with', target, sr_expr)"""
        _, target, sr_expr = stmt
        
        # Evaluate SR expression
        if self._evaluate_sr_expression(sr_expr):
            old_phase = self.context.current_phase
            self.context.current_phase = target
            self.context.phase_history.append(target)
            return f"🚀 Conditional phase transition: {old_phase} → {target}"
        else:
            return f"🚫 Phase transition blocked: SR condition not met"
    
    # ===== Narrative Commands =====
    
    def _execute_describe(self, stmt: Tuple) -> str:
        """Execute describe: ('describe', name, content)"""
        _, name, content = stmt
        return f"📝 Describe {name}: {content}"
    
    def _execute_narrate(self, stmt: Tuple) -> str:
        """Execute narrate: ('narrate', name, content)"""
        _, name, content = stmt
        return f"📖 Narrate {name}: {content}"
    
    def _execute_visualize(self, stmt: Tuple) -> str:
        """Execute visualize: ('visualize', name, content)"""
        _, name, content = stmt
        return f"🎨 Visualize {name}: {content}"
    
    # ===== Function Management =====
    
    def _execute_function_def(self, stmt: Tuple) -> str:
        """Execute function definition: ('function_def', name, params, statements)"""
        _, name, params, statements = stmt
        
        self.context.functions[name] = {
            'params': params,
            'body': statements
        }
        
        # Also store in global registry for backward compatibility
        function_registry[name] = statements
        
        return f"✅ Function '{name}' defined with params: {params}"
    
    # ===== Helper Methods =====
    
    def _evaluate_sr_condition(self, condition: Any) -> bool:
        """Evaluate SR condition: ('sr_condition', expression, operator, value)"""
        if not isinstance(condition, tuple) or condition[0] != 'sr_condition':
            return False
        
        _, sr_expr, operator, threshold = condition
        
        sr_value = self._evaluate_sr_expression(sr_expr)
        
        return self._compare_values(sr_value, operator, threshold)
    
    def _evaluate_sr_expression(self, sr_expr: Any) -> float:
        """Evaluate SR expression: ('sr_expr', persona, context)"""
        if not isinstance(sr_expr, tuple) or sr_expr[0] != 'sr_expr':
            return 0.0
        
        _, persona, context = sr_expr
        
        return self.context.get_persona_sr(persona, context)
    
    def _compare_values(self, value: float, operator: str, threshold: float) -> bool:
        """Compare values using operator"""
        operators = {
            ">": lambda a, b: a > b,
            ">=": lambda a, b: a >= b,
            "<": lambda a, b: a < b,
            "<=": lambda a, b: a <= b,
            "==": lambda a, b: a == b,
            "!=": lambda a, b: a != b,
        }
        
        return operators.get(operator, lambda a, b: False)(value, threshold)
    
    def _resolve_value(self, value: Any) -> Any:
        """Resolve variable references and return actual values"""
        if isinstance(value, str) and value in self.context.variables:
            return self.context.variables[value]
        return value
    
    def _execute_ast_node(self, node: Any) -> Union[str, List[str], None]:
        """Execute AST node objects (for future dataclass support)"""
        if hasattr(node, 'node_type'):
            return f"🔮 AST Node: {node.node_type} (not yet implemented)"
        return None

# ==================== Legacy Compatibility Functions ====================

def execute(statements: List[Any], env: Optional[Dict] = None, sr_value: float = 0.0) -> List[str]:
    """Legacy compatibility function"""
    context = REMExecutionContext()
    if env:
        context.variables.update(env)
    context.global_sr = sr_value
    
    executor = REMExecutor(context)
    return executor.execute(statements, sr_value)

def execute_function(lines: List[str], sr_value: float = 0.0) -> List[str]:
    """Legacy compatibility function for direct line execution"""
    try:
        from engine.ast_generator import create_ast_generator
        
        generator = create_ast_generator()
        ast = generator.generate_ast(lines)
        
        if isinstance(ast, dict) and "error" in ast:
            return [f"❌ Parse Error: {ast['error']}"]
        
        executor = REMExecutor()
        return executor.execute(ast, sr_value)
        
    except Exception as e:
        return [f"❌ Execution Error: {e}"]

def compare(sr: float, op: str, threshold: float) -> bool:
    """Legacy compatibility function"""
    operators = {
        ">": sr > threshold,
        ">=": sr >= threshold,
        "<": sr < threshold,
        "<=": sr <= threshold,
        "==": sr == threshold,
        "!=": sr != threshold,
    }
    return operators.get(op, False)

def flatten_statements(stmts: List[Any]) -> List[Any]:
    """Legacy compatibility function"""
    flat = []
    for stmt in stmts:
        if isinstance(stmt, list):
            flat.extend(flatten_statements(stmt))
        else:
            flat.append(stmt)
    return flat

# ==================== Factory Functions ====================

def create_executor(context: Optional[REMExecutionContext] = None) -> REMExecutor:
    """Factory function to create REM executor"""
    return REMExecutor(context)

def create_context() -> REMExecutionContext:
    """Factory function to create execution context"""
    return REMExecutionContext()