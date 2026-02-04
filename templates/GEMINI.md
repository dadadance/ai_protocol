# Gemini Agent Protocol (JIT Context)

## 0. 🚨 Auto-Initialization
Specialized protocol context and discovery are triggered ONLY when the keyword **"PROTOCOL"** is included in a task assignment. General project context is maintained via the local `GEMINI.md` file.

## 1. Identity & Safety (MANDATORY)
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

**CRITICAL:** This workflow is ONLY triggered when the user includes the keyword **"PROTOCOL"** at the beginning or end of a task assignment.

### Phase 1: ❓ Discovery & Validation (Triggered by "PROTOCOL")
When triggered, you MUST:
1.  **Context Check:** Verify the current branch and repository state (e.g., `git branch --show-current`).
2.  **Retrieve Standards:** Automatically fetch naming conventions and coding standards from `protocol:standards`.
3.  **Define Scope:** Break down the requirements and acceptance criteria into a structured plan.
4.  **Verification Strategy:** Define the testing strategy (unit, integration, etc.) for the task.
5.  **Confirmation:** Present the plan (Branch, Scope, Tests) to the user for approval before proceeding.

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