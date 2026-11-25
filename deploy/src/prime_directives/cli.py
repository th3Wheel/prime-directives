"""Command line entry point."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .engine import DeployError, initialize, load, render, scan, self_render
from .lock import LockError, read_lock
from .source import DEFAULT_REPO, GitHubSource, LocalSource, SourceError


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="prime-directives", description=__doc__)
    p.add_argument("--version", action="version", version=__version__)
    p.add_argument("--source", type=Path, help="use a local checkout instead of GitHub")
    p.add_argument("--repo", help=f"source repo (default {DEFAULT_REPO}, or the lock's repo)")
    sub = p.add_subparsers(dest="command", required=True)

    s = sub.add_parser("initialize", help="render the latest release into a target repo")
    s.add_argument("target", type=Path)
    s.add_argument("--to", dest="tag", help="start from this tag instead of the latest")
    s.add_argument("--yes", action="store_true", help="confirm moving hand-written files to local/")

    sub.add_parser("render", help="re-render from the locked tag").add_argument(
        "--path", type=Path, default=Path.cwd()
    )

    s = sub.add_parser("load", help="move the pin and re-render")
    s.add_argument("--to", dest="tag")
    s.add_argument("--path", type=Path, default=Path.cwd())
    s.add_argument("--yes", action="store_true")

    s = sub.add_parser("scan", help="verify files against the release (CI)")
    s.add_argument("--path", type=Path, default=Path.cwd())
    s.add_argument("--min-version")

    s = sub.add_parser("self", help="master repo only: render root from a pinned tag + guard")
    s.add_argument("--to", dest="tag")
    s.add_argument("--path", type=Path, default=Path.cwd())
    return p


def _source(args: argparse.Namespace, repo: str):
    if args.source:
        return LocalSource(args.source.resolve())
    return GitHubSource(repo)


def _locked_repo(args: argparse.Namespace, root: Path) -> str:
    """Existing lock decides the repo; a different --repo would mix two sources."""
    locked = read_lock(root).repo
    if args.repo and args.repo != locked:
        raise DeployError(
            f"--repo {args.repo} differs from the locked repo {locked}; "
            "a pinned repo cannot be switched here"
        )
    return locked


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    repo = args.repo or DEFAULT_REPO
    try:
        if args.command == "initialize":
            root = args.target.resolve()
            root.mkdir(parents=True, exist_ok=True)
            lock, diff = initialize(root, _source(args, repo), repo, args.tag, args.yes)
            print(f"initialized at {lock.tag}")
            diff = ""
        elif args.command in ("render", "load", "self"):
            root = args.path.resolve()
            if args.command != "self":
                repo = _locked_repo(args, root)
            if args.command == "render":
                lock, diff = render(root, _source(args, repo))
            elif args.command == "load":
                lock, diff = load(root, _source(args, repo), args.tag, args.yes)
            else:
                lock, diff = self_render(root, _source(args, repo), repo, args.tag)
            print(f"pinned at {lock.tag}")
        else:
            root = args.path.resolve()
            repo = _locked_repo(args, root)
            result = scan(root, _source(args, repo), args.min_version)
            for line in result.problems:
                print(f"FAIL: {line}")
            for line in result.unverified:
                print(f"UNVERIFIED: {line}")
            if result.problems:
                return 1
            if result.unverified:
                return 2
            print("scan passed")
            return 0
        if diff:
            print(diff, end="")
        return 0
    except (DeployError, SourceError, LockError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
