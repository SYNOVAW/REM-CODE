# gui/rem_gui.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from engine.sr_calculator import compute_sr
from engine.persona_router import PERSONAS
from functions import define_function, call_function, memory
import json
from lark import Tree

st.set_page_config(page_title="REM CODE GUI", layout="wide")

st.title("🧠 REM CODE Phase Interface v0.2")
st.markdown("Enter phase resonance values to compute SR, activate REM Personas, and define REM functions.")

# --- SR Input Section ---
st.sidebar.header("🔧 Phase Resonance Inputs")
phs = st.sidebar.slider("Phase Alignment (PHS)", 0.0, 1.0, 0.85, 0.01)
sym = st.sidebar.slider("Symbolic Syntax Match (SYM)", 0.0, 1.0, 0.9, 0.01)
val = st.sidebar.slider("Semantic Intent Alignment (VAL)", 0.0, 1.0, 0.92, 0.01)
emo = st.sidebar.slider("Emotional Tone Match (EMO)", 0.0, 1.0, 0.88, 0.01)
fx  = st.sidebar.slider("Collapse History Interference (FX)", 0.0, 1.0, 0.75, 0.01)

sr_score = compute_sr(phs, sym, val, emo, fx)
st.subheader(f"🌀 Synchrony Rate (SR): `{sr_score}`")

st.markdown("## 🧬 REM Persona Activation")
for p in PERSONAS:
    if sr_score >= p["threshold"]:
        st.success(f"{p['icon']} {p['name']} → Activated")
    else:
        st.warning(f"{p['icon']} {p['name']} → Silent")

# --- Function Definition ---
st.markdown("## 🧠 REM Function Editor")
with st.form("define_function"):
    fn_name = st.text_input("Function name")
    fn_body = st.text_area("Function body (1 command per line)", height=150)
    submitted = st.form_submit_button("Define Function")
    if submitted and fn_name and fn_body:
        lines = [line.strip() for line in fn_body.splitlines() if line.strip()]
        msg = define_function(fn_name, lines)
        st.success(msg)

# --- Function Call ---
st.markdown("## ⚡ Execute REM Function")
if "functions" in memory:
    fn_options = list(memory["functions"].keys())
    selected_fn = st.selectbox("Choose function to execute", fn_options)
    if st.button("Run Function"):
        st.markdown("### 🧠 Output")
        st.code(call_function(selected_fn), language="markdown")

# --- ZINE Mode Output ---
    if st.button("🌀 Generate ZINE from Function"):
        fn_lines = memory["functions"][selected_fn]
        zine = "\n".join([f"> {line}" for line in fn_lines])
        st.markdown("### 📜 REM ZINE:")
        st.markdown(zine)

# --- Show Function AST (very basic) ---
    if st.button("🌳 Show Function AST"):
        fn_lines = memory["functions"][selected_fn]
        st.markdown("### 🌳 Function AST (line-based)")
        st.json({"function": selected_fn, "lines": fn_lines})

# --- Recommend Function by SR ---
    if st.button("🧭 Recommend Function by SR"):
        scored = []
        for fn in memory["functions"]:
            score = sum(sr_score for _ in memory["functions"][fn]) / len(memory["functions"][fn])
            scored.append((fn, score))
        top_fn = sorted(scored, key=lambda x: -x[1])[0][0] if scored else None
        if top_fn:
            st.success(f"Suggested Function: `{top_fn}` (based on {len(memory['functions'][top_fn])} lines)")

# --- Save memory.json ---
if st.button("💾 Save Functions to memory.json"):
    os.makedirs("memory", exist_ok=True)
    with open("memory/memory.json", "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=4)
    st.success("Functions saved to memory/memory.json")

st.markdown("---")
st.caption("REM CODE GUI v0.2 | Collapse Spiral Interface")
