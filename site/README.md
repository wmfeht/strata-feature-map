# Strata documentation site

Strata's user documentation, built with mdBook and published on GitHub Pages. It
describes the latest stable Strata release, named in `sources.yaml` under `site`.

The site has two tiers. The guide (`src/guide/`, plus `src/introduction.md`)
teaches the common path by task. The reference (`src/reference/`) holds every
user-facing fact the upstream docs held when they were migrated here. The feature
tree under `features/` stays the spec; the site never cites it.

## Layout

| Path | Purpose | Written by |
| --- | --- | --- |
| `pagemap.yaml` | Pages, their titles, nodes, and `##` sections. | People only |
| `unguided.yaml` | Shipped nodes no reference page names, with reasons. | People |
| `src/**/*.md` | Pages. | People and the bot, inside the map |
| `src/SUMMARY.md` | mdBook's table of contents. | `featuremap.py index` |
| `src/img/` | Screenshots, named after their page. | Human maintainers only |
| `drafts/<slug>.md` | Proposals with no section to land in. Never built. | The bot, then people |
| `preprocessors/strip.py` | Drops front matter and HTML comments before rendering. | People |
| `book.toml` | mdBook configuration. `featuremap.py index` sets its `title`. | People |

## Page format

```markdown
---
nodes: [integration/custom-actions]
reviewed_at: 0a086aa3bdb251842a1e8413e2a6b35970d0b409
---

# Custom actions

Opening paragraph.

## Your first action in five minutes

<!-- node: integration/custom-actions, Settings → Actions -->

Section body.
```

- `nodes` equals the page's `nodes` in `pagemap.yaml`. `reviewed_at` is the full
  upstream SHA of the release commit the page was last checked against.
- The `#` heading equals the map's `title`. The `##` headings equal the map's
  `sections`, in order. `###` and deeper headings are free.
- A section may carry `<!-- node: <id>[, <Behavior group>] -->` comments naming
  the node, and the `###` group of its Behavior, it draws on. The id must be in
  the page's `nodes`.
- The preprocessor strips front matter and HTML comments, so no rendered page
  names a node.

## Writing rules

Guide pages:

- **Task first.** Each page opens with what the reader can do, then how.
  Headings are verbs or tasks.
- **Second person, present tense, imperative.** "Press Ctrl+K", not "the user may
  press".
- **One example beats three sentences.** Prefer a copy-paste block to a
  description of a format. Every block comes from a reference page or was run
  once by the author.
- **Non-exhaustive on purpose.** The common path and at most five "Good to know"
  bullets. Edge cases, limits, and refusal rules belong on the reference page.
- **Under 600 words a page.** If a page wants more, the overflow belongs in the
  reference.
- **Full detail footer.** A guide page with a reference page ends with
  `**Full detail:**` and links to it.

Reference pages:

- **Complete.** A reference page says everything a user can observe about its
  topic. If a Behavior bullet on a node the page names has no sentence on the
  page, one of them is wrong.
- **Code is the source of truth.** When a page and the code at its
  `reviewed_at` disagree, the page is a bug, fixed in the PR that found it.
- **Shipped behavior only.** Planned behavior goes in the node's Known gaps with
  an issue, never on the site.

Both tiers:

- **Stay inside the map.** Edit under the `##` headings `pagemap.yaml` declares.
  Never add, rename, reorder, or remove a page or a `##` section; that is a map
  change, and a person makes it.
- **Draft what fits nowhere.** Content with no section goes in
  `drafts/<slug>.md` and under "Proposed pages" in the PR description.
- **No citations in prose.** No PR or issue references, and no links to the
  feature map. Link other site pages relatively; link third-party sites when a
  page needs them.
- **Name real UI.** Match menu paths and labels as Strata shows them:
  **Settings → Actions → New action…**. Write keys as `Ctrl+Shift+N`, the same
  form on every page.
- **Screenshots come from human maintainers.** An agent never records or commits
  a capture. It lists each stale or needed capture under "Screenshots needed" in
  the PR description: the page, the state to capture, and what to sanitize.
  Captures live under `src/img/`, named after the page, with no personal file
  names visible.

## Drafts

```markdown
---
proposed: {page: guide/operations.md, section: Archives}   # or page: new
nodes: [operations/archives]
reason: Password-protected archives have no section on any page.
release: v1.0.0
---

Raw material for a person to merge, promote, or reject.
```

`release` is the release docs run that wrote the draft. `check` warns about a
draft from an earlier release, so proposals do not pile up unreviewed.

## Release docs run

The feature map syncs daily; the site updates once per stable release. When a
`vX.Y.Z` tag lands upstream:

1. `scripts/featuremap.py release-docs --tag vX.Y.Z` lists the PRs merged since the
   previous stable tag, the nodes they touched, and the pages naming those nodes.
2. Edit the matching section of each listed page in place.
3. Write a draft for content no section covers.
4. `scripts/featuremap.py release-docs --tag vX.Y.Z --bump` sets `site.release` in
   `sources.yaml` and every page's `reviewed_at` to the release commit.
5. Run `index` and `check`, and open a `docs: vX.Y.Z` PR whose description has
   "Docs updated", "Proposed pages", and "Screenshots needed" sections. The
   `release-docs` report renders them.

Alpha, beta, RC, and nightly tags trigger nothing.

## Building

`mise.toml` pins mdBook 0.4.52, mdbook-linkcheck 0.7.7, and uv. Run `mise install`
once, then:

| Command | Does |
| --- | --- |
| `mise run serve` | Preview at http://localhost:3000, rebuilding on every save. |
| `mise run build` | Build into `site/book/`, check links, and fail if a node id reaches the HTML. |
| `mise run check` | Validate the tree, the sweeps, and the site against upstream. |
| `mise run ci` | Everything CI runs: tests, a current index, `check`, and the build. |

Each task runs from the repository root, which the preprocessor path in
`book.toml` requires. The `pages` workflow installs the same tools through mise,
builds on every pull request, and deploys `main` to GitHub Pages.
