# TypeScript and JavaScript

- Prefer TypeScript. Enable `strict`; do not use `any` without a comment saying why.
- Lint with ESLint (shared config from the master) and format with Prettier. Both must pass before you commit.
- Use `const` by default, ES modules, and `async`/`await` over raw promise chains.
- Validate data at boundaries (network, files, user input); do not trust casts.
- Tests live beside the code or in `tests/`; a bug fix comes with a test that failed before the fix.
- Pin dependencies with the lock file. Add a dependency only when it earns its weight.
