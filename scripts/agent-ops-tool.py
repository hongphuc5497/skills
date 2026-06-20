#!/usr/bin/env python3
"""JSON bridge for Agent Ops integrations.

This is intentionally dependency-free. It gives coding agents a structured tool
surface without requiring a daemon or full MCP server.

State mutations are guarded by an exclusive POSIX file lock on `.ai/state/.lock`
so concurrent agents calling `claim`, `start`, `finish`, or `handoff` cannot
race each other. Writes are atomic (temp file + rename) so a crash mid-write
cannot leave a state file half-written.
"""

from __future__ import annotations

import argparse
import contextlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

try:
    import fcntl  # POSIX
except ImportError:  # pragma: no cover - Windows fallback
    fcntl = None  # type: ignore[assignment]


ROOT = Path.cwd()
AI_DIR = ROOT / ".ai"
STATE_DIR = AI_DIR / "state"
TASKS_DIR = AI_DIR / "tasks"
ACTIVE_TASK = STATE_DIR / "active-task.json"
CLAIMS_FILE = STATE_DIR / "file-claims.json"
HANDOFFS_FILE = STATE_DIR / "handoffs.jsonl"
ROUTING_FILE = AI_DIR / "routing.json"
STATE_LOCK = STATE_DIR / ".lock"
# v0.5.0 moved these from the repo root into .ai/. The migration paths are
# checked by doctor() so users with old-layout repos get a clear remedy.
TASK_MD = AI_DIR / "TASK.md"
ROUTING_MD = AI_DIR / "ROUTING.md"
DECISIONS_MD = AI_DIR / "DECISIONS.md"
INTEGRATIONS_DIR = AI_DIR / "integrations"
LEGACY_TASK_MD = ROOT / "TASK.md"
LEGACY_ROUTING_MD = ROOT / "ROUTING.md"
LEGACY_DECISIONS_MD = ROOT / "DECISIONS.md"
LEGACY_INTEGRATIONS_DIR = ROOT / "integrations"
TASK_ID_RE = re.compile(r"^[0-9]{8}-[0-9]{6}-[a-z0-9-]+$")
TOOL_VERSION = "0.5.0"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def emit(payload: dict[str, Any], exit_code: int = 0) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))
    raise SystemExit(exit_code)


def ensure_dirs() -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    TASKS_DIR.mkdir(parents=True, exist_ok=True)
    (TASKS_DIR / "archive").mkdir(parents=True, exist_ok=True)
    if not CLAIMS_FILE.exists():
        CLAIMS_FILE.write_text('{\n  "claims": []\n}\n')
    if not HANDOFFS_FILE.exists():
        HANDOFFS_FILE.write_text("")
    if not STATE_LOCK.exists():
        STATE_LOCK.touch()


@contextlib.contextmanager
def state_lock() -> Iterator[None]:
    """Hold an exclusive advisory lock on `.ai/state/.lock` for the block.

    All state mutations (claim/start/finish/handoff/delegate/update-task) wrap
    their read+modify+write in this lock so two concurrent agents cannot both
    pass a conflict check and then both write a conflicting claim. On non-POSIX
    systems the lock is a no-op; atomic writes still protect against torn files.
    """
    ensure_dirs()
    if fcntl is None:
        yield
        return
    with STATE_LOCK.open("a+") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        emit(
            {
                "ok": False,
                "error": f"invalid json in {path}: {exc}",
                "remedy": f"inspect {path.relative_to(ROOT) if path.is_absolute() else path} "
                          "and restore from .ai/tasks/archive or git history",
            },
            1,
        )


def write_json(path: Path, payload: Any) -> None:
    """Atomically write JSON: write to a temp file in the same dir, fsync, rename."""
    body = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent)
    )
    try:
        with os.fdopen(fd, "w") as handle:
            handle.write(body)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, path)
    except Exception:
        with contextlib.suppress(FileNotFoundError):
            os.unlink(tmp_name)
        raise


def append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    """Append a JSON line. POSIX guarantees O_APPEND writes are atomic for
    small lines, so concurrent appenders cannot interleave bytes."""
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(payload, sort_keys=True) + "\n"
    with path.open("a") as handle:
        handle.write(line)


# --- Structural validators ------------------------------------------------
#
# We deliberately avoid a jsonschema dependency: this is the entire contract.
# Each validator returns a list of human-readable problems; empty list = ok.


def validate_active_task(task: Any) -> list[str]:
    if not isinstance(task, dict):
        return ["active-task.json must be a JSON object"]
    problems: list[str] = []
    required = ("id", "title", "owner", "status", "started_at", "task_file")
    for key in required:
        if key not in task:
            problems.append(f"active task missing required field: {key}")
        elif not isinstance(task[key], str) or not task[key].strip():
            problems.append(f"active task field '{key}' must be a non-empty string")
    if isinstance(task.get("status"), str) and task["status"] not in (
        "active", "done", "parked", "killed",
    ):
        problems.append(f"active task status invalid: {task['status']!r}")
    if "id" in task and isinstance(task["id"], str) and not TASK_ID_RE.match(task["id"]):
        problems.append(f"active task id does not match expected pattern: {task['id']!r}")
    for list_field in ("files_in_scope", "out_of_scope"):
        if list_field in task and not isinstance(task[list_field], list):
            problems.append(f"active task field '{list_field}' must be an array")
    return problems


def validate_claims(payload: Any) -> list[str]:
    if not isinstance(payload, dict):
        return ["file-claims.json must be a JSON object"]
    claims = payload.get("claims")
    if not isinstance(claims, list):
        return ["file-claims.json must contain a 'claims' array"]
    problems: list[str] = []
    for index, claim in enumerate(claims):
        if not isinstance(claim, dict):
            problems.append(f"claims[{index}] must be an object")
            continue
        for key in ("task_id", "owner", "created_at"):
            if not isinstance(claim.get(key), str) or not claim[key].strip():
                problems.append(f"claims[{index}].{key} must be a non-empty string")
        if not isinstance(claim.get("paths"), list) or not claim["paths"]:
            problems.append(f"claims[{index}].paths must be a non-empty array")
        elif any(not isinstance(p, str) or not p for p in claim["paths"]):
            problems.append(f"claims[{index}].paths must contain non-empty strings")
    return problems


def validate_handoff(event: Any) -> list[str]:
    if not isinstance(event, dict):
        return ["handoff event must be a JSON object"]
    problems: list[str] = []
    for key in ("from", "to", "task_id", "created_at"):
        if not isinstance(event.get(key), str) or not event[key].strip():
            problems.append(f"handoff.{key} must be a non-empty string")
    if "files" in event and not isinstance(event["files"], list):
        problems.append("handoff.files must be an array")
    return problems


def validate_routing(payload: Any) -> list[str]:
    """Validate the per-repo `.ai/routing.json` schema.

    Returns a list of human-readable problems (empty = ok). This is the
    contract for per-repo routing overrides; if anything in the file is
    wrong we want to surface specific, actionable errors rather than
    silently fall through to the hardcoded routes (which would mask the
    user's customization).
    """
    if not isinstance(payload, dict):
        return ["routing.json must be a JSON object"]
    rules = payload.get("rules")
    if not isinstance(rules, list):
        return ["routing.json must contain a 'rules' array"]
    problems: list[str] = []
    for index, rule in enumerate(rules):
        prefix = f"rules[{index}]"
        if not isinstance(rule, dict):
            problems.append(f"{prefix} must be an object")
            continue
        if not isinstance(rule.get("name"), str) or not rule["name"].strip():
            problems.append(f"{prefix}.name must be a non-empty string")
        when = rule.get("when")
        if not isinstance(when, dict):
            problems.append(f"{prefix}.when must be an object")
        else:
            any_clause = when.get("any")
            if not isinstance(any_clause, list) or not any_clause:
                problems.append(f"{prefix}.when.any must be a non-empty array")
            else:
                for m_index, matcher in enumerate(any_clause):
                    m_prefix = f"{prefix}.when.any[{m_index}]"
                    if not isinstance(matcher, dict):
                        problems.append(f"{m_prefix} must be an object")
                        continue
                    has_keyword = isinstance(matcher.get("keyword"), str) and matcher["keyword"]
                    has_regex = isinstance(matcher.get("regex"), str) and matcher["regex"]
                    if not (has_keyword or has_regex):
                        problems.append(
                            f"{m_prefix} must specify 'keyword' or 'regex' as a non-empty string"
                        )
                    if has_regex:
                        try:
                            re.compile(matcher["regex"])
                        except re.error as exc:
                            problems.append(f"{m_prefix}.regex is invalid: {exc}")
        route = rule.get("route")
        if not isinstance(route, dict):
            problems.append(f"{prefix}.route must be an object")
        else:
            for field in ("owner", "workflow", "verification", "advisor", "type"):
                if field in route and not isinstance(route[field], str):
                    problems.append(f"{prefix}.route.{field} must be a string")
    return problems


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:60] or "task"


def active_task() -> dict[str, Any] | None:
    task = read_json(ACTIVE_TASK, None)
    if task and task.get("status") == "active":
        return task
    return None


def task_age_hours(task: dict[str, Any]) -> float:
    started = datetime.fromisoformat(task["started_at"])
    return (datetime.now(timezone.utc) - started).total_seconds() / 3600


def claims_payload() -> dict[str, Any]:
    payload = read_json(CLAIMS_FILE, {"claims": []})
    problems = validate_claims(payload)
    if problems:
        emit(
            {
                "ok": False,
                "error": "file-claims.json failed validation",
                "problems": problems,
                "remedy": "restore .ai/state/file-claims.json from git history, "
                          "or reset to {\"claims\": []} if no active work depends on it",
            },
            1,
        )
    return payload


def write_task_md(task: dict[str, Any]) -> None:
    TASK_MD.write_text(
        f"""# Active Task

Status: {task["status"]}
Owner: {task["owner"]}
Started: {task["started_at"]}
Task file: {task["task_file"]}
Repo: {task.get("repo", "")}
Workflow: {task.get("workflow", "")}
Verification: {task.get("verification", "")}

## Current Objective

{task["title"]}

## Rules

- Exactly one owner edits the active concern.
- Agents must claim files before editing.
- Advisors can research or review, but should not edit unless ownership is transferred.
- Finish or park the active task before starting another.
"""
    )


def task_id_from_file(path: Path) -> str:
    return path.stem


def task_markdown(task: dict[str, Any]) -> str:
    return f"""# {task["title"]}

Status: {task["status"]}
Owner: {task["owner"]}
Started: {task.get("started_at", "")}
Repo: {task.get("repo", "")}
Workflow: {task.get("workflow", "")}
Verification: {task.get("verification", "")}

## Objective

## Acceptance Criteria

- TODO

## Files In Scope

{chr(10).join(f"- `{item}`" for item in task.get("files_in_scope", [])) or "- "}

## Out Of Scope

{chr(10).join(f"- `{item}`" for item in task.get("out_of_scope", [])) or "- "}

## Result

Changed files:

Verification:

Risks:
"""


def parse_markdown_task(path: Path) -> dict[str, Any]:
    text = path.read_text()
    lines = text.splitlines()
    title = task_id_from_file(path)
    if lines and lines[0].startswith("# "):
        title = lines[0][2:].strip()
    fields: dict[str, str] = {}
    for line in lines[1:12]:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip().lower().replace(" ", "_")] = value.strip()
    return {
        "id": task_id_from_file(path),
        "title": title,
        "status": fields.get("status", "backlog") or "backlog",
        "owner": fields.get("owner", ""),
        "workflow": fields.get("workflow", ""),
        "verification": fields.get("verification", ""),
        "task_file": str(path.relative_to(ROOT)),
        "created_at": fields.get("started", ""),
        "finished_at": None,
        "files_in_scope": [],
        "out_of_scope": [],
    }


def normalize_task(task: dict[str, Any], *, fallback_status: str = "backlog") -> dict[str, Any]:
    task_file = task.get("task_file", "")
    return {
        "id": task.get("id") or (task_id_from_file(ROOT / task_file) if task_file else ""),
        "title": task.get("title", ""),
        "status": task.get("status") or fallback_status,
        "owner": task.get("owner", ""),
        "workflow": task.get("workflow", ""),
        "verification": task.get("verification", ""),
        "verification_result": task.get("verification_result", ""),
        "task_file": task_file,
        "created_at": task.get("created_at") or task.get("started_at", ""),
        "started_at": task.get("started_at", ""),
        "finished_at": task.get("finished_at"),
        "repo": task.get("repo", ""),
        "files_in_scope": task.get("files_in_scope", []),
        "out_of_scope": task.get("out_of_scope", []),
    }


def apply_task_updates(task: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    if args.title is not None:
        task["title"] = args.title
    if args.owner is not None:
        task["owner"] = args.owner
    if args.workflow is not None:
        task["workflow"] = args.workflow
    if args.verification is not None:
        task["verification"] = args.verification
    if args.files is not None:
        task["files_in_scope"] = args.files
    if args.out_of_scope is not None:
        task["out_of_scope"] = args.out_of_scope
    task["started_at"] = task.get("started_at") or task.get("created_at", "")
    return task


def build_task_payload(
    title: str,
    *,
    status: str,
    owner: str,
    repo: str = "",
    workflow: str = "",
    verification: str = "",
    files_in_scope: list[str] | None = None,
    out_of_scope: list[str] | None = None,
) -> dict[str, Any]:
    created = now()
    task_id = f"{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}-{slugify(title)}"
    task_file = f".ai/tasks/{task_id}.md"
    return {
        "id": task_id,
        "title": title,
        "owner": owner,
        "status": status,
        "started_at": created,
        "task_file": task_file,
        "repo": repo,
        "workflow": workflow,
        "verification": verification,
        "files_in_scope": files_in_scope or [],
        "out_of_scope": out_of_scope or [],
    }


def check_payload() -> dict[str, Any]:
    required = [
        ".ai/TASK.md",
        ".ai/ROUTING.md",
        ".ai/DECISIONS.md",
        "docs/supported-integrations.md",
        ".ai/protocol.md",
        ".ai/schema/task.schema.json",
        ".ai/schema/file-claims.schema.json",
        ".ai/schema/handoff.schema.json",
        "scripts/agent-ops-tool.py",
        "scripts/ao",
        "scripts/install-integration.sh",
        "scripts/init-repo.sh",
        "scripts/agent-ops-check.sh",
        ".ai/integrations/templates/codex/AGENTS.template.md",
        ".ai/integrations/templates/claude/CLAUDE.template.md",
        ".github/workflows/agent-ops-check.yml",
        ".github/workflows/notify-failure.yml",
        ".github/workflows/stale-task-monitor.yml",
    ]
    missing = [path for path in required if not (ROOT / path).exists()]
    invalid_json: list[str] = []
    for path in [
        ".ai/schema/task.schema.json",
        ".ai/schema/file-claims.schema.json",
        ".ai/schema/handoff.schema.json",
        ".ai/state/file-claims.json",
    ]:
        file_path = ROOT / path
        if not file_path.exists():
            continue
        try:
            json.loads(file_path.read_text())
        except json.JSONDecodeError as exc:
            invalid_json.append(f"{path}: {exc}")

    invalid_jsonl: list[str] = []
    if HANDOFFS_FILE.exists():
        for index, line in enumerate(HANDOFFS_FILE.read_text().splitlines(), start=1):
            if not line.strip():
                continue
            try:
                json.loads(line)
            except json.JSONDecodeError as exc:
                invalid_jsonl.append(f"{HANDOFFS_FILE}:{index}: {exc}")

    stale = False
    task = active_task()
    if task:
        stale = task_age_hours(task) > 48
    return {
        "ok": not missing and not stale and not invalid_json and not invalid_jsonl,
        "missing": missing,
        "invalid_json": invalid_json,
        "invalid_jsonl": invalid_jsonl,
        "stale": stale,
    }


def read_handoffs() -> list[dict[str, Any]]:
    if not HANDOFFS_FILE.exists():
        return []
    events: list[dict[str, Any]] = []
    for line in HANDOFFS_FILE.read_text().splitlines():
        if not line.strip():
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return events


def command_status(_: argparse.Namespace) -> None:
    ensure_dirs()
    task = active_task()
    claims = claims_payload()["claims"]
    if not task:
        emit({"ok": True, "active": False, "claims": claims})
    emit(
        {
            "ok": True,
            "active": True,
            "task": task,
            "age_hours": round(task_age_hours(task), 2),
            "stale": task_age_hours(task) > 48,
            "claims": claims,
        }
    )


def _hardcoded_route(description: str) -> dict[str, str]:
    """Built-in fallback routes. Preserved verbatim from v0.3.x so repos
    without `.ai/routing.json` see zero behavior change."""
    text = description.lower()
    if any(word in text for word in ["ci", "github action", "workflow failed", "check failed"]):
        return {
            "type": "ci-failure",
            "owner": "Codex",
            "advisor": "GitHub Actions logs, Augment",
            "workflow": ".ai/workflows/ci-failure.md",
            "verification": "reproduce failing check locally, patch, rerun matching command",
        }
    if any(word in text for word in ["bug", "debug", "failure", "failing", "error", "regression"]):
        return {
            "type": "debugging",
            "owner": "Codex",
            "advisor": "Augment",
            "workflow": ".ai/workflows/debugging.md",
            "verification": "reproduce failure, add regression or minimal repro, rerun failing command",
        }
    if any(word in text for word in ["review", "critique", "scope", "product", "positioning"]):
        return {
            "type": "review",
            "owner": "OpenClaw",
            "advisor": "Codex for implementation facts",
            "workflow": ".ai/workflows/review.md",
            "verification": "recommend continue, park, or kill with evidence",
        }
    if any(word in text for word in ["experiment", "spike", "prototype", "try"]):
        return {
            "type": "experiment",
            "owner": "Codex",
            "advisor": "OpenClaw",
            "workflow": ".ai/workflows/experimentation.md",
            "verification": "time box, kill date, continue evidence",
        }
    return {
        "type": "feature",
        "owner": "Codex",
        "advisor": "Augment, OpenClaw if product scope changes",
        "workflow": ".ai/workflows/feature.md",
        "verification": "targeted tests, lint, build, or browser check as appropriate",
    }


def load_routing_rules() -> list[dict[str, Any]]:
    """Read and validate `.ai/routing.json`. Returns the rules list, or
    [] if the file doesn't exist. Emits a typed error and exits non-zero
    when the file is present but malformed — we'd rather fail loud than
    silently fall back to defaults and have the user wondering why their
    custom rule isn't applied.
    """
    if not ROUTING_FILE.exists():
        return []
    payload = read_json(ROUTING_FILE, {"rules": []})
    problems = validate_routing(payload)
    if problems:
        emit(
            {
                "ok": False,
                "error": ".ai/routing.json failed validation",
                "problems": problems,
                "remedy": "fix the listed problems in .ai/routing.json, or delete the file "
                          "to fall back to the built-in routes",
            },
            1,
        )
    return payload["rules"]


def _matches(matcher: dict[str, Any], text_lower: str, text_original: str) -> bool:
    """Apply one matcher (a `keyword` or `regex` clause) to a description.

    Keyword matches are case-insensitive substring; regex matches use
    `re.search` against the original text so users keep full control of
    case-sensitivity via flags inside their pattern.
    """
    if "keyword" in matcher and matcher["keyword"]:
        return matcher["keyword"].lower() in text_lower
    if "regex" in matcher and matcher["regex"]:
        try:
            return bool(re.search(matcher["regex"], text_original))
        except re.error:
            # validate_routing already rejects unparseable regexes; if we
            # somehow got here with a bad pattern, treat it as no-match.
            return False
    return False


def match_rule(rule: dict[str, Any], description: str) -> bool:
    """True iff `description` matches the rule's `when` clause. Only the
    `any:` combinator is supported in v0.4.0 — additional combinators
    (`all`, `not`) can be added without breaking the schema."""
    when = rule.get("when") or {}
    any_clause = when.get("any") or []
    text_lower = description.lower()
    return any(_matches(m, text_lower, description) for m in any_clause)


def infer_route(description: str) -> dict[str, str]:
    """Pick a route for a task description.

    Two-stage: per-repo `.ai/routing.json` rules first (in order, first
    match wins), then the built-in keyword fallback. A matching rule's
    `route` block is merged on top of the built-in default for the same
    type so partial overrides work — e.g., a rule that only sets `owner`
    keeps the default workflow/verification fields.
    """
    rules = load_routing_rules()
    for rule in rules:
        if match_rule(rule, description):
            # Start from a sensible default so the user can override just
            # the fields they care about. The default is the hardcoded
            # route for the same description, so behavior is "extend or
            # override" rather than "replace and lose fields."
            merged = dict(_hardcoded_route(description))
            override = rule.get("route") or {}
            for key, value in override.items():
                if isinstance(value, str) and value:
                    merged[key] = value
            # The rule's `name` becomes the route's `type` if the user
            # didn't supply one explicitly. This lets `agent-ops doctor`
            # and downstream tooling identify which rule fired.
            if "type" not in override:
                merged["type"] = rule.get("name", merged.get("type", "custom"))
            return merged
    return _hardcoded_route(description)


def command_route(args: argparse.Namespace) -> None:
    emit({"ok": True, "route": infer_route(args.description)})


def command_create_task(args: argparse.Namespace) -> None:
    ensure_dirs()
    route = infer_route(args.title)
    status = "active" if args.active else "backlog"
    if status == "active" and active_task():
        emit({"ok": False, "error": "active task already exists", "status": active_task()}, 1)
    task = build_task_payload(
        args.title,
        status=status,
        owner=args.owner or route["owner"],
        repo=args.repo or "",
        workflow=args.workflow or route["workflow"],
        verification=args.verification or route["verification"],
        files_in_scope=args.files or [],
        out_of_scope=args.out_of_scope or [],
    )
    task_path = ROOT / task["task_file"]
    task_path.write_text(task_markdown(task))
    if status == "active":
        write_json(ACTIVE_TASK, task)
        write_task_md(task)
    emit({"ok": True, "task": normalize_task(task, fallback_status=status)})


def command_start(args: argparse.Namespace) -> None:
    ensure_dirs()
    with state_lock():
        if active_task():
            emit({"ok": False, "error": "active task already exists", "status": active_task()}, 1)
        _command_start_locked(args)


def _command_start_locked(args: argparse.Namespace) -> None:
    created = now()
    task_id = f"{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}-{slugify(args.title)}"
    route = infer_route(args.title)
    task_file = f".ai/tasks/{task_id}.md"
    task_path = ROOT / task_file
    task: dict[str, Any] = {
        "id": task_id,
        "title": args.title,
        "owner": args.owner or route["owner"],
        "status": "active",
        "started_at": created,
        "task_file": task_file,
        "repo": args.repo or "",
        "workflow": args.workflow or route["workflow"],
        "verification": args.verification or route["verification"],
        "files_in_scope": args.files or [],
        "out_of_scope": args.out_of_scope or [],
    }
    write_json(ACTIVE_TASK, task)
    task_path.write_text(
        f"""# {args.title}

Status: active
Owner: {task["owner"]}
Started: {created}
Repo: {task["repo"]}
Workflow: {task["workflow"]}
Verification: {task["verification"]}

## Objective

## Acceptance Criteria

- 

## Files In Scope

{chr(10).join(f"- `{item}`" for item in task["files_in_scope"]) or "- "}

## Out Of Scope

{chr(10).join(f"- `{item}`" for item in task["out_of_scope"]) or "- "}

## Result

Changed files:

Verification:

Risks:
"""
    )
    write_task_md(task)
    emit({"ok": True, "task": task})


def command_claim(args: argparse.Namespace) -> None:
    ensure_dirs()
    # Hold the lock across the conflict check AND the write so two concurrent
    # agents claiming overlapping paths cannot both pass the check before
    # either writes — exactly one wins, the other gets a clear conflict error.
    with state_lock():
        task = active_task()
        if not task:
            emit({"ok": False, "error": "cannot claim files without active task"}, 1)
        owner = args.owner or task["owner"]
        payload = claims_payload()
        existing_claims = payload["claims"]
        requested = set(args.paths)

        conflicts: list[dict[str, Any]] = []
        for claim in existing_claims:
            existing = set(claim.get("paths", []))
            if claim.get("task_id") != task["id"] and requested.intersection(existing):
                conflicts.append(claim)
            if claim.get("task_id") == task["id"] and claim.get("owner") != owner and requested.intersection(existing):
                conflicts.append(claim)
        if conflicts:
            emit({"ok": False, "error": "claim conflict", "conflicts": conflicts}, 1)

        claim = {
            "task_id": task["id"],
            "owner": owner,
            "paths": args.paths,
            "created_at": now(),
            "reason": args.reason,
        }
        existing_claims.append(claim)
        write_json(CLAIMS_FILE, payload)
        emit({"ok": True, "claim": claim})


def command_handoff(args: argparse.Namespace) -> None:
    ensure_dirs()
    with state_lock():
        task = active_task()
        if not task:
            emit({"ok": False, "error": "cannot hand off without active task"}, 1)
        event = {
            "from": args.from_owner or task["owner"],
            "to": args.to,
            "task_id": task["id"],
            "files": args.files or [],
            "acceptance": args.acceptance,
            "verification": args.verification or "",
            "notes": args.notes or "",
            "created_at": now(),
        }
        append_jsonl(HANDOFFS_FILE, event)
        emit({"ok": True, "handoff": event})


def command_delegate(args: argparse.Namespace) -> None:
    """Route a task description to the right agent and record a handoff.
    
    Requires an active task. Uses route inference to pick the best owner
    unless --to is explicitly provided. Records a handoff from the current
    owner to the delegated agent.
    """
    ensure_dirs()
    with state_lock():
        task = active_task()
        if not task:
            emit({"ok": False, "error": "no active task to delegate from; start a task first"}, 1)

        route = infer_route(args.description)
        to_agent = args.to or route["owner"]
        from_agent = args.from_owner or task["owner"]

        event = {
            "from": from_agent,
            "to": to_agent,
            "task_id": task["id"],
            "description": args.description,
            "files": args.files or [],
            "acceptance": args.acceptance or route["verification"],
            "verification": args.verification or route["verification"],
            "notes": args.notes or "",
            "created_at": now(),
        }
        append_jsonl(HANDOFFS_FILE, event)

        emit({
            "ok": True,
            "delegated_to": to_agent,
            "delegated_from": from_agent,
            "route": route,
            "handoff": event,
        })


def command_finish(args: argparse.Namespace) -> None:
    ensure_dirs()
    with state_lock():
        task = active_task()
        if not task:
            emit({"ok": False, "error": "no active task"}, 1)
        task["status"] = args.result
        task["finished_at"] = now()
        if args.verification:
            task["verification_result"] = args.verification
        archive_file = f".ai/tasks/archive/{task['id']}.json"
        archive_path = ROOT / archive_file
        write_json(archive_path, task)
        ACTIVE_TASK.unlink(missing_ok=True)

        claims = claims_payload()
        claims["claims"] = [claim for claim in claims["claims"] if claim.get("task_id") != task["id"]]
        write_json(CLAIMS_FILE, claims)

    TASK_MD.write_text(
        """# Active Task

Status: none
Owner: none
Started: none
Task file: none

## Current Objective

No active task.

## Rules

- Start exactly one task before implementation.
- Keep the owner responsible for edits, verification, and final summary.
- Advisors can comment, review, or research, but they do not edit the active
  concern unless ownership is transferred.
- Finish or park the active task before starting another.
"""
    )
    emit({"ok": True, "finished": task, "archive": archive_file})


def command_kanban_snapshot(_: argparse.Namespace) -> None:
    ensure_dirs()
    columns: dict[str, list[dict[str, Any]]] = {
        "backlog": [],
        "active": [],
        "parked": [],
        "done": [],
        "killed": [],
    }
    archived_ids: set[str] = set()

    for archive_path in sorted((TASKS_DIR / "archive").glob("*.json")):
        task = read_json(archive_path, {})
        if not isinstance(task, dict):
            continue
        task.setdefault("id", archive_path.stem)
        task.setdefault("task_file", f".ai/tasks/{archive_path.stem}.md")
        normalized = normalize_task(task)
        archived_ids.add(normalized["id"])
        status = normalized["status"]
        if status in columns:
            columns[status].append(normalized)

    active = active_task()
    active_id = ""
    if active:
        normalized_active = normalize_task(active, fallback_status="active")
        active_id = normalized_active["id"]
        columns["active"].append(normalized_active)

    for task_path in sorted(TASKS_DIR.glob("*.md")):
        task_id = task_id_from_file(task_path)
        if task_id in archived_ids or task_id == active_id:
            continue
        task = parse_markdown_task(task_path)
        if task["status"] not in columns or task["status"] == "active":
            task["status"] = "backlog"
        columns[task["status"]].append(normalize_task(task))

    emit(
        {
            "ok": True,
            "repo": str(ROOT),
            "active": bool(active),
            "columns": columns,
            "claims": claims_payload()["claims"],
            "handoffs": read_handoffs(),
            "health": check_payload(),
        }
    )


def command_update_task(args: argparse.Namespace) -> None:
    ensure_dirs()
    if not TASK_ID_RE.match(args.task_id):
        emit({"ok": False, "error": "invalid task id"}, 1)

    with state_lock():
        task = active_task()
        if task and task.get("id") == args.task_id:
            updated = apply_task_updates(task, args)
            write_json(ACTIVE_TASK, updated)
            task_path = ROOT / updated["task_file"]
            task_path.write_text(task_markdown(updated))
            write_task_md(updated)
            emit({"ok": True, "task": normalize_task(updated, fallback_status="active")})

        archive_path = TASKS_DIR / "archive" / f"{args.task_id}.json"
        if archive_path.exists():
            archived = read_json(archive_path, {})
            if not isinstance(archived, dict):
                emit({"ok": False, "error": f"invalid task archive: {archive_path}"}, 1)
            archived.setdefault("id", args.task_id)
            archived.setdefault("task_file", f".ai/tasks/{args.task_id}.md")
            updated = apply_task_updates(archived, args)
            write_json(archive_path, updated)
            emit({"ok": True, "task": normalize_task(updated)})

        markdown_path = TASKS_DIR / f"{args.task_id}.md"
        if markdown_path.exists():
            markdown_task = parse_markdown_task(markdown_path)
            updated = apply_task_updates(markdown_task, args)
            markdown_path.write_text(task_markdown(updated))
            emit({"ok": True, "task": normalize_task(updated)})

        emit({"ok": False, "error": "task not found", "task_id": args.task_id}, 1)


def command_check(_: argparse.Namespace) -> None:
    ensure_dirs()
    payload = check_payload()
    emit(payload, 0 if payload["ok"] else 1)


def _tool_version(binary: str, *flags: str) -> str:
    try:
        result = subprocess.run(
            [binary, *flags],
            capture_output=True,
            text=True,
            timeout=2,
            check=False,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return ""
    out = (result.stdout or result.stderr or "").strip().splitlines()
    return out[0] if out else ""


def doctor_payload() -> dict[str, Any]:
    """Diagnose this Agent Ops install. Read-only; safe to run at any time.

    The output is structured so it can be parsed by tooling, but is also
    human-skimmable. Each section reports a status and the evidence used to
    derive it, so a user can act on a 'fail' without guessing what we checked.
    """
    health = check_payload()
    state_problems: dict[str, list[str]] = {}

    active = read_json(ACTIVE_TASK, None) if ACTIVE_TASK.exists() else None
    if active is not None:
        problems = validate_active_task(active)
        if problems:
            state_problems["active-task.json"] = problems

    if CLAIMS_FILE.exists():
        claims = read_json(CLAIMS_FILE, {"claims": []})
        problems = validate_claims(claims)
        if problems:
            state_problems["file-claims.json"] = problems

    handoff_problems: list[str] = []
    if HANDOFFS_FILE.exists():
        for index, line in enumerate(HANDOFFS_FILE.read_text().splitlines(), start=1):
            if not line.strip():
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError as exc:
                handoff_problems.append(f"line {index}: invalid json — {exc}")
                continue
            for problem in validate_handoff(event):
                handoff_problems.append(f"line {index}: {problem}")
    if handoff_problems:
        state_problems["handoffs.jsonl"] = handoff_problems

    repo_initialized = (ROOT / "scripts" / "agent-ops-tool.py").exists() and (
        ROOT / ".ai" / "protocol.md"
    ).exists()

    # v0.5.0 moved several things from the repo root into .ai/. Surface
    # old-layout repos as a typed problem with a one-line remedy so users
    # know exactly what to do.
    legacy_layout: list[str] = []
    for legacy in (LEGACY_TASK_MD, LEGACY_ROUTING_MD, LEGACY_DECISIONS_MD):
        if legacy.exists():
            legacy_layout.append(str(legacy.relative_to(ROOT)))
    if LEGACY_INTEGRATIONS_DIR.is_dir():
        legacy_layout.append(
            str(LEGACY_INTEGRATIONS_DIR.relative_to(ROOT)) + "/"
        )

    return {
        "ok": health["ok"] and not state_problems and not legacy_layout,
        "agent_ops": {
            "tool_version": TOOL_VERSION,
            "repo_initialized": repo_initialized,
            "repo_root": str(ROOT),
        },
        "runtime": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "node": _tool_version("node", "--version"),
            "git": _tool_version("git", "--version"),
            "locking": "fcntl" if fcntl is not None else "atomic-write-only",
        },
        "health": health,
        "state_problems": state_problems,
        "legacy_layout": {
            "files_at_root": legacy_layout,
            "remedy": (
                "run `agent-ops upgrade` to migrate them into .ai/ — content is preserved"
                if legacy_layout
                else ""
            ),
        },
    }


def command_doctor(_: argparse.Namespace) -> None:
    ensure_dirs()
    payload = doctor_payload()
    emit(payload, 0 if payload["ok"] else 1)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Agent Ops JSON bridge")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("status").set_defaults(func=command_status)

    route = sub.add_parser("route")
    route.add_argument("description")
    route.set_defaults(func=command_route)

    create_task = sub.add_parser("create-task")
    create_task.add_argument("title")
    create_task.add_argument("--owner")
    create_task.add_argument("--repo")
    create_task.add_argument("--workflow")
    create_task.add_argument("--verification")
    create_task.add_argument("--files", action="append")
    create_task.add_argument("--out-of-scope", action="append")
    create_task.add_argument("--active", action="store_true")
    create_task.set_defaults(func=command_create_task)

    update_task = sub.add_parser("update-task")
    update_task.add_argument("task_id")
    update_task.add_argument("--title")
    update_task.add_argument("--owner")
    update_task.add_argument("--workflow")
    update_task.add_argument("--verification")
    update_task.add_argument("--files", action="append")
    update_task.add_argument("--out-of-scope", action="append")
    update_task.set_defaults(func=command_update_task)

    start = sub.add_parser("start")
    start.add_argument("title")
    start.add_argument("--owner")
    start.add_argument("--repo")
    start.add_argument("--workflow")
    start.add_argument("--verification")
    start.add_argument("--files", action="append")
    start.add_argument("--out-of-scope", action="append")
    start.set_defaults(func=command_start)

    claim = sub.add_parser("claim")
    claim.add_argument("paths", nargs="+")
    claim.add_argument("--owner")
    claim.add_argument("--reason", default="active implementation")
    claim.set_defaults(func=command_claim)

    handoff = sub.add_parser("handoff")
    handoff.add_argument("--from-owner")
    handoff.add_argument("--to", required=True)
    handoff.add_argument("--files", action="append")
    handoff.add_argument("--acceptance", required=True)
    handoff.add_argument("--verification")
    handoff.add_argument("--notes")
    handoff.set_defaults(func=command_handoff)

    delegate = sub.add_parser("delegate")
    delegate.add_argument("description")
    delegate.add_argument("--to")
    delegate.add_argument("--from-owner")
    delegate.add_argument("--files", action="append")
    delegate.add_argument("--acceptance")
    delegate.add_argument("--verification")
    delegate.add_argument("--notes")
    delegate.set_defaults(func=command_delegate)

    finish = sub.add_parser("finish")
    finish.add_argument("result", choices=["done", "parked", "killed"])
    finish.add_argument("--verification")
    finish.set_defaults(func=command_finish)

    sub.add_parser("kanban-snapshot").set_defaults(func=command_kanban_snapshot)

    sub.add_parser("check").set_defaults(func=command_check)

    sub.add_parser("doctor").set_defaults(func=command_doctor)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
