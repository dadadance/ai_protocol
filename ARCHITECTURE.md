# AI Protocol Architecture: The "Seed Bank" Model

This repository serves as the central source of truth for the AI Agent Protocol. It cleanly separates the **Payload** (files to be injected) from the **Injector** (the delivery mechanism).

## 1. Repository Structure

```text
ai_protocol/ (Root)
│
├── templates/ ........................ [THE PAYLOAD] "Golden Copy" of all files
│   ├── PROTOCOL_BOOTLOADER.md          # Single source: agent instructions (→ GEMINI.md / CLAUDE.md at inject)
│   ├── SCRIPTS-CATALOG.md              # Template registry
│   │
│   ├── docs/ ......................... [Documentation Templates]
│   │   ├── CODING_STANDARDS.md         # Template engineering standards
│   │   ├── TESTING.md                  # Template testing strategy
│   │   ├── PROGRESS.md                 # Template progress tracker
│   │   ├── context_registry.json       # JIT context mapping
│   │   └── requirements/
│   │       └── TEMPLATE.md             # Requirement doc template
│   │
│   └── scripts/ ...................... [Injected Tools]
│       └── context.py                  # The JIT Context Engine (deployed to target)
│
├── scripts/ .......................... [THE INJECTOR] Tools for *this* repo
│   ├── bootstrap.py                    # The "Seeder" script
│   └── check_protocol.py               # Compare protocol version with a target (drift check)
│
├── VERSION                             # Protocol version (e.g. 1.0.0)
├── README.md
└── LICENSE
```

## 2. The Injection Process (`bootstrap.py`)

When you run `bootstrap.py`, it acts as a "Seeder," copying files from `templates/` to your target project.

```text
       [Source: ai_protocol/templates]                  [Target Project]
       ───────────────────────────────                  ────────────────
                                                        (e.g., ../cv_maker)

          PROTOCOL_BOOTLOADER.md ────(Copy as <Agent>.md)──►  GEMINI.md | CLAUDE.md
                                          │
          templates/docs/*     ────────(Copy)────────►  docs/*
                                          │
          templates/scripts/*  ────────(Copy)────────►  scripts/context.py
                                          │
          SCRIPTS-CATALOG.md   ────────(Copy)────────►  SCRIPTS-CATALOG.md
```

## 3. Workflow for a New Project

1.  **Run the Injector:**
    ```bash
    # From ai_protocol/
    uv run scripts/bootstrap.py ../new_project --agent gemini
    ```

2.  **Result in Target:**
    The new project is instantly hydrated with the full protocol stack:
    *   `<Agent>.md` (e.g. GEMINI.md or CLAUDE.md — copied from PROTOCOL_BOOTLOADER.md)
    *   `scripts/context.py` (JIT tool)
    *   `docs/` (Standards & Progress)

3.  **Activate:**
    User gives the "Handshake Prompt" to the agent in the new project.
