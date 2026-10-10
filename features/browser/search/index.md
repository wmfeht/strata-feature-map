---
title: Search
status: shipped
origin: {issue: null, pr: lgse/strata#222}
branch: null
reviewed_at: 72b840e69d6f0df9d33fb5583e62a3a2944886a1
review: draft
code: [src/services/search.rs, src/ui/search.rs, src/ui/window/composition/search.rs]
tests: [src/services/search/tests.rs, src/services/search/tests/multi_root.rs, src/services/search/tests/performance.rs, src/services/search/tests/refresh.rs, src/ui/search/tests.rs, tests/e2e/scenarios/test_search_filter_sort.py]
docs: []
related: [browser/navigation, devices/volumes, integration/10xer-mode]
---

## Summary

Ctrl+K global search finds files and folders by fuzzy name or path across Home and mounted local drives, from any folder. It runs on a bounded in-memory index built by the same service as the pane filter. Children: `browser/search/filter` (the Ctrl+F pane filter) and `browser/search/exclusions` (user-defined global search exclusions).

## Behavior

### Opening and scope

- Ctrl+K or the header search button opens the search dialog over a blurred window; Ctrl+K again closes it. lgse/strata#222 (unverified)
- Search covers Home and every mounted local drive, regardless of the open folder. lgse/strata#222, lgse/strata#493
- An ejected drive's results are gone the next time search opens. lgse/strata#493
- The search field's accessible description lists the searched locations and says remote shares are not included. lgse/strata#493, lgse/strata#1359
- A drive mounted inside Home or another root appears once in results, not once per root. lgse/strata#493
- On open, the empty query shows "Type to search Home and mounted local drives"; clearing a typed query adds "Fuzzy matching · try a name or path fragment". lgse/strata#493 (unverified)

### Matching and results

- A query also matches paths that contain its characters in order: `cat-01` matches `bucket-cat/file-01-noise.jpg`, below `cat-01-photo.jpg`. lgse/strata#695, lgse/strata#758
- Name matches rank above path-only matches, and a shallower duplicate ranks above a deeper one. lgse/strata#307, lgse/strata#493 (unverified)
- A contiguous match of accented or CJK characters ranks above the same characters separated by `_`. lgse/strata#739
- An NFC query such as `résumé` matches an NFD filename, and an NFD query matches an NFC filename. lgse/strata#813
- Dotfiles are indexed only while hidden files are shown. lgse/strata#376
- Generated trees such as `node_modules/`, `target/`, `.venv/`, `.cache/`, `go/pkg/mod/`, and `__pycache__/` are skipped; with hidden files shown, `.cargo/config.toml` stays searchable. lgse/strata#473, lgse/strata#1287
- Paths excluded by a `.gitignore` or `.ignore` file are not indexed. lgse/strata#758 (unverified)
- At most 100 results are shown, best first. lgse/strata#473
- Each result shows its name, its full path, and a thumbnail for images. lgse/strata#493, lgse/strata#548
- A spinner shows in the search bar while indexing runs. lgse/strata#72 (unverified)
- When indexing stops early, the footer shows "Partial results"; its description names each cause, such as "some folders could not be read". lgse/strata#72, lgse/strata#493, lgse/strata#1066
- A small tree with one unreadable folder reports the unreadable folder, not an entry limit. lgse/strata#493
- While indexing adds results, the highlighted result stays selected by path and unchanged rows are not rebuilt. lgse/strata#758

### Outside changes

- A file another program creates, deletes, or renames in a watched folder rescans every index whose walk lists that folder. lgse/strata#1439, lgse/strata#1544
- A burst of such changes during a walk does not cancel it; one more walk follows after it publishes. lgse/strata#1439, lgse/strata#1544
- Rescans of one index for outside changes start at least 1 second apart, and every session sharing the index gets the new results. lgse/strata#1439, lgse/strata#1544
- A change in a folder the walk skips triggers no rescan. Skipped are generated trees such as `target/`, exclusions, hidden folders while hidden files are off, and depth 64 or more. lgse/strata#1544
- For an index built without subfolders, only a change in its root folder triggers a rescan. lgse/strata#1544 (unverified)
- When another program moves a folder that is an index root or contains one, those indexes move to the new path and restart. lgse/strata#1544 (unverified)
- While Ctrl+K is open, a change in a watched folder under its roots triggers a full Ctrl+K rescan, at most once a second. lgse/strata#1544

### Keyboard and activation

- Up and Down move the highlight while the caret stays in the query field; typing edits the query. lgse/strata#758
- When the first result is preselected, one Down highlights the second result. lgse/strata#953
- Enter or a single click on a result opens it and closes search. lgse/strata#177, lgse/strata#758
- Opening a folder result navigates into that folder. lgse/strata#177 (unverified)
- Opening a file result reveals it selected in its folder and opens quick preview. lgse/strata#1499
- With **Open search results directly** on, opening a file result launches it instead of previewing it, and still reveals it in its folder. lgse/strata#144 (unverified)
- Alt+Enter, or right-click → **Open containing folder**, closes search and opens the result's parent with the result selected and focused. lgse/strata#1066
- For a folder result, **Open containing folder** selects the folder in its parent rather than opening it. lgse/strata#1066
- Escape, or a click outside the dialog panel, closes search. lgse/strata#112 (unverified)
- Closing search with Escape, Ctrl+K, or a click outside the panel returns focus to its opener, such as the file list's cursor row. lgse/strata#1430, lgse/strata#1533
- Opening a result, or Open containing folder, hands focus to the revealed item in the browser rather than the control that opened search. lgse/strata#1430, lgse/strata#1533

## Design

Global search and the pane filter are separate tools: Ctrl+K finds anything anywhere, and Ctrl+F finds within the current folder (lgse/strata#222).

- lgse/strata#277 proposed a Current-folder scope in the Ctrl+K dialog. Instead the Ctrl+F filter learned to search subfolders (lgse/strata#275), and Ctrl+K was fixed to Home (lgse/strata#222).
- Ctrl+K later widened to mounted local drives because files on a USB drive were unreachable (lgse/strata#441, lgse/strata#493). Remote shares stay out of scope (lgse/strata#87).
- The index is in memory and bounded: 200,000 entries, depth 64, and 10 seconds of indexing (lgse/strata#13, lgse/strata#72). A disk-backed index was deferred for its own discussion (lgse/strata#72).
- Raising the cap to 400,000 entries was rejected because it roughly doubles worst-case memory and query work (lgse/strata#471).
- Concurrent sessions with the same roots, hidden-file setting, scope, and exclusions share one index snapshot. Only the best 100 matches are kept, in a bounded heap (lgse/strata#473).
- Roots share one entry budget and take turns, so a large Home cannot starve a drive (lgse/strata#493). Folders share indexing work so a dense subtree cannot exhaust the budget first (lgse/strata#758).
- Among directories with equal pending work, shallower ones are scheduled first, so sibling folders are found before deep subtrees (lgse/strata#1286, lgse/strata#1287).
- Generated trees are pruned by glob rather than whole dot-directories, so tool configuration stays searchable (lgse/strata#471, lgse/strata#473).
- The index is not a snapshot. Concurrent filesystem changes can cause transient omissions (lgse/strata#758).
- An outside change refreshes the shared index rather than restarting one session. Another pane sharing the index would otherwise keep the stale snapshot (lgse/strata#1439).
- Refreshes for outside changes coalesce to about one walk per second per index. A constantly changing folder, such as build output, cannot run walks back to back (lgse/strata#1439, lgse/strata#1544).
- The pruned-folder check caches its glob set per root; rebuilding it per change stalled the window for up to 1.8 s during bursts (lgse/strata#1544).
- A root rename or move still cancels and restarts the walk, because the roots themselves changed (lgse/strata#1544).
- Unreadable folders are reported apart from size limits, because a walker error had been described as a very large tree (lgse/strata#431).
- Queries and indexed names are folded with lowercase and NFC, with an ASCII fast path (lgse/strata#809, lgse/strata#813).
- Ctrl+Shift+K reuses this dialog to rank visited folders; that folder jump belongs to `browser/navigation`.

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-10 | lgse/strata#1544 | fix | Rescanned indexes listing a folder changed outside the app, coalescing bursts and skipping pruned folders. |
| 2026-09-27 | lgse/strata#1287 | fix | Scheduled shallow directories first and pruned Go and Python caches so sibling folders are not starved. |
| 2026-09-17 | lgse/strata#1066 | feat | Added Open containing folder to results through the result menu and Alt+Enter. |
| 2026-09-17 | lgse/strata#1105 | fix | Added a folder icon to the reveal shortcut hint in search results. |
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
