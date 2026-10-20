---
title: Permanent deletion
status: shipped
origin: {issue: lgse/strata#163, pr: lgse/strata#164}
branch: null
reviewed_at: e0f73973926ff67e77c2c56cf288b7b7617bb2e5
review: draft
code: [src/ui/browser/dissolve_delete.rs, src/adapters/local_operations/deletion.rs, scripts/benchmark-delete.sh]
tests: [src/adapters/local_operations/tests/deletion.rs]
related: [operations/trash, operations/progress]
---

## Summary

Deleting files and folders without Trash, from Shift+Delete or the item menu's "Permanently delete", after a confirmation that shows the recursive total. Local trees are deleted descriptor-relative and in parallel, and the deleted rows dissolve afterwards. Deletion inside Trash, and the fallback where Trash is unsupported, are Trash's rules (`operations/trash`).

## Behavior

### Entry points

- Shift+Delete on a selection outside Trash opens the permanent-delete confirmation; Delete without Shift opens it only where Trash is unsupported (`operations/trash`). lgse/strata#164, lgse/strata#1533
- Outside Trash, the item menu shows "Permanently delete" with a Shift+Del hint below Move to Trash, for single and multiple selections. lgse/strata#164
- On a remote selection, the item menu shows a danger-styled "Delete without Trash" with the Shift+Del hint in place of "Permanently delete". lgse/strata#1614
- A selection is remote only when every item is remote. lgse/strata#1571, lgse/strata#1614
- A remote item is a native path on a network mount, such as NFS, SMB, or sshfs, or a non-`trash:` URI. lgse/strata#1614
- `fuseblk` drives and local FUSE overlays, such as mergerfs or gocryptfs, count as local. lgse/strata#1614
- The menu hides "Permanently delete" when `access::can-delete` reports false for the folder's contents, and shows it when the query is unresolved. lgse/strata#361
- In a folder without write permission, such as after `chmod 555`, neither Move to Trash nor Permanently delete appears in the item menu. lgse/strata#361
- Shift+Delete does nothing while the filter entry or a text widget, such as quick preview text, has focus. lgse/strata#670
- Outside 10xer mode, Shift+Delete works while focus is outside the file list, such as on a header button, as long as items are selected. lgse/strata#136 (unverified)
- In Columns view, Shift+Delete with no selection targets the cursor row, or the open folder when its column has neither fill nor cursor. lgse/strata#90, lgse/strata#1486

### Confirmation

- For a local or mixed selection, the dialog is titled "Permanently delete N items?" and its danger-styled button reads "Permanently delete N items". lgse/strata#164, lgse/strata#1614
- Its text reads "This item will be permanently deleted. This action cannot be undone.", or "These items…" for several. lgse/strata#1614
- For a remote selection, the title reads "Delete N items without Trash?" and the button "Delete N items". lgse/strata#1571, lgse/strata#1614
- Its text reads "This item will be deleted without using Trash. Strata can't undo this; whether it can be recovered depends on the storage provider." lgse/strata#1571, lgse/strata#1614
- It lists each item with its icon, name, and size, "—" when the size is unknown, or "Folder" for folders, scrolling past 10 items. lgse/strata#1134 (unverified)
- A symlink to a folder is listed with "Folder link" in place of a size. lgse/strata#1627
- It renders at most 50 rows and adds "… and N more items"; confirming still deletes every selected item. lgse/strata#703
- While the total calculates, a spinner shows beside a kind subtitle. lgse/strata#1134 (unverified)
- That subtitle reads "N files" when every item is a file or file link, "N folders" when every item is a real folder, otherwise "N items". lgse/strata#1134, lgse/strata#1627 (unverified)
- A single selected symlink to a folder reads "1 item" beside the spinner; a folder link plus a file reads "2 items". lgse/strata#1627 (unverified)
- When the walk finishes, the spinner hides and the subtitle reads "N items · X will be permanently deleted", counting folder contents recursively. lgse/strata#1134
- For a remote selection the subtitle reads "N items · X will be deleted". lgse/strata#1614
- A selected symlink to a folder counts as 1 item of 0 B; its target's contents are not counted. lgse/strata#1627
- A selected symlink whose size is unknown, such as a dangling link, does not make the finished subtitle read "At least". lgse/strata#1627 (unverified)
- When the walk is truncated, the subtitle reads "At least N items · at least X will be permanently deleted". lgse/strata#1134
- For a remote selection, it ends "…will be deleted" instead. lgse/strata#1614
- After Shift+Delete, Permanently delete, or Delete without Trash, the confirm button is focused and can be activated while the total is still calculating. lgse/strata#1206, lgse/strata#1266, lgse/strata#1533, lgse/strata#1614
- Left or `h` focuses Cancel and Right or `l` focuses confirm; Enter and keypad Enter activate the focused button. lgse/strata#1052
- With Cancel or Close focused, Enter dismisses the dialog and the files stay. lgse/strata#1052
- Escape, Cancel, or Close dismiss the dialog without deleting anything. lgse/strata#1052, lgse/strata#1206

### Deleting

- Permanently deleting a folder that contains a symlink removes the symlink and leaves its target untouched. lgse/strata#253
- A selected symlink to a folder is removed as a symlink; the folder it points to keeps its contents. lgse/strata#253, lgse/strata#1627
- Deleting through a parent path that contains a symlink, such as a folder alias, succeeds and leaves the alias in place. lgse/strata#477
- If a folder in the tree is moved while it is being deleted, deletion stops with an error instead of following it. lgse/strata#869
- When some selected items cannot be deleted, the rest are still deleted and a dialog reads "N items could not be deleted. The remaining items were processed." lgse/strata#75 (unverified)
- That dialog lists the first 8 errors as "name: reason" and adds "… and N more items" for the rest. lgse/strata#75 (unverified)
- Cancelling a permanent delete counts an item it had started as failed, and items not yet started as not attempted. lgse/strata#1615
- Ctrl+Z after a permanent delete does not restore the items; it undoes the undoable operation before it, such as a Move to Trash. lgse/strata#228 (unverified)

### Dissolve animation

- After a successful permanent delete, the deleted rows that were visible when it began break into fragments that scatter and fade. lgse/strata#626, lgse/strata#899
- A permanent delete that succeeds before its progress card appears dissolves its rows, and no card appears. lgse/strata#1562
- A permanent delete still running when its card appears, after 350 ms or at once for 16 or more items, plays no dissolve. lgse/strata#1562 (unverified)
- While a permanent delete runs in Columns, List, or Icons, clicks reach the file view and navigating to another folder works. lgse/strata#1562
- A foreground operation that fails while a quick permanent delete runs leaves that delete's dissolve to play. lgse/strata#1539
- When a second quick permanent delete finishes while the first dissolve plays, it plays no dissolve, and the view takes clicks again afterwards. lgse/strata#1562 (unverified)
- During the dissolve, surviving rows show at their pre-delete positions, then appear at their new positions. lgse/strata#931, lgse/strata#1562 (unverified)
- "This directory is empty" stays hidden until the dissolve finishes when every item was deleted. lgse/strata#910
- A failed, partial, or cancelled deletion plays no dissolve. lgse/strata#899, lgse/strata#1490
- With animations disabled, no dissolve plays and the updated listing appears at once. lgse/strata#899, lgse/strata#931

## Design

Move to Trash is the default delete because it is reversible; permanent deletion needs Shift+Delete or an explicit menu item, then a danger-toned confirmation (lgse/strata#205, lgse/strata#163).

- lgse/strata#163 proposed a "Show permanently delete" setting, default off. The merged lgse/strata#164 shows the menu item unconditionally outside Trash instead.
- Menu visibility mirrors Move to Trash: one `access::can-delete` query per directory load, and an unresolved query keeps the item (lgse/strata#361). Only the menu is gated; keyboard and other paths are left to lgse/strata#66.
- The confirmation renders at most 50 rows because one GTK row per item on the main thread froze the UI at 1000 items (lgse/strata#622, lgse/strata#703).
- A selected folder hides its nested contents behind one "Folder" row. The subtitle therefore reuses Empty Trash's bounded directory summary and reports a lower bound when truncated (lgse/strata#900, lgse/strata#1134).
- A selected symlink root is counted as one item and never walked, because enumerating a root follows the link even with no-follow flags on its children (lgse/strata#1592, lgse/strata#1627).
- A network or cloud provider may keep its own copy, so wording that promises permanent loss is kept for local storage. A mixed selection keeps the stronger local warning (lgse/strata#1571, lgse/strata#1614).
- Reach is judged from the path as shown, without resolving symlinks on the main thread (lgse/strata#1614).
- Confirm takes initial focus, matching Finder, so Enter confirms and Escape cancels (lgse/strata#1204). Trash's no-Trash fallback is the exception (`operations/trash`, lgse/strata#1425). Enter honors the focused button because always confirming was a data-loss path (lgse/strata#854).
- Local deletion walks descriptor-relative from each open directory with `openat2` and `RESOLVE_BENEATH | RESOLVE_NO_SYMLINKS | RESOLVE_NO_MAGICLINKS`. Each entry's type is re-read before recursing or unlinking, never trusted from the listing (lgse/strata#8, lgse/strata#253).
- The parent of a selected item resolves with `openat2(IN_ROOT | NO_MAGICLINKS)` so directory aliases work, while traversal inside the tree stays no-follow (lgse/strata#477).
- Remote GVfs locations have no descriptor to walk, so they keep GIO's path-based delete and claim no equivalent guarantee (lgse/strata#253).
- A work-stealing queue deletes trees on parallel workers at `nice +10`, one worker on rotational disks (lgse/strata#869). The first failure stops dispatch, started workers are joined, and transient open retries are bounded (lgse/strata#911).
- The dissolve snapshots visible rows before the operation mutates the model, because rows leave the model during progress (lgse/strata#895, lgse/strata#899). It uses 48 fragments per row within an 80 to 192 fragment budget, over 560 ms.
- Docking deletions into the progress dock dropped the prepared dissolve; the background completion now plays or discards it (lgse/strata#1489, lgse/strata#1490).
- Preparing the dissolve only takes the snapshot. The view is hidden and ignores input only during the 560 ms playback, so a slow deletion never locks the window (lgse/strata#1562).
- A deletion whose card is presented drops its dissolve, so a slower deletion never locks the window behind an animation (lgse/strata#1562).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-15 | lgse/strata#1627 | fix | Counted a symlink to a folder as one 0 B "Folder link" item on the confirmation, since only the link is deleted. |
| 2026-10-05 | lgse/strata#1486 | fix | Targeted the cursor row or open folder for Delete and Shift+Delete in Columns view. |
| 2026-10-05 | lgse/strata#1490 | fix | Restored the dissolve after operation docking dropped it. |
| 2026-09-22 | lgse/strata#1134 | feat | Showed a recursive item count and size on the confirmation, since folders hid their contents. |
| 2026-09-18 | lgse/strata#1052 | fix | Made Enter activate the focused button instead of always confirming. |
| 2026-09-13 | lgse/strata#931 | fix | Kept surviving rows stationary until dissolve fragments finish. |
| 2026-09-12 | lgse/strata#910 | fix | Deferred the empty-folder message until the dissolve finishes. |
| 2026-09-12 | lgse/strata#869 | perf | Deleted local trees on parallel workers through a descriptor-relative work queue. |
| 2026-09-12 | lgse/strata#899 | fix | Played the dissolve after progress closes, and only for successful deletions. |
| 2026-09-09 | lgse/strata#703 | fix | Capped confirmation rows at 50 to stop large selections freezing the UI. |
| 2026-09-06 | lgse/strata#477 | fix | Allowed symlinks in the parent path of deleted items. |
| 2026-09-05 | lgse/strata#361 | feat | Hid Permanently delete where `access::can-delete` is false. |
| 2026-09-04 | lgse/strata#253 | fix | Deleted local trees descriptor-relative so symlink swaps cannot redirect deletion. |
| 2026-09-02 | lgse/strata#164 | feat | Added a Permanently delete item to the item menu outside Trash. |
| 2026-09-01 | lgse/strata#90 | fix | Targeted the entered folder when its column has no selection, so Delete no longer silently does nothing. |
| 2026-09-01 | lgse/strata#136 | fix | Let Delete and Shift+Delete reach the confirmation when focus is outside the file list. |

## Known gaps

- Shift+Delete still opens the permanent-delete confirmation where `access::can-delete` is false; only the item menu is capability-gated. lgse/strata#66
