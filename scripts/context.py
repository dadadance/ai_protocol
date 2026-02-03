#!/usr/bin/env python3
import sys, json, os

REGISTRY_PATH = "docs/context_registry.json"

def load_registry():
    with open(REGISTRY_PATH, "r") as f: return json.load(f)

def extract_section(file_path, header_title):
    if not os.path.exists(file_path): return "Error: File not found."
    with open(file_path, "r", encoding="utf-8") as f: lines = f.readlines()
    capturing, captured_lines, target_level = False, [], 0
    in_code_block = False
    search_title = header_title.lower().strip()
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block

        if not in_code_block and stripped.startswith("#"):
            parts = stripped.split(" ", 1)
            if len(parts) >= 2:
                level, title = len(parts[0]), parts[1].strip().lower()
                if not capturing and search_title in title:
                    capturing, target_level = True, level
                    captured_lines.append(line)
                    continue
                if capturing and level <= target_level: break
        if capturing: captured_lines.append(line)
    return "".join(captured_lines).strip() if captured_lines else "Section not found."

def fetch_context(key):
    reg = load_registry()
    if key not in reg: print("Key not found."); sys.exit(1)

    entries = reg[key]
    if isinstance(entries, dict): entries = [entries]
    elif isinstance(entries, str): entries = [entries]

    print("--- Context: " + key + " ---")
    for entry in entries:
        file_path, section = None, None
        if isinstance(entry, str): file_path = entry
        elif isinstance(entry, dict): file_path, section = entry.get("file"), entry.get("section")

        if not file_path: continue
        
        if section: print(extract_section(file_path, section))
        else:
            try:
                with open(file_path, "r", encoding="utf-8") as f: print(f.read())
            except Exception as e: print(f"Error reading {file_path}: {e}")
    print("\n--- End of Context ---")

if __name__ == "__main__":
    if len(sys.argv) < 2: sys.exit(1)
    if sys.argv[1] == "list":
        reg = load_registry()
        for k in reg: print(k)
    elif sys.argv[1] == "fetch": fetch_context(sys.argv[2])
