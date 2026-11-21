"""initialize / render / load / scan / self, on top of render and lock."""

from __future__ import annotations

import difflib
import json
import shutil
from collections.abc import Iterator
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Protocol

from .lock import LOCK_PATH, Lock, LockedFile, LockError, read_lock, sha256, write_lock
from .render import (
    AGENTS_BUDGET,
    Rendered,
    RenderError,
    is_generated,
    managed_settings_match,
    managed_text,
    render_release,
)
from .source import Release, parse_version

LOCAL_DIR = Path(".prime-directives") / "local"
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", ".prime-directives"}
ROGUE_NAMES = {"CLAUDE.local.md", ".cursorrules", ".windsurfrules"}
STUB = "@AGENTS.md"


class DeployError(Exception):
    """An operation was refused (not an unexpected failure)."""


class Source(Protocol):
    def fetch(self, tag: str | None) -> object: ...


@dataclass
class ScanResult:
    problems: list[str] = field(default_factory=list)
    unverified: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.problems and not self.unverified


def _now() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def _existing(root: Path, rel: str) -> str | None:
    path = root / rel
    return path.read_text() if path.is_file() else None


def _render(root: Path, release: Release, repo: str, profile: str) -> list[Rendered]:
    try:
        return render_release(
            release.root / "master",
            release.tag,
            repo,
            profile=profile,
            existing_settings=_existing(root, ".vscode/settings.json"),
        )
    except RenderError as exc:
        raise DeployError(str(exc)) from exc


def _protect_existing(
    root: Path, files: list[Rendered], confirm: bool, managed: set[str]
) -> list[tuple[Path, Path]]:
    """Plan moves of hand-written AGENTS.md/CLAUDE.md into local/. Refuse without confirm."""
    moves: list[tuple[Path, Path]] = []
    for item in files:
        if item.target not in (
            "AGENTS.md",
            "CLAUDE.md",
            "GEMINI.md",
            ".github/copilot-instructions.md",
        ):
            continue
        current = _existing(root, item.target)
        if current is None or is_generated(current) or item.target in managed:
            continue  # ours already (or tracked by the lock): safe to overwrite
        dest = root / LOCAL_DIR / Path(item.target).name
        if dest.exists():
            raise DeployError(
                f"{item.target} is hand-written and {dest} already exists; resolve by hand"
            )
        moves.append((root / item.target, dest))
    if moves and not confirm:
        names = ", ".join(str(src.relative_to(root)) for src, _ in moves)
        raise DeployError(
            f"{names} exist without a Prime Directives header; they would move into "
            f"{LOCAL_DIR}/. Re-run with --yes to confirm."
        )
    return moves


def apply(
    root: Path, release: Release, repo: str, *, profile: str = "project", confirm: bool = False
) -> tuple[Lock, dict[str, tuple[str, str]]]:
    """Render and write. Returns the new lock and {target: (old, new)} for the diff."""
    files = _render(root, release, repo, profile)
    try:
        managed = {f.target for f in read_lock(root).files}
    except LockError:
        managed = set()
    moves = _protect_existing(root, files, confirm, managed)
    changes: dict[str, tuple[str, str]] = {}
    for src, dest in moves:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(src, dest)
    for item in files:
        path = root / item.target
        old = path.read_text() if path.is_file() else ""
        if old != item.content:
            changes[item.target] = (old, item.content)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(item.content)
    (root / LOCAL_DIR).mkdir(parents=True, exist_ok=True)
    keep = root / LOCAL_DIR / ".gitkeep"
    if not any((root / LOCAL_DIR).iterdir()):
        keep.touch()
    lock = Lock(
        repo=repo,
        tag=release.tag,
        commit=release.commit,
        rendered_at=_now(),
        profile=profile,
        files=[f.locked() for f in files],
    )
    write_lock(root, lock)
    return lock, changes


def format_diff(changes: dict[str, tuple[str, str]]) -> str:
    chunks = []
    for target, (old, new) in sorted(changes.items()):
        chunks.extend(
            difflib.unified_diff(
                old.splitlines(keepends=True),
                new.splitlines(keepends=True),
                fromfile=f"a/{target}",
                tofile=f"b/{target}",
            )
        )
    return "".join(chunks)


def initialize(root: Path, source, repo: str, tag: str | None, confirm: bool) -> tuple[Lock, str]:
    if (root / LOCK_PATH).exists():
        raise DeployError("already initialized; use `load` to change the pinned version")
    with source.fetch(tag) as release:
        lock, changes = apply(root, release, repo, confirm=confirm)
    _must_pass(root, source, lock)
    return lock, format_diff(changes)


def render(root: Path, source) -> tuple[Lock, str]:
    lock = _read(root)
    with source.fetch(lock.tag) as release:
        _check_commit(lock, release)
        new, changes = apply(root, release, lock.repo, profile=lock.profile, confirm=False)
    _must_pass(root, source, new)
    return new, format_diff(changes)


def load(root: Path, source, tag: str | None, confirm: bool) -> tuple[Lock, str]:
    lock = _read(root)
    with source.fetch(tag) as release:
        new, changes = apply(root, release, lock.repo, profile=lock.profile, confirm=confirm)
    _must_pass(root, source, new)
    return new, format_diff(changes)


def self_render(root: Path, source, repo: str, tag: str | None) -> tuple[Lock, str]:
    """Master repo only: render the root from a pinned tag and add the guard section."""
    if not (root / "master" / "AGENTS.master.md").is_file():
        raise DeployError("`self` runs in the master repo (no master/AGENTS.master.md here)")
    with source.fetch(tag) as release:
        lock, changes = apply(root, release, repo, profile="master", confirm=True)
    _must_pass(root, source, lock)
    return lock, format_diff(changes)


def _read(root: Path) -> Lock:
    try:
        return read_lock(root)
    except LockError as exc:
        raise DeployError(str(exc)) from exc


def _check_commit(lock: Lock, release: Release) -> None:
    if set(release.commit) != {"0"} and release.commit != lock.commit:
        raise DeployError(
            f"{lock.tag} now resolves to {release.commit[:7]} but the lock pins {lock.commit[:7]}; "
            "a published tag must never move. Refusing."
        )


def _must_pass(root: Path, source, lock: Lock) -> None:
    result = scan(root, source, min_version=None)
    if not result.ok:
        raise DeployError(
            "post-render scan failed:\n  " + "\n  ".join(result.problems + result.unverified)
        )


def _walk(root: Path) -> Iterator[Path]:
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if any(part in SKIP_DIRS for part in rel.parts[:-1]) or (
            path.is_dir() and path.name in SKIP_DIRS
        ):
            continue
        if path.is_file():
            yield path


def scan(root: Path, source, min_version: str | None) -> ScanResult:
    result = ScanResult()
    try:
        lock = read_lock(root)
    except Exception as exc:  # noqa: BLE001 - any lock failure is a scan failure
        result.problems.append(str(exc))
        return result

    if min_version and parse_version(lock.tag) < parse_version(min_version):
        result.problems.append(f"pinned {lock.tag} is older than the minimum {min_version}")

    locked = {f.target: f for f in lock.files}
    _check_lock_files(root, locked, result)
    _check_rogue(root, locked, result)

    # Tamper-proof check: re-render from the release rather than trusting lock.json alone.
    try:
        with source.fetch(lock.tag) as release:
            _check_commit(lock, release)
            expected = _render(root, release, lock.repo, lock.profile)
        for item in expected:
            if item.target not in locked or locked[item.target].sha256 != item.locked().sha256:
                result.problems.append(f"{item.target}: lock does not match the release {lock.tag}")
            current = _existing(root, item.target)
            if current is None:
                continue  # already reported by the lock check
            if item.managed is not None:
                if not managed_settings_match(current, item.managed):
                    result.problems.append(f"{item.target}: managed keys differ from {lock.tag}")
            elif current != item.content:
                result.problems.append(f"{item.target}: differs from the {lock.tag} render")
    except Exception as exc:  # noqa: BLE001 - fail closed: never report "passed" unverified
        result.unverified.append(
            f"could not re-render from {lock.tag} ({exc}); results are unverified"
        )
    return result


def _check_lock_files(root: Path, locked: dict[str, LockedFile], result: ScanResult) -> None:
    for target, entry in locked.items():
        current = _existing(root, target)
        if current is None:
            result.problems.append(f"{target}: listed in the lock but missing")
            continue
        if entry.kind == "json-merge":
            try:
                data = json.loads(current)
                managed = {k: data[k] for k in entry.keys}
            except (json.JSONDecodeError, KeyError, TypeError):
                result.problems.append(f"{target}: managed keys missing or file is not JSON")
                continue
            digest = sha256(managed_text(managed))
        else:
            digest = sha256(current)
            if target == "AGENTS.md" and len(current.encode()) > AGENTS_BUDGET:
                result.problems.append(f"AGENTS.md is over the {AGENTS_BUDGET} byte budget")
        if digest != entry.sha256:
            result.problems.append(f"{target}: checksum differs from the lock (edited by hand?)")


def _check_rogue(root: Path, locked: dict[str, LockedFile], result: ScanResult) -> None:
    for path in _walk(root):
        rel = path.relative_to(root)
        key = rel.as_posix()
        if key in locked:
            continue
        if path.name in ROGUE_NAMES or (rel.parts[0] == ".cursor" and len(rel.parts) > 1):
            result.problems.append(f"{key}: unmanaged instruction file")
        elif path.name == "CLAUDE.md":
            if path.read_text().strip() != STUB and not is_generated(path.read_text()):
                result.problems.append(f"{key}: nested CLAUDE.md must be the `{STUB}` stub")
            if not (path.parent / "AGENTS.md").is_file():
                result.problems.append(f"{key}: stub has no sibling AGENTS.md")
        elif path.name == "AGENTS.md":
            stub = path.parent / "CLAUDE.md"
            if not stub.is_file():
                result.problems.append(f"{key}: no CLAUDE.md stub next to it")
            elif stub.read_text().strip() != STUB:
                result.problems.append(f"{key}: sibling CLAUDE.md is not the `{STUB}` stub")
