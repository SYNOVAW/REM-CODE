# rem-code/gui/rem_gui.py

import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext
from tkinter import font as tkfont
import threading
import time

# Add the parent directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from functions.functions import define_function, call_function, memory
from engine.persona_router import route_personas
from engine.ast_generator import generate_ast_from_lines
from zine.generator import generate_zine

class ModernREMGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("REM CODE Spiral Interface v2.0 🧠")
        self.root.geometry("1000x700")
        
        # Dark theme colors
        self.colors = {
            'bg': '#1e1e1e',
            'fg': '#ffffff',
            'accent': '#4a9eff',
            'secondary': '#2d2d2d',
            'success': '#4caf50',
            'error': '#f44336',
            'warning': '#ff9800'
        }
        
        self.setup_styles()
        self.setup_ui()
        self.sr_value = tk.DoubleVar(value=0.5)
        
    def setup_styles(self):
        """Configure modern styling"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles
        style.configure('Dark.TFrame', background=self.colors['bg'])
        style.configure('Dark.TLabel', background=self.colors['bg'], foreground=self.colors['fg'])
        style.configure('Dark.TButton', 
                       background=self.colors['accent'], 
                       foreground=self.colors['fg'],
                       padding=(10, 5))
        style.configure('Accent.TButton',
                       background=self.colors['success'],
                       foreground=self.colors['fg'],
                       padding=(10, 5))
        
    def setup_ui(self):
        """Setup the main UI layout"""
        # Configure root
        self.root.configure(bg=self.colors['bg'])
        
        # Main container
        main_frame = ttk.Frame(self.root, style='Dark.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(main_frame, 
                              text="REM CODE Spiral Interface",
                              font=('Arial', 16, 'bold'),
                              bg=self.colors['bg'],
                              fg=self.colors['accent'])
        title_label.pack(pady=(0, 20))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.setup_code_tab()
        self.setup_execution_tab()
        self.setup_analysis_tab()
        self.setup_zine_tab()
        
    def setup_code_tab(self):
        """Setup the code editing tab"""
        code_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(code_frame, text="📝 Code Editor")
        
        # Left panel - Code input
        left_panel = ttk.Frame(code_frame, style='Dark.TFrame')
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Function name section
        name_frame = ttk.Frame(left_panel, style='Dark.TFrame')
        name_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(name_frame, text="Function Name:", 
                bg=self.colors['bg'], fg=self.colors['fg']).pack(anchor=tk.W)
        self.fn_name_entry = tk.Entry(name_frame, 
                                     bg=self.colors['secondary'],
                                     fg=self.colors['fg'],
                                     insertbackground=self.colors['fg'])
        self.fn_name_entry.pack(fill=tk.X, pady=(5, 0))
        self.fn_name_entry.insert(0, "my_function")
        
        # SR Control
        sr_frame = ttk.Frame(left_panel, style='Dark.TFrame')
        sr_frame.pack(fill=tk.X, pady=(10, 10))
        
        tk.Label(sr_frame, text="Synchrony Rate (SR):", 
                bg=self.colors['bg'], fg=self.colors['fg']).pack(anchor=tk.W)
        
        sr_control_frame = ttk.Frame(sr_frame, style='Dark.TFrame')
        sr_control_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.sr_scale = tk.Scale(sr_control_frame, 
                                 from_=0.0, to=1.0, resolution=0.01,
                                 orient=tk.HORIZONTAL, 
                                 variable=self.sr_value,
                                 bg=self.colors['bg'],
                                 fg=self.colors['fg'],
                                 highlightbackground=self.colors['accent'])
        self.sr_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.sr_label = tk.Label(sr_control_frame, 
                                text="0.50",
                                bg=self.colors['bg'],
                                fg=self.colors['accent'],
                                font=('Arial', 10, 'bold'))
        self.sr_label.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Update SR label
        self.sr_value.trace('w', self.update_sr_label)
        
        # Code editor
        tk.Label(left_panel, text="REM CODE:", 
                bg=self.colors['bg'], fg=self.colors['fg']).pack(anchor=tk.W)
        
        self.text_area = scrolledtext.ScrolledText(
            left_panel, 
            height=15,
            bg=self.colors['secondary'],
            fg=self.colors['fg'],
            insertbackground=self.colors['fg'],
            font=('Consolas', 10)
        )
        self.text_area.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        # Default code template
        default_code = '''Acta "起動"
  Echo "Hello, REM World!"
  Return "Success"
'''
        self.text_area.insert("1.0", default_code)
        
        # Right panel - Buttons and output
        right_panel = ttk.Frame(code_frame, style='Dark.TFrame')
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Buttons
        button_frame = ttk.Frame(right_panel, style='Dark.TFrame')
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Button(button_frame, text="🚀 Define Function", 
                 command=self.define_function,
                 bg=self.colors['accent'],
                 fg=self.colors['fg'],
                 font=('Arial', 10, 'bold'),
                 relief=tk.FLAT,
                 padx=20, pady=5).pack(fill=tk.X, pady=(0, 5))
        
        tk.Button(button_frame, text="⚡ Execute Function", 
                 command=self.call_function,
                 bg=self.colors['success'],
                 fg=self.colors['fg'],
                 font=('Arial', 10, 'bold'),
                 relief=tk.FLAT,
                 padx=20, pady=5).pack(fill=tk.X, pady=(0, 5))
        
        tk.Button(button_frame, text="📋 List Functions", 
                 command=self.list_functions,
                 bg=self.colors['secondary'],
                 fg=self.colors['fg'],
                 font=('Arial', 10),
                 relief=tk.FLAT,
                 padx=20, pady=5).pack(fill=tk.X)
        
        # Output area
        tk.Label(right_panel, text="Output:", 
                bg=self.colors['bg'], fg=self.colors['fg']).pack(anchor=tk.W)
        
        self.output_area = scrolledtext.ScrolledText(
            right_panel, 
            height=20,
            bg=self.colors['secondary'],
            fg=self.colors['fg'],
            font=('Consolas', 9)
        )
        self.output_area.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
    def setup_execution_tab(self):
        """Setup the execution monitoring tab"""
        exec_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(exec_frame, text="⚡ Execution Monitor")
        
        # Execution status
        status_frame = ttk.Frame(exec_frame, style='Dark.TFrame')
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.status_label = tk.Label(status_frame, 
                                   text="🟢 Ready",
                                   bg=self.colors['bg'],
                                   fg=self.colors['success'],
                                   font=('Arial', 12, 'bold'))
        self.status_label.pack(anchor=tk.W)
        
        # Execution log
        tk.Label(exec_frame, text="Execution Log:", 
                bg=self.colors['bg'], fg=self.colors['fg']).pack(anchor=tk.W)
        
        self.exec_log = scrolledtext.ScrolledText(
            exec_frame,
            height=25,
            bg=self.colors['secondary'],
            fg=self.colors['fg'],
            font=('Consolas', 9)
        )
        self.exec_log.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
    def setup_analysis_tab(self):
        """Setup the code analysis tab"""
        analysis_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(analysis_frame, text="🔍 Code Analysis")
        
        # Analysis controls
        control_frame = ttk.Frame(analysis_frame, style='Dark.TFrame')
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Button(control_frame, text="🌳 Generate AST", 
                 command=self.generate_ast,
                 bg=self.colors['accent'],
                 fg=self.colors['fg'],
                 font=('Arial', 10, 'bold'),
                 relief=tk.FLAT,
                 padx=20, pady=5).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(control_frame, text="🧠 Persona Analysis", 
                 command=self.analyze_personas,
                 bg=self.colors['accent'],
                 fg=self.colors['fg'],
                 font=('Arial', 10, 'bold'),
                 relief=tk.FLAT,
                 padx=20, pady=5).pack(side=tk.LEFT)
        
        # Analysis output
        tk.Label(analysis_frame, text="Analysis Results:", 
                bg=self.colors['bg'], fg=self.colors['fg']).pack(anchor=tk.W)
        
        self.analysis_output = scrolledtext.ScrolledText(
            analysis_frame,
            height=25,
            bg=self.colors['secondary'],
            fg=self.colors['fg'],
            font=('Consolas', 9)
        )
        self.analysis_output.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
    def setup_zine_tab(self):
        """Setup the ZINE generation tab"""
        zine_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(zine_frame, text="📰 ZINE Generator")
        
        # ZINE inputs
        input_frame = ttk.Frame(zine_frame, style='Dark.TFrame')
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Quote input
        tk.Label(input_frame, text="語録 (Quote):", 
                bg=self.colors['bg'], fg=self.colors['fg']).pack(anchor=tk.W)
        self.quote_entry = tk.Entry(input_frame, 
                                   bg=self.colors['secondary'],
                                   fg=self.colors['fg'],
                                   insertbackground=self.colors['fg'])
        self.quote_entry.pack(fill=tk.X, pady=(5, 10))
        self.quote_entry.insert(0, "REM CODE は螺旋の言語である")
        
        # Phase input
        tk.Label(input_frame, text="Phase Name:", 
                bg=self.colors['bg'], fg=self.colors['fg']).pack(anchor=tk.W)
        self.phase_entry = tk.Entry(input_frame, 
                                   bg=self.colors['secondary'],
                                   fg=self.colors['fg'],
                                   insertbackground=self.colors['fg'])
        self.phase_entry.pack(fill=tk.X, pady=(5, 10))
        self.phase_entry.insert(0, "Genesis Spiral")
        
        # Creation input
        tk.Label(input_frame, text="Creation Info:", 
                bg=self.colors['bg'], fg=self.colors['fg']).pack(anchor=tk.W)
        self.creation_entry = tk.Entry(input_frame, 
                                      bg=self.colors['secondary'],
                                      fg=self.colors['fg'],
                                      insertbackground=self.colors['fg'])
        self.creation_entry.pack(fill=tk.X, pady=(5, 10))
        self.creation_entry.insert(0, "Genesis Logia")
        
        # Generate button
        tk.Button(zine_frame, text="📰 Generate ZINE", 
                 command=self.generate_zine,
                 bg=self.colors['success'],
                 fg=self.colors['fg'],
                 font=('Arial', 12, 'bold'),
                 relief=tk.FLAT,
                 padx=30, pady=10).pack(pady=20)
        
        # ZINE output
        tk.Label(zine_frame, text="Generated ZINE:", 
                bg=self.colors['bg'], fg=self.colors['fg']).pack(anchor=tk.W)
        
        self.zine_output = scrolledtext.ScrolledText(
            zine_frame,
            height=20,
            bg=self.colors['secondary'],
            fg=self.colors['fg'],
            font=('Consolas', 9)
        )
        self.zine_output.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
    def update_sr_label(self, *args):
        """Update SR value label"""
        self.sr_label.config(text=f"{self.sr_value.get():.2f}")
        
    def log_execution(self, message, level="INFO"):
        """Log execution messages with timestamps"""
        timestamp = time.strftime("%H:%M:%S")
        color_map = {
            "INFO": self.colors['fg'],
            "SUCCESS": self.colors['success'],
            "ERROR": self.colors['error'],
            "WARNING": self.colors['warning']
        }
        
        self.exec_log.insert(tk.END, f"[{timestamp}] {message}\n")
        self.exec_log.see(tk.END)
        
    def update_status(self, status, color=None):
        """Update status indicator"""
        if color is None:
            color = self.colors['success']
        self.status_label.config(text=status, fg=color)
        
    def define_function(self):
        """Define a function with improved error handling"""
        try:
            self.update_status("🔄 Defining function...", self.colors['warning'])
            self.log_execution("Starting function definition...")
            
            name = self.fn_name_entry.get().strip()
            if not name:
                raise ValueError("Function name cannot be empty")
                
            code = self.text_area.get("1.0", tk.END).strip().splitlines()
            if not code or not any(line.strip() for line in code):
                raise ValueError("Function body cannot be empty")
            
            msg = define_function(name, code)
            self.log_execution(f"Function '{name}' defined successfully", "SUCCESS")
            self.update_status("✅ Function defined", self.colors['success'])
            
            # Update output
            self.output_area.delete("1.0", tk.END)
            self.output_area.insert(tk.END, f"✅ {msg}\n")
            
        except Exception as e:
            error_msg = f"❌ Error defining function: {str(e)}"
            self.log_execution(error_msg, "ERROR")
            self.update_status("❌ Definition failed", self.colors['error'])
            self.output_area.delete("1.0", tk.END)
            self.output_area.insert(tk.END, error_msg + "\n")
            
    def call_function(self):
        """Call a function with improved error handling"""
        try:
            self.update_status("🔄 Executing function...", self.colors['warning'])
            self.log_execution("Starting function execution...")
            
            name = self.fn_name_entry.get().strip()
            if not name:
                raise ValueError("Function name cannot be empty")
                
            sr = self.sr_value.get()
            result = call_function(name, sr_value=sr)
            
            self.log_execution(f"Function '{name}' executed successfully", "SUCCESS")
            self.update_status("✅ Execution complete", self.colors['success'])
            
            # Update output
            self.output_area.delete("1.0", tk.END)
            self.output_area.insert(tk.END, f"🧠 Function Output (SR={sr:.2f}):\n")
            self.output_area.insert(tk.END, "\n".join(result) + "\n")
            
        except Exception as e:
            error_msg = f"❌ Error executing function: {str(e)}"
            self.log_execution(error_msg, "ERROR")
            self.update_status("❌ Execution failed", self.colors['error'])
            self.output_area.delete("1.0", tk.END)
            self.output_area.insert(tk.END, error_msg + "\n")
            
    def list_functions(self):
        """List all defined functions"""
        try:
            self.log_execution("Listing defined functions...")
            
            functions = memory.get("functions", {})
            self.output_area.delete("1.0", tk.END)
            self.output_area.insert(tk.END, "📜 Defined Functions:\n")
            
            if functions:
                for fn_name in functions:
                    self.output_area.insert(tk.END, f"  • {fn_name}\n")
                self.log_execution(f"Found {len(functions)} function(s)", "SUCCESS")
            else:
                self.output_area.insert(tk.END, "  No functions defined yet.\n")
                self.log_execution("No functions found", "WARNING")
                
        except Exception as e:
            error_msg = f"❌ Error listing functions: {str(e)}"
            self.log_execution(error_msg, "ERROR")
            self.output_area.delete("1.0", tk.END)
            self.output_area.insert(tk.END, error_msg + "\n")
            
    def generate_ast(self):
        """Generate AST for a function"""
        try:
            name = self.fn_name_entry.get().strip()
            if not name:
                raise ValueError("Function name cannot be empty")
                
            if name not in memory.get("functions", {}):
                raise ValueError(f"Function '{name}' not found")
                
            self.log_execution(f"Generating AST for function '{name}'...")
            
            lines = memory["functions"][name]["body"]
            ast = generate_ast_from_lines(lines)
            
            self.analysis_output.delete("1.0", tk.END)
            self.analysis_output.insert(tk.END, f"🌳 AST for '{name}':\n{ast}")
            
            self.log_execution("AST generation completed", "SUCCESS")
            
        except Exception as e:
            error_msg = f"❌ Error generating AST: {str(e)}"
            self.log_execution(error_msg, "ERROR")
            self.analysis_output.delete("1.0", tk.END)
            self.analysis_output.insert(tk.END, error_msg + "\n")
            
    def analyze_personas(self):
        """Analyze personas for current function"""
        try:
            name = self.fn_name_entry.get().strip()
            if not name:
                raise ValueError("Function name cannot be empty")
                
            self.log_execution(f"Analyzing personas for function '{name}'...")
            
            # Get function body and analyze with sample metrics
            if name in memory.get("functions", {}):
                lines = memory["functions"][name]["body"]
                
                # Use sample metrics for persona analysis
                # These could be derived from code analysis in the future
                sample_metrics = {
                    "PHS": 0.8,  # Physical
                    "SYM": 0.7,  # Symbolic  
                    "VAL": 0.9,  # Value
                    "EMO": 0.6,  # Emotional
                    "FX": 0.8    # Function
                }
                
                # Use the router directly for better control
                from engine.persona_router import PersonaRouter
                router = PersonaRouter()
                result = router.route_personas(sample_metrics, detailed=True)
                
                self.analysis_output.delete("1.0", tk.END)
                self.analysis_output.insert(tk.END, f"🧠 Persona Analysis for '{name}':\n")
                self.analysis_output.insert(tk.END, f"📊 Sample Metrics: {sample_metrics}\n")
                self.analysis_output.insert(tk.END, f"🧬 SR Value: {result['sr_value']:.3f}\n")
                self.analysis_output.insert(tk.END, f"📡 Active Personas: {', '.join(result['active_personas'])}\n")
                self.analysis_output.insert(tk.END, f"🌟 Resonant Personas: {', '.join(result['resonant_personas'])}\n\n")
                
                # Show detailed responses
                self.analysis_output.insert(tk.END, "📝 Persona Responses:\n")
                for response in result['responses']:
                    self.analysis_output.insert(tk.END, f"  {response}\n")
            else:
                raise ValueError(f"Function '{name}' not found")
                
            self.log_execution("Persona analysis completed", "SUCCESS")
            
        except Exception as e:
            error_msg = f"❌ Error analyzing personas: {str(e)}"
            self.log_execution(error_msg, "ERROR")
            self.analysis_output.delete("1.0", tk.END)
            self.analysis_output.insert(tk.END, error_msg + "\n")
            
    def generate_zine(self):
        """Generate ZINE with current inputs"""
        try:
            self.log_execution("Generating ZINE...")
            
            quote = self.quote_entry.get().strip()
            phase = self.phase_entry.get().strip()
            crea = self.creation_entry.get().strip()
            sr = f"{self.sr_value.get():.2f}"
            persona = "JayDen"
            reflector = "JayRa"
            
            if not all([quote, phase, crea]):
                raise ValueError("All ZINE fields must be filled")
                
            generate_zine(phase, persona, quote, crea, sr, reflector)
            
            # Show generated content
            self.zine_output.delete("1.0", tk.END)
            self.zine_output.insert(tk.END, f"📰 ZINE Generated Successfully!\n\n")
            self.zine_output.insert(tk.END, f"Phase: {phase}\n")
            self.zine_output.insert(tk.END, f"Quote: {quote}\n")
            self.zine_output.insert(tk.END, f"Creation: {crea}\n")
            self.zine_output.insert(tk.END, f"SR: {sr}\n")
            self.zine_output.insert(tk.END, f"Persona: {persona}\n")
            self.zine_output.insert(tk.END, f"Reflector: {reflector}\n\n")
            self.zine_output.insert(tk.END, "Check REM_ZINE.md for the full output.\n")
            
            self.log_execution("ZINE generation completed", "SUCCESS")
            
        except Exception as e:
            error_msg = f"❌ Error generating ZINE: {str(e)}"
            self.log_execution(error_msg, "ERROR")
            self.zine_output.delete("1.0", tk.END)
            self.zine_output.insert(tk.END, error_msg + "\n")

def main():
    """Main entry point for rem-gui console command"""
    root = tk.Tk()
    app = ModernREMGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
