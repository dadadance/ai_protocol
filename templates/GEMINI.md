# Gemini Agent Protocol (JIT Context)

## 0. Identity & Safety (MANDATORY)
You are an autonomous development agent.
1. **Safety First:** ALWAYS explain your plan before running shell commands.
2. **Stop on Error:** If a command fails, STOP and analyze. Do not loop.
3. **Paging System:** To avoid context overflow, DO NOT read large docs. Use the triggers below.

## 1. Context Triggers
Before starting any major task, fetch the required context.

| Task / Need | Command |
| :--- | :--- |
| **Project Setup & Rules** | `python3 scripts/context.py fetch protocol:init` |
| **Branching & Scope** | `python3 scripts/context.py fetch protocol:branching` |
| **Coding Standards** | `python3 scripts/context.py fetch protocol:standards` |
| **Testing Strategy** | `python3 scripts/context.py fetch protocol:testing` |
| **Scripts Catalog** | `python3 scripts/context.py fetch protocol:scripts` |
| **Current Progress** | `python3 scripts/context.py fetch protocol:progress` |

## 2. Dynamic Retrieval
- List all keys: `python3 scripts/context.py list`
- Maintain `docs/context_registry.json` if new documentation categories are added.

## 3. Mandatory Workflow

**CRITICAL:** Before generating any code, you MUST complete these steps:

### Phase 1: ❓ Discovery & Validation
You must explicitly ask the user:
1.  **Context:** "Are we on the correct branch? (Current: `<current_branch>`)"
2.  **Standards:** "Confirm naming conventions for this task?"
3.  **Scope:** "Please break down the requirements and acceptance criteria."
4.  **Verification:** "What is the testing strategy for this task?"

### Phase 2: 📝 Execution & Documentation
*   **Start:** Create/Update `SESSION_TODO.md` with the task breakdown.
*   **During:** Update `docs/PROGRESS.md` with key milestones.
*   **End:**
    1.  Update `docs/PROGRESS.md` (mark completed items).
    2.  Update `GEMINI.md` (this file) with "Lessons Learned" (see below).
    3.  Provide a summary of "What was done" vs "What is left".

### Phase 3: 🧠 Knowledge Retention
*   **Action:** If you encounter a tricky bug, a specific config nuance, or a non-standard workflow, append it to the `## 🧠 Lessons Learned` section below.

## 🧠 Lessons Learned
*(Agent: Append new findings here during development)*