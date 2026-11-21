# prime-directives deploy tool

Renders the `master/` rule files of a tagged Prime Directives release into a repo, records a lock file, and checks the result.

```text
prime-directives initialize <target>   # latest release -> target, writes .prime-directives/lock.json
prime-directives render                # re-render from the locked tag (repair drift)
prime-directives load [--to vX.Y]      # move the pin (default: latest), show the diff
prime-directives scan [--min-version vX.Y]   # CI check; exit 1 = fail, 2 = unverified
prime-directives self [--to vX.Y]      # master repo only: render its root from a pinned tag + guard
```

Run without installing:

```bash
uvx --from "git+https://github.com/th3Wheel/prime-directives@v0.1.0#subdirectory=deploy" prime-directives initialize .
```

`--source PATH` uses a local checkout instead of GitHub (for tests and offline work). `--repo OWNER/NAME` overrides the source repo.

Development: `uv sync && uv run ruff check && uv run ruff format --check && uv run ty check && uv run pytest`.
