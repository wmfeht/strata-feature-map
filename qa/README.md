# QA sweeps

How to test Strata against the feature map: a targeted sweep for one PR, a full sweep across every area, or one area on demand. The feature nodes are the spec. A sweep says how to exercise an area and what else to try. `scripts/featuremap.py qa` says which nodes and sweeps a change reaches.

Three things, three places:

| What | Where |
| --- | --- |
| What must be true | `features/<area>/…` Behavior bullets, at the node's `reviewed_at` |
| How to exercise it | `qa/sweeps/<area>.md`: Setup, probes per node, hand-offs |
| What a change reaches | the plan `featuremap.py qa` renders |

Plans and reports are outputs. They live under `~/.cache/strata-qa/<ref>/` and never enter this repository. What a run found goes to a Strata issue or PR comment, filed by a person.

## Three ways to run

### Validate a PR

```sh
scripts/featuremap.py qa --pr 1533 --out ~/.cache/strata-qa/1533/plan.md
```

The plan lists the primary nodes the PR's files touch, the regression radius around them, the sweeps to launch, and for each sweep the Behavior bullets to verify, the probes to run, and the tests and docs to read. Then:

1. Check out the PR in a dedicated Strata worktree with the command the plan prints. Never test in a checkout that has other work.
2. Launch one agent per sweep in the plan. Give each the plan, its sweep file, and this page. For `browser` and `operations`, which are large, split along the plan's `### Feature` headings so each agent gets a few feature subtrees.
3. Each agent reports in the shape below. Aggregate as described under Aggregation.

`--tier 1` keeps the radius to the primary nodes and their family; `--tier 3` adds every node that lists a primary as `related`. The default is tier 2. Fork PRs take `--pr wmfeht/strata#12`. An open PR is fetched from GitHub and not stored.

For a local diff instead of a PR:

```sh
git -C <strata> diff --name-only main...HEAD | scripts/featuremap.py qa --files - --head "$(git -C <strata> rev-parse HEAD)"
```

### Full sweep

```sh
scripts/featuremap.py qa --all --head <sha> --out ~/.cache/strata-qa/<sha>/plan.md
```

Eight sweeps, one agent each, plus one or two extra agents for `browser` and `operations`. Use it for a release candidate, a nightly, or after a refactor of shared code.

### One area or one node

```sh
scripts/featuremap.py qa --sweep preview --head <sha>
scripts/featuremap.py qa --node operations/trash/restore
```

## Cross-cutting changes

Run a full sweep, not a targeted one, when a PR touches `tests/e2e/harness/**`, `scripts/e2e*`, `Cargo.toml`, `Cargo.lock`, `.github/**`, or primary nodes in more than two areas. The plan's "Unmapped changes" line lists files no node or trigger owns; read those files before deciding the radius is complete.

## Environment

Strata's own rules apply: `AGENTS.md` and `docs/e2e-testing.md` in the Strata checkout. The points that matter most for a sweep:

- **Worktree per PR.** `git -C <strata> fetch https://github.com/lgse/strata.git pull/<n>/head:qa-<n> && git -C <strata> worktree add ../strata-qa-<n> qa-<n>`. Merge the latest `main` into it before building if the PR is stale. Remove the worktree when the report is done.
- **Build once.** `mise run build` or `cargo build` in the worktree. Note the binary path and the exact commit in the report.
- **Private display and bus.** Every GUI check runs on a private Xvfb and a private D-Bus session with inherited display variables cleared. The user's desktop and session bus are never used. A missing isolated display stops the run; it is never a reason to fall back.
- **Throwaway HOME.** Launch `strata <fixture dir>` with `HOME` and the `XDG_*` directories pointed at a temporary directory so preferences start at their defaults and real Trash is never touched. `tests/e2e/harness/environment.py` lists the variables the E2E suite sets, including `GIO_USE_VFS=local` and `GSETTINGS_BACKEND=memory`; copy them. Preferences live in `$XDG_CONFIG_HOME/strata/settings.toml`.
- **Drive through accessibility.** Discover and read state over AT-SPI and send input with XTEST, the way `tests/e2e/harness/browser.py`, `interaction.py`, and `xtest.py` do. `~/dev/strata-mcp-harness` wraps the same harness for exploratory driving. Ad-hoc scripts stay in `/tmp`.
- **Fixtures.** `tests/e2e/harness/fixtures.py` builds the standard tree; `scripts/generate-fixture.sh` builds large ones. Use disposable fixtures only.
- **Evidence.** Screenshots with ImageMagick `import` on the private display, the app log with `RUST_LOG` set, and the exact commands run. Store them next to the report.
- **Automation as evidence.** Run the E2E and Rust commands the plan prints. `./scripts/e2e.sh <scenario paths>` runs in the pinned container; `./scripts/test-headless.py <filter>` runs Rust tests on a private display. Confirm the selection collected tests. Automation never replaces the probes.

## Probing style

- Exercise each behavior in every presentation that offers it: Columns, Icons, List.
- Check the three signal states separately: selection, keyboard cursor, open path.
- Try the standing edge inventory: an empty directory, a large one, hidden files on and off, non-UTF-8 and Unicode names, long names, a read-only location, and a second window when the behavior is app-wide.
- Watch the log. A GTK critical during a supported flow is a finding even when the UI looks right.
- Stay in the sweep. A defect in another area goes under Out-of-scope observations with the owning sweep named; the sweep's Hand-offs say who that is.

## Verdicts and findings

Each sweep ends in one verdict: `pass`, `pass-with-nits`, or `fail`.

- **Product non-nit.** Wrong result, data loss, crash, hang, unrecoverable state, a Behavior bullet that does not hold, a workflow that works in one view and not another, or a GTK critical in a supported flow. Any one of these makes the verdict `fail`.
- **Nit or process.** Wording, alignment, minor inconsistency, doc drift with no functional impact, a coverage gap that is not a product break.
- **Map drift.** The app disagrees with a Behavior bullet. When the bullet is sourced and the app changed, it is a product finding and a regression. When the code is right and the bullet is wrong, it is a finding against this repository: fix the node, cite the PR that made the code so, and set `review: draft`. Unverified bullets that turn out true lose their `(unverified)` mark in the same fix.
- **Doc drift.** An upstream doc disagrees with the app. Record it for an upstream follow-up.

A probe that finds a defect becomes a Known gaps bullet on the node once an issue exists, never before.

## Report

One file per sweep, `~/.cache/strata-qa/<ref>/<area>.md`:

```markdown
# QA: <area> for <ref>

- verdict: pass | pass-with-nits | fail
- head: <sha tested>
- build: <how it was built and launched>
- agent: <id>

## Coverage

Per node: the Behavior bullets exercised, in which views and states, and the bullets not exercised with the reason.

## Findings: product non-nits

Numbered. Steps, expected, actual, evidence path, and the Behavior bullet or probe that caught it.

## Findings: nits

## Out-of-scope observations

One line each with the owning sweep.

## Map drift

Node and bullet, what the app does, which side is wrong.

## Doc drift

Doc, what it says, what the app does.
```

## Aggregation

The coordinator routes and does not test.

1. Collect the verdict per sweep. Any `fail` blocks; `pass-with-nits` never blocks on its own.
2. De-duplicate Out-of-scope observations against the owning sweep's findings. Anything unclaimed becomes a finding for that sweep.
3. Collect Map drift into one list and turn it into a feature-map PR.
4. Collect Doc drift into one list for an upstream follow-up.
5. Write `summary.md` beside the reports: sweep to verdict, numbered non-nits with owning sweep, nits, drift, and what no agent could exercise and why.
6. After a fix, rerun only the sweeps whose nodes the fix touched. `featuremap.py qa --files` on the fix's diff names them.

Agents never file issues, comment on PRs, or change the PR. A person does that with the summary in hand.

## Keeping this current

`AGENTS.md` holds the rules. In short: a sweep owns its area by directory, so new nodes are covered without an edit; a changed Behavior means re-reading that node's probes and moving the sweep's `reviewed_at`; `check` fails on an area without a sweep, a probe heading that is not a node, a hand-off to a sweep that does not exist, or a trigger or tool that is missing upstream; `index/qa.md` lists nodes without probes and nodes without E2E scenarios.
