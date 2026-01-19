# AI Protocol & Context Management

This repository stores the "AI Context Files" (e.g., `CLAUDE.md`, `GEMINI.md`) and standard protocols used to guide AI agents in software projects.

## Usage

1.  **Copy the Template:**
    - Copy `PROTOCOL.md` to your project's root directory.
    - Rename it to match your AI tool (e.g., `CLAUDE.md` or `GEMINI.md`).

2.  **Customize:**
    - Fill in the `<!-- CUSTOMIZE -->` sections in the copied file.
    - Define your project's `Goal`, `Tech Stack`, and `Architecture`.
    - Update the `Tooling & Environment` section with your specific commands.

3.  **Establish Standards:**
    - Copy `docs/CODING_STANDARDS.md` to your project's `docs/` folder (or customize it).
    - Ensure your AI agent reads these files at the start of every session.

## Examples

See the `examples/` directory for real-world usages:
- `examples/DJANGO_CLAUDE.md`: A Django-based CV Maker project.
- `examples/ODOO_GEMINI.md`: An Odoo 18 enterprise integration project.
- `examples/ODOO_STANDARDS_EXAMPLE.md`: Detailed coding standards for Odoo.

## Core Philosophy

- **Context is King:** The AI must know *where* it is (branch), *what* it is doing (requirements), and *how* to do it (standards) before writing code.
- **Strict Safety:** AI agents must never execute dangerous commands without permission.
- **Documentation First:** Requirements and progress must be updated *as part of the work*, not after.
