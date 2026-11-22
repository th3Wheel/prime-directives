"""Lock file: what was rendered, from which release, with which checksums."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

from . import __version__

SCHEMA_VERSION = 1
LOCK_PATH = Path(".prime-directives") / "lock.json"


class LockError(Exception):
    """The lock file is missing, unreadable, or from an unsupported schema."""


@dataclass
class LockedFile:
    target: str
    source: str
    sha256: str
    kind: str = "file"  # "file" or "json-merge" (checksum covers managed keys only)
    keys: list[str] = field(default_factory=list)  # managed keys of a json-merge file


@dataclass
class Lock:
    repo: str
    tag: str
    commit: str
    rendered_at: str
    profile: str = "project"  # "project" or "master"
    files: list[LockedFile] = field(default_factory=list)
    schema_version: int = SCHEMA_VERSION
    tool_version: str = __version__

    def to_json(self) -> str:
        data = {
            "schemaVersion": self.schema_version,
            "toolVersion": self.tool_version,
            "source": {"repo": self.repo, "url": f"https://github.com/{self.repo}"},
            "tag": self.tag,
            "commit": self.commit,
            "renderedAt": self.rendered_at,
            "profile": self.profile,
            "files": [asdict(f) for f in self.files],
        }
        return json.dumps(data, indent=2) + "\n"


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def read_lock(root: Path) -> Lock:
    path = root / LOCK_PATH
    try:
        data = json.loads(path.read_text())
    except FileNotFoundError as exc:
        raise LockError(f"no lock file at {path}; run `prime-directives initialize`") from exc
    except json.JSONDecodeError as exc:
        raise LockError(f"lock file {path} is not valid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise LockError(f"lock file {path} must contain a JSON object")
    if data.get("schemaVersion") != SCHEMA_VERSION:
        raise LockError(
            f"lock schema {data.get('schemaVersion')!r} is not supported by this tool "
            f"(expects {SCHEMA_VERSION}); run `prime-directives load` to upgrade"
        )
    try:
        lock = Lock(
            repo=data["source"]["repo"],
            tag=data["tag"],
            commit=data["commit"],
            rendered_at=data["renderedAt"],
            profile=data.get("profile", "project"),
            files=[LockedFile(**f) for f in data["files"]],
            schema_version=data["schemaVersion"],
            tool_version=data["toolVersion"],
        )
    except (KeyError, TypeError) as exc:
        raise LockError(f"lock file {path} is malformed: {exc!r}") from exc
    _validate(lock, path)
    return lock


def _validate(lock: Lock, path: Path) -> None:
    """The dataclasses do not check types, so reject malformed field values here."""
    top = {
        "source.repo": lock.repo,
        "tag": lock.tag,
        "commit": lock.commit,
        "renderedAt": lock.rendered_at,
        "profile": lock.profile,
        "toolVersion": lock.tool_version,
    }
    for name, value in top.items():
        if not isinstance(value, str):
            raise LockError(f"lock file {path} is malformed: {name} must be a string")
    if not isinstance(lock.files, list):
        raise LockError(f"lock file {path} is malformed: files must be a list")
    for entry in lock.files:
        for name in ("target", "source", "sha256", "kind"):
            if not isinstance(getattr(entry, name), str):
                raise LockError(f"lock file {path} is malformed: files[].{name} must be a string")
        if not isinstance(entry.keys, list) or not all(isinstance(k, str) for k in entry.keys):
            raise LockError(
                f"lock file {path} is malformed: files[].keys must be a list of strings"
            )


def write_lock(root: Path, lock: Lock) -> None:
    path = root / LOCK_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(lock.to_json())
