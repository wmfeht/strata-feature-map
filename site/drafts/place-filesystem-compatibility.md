---
proposed: {page: new}
nodes: [operations/filesystem-compatibility, operations/filesystem-compatibility/leftovers, operations/filesystem-compatibility/open-files, operations/trash/fuse-refusals]
reason: 'How moves, copies, and names behave on NFS, SMB, FUSE, FAT, exFAT, and NTFS, the completion report, open-file waits and messages, the leftover review after a crash or unplug, and FUSE mounts that refuse Trash are user-visible, and no page names these nodes. Pages already carry some of it, so the new page should link rather than repeat: typed-name refusals and case-only renames (Keyboard navigation, "Creating files and folders"); the 2 s release of Strata''s own reads and "This item is being changed by a file operation." (Preview sandbox, "Scheduling and deadlines"); the tip that a FUSE mount that refused Trash gets the permanent confirmation (Everyday operations guide, "Trash, restore, and delete", and 10xer mode reference, "Files"); and "Writing to device…" and the docked transfer report (Archives, "Feedback and cancellation"). No section covers the rest. Upstream keeps it in docs/filesystem-compatibility.md; proposed as a "Filesystem compatibility" reference page with one `##` section per heading below, mirroring that doc''s user-facing headings.'
release: v1.1.1
---

Raw material for a "Filesystem compatibility" reference page. Network change
checks are drafted separately in place-network-checks.md.

## Guarantees

Every local move, copy, Replace, Merge, restore, rename, undo, and archive
publication follows three rules:

- An item that appears at the destination meanwhile is never overwritten.
- Nothing only the copy holds is deleted before the copy is flushed to the
  device.
- No disk work runs on the window's thread, so a slow mount never freezes the
  window.

Every name Strata changes, and every item it leaves out, is reported.

## Moves

- A move within one filesystem renames in place without copying data, also on
  NFS, ntfs-3g, 9p, ceph, sshfs, vboxsf, rclone, and s3fs. A move copies only
  across filesystems, or where no rename can place the item. On sshfs whose
  server lacks `posix-rename@openssh.com`, the move copies.
- A rename refused for an invalid name reports it as such. A folder moved into
  itself is refused, not copied.
- A move checks the source name just before it runs, and refuses another item
  found there, moving nothing.
- If the reply to a rename is lost (`EIO`, `ETIMEDOUT`), mounts with stable inode
  numbers clean up and report the error. On sshfs and vboxsf, both names stay and
  the item is reported as unconfirmed. An item found at the destination with
  another identity right after a move also stays there, reported as unconfirmed,
  and is never moved back.

## Copying

Pastes, Duplicate, Keep Both, moves between filesystems, Replace, Merge, and
Trash restores between local paths use Strata's own copy engine. GVfs locations
use GIO, with no flush, content check, or retry of a refused name.

- A copied item appears under its final name only when complete. A cancelled or
  failed copy leaves nothing partial under a real name. On local POSIX disks a
  file is written unnamed and linked when done; elsewhere the copy is built in a
  hidden `.strata-copy-*` folder first.
- Every file copy reports byte progress.
- Sparse files of 1 MiB or more keep their holes when copied from ext4, XFS,
  btrfs, tmpfs, or f2fs. Holes are filled onto FAT, exFAT, and NTFS.
- Copied folders keep mode, times, owner, and extended attributes; a `0555`
  folder stays `0555`. A read-only item keeps its `user.*` attributes. A copy into
  a setgid folder keeps the folder's group, and a copy that cannot keep the owner
  drops setuid and setgid.
- Hard links inside one copied item stay linked where the destination keeps hard
  links. They are never kept from plain SMB shares or sshfs.
- Named pipes are recreated. Sockets and device files are left out and reported,
  and the copy goes on.
- An unreadable source fails with "Could not copy \<name>: \<error>".
- A paste of more than 8 files with no conflicts runs up to 8 at a time, or 1
  when either disk is rotational.

### Moves that copy

A move between filesystems deletes each source item only if it still matches the
copy: type, size, and times, plus inode, change time, and link count where the
mount keeps them stable.

- A file written during its copy is copied once more. If it changes again, it
  stays at the source.
- A file modified within the mount's timestamp tick, 2 s on FAT and exFAT and 3 s
  on sshfs, is compared by content first. So moving a just-saved file takes up to
  that long. Without multigrain timestamps, such as before Linux 6.13, a file
  modified within 100 ms of its read is compared by content.
- A source item that no longer matches, or cannot be deleted, stays where it was,
  is reported, and is left out of Undo.
- Nothing is deleted until the destination is flushed, and a failed flush deletes
  nothing. That covers move sources, Replace originals, merge set-asides, and
  restored Trash copies. On vfat, msdos, exFAT, ntfs3, ntfs-3g, and exfat-fuse,
  the flush is a folder fsync, syncfs, then a folder fsync again.
- Source deletions after a flush are batched at 256 items, 1 GiB, or 5 seconds.
- For a hard-linked file, later names follow the first name's content check, so a
  rewrite within the tick keeps every name at the source. On an SMB source, every
  later name of a file whose first name was compared by content stays at the
  source, reported as changed.

### Same-item checks

Strata decides whether an item is still the one it read using what each mount
keeps:

| Mount | Proof |
| --- | --- |
| vfat, exFAT | Birth time plus the recorded size and modification time |
| NFSv3, ext2/3/4 without birth times | File handle |
| SMB | The server's creation time, plus the server inode number while the mount shows `serverino` |
| ntfs-3g | Inode number, once Strata's probe shows the mount keeps it |

- On vfat and exFAT, a copy or Replace completes even when the kernel renumbers
  the entry.
- On sshfs, exfat-fuse, and vboxsf, a Replace target swapped for a same-size,
  same-time file during the copy is refused as changed. A move's copy replaced
  that way before the source is deleted keeps the source.
- A move from an SMB share whose `serverino` went off after the copy still deletes
  its sources once proven.

## Names

Names brought onto FAT, exFAT, NTFS, SMB without POSIX extensions, or MTP change
to fit:

| Name | Becomes |
| --- | --- |
| `< > : " \ \| ? *` and control characters | `_`, so `10:00` is saved as `10_00` |
| Trailing dots and spaces | Dropped |
| Malformed UTF-8 bytes | `_` |
| `CON` and other Windows device names | `CON_` |
| `aux.c` | Kept on FAT, exFAT, and ntfs3; `aux_.c` on ntfs-3g, ntfs3 with `windows_names`, and SMB without POSIX extensions |

- On every destination, a name too long for it is cut in the destination's
  unit, keeping the extension and whole characters. For example, a name of 100
  CJK characters copied onto ext4 arrives as 83 characters plus `.txt`.
- Duplicates, restores, and moves within one filesystem keep every name.
- Two names the destination cannot tell apart, on FAT, exFAT, SMB, or a
  case-folding folder, both arrive: of `Makefile` and `makefile`, the later in
  byte order is saved as `makefile (1)`. Top-level items from two folders with the
  same name, such as `notes.txt`, save the later as `notes (1).txt`.
- A destination reached through a symlink, such as `~/stick` into
  `/run/media/…`, follows the rules of the drive behind it, including the 4 GiB
  file limit on FAT32.
- A name an sshfs or other FUSE mount still refuses is retried under Windows
  rules, which that mount then keeps. When nothing helps, the item fails with "The
  name isn’t valid at this location" or "The name is too long".
- Pasting `10:00` onto a FAT drive that already holds `10_00` asks about the
  conflict, explaining "“10:00” will be saved as “10_00” in this location."
- A name you type, in a rename, a new item, or an archive name, is refused with
  the reason instead of fixed: "Names in this location can’t contain “:”",
  "Names in this location can’t end with a space or a period", "“CON” is a
  reserved name in this location", or "The name is too long".
- A case-only rename, such as `notes.txt` to `Notes.txt`, works on vfat, exFAT,
  SMB, case-folding ext4, and exfat-fuse, and so does its undo. Renaming a file to
  the name of another hard link to it, in the 10xer prompt, keeps the prompt open
  with "“link.txt” already exists".
- A symlink the destination cannot store is left out and reported, and the paste
  goes on: at once on FAT and exFAT, after the first refusal on SMB without POSIX
  extensions. A move keeps such a link at the source and leaves its item out of
  Undo.
- Link targets are never rewritten, so a link to a renamed entry dangles. Only
  names are checked, not whole paths.

## Completion report

- One renamed item whose report line is 120 characters or fewer shows a dock
  notice for 6 seconds.
- Several renamed items open "N items were saved under new names", adding "Names
  changed for different reasons" when the reasons differ.
- Any item left out or left behind opens a warning listing every section.
- A cancelled or failed transfer shows one dialog: its outcome, then the report.

Sections read "The destination can’t tell these names apart", "These names were
already taken", "The destination doesn’t allow these names", "These names were
too long for the destination", "These special files can’t be copied and were left
out", and "These symbolic links can’t be stored at the destination and were left
out", or their singular forms for one item. Each line quotes its names, such as
"“10:00” was saved as “10_00”". A move whose items partly stayed at the source
adds "Undo can’t move these items back, as part of each stayed in its original
folder."

## Files that are still open

Rename, paste, Delete, Trash, restore, undo, redo, compress, extract, new item,
leftover restore, Empty Trash, and unmount first stop Strata's own reads of what
they change, such as a preview, and wait for them up to 2 s. A read of an item
being changed reports "This item is being changed by a file operation." So
deleting or moving a folder on NFS, SMB, or FUSE while Strata previews a file in
it leaves no hidden leftover.

Another program's `.nfs…`, `.__smbfile_silly…`, or `.fuse_hidden…` file inside a
copied or moved folder is left out silently. A move keeps that source folder and
reports "“\<name>” was left in “\<folder>”, as a file in it is still open in
\<program>".

Deleting a folder that holds only such a file waits for it to close: up to 2 s
for `.nfs…` and `.fuse_hidden…`, and on SMB the mount's `closetimeo` plus 0.5 s,
at most 10 s. Closing the program during the wait lets the operation succeed.
One wait covers a whole Delete or paste. If the file stays open, the error names
the holder:

| Holder | Message |
| --- | --- |
| A program Strata can find | "A file in it is still open in \<program>. Close it there and try again." |
| None found | "A file in it is still open in another program. Close it and try again." |
| None found, on SMB without POSIX extensions | "A file in it is still open in a program on this or another computer." |
| None found, on SMB with POSIX extensions | The system error, such as "Permission denied" |
| Strata itself | "A file in it is still in use by Strata. Try again when its other operation or search ends." |

The program is named by its application where its process says which one,
otherwise by its process name, such as `tail`. Strata can see only processes on
this computer that it may read.

On SMB, a folder rename, same-share move, or Move to Trash refused while a file is
open is retried for the same time, then names the holder or keeps "Permission
denied"; with POSIX extensions nothing waits. A file rename, move, or Move to
Trash refused as busy reports "It is still open in a program on this or another
computer." A single file another program has open is deleted without a report,
as on local disks.

## Leftovers after a crash or unplug

A crash, kill, or unplug during an operation can leave hidden items: originals
set aside (`.strata-originals-*`), merges (`.strata-merge-*`), incomplete copies
(`.strata-copy-*`, `.strata-extraction-*`), and older builds' names such as
`.strata-replacement-ab12Cd`. A name counts only as a known prefix followed by an
id, so `.strata-copy-notes` is an ordinary file, and `.nfs…`, `.fuse_hidden…`, and
`.__smbfile_silly…` files never count.

A folder holding one gets an icon-only pane-header button, "Items left by an
interrupted operation", in every Columns column and in Icons and List. While a
Strata operation is changing the folder, the button waits until it ends. The
system file chooser, Trash, and Recent show no button. The first time per session
a shown folder holds possible originals, a dock card reads "“\<folder>” holds
originals that an interrupted operation set aside." with **Review**, which opens
the folder if it was closed. The card closes after 15 s unless pinned. A folder
holding only an incomplete copy shows the button but no card.

The review lists each item with its kind, contents, date, and hidden name, under
"Another program or computer may still be using these items. Restore never
replaces an existing item."

- **Restore**, for originals and merges, puts the items back under their own
  names, selects them, and removes the emptied hidden folder. It adds nothing to
  Undo. A name taken meanwhile gets the next Keep Both number, such as
  `song (1).flac`, listed under "This name was already taken". An older build's flat hidden name restores as
  "Recovered item", numbered if taken, with the name editor open; that rename
  can be undone.
- **Show** reveals the item and turns hidden files on.
- **Delete…**, for incomplete copies ("A copy that never finished. Its source was
  not changed."), runs the usual confirmed Delete, to Trash where the folder has
  one.
- An item still open in another program, or gone ("No longer here"), offers no
  Restore. GVfs locations offer no Restore for originals or merges.
- While an operation runs in the folder, Restore and Delete… report "Wait for the
  running operation to finish, then try again."; Show still works.
- On a read-only ntfs3 drive, Restore reports "The drive is read-only. It may
  need to be checked for errors after it was unplugged without being ejected."

With hidden files shown, the menu of a single originals, merge, or older-build
leftover row also offers **Restore**. Strata removes nothing on its own except
its own empty `.strata-probe-*` items over an hour old, once per folder per
session. Leftovers in a folder nobody opens stay.

## FUSE mounts that refuse Trash

Some FUSE mounts, such as sshfs, rclone, s3fs, and mergerfs, report Trash support
but refuse the move partway. On a FUSE mount, a trash move refused with
permission denied, failed, or invalid argument, or a failure writing the
`.trashinfo` file other than a full disk, a missing path, a read-only mount, or a
name too long, makes Strata treat the mount as having no Trash. That holds only
while the item is still there, the mount answers, the item is off your home
drive, and you may remove it. On other disks, only a not-supported error counts,
and Strata does not remember it.

After such a refusal on a FUSE mount, the folder reloads, and the next Delete on
that mount opens the permanent-deletion confirmation with the reason, without
trying Trash. **Move to
Trash** is hidden on that mount. Strata removes any new, empty `.Trash-$uid` or
`.Trash/$uid` folder the attempt created, unless something in the same batch was
trashed there. The mount is remembered in every window until it is remounted, or
until **F5** or a pane's Refresh, which try Trash again. A disconnected FUSE mount
keeps its own error instead of "This location doesn't support Trash."
