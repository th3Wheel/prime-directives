# SonarCloud

SonarCloud analyses this repo from CI (job `checks` in `.github/workflows/ci.yml`), not as Automatic Analysis. Settings live in `sonar-project.properties`.

- CI runs `pytest --cov` and writes `coverage.xml` at the repo root. SonarCloud imports it. New Python code needs tests, or coverage drops.
- Fix every SonarCloud finding in code you modified before the PR is ready, including minor code smells. A passing quality gate is not enough.
- Do not edit `sonar-project.properties`, `.github/workflows/ci.yml` or the project key without saying so in the description. Workflow changes are Thomas's to push.
- Never put `SONAR_TOKEN` in a file, a commit message or a log.
