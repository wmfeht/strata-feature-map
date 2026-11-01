---
title: Search
status: shipped
origin: {issue: null, pr: lgse/strata#222}
branch: null
reviewed_at: 44bfeab305cfb68993bafcf4794fe0bbf7ff1433
review: reviewed
code: [src/services/search.rs, src/ui/search.rs, src/ui/window/composition/search.rs]
tests: [src/services/search/tests.rs, src/services/search/tests/multi_root.rs, src/services/search/tests/performance.rs, src/services/search/tests/refresh.rs, src/ui/search/tests.rs, tests/qa/scenarios/search_filter_sort/global-search-*]
docs: [docs/preferences.md]
related: [browser/navigation/folder-jump, devices/volumes, integration/10xer-mode, settings/preferences]
---

## Summary

Ctrl+K global search finds files and folders across Home and mounted local drives, from any folder. It matches by fuzzy name or path, or by every term of a multi-word query. It runs on a bounded in-memory index built by the same service as the pane filter. Children: `browser/search/filter` (the Ctrl+F pane filter) and `browser/search/exclusions` (user-defined global search exclusions).

## Behavior

### Opening and scope

- Ctrl+K or the header search button opens the search dialog over a blurred window; Ctrl+K again closes it. lgse/strata#222 (unverified)
- Every search covers the global roots that `devices/volumes` lists, whatever folder is open. lgse/strata#222, lgse/strata#493
- An ejected drive's results are gone the next time search opens. lgse/strata#493
- A drive mounted inside Home or another root appears once in results, not once per root. lgse/strata#493
- The search field's accessible description lists the searched locations and says remote shares are not included. lgse/strata#493, lgse/strata#1359
- The search field is named "Search files and folders…". lgse/strata#1896
- On open, the empty query shows "Type to search Home and mounted local drives"; clearing a typed query adds "Fuzzy matching · try a name or path fragment". lgse/strata#493 (unverified)
- The status text sits centered horizontally and vertically in the results area, with wrapped lines center-justified. lgse/strata#1648

### Matching and results

- A query also matches paths that contain its characters in order: `cat-01` matches `bucket-cat/file-01-noise.jpg`, below `cat-01-photo.jpg`. lgse/strata#695, lgse/strata#758
- Name matches rank above path-only matches, and a shallower duplicate ranks above a deeper one. lgse/strata#307, lgse/strata#493, lgse/strata#1899 (unverified)
- With `duck txt notes.md`, `ducks_in_the_pool.txt`, `duck.md`, and `goose.txt` under Home, `duck txt` lists only the first two, phrase match first. lgse/strata#1899
- Query terms may fall in different path parts: `subfolder txt` finds `nested/subfolder/notes.txt`. lgse/strata#1899
- `quarterly` lists `quarterly-summary.txt` and `quarterly-summary.md`; `quarterly txt` keeps the `.txt` file and drops the `.md` file. lgse/strata#1899
- Results rank in tiers: whole query in the name, whole query in the path, every term in the name, every term in the path, then fuzzy matches. lgse/strata#1899
- Path length, depth, folder type, and an exact-name bonus never move a result across tiers. A file named 200 `x`s then `duck txt.md`, 63 folders deep, ranks above `duck txt archive/notes.md`. lgse/strata#1899
- In a multi-word query, each term of four or more letters or digits tolerates one typo against a name or path word: `abc text` matches `abc_tent.doc`. A one-word query gets no typo tolerance. lgse/strata#1899 (unverified)
- A multi-word query is not a strict filter: a fuzzy-only match still shows, ranked below every term match. lgse/strata#1899
- The fuzzy match keeps a multi-word query's spaces, so it matches only paths that contain a space. lgse/strata#1899 (unverified)
- Terms match the path below the searched root, not the root's own path. lgse/strata#1899 (unverified)
- A contiguous match of accented or CJK characters ranks above the same characters separated by `_`. lgse/strata#739
- An NFC query such as `résumé` matches an NFD filename, and an NFD query matches an NFC filename. lgse/strata#813
- Dotfiles are indexed only while hidden files are shown. lgse/strata#376
- Generated trees such as `node_modules/`, `target/`, `.venv/`, `.cache/`, `go/pkg/mod/`, and `__pycache__/` are skipped; with hidden files shown, `.cargo/config.toml` stays searchable. lgse/strata#473, lgse/strata#1287
- Paths excluded by a `.gitignore` or `.ignore` file are not indexed. lgse/strata#758 (unverified)
- At most 100 results are shown, best first. lgse/strata#473
- Each result shows its name, its full path, and a thumbnail for images. lgse/strata#493, lgse/strata#548
- A spinner shows in the search bar while indexing runs. lgse/strata#72 (unverified)
- The footer shows key hints for navigate, open, and Alt+Enter "open containing folder", the last beside a folder-open icon. lgse/strata#1066, lgse/strata#1105
- When indexing stops early, the footer shows "Partial results"; its description names each cause, such as "some folders could not be read". lgse/strata#72, lgse/strata#493, lgse/strata#1066
- Hovering **Partial results** shows a tooltip with the same causes as its description; complete results clear the tooltip. lgse/strata#1667
- A small tree with one unreadable folder reports the unreadable folder, not an entry limit. lgse/strata#493
- A hit whose file was deleted is dropped before it shows. A hit whose check fails stays; only a hit proven gone is dropped. lgse/strata#1729
- A file operation that renames, moves, or deletes a folder during an index walk stops the walk there. The results are then marked partial. lgse/strata#1729
- While indexing adds results, the highlighted result stays selected by path and unchanged rows are not rebuilt. lgse/strata#758

### Search limits

- Every index walk stops at the saved time or entry limit; with **No limit** it walks until its roots are exhausted. Depth stays capped at 64. lgse/strata#1667
- Ctrl+K reads the saved limits each time it opens, including before Settings has opened; a changed limit applies at the next open. lgse/strata#1667
- Rescans for outside changes, F5, and network-folder re-lists rebuild an index with the limits it was opened with. lgse/strata#1667, lgse/strata#1729 (unverified)
- When the time or entry limit stopped the walk, the partial-search message ends "Raise the limits in Settings → General → Search & filtering." Other causes alone do not add it. lgse/strata#1667

### Outside changes

- A file another program creates, deletes, or renames in a watched local folder rescans every index whose walk lists that folder. lgse/strata#1439, lgse/strata#1544
- Changes in Recent or in non-native locations such as SFTP folders trigger no rescan. lgse/strata#1544 (unverified)
- A burst of such changes during a walk does not cancel it; one more walk follows after it publishes. lgse/strata#1439, lgse/strata#1544
- Rescans of one index for outside changes start at least 1 second apart, and every session sharing the index gets the new results. lgse/strata#1439, lgse/strata#1544
- A change in a folder the walk skips, such as `target/`, `node_modules/`, an exclusion, or a hidden folder, triggers no rescan. lgse/strata#1544
- Hidden folders are skipped only while hidden files are off, and folders 64 or more levels deep are skipped too. lgse/strata#1544 (unverified)
- For an index built without subfolders, only a change in its root folder triggers a rescan. lgse/strata#1544 (unverified)
- When another program moves a folder inside a watched folder, indexes rooted at or below it follow it. They restart at the new path. lgse/strata#1544 (unverified)
- F5, a network-folder re-list, and a monitor rescan also rescan every index listing that folder, coalesced the same way. lgse/strata#1544, lgse/strata#1729 (unverified)
- While Ctrl+K is open, a change in a watched folder under its roots triggers a full Ctrl+K rescan, at most once a second. lgse/strata#1544

### Keyboard and activation

- Up and Down move the highlight while the caret stays in the query field; typing edits the query. lgse/strata#758
- When the first result is preselected, one Down highlights the second result. lgse/strata#953
- Enter or a single click on a result opens it and closes search. lgse/strata#177, lgse/strata#758
- With an input method composing in the query field, Enter that the input method passes back after committing opens the highlighted result. lgse/strata#1583
- Opening a folder result navigates into that folder. lgse/strata#177 (unverified)
- Opening a file result reveals it selected in its folder and opens quick preview. lgse/strata#1499
- With **Open search results directly** on, opening a file result launches it instead of previewing it, and still reveals it in its folder. lgse/strata#144 (unverified)
- Alt+Enter, or right-click → **Open containing folder**, closes search and opens the result's parent with the result selected and focused. lgse/strata#1066
- Alt+Enter with Hyper or Meta held also opens the containing folder. lgse/strata#1576
- For a folder result, **Open containing folder** selects the folder in its parent rather than opening it. lgse/strata#1066
- Escape, or a click outside the dialog panel, closes search. lgse/strata#112 (unverified)
- With a pinyin input method composing in the query field, Escape cancels only the composition and search stays open. lgse/strata#1583
- Closing search with Escape, Ctrl+K, or a click outside the panel returns focus to its opener, such as the file list's cursor row. lgse/strata#1430, lgse/strata#1533
- Opening a result, or Open containing folder, hands focus to the revealed item in the browser rather than the control that opened search. lgse/strata#1430, lgse/strata#1533

### Folder jump palette

- Ctrl+Shift+K opens this dialog as a "Jump to a folder…" palette; Ctrl+K still opens global file search. lgse/strata#959
- Pressing Ctrl+Shift+K while the search palette is open closes it. lgse/strata#959 (unverified)
- Arrow keys choose a row, and Enter opens the chosen folder. lgse/strata#959
- Before any folder is recorded, the palette shows "No folder history yet". lgse/strata#959 (unverified)
- A query that matches no visited folder shows "No matching folders". lgse/strata#959 (unverified)
- Closing the palette with Escape returns focus to the control that opened it, such as the file list's cursor row. lgse/strata#1430, lgse/strata#1533
- Only local folders that finish loading are recorded as visits. lgse/strata#959
- A folder that fails to load is recorded after a successful retry. lgse/strata#959 (unverified)

## Design

Global search and the pane filter are separate tools: Ctrl+K finds anything anywhere, and Ctrl+F finds within the current folder (lgse/strata#222).

- lgse/strata#277 proposed a Current-folder scope in the Ctrl+K dialog. Instead the Ctrl+F filter learned to search subfolders (lgse/strata#275), and Ctrl+K was fixed to Home (lgse/strata#222).
- Ctrl+K later widened to mounted local drives because files on a USB drive were unreachable (lgse/strata#441, lgse/strata#493). Remote shares stay out of scope (lgse/strata#87).
- The index is in memory and bounded: by default 200,000 entries, depth 64, and 10 seconds of indexing (lgse/strata#13, lgse/strata#72). A disk-backed index was deferred for its own discussion (lgse/strata#72).
- Raising the default cap to 400,000 entries was rejected because it roughly doubles worst-case memory and query work (lgse/strata#471). The default stays; users opt into more.
- The time and entry limits are preferences because on rclone and other FUSE mounts each listing is a network round trip. The fixed 10 s walk missed visible files there. Warming the mount's cache and adding exclusions were rejected: neither fixes a large local tree (lgse/strata#1665, lgse/strata#1667).
- The entry limit still bounds index memory, so its row warns that higher limits use more memory (lgse/strata#1665, lgse/strata#1667).
- The limits are part of the shared-index key, so snapshots with different budgets are never shared (lgse/strata#1667).
- The **Partial results** tooltip is a deliberate exception to tooltips only on icon-only buttons (lgse/strata#1667).
- Concurrent sessions with the same roots, hidden-file setting, scope, and exclusions share one index snapshot. Only the best 100 matches are kept, in a bounded heap (lgse/strata#473).
- Roots share one entry budget and take turns, so a large Home cannot starve a drive (lgse/strata#493). Folders share indexing work so a dense subtree cannot exhaust the budget first (lgse/strata#758).
- Among directories with equal pending work, shallower ones are scheduled first, so sibling folders are found before deep subtrees (lgse/strata#1286, lgse/strata#1287).
- Generated trees are pruned by glob rather than whole dot-directories, so tool configuration stays searchable (lgse/strata#471, lgse/strata#473).
- The index is not a snapshot. Concurrent filesystem changes can cause transient omissions (lgse/strata#758).
- An outside change refreshes the shared index rather than restarting one session. Another pane sharing the index would otherwise keep the stale snapshot (lgse/strata#1439).
- Refreshes for outside changes coalesce to about one walk per second per index. A constantly changing folder, such as build output, cannot run walks back to back (lgse/strata#1439, lgse/strata#1544).
- The pruned-folder check caches its glob set per root; rebuilding it per change stalled the window for up to 1.8 s during bursts (lgse/strata#1544).
- Unreadable folders are reported apart from size limits, because a walker error had been described as a very large tree (lgse/strata#431).
- Matches sit in fixed score tiers, so length, depth, and fuzzy bonuses cannot invert their order. The fuzzy fallback stays on purpose, so a multi-word query is not a strict AND filter (lgse/strata#1899).
- Queries and indexed names are folded with lowercase and NFC, with an ASCII fast path (lgse/strata#809, lgse/strata#813).
- Ctrl+Shift+K reuses this dialog to rank visited folders; that folder jump belongs to `browser/navigation/folder-jump`.

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-10 | lgse/strata#1539 | fix | Read the new column-truncation event shape when recording visited folders. |
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
- During bursts of outside changes, a rescan request can block the window for up to one scoring pass. lgse/strata#1544
- Whether global search scans mounts the volume monitor hides, such as a cache subvolume, is undecided. lgse/strata#533
- Index walks bypass the mount request lanes. A walk that reaches a dead mount waits until the server answers. lgse/strata#1729
