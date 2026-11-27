from __future__ import annotations

import shutil
from pathlib import Path

import pytest

MASTER_SRC = Path(__file__).resolve().parents[2] / "master"


def _make_release(path: Path) -> Path:
    master = path / "master"
    refs = master / "references"
    refs.mkdir(parents=True)
    (master / "AGENTS.master.md").write_text("# Rules\n\nFollow `.prime-directives/python.md`.\n")
    (master / "CLAUDE.master.md").write_text("@AGENTS.md\n")
    (master / "GEMINI.master.md").write_text("@./AGENTS.md\n")
    (master / "copilot-instructions.master.md").write_text("# Summary\n")
    (master / "settings.master.json").write_text(
        '{"chat.useAgentsMdFile": true, "chat.useNestedAgentsMdFiles": true}\n'
    )
    (refs / "python.master.md").write_text("# Python\n")
    return path


@pytest.fixture
def release(tmp_path: Path) -> Path:
    return _make_release(tmp_path / "release")


@pytest.fixture
def target(tmp_path: Path) -> Path:
    path = tmp_path / "project"
    path.mkdir()
    return path


@pytest.fixture
def real_master(tmp_path: Path) -> Path | None:
    """The repo's real master/ folder, when running inside the full repo."""
    if not MASTER_SRC.is_dir():
        return None
    root = tmp_path / "real-release"
    shutil.copytree(MASTER_SRC, root / "master")
    return root
