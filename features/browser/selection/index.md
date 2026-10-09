---
title: Selection
status: shipped
origin: {issue: lgse/strata#521, pr: lgse/strata#526}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [src/ui/collection_interaction.rs]
tests: [src/ui/collection_interaction/tests.rs, src/app/browser/tests/selection.rs, tests/e2e/scenarios/test_selection.py, tests/e2e/scenarios/test_background_selection.py, tests/e2e/scenarios/test_escape_selection.py, tests/e2e/scenarios/test_preselected_hover.py, tests/e2e/scenarios/test_monitor_selection.py]
docs: [docs/keyboard-navigation.md]
related: [browser/view-modes, integration/10xer-mode]
---

## Summary

Which entries are selected in Columns, Icons, and List, and how clicks, modifier clicks, Shift keys, Escape, and empty-space clicks change that. Children: `browser/selection/marquee` (rubber-band selection), `browser/selection/pointer-intent` (press-and-drag routing), `browser/selection/click-modes` (single- or double-click opening), and `browser/selection/keyboard-navigation` (arrow focus movement).

## Behavior

### Clicks

- A plain click on an entry selects only that entry and replaces the previous selection. lgse/strata#526 (unverified)
- Ctrl+click toggles one entry in or out of the selection and moves the range anchor to it. lgse/strata#526
- Shift+click selects every entry from the range anchor to the clicked entry. lgse/strata#526
- After a navigation auto-selects the first entry, the first Shift+click ranges from that entry, in all three views. lgse/strata#526
- A click re-anchors Shift+Down and Shift+Up, so keyboard extension continues from the clicked entry. lgse/strata#526
- Ctrl+click on a filename moves keyboard focus to the toggled entry, so the preview follows it. lgse/strata#1164
- Releasing Shift before the mouse button on blank row space keeps the pressed range, in Columns, Icons, and List. lgse/strata#786, lgse/strata#797
- Releasing Ctrl before the mouse button on blank row space still adds the row. lgse/strata#797
- Right-clicking an unselected entry makes it the only selected entry and the keyboard cursor. lgse/strata#666
- Right-clicking an entry inside a multi-selection keeps the whole selection. lgse/strata#666

### Keyboard selection

- Shift+Up and Shift+Down extend the selection by one entry from the range anchor. lgse/strata#526
- Shift+Page Up and Shift+Page Down extend or shrink the selection by one page from the range anchor. lgse/strata#1313
- The file chooser leaves Shift+Page Up and Shift+Page Down to GTK. lgse/strata#1313
- Shift+Down with nothing selected selects only the first entry; the next Shift+Down selects two. lgse/strata#738
- After Escape clears a selection, the next Shift+arrow range starts at the keyboard cursor. lgse/strata#1313
- Ctrl+A selects every entry in the focused column, not the deepest open column. lgse/strata#358
- With hidden files off, Ctrl+A in Icons, List, and the chooser leaves hidden entries unselected. lgse/strata#916
- Returning to a column with the keyboard keeps its multi-selection. lgse/strata#522

### Empty space

- A plain press on blank pane space clears the selection before the drag intent is known. lgse/strata#1164
- A Ctrl or Shift press on blank pane space keeps the selection. lgse/strata#522 (unverified)
- In Columns, a click on blank space in a column clears the selections of every column. lgse/strata#522
- In Columns, a click on blank space in a column closes the columns to its right. lgse/strata#1265
- A click on the blank strip right of the last column clears the selection. lgse/strata#522
- A click on blank content of an inactive column focuses it, scrolls it into view, and selects its first visible entry. lgse/strata#523, lgse/strata#526
- A click on a column heading focuses that column without changing its selection or closing its child column. lgse/strata#523
- A blank-space click in a scrolled column keeps its scroll position instead of returning to the selected row. lgse/strata#1084

### Escape

- With no transient UI open, Escape clears the active pane's selection and keeps the keyboard cursor and directory. lgse/strata#529
- In Columns, Escape clears only the active column; parent selections and open columns stay. lgse/strata#529
- An open menu, Properties, rename or new-entry editor, location editor, filter, or quick preview closes on the first Escape; the next clears the selection. lgse/strata#529
- Enter after Escape opens the folder under the keyboard cursor. lgse/strata#529
- In Columns, Escape with nothing selected closes the deepest column. lgse/strata#1179 (unverified)

### Keeping the selection

- F5 or the pane Refresh button keeps a multi-selection; entries gone from disk are dropped. lgse/strata#922
- Removing the focused entry focuses the next visible entry, else the previous visible one, and the preview follows. lgse/strata#1043, lgse/strata#1415
- Removing the last visible entry clears focus and selection. lgse/strata#1043, lgse/strata#1415
- Background changes to an open directory keep the selection and scroll position and do not take focus. lgse/strata#803

### Hover

- In List, the hover highlight and the click target cover the same row area, including the divider. lgse/strata#327
- An entry selected at startup or by keyboard folder entry shows hover feedback before any click, without changing selection. lgse/strata#805
- After keyboard navigation, a parked pointer's row hover and pending folder peek are suppressed until the pointer moves. lgse/strata#358

## Design

[docs/keyboard-navigation.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/keyboard-navigation.md) describes selection, the keyboard cursor, and the open-path marker as three separate signals (lgse/strata#358).

- Each directory has one range anchor, held in navigation state as a location. Pointer and keyboard share it, so it survives pane rebuilds and re-sorts (lgse/strata#526).
- Pointer selection decisions run on displayed positions in one shared module for all views and the chooser. Views translate the result to source entries (lgse/strata#1174).
- A modified press always claims its gesture, so GTK's unmodified release cannot replace the pressed range (lgse/strata#786, lgse/strata#797).
- Escape was chosen over clicking empty space, which a full pane lacks, and over a dedicated shortcut. Transient surfaces keep precedence (lgse/strata#528).
- Refresh snapshots selected locations and re-applies them after GTK reconnects its selection model (lgse/strata#922).
- The replacement after a removal skips hidden entries, mirroring how hiding hidden files moves focus (lgse/strata#1415).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-07 | lgse/strata#1415 | fix | Moved focus after a removal to the nearest visible entry instead of a hidden one. |
| 2026-09-28 | lgse/strata#1313 | feat | Extended the selection by a page with Shift+Page Up/Down. |
| 2026-09-16 | lgse/strata#1043 | fix | Moved focus to the neighbor of a removed entry instead of clearing it. |
| 2026-09-13 | lgse/strata#922 | fix | Kept a multi-selection across F5 refresh. |
| 2026-09-13 | lgse/strata#916 | fix | Excluded hidden entries from Select All in Icons, List, and the chooser. |
| 2026-09-11 | lgse/strata#797 | fix | Claimed Columns blank-space Shift+click so an early Shift release keeps the range. |
| 2026-09-10 | lgse/strata#786 | fix | Claimed List and Icons modified presses on blank row space so the range survives release. |
| 2026-09-10 | lgse/strata#738 | fix | Started Shift+arrow selection from one entry when nothing is selected. |
| 2026-09-07 | lgse/strata#529 | feat | Cleared the active selection with Escape after transient UI closes. |
| 2026-09-07 | lgse/strata#526 | fix | Shared one range anchor between clicks and the keyboard so the first Shift+click after navigation ranges. |

## Known gaps

- A plain click on empty preview pane space deselects the previewed file and blanks the preview; the fix is unmerged. lgse/strata#1450, lgse/strata#1546
- In List and Icons, F5 and large external change bursts move the keyboard cursor to the first entry; the fix is unmerged. lgse/strata#1434, lgse/strata#1544
- docs/keyboard-navigation.md says blank-column presses keep descendants and wait for marquee intent; the code clears on press and closes deeper columns. lgse/strata#1164, lgse/strata#1265
