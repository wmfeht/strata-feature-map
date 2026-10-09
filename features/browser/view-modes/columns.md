---
title: Columns view
status: shipped
origin: {issue: lgse/strata#140, pr: lgse/strata#171}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [src/ui/browser/columns.rs, src/ui/browser/columns/rows.rs, src/ui/browser/columns/reveal.rs]
tests: [tests/e2e/scenarios/test_column_headers.py, tests/e2e/scenarios/test_column_background.py]
related: [preview/preview-panel, browser/selection]
---

## Summary

Miller columns, the default view: each opened folder appends a column to a horizontally scrolling strip, so the path from the first folder to the current one stays visible.

## Behavior

### Opening and closing columns

- With default click settings, a single click on a folder opens it as the next column. lgse/strata#171
- Clicking the name of a folder whose column is already open starts slow-click rename instead of closing its column. lgse/strata#1265
- Each column after the first has a "Close this pane" X button that closes it. lgse/strata#171
- With Mirror columns selection on, the default, Up or Down onto a folder shows its contents in the next column without moving focus. lgse/strata#1179
- Up or Down onto a previewable file opens Quick Preview when single-click previews are on; onto any other file it closes the child column. lgse/strata#1179
- Mirroring waits 75 ms after the last key, so holding Down loads only the folder where the cursor stops. lgse/strata#1179

### Column header

- The header shows the folder name, middle-ellipsized within the column, vertically centered with its actions. lgse/strata#805, lgse/strata#1143
- Header actions (Empty Trash at `trash:///`, Refresh, sort direction, Sort by, filter, Close) show only in the column targeted by the latest pointer or keyboard input. lgse/strata#555
- While an item or background context menu is open in a column, that column keeps the header actions even when the pointer moves over another column. lgse/strata#555
- The header spinner shows only while that column is loading and is hidden when idle, including after switching from another view. lgse/strata#411
- Clicking a column's title focuses that column, keeps its selection, and leaves deeper columns open. lgse/strata#523

### Background clicks and scrolling

- Clicking empty space in an inactive column focuses that column and scrolls it into view. lgse/strata#523
- Clicking empty space in the active column clears its selection and closes deeper columns. lgse/strata#1265
- Clicking empty space in a column keeps that column's vertical scroll position. lgse/strata#1084
- Shift+wheel over a listing scrolls the column strip horizontally; vertical wheel ticks scroll only the listing. lgse/strata#1125
- Horizontal touchpad gestures over a listing scroll the column strip. lgse/strata#1125 (unverified)
- Columns fill the strip's full height with no per-column paste footer; the paste destination column is marked by its header. lgse/strata#1215
- The horizontal scrollbar shows no contrasting square at its leading edge. lgse/strata#696, lgse/strata#702

### Width

- Dragging a column's right edge resizes it, never below 300 px. lgse/strata#114
- Double-clicking a column's right edge fits the column to its widest content, never below 300 px. lgse/strata#114
- A resize or autofit is saved as `browser_column_width`, or `chooser_column_width` in the file chooser; new columns open at that width and open columns keep theirs. lgse/strata#1339

## Design

Columns is browse-as-you-go: a single click opens a folder, as in Finder, ranger, and lf. The X button was kept for discoverability, and Enter does not close a column because Backspace and Escape already do (lgse/strata#140).

- Header actions follow the latest input target to remove repeated icons. The header keeps a hidden page of the same size, so columns do not resize as the target moves (lgse/strata#552, lgse/strata#555).
- Selection mirroring follows Finder's column view. The 75 ms timer re-checks focus when it fires, so a stale selection or an explicit close cannot reopen a column (lgse/strata#1178).
- Background focus fires on click release and is grouped with marquee selection, so neither gesture swallows the other (lgse/strata#523).
- Horizontal scroll is routed in the capture phase because nested vertical listings consume horizontal events (lgse/strata#1124).
- Autofit is detected as two drag starts on the same edge within 400 ms. A separate click gesture would compete with the drag for the event (lgse/strata#114).
- Saved widths are unscaled by text size, so text-size changes scale them without compounding. Browser and chooser defaults are independent (lgse/strata#1338).
- The "square" beside the scrollbar was the sidebar's paned handle showing through a transparent trough, so the mode scrollers' horizontal trough is opaque (lgse/strata#702).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-24 | lgse/strata#1215 | fix | Removed the bottom gap and the per-column paste footer. |
| 2026-09-23 | lgse/strata#1179 | feat | Mirrored keyboard selection into the next column, as in Finder. |
| 2026-09-18 | lgse/strata#1125 | fix | Routed horizontal and Shift+wheel scrolling to the column strip. |
| 2026-09-18 | lgse/strata#1084 | fix | Kept a column's scroll position when its empty space is clicked. |
| 2026-09-16 | lgse/strata#1072 | fix | Drew one sidebar divider without a gap before the first column. |
| 2026-09-09 | lgse/strata#702 | fix | Made the horizontal trough opaque to hide the sidebar handle beneath it. |
| 2026-09-09 | lgse/strata#696 | fix | Painted the horizontal scrollbar with the theme background to remove an edge square. |
| 2026-09-07 | lgse/strata#555 | feat | Showed header actions only in the latest input's column and kept a context menu's column targeted. |
| 2026-09-07 | lgse/strata#453 | fix | Vertically centered row labels with their icons. |
| 2026-09-07 | lgse/strata#523 | fix | Focused and revealed a column when its empty space or header is clicked. |
| 2026-09-06 | lgse/strata#411 | fix | Stopped header spinners left running after view switches. |
| 2026-09-03 | lgse/strata#171 | feat | Opened folders on single click and closed a child column by clicking its folder again. |
| 2026-09-01 | lgse/strata#114 | feat | Added double-click autofit on column resize edges. |

## Known gaps

- Home and End move the cursor without updating the mirrored child column; the fix is unmerged. lgse/strata#1447, lgse/strata#1533
- Back, Up, or a breadcrumb return to a parent selects its first entry instead of the folder you came from; the fix is unmerged. lgse/strata#1437, lgse/strata#1544
- Double-click autofit has no upper bound, and the fitted width becomes the saved default. lgse/strata#1448
- Closing a column and autofit change width without animation, and keyboard moves between columns shift the open preview panel. lgse/strata#1513
- There is no modifier to resize every visible column at once and no default-width setting. lgse/strata#1112
