# Agent PR flow

Project rules for agents that change this repo. Workflows on `main` enforce most of this, and you cannot change them. Read this before you push.

## Branch and PR

- Push your work to a branch named `agent/<type>-<slug>`, for example `agent/feat-ci-uv`. Stacked branches (gh stack) each get their own PR, based on the closest other `agent/**` branch.
- Do not open the PR, edit its body or labels, mark it ready, approve it or merge it. A workflow opens a draft PR on every push from the template on `main`, then the AI reviewer runs. The PR becomes ready only on a clean review verdict. Thomas (`th3Wheel`) approves and merges.
- The PR body is generated. Everything in it that comes from you comes from your head commit message, so the head commit message must carry the whole description.

## Head commit message

Only the head (newest) commit of the branch is quoted, so put the full description there, not in earlier commits.

```text
feat: add uv-based CI

What changed and why, covering every change in the diff. Name the ticket or issue
number and any references. Say how you verified it and what you skipped.

Production risk:
Failure mode 1
  Scenario: <how it fails after deploy>
  Impact: <who or what breaks>
  Detection: <observable signal: alert, log line, metric, failing check>
  Mitigation: <actionable step; how to recover or roll back>
Failure mode 2
  ...
Failure mode 3
  ...

Agent-Session: <your session id or link>
```

- The subject is a Conventional Commit, 72 characters or fewer.
- `Production risk:` comes after the description and runs to the trailers. Give at least three failure modes specific to this change, each with Scenario, Impact, Detection and Mitigation. Detection is required and must name something observable, not "we would notice".
- Keep the `Agent-Session:` trailer. Without it the PR table says the session is missing.
- The workflow shows about 30 lines of description and 60 lines of risk, as plain printable ASCII. Backticks and tildes are removed. Be brief.

## What the AI reviewer checks

The checklist is the one in `.github/PULL_REQUEST_TEMPLATE.md` on `main`. In practice:

- The description covers every change in the diff, with no hidden changes. One concern per PR.
- CI is green on the head commit. Linters, formatters and type checks pass with no new warnings.
- New dependencies are justified and pinned. GitHub Actions are pinned to a full commit SHA, and recorded in the lockfile once one exists.
- Changes to workflows, rulesets, CODEOWNERS or permissions are called out in the description.
- The Production risk section is complete (see above).
- Every review comment, including Copilot overview-only notes, is fixed or answered. Thomas will not approve a PR with unaddressed items.

If the verdict is "Needs fixes", read the reviewer's comment, push the fix to the same branch (a new head commit gets a new review) and put the updated description in that new head commit message. Watch the PR so you see reviews and CI results.

## Never

- Tick Human Oversight, Reviewer Sign-Off or Merge Decision. Those boxes are Thomas's.
- Edit `.github/workflows/`, `.github/scripts/`, `.github/PULL_REQUEST_TEMPLATE.md` or `.github/CODEOWNERS` without saying so up front in the description. Agents cannot push workflow files; if a workflow must change, say so and ask Thomas.
- Add a bot or an agent to CODEOWNERS, or set an `ANTHROPIC_API_KEY` secret (a static key overrides the federated login).
