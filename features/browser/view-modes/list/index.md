---
title: List view
status: shipped
origin: {issue: lgse/strata#188, pr: lgse/strata#191}
branch: null
reviewed_at: bae71c026b94e109b7507c4fe895c3ceed642f8f
review: draft
code: [src/ui/browser_modes/list_factory.rs, src/ui/browser_modes/grouped_model.rs, src/ui/browser_modes/list_headings.rs, src/ui/browser_modes/list_pane.rs]
tests: [tests/qa/scenarios/view_switching/list-column-resize-tracks-pointer.jsonl, src/ui/browser_modes/grouped_model/tests.rs, tests/qa/scenarios/search_filter_sort/grouped-list-keeps-file-targets.jsonl]
related: [browser/navigation]
---

## Summary

A single-pane table of the current folder with Name, Mode, Size, Type, and Modified columns, sortable headings, and optional file-type groups. Formerly called Explorer. Child: `browser/view-modes/list/column-layout` (column order and visibility). Restoring a folder's position on return or refresh is shared with Icons and belongs to `browser/view-modes/position-restore`.

## Behavior

### Table

- By default List shows Name, Mode, Size, Type, and Modified columns, in that order. lgse/strata#308, lgse/strata#1651
- Name takes the width left after the metadata columns until it is resized by hand; below the minimum widths the table scrolls horizontally. lgse/strata#191
- Mode shows a type character, symbolic permissions, and the octal value, such as `drwxrwxrwx  777`, in full at its default 160 px width. lgse/strata#308, lgse/strata#492
- A folder's Size cell shows "No items" or its item count, such as "4 items"; files show their size. lgse/strata#1564
- The count covers the folder's immediate entries, hidden ones included, and not deeper contents. lgse/strata#1564
- A folder that cannot be read, or one without a local path, leaves its Size cell blank. lgse/strata#1564 (unverified)
- Type shows the description of the MIME type guessed from the filename, such as "JSON document"; folders show "Folder" and unrecognized files "Other". lgse/strata#946

### Headings

- Clicking the Name, Size, Type, or Modified heading sorts by that field ascending; clicking the current sort heading reverses it, and an arrow marks it. lgse/strata#877
- Clicking the Mode heading does not sort. lgse/strata#308
- List has no Sort by menu outside Recent and Camera Photos. lgse/strata#335 (unverified)
- Dragging a heading's right edge resizes that column and follows the pointer without an initial jump. lgse/strata#931
- A drag cannot shrink a column below its minimum: Name 160, Mode 80, Size 70, Type 80, and Modified 110 px. lgse/strata#191 (unverified)
- Double-clicking a heading's right edge fits the column to its widest content. lgse/strata#1116
- Resized widths are saved as `[browser_list_columns]`, or `[chooser_list_columns]` in the file chooser, and new List panes open with them; Name is saved only after it is resized itself. lgse/strata#1339

### Grouping

- Appearance → Group by file type is sensitive only in List. lgse/strata#510
- With grouping on, folders form a Folder group first, then files group under their MIME descriptions A–Z with Other last, keeping the pane's sort inside each group. lgse/strata#235, lgse/strata#946
- While sorted by Type, groups follow the sort: Descending reverses them with Other first, and Folder leads only when Folders first is on. lgse/strata#946 (unverified)
- The setting is saved across restarts. lgse/strata#235
- Grouping is not applied in Recent or in a Camera Photos library while it loads or uses Device order. lgse/strata#1029 (unverified)
- With grouping on, a 100,000-entry folder of mixed file types finishes loading with its files and previews, without repeated whole-list stalls. lgse/strata#1913, lgse/strata#1928

### Rows

- A click selects the row whose hover highlight is shown; no strip between rows highlights one row but selects another. lgse/strata#327
- Hovered and selected rows use the same rounded highlight as Columns, dimmed when the list loses focus. lgse/strata#554
- Rows bound while scrolling show their text, icon, and a static date at once; cut styling and live-updating dates apply once scrolling settles. lgse/strata#371, lgse/strata#1081, lgse/strata#1673 (unverified)

## Design

Explorer's Name column started at a fixed 600 px and pushed metadata out of narrow windows. Name now absorbs the leftover space; a smaller fixed width and relying on horizontal scrolling were rejected (lgse/strata#188).

- Grouping uses list-view sections, so one selection, keyboard navigation, and marquee span every group (lgse/strata#235). Icons lost grouping because grouped grids inflated cards and could abort GTK (lgse/strata#372, lgse/strata#509).
- Grouping projects the pane's sorted rows into type buckets with the existing type comparator, replacing GTK's sort model and section sorter. Arrivals are binary-searched into their group, so mixed-type batches emit narrow changes instead of regrouping the whole list (lgse/strata#1913, lgse/strata#1928).
- A background MIME-preparation and notification-batching experiment reached sub-second loads but was left out of lgse/strata#1928 ([comment](https://github.com/lgse/strata/pull/1928#issuecomment-6478299896)).
- Autofit measures each cell with its fixed width and one-character label cap lifted; with them in place the measurement returned the current width (lgse/strata#1115).
- Scroll deferral began as the Icons 80 ms settle (lgse/strata#368, lgse/strata#371). lgse/strata#1081 replaced the fixed wait with the next GTK frame, so continuous scrolling does not postpone updates. lgse/strata#1673 returned to a quiet period, recorded on `browser/view-modes`.
- List, Icons, and Columns format folder counts with one shared function, so the three views match (lgse/strata#1564).
- Mode's default width is 160 px so the octal value fits at every text size (lgse/strata#435).
- Saved widths are unscaled by text size, and browser and chooser widths are independent (lgse/strata#1338).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-11-01 | lgse/strata#1928 | perf | Grouped List by type buckets and a lazy index, so mixed-type arrivals no longer regroup the whole list. |
| 2026-10-11 | lgse/strata#1564 | feat | Showed folder item counts in the Size column, matching Icons. |
| 2026-09-19 | lgse/strata#1116 | fix | Made double-click autofit work on List heading resize edges. |
| 2026-09-12 | lgse/strata#893 | feat | Restored selection, cursor, and scroll position when returning to a List folder. |
| 2026-09-08 | lgse/strata#608 | refactor | Moved List item setup, binding, and thumbnail cancellation into a factory module. |
| 2026-09-07 | lgse/strata#554 | fix | Matched List row hover and selection styling to Columns. |
| 2026-09-07 | lgse/strata#492 | fix | Widened the default Mode column to 160 px so octal permissions show. |
| 2026-09-05 | lgse/strata#371 | perf | Deferred List icon, metadata, and date work until scrolling settles. |
| 2026-09-05 | lgse/strata#327 | fix | Removed row padding so hover and click share the same bounds. |
| 2026-09-04 | lgse/strata#308 | feat | Added a non-sortable Mode column with file permissions. |
| 2026-09-04 | lgse/strata#235 | feat | Added Group by file type for Explorer and Grid. |
| 2026-09-03 | lgse/strata#191 | feat | Let the Name column absorb the space left after the metadata columns. |

## Known gaps

- List cannot expand folders in place as a tree; a PR is open. lgse/strata#1495, lgse/strata#1496
- Grouped loads of very large folders are not sub-second: a 100,000-entry mixed-type folder takes about 2 s to publish. lgse/strata#1928
- In grouped List, a first visit by typed path puts the cursor on the first entry by name, not the first visible row. That is the visually last file of a 4-file folder, or the middle of a 44,000-file one. lgse/strata#2016
