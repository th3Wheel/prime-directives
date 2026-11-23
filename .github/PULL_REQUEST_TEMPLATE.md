## Summary

<!-- What changed and why, in a few lines. Include the ticket or issue number and any references, and cover every change in the diff. -->

## Verification

<!-- Commands run or checks relied on, and results. -->

## Rollback

<!-- How to undo this. Reverting the squash commit is usually enough; add migration or data notes if not. -->

## Production Risk

> Required for all pull requests. Mandatory for agent-created PRs.

Document at least three realistic production failure modes introduced or affected by this change. Detection is required for every failure mode: name the observable signal (alert, log line, metric, failing check) that would show it, because fast detection sets time-to-recovery.

### Failure Mode 1

**Scenario**

**Impact**

**Detection** (required)

**Mitigation**

### Failure Mode 2

**Scenario**

**Impact**

**Detection** (required)

**Mitigation**

### Failure Mode 3

**Scenario**

**Impact**

**Detection** (required)

**Mitigation**

<details>
<summary>Agent metadata (complete if an AI agent created or modified this PR)</summary>

**Author Type**

- [ ] Human-authored
- [ ] AI-assisted
- [ ] Agent-generated

| Field | Value |
|---------|---------|
| Agent Name | |
| Model | |
| Workflow | |
| Run ID | |
| Task Source | |
| Issue / Ticket | |

</details>

<!-- part:reviewer
Everything from here to the next part marker is NOT in the PR body. The AI reviewer fills it out in its own
comment, updated in place on every run (see .github/review-rubric.md). -->

## AI review checklist

### Functionality
- [ ] Meets requirements
- [ ] Handles expected edge cases
- [ ] No obvious bugs introduced
- [ ] One concern per PR, with no unrelated changes

### Code Quality
- [ ] Code is readable and maintainable
- [ ] Naming is clear and consistent
- [ ] No unnecessary complexity or duplication
- [ ] Linters, formatters and type checks pass with no new warnings

### Testing
- [ ] Relevant tests added or updated
- [ ] All tests pass
- [ ] Changes verified manually if needed
- [ ] CI is green on the current head commit

### Security & Performance
- [ ] No secrets, credentials, or sensitive data committed
- [ ] Input validation and error handling reviewed
- [ ] No significant performance regressions
- [ ] No changes to workflows, rulesets, CODEOWNERS or permissions that aren't called out
- [ ] New dependencies are justified, pinned, in the lockfile, and under acceptable licenses

### Documentation
- [ ] PR description clearly explains the change
- [ ] PR description has all required information (ticket or issue number, references) and covers every change in the diff, with no hidden changes
- [ ] Documentation/comments updated if needed
- [ ] Breaking changes are identified
- [ ] How to roll back is clear, with migration notes if needed

### Production Risk Assessment
- [ ] At least three credible failure modes documented.
- [ ] Every failure mode contains a Detection section.
- [ ] Detection methods reference observable signals.
- [ ] Failure modes are specific to this change.
- [ ] Mitigations are actionable.
- [ ] Recovery or rollback strategy exists.

### Review Items
- [ ] Every review comment, including Copilot overview-only notes, is fixed or answered

### Reproducibility
- [ ] If another AI agent inherited this repository tomorrow with no additional context, it would make the same decision and produce the same outcome

<!-- part:human
Everything from here on is posted once as its own comment when the PR opens, for the code owner to tick. It is
never overwritten on later runs. -->

## Human review checklist

### Human Oversight

- [ ] Human reviewed implementation.
- [ ] Human reviewed tests.
- [ ] Human reviewed production risks.
- [ ] Human authorized merge readiness.

### Reviewer Sign-Off

- [ ] Functionality reviewed.
- [ ] Testing reviewed.
- [ ] Security reviewed.
- [ ] Production risks reviewed.
- [ ] Safe to merge.

### Merge Decision

- [ ] ✅ Approve
- [ ] 🔄 Approve with comments
- [ ] ❌ Request changes
