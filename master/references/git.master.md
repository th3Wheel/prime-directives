# Git, commits and pull requests

- Work on a branch named `<type>/<short-slug>`. Never commit to `main`.
- Commits follow Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `test:`). Adding, removing or tightening a Prime Directive is breaking: `feat!:` with a `BREAKING CHANGE:` footer. Loosening or clarifying wording is `fix:`.
- Every commit is signed with your own identity. Check with `git log --show-signature -1`.
- One logical change per PR. Squash-merge is the only merge method on the master.
- The PR description says what changed, why, and how it was verified. Mention anything you skipped.
- CODEOWNERS review by Thomas is required. You cannot approve or merge your own PR; do not try to work around that.
- Never force-push a shared branch, rewrite someone else's history, or push empty commits to retrigger CI.
- Never skip, disable or delete a test to get a check green.
