"""Template consistency validation tests.

Ensures that the template payload is internally consistent:
- Registry keys point to real files
- Section references resolve to actual content
- uv commands use `uv run` syntax
- PROGRESS.md template is generic (no project-specific content)
- All expected template files exist
- _meta.protocol_version matches VERSION file
"""

import json
import re
from pathlib import Path

import pytest

from conftest import REPO_ROOT

TEMPLATES_ROOT = REPO_ROOT / "templates"

# All 10 expected template files
EXPECTED_TEMPLATE_FILES = [
    "AGENT_SUBMODULE.md",
    "PROTOCOL.md",
    "PROTOCOL_BOOTLOADER.md",
    "SCRIPTS-CATALOG.md",
    "docs/CODING_STANDARDS.md",
    "docs/PROGRESS.md",
    "docs/TESTING.md",
    "docs/context_registry.json",
    "docs/requirements/TEMPLATE.md",
    "scripts/context.py",
]


@pytest.fixture(scope="module")
def registry():
    path = TEMPLATES_ROOT / "docs" / "context_registry.json"
    with open(path, encoding="utf-8") as f:
        return json.load(f)


class TestTemplateConsistency:
    def test_registry_keys_point_to_real_files(self, registry):
        """Every non-_meta registry key should reference a file that exists under templates/."""
        for key, value in registry.items():
            if key.startswith("_"):
                continue
            if isinstance(value, str):
                assert (TEMPLATES_ROOT / value).exists(), (
                    f"Registry key '{key}' → '{value}' not found"
                )
            elif isinstance(value, dict) and "file" in value:
                assert (TEMPLATES_ROOT / value["file"]).exists(), (
                    f"Registry key '{key}' → '{value['file']}' not found"
                )
            elif isinstance(value, list):
                for item in value:
                    f = item if isinstance(item, str) else item.get("file")
                    if f:
                        assert (TEMPLATES_ROOT / f).exists(), (
                            f"Registry key '{key}' → '{f}' not found"
                        )

    def test_section_references_resolve(self, registry, context_module):
        """Section references in the registry should find actual content."""
        for key, value in registry.items():
            if key.startswith("_"):
                continue
            if isinstance(value, dict) and "section" in value:
                file_path = TEMPLATES_ROOT / value["file"]
                result = context_module.extract_section(file_path, value["section"])
                assert result != "Section not found.", (
                    f"Registry '{key}' section '{value['section']}' not found in {value['file']}"
                )

    def test_uv_commands_use_uv_run(self):
        """All .md files under templates/ should use `uv run` syntax, not bare `uv <script>`."""
        # Pattern: `uv scripts/` or `uv context.py` etc. without `run` after uv
        # We look for `uv ` followed by a path-like arg that's NOT a known uv subcommand
        uv_subcommands = {
            "run", "init", "add", "remove", "sync", "lock", "pip", "venv",
            "build", "publish", "tool", "python", "cache", "self", "version",
            "help", "--help", "-V", "--version",
        }
        violations = []
        for md_file in TEMPLATES_ROOT.rglob("*.md"):
            content = md_file.read_text(encoding="utf-8")
            in_code_block = False
            for i, line in enumerate(content.splitlines(), 1):
                stripped = line.strip()
                if stripped.startswith("```"):
                    in_code_block = not in_code_block
                # Only check inside code blocks (that's where commands live)
                # Also check plain lines that look like commands
                for match in re.finditer(r'\buv\s+(\S+)', line):
                    first_arg = match.group(1)
                    if first_arg not in uv_subcommands and not first_arg.startswith("-"):
                        violations.append(
                            f"{md_file.relative_to(TEMPLATES_ROOT)}:{i}: `uv {first_arg}`"
                        )
        assert not violations, (
            "Found bare `uv <script>` commands (should be `uv run <script>`):\n"
            + "\n".join(violations)
        )

    def test_progress_template_is_generic(self):
        """PROGRESS.md template must not contain project-specific content."""
        content = (TEMPLATES_ROOT / "docs" / "PROGRESS.md").read_text(encoding="utf-8")
        project_specific_terms = ["Seed Bank", "ai-protocol", "AADP", "bootstrap.py"]
        for term in project_specific_terms:
            assert term not in content, (
                f"PROGRESS.md template contains project-specific term: '{term}'"
            )

    def test_all_expected_template_files_exist(self):
        """All 10 expected template files should exist."""
        for rel in EXPECTED_TEMPLATE_FILES:
            assert (TEMPLATES_ROOT / rel).exists(), f"Missing template: {rel}"

    def test_meta_protocol_version_matches_version_file(self, registry):
        """_meta.protocol_version should match the VERSION file."""
        version_file = REPO_ROOT / "VERSION"
        assert version_file.exists(), "VERSION file not found"
        file_version = version_file.read_text().strip()
        meta_version = registry.get("_meta", {}).get("protocol_version")
        assert meta_version == file_version, (
            f"Version mismatch: VERSION={file_version}, "
            f"_meta.protocol_version={meta_version}"
        )
