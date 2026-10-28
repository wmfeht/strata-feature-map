---
title: Pane filter
status: shipped
origin: {issue: lgse/strata#277, pr: lgse/strata#275}
branch: null
reviewed_at: 86df474dc0e8352e0e2098637a017cc4c77a8c44
review: draft
code: [src/ui/inline_search.rs, src/ui/inline_search/**, src/ui/browser/collection.rs, src/ui/search_session.rs, src/ui/browser/columns/search.rs, src/services/search/directory.rs, src/services/search/pattern.rs]
tests: [src/ui/search_session/tests.rs, src/ui/browser/collection/tests.rs, src/services/search/directory/tests.rs, src/services/search/pattern/tests.rs, src/services/search/tests/scope.rs, src/ui/window/tests/keyboard_dispatch/filter_focus.rs, tests/qa/scenarios/filter_results/delete-trashes-filtered-result.jsonl, tests/qa/scenarios/filter_results/filtered-control-selection-group.jsonl, tests/qa/scenarios/filter_results/filtered-file-click-previews.jsonl, tests/qa/scenarios/filter_results/filtered-results-group-selection.jsonl, tests/qa/scenarios/filter_results/filter-results-follow-external-changes.jsonl, tests/qa/scenarios/filter_results/filter-updates-retain-state.jsonl, tests/qa/scenarios/filter_results/space-completes-composition.jsonl, tests/qa/scenarios/search_filter_sort/dismissing-filter-keeps-hidden.jsonl, tests/qa/scenarios/search_filter_sort/local-filtered-result-opens-once.jsonl, tests/qa/scenarios/search_filter_sort/recursive-filtered-result-opens-once.jsonl, tests/qa/scenarios/search_filter_sort/recursive-file-double-click-launches-once.jsonl, tests/qa/scenarios/search_filter_sort/type-to-search-finds-nested.jsonl, tests/qa/scenarios/search_filter_sort/wildcard-filter-patterns.jsonl, tests/qa/mutations/filter-results.patch]
docs: [site/src/reference/keyboard-navigation.md, docs/preferences.md]
related: [integration/10xer-mode, browser/context-menu, browser/view-modes, preview/quick-preview, browser/thumbnails, browser/view-modes/columns, integration/10xer-mode/search]
---

## Summary

The Ctrl+F filter narrows the focused pane by filename, in the current folder and, by default, its subfolders. It works in Columns, Icons, and List, and its results support the normal item actions. Child: `browser/search/filter/enter-target` (the outlined result Enter opens).

## Behavior

### Opening and closing

- Ctrl+F, or the pane's filter button, reveals the filter field for the focused pane. lgse/strata#307, lgse/strata#389
- With **Type to search** on, typing a printable character in a file view opens the filter with that character as the query. lgse/strata#307
- **Type to search** is on unless the user turned it off. lgse/strata#387
- With **Type to search** on, `/` in a file view opens an empty filter without inserting `/`. lgse/strata#416
- With **Type to search** on, keypad `/` opens an empty filter like `/`. lgse/strata#1576
- With **Type to search** on, a letter a layout types on the US `/` key, such as Icelandic þ, starts type-to-search with that letter. lgse/strata#1576
- Space in a file view opens quick preview, not the filter. lgse/strata#416
- Escape in the filter field, or clearing the query, restores the normal listing; hidden files stay hidden. lgse/strata#307, lgse/strata#310
- With a pinyin input method composing in the filter field, Escape cancels only the composition and the filter stays open. lgse/strata#1583
- Escape on a focused result closes the filter and shows the full listing at once. Focus goes to the directory's cursor row, with the directory's own selection. lgse/strata#1440, lgse/strata#1533
- Escape on a focused row also closes a filter that narrows rows in place. That covers Trash, Recent, network locations, and Columns with Include subfolders off. lgse/strata#1440, lgse/strata#1533
- With a result focused and its quick preview open, the first Escape closes only the filter. A second Escape closes the preview. lgse/strata#1440, lgse/strata#1533
- Switching between Columns, Icons, and List keeps the query, the open filter field, and the narrowed listing. lgse/strata#925
- Ctrl+1, Ctrl+2, or Ctrl+3 with the filter field focused keeps focus in the field with the caret after the query; Down then reaches a result. lgse/strata#1441, lgse/strata#1533
- Ctrl+1, Ctrl+2, or Ctrl+3 with a result focused moves focus to the carried-over results once they show. lgse/strata#1441, lgse/strata#1533
- Switching view from the View menu with a query typed gives the results focus once they show. lgse/strata#1441, lgse/strata#1533
- Press Ctrl+F while a large Icons or List folder is loading. When the load completes, focus stays in the field, so Ctrl+A and Backspace edit the query. lgse/strata#1444, lgse/strata#1533
- In Columns, a click outside the filtered column closes and clears its filter; a click inside that column keeps it. lgse/strata#887
- In Columns, after moving through filter results with the keyboard, Ctrl+F returns focus to that column's open filter field with its query. With Type to search on, `/` does the same. lgse/strata#1226 (unverified)

### Matching

- Plain text matches a case-insensitive substring of the file or folder name; parent folder names never qualify a result. lgse/strata#1119
- A query with spaces also matches a name that contains every word in any order: `duck txt` matches `ducks_in_the_pool.txt` and `duck.txt`, not `only-duck.md`. lgse/strata#1693, lgse/strata#1768
- `duck goose` does not match `ducks_in_the_pool.txt`, and `summer holiday` does not match `holiday.jpg`. lgse/strata#1768
- A trailing space keeps the matches: `duck ` still matches `duck.txt`. lgse/strata#1768
- An alphanumeric query of 4 or more characters also matches a name word one edit away: `trahs` finds `strata-trash.svg`. lgse/strata#1119
- In a query with spaces, each word of 4 or more alphanumerics allows one edit: `abc text` matches `abc_tent.doc`, but `abc tex` does not. lgse/strata#1768
- Literal matches rank above typo matches. A name containing the whole query ranks above names matching scattered words: with Include subfolders on, `duck txt` lists `duck txt notes.md` before `ducks_in_the_pool.txt`. lgse/strata#1119, lgse/strata#1768
- A name containing the whole query ranks above non-contiguous matches at any depth. lgse/strata#1899
- Where the filter narrows rows in place, editing `abc tex` to `abc text` shows `abc_tent.doc` at once. lgse/strata#1768
- `*` matches zero or more characters across the whole name: `*.MOV` matches `clip.MOV` but not `clip.MOV.bak`. lgse/strata#989
- `IMG*.MOV` matches only names starting with `IMG` and ending in `.MOV`; `*` alone matches every name. lgse/strata#989
- Wildcard queries allow no typos, and other punctuation such as `?` or `[]` is literal. lgse/strata#989, lgse/strata#1119
- In a query with `*`, spaces are literal and words are not matched separately: `duck *.txt` needs `duck ` at the start of the name. lgse/strata#1768 (unverified)

### Scope

- With **Include subfolders** on, the default, results come from the current folder and all its descendants. lgse/strata#275, lgse/strata#602
- Recursive results show their path relative to the filtered folder below the name. lgse/strata#345
- With **Include subfolders** off, only immediate files and folders match, without path subtitles. lgse/strata#602
- Toggling **Include subfolders** refreshes active filters in every window without stale results, and the choice survives restarts. lgse/strata#602
- With **Include subfolders** off, a symlink to a folder matches as a folder and names in `.hidden` stay hidden while hidden files are off. lgse/strata#752
- At Trash, network, and other non-local locations, the filter narrows the loaded entries without searching subfolders. lgse/strata#995
- Results stop at 100; the status reads "Searching…", "No matching files", or the partial-search reason. lgse/strata#989 (unverified)
- The filter, 10xer path search, and folder pickers read the saved search time and entry limits at each query. lgse/strata#1667
- After a limit changes in Settings, the next typed character restarts the index walk instead of reusing the running one. lgse/strata#1667
- A partial filter status shows the same partial-search message as Ctrl+K. lgse/strata#1667
- In Icons and List, with no results, the status sits centered horizontally and vertically in the results pane. lgse/strata#1648

### Live updates

- With a filter open, a match another program creates or renames in a watched folder appears in the results within about a second. lgse/strata#1439, lgse/strata#1544
- Watched folders are the filtered folder and, with Include subfolders on in Columns, the open columns below it. lgse/strata#1439, lgse/strata#1544
- A matching file another program deletes leaves the results as soon as the listing drops it, before the rescan finishes. lgse/strata#1439, lgse/strata#1544
- In Icons and List, when a deletion, rename, or move removes the last result, the status reads "No matching files", centered. lgse/strata#1648 (unverified)
- In Columns, Enter after Down opens a remaining hit, with no "Unable to open file" dialog. In List and Icons, Down from the field lands on a remaining hit. lgse/strata#1439, lgse/strata#1544
- With Include subfolders on, a change below the watched folders shows only after F5, a network re-list, a monitor rescan, or reopening the filter. lgse/strata#1439, lgse/strata#1544, lgse/strata#1729 (unverified)
- A result whose existence check fails or times out, as on a mount that stopped answering, stays; only a result proven gone leaves. lgse/strata#1729
- Dropped hits can leave fewer than 100 results while more candidates exist. The search then ranks twice as many candidates to fill them. lgse/strata#1729
- When another program deletes the listing's cursor entry in any view, a focused filter field or result keeps focus. lgse/strata#1439, lgse/strata#1544

### Results

- Down from the field focuses a result; in Icons and List, the outlined top result or the result picked since the last query change. Up from the first result returns to the field with the query kept. lgse/strata#995, lgse/strata#1018, lgse/strata#1822
- In List and Icons, Tab from a focused result leaves the results in one press. Shift+Tab then returns to the result that held the cursor. lgse/strata#1550, lgse/strata#1575
- Enter on a focused result opens it, file or folder, whatever the click-count and preview preferences. lgse/strata#697
- In the filter field or its results, Space toggles quick preview for the selected file result and keeps the query; Shift+Space types a space. lgse/strata#585, lgse/strata#1714
- With a file result selected, Space in the location bar, the preview find bar, or the archive password field types a space. lgse/strata#1714
- In those fields Space opens no preview, in every view. lgse/strata#1714
- With a file result selected and focus on a sidebar row or a toolbar button, Space does what that control does and does not preview the result. lgse/strata#1714
- In the file chooser, Space typed in the file name or location field with a result selected types a space. lgse/strata#1714
- With a pinyin input method composing in the filter, Space picks a candidate and does not open quick preview. lgse/strata#1583
- With preview open, Up and Down move it to the newly selected result. lgse/strata#1119
- Ctrl-click, Shift-click, Shift+Arrow, Ctrl+A, and marquee select results. lgse/strata#1018
- Dragging, the item menu, Ctrl+C, and Ctrl+X act on the selected results at their real locations. lgse/strata#639, lgse/strata#1018
- Right-click on empty result space still opens the background menu with New Folder and New File. lgse/strata#639
- A result renamed, deleted, or moved through its menu leaves the results; a rename that still matches stays at its real parent. lgse/strata#800, lgse/strata#1155
- As results update for the same query, rows still matching keep their widgets, thumbnails, and selection, without flashing. lgse/strata#639, lgse/strata#778, lgse/strata#1822
- When the selected result disappears, the next result, or the last remaining one, is selected. lgse/strata#639
- In List and Icons, Delete, or Shift+Delete and confirm, on a focused result moves focus to the first remaining selected result, with a visible focus ring. lgse/strata#1632
- If no selected result remains, focus goes to the result now in the deleted one's slot, or to the last result. Escape then closes the filter. lgse/strata#1632
- Deleting the last remaining result that way moves focus to the filter field; Escape then closes the filter. lgse/strata#1632
- Icons shows results as an icon grid and List as rows. lgse/strata#1155

## Design

Ctrl+F finds within the current location and Ctrl+K finds anywhere (lgse/strata#222, lgse/strata#1211).

- lgse/strata#277 asked for a current-folder scope in Ctrl+K. lgse/strata#275 instead made Ctrl+F search subfolders with the global index scoped to the folder.
- Subfolder search is a saved preference, on by default to keep existing behavior. A per-filter scope toggle was left for separate consideration (lgse/strata#586, lgse/strata#602).
- The filter matches names only, while Ctrl+K stays fuzzy over paths (lgse/strata#989, lgse/strata#1119). Wildcards are `*` only; regular expressions were not wanted (lgse/strata#988).
- Typo tolerance is limited to one edit in a whole word for 4 or more alphanumeric characters, so short queries stay literal (lgse/strata#1119).
- lgse/strata#1693 asked for the exact phrase first, then all words. Phrase hits rank first through the fuzzy score. A fixed −500 offset for scattered hits was dropped: it moved every scattered hit equally (lgse/strata#1768).
- Any query edit with a typo-eligible word counts as a full filter change. A typo edit can both add and remove matches (lgse/strata#1768).
- The directory-only index reuses the GIO listing's symlink and `.hidden` rules so filter results match the visible listing (lgse/strata#692, lgse/strata#752).
- Results are reconciled by full path, so progressive updates keep rows, thumbnails, focus, and selection (lgse/strata#620, lgse/strata#639, lgse/strata#719). Since lgse/strata#1822 search results keep their selection only across updates for the same query; the in-place filter keeps the listing's selection.
- lgse/strata#1628 selected the first match on each query change and was closed with a request to keep the selection ([comment](https://github.com/lgse/strata/pull/1628#issuecomment-6150008036)). lgse/strata#1643 first proposed keeping it. After pushback ([comment](https://github.com/lgse/strata/issues/1643#issuecomment-6154138056)), its description changed so a new query returns to the first match ([comment](https://github.com/lgse/strata/issues/1643#issuecomment-6237184764)).
- The in-place filter keeps the listing's selection because that selection belongs to the browser, not the filter (lgse/strata#1822).
- Icons and List share one result collection with view-specific presentation; Columns keeps its native collection (lgse/strata#1155, lgse/strata#1167).
- List and Icons results are one Tab stop, like the listings, because Tab otherwise took one press per result (lgse/strata#1550, lgse/strata#1575).
- Scope changes cancel the old search session, and a session drops batches for any query but the current one, so a stale worker cannot update a rebuilt view (lgse/strata#602, lgse/strata#1174).
- Results are pruned by checking that each path still exists, rather than tracking each operation's old and new paths (lgse/strata#800).
- The same check runs whenever a listing splice removes rows, whoever removed them, so outside deletions leave before the rescan. It costs at most 100 stat calls (lgse/strata#1439, lgse/strata#1544). Since lgse/strata#1729 it runs on a worker, and only a proven absence removes a result.
- Changes below the watched folders appear only on refresh. The GIO monitor watches only open folders, and recursive watching hits inotify limits (lgse/strata#1439).
- Filtered folders ignore the click-count preferences and open on one plain click (lgse/strata#681, lgse/strata#697).
- Filtered files follow the unfiltered click-count and preview rules. Always opening them left users with previews on unable to select or preview a filtered file (lgse/strata#1881, lgse/strata#1888).
- One rule decides a plain click on a filtered file in Columns, search results, and the in-place filter, so the three paths cannot drift apart. Chooser and trashed files never open from it (lgse/strata#1888).
- Columns dismisses on any outside click through one window-level gesture, because focus stays in the entry when non-focusable widgets are clicked (lgse/strata#887).
- The field and its results together count as the filter owning focus. Escape, view switches, and loads therefore treat a focused result like the field. Backspace dismissal stays field-only (lgse/strata#1440).
- Escape dismisses the filter before closing quick preview, the same order as in the field, the file chooser, and 10xer `f` results (lgse/strata#1440, lgse/strata#1533).
- A background load or live change refocuses the listing only when the listing itself held focus, never the filter field or its results (lgse/strata#1444, lgse/strata#1533).
- After an in-app delete, the focused widget is an unmapped row of the hidden listing, which cannot take keys. The results therefore reclaim focus from any unmapped list row, but only when focus was in the results (lgse/strata#1593, lgse/strata#1632).
- A fallback of the selected results to the focused one was reverted: it would change copy, cut, chooser accept, and menu targets (lgse/strata#1632).
- An outside deletion of the cursor entry follows that rule too. Before, deleting the cursor item outside the app left nothing focused (lgse/strata#1439, lgse/strata#1544).
- 10xer mode drives this same field for its **f** filter and **s** search with fzf-style path terms, overriding the subfolder preference without saving it (lgse/strata#1297, lgse/strata#1403).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-27 | lgse/strata#1899 | feat | Shared the filter's term and typo matcher with Ctrl+K so multi-word global queries match every term. |
| 2026-10-25 | lgse/strata#1888 | fix | Made a plain click on a filtered file follow the click-count and single-click preview preferences, so previews work on filtered files. |
| 2026-10-22 | lgse/strata#1822 | feat | Outlined the top result Enter opens and kept it in view until a pick or scroll, so Enter is predictable. |
| 2026-10-20 | lgse/strata#1768 | feat | Matched space-separated queries when the name contains every word, ranking whole-phrase hits first. |
| 2026-10-15 | lgse/strata#1632 | fix | Returned focus to the next result, or the filter field, after deleting a focused List or Icons result. |
| 2026-10-15 | lgse/strata#1667 | feat | Read configurable search time and entry limits at each query and restarted the walk when they change. |
| 2026-10-14 | lgse/strata#1648 | fix | Centered the empty-state status over the results and showed "No matching files" when pruning removes every result. |
| 2026-10-11 | lgse/strata#1575 | fix | Made List and Icons filter results one Tab stop, matching the listings. |
| 2026-10-10 | lgse/strata#1554 | fix | Tracked whether a filter query still awaits its first results, so the default footer can keep describing the folder. |
| 2026-10-09 | lgse/strata#1533 | fix | Kept focus with the filter on Escape from a result, across view switches, and through background loads. |
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

- In List and Icons, a reload briefly hides the filter field, so a character typed in that instant can be dropped. lgse/strata#1544
- In List and Icons, renaming a hit moves focus to the hit now in its slot. lgse/strata#1544
- The filter cannot search file contents. lgse/strata#1211
- In List and Icons, selecting a filter result leaves GTK's range origin in place. A following Shift+arrow can extend from a stale entry. lgse/strata#1871
