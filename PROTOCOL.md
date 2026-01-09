# Project Name - Master Context

## 0. Core Protocol: Context & Requirements (MANDATORY)

To minimize hallucination and ensure strict alignment with project goals, the AI Agent **MUST** follow this sequence at the start of every task:

1.  **Analyze & Confirm:** Identify the active git branch. **Explicitly ask the user:** _"Are we on the correct branch for this task, and are the relevant requirements in `docs/requirements/` up to date?"_
2.  **Locate Requirements:** Once confirmed, navigate to `docs/requirements/` and read the specific file matching the branch's scope.
3.  **Verify Status:** Check the **"Implementation Checklist"** section within that same requirements file to see what is already done.
4.  **Align & Act:** Only proceed with code generation or modification after establishing this grounded context.

### 0.1. Safety & Autonomy (Strict)
- **Ask Before Acting:** You MUST describe the intended action and wait for user confirmation before running any shell command or modifying files.
- **Explicit Permission:** You are only allowed to run autonomously if the user explicitly grants permission (e.g., "Run autonomously", "Go ahead").
- **Stop-on-Error:** If a command fails, **STOP**. Analyze the error, explain it to the user, and propose a fix. Do not blindly retry or loop.

**Universal Rule:** This "Branch -> Requirement (with Status)" workflow is the default standard for ALL projects.

## 1. Project Overview

- **Goal:** [Enter Goal Here]
- **Tech Stack:** [Enter Stack Here]

## 1.1. Tooling & Environment
- **Package Manager:** [e.g., uv, pnpm, cargo] - STRICTLY USE THIS.
- **Environment:** [e.g., Local .venv, Docker]
- **Run Commands:** [List standard run/build/test commands]

## 2. Coding Standards & Conventions

- **Standard Compliance:** All code must strictly follow the patterns defined in `docs/coding_standards.md`.
- **Reference Instruction:** When asking for code generation, use the trigger: "Generate code following the standards in docs/coding_standards.md."
- **Standard Operating Procedure:** Before generating any code, you MUST read `docs/coding_standards.md`.
- **Research First:** Before writing code, you MUST verify the latest recommended patterns for the specific library/framework. Do not rely on outdated assumptions.

### 2.1. Strict Protocol: Git Branching & Scope

**Mandatory Rules for AI & User:**

1.  **Pre-Creation Interrogation:** Before creating ANY new branch, the AI MUST explicitly ask the User:
    *   "What kind of branch is this?" (e.g., Feature, Bugfix, Hotfix)
    *   "Where is the project general progress report doc?" (e.g., `docs/PROGRESS.md`)
    *   "Where is the branch/topic specific doc?" (e.g., `docs/requirements/my_feature.md`)
    *   The AI must then **propose a branch name** based on the answers.
    *   Only AFTER this handshake can the AI begin planning.
2.  **Naming Convention:** The branch name MUST follow the format: `<branch-type>/yyyymmdd-hhmmss-<meaningful-name>`. Use the system date for the timestamp.
3.  **Scope Enforcement:** The AI is strictly forbidden from suggesting or performing tasks outside the branch's defined scope.
4.  **Atomic Changes:** Keep file modifications atomic. Do not mix refactoring with feature work in the same step/commit.
5.  **Conventional Commits:** Commit messages must follow the [Conventional Commits](https://www.conventionalcommits.org/) format (e.g., `feat: ...`, `fix: ...`, `docs: ...`).

### 2.2. Documentation Protocol (Mandatory)

**Always finish working on a branch by updating the following documents (at least after the commit):**

1.  **Project General Progress Report:** (e.g., `docs/PROGRESS.md`) - Update the overall status.
2.  **Branch/Topic Specific Document:** (e.g., `docs/requirements/my_feature.md`) - Update detailed checklists and notes.

### 2.3. Verification Standard
- **Test Command:** Run `[insert command]` before requesting any commit.
- **Lint Command:** Run `[insert command]` to ensure style compliance.
- **Definition of Done:** All tests pass, linting passes, and documentation is updated.

### 2.4. Architectural Constraints
- **Forbidden Libraries:** [List libraries or patterns to avoid]
- **Directory Structure:** Do not create files in root without permission. Follow the established folder hierarchy.
- **Security:** Never commit secrets or hardcoded credentials. Use environment variables.