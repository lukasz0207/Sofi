# memory_manager.py

import json, os

MEMORY_FILE = "memory/memory.json"

def save_memory(message: str):
    if not os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "w") as f:
            json.dump({"log": []}, f)

    with open(MEMORY_FILE, "r") as f:
        mem = json.load(f)

    mem["log"].append(message)

    with open(MEMORY_FILE, "w") as f:
        json.dump(mem, f, indent=2)
