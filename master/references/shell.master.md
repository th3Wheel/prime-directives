# Shell

- Bash scripts start with `#!/usr/bin/env bash` and `set -euo pipefail`.
- Check with ShellCheck and format with shfmt. Both must pass before you commit.
- Quote every expansion (`"$var"`). Use `[[ ]]` for tests and `$(...)` for command substitution.
- Take paths and options as arguments; do not hard-code user-specific paths.
- Destructive commands (`rm -rf`, `git reset --hard`, force pushes) need a stated reason and, where the target is not obviously yours, confirmation first.
- Never echo secrets or put them on a command line.
