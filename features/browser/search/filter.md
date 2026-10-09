---
title: Pane filter
status: shipped
origin: {issue: lgse/strata#277, pr: lgse/strata#275}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [src/ui/inline_search.rs, src/ui/inline_search/**, src/ui/search_session.rs, src/ui/browser/columns/search.rs, src/services/search/directory.rs, src/services/search/pattern.rs]
tests: [src/ui/search_session/tests.rs, src/services/search/directory/tests.rs, src/services/search/pattern/tests.rs, src/services/search/tests/scope.rs, tests/e2e/scenarios/test_filter_results.py]
docs: [docs/keyboard-navigation.md, docs/preferences.md]
related: [integration/10xer-mode, browser/view-modes, preview/quick-preview, browser/thumbnails]
---

## Summary

The Ctrl+F filter narrows the focused pane by filename, in the current folder and, by default, its subfolders. It works in Columns, Icons, and List, and its results support the normal item actions.

## Behavior

### Opening and closing

- Ctrl+F, or the pane's filter button, reveals the filter field for the focused pane. lgse/strata#307, lgse/strata#389
- With **Type to search** on, typing a printable character in a file view opens the filter with that character as the query. lgse/strata#307
- **Type to search** is on unless the user turned it off. lgse/strata#387
- With **Type to search** on, `/` in a file view opens an empty filter without inserting `/`. lgse/strata#416
- Space in a file view opens quick preview, not the filter. lgse/strata#416
- Escape in the filter field, or clearing the query, restores the normal listing; hidden files stay hidden. lgse/strata#307, lgse/strata#310
- Switching between Columns, Icons, and List keeps the query, the open filter field, and the narrowed listing. lgse/strata#925
- In Columns, opening a filter in one column closes and clears any other column's filter. lgse/strata#887
- In Columns, a click outside the filtered column closes and clears its filter; a click inside that column keeps it. lgse/strata#887
- In Columns, moving focus out of the filtered column closes the filter; focus in its own results, a popover, or a dialog keeps it. lgse/strata#896

### Matching

- Plain text matches a case-insensitive substring of the file or folder name; parent folder names never qualify a result. lgse/strata#1119
- An alphanumeric query of 4 or more characters also matches a name word one edit away: `trahs` finds `strata-trash.svg`. lgse/strata#1119
- Literal matches rank above typo matches. lgse/strata#1119
- `*` matches zero or more characters across the whole name: `*.MOV` matches `clip.MOV` but not `clip.MOV.bak`. lgse/strata#989
- `IMG*.MOV` matches only names starting with `IMG` and ending in `.MOV`; `*` alone matches every name. lgse/strata#989
- Wildcard queries allow no typos, and other punctuation such as `?` or `[]` is literal. lgse/strata#989, lgse/strata#1119

### Scope

- With **Include subfolders** on, the default, results come from the current folder and all its descendants. lgse/strata#275, lgse/strata#602
- Recursive results show their path relative to the filtered folder below the name. lgse/strata#345
- With **Include subfolders** off, only immediate files and folders match, without path subtitles. lgse/strata#602
- Toggling **Include subfolders** refreshes active filters in every window without stale results, and the choice survives restarts. lgse/strata#602
- With **Include subfolders** off, a symlink to a folder matches as a folder and names in `.hidden` stay hidden while hidden files are off. lgse/strata#752
- At Trash, network, and other non-local locations, the filter narrows the loaded entries without searching subfolders. lgse/strata#995
- Results stop at 100; the status reads "Searching…", "No matching files", or the partial-search reason. lgse/strata#989 (unverified)

### Results

- Down from the field focuses the selected or first result; Up from the first result returns to the field with the query kept. lgse/strata#995, lgse/strata#1018
- One unmodified click or Enter opens a result, whatever the click-count and preview preferences. lgse/strata#697
- In Columns, a filtered result opens on release, so a press-and-move starts a drag instead. lgse/strata#753
- Space toggles quick preview for the selected file result and keeps the query; Shift+Space types a space. lgse/strata#585
- With preview open, Up and Down move it to the newly selected result. lgse/strata#1119
- Ctrl-click, Shift-click, Shift+Arrow, Ctrl+A, and marquee select results. lgse/strata#1018
- Dragging, the item menu, Ctrl+C, and Ctrl+X act on the selected results at their real locations. lgse/strata#639, lgse/strata#1018
- Right-click on empty result space still opens the background menu with New Folder and New File. lgse/strata#639
- A single file result's menu offers **Open file location**, which opens its folder with the file selected. lgse/strata#1041
- A result renamed, deleted, or moved through its menu leaves the results; a rename that still matches stays at its real parent. lgse/strata#800, lgse/strata#1155
- As results update, rows still matching keep their widgets, thumbnails, and selection, without flashing. lgse/strata#639, lgse/strata#778
- When the selected result disappears, the next result, or the last remaining one, is selected. lgse/strata#639
- Icons shows results as an icon grid and List as rows. lgse/strata#1155

## Design

Ctrl+F finds within the current location and Ctrl+K finds anywhere (lgse/strata#222, lgse/strata#1211).

- lgse/strata#277 asked for a current-folder scope in Ctrl+K. lgse/strata#275 instead made Ctrl+F search subfolders with the global index scoped to the folder.
- Subfolder search is a saved preference, on by default to keep existing behavior. A per-filter scope toggle was left for separate consideration (lgse/strata#586, lgse/strata#602).
- The filter matches names only, while Ctrl+K stays fuzzy over paths (lgse/strata#989, lgse/strata#1119). Wildcards are `*` only; regular expressions were not wanted (lgse/strata#988).
- Typo tolerance is limited to one edit in a whole word for 4 or more alphanumeric characters, so short queries stay literal (lgse/strata#1119).
- The directory-only index reuses the GIO listing's symlink and `.hidden` rules so filter results match the visible listing (lgse/strata#692, lgse/strata#752).
- Results are reconciled by full path, so progressive updates keep rows, thumbnails, focus, and selection (lgse/strata#620, lgse/strata#639, lgse/strata#719).
- Icons and List share one result collection with view-specific presentation; Columns keeps its native collection (lgse/strata#1155, lgse/strata#1167).
- Scope changes cancel the old search session, and a session drops batches for any query but the current one, so a stale worker cannot update a rebuilt view (lgse/strata#602, lgse/strata#1174).
- Results are pruned by checking that each path still exists, rather than tracking each operation's old and new paths (lgse/strata#800).
- Filtered results ignore the click-count and preview preferences, which keep governing unfiltered rows (lgse/strata#681, lgse/strata#697).
- Columns dismisses on any outside click through one window-level gesture, because focus stays in the entry when non-focusable widgets are clicked (lgse/strata#887).
- 10xer mode drives this same field for its **f** filter and **s** search with fzf-style path terms, overriding the subfolder preference without saving it (lgse/strata#1297, lgse/strata#1403).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-21 | lgse/strata#1155 | fix | Replaced the separate filtered view with a shared collection and kept matching renamed results searchable. |
| 2026-09-16 | lgse/strata#1041 | feat | Added Open file location to file results so a match can be opened in place. |
| 2026-09-15 | lgse/strata#1018 | fix | Restored drag, multi-selection, marquee, and clipboard actions on filtered results. |
| 2026-09-15 | lgse/strata#925 | fix | Kept the pane filter when switching view modes. |
| 2026-09-14 | lgse/strata#995 | fix | Filtered loaded entries in Columns at non-local locations such as Trash. |
| 2026-09-14 | lgse/strata#989 | feat | Added `*` whole-name patterns to the filter. |
| 2026-09-14 | lgse/strata#896 | fix | Closed a Columns filter when focus leaves its column. |
| 2026-09-12 | lgse/strata#887 | fix | Closed Columns filters on outside clicks and allowed only one open filter. |
| 2026-09-11 | lgse/strata#800 | fix | Removed results renamed, deleted, or moved from their menu. |
| 2026-09-11 | lgse/strata#778 | fix | Reused unchanged Columns result rows instead of replacing the model on each keystroke. |
| 2026-09-11 | lgse/strata#753 | fix | Opened filtered Columns results on release so drags do not launch files. |
| 2026-09-10 | lgse/strata#752 | fix | Matched the directory-only index to the GIO listing for folder symlinks and `.hidden`. |
| 2026-09-09 | lgse/strata#697 | fix | Opened results with one click or Enter regardless of click preferences. |
| 2026-09-09 | lgse/strata#639 | fix | Kept List and Icons result rows across updates and gave results the item menu. |
| 2026-09-08 | lgse/strata#602 | feat | Added the saved Include subfolders preference. |
| 2026-09-05 | lgse/strata#389 | fix | Restored Columns thumbnails and hover sizes when the filter is cleared. |
| 2026-09-05 | lgse/strata#387 | feat | Turned Type to search on by default. |
| 2026-09-05 | lgse/strata#345 | fix | Showed result paths relative to the filtered folder. |
| 2026-09-05 | lgse/strata#307 | feat | Added Type to search and subfolder results in Explorer and Grid. |
| 2026-09-04 | lgse/strata#275 | feat | Searched subfolders from the Ctrl+F filter. |

## Known gaps

- Escape with a result focused does not dismiss the filter in one press; the fix landed after this snapshot. lgse/strata#1440, lgse/strata#1533
- Switching view mode does not keep keyboard focus in the filter field; the fix landed after this snapshot. lgse/strata#1441, lgse/strata#1533
- Ctrl+F during a very large Icons load loses focus to the loading listing; the fix landed after this snapshot. lgse/strata#1444, lgse/strata#1533
- The filter cannot search file contents. lgse/strata#1211
