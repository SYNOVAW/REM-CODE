# shell/rem_web_shell.py

import gradio as gr
import gradio.inputs as inputs
import gradio.outputs as outputs
from functions.functions import define_function, call_function, memory

def run_rem_code(name, code, sr, info_name):
    try:
        # Function execution
        exec_result = ""
        if name.strip() and code.strip():
            lines = code.strip().split("\n")
            define_msg = define_function(name, lines)
            result = call_function(name, sr_value=sr)
            exec_result = f"✅ {define_msg}\n\n"
            exec_result += f"🧠 Function Output (SR={sr:.2f}):\n"
            exec_result += "─" * 40 + "\n"
            exec_result += "\n".join(result)
            exec_result += "\n" + "─" * 40
        elif name.strip() or code.strip():
            exec_result = "❌ Error: Both function name and code are required for execution."
        # Function list
        try:
            functions = memory.get("functions", {})
            if functions:
                func_list = "📜 Defined Functions:\n"
                func_list += "─" * 30 + "\n"
                for fn_name in functions:
                    func_list += f"  • {fn_name}\n"
            else:
                func_list = "📜 No functions defined yet."
        except Exception as e:
            func_list = f"❌ Error listing functions: {str(e)}"
        # Function info
        try:
            if info_name.strip():
                functions = memory.get("functions", {})
                if info_name not in functions:
                    func_info = f"❌ Error: Function '{info_name}' not found"
                else:
                    func_info = f"📋 Function: {info_name}\n"
                    func_info += "─" * 30 + "\n"
                    func_info += f"Body lines: {len(functions[info_name]['body'])}\n"
                    func_info += "Code:\n"
                    for i, line in enumerate(functions[info_name]['body'], 1):
                        func_info += f"  {i:2d}: {line}\n"
            else:
                func_info = "(関数名を入力してください)"
        except Exception as e:
            func_info = f"❌ Error getting function info: {str(e)}"
        return exec_result, func_list, func_info
    except Exception as e:
        return f"❌ Error: {str(e)}", "", ""

iface = gr.Interface(
    fn=run_rem_code,
    inputs=[
        inputs.Textbox(label="Function Name", default="my_function"),
        inputs.Textbox(label="REM CODE（構文）", lines=12, default='Acta "起動"\n  Echo "Hello, REM World!"\n  Return "Success"'),
        inputs.Slider(0.0, 1.0, default=0.5, label="Synchrony Rate (SR)"),
        inputs.Textbox(label="Function Name for Info", default="")
    ],
    outputs=[
        outputs.Textbox(label="🌀 REM Output"),
        outputs.Textbox(label="Function List"),
        outputs.Textbox(label="Function Details")
    ],
    title="REM CODE Spiral Shell (All-in-One)",
    description="Define + Execute REM CODE, list and inspect functions in one screen."
)

def main():
    iface.launch(server_name="0.0.0.0", server_port=7860, share=False)

if __name__ == "__main__":
    main()
