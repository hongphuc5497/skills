#!/usr/bin/env bash
set -euo pipefail

target="${1:-}"
shift || true

if [[ -z "$target" ]]; then
  echo "usage: $0 <target-repo> [--dry-run] [--force] [--upgrade]" >&2
  exit 2
fi

dry_run=0
force=0
upgrade=0
for arg in "$@"; do
  case "$arg" in
    --dry-run)
      dry_run=1
      ;;
    --force)
      force=1
      ;;
    --upgrade)
      upgrade=1
      ;;
    *)
      echo "unknown option: $arg" >&2
      exit 2
      ;;
  esac
done

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source_root="$(cd "$script_dir/.." && pwd)"

if [[ ! -d "$target" ]]; then
  echo "target repo does not exist: $target" >&2
  exit 1
fi

target_root="$(cd "$target" && pwd)"

# Upgrade mode refreshes the tooling in a repo that already has Agent Ops.
# Refuse to "upgrade" a repo that was never initialized — the user wants init.
if [[ "$upgrade" -eq 1 ]]; then
  if [[ ! -f "$target_root/scripts/agent-ops-tool.py" && ! -f "$target_root/.ai/protocol.md" ]]; then
    echo "no existing Agent Ops install found in: $target_root" >&2
    echo "run 'agent-ops init' first; --upgrade only refreshes an existing install" >&2
    exit 1
  fi
fi

if ! git -C "$target_root" rev-parse --git-dir >/dev/null 2>&1; then
  echo "target is not a git repository: $target_root" >&2
  echo "run 'git init' in the target first, or use --force to skip this check" >&2
  if [[ "$force" -eq 0 ]]; then
    exit 1
  fi
  echo "proceeding anyway (--force)" >&2
fi

copy_files=(
  "ROUTING.md"
  "docs/supported-integrations.md"
  ".ai/protocol.md"
  ".ai/schema/task.schema.json"
  ".ai/schema/file-claims.schema.json"
  ".ai/schema/handoff.schema.json"
  ".ai/workflows/daily.md"
  ".ai/workflows/feature.md"
  ".ai/workflows/debugging.md"
  ".ai/workflows/ci-failure.md"
  ".ai/workflows/review.md"
  ".ai/workflows/experimentation.md"
  ".ai/templates/task.md"
  ".ai/templates/decision.md"
  ".ai/templates/project-score.md"
  "integrations/README.md"
  "integrations/codex/AGENTS.template.md"
  "integrations/claude/CLAUDE.template.md"
  "integrations/opencode/instructions.md"
  "integrations/augment/discovery-guide.md"
  "integrations/openclaw/review.md"
  "integrations/hermes/monitor.md"
  "integrations/mcp/README.md"
  "scripts/agent-ops-tool.py"
  "scripts/ao"
  "scripts/install-integration.sh"
  "scripts/agent-ops-check.sh"
  "scripts/init-repo.sh"
  ".github/workflows/agent-ops-check.yml"
  ".github/workflows/notify-failure.yml"
  ".github/workflows/stale-task-monitor.yml"
)

generated_files=(
  "TASK.md"
  "DECISIONS.md"
  ".ai/state/file-claims.json"
  ".ai/state/handoffs.jsonl"
)

get_default_content() {
  local rel="$1"
  case "$rel" in
    TASK.md)
      printf '%s\n' \
        "# Active Task" \
        "" \
        "Status: none" \
        "Owner: none" \
        "Started: none" \
        "Task file: none" \
        "" \
        "## Current Objective" \
        "" \
        "No active task." \
        "" \
        "## Rules" \
        "" \
        "- Start exactly one task before implementation." \
        "- Keep the owner responsible for edits, verification, and final summary." \
        "- Advisors can comment, review, or research, but they do not edit the active" \
        "  concern unless ownership is transferred." \
        "- Finish or park the active task before starting another."
      ;;
    DECISIONS.md)
      printf '%s\n' \
        "# Decisions" \
        "" \
        "Record durable workflow, architecture, and product decisions here."
      ;;
    .ai/state/file-claims.json)
      printf '%s\n' '{' '  "claims": []' '}'
      ;;
    .ai/state/handoffs.jsonl)
      # empty file
      ;;
    *)
      echo "unknown generated file: $rel" >&2
      exit 1
      ;;
  esac
}

is_generated_file() {
  local rel="$1"
  local item
  for item in "${generated_files[@]}"; do
    if [[ "$item" == "$rel" ]]; then
      return 0
    fi
  done
  return 1
}

check_conflict() {
  local rel="$1"
  local dst="$target_root/$rel"
  local src="$source_root/$rel"
  if [[ "$force" -eq 0 && -e "$dst" ]]; then
    # If the file exists and is identical to what we would write/copy, it is not a conflict
    if is_generated_file "$rel"; then
      if [[ -f "$dst" ]] && get_default_content "$rel" | cmp -s - "$dst"; then
        return 0
      fi
    else
      if [[ -f "$src" && -f "$dst" ]] && cmp -s "$src" "$dst"; then
        return 0
      fi
    fi
    echo "would overwrite existing file: $rel" >&2
    return 1
  fi
}

# Upgrade re-copies only the tooling (copy_files) and never writes over an
# existing generated file (TASK.md, DECISIONS.md, .ai/state/*), so there is
# nothing to guard against — skip the conflict gate entirely.
if [[ "$upgrade" -eq 0 ]]; then
  conflicts=0
  for rel in "${copy_files[@]}" "${generated_files[@]}"; do
    check_conflict "$rel" || conflicts=1
  done

  if [[ "$conflicts" -ne 0 ]]; then
    echo "refusing to overwrite files; rerun with --force if intentional" >&2
    exit 1
  fi
fi

ensure_parent() {
  local rel="$1"
  mkdir -p "$(dirname "$target_root/$rel")"
}

copy_file() {
  local rel="$1"
  local src="$source_root/$rel"
  local dst="$target_root/$rel"
  if [[ ! -f "$src" ]]; then
    echo "missing source file: $rel" >&2
    exit 1
  fi
  if [[ "$dry_run" -eq 1 ]]; then
    echo "would copy $rel"
    return
  fi
  ensure_parent "$rel"
  cp "$src" "$dst"
  echo "copied $rel"
}

write_file() {
  local rel="$1"
  if [[ "$dry_run" -eq 1 ]]; then
    echo "would write $rel"
    return
  fi
  ensure_parent "$rel"
  get_default_content "$rel" > "$target_root/$rel"
  echo "wrote $rel"
}

# .ai/ holds runtime state (active task, file claims, handoffs, task records)
# that agent-ops writes during work. It must never be committed — doing so
# leaks local paths and workflow metadata, especially in public repos.
ensure_gitignore() {
  local gi="$target_root/.gitignore"
  if [[ -f "$gi" ]] && grep -qE '^/?\.ai/?$' "$gi"; then
    echo ".gitignore already ignores .ai/"
    return 0
  fi
  if [[ "$dry_run" -eq 1 ]]; then
    echo "would add .ai/ to .gitignore"
    return 0
  fi
  {
    [[ -s "$gi" ]] && printf '\n'
    printf '%s\n' "# Agent Ops runtime directory (managed by agent-ops init)."
    printf '%s\n' ".ai/"
  } >> "$gi"
  echo "updated .gitignore: ignore .ai/"
}

if [[ "$dry_run" -eq 0 ]]; then
  mkdir -p "$target_root/.ai/tasks/archive" "$target_root/.ai/reviews"
fi

for rel in "${copy_files[@]}"; do
  copy_file "$rel"
done

for rel in "${generated_files[@]}"; do
  # In upgrade mode, never clobber a project's real TASK.md/DECISIONS.md or live
  # runtime state. Only seed a generated file when it is genuinely missing
  # (e.g. a new generated file added in a later version, or .ai/state absent on
  # a fresh clone because .ai/ is gitignored).
  if [[ "$upgrade" -eq 1 && -e "$target_root/$rel" ]]; then
    if [[ "$dry_run" -eq 1 ]]; then
      echo "would preserve $rel"
    else
      echo "preserved $rel"
    fi
    continue
  fi
  write_file "$rel"
done

ensure_gitignore

if [[ "$dry_run" -eq 0 ]]; then
  chmod +x "$target_root/scripts/agent-ops-tool.py"
  chmod +x "$target_root/scripts/ao"
  chmod +x "$target_root/scripts/install-integration.sh"
  chmod +x "$target_root/scripts/agent-ops-check.sh"
  chmod +x "$target_root/scripts/init-repo.sh"
fi

if [[ "$upgrade" -eq 1 ]]; then
  echo "Agent Ops upgraded in $target_root"
  echo "Next: cd $target_root && ./scripts/agent-ops-check.sh"
else
  echo "Agent Ops initialized in $target_root"
  echo "Next: cd $target_root && ./scripts/install-integration.sh codex --dry-run"
fi
