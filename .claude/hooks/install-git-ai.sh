#!/bin/bash
set -euo pipefail

# Only run in remote (Claude Code on the web) environments
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

# Install git-ai for AI code attribution
# https://github.com/git-ai-project/git-ai
if ! command -v git-ai &> /dev/null; then
  installer_file="$(mktemp "${TMPDIR:-/tmp}/git-ai-install.XXXXXX")"
  trap 'rm -f -- "$installer_file"' EXIT

  curl --disable \
    --fail \
    --silent \
    --show-error \
    --location \
    --proto '=https' \
    --proto-redir '=https' \
    --tlsv1.2 \
    --connect-timeout 10 \
    --max-time 120 \
    --output "$installer_file" \
    https://usegitai.com/install.sh

  bash -n "$installer_file"
  bash "$installer_file"
fi

# Ensure git-ai is on the PATH for the session
if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  path_export="export PATH=\"\$HOME/.git-ai/bin:\$HOME/.local/bin:\$PATH\""
  if [ ! -f "$CLAUDE_ENV_FILE" ] || ! grep -Fxq -- "$path_export" "$CLAUDE_ENV_FILE"; then
    printf '%s\n' "$path_export" >> "$CLAUDE_ENV_FILE"
  fi
fi
