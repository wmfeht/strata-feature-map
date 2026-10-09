---
title: Drag and drop
status: shipped
origin: {issue: lgse/strata#285, pr: lgse/strata#350}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: []
tests: [tests/e2e/scenarios/test_drag_and_drop.py, tests/e2e/scenarios/test_drag_animation.py, tests/e2e/scenarios/test_sidebar_file_drops.py, tests/e2e/mutations/drag-and-drop.patch]
docs: [docs/preferences.md]
related: [operations/trash, operations/clipboard, browser/selection, browser/tabs]
---

## Summary

Moving and copying files by dragging them onto folders, pane backgrounds, sidebar places, and breadcrumbs, within and between windows and to or from other applications. Children: `operations/drag-and-drop/copy-or-move` (choosing copy or move, including across devices) and `operations/drag-and-drop/column-autoscroll` (edge scrolling during Columns drags).

## Behavior

### Starting a drag

- Pressing an unselected item while another is selected and dragging it drags only that item, and the selection moves to it on press. lgse/strata#789
- Dragging one item of a multi-selection transfers every selected item. lgse/strata#415 (unverified)
- In List with one-click folder activation, pressing and moving a folder starts a drag; a click without movement opens the folder. lgse/strata#348
- Ctrl-drag and Shift-drag that start on an item's icon or name start a file drag in Columns, List, and Icons. lgse/strata#623
- In Columns, dragging a folder whose child column is open onto a sibling folder moves the folder and its contents. lgse/strata#415
- In Columns, dragging a file from a column clipped by a narrow window starts a drag and drops normally. lgse/strata#1049
- Ctrl+F filter results, with Include subfolders on or off, can be dragged singly or as a selected group. lgse/strata#1018
- In Columns, a press-and-move on a filter result starts a drag instead of opening the file. lgse/strata#753
- Dragging the preview header or an image preview drags the previewed file. lgse/strata#292

### Drag feedback

- A single-item drag shows the item's file or folder icon instead of its name. lgse/strata#1487
- A multi-item drag shows stacked icons with an accent badge giving the item count. lgse/strata#1487 (unverified)
- A folder row, sidebar row, or breadcrumb under a file drag is outlined with the selection border and corner geometry. lgse/strata#1487
- Starting a drag closes any open folder peek, and cancelling a drag over a folder leaves that folder unopened. lgse/strata#630
- In Columns, after a drag ends by Escape, release outside the window, copy, move, no-op, or failed transfer, the source label stays in place and its dimming clears within 240 ms. lgse/strata#637

### Drop targets

- Dropping onto a folder row in Columns, List, or Icons transfers the dragged items into that folder. lgse/strata#587
- Dropping onto the background of a pane or column showing another folder transfers into that folder. lgse/strata#587 (unverified)
- Sidebar Home, standard places, pinned folders, and mounted native devices accept file drops from every view; Network and other URI locations do not. lgse/strata#350
- Parent breadcrumbs accept file drops. lgse/strata#1487
- Folder rows and panes for Trash and Recent accept no file drops. lgse/strata#350 (unverified)
- Dropping a folder onto itself or its descendants, or items onto their own folder, transfers nothing and opens no progress dialog. lgse/strata#587
- When a dropped selection mixes items already in the destination with others, the others still transfer. lgse/strata#502
- Pressing Escape or releasing outside every drop target ends the drag without transferring. lgse/strata#630
- A file list dragged from another application transfers like an internal drag; image, text, and web-link payloads are refused. lgse/strata#1545
- Dragged items are offered as a GDK file list and a `text/uri-list`, so other applications can receive them. lgse/strata#292 (unverified)

### Spring-loaded navigation

- Holding a file drag over a folder row, sidebar row, or parent breadcrumb for 750 ms navigates there, and the drag stays held. lgse/strata#1487
- Spring navigation can return to the drag's source folder, and releasing over a spring-opened pane's background drops into that folder. lgse/strata#1487
- Dropping onto a breadcrumb before 750 ms transfers into it without navigating. lgse/strata#1487
- Leaving the hovered target or dropping before 750 ms cancels the pending navigation. lgse/strata#1487 (unverified)

### After the drop

- By default, a successful drop keeps the source listing open. lgse/strata#933
- With Settings → General → File transfers → Open folder after dropping files on, a successful drop opens a child column in Columns or navigates in Icons and List. lgse/strata#933
- The destination opens only if the user has not navigated away while the transfer ran. lgse/strata#933
- The setting covers drops confirmed through the cross-device Copy or Move dialog, and a change in one window applies to drops in others. lgse/strata#933
- With the setting on in Columns, only the dropped item is selected, in the destination column. lgse/strata#933 (unverified)

## Design

[docs/preferences.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/preferences.md) carries the Open folder after dropping files and cross-device strategy preferences.

- All drops funnel into one transfer path, so one no-op guard covers Columns, List, Icons, pane, and sidebar drops. It runs before the size walk that would show a progress dialog (lgse/strata#424, lgse/strata#587).
- Click activation waits for release, so a press-and-move can become a drag first (lgse/strata#348, lgse/strata#753).
- The content modifier-click gesture is grouped with the row's drag source. Claiming the click would otherwise deny the drag before it reached the threshold (lgse/strata#623).
- Local sidebar rows take file payloads ahead of the pinned-place reorder target, which accepts only string payloads (lgse/strata#350).
- GTK's drag-end `delete_data` arrives before Strata's asynchronous transfer and cannot prove the source moved. The source row therefore never plays an exit animation; filesystem events remove it after a move (lgse/strata#598, lgse/strata#637). A downward settle animation was proposed and closed as not planned (lgse/strata#337).
- Opening the destination after a drop surprised users, so it became an opt-in setting (lgse/strata#859, lgse/strata#933). Paste and Move/Copy to… still reveal their destination independently.
- Spring navigation during a held drag is distinct from that post-drop setting (lgse/strata#1498). It ignores drop validity so the source folder can spring open although dropping on it is forbidden (lgse/strata#1487).
- Single-item drag previews show an icon because short filenames disappeared behind the cursor (lgse/strata#1487). This replaced the filename-only Explorer preview from lgse/strata#350.

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-05 | lgse/strata#1487 | feat | Added 750 ms spring-loaded navigation during held drags, icon drag previews, and selection-style drop outlines. |
| 2026-09-16 | lgse/strata#1049 | fix | Made the clipped-column reveal overlay non-targetable so drags start in narrow windows. |
| 2026-09-13 | lgse/strata#933 | feat | Stopped opening the destination after a drop by default and added the Open folder after dropping files setting. |
| 2026-09-09 | lgse/strata#637 | fix | Removed the Columns source-row exit animation on drag end, since drop acceptance cannot prove the source moved. |
| 2026-09-09 | lgse/strata#630 | fix | Cancelled folder peeks when a drag begins and ends so a cancelled drag no longer opens the hovered folder. |
| 2026-09-09 | lgse/strata#623 | fix | Grouped the content modifier-click gesture with the drag source so Ctrl-drag and Shift-drag start. |
| 2026-09-08 | lgse/strata#587 | fix | Filtered no-op sources before queuing so self-drops start no transfer or progress dialog. |
| 2026-09-06 | lgse/strata#415 | test | Fixed dragging an already-open Columns folder on GTK 4.14 while adding the E2E harness. |
| 2026-09-05 | lgse/strata#348 | fix | Deferred List folder activation to release so a press-and-move drags the folder. |
| 2026-09-05 | lgse/strata#350 | fix | Let local sidebar rows accept file drops ahead of place reordering, and compacted Explorer drag previews. |
| 2026-09-04 | lgse/strata#292 | feat | Made the preview header and image previews drag sources for the previewed file. |

## Known gaps

- Images, selected text, and web links dragged from a browser cannot be dropped to save them as files. lgse/strata#1545
- Drag and drop onto remote locations is not yet gated by the backend's supported operations. lgse/strata#66
