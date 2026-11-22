## Summary

<!-- What changed and why, in a few lines. Include the ticket or issue number and any references, and cover every change in the diff. -->

## Verification

<!-- Commands run or checks relied on, and results. -->

## Rollback

<!-- How to undo this. Reverting the squash commit is usually enough; add migration or data notes if not. -->

## Pull Request Review Checklist

<!-- An AI reviewer fills this out in a comment before human review. See .github/review-rubric.md. -->

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

### Review Items
- [ ] Every review comment, including Copilot overview-only notes, is fixed or answered

### Reproducibility
- [ ] If another AI agent inherited this repository tomorrow with no additional context, it would make the same decision and produce the same outcome

### Merge Decision
- [ ] ✅ Approve
- [ ] 🔄 Approve with comments
- [ ] ❌ Request changes
