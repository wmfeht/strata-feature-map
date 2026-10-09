---
title: Scrolling
status: shipped
origin: {issue: lgse/strata#293, pr: lgse/strata#311}
branch: null
reviewed_at: aee71335dfecd059b9af23efeac2ed52c43e3b19
review: draft
code: [src/ui/scrolling.rs, src/ui/scrolling/popover.rs]
tests: [src/ui/scrolling/popover/tests.rs, tests/e2e/scenarios/test_popover_scrolling.py, tests/e2e/mutations/popover-scrolling.patch]
related: [browser/view-modes, browser/view-modes/columns, browser/view-modes/text-size, browser/selection, operations/drag-and-drop/column-autoscroll]
---

## Summary

Fast ways through long listings in Columns, Icons, and List: middle-click autoscroll, Page Up/Down paging, and Ctrl+Up/Down or Home/End jumps to either end. Also covers the app's overlay scrollbars and how wheel and touchpad events reach the right scroller.

## Behavior

### Middle-click autoscroll

- Middle-clicking a Columns, Icons, or List listing that can scroll starts autoscroll and marks the press point with a round anchor. lgse/strata#311
- While autoscroll runs, the pointer over that listing shows the all-scroll cursor. lgse/strata#311 (unverified)
- Moving the pointer away from the anchor scrolls toward it, faster the further away, on both axes the listing can scroll. lgse/strata#311
- The pointer must move more than 12 px from the anchor before scrolling starts; speed reaches 32 px per 16 ms frame at 232 px. lgse/strata#311 (unverified)
- Escape, or another click with any button anywhere in the window, stops autoscroll. lgse/strata#311
- The click that stops autoscroll does not also select, open, or start a marquee. lgse/strata#311 (unverified)
- Middle-clicking a listing that fits its viewport starts no autoscroll. lgse/strata#311 (unverified)
- Middle-clicking a text field, such as the filter field, pastes as usual and starts no autoscroll. lgse/strata#311
- Mouse buttons 8 and 9 still go back and forward in history. lgse/strata#311
- Navigating away from, hiding, or closing a listing while it autoscrolls stops the autoscroll and hides the anchor. lgse/strata#311, lgse/strata#1187 (unverified)
- Escape while autoscroll runs stops only the autoscroll and cancels an armed 10xer chord. lgse/strata#1296, lgse/strata#1307 (unverified)

### Paging and jumps

- Page Up and Page Down, including the keypad keys, move the focus and selection by one page in the focused listing; in Columns only the focused column moves. lgse/strata#311
- A page is the number of rows that fit the viewport minus one, kept as overlap; in Icons it is those rows times the tiles per row. lgse/strata#311
- Paging stops at the first and last entry and keeps the selected item in view. lgse/strata#311
- In Icons the tiles per row follow the current width, so opening the preview or changing thumbnail size changes the next page at once. lgse/strata#373 (unverified)
- Ctrl+Up and Ctrl+Down select the first or last entry of the focused pane or column and scroll to that edge. lgse/strata#362
- Ctrl+Up and Ctrl+Down skip hidden entries unless hidden files are shown. lgse/strata#362
- Ctrl+Up or Ctrl+Down with Shift, Alt, or Super added does not jump. lgse/strata#362 (unverified)
- In the default key map, Home and End on a focused listing jump to the first or last entry like Ctrl+Up and Ctrl+Down. Keypad Home and End do the same. lgse/strata#1447, lgse/strata#1533
- Shift+Home and Shift+End extend the selection range instead of jumping. lgse/strata#1447, lgse/strata#1533
- Plain Home or End with several entries selected leaves only the target entry selected. lgse/strata#1447, lgse/strata#1533 (unverified)
- In Columns, Ctrl+Up, Ctrl+Down, Home, and End also jump while focus is on a column's list rather than a row. lgse/strata#1447, lgse/strata#1533

### Scrollbars

- Scrollbars across the app overlay their content with a 4 px accent thumb, at least 32 px long, on a faint rounded trough. lgse/strata#1141, lgse/strata#1208
- Scrollbars fade in on hover or scrolling and stay hidden at rest; the trough strengthens on hover and while dragging. lgse/strata#1141, lgse/strata#1208
- The vertical scrollbar of an Icons or List listing is 9 px wide, with a 7 px fully rounded thumb on a fainter trough. lgse/strata#1484
- The List vertical scrollbar has no gaps at its ends. lgse/strata#1484

### Wheel and touchpad routing

- A two-finger horizontal touchpad swipe over Columns scrolls the column strip. lgse/strata#1140
- Vertical touchpad scrolling in listings moves smoothly instead of in wheel-sized steps. lgse/strata#1140
- A wheel tick outside an open Sort by, Appearance, or Icons Thumbnail size panel closes it. lgse/strata#328, lgse/strata#590
- Wheel scrolling inside an open panel keeps it open. lgse/strata#590
- The tick that closes a panel also scrolls the listing under the pointer, and no other; over the sidebar or chrome it only closes the panel. lgse/strata#328, lgse/strata#590
- That forwarded tick moves the listing by the step a wheel notch normally moves it. lgse/strata#590 (unverified)
- Shift+wheel outside an open panel closes it and scrolls the pointed listing horizontally. lgse/strata#590 (unverified)

## Design

Issue lgse/strata#293 asked for fast movement through large folders. Raising wheel speed globally would hurt precise scrolling, and widening the scrollbar alone leaves keyboard and mouse gaps, so three gestures were added instead (lgse/strata#311).

- Only one autoscroll runs at a time, held in thread-local state, so any click or Escape can end it without knowing which view started it (lgse/strata#311).
- The anchor and pointer are kept in the scrolled window's coordinates, which do not move as content scrolls underneath. Speed grows with the square of the distance so small movements stay controllable (lgse/strata#311).
- A press is claimed only when the listing can scroll, so a listing that fits keeps the middle click for other handlers (lgse/strata#311).
- Autoscroll state once held its scroller strongly, a cycle that kept every retired listing alive. After 60 folder switches, loads grew from about 75 ms to 290 ms, so it now holds weak references (lgse/strata#1185, lgse/strata#1187).
- Icons pages scroll the viewport by pixels. GridView's `scroll_to` uses estimated cell sizes that lag behind a resize or preview split (lgse/strata#373). List and Columns scroll to the selected item.
- Ctrl+Up/Down was chosen over Home/End, which clashed with Alt+Home and text-field editing, and over Vim-style `gg`/`G`, which needed chord handling Strata lacked then (lgse/strata#357). Plain Home and End later joined them, handled by Strata in every view like Ctrl+Up/Down (lgse/strata#1447, lgse/strata#1533).
- lgse/strata#311 widened file-view scrollbar troughs to 14 px while keeping a 3 px visible bar. lgse/strata#1208 then made the path-bar overlay indicator the one style everywhere, removing the fixed-scrollbar opt-outs. Always-visible fixed bars with unified colors were rejected (lgse/strata#1141).
- lgse/strata#1484 gave Icons and List back a wider vertical grab target than the shared 4 px bar.
- The window-level Ctrl+wheel text zoom controller runs in the capture phase. GTK's `DISCRETE` flag masked the horizontal axis and claimed sub-step smooth deltas, so touchpad scrolling never reached descendant scrollers (lgse/strata#1124). The controller now accumulates deltas itself and passes events on unless Ctrl zoom applies (lgse/strata#1140).
- Outside wheel events can target the parent surface instead of the popup, depending on the display backend and GTK version. A panel therefore adds a capture wheel controller to its window while mapped (lgse/strata#590).
- Only scrollers marked as browser listings receive a forwarded tick, so a tick over the sidebar or chrome only closes the panel (lgse/strata#335).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-23 | lgse/strata#1208 | feat | Unified overlay scrollbars across views and highlighted the column under a file drag. |
| 2026-09-22 | lgse/strata#1187 | fix | Held autoscroll's scroller weakly so retired folder views are released and navigation stops slowing. |
| 2026-09-19 | lgse/strata#1140 | fix | Stopped the Ctrl+wheel zoom controller from swallowing smooth scroll events meant for descendant scrollers. |
| 2026-09-05 | lgse/strata#362 | feat | Added Ctrl+Up and Ctrl+Down to jump to the first or last entry of the focused pane. |
| 2026-09-05 | lgse/strata#311 | feat | Added middle-click autoscroll, Page Up/Down paging, and a wider scrollbar grab target. |

## Known gaps

- Middle-clicking a folder row starts autoscroll; opening the folder in a new tab instead is proposed. lgse/strata#1540
