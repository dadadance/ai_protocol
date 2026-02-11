# AI Agent Development Protocol (AADP)

A battle-tested, general-purpose framework designed to orchestrate AI agents (Gemini, Claude, GPT) for high-performance, safe, and context-aware software development. 

This protocol bridges the gap between raw LLM capabilities and professional engineering standards by enforcing a JIT (Just-In-Time) context architecture and strict operational handshakes.

## 🎯 Purpose

- **Context-Grounded Development:** Agents fetch task-specific requirements and standards dynamically, reducing hallucination by grounding decisions in real project documentation.
- **Strict Safety Handshakes:** Mandatory explanation and confirmation for all system-modifying actions.
- **Headless-First Engineering:** Prioritizes CLI accessibility and scriptability over fragile UI-only logic.
- **Project Agnostic:** Designed to be dropped into any project (New or Existing, Python, JS, Go, etc.).

## ✨ Core Pillars

1.  **JIT Context Injection:** Uses `scripts/context.py` to pull precise sections of documentation into the agent's context window.
2.  **Strict Branching & Scope:** Forces a "Branch -> Requirement -> Implementation" workflow to prevent scope creep and logic fragmentation.
3.  **Functional-First Standards:** Promotes pure functions, immutability, and composition for testable and predictable codebases.
4.  **Scripts Catalog:** A centralized registry (`SCRIPTS-CATALOG.md`) that acts as the "Source of Truth" for automation scripts.

## ⚡ Quick Start: New Project

If you are starting a brand new project, use this one-liner from your projects directory:

```bash
# 1. Create and initialize the project
mkdir my-new-project && cd my-new-project && git init

# 2. Inject the Protocol (assuming ai-protocol is a sibling directory)
uv run ../ai-protocol/scripts/bootstrap.py . --agent claude
```

## 🚀 How to Adopt (Existing Projects)

### 1. Run the Bootstrap Script
From within this `ai_protocol` repository, run the bootstrapper pointing to your target project:

```bash
uv run scripts/bootstrap.py /path/to/your/project --agent claude
```

### 2. Verify and Customize
The script will inject all necessary files. You may want to:
- Review and edit `docs/context_registry.json` if you have custom documentation paths.
- Customize `docs/CODING_STANDARDS.md` for your specific tech stack.

### 3. Initialize your Agent
Open your project and provide your AI agent with this activation prompt (use the agent file name you chose, e.g. GEMINI.md or CLAUDE.md):
> "I have initialized the AI Protocol for this project. Please read GEMINI.md to bootstrap your context and confirm you are ready."

## 📁 Repository Structure

**In this repo (ai-protocol):** One agent instruction template; bootstrap creates the agent file in the target.

```text
ai-protocol/
├── templates/
│   ├── PROTOCOL_BOOTLOADER.md   # Single source for agent instructions
│   ├── AGENT_SUBMODULE.md       # Thin agent file for monorepo submodules
│   ├── PROTOCOL.md              # Full protocol (fetched via context.py)
│   ├── SCRIPTS-CATALOG.md       # Registry of automation scripts
│   ├── docs/
│   │   ├── CODING_STANDARDS.md  # Universal engineering guidelines
│   │   ├── PROGRESS.md          # Project-wide status tracker (Template)
│   │   ├── context_registry.json # Mapping for JIT context fetching
│   │   └── requirements/        # Task-specific requirement documents
│   └── scripts/context.py      # JIT context engine (injected to target)
└── scripts/bootstrap.py        # One-command protocol installer
```

**After bootstrap**, the target project gets e.g. `GEMINI.md` or `CLAUDE.md` (content from PROTOCOL_BOOTLOADER.md), plus `docs/`, `scripts/context.py`, and `SCRIPTS-CATALOG.md`.

## Single-project vs monorepo

- **Single-project mode (default):** One repo, one protocol. Bootstrap injects the full agent file (e.g. `GEMINI.md`), `scripts/context.py`, and `docs/` into that repo. The agent runs in that repo and uses local context only.
- **Monorepo mode:** Protocol and context live at the **repository root**. The root has the full bootloader (in `GEMINI.md` / `CLAUDE.md`), `scripts/context.py`, and `docs/context_registry.json`. Submodules get a **thin agent file** that delegates to the root:
  - Run bootstrap with `--monorepo-submodule` to inject `templates/AGENT_SUBMODULE.md` as e.g. `GEMINI.md`:  
    `uv run scripts/bootstrap.py /path/to/submodule --agent claude --monorepo-submodule`
  - Use `--module-name` and `--description` to auto-fill placeholders:  
    `uv run scripts/bootstrap.py /path/to/submodule --agent claude --monorepo-submodule --module-name "my-module" --description "One-line description"`
  - Or manually edit the injected file to replace `{{MODULE_NAME}}` and `{{ONE_LINE_DESCRIPTION}}`.
  - The agent should use the root for protocol and JIT context (e.g. run `./scripts/context.py` from repo root).

After bootstrap in a monorepo, you can replace a submodule's agent file with the thin template so submodule sessions still get protocol and context from the root.

### Monorepo context.py limitations

`context.py` resolves the repository root using `git rev-parse --show-toplevel`. In a monorepo with git submodules, this command returns the **submodule's** root when run from inside a submodule, not the parent monorepo's root. This means:

- **Always run `context.py` from the monorepo root**, not from inside a submodule.
- Alternatively, set the `REPO_ROOT` environment variable to the monorepo root before running `context.py`.
- You can also call the root's `context.py` explicitly from submodules: `../scripts/context.py fetch <key>` (adjust path as needed).

If you run `context.py` from inside a submodule without these precautions, it will look for `docs/context_registry.json` in the submodule (which may not exist or may have different content).

## Protocol version and drift check

The template injects `_meta.protocol_version` in `docs/context_registry.json` (e.g. `1.0.0`). The canonical version lives in this repo's `VERSION` file. To check if a target project is in sync:

```bash
# From ai-protocol directory
uv run scripts/check_protocol.py /path/to/target
```

If omitted, the target defaults to the current directory. Exit code 0 means version match or no version to compare; exit code 1 means drift. The script does not modify any files.

## Development (this repo)

- Install dev deps: `uv sync --extra dev` (includes Ruff).
- Lint: `uv run ruff check .`
- Format: `uv run ruff format .`

## 📄 License
[MIT License](./LICENSE)
