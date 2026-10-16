#!/usr/bin/env python3
"""Conservative GitHub branch cleanup. No dependency beyond Python stdlib.

Only prune:
1. branches at the exact SHA of an already MERGED same-repository PR; or
2. branches with no associated PR and with a tip already ancestral to main.

Never prune open-PR, closed-unmerged, protected, advanced or otherwise
ambiguous branches. Re-fetch SHA/protection before deleting.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen


def list_pages(api, path):
    collected = []
    for page in range(1, 100):
        rows = api(f"{path}{'&' if '?' in path else '?'}per_page=100&page={page}")
        if not isinstance(rows, list):
            raise RuntimeError(f"Expected list from {path}")
        collected.extend(rows)
        if len(rows) < 100:
            return collected
    raise RuntimeError(f"Unexpected pagination limit for {path}: aborting safely")


def plan(branches, pulls, default_branch, main_sha, is_ancestor):
    """Pure planner: return [(name, expected_sha, reason)] and skipped names."""
    by_name = {}
    for pr in pulls:
        head = pr.get("head") or {}
        origin = head.get("repo") or {}
        if origin.get("full_name") != os.environ["GITHUB_REPOSITORY"]:
            continue
        by_name.setdefault(head.get("ref"), []).append(pr)

    chosen, skipped = [], []
    for b in branches:
        name, sha = b["name"], b["commit"]["sha"]
        if name == default_branch or b.get("protected"):
            skipped.append((name, "default/protected"))
            continue
        related = by_name.get(name, [])
        if any(pr.get("state") == "open" for pr in related):
            skipped.append((name, "open PR"))
            continue
        if related:
            matching_merged = [
                pr for pr in related
                if pr.get("merged_at") and (pr.get("head") or {}).get("sha") == sha
            ]
            if matching_merged:
                chosen.append((name, sha, "exact merged PR head"))
            else:
                skipped.append((name, "PR closed-unmerged or SHA differs"))
        elif is_ancestor(sha, main_sha):
            chosen.append((name, sha, "no PR; already contained in main"))
        else:
            skipped.append((name, "unmerged/untracked commits"))
    return chosen, skipped


def format_skipped(skipped):
    """Display the (name, reason) pairs produced by the conservative planner."""
    return [f"KEEP {name}: {reason}" for name, reason in skipped]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true",
                        help="Perform deletion (default is dry-run)")
    args = parser.parse_args()
    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPOSITORY")
    if not token or not repo or repo != "StanleyLl0yd/morph-kem":
        raise SystemExit("Missing token or repository mismatch; refusing to run")

    def api(path, method="GET"):
        url = "https://api.github.com/" + path.lstrip("/")
        req = Request(url, method=method, headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "MORPH-KEM-branch-housekeeping",
        })
        try:
            with urlopen(req, timeout=30) as response:
                data = response.read()
                return json.loads(data) if data else None
        except HTTPError as e:
            detail = e.read().decode("utf-8", errors="replace")[:500]
            raise RuntimeError(f"{method} {path}: HTTP {e.code} {detail}") from None

    repository = api(f"repos/{repo}")
    default = repository["default_branch"]
    main_branch = api(f"repos/{repo}/branches/{quote(default, safe='')}")
    main_sha = main_branch["commit"]["sha"]
    branches = list_pages(api, f"repos/{repo}/branches")
    pulls = list_pages(api, f"repos/{repo}/pulls?state=all")

    def ancestor(branch_sha, expected_main):
        data = api(f"repos/{repo}/compare/{branch_sha}...{expected_main}")
        return data["behind_by"] == 0 and data["status"] in ("ahead", "identical")

    chosen, skipped = plan(branches, pulls, default, main_sha, ancestor)
    print(f"main={main_sha}; branches={len(branches)}; PRs={len(pulls)}; "
          f"eligible={len(chosen)}; protected/ambiguous={len(skipped)}")
    for line in format_skipped(skipped):
        print(line)

    errors, deleted = [], []
    for name, expected_sha, reason in chosen:
        if not args.apply:
            print(f"DRY-RUN DELETE {name} {expected_sha}: {reason}")
            continue
        try:
            current = api(f"repos/{repo}/branches/{quote(name, safe='/')}")
            if current["commit"]["sha"] != expected_sha or current.get("protected"):
                print(f"SKIP CHANGED/PROTECTED {name}")
                continue
            # An open PR may have appeared since the first pagination snapshot.
            owner = repo.split("/")[0]
            open_prs = api(
                f"repos/{repo}/pulls?state=open&head={quote(owner + ':' + name, safe='')}&per_page=100"
            )
            if open_prs:
                print(f"SKIP OPEN PR {name}")
                continue
            api(f"repos/{repo}/git/refs/heads/{quote(name, safe='/')}", "DELETE")
            deleted.append(name)
            print(f"DELETED {name}: {reason}")
        except RuntimeError as exc:
            errors.append((name, str(exc)))
            print(f"FAILED {name}: {exc}", file=sys.stderr)
            if "HTTP 403" in str(exc):
                break
    print(f"RESULT: deleted={len(deleted)}; retained={len(skipped)}; "
          f"errors={len(errors)}; apply={args.apply}")
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
