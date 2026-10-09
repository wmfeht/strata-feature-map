import json
import tempfile
import unittest
from pathlib import Path

import yaml

import featuremap as fm

SHA = "b8938864dc95d2e041a0a442b3b7a63755681f4e"
OLD_SHA = "8a481e80" + "0" * 32
HISTORY = "| Date | PR | Type | Change |\n| --- | --- | --- | --- |\n"


def feature(meta=None, sections=None, drop=()):
    m = {
        "title": "Trash",
        "status": "shipped",
        "origin": {"issue": None, "pr": "lgse/strata#1"},
        "branch": None,
        "reviewed_at": SHA,
        "review": "draft",
        "code": ["src/trash.rs"],
        "tests": ["src/trash/tests.rs"],
        "docs": ["docs/trash.md"],
        "related": [],
    }
    m.update(meta or {})
    for key in drop:
        m.pop(key)
    s = {
        "Summary": "Moves files to the trash.",
        "Behavior": "- Delete moves the selection to the trash. lgse/strata#1",
        "Design": "Follows the freedesktop trash specification.",
        "History": HISTORY + "| 2026-09-01 | lgse/strata#1 | feat | Added trash. |",
        "Known gaps": "None known.",
    }
    s.update(sections or {})
    body = "".join(f"## {name}\n\n{text}\n\n" for name, text in s.items() if text is not None)
    return "---\n" + yaml.safe_dump(m, sort_keys=False) + "---\n\n" + body


RESTORE = feature(
    {"title": "Restore", "origin": {"issue": None, "pr": "lgse/strata#2"}, "code": ["src/trash/restore.rs"],
     "tests": ["src/trash/restore/**"], "docs": []},
    {
        "Behavior": "- Restore returns an item to its original folder. lgse/strata#2",
        "History": HISTORY + "| 2026-09-02 | lgse/strata#2 | feat | Added restore. |",
    },
)


class Fixture:
    def __init__(self, files=None):
        self.dir = tempfile.TemporaryDirectory()
        self.root = Path(self.dir.name)
        defaults = {
            "sources.yaml": "upstream: {repo: lgse/strata, branch: main}\nwatermark: null\n",
            "scopes.yaml": "ignore: [deps]\nscopes:\n  trash: operations/trash\n  browser: null\n",
            "features/operations/trash/index.md": feature(),
            "features/operations/trash/restore.md": RESTORE,
        }
        defaults.update(files or {})
        for rel, text in defaults.items():
            if text is not None:
                self.write(rel, text)

    def write(self, rel, text):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def issues(self, lister=None, level="error"):
        return [str(i) for i in fm.check(self.root, lister) if i.level == level]

    def close(self):
        self.dir.cleanup()


class CheckTest(unittest.TestCase):
    def fixture(self, files=None, index=True):
        f = Fixture(files)
        self.addCleanup(f.close)
        if index:
            fm.write_index(f.root)
        return f

    def test_valid_tree_passes(self):
        f = self.fixture()
        self.assertEqual(f.issues(), [])
        self.assertEqual(f.issues(level="warning"), [])

    def test_rejections(self):
        restore ="features/operations/trash/restore.md"
        cases = [
            ({restore: feature(sections={"Design": None})}, "missing section(s): Design"),
            ({restore: feature(sections={"Extra": "x"})}, "unexpected section(s): Extra"),
            ({restore: "---\ntitle: x\n---\n# Title\n"}, "no '#' title"),
            ({restore: feature(sections={"Behavior": "- Restores files."})}, "lacks a trailing citation"),
            ({restore: feature(sections={"Behavior": "- A. lgse/strata#2\n  - nested. lgse/strata#2"})},
             "allows only '- ' bullets"),
            ({restore: feature({"status": "done"})}, "status must be one of"),
            ({restore: feature({"review": "ok"})}, "review must be one of"),
            ({restore: feature({"id": "operations/trash/restore"})}, "id is derived from the path"),
            ({restore: feature({"owner": "me"})}, "unknown field 'owner'"),
            ({restore: feature(drop=["tests"])}, "missing field 'tests'"),
            ({restore: feature({"reviewed_at": "b893886"})}, "full 40-character SHA"),
            ({restore: feature({"origin": {"issue": None, "pr": None}})}, "origin needs an issue or a PR"),
            ({restore: feature({"origin": {"pr": "#12", "issue": None}})}, "origin.pr must be owner/repo#n"),
            ({restore: feature({"branch": "feat/12-x"})}, "branch must be null"),
            ({restore: feature({"status": "in-progress"})}, "branch is required"),
            ({restore: feature({"code": "src/trash.rs"})}, "code must be a list"),
            ({restore: feature({"related": ["operations/nope"]})}, "related id 'operations/nope' does not exist"),
            ({restore: feature({"related": ["operations/trash/restore"]})}, "related lists the node itself"),
            ({restore: feature({"origin": {"issue": None, "pr": "lgse/strata#2"}},
                               {"History": HISTORY + "| 2026-09-02 | lgse/strata#2 | feat | Added restore. |"})},
             "Behavior bullet also in ancestor operations/trash"),
            ({restore: feature(sections={"Behavior": "- Other. lgse/strata#2"})},
             "lgse/strata#1 also has a History row on ancestor operations/trash"),
            ({restore: feature(sections={"Behavior": "- Other. lgse/strata#2", "History": HISTORY})},
             None),
            ({restore: feature(sections={"Behavior": "- Other. lgse/strata#2", "History": "Added in #2."})},
             "History must be a single table"),
            ({restore: feature(sections={"Behavior": "- Other. lgse/strata#2", "History": HISTORY
                                         + "| 2026-09-01 | lgse/strata#3 | fix | A. |\n"
                                         + "| 2026-09-02 | lgse/strata#4 | fix | B. |"})},
             "newest first"),
            ({restore: feature(sections={"Behavior": "- Other. lgse/strata#2", "History": HISTORY
                                         + "| 2026-09-01 | lgse/strata#3 | bugfix | A. |"})},
             "Type must be one of"),
            ({restore: feature(sections={"Behavior": "- Other. lgse/strata#2", "History": HISTORY
                                         + "| 2026-09-01 | #3 | fix | A. |"})},
             "PR must be owner/repo#n"),
            ({restore: feature(sections={"Behavior": "- Other. lgse/strata#2", "Known gaps": "- No undo."})},
             "Known gaps bullet must cite an issue"),
            ({restore: feature(sections={"Behavior": "- Other. lgse/strata#2", "Known gaps": ""})},
             "Known gaps is empty"),
            ({restore: feature(sections={"Behavior": "", "History": HISTORY})}, "a shipped leaf needs Behavior"),
            ({"features/operations/trash.md": feature()}, "trash.md and trash/ both define one id"),
            ({"features/operations/empty/notes.md": RESTORE}, "directory without index.md"),
            ({"features/trash.md": RESTORE}, "no files directly under features/"),
            ({"features/operations/index.md": RESTORE}, "an area has no index.md"),
            ({"features/operations/trash/notes.txt": "x"}, "only Markdown files"),
            ({"scopes.yaml": "scopes:\n  trash: operations/gone\n"}, "maps to missing node 'operations/gone'"),
            ({"scopes.yaml": "ignore: [trash]\nscopes:\n  trash: operations/trash\n"}, "both mapped and ignored"),
            ({"sources.yaml": "upstream: {repo: lgse/strata}\nwatermark: abc\n"}, "watermark must be null"),
        ]
        for files, expected in cases:
            with self.subTest(expected=expected):
                issues = self.fixture(files).issues()
                if expected is None:
                    self.assertEqual(issues, [])
                else:
                    self.assertTrue(any(expected in i for i in issues), issues)

    def test_unverified_and_multiple_citations_are_accepted(self):
        behavior = "- Restore refuses a missing parent. lgse/strata#2, lgse/strata#777 (unverified)"
        f = self.fixture({"features/operations/trash/restore.md": feature(sections={
            "Behavior": "### Safety\n\n" + behavior + "\n- Wrapped across\n  two lines. lgse/strata#2",
            "History": HISTORY})})
        self.assertEqual(f.issues(), [])

    def test_depth_beyond_grandchild_warns(self):
        f = self.fixture({
            "features/a/b/index.md": feature(sections={"Behavior": "- B. lgse/strata#1"}),
            "features/a/b/c/index.md": feature(sections={"Behavior": "- C. lgse/strata#1", "History": HISTORY}),
            "features/a/b/c/d/index.md": feature(sections={"Behavior": "- D. lgse/strata#1", "History": HISTORY}),
            "features/a/b/c/d/e.md": feature(sections={"Behavior": "- E. lgse/strata#1", "History": HISTORY}),
        })
        self.assertEqual(f.issues(), [])
        self.assertTrue(any("deeper than" in i and "e.md" in i for i in f.issues(level="warning")))

    def test_stale_index_is_reported_until_regenerated(self):
        f = self.fixture()
        f.write("features/operations/trash/index.md", feature({"title": "Bin"}))
        self.assertTrue(any("stale index" in i for i in f.issues()))
        fm.write_index(f.root)
        self.assertEqual(f.issues(), [])
        self.assertIn("[Bin](features/operations/trash/index.md)", (f.root / "README.md").read_text())

    def test_upstream_paths_must_exist_at_reviewed_at(self):
        f = self.fixture()
        present = {"src/trash.rs", "src/trash/tests.rs", "docs/trash.md", "src/trash/restore.rs"}
        self.assertTrue(any("'src/trash/restore/**' matches nothing" in i for i in f.issues(lambda sha: present)))
        present.add("src/trash/restore/tests.rs")
        self.assertEqual(f.issues(lambda sha: present), [])
        self.assertTrue(any("is not an upstream commit" in i for i in f.issues(lambda sha: None)))


class GlobTest(unittest.TestCase):
    def test_matching(self):
        cases = [
            ("src/trash.rs", "src/trash.rs", True),
            ("src/trash.rs", "src/trash.rs.bak", False),
            ("src/trash", "src/trash/tests.rs", True),
            ("src/trash", "src/trash_restore.rs", False),
            ("src/trash*", "src/trash_restore.rs", True),
            ("src/trash*", "src/trash/tests.rs", False),
            ("src/trash/**", "src/trash/a/b.rs", True),
            ("src/**/tests.rs", "src/tests.rs", True),
            ("src/**/tests.rs", "src/a/b/tests.rs", True),
            ("tests/e2e/test_?.py", "tests/e2e/test_a.py", True),
        ]
        for pattern, path, expected in cases:
            with self.subTest(pattern=pattern, path=path):
                self.assertEqual(fm.matches(pattern, path), expected)


class AssignTest(unittest.TestCase):
    def setUp(self):
        self.fixture = Fixture({
            "features/operations/trash/fly.md": feature(
                {"code": ["src/ui/fly.rs"], "tests": []},
                {"Behavior": "- Fly. lgse/strata#3", "History": HISTORY}),
            "features/browser/tabs.md": feature(
                {"code": ["src/ui/tabs.rs"], "tests": []},
                {"Behavior": "- Tabs. lgse/strata#4", "History": HISTORY}),
        })
        self.addCleanup(self.fixture.close)
        self.tree = fm.load_tree(self.fixture.root)
        self.scopes = fm.load_scopes(self.fixture.root)

    def test_assignment(self):
        cases = [
            ("trash", ["src/trash/restore.rs", "src/trash.rs"], "operations/trash/restore"),
            ("trash", ["README.md"], "operations/trash"),
            ("trash", ["src/trash/restore.rs", "src/ui/fly.rs"], "operations/trash"),
            ("trash", ["src/ui/tabs.rs"], "operations/trash"),
            (None, ["src/ui/tabs.rs"], "browser/tabs"),
            ("browser", ["src/ui/other.rs"], None),
            ("newscope", ["src/ui/other.rs"], None),
            (None, ["src/ui/tabs.rs", "src/ui/fly.rs"], None),
            ("deps", ["src/trash.rs"], None),
        ]
        for scope, files, expected in cases:
            with self.subTest(scope=scope, files=files):
                result = fm.assign(self.tree, self.scopes, {"scope": scope, "files": files})
                self.assertEqual(result.node, expected, result.reason)

    def test_affected_lists_every_touched_node(self):
        result = fm.assign(self.tree, self.scopes, {"scope": "deps", "files": ["src/trash.rs", "src/ui/tabs.rs"]})
        self.assertEqual(result.affected, ["browser/tabs", "operations/trash"])
        self.assertIn("ignored", result.reason)


class IndexTest(unittest.TestCase):
    def test_prs_since_review_counts_subtree_changes(self):
        f = Fixture({"features/operations/trash/restore.md": RESTORE.replace(SHA, OLD_SHA)})
        self.addCleanup(f.close)
        rows = [
            {"number": 10, "merge_commit": OLD_SHA, "merged_at": "2026-09-01T00:00:00Z", "files": []},
            {"number": 11, "merge_commit": SHA, "merged_at": "2026-09-05T00:00:00Z", "files": []},
            {"number": 12, "merged_at": "2026-09-03T00:00:00Z", "files": ["src/trash/restore.rs"]},
            {"number": 13, "merged_at": "2026-09-06T00:00:00Z", "files": ["src/trash.rs"]},
            {"number": 14, "merged_at": "2026-09-07T00:00:00Z", "files": ["src/unrelated.rs"]},
        ]
        f.write("data/prs.jsonl", "".join(json.dumps(r) + "\n" for r in rows))
        tree = fm.load_tree(f.root)
        dataset = fm.load_dataset(f.root)
        self.assertEqual(fm.changes_since(tree, "operations/trash/restore", dataset), "1")
        self.assertEqual(fm.changes_since(tree, "operations/trash", dataset), "2")
        self.assertEqual(fm.changes_since(tree, "operations/trash", {}), "?")

    def test_indexes_link_paths_at_reviewed_at_and_list_history(self):
        f = Fixture()
        self.addCleanup(f.close)
        fm.write_index(f.root)
        by_path = (f.root / "index/by-path.md").read_text()
        self.assertIn("| `src/trash/restore/**` | tests | [Restore](../features/operations/trash/restore.md) | "
                      "[Trash](../features/operations/trash/index.md) |", by_path)
        by_area = (f.root / "index/by-area.md").read_text()
        self.assertIn(f"https://github.com/lgse/strata/tree/{SHA}/src/trash/restore", by_area)
        self.assertIn("(inherited)", by_area)
        by_pr = (f.root / "index/by-pr.md").read_text().splitlines()
        self.assertLess(by_pr.index(next(l for l in by_pr if "lgse/strata#2" in l)),
                        by_pr.index(next(l for l in by_pr if "lgse/strata#1" in l)))


class ParsingTest(unittest.TestCase):
    def test_title(self):
        self.assertEqual(fm.parse_title("fix(trash): refuse restore (#913)"),
                         ("fix", "trash", False, "refuse restore (#913)"))
        self.assertEqual(fm.parse_title("feat!: drop X"), ("feat", None, True, "drop X"))
        self.assertEqual(fm.parse_title("Merge pull request #547"), (None, None, False, "Merge pull request #547"))

    def test_pr_section(self):
        body = ("## Description\n\nRefuses restore.\n<!-- hint -->\n\n### Details\n\nmore\n\n"
                "## How to test\n\n1. Trash a file.\n\n## Related issue\n\nCloses #1")
        self.assertEqual(fm.pr_section(body, "Description"), "Refuses restore.\n\n### Details\n\nmore")
        self.assertEqual(fm.pr_section(body, "How to test"), "1. Trash a file.")
        self.assertEqual(fm.pr_section(body, "Visual evidence"), "")


if __name__ == "__main__":
    unittest.main()
