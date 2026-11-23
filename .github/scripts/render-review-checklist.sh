#!/usr/bin/env bash
# Prints the checklist the AI reviewer fills out, taken from the PR template (the single source).
# It keeps the "###" section headings and the checklist items, and drops the sections that belong to the human
# (Agent Metadata, Reviewer Sign-Off). Prose, tables and the failure-mode skeleton are not copied.
# Exits non-zero if a section the reviewer's guidance depends on is missing or has no items, so a renamed or removed
# section fails loudly instead of silently changing what is reviewed.
#
# Required env: TEMPLATE (path to the template file)
set -euo pipefail
[ -n "${TEMPLATE:-}" ] && [ -f "$TEMPLATE" ] || { echo "render-review-checklist: TEMPLATE is not set or not a file" >&2; exit 2; }

awk '
/^## / { skip = 0 }
/^### / {
  sec = $0
  skip = ($0 ~ /^### (Agent Metadata|Reviewer Sign-Off)$/)
  if (!skip) { if (!started) { print "## Pull Request Review Checklist"; started = 1 } print "\n" $0; seen[sec] = 1 }
  next
}
!skip && /^- \[[ xX]\] / { print; count[sec]++ }
END {
  n = split("### Functionality|### Code Quality|### Testing|### Security & Performance|### Documentation|### Production Risk Assessment|### Review Items|### Reproducibility|### Merge Decision", need, "|")
  for (i = 1; i <= n; i++) if (!(need[i] in seen) || count[need[i]] == 0) { print "render-review-checklist: missing section or items: " need[i] > "/dev/stderr"; bad = 1 }
  if (bad) exit 1
}
' "$TEMPLATE"
