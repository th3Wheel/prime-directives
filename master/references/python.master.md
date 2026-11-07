# Python

- Target the Python version in `pyproject.toml`. Use `uv` for environments and dependencies; commit `uv.lock`.
- Lint and format with Ruff (`ruff check`, `ruff format`). Type check with ty. Both must pass clean before you commit.
- Type-annotate all public functions. Prefer `pathlib` over `os.path`, dataclasses or Pydantic over loose dicts, and f-strings over `%` or `.format`.
- Source layout: `src/<package>/`; tests in `tests/` with pytest. A bug fix comes with a test that failed before the fix.
- No bare `except:`. Catch the narrowest exception, and never swallow one silently.
- No mutable default arguments. No wildcard imports. No `print` in library code; use `logging`.
- Pin dependencies through the lock file; add a new dependency only when the standard library will not do.
