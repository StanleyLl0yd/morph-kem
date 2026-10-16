"""Offline safety cases for one-time preservation of divergent Git branches."""
import importlib.util
import sys
import unittest
from pathlib import Path

file = Path(__file__).resolve().parents[1] / "scripts" / "archive_legacy_branches.py"
spec = importlib.util.spec_from_file_location("archive_legacy_branches", file)
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


class ArchiveLegacyBranchTests(unittest.TestCase):
    def test_allowlist_is_exactly_eight_unique_non_main_branches(self):
        self.assertEqual(mod.validate_records(), 8)
        self.assertEqual(len({r[0] for r in mod.RECORDS}), 8)
        self.assertEqual(len({r[2] for r in mod.RECORDS}), 8)

    def test_delete_requires_verified_matching_durable_tag(self):
        k = lambda **kw: mod.safe_for_deletion(
            "old", "a" * 40, kw.get("actual_sha", "a" * 40),
            kw.get("protected", False), kw.get("open_prs", []),
            kw.get("default_branch", "main"),
            kw.get("tag_sha", "a" * 40),
        )
        self.assertTrue(k())
        self.assertFalse(k(tag_sha=None))
        self.assertFalse(k(tag_sha="b" * 40))
        self.assertFalse(k(actual_sha="b" * 40))
        self.assertFalse(k(open_prs=[{"number": 1}]))
        self.assertFalse(k(protected=True))
        self.assertFalse(k(default_branch="old"))

    def test_reject_unsafe_manifest(self):
        with self.assertRaises(ValueError):
            mod.validate_records((("main", "a" * 40,
                                   "archive/2026-10-16/main"),))
        with self.assertRaises(ValueError):
            mod.validate_records((mod.RECORDS[0], mod.RECORDS[0]))
        with self.assertRaises(ValueError):
            mod.validate_records((("example", "bad",
                                   "archive/2026-10-16/example"),))


if __name__ == "__main__":
    unittest.main()
