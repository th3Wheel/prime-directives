#!/usr/bin/env bash
# Prints the checklist the AI reviewer fills out, taken from the PR template (the single source): the part after the
# "<!-- part:reviewer" marker and before the next marker. It keeps the "##"/"###" headings and the checklist items;
# prose and comments are not copied.
# Exits non-zero if the part marker or a section the reviewer's guidance depends on is missing or has no items, so a
# renamed or removed section fails loudly instead of silently changing what is reviewed.
#
# Required env: TEMPLATE (path to the template file)
set -euo pipefail
[[ -n "${TEMPLATE:-}" ]] && [[ -f "$TEMPLATE" ]] || { echo "render-review-checklist: TEMPLATE is not set or not a file" >&2; exit 2; }

awk '
/^<!-- part:/ { in_part = ($0 ~ /^<!-- part:reviewer/); if (in_part) found = 1; next }
!in_part { next }
/^## / { print $0; next }
/^### / { sec = $0; seen[sec] = 1; print "\n" $0; next }
/^- \[[ xX]\] / { print; count[sec]++ }
END {
  if (!found) { print "render-review-checklist: part marker not found: part:reviewer" > "/dev/stderr"; exit 1 }
  n = split("### Functionality|### Code Quality|### Testing|### Security & Performance|### Documentation|### Production Risk Assessment|### Review Items|### Reproducibility", need, "|")
  for (i = 1; i <= n; i++) if (!(need[i] in seen) || count[need[i]] == 0) { print "render-review-checklist: missing section or items: " need[i] > "/dev/stderr"; bad = 1 }
  if (bad) exit 1
}
' "$TEMPLATE"
