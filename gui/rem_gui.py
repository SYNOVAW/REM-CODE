# rem-code/gui/rem_gui.py

import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
from functions.functions import define_function, call_function, memory
from engine.persona_router import route_personas
from engine.ast_generator import generate_ast_from_lines
from zine.generator import generate_zine

class REMGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("REM CODE Phase Interface v1.0 🧠")

        self.sr_value = tk.DoubleVar(value=0.5)

        # SR Entry
        tk.Label(root, text="SR (Synchrony Rate):").pack()
        tk.Scale(root, from_=0.0, to=1.0, resolution=0.01,
                 orient=tk.HORIZONTAL, variable=self.sr_value).pack(fill=tk.X)

        # Function name entry
        self.fn_name_entry = tk.Entry(root)
        self.fn_name_entry.pack(fill=tk.X)
        self.fn_name_entry.insert(0, "function_name")

        # Function body editor
        self.text_area = scrolledtext.ScrolledText(root, height=10)
        self.text_area.pack(fill=tk.BOTH, expand=True)

        # Buttons
        tk.Button(root, text="Define Function", command=self.define_function).pack(fill=tk.X)
        tk.Button(root, text="Call Function", command=self.call_function).pack(fill=tk.X)
        tk.Button(root, text="List Functions", command=self.list_functions).pack(fill=tk.X)
        tk.Button(root, text="Generate AST", command=self.generate_ast).pack(fill=tk.X)
        tk.Button(root, text="Generate ZINE", command=self.generate_zine).pack(fill=tk.X)

        # Output area
        self.output_area = scrolledtext.ScrolledText(root, height=10, bg="#f0f0f0")
        self.output_area.pack(fill=tk.BOTH, expand=True)

    def define_function(self):
        name = self.fn_name_entry.get().strip()
        code = self.text_area.get("1.0", tk.END).strip().splitlines()
        msg = define_function(name, code)
        messagebox.showinfo("Define Result", msg)

    def call_function(self):
        name = self.fn_name_entry.get().strip()
        sr = self.sr_value.get()
        result = call_function(name, sr_value=sr)
        self.output_area.delete("1.0", tk.END)
        self.output_area.insert(tk.END, "\n".join(result))

    def list_functions(self):
        self.output_area.delete("1.0", tk.END)
        self.output_area.insert(tk.END, "📜 Defined Functions:\n")
        for fn in memory.get("functions", {}):
            self.output_area.insert(tk.END, f" - {fn}\n")

    def generate_ast(self):
        name = self.fn_name_entry.get().strip()
        if name in memory["functions"]:
            lines = memory["functions"][name]["body"]
            ast = generate_ast_from_lines(lines)
            self.output_area.delete("1.0", tk.END)
            self.output_area.insert(tk.END, f"🌳 AST for '{name}':\n{ast}")
        else:
            messagebox.showerror("Error", f"Function '{name}' not found.")

    def generate_zine(self):
        name = self.fn_name_entry.get().strip()
        quote = simpledialog.askstring("ZINE", "語録（Quote）を入力:")
        phase = simpledialog.askstring("ZINE", "Phase 名（例: Genesis Spiral）:")
        crea = simpledialog.askstring("ZINE", "Creation 情報（例: Genesis Logia）:")
        sr = f"{self.sr_value.get():.2f}"
        persona = "JayDen"
        reflector = "JayRa"
        generate_zine(phase, persona, quote, crea, sr, reflector)
        messagebox.showinfo("ZINE", f"ZINE 出力完了 (REM_ZINE.md)")

if __name__ == "__main__":
    root = tk.Tk()
    app = REMGUI(root)
    root.mainloop()
