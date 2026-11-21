"""Where a release comes from: GitHub tarball (verified against its commit SHA) or a local dir."""

from __future__ import annotations

import io
import json
import re
import shutil
import tarfile
import tempfile
import time
import urllib.error
import urllib.request
from collections.abc import Callable
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

DEFAULT_REPO = "th3Wheel/prime-directives"
USER_AGENT = "prime-directives-deploy"


class SourceError(Exception):
    """A release could not be fetched or verified."""


@dataclass
class Release:
    tag: str
    commit: str
    root: Path  # directory that contains master/


def parse_version(tag: str) -> tuple[int, ...]:
    match = re.fullmatch(r"v?(\d+(?:\.\d+)*)", tag)
    if not match:
        raise SourceError(f"{tag!r} is not a version tag like v1.3 or v0.1.0")
    return tuple(int(p) for p in match.group(1).split("."))


def _retry[T](fn: Callable[[], T], attempts: int = 4) -> T:
    delay = 1.0
    for attempt in range(attempts):
        try:
            return fn()
        except (urllib.error.URLError, TimeoutError) as exc:
            if attempt == attempts - 1:
                raise SourceError(f"download failed after {attempts} attempts: {exc}") from exc
            time.sleep(delay)
            delay *= 2
    raise AssertionError("unreachable")


def _get(url: str) -> bytes:
    if not url.startswith("https://"):
        raise SourceError(f"refusing non-https url {url}")
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})  # noqa: S310

    def fetch() -> bytes:
        with urllib.request.urlopen(req, timeout=30) as resp:  # noqa: S310
            return resp.read()

    return _retry(fetch)


class GitHubSource:
    def __init__(self, repo: str = DEFAULT_REPO) -> None:
        self.repo = repo

    def latest_tag(self) -> str:
        data = json.loads(_get(f"https://api.github.com/repos/{self.repo}/releases/latest"))
        return str(data["tag_name"])

    def commit_for(self, tag: str) -> str:
        data = json.loads(_get(f"https://api.github.com/repos/{self.repo}/commits/{tag}"))
        return str(data["sha"])

    @contextmanager
    def fetch(self, tag: str | None):
        tag = tag or self.latest_tag()
        parse_version(tag)
        commit = self.commit_for(tag)
        blob = _get(f"https://github.com/{self.repo}/archive/refs/tags/{tag}.tar.gz")
        tmp = Path(tempfile.mkdtemp(prefix="prime-directives-"))
        try:
            with tarfile.open(fileobj=io.BytesIO(blob), mode="r:gz") as tar:
                # GitHub stamps the commit SHA into the archive's pax header.
                stamped = tar.pax_headers.get("comment", "")
                if stamped != commit:
                    raise SourceError(
                        f"tarball commit {stamped[:7] or 'unknown'} does not match "
                        f"{commit[:7]} for {tag}"
                    )
                tar.extractall(tmp, filter="data")
            tops = [p for p in tmp.iterdir() if p.is_dir()]
            if len(tops) != 1:
                raise SourceError("unexpected tarball layout")
            yield Release(tag=tag, commit=commit, root=tops[0])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class LocalSource:
    """A local checkout standing in for a release (tests, offline work)."""

    def __init__(self, path: Path, tag: str | None = None) -> None:
        self.path = path
        self._tag = tag

    @contextmanager
    def fetch(self, tag: str | None):
        tag = tag or self._tag or "v0.0.0-local"
        yield Release(tag=tag, commit="0" * 40, root=self.path)
