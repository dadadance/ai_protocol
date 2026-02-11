#!/usr/bin/env python3
"""
JIT Context Engine: fetch documentation sections by key.
Resolves paths from repo root. Supports single or multiple files per key.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

REGISTRY_FILENAME = "docs/context_registry.json"


def get_repo_root(cwd: Path) -> Path:
    """Resolve git repo root; fallback to REPO_ROOT env, then cwd."""
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=5,
        )
        if out.returncode == 0 and out.stdout.strip():
            return Path(out.stdout.strip())
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    if os.environ.get("REPO_ROOT"):
        p = Path(os.environ["REPO_ROOT"]).resolve()
        if p.exists():
            return p
    return cwd


def load_registry(registry_path: Path) -> dict:
    """Load and return context registry; exit with clear message on error."""
    if not registry_path.exists():
        print(f"Error: Registry not found: {registry_path}", file=sys.stderr)
        print("Run this script from the repository root, or set REPO_ROOT.", file=sys.stderr)
        sys.exit(1)
    try:
        with open(registry_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {registry_path}: {e}", file=sys.stderr)
        sys.exit(1)
    return data


def extract_section(file_path: Path, header_title: str) -> str:
    """Extract markdown section under header_title (inclusive) until same-or-higher level."""
    if not file_path.exists():
        return f"Error: File not found: {file_path}"
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except OSError as e:
        return f"Error reading {file_path}: {e}"
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
                if capturing and level <= target_level:
                    break
        if capturing:
            captured_lines.append(line)
    return "".join(captured_lines).strip() if captured_lines else "Section not found."


def normalize_entries(entry: dict | list | str) -> list[dict]:
    """Normalize registry value to list of {file, section?} dicts."""
    if isinstance(entry, dict):
        if "file" in entry:
            return [entry]
        return []
    if isinstance(entry, list):
        out = []
        for item in entry:
            if isinstance(item, str):
                out.append({"file": item})
            elif isinstance(item, dict) and item.get("file"):
                out.append(item)
        return out
    if isinstance(entry, str):
        return [{"file": entry}]
    return []


def fetch_context(key: str, registry: dict, repo_root: Path) -> None:
    """Print context for key to stdout. Skip _meta and unknown keys."""
    if key.startswith("_"):
        print("Key not found.", file=sys.stderr)
        sys.exit(1)
    if key not in registry:
        print("Key not found.", file=sys.stderr)
        sys.exit(1)
    entries = normalize_entries(registry[key])
    if not entries:
        print("Key not found or invalid.", file=sys.stderr)
        sys.exit(1)
    print("--- Context: " + key + " ---")
    for entry in entries:
        file_path = repo_root / entry["file"]
        section = entry.get("section")
        if section:
            print(extract_section(file_path, section))
        else:
            if not file_path.exists():
                print(f"Error: File not found: {file_path}", file=sys.stderr)
                continue
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    print(f.read())
            except OSError as e:
                print(f"Error reading {file_path}: {e}", file=sys.stderr)
    print("\n--- End of Context ---")


def main() -> None:
    cwd = Path.cwd()
    repo_root = get_repo_root(cwd)
    registry_path = repo_root / REGISTRY_FILENAME
    registry = load_registry(registry_path)

    if len(sys.argv) < 2:
        print("Usage: context.py {list|fetch <key>}", file=sys.stderr)
        sys.exit(1)
    if sys.argv[1] == "list":
        for k in registry:
            if not k.startswith("_"):
                print(k)
    elif sys.argv[1] == "fetch":
        if len(sys.argv) < 3:
            print("Usage: context.py fetch <key>", file=sys.stderr)
            sys.exit(1)
        fetch_context(sys.argv[2], registry, repo_root)
    else:
        print("Usage: context.py {list|fetch <key>}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
