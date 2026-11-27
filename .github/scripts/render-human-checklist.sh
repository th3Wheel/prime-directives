#!/usr/bin/env bash
# Prints the checklist for the human reviewer, taken from the PR template (the single source): the part after the
# "<!-- part:human" marker. The workflow posts it once as its own comment when the PR opens, so the code owner can tick
# it there. It keeps the "##"/"###" headings and the checklist items; prose and comments are not copied.
# Exits non-zero if the marker or a section is missing or has no items.
#
# Required env: TEMPLATE (path to the template file)
set -euo pipefail
[[ -n "${TEMPLATE:-}" ]] && [[ -f "$TEMPLATE" ]] || { echo "render-human-checklist: TEMPLATE is not set or not a file" >&2; exit 2; }

awk '
/^<!-- part:/ { in_part = ($0 ~ /^<!-- part:human/); if (in_part) found = 1; next }
!in_part { next }
/^## / { print $0; next }
/^### / { sec = $0; seen[sec] = 1; print "\n" $0; next }
/^- \[[ xX]\] / { print; count[sec]++ }
END {
  if (!found) { print "render-human-checklist: part marker not found: part:human" > "/dev/stderr"; exit 1 }
  n = split("### Human Oversight|### Reviewer Sign-Off|### Merge Decision", need, "|")
  for (i = 1; i <= n; i++) if (!(need[i] in seen) || count[need[i]] == 0) { print "render-human-checklist: missing section or items: " need[i] > "/dev/stderr"; bad = 1 }
  if (bad) exit 1
}
' "$TEMPLATE"
