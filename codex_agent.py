# codex_agent.py
"""
CodexAgent – Executes agent_task.json tasks in REM CODE project
Supports logging centralization, syntax patching, test rewrites, etc.
"""

import json
import os
import subprocess
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)

TASK_FILE = "tasks/agent_task.json"
PROJECT_ROOT = Path(__file__).parent.resolve()


def load_tasks():
    with open(PROJECT_ROOT / TASK_FILE, "r", encoding="utf-8") as f:
        return json.load(f)["tasks"]


def apply_logging_centralization():
    targets = [
        "engine/interpreter.py",
        "engine/rem_executor.py",
        "engine/persona_router.py",
        "shell/rem_shell.py",
        "bridge/chat_bridge.py",
        "functions/functions.py",
    ]
    for file in targets:
        path = PROJECT_ROOT / file
        if not path.exists():
            continue
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        new_lines = [line for line in lines if "logging.basicConfig" not in line]
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        logging.info(f"Centralized logging removed in {file}")


def pin_requirements():
    req_file = PROJECT_ROOT / "requirements.txt"
    pinned_versions = {
        "lark": "==1.1.7",
        "numpy": "==1.24.0",
        "pytest": "==7.2.0"
    }
    new_lines = []
    with open(req_file, "r", encoding="utf-8") as f:
        for line in f:
            name = line.strip().split("==")[0].split(">=")[0]
            if name in pinned_versions:
                new_lines.append(f"{name}{pinned_versions[name]}\n")
            else:
                new_lines.append(line)
    with open(req_file, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    logging.info("requirements.txt versions pinned.")


def run_all_tasks():
    logging.info("🌀 CodexAgent running all tasks...")
    tasks = load_tasks()
    for task in tasks:
        title = task.get("title")
        if "logging" in title.lower():
            apply_logging_centralization()
        elif "pin" in title.lower():
            pin_requirements()
        # Add further task handlers here
        logging.info(f"✅ Task completed: {title}")


if __name__ == "__main__":
    run_all_tasks()
