---
title: Trash
status: shipped
origin: {issue: lgse/strata#205, pr: lgse/strata#228}
branch: null
reviewed_at: aee71335dfecd059b9af23efeac2ed52c43e3b19
review: draft
code: [src/ui/browser/trash.rs]
tests: [src/ui/browser/trash/tests.rs, src/adapters/local_files/tests/trash.rs, src/adapters/local_operations/tests/trash_capabilities.rs]
docs: [docs/trash-restore-testing.md]
related: [operations/delete, integration/10xer-mode/file-verbs]
---

## Summary

Moving files and folders to the freedesktop.org Trash, undoing that move, and browsing `trash:///` in every view mode. Children: `operations/trash/restore` (Restore from Trash), `operations/trash/empty` (Empty Trash), and `operations/trash/animation` (flights between rows and the sidebar Trash button).

## Behavior

### Moving to Trash

- Delete without Shift on a selection outside Trash moves it to Trash with no confirmation dialog, except in the no-Trash folders below. lgse/strata#228, lgse/strata#1533
- Ctrl+Z after Move to Trash returns the items to their original locations, including when pressed in another Strata window. lgse/strata#228
- Dropping files onto the sidebar Trash row moves them to Trash, and Ctrl+Z returns them, except from the no-Trash folders below. lgse/strata#626, lgse/strata#836, lgse/strata#1533
- Delete on a selected Ctrl+F filter result moves that result to Trash and leaves the hidden directory selection untouched. lgse/strata#915

### Locations without Trash

- Outside Trash, the item context menu hides Move to Trash when the folder's listing reports `access::can-trash` false, and shows it when the value is unknown. lgse/strata#314
- A no-Trash folder is an open folder reporting `access::can-trash` false and `access::can-delete` true, such as `/dev/shm`. lgse/strata#1533
- Delete, or a drop on the sidebar Trash row, opens "Permanently delete N items?" at once when every item is in a no-Trash folder. lgse/strata#1533
- In that case no trash move is attempted, so nothing reaches the Trash. lgse/strata#1533
- That dialog adds "This location doesn't support Trash. This item will be permanently deleted." for one item. lgse/strata#1533
- For several items it reads "These items will be permanently deleted.", and both versions end "This action cannot be undone." lgse/strata#1533
- That dialog focuses Cancel, still after the size summary loads, so Enter closes it and keeps the files. lgse/strata#1533
- When the folder's `access::can-trash` value is unknown, or the item's folder is not open, Delete attempts the trash move first. lgse/strata#1533 (unverified)
- In a read-only folder, where `access::can-trash` and `access::can-delete` are both false, Delete still attempts the trash move and opens no dialog first. lgse/strata#1533
- When a trash move fails because every failed item's location lacks Trash, the same explained dialog opens with Cancel focused, for only those items. lgse/strata#225, lgse/strata#1425, lgse/strata#1533
- When some items failed for other reasons, Delete Permanently in the error dialog opens the explained dialog for the trash-unsupported items only. lgse/strata#225, lgse/strata#1533
- Both fallbacks apply to docked deletions as well as foreground ones. lgse/strata#1533

### Browsing Trash

- In Trash, Delete and the item menu's "Permanently delete" ask for permanent-deletion confirmation instead of moving to Trash. lgse/strata#361, lgse/strata#499 (unverified)
- Trash menus omit Rename, Compress, New Folder, New File, and paste destinations. lgse/strata#499
- Top-level Trash items keep Restore, Cut, Move to…, Copy, and permanent deletion in their menus. lgse/strata#499
- Items inside a trashed folder cannot be cut, moved, deleted, or restored from the menu or keyboard. lgse/strata#499
- Images in Trash show thumbnails rendered from their local Trash storage; folders and unsupported files keep their type icons. lgse/strata#419
- An open Trash pane adds items trashed by other applications and removes items restored or purged elsewhere, without F5. lgse/strata#463
- With `gvfsd` running, Trash lists a file whose name holds byte `\xe9` as `caf�.txt (invalid encoding)`. lgse/strata#1533
- The footer counts such an item. lgse/strata#1533
- The path bar and Properties show such an item's percent-encoded URI, such as `trash:///caf%E9.txt`. lgse/strata#1533

## Design

Trashing is reversible, so it runs immediately and Ctrl+Z replaces a confirmation; permanent deletion keeps its confirmation (lgse/strata#205).

- A Trash item keeps its `trash:///` location for navigation, restore, and deletion. GVfs's `standard::target-uri` native path is carried separately, for thumbnails and as the physical restore source. Remote target URIs are rejected (lgse/strata#417).
- Move to Trash visibility comes from `access::can-trash` on one listed entry per directory load, not on the folder: `$HOME` cannot itself be trashed but its entries can. An unknown value keeps the item visible so the only delete path never disappears; the trash-unsupported failure then offers permanent deletion (lgse/strata#314, lgse/strata#284, lgse/strata#179).
- The trash-unsupported fallback reused the Shift+Delete dialog. lgse/strata#66 forbids silently substituting permanent deletion for Trash. The dialog now explains the missing Trash and focuses Cancel, because the user asked for Trash (lgse/strata#1425).
- The up-front check uses the menu's `access::can-trash` signal. By owner decision it runs on every route, including drag-to-Trash. It requires `access::can-delete` true, so read-only folders still report "Permission denied" (lgse/strata#179, lgse/strata#1533).
- Every selected entry is checked, because a search-result selection can span locations (lgse/strata#1425).
- GVfs can move or delete whole trashed items but not their children, so actions on nested Trash children are hidden rather than left to fail (lgse/strata#433).
- Undo finds the trashed items through home-trash `.trashinfo` metadata before `trash:///`, because GVfs can miss an item re-trashed under the same name (lgse/strata#228).
- URI locations are monitored through GIO, so `trash:///` receives `gvfsd-trash` change events; events about the watched root itself are dropped, except its removal (lgse/strata#432, lgse/strata#463).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-09 | lgse/strata#1533 | fix | Explained a missing Trash with Cancel focused, and listed Trash items with non-UTF-8 names. |
| 2026-09-14 | lgse/strata#915 | fix | Let Delete reach Move to Trash when a filter result is selected. |
| 2026-09-07 | lgse/strata#499 | fix | Hid Trash actions GVfs cannot perform and blocked mutations of nested trashed items. |
| 2026-09-06 | lgse/strata#463 | fix | Monitored `trash:///` through GIO so an open Trash pane follows external changes. |
| 2026-09-06 | lgse/strata#419 | fix | Rendered Trash thumbnails from local storage while keeping the `trash:///` identity. |
| 2026-09-04 | lgse/strata#314 | fix | Hid Move to Trash where `access::can-trash` is false, keeping it when unknown. |
| 2026-09-04 | lgse/strata#225 | fix | Offered permanent deletion for items whose trash move failed because the location lacks Trash. |
| 2026-09-03 | lgse/strata#228 | feat | Removed the Move to Trash confirmation and added Ctrl+Z undo, since trashing is reversible. |

## Known gaps

- A first listed entry that symlinks into tmpfs makes its whole folder report no Trash, so Delete asks to delete permanently. lgse/strata#1533
