#!/usr/bin/env python3
"""One-time archival cleanup: create exact Git tags BEFORE removing old branches.

Never force or move an existing tag. No deletion before a durable remote tag is
re-read and verified to point to the branch's exact expected commit. The
allowlist is deliberately immutable and narrowly scoped to the eight
divergent legacy branches reviewed on 2026-10-16.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen

REPOSITORY = "StanleyLl0yd/morph-kem"
RECORDS = (
    ("g1/hges-cycle-gluing", "a930b26827c3f6a2d337af791eabe8f43e6154ba", "archive/2026-10-16/g1/hges-cycle-gluing"),
    ("g14/stacked-sphere-reverse-normalization", "bf3f35ef1f36e4368b52235a7c2b1d39ddfb94d8", "archive/2026-10-16/g14/stacked-sphere-reverse-normalization"),
    ("hga1/markoff-navigation-control", "77a1d11bb4da93799f3274d6a2ef265ac3bc555b", "archive/2026-10-16/hga1/markoff-navigation-control"),
    ("hga4f/adaptive-representation-ensemble", "0ec0fe3476464028399fbdf74cdbae2b6c084220", "archive/2026-10-16/hga4f/adaptive-representation-ensemble"),
    ("nat7/public-tree-gauge-normalization-clean", "bd9a8cd959a50e75e17365485645b946cf6a8f0d", "archive/2026-10-16/nat7/public-tree-gauge-normalization-clean"),
    ("research/n1-56-57-no-go-20261014", "bdd26a26d4baec950d39b13cb055ac3638385ba1", "archive/2026-10-16/research/n1-56-57-no-go-20261014"),
    ("tdc2f/rank-matched-kernel-control", "27824f521b5d813211b7df3a18c3511604e43c48", "archive/2026-10-16/tdc2f/rank-matched-kernel-control"),
    ("tdc3/matched-decoder-work", "0dda0e1eb023424ef0d4d4f01d7674b2163eeb56", "archive/2026-10-16/tdc3/matched-decoder-work"),
)


def validate_records(records=RECORDS):
    branches = set()
    tags = set()
    for branch, sha, tag in records:
        if (not branch or branch == "main" or branch in branches or
                not re.fullmatch(r"[a-f0-9]{40}", sha) or
                not tag.startswith("archive/2026-10-16/") or
                tag != "archive/2026-10-16/" + branch or tag in tags):
            raise ValueError("Invalid archive allowlist; refusing mutation")
        branches.add(branch)
        tags.add(tag)
    return len(branches)


def safe_for_deletion(branch, expected_sha, actual_sha, protected,
                      open_pull_requests, default_branch, tag_target_sha):
    """Pure conservative gate; the remote tag MUST already exist and match."""
    return (branch != default_branch and actual_sha == expected_sha and
            not protected and not open_pull_requests and
            tag_target_sha == expected_sha)


class APIError(Exception):
    def __init__(self, method, path, code, detail):
        super().__init__(f"{method} {path}: HTTP {code}: {detail}")
        self.code = code


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    validate_records()
    token = os.environ.get("GITHUB_TOKEN")
    if not token or os.environ.get("GITHUB_REPOSITORY") != REPOSITORY:
        raise SystemExit("Missing token or repository mismatch")

    def api(path, method="GET", payload=None, missing_ok=False):
        req = Request(
            "https://api.github.com/" + path.lstrip("/"),
            method=method,
            data=json.dumps(payload).encode("utf-8") if payload is not None else None,
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {token}",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "MORPH-KEM-legacy-branch-archiver",
                **({"Content-Type": "application/json"} if payload is not None else {}),
            },
        )
        try:
            with urlopen(req, timeout=30) as response:
                data = response.read()
                return json.loads(data) if data else None
        except HTTPError as e:
            if missing_ok and e.code == 404:
                return None
            raise APIError(method, path, e.code,
                           e.read().decode("utf-8", errors="replace")[:400]) from None

    metadata = api(f"repos/{REPOSITORY}")
    default_branch = metadata["default_branch"]
    if default_branch != "main":
        raise SystemExit("Default branch changed: refuse archival deletion")

    count_archived = count_deleted = count_already_deleted = 0
    for name, expected, tag in RECORDS:
        branch_path = f"repos/{REPOSITORY}/branches/{quote(name, safe='/')}"
        tag_path = f"repos/{REPOSITORY}/git/ref/tags/{quote(tag, safe='/')}"
        ref_path = f"repos/{REPOSITORY}/git/refs/heads/{quote(name, safe='/')}"
        branch = api(branch_path, missing_ok=True)
        existing_tag = api(tag_path, missing_ok=True)
        tag_sha = (existing_tag or {}).get("object", {}).get("sha")
        if existing_tag and (tag_sha != expected or
                             (existing_tag.get("object") or {}).get("type") != "commit"):
            raise RuntimeError(f"STOP: archived tag {tag} points elsewhere")
        if not branch:
            if tag_sha == expected:
                print(f"ALREADY ARCHIVED/DELETED {name}: {tag} -> {expected}")
                count_already_deleted += 1
                continue
            raise RuntimeError(f"STOP: branch {name} missing without expected tag")
        if branch["commit"]["sha"] != expected or branch.get("protected"):
            raise RuntimeError(f"STOP: branch moved/protected: {name}")

        owner = REPOSITORY.split("/")[0]
        head_filter = quote(owner + ":" + name, safe="")
        open_prs = api(
            f"repos/{REPOSITORY}/pulls?state=open&head={head_filter}&per_page=100"
        )
        if open_prs:
            raise RuntimeError(f"STOP: open pull request on {name}")

        if not args.apply:
            print(f"DRY-RUN {name} {expected} -> tag {tag}")
            continue
        if not existing_tag:
            api(
                f"repos/{REPOSITORY}/git/refs", "POST",
                {"ref": "refs/tags/" + tag, "sha": expected},
            )
        observed = api(tag_path)
        tag_sha = (observed.get("object") or {}).get("sha")
        tag_type = (observed.get("object") or {}).get("type")
        if tag_sha != expected or tag_type != "commit":
            raise RuntimeError(f"STOP: tag verification failure: {name}")
        count_archived += 1

        # Last checks: re-read branch, check no new PR, retain exact tag.
        current = api(branch_path)
        open_prs = api(
            f"repos/{REPOSITORY}/pulls?state=open&head={head_filter}&per_page=100"
        )
        if not safe_for_deletion(
            name, expected, current["commit"]["sha"], current.get("protected"),
            open_prs, default_branch, tag_sha
        ):
            raise RuntimeError(f"STOP: branch not safe for removal: {name}")
        api(ref_path, "DELETE")
        if api(branch_path, missing_ok=True):
            raise RuntimeError(f"STOP: branch still exists after DELETE: {name}")
        print(f"ARCHIVED + DELETED {name}: {tag} -> {expected}")
        count_deleted += 1

    print(f"RESULT: archived={count_archived}; deleted={count_deleted}; "
          f"already_archived_deleted={count_already_deleted}; dry_run={not args.apply}")


if __name__ == "__main__":
    try:
        main()
    except (APIError, ValueError, RuntimeError) as exc:
        print(f"FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)
