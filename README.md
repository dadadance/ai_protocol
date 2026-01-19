# AI Agent Development Protocol (AADP)

A battle-tested, general-purpose framework designed to orchestrate AI agents (Gemini, Claude, GPT) for high-performance, safe, and context-aware software development. 

This protocol bridges the gap between raw LLM capabilities and professional engineering standards by enforcing a JIT (Just-In-Time) context architecture and strict operational handshakes.

## 🎯 Purpose

- **Zero-Hallucination Context:** Agents fetch task-specific requirements and standards dynamically.
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
uv run ../ai-protocol/scripts/bootstrap.py . --agent gemini
```

## 🚀 How to Adopt (Existing Projects)

### 1. Run the Bootstrap Script
From within this `ai_protocol` repository, run the bootstrapper pointing to your target project:

```bash
uv run scripts/bootstrap.py /path/to/your/project --agent gemini
```

### 2. Verify and Customize
The script will inject all necessary files. You may want to:
- Review and edit `docs/context_registry.json` if you have custom documentation paths.
- Customize `docs/CODING_STANDARDS.md` for your specific tech stack.

### 3. Initialize your Agent
Open your project and provide your AI agent with this activation prompt:
> "I have initialized the AI Protocol for this project. Please read GEMINI.md to bootstrap your context and confirm you are ready."

## 📁 Repository Structure

```text
.
├── PROTOCOL.md           # Full protocol content (Master Source)
├── PROTOCOL_BOOTLOADER.md # Lightweight entry point for agents (Template)
├── GEMINI.md             # Example: JIT bootloader for Gemini agents
├── SCRIPTS-CATALOG.md    # Registry of automation scripts
├── docs/
│   ├── CODING_STANDARDS.md  # Universal engineering guidelines
│   ├── PROGRESS.md          # Project-wide status tracker (Template)
│   ├── context_registry.json # Mapping for JIT context fetching
│   └── requirements/        # Task-specific requirement documents
└── scripts/
    ├── context.py           # The JIT context engine
    └── bootstrap.py         # The one-command protocol installer
```

## 📄 License
[MIT License](./LICENSE)