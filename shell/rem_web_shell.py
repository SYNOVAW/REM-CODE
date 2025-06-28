# shell/rem_web_shell.py

import gradio as gr
from functions.functions import define_function, call_function

def run_rem_code(name, code, sr):
    try:
        lines = code.strip().split("\n")
        print(">>> Code Lines:", lines)  # 🔍 ここで行分割チェック
        define_msg = define_function(name, lines)
        result = call_function(name, sr_value=sr)
        print(">>> Result:", result)     # 🔍 実行結果を出力
        return f"{define_msg}\n🧠 Function Output:\n" + "\n".join(result)
    except Exception as e:
        return f"❌ Error: {str(e)}"

iface = gr.Interface(
    fn=run_rem_code,
    inputs=[
        gr.Textbox(label="Function Name", placeholder="enter name..."),
        gr.Textbox(lines=8, label="REM CODE（構文）", placeholder='Acta "起動"\n...'),
        gr.Slider(0.0, 1.0, step=0.01, label="Synchrony Rate (SR)")
    ],
    outputs=gr.Textbox(label="🌀 REM Output", lines=10),
    title="REM CODE Spiral Shell",
    description="Define + Execute REM CODE in web terminal form"
)

if __name__ == "__main__":
    iface.launch(share=False)
