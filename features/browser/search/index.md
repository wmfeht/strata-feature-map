---
title: Search
status: shipped
origin: {issue: null, pr: lgse/strata#222}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [src/services/search.rs, src/ui/search.rs, src/ui/window/composition/search.rs]
tests: [src/services/search/tests.rs, src/services/search/tests/multi_root.rs, src/services/search/tests/performance.rs, src/services/search/tests/refresh.rs, src/ui/search/tests.rs, tests/e2e/scenarios/test_search_filter_sort.py]
docs: []
related: [browser/navigation, devices/volumes, integration/10xer-mode]
---

## Summary

Ctrl+K global search finds files and folders by fuzzy name or path across Home and mounted local drives, from any folder. It runs on a bounded in-memory index that the pane filter also uses. Children: `browser/search/filter` (the Ctrl+F pane filter) and `browser/search/exclusions` (user-defined global search exclusions).

## Behavior

### Opening and scope

- Ctrl+K or the header search button opens the search dialog over a blurred window; Ctrl+K again closes it. lgse/strata#222 (unverified)
- Search covers Home and every mounted local drive, regardless of the open folder. lgse/strata#222, lgse/strata#493
- An ejected drive's results are gone the next time search opens. lgse/strata#493
- The search field's accessible description lists the searched locations and says remote shares are not included. lgse/strata#493, lgse/strata#1359
- With no local search location available, the dialog shows "No local search locations available." and the field is insensitive. lgse/strata#493
- An empty query shows "Type to search Home and mounted local drives". lgse/strata#493

### Matching and results

- A query matches names and paths fuzzily: `cat-01` also returns `bucket-01` and `file-01-*`. lgse/strata#758
- Name matches rank above path-only matches, and a shallower duplicate ranks above a deeper one. lgse/strata#307, lgse/strata#493 (unverified)
- A contiguous match of accented or CJK characters ranks above the same characters separated by `_`. lgse/strata#739
- An NFC query such as `résumé` matches an NFD filename, and an NFD query matches an NFC filename. lgse/strata#813
- Dotfiles are indexed only while hidden files are shown. lgse/strata#376
- Generated trees such as `node_modules/`, `target/`, `.venv/`, `.cache/`, `go/pkg/mod/`, and `__pycache__/` are skipped; `.cargo/config.toml` stays searchable. lgse/strata#473, lgse/strata#1287
- At most 100 results are shown, best first. lgse/strata#473
- Each result shows its name, its full path, and a thumbnail for images. lgse/strata#493, lgse/strata#548
- A spinner shows in the search bar while indexing runs. lgse/strata#72 (unverified)
- When indexing stops early, the footer shows "Partial results"; its description names each cause, such as "some folders could not be read". lgse/strata#72, lgse/strata#493
- A small tree with one unreadable folder reports the unreadable folder, not an entry limit. lgse/strata#493
- While indexing adds results, the highlighted result stays selected by path and unchanged rows are not rebuilt. lgse/strata#758

### Keyboard and activation

- Up and Down move the highlight while the caret stays in the query field; typing edits the query. lgse/strata#758
- When the first result is preselected, one Down highlights the second result. lgse/strata#953
- Enter or a single click on a result opens it and closes search. lgse/strata#177, lgse/strata#758
- Opening a folder result navigates into that folder. lgse/strata#177 (unverified)
- Opening a file result reveals it selected in its folder and opens quick preview. lgse/strata#1499
- With **Open search results directly** on, opening a file result launches it instead of previewing it. lgse/strata#144 (unverified)
- Alt+Enter, or right-click → **Open containing folder**, closes search and opens the result's parent with the result selected and focused. lgse/strata#1066
- For a folder result, **Open containing folder** selects the folder in its parent rather than opening it. lgse/strata#1066
- Escape, or a click outside the dialog panel, closes search. lgse/strata#112 (unverified)

## Design

Global search and the pane filter are separate tools: Ctrl+K finds anything anywhere, and Ctrl+F finds within the current folder (lgse/strata#222).

- lgse/strata#277 proposed a Current-folder scope in the Ctrl+K dialog. Instead the Ctrl+F filter learned to search subfolders (lgse/strata#275), and Ctrl+K was fixed to Home (lgse/strata#222).
- Ctrl+K later widened to mounted local drives because files on a USB drive were unreachable (lgse/strata#441, lgse/strata#493). Remote shares stay out of scope (lgse/strata#87).
- The index is in memory and bounded: 200,000 entries, depth 64, and 10 seconds of indexing (lgse/strata#13, lgse/strata#72). A disk-backed index was deferred for its own discussion (lgse/strata#72).
- Raising the cap to 400,000 entries was rejected because it roughly doubles worst-case memory and query work (lgse/strata#471).
- Concurrent sessions with the same roots, hidden-file setting, scope, and exclusions share one index snapshot. Only the best 100 matches are kept, in a bounded heap (lgse/strata#473).
- Roots share one entry budget and take turns, so a large Home cannot starve a drive (lgse/strata#493). Folders share indexing work so a dense subtree cannot exhaust the budget first (lgse/strata#758).
- Shallower directories are scheduled first, so sibling folders are found before deep subtrees (lgse/strata#1286, lgse/strata#1287).
- Generated trees are pruned by glob rather than whole dot-directories, so tool configuration stays searchable (lgse/strata#471, lgse/strata#473).
- The index is not a snapshot. Concurrent filesystem changes can cause transient omissions (lgse/strata#758).
- Unreadable folders are reported apart from size limits, because a walker error had been described as a very large tree (lgse/strata#431).
- Queries and indexed names are folded with lowercase and NFC, with an ASCII fast path (lgse/strata#809, lgse/strata#813).
- Ctrl+Shift+K reuses this dialog to rank visited folders; that folder jump belongs to `browser/navigation`.

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-27 | lgse/strata#1287 | fix | Scheduled shallow directories first and pruned Go and Python caches so sibling folders are not starved. |
| 2026-09-17 | lgse/strata#1066 | feat | Added Open containing folder to results through the result menu and Alt+Enter. |
| 2026-09-13 | lgse/strata#953 | fix | Made the first Down advance from the preselected result. |
| 2026-09-11 | lgse/strata#813 | fix | Folded queries and indexed names with NFC so composed and decomposed names match. |
| 2026-09-10 | lgse/strata#758 | fix | Shared indexing work across folders and kept the caret in the query during arrow navigation and updates. |
| 2026-09-10 | lgse/strata#739 | fix | Awarded the contiguous-match bonus to mixed-width multibyte characters. |
| 2026-09-06 | lgse/strata#473 | perf | Shared one index across sessions, pruned generated trees, and kept only the best 100 matches. |
| 2026-09-05 | lgse/strata#376 | fix | Indexed dotfiles when hidden files are shown, for every search surface. |
| 2026-09-03 | lgse/strata#222 | fix | Searched from Home instead of the current folder, since the pane filter covers folder scope. |
| 2026-09-03 | lgse/strata#177 | fix | Opened results on a single click. |

## Known gaps

- Remote shares such as SMB are not searched. lgse/strata#87
- Whether global search scans mounts the volume monitor hides, such as a cache subvolume, is undecided. lgse/strata#533
- Closing Ctrl+K does not return focus to the file list; the fix is unmerged. lgse/strata#1430, lgse/strata#1533
