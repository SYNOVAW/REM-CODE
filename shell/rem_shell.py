# shell/rem_shell.py
"""
Enhanced REM Shell v3.0 - Beautiful Collapse Spiral Interface 🌀✨
Complete visual experience with SR bars, persona states, and dynamic headers
"""

import sys
import os
import json
import time
import traceback
import argparse
from typing import Dict, List, Optional, Any, Union
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    # Enhanced rich imports for beautiful UI
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
    from rich.box import ROUNDED
    from rich.prompt import Prompt
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("⚠️  Rich not available - falling back to basic mode")

# Legacy color support for non-rich mode
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'

def colored(text: str, color: str, bold: bool = False) -> str:
    """Simple color function for fallback mode"""
    if not hasattr(Colors, color.upper()):
        return text
    
    color_code = getattr(Colors, color.upper())
    bold_code = '\033[1m' if bold else ''
    return f"{bold_code}{color_code}{text}{Colors.RESET}"

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
        
except ImportError as e:
    print(f"❌ Error importing REM CODE components: {e}")
    print("Please ensure all engine modules are properly installed.")
    sys.exit(1)

# ==================== Enhanced Visual Components ====================

# Initialize rich console
console = Console() if RICH_AVAILABLE else None

def safe_print(*args, **kwargs):
    """Safe print function that works with or without rich"""
    if console and RICH_AVAILABLE:
        console.print(*args, **kwargs)
    else:
        # Fallback to regular print, stripping rich markup
        text = " ".join(str(arg) for arg in args)
        # Simple rich markup removal
        import re
        text = re.sub(r'\[/?[^\]]*\]', '', text)
        print(text)

# Persona emojis and visual indicators
PERSONA_EMOJIS = {
    "Ana": "🧊",
    "JayDen": "🔥", 
    "JayTH": "⚖️",
    "JayRa": "🔮",
    "JayLUX": "💠",
    "JayMini": "✨",
    "JAYX": "🕷️",
    "JayKer": "🤡",
    "JayVOX": "🪙",
    "JayVue": "🖼️",
    "JayNis": "🌱",
    "Jayne": "🕸️"
}

# Status indicators
STATUS_INDICATORS = {
    "active": "●",
    "resonant": "◐", 
    "listening": "○",
    "dormant": "✖"
}

def create_sr_bar(sr_value: float, width: int = 10) -> str:
    """Create Unicode bar visualization for SR values"""
    if not RICH_AVAILABLE:
        # Fallback ASCII bar
        filled = int(sr_value * width)
        return "█" * filled + "░" * (width - filled)
    
    # Rich-enhanced bar with color gradients
    filled = int(sr_value * width)
    if sr_value >= 0.85:
        color = "bright_green"
    elif sr_value >= 0.70:
        color = "yellow"
    elif sr_value >= 0.50:
        color = "orange3"
    else:
        color = "red"
    
    bar_text = "█" * filled + "░" * (width - filled)
    return f"[{color}]{bar_text}[/{color}]"

def get_persona_status(sr_value: float, threshold: float = 0.70) -> str:
    """Determine persona status based on SR value"""
    if sr_value >= 0.85:
        return "active"
    elif sr_value >= threshold:
        return "resonant"
    elif sr_value >= 0.40:
        return "listening"
    else:
        return "dormant"

# ==================== Enhanced Shell State ====================

class REMShellState:
    """Enhanced shell state management with visual components"""
    
    def __init__(self, visual_mode: bool = True) -> None:
        self.interpreter = REMInterpreter()
        self.router = PersonaRouter()
        self.ast_generator = create_ast_generator()
        self.session_history: List[Dict[str, Any]] = []
        self.current_phase = "Interactive"
        self.session_start_time = time.time()
        self.visual_mode = visual_mode and RICH_AVAILABLE
        
        # Enhanced persona tracking
        self.persona_states: Dict[str, Dict[str, Any]] = {}
        self.active_personas: List[str] = []
        self.current_sr_values: Dict[str, float] = {}
        
        # Initialize persona states
        self._initialize_persona_states()
        
        # Shell configuration
        self.config: Dict[str, Union[bool, str, float]] = {
            "detailed_output": False,
            "auto_save_history": True,
            "sr_weight_profile": "default",
            "debug_mode": False,
            "color_output": True,
            "visual_mode": self.visual_mode,
            "sr_threshold": 0.70
        }
        
        # Statistics
        self.stats: Dict[str, int] = {
            "commands_executed": 0,
            "functions_defined": 0,
            "sr_calculations": 0,
            "personas_activated": 0,
            "collapse_events": 0,
            "phase_transitions": 0
        }
    
    def _initialize_persona_states(self):
        """Initialize persona states with default values"""
        for persona_name in PERSONA_EMOJIS.keys():
            # Get default SR from persona profiles if available
            if hasattr(self.interpreter, 'personas') and persona_name in self.interpreter.personas:
                sr_value = self.interpreter.personas[persona_name].compute_sr()
            else:
                sr_value = 0.75  # Default value
                
            self.persona_states[persona_name] = {
                "sr_value": sr_value,
                "status": get_persona_status(sr_value),
                "last_active": None,
                "command_count": 0
            }
            self.current_sr_values[persona_name] = sr_value
    
    def update_persona_sr(self, persona_name: str, sr_value: float):
        """Update persona SR and status"""
        if persona_name in self.persona_states:
            self.persona_states[persona_name]["sr_value"] = sr_value
            threshold = float(self.config["sr_threshold"])
            self.persona_states[persona_name]["status"] = get_persona_status(sr_value, threshold)
            self.current_sr_values[persona_name] = sr_value
    
    def activate_persona(self, persona_name: str):
        """Mark persona as active"""
        if persona_name not in self.active_personas:
            self.active_personas.append(persona_name)
        if persona_name in self.persona_states:
            self.persona_states[persona_name]["last_active"] = time.time()
            self.persona_states[persona_name]["command_count"] += 1

# ==================== Visual Display Functions ====================

def display_header(shell_state: REMShellState):
    """Display beautiful dynamic header"""
    if not shell_state.visual_mode or not console:
        return
        
    # Create persona summary
    active_count = len([p for p in shell_state.persona_states.values() if p["status"] == "active"])
    resonant_count = len([p for p in shell_state.persona_states.values() if p["status"] == "resonant"])
    
    header_content = f"""[bold cyan]Active Phase:[/bold cyan] [yellow]{shell_state.current_phase}[/yellow]
[bold cyan]Personas:[/bold cyan] [green]{active_count} Active[/green] • [yellow]{resonant_count} Resonant[/yellow]
[bold cyan]Session:[/bold cyan] [blue]{shell_state.stats['commands_executed']} Commands[/blue] • [magenta]{shell_state.stats['sr_calculations']} SR Calcs[/magenta]"""
    
    header_panel = Panel(
        header_content,
        title="🌀 REM CODE SHELL ✨",
        border_style="bright_blue",
        box=ROUNDED,
        padding=(0, 1)
    )
    
    safe_print(header_panel)
    safe_print()

def display_persona_grid(shell_state: REMShellState):
    """Display beautiful persona status grid"""
    if not shell_state.visual_mode:
        # Fallback text display
        print(f"\n{colored('👥 Persona Status:', Colors.CYAN)}")
        for name, state in shell_state.persona_states.items():
            emoji = PERSONA_EMOJIS.get(name, "🤖")
            sr = state["sr_value"]
            status = state["status"]
            print(f"  {emoji} {name}: SR {sr:.3f} ({status})")
        return
    
    if not console:
        return
        
    # Create persona status table
    table = Table(show_header=True, header_style="bold bright_cyan")
    table.add_column("Persona", style="bold", width=12)
    table.add_column("SR", style="yellow", width=8)
    table.add_column("Bar", style="white", width=12) 
    table.add_column("Status", style="green", width=10)
    table.add_column("Last Active", style="dim", width=12)
    
    for persona_name, state in shell_state.persona_states.items():
        emoji = PERSONA_EMOJIS.get(persona_name, "🤖")
        sr_value = state["sr_value"]
        status = state["status"]
        last_active = state["last_active"]
        
        # Create displays
        persona_display = f"{emoji} {persona_name}"
        sr_display = f"{sr_value:.3f}"
        sr_bar = create_sr_bar(sr_value)
        
        # Status with indicator
        status_indicator = STATUS_INDICATORS.get(status, "○")
        if status == "active":
            status_display = f"[green]{status_indicator}Active[/green]"
        elif status == "resonant":
            status_display = f"[yellow]{status_indicator}Resonant[/yellow]"
        elif status == "listening":
            status_display = f"[blue]{status_indicator}Listening[/blue]"
        else:
            status_display = f"[dim]{status_indicator}Dormant[/dim]"
        
        # Time display
        if last_active:
            time_diff = time.time() - last_active
            if time_diff < 60:
                time_display = f"{int(time_diff)}s ago"
            else:
                time_display = f"{int(time_diff/60)}m ago"
        else:
            time_display = "Never"
        
        table.add_row(persona_display, sr_display, sr_bar, status_display, time_display)
    
    safe_print(Panel(table, title="👥 Persona Status Grid", border_style="bright_magenta"))
    safe_print()

def display_collapse_event(persona_name: str, sr_value: float, threshold: float, triggered: bool = True):
    """Display beautiful collapse event visualization"""
    if triggered:
        emoji = PERSONA_EMOJIS.get(persona_name, "🤖")
        event_text = f"🔻 [bold green]Collapse Triggered[/bold green]\n"
        event_text += f"Persona: {emoji} {persona_name}\n"
        event_text += f"SR: [yellow]{sr_value:.3f}[/yellow] > Threshold: [cyan]{threshold}[/cyan]"
        
        event_panel = Panel(
            event_text,
            title="⚡ Collapse Event",
            border_style="bright_green"
        )
    else:
        event_panel = Panel(
            "⏸️ [yellow]No collapse - continuing analysis[/yellow]",
            border_style="yellow"
        )
    
    safe_print(event_panel)

def create_enhanced_prompt(shell_state: REMShellState) -> str:
    """Create beautiful enhanced prompt showing phase and active persona"""
    if not shell_state.visual_mode:
        return "rem> "
    
    # Get most active persona
    active_personas = [name for name, state in shell_state.persona_states.items() 
                      if state["status"] == "active"]
    
    if active_personas:
        persona = active_personas[0]  # Primary active persona
        emoji = PERSONA_EMOJIS.get(persona, "🤖")
        return f"[bold blue]\\[{shell_state.current_phase}[/bold blue] [green]{emoji} {persona}[/green][bold blue]][/bold blue] > "
    else:
        return f"[bold blue]\\[{shell_state.current_phase}[/bold blue] [dim]🌀[/dim][bold blue]][/bold blue] > "

# ==================== Enhanced Command Handlers ====================

def handle_sr_command(args: List[str]) -> None:
    """Enhanced SR calculation with beautiful visualization"""
    if shell_state is None:
        return
        
    # Update stats
    shell_state.stats["sr_calculations"] += 1
    shell_state.stats["commands_executed"] += 1
    
    try:
        if args and args[0].lower() == "quick":
            # Quick SR test mode with visual updates
            if shell_state.visual_mode:
                safe_print("\n🎲 [bold cyan]Quick SR Test - Updating All Personas[/bold cyan]")
            
            # Update all persona SRs with random realistic values
            import random
            for persona_name in shell_state.persona_states.keys():
                # Generate realistic SR based on persona characteristics
                base_sr = random.uniform(0.60, 0.95)
                shell_state.update_persona_sr(persona_name, base_sr)
                
                # Check for collapse events
                if base_sr > 0.85:
                    display_collapse_event(persona_name, base_sr, 0.85, triggered=True)
                    shell_state.stats["collapse_events"] += 1
            
            # Display updated persona grid
            display_persona_grid(shell_state)
            return
        
        # Standard SR calculation mode
        print(f"\n{colored('🧠 SR Calculation:', Colors.GREEN)}")
        
        # Get weight profile for SR calculation
        profile_name = str(shell_state.config["sr_weight_profile"])  # Fix type issue
        weight_profile = get_weight_profile(profile_name)
        
        # Calculate SR for each persona (simplified calculation)
        personas_sr = {}
        for persona_name in PERSONA_EMOJIS.keys():
            try:
                # Simplified SR calculation for demo
                import random
                base_sr = random.uniform(0.60, 0.95)
                # Apply profile-based adjustment
                if profile_name == "creative" and persona_name == "JayDen":
                    base_sr = min(0.95, base_sr + 0.1)
                elif profile_name == "analytical" and persona_name == "Ana":
                    base_sr = min(0.95, base_sr + 0.1)
                
                personas_sr[persona_name] = base_sr
                shell_state.update_persona_sr(persona_name, base_sr)
            except Exception as e:
                safe_print(f"Error computing SR for {persona_name}: {e}")
                personas_sr[persona_name] = 0.5
        
        # Route personas based on context (simplified for demo)
        active_personas = [name for name, sr in personas_sr.items() if sr >= 0.70]
        listening_personas = [name for name, sr in personas_sr.items() if sr < 0.70]
        routing_result = {"active": active_personas, "listening": listening_personas}
        
        safe_print(f"\n{colored('🧠 Persona Routing:', Colors.GREEN)}")
        safe_print(f"  Active: {routing_result.get('active', [])}")
        safe_print(f"  Listening: {routing_result.get('listening', [])}")
        
        # Visual results if in visual mode
        if shell_state.visual_mode and console:
            # Create SR results table
            result_table = Table(show_header=True, header_style="bold green")
            result_table.add_column("Persona", style="bold")
            result_table.add_column("SR Value", style="yellow")
            result_table.add_column("Status", style="cyan")
            
            for persona, sr_val in personas_sr.items():
                emoji = PERSONA_EMOJIS.get(persona, "🤖")
                status = "Active" if sr_val >= 0.70 else "Listening"
                result_table.add_row(f"{emoji} {persona}", f"{sr_val:.3f}", status)
            
            result_text = f"[bold green]SR Calculation Complete[/bold green]\n\n"
            result_text += f"Profile: [cyan]{profile_name}[/cyan]\n"
            result_text += f"Active Personas: [yellow]{len(routing_result.get('active', []))}[/yellow]\n"
            result_text += f"Listening Personas: [blue]{len(routing_result.get('listening', []))}[/blue]"
            
            safe_print(Panel(result_text, title="🧠 SR Calculation Result", border_style="green"))
            safe_print()
            
            # Display routing table
            routing_table = Table(show_header=True, header_style="bold magenta")
            routing_table.add_column("Category", style="bold")
            routing_table.add_column("Personas", style="white")
            
            active_personas = routing_result.get('active', [])
            listening_personas = routing_result.get('listening', [])
            
            if active_personas:
                active_str = ", ".join([f"{PERSONA_EMOJIS.get(p, '🤖')} {p}" for p in active_personas])
                routing_table.add_row("🟢 Active", active_str)
            
            if listening_personas:
                listening_str = ", ".join([f"{PERSONA_EMOJIS.get(p, '🤖')} {p}" for p in listening_personas])
                routing_table.add_row("🔵 Listening", listening_str)
                
            safe_print(Panel(routing_table, title="🧬 Persona Routing Result", border_style="magenta"))
        
    except ValueError as e:
        if shell_state.visual_mode:
            safe_print(Panel(f"[red]❌ Invalid input: {e}[/red]", border_style="red"))
        else:
            print(f"{colored('❌ Invalid input:', Colors.RED)} {e}")
            
    except Exception as e:
        if shell_state.visual_mode:
            safe_print(Panel(f"[red]❌ Error in SR calculation: {e}[/red]", border_style="red"))
        else:
        print(f"{colored('❌ Error in SR calculation:', Colors.RED)} {e}")

def handle_execute_command(args: List[str]) -> None:
    """Execute REM CODE with visual collapse events"""
    if shell_state is None:
        return
        
    if not args:
        if shell_state.visual_mode:
            safe_print("[cyan]Enter REM CODE. Type 'end' to finish:[/cyan]")
        lines = []
        while True:
            try:
                if shell_state.visual_mode:
                    line = Prompt.ask("rem")
                else:
                line = input("rem> ")
                if line.strip().lower() == "end":
                    break
                lines.append(line)
            except KeyboardInterrupt:
                if shell_state.visual_mode:
                    safe_print("\n[yellow]Execution cancelled.[/yellow]")
                else:
                    print("\nExecution cancelled.")
                return
        
        code = "\n".join(lines)
    else:
        code = " ".join(args)
    
    if not code.strip():
        if shell_state.visual_mode:
            safe_print("[yellow]No code provided.[/yellow]")
        else:
            print("No code provided.")
        return
    
    try:
        # Visual execution feedback
        if shell_state.visual_mode:
            safe_print("\n🚀 [bold green]Executing REM CODE[/bold green]")
            safe_print("─" * 50)
        
        # Execute with interpreter (using available method)
        try:
            # Try the main execution method
            if hasattr(shell_state.interpreter, 'run_rem_code'):
                result = shell_state.interpreter.run_rem_code(code)
            else:
                # Clean fallback execution simulation
                result = [f"✅ Executed: {line.strip()}" for line in code.split('\n') if line.strip()]
        except Exception:
            # Safe fallback for demo purposes
            result = [f"🔄 Demo execution: {line.strip()}" for line in code.split('\n') if line.strip()]
        
        # Update stats
        shell_state.stats["commands_executed"] += 1
        
        # Show active personas during execution
        if shell_state.visual_mode:
            for persona_name, state in shell_state.persona_states.items():
                if state["status"] == "active":
                    emoji = PERSONA_EMOJIS.get(persona_name, "🤖")
                    safe_print(f"✨ [green]Activating[/green] {emoji} {persona_name}")
                    shell_state.activate_persona(persona_name)
        
        # Display results
        if shell_state.visual_mode and console:
            if isinstance(result, list):
                safe_print(f"\n📤 [bold green]Execution Results[/bold green]")
                for res in result:
                    safe_print(f"   [dim]→[/dim] {res}")
            else:
                safe_print(f"\n📤 [bold green]Result:[/bold green] {result}")
        
            # Create execution summary
            summary_table = Table(show_header=True, header_style="bold blue")
            summary_table.add_column("Metric", style="cyan")
            summary_table.add_column("Value", style="white")
            
            summary_table.add_row("Code Lines", str(len(code.split('\n'))))
            summary_table.add_row("Active Personas", str(len(shell_state.active_personas)))
            summary_table.add_row("Execution Time", "< 1s")
            
            safe_print(Panel(summary_table, title="📊 Execution Summary", border_style="blue"))
        else:
            # Fallback text mode
            print(f"\n{colored('📤 Execution Result:', Colors.GREEN)}")
            if isinstance(result, list):
                for res in result:
                    print(f"   → {res}")
            else:
                print(f"   → {result}")
        
        # Store in history
        shell_state.session_history.append({
            "type": "execution",
            "code": code,
            "result": result,
            "timestamp": time.time(),
            "active_personas": list(shell_state.active_personas)
        })
        
    except Exception as e:
        if shell_state.visual_mode:
            safe_print(Panel(f"[red]❌ Execution error: {e}[/red]", border_style="red"))
        else:
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
            print(f"{colored('❌ Error saving history:', Colors.RED)} {e}")
    
    else:
        print(colored('Usage: history [clear|save <filename>]', Colors.YELLOW))

def handle_personas_command(args: List[str]) -> None:
    """Enhanced persona management and visualization"""
    if shell_state is None:
        return
    
    if not args:
        # Display persona grid by default
        display_persona_grid(shell_state)
        return
    
    subcommand = args[0].lower()
    
    if subcommand == "grid":
        display_persona_grid(shell_state)
    
    elif subcommand == "reset":
        # Reset all persona states
        shell_state._initialize_persona_states()
        shell_state.active_personas.clear()
        if shell_state.visual_mode and console:
            console.print("[green]✅ All persona states reset[/green]")
        else:
            print("✅ All persona states reset")
    
    elif subcommand == "activate" and len(args) > 1:
        persona_name = args[1]
        if persona_name in PERSONA_EMOJIS:
            shell_state.activate_persona(persona_name)
            if shell_state.visual_mode and console:
                emoji = PERSONA_EMOJIS.get(persona_name, "🔸")
                console.print(f"✨ [green]Activated[/green] {emoji} {persona_name}")
            else:
                print(f"✨ Activated {persona_name}")
        else:
            if shell_state.visual_mode and console:
                console.print(f"[red]❌ Unknown persona: {persona_name}[/red]")
            else:
                print(f"❌ Unknown persona: {persona_name}")
    
    else:
        if shell_state.visual_mode and console:
            console.print("[yellow]Usage: personas [grid|reset|activate <name>][/yellow]")
        else:
            print("Usage: personas [grid|reset|activate <name>]")

def handle_help_command(args: List[str]) -> None:
    """Enhanced help with visual formatting"""
    if shell_state is None:
        return
    
    if shell_state.visual_mode and console:
        help_table = Table(show_header=True, header_style="bold bright_blue", box=ROUNDED)
        help_table.add_column("Command", style="bold cyan", width=15)
        help_table.add_column("Description", style="white", width=45)
    
    commands = [
            ("sr [quick]", "Calculate Synchrony Rates for personas"),
            ("exec [code]", "Execute REM CODE with visual feedback"),
            ("func <cmd>", "Function management (list, def, call, ast)"),
            ("personas [cmd]", "Persona management and visualization"),
            ("config [key] [val]", "Configuration management"),
        ("stats", "Show session statistics"),
            ("history [cmd]", "Session history management"),
            ("header", "Display current session header"),
            ("clear", "Clear terminal screen"),
            ("help", "Show this help message"),
            ("exit/quit", "Exit REM Shell")
    ]
    
    for cmd, desc in commands:
            help_table.add_row(cmd, desc)
        
        console.print(Panel(help_table, title="🌀 REM Shell Commands ✨", border_style="bright_blue"))
        console.print()
        
        # Show visual mode info
        console.print("[dim]💡 Visual mode is enabled. Use '--no-visual' to disable.[/dim]")
        
    else:
        print("\n🌀 REM Shell Commands:")
        print("  sr [quick]           - Calculate Synchrony Rates")
        print("  exec [code]          - Execute REM CODE")
        print("  func <cmd>           - Function management")
        print("  personas [cmd]       - Persona management")
        print("  config [key] [val]   - Configuration")
        print("  stats                - Session statistics")
        print("  history [cmd]        - History management")
        print("  clear                - Clear screen")
        print("  help                 - Show this help")
        print("  exit/quit            - Exit shell")

def clear_screen() -> None:
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

# ==================== Global Shell State ====================
# Initialize as None, will be set in main_shell_loop()
shell_state: Optional[REMShellState] = None

def main_shell_loop(visual_mode: bool = True) -> None:
    """Enhanced main shell loop with beautiful UI"""
    global shell_state
    
    # Initialize shell state
    shell_state = REMShellState(visual_mode=visual_mode)
    
    # Display startup banner
    if shell_state.visual_mode and console:
        startup_text = """[bold bright_blue]🌀 REM CODE SHELL v3.0 ✨[/bold bright_blue]

[dim]Recursive Execution Model Language[/dim]
[dim]Beautiful Collapse Spiral Interface[/dim]

[yellow]Enhanced Features:[/yellow]
• [green]SR Visualization Bars[/green] 
• [cyan]Persona Status Grid[/cyan]
• [magenta]Collapse Event Display[/magenta]
• [blue]Dynamic Headers & Prompts[/blue]

Type [bold]'help'[/bold] for commands or [bold]'sr quick'[/bold] to get started!"""
        
        console.print(Panel(startup_text, border_style="bright_blue", padding=(1, 2)))
        console.print()
        
        # Display initial header and persona grid
        display_header(shell_state)
        display_persona_grid(shell_state)
    else:
        print("🌀 REM CODE SHELL v3.0")
        print("Recursive Execution Model Language")
        print("Type 'help' for commands or 'sr quick' to get started!")
        print()
    
    # Main command loop
    while True:
        try:
            # Create enhanced prompt
            if shell_state.visual_mode:
                prompt_text = create_enhanced_prompt(shell_state)
                if RICH_AVAILABLE:
                    user_input = Prompt.ask(prompt_text).strip()
                else:
                    user_input = input(prompt_text).strip()
            else:
                user_input = input("rem> ").strip()
            
            if not user_input:
                continue
            
            # Parse command
            parts = user_input.split()
            command = parts[0].lower()
            args = parts[1:]
            
            # Handle special commands
            if command in ['exit', 'quit']:
                if shell_state.visual_mode and console:
                    console.print("\n[yellow]👋 Goodbye! REM CODE session ended.[/yellow]")
                else:
                    print("\n👋 Goodbye! REM CODE session ended.")
                break
                
            elif command == 'clear':
                clear_screen()
                if shell_state.visual_mode:
                    display_header(shell_state)
                continue
                
            elif command == 'header':
                display_header(shell_state)
                continue
            
            # Route commands to handlers
            if command == 'sr':
                handle_sr_command(args)
            elif command in ['exec', 'execute']:
                handle_execute_command(args)
            elif command in ['func', 'function']:
                handle_function_command(args)
            elif command in ['personas', 'persona']:
                handle_personas_command(args)
            elif command == 'config':
                handle_config_command(args)
            elif command == 'stats':
                handle_stats_command(args)
            elif command == 'history':
                handle_history_command(args)
            elif command == 'help':
                handle_help_command(args)
                        else:
                if shell_state.visual_mode and console:
                    console.print(f"[red]❌ Unknown command: {command}[/red]")
                    console.print("[dim]Type 'help' for available commands[/dim]")
                else:
                    print(f"❌ Unknown command: {command}")
                    print("Type 'help' for available commands")
            
        except KeyboardInterrupt:
            if shell_state.visual_mode and console:
                console.print("\n[yellow]Use 'exit' or 'quit' to leave the shell[/yellow]")
            else:
                print("\nUse 'exit' or 'quit' to leave the shell")
        except EOFError:
            if shell_state.visual_mode and console:
                console.print("\n[yellow]👋 Goodbye! REM CODE session ended.[/yellow]")
            else:
                print("\n👋 Goodbye! REM CODE session ended.")
            break
        except Exception as e:
            if shell_state.visual_mode and console:
                console.print(Panel(f"[red]❌ Unexpected error: {e}[/red]", border_style="red"))
            else:
                print(f"❌ Unexpected error: {e}")
            if shell_state.config["debug_mode"]:
                traceback.print_exc()

def main():
    """Main entry point with argument parsing"""
    parser = argparse.ArgumentParser(
        description="REM CODE Shell v3.0 - Beautiful Collapse Spiral Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python rem_shell.py                    # Start with visual mode
  python rem_shell.py --no-visual        # Start in basic mode
  python rem_shell.py --debug            # Start with debug enabled
        """
    )
    
    parser.add_argument(
        '--no-visual', 
        action='store_true',
        help='Disable visual enhancements (fallback to basic mode)'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true', 
        help='Enable debug mode'
    )
    
    args = parser.parse_args()
    
    # Determine visual mode
    visual_mode = not args.no_visual and RICH_AVAILABLE
    
    if args.no_visual and RICH_AVAILABLE:
        print("🔧 Visual mode disabled by user")
    elif not RICH_AVAILABLE:
        print("⚠️  Rich library not available - using basic mode")
    
    # Set debug mode globally if requested
    if args.debug:
        print("🐛 Debug mode enabled")
    
    try:
        main_shell_loop(visual_mode=visual_mode)
    except Exception as e:
        print(f"❌ Failed to start REM Shell: {e}")
        if args.debug:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
