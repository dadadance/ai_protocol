#!/usr/bin/env python3
"""
AI Protocol Bootstrapper

Usage:
    uv run scripts/bootstrap.py <target_directory> [--agent <name>] [--force]

Description:
    Injects the AI Protocol from the 'templates/' directory into an existing project.
    Safe by default: will not overwrite existing files unless --force is used.
"""

import argparse
import shutil
import sys
import os
from pathlib import Path

def setup_args():
    parser = argparse.ArgumentParser(description="Inject AI Protocol into a project.")
    parser.add_argument("target_dir", help="Target project directory")
    parser.add_argument("--agent", default="GEMINI", help="Name of the agent file (default: GEMINI)")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    parser.add_argument(
        "--monorepo-submodule",
        action="store_true",
        help="Inject thin agent file from AGENT_SUBMODULE.md (for submodules delegating to root)",
    )
    parser.add_argument(
        "--module-name",
        help="Module name to substitute in AGENT_SUBMODULE.md (replaces {{MODULE_NAME}})",
    )
    parser.add_argument(
        "--description",
        help="One-line description to substitute in AGENT_SUBMODULE.md (replaces {{ONE_LINE_DESCRIPTION}})",
    )
    return parser.parse_args()

def resolve_roots():
    """Resolve the source (templates) and target directories."""
    # This script is in ai_protocol/scripts/bootstrap.py
    # So templates is in ai_protocol/templates/
    script_path = Path(__file__).resolve()
    repo_root = script_path.parent.parent
    templates_root = repo_root / "templates"
    return templates_root

def main():
    args = setup_args()
    templates_root = resolve_roots()
    target_root = Path(args.target_dir).resolve()
    agent_name = args.agent.upper()
    agent_file_name = f"{agent_name}.md"

    if not target_root.exists():
        print(f"❌ Error: Target directory '{target_root}' does not exist.")
        sys.exit(1)
    
    if not templates_root.exists():
         print(f"❌ Error: Templates directory '{templates_root}' not found.")
         sys.exit(1)

    print(f"🚀 Bootstrapping AI Protocol into: {target_root}")
    print(f"📂 Source: {templates_root}")
    print(f"🤖 Agent Name: {agent_name}")
    print("-" * 40)

    # Agent file source: full bootloader or thin submodule template
    if args.monorepo_submodule:
        source_agent_file = templates_root / "AGENT_SUBMODULE.md"
    else:
        source_agent_file = templates_root / "PROTOCOL_BOOTLOADER.md"
    if not source_agent_file.exists():
        print(f"❌ Error: {source_agent_file.name} not found in templates.")
        sys.exit(1)

    payload = {
        # Agent file: bootloader or submodule template copied as <Agent>.md
        source_agent_file.name: agent_file_name,
        
        # Core Files
        "SCRIPTS-CATALOG.md": "SCRIPTS-CATALOG.md",
        "PROTOCOL.md": "PROTOCOL.md",
        
        # Docs
        "docs/CODING_STANDARDS.md": "docs/CODING_STANDARDS.md",
        "docs/TESTING.md": "docs/TESTING.md",
        "docs/PROGRESS.md": "docs/PROGRESS.md",
        "docs/context_registry.json": "docs/context_registry.json",
        "docs/requirements/TEMPLATE.md": "docs/requirements/TEMPLATE.md",
        
        # Scripts
        "scripts/context.py": "scripts/context.py"
    }

    created_count = 0
    skipped_count = 0

    for src_rel, dest_rel in payload.items():
        src_path = templates_root / src_rel
        dest_path = target_root / dest_rel

        if not src_path.exists():
            print(f"⚠️  Warning: Source file missing: {src_rel}")
            continue

        # Ensure destination directory exists
        dest_path.parent.mkdir(parents=True, exist_ok=True)

        if dest_path.exists() and not args.force:
            print(f"⏭️  Skipped (exists): {dest_rel}")
            skipped_count += 1
        else:
            try:
                shutil.copy2(src_path, dest_path)
                status = "Overwritten" if dest_path.exists() and args.force else "Created"
                print(f"✅ {status}: {dest_rel}")
                created_count += 1
            except Exception as e:
                print(f"❌ Failed to copy {src_rel}: {e}")

    # Substitute placeholders in agent file if using monorepo-submodule with flags
    if args.monorepo_submodule and (args.module_name or args.description):
        agent_dest = target_root / agent_file_name
        if agent_dest.exists():
            try:
                content = agent_dest.read_text(encoding="utf-8")
                if args.module_name:
                    content = content.replace("{{MODULE_NAME}}", args.module_name)
                if args.description:
                    content = content.replace("{{ONE_LINE_DESCRIPTION}}", args.description)
                agent_dest.write_text(content, encoding="utf-8")
                print(f"✅ Substituted placeholders in {agent_file_name}")
            except Exception as e:
                print(f"⚠️  Warning: Failed to substitute placeholders: {e}")

    print("-" * 40)
    print(f"🎉 Bootstrap Complete! ({created_count} created, {skipped_count} skipped)")

    # --- FINAL INSTRUCTIONS ---
    print("\n" + "="*60)
    print("📝 NEXT STEPS FOR THE USER")
    print("="*60)
    print(f"1.  Go to your project directory:\n    cd {args.target_dir}")
    print("\n2.  (Optional) Customize the context registry if needed:\n    Edit docs/context_registry.json")
    print("\n3.  Initialize your AI Agent with this prompt:")
    print("-" * 20)
    print(f'   "I have initialized the AI Protocol for this project.')
    print(f'    Please read {agent_file_name} to bootstrap your context and confirm you are ready."')
    print("-" * 20)
    print("="*60)

if __name__ == "__main__":
    main()