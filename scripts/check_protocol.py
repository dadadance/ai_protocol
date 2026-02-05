#!/usr/bin/env python3
"""
Check protocol version drift between ai-protocol and a target project.

Usage:
    uv run scripts/check_protocol.py [target_directory]

If target_directory is omitted, uses current working directory.
Reads ai-protocol VERSION and target's docs/context_registry.json (_meta.protocol_version).
Reports OK or drift; does not modify any files.
"""

import json
import sys
from pathlib import Path


def get_script_root() -> Path:
    return Path(__file__).resolve().parent.parent


def read_protocol_version(ai_protocol_root: Path) -> str | None:
    version_file = ai_protocol_root / "VERSION"
    if not version_file.exists():
        return None
    return version_file.read_text().strip() or None


def read_target_version(target_root: Path) -> str | None:
    registry_path = target_root / "docs" / "context_registry.json"
    if not registry_path.exists():
        return None
    try:
        with open(registry_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError):
        return None
    meta = data.get("_meta") or {}
    return meta.get("protocol_version") or None


def main() -> None:
    target_root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    ai_root = get_script_root()

    if not target_root.exists() or not target_root.is_dir():
        print(f"Error: Target directory does not exist or is not a directory: {target_root}")
        sys.exit(1)

    protocol_ver = read_protocol_version(ai_root)
    target_ver = read_target_version(target_root)

    if protocol_ver is None:
        print("Warning: ai-protocol VERSION file not found; cannot compare.")
        sys.exit(0)

    if target_ver is None:
        print(
            "Target has no protocol version (missing docs/context_registry.json or _meta.protocol_version)."
        )
        print("Run bootstrap to inject the protocol, or add _meta.protocol_version to the registry.")
        sys.exit(0)

    if protocol_ver == target_ver:
        print(f"OK: Protocol version match ({protocol_ver}).")
        sys.exit(0)

    print(f"Drift: ai-protocol is {protocol_ver}, target reports {target_ver}.")
    print(
        "To refresh the target, run: uv run scripts/bootstrap.py <target_dir> --force"
        " (review changes; --force overwrites existing files)."
    )
    sys.exit(1)


if __name__ == "__main__":
    main()
