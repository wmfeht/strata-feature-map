---
title: Permanent deletion
status: shipped
origin: {issue: lgse/strata#163, pr: lgse/strata#164}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [src/ui/browser/dissolve_delete.rs, scripts/benchmark-delete.sh]
tests: [src/adapters/local_operations/tests/deletion.rs]
related: [operations/trash, operations/progress]
---

## Summary

Deleting files and folders without Trash, from Shift+Delete or the item menu's "Permanently delete", after a confirmation that shows the recursive total. Local trees are deleted descriptor-relative and in parallel, and the deleted rows dissolve afterwards. Deletion inside Trash, and the fallback where Trash is unsupported, are Trash's rules (`operations/trash`).

## Behavior

### Entry points

- Shift+Delete on a selection outside Trash opens the permanent-delete confirmation; Delete without Shift moves to Trash instead. lgse/strata#164
- Outside Trash, the item menu shows "Permanently delete" with a Shift+Del hint below Move to Trash, for single and multiple selections. lgse/strata#164
- The menu hides "Permanently delete" when `access::can-delete` reports false for the folder's contents, and shows it when the query is unresolved. lgse/strata#361
- In a folder without write permission, such as after `chmod 555`, neither Move to Trash nor Permanently delete appears in the item menu. lgse/strata#361
- Shift+Delete does nothing while the filter entry or a text widget, such as quick preview text, has focus. lgse/strata#670
- Outside 10xer mode, Shift+Delete works while focus is outside the file list, such as on a header button, as long as items are selected. lgse/strata#136 (unverified)
- In Columns view, Shift+Delete with no selection targets the cursor row, or the open folder when its column has neither fill nor cursor. lgse/strata#90, lgse/strata#1486

### Confirmation

- The dialog is titled "Permanently delete N items?" and its danger-styled button reads "Permanently delete N items". lgse/strata#164
- It lists each item with its icon, name, and size, "—" when the size is unknown, or "Folder" for folders, scrolling past 10 items. lgse/strata#1134 (unverified)
- It renders at most 50 rows and adds "… and N more items"; confirming still deletes every selected item. lgse/strata#703
- While the total calculates, a spinner shows beside the subtitle "N files", "N folders", or, for a mixed selection, "N items". lgse/strata#1134 (unverified)
- When the walk finishes, the spinner hides and the subtitle reads "N items · X will be permanently deleted", counting folder contents recursively. lgse/strata#1134
- When the walk is truncated, the subtitle reads "At least N items · at least X will be permanently deleted". lgse/strata#1134
- The confirm button is focused and can be activated while the total is still calculating. lgse/strata#1206, lgse/strata#1266
- Left or `h` focuses Cancel and Right or `l` focuses confirm; Enter and keypad Enter activate the focused button. lgse/strata#1052
- With Cancel or Close focused, Enter dismisses the dialog and the files stay. lgse/strata#1052
- Escape, Cancel, or Close dismiss the dialog without deleting anything. lgse/strata#1052, lgse/strata#1206

### Deleting

- Permanently deleting a folder that contains a symlink removes the symlink and leaves its target untouched. lgse/strata#253
- A selected symlink to a folder is removed as a symlink; the folder it points to keeps its contents. lgse/strata#253
- Deleting through a parent path that contains a symlink, such as a folder alias, succeeds and leaves the alias in place. lgse/strata#477
- If a folder in the tree is moved while it is being deleted, deletion stops with an error instead of following it. lgse/strata#869
- When some selected items cannot be deleted, the rest are still deleted and a dialog reads "N items could not be deleted. The remaining items were processed." lgse/strata#75 (unverified)
- That dialog lists the first 8 errors as "name: reason" and adds "… and N more items" for the rest. lgse/strata#75 (unverified)
- Ctrl+Z after a permanent delete does not restore the items; it undoes the undoable operation before it, such as a Move to Trash. lgse/strata#228 (unverified)

### Dissolve animation

- After a successful permanent delete, the deleted rows that were visible when it began break into fragments that scatter and fade. lgse/strata#626, lgse/strata#899
- The dissolve plays after the progress dialog closes, or while the "Deletion complete" card stays in the dock. lgse/strata#899, lgse/strata#1490
- Surviving rows stay in place until the dissolve finishes, then move into their new positions. lgse/strata#931
- "This directory is empty" stays hidden until the dissolve finishes when every item was deleted. lgse/strata#910
- A failed, partial, or cancelled deletion plays no dissolve. lgse/strata#899, lgse/strata#1490
- With animations disabled, no dissolve plays and the updated listing appears at once. lgse/strata#899, lgse/strata#931

## Design

Move to Trash is the default delete because it is reversible; permanent deletion needs Shift+Delete or an explicit menu item, then a danger-toned confirmation (lgse/strata#205, lgse/strata#163).

- lgse/strata#163 proposed a "Show permanently delete" setting, default off. The merged lgse/strata#164 shows the menu item unconditionally outside Trash instead.
- Menu visibility mirrors Move to Trash: one `access::can-delete` query per directory load, and an unresolved query keeps the item (lgse/strata#361). Only the menu is gated; keyboard and other paths are left to lgse/strata#66.
- The confirmation renders at most 50 rows because one GTK row per item on the main thread froze the UI at 1000 items (lgse/strata#622, lgse/strata#703).
- A selected folder hides its nested contents behind one "Folder" row. The subtitle therefore reuses Empty Trash's bounded directory summary and reports a lower bound when truncated (lgse/strata#900, lgse/strata#1134).
- Confirm takes initial focus, matching Finder, so Enter confirms and Escape cancels (lgse/strata#1204). Enter honors the focused button because always confirming was a data-loss path (lgse/strata#854).
- Local deletion walks descriptor-relative from each open directory with `openat2` and `RESOLVE_BENEATH | RESOLVE_NO_SYMLINKS | RESOLVE_NO_MAGICLINKS`. Each entry's type is re-read before recursing or unlinking, never trusted from the listing (lgse/strata#8, lgse/strata#253).
- The parent of a selected item resolves with `openat2(IN_ROOT | NO_MAGICLINKS)` so directory aliases work, while traversal inside the tree stays no-follow (lgse/strata#477).
- Remote GVfs locations have no descriptor to walk, so they keep GIO's path-based delete and claim no equivalent guarantee (lgse/strata#253).
- A work-stealing queue deletes trees on parallel workers at `nice +10`, one worker on rotational disks (lgse/strata#869). The first failure stops dispatch, started workers are joined, and transient open retries are bounded (lgse/strata#911).
- The dissolve snapshots visible rows before the operation mutates the model, because rows leave the model during progress (lgse/strata#895, lgse/strata#899). It uses 48 fragments per row within an 80 to 192 fragment budget, over 560 ms.
- Docking deletions into the progress dock dropped the prepared dissolve; the background completion now plays or discards it (lgse/strata#1489, lgse/strata#1490).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
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
