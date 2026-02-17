"""Tests for scripts/check_protocol.py — Protocol version drift checker."""

import json
import subprocess
import sys

import pytest

from conftest import REPO_ROOT


# ---------------------------------------------------------------------------
# get_script_root
# ---------------------------------------------------------------------------


class TestGetScriptRoot:
    def test_returns_repo_root(self, check_protocol_module):
        root = check_protocol_module.get_script_root()
        assert root == REPO_ROOT
        assert (root / "VERSION").exists()


# ---------------------------------------------------------------------------
# read_protocol_version
# ---------------------------------------------------------------------------


class TestReadProtocolVersion:
    def test_valid(self, check_protocol_module, tmp_path):
        (tmp_path / "VERSION").write_text("2.0.0\n")
        assert check_protocol_module.read_protocol_version(tmp_path) == "2.0.0"

    def test_missing(self, check_protocol_module, tmp_path):
        assert check_protocol_module.read_protocol_version(tmp_path) is None

    def test_empty(self, check_protocol_module, tmp_path):
        (tmp_path / "VERSION").write_text("")
        assert check_protocol_module.read_protocol_version(tmp_path) is None


# ---------------------------------------------------------------------------
# read_target_version
# ---------------------------------------------------------------------------


class TestReadTargetVersion:
    def test_valid(self, check_protocol_module, tmp_path):
        docs = tmp_path / "docs"
        docs.mkdir()
        registry = {"_meta": {"protocol_version": "1.0.0"}}
        (docs / "context_registry.json").write_text(json.dumps(registry))
        assert check_protocol_module.read_target_version(tmp_path) == "1.0.0"

    def test_missing_registry(self, check_protocol_module, tmp_path):
        assert check_protocol_module.read_target_version(tmp_path) is None

    def test_no_meta(self, check_protocol_module, tmp_path):
        docs = tmp_path / "docs"
        docs.mkdir()
        (docs / "context_registry.json").write_text('{"key": "value"}')
        assert check_protocol_module.read_target_version(tmp_path) is None

    def test_invalid_json(self, check_protocol_module, tmp_path):
        docs = tmp_path / "docs"
        docs.mkdir()
        (docs / "context_registry.json").write_text("{bad json")
        assert check_protocol_module.read_target_version(tmp_path) is None


# ---------------------------------------------------------------------------
# Integration tests (subprocess)
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestCheckProtocolCLI:
    SCRIPT = str(REPO_ROOT / "scripts" / "check_protocol.py")

    def _setup_target(self, tmp_path, version=None):
        """Create a target project dir with optional protocol version."""
        docs = tmp_path / "docs"
        docs.mkdir()
        if version is not None:
            registry = {"_meta": {"protocol_version": version}}
            (docs / "context_registry.json").write_text(json.dumps(registry))
        return tmp_path

    def _run(self, *args):
        return subprocess.run(
            [sys.executable, self.SCRIPT, *args],
            capture_output=True,
            text=True,
            timeout=10,
        )

    def test_version_match(self, tmp_path):
        # Read actual protocol version
        version = (REPO_ROOT / "VERSION").read_text().strip()
        self._setup_target(tmp_path, version)
        result = self._run(str(tmp_path))
        assert result.returncode == 0
        assert "OK" in result.stdout

    def test_version_drift(self, tmp_path):
        self._setup_target(tmp_path, "0.0.0-fake")
        result = self._run(str(tmp_path))
        assert result.returncode == 1
        assert "Drift" in result.stdout

    def test_no_target_version(self, tmp_path):
        self._setup_target(tmp_path, version=None)
        result = self._run(str(tmp_path))
        assert result.returncode == 0
        assert "no protocol version" in result.stdout.lower()

    def test_nonexistent_target(self):
        result = self._run("/tmp/nonexistent_dir_xyz_999")
        assert result.returncode == 1
        assert "Error" in result.stdout or "does not exist" in result.stdout
