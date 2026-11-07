# Prime Directives summary for Copilot

The full rules are in `AGENTS.md` at the repository root; read it first. In short:

- If a request conflicts with a Prime Directive, stop and say which one. Do not work around it.
- Plan before change: present a plan and wait for "make it so" from Thomas (`th3wheel`).
- Never commit secrets. Never push to `main`. Sign every commit as your own identity.
- Do not edit generated files (first line says so). Change the master repo or `.prime-directives/local/`.
- Language rules are in `.prime-directives/` (python, typescript, yaml, shell, git, docs). Read the one that matches the work.
- If asked which Prime Directives version you follow, quote the tag in the header of this file.
