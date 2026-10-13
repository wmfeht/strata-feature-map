# Agent Instructions

This repository is the Strata feature map: one Markdown file per feature or
child feature, each tying shipped behavior and design to the upstream issues
and PRs that produced it. It answers three questions for a feature: what it
does today, why it was built that way, and how it got here.

Strata's code is only ever read. The one write to `lgse/strata` is an issue for
a bug the sync finds that no existing issue covers, filed only when a person asks.
Nothing else is written to `lgse/strata` or `wmfeht/strata`, and nothing there
knows this map exists.

## Layout

| Path | Purpose | Written by |
| --- | --- | --- |
| `features/<area>/<feature>.md` | A leaf node. | Backfill, then the bot |
| `features/<area>/<feature>/index.md` + `<child>.md` | A node with children: `index.md` is the parent. | Backfill, then the bot |
| `qa/README.md` | The QA sweep plan: environment, full and targeted sweeps, report template. | People |
| `qa/sweeps/<area>.md` | One QA sweep per area: setup, probes per node, hand-offs, triggers. | Backfill, then the bot |
| `README.md`, `index/*.md`, `site/src/SUMMARY.md` | Generated indexes. Never hand-edit. | `featuremap.py index` |
| `sources.yaml` | Tracked repositories, the sync watermark, and the release the site describes. | Backfill sets it, the bot advances it |
| `scopes.yaml` | Conventional Commit scope to node id, plus `fallback` nodes. | Backfill, refined during triage |
| `data/prs.jsonl` | Extracted upstream PR dataset. | `featuremap.py extract` / `drift` |
| `scripts/` | Tooling and its unittest coverage. | People |
| `site/` | Official user documentation. Pages and sections by people, prose by people and the bot. See `site/README.md`. | People, then the release docs run |

Beyond the feature map and the documentation site under `site/`, nothing else
belongs in the repository: no test results, CI status, review history, release
notes, QA reports or plans, or task checklists. Those live in issues and PRs, or
outside the repository. Sweeps say how to test, never what a run found.

## Feature tree

A node's id is its path under `features/` without `.md` or `/index`, such as
`operations/trash` or `operations/trash/restore`. Ids are derived, never typed.

- **Areas** are directories only. A file directly under `features/` or an
  `index.md` directly in an area is an error.
- **Depth** is area, feature, child, grandchild. `check` warns beyond that.
- **Nest** only when the child has its own origin PR or issue, its own Behavior
  bullets, and its own tests. Otherwise it is a paragraph or bullet group in the
  parent.
- **Promote** a leaf to a parent by moving `x.md` to `x/index.md`. The id does not
  change. Renaming a node retires its id; `check` reports every `related` entry
  that still points at it.

| Concern | Rule |
| --- | --- |
| Inheritance | Children inherit the parent's `docs` and Design and record only what differs. Everything else is per node. |
| Behavior | Owned by exactly one node: the one whose `code` implements it, even when another node's feature triggers it. A parent's Behavior covers only what no child owns. |
| History | A PR's row goes on the node `drift` names, never on both a parent and its child. A batch PR that bundles independent fixes gets a row on each node whose code it changed. See "Row placement" under Sync contract. |
| Coverage | A parent's effective code and tests are the union of its own and its subtree's. |
| Staleness | Each node has its own `reviewed_at`. A parent's effective staleness is its oldest descendant's. |
| Status | Per node. A shipped parent may have an in-progress child. |

## Feature file format

YAML front matter, then exactly these five `##` sections in this order, and
nothing else. No `#` title: the title lives in the front matter.

```markdown
---
title: Keyboard tab navigation and reordering
status: shipped
origin: {issue: lgse/strata#1505, pr: lgse/strata#1506}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [src/ui/window/composition/tabs.rs, src/ui/window/composition/tabs/**]
tests: [src/ui/window/composition/tabs/tests.rs, tests/e2e/scenarios/test_tabs.py]
docs: [docs/keyboard-navigation.md]
related: [integration/10xer-mode]
---

## Summary

Two or three sentences: what the feature is and who it is for. A parent names
its children.

## Behavior

- Ctrl+Page Up and Ctrl+Page Down move between tabs in strip order, wrapping at either end. lgse/strata#1506

## Design

Why it works this way: constraints, invariants, rejected approaches. Link the
maintained Strata doc when one carries the design, and summarize it here.

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-05 | lgse/strata#1506 | feat | Added keyboard tab cycling so the strip is usable without a pointer. |

## Known gaps

- Reordering does not yet announce the new position to screen readers. lgse/strata#1510
```

### Front matter

| Field | Required | Value |
| --- | --- | --- |
| `title` | yes | Human name of the feature. |
| `status` | yes | `proposed`, `in-progress`, `shipped`, `deprecated`, or `removed`. |
| `origin` | yes | `{issue: <ref>\|null, pr: <ref>\|null}` with at least one set: the issue and PR that introduced the feature. |
| `branch` | yes | Fork branch while `status: in-progress`, otherwise `null`. |
| `reviewed_at` | yes | Full 40-character upstream SHA the content was last verified against. |
| `review` | yes | `draft` or `reviewed`. Only the owner sets `reviewed`, or the bot at Sync contract step 7. |
| `code` | yes | Upstream paths or globs (`*`, `**`) owning the feature. A plain path also matches everything under it. Used to map PRs to nodes, so be specific: no shared modules, except on a `fallback` node. |
| `tests` | yes | Upstream test files or globs that cover the feature: Rust test modules and E2E scenarios. May be `[]`. |
| `docs` | no | Maintained docs: a site page such as `site/src/reference/archives.md`, or an upstream contributor doc such as `docs/architecture.md`. Children inherit them. |
| `related` | no | Node ids whose behavior moves when this one changes. |

A `<ref>` is always fully qualified, `owner/repo#n`: `lgse/strata#1506` upstream,
`wmfeht/strata#12` for fork-only issues. GitHub resolves a number to an issue or
PR, so the same form serves both.

Every `code` and `tests` entry, and every `docs` entry outside `site/`, must exist
in upstream at `reviewed_at`. A `docs` entry under `site/` must exist in this
repository.

### Sections

- **Summary.** Plain prose.
- **Behavior.** One checkable statement of shipped behavior per bullet, ending in
  one or more citations separated by commas. A statement inferred from code or a
  diff rather than stated by the PR or issue ends with `(unverified)` after its
  citations. Write assertions a QA agent could test: name the input, the state,
  and the observable result. "Handles focus correctly" is not a behavior.
  Group with `###` subheadings when the list is long; nothing else may sit
  between bullets.
- **Design.** Prose and bullets. A design change needs a linked issue or PR that
  justifies it.
- **History.** One table, newest first. `Date` is the merge date (YYYY-MM-DD),
  `PR` a ref, `Type` the Conventional Commit type, `Change` one line on what
  changed and why. Refactor and perf PRs get a row and no Behavior edit.
  Trivial PRs (typos, formatting) need no row.
- **Known gaps.** Bullets, each citing an issue: open issues, deferred work,
  intended behavior not yet shipped. A limitation stated in a merged PR body,
  with no issue, cites that PR. A gap goes on the node whose code would fix it.
  `None known.` when there are none.

## Writing rules

- Every claim traces to a PR, an issue, an issue comment, or a maintained doc:
  a site page, or an upstream doc that stayed upstream.
  Read the PR body's Description and How to test sections and the linked issue
  with its comments; design discussion lives in the comments.
- Code is the source of truth for current behavior. When a PR and the code at
  `reviewed_at` disagree, describe the code and cite the PR that made it so.
- Be concise. Sentences under 25 words. No adjectives where a number, key, or
  name will do.
- Never record test results, CI status, release notes, or review discussion.

## QA sweeps

A sweep is one QA agent's brief for an area. `qa/sweeps/<area>.md` owns every
node under `features/<area>/`; `check` fails on an area without a sweep or a
sweep without an area. `qa/README.md` says how to run one.

YAML front matter, then exactly these four `##` sections in this order.

| Field | Required | Value |
| --- | --- | --- |
| `title` | yes | Human name of the sweep. |
| `reviewed_at` | yes | Full 40-character upstream SHA the probes were last verified against. |
| `triggers` | no | Upstream globs for shared modules no node owns. A PR touching one forces the sweep into every targeted plan. |
| `tools` | no | Upstream docs, scripts, and fixtures the sweep relies on. |

Every `triggers` and `tools` entry must exist in upstream at `reviewed_at`. A
trigger that a node's `code` already covers is a warning: drop it.

- **Scope.** Prose: what the sweep exercises, by top-level feature, and what it
  leaves to other sweeps.
- **Setup.** Fixtures, mounts, environment, and tools beyond the common
  environment in `qa/README.md`.
- **Probes.** `- ` bullets under `### <node id>` subheadings naming nodes in the
  area. Bullets before the first subheading apply to the whole sweep. A probe
  names an input, state, or combination to exercise that the node's tests skip;
  the node's Behavior says what must be true. Probes carry no citations and never
  restate a Behavior bullet.
- **Hand-offs.** `- <what> → `<area>`` for behavior a tester meets here that
  another sweep owns, or `None.`

A node without probes is fine; its Behavior is its whole checklist. `index/qa.md`
lists those nodes and the nodes with no E2E scenario.

`featuremap.py qa` turns a PR, a diff, a node, or a sweep into a plan: primary
nodes from the changed paths, then tier 1 (ancestors and descendants), tier 2
(`related`), tier 3 (nodes listing a primary as `related`), plus sweeps whose
triggers fired. Plans and reports are output; they never enter this repository.

## Tooling

`scripts/featuremap.py` runs through `uv`, which supplies PyYAML.

| Command | Purpose |
| --- | --- |
| `scripts/featuremap.py extract` | Pull every merged upstream PR into `data/prs.jsonl`. |
| `scripts/featuremap.py index` | Regenerate `README.md` and `index/`, including `index/qa.md`, plus `site/src/SUMMARY.md` and the book title. |
| `scripts/featuremap.py check` | Validate the tree, the sweeps, and the site. `--offline` skips the upstream path and release checks. |
| `scripts/featuremap.py drift` | Extract PRs after the watermark, map them, and print the drift report. |
| `scripts/featuremap.py qa --pr N \| --files F \| --node ID \| --sweep AREA \| --all` | Render a QA plan to stdout or `--out`. `--tier 1..3` bounds the radius. |
| `scripts/featuremap.py release-docs --tag vX.Y.Z [--bump]` | Map a stable release's PRs to the site pages they affect; `--bump` moves the site to the release. |

The upstream check uses a blobless bare clone in `.cache/upstream.git`, or the
clone named by `FEATUREMAP_UPSTREAM`. Run `index` then `check` before every
commit. Tests: `uv run --with pyyaml python -m unittest discover -s scripts`.
`mise.toml` pins the site's tools and wraps these as tasks: `mise run ci` runs
everything CI runs, and `mise run serve` previews the site.

## Documentation site

`site/` is Strata's user documentation, an mdBook published on GitHub Pages.
`site/README.md` holds its page format and writing rules; follow them for any
edit under `site/`.

- **Page map.** `site/pagemap.yaml` declares every page, its title, its nodes,
  and its `##` sections. Only a person adds, removes, renames, or reorders a page
  or a `##` section. Agents edit under the declared headings: prose, bullets,
  tables, code blocks, and `###` subsections.
- **Drafts.** Content no section covers goes in `site/drafts/<slug>.md` with
  `proposed`, `nodes`, `reason`, and `release` front matter, and under "Proposed
  pages" in the PR description. Drafts are never built. A person merges,
  promotes, or rejects each one.
- **Cadence.** The feature map syncs daily; the site moves once per stable
  release and describes the latest one. When a `vX.Y.Z` tag lands upstream, run
  `release-docs --tag vX.Y.Z`, edit the sections it names, run it again with
  `--bump`, and open a `docs: vX.Y.Z` PR with "Docs updated", "Proposed pages",
  and "Screenshots needed" sections. Alpha, beta, RC, and nightly tags trigger
  nothing.
- **Screenshots.** Human maintainers record every capture. An agent lists a
  stale or needed one under "Screenshots needed": the page, the state to
  capture, and what to sanitize.
- **Accuracy.** Code is the source of truth. A site page that disagrees with the
  code at its `reviewed_at` is a site bug, fixed in the PR that found it. Pages
  describe shipped behavior only and carry no PR or issue citations.
- **Coverage.** Every shipped node is named by a reference page or listed in
  `site/unguided.yaml` with a reason.

## Sync contract (the bot)

On each scheduled run:

1. Run `drift`. It fetches upstream from the watermark to head, extracts the new
   merged PRs, maps each to the most specific node, and reports affected nodes and
   a triage list.
2. For each affected node, append History rows, edit Behavior only where shipped
   behavior changed, and set `reviewed_at` to the new head. Keep `review` as it
   is unless content changed; a content change, a new History row included,
   sets `review: draft`.
3. For each affected node, reread its probes in `qa/sweeps/<area>.md`. Add
   probes for new behavior, retire probes for removed behavior, and set the
   sweep's `reviewed_at` to the new head.
4. For each triage PR you can source, propose a new node. Otherwise leave it in
   the PR description for a person. A new node is owned by its area's sweep
   without any edit; a new area needs `qa/sweeps/<area>.md` in the same PR. A
   new shipped node goes in `site/unguided.yaml` with the reason "New since
   <release>; the next release docs run places it." The daily sync edits nothing
   else under `site/`.
5. For each synced PR, run `qa --pr N` and give every file under "Unmapped
   changes" an owner in the same PR (see the ownership rule below).
6. Set `watermark` in `sources.yaml` to the head `drift` reported, run `index` and
   `check`, and open a PR. A person reviews and merges.
7. Once the PR's adversarial review passes and the owner has resolved its open
   questions, set `review: reviewed` on the PR's draft nodes in a follow-up commit.

Rules:

- Append to History; never rewrite earlier rows.
- **Row placement.** A PR gets one History row, on the node `drift` names
  ("History row here"). Other nodes whose bullets the PR changes cite it there
  without a row. Never put rows on both a parent and child. Exceptions:
  - A batch PR of independent fixes (a "triage batch" title, or a body listing
    separate fixes) gets a row on each node whose code each fix changed.
  - A PR in triage gets a new node when it passes the Nest rule, and that node
    takes the row. Otherwise the row goes on the fallback node.
  - When a PR touches only fallback files, its scope decides: a scope mapped in
    `scopes.yaml` takes the row, otherwise the fallback does. Follow `drift`;
    do not reargue it.
- **Behavior placement.** A Behavior bullet lives on the node whose `code`
  implements it, even when another node's feature triggers it. Other nodes
  link the owner through `related`.
- Edit Behavior only when the PR changed shipped behavior, and cite it on the
  changed bullet.
- Edit Design only with a linked issue or PR that justifies the change.
- Create a child node only with an origin PR or issue. When a parent section
  gathers three or more History rows about one sub-behavior, propose the child
  in the PR description rather than creating it.
- Mark anything inferred rather than sourced `(unverified)`.
- Never guess a mapping. An unmapped PR stays in triage for a person.
- Renaming a node renames its probe subheading; `check` reports the stale one.
- A shared module no feature owns belongs to `app/infrastructure`, a `fallback`
  node in `scopes.yaml`. A PR that also touches other nodes maps past it when
  those nodes own at least as many of its files.
- Every upstream file a synced PR changes needs an owner. Assign each unmapped
  file to the first that fits:
  1. The node whose behavior it implements: `code` for source, `tests` for a test
     file or fixture.
  2. A new node, when the file carries a feature of its own that passes the Nest
     rule.
  3. `app/infrastructure`, for a shared module, a module root, test support, or a
     repository file no feature owns.
  4. A sweep `triggers` entry, for the tests of a module that is already a
     trigger.
  A file that mixes features goes to the node whose behavior most of its lines
  implement. Build, lint, editor, and CI configuration always goes to the
  fallback node, whatever it enforces. A catalog module that every feature edits
  to register itself (key bindings, message catalogs, style sheets) never goes
  in a feature node's `code`: give it to the fallback node or make it a sweep
  trigger.
  Name each assignment and its reason in the PR description. Never give a file to
  a node whose behavior it does not implement just to empty the list.
- When a PR, issue comment, or the code shows a bug that no issue covers, search
  `lgse/strata` issues, open and closed, and list it in the PR description. File
  an issue there only when a person asks, then cite it in Known gaps. Say "found
  by code reading" when no source states the bug. A maintained upstream doc that
  contradicts the code at `reviewed_at` is such a bug: list it, never record it
  in a node.
- Probes never record results, dates, or verdicts.
- Never open a PR that fails `check`.
- Imitate the reviewed files. They are the format's reference.
