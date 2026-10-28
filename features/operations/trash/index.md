---
title: Trash
status: shipped
origin: {issue: lgse/strata#205, pr: lgse/strata#228}
branch: null
reviewed_at: 86df474dc0e8352e0e2098637a017cc4c77a8c44
review: draft
code: [src/ui/browser/trash.rs, src/adapters/local_operations/trash.rs]
tests: [src/ui/browser/trash/tests.rs, src/adapters/local_files/tests/trash.rs, src/adapters/local_operations/tests/trash_capabilities.rs, tests/qa/mutations/trash.patch, tests/qa/scenarios/entry_management/delete-to-trash.jsonl, tests/qa/scenarios/entry_management/delete-without-trash-focuses-cancel.jsonl, tests/qa/scenarios/entry_management/delete-file-symlink-sizes-link.jsonl, tests/qa/scenarios/entry_management/trashing-open-folder-opens-next.jsonl]
docs: [docs/trash-restore-testing.md]
related: [operations/delete, integration/10xer-mode/file-verbs, operations/filesystem-compatibility, browser/context-menu]
---

## Summary

Moving files and folders to the freedesktop.org Trash, undoing that move, and browsing `trash:///` in every view mode. Trash's UI module also builds the deletion confirmations and the no-Trash fallback. Children: `operations/trash/restore` (Restore from Trash), `operations/trash/empty` (Empty Trash), `operations/trash/animation` (flights between rows and the sidebar Trash button), and `operations/trash/fuse-refusals` (FUSE mounts that refuse Trash).

## Behavior

### Moving to Trash

- Delete without Shift on a selection outside Trash moves it to Trash with no confirmation dialog, except in the no-Trash folders below. lgse/strata#228, lgse/strata#1533
- Ctrl+Z after Move to Trash returns the items to their original locations, including when pressed in another Strata window. lgse/strata#228
- Dropping files onto the sidebar Trash row moves them to Trash, and Ctrl+Z returns them, except from the no-Trash folders below. lgse/strata#626, lgse/strata#836, lgse/strata#1533
- Delete on a selected Ctrl+F filter result moves that result to Trash and leaves the hidden directory selection untouched. lgse/strata#915
- A Trash move that reports success while the item is still in place fails as Trash unsupported, and records no Undo. lgse/strata#1615
- When another item took the name during the Trash call, Undo and saved views follow the newest Trash entry made for that path. lgse/strata#1729

### Locations without Trash

- A folder whose first listed entry is a symlink into `/dev/shm` still offers Move to Trash, and Delete moves a regular file there to Trash. lgse/strata#1551, lgse/strata#1584
- A no-Trash folder is an open folder reporting `access::can-trash` false and `access::can-delete` true, such as `/dev/shm`. lgse/strata#1533
- Delete, or a drop on the sidebar Trash row, opens "Permanently delete N items?" at once when every item is in a no-Trash folder. lgse/strata#1533
- In that case no trash move is attempted, so nothing reaches the Trash. lgse/strata#1533
- That dialog's text opens with the paragraph "This location doesn't support Trash." lgse/strata#1533, lgse/strata#1614
- When a refusal was recorded for the first item's mount, the next paragraph reads "Trash isn't available on <mount point> (<type>)." lgse/strata#1614
- The last paragraph is the local or remote deletion sentence of the permanent-delete confirmation, below. lgse/strata#1533, lgse/strata#1614
- That dialog focuses Cancel, still after the size summary loads, so Enter closes it and keeps the files. lgse/strata#1533
- When the folder's `access::can-trash` value is unknown, or the item's folder is not open, Delete attempts the trash move first. lgse/strata#1533 (unverified)
- In a read-only folder, where `access::can-trash` and `access::can-delete` are both false, Delete still attempts the trash move and opens no dialog first. lgse/strata#1533
- When a trash move fails because every failed item's location lacks Trash, the same explained dialog opens with Cancel focused, for only those items. lgse/strata#225, lgse/strata#1425, lgse/strata#1533
- When some items failed for other reasons, the error dialog's retry button opens the explained dialog for the trash-unsupported items only. lgse/strata#225, lgse/strata#1533
- That button reads "Delete without Trash" when every retryable item is remote, otherwise "Delete Permanently". lgse/strata#1614
- In the "Completed with errors" list, a trash-unsupported item reads "<name>: This location doesn't support Trash." lgse/strata#1614
- A read-only location reads "<name>: This location is read-only.", and a full disk "<name>: Not enough space to move to Trash." lgse/strata#1614
- Both fallbacks apply to docked deletions as well as foreground ones. lgse/strata#1533

### Deletion confirmations

- A selection is remote only when every item is remote; a mixed selection gets the local wording. lgse/strata#1571, lgse/strata#1614
- A remote item is a native path on a network mount, such as NFS, SMB, or sshfs, or a non-`trash:` URI. lgse/strata#1614
- `fuseblk` drives and local FUSE overlays, such as mergerfs or gocryptfs, count as local. lgse/strata#1614
- For a local or mixed selection, the permanent-delete dialog is titled "Permanently delete N items?" and its danger-styled button reads "Permanently delete N items". lgse/strata#164, lgse/strata#1614
- Its text reads "This item will be permanently deleted. This action cannot be undone.", or "These items…" for several. lgse/strata#1614
- For a remote selection, the title reads "Delete N items without Trash?" and the button "Delete N items". lgse/strata#1571, lgse/strata#1614
- Its text reads "This item will be deleted without using Trash. Strata can't undo this; whether it can be recovered depends on the storage provider." lgse/strata#1571, lgse/strata#1614
- The "Move N items to Trash?" confirmation, such as from 10xer `d` or a leftover's Delete…, reads "This item can be restored from Trash." and shows no total. lgse/strata#1306 (unverified)
- It lists each item with its icon, name, and size, "—" when the size is unknown, or "Folder" for folders, scrolling past 10 items. lgse/strata#1134 (unverified)
- A symlink to a folder is listed with "Folder link" in place of a size. lgse/strata#1627
- A selected 11 B symlink to a 100 kB file lists "11 B", while the size column shows "100 kB". The subtitle reads "1 item · 11 B will be permanently deleted". lgse/strata#1853, lgse/strata#1880
- A file link's row shows "—" until its own size is measured. lgse/strata#1880 (unverified)
- The "Move N items to Trash?" confirmation also lists a file link at its own size. lgse/strata#1880 (unverified)
- It renders at most 50 rows and adds "… and N more items"; confirming still deletes every selected item. lgse/strata#703
- While the total calculates, a spinner shows beside a kind subtitle. lgse/strata#1134 (unverified)
- That subtitle reads "N files" when every item is a file or file link, "N folders" when every item is a real folder, otherwise "N items". lgse/strata#1134, lgse/strata#1627 (unverified)
- A single selected symlink to a folder reads "1 item" beside the spinner; a folder link plus a file reads "2 items". lgse/strata#1627 (unverified)
- When the walk finishes, the spinner hides and the subtitle reads "N items · X will be permanently deleted", counting folder contents recursively. lgse/strata#1134
- For a remote selection the subtitle reads "N items · X will be deleted". lgse/strata#1614
- A selected symlink to a folder counts as 1 item of 0 B; its target's contents are not counted. lgse/strata#1627
- A selected dangling symlink does not make the finished subtitle read "At least". lgse/strata#1627 (unverified)
- With 51 selected 11 B file links, the subtitle reads "51 items · 561 B will be permanently deleted", counting links past the 50 rows. lgse/strata#1880 (unverified)
- A selected file link removed before it is measured shows "—". The subtitle reads "At least 1 item · at least 0 B will be permanently deleted". lgse/strata#1880 (unverified)
- When the walk is truncated, the subtitle reads "At least N items · at least X will be permanently deleted". lgse/strata#1134
- For a remote selection, it ends "…will be deleted" instead. lgse/strata#1614
- After Shift+Delete, Permanently delete, or Delete without Trash, the confirm button is focused and can be activated while the total is still calculating. lgse/strata#1206, lgse/strata#1266, lgse/strata#1533, lgse/strata#1614
- Left or `h` focuses Cancel and Right or `l` focuses confirm; Enter and keypad Enter activate the focused button. lgse/strata#1052
- With Cancel or Close focused, Enter dismisses the dialog and the files stay. lgse/strata#1052
- In 10xer mode, `d` in the "Move N items to Trash?" confirmation confirms it; in the permanent and no-Trash confirmations `d` does not confirm. lgse/strata#1340, lgse/strata#1508, lgse/strata#1533
- A backdrop click, Escape, Cancel, or Close dismisses the permanent-delete confirmation without deleting anything. lgse/strata#1052, lgse/strata#1206, lgse/strata#1900
- Each of those returns keyboard focus to the listing's cursor row, so arrow keys then move in the visible pane. lgse/strata#1900
- The no-Trash and "Move N items to Trash?" confirmations return focus the same way. lgse/strata#1900 (unverified)

### Confirmation file list

- The file list in the Shift+Delete and no-Trash confirmations has square corners at corner roundness 0, 1.8px at the default 60, and 6px at 200. lgse/strata#1906, lgse/strata#1908
- The file list in the "Move N items to Trash?" confirmation has the same corners at each roundness. lgse/strata#1906, lgse/strata#1908 (unverified)
- The file list in the "Restore N items?" confirmation has the same corners at each roundness. lgse/strata#1906, lgse/strata#1908

### Browsing Trash

- In Trash, Delete and the item menu's "Permanently delete" ask for permanent-deletion confirmation instead of moving to Trash. lgse/strata#361, lgse/strata#499 (unverified)
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
- The probe queries that entry without following symlinks: a link is trashed as itself, and its target may be slow or unreachable to stat (lgse/strata#1551). GIO derives `can-trash` from the entry's parent directory, not from a link target (lgse/strata#1584).
- The trash-unsupported fallback reused the Shift+Delete dialog. lgse/strata#66 forbids silently substituting permanent deletion for Trash. The dialog now explains the missing Trash and focuses Cancel, because the user asked for Trash (lgse/strata#1425).
- The up-front check uses the menu's `access::can-trash` signal. By owner decision it runs on every route, including drag-to-Trash. It requires `access::can-delete` true, so read-only folders still report "Permission denied" (lgse/strata#179, lgse/strata#1533).
- Every selected entry is checked, because a search-result selection can span locations (lgse/strata#1425).
- GLib 2.86.0 to 2.88.4 can report success without trashing anything on some FUSE mounts (GLib #4060), so a trashed local item is checked gone first (lgse/strata#1615). The check uses the mount's identity rule and holds the item across GLib's call, except on NFS, where a hold leaves a `.nfs…` file (lgse/strata#1729).
- GVfs can move or delete whole trashed items but not their children, so actions on nested Trash children are hidden rather than left to fail (lgse/strata#433).
- Undo finds the trashed items through home-trash `.trashinfo` metadata before `trash:///`, because GVfs can miss an item re-trashed under the same name (lgse/strata#228).
- URI locations are monitored through GIO, so `trash:///` receives `gvfsd-trash` change events; events about the watched root itself are dropped, except its removal (lgse/strata#432, lgse/strata#463).
- The deletion confirmation renders at most 50 rows because one GTK row per item on the main thread froze the UI at 1000 items (lgse/strata#622, lgse/strata#703).
- A selected folder hides its nested contents behind one "Folder" row. The subtitle therefore reuses Empty Trash's bounded directory summary and reports a lower bound when truncated (lgse/strata#900, lgse/strata#1134).
- A selected symlink root is counted as one item and never walked, because enumerating a root follows the link even with no-follow flags on its children (lgse/strata#1592, lgse/strata#1627).
- The listing stats with follow, so the browser's size column keeps showing a file link's target size. The confirmation queries each file link without following it, once, for both its row and the total (lgse/strata#1853, lgse/strata#1880).
- A network or cloud provider may keep its own copy, so wording that promises permanent loss is kept for local storage. A mixed selection keeps the stronger local warning (lgse/strata#1571, lgse/strata#1614).
- Reach is judged from the path as shown, without resolving symlinks on the main thread (lgse/strata#1614).
- Confirm takes initial focus, matching Finder, so Enter confirms and Escape cancels (lgse/strata#1204). The no-Trash fallback is the exception (lgse/strata#1425). Enter honors the focused button because always confirming was a data-loss path (lgse/strata#854).
- The deletion confirmation reuses the shared modal focus restoration, so focus returns to the visible pane however the dialog closes (lgse/strata#1859, lgse/strata#1900).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-27 | lgse/strata#1900 | fix | Returned focus to the listing when the deletion confirmation closes by backdrop click, Escape, Cancel, or Close. |
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

- Through a symlink alias, the dialog's mount sentence and remote wording fall back to local wording. lgse/strata#1614
- On NFS, nothing holds the item across GLib's Trash call, so an item swapped in at the name during the call is not noticed. lgse/strata#1729
