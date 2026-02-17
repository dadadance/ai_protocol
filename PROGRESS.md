# AADP — Post-Review Roadmap Progress

> Tracking execution of the Post-Review Action Plan.
> Branch: `feature/20260212-013645-add-test-suite`
> Last Updated: 2026-02-12

---

## High-Level Status

| Tier | Status | Summary |
|------|--------|---------|
| **P0 — Broken on First Use** | **DONE** | All 5 items committed (`cd28d03`) |
| **P1 — Self-Consistency** | **DONE** | All 9 items committed (`b8901d3`) |
| **P2 — Tests & Validation** | **DONE** | 58 tests, all passing (`feature/20260212-013645-add-test-suite`) |
| **P3 — Production Features** | NOT STARTED | Each item needs own branch |

---

## Completed — P0 (commit `cd28d03`)

- [x] **0.1** Fix `uv` → `uv run` in PROTOCOL_BOOTLOADER.md (7 commands)
- [x] **0.2** Port code-block fence tracking into `templates/scripts/context.py`
- [x] **0.3** Remove `section` filter from `protocol:standards` registry key
- [x] **0.4** Clean `templates/docs/PROGRESS.md` of project-specific history
- [x] **0.5** Remove dangling `GEMINI.md` symlink

## Completed — P1 (commit `b8901d3`)

- [x] **1.1** Delete diverged root `scripts/context.py`
- [x] **1.2** Remove `docs -> templates/docs` symlink
- [x] **1.3** Add root `.gitignore`
- [x] **1.4** Delete dead `main.py`
- [x] **1.5** Fix `pyproject.toml` — version `1.0.0`, real description
- [x] **1.6** Add usage message to `context.py` (no-args and invalid command)
- [x] **1.7** Fix bootstrap.py `Created/Overwritten` status (check existence before copy)
- [x] **1.8** Make `--agent` required (no more GEMINI default)
- [x] **1.9** Replace "Zero-Hallucination Context" with "Context-Grounded Development" in README

---

## Completed — P2 (`feature/20260212-013645-add-test-suite`)

- [x] **2.1** Add pytest + pytest-cov to dev dependencies in `pyproject.toml`
- [x] **2.2** Create `tests/` directory structure (`conftest.py`, `test_context.py`, `test_bootstrap.py`, `test_check_protocol.py`)
- [x] **2.3** Test `extract_section()` — header matching, nested headers, code-block regression test
- [x] **2.4** Test `normalize_entries()` — string/dict/list inputs, `_meta` filtering
- [x] **2.5** Test `bootstrap.py` — normal inject, skip existing, `--force`, `--monorepo-submodule`, missing templates, bad target dir
- [x] **2.6** Test `check_protocol.py` — version match/drift/missing
- [x] **2.7** Template consistency validation — registry keys point to real files, sections exist, `uv run` syntax, clean PROGRESS.md

---

## Next: P3 — Production Features (separate branches each)

- [ ] **3.1** Non-destructive upgrade path (`check_protocol.py --diff`, `bootstrap.py --update`, checksum manifest)
- [ ] **3.2** `--dry-run` for bootstrap.py (prerequisite for 3.1)
- [ ] **3.3** Selective injection (`--only`, `--skip`)
- [ ] **3.4** Reduce Python bias — honest scoping in README, `--lang` flag, lang-specific templates
- [ ] **3.5** CI pipeline (`.github/workflows/ci.yml`)
- [ ] **3.6** Add `.gitignore` to bootstrap payload
- [ ] **3.7** Improve agent activation docs (per-agent setup instructions)

**Dependency:** 3.2 (dry-run) before 3.1 (upgrade path). 3.5 (CI) ideally right after P2.

---

## Known Issues

- Pre-existing lint warnings in `bootstrap.py` and `check_protocol.py` (whitespace, line length, unused import `os`, f-string without placeholder). Not fixed — out of scope for this branch per atomic-change rule. Should be addressed in a separate `refactor/` branch or as part of P2.
- `SCRIPTS-CATALOG.md` symlink still exists at root (valid, target exists). Not removed — wasn't in scope.
