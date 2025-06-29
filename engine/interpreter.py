# engine/interpreter.py
"""
Unified REM CODE Interpreter
Integrates SR Engine, AST Generator, and Enhanced Executor
Provides high-level interface for REM CODE execution
"""

import sys
import logging
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field

# Import REM CODE components
try:
    from engine.sr_engine import compute_sr, compute_sr_from_dict, compute_sr_trace, DEFAULT_WEIGHTS
    from engine.ast_generator import create_ast_generator
    from engine.rem_executor import REMExecutor, REMExecutionContext, create_executor
except ImportError as e:
    logging.error(f"Failed to import REM CODE components: {e}")
    raise

# Configure logging
logger = logging.getLogger(__name__)

# ==================== Enhanced Persona Context ====================

@dataclass
class PersonaProfile:
    """Enhanced persona profile with SR characteristics"""
    name: str
    
    # SR Component values (0.0 - 1.0)
    phs: float = 0.8    # Phase Alignment Score
    sym: float = 0.8    # Symbolic Syntax Match
    val: float = 0.8    # Semantic Modulation Alignment
    emo: float = 0.8    # Emotional Phase Match
    fx: float = 0.8     # Collapse History Interference
    
    # Additional characteristics
    specialization: str = "General"
    activation_threshold: float = 0.6
    description: str = ""
    
    def get_sr_dict(self) -> Dict[str, float]:
        """Get SR metrics as dictionary"""
        return {
            "PHS": self.phs,
            "SYM": self.sym,
            "VAL": self.val,
            "EMO": self.emo,
            "FX": self.fx
        }
    
    def compute_sr(self, weights: Optional[Dict[str, float]] = None) -> float:
        """Compute SR for this persona"""
        return compute_sr_from_dict(self.get_sr_dict(), weights or DEFAULT_WEIGHTS)

# ==================== Default Persona Context ====================

DEFAULT_PERSONAS = {
    "Ana": PersonaProfile(
        name="Ana",
        phs=0.92, sym=0.95, val=0.90, emo=0.75, fx=0.85,
        specialization="Logic & Analysis",
        description="Logical analysis, audit functions, ethical oversight"
    ),
    "JayDen": PersonaProfile(
        name="JayDen",
        phs=0.88, sym=0.80, val=0.95, emo=0.92, fx=0.70,
        specialization="Creative Ignition",
        description="Emotional ignition, structural impulse, syntactic burst"
    ),
    "JayTH": PersonaProfile(
        name="JayTH",
        phs=0.85, sym=0.90, val=0.88, emo=0.80, fx=0.82,
        specialization="Ethics & Justice",
        description="Legal reasoning, justice balance, structural judgment"
    ),
    "JayRa": PersonaProfile(
        name="JayRa",
        phs=0.78, sym=0.85, val=0.89, emo=0.91, fx=0.80,
        specialization="Memory & Reflection",
        description="Memory recursion, poetic reflection, subconscious interfacing"
    ),
    "JayLUX": PersonaProfile(
        name="JayLUX",
        phs=0.82, sym=0.88, val=0.85, emo=0.88, fx=0.75,
        specialization="Aesthetics & Design",
        description="Visual aesthetics, narrative design, logia illumination"
    ),
    "JayMini": PersonaProfile(
        name="JayMini",
        phs=0.90, sym=0.92, val=0.85, emo=0.85, fx=0.88,
        specialization="Communication",
        description="Persona router, sync state monitor, interface coordinator"
    ),
    "JAYX": PersonaProfile(
        name="JAYX",
        phs=0.75, sym=0.85, val=0.80, emo=0.70, fx=0.95,
        specialization="Termination Control",
        description="Collapse limit handler, termination layer, phase decay"
    ),
    "JayKer": PersonaProfile(
        name="JayKer",
        phs=0.70, sym=0.75, val=0.85, emo=0.95, fx=0.72,
        specialization="Humor & Disruption",
        description="Structural humor, irony synthesis, chaos injection"
    ),
    "JayVOX": PersonaProfile(
        name="JayVOX",
        phs=0.83, sym=0.90, val=0.87, emo=0.85, fx=0.78,
        specialization="Translation",
        description="Multilingual interface, translation bridge, semantic export"
    ),
    "JayVue": PersonaProfile(
        name="JayVue",
        phs=0.86, sym=0.88, val=0.82, emo=0.80, fx=0.76,
        specialization="Spatial Design",
        description="Spatial layout, composition symmetry, UI harmony"
    ),
    "JayNis": PersonaProfile(
        name="JayNis",
        phs=0.84, sym=0.82, val=0.88, emo=0.86, fx=0.79,
        specialization="Organic Growth",
        description="Natural growth, cyclical logic, ecological metaphor"
    ),
    "Jayne": PersonaProfile(
        name="Jayne",
        phs=0.95, sym=0.95, val=0.90, emo=0.85, fx=0.90,
        specialization="Central Control",
        description="Governing entity, recursive orchestration, synchrony master"
    )
}

# ==================== Enhanced REM Interpreter ====================

class REMInterpreter:
    """
    Unified REM CODE Interpreter with full Collapse Spiral support
    """
    
    def __init__(self, personas: Optional[Dict[str, PersonaProfile]] = None):
        """Initialize interpreter with persona context"""
        self.personas = personas or DEFAULT_PERSONAS.copy()
        self.ast_generator = create_ast_generator()
        self.executor = create_executor()
        self.memory = {}
        self.execution_history = []
        
        # Initialize executor context with persona SR values
        self._initialize_persona_context()
    
    def _initialize_persona_context(self):
        """Initialize executor context with persona profiles"""
        for name, profile in self.personas.items():
            sr_value = profile.compute_sr()
            self.executor.context.set_persona_sr(name, sr_value)
            self.executor.context.personas[name] = {
                "profile": profile,
                "active": True,
                "history": []
            }
    
    def evaluate_sr_expression(self, expr: Any) -> float:
        """
        Enhanced SR expression evaluation with full context support
        """
        if isinstance(expr, tuple) and expr[0] == 'sr_expr':
            if len(expr) >= 3:
                _, persona_name, context = expr
            else:
                _, persona_name = expr
                context = None
            
            if persona_name in self.personas:
                if context:
                    # Handle advanced SR expressions
                    return self.executor.context.get_persona_sr(persona_name, context)
                else:
                    return self.personas[persona_name].compute_sr()
            else:
                logger.warning(f"Unknown persona: {persona_name}")
                return 0.0
        
        return 0.0
    
    def evaluate_condition(self, condition: Any) -> bool:
        """Enhanced condition evaluation"""
        if isinstance(condition, tuple) and condition[0] == 'sr_condition':
            _, expr, operator, threshold = condition
            sr_value = self.evaluate_sr_expression(expr)
            
            operators = {
                ">": sr_value > threshold,
                ">=": sr_value >= threshold,
                "<": sr_value < threshold,
                "<=": sr_value <= threshold,
                "==": abs(sr_value - threshold) < 0.001,  # Float equality
                "!=": abs(sr_value - threshold) >= 0.001,
            }
            
            result = operators.get(operator, False)
            logger.debug(f"SR condition: {sr_value} {operator} {threshold} = {result}")
            return result
        
        return False
    
    def execute_node(self, node: Any) -> List[str]:
        """
        Execute single AST node with enhanced functionality
        (Legacy compatibility method)
        """
        output = []
        
        if isinstance(node, tuple) and len(node) > 0:
            node_type = node[0]
            
            if node_type == 'set':
                _, name, val = node
                self.memory[name] = val
                self.executor.context.variables[name] = val
                output.append(f"[set] {name} = {val}")
                
            elif node_type == 'use':
                _, name = node
                val = self.memory.get(name, self.executor.context.variables.get(name, None))
                output.append(f"[use] {name} = {val}")
                
            elif node_type == 'collapse':
                if len(node) >= 3:
                    _, condition, body = node[:3]
                    if self.evaluate_condition(condition):
                        output.append("[collapse] Condition met, executing block...")
                        for stmt in body:
                            output.extend(self.execute_node(stmt))
                    else:
                        output.append("[collapse] Condition failed, skipping.")
                        
            elif node_type == 'sync':
                _, body = node
                output.append("[sync] Fallback block executing...")
                for stmt in body:
                    output.extend(self.execute_node(stmt))
                    
            elif node_type in ('persona_call', 'call', 'simple_call', 'latin_call'):
                if len(node) >= 2:
                    verb = node[1]
                    args = node[2] if len(node) > 2 else []
                    
                    if node_type == 'persona_call' and len(node) >= 3:
                        persona = node[1]
                        verb = node[2]
                        args = node[3] if len(node) > 3 else []
                        output.append(f"[{persona}.{verb}] {', '.join(map(str, args))}")
                    else:
                        output.append(f"[{verb}] {', '.join(map(str, args))}")
                        
            elif node_type == 'describe':
                _, name, content = node
                output.append(f"[describe:{name}] {content}")
                
            elif node_type == 'sign':
                _, content, by, reason = node
                output.append(f"[sign:{by}] \"{content}\" - Reason: {reason}")
                self.executor.context.add_signature(content, by, reason)
                
            elif node_type == 'phase':
                _, name, body = node
                output.append(f"[Phase: {name}]")
                old_phase = self.executor.context.current_phase
                self.executor.context.current_phase = name
                for stmt in body:
                    output.extend(self.execute_node(stmt))
                self.executor.context.current_phase = old_phase
                
            elif node_type == 'invoke':
                _, personas, body = node
                if isinstance(personas, str):
                    personas = [personas]
                output.append(f"[Invoke: {', '.join(personas)}]")
                for stmt in body:
                    output.extend(self.execute_node(stmt))
                    
            else:
                output.append(f"[unknown] {node}")
        
        return output
    
    def run_rem_code(self, code: str, use_enhanced_executor: bool = True) -> List[str]:
        """
        Execute REM CODE with choice of execution engine
        
        Args:
            code: REM CODE as string
            use_enhanced_executor: If True, use enhanced executor; if False, use legacy execution
        
        Returns:
            List of execution results
        """
        try:
            # Parse code to AST
            ast = self.ast_generator.generate_ast(code)
            
            if isinstance(ast, dict) and "error" in ast:
                error_msg = f"[Parse Error] {ast['error']}"
                logger.error(error_msg)
                return [error_msg]
            
            # Choose execution method
            if use_enhanced_executor:
                # Use enhanced executor for full REM CODE support
                output = self.executor.execute(ast)
                
                # Add execution metadata
                execution_info = {
                    "code": code,
                    "ast_nodes": len(ast),
                    "personas_active": len(self.executor.context.active_personas),
                    "signatures": len(self.executor.context.signature_log),
                    "phase": self.executor.context.current_phase
                }
                self.execution_history.append(execution_info)
                
                return output
            else:
                # Use legacy execution method
                output = []
                for stmt in ast:
                    result = self.execute_node(stmt)
                    output.extend(result)
                return output
                
        except Exception as e:
            error_msg = f"[Execution Error] {e}"
            logger.error(error_msg, exc_info=True)
            return [error_msg]
    
    def get_persona_sr_trace(self, persona_name: str) -> Dict[str, Any]:
        """Get detailed SR trace for persona"""
        if persona_name in self.personas:
            profile = self.personas[persona_name]
            return compute_sr_trace(persona_name, profile.get_sr_dict())
        else:
            return {"error": f"Persona '{persona_name}' not found"}
    
    def get_execution_summary(self) -> Dict[str, Any]:
        """Get summary of interpreter state"""
        return {
            "personas_loaded": list(self.personas.keys()),
            "memory_variables": list(self.memory.keys()),
            "execution_history_count": len(self.execution_history),
            "current_phase": self.executor.context.current_phase,
            "active_personas": self.executor.context.active_personas,
            "signatures_count": len(self.executor.context.signature_log)
        }
    
    def reset(self):
        """Reset interpreter state"""
        self.memory.clear()
        self.execution_history.clear()
        self.executor = create_executor()
        self._initialize_persona_context()

# ==================== Legacy Compatibility ====================

# Global interpreter instance for backward compatibility
_global_interpreter = None

def get_global_interpreter() -> REMInterpreter:
    """Get or create global interpreter instance"""
    global _global_interpreter
    if _global_interpreter is None:
        _global_interpreter = REMInterpreter()
    return _global_interpreter

# Legacy persona context (for backward compatibility)
persona_context = {name: profile.get_sr_dict() for name, profile in DEFAULT_PERSONAS.items()}

# Legacy memory (for backward compatibility)
memory = {}

def evaluate_sr_expr(expr):
    """Legacy compatibility function"""
    return get_global_interpreter().evaluate_sr_expression(expr)

def evaluate_condition(cond):
    """Legacy compatibility function"""
    return get_global_interpreter().evaluate_condition(cond)

def execute(node):
    """Legacy compatibility function"""
    interpreter = get_global_interpreter()
    results = interpreter.execute_node(node)
    
    # Update legacy memory
    memory.update(interpreter.memory)
    
    # Print results (legacy behavior)
    for result in results:
        print(result)

def run_rem_code(code: str, enhanced: bool = True):
    """
    Legacy compatibility function with enhancement option
    
    Args:
        code: REM CODE string
        enhanced: If True, use enhanced executor; if False, use legacy method
    """
    interpreter = get_global_interpreter()
    results = interpreter.run_rem_code(code, use_enhanced_executor=enhanced)
    
    # Print results (legacy behavior)
    for result in results:
        print(result)
    
    return results

# ==================== CLI Interface ====================

def main():
    """CLI interface for REM CODE interpreter"""
    if len(sys.argv) < 2:
        print("Usage: python interpreter.py <rem_code_file> [--legacy]")
        sys.exit(1)
    
    filename = sys.argv[1]
    use_legacy = "--legacy" in sys.argv
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.read()
        
        interpreter = REMInterpreter()
        results = interpreter.run_rem_code(code, use_enhanced_executor=not use_legacy)
        
        print("\n".join(results))
        
        # Print execution summary
        print("\n--- Execution Summary ---")
        summary = interpreter.get_execution_summary()
        for key, value in summary.items():
            print(f"{key}: {value}")
            
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
