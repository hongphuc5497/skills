#!/usr/bin/env bash
set -euo pipefail

integration="${1:-}"
mode="${2:-}"

if [[ -z "$integration" ]]; then
  echo "usage: $0 <list|codex|opencode|augment|openclaw|hermes|claude> [--dry-run]" >&2
  exit 2
fi

if [[ "$integration" == "list" ]]; then
  cat <<'EOF'
Supported Agent Ops integrations:

agent     artifact                                  role
claude    CLAUDE.md                                 brain or worker
codex     AGENTS.md                                 default implementer
opencode  .ai/integrations/opencode-instructions.md isolated implementation lane
augment   .ai/integrations/augment-discovery.md    codebase navigator
openclaw  .ai/integrations/openclaw-review.md      product and scope reviewer
hermes    .ai/integrations/hermes-monitor.md       watcher and notifier
EOF
  exit 0
fi

if [[ "$mode" != "" && "$mode" != "--dry-run" ]]; then
  echo "unknown option: $mode" >&2
  exit 2
fi

dry_run=0
if [[ "$mode" == "--dry-run" ]]; then
  dry_run=1
fi

mkdir -p .ai/integrations

copy_file() {
  local src="$1"
  local dst="$2"
  if [[ "$dry_run" -eq 1 ]]; then
    echo "would write $dst from $src"
    return
  fi
  cp "$src" "$dst"
  echo "wrote $dst"
}

case "$integration" in
  codex)
    src=".ai/integrations/templates/codex/AGENTS.template.md"
    if [[ ! -f "$src" ]]; then
      echo "missing $src" >&2
      exit 1
    fi
    if [[ "$dry_run" -eq 1 ]]; then
      echo "would append Agent Ops Codex rules to AGENTS.md"
    elif grep -q "Agent Ops Rules for Codex" AGENTS.md; then
      echo "AGENTS.md already contains Agent Ops Codex rules"
    else
      {
        printf "\n"
        cat "$src"
      } >> AGENTS.md
      echo "updated AGENTS.md"
    fi
    ;;
  opencode)
    copy_file ".ai/integrations/templates/opencode/instructions.md" ".ai/integrations/opencode-instructions.md"
    ;;
  augment)
    copy_file ".ai/integrations/templates/augment/discovery-guide.md" ".ai/integrations/augment-discovery.md"
    ;;
  openclaw)
    copy_file ".ai/integrations/templates/openclaw/review.md" ".ai/integrations/openclaw-review.md"
    ;;
  hermes)
    copy_file ".ai/integrations/templates/hermes/monitor.md" ".ai/integrations/hermes-monitor.md"
    ;;
  claude)
    src=".ai/integrations/templates/claude/CLAUDE.template.md"
    if [[ ! -f "$src" ]]; then
      echo "missing $src" >&2
      exit 1
    fi
    if [[ "$dry_run" -eq 1 ]]; then
      echo "would append Agent Ops Claude rules to CLAUDE.md"
    elif grep -q "Agent Ops Rules for Claude" CLAUDE.md; then
      echo "CLAUDE.md already contains Agent Ops Claude rules"
    else
      {
        printf "\n"
        cat "$src"
      } >> CLAUDE.md
      echo "updated CLAUDE.md"
    fi
    ;;
  *)
    echo "unknown integration: $integration" >&2
    echo "run: $0 list" >&2
    exit 2
    ;;
esac
