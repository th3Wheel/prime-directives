## Summary

<!-- What changed and why, in a few lines. Include the ticket or issue number and any references, and cover every change in the diff. -->

## Verification

<!-- Commands run or checks relied on, and results. -->

## Rollback

<!-- How to undo this. Reverting the squash commit is usually enough; add migration or data notes if not. -->

## Pull Request Review Checklist

<!-- An AI reviewer fills out the sections below Human Oversight in a comment before human review. See .github/review-rubric.md. -->

### Agent Metadata

Complete if this PR was created or modified by an AI agent.

#### Author Type

- [ ] Human-authored
- [ ] AI-assisted
- [ ] Agent-generated

#### Agent Information

| Field | Value |
|---------|---------|
| Agent Name | |
| Model | |
| Workflow | |
| Run ID | |
| Task Source | |
| Issue / Ticket | |

#### Human Oversight

- [ ] Human reviewed implementation.
- [ ] Human reviewed tests.
- [ ] Human reviewed production risks.
- [ ] Human authorized merge readiness.

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

> Required for all pull requests.
>
> Mandatory for agent-created PRs.

#### How This Could Fail in Production

Document at least three realistic production failure modes introduced or affected by this change.

##### Failure Mode 1

**Scenario**

**Impact**

**Detection**

**Mitigation**

##### Failure Mode 2

**Scenario**

**Impact**

**Detection**

**Mitigation**

##### Failure Mode 3

**Scenario**

**Impact**

**Detection**

**Mitigation**

#### Author Confirmation

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

### Merge Decision
- [ ] ✅ Approve
- [ ] 🔄 Approve with comments
- [ ] ❌ Request changes
