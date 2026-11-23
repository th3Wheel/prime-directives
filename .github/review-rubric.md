# PR review rubric

The rubric lives in exactly one place: the prompt in [`.github/workflows/ai-review.yml`](workflows/ai-review.yml). That is the standard every PR is reviewed against. It is not duplicated here, so it cannot drift.

- **Who applies it:** an AI reviewer (Claude Code Action, read-only) fills out the Pull Request Review Checklist as one PR comment before the human review. It never approves. Merge Decision is the human's alone.
- **Why agents cannot change it:** workflow files are protected by CODEOWNERS, and the reviewer runs the workflow's own copy, so an agent cannot edit the standard it is judged by.
- **To change the rubric:** edit the prompt in `ai-review.yml` through a PR that the code owner approves.
- **Other repos:** call the reusable workflow with `uses: th3Wheel/prime-directives/.github/workflows/ai-review.yml@main`. Grant `contents: read`, `pull-requests: write`, `issues: write`, `checks: read`, `actions: read` and `id-token: write`. While the host repo is private, set Settings, Actions, General, Access to "Accessible from repositories owned by th3Wheel". No rubric file, variables or secrets are needed in the caller.

## Production Risk Assessment for agent PRs

Agents cannot edit the PR body that `open-agent-pr.yml` generates, so they supply the assessment in the head commit message. Put a line `Production risk:` after the description, then at least three failure modes, each with Scenario, Impact, Detection and Mitigation:

```
Production risk:
Failure mode 1
  Scenario: ...
  Impact: ...
  Detection: <observable signal: alert, log line, metric, failing check>
  Mitigation: ...
Failure mode 2
  ...
```

The workflow quotes the section (sanitized, length-capped) into the PR body, and the AI reviewer checks the six author confirmations against it and the diff. A missing section leaves them unticked, so the PR stays a draft. Keep the `Agent-Session:` trailer after the section; trailer lines are not treated as part of it.
