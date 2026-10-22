---
title: Columns view
status: shipped
origin: {issue: lgse/strata#140, pr: lgse/strata#171}
branch: null
reviewed_at: c94eeb0020fa1154e11c741888f1b56d92ce70d6
review: draft
code: [src/ui/browser/columns.rs, src/ui/browser/columns/rows.rs, src/ui/browser/columns/reveal.rs]
tests: [src/ui/browser/columns/tests.rs, tests/qa/scenarios/column_background]
docs: [docs/preview-panel-layout.md, docs/preferences.md]
related: [preview/preview-panel, preview/preview-panel/layout, browser/selection, browser/selection/click-modes, operations/rename, settings/preferences]
---

## Summary

Miller columns, the default view: each opened folder appends a column to a horizontally scrolling strip, so the path from the first folder to the current one stays visible.

## Behavior

### Opening and closing columns

- With default click settings, a single click on a folder opens it as the next column. lgse/strata#171
- Each column after the first has a "Close this pane" X button that closes it. lgse/strata#171
- Clicking a folder whose child column is already open focuses and reveals that column instead of closing it. Context-menu Open does the same. lgse/strata#1513, lgse/strata#1539
- A slow second click on the name of a selected, open folder still starts a rename. lgse/strata#1539
- Double-clicking a closed folder ends as a single click does: its column opens, focused and scrolled into view, with nothing selected in it. lgse/strata#1539 (unverified)
- The same holds when the first press scrolls the strip, with double-click folders, and from a partly clipped parent column. lgse/strata#1539
- With folders opening on one click, a plain click on a folder inside a multi-selection collapses the selection to it and opens its column. lgse/strata#1446, lgse/strata#1570
- With single-click previews on, a plain click on a previewable file inside a multi-selection collapses the selection to it and previews it. lgse/strata#1446, lgse/strata#1570
- With a folder open, opening a sibling fades the new column in where the old one stood, with no 24 px slide. Deeper columns of the old branch shrink away. lgse/strata#1539
- Pressing a folder does not shift the strip and shift it back before its column takes focus. lgse/strata#1539
- A column closed with nothing replacing it narrows and fades out over 220 ms. lgse/strata#1513, lgse/strata#1539
- That close animation covers its X button, Escape, Backspace, and a file click in a parent. lgse/strata#1539 (unverified)
- With reduced motion or animations off, a closing column is removed at once. lgse/strata#1539
- A closing column takes no clicks, hovers, or drops while it leaves. lgse/strata#1539
- Opening another location, rebuilding the strip, or switching away from Columns replaces the columns with no exit animation. lgse/strata#1539
- Deleting the focused, open folder, by mouse or keyboard, reveals the entry that takes its place, folder or file, and mirrors it. lgse/strata#1497, lgse/strata#1539
- That mirroring needs Mirror columns selection on; with it off, the replacement is only revealed. lgse/strata#1539 (unverified)
- A keyboard move reveals a column clipped by up to 4 px fully and leaves an already visible column in place. lgse/strata#1513, lgse/strata#1539
- A column wider than the viewport that already fills it stays in place; a partly off-screen one scrolls to its left edge. lgse/strata#1539
- With Mirror columns selection on, the default, Up or Down onto a folder shows its contents in the next column without moving focus. lgse/strata#1179
- Up or Down onto a previewable file opens Quick Preview when single-click previews are on; onto any other file it closes the child column. lgse/strata#1179
- Page Up, Page Down, Home, End, and Ctrl+Up or Ctrl+Down mirror the new cursor like Up or Down. Keypad Home and End do too, including after pointer input. lgse/strata#1447, lgse/strata#1533
- End onto a plain file closes the stale child column, and the breadcrumb follows the cursor. lgse/strata#1447, lgse/strata#1533
- In a column with no keyboard cursor yet, Home or Ctrl+Up lands on the first entry and End or Ctrl+Down on the last. lgse/strata#1447, lgse/strata#1533
- Shift+Home, Shift+End, and other Shift-extended ranges do not mirror. lgse/strata#1447, lgse/strata#1533
- Mirroring waits 75 ms after the last key, so holding Down loads only the folder where the cursor stops. lgse/strata#1179
- With Mirror columns selection on, Return on a folder still validating when the 75 ms mirror fires opens it in the next column. Focus lands on its first entry. lgse/strata#1771 (unverified)

### Returning to an ancestor

- Back, Forward, or Alt+Up to an ancestor selects the folder you came from, at any depth, with the cursor on it. lgse/strata#1437, lgse/strata#1544
- The came-from folder's own column stays closed; Alt+Left from `documents/b2` selects `b2` with no `b2` column. lgse/strata#1437, lgse/strata#1544
- When the came-from folder is gone, or hidden with hidden files off, the first visible entry is selected once the listing completes. Hidden files stay off and no error shows. lgse/strata#1437, lgse/strata#1544
- Back to a folder that is not an ancestor selects its first entry. lgse/strata#1437, lgse/strata#1544
- A sidebar place that is an ancestor of the current folder does not select the came-from folder. lgse/strata#1437 (unverified)

### Refreshing

- F5 keeps focus on a focused row, or in a focused Ctrl+F field, through the reload. lgse/strata#1434, lgse/strata#1544, lgse/strata#1729
- After a reload removes an open rename field, F2 renames that row again and Menu or Shift+F10 opens its context menu. lgse/strata#1438, lgse/strata#1554

### Column header

- The header shows the folder name, middle-ellipsized within the column, vertically centered with its actions. lgse/strata#805, lgse/strata#1143
- Header actions (Empty Trash at `trash:///`, Refresh, sort direction, Sort by, filter, Close) show only in the column targeted by the latest pointer or keyboard input. lgse/strata#555
- While an item or background context menu is open in a column, that column keeps the header actions even when the pointer moves over another column. lgse/strata#555
- The header spinner shows only while that column is loading and is hidden when idle, including after switching from another view. lgse/strata#411
- Clicking a column's title focuses that column, keeps its selection, and leaves deeper columns open. lgse/strata#523
- A dialog, popover, or focused filter field that opens before a rebuilt column's deferred refocus keeps keyboard focus. lgse/strata#1430, lgse/strata#1441, lgse/strata#1533

### Open-path marker

- The row of the folder whose column is active gets a strong accent fill; older folders on the open path get a faint one. lgse/strata#1265
- Clicking empty space in a column after the first pulses its parent folder's row for 420 ms. lgse/strata#1265 (unverified)

### Background clicks and scrolling

- Clicking empty space in an inactive column closes deeper columns, focuses and reveals that column, and selects its first visible entry. lgse/strata#523, lgse/strata#1164, lgse/strata#1265
- Clicking empty space in the active column clears the selection in every column and closes deeper columns. lgse/strata#522, lgse/strata#1265
- Clicking the blank strip right of the last column clears the selection. lgse/strata#522
- Clicking a column heading focuses that column without changing its selection or closing its child column. lgse/strata#523
- Clicking empty space in a column keeps that column's vertical scroll position instead of returning to the selected row. lgse/strata#1084
- Shift+wheel over a listing scrolls the column strip horizontally; vertical wheel ticks scroll only the listing. lgse/strata#1125
- Horizontal touchpad gestures over a listing scroll the column strip. lgse/strata#1125
- Columns fill the strip's full height with no per-column paste footer; the paste destination column is marked by its header. lgse/strata#1215
- The horizontal scrollbar shows no contrasting square at its leading edge. lgse/strata#696, lgse/strata#702

### Width

- Dragging a column's right edge resizes only that column while the pointer moves, never below 300 px. lgse/strata#114, lgse/strata#1539
- On release, the window's other open columns ease to the dragged width once; other windows keep theirs. A click on an edge without dragging also spreads. lgse/strata#1539
- A press within 6 px either side of the line between two columns resizes the left column, even when partly scrolled out of view. lgse/strata#1539
- Resting the pointer on a column edge for 400 ms shows a "Column width" caption, which follows the edge during a drag. lgse/strata#1539
- Hovering the edge of the column that meets the preview also lights the preview divider line. lgse/strata#1539
- Double-clicking a column's right edge eases that column alone to its widest content over 220 ms, never below 300 px. lgse/strata#114, lgse/strata#1539
- Autofit and edge drags stop at the visible browser area: the preview split less its divider, with the sidebar counted at full width. lgse/strata#1448, lgse/strata#1570
- The width cap never goes below the 300 px standard column, scaled by text size. lgse/strata#1570
- A resize or autofit is saved as `browser_column_width`, or `chooser_column_width` in the file chooser; new columns open at that width and open columns keep theirs. lgse/strata#1339, lgse/strata#1539
- An autofit saves its capped width. lgse/strata#1448, lgse/strata#1570
- A saved width wider than the area, such as `browser_column_width = 1729` in a 1200 px window, opens columns narrowed to the area. The setting is unchanged. lgse/strata#1448, lgse/strata#1570
- After a text-size change, open columns wider than the area are narrowed; returning to the earlier text size restores the dragged width. lgse/strata#1570
- Shrinking the window does not narrow open columns; dragging the edge of such a column snaps it to the area. lgse/strata#1570
- A cancelled edge drag restores the column's previous width. lgse/strata#1570 (unverified)

### Size badge

- Hovering or selecting a folder row, or a folder on the open path, shows "No items" or "N items" in the right-side badge. lgse/strata#1564
- Files show their size in the same badge. lgse/strata#1564
- With Show sizes in Columns view off, the badge stays hidden for files and folders in every open window. lgse/strata#1564
- With the setting off, Columns requests no folder counts. Turning it on fills counts for folder rows already shown. lgse/strata#1564
- A count that arrives after the setting is turned off leaves the badge hidden. lgse/strata#1564
- Moving the pointer onto a row fades its badge in over 120 ms. lgse/strata#1674
- Selecting a row, or opening a folder onto the open path, shows its badge at once. lgse/strata#1674
- Moving the selection off a row hides that row's badge at once. lgse/strata#1674
- Moving the pointer off a row hides its badge at once, without a fade. lgse/strata#1674
- With the pointer resting on an unselected row, arrow keys that move the selection hide that row's badge at once. lgse/strata#1674
- Moving the pointer then fades that badge in again. lgse/strata#1674 (unverified)
- While a row is being renamed its badge stays hidden; after the rename ends it returns only with the setting on. lgse/strata#1564
- In Columns, the Appearance menu has a "Show sizes in Columns view" check item after Group by file type. It toggles the same setting and closes the menu. lgse/strata#1564
- The Appearance item is hidden in Icons and List, and its check mark follows changes made in Settings. lgse/strata#1564

### Row drags

- Pressing a row and moving less than GTK's drag threshold starts no file drag. lgse/strata#1564

## Design

Columns is browse-as-you-go: a single click opens a folder, as in Finder, ranger, and lf. The X button was kept for discoverability, and Enter does not close a column because Backspace and Escape already do (lgse/strata#140).

- Header actions follow the latest input target to remove repeated icons. The header keeps a hidden page of the same size, so columns do not resize as the target moves (lgse/strata#552, lgse/strata#555).
- The came-from folder is derived from the ancestor chain of the current path, not stored per folder. It is selected without mirroring, so its column stays closed, and a missing one falls back quietly (lgse/strata#1437).
- Selection mirroring follows Finder's column view. The 75 ms timer re-checks focus when it fires, so a stale selection or an explicit close cannot reopen a column (lgse/strata#1178).
- Re-clicking an open folder focuses its column rather than closing it, so single clicks and double-clicks share one path. This replaces the close toggle of lgse/strata#171 (lgse/strata#1539).
- A folder press reuses the tab-location hold, so the reserved preview slot lends no width until the new column takes focus. A trace showed the strip shifting at the press (lgse/strata#1539).
- A closing column's width and opacity run from one tick callback on an accelerating curve, so they stay in lockstep (lgse/strata#1539).
- Edge hints are captions, not tooltips, because the repository allows tooltips only on icon-only buttons (lgse/strata#1539).
- Widths spread once on release, not every frame, to avoid relaying out every column per frame. Resizing the grabbed side was rejected: a column grows only at its right edge (lgse/strata#1539).
- The 4 px reveal tolerance was removed because it broke the rule that the focused column is always fully visible (lgse/strata#1539).
- The owner capped widths at the full visible area rather than the area less the preview minimum. Autofit keeps saving, List drags stay uncapped, and window shrinks do not re-clamp (lgse/strata#1448, lgse/strata#1570).
- The cap is captured at drag start, so it cannot creep as the preview yields (lgse/strata#1570).
- A plain press inside a multi-selection once kept the group for a drag and skipped activation. Activation already waits for release past a drag threshold, so the guard was dropped, matching List and Icons (lgse/strata#1446, lgse/strata#1570).
- Rows are recorded at setup and dropped at teardown, so a reload left a detached row with its old position. Lookups now take only the mapped row (lgse/strata#1438, lgse/strata#1554).
- Only pointer hover fades the badge. With badges on by default, keyboard navigation kept several 120 ms fades running and GTK repainted each per frame (lgse/strata#1671, lgse/strata#1674).
- Suppressing the hover fade during wheel scrolling with a class on the scrolling column was rejected. Toggling the class restyled the whole column at scroll start and end (lgse/strata#1674).
- Reveal buttons for clipped columns update after each layout pass instead of on every frame, so the frame clock can stop while the window is idle (lgse/strata#1671, lgse/strata#1677).
- Folder counts use the formatter List and Icons share, and Columns asks for them only while the badge is on, saving `read_dir` work. A widened-column redesign was rejected (lgse/strata#1564).
- Background focus fires on click release and is grouped with marquee selection, so neither gesture swallows the other (lgse/strata#523).
- Home and End go through Strata's own jump, like Ctrl+Up and Ctrl+Down. GTK's native keys emit only a selection echo the mirror ignores, and mirroring that echo risked the reopen loops lgse/strata#1179 avoided (lgse/strata#1447).
- Horizontal scroll is routed in the capture phase because nested vertical listings consume horizontal events (lgse/strata#1124).
- Autofit is detected as two drag starts on the same edge within 400 ms. A separate click gesture would compete with the drag for the event (lgse/strata#114).
- Saved widths are unscaled by text size, so text-size changes scale them without compounding. Browser and chooser defaults are independent (lgse/strata#1338).
- The "square" beside the scrollbar was the sidebar's paned handle showing through a transparent trough, so the mode scrollers' horizontal trough is opaque (lgse/strata#702).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-15 | lgse/strata#1674 | perf | Faded size badges only on pointer hover and indexed clipboard marks, to cut arrow-key and scroll cost. |
| 2026-10-15 | lgse/strata#1677 | perf | Updated column reveal buttons after each layout pass instead of every frame, so an idle window stops drawing frames. |
| 2026-10-11 | lgse/strata#1564 | feat | Showed folder item counts in the hover badge and added a setting to hide Columns sizes. |
| 2026-10-11 | lgse/strata#1570 | fix | Opened or previewed a plain-clicked item inside a multi-selection and capped column widths at the visible browser area. |
| 2026-10-10 | lgse/strata#1554 | fix | Looked up only the mapped row, so F2 and Menu reach a row after a reload ends its rename. |
| 2026-10-10 | lgse/strata#1539 | fix | Animated column open, close, swap, and autofit; focused open folders on re-click; spread drag widths on release; opened the replacement after a delete. |
| 2026-10-09 | lgse/strata#1533 | fix | Mirrored Home and End, made the strip one Tab stop, and gave empty columns a focusable surface. |
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

- There is no modifier to resize every visible column at once and no default-width setting. lgse/strata#1112
- A row passing under the pointer during wheel scrolling still plays the badge's hover fade. lgse/strata#1674
- With recursive filter results, the modal focus fallback, view switches, and hiding the preview with the mouse still focus GTK's last focused result, not the cursor's. lgse/strata#1611
