---
title: Trash
status: shipped
origin: {issue: lgse/strata#205, pr: lgse/strata#228}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: reviewed
code: [src/ui/browser/trash.rs]
tests: [src/ui/browser/trash/tests.rs, src/adapters/local_files/tests/trash.rs, src/adapters/local_operations/tests/trash_capabilities.rs]
docs: []
related: []
---

## Summary

Moving files and folders to the freedesktop.org Trash, undoing that move, and browsing `trash:///` in every view mode. Children: `operations/trash/restore` (Restore from Trash), `operations/trash/empty` (Empty Trash), and `operations/trash/animation` (flights between rows and the sidebar Trash button).

## Behavior

### Moving to Trash

- Delete without Shift on a selection outside Trash moves it to Trash with no confirmation dialog. lgse/strata#228
- Ctrl+Z after Move to Trash returns the items to their original locations, including when pressed in another Strata window. lgse/strata#228
- Dropping files onto the sidebar Trash row moves them to Trash, and Ctrl+Z returns them. lgse/strata#626, lgse/strata#836
- Delete on a selected Ctrl+F filter result moves that result to Trash and leaves the hidden directory selection untouched. lgse/strata#915
- Outside Trash, the item context menu hides Move to Trash when the folder's listing reports `access::can-trash` false, and shows it when the value is unknown. lgse/strata#314
- When every failed item failed because its location lacks Trash, Strata opens the permanent-delete confirmation for only those items. lgse/strata#225, lgse/strata#1425
- When some items failed for other reasons, the error dialog shows a Delete Permanently button that confirms only the trash-unsupported items. lgse/strata#225

### Browsing Trash

- In Trash, Delete and the item menu's "Permanently delete" ask for permanent-deletion confirmation instead of moving to Trash. lgse/strata#361, lgse/strata#499 (unverified)
- Trash menus omit Rename, Compress, New Folder, New File, and paste destinations. lgse/strata#499
- Top-level Trash items keep Restore, Cut, Move to…, Copy, and permanent deletion in their menus. lgse/strata#499
- Items inside a trashed folder cannot be cut, moved, deleted, or restored from the menu or keyboard. lgse/strata#499
- Images in Trash show thumbnails rendered from their local Trash storage; folders and unsupported files keep their type icons. lgse/strata#419
- An open Trash pane adds items trashed by other applications and removes items restored or purged elsewhere, without F5. lgse/strata#463

## Design

Trashing is reversible, so it runs immediately and Ctrl+Z replaces a confirmation; permanent deletion keeps its confirmation (lgse/strata#205).

- A Trash item keeps its `trash:///` location for navigation, restore, and deletion. GVfs's `standard::target-uri` native path is carried separately, for thumbnails and as the physical restore source. Remote target URIs are rejected (lgse/strata#417).
- Move to Trash visibility comes from `access::can-trash` on one listed entry per directory load, not on the folder: `$HOME` cannot itself be trashed but its entries can. An unknown value keeps the item visible so the only delete path never disappears; the trash-unsupported failure then offers permanent deletion (lgse/strata#314, lgse/strata#284, lgse/strata#179).
- GVfs can move or delete whole trashed items but not their children, so actions on nested Trash children are hidden rather than left to fail (lgse/strata#433).
- Undo finds the trashed items through home-trash `.trashinfo` metadata before `trash:///`, because GVfs can miss an item re-trashed under the same name (lgse/strata#228).
- URI locations are monitored through GIO, so `trash:///` receives `gvfsd-trash` change events; events about the watched root itself are dropped, except its removal (lgse/strata#432, lgse/strata#463).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-14 | lgse/strata#915 | fix | Let Delete reach Move to Trash when a filter result is selected. |
| 2026-09-07 | lgse/strata#499 | fix | Hid Trash actions GVfs cannot perform and blocked mutations of nested trashed items. |
| 2026-09-06 | lgse/strata#463 | fix | Monitored `trash:///` through GIO so an open Trash pane follows external changes. |
| 2026-09-06 | lgse/strata#419 | fix | Rendered Trash thumbnails from local storage while keeping the `trash:///` identity. |
| 2026-09-04 | lgse/strata#314 | fix | Hid Move to Trash where `access::can-trash` is false, keeping it when unknown. |
| 2026-09-04 | lgse/strata#225 | fix | Offered permanent deletion for items whose trash move failed because the location lacks Trash. |
| 2026-09-03 | lgse/strata#228 | feat | Removed the Move to Trash confirmation and added Ctrl+Z undo, since trashing is reversible. |

## Known gaps

- Where Trash is unsupported, Delete opens the permanent-delete confirmation with the destructive button focused and no explanation; lgse/strata#1533 fixes it after `reviewed_at`. lgse/strata#1425, lgse/strata#1533
- Trashed items whose names are not valid UTF-8 are not listed in Trash, so they cannot be restored or deleted from Strata; lgse/strata#1533 fixes it after `reviewed_at`. lgse/strata#1424, lgse/strata#1533
