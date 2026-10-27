---
title: Trash
status: shipped
origin: {issue: lgse/strata#205, pr: lgse/strata#228}
branch: null
reviewed_at: 923b39ddf4950227e0779ef5b6216af7f4773727
review: draft
code: [src/ui/browser/trash.rs, src/adapters/trash_support.rs, src/adapters/local_operations/trash.rs]
tests: [src/ui/browser/trash/tests.rs, src/adapters/trash_support/tests.rs, src/adapters/local_files/tests/trash.rs, src/adapters/local_operations/tests/trash_capabilities.rs, tests/qa/mutations/trash.patch]
docs: [docs/trash-restore-testing.md]
related: [operations/delete, integration/10xer-mode/file-verbs, operations/filesystem-compatibility]
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
- A folder on a FUSE mount that already refused Trash lists `access::can-trash` false, so Move to Trash is hidden there until Reload. lgse/strata#1614
- A folder whose first listed entry is a symlink into `/dev/shm` still offers Move to Trash, and Delete moves a regular file there to Trash. lgse/strata#1551, lgse/strata#1584
- A no-Trash folder is an open folder reporting `access::can-trash` false and `access::can-delete` true, such as `/dev/shm`. lgse/strata#1533
- Delete, or a drop on the sidebar Trash row, opens "Permanently delete N items?" at once when every item is in a no-Trash folder. lgse/strata#1533
- In that case no trash move is attempted, so nothing reaches the Trash. lgse/strata#1533
- That dialog's text opens with the paragraph "This location doesn't support Trash." lgse/strata#1533, lgse/strata#1614
- When a refusal was recorded for the first item's mount, the next paragraph reads "Trash isn't available on <mount point> (<type>)." lgse/strata#1614
- The last paragraph is the local or remote deletion sentence of the permanent-delete confirmation (`operations/delete`). lgse/strata#1533, lgse/strata#1614
- That dialog focuses Cancel, still after the size summary loads, so Enter closes it and keeps the files. lgse/strata#1533
- When the folder's `access::can-trash` value is unknown, or the item's folder is not open, Delete attempts the trash move first. lgse/strata#1533 (unverified)
- In a read-only folder, where `access::can-trash` and `access::can-delete` are both false, Delete still attempts the trash move and opens no dialog first. lgse/strata#1533
- When a trash move fails because every failed item's location lacks Trash, the same explained dialog opens with Cancel focused, for only those items. lgse/strata#225, lgse/strata#1425, lgse/strata#1533
- When some items failed for other reasons, the error dialog's retry button opens the explained dialog for the trash-unsupported items only. lgse/strata#225, lgse/strata#1533
- That button reads "Delete without Trash" when every retryable item is remote, otherwise "Delete Permanently". lgse/strata#1614
- In the "Completed with errors" list, a trash-unsupported item reads "<name>: This location doesn't support Trash." lgse/strata#1614
- A read-only location reads "<name>: This location is read-only.", and a full disk "<name>: Not enough space to move to Trash." lgse/strata#1614
- Both fallbacks apply to docked deletions as well as foreground ones. lgse/strata#1533

### FUSE mounts that refuse Trash

- On a FUSE mount, including `fuseblk`, a trash move failing with permission denied, failed, or invalid argument counts as Trash unsupported. lgse/strata#1614
- So does an error writing the `.trashinfo` file, other than a full disk, a missing path, a read-only mount, or a name too long. lgse/strata#1614
- It counts only while the item is still present and the mount root answers `stat`. lgse/strata#1614
- The parent must also be off the home device, and the user must be allowed to remove the item. lgse/strata#1614
- On other local disks, only a not-supported error counts as Trash unsupported. lgse/strata#1614
- A disconnected FUSE mount, whose root `stat` fails, keeps the raw error instead of "doesn't support Trash". lgse/strata#1614
- After a counted refusal, the mount is remembered in every window, keyed by mount instance; a remount starts fresh. lgse/strata#1614
- After that failed delete, the parent folders reload, and the next Delete there opens the explained dialog without a trash attempt. lgse/strata#1614
- F5 forgets every remembered mount, so the next Delete tries Trash again. lgse/strata#1614
- The pane refresh button, the folder menu's reload, and F5 in the file chooser also forget them. lgse/strata#1614 (unverified)
- After a batch whose trash moves on a FUSE mount were refused as unsupported, new empty `.Trash-$uid` or `.Trash/$uid` folders are removed from its root. lgse/strata#1614
- That cleanup is skipped on a mount where any item in the batch was trashed. lgse/strata#1614
- A Trash move that reports success while the item is still in place fails as Trash unsupported, and records no Undo. lgse/strata#1615
- When another item took the name during the Trash call, Undo and saved views follow the newest Trash entry made for that path. lgse/strata#1729

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

### Confirmation file list

- The file list in the Shift+Delete and no-Trash confirmations has square corners at corner roundness 0, 1.8px at the default 60, and 6px at 200. lgse/strata#1906, lgse/strata#1908
- The file list in the "Move N items to Trash?" confirmation has the same corners at each roundness. lgse/strata#1906, lgse/strata#1908 (unverified)
- The file list in the "Restore N items?" confirmation has the same corners at each roundness. lgse/strata#1906, lgse/strata#1908

## Design

Trashing is reversible, so it runs immediately and Ctrl+Z replaces a confirmation; permanent deletion keeps its confirmation (lgse/strata#205).

- A Trash item keeps its `trash:///` location for navigation, restore, and deletion. GVfs's `standard::target-uri` native path is carried separately, for thumbnails and as the physical restore source. Remote target URIs are rejected (lgse/strata#417).
- Move to Trash visibility comes from `access::can-trash` on one listed entry per directory load, not on the folder: `$HOME` cannot itself be trashed but its entries can. An unknown value keeps the item visible so the only delete path never disappears; the trash-unsupported failure then offers permanent deletion (lgse/strata#314, lgse/strata#284, lgse/strata#179).
- The probe queries that entry without following symlinks: a link is trashed as itself, and its target may be slow or unreachable to stat (lgse/strata#1551). GIO derives `can-trash` from the entry's parent directory, not from a link target (lgse/strata#1584).
- The trash-unsupported fallback reused the Shift+Delete dialog. lgse/strata#66 forbids silently substituting permanent deletion for Trash. The dialog now explains the missing Trash and focuses Cancel, because the user asked for Trash (lgse/strata#1425).
- The up-front check uses the menu's `access::can-trash` signal. By owner decision it runs on every route, including drag-to-Trash. It requires `access::can-delete` true, so read-only folders still report "Permission denied" (lgse/strata#179, lgse/strata#1533).
- Every selected entry is checked, because a search-result selection can span locations (lgse/strata#1425).
- GIO reports `can-trash` on writable FUSE roots, so a refusal shows only mid-attempt. `access()` is not trusted, because sshfs answers success without `default_permissions`; mode and sticky bits are read (lgse/strata#1614).
- A refusal is remembered per mount instance so a remount retries, and Reload clears every record rather than probe a possibly hung folder (lgse/strata#1614).
- A failure in the home Trash says nothing about the mount, so items on the home device are excluded (lgse/strata#1614).
- GLib 2.86.0 to 2.88.4 can report success without trashing anything on some FUSE mounts (GLib #4060), so a trashed local item is checked gone first (lgse/strata#1615). The check uses the mount's identity rule and holds the item across GLib's call, except on NFS, where a hold leaves a `.nfs…` file (lgse/strata#1729).
- GVfs can move or delete whole trashed items but not their children, so actions on nested Trash children are hidden rather than left to fail (lgse/strata#433).
- Undo finds the trashed items through home-trash `.trashinfo` metadata before `trash:///`, because GVfs can miss an item re-trashed under the same name (lgse/strata#228).
- URI locations are monitored through GIO, so `trash:///` receives `gvfsd-trash` change events; events about the watched root itself are dropped, except its removal (lgse/strata#432, lgse/strata#463).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-16 | lgse/strata#1614 | fix | Classified FUSE Trash refusals as unsupported, remembered them per mount until Reload, and cleaned leftover Trash folders. |
| 2026-10-12 | lgse/strata#1584 | fix | Probed Trash support without following a symlinked first entry; hardening, as GIO already derived `can-trash` from the parent. |
| 2026-10-10 | lgse/strata#1539 | fix | Kept a docked deletion's claimed dissolve when a foreground operation fails; only a new permanent delete takes the slot. |
| 2026-10-09 | lgse/strata#1533 | fix | Explained a missing Trash with Cancel focused, and listed Trash items with non-UTF-8 names. |
| 2026-09-14 | lgse/strata#915 | fix | Let Delete reach Move to Trash when a filter result is selected. |
| 2026-09-07 | lgse/strata#499 | fix | Hid Trash actions GVfs cannot perform and blocked mutations of nested trashed items. |
| 2026-09-06 | lgse/strata#463 | fix | Monitored `trash:///` through GIO so an open Trash pane follows external changes. |
| 2026-09-06 | lgse/strata#419 | fix | Rendered Trash thumbnails from local storage while keeping the `trash:///` identity. |
| 2026-09-04 | lgse/strata#314 | fix | Hid Move to Trash where `access::can-trash` is false, keeping it when unknown. |
| 2026-09-04 | lgse/strata#225 | fix | Offered permanent deletion for items whose trash move failed because the location lacks Trash. |
| 2026-09-03 | lgse/strata#228 | feat | Removed the Move to Trash confirmation and added Ctrl+Z undo, since trashing is reversible. |

## Known gaps

- A persistent or per-mount "Use Trash" setting, and recovery declared by a provider, are deferred. lgse/strata#1614
- Through a symlink alias, the dialog's mount sentence and remote wording fall back to local wording. lgse/strata#1614
- On NFS, nothing holds the item across GLib's Trash call, so an item swapped in at the name during the call is not noticed. lgse/strata#1729
