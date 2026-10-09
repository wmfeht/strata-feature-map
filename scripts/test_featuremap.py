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


def sweep(meta=None, sections=None, drop=()):
    m = {"title": "Operations sweep", "reviewed_at": SHA}
    m.update(meta or {})
    for key in drop:
        m.pop(key)
    s = {
        "Scope": "Trash and restore.",
        "Setup": "- A throwaway HOME so Trash starts empty.",
        "Probes": "- Watch the log for GTK criticals.\n\n### operations/trash\n\n- Trash from each view mode.",
        "Hand-offs": "None.",
    }
    s.update(sections or {})
    body = "".join(f"## {name}\n\n{text}\n\n" for name, text in s.items() if text is not None)
    return "---\n" + yaml.safe_dump(m, sort_keys=False) + "---\n\n" + body


class Fixture:
    def __init__(self, files=None):
        self.dir = tempfile.TemporaryDirectory()
        self.root = Path(self.dir.name)
        defaults = {
            "sources.yaml": "upstream: {repo: lgse/strata, branch: main}\nwatermark: null\n",
            "scopes.yaml": "ignore: [deps]\nscopes:\n  trash: operations/trash\n  browser: null\n",
            "features/operations/trash/index.md": feature(),
            "features/operations/trash/restore.md": RESTORE,
            "qa/sweeps/operations.md": sweep(),
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
            ({"scopes.yaml": "fallback: [app/gone]\nscopes:\n  trash: operations/trash\n"}, "fallback names missing node 'app/gone'"),
            ({"sources.yaml": "upstream: {repo: lgse/strata}\nwatermark: abc\n"}, "watermark must be null"),
        ]
        for files, expected in cases:
            with self.subTest(expected=expected):
                issues = self.fixture(files).issues()
                if expected is None:
                    self.assertEqual(issues, [])
                else:
                    self.assertTrue(any(expected in i for i in issues), issues)

    def test_sweep_rejections(self):
        ops = "qa/sweeps/operations.md"
        cases = [
            ({ops: sweep(drop=["reviewed_at"])}, "missing field 'reviewed_at'"),
            ({ops: sweep({"nodes": ["operations/trash"]})}, "unknown field 'nodes'"),
            ({ops: sweep({"reviewed_at": "b893886"})}, "full 40-character SHA"),
            ({ops: sweep({"triggers": "src/shared.rs"})}, "triggers must be a list"),
            ({ops: sweep({"title": ""})}, "title must be a non-empty string"),
            ({ops: sweep(sections={"Hand-offs": None})}, "missing section(s): Hand-offs"),
            ({ops: sweep(sections={"Evidence": "x"})}, "unexpected section(s): Evidence"),
            ({ops: sweep(sections={"Scope": ""})}, "Scope is empty"),
            ({ops: sweep(sections={"Setup": ""})}, "Setup is empty"),
            ({ops: sweep(sections={"Probes": "### browser/tabs\n\n- Open a tab."})},
             "Probes subheading 'browser/tabs' is not a node under features/operations/"),
            ({ops: sweep(sections={"Probes": "### operations/trash"})}, "Probes subheading 'operations/trash' has no bullets"),
            ({ops: sweep(sections={"Probes": "Some prose."})}, "Probes allows only"),
            ({ops: sweep(sections={"Probes": "- Trash. lgse/strata#1\n  - nested"})}, "Probes allows only"),
            ({ops: sweep(sections={"Hand-offs": "- Tabs to browser"})}, "Hand-off must read"),
            ({ops: sweep(sections={"Hand-offs": "- Tabs → `browser`"})}, "hand-off target 'browser' is not a sweep"),
            ({ops: sweep(sections={"Hand-offs": "- Trash → `operations`"})}, "hand-off lists the sweep itself"),
            ({ops: sweep(sections={"Hand-offs": ""})}, "Hand-offs is empty"),
            ({ops: "## Scope\n\nx\n"}, "missing YAML front matter"),
            ({"qa/sweeps/browser.md": sweep()}, "'browser' is not an area under features/"),
            ({"qa/sweeps/notes.txt": "x"}, "only Markdown files belong under qa/sweeps/"),
            ({ops: sweep(sections={"Probes": "### `operations/trash`\n\n- Backticked heading is fine.",
                                   "Hand-offs": "- Tabs → `operations`."})}, "hand-off lists the sweep itself"),
            ({ops: sweep(sections={"Probes": "### `operations/trash`\n\n- Backticked heading is fine."})}, None),
        ]
        for files, expected in cases:
            with self.subTest(expected=expected):
                issues = self.fixture(files).issues()
                if expected is None:
                    self.assertEqual(issues, [])
                else:
                    self.assertTrue(any(expected in i for i in issues), issues)

    def test_every_area_needs_a_sweep(self):
        f = self.fixture({"qa/sweeps/operations.md": None}, index=False)
        issues = f.issues()
        self.assertIn("error: qa/sweeps/: directory is missing", issues)
        self.assertIn("error: qa/sweeps/: area 'operations' has no sweep; add qa/sweeps/operations.md", issues)
        self.assertFalse(any("stale index" in i for i in issues), issues)

    def test_sweep_paths_must_exist_at_reviewed_at(self):
        f = self.fixture({"qa/sweeps/operations.md": sweep({"triggers": ["src/shared.rs"], "tools": ["docs/qa.md"]})})
        present = {"src/trash.rs", "src/trash/tests.rs", "docs/trash.md", "src/trash/restore.rs",
                   "src/trash/restore/tests.rs"}
        issues = f.issues(lambda sha: present)
        self.assertTrue(any("triggers entry 'src/shared.rs' matches nothing" in i for i in issues), issues)
        self.assertTrue(any("tools entry 'docs/qa.md' matches nothing" in i for i in issues), issues)
        present |= {"src/shared.rs", "docs/qa.md"}
        self.assertEqual(f.issues(lambda sha: present), [])
        self.assertTrue(any("qa/sweeps/operations.md: reviewed_at" in i and "not an upstream commit" in i
                            for i in f.issues(lambda sha: None)))

    def test_trigger_owned_by_a_node_warns(self):
        f = self.fixture({"qa/sweeps/operations.md": sweep({"triggers": ["src/trash*"]})})
        present = {"src/trash.rs", "src/trash/tests.rs", "docs/trash.md", "src/trash/restore.rs",
                   "src/trash/restore/tests.rs"}
        self.assertEqual(f.issues(lambda sha: present), [])
        warnings = f.issues(lambda sha: present, level="warning")
        self.assertTrue(any("trigger 'src/trash*' is already owned by operations/trash" in w for w in warnings), warnings)

    def test_stale_qa_index_is_reported_until_regenerated(self):
        f = self.fixture()
        f.write("qa/sweeps/operations.md", sweep({"title": "Ops"}))
        self.assertTrue(any("stale index" in i and "index/qa.md" in i for i in f.issues()))
        fm.write_index(f.root)
        self.assertEqual(f.issues(), [])
        self.assertIn("[Ops](../qa/sweeps/operations.md)", (f.root / "index/qa.md").read_text())

    def test_unverified_and_multiple_citations_are_accepted(self):
        behavior = "- Restore refuses a missing parent. lgse/strata#2, lgse/strata#777 (unverified)"
        f = self.fixture({"features/operations/trash/restore.md": feature(sections={
            "Behavior": "### Safety\n\n" + behavior + "\n- Wrapped across\n  two lines. lgse/strata#2",
            "History": HISTORY})})
        self.assertEqual(f.issues(), [])

    def test_depth_beyond_grandchild_warns(self):
        f = self.fixture({
            "qa/sweeps/a.md": sweep({"title": "A"}, {"Probes": "- Probe a."}),
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

    def test_fallback_node_yields_to_nodes_owning_as_many_files(self):
        self.fixture.write("features/app/infrastructure.md", feature(
            {"code": ["src/model.rs", "src/model.rs.in"], "tests": []},
            {"Behavior": "- Model. lgse/strata#5", "History": HISTORY}))
        self.fixture.write("scopes.yaml", "fallback: [app/infrastructure]\nscopes:\n  trash: operations/trash\n")
        tree = fm.load_tree(self.fixture.root)
        scopes = fm.load_scopes(self.fixture.root)
        cases = [
            (None, ["src/model.rs"], "app/infrastructure"),
            (None, ["src/model.rs", "src/ui/tabs.rs"], "browser/tabs"),
            ("trash", ["src/model.rs"], "operations/trash"),
            (None, ["src/model.rs", "src/model.rs.in", "src/ui/tabs.rs"], None),
        ]
        for scope, files, expected in cases:
            with self.subTest(scope=scope, files=files):
                result = fm.assign(tree, scopes, {"scope": scope, "files": files})
                self.assertEqual(result.node, expected, result.reason)
                self.assertIn("app/infrastructure", result.affected)

    def test_affected_lists_every_touched_node(self):
        result = fm.assign(self.tree, self.scopes, {"scope": "deps", "files": ["src/trash.rs", "src/ui/tabs.rs"]})
        self.assertEqual(result.affected, ["browser/tabs", "operations/trash"])
        self.assertIn("ignored", result.reason)


class RadiusTest(unittest.TestCase):
    def setUp(self):
        self.fixture = Fixture({
            "features/operations/trash/fly.md": feature(
                {"code": ["src/ui/fly.rs"], "tests": [], "related": ["browser/tabs"]},
                {"Behavior": "- Fly. lgse/strata#3", "History": HISTORY}),
            "features/browser/tabs.md": feature(
                {"code": ["src/ui/tabs.rs"], "tests": ["tests/e2e/scenarios/test_tabs.py"]},
                {"Behavior": "- Tabs. lgse/strata#4", "History": HISTORY}),
            "qa/sweeps/browser.md": sweep({"title": "Browser sweep", "triggers": ["src/ui/window/**"]},
                                          {"Probes": "- Resize the window."}),
        })
        self.addCleanup(self.fixture.close)
        self.tree = fm.load_tree(self.fixture.root)
        self.sweeps = fm.load_sweeps(self.fixture.root)

    def test_tiers_are_disjoint_and_forced_sweeps_come_from_triggers(self):
        files = ["src/ui/fly.rs", "src/ui/window/keyboard.rs", "README.md", "docs/trash.md"]
        r = fm.radius(self.tree, self.sweeps, ["operations/trash/fly"], files, owner="operations/trash/fly")
        self.assertEqual(r.primary, ["operations/trash/fly"])
        self.assertEqual(r.tiers, {1: ["operations/trash"], 2: ["browser/tabs"], 3: []})
        self.assertEqual(r.why["operations/trash"], "ancestor of `operations/trash/fly`")
        self.assertEqual(r.forced, {"browser": ["trigger `src/ui/window/**` matched `src/ui/window/keyboard.rs`"]})
        self.assertEqual(r.unmapped, ["README.md"])
        self.assertEqual(r.tier_of("operations/trash/fly"), 0)
        self.assertEqual(r.tier_of("browser/tabs"), 2)
        self.assertEqual(r.nodes(1), ["operations/trash/fly", "operations/trash"])

    def test_inbound_related_is_tier_three_and_family_includes_children(self):
        r = fm.radius(self.tree, self.sweeps, ["browser/tabs"], [])
        self.assertEqual(r.tiers, {1: [], 2: [], 3: ["operations/trash/fly"]})
        r = fm.radius(self.tree, self.sweeps, ["operations/trash"], [])
        self.assertEqual(r.tiers[1], ["operations/trash/fly", "operations/trash/restore"])

    def test_launch_names_owners_and_triggers(self):
        files = ["src/ui/fly.rs", "src/ui/window/keyboard.rs"]
        r = fm.radius(self.tree, self.sweeps, ["operations/trash/fly"], files)
        self.assertEqual(fm.launch(r, self.sweeps, 2), {
            "browser": ["owns tier-2 node `browser/tabs`",
                        "trigger `src/ui/window/**` matched `src/ui/window/keyboard.rs`"],
            "operations": ["owns primary `operations/trash/fly`", "owns tier-1 node `operations/trash`"],
        })
        self.assertEqual(fm.launch(r, self.sweeps, 1)["browser"],
                         ["trigger `src/ui/window/**` matched `src/ui/window/keyboard.rs`"])

    def test_rust_filter(self):
        cases = [
            ("src/a/b/tests/c.rs", "a::b::tests::c"),
            ("src/a/b/tests.rs", "a::b::tests"),
            ("src/a/mod.rs", "a"),
            ("src/main.rs", None),
            ("src/ui/pointer/**", None),
            ("tests/e2e/scenarios/test_x.py", None),
            ("scripts/test_installer.py", None),
        ]
        for path, expected in cases:
            with self.subTest(path=path):
                self.assertEqual(fm.rust_filter(path), expected)


class PlanTest(unittest.TestCase):
    def setUp(self):
        self.fixture = Fixture({
            "features/operations/trash/fly.md": feature(
                {"code": ["src/ui/fly.rs"], "tests": ["tests/e2e/scenarios/test_fly.py", "src/ui/fly/tests.rs"],
                 "related": ["browser/tabs"]},
                {"Behavior": "### Flights\n\n- Fly to the sidebar. lgse/strata#3", "History": HISTORY,
                 "Known gaps": "- Flights skip hidden rows. lgse/strata#9"}),
            "features/browser/tabs.md": feature(
                {"code": ["src/ui/tabs.rs"], "tests": ["tests/e2e/scenarios/test_tabs.py"]},
                {"Behavior": "- Tabs. lgse/strata#4", "History": HISTORY}),
            "qa/sweeps/browser.md": sweep({"title": "Browser sweep", "triggers": ["src/ui/window/**"]},
                                          {"Probes": "- Resize the window."}),
        })
        self.addCleanup(self.fixture.close)
        fm.write_index(self.fixture.root)

    def run_qa(self, *args):
        out = self.fixture.root / "out" / "plan.md"
        self.assertEqual(fm.main(["--root", str(self.fixture.root), "qa", *args, "--out", str(out)]), 0)
        return out.read_text()

    def test_node_plan_expands_behavior_probes_and_tests(self):
        text = self.run_qa("--node", "operations/trash/fly")
        self.assertIn("# QA plan: node `operations/trash/fly`", text)
        self.assertIn("- Primary: `operations/trash/fly` (owning node)", text)
        self.assertIn("## Sweep: Operations sweep (`operations`)", text)
        self.assertIn("#### `operations/trash/fly` — Trash (primary, owning node)", text)
        self.assertIn("**Flights**\n\n- Fly to the sidebar. lgse/strata#3", text)
        self.assertIn("#### `operations/trash` — Trash (regression, tier 1: ancestor of `operations/trash/fly`)", text)
        self.assertIn("Probes:\n\n- Trash from each view mode.", text)
        self.assertIn("### Sweep-wide probes\n\n- Watch the log for GTK criticals.", text)
        self.assertIn("- `./scripts/e2e.sh tests/e2e/scenarios/test_fly.py`", text)
        self.assertIn("- `./scripts/test-headless.py -- trash::tests ui::fly::tests`", text)
        self.assertIn("- Docs: `docs/trash.md`", text)
        self.assertIn("## Known gaps on primary nodes", text)
        self.assertIn("- Flights skip hidden rows. lgse/strata#9", text)
        self.assertIn("## Sweep: Browser sweep (`browser`)", text)
        self.assertIn("(regression, tier 2: related from `operations/trash/fly`)", text)
        self.assertIn("- Tier 3 (inbound related, not expanded): none", text)

    def test_tier_one_leaves_related_sweeps_out(self):
        text = self.run_qa("--node", "operations/trash/fly", "--tier", "1")
        self.assertIn("- Tier 2 (related, not expanded): `browser/tabs`", text)
        self.assertNotIn("## Sweep: Browser sweep", text)

    def test_pr_plan_quotes_how_to_test_and_lists_unmapped_files(self):
        rows = [{"number": 7, "title": "feat(trash): fly", "scope": "trash", "author": "me",
                 "merged_at": "2026-09-05T00:00:00Z", "merge_commit": SHA,
                 "body": "## Description\n\nFlies.\n\n## How to test\n\n1. Trash a file.",
                 "files": ["src/ui/fly.rs", "src/ui/window/keyboard.rs", "CHANGELOG.md"],
                 "issues": [{"ref": "lgse/strata#6", "title": "Fly please"}]}]
        self.fixture.write("data/prs.jsonl", "".join(json.dumps(r) + "\n" for r in rows))
        text = self.run_qa("--pr", "7")
        self.assertIn("# QA plan: lgse/strata#7 · feat(trash): fly", text)
        self.assertIn(f"- Head: `{SHA}`", text)
        self.assertIn("merged 2026-09-05 · by me", text)
        self.assertIn("[lgse/strata#6](https://github.com/lgse/strata/issues/6) Fly please", text)
        self.assertIn("pull/7/head:qa-7", text)
        self.assertIn("## How to test (from the PR)\n\n> 1. Trash a file.", text)
        self.assertIn("- Unmapped changes, no node or trigger: 1\n  - `CHANGELOG.md`", text)
        self.assertIn("- Forced sweeps:\n  - `browser`: trigger `src/ui/window/**` matched `src/ui/window/keyboard.rs`", text)
        self.assertIn("| `browser` | 1 | owns tier-2 node `browser/tabs`; trigger", text)

    def test_all_plan_covers_every_sweep_without_a_radius(self):
        text = self.run_qa("--all")
        self.assertIn("# QA plan: all sweeps", text)
        self.assertNotIn("- Primary:", text)
        self.assertIn("## Sweep: Browser sweep (`browser`)", text)
        self.assertIn("## Sweep: Operations sweep (`operations`)", text)
        self.assertIn("#### `browser/tabs` — Trash (sweep)", text)
        self.assertIn("### Feature `operations/trash`", text)

    def test_unmatched_files_are_an_error(self):
        self.fixture.write("changed.txt", "README.md\n")
        with self.assertRaises(SystemExit) as caught:
            fm.main(["--root", str(self.fixture.root), "qa", "--files", str(self.fixture.root / "changed.txt")])
        self.assertIn("nothing to plan", str(caught.exception))


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

    def test_qa_index_lists_sweeps_probes_and_gaps(self):
        f = Fixture({"features/operations/trash/restore.md": RESTORE.replace(
            "- src/trash/restore/**", "- src/trash/restore/**\n- tests/e2e/scenarios/test_restore.py")})
        self.addCleanup(f.close)
        fm.write_index(f.root)
        qa = (f.root / "index/qa.md").read_text()
        self.assertIn("## [Operations sweep](../qa/sweeps/operations.md) `operations`", qa)
        self.assertIn("2 nodes, 1 with probes", qa)
        self.assertIn("| [Trash](../features/operations/trash/index.md) `operations/trash` | 1 | — | 1 | "
                      f"[`docs/trash.md`](https://github.com/lgse/strata/blob/{SHA}/docs/trash.md) |", qa)
        self.assertIn("| ↳ [Restore](../features/operations/trash/restore.md) `operations/trash/restore` | 0 | "
                      f"[`tests/e2e/scenarios/test_restore.py`](https://github.com/lgse/strata/blob/{SHA}/"
                      "tests/e2e/scenarios/test_restore.py) | 1 | "
                      f"[`docs/trash.md`](https://github.com/lgse/strata/blob/{SHA}/docs/trash.md) (inherited) |", qa)
        without_probes = qa.split("## Nodes without probes")[1].split("## Nodes without E2E")[0]
        self.assertIn("`operations/trash/restore`", without_probes)
        self.assertNotIn("`operations/trash` ", without_probes)
        self.assertIn("## Nodes without E2E scenarios (0)", qa)
        self.assertIn("QA sweep: [`qa/sweeps/operations.md`](qa/sweeps/operations.md)", (f.root / "README.md").read_text())


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

    def test_probes_and_handoffs(self):
        probes, problems = fm.parse_probes("- Shared one.\n\n### a/b\n\n- First\n  continued.\n- Second.\n\n### a/c\n")
        self.assertEqual(problems, [])
        self.assertEqual(probes, {None: ["Shared one."], "a/b": ["First continued.", "Second."], "a/c": []})
        self.assertEqual(fm.parse_handoffs("None."), ([], []))
        handoffs, problems = fm.parse_handoffs("- Sidebar drops → `browser`.\n- Open With → `integration`")
        self.assertEqual(problems, [])
        self.assertEqual(handoffs, [("Sidebar drops", "browser"), ("Open With", "integration")])


if __name__ == "__main__":
    unittest.main()
