#!/usr/bin/env bash
set -euo pipefail

# Files that are always tracked and must exist in every Agent Ops repo.
# These live OUTSIDE .ai/, so they are committed even when a target repo
# gitignores the whole .ai/ runtime directory (the default `agent-ops init`
# layout). They are required unconditionally.
core_files=(
  "docs/supported-integrations.md"
  "scripts/agent-ops-tool.py"
  "scripts/ao"
  "scripts/install-integration.sh"
  "scripts/init-repo.sh"
  "scripts/agent-ops-check.sh"
  ".github/workflows/agent-ops-check.yml"
  ".github/workflows/notify-failure.yml"
  ".github/workflows/stale-task-monitor.yml"
)

# Files under .ai/. This is the runtime/source directory agent-ops manages, and
# `agent-ops init` gitignores it by default — so on a clean checkout (e.g. CI in
# a target repo) it is absent. Validate these only when .ai/ is actually
# committed, detected via the .ai/protocol.md sentinel. A repo that commits the
# .ai/ source (like this one) gets full validation; a repo that gitignores it
# (the default) skips these and still passes. TASK.md/DECISIONS.md are user data
# and the integration templates are protocol source — both belong here, NOT in
# core_files, so a gitignored-.ai/ target repo isn't forced to commit them.
ai_files=(
  ".ai/protocol.md"
  ".ai/TASK.md"
  ".ai/ROUTING.md"
  ".ai/DECISIONS.md"
  ".ai/schema/task.schema.json"
  ".ai/schema/file-claims.schema.json"
  ".ai/schema/handoff.schema.json"
  ".ai/workflows/daily.md"
  ".ai/workflows/feature.md"
  ".ai/workflows/debugging.md"
  ".ai/workflows/ci-failure.md"
  ".ai/workflows/review.md"
  ".ai/workflows/experimentation.md"
  ".ai/templates/project-score.md"
  ".ai/integrations/templates/README.md"
  ".ai/integrations/templates/codex/AGENTS.template.md"
  ".ai/integrations/templates/claude/CLAUDE.template.md"
  ".ai/integrations/templates/opencode/instructions.md"
  ".ai/integrations/templates/augment/discovery-guide.md"
  ".ai/integrations/templates/openclaw/review.md"
  ".ai/integrations/templates/hermes/monitor.md"
  ".ai/integrations/templates/mcp/README.md"
)

missing=0
for file in "${core_files[@]}"; do
  if [[ ! -f "$file" ]]; then
    echo "missing required file: $file" >&2
    missing=1
  fi
done

ai_present=0
if [[ -f ".ai/protocol.md" ]]; then
  ai_present=1
  for file in "${ai_files[@]}"; do
    if [[ ! -f "$file" ]]; then
      echo "missing required file: $file" >&2
      missing=1
    fi
  done
else
  echo "note: .ai/ not present (runtime dir is gitignored); skipping Agent Ops state checks"
fi

if [[ "$missing" -ne 0 ]]; then
  exit 1
fi

if [[ -f ".ai/state/active-task.json" ]]; then
  python3 - <<'PY'
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

state = json.loads(Path(".ai/state/active-task.json").read_text())
if state.get("status") != "active":
    raise SystemExit(0)

started = datetime.fromisoformat(state["started_at"])
age_hours = (datetime.now(timezone.utc) - started).total_seconds() / 3600
if age_hours > 48:
    print(f"active task is stale: {age_hours:.1f} hours", file=sys.stderr)
    raise SystemExit(1)
PY
fi

bash -n scripts/*.sh
python3 -m py_compile scripts/agent-ops-tool.py
if [[ "$ai_present" -eq 1 ]]; then
  python3 scripts/agent-ops-tool.py check >/dev/null
fi
echo "agent-ops check passed"
