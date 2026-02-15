"""Tests for templates/scripts/context.py — JIT Context Engine."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

from conftest import REPO_ROOT

# ---------------------------------------------------------------------------
# get_repo_root
# ---------------------------------------------------------------------------


class TestGetRepoRoot:
    def test_returns_git_root_for_repo(self, context_module, tmp_path):
        """Inside a real git repo, should return the repo root."""
        root = context_module.get_repo_root(REPO_ROOT)
        assert root == REPO_ROOT

    def test_env_fallback(self, context_module, tmp_path, monkeypatch):
        """When git fails, fall back to REPO_ROOT env var."""
        monkeypatch.setenv("REPO_ROOT", str(tmp_path))
        # Use a directory that is NOT inside a git repo
        non_git = tmp_path / "not_a_repo"
        non_git.mkdir()
        root = context_module.get_repo_root(non_git)
        assert root == tmp_path

    def test_cwd_fallback(self, context_module, tmp_path, monkeypatch):
        """When git fails and no REPO_ROOT env, fall back to cwd argument."""
        monkeypatch.delenv("REPO_ROOT", raising=False)
        non_git = tmp_path / "not_a_repo"
        non_git.mkdir()
        root = context_module.get_repo_root(non_git)
        assert root == non_git

    def test_nonexistent_env_path(self, context_module, tmp_path, monkeypatch):
        """REPO_ROOT env pointing to nonexistent dir should fall through to cwd."""
        monkeypatch.setenv("REPO_ROOT", "/tmp/does_not_exist_xyz_999")
        non_git = tmp_path / "no_git"
        non_git.mkdir()
        root = context_module.get_repo_root(non_git)
        assert root == non_git


# ---------------------------------------------------------------------------
# load_registry
# ---------------------------------------------------------------------------


class TestLoadRegistry:
    def test_valid_json(self, context_module, tmp_path):
        reg = tmp_path / "reg.json"
        reg.write_text('{"key": "value"}')
        data = context_module.load_registry(reg)
        assert data == {"key": "value"}

    def test_missing_file_exits(self, context_module, tmp_path):
        with pytest.raises(SystemExit) as exc_info:
            context_module.load_registry(tmp_path / "missing.json")
        assert exc_info.value.code == 1

    def test_invalid_json_exits(self, context_module, tmp_path):
        bad = tmp_path / "bad.json"
        bad.write_text("{not valid json")
        with pytest.raises(SystemExit) as exc_info:
            context_module.load_registry(bad)
        assert exc_info.value.code == 1


# ---------------------------------------------------------------------------
# extract_section
# ---------------------------------------------------------------------------


class TestExtractSection:
    def test_basic_h2(self, context_module, tmp_path):
        md = tmp_path / "doc.md"
        md.write_text("# Title\n\n## Target\nContent here.\n\n## Other\nOther content.\n")
        result = context_module.extract_section(md, "Target")
        assert "## Target" in result
        assert "Content here." in result
        assert "Other content." not in result

    def test_nested_h3_included(self, context_module, tmp_path):
        md = tmp_path / "doc.md"
        md.write_text("## Parent\nIntro.\n### Child\nChild content.\n## Sibling\nStop.\n")
        result = context_module.extract_section(md, "Parent")
        assert "### Child" in result
        assert "Child content." in result
        assert "Sibling" not in result

    def test_stops_at_same_level(self, context_module, tmp_path):
        md = tmp_path / "doc.md"
        md.write_text("## A\nContent A.\n## B\nContent B.\n")
        result = context_module.extract_section(md, "A")
        assert "Content A." in result
        assert "Content B." not in result

    def test_stops_at_higher_level(self, context_module, tmp_path):
        md = tmp_path / "doc.md"
        md.write_text("## A\n### Sub\nSub content.\n# Top\nTop content.\n")
        result = context_module.extract_section(md, "A")
        assert "Sub content." in result
        assert "Top content." not in result

    def test_code_block_with_hash_not_treated_as_header(self, context_module, tmp_path):
        """P0.2 regression: # inside code blocks must not be treated as headers."""
        md = tmp_path / "doc.md"
        md.write_text(
            "## Config\nSome config.\n```bash\n# this is a comment\n## not a header\n```\n"
            "Still in Config.\n## Next\nDone.\n"
        )
        result = context_module.extract_section(md, "Config")
        assert "# this is a comment" in result
        assert "Still in Config." in result
        assert "Done." not in result

    def test_case_insensitive(self, context_module, tmp_path):
        md = tmp_path / "doc.md"
        md.write_text("## My Section\nContent.\n")
        result = context_module.extract_section(md, "my section")
        assert "Content." in result

    def test_not_found(self, context_module, tmp_path):
        md = tmp_path / "doc.md"
        md.write_text("## Existing\nContent.\n")
        result = context_module.extract_section(md, "Nonexistent")
        assert result == "Section not found."

    def test_file_not_found(self, context_module, tmp_path):
        result = context_module.extract_section(tmp_path / "nope.md", "Anything")
        assert "Error" in result


# ---------------------------------------------------------------------------
# normalize_entries
# ---------------------------------------------------------------------------


class TestNormalizeEntries:
    def test_string_input(self, context_module):
        result = context_module.normalize_entries("file.md")
        assert result == [{"file": "file.md"}]

    def test_dict_with_file(self, context_module):
        result = context_module.normalize_entries({"file": "a.md", "section": "Intro"})
        assert result == [{"file": "a.md", "section": "Intro"}]

    def test_dict_without_file(self, context_module):
        result = context_module.normalize_entries({"description": "meta stuff"})
        assert result == []

    def test_mixed_list(self, context_module):
        result = context_module.normalize_entries(["a.md", {"file": "b.md"}])
        assert len(result) == 2
        assert result[0] == {"file": "a.md"}
        assert result[1] == {"file": "b.md"}

    def test_list_with_invalid_items(self, context_module):
        result = context_module.normalize_entries([42, {"no_file": True}, "ok.md"])
        assert len(result) == 1
        assert result[0] == {"file": "ok.md"}

    def test_non_standard_type(self, context_module):
        result = context_module.normalize_entries(42)
        assert result == []


# ---------------------------------------------------------------------------
# fetch_context
# ---------------------------------------------------------------------------


class TestFetchContext:
    def _make_registry(self, tmp_path, entries):
        """Helper: write a minimal registry and return (registry_dict, repo_root)."""
        reg = {"_meta": {"protocol_version": "1.0.0"}}
        reg.update(entries)
        return reg

    def test_whole_file_key(self, context_module, tmp_path, capsys):
        f = tmp_path / "hello.md"
        f.write_text("Hello world\n")
        registry = self._make_registry(tmp_path, {"greet": "hello.md"})
        context_module.fetch_context("greet", registry, tmp_path)
        out = capsys.readouterr().out
        assert "Hello world" in out
        assert "--- Context: greet ---" in out

    def test_section_key(self, context_module, tmp_path, capsys):
        f = tmp_path / "doc.md"
        f.write_text("## Intro\nWelcome.\n## Other\nBye.\n")
        registry = self._make_registry(
            tmp_path, {"intro": {"file": "doc.md", "section": "Intro"}}
        )
        context_module.fetch_context("intro", registry, tmp_path)
        out = capsys.readouterr().out
        assert "Welcome." in out
        assert "Bye." not in out

    def test_meta_key_exits(self, context_module, tmp_path):
        registry = {"_meta": {"protocol_version": "1.0.0"}}
        with pytest.raises(SystemExit) as exc_info:
            context_module.fetch_context("_meta", registry, tmp_path)
        assert exc_info.value.code == 1

    def test_unknown_key_exits(self, context_module, tmp_path):
        registry = {"known": "file.md"}
        with pytest.raises(SystemExit) as exc_info:
            context_module.fetch_context("unknown", registry, tmp_path)
        assert exc_info.value.code == 1

    def test_missing_file(self, context_module, tmp_path, capsys):
        registry = self._make_registry(tmp_path, {"broken": "nonexistent.md"})
        context_module.fetch_context("broken", registry, tmp_path)
        captured = capsys.readouterr()
        assert "Error" in captured.err or "not found" in captured.err


# ---------------------------------------------------------------------------
# Integration tests (subprocess)
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestContextCLI:
    SCRIPT = str(REPO_ROOT / "templates" / "scripts" / "context.py")

    def _run(self, *args, cwd=None):
        return subprocess.run(
            [sys.executable, self.SCRIPT, *args],
            capture_output=True,
            text=True,
            cwd=cwd or REPO_ROOT,
            timeout=10,
        )

    def _setup_project(self, tmp_path):
        """Create a minimal project with registry for CLI tests."""
        docs = tmp_path / "docs"
        docs.mkdir()
        (tmp_path / "hello.md").write_text("# Hello\nWorld.\n")
        registry = {
            "_meta": {"protocol_version": "1.0.0"},
            "greet": "hello.md",
        }
        (docs / "context_registry.json").write_text(json.dumps(registry))
        # Need a git repo so get_repo_root works
        subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True)
        return tmp_path

    def test_list_command(self, tmp_path):
        project = self._setup_project(tmp_path)
        result = self._run("list", cwd=project)
        assert result.returncode == 0
        assert "greet" in result.stdout

    def test_fetch_command(self, tmp_path):
        project = self._setup_project(tmp_path)
        result = self._run("fetch", "greet", cwd=project)
        assert result.returncode == 0
        assert "World." in result.stdout

    def test_no_args_usage(self, tmp_path):
        project = self._setup_project(tmp_path)
        result = self._run(cwd=project)
        assert result.returncode == 1
        assert "Usage" in result.stderr

    def test_invalid_command(self, tmp_path):
        project = self._setup_project(tmp_path)
        result = self._run("bogus", cwd=project)
        assert result.returncode == 1
        assert "Usage" in result.stderr
