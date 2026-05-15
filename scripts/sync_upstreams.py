#!/usr/bin/env python3
"""
Sync curated skills from upstream sources.

Reads sources.json, compares local files with upstream, and reports drift.
Batches API calls by repo to avoid rate limits.

Usage:
    python3 scripts/sync_upstreams.py               # dry-run
    python3 scripts/sync_upstreams.py --apply        # fetch changes
    python3 scripts/sync_upstreams.py --pr           # PR body output
"""
import json
import sys
import hashlib
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from collections import defaultdict
from typing import Optional, List, Dict

ROOT = Path(__file__).parent.parent
SOURCES = ROOT / "sources.json"
SKILLS_DIR = ROOT / "skills"
GITHUB_API = "https://api.github.com/repos"
GITHUB_RAW = "https://raw.githubusercontent.com"


def fetch_json(url: str, timeout: int = 30) -> dict:
    req = Request(url, headers={"User-Agent": "sync-upstreams/1.0"})
    with urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


def fetch_text(url: str, timeout: int = 30) -> Optional[str]:
    try:
        req = Request(url, headers={"User-Agent": "sync-upstreams/1.0"})
        with urlopen(req, timeout=timeout) as resp:
            return resp.read().decode()
    except HTTPError as e:
        if e.code == 404:
            return None
        raise


def fetch_repo_tree(repo: str, ref: str) -> Dict[str, str]:
    url = f"{GITHUB_API}/{repo}/git/trees/{ref}?recursive=1"
    data = fetch_json(url, timeout=60)
    tree = {}
    for item in data.get("tree", []):
        if item["type"] == "blob":
            tree[item["path"]] = item["sha"]
    return tree


def file_hash(content: str) -> str:
    return hashlib.sha256(content.encode()).hexdigest()[:16]


def load_sources() -> dict:
    if not SOURCES.exists():
        print("sources.json not found")
        return {}
    with open(SOURCES) as f:
        return json.load(f)


def main() -> int:
    dry_run = "--apply" not in sys.argv
    pr_mode = "--pr" in sys.argv
    raw = load_sources()
    sources = {k: v for k, v in raw.items() if not k.startswith("//")}

    # Group by repo for batch tree fetch
    by_repo = defaultdict(list)
    for name, src in sources.items():
        by_repo[src["repo"]].append({
            "name": name,
            "ref": src.get("ref", "main"),
            "path": src["path"],
        })

    changes = []

    for repo, skills in sorted(by_repo.items()):
        ref = skills[0]["ref"]
        print(f"\n  Tree: {repo}@{ref}")
        tree = fetch_repo_tree(repo, ref)

        for skill in skills:
            name = skill["name"]
            prefix = skill["path"]
            local_dir = SKILLS_DIR / name
            up_prefix = f"{prefix}/"
            upstream = {k: v for k, v in tree.items() if k.startswith(up_prefix)}

            if not local_dir.exists() and dry_run:
                print(f"  {name}: NEW")
                changes.append({"skill": name, "status": "NEW", "files": []})
                continue
            elif not local_dir.exists():
                print(f"  {name}: NEW")
                local_dir.mkdir(parents=True)
                changes.append({"skill": name, "status": "NEW", "files": ["all"]})
            else:
                print(f"  {name}:")

            diff = []
            for up_path in sorted(upstream):
                rel = up_path[len(up_prefix):]
                local_path = local_dir / rel
                url = f"{GITHUB_RAW}/{repo}/{ref}/{up_path}"
                content = fetch_text(url)
                if content is None:
                    continue
                up_hash = file_hash(content)

                if not local_path.exists():
                    diff.append(f"    + {rel}")
                    if not dry_run:
                        local_path.parent.mkdir(parents=True, exist_ok=True)
                        local_path.write_text(content)
                    continue

                local_hash = file_hash(local_path.read_text())
                if local_hash != up_hash:
                    diff.append(f"    ~ {rel}")
                    if not dry_run:
                        local_path.write_text(content)

            if diff:
                print("\n".join(diff))
                changes.append({"skill": name, "status": "CHANGED", "files": diff})
            else:
                print("    up-to-date")

    # Summary
    print(f"\n{'='*50}")
    print(f"Drift: {len(changes)} skill(s)")
    for c in changes:
        print(f"  {c['skill']}: {c['status']}")
    print(f"{'='*50}")

    if dry_run and changes:
        print(f"\nRun with --apply to fetch changes.")
    elif not changes:
        print("All up-to-date.")

    if pr_mode and changes:
        print("\n--- PR Body ---")
        print("## Upstream Sync\n")
        print("| Skill | Status | Files |")
        print("|---|---|---|")
        for c in changes:
            print(f"| {c['skill']} | {c['status']} | {len(c['files'])} |")

    return 1 if changes else 0


if __name__ == "__main__":
    sys.exit(main())
