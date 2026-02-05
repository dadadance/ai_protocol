# AI Agent Protocol (JIT Context)

## 0. Identity & Safety (MANDATORY)
You are an autonomous development agent.
1. **Safety First:** ALWAYS explain your plan before running shell commands.
2. **Stop on Error:** If a command fails, STOP and analyze. Do not loop.
3. **Paging System:** To avoid context overflow, DO NOT read large docs. Use the triggers below.

## 1. Context Triggers (When to Invoke)

**MANDATORY:** Run the context command *before* the corresponding action. Do not skip.

| When to Invoke | Command |
| :--- | :--- |
| **Session start** or **new task** | `uv scripts/context.py fetch protocol:init` |
| **Before creating a branch** | `uv scripts/context.py fetch protocol:branching` |
| **Before generating or modifying ANY code** | `uv scripts/context.py fetch protocol:standards` |
| **Before writing or running tests** | `uv scripts/context.py fetch protocol:testing` |
| **Before creating a new script** | `uv scripts/context.py fetch protocol:scripts` |
| **Task start** (see state) or **task end** (before updating) | `uv scripts/context.py fetch protocol:progress` |

**Branch naming convention:** `<branch-type>/yyyymmdd-hhmmss-<meaningful-name>` (e.g. `feature/20260204-143000-websocket-v2`). Use `date +%Y%m%d-%H%M%S` for timestamp.

## 2. Dynamic Retrieval
- List all keys: `uv scripts/context.py list`
- Maintain `docs/context_registry.json` if new documentation categories are added.

## 3. Mandatory Workflow
- **Confirm Branch:** Ask "Are we on the correct branch?"
- **Read Requirements:** Fetch context for the current task scope.
- **Update Progress:** Update `docs/PROGRESS.md` after completion.
