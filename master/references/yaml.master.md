# YAML

- Two-space indent, no tabs. Lint with yamllint using the shared config.
- Quote strings that could be read as another type (`"yes"`, `"1.10"`, `"on"`).
- Keep keys in a stable, meaningful order. Comment the why, not the what.
- Never put secrets in YAML. Reference them by name from the secret store.
- GitHub Actions: pin third-party actions to a full commit SHA and keep `permissions:` minimal.
