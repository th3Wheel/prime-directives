# PR review rubric

There is one checklist source and one place it lives: [`.github/PULL_REQUEST_TEMPLATE.md`](PULL_REQUEST_TEMPLATE.md) on `main`. It has three parts, split by `<!-- part:... -->` markers:

- **The body** (everything before the first marker): Summary, Verification, Rollback, Production Risk and a collapsed Agent metadata block. Agent PR bodies are rendered from it by `scripts/render-agent-pr-body.sh`.
- **The AI review checklist** (`part:reviewer`): the AI reviewer fills it out in one comment that it updates in place on every run (`scripts/render-review-checklist.sh`). Only the guidance for how to judge each item lives in the prompt in [`workflows/ai-review.yml`](workflows/ai-review.yml).
- **The human review checklist** (`part:human`): Human Oversight, Reviewer Sign-Off and Merge Decision. It is posted once as its own comment when the PR opens, so the code owner can tick it, and is never overwritten (`scripts/render-human-checklist.sh`).

- **Who applies it:** an AI reviewer (Claude Code Action, read-only) fills out its checklist before the human review. It never approves and never touches the human checklist.
- **Why agents cannot change it:** the workflows, scripts and template are protected by CODEOWNERS, and the body and both comments are built from `main`, never from the PR under review. The workflow token posts the comments, and the App has no pull request or issues permission, so agents cannot edit them.
- **To change a checklist:** edit the template through a PR the code owner approves. To change how items are judged, edit the prompt in `ai-review.yml`. If you rename or remove a section or marker the scripts rely on, they fail loudly instead of quietly changing what is reviewed.
- **Gate guard:** a PR that touches the review gate (workflows, scripts, template, rubric doc, CODEOWNERS, dependabot.yml) gets no AI review and stays a draft, so an agent cannot get its own change to the gate passed by the reviewer it changes. It covers what an agent can push (the App cannot push `.github/workflows/`). It does not cover a human pusher, changes to the agent instruction files, or the fact that the `ai-review.yml` that runs is the one on the pushed commit. The full fix (run the reviewer from `main`) is tabled in a follow-up issue.
- **Manual PRs** get the whole template as their body, markers included. The reviewer and human checklists are posted as comments only for agent PRs.
- **Other repos:** call `uses: th3Wheel/prime-directives/.github/workflows/ai-review.yml@main`. Grant `contents: read`, `pull-requests: write`, `issues: write`, `checks: read`, `actions: read` and `id-token: write`. The reviewer reads the template from `th3Wheel/prime-directives@main`. While that repo is private and the caller is another repo, the default token cannot read it: pass a token that can as the optional `rubric_token` secret, or make the repo public. While the host repo is private, also set Settings, Actions, General, Access to "Accessible from repositories owned by th3Wheel".

## Production Risk Assessment for agent PRs

Agents cannot edit the generated PR body, so they supply the assessment in the head commit message. The format is in [`.prime-directives/local/agent-pr-flow.md`](../.prime-directives/local/agent-pr-flow.md).
