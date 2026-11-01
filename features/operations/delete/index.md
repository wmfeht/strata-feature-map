---
title: Permanent deletion
status: shipped
origin: {issue: lgse/strata#163, pr: lgse/strata#164}
branch: null
reviewed_at: 41070b59c09f21eba33918c1e99be2eb3047de7e
review: draft
code: [src/adapters/local_operations/deletion.rs, scripts/benchmark-delete.sh]
tests: [src/adapters/local_operations/tests/deletion.rs, tests/qa/scenarios/entry_management/permanent-delete-symlinked-parent.jsonl]
related: [operations/trash, operations/progress, operations/filesystem-compatibility/open-files, browser/context-menu]
---

## Summary

Deleting files and folders without Trash, from Shift+Delete or the item menu's "Permanently delete", after a confirmation. Local trees are deleted descriptor-relative and in parallel. The confirmation dialog, its wording by location, and the no-Trash fallback are built in Trash's module (`operations/trash`); the menu items are `browser/context-menu`'s. Child: `operations/delete/dissolve` (the rows' dissolve after a successful delete).

## Behavior

### Entry points

- Shift+Delete on a selection outside Trash opens the permanent-delete confirmation; Delete without Shift opens it only where Trash is unsupported (`operations/trash`). lgse/strata#164, lgse/strata#1533
- Shift+Delete does nothing while the filter entry or a text widget, such as quick preview text, has focus. lgse/strata#670
- Outside 10xer mode, Shift+Delete works while focus is outside the file list, such as on a header button, as long as items are selected. lgse/strata#136 (unverified)
- In Columns view, Shift+Delete with no selection targets the cursor row, or the open folder when its column has neither fill nor cursor. lgse/strata#90, lgse/strata#1486

### Deleting

- Permanently deleting a folder that contains a symlink removes the symlink and leaves its target untouched. lgse/strata#253
- A selected symlink to a folder is removed as a symlink; the folder it points to keeps its contents. lgse/strata#253, lgse/strata#1627
- Deleting through a parent path that contains a symlink, such as a folder alias, succeeds and leaves the alias in place. lgse/strata#477
- If a folder in the tree is moved while it is being deleted, deletion stops with an error instead of following it. lgse/strata#869
- Deleting a folder on NFS, SMB, or FUSE leaves another program's `.nfs…`, `.__smbfile_silly…`, or `.fuse_hidden…` file in place. lgse/strata#1729
- Such a leftover selected by name is deleted like any file, and the mount's refusal is reported. lgse/strata#1729
- When some selected items cannot be deleted, the rest are still deleted and a dialog reads "N items could not be deleted. The remaining items were processed." lgse/strata#75 (unverified)
- That dialog lists the first 8 errors as "name: reason" and adds "… and N more items" for the rest. lgse/strata#75 (unverified)
- Cancelling a permanent delete counts an item it had started as failed, and items not yet started as not attempted. lgse/strata#1615
- Permanently deleting one local folder shows an "N items deleted" count that includes every file, symlink, and folder removed. lgse/strata#1935
- A leftover `.nfs…`, `.__smbfile_silly…`, or `.fuse_hidden…` file left in place is not included in the "N items deleted" count. lgse/strata#1935 (unverified)
- The "N items deleted" count refreshes about every 250 ms, and only when it changes. lgse/strata#1935
- Moving one folder to Trash shows no "N items deleted" count. lgse/strata#1935
- Permanently deleting one remote GVfs folder, or one item in `trash:///`, shows no "N items deleted" count. lgse/strata#1935 (unverified)
- Ctrl+Z after a permanent delete does not restore the items; it undoes the undoable operation before it, such as a Move to Trash. lgse/strata#228 (unverified)

## Design

Move to Trash is the default delete because it is reversible; permanent deletion needs Shift+Delete or an explicit menu item, then a danger-toned confirmation (lgse/strata#205, lgse/strata#163).

- lgse/strata#163 proposed a "Show permanently delete" setting, default off. The merged lgse/strata#164 shows the menu item unconditionally outside Trash instead.
- Menu visibility mirrors Move to Trash: one `access::can-delete` query per directory load, and an unresolved query keeps the item (lgse/strata#361). Only the menu is gated; keyboard and other paths are left to lgse/strata#66.
- Local deletion walks descriptor-relative from each open directory with `openat2` and `RESOLVE_BENEATH | RESOLVE_NO_SYMLINKS | RESOLVE_NO_MAGICLINKS`. Each entry's type is re-read before recursing or unlinking, never trusted from the listing (lgse/strata#8, lgse/strata#253).
- The parent of a selected item resolves with `openat2(IN_ROOT | NO_MAGICLINKS)` so directory aliases work, while traversal inside the tree stays no-follow (lgse/strata#477).
- Remote GVfs locations have no descriptor to walk, so they keep GIO's path-based delete and claim no equivalent guarantee (lgse/strata#253).
- A work-stealing queue deletes trees on parallel workers at `nice +10`, one worker on rotational disks (lgse/strata#869). The first failure stops dispatch, started workers are joined, and transient open retries are bounded (lgse/strata#911).
- Progress counted whole top-level items, so one large folder stayed at 0% until its last entry was gone. Workers now count removed entries on the `Deadline` every delete job already carries, so copy, replace, and merge callers need no new parameter (lgse/strata#1930, lgse/strata#1935).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-30 | lgse/strata#1935 | fix | Counted the entries a permanent delete removes, since one large folder showed 0% until it was gone. |
| 2026-10-25 | lgse/strata#1880 | fix | Sized a selected file symlink as the link itself on the confirmation, since it showed the target's size. |
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
- After confirming a permanent delete of a 600,000-file folder, progress shows 0% for about 1.5 s before the first entry is removed. lgse/strata#1935
