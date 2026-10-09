---
title: Restore from Trash
status: shipped
origin: {issue: lgse/strata#478, pr: lgse/strata#502}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: reviewed
code: [src/adapters/trash_restore.rs]
tests: [src/adapters/trash_restore/**, src/adapters/local_operations/tests/restore_safety.rs]
docs: [docs/trash-restore-testing.md]
related: []
---

## Summary

Returning trashed items to their original locations, from the Restore menu item or by undoing Move to Trash. Strata treats `.trashinfo` metadata as untrusted, confirms each full destination, and never overwrites an existing file.

## Behavior

### Lookup and confirmation

- Restore appears in the item menu only when every selected item is a top-level Trash item. lgse/strata#499
- Choosing Restore shows "Finding restore destinations…"; Cancel or Escape ends the lookup without moving files or deleting metadata. lgse/strata#502
- After lookup, a "Restore N items?" confirmation lists each item with its full original path; Cancel or Escape changes nothing. lgse/strata#502
- Items that fail validation are left out of the confirmation, which lists their names and reasons below the valid items. lgse/strata#502 (unverified)
- When every selected item fails validation, an "Unable to restore" dialog lists the reasons and no confirmation appears. lgse/strata#502 (unverified)
- A destination lookup that stalls for 2 seconds fails with "Timed out looking up the original location". lgse/strata#502 (unverified)

### Destination validation

- A `Path=` outside the mount that holds the trashed item is refused with "The original location is outside the trash volume and cannot be restored." lgse/strata#502
- A home-trash item whose original path is on another filesystem, such as `/dev/shm`, is refused with the same "outside the trash volume" message. lgse/strata#776
- A destination across a bind mount or subvolume on the same filesystem is refused with "crosses a bind mount or subvolume boundary". lgse/strata#502, lgse/strata#776
- A `Path=` containing a `..` component, plain or percent-encoded, is refused with "The original location is invalid". lgse/strata#502
- A destination inside the trash directory, including anywhere in a shared `.Trash` tree, is refused with "The original location must not be inside the trash directory". lgse/strata#502
- A destination whose parent folder no longer exists is refused at lookup with "The original location's parent folder no longer exists". lgse/strata#777
- A destination whose parent is a symlink is refused with "The original location's parent is a symlink and cannot be restored.", even on the same volume. lgse/strata#913
- When GVfs gives no physical path, the item search includes a shared `.Trash/$uid` only if `.Trash` is a real, sticky directory. lgse/strata#502 (unverified)
- A relative `Path=` in volume trash resolves against the volume top directory, including the shared `.Trash/$uid` layout. lgse/strata#502

### Execution

- A confirmed restore moves the item to the confirmed path and removes its `.trashinfo`. lgse/strata#502
- If the original location changes after confirmation, the restore fails with "no longer matches the confirmed destination" and the payload and metadata stay in Trash. lgse/strata#502
- If something exists at the destination, the restore fails with "something already exists at the destination" and the item stays in Trash. lgse/strata#502, lgse/strata#1527
- On filesystems without `RENAME_NOREPLACE`, such as NTFS via ntfs-3g, files and folders restore when the destination is free. lgse/strata#1527

### Undo

- Ctrl+Z after Move to Trash applies the same destination validation without showing the restore confirmation. lgse/strata#502
- Cancel during an undo restore stops the trash lookup within one 64-item batch and reports the operation as cancelled. lgse/strata#873

## Design

[docs/trash-restore-testing.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/trash-restore-testing.md) carries the safety model, the automated regressions, and the manual acceptance steps.

- Metadata is untrusted. An attacker who can write a mounted volume's `.Trash-$uid` could plant `Path=` targets such as `~/.config/autostart/` (lgse/strata#478). Destinations are therefore confined to the mount hosting the physical trash item and shown in full before moving.
- The physical item is resolved through `standard::target-uri`, because GVfs volume-trash basenames do not identify the entry (lgse/strata#502).
- Lookup runs before confirmation and execution re-plans each item. A mismatch with the confirmed path fails rather than restoring elsewhere (lgse/strata#502).
- Home-trash items whose original path is on another filesystem could have been returned there or refused. Refusing was chosen, with a message that names the volume rather than bind mounts (lgse/strata#735, lgse/strata#776).
- A missing parent is refused rather than recreated, matching Finder's Put Back instead of Nautilus (lgse/strata#777).
- The parent is checked with `symlink_metadata` before canonicalization, which would otherwise follow a same-volume symlink into its target (lgse/strata#862).
- No-clobber must be atomic: `RENAME_NOREPLACE`, never a check followed by a plain rename (lgse/strata#502). Without it, a file is hard-linked, otherwise copied exclusively with metadata, and the source deleted only if unchanged. A failed copy removes only entries Strata provably created (lgse/strata#1526).
- Execution keeps `openat2` confinement beneath the allowed mount against concurrent changes (lgse/strata#502).
- Lookups run at most 8 at a time. Cancelling drops pending futures but cannot stop a system call already blocked in the kernel (lgse/strata#502).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-08 | lgse/strata#1527 | fix | Restored without `RENAME_NOREPLACE` through hard links or exclusive copies, keeping no-clobber. |
| 2026-09-14 | lgse/strata#913 | fix | Refused restore through a same-volume symlink parent. |
| 2026-09-12 | lgse/strata#873 | fix | Made the undo restore's trash scan cancellable. |
| 2026-09-10 | lgse/strata#776 | fix | Checked filesystem identity before mount boundaries so cross-filesystem home-trash refusals name the cause. |
| 2026-09-10 | lgse/strata#777 | fix | Refused restore at lookup when the destination's parent folder is gone. |
| 2026-09-10 | lgse/strata#502 | fix | Validated untrusted `.trashinfo` destinations against the trash volume and confirmed full paths before moving. |

## Known gaps

- A lookup timeout frees its batch slot while the blocking worker may still run, so more than 8 lookups can be outstanding. lgse/strata#733
- docs/trash-restore-testing.md still says filesystems without `RENAME_NOREPLACE` get an error; restore now falls back instead. lgse/strata#1526
