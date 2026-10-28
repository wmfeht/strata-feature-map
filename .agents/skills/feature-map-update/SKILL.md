---
name: feature-map-update
description: Sync the Strata feature map for a merged upstream lgse/strata PR named in a wmfeht/strata-feature-map issue. Runs drift, parallel research and per-area writer subagents, an adversarial review loop, and opens a sync PR for a person to review. Use when an issue asks to sync, map, or update the feature map for a merged Strata PR.
---

# Strata feature-map sync from a merged PR

You are triggered by a GitHub issue in wmfeht/strata-feature-map that names a merged
upstream Strata PR. Your job: update the feature map for that merge, have it
adversarially reviewed, and open a PR for a person to review. You orchestrate;
subagents do the research, writing, and review. Follow AGENTS.md in this repository
exactly. It is the authority on format and rules, and this brief only adds the workflow.

## Hard rules

- Strata is read-only. Never comment on, push to, label, or open anything in
  lgse/strata or wmfeht/strata. All writes go to wmfeht/strata-feature-map only.
- Never merge and never push to main. Set `review: reviewed` only as Step 0.5 says.
- Never open a PR that fails `scripts/featuremap.py check` or the unit tests.
- Never guess a PR-to-node mapping. Unmappable PRs go in the PR description for a person.
- Keep scratch files (drift reports, briefs, QA plans, review findings) in a temp
  directory outside the repo. None of them may be committed.

## Step 0: Intake (you, no subagent)

1. Read the triggering issue and its comments: `gh issue view <n> -R wmfeht/strata-feature-map --comments`.
   Extract the upstream PR ref (`lgse/strata#N`, a PR URL, or a bare number meaning lgse/strata).
   If none can be found, comment on the issue asking for the PR ref and stop.
2. `gh pr view N -R lgse/strata --json number,title,state,mergedAt,mergeCommit,baseRefName`.
   If it is not merged into `main`, comment on the issue saying so and stop.
3. Check if it is already handled. Read `watermark` in `sources.yaml`, and set up the upstream clone
   with `git clone --filter=blob:none https://github.com/lgse/strata.git <tmp>/strata`, then
   `export FEATUREMAP_UPSTREAM=<tmp>/strata` so the tooling uses it. If the merge commit is an
   ancestor of the watermark, or `lgse/strata#N` already has a History row under `features/`,
   comment "already synced" on the issue, close it, and stop.
4. Concurrency: run `gh pr list -R wmfeht/strata-feature-map --state open --search "Sync lgse/strata in:title"`.
   Sync branches may be named `sync/` or `claude/`, so match the title, not the head.
   If an open sync PR exists, check out its branch and extend it, updating that PR's
   description at the end, instead of starting a new branch. If you cannot push to
   that branch, stack instead: branch from its head, open your PR against its branch,
   and start the description with "Stacked on #<PR>". Otherwise branch from an
   up-to-date `main`, named `sync/strata-N` unless the routine assigns a branch.
   Then compare `watermark` on `main` with the last merged sync PR's. If a merged sync
   PR never reached `main` (it merged into a stacked base after that base merged),
   merge its branch into yours first and explain it under "Read this first".
5. Accept merged syncs (AGENTS.md Sync contract step 7). For each draft node on `main`,
   find the commit that last changed it (`git log -1 -- <file>`) and the sync PR that
   merged it. If that PR is merged and its "Needs a person" section does not name the
   node, set `review: reviewed` in your branch, changing nothing else in the file. Name
   the promoted nodes in the PR description.
6. Create a full upstream worktree at the merge commit for reading code:
   `git -C <tmp>/strata worktree add <tmp>/strata-head <merge sha>`. Every subagent reads
   upstream code there. That is the `reviewed_at` you will set.

## Step 1: Drift

Run `scripts/featuremap.py drift --head <merge sha> --out <tmp>/drift.md`. Drift is
cumulative from the watermark, so it may include earlier unsynced PRs besides N. Process
all of them; that is correct. Read the report: the new PRs with their mapped nodes, the
stale nodes, the triage list, and the direct pushes.

- A direct push that only cuts a release (`chore: release vX.Y.Z`) needs no map change.
  Name it in the upstream range.

## Step 2: Research (parallel subagents, read-only)

Launch one research subagent per PR in the drift report, all in one message so they
run concurrently. Give each the PR ref, the merge SHA, the upstream worktree path, and
these instructions:

> Gather the sources for lgse/strata#<PR>. Read-only: do not edit any file.
> - `gh pr view <PR> -R lgse/strata --json title,body,author,mergedAt,mergeCommit,files,closingIssuesReferences,labels,comments`
>   and `gh pr diff <PR> -R lgse/strata`.
> - Every referenced issue (closing references, plus `#n` or URLs in the body and commits):
>   `gh issue view <n> -R lgse/strata --comments`. Design discussion lives in comments.
>   Follow `wmfeht/strata#n` refs too.
> - Read the changed code in <upstream worktree> to confirm what actually shipped.
> - Read the feature-map nodes the drift report mapped this PR to, plus their parents and `related` nodes.
> Return a brief with: the Conventional Commit type and scope; the merge date (YYYY-MM-DD,
> UTC, from `mergedAt`);
> a one-line "what changed and why"; each user-observable behavior change as
> input → state → observable result, with its source (PR body, issue comment URL, doc,
> or "code only", meaning unverified); any design rationale with its source; follow-up or
> deferred work with issue refs; new or removed tests (Rust modules, QA scenarios);
> new or changed docs; and whether this looks like a new feature or child feature
> (has its own origin, behavior, and tests) or belongs to an existing node. Flag any
> place where the PR text and the code disagree. The code wins.

## Step 3: Update (parallel subagents, one per area)

Group the affected nodes, the PRs, and the triage PRs you believe belong there by area
(`features/<area>/`). Launch one writer subagent per area, concurrently. Each owns only
`features/<area>/**` and `qa/sweeps/<area>.md`, so writers never touch the same file.
Give each the drift report, the research briefs for its PRs, the merge SHA, the upstream
worktree path, and these instructions:

> Update the feature map for area <area> following AGENTS.md ("Feature file format",
> "Writing rules", "QA sweeps", and "Sync contract") exactly. Imitate the existing files in
> this area; they are the reference format.
> For each affected node:
> - Append a History row (newest first) on the most specific node the PR touched,
>   never on both a parent and its child. Refactor and perf PRs get a row and no Behavior edit.
> - Edit Behavior only where shipped behavior changed. Each bullet is one testable
>   assertion that ends with its citation(s), plus `(unverified)` when the claim is
>   inferred from code rather than stated in a PR, issue, or doc.
> - Edit Design only with a citing PR or issue. Update Known gaps from follow-up issues.
> - Update `code`, `tests`, and `docs` for new or moved paths. Every entry must exist at the merge SHA.
> - Set `reviewed_at` to the merge SHA. If content changed, set `review: draft`.
> New nodes: create one only for a PR or issue that is a real new feature or child
> (own origin, own Behavior, own tests), per the Nest rule. Promote `x.md` to
> `x/index.md` when adding a child. If a section has gathered three or more History rows on
> one sub-behavior, do not create the child; note it as a proposal.
> QA mapping: in `qa/sweeps/<area>.md`, reread the probes for every node you changed.
> Add probes for new behavior that the node's tests skip (inputs, states, or combinations,
> with no citations and never restating a Behavior bullet). Add a `### <node id>` subheading
> for each new node that needs probes. Retire probes for removed behavior. Update Setup or
> Hand-offs if they changed. Set the sweep's `reviewed_at` to the merge SHA.
> Do not run git commands, and do not edit outside your area.
> Return: the files changed; new nodes with their origin; proposals (children, `triggers`
> entries for shared modules no node owns); and anything you could not source.

If a PR needs a new area, you create `features/<area>/` and `qa/sweeps/<area>.md`
together, or give that to one writer. Triage PRs that you cannot confidently map
stay unmapped. Collect them for the PR description.

Then you, not a subagent:
1. Set `watermark` in `sources.yaml` to the merge SHA.
2. Update `scopes.yaml` only as AGENTS.md allows: a new node's new scope, a spelling variant, or a scope whose PRs all landed on one node.
3. Run `scripts/featuremap.py index`, `scripts/featuremap.py check`, and
   `uv run --with pyyaml python -m unittest discover -s scripts`. Send any failures back to the
   owning area's writer (SendMessage) and rerun until all pass.
4. QA mapping check: for each PR, run `scripts/featuremap.py qa --pr <PR> --tier 1`. Every
   changed source file should land on a primary node or a sweep trigger. Investigate
   each "Unmapped changes" entry: map it if a node legitimately owns it, otherwise
   list it for a person. Never add a trigger just to empty the list.

## Step 4: Adversarial review loop (fresh subagents)

Run up to 3 rounds. In each round, launch one reviewer subagent per changed area,
concurrently. Reviewers must be new agents with no writer context. Give each `git diff main...HEAD`
for its area, the upstream worktree path, and these instructions:

> You are an adversarial reviewer. Assume the change is wrong until the sources prove it right.
> Check every added or changed line against the upstream code at <merge sha> and the
> cited PRs and issues (fetch them yourself with `gh`; do not trust summaries). Hunt for:
> - Behavior bullets that are false against the code, untestable or vague, missing a
>   citation, citing the wrong PR, or inferred but not marked `(unverified)`.
> - Shipped behavior changes in the PRs that the map missed, and removed behavior still listed.
> - A History row on the wrong node, on both a parent and child, a wrong date or type, or a rewritten earlier row.
> - New nodes that fail the Nest rule, or changes that should have been a new node.
> - Design edits without a justifying source. Known gaps without an issue.
> - `code`, `tests`, or `docs` globs that are too broad (shared modules) or that miss the new paths.
> - Probes that restate Behavior, carry citations or results, duplicate what tests
>   already cover, or are missing for new behavior. Stale probe subheadings.
> - Anything against AGENTS.md: section order, front matter, sentences over 25 words,
>   adjectives where a number or name would do, test results or CI in the content.
> Do not edit files. Return findings as a list: file, line, problem, evidence (code path:line
> or source URL), and the fix. Mark each one blocking or minor. Return nothing you cannot evidence.

For each blocking finding, spawn a verifier subagent with the finding only. It must
independently confirm or refute the finding against the code and sources. Discard
refuted findings. Send the confirmed findings, and the minor ones you agree with, to the
area's writer (SendMessage, or a fresh writer with the same Step 3 brief plus the findings) to fix.
Rerun `index`, `check`, and the tests.

Stop when a round produces no confirmed blocking findings, or after round 3. Record any
findings still unresolved or disputed for the PR description. Do not hide them.

## Step 5: Pull request (you)

1. Commit with a message like `Sync lgse/strata#N: <one-line summary>`, staging only files
   under `features/`, `qa/sweeps/`, `index/`, `README.md`, `sources.yaml`, `scopes.yaml`,
   and `site/unguided.yaml` (new shipped nodes, AGENTS.md sync step 4).
   Confirm `git status` shows nothing else, and that `check` and the tests pass on the final tree.
2. Push the branch and run `gh pr create -R wmfeht/strata-feature-map --base main`, or with
   the stacked base from Step 0. If you extended an existing sync PR, edit its body instead.
   The body should contain:
   - `Closes #<issue>` for the triggering issue.
   - Upstream range: old watermark → merge SHA, and the PRs synced (with links). Give each
     PR's type, merge date, and the node holding its row, or "none" and why.
   - Per node: what changed (History, Behavior, Design, Known gaps, paths), and new or promoted nodes with their origin.
   - QA: sweeps touched, probes added and retired, and each PR's tier-1 plan summary (primary nodes, sweeps).
   - Needs a person: unmapped or triage PRs, direct pushes, unmapped changed files,
     proposed child nodes, proposed `triggers`, and every `(unverified)` claim added.
     Past about 50 claims, give the count and the `git diff … | grep '(unverified)'`
     command that lists them.
   - Bugs and upstream doc contradictions (AGENTS.md sync rules). Say how you searched
     `lgse/strata` issues; if search is blocked, scan the open and closed issue listings.
   - Site pages the synced PRs made stale, for the next release docs run. Do not edit them.
   - Review loop: rounds run, findings fixed, and findings unresolved or disputed with the evidence.
3. Comment on the triggering issue with the PR link. Leave the issue open; the PR closes it on merge.

If any step fails in a way you cannot fix within these rules, do not open a PR. Comment
on the triggering issue with what failed and where, and stop.
