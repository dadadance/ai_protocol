"""Shared fixtures for the ai-protocol test suite."""

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


def _import_script(name: str, path: Path):
    """Import a standalone script as a module (scripts aren't packages)."""
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="session")
def context_module():
    return _import_script("context", REPO_ROOT / "templates" / "scripts" / "context.py")


@pytest.fixture(scope="session")
def bootstrap_module():
    return _import_script("bootstrap", REPO_ROOT / "scripts" / "bootstrap.py")


@pytest.fixture(scope="session")
def check_protocol_module():
    return _import_script("check_protocol", REPO_ROOT / "scripts" / "check_protocol.py")
