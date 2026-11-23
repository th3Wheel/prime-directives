# PR review rubric

There is one checklist and one place it lives: [`.github/PULL_REQUEST_TEMPLATE.md`](PULL_REQUEST_TEMPLATE.md) on `main`. Manual PRs use it as is, agent PR bodies are rendered from it (`scripts/render-agent-pr-body.sh`), and the AI reviewer fills out the same items (`scripts/render-review-checklist.sh`). Only the guidance for how to judge each item lives in the prompt in [`workflows/ai-review.yml`](workflows/ai-review.yml).

- **Who applies it:** an AI reviewer (Claude Code Action, read-only) fills out the checklist as one PR comment before the human review. It never approves. Merge Decision, Human Oversight and Reviewer Sign-Off are the human's alone.
- **Why agents cannot change it:** the workflows, scripts and template are protected by CODEOWNERS, and both the PR body and the review read them from `main`, never from the PR under review.
- **To change the checklist:** edit the template through a PR the code owner approves. To change how items are judged, edit the prompt in `ai-review.yml`. If you rename or remove a section the scripts rely on, they fail loudly instead of quietly changing what is reviewed.
- **Other repos:** call `uses: th3Wheel/prime-directives/.github/workflows/ai-review.yml@main`. Grant `contents: read`, `pull-requests: write`, `issues: write`, `checks: read`, `actions: read` and `id-token: write`. The reviewer reads the template from `th3Wheel/prime-directives@main`. While that repo is private and the caller is another repo, the default token cannot read it: pass a token that can as the optional `rubric_token` secret, or make the repo public. While the host repo is private, also set Settings, Actions, General, Access to "Accessible from repositories owned by th3Wheel".

## Production Risk Assessment for agent PRs

Agents cannot edit the generated PR body, so they supply the assessment in the head commit message. The format is in [`.prime-directives/local/agent-pr-flow.md`](../.prime-directives/local/agent-pr-flow.md).
