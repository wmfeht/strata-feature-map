---
title: Filesystem-safe placement and copying
status: shipped
origin: {issue: lgse/strata#1590, pr: lgse/strata#1615}
branch: null
reviewed_at: fd6327265eaa3266f8420fe8bd25e965146344b0
review: draft
code: [src/adapters/local_operations/placement.rs, src/adapters/local_operations/copy_engine.rs, src/adapters/local_operations/copy_engine/**, src/adapters/local_operations/case_variants.rs, src/adapters/local_operations/environment.rs, src/adapters/local_operations/mount_profile.rs, src/adapters/local_operations/names.rs, src/adapters/local_operations/names/fix.rs, src/adapters/local_operations/owed.rs, src/adapters/local_operations/typed_names.rs, src/adapters/volume/mount_capabilities.rs, src/adapters/volume/names.rs, src/ui/browser/transfer_report.rs, src/services/item_identity.rs, src/model/hidden_names.rs]
tests: [src/adapters/local_operations/tests/placement.rs, src/adapters/local_operations/tests/fs_quirks.rs, src/adapters/local_operations/tests/file_copy.rs, src/adapters/local_operations/tests/folder_copy.rs, src/adapters/local_operations/tests/aliases.rs, src/adapters/local_operations/mount_profile/tests.rs, src/adapters/volume/names/tests.rs, src/ui/browser/transfer_report/tests.rs, scripts/fslab/**, src/services/item_identity/tests.rs, src/adapters/local_operations/environment/tests.rs, src/model/hidden_names/tests.rs]
docs: [docs/filesystem-compatibility.md]
related: [operations/clipboard, operations/clipboard/conflicts, operations/rename, operations/create, operations/trash, operations/trash/restore, operations/archives, operations/undo, operations/progress, operations/progress/dock]
---

## Summary

The no-clobber placement routine, the native copy engine, the identity rule, and the name rules behind every local file operation. They cover move, copy, Replace, Merge, restore, rename, undo, and archive publish. They keep these working on NFS, SMB, FUSE, FAT, exFAT, NTFS, and case-insensitive mounts. Every changed name and left-out item is reported. Children: `operations/filesystem-compatibility/open-files` (releasing open files before a change) and `operations/filesystem-compatibility/leftovers` (what a crash or unplug leaves).

## Behavior

### Placement

- A move within one NFS, ntfs-3g, 9p, or ceph mount, where `RENAME_NOREPLACE` returns `EINVAL`, finishes without copying any data. lgse/strata#1615
- There a file is hard-linked and its old name unlinked once the link proves its identity; a folder is renamed over an exclusive empty placeholder. lgse/strata#1615
- On sshfs, vboxsf, rclone, and s3fs, a file is renamed over an exclusive empty placeholder after a check. lgse/strata#1615
- On sshfs a folder is renamed over an exclusive empty placeholder. On vboxsf a folder is renamed to a name found free. lgse/strata#1615
- On sshfs whose server lacks `posix-rename@openssh.com`, the move copies instead. lgse/strata#1615
- A move copies only across devices, or where no placement step can place the item. lgse/strata#1615
- An item that appears at the destination meanwhile is never overwritten, except in the reserved-name step's window. lgse/strata#1615
- An `EINVAL` from a rename reports an invalid name as such and refuses a folder moved into itself, instead of copying. lgse/strata#1615
- A lost reply (`EIO`, `ETIMEDOUT`) to the rename over a placeholder removes the placeholder and reports the error on mounts with stable inode numbers. lgse/strata#1615
- On sshfs and vboxsf, such a lost reply keeps both names and reports the item as unconfirmed. lgse/strata#1615
- On a mount whose type is unknown or unreadable, a lost reply never removes the placeholder on an equal inode number. lgse/strata#1729
- An item found at a placement's destination with another identity right after the move stays there, reported as unconfirmed, and is never moved back. lgse/strata#1729

### Identity

- On vfat and exFAT, a copy or Replace whose entry the kernel renumbered completes without "… changed while the operation was in progress". lgse/strata#1729
- There a file is proven by birth time plus its recorded size and modification time. Without that record, only the exact inode passes. lgse/strata#1729
- On NFSv3 and on ext2/3/4 without birth times, an item recreated with the old inode number counts as another item by its file handle. lgse/strata#1729
- On SMB, an item is proven by the server's creation time, plus the server inode number while the mount options still show `serverino`. lgse/strata#1729
- A move from an SMB share whose `serverino` went off after the copy deletes its sources once proven. lgse/strata#1729
- On SMB after `serverino` goes off, a Replace target replaced elsewhere with the same modification time is refused as changed. lgse/strata#1729
- On sshfs, exfat-fuse, and vboxsf, a Replace target swapped for a same-size, same-time file during the copy is refused as changed. lgse/strata#1729
- There a move's copy replaced by a same-size, same-time file before the source is deleted keeps the source. lgse/strata#1729
- On ntfs-3g, inode numbers count as kept once Strata's probe link keeps the number with two links. lgse/strata#1729
- In 10xer mode, the rename prompt accepts a case-only rename such as `foo` to `Foo` on exfat-fuse, and on SMB after `serverino` went off. lgse/strata#1729
- Renaming `a.txt` to another hard link's name, `link.txt`, or its case variant on a case-insensitive folder, keeps the prompt open with "“link.txt” already exists"; nothing changes. lgse/strata#1729

### Copying

- Pastes, Duplicate, Keep Both, cross-filesystem moves, Replace, Merge, and restore copies between native paths use Strata's copy engine. GVfs locations use GIO. lgse/strata#1615
- A copied item appears under its final name only when complete. A cancelled or failed copy leaves nothing partial at a real name. lgse/strata#1615
- On local POSIX filesystems a copied file is written unnamed (`O_TMPFILE`) and linked when done; elsewhere the copy is built in a hidden `.strata-copy-*` stage. lgse/strata#1615
- Every native file copy reports byte progress. lgse/strata#1615
- A sparse file of 1 MiB or more copied from ext4, XFS, btrfs, tmpfs, or f2fs keeps its holes. lgse/strata#1615
- Holes are filled onto FAT, exFAT, and NTFS, including exfat-fuse and ntfs-3g. lgse/strata#1615
- A copied folder keeps its mode, times, owner, and xattrs; a `0555` folder stays `0555`. lgse/strata#1615
- A read-only item keeps its `user.*` xattrs. lgse/strata#1615
- A copy into a setgid folder keeps the folder's group. lgse/strata#1615
- A copy that cannot keep the source's owner drops setuid and setgid. lgse/strata#1615
- Hard links inside one copied item stay linked where the destination keeps hard links. lgse/strata#1615
- A named pipe inside a copied folder is recreated. lgse/strata#707, lgse/strata#1615
- Sockets and device files inside a copied folder are left out and reported, and the copy goes on. lgse/strata#1615
- Another program's `.nfs…`, `.__smbfile_silly…`, or `.fuse_hidden…` file inside a copied or moved folder is left out without a report line. lgse/strata#1729
- A move keeps such a source folder and reports "“%{name}” was left in “%{folder}”, as a file in it is still open in %{program}". lgse/strata#1729
- An unreadable source, such as one refusing with `EACCES` or `EIO`, fails with "Could not copy <name>: <error>". lgse/strata#1615 (unverified)

### Moves that copy

- A move that copies deletes each source entry only if it still matches the copy. lgse/strata#215, lgse/strata#1615
- The match compares type, size, and times, plus inode, change time, and link count where those are stable. lgse/strata#1615
- A source entry that no longer matches, or cannot be deleted, stays at the source, is reported, and keeps its item out of Undo. lgse/strata#1615
- A file written during its copy is copied once more; if it changes again, it stays at the source. lgse/strata#1615
- A file modified within the mount's timestamp tick is compared by content before its source is deleted. lgse/strata#1615
- That tick is 2 s on FAT and exFAT, and 3 s on sshfs. lgse/strata#1615
- Without multigrain timestamps, such as before Linux 6.13, a file modified within 100 ms of its read is compared by content. lgse/strata#1615
- When the first name of a hard-linked file was compared by content, later names use that content check. A rewrite within the tick keeps every name at the source. lgse/strata#1751
- On an SMB source, every later name of a file whose first name was compared by content stays at the source, reported as changed. lgse/strata#1751
- Nothing only the copy holds is deleted before the destination is flushed. lgse/strata#1615
- That covers move sources, Replace originals, merge set-asides, and restored Trash copies. lgse/strata#1615
- A failed flush deletes nothing. lgse/strata#1615
- On vfat, exFAT, ntfs-3g, and exfat-fuse, a set-aside original is removed after flushing its folder, the filesystem, then the folder again. On ntfs3 the folder is flushed first. lgse/strata#1729
- Source deletions after a flush are batched at 256 items, 1 GiB, or 5 seconds. lgse/strata#1615
- A paste of more than 8 native files with no conflicts copies or moves up to 8 at a time, or 1 when either disk is rotational. lgse/strata#1615
- An SMB open of another hard-linked name refused during the client's deferred close is retried for `closetimeo` plus 0.5 s, at most 10 s. lgse/strata#1615

### Names

- Names brought onto FAT, exFAT, NTFS, SMB without POSIX extensions, or MTP turn `< > : " \ | ? *` and control characters into `_`. lgse/strata#1126, lgse/strata#1615
- There trailing dots and spaces are dropped, and malformed UTF-8 bytes become `_`. lgse/strata#1126, lgse/strata#1615
- `CON` becomes `CON_` wherever Windows rules apply. lgse/strata#1615
- `aux.c` keeps its name on FAT, exFAT, and ntfs3, and becomes `aux_.c` on ntfs-3g, ntfs3 with `windows_names`, and SMB without POSIX extensions. lgse/strata#1615
- A name too long for the destination is cut in the destination's unit, keeping the extension and whole characters. lgse/strata#1615
- For example, a name of 100 CJK characters copied onto ext4 arrives as 83 characters plus `.txt`. lgse/strata#1615
- Duplicates, restores, and moves within one filesystem keep every name. lgse/strata#1615
- Two source names that FAT, exFAT, SMB, or a casefold folder cannot tell apart both arrive, under separate names. lgse/strata#1126, lgse/strata#1615
- Of `Makefile` and `makefile`, the later in byte order is saved as `makefile (1)`. lgse/strata#1126, lgse/strata#1615
- Top-level items from two folders sharing a name, such as `notes.txt`, save the later one as `notes (1).txt` before copying. lgse/strata#1615
- A destination reached through a symlink, such as `~/stick` into `/run/media/…`, gets the rules and the 4 GiB check of the mount behind it. lgse/strata#1615
- A name an sshfs or other FUSE mount still refuses is retried under stricter Windows rules, which that mount then keeps. lgse/strata#1615
- When no rule helps, the item fails with "The name isn’t valid at this location" or "The name is too long". lgse/strata#1615
- A symlink the destination cannot store is left out and reported, and the paste goes on. lgse/strata#1615
- This happens at once on FAT and exFAT, and after the first refusal on SMB without POSIX extensions. lgse/strata#1615
- A move keeps such a link at the source, and Undo leaves its item out, naming it. lgse/strata#1615

### Completion report

- A transfer that renamed one item, with a line of 120 characters or fewer, shows a dock notice with the section heading for 6 seconds. lgse/strata#1615 (unverified)
- Several renamed items open an information dialog, "N items were saved under new names"; renames for several reasons add "Names changed for different reasons". lgse/strata#1615
- Any item left out or left behind opens a warning listing every section. lgse/strata#1615
- A cancelled or failed transfer shows one dialog: its outcome, then the report. lgse/strata#1615
- Sections with several items read "The destination can’t tell these names apart", "These names were already taken", "The destination doesn’t allow these names", or "These names were too long for the destination". lgse/strata#1615, lgse/strata#1729
- A section with one item reads "The destination can’t tell this name apart from another", "This name was already taken", "The destination doesn’t allow this name", or "This name was too long for the destination". lgse/strata#1729
- Left-out sections with several items read "These special files can’t be copied and were left out" and "These symbolic links can’t be stored at the destination and were left out". lgse/strata#1615, lgse/strata#1729
- With one item they read "This special file can’t be copied and was left out" and "This symbolic link can’t be stored at the destination and was left out". lgse/strata#1729
- Each line quotes its names, such as "“10:00” was saved as “10_00”". lgse/strata#1729
- A move whose items partly stayed at the source adds "Undo can’t move these items back, as part of each stayed in its original folder." lgse/strata#1615

## Design

[docs/filesystem-compatibility.md](https://github.com/lgse/strata/blob/fd6327265eaa3266f8420fe8bd25e965146344b0/docs/filesystem-compatibility.md) carries the guarantees, placement, identity, copying, names, open files, leftovers, and per-filesystem notes. lgse/strata#1615 shipped steps 1 to 3 of lgse/strata#1590, and lgse/strata#1729 steps 4 to 8.

- Invariants: never overwrite a destination that appeared concurrently, never delete what the copy does not hold, and run no disk operation on the GTK main thread (lgse/strata#1590, lgse/strata#1615).
- Placement tries `renameat2(NOREPLACE)`, then a file hard link, then a folder rename over an exclusive placeholder, then the reserved-name step, then a copy. `EEXIST` stays authoritative (lgse/strata#1615).
- The reserved-name step loses only a write that another program makes to that exact name between the check and the rename. GLib checks then renames with no placeholder, which is weaker (lgse/strata#1615).
- Rejected: check-then-rename as in GLib, Nautilus, KIO, and coreutils; the copy fallbacks of lgse/strata#1515 and lgse/strata#1586, which doubled writes and lost metadata; and gating on filesystem type (lgse/strata#1590).
- Capabilities are probed per mount and cached by mount ID until the mount table changes. The filesystem family decides only naming, flushing, `O_TMPFILE`, and timestamp granularity (lgse/strata#1590, lgse/strata#1615).
- `RENAME_EXCHANGE` is used only on in-kernel local filesystems. exfat-fuse reports success for it but overwrites (lgse/strata#1615).
- Every "is this still the same item?" decision goes through one rule per mount, replacing two rules that disagreed. It weighs device, type, file handle, birth time, inode, and recorded size and times, by what the mount keeps (lgse/strata#1729).
- FAT counts births in 10 ms ticks, so a file's birth time needs the recorded size and modification time beside it (lgse/strata#1729).
- exFAT folder births are not compared, because every rename into a folder reset it, 12 of 12 in the lab (lgse/strata#1729).
- NFSv3 and ext without births compare file handles, which changed in 198 of 198 NFSv3 inode reuses in the lab (lgse/strata#1729).
- Where nothing else proves a single Replace target or stage, it is held with an `O_PATH` descriptor so it keeps its number. Never on NFS, where a hold left a `.nfs…` file in 10 of 10 runs (lgse/strata#1729).
- SMB's creation time stands in for the inode, because the client can drop `serverino` without a mount-table event. The options are read again at each decision (lgse/strata#1729).
- Records kept after an operation, such as Trash lookups and saved views, carry the mount's traits in `ItemIdentity`. A comparison uses the weaker of two (lgse/strata#1729).
- Each filesystem is flushed the way the lab measured it reaches the device. `syncfs` alone flushes nothing on vfat, exFAT, and FUSE daemons (lgse/strata#1615).
- Only the first name of a hard-linked file is read during a copy, so later names inherit its digest. SMB refuses to open another name of a file it recently opened, so keeping them is the safe choice (lgse/strata#1750, lgse/strata#1751).
- Owner decisions: pipes are recreated and other special files skipped, the setgid group is kept, and typed names are refused, never fixed (lgse/strata#1615).
- Lead decisions: malformed UTF-8 becomes `_`, not U+FFFD; `CON` becomes `CON_`; NTFS case pairs are not numbered; holes are kept as with `cp --sparse=auto` (lgse/strata#1615).
- Device names follow the Windows 11 rule where a filesystem stores them, and the full rule where they are refused or mangled (lgse/strata#1615).
- One dialog per outcome, never a stacked report (lgse/strata#1615).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-20 | lgse/strata#1729 | fix | Released Strata's reads, identified items by one rule per mount, and recovered crash leftovers, finishing lgse/strata#1590. |
| 2026-10-18 | lgse/strata#1751 | fix | Compared later hard-link names by the first name's digest, so a cross-volume move keeps a rewritten later name. |
| 2026-10-17 | lgse/strata#1615 | fix | Added a no-clobber placement ladder, a native copy engine, and per-mount name rules, so operations work on NFS, SMB, FUSE, FAT, and casefold mounts. |

## Known gaps

- On SMB2/3, `NOREPLACE` is enforced only on the client, and a writer that keeps a file open still fails a linked-name copy. lgse/strata#1615
- A share set to compare case still gets `(1)` for case pairs. lgse/strata#1615
- SFTP without `posix-rename@openssh.com` cannot rename over a placeholder, so file renames, archive publication, and setting a file aside are refused. lgse/strata#1615
- On ntfs-3g a reused inode number passes for the original. On exfat-fuse and sshfs an unheld item with the same type, size, and times passes. lgse/strata#1729
- On vfat and exFAT, a file made within the same 10 ms tick with the same size and modification time passes. lgse/strata#1729
- On SMB after `serverino` goes off, neither a moved copy's proof nor the removal of what an operation set aside compares the change time. lgse/strata#1729
- File handles were measured only on knfsd `no_subtree_check` exports; elsewhere a false "different" keeps the item. lgse/strata#1729
- On sshfs and vboxsf, a folder put at a held Replace target's name passes for the target. lgse/strata#1729
- On SMB without server numbers, two names of one hard-linked file moved as separate items leave the later name at the source. lgse/strata#1729
- A hard-linked file's change time is checked only within one item. lgse/strata#1729
- A folder the user can neither write nor chmod cannot be set aside or case-renamed: "Permission denied", where earlier builds' flat hidden name worked. lgse/strata#1729
- A server or daemon clock more than 100 ms behind the client (2 s on sshfs) can hide a same-size rewrite. lgse/strata#1615
- Moving a just-saved file takes up to 2 s longer on FAT and exFAT, and 3 s on sshfs. lgse/strata#1615
- On ntfs-3g, an empty folder created at a 237-unit name in the check window is replaced. lgse/strata#1615
- Hard links are never kept from plain SMB shares or sshfs. lgse/strata#1615
- GVfs destinations get no flush, no content check, and no retry of a refused name. lgse/strata#1615
- Only names are checked, not paths, so Windows' `MAX_PATH` is not predicted. lgse/strata#1615
- Link targets are never rewritten, so a link to a renamed entry dangles. lgse/strata#1615
