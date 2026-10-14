---
name: docs-update
description: Update Strata's user documentation under site/ for a stable upstream release (vX.Y.Z) named in a wmfeht/strata-feature-map issue. Runs release-docs, per-page writer subagents, an adversarial review loop, and opens a `docs: vX.Y.Z` PR for a person to review. Use when an issue asks to update, refresh, or publish the docs site for a Strata release.
---

# Strata documentation update for a stable release

You are triggered by a GitHub issue in wmfeht/strata-feature-map that names a stable
upstream Strata release, a `vX.Y.Z` tag. Your job: bring the documentation site under
`site/` up to that release, have it adversarially reviewed, and open a `docs: vX.Y.Z`
PR for a person to review. You orchestrate; subagents do the writing and review.
Follow AGENTS.md ("Documentation site") and `site/README.md` ("Page format", "Writing
rules", "Drafts", "Release docs run") exactly. They are the authority on format and
rules, and this brief only adds the workflow.

## Hard rules

- Strata is read-only. Never comment on, push to, label, or open anything in
  lgse/strata or wmfeht/strata. All writes go to wmfeht/strata-feature-map only.
- Never merge and never push to main. Merging deploys the site, so that is a person's call.
- Agents edit inside the page map, never the map itself. Never add, remove, rename,
  or reorder a page or a `##` section. Never edit `site/pagemap.yaml`,
  `site/unguided.yaml`, `site/theme/`, `site/preprocessors/`, or `features/` and `qa/`.
  Propose those changes in the PR description instead.
- Never record, edit, or commit a screenshot, and never add files under `site/src/img/`.
  List captures under "Screenshots needed".
- Pages describe shipped behavior at the release only. No PR or issue citations, no
  node ids in prose, no planned behavior, no links to the feature map.
- Never open a PR that fails `scripts/featuremap.py check`, the unit tests, or `mise run build`.
- Keep scratch files (release reports, briefs, review findings) in a temp directory
  outside the repo. None of them may be committed.
- Alpha, beta, RC, and nightly tags trigger nothing.

## Step 0: Intake (you, no subagent)

1. Read the triggering issue and its comments: `gh issue view <n> -R wmfeht/strata-feature-map --comments`.
   Extract the release tag (`vX.Y.Z`, or a release URL that names one). If none can be
   found, comment on the issue asking for the tag and stop. If the tag is not a stable
   `vX.Y.Z` (alpha, beta, RC, nightly), comment that pre-release tags trigger no docs run,
   close the issue, and stop.
2. Set up the upstream clone with `git clone --filter=blob:none https://github.com/lgse/strata.git <tmp>/strata`,
   then `export FEATUREMAP_UPSTREAM=<tmp>/strata` so the tooling uses it. Resolve the tag:
   `git -C <tmp>/strata rev-parse 'vX.Y.Z^{commit}'`. If it does not exist, comment and stop.
3. Check if it is already handled. Read `site.release` and `site.commit` in `sources.yaml`.
   If `site.release` is this tag or a later one, comment "already published" on the issue,
   close it, and stop.
4. Check the feature map is current. Pages are held to node Behavior, so the map must be
   synced through the release. Run `git -C <tmp>/strata merge-base --is-ancestor <tag sha> <watermark>`
   with `watermark` from `sources.yaml` on main. If it fails, comment that the feature map
   must sync through `<tag sha>` first (the feature-map-update skill), name any open sync
   PR, and stop.
5. Concurrency: run `gh pr list -R wmfeht/strata-feature-map --state open --search "head:docs/"`.
   If an open docs PR covers an earlier release, check out its branch and extend it to this
   release, updating that PR's title and description at the end. If one already covers this
   tag, comment its link on the issue and stop. Otherwise branch `docs/vX.Y.Z` from an
   up-to-date `main`.
6. Create a full upstream worktree at the tag for reading code:
   `git -C <tmp>/strata worktree add <tmp>/strata-release <tag sha>`. Every subagent reads
   upstream code there.

## Step 1: Release report

Run `scripts/featuremap.py release-docs --tag vX.Y.Z --since <site.release> --out <tmp>/release.md`,
with `<site.release>` from `sources.yaml` on main. Passing `--since` covers any release the
site skipped. Read the report:

- **Pages to update**: each page with the PRs that touched its nodes.
- **Nodes on no page**: touched nodes that no page names, with their `unguided.yaml` reason if any.
- **PRs on no node**: PRs the feature map does not cover.
- **PR description**: the skeleton for Step 5.

Also collect:

- Entries in `site/unguided.yaml` whose reason reads "New since <release>; the next release
  docs run places it." This run proposes where each one goes.
- Existing drafts in `site/drafts/`. They wait for a person; list them, never delete them.
- `<!-- Screenshot: ... -->` comments on the listed pages.

## Step 2: Write (parallel subagents, grouped by shared nodes)

Group the pages to update so that pages sharing a node go to the same writer. A guide page
and the reference page for its topic usually land together, which keeps them consistent.
Launch one writer subagent per group, concurrently. Each owns only its pages and the drafts
it creates, so writers never touch the same file. Give each the release report, its pages,
the PRs per page, the tag, the tag SHA, the previous `site.release`, the upstream worktree
path, and these instructions:

> Update these Strata documentation pages for <tag>, following `site/README.md` ("Page format",
> "Writing rules", "Drafts") and AGENTS.md ("Documentation site") exactly. Imitate the existing
> pages; they are the reference format.
> Sources, for each PR listed against your pages:
> - The feature-map nodes the page names: the History rows and Behavior bullets that cite the
>   PR, and their Design and Known gaps. The map is synced through the release.
> - `gh pr view <PR> -R lgse/strata --json title,body,files,closingIssuesReferences` and the
>   linked issues with `gh issue view <n> -R lgse/strata --comments`.
> - The code in <upstream worktree>. It is the source of truth: UI labels, menu paths,
>   defaults, key bindings, and messages must match the strings there exactly.
> Edit:
> - Change only prose, bullets, tables, code blocks, and `###` subsections under the `##`
>   headings `site/pagemap.yaml` declares. Put each change in the section it belongs to.
> - Reference pages are complete. For every node your pages name that a PR touched, each
>   Behavior bullet needs a sentence on the page, and each sentence must still be true at the
>   tag. Remove behavior the release removed. If a page and a node disagree, the code decides;
>   report a wrong node rather than editing `features/`.
> - Guide pages are task first, second person, present tense, imperative. They show the common
>   path, at most five "Good to know" bullets, and end with the `**Full detail:**` footer when a
>   reference page exists. Prose stays under 600 words, not counting tables, code blocks,
>   front matter, or HTML comments.
> - Keep `<!-- node: <id>[, <Behavior group>] -->` comments accurate for the Behavior groups
>   each section draws on. Ids must be in the page's `nodes`.
> - Write keys as `Ctrl+Shift+N` and menu paths as **Settings → Actions → New action…**.
>   Link other site pages relatively.
> - A placeholder in prose such as <name> or <path> must be escaped as `\<name>` or sit inside
>   a code span. mdBook passes a bare tag through as HTML: the placeholder vanishes, and
>   `<option>` breaks the paragraph's wrapping.
> - No PR or issue citations, no node ids in prose, no planned behavior.
> - Content that no declared section covers goes in `site/drafts/<slug>.md` with `proposed`,
>   `nodes`, `reason`, and `release: <tag>` front matter. Prefix the slug with the page or topic
>   so it cannot collide with another writer's.
> - When a change makes a screenshot stale or a new state needs one, do not capture it. Report
>   the page, the state to capture, and what to sanitize.
> Do not run git commands, and do not edit outside your pages and your drafts.
> Return: the files changed; per page, the sections edited and what changed; drafts written
> with their proposed placement; screenshots needed; disagreements between a page, a node, an
> upstream doc, and the code, with evidence (code path:line); and anything you could not source.

Then launch one more writer, concurrently, for placement. Give it the "Nodes on no page"
list, the "New since" `unguided.yaml` entries, the tag, and the worktree path, with the same
writing rules, and these instructions:

> For each node: if users can observe it at <tag>, write a draft in `site/drafts/<slug>.md`
> proposing the page and section where it belongs, or `page: new`. Say in `reason` why no
> declared section covers it. When an existing section already covers it, the proposal is to
> add the node to that page's `nodes` in `site/pagemap.yaml`; draft only the missing text.
> If users cannot observe it, propose an `unguided.yaml` reason instead. Edit no page and no
> map file. Return each node with its proposal.

PRs on no node stay unplaced. Collect them for the PR description; they are feature-map
gaps for a person.

Then you, not a subagent:
1. Run `scripts/featuremap.py release-docs --tag vX.Y.Z --bump`. It sets `site.release` and
   `site.commit` in `sources.yaml` and every page's `reviewed_at` to the release commit.
2. Run `scripts/featuremap.py index`, which renders `site/src/SUMMARY.md` and the book title.
3. Run `scripts/featuremap.py check`, `uv run --with pyyaml python -m unittest discover -s scripts`,
   and `mise run build`. The build checks links and refuses node ids or front matter in the HTML.
   Send any failures back to the owning writer (SendMessage) and rerun until all pass.
   Warnings about drafts from earlier releases are expected; list them for a person.

## Step 3: Adversarial review loop (fresh subagents)

Run up to 3 rounds. In each round, launch one reviewer subagent per writer group,
concurrently. Reviewers must be new agents with no writer context. Give each
`git diff main...HEAD` for its pages and drafts, the release report, the upstream worktree
path, and these instructions:

> You are an adversarial reviewer. Assume the change is wrong until the sources prove it right.
> Check every added or changed line against the upstream code at <tag sha>, the feature-map
> nodes the page names, and the PRs in the release (fetch them yourself with `gh`; do not trust
> summaries). Hunt for:
> - Statements false against the code: labels, menu paths, defaults, keys, limits, messages.
> - User-observable changes in the release that the pages missed, and removed behavior still described.
> - On reference pages, Behavior bullets of touched nodes with no sentence on the page.
> - Guide rules: not task first, not imperative, prose over 600 words (count it; tables, code
>   blocks, front matter, and comments do not count), more than five "Good to know" bullets,
>   or a missing `**Full detail:**` footer.
> - Structure: `#` heading or `##` headings that differ from `site/pagemap.yaml`, front matter
>   that differs from the map, node comments naming ids outside the page's `nodes`.
> - PR or issue citations, node ids in prose, planned behavior, feature-map links.
> - Bare `<placeholder>` text outside code that would render as HTML.
> - Contradictions with other site pages: grep `site/src/` for the same feature, key, or setting.
> - Drafts with missing or wrong front matter, or content that a declared section already covers.
> - Screenshot needs the writer missed.
> Do not edit files. Return findings as a list: file, line, problem, evidence (code path:line
> or source URL), and the fix. Mark each one blocking or minor. Return nothing you cannot evidence.

For each blocking finding, spawn a verifier subagent with the finding only. It must
independently confirm or refute the finding against the code and sources. Discard refuted
findings. Send the confirmed findings, and the minor ones you agree with, to the group's
writer (SendMessage, or a fresh writer with the same Step 2 brief plus the findings) to fix.
Rerun `check`, the tests, and `mise run build`.

Stop when a round produces no confirmed blocking findings, or after round 3. Record any
findings still unresolved or disputed for the PR description. Do not hide them.

When a page, node, or maintained upstream doc contradicts the code, or the code shows a bug
no issue covers, search `lgse/strata` issues, open and closed, and list it for a person. Fix
a wrong page in this PR. Never edit `features/`; a wrong node goes to a person or the next sync.

## Step 4: Pull request (you)

1. Commit with the message `docs: vX.Y.Z`, staging only files under `site/src/` and
   `site/drafts/`, plus `site/book.toml` and `sources.yaml`. Confirm `git status` shows nothing
   else, and that `check`, the tests, and `mise run build` pass on the final tree.
2. Push the branch and run `gh pr create -R wmfeht/strata-feature-map --base main --title "docs: vX.Y.Z"`.
   If you extended an existing docs PR, retitle it and edit its body instead. Build the body
   from the report's "PR description" skeleton:
   - `Closes #<issue>` for the triggering issue.
   - Range: previous `site.release` → tag (with the SHA), and the PRs in the release (with links).
   - **Docs updated**: per page, the sections edited and what changed.
   - **Proposed pages**: each draft with its proposed page and section, and every change a
     person must make to `site/pagemap.yaml` or `site/unguided.yaml` to place a node.
   - **Screenshots needed**: per capture, the page, the state to capture, and what to sanitize.
   - **Needs a person**: PRs on no node, page-node disagreements, upstream doc or code bugs
     with any matching `lgse/strata` issues, earlier drafts still unreviewed, and `check` warnings.
   - **Review loop**: rounds run, findings fixed, and findings unresolved or disputed with the evidence.
   - A note that merging deploys the site to GitHub Pages.
3. Comment on the triggering issue with the PR link. Leave the issue open; the PR closes it on merge.

If any step fails in a way you cannot fix within these rules, do not open a PR. Comment on
the triggering issue with what failed and where, and stop.
