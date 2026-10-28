---
title: Releasing open files before a change
status: shipped
origin: {issue: lgse/strata#1590, pr: lgse/strata#1729}
branch: null
reviewed_at: 86df474dc0e8352e0e2098637a017cc4c77a8c44
review: draft
code: [src/adapters/local_operations/release.rs, src/adapters/local_operations/holders.rs, src/adapters/local_operations/deferred_close.rs, src/services/file_activity.rs]
tests: [src/adapters/local_operations/tests/release.rs, src/adapters/local_operations/holders/tests.rs, src/services/file_activity/tests.rs]
related: [operations/filesystem-compatibility/leftovers, operations/delete, preview/preview-panel/sandbox, devices/volumes/release]
---

## Summary

Before a file operation changes an item, Strata stops its own reads of it. It then waits briefly for files other programs are about to close, and otherwise names the program that holds one. This keeps NFS, SMB, and FUSE from leaving `.nfs…`, `.__smbfile_silly…`, or `.fuse_hidden…` files because of Strata.

## Behavior

### Strata's own reads

- Rename, paste, Delete, Trash, restore, undo, redo, compress, extract, new item, leftover restore, Empty Trash, and unmount refuse new reads of what they change. lgse/strata#1729
- A refused read, such as a preview, of that item or anything inside it reports "This item is being changed by a file operation." lgse/strata#1729
- Running reads of the item are told to stop, and the operation waits for them at most 2 s before going on. lgse/strata#1729
- Deleting or moving a folder on NFS, SMB, or FUSE while Strata previews a file in it succeeds and leaves no hidden leftover. lgse/strata#1729

### Other programs' open files

- Deleting a folder that holds only another program's `.nfs…` or `.fuse_hidden…` file waits up to 2 s for the file to close. lgse/strata#1729
- On SMB the wait for a `.__smbfile_silly…` file is the client's `closetimeo` plus 0.5 s, at most 10 s. lgse/strata#1729
- Closing the program during the wait lets the operation succeed. One wait covers a whole Delete or paste. lgse/strata#1729
- If the file stays open, the folder's error reads "A file in it is still open in %{program}. Close it there and try again." lgse/strata#1729
- The program is named by its app where its process says which one, otherwise by its process name, such as `tail`. lgse/strata#1729
- With no holder found, the error reads "A file in it is still open in another program. Close it and try again." lgse/strata#1729
- On SMB with no holder found, it reads "A file in it is still open in a program on this or another computer." lgse/strata#1729
- When the holder is another Strata read or operation, it reads "A file in it is still in use by Strata. Try again when its other operation or search ends." lgse/strata#1729
- On SMB, a folder rename, same-share move, or Move to Trash refused with `EACCES` is retried for the same budget. lgse/strata#1729
- After that budget it names the holder, or keeps "Permission denied"; with POSIX extensions nothing waits. lgse/strata#1729
- An SMB file rename, move, or Move to Trash refused with `EBUSY` reports "It is still open in a program on this or another computer." lgse/strata#1729

## Design

[docs/filesystem-compatibility.md](https://github.com/lgse/strata/blob/fd6327265eaa3266f8420fe8bd25e965146344b0/docs/filesystem-compatibility.md) "Files that are still open" carries the release, what each mount leaves, and the holder search.

- One registry, `services::file_activity`, records every read of a user's file and every running operation. A folder the user opens is not registered, so browsing where an operation works is never blocked (lgse/strata#1729).
- The release runs on every mount, local disks included (lgse/strata#1729). It resolves the folder's real path, so a read opened through a symlink is released too (lgse/strata#1729).
- Other programs' leftovers are never deleted, renamed, copied, or moved on Strata's own; the error names the holder instead (lgse/strata#1729).
- The holder search checks Strata's own registry first, then `/proc/*/fd` confirmed by `fdinfo`, then `/proc/*/maps`, and stops after 200 ms. It never calls `stat` through another process's descriptor (lgse/strata#1729).
- The SMB rename retry runs only after a refusal. On Linux 7.2.5 no rename was refused after a close, 0 of 360; the retry covers 6.17 to 7.1 (lgse/strata#1729).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |

## Known gaps

- The holder search sees only processes on this computer that Strata may read, and its 200 ms limit is an estimate. lgse/strata#1729
- A leftover nobody holds, such as a crashed NFS client's, keeps its folder until removed by hand. lgse/strata#1729
- An SMB unlink refused by another computer holding the file without delete sharing fails with `EIO`, reported as an I/O error. lgse/strata#1729
- SMB before Linux 6.17 keeps a deleted open file under its own name, which is not recognised. lgse/strata#1729
- The SMB rename retry for Linux 6.17 to 7.1 is unverified. lgse/strata#1729
- rclone, gvfsd-fuse, and GVfs's own deletes meet leftovers with their own errors. lgse/strata#1729
- A single file another program has open is deleted without a report, as on local disks. lgse/strata#1729
