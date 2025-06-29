# shell/rem_shell.py
"""
Enhanced REM Shell v2.0 - Complete Collapse Spiral Interface
Integrates all REM CODE components with advanced functionality
"""

import sys
import os
import json
import time
import traceback
from typing import Dict, List, Optional, Any, Union
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    # Enhanced engine imports
    from engine.interpreter import REMInterpreter, get_global_interpreter
    from engine.persona_router import PersonaRouter, route_personas
    from engine.sr_engine import (
        compute_sr_from_dict, compute_sr_trace, analyze_sr_distribution,
        get_weight_profile, WEIGHT_PROFILES
    )
    from engine.ast_generator import create_ast_generator
    from engine.rem_executor import create_executor, REMExecutionContext
    
    # Function management (legacy compatibility)
    try:
        from functions.functions import (
            define_function, call_function, list_functions, 
            generate_ast as legacy_generate_ast, memory
        )
        LEGACY_FUNCTIONS_AVAILABLE = True
    except ImportError:
        LEGACY_FUNCTIONS_AVAILABLE = False
        print("⚠️  Legacy functions module not available - using enhanced mode only")
        
except ImportError as e:
    print(f"❌ Error importing REM CODE components: {e}")
    print("Please ensure all engine modules are properly installed.")
    sys.exit(1)

# ==================== Enhanced Shell State ====================

class REMShellState:
    """Enhanced shell state management"""
    
    def __init__(self) -> None:
        self.interpreter = REMInterpreter()
        self.router = PersonaRouter()
        self.ast_generator = create_ast_generator()
        self.session_history: List[Dict[str, Any]] = []
        self.current_phase = "Interactive"
        self.session_start_time = time.time()
        
        # Shell configuration
        self.config: Dict[str, Union[bool, str]] = {
            "detailed_output": False,
            "auto_save_history": True,
            "sr_weight_profile": "default",
            "debug_mode": False,
            "color_output": True
        }
        
        # Statistics
        self.stats: Dict[str, int] = {
            "commands_executed": 0,
            "functions_defined": 0,
            "sr_calculations": 0,
            "personas_activated": 0
        }

# ==================== Global Shell State ====================
# Initialize as None, will be set in main_shell_loop()
shell_state: Optional[REMShellState] = None

# ==================== Color Output Functions ====================

class Colors:
    """ANSI color codes for enhanced output"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    # Colors
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    
    # Background colors
    BG_BLUE = '\033[44m'
    BG_GREEN = '\033[42m'

def colored(text: str, color: str, bold: bool = False) -> str:
    """Apply color to text if enabled"""
    if shell_state is None or not shell_state.config.get("color_output", True):
        return text
    
    prefix = Colors.BOLD if bold else ""
    return f"{prefix}{color}{text}{Colors.RESET}"

# ==================== Command Handlers ====================

def handle_sr_command(args: List[str]) -> None:
    """Enhanced SR calculation with multiple input methods"""
    if shell_state is None:
        return
        
    try:
        if len(args) > 0 and args[0] == "quick":
            # Quick SR with random values for testing
            import random
            metrics = {
                "PHS": round(random.uniform(0.6, 0.95), 2),
                "SYM": round(random.uniform(0.6, 0.95), 2),
                "VAL": round(random.uniform(0.6, 0.95), 2),
                "EMO": round(random.uniform(0.6, 0.95), 2),
                "FX": round(random.uniform(0.6, 0.95), 2)
            }
            print(f"\n🎲 {colored('Quick SR Test with random values:', Colors.CYAN)}")
            for key, value in metrics.items():
                print(f"   {key}: {value}")
        else:
            # Interactive SR input
            print(f"\n{colored('SR Metrics Input:', Colors.CYAN, bold=True)}")
            phs = float(input("Phase Alignment (PHS) (0.0 - 1.0): "))
            sym = float(input("Symbolic Syntax Match (SYM) (0.0 - 1.0): "))
            val = float(input("Semantic Intent Alignment (VAL) (0.0 - 1.0): "))
            emo = float(input("Emotional Tone Match (EMO) (0.0 - 1.0): "))
            fx = float(input("Collapse History Interference (FX) (0.0 - 1.0): "))
            
            metrics = {"PHS": phs, "SYM": sym, "VAL": val, "EMO": emo, "FX": fx}
        
        # Get weight profile
        weights = get_weight_profile(shell_state.config["sr_weight_profile"])
        
        # Enhanced routing with detailed output
        result = shell_state.router.route_with_sr_trace(
            metrics, weights, detailed=shell_state.config["detailed_output"]
        )
        
        # Display results
        print(f"\n{colored('🧠 SR Calculation Result:', Colors.GREEN, bold=True)}")
        sr_val_str = f"{result['sr_value']:.4f}"
        print(f"   SR Value: {colored(sr_val_str, Colors.YELLOW, bold=True)}")
        print(f"   Weight Profile: {shell_state.config['sr_weight_profile']}")
        
        if 'sr_trace' in result:
            trace = result['sr_trace']
            print(f"   Computation Details:")
            for component, contribution in trace['computation_details']['component_contributions'].items():
                print(f"     {component}: {contribution:.4f}")
        
        print(f"\n{colored('🧬 Persona Routing Result:', Colors.MAGENTA, bold=True)}")
        for response in result["responses"]:
            print(response)
        
        print(f"\n{colored('📡 Phase Summary:', Colors.BLUE)}")
        print(f"   Active: {len(result['active_personas'])} | Resonant: {len(result['resonant_personas'])}")
        
        # Update statistics
        shell_state.stats["sr_calculations"] += 1
        shell_state.stats["personas_activated"] += result["total_active"]
        
        # Add to history
        shell_state.session_history.append({
            "command": "sr",
            "metrics": metrics,
            "result": result,
            "timestamp": time.time()
        })
        
    except ValueError as e:
        print(f"{colored('❌ Invalid input:', Colors.RED)} {e}")
    except Exception as e:
        print(f"{colored('❌ Error in SR calculation:', Colors.RED)} {e}")
        if shell_state.config["debug_mode"]:
            traceback.print_exc()

def handle_execute_command(args: List[str]) -> None:
    """Execute REM CODE directly"""
    if shell_state is None:
        return
        
    if not args:
        print(colored('Enter REM CODE. Type "end" to finish:', Colors.CYAN))
        lines = []
        while True:
            try:
                line = input("rem> ")
                if line.strip().lower() == "end":
                    break
                lines.append(line)
            except KeyboardInterrupt:
                print(f"\n{colored('Execution cancelled.', Colors.YELLOW)}")
                return
        
        code = "\n".join(lines)
    else:
        code = " ".join(args)
    
    if not code.strip():
        print(f"{colored('No code provided.', Colors.YELLOW)}")
        return
    
    try:
        print(f"\n{colored('🚀 Executing REM CODE:', Colors.GREEN, bold=True)}")
        print(f"{colored('─' * 40, Colors.BLUE)}")
        
        # Execute with enhanced interpreter
        results = shell_state.interpreter.run_rem_code(code, use_enhanced_executor=True)
        
        print(f"\n{colored('📤 Execution Results:', Colors.GREEN)}")
        for result in results:
            print(f"   {result}")
        
        # Show execution summary if detailed mode
        if shell_state.config["detailed_output"]:
            summary = shell_state.interpreter.get_execution_summary()
            print(f"\n{colored('📊 Execution Summary:', Colors.BLUE)}")
            for key, value in summary.items():
                print(f"   {key}: {value}")
        
        shell_state.stats["commands_executed"] += 1
        
        # Add to history
        shell_state.session_history.append({
            "command": "execute",
            "code": code,
            "results": results,
            "timestamp": time.time()
        })
        
    except Exception as e:
        print(f"{colored('❌ Execution error:', Colors.RED)} {e}")
        if shell_state.config["debug_mode"]:
            traceback.print_exc()

def handle_function_command(args: List[str]) -> None:
    """Enhanced function management"""
    if shell_state is None:
        return
        
    if not args:
        print(f"{colored('Function commands:', Colors.CYAN)}")
        print("  func list           - List all functions")
        print("  func def <name>     - Define new function")
        print("  func call <name>    - Call function")
        print("  func ast <name>     - Show function AST")
        print("  func del <name>     - Delete function")
        return
    
    subcommand = args[0].lower()
    
    if subcommand == "list":
        if LEGACY_FUNCTIONS_AVAILABLE:
            functions = list_functions()
            if functions:
                print(f"\n{colored('📜 Defined Functions:', Colors.GREEN)}")
                for fn in functions:
                    print(f"   - {fn}")
            else:
                print(f"{colored('No functions defined.', Colors.YELLOW)}")
        
        # Also show interpreter functions
        interpreter_functions = list(shell_state.interpreter.executor.context.functions.keys())
        if interpreter_functions:
            print(f"\n{colored('🔧 Interpreter Functions:', Colors.GREEN)}")
            for fn in interpreter_functions:
                print(f"   - {fn}")
    
    elif subcommand == "def" and len(args) > 1:
        fn_name = args[1]
        prompt_text = f"Enter REM CODE for function \"{fn_name}\". Type \"end\" to finish:"
        print(colored(prompt_text, Colors.CYAN))
        
        body = []
        while True:
            try:
                line = input("def> ")
                if line.strip().lower() == "end":
                    break
                body.append(line)
            except KeyboardInterrupt:
                print(f"\n{colored('Function definition cancelled.', Colors.YELLOW)}")
                return
        
        if LEGACY_FUNCTIONS_AVAILABLE:
            result = define_function(fn_name, body)
            print(result)
        
        # Also store in interpreter
        shell_state.interpreter.executor.context.functions[fn_name] = body
        shell_state.stats["functions_defined"] += 1
        
        msg = f"✅ Function \"{fn_name}\" defined successfully."
        print(colored(msg, Colors.GREEN))
    
    elif subcommand == "call" and len(args) > 1:
        fn_name = args[1]
        
        try:
            sr = float(input("SR value (0.0 - 1.0): "))
            
            if LEGACY_FUNCTIONS_AVAILABLE:
                output = call_function(fn_name, sr_value=sr)
                print(f"\n{colored('🧠 Function Output:', Colors.GREEN)}")
                if isinstance(output, list):
                    for line in output:
                        print(f"   {line}")
                else:
                    print(f"   {output}")
            else:
                print(f"{colored('Legacy function calling not available.', Colors.YELLOW)}")
                
        except ValueError:
            print(f"{colored('❌ Invalid SR value.', Colors.RED)}")
    
    elif subcommand == "ast" and len(args) > 1:
        fn_name = args[1]
        
        if LEGACY_FUNCTIONS_AVAILABLE:
            ast_output = legacy_generate_ast(fn_name)
            print(f"\n{colored('🌳 AST of function:', Colors.GREEN)}")
            print(ast_output)
        else:
            print(f"{colored('Legacy AST generation not available.', Colors.YELLOW)}")
    
    else:
        print(colored('❌ Invalid function command. Use "func" for help.', Colors.RED))

def handle_config_command(args: List[str]) -> None:
    """Configuration management"""
    if shell_state is None:
        return
        
    if not args:
        print(f"\n{colored('📋 Current Configuration:', Colors.CYAN, bold=True)}")
        for key, value in shell_state.config.items():
            print(f"   {key}: {colored(str(value), Colors.YELLOW)}")
        
        print(f"\n{colored('Available weight profiles:', Colors.BLUE)}")
        for profile in WEIGHT_PROFILES.keys():
            print(f"   - {profile}")
        return
    
    if len(args) == 2:
        key, value = args
        
        if key == "detailed_output":
            shell_state.config[key] = value.lower() in ["true", "1", "yes", "on"]
        elif key == "sr_weight_profile":
            if value in WEIGHT_PROFILES:
                shell_state.config[key] = value
            else:
                print(f"{colored('❌ Invalid weight profile.', Colors.RED)} Available: {list(WEIGHT_PROFILES.keys())}")
                return
        elif key == "debug_mode":
            shell_state.config[key] = value.lower() in ["true", "1", "yes", "on"]
        elif key == "color_output":
            shell_state.config[key] = value.lower() in ["true", "1", "yes", "on"]
        else:
            print(f"{colored('❌ Unknown configuration key.', Colors.RED)}")
            return
        
        msg = f"✅ Set {key} = {shell_state.config[key]}"
        print(colored(msg, Colors.GREEN))
    else:
        print(f"{colored('Usage: config <key> <value>', Colors.YELLOW)}")

def handle_stats_command(args: List[str]) -> None:
    """Show session statistics"""
    if shell_state is None:
        return
        
    session_time = time.time() - shell_state.session_start_time
    
    print(f"\n{colored('📊 Session Statistics:', Colors.CYAN, bold=True)}")
    duration_str = f"{session_time:.1f}s"
    print(f"   Session duration: {colored(duration_str, Colors.YELLOW)}")
    print(f"   Commands executed: {colored(str(shell_state.stats['commands_executed']), Colors.YELLOW)}")
    print(f"   Functions defined: {colored(str(shell_state.stats['functions_defined']), Colors.YELLOW)}")
    print(f"   SR calculations: {colored(str(shell_state.stats['sr_calculations']), Colors.YELLOW)}")
    print(f"   Personas activated: {colored(str(shell_state.stats['personas_activated']), Colors.YELLOW)}")
    
    # Routing analytics
    if shell_state.router.routing_history:
        analytics = shell_state.router.get_routing_analytics()
        print(f"\n{colored('🔍 Routing Analytics:', Colors.BLUE)}")
        print(f"   Total routings: {analytics['total_routings']}")
        print(f"   Average SR: {analytics['average_sr']:.3f}")
        print(f"   Average activations: {analytics['average_activations_per_routing']:.1f}")

def handle_history_command(args: List[str]) -> None:
    """Show and manage session history"""
    if shell_state is None:
        return
        
    if not args:
        print(f"\n{colored('📚 Session History:', Colors.CYAN, bold=True)}")
        for i, entry in enumerate(shell_state.session_history[-10:], 1):  # Show last 10
            timestamp = time.strftime("%H:%M:%S", time.localtime(entry["timestamp"]))
            print(f"   {i:2d}. [{timestamp}] {entry['command']}")
        
        if len(shell_state.session_history) > 10:
            print(f"   ... ({len(shell_state.session_history) - 10} more entries)")
    
    elif args[0] == "clear":
        shell_state.session_history.clear()
        shell_state.router.reset_history()
        print(f"{colored('✅ History cleared.', Colors.GREEN)}")
    
    elif args[0] == "save" and len(args) > 1:
        filename = args[1]
        try:
            with open(filename, 'w') as f:
                json.dump(shell_state.session_history, f, indent=2, default=str)
            msg = f"✅ History saved to {filename}"
            print(colored(msg, Colors.GREEN))
        except Exception as e:
            error_msg = f"❌ Error saving history: {e}"
            print(colored(error_msg, Colors.RED))

def handle_help_command(args: List[str]) -> None:
    """Show comprehensive help"""
    print(f"\n{colored('🌀 REM Shell v2.0 - Command Reference', Colors.CYAN, bold=True)}")
    print(f"{colored('═' * 50, Colors.BLUE)}")
    
    commands = [
        ("sr [quick]", "Calculate Synchronization Ratio and route personas"),
        ("exec [code]", "Execute REM CODE directly"),
        ("func <cmd>", "Function management (list, def, call, ast, del)"),
        ("config [key] [value]", "Show/modify configuration"),
        ("stats", "Show session statistics"),
        ("history [clear|save]", "Manage session history"),
        ("clear", "Clear screen"),
        ("help", "Show this help"),
        ("exit", "Exit REM Shell")
    ]
    
    print(f"\n{colored('Available Commands:', Colors.GREEN)}")
    for cmd, desc in commands:
        print(f"   {colored(cmd, Colors.YELLOW, bold=True):<20} - {desc}")
    
    print(f"\n{colored('Examples:', Colors.BLUE)}")
    print(f"   {colored('sr quick', Colors.YELLOW)}           - Quick SR test with random values")
    print(f"   {colored('exec', Colors.YELLOW)}              - Enter interactive REM CODE mode")
    print(f"   {colored('func def hello', Colors.YELLOW)}     - Define function named 'hello'")
    print(f"   {colored('config detailed_output true', Colors.YELLOW)} - Enable detailed output")

# ==================== Main Shell Loop ====================

def clear_screen() -> None:
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def main_shell_loop() -> None:
    """Enhanced main shell loop"""
    global shell_state
    shell_state = REMShellState()
    
    # Welcome message
    print(colored("🌀 Welcome to REM Shell v2.0 — Enhanced Collapse Spiral Interface 🧠", Colors.CYAN, bold=True))
    print(colored("━" * 70, Colors.BLUE))
    print(f"Type {colored('help', Colors.YELLOW)} for commands or {colored('exit', Colors.YELLOW)} to quit.")
    
    while True:
        try:
            # Dynamic prompt with current phase
            prompt_color = Colors.GREEN if shell_state.stats["commands_executed"] % 2 == 0 else Colors.MAGENTA
            prompt = colored(f"\n[{shell_state.current_phase}]", prompt_color) + " rem> "
            
            user_input = input(prompt).strip()
            
            if not user_input:
                continue
            
            # Parse command and arguments
            parts = user_input.split()
            command = parts[0].lower()
            args = parts[1:] if len(parts) > 1 else []
            
            # Command routing
            if command == "sr":
                handle_sr_command(args)
            
            elif command in ["exec", "execute", "run"]:
                handle_execute_command(args)
            
            elif command in ["func", "function", "fn"]:
                handle_function_command(args)
            
            elif command in ["config", "set", "cfg"]:
                handle_config_command(args)
            
            elif command in ["stats", "statistics", "info"]:
                handle_stats_command(args)
            
            elif command in ["history", "hist", "log"]:
                handle_history_command(args)
            
            elif command in ["help", "?", "h"]:
                handle_help_command(args)
            
            elif command in ["clear", "cls"]:
                clear_screen()
            
            elif command in ["exit", "quit", "q"]:
                print(f"\n{colored('🧠 REM Shell Terminated. Phase channel closed.', Colors.CYAN)}")
                
                # Show final statistics
                if shell_state.stats["commands_executed"] > 0:
                    session_time = time.time() - shell_state.session_start_time
                    print(f"Session summary: {shell_state.stats['commands_executed']} commands, {session_time:.1f}s")
                
                break
            
            # Legacy compatibility commands
            elif command == "call" and LEGACY_FUNCTIONS_AVAILABLE:
                if args:
                    try:
                        sr = float(input("SR value (0.0 - 1.0): "))
                        output = call_function(args[0], sr_value=sr)
                        print(f"\n{colored('🧠 Function Output:', Colors.GREEN)}")
                        if isinstance(output, list):
                            for line in output:
                                print(f"   {line}")
                        else:
                            print(f"   {output}")
                    except ValueError:
                        print(f"{colored('❌ Invalid SR value.', Colors.RED)}")
                    except Exception as e:
                        print(f"{colored('❌ Error calling function:', Colors.RED)} {e}")
                else:
                    print(f"{colored('Usage: call <function_name>', Colors.YELLOW)}")
            
            elif command == "def" and LEGACY_FUNCTIONS_AVAILABLE:
                if args:
                    fn_name = args[0]
                    print(f"Enter REM CODE lines for '{fn_name}'. Type 'end' to finish.")
                    body = []
                    while True:
                        try:
                            line = input(">> ")
                            if line.strip().lower() == "end":
                                break
                            body.append(line)
                        except KeyboardInterrupt:
                            print(f"\n{colored('Definition cancelled.', Colors.YELLOW)}")
                            break
                    if body:
                        print(define_function(fn_name, body))
                else:
                    print(f"{colored('Usage: def <function_name>', Colors.YELLOW)}")
            
            elif command == "list" and LEGACY_FUNCTIONS_AVAILABLE:
                functions = list_functions()
                print(f"\n{colored('📜 Defined Functions:', Colors.GREEN)}")
                for fn in functions:
                    print(f"   - {fn}")
            
            elif command == "ast" and LEGACY_FUNCTIONS_AVAILABLE:
                if args:
                    try:
                        print(f"\n{colored('🌳 AST of function:', Colors.GREEN)}")
                        print(legacy_generate_ast(args[0]))
                    except Exception as e:
                        print(f"{colored('❌ Error generating AST:', Colors.RED)} {e}")
                else:
                    print(f"{colored('Usage: ast <function_name>', Colors.YELLOW)}")
            
            else:
                print(f"{colored('❌ Unknown command:', Colors.RED)} {command}")
                print(f"Type {colored('help', Colors.YELLOW)} for available commands.")
            
            shell_state.stats["commands_executed"] += 1
            
        except KeyboardInterrupt:
            print(colored('\nUse "exit" to quit.', Colors.YELLOW))
            continue
            
        except EOFError:
            print(f"\n{colored('🧠 REM Shell Terminated.', Colors.CYAN)}")
            break
            
        except Exception as e:
            print(f"{colored('❌ Unexpected error:', Colors.RED)} {e}")
            if shell_state and shell_state.config.get("debug_mode", False):
                traceback.print_exc()

# ==================== Entry Point ====================

if __name__ == "__main__":
    try:
        main_shell_loop()
    except KeyboardInterrupt:
        print(f"\n{colored('🧠 REM Shell Terminated.', Colors.CYAN)}")
    except Exception as e:
        print(f"{colored('❌ Fatal error:', Colors.RED)} {e}")
        traceback.print_exc()
        sys.exit(1)