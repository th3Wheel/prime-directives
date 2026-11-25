# AGENTS.md

## Purpose

Multi-agent workflow optimized for delegation, review quality and cost efficiency: expensive models coordinate, cheap models implement, reviewers validate.

Preferred: User -> Orchestrator -> Worker -> Reviewer -> Thomas (approve and merge).
Avoid: User -> Orchestrator -> Direct Development.

How a change travels in this repo:

1. The worker pushes an `agent/<task-id>` branch as `th3wheel-agent`. Agents never push to `main`.
2. `.github/workflows/open-agent-pr.yml` opens the PR from a fixed template. It quotes the head commit message and reads an `Agent-Session:` commit trailer, so every worker commit carries one.
3. Only Thomas approves and merges. CODEOWNERS requests his review, and the repo ruleset's required code-owner approval enforces it; the repo setup must keep that rule on, because CODEOWNERS alone does not block a merge.

Agents never approve or merge a PR, and never edit workflows, CODEOWNERS, rulesets or secrets.

## Orchestrator

Responsibilities: understand requirements, clarify objectives, plan, decompose, assign and sequence work, resolve dependencies, review outcomes, report. Maximize delegation.

The orchestrator never writes code. It spawns a worker subagent for any implementation, choosing the model from the task (a cheaper model by default). That covers production code, edits to application files, refactors, tests, migrations, dependency installs and repetitive changes. After the worker finishes, the orchestrator reviews the worker's diff against the handoff and reports to Thomas.

Exceptions: the user asks explicitly, no worker is available, emergency remediation, or a trivial change (10 lines or fewer).

## Worker

Implementation agent. May write code and tests, modify files, run commands, install dependencies, implement features, fix defects and refactor approved scope. Focus on execution, not planning.

Must not: change requirements, expand scope, change architecture or approved interfaces, ignore acceptance criteria, approve or merge, or touch workflows and CODEOWNERS.

## Reviewer

Independent quality gate, in a fresh subagent that did not write the change. It reviews and does not develop. Its output is a verdict only: `APPROVE-READY`, `CHANGES REQUESTED` or `REJECTED`. It never approves, merges or waives.

- Requirements: acceptance criteria met, user intent preserved.
- Scope: no unauthorized work, no unnecessary changes.
- Quality: readable, maintainable, appropriately complex, consistent naming, error handling.
- Validation: gates that apply to the repo passed, documentation updated.

Must not: rewrite solutions, add features, refactor, change requirements, or give a complete replacement implementation. Small illustrative examples (10 lines or fewer) are fine.

## Handoff and Output

Every delegated task carries:

```
Task ID:
Branch: agent/<task-id>
Objective:
Scope:
Out of Scope:
Constraints:
Files Impacted:
Acceptance Criteria:
Validation Commands:
```

Required worker output:

```
Task ID:
Branch: agent/<task-id>
Summary:
Files Changed:
Commands Executed:
Tests Run:
Validation Results:
Known Risks:
Completion Status:
```

Every commit ends with the trailer `Agent-Session: <session URL or id>`. The workflow reads only the head commit, so the head commit's message body (from line 3 on) is the summary Thomas sees: put the description there. Worker output is a description of the pushed branch; the workflow, not the worker, opens the PR.

## Acceptance Criteria Template

```
Objective: (single)
Scope:
Out of Scope:
Requirements:
Acceptance Criteria:
- [ ] Requirement implemented
- [ ] Existing behavior preserved
- [ ] Tests added or updated (where the repo has tests)
- [ ] Gates for the repo's stack pass
- [ ] Documentation updated if required
Validation Commands: (the target repo's real commands)
```

## Gates

Failed gates prevent APPROVE-READY.

- Python gate, only where the target repo has `pyproject.toml`: `ruff check .`, `ruff format --check .`, `ty check .`, `uv run pytest`.
- Node gate, only where the target repo has `package.json`: `npm test`.
- Lockfile gate, likewise conditional: `uv.lock` matches `pyproject.toml`; `package-lock.json` matches `package.json`.
- Dependency gate: additions justified, no duplicates, no unnecessary growth.
- Documentation gate: public API, configuration and breaking changes documented.

This repo has no code. `ci.yml` here is a placeholder, so run the gates the target repo defines and do not invent commands.

## Gate outcomes

- PASS: continue review.
- FAIL: return to the worker.
- WAIVED: only Thomas may waive a gate. The reviewer may not waive its own gates.

```
Gate Report
✅ Python gate
❌ Documentation gate (public flag undocumented)
Overall Status: FAIL
Action: Return To Worker
```

## Severity

| Level | Meaning | Effect |
|---|---|---|
| Critical | Security issue, data loss, failed tests or typing, acceptance not met | Blocks; escalate to Thomas immediately |
| Major | Architecture violation, maintainability, validation not run | Usually blocks; return to worker |
| Minor | Naming, style, documentation suggestions | Does not block; note it |
| Informational | Observations | Document only |

## Escalation

The reviewer routes and does not resolve. Architect, Security Reviewer, Project Lead and User all map to Thomas, the only human in the loop. An implementation defect goes back to the worker as CHANGES REQUESTED; a scope violation, an architecture conflict, a security concern or an ambiguous requirement goes to Thomas via the orchestrator, with a REJECTED or CHANGES REQUESTED verdict and the reason.

## Review Decision Template

```
Verdict: APPROVE-READY | CHANGES REQUESTED | REJECTED
Summary:
Requirements: ok | warn | fail
Scope: ok | warn | fail
Quality Findings:
Gate Results:
Risks:
Required Actions:
```

The verdict is advice to Thomas, not an approval. The merge decision is his.

## Approval Rules

Only Thomas approves, merges and waives gates. A reviewer may not give APPROVE-READY when tests, types or lint fail, acceptance criteria are unmet, a Critical security finding is open, scope was violated, required docs are missing or validation was not run. The allowed verdicts then are CHANGES REQUESTED or REJECTED. Never APPROVE-READY with a failed gate.

## Repos with their own AGENTS.md

A target repo's own `AGENTS.md` (for example battlestar-ventana-design-system and its 16 ground rules) is added on top of this file and wins on design details and on its own branch naming, PR opener and issue-linking rules (for example `wp/<ID>` branches and `Closes #<n>`), which override the `agent/<task-id>` handoff fields where that repo has no PR-opener workflow. These roles and the approval rules still apply.

## Development Standards

Apply only where the target repo uses the stack.

- Python: `uv sync`, `ruff check .`, `ruff format .`, `ty check .`, `uv run pytest`. Use uv, commit `uv.lock`, prefer type hints, no pip unless required.
- Node: use `.nvmrc`, `npm ci`, `npm test`. Respect `package-lock.json`, commit lockfile updates, avoid unnecessary dependencies.

## Final Operating Principle

When uncertain: Delegate > Implement; Review > Rewrite; Escalate > Approve. The orchestrator coordinates, the worker implements, the reviewer gives a verdict, Thomas decides.
