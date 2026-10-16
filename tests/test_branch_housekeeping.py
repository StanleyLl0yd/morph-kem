"""Offline deterministic tests for conservative branch cleanup planner."""
import importlib.util
import os
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location(
    "branch_housekeeping",
    Path(__file__).resolve().parents[1] / "scripts" / "branch_housekeeping.py",
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def b(name, sha, protected=False):
    return {"name": name, "commit": {"sha": sha}, "protected": protected}


def p(name, sha, merged=True, state="closed", origin="StanleyLl0yd/morph-kem"):
    return {"head": {"ref": name, "sha": sha, "repo": {"full_name": origin}},
            "merged_at": "2026-10-16T00:00:00Z" if merged else None,
            "state": state}


class BranchHousekeepingTest(unittest.TestCase):
    def setUp(self):
        self.old = os.environ.get("GITHUB_REPOSITORY")
        os.environ["GITHUB_REPOSITORY"] = "StanleyLl0yd/morph-kem"

    def tearDown(self):
        if self.old is None:
            os.environ.pop("GITHUB_REPOSITORY", None)
        else:
            os.environ["GITHUB_REPOSITORY"] = self.old

    def test_merged_exact_head_and_ancestral_no_pr_only(self):
        rows = [b("main", "MAIN", True), b("merged", "A"),
                b("stale", "B"), b("diverged", "C"),
                b("closed", "D"), b("advanced", "E"),
                b("open", "F"), b("protected", "G", True)]
        prs = [p("merged", "A"), p("closed", "D", merged=False),
               p("advanced", "OLD"), p("open", "F", state="open", merged=False)]
        picked, skipped = mod.plan(
            rows, prs, "main", "MAIN", lambda old, main: old == "B"
        )
        self.assertEqual([x[0] for x in picked], ["merged", "stale"])
        self.assertEqual(len(skipped), 6)

    def test_skipped_reporting_matches_planner_shape(self):
        rows = [b("main", "MAIN", True), b("unique", "X")]
        selected, skipped = mod.plan(
            rows, [], "main", "MAIN", lambda *_: False
        )
        self.assertEqual(selected, [])
        self.assertEqual(
            mod.format_skipped(skipped),
            ["KEEP main: default/protected",
             "KEEP unique: unmerged/untracked commits"],
        )

    def test_closed_unmerged_and_external_pr_not_auto_deleted(self):
        rows = [b("old", "X"), b("fork", "Y")]
        prs = [p("old", "X", merged=False), p("fork", "Y", origin="other/repo")]
        picked, skipped = mod.plan(rows, prs, "main", "MAIN", lambda *_: False)
        self.assertEqual(picked, [])
        self.assertEqual(len(skipped), 2)


if __name__ == "__main__":
    unittest.main()
