"""Tests for scripts/bootstrap.py — AI Protocol Bootstrapper."""

import subprocess
import sys

import pytest

from conftest import REPO_ROOT

# The set of destination files created by a normal (non-submodule) bootstrap.
# The agent file name depends on --agent; here we assume --agent claude → CLAUDE.md
EXPECTED_DEST_FILES = {
    "CLAUDE.md",
    "SCRIPTS-CATALOG.md",
    "PROTOCOL.md",
    "docs/CODING_STANDARDS.md",
    "docs/TESTING.md",
    "docs/PROGRESS.md",
    "docs/context_registry.json",
    "docs/requirements/TEMPLATE.md",
    "scripts/context.py",
}


class TestResolveRoots:
    def test_returns_templates_dir(self, bootstrap_module):
        templates = bootstrap_module.resolve_roots()
        assert templates.name == "templates"
        assert templates.exists()
        assert (templates / "PROTOCOL_BOOTLOADER.md").exists()


class TestBootstrapNormal:
    """Unit tests that drive main() via monkeypatched sys.argv."""

    def test_normal_inject_creates_files(self, bootstrap_module, tmp_path, monkeypatch):
        monkeypatch.setattr(
            sys, "argv", ["bootstrap.py", str(tmp_path), "--agent", "claude"]
        )
        bootstrap_module.main()
        for rel in EXPECTED_DEST_FILES:
            assert (tmp_path / rel).exists(), f"Missing: {rel}"

    def test_creates_subdirectories(self, bootstrap_module, tmp_path, monkeypatch):
        monkeypatch.setattr(
            sys, "argv", ["bootstrap.py", str(tmp_path), "--agent", "claude"]
        )
        bootstrap_module.main()
        assert (tmp_path / "docs").is_dir()
        assert (tmp_path / "scripts").is_dir()
        assert (tmp_path / "docs" / "requirements").is_dir()

    def test_skip_existing_no_force(self, bootstrap_module, tmp_path, monkeypatch):
        sentinel = "ORIGINAL CONTENT"
        agent_file = tmp_path / "CLAUDE.md"
        agent_file.parent.mkdir(parents=True, exist_ok=True)
        agent_file.write_text(sentinel)
        monkeypatch.setattr(
            sys, "argv", ["bootstrap.py", str(tmp_path), "--agent", "claude"]
        )
        bootstrap_module.main()
        assert agent_file.read_text() == sentinel

    def test_force_overwrites(self, bootstrap_module, tmp_path, monkeypatch):
        sentinel = "ORIGINAL CONTENT"
        agent_file = tmp_path / "CLAUDE.md"
        agent_file.parent.mkdir(parents=True, exist_ok=True)
        agent_file.write_text(sentinel)
        monkeypatch.setattr(
            sys,
            "argv",
            ["bootstrap.py", str(tmp_path), "--agent", "claude", "--force"],
        )
        bootstrap_module.main()
        assert agent_file.read_text() != sentinel

    def test_monorepo_submodule(self, bootstrap_module, tmp_path, monkeypatch):
        monkeypatch.setattr(
            sys,
            "argv",
            [
                "bootstrap.py",
                str(tmp_path),
                "--agent",
                "claude",
                "--monorepo-submodule",
            ],
        )
        bootstrap_module.main()
        agent_content = (tmp_path / "CLAUDE.md").read_text()
        assert "submodule" in agent_content.lower()

    def test_monorepo_submodule_substitution(
        self, bootstrap_module, tmp_path, monkeypatch
    ):
        monkeypatch.setattr(
            sys,
            "argv",
            [
                "bootstrap.py",
                str(tmp_path),
                "--agent",
                "claude",
                "--monorepo-submodule",
                "--module-name",
                "my_module",
                "--description",
                "A great module",
            ],
        )
        bootstrap_module.main()
        content = (tmp_path / "CLAUDE.md").read_text()
        assert "my_module" in content
        assert "A great module" in content
        assert "{{MODULE_NAME}}" not in content
        assert "{{ONE_LINE_DESCRIPTION}}" not in content

    def test_bad_target_exits(self, bootstrap_module, monkeypatch):
        monkeypatch.setattr(
            sys,
            "argv",
            ["bootstrap.py", "/tmp/nonexistent_xyz_999", "--agent", "claude"],
        )
        with pytest.raises(SystemExit) as exc_info:
            bootstrap_module.main()
        assert exc_info.value.code == 1

    def test_payload_completeness(self, bootstrap_module, tmp_path, monkeypatch):
        """All created files should match the expected set exactly."""
        monkeypatch.setattr(
            sys, "argv", ["bootstrap.py", str(tmp_path), "--agent", "claude"]
        )
        bootstrap_module.main()
        created = set()
        for p in tmp_path.rglob("*"):
            if p.is_file():
                created.add(str(p.relative_to(tmp_path)))
        assert created == EXPECTED_DEST_FILES


@pytest.mark.integration
class TestBootstrapCLI:
    SCRIPT = str(REPO_ROOT / "scripts" / "bootstrap.py")

    def test_end_to_end(self, tmp_path):
        result = subprocess.run(
            [sys.executable, self.SCRIPT, str(tmp_path), "--agent", "claude"],
            capture_output=True,
            text=True,
            timeout=15,
        )
        assert result.returncode == 0
        assert "Bootstrap Complete" in result.stdout
        for rel in EXPECTED_DEST_FILES:
            assert (tmp_path / rel).exists(), f"Missing: {rel}"
