---
title: List view
status: shipped
origin: {issue: lgse/strata#188, pr: lgse/strata#191}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: reviewed
code: [src/ui/browser_modes/list_factory.rs, src/ui/browser_modes/navigation.rs]
tests: []
docs: [docs/keyboard-navigation.md]
related: [browser/navigation]
---

## Summary

A single-pane table of the current folder with Name, Mode, Size, Type, and Modified columns, sortable headings, and optional file-type groups. Formerly called Explorer.

## Behavior

### Table

- List shows Name, Mode, Size, Type, and Modified columns. lgse/strata#308
- Name takes the width left after the metadata columns until it is resized by hand; below the minimum widths the table scrolls horizontally. lgse/strata#191
- Mode shows a type character, symbolic permissions, and the octal value, such as `drwxrwxrwx  777`, in full at its default 160 px width. lgse/strata#308, lgse/strata#492
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

### Returning to a folder

- Back, Forward, and Up restore the selection, keyboard cursor, and scroll position of each of the last 128 folders left in List, once its entries load. lgse/strata#893
- Pressing Down after a restore moves from the restored row, not the first row. lgse/strata#893
- Opening a remembered folder another way, such as double-clicking it, also restores its position. lgse/strata#893 (unverified)
- A restored selection does not make Ctrl+V paste into the selected folder until the user selects it explicitly. lgse/strata#893
- Opening a typed file path, a Ctrl+K result, Open file location, or a FileManager1 request selects that target instead of the remembered position. lgse/strata#1499

### Rows

- A click selects the row whose hover highlight is shown; no strip between rows highlights one row but selects another. lgse/strata#327
- Hovered and selected rows use the same rounded highlight as Columns, dimmed when the list loses focus. lgse/strata#554
- Rows bound while scrolling show their text, icon, and a static date at once; cut styling and live-updating dates apply on the next frame. lgse/strata#371, lgse/strata#1081 (unverified)

## Design

Explorer's Name column started at a fixed 600 px and pushed metadata out of narrow windows. Name now absorbs the leftover space; a smaller fixed width and relying on horizontal scrolling were rejected (lgse/strata#188).

- Grouping uses list-view sections, so one selection, keyboard navigation, and marquee span every group (lgse/strata#235). Icons lost grouping because grouped grids inflated cards and could abort GTK (lgse/strata#372, lgse/strata#509).
- Autofit measures each cell with its fixed width and one-character label cap lifted; with them in place the measurement returned the current width (lgse/strata#1115).
- Scroll deferral began as the Icons 80 ms settle (lgse/strata#368, lgse/strata#371). lgse/strata#1081 replaced the fixed wait with the next GTK frame, so continuous scrolling does not postpone updates.
- Restoring matches entries by location, not row number, so a deleted entry is never selected; a restored selection does not redirect paste until it is selected again (lgse/strata#893).
- An explicit target beats the remembered position because the user named it (lgse/strata#1499).
- Mode's default width is 160 px so the octal value fits at every text size (lgse/strata#435).
- Saved widths are unscaled by text size, and browser and chooser widths are independent (lgse/strata#1338).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
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
