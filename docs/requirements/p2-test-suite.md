# P2 — Tests & Validation

> Branch: `feature/20260212-013645-add-test-suite`
> Parent: `main` at `b8901d3`

---

## Purpose

Add a comprehensive pytest suite covering all three scripts (`context.py`, `bootstrap.py`, `check_protocol.py`) plus template consistency validation.

---

## Implementation Checklist

- [x] **2.1** Add pytest + pytest-cov to dev dependencies in `pyproject.toml`
- [x] **2.2** Create `tests/` directory structure (`conftest.py`, `test_context.py`, `test_bootstrap.py`, `test_check_protocol.py`)
- [x] **2.3** Test `extract_section()` — header matching, nested headers, code-block regression test
- [x] **2.4** Test `normalize_entries()` — string/dict/list inputs, `_meta` filtering
- [x] **2.5** Test `bootstrap.py` — normal inject, skip existing, `--force`, `--monorepo-submodule`, missing templates, bad target dir
- [x] **2.6** Test `check_protocol.py` — version match/drift/missing
- [x] **2.7** Template consistency validation — registry keys point to real files, sections exist, `uv run` syntax, clean PROGRESS.md

---

## Test Summary

| File | Unit | Integration | Total |
|------|------|-------------|-------|
| `test_context.py` | 26 | 4 | 30 |
| `test_bootstrap.py` | 9 | 1 | 10 |
| `test_check_protocol.py` | 8 | 4 | 12 |
| `test_template_consistency.py` | 6 | 0 | 6 |
| **Total** | **49** | **9** | **58** |

---

## Design Decisions

1. **Import via `importlib.util`** — scripts aren't packages; session-scoped fixtures keep it fast
2. **Unit + integration split** — pure functions tested directly; CLI entry points tested via subprocess with `@pytest.mark.integration` marker
3. **`sys.exit` handling** — `pytest.raises(SystemExit)` for unit tests; `returncode` check for subprocess tests
4. **`tmp_path` for filesystem isolation** — never `cd` into temp dirs; use `cwd=` param or absolute paths
5. **Real templates dir** — `resolve_roots()` / `get_script_root()` work correctly via importlib since `__file__` is preserved
