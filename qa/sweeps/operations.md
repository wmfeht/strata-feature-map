---
title: Operations sweep
reviewed_at: bf26829b4fd74c1f25ac170aad9521a633234a30
triggers: [src/services/operations.rs, src/services/operations/**, src/services/file_source.rs, src/services/file_source/tests.rs, src/adapters/local_operations.rs, src/adapters/local_operations/tests.rs]
tools: [docs/trash-restore-testing.md, docs/archives.md, docs/filesystem-compatibility.md, scripts/fslab, scripts/generate-fixture.sh, scripts/qa-mutation.sh, tests/qa/fixtures/content-encrypted.7z, tests/qa/mutations]
---

## Scope

Everything that changes files on disk from the browser: New Folder and New File, inline rename, copy, cut, and paste with their name conflicts, Move to and Copy to, Send to, drag and drop with its copy-or-move policy and column autoscroll, filesystem-safe placement, copying, identity, and name fixing, releasing open files, leftover recovery, Trash with restore, Empty Trash and the flight animation, permanent deletion, archives with RAR and archive preview, operation progress with the dock and the job queue, and undo and redo across all of them.

Left to other sweeps: pointer gestures and selection before a drag starts, the sidebar Trash row as a place to navigate to, the modal dialog shell, rendering of archive members in the preview panel, the devices Send to lists, provider destinations inside Send to…, folder reloads after operations, and the 10xer-mode key variants.

## Setup

- A fixture tree with mixed names: Unicode, a non-UTF-8 name made with `printf 'bad\xff.txt'`, a 255-byte name, two names differing only by case, dot-prefixed files, a symlink, a read-only folder (`chmod 555`), and an empty folder.
- A second filesystem. `/dev/shm` serves cross-volume drops, Trash-unsupported paths, and copy-or-move prompts. Free-space refusals need a small tmpfs (`mount -t tmpfs -o size=8m`); skip those probes and say so when no mount is available.
- A filesystem without `RENAME_NOREPLACE`: a loop image made with `mkfs.ntfs -F`, mounted with `ntfs-3g -o permissions` so modes apply. `/dev/shm` and tmpfs support the flag.
- Run the ntfs-3g probes as a non-root user, so mode `0000` blocks reads. Skip them and say so when ntfs-3g is unavailable.
- `scripts/fslab/fslab.sh up` starts a privileged container with NFS, SMB, sshfs, vfat, exFAT, ntfs3, ntfs-3g, exfat-fuse, and casefold mounts; `fslab.sh probe` reports what each supports. Skip lab probes and say so when Docker cannot run privileged.
- A real USB stick formatted vfat, and one exFAT, for flush and unplug probes; the lab's loop devices live in RAM.
- An sshfs mount without `default_permissions` and an rclone mount, for FUSE Trash refusals. The lab has no rclone; skip those probes and say so when it is unavailable.
- A 9p or virtiofs share and a mergerfs pool, for deletion wording. The lab has neither; skip those probes and say so when unavailable.
- A holder for open files on the NFS, SMB, and sshfs mounts: `less` or `tail -f` run from a terminal app, and the same run as a plain process outside any app unit.
- A large tree from `scripts/generate-fixture.sh` for progress, cancellation, and Empty Trash measuring.
- Archives built with system tools in ZIP, 7Z, TAR, and TAR.GZ; `tests/qa/fixtures/content-encrypted.7z` for passwords; hostile archives under `/tmp` with a `../` member, an absolute-path member, a symlink member pointing outside, and a header that lies about its size. RAR needs `rar` on PATH or a sample from `tests/fixtures/rar/`.
- Two windows of the same build for cross-window paste, undo, and progress dock checks.
- A desktop session running `gvfsd` for `trash:///` listings. The pinned test container sets `GIO_USE_VFS=local` and cannot browse Trash.
- Verify every operation on disk with `ls -la`, `stat`, and `cmp`, never in the listing alone. Watch the log for GTK criticals during dialogs and animations.
- `tests/qa/mutations/` holds deliberate defects the QA scenarios must catch; `./scripts/qa-mutation.sh drag-and-drop` or `rename-caret` is evidence when those areas changed.

## Probes

- Run each operation in Columns, Icons, and List, from the item menu, the keyboard, and the background menu where offered; the result on disk must be the same.
- Repeat a destructive operation on a directory removed underneath Strata (`rm -rf` from a shell while the dialog is open).
- After each operation, press Ctrl+Z then Ctrl+Shift+Z and diff the tree against a `find -printf '%p %s %T@\n'` snapshot taken before.

### operations/create

- Create inside an empty folder, a read-only folder, Trash, a Ctrl+F result, and in a Columns pane that is not the last column; note which column the editor opens in.
- Create with a 255-byte name, a name ending in a space, and `.hidden` with hidden files off.
- Press Ctrl+Shift+N ten times quickly while earlier items are still in their editors; the `(n)` suffixes must stay unique.
- Press Ctrl+Alt+N in Columns with a selection in one column and keyboard focus in another, and with a selection of only hidden items after hidden files are turned off.
- On vfat and on an SMB share with POSIX extensions, take `new folder` with a file, then create there.
- Create in a folder whose names are near the length limit.

### operations/rename

- Commit by Enter, by clicking another item, by clicking the background, and press F5 while editing.
- Focus a second window mid-edit, then come back and press Escape.
- Mid-edit, switch input methods with Super+Space under IBus and Ctrl+Space under fcitx5.
- Leave an edit open while another window is active, then close the Strata window from the taskbar; read the name on disk.
- On a vfat or SMB mount, rename to a case-only variant, to a name holding a tab or a combining mark, and to `notes.`; then undo each.
- Rename to a name differing only by case, to an existing name, to a name containing `/`, and to a 255-byte name, in each mode.
- Rename an item at the edge of the viewport, in a column narrower than the name, and while a filter is active.
- Rename an image while its thumbnail is still loading; the thumbnail must follow the new name.
- In Columns, toggle Show sizes in Columns view while a rename editor is open, then commit and cancel.
- With hidden files off, rename a file and a folder to dot names in each mode. Then create a file there from a shell, and repeat with hidden files on.
- With airy spacing, commit a rename that stays visible, then click into another folder before the reveal ends.
- Create an item in a slot that is already visible, with the list scrolled partway.

### operations/clipboard

- Cut, then navigate away, switch mode, restart Strata, and paste in a second window; cut styling must clear on completion and on cancel.
- Paste with the pointer parked over a different column than the keyboard cursor; the destination footer names the folder that receives the files.
- Copy a file, delete or hide the current folder from a shell, press Alt+Up in Icons and List, then Ctrl+V.
- Copy name and Copy path for a multi-selection with non-UTF-8 and space-containing names; paste into a terminal and compare bytes.
- Copy the path of a non-UTF-8 name, and of a folder whose name holds a newline, from the location-bar crumb and from Properties; paste into zsh, fish, and dash.
- Cut one file in a large Columns folder, scroll it out of view and back, then copy 1,000 files and scroll again.
- Start a foreground Move to…, cancel it, then fail one, and run Extract here after each.
- Paste an image copied from a browser, and paste into a read-only folder.
- Move to… and Copy to…: reach the destination through the dialog's search, pick Trash, pick a remote location, and pick the source folder itself.
- On the ntfs-3g mount, copy a folder and cancel the moment the progress bar fills; list the destination's parent with `ls -la`.

### operations/clipboard/conflicts

- Paste a folder over a folder, a file over a folder, and a folder over a file; take each choice with Apply to all, then cancel midway through a batch of 20.
- Keep both twice on the same source and read the suffix sequence.
- On vfat, paste `a:b` where `a_b` exists, then where both `a_b` and `A_B` exist; answer Keep Both on a cut-paste and undo.
- Replace and Merge on tmpfs, where Trash is unavailable; cancel midway, then list hidden `.strata-originals-*` and `.strata-merge-*` names.
- Merge without Trash on NFS while another program holds one replaced file open; then cancel a second such merge.
- After a Merge, edit one placed file, only `touch` another, then undo.

### operations/clipboard/send-to

- Send to a mounted USB stick, an unmounted one, and a full one; open the menu with no removable device attached.
- With a provider destination and no drive, open Send to…, plug a drive in, then let the provider withdraw its destination.

### operations/drag-and-drop

- Drop onto the source folder, onto a descendant of the dragged folder, onto a read-only place, onto the sidebar Trash row, onto a tab header, and onto another window.
- Hover a folder until it spring-loads, move away before it opens, then let it open and press Escape mid-drag.
- Start a drag in Icons from caption whitespace and from tile content, and in List from an unselected row.
- Start a multi-selection drag in the large fixture folder in List, Icons, and Columns, and hover several folders before dropping.

### operations/drag-and-drop/column-autoscroll

- Drag to the right edge of a column strip wider than the window; autoscroll must stop when the pointer leaves the edge and when Escape cancels the drag.

### operations/drag-and-drop/copy-or-move

- Drop from `/dev/shm` to home and back under each preference value; cancel the ask dialog and check the source is untouched.
- Drop between two folders on a bind-mounted path to see which device the detection reports.
- Drag a selection from a folder with a mount point directly inside, the mount-point folder included, onto another device. Mount or unmount a device while hovering.
- Answer the Always Ask dialog by keyboard in List and Icons.

### operations/filesystem-compatibility

- Build a folder holding `10:00`, `notes.`, `CON`, `aux.c`, `report?.txt`, a non-UTF-8 `caf\xe9.txt`, a symlink to `10:00` and a dangling symlink. Copy, move, undo and redo it onto every lab mount and a real stick, then extract it as a tar.
- Move a folder across disks while one shell loop appends to a file in it. Repeat while another loop renames a sibling into it.
- Move hard-linked files off an SMB share right after writing them, and off FAT within 2 s of saving them.
- Move a folder holding two hard-linked names from a real SMB share and from a vfat stick. Rewrite the later name, at the same size, within 1 s of starting.
- Copy a folder holding hard links, a FIFO, a socket, and a device node into a setgid folder.
- Copy a `0555` subfolder with `user.*` xattrs and a 1 GiB sparse file the same way.
- Pull the real stick during a copy and during a move's final flush; then list hidden `.strata-copy-*` entries on both sides.
- Pause `sftp-server` with `kill -STOP` during a move onto sshfs, resume after 30 s, and compare both sides.
- Paste onto a stick reached through two nested symlinks, and onto a bind mount of it.
- Move 300 files to a rotational USB disk and to an SSD; watch for "Writing to device…" and count files on arrival.
- Produce every report section in one transfer, in a narrow window, while a Send to notice is visible.
- On an SMB share, look up a folder under a second spelling so the client drops `serverino`. Then move a folder off the share and Replace a file on it.
- On a vfat stick, Replace a file after a remount between the prompt and the copy, so the kernel renumbers its entries.

### operations/filesystem-compatibility/open-files

- Hold a file below a folder on NFS, SMB, and sshfs, and unlink it from a shell. Then Delete, Move to another disk, and Move to Trash the folder.
- Repeat with each holder from Setup, and with the holder owned by another user.
- Delete 50 held folders at once and time the wait.
- On SMB without and with POSIX extensions, rename and move a folder while a file below it is open in another program.
- Play a video in the preview and move its folder to another disk from a second window, on NFS and on a local disk.
- Start a Delete while a thumbnail of a large image in that folder is still loading.

### operations/filesystem-compatibility/leftovers

- Make each kind by hand: `.strata-originals-<uuid>/`, `.strata-merge-<uuid>/`, `.strata-copy-<uuid>`, `.strata-extraction-<uuid>`, an older `.strata-replaced-<uuid>`, `.strata-replacement-ab12Cd`, and `.strata-copy-notes`. Open the folder in Columns, List, Icons, the portal chooser, and a peek.
- Restore an originals folder whose names are taken by a file, a folder, and a symlink; restore a merge folder whose subfolders were deleted.
- Open the review, remove one item from a shell, then press Restore and Delete… on it.
- Close the folder before pressing Review on the card; reopen the same folder in a second window in the same session.
- Kill Strata with `kill -9` during a Replace on sshfs and on NFS, then open the folder.
- Open an `sftp://` folder holding leftovers.
- Unplug an ntfs3 stick during a Replace without Trash, then plug it in with udisks' default options and open the folder.
- Mount a vfat stick last written in a time zone to the west that holds a fresh `.strata-probe-*`.

### operations/trash

- Trash from a Ctrl+F result, from a multi-column selection, from a second window viewing the same folder, and look for it in the file chooser, where it must not be offered.
- Drop a `/dev/shm` selection on the sidebar Trash row.
- Delete a recursive Ctrl+F result selection mixing `/dev/shm` and home items.
- Delete in a read-only tmpfs mount.
- Open and Delete in folders whose first listed entry is a dangling symlink, or a symlink into a stalled or unmounted network mount.
- Dismiss each no-Trash dialog by Escape and by backdrop click, then confirm the payload still exists on disk.
- Under `gvfsd`, re-trash a restored non-UTF-8 name and delete it permanently from Trash.
- Trash the folder open in another window and watch how that window recovers.
- Watch for GTK criticals while the Trash pane refreshes during an open Restore or Empty dialog.
- Drop a link to a folder on a stalled or unmounted network mount onto the sidebar Trash row.
- On sshfs without `default_permissions` and on rclone, Delete a file, a read-only file, and a selection spanning both mounts. List the mount roots with `ls -la`.
- After a refusal, open the same folder in a second window and in the file chooser, then reload each way: F5, the pane refresh button, the folder menu, chooser F5.
- Kill the sshfs process mid-delete, then Delete again; remount and Delete again.

### operations/trash/restore

- Walk the Manual acceptance list in `docs/trash-restore-testing.md`.
- Restore a non-UTF-8 name under `gvfsd` into a folder holding a similar UTF-8 name; compare bytes with `ls --quoting-style=escape`.
- Restore after the original directory was renamed, deleted, replaced by a file, or replaced by a symlink pointing elsewhere.
- Restore a mixed selection where one original lives on an unmounted volume.
- Restore 200 items at once and cancel midway.
- Restore on the ntfs-3g and sshfs mounts, and from an exFAT stick's Trash into a folder on another disk, cancelling one copy midway.
- On vfat and ext4, Delete `notes.txt`, then create and trash another `notes.txt` from a shell within the same second, and press Ctrl+Z.
- With `GIO_USE_VFS=local`, undo a Replace on a USB stick whose `.Trash-$uid` is a symlink, then one owned by another user.

### operations/trash/empty

- Empty with Trash open in a second window, with a Restore dialog open, and while contents are still being measured; cancel at each stage.
- Empty a Trash holding a non-UTF-8 name and a 10k-entry folder.

### operations/trash/animation

- Trash with reduce motion on and off, with the sidebar hidden, and with the Trash row scrolled out of view; the animation must never delay the operation or move focus.
- Move to Trash 15 items, then a folder that takes about 350 ms; switch tabs during a quick one.

### operations/delete

- Shift+Delete with no selection in each mode, inside a read-only folder, and on a selection mixing Trash and non-Trash items reached through search.
- In the confirmation: Escape, backdrop click, Enter, and Tab order, both after Shift+Delete and after Delete in `/dev/shm`.
- Delete a 10k-entry folder, cancel at about half, and count what remains.
- Shift+Delete 15 items, then a folder that takes about 350 ms; switch tabs or view mode during a quick one.
- Shift+Delete 1 to 15 rows above other rows in each mode and watch whether deleted rows vanish and reappear before the dissolve.
- Start a second Shift+Delete while the first dissolve plays, then click a row.
- Shift+Delete a mixed selection of a folder link, a file link, a dangling link, and a socket; repeat with Delete in `/dev/shm`.
- Shift+Delete on NFS, SMB, sshfs, virtiofs or 9p, a `fuseblk` drive, and a mergerfs pool; read each title and subtitle.
- Shift+Delete through a symlink alias into an NFS folder.

### operations/archives

- Compress a selection with hidden files, a symlink, a non-UTF-8 name, and an empty folder in each format; list the result with `unzip -l`, `7z l`, and `tar tvf` and compare entries, modes, and mtimes.
- Extract each format into an empty folder, a folder with a same-named entry, and a read-only folder; the destination must be clean after each refusal.
- Feed the hostile archives: `../` member, absolute path, symlink out, size-lying header.
- Extract a TAR whose first directory entry is `.\`, and a RAR whose first entry is `.\` or `./`. Build the `.\` TAR with a script, since `tar` writes only `./`.
- Extract a password-protected ZIP that holds a `./` directory marker, through the password prompt.
- Fill the small tmpfs and extract into it; compare ZIP, 7Z, and TAR behavior at the boundary.
- Cancel a large extraction at about a third and compare cleanup with `docs/archives.md`.
- Enter a wrong password three times, then the right one, on `content-encrypted.7z`.
- Close the Compress dialog with its X, then press Down.
- Close the conflict prompt opened from a Ctrl+F result, then press Down.
- Cancel the Extract password dialog with Escape after Extract to…, then press Down.
- Extract to… a folder that is deleted or unmounted during extraction, close the error, then extract another archive in List and Columns.
- Extract a multi-root archive, a single-root archive whose name is taken, and a third archive cancelled midway; press Ctrl+Z three times, then Ctrl+Shift+Z once.
- Extract by Enter in List and after a password retry, then press Ctrl+Z from a second window.
- On the ntfs-3g mount, take `name` with a file and `name (2)` with a folder, then extract a single-root folder archive named `name`.
- On local disk and on the ntfs-3g mount, extract a single-root archive whose root is a symlink to a folder, named `v1.2`, where that name is taken.
- On the ntfs-3g mount, extract into a folder reached through a symlink.
- On the ntfs-3g mount, extract an archive holding a nested `0555` folder and a symlink member.
- On the ntfs-3g mount, extract a large ZIP built with `zip -D`, so it lists no folder entries. Mid-extraction, chmod one of its nested staging folders to `0000`.
- After that run, list the destination with hidden files shown.
- Extract into a sshfs folder and onto a vfat stick an archive holding `10:00/` and `10_00/`, a symlink, a hard link to it, and `c:notes`.
- On tmpfs, compress with Replace over an existing archive, cancel once, then let it finish and press Ctrl+Z.
- On SMB without server inode numbers, cancel a Compress just as it publishes, then list `.strata-copy-*` names.
- Extract into a folder open in a second window that has no monitor, such as an SFTP folder.
- Compress in Columns into the active child column, a parent column, and a column four levels deep.

### operations/archives/rar

- Extract a RAR with a symlink member, then repeat with `rar` removed from PATH and read the error.

### operations/archives/preview

- Open a 50k-member archive, a password-protected one, and an archive inside an archive; drive the listing with the keyboard only.
- Mix pointer and keys: hover across rows then press Right, and click a row then press Up.
- Shift+click two members, and double-click a folder in a long list scrolled halfway.
- Click a row at its bottom edge.
- With the preview open, hold Down through a mix of plain and password-protected archives in each view and with each key map; then press Right in Icons on a locked archive.
- Type a wrong password, then move the cursor away and back to the archive.

### operations/progress

- Copy the large tree and cancel at once, cancel near the end, and let one run finish; compare partial output with what the dialog claimed.
- Press Escape on the progress dialog mid-operation; the operation must keep running and stay reachable from the dock.
- Move the focused large tree to another folder, then press Down once the progress dialog closes.
- Repeat with a move that ends in an error dialog.
- Cancel a 300-file cross-disk move, a Trash delete, and a restore partway; compare the not-attempted count with what is on disk.

### operations/progress/dock

- Run three operations at once from two windows, cancel one from the other window, and eject a device mid-copy.
- Read the footer of a cancelled compression and of a drive format card.
- Cancel a slow deletion on a stalled device with X, then click rows and navigate with the pointer while cancellation is pending.
- Show a Send to success notice and a file provider notice while a copy card runs, and in quick succession with no card.
- Let a notice expire while a card runs, after the card completes, and after the card is pinned; click where the notice sits.
- Trigger a notice with a long device or provider name in a narrow window.
- Press Ctrl++ repeatedly while a transfer report notice shows, then finish two docked copies that both rename items.

### operations/progress/jobs

- Queue five custom-action invocations on a 100-item selection, cancel from the dashboard, then restart Strata with jobs pending.

### operations/undo

- Perform ten mixed operations (create, rename, paste, trash, compress, extract), undo all, redo all; the tree must match snapshots taken before and after.
- Change an operation's target from a shell, then undo it; expect a clear failure and an intact history.
- Press Ctrl+Z in a second window and in the file chooser.
- Move the folder built for `operations/filesystem-compatibility` onto vfat, rename one fixed name on the stick, then undo and redo.
- Move a dangling symlink and a link into a stopped sshfs mount, then undo.

## Hand-offs

- Pointer gestures before a drag starts, marquee, and click modes → `browser`.
- The sidebar Trash row as a navigation target → `browser`.
- Modal dialog shell: blur, Escape, backdrop, focus return → `app`.
- Rendering of archive members and documents inside the preview panel → `preview`.
- Preview playback stopping, the sandbox wait, and the preview following a renamed item during an operation → `preview`.
- Thumbnails asked for again after an operation stopped them → `browser`.
- Releasing reads under a mount root before an unmount → `devices`.
- Mounting, unmounting, and ejecting the devices Send to lists → `devices`.
- Provider destinations inside Send to… and their protocol → `remote`.
- Folder reloads and monitor events after an operation ends → `browser`.
- 10xer-mode key variants of these operations → `integration`.
