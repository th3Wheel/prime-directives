#!/usr/bin/env bash
# Renders the body of an agent PR from .github/PULL_REQUEST_TEMPLATE.md, so the template is the single source.
# Only the part of the template before the first "<!-- part:" marker is the body: the reviewer checklist and the
# human checklist after it are posted as their own comments (render-review-checklist.sh, render-human-checklist.sh).
# It prepends the "Agent change" table and fills only these spots in the body:
#   - the Summary, Verification and Rollback placeholder comments
#   - Author Type (ticks "Agent-generated") and the Agent Name, Workflow and Run ID rows
#   - the failure-mode skeleton of the Production Risk section, replaced by the quoted commit-message section
# Everything else in the body passes through unchanged. If an anchor above is missing from the template
# (for example after a rename), it exits non-zero instead of silently producing a different body.
# Values come from the environment; agent-written text (SUMMARY, RISK) must already be sanitized by the caller.
#
# Required env: TEMPLATE BRANCH BASE PUSHER SHA_SHORT STAT SESSION_TXT RUN_URL RUN_ID REVIEWER
# Optional env: SUMMARY RISK
set -euo pipefail
for v in TEMPLATE BRANCH BASE PUSHER SHA_SHORT STAT SESSION_TXT RUN_URL RUN_ID REVIEWER; do
  [ -n "${!v:-}" ] || { echo "render-agent-pr-body: $v is not set" >&2; exit 2; }
done
[ -f "$TEMPLATE" ] || { echo "render-agent-pr-body: template not found: $TEMPLATE" >&2; exit 2; }
export SUMMARY="${SUMMARY:-}" RISK="${RISK:-}"

awk '
function quote(t) { return "~~~text\n" t "\n~~~" }
BEGIN {
  print "## Agent change\n"
  print "| | |"
  print "|---|---|"
  print "| Branch | `" ENVIRON["BRANCH"] "` |"
  print "| Base | `" ENVIRON["BASE"] "` |"
  print "| Pushed by | `" ENVIRON["PUSHER"] "` |"
  print "| Head commit | `" ENVIRON["SHA_SHORT"] "` |"
  print "| Size | " ENVIRON["STAT"] " |"
  print "| Session | " ENVIRON["SESSION_TXT"] " |"
  print "| Opened by | [workflow run](" ENVIRON["RUN_URL"] ") |"
  print ""
}
/^<!-- part:/ { found["part"] = 1; exit }
skip {
  if ($0 ~ /^<details>/) skip = 0; else next
}
/^## / { sec = $0 }
/^## Production Risk/ {
  print "## Production Risk (quoted from the commit message, unverified)\n"
  r = ENVIRON["RISK"]
  if (r == "") r = "(none provided: the commit message needs a \"Production risk:\" section, see .github/review-rubric.md)"
  print quote(r) "\n"
  skip = 1; found["risk"] = 1; next
}
/^<!--.*-->[ \t]*$/ {
  if (sec == "## Summary") {
    s = ENVIRON["SUMMARY"]; if (s == "") s = "(none provided)"
    print "Agent description (quoted, unverified):\n"; print quote(s); found["summary"] = 1; next
  }
  if (sec == "## Verification") { print "Not supplied by the agent. See the checks on this PR."; found["verification"] = 1; next }
  if (sec == "## Rollback") { print "Revert the squash commit unless the description says otherwise."; found["rollback"] = 1; next }
}
/^- \[ \] Agent-generated/ { print "- [x] Agent-generated"; found["author"] = 1; next }
/^\| Agent Name \|/ { print "| Agent Name | `" ENVIRON["PUSHER"] "` |"; found["name"] = 1; next }
/^\| Workflow \|/ { print "| Workflow | `Open agent PR` |"; found["workflow"] = 1; next }
/^\| Run ID \|/ { print "| Run ID | `" ENVIRON["RUN_ID"] "` |"; found["run"] = 1; next }
{ print }
END {
  print "\nMerges only with approval from @" ENVIRON["REVIEWER"] " (squash). If Base is not main, this PR is part of a stack: merge from the bottom up."
  n = split("summary verification rollback author name workflow run risk part", need, " ")
  for (i = 1; i <= n; i++) if (!(need[i] in found)) { print "render-agent-pr-body: template anchor missing: " need[i] > "/dev/stderr"; bad = 1 }
  if (bad) exit 1
}
' "$TEMPLATE"
