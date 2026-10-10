---
title: Position restore on return and refresh
status: shipped
origin: {issue: lgse/strata#868, pr: lgse/strata#893}
branch: null
reviewed_at: 72b840e69d6f0df9d33fb5583e62a3a2944886a1
review: draft
code: [src/ui/browser_modes/navigation.rs]
tests: [src/ui/window/tests/keyboard_dispatch/reload_cursor.rs]
related: [operations/clipboard]
---

## Summary

Icons and List remember each folder's selection, cursor, and scroll position, and restore them on return and through a refresh. It is for users moving through long folders who expect to continue from where they left off. Columns' came-from selection belongs to `browser/view-modes/columns`.

## Behavior

### Returning to a folder

- In Icons and List, returning to one of the last 128 folders left restores its selection, cursor, range anchor, and scroll position after loading. lgse/strata#893, lgse/strata#1436, lgse/strata#1544
- Back, Forward, Alt+Up, Backspace, a breadcrumb, and a path typed after Ctrl+L all restore it. lgse/strata#1436, lgse/strata#1544
- Opening a remembered folder another way, such as a sidebar place or a double-click, also restores its position. lgse/strata#893, lgse/strata#1544 (unverified)
- Pressing Down after a restore moves from the restored row, not the first row. lgse/strata#893, lgse/strata#1544
- Selection, cursor, and anchor carry between Icons and List: a folder left in Icons and reopened in List has the same entries selected. lgse/strata#1436, lgse/strata#1544
- The exact scroll offset returns only in the view the folder was left in, and for Icons only at the same grid width. Otherwise the view scrolls the cursor into view. lgse/strata#1436, lgse/strata#1544
- With no remembered position, returning to an ancestor selects the folder you came from, as Columns does. lgse/strata#1437, lgse/strata#1544
- Back, Forward, or Up into a remembered folder that is now empty gives keyboard focus to the pane, not the hidden list. lgse/strata#1466, lgse/strata#1533 (unverified)
- Opening a typed file path, a Ctrl+K result, Open file location, or a FileManager1 request selects that target instead of the remembered position. lgse/strata#1499
- A click, scroll, or key press in the pane before a restore settles cancels it. So do a view switch and a failed load. lgse/strata#893, lgse/strata#1544 (unverified)

### Focus on return

- In Icons and List, Back, Forward, and Up focus the restored listing only if focus was in the pane left or nowhere. Its Ctrl+F field counts as the pane. lgse/strata#1436, lgse/strata#1544
- Back from the pane header's Back button keeps focus on the button; with the sidebar focused, focus stays in the sidebar. lgse/strata#1436, lgse/strata#1544
- Sidebar places, breadcrumbs, and typed paths focus the new listing, as on a first visit. lgse/strata#1544
- A pane in a hidden tab, or while a rename is open in that pane, never takes focus when its restore applies. lgse/strata#1544 (unverified)

### Refreshing

- In Icons and List, F5, the Refresh button, auto-refresh, or a rescan past 4,096 queued changes keeps the cursor row, selection, and scroll offset. lgse/strata#1434, lgse/strata#1544
- After End then F5, the last row keeps the cursor at the same position on screen, and Left or Up moves from it. lgse/strata#1434, lgse/strata#1544
- In Icons and List, a refresh keeps focus on a focused row, or in a focused Ctrl+F field with its query. That holds through a slow reload. lgse/strata#1434, lgse/strata#1544
- Typing in the Ctrl+F field during that reload does not stop focus returning to it. Tab, Escape, or pointer input does. lgse/strata#1544
- Escape that closes the filter during the reload sends focus to the listing instead. lgse/strata#1544
- A refresh never takes focus from the sidebar, the location entry, or a dialog. lgse/strata#1434, lgse/strata#1544
- With a filter result focused, a refresh restores the viewport and leaves focus to the filter. lgse/strata#1544 (unverified)

## Design

Issue lgse/strata#868 asked for List's viewport and selection to survive entering a child folder and returning. Restoring only the selection was rejected, because the viewport would still be lost.

- Icons and List share one history of positions keyed by folder. Scroll offsets mean different things per view, and an Icons grid of another width wraps differently. The offset is reused only in the same view and width (lgse/strata#1436).
- lgse/strata#893 built the restore for List only; lgse/strata#1267 then described it for Icons and List without code (lgse/strata#1436).
- Restoring matches entries by location, not row number, so a deleted entry is never selected (lgse/strata#893). Where Ctrl+V pastes after a restore belongs to `operations/clipboard`.
- An explicit target beats the remembered position because the user named it (lgse/strata#1499).
- Focus follows the route. A sidebar place, breadcrumb, or typed path is an explicit visit and focuses the listing. History keys leave focus outside the pane where it is (lgse/strata#1544).
- A reload switches the pane to its pending page and empties the model. That unmaps the rows and resets GTK's cursor, scroll, and focus. The model keeps the selection by identity, and the view restores viewport and focus after the load (lgse/strata#1434, lgse/strata#1544).
- Views capture the outgoing position on `NavigationStarting` and `ColumnReloading`, before the model changes ([docs/architecture.md](https://github.com/lgse/strata/blob/72b840e69d6f0df9d33fb5583e62a3a2944886a1/docs/architecture.md), lgse/strata#1544).
- [docs/keyboard-navigation.md](https://github.com/lgse/strata/blob/72b840e69d6f0df9d33fb5583e62a3a2944886a1/docs/keyboard-navigation.md) carries the "Returning to a visited directory" and "Refreshing a directory" rules.

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-12 | lgse/strata#893 | feat | Restored selection, cursor, and scroll position when returning to a List folder. |

## Known gaps

None known.
