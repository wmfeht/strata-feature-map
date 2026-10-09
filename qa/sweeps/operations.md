---
title: Operations sweep
reviewed_at: aee71335dfecd059b9af23efeac2ed52c43e3b19
triggers: [src/services/operations.rs, src/services/operations/**, src/services/file_source.rs]
tools: [docs/trash-restore-testing.md, docs/archives.md, scripts/generate-fixture.sh, scripts/e2e-mutation-check.sh, tests/e2e/fixtures/content-encrypted.7z, tests/e2e/mutations]
---

## Scope

Everything that changes files on disk from the browser: New Folder and New File, inline rename, copy, cut, and paste with their name conflicts, Move to and Copy to, Send to, drag and drop with its copy-or-move policy and column autoscroll, Trash with restore, Empty Trash and the flight animation, permanent deletion, archives with RAR and archive preview, operation progress with the dock and the job queue, and undo and redo across all of them.

Left to other sweeps: pointer gestures and selection before a drag starts, the sidebar Trash row as a place to navigate to, the modal dialog shell, rendering of archive members in the preview panel, the devices Send to lists, and the 10xer-mode key variants.

## Setup

- A fixture tree with mixed names: Unicode, a non-UTF-8 name made with `printf 'bad\xff.txt'`, a 255-byte name, two names differing only by case, dot-prefixed files, a symlink, a read-only folder (`chmod 555`), and an empty folder.
- A second filesystem. `/dev/shm` serves cross-volume drops, Trash-unsupported paths, and copy-or-move prompts. Free-space refusals need a small tmpfs (`mount -t tmpfs -o size=8m`); skip those probes and say so when no mount is available.
- A large tree from `scripts/generate-fixture.sh` for progress, cancellation, and Empty Trash measuring.
- Archives built with system tools in ZIP, 7Z, TAR, and TAR.GZ; `tests/e2e/fixtures/content-encrypted.7z` for passwords; hostile archives under `/tmp` with a `../` member, an absolute-path member, a symlink member pointing outside, and a header that lies about its size. RAR needs `rar` on PATH or a sample from `tests/fixtures/rar/`.
- Two windows of the same build for cross-window paste, undo, and progress dock checks.
- A desktop session running `gvfsd` for `trash:///` listings. The E2E container sets `GIO_USE_VFS=local` and cannot browse Trash.
- Verify every operation on disk with `ls -la`, `stat`, and `cmp`, never in the listing alone. Watch the log for GTK criticals during dialogs and animations.
- `tests/e2e/mutations/` holds deliberate defects the suite must catch; `./scripts/e2e-mutation-check.sh drag-and-drop` or `rename-caret` is evidence when those areas changed.

## Probes

- Run each operation in Columns, Icons, and List, from the item menu, the keyboard, and the background menu where offered; the result on disk must be the same.
- Repeat a destructive operation on a directory removed underneath Strata (`rm -rf` from a shell while the dialog is open).
- After each operation, press Ctrl+Z then Ctrl+Shift+Z and diff the tree against a `find -printf '%p %s %T@\n'` snapshot taken before.

### operations/create

- Create inside an empty folder, a read-only folder, Trash, a Ctrl+F result, and in a Columns pane that is not the last column; note which column the editor opens in.
- Create with a 255-byte name, a name ending in a space, and `.hidden` with hidden files off.
- Press Ctrl+Shift+N ten times quickly while earlier items are still in their editors; the `(n)` suffixes must stay unique.

### operations/rename

- Commit by Enter, by clicking another item, by clicking the background, by focusing a second window, and press F5 while editing.
- Rename to a name differing only by case, to an existing name, to a name containing `/`, and to a 255-byte name, in each mode.
- Rename an item at the edge of the viewport, in a column narrower than the name, and while a filter is active.
- Rename an image while its thumbnail is still loading; the thumbnail must follow the new name.

### operations/clipboard

- Cut, then navigate away, switch mode, restart Strata, and paste in a second window; cut styling must clear on completion and on cancel.
- Paste with the pointer parked over a different column than the keyboard cursor; the destination footer names the folder that receives the files.
- Copy name and Copy path for a multi-selection with non-UTF-8 and space-containing names; paste into a terminal and compare bytes.
- Paste an image copied from a browser, and paste into a read-only folder.
- Move to… and Copy to…: reach the destination through the dialog's search, pick Trash, pick a remote location, and pick the source folder itself.

### operations/clipboard/conflicts

- Paste a folder over a folder, a file over a folder, and a folder over a file; take each choice with Apply to all, then cancel midway through a batch of 20.
- Keep both twice on the same source and read the suffix sequence.

### operations/clipboard/send-to

- Send to a mounted USB stick, an unmounted one, and a full one; open the menu with no removable device attached.

### operations/drag-and-drop

- Drop onto the source folder, onto a descendant of the dragged folder, onto a read-only place, onto the sidebar Trash row, onto a tab header, and onto another window.
- Hover a folder until it spring-loads, move away before it opens, then let it open and press Escape mid-drag.
- Start a drag in Icons from caption whitespace and from tile content, and in List from an unselected row.

### operations/drag-and-drop/column-autoscroll

- Drag to the right edge of a column strip wider than the window; autoscroll must stop when the pointer leaves the edge and when Escape cancels the drag.

### operations/drag-and-drop/copy-or-move

- Drop from `/dev/shm` to home and back under each preference value; cancel the ask dialog and check the source is untouched.
- Drop between two folders on a bind-mounted path to see which device the detection reports.

### operations/trash

- Trash from a Ctrl+F result, from a multi-column selection, from a second window viewing the same folder, and look for it in the file chooser, where it must not be offered.
- Delete from `/dev/shm` by a drop on the sidebar Trash row, and from a Ctrl+K selection mixing `/dev/shm` and home items whose folders are not open.
- Delete in a folder whose first listed entry is a symlink into `/dev/shm`, and in a read-only tmpfs mount.
- Dismiss each no-Trash dialog by Enter, Escape, and backdrop click, then confirm the payload still exists on disk.
- Restore, re-trash, and permanently delete a non-UTF-8 name from Trash under `gvfsd`; compare name bytes with `ls --quoting-style=escape`.
- Trash the folder open in another window and watch how that window recovers.
- Watch for GTK criticals while the Trash pane refreshes during an open Restore or Empty dialog.

### operations/trash/restore

- Walk the Manual acceptance list in `docs/trash-restore-testing.md`.
- Restore after the original directory was renamed, deleted, replaced by a file, or replaced by a symlink pointing elsewhere.
- Restore a mixed selection where one original lives on an unmounted volume.
- Restore 200 items at once and cancel midway.

### operations/trash/empty

- Empty with Trash open in a second window, with a Restore dialog open, and while contents are still being measured; cancel at each stage.
- Empty a Trash holding a non-UTF-8 name and a 10k-entry folder.

### operations/trash/animation

- Trash with reduce motion on and off, with the sidebar hidden, and with the Trash row scrolled out of view; the animation must never delay the operation or move focus.

### operations/delete

- Shift+Delete with no selection in each mode, inside a read-only folder, and on a selection mixing Trash and non-Trash items reached through search.
- In the confirmation: Escape, backdrop click, Enter, and Tab order, both after Shift+Delete and after Delete in `/dev/shm`.
- Delete a 10k-entry folder, cancel at about half, and count what remains.

### operations/archives

- Compress a selection with hidden files, a symlink, a non-UTF-8 name, and an empty folder in each format; list the result with `unzip -l`, `7z l`, and `tar tvf` and compare entries, modes, and mtimes.
- Extract each format into an empty folder, a folder with a same-named entry, and a read-only folder; the destination must be clean after each refusal.
- Feed the hostile archives: `../` member, absolute path, symlink out, size-lying header.
- Fill the small tmpfs and extract into it; compare ZIP, 7Z, and TAR behavior at the boundary.
- Cancel a large extraction at about a third and compare cleanup with `docs/archives.md`.
- Enter a wrong password three times, then the right one, on `content-encrypted.7z`.
- Close the Compress dialog with its X, and the conflict prompt opened from a Ctrl+F result, then press Down; the cursor must move in the listing.
- Cancel the Extract password dialog with Escape after Extract to…, then press Down.

### operations/archives/rar

- Extract a RAR with a symlink member, then repeat with `rar` removed from PATH and read the error.

### operations/archives/preview

- Open a 50k-member archive, a password-protected one, and an archive inside an archive; drive the listing with the keyboard only.

### operations/progress

- Copy the large tree and cancel at once, cancel near the end, and let one run finish; compare partial output with what the dialog claimed.
- Press Escape on the progress dialog mid-operation; the operation must keep running and stay reachable from the dock.
- Move the focused large tree to another folder, press Down once the progress dialog closes, then repeat with a move that ends in an error dialog.

### operations/progress/dock

- Run three operations at once from two windows, cancel one from the other window, and eject a device mid-copy.

### operations/progress/jobs

- Queue five custom-action invocations on a 100-item selection, cancel from the dashboard, then restart Strata with jobs pending.

### operations/undo

- Perform ten mixed operations (create, rename, paste, trash, compress), undo all, redo all; the tree must match snapshots taken before and after.
- Change an operation's target from a shell, then undo it; expect a clear failure and an intact history.
- Press Ctrl+Z in a second window and in the file chooser.

## Hand-offs

- Pointer gestures before a drag starts, marquee, and click modes → `browser`.
- The sidebar Trash row as a navigation target → `browser`.
- Modal dialog shell: blur, Escape, backdrop, focus return → `app`.
- Rendering of archive members and documents inside the preview panel → `preview`.
- Mounting, unmounting, and ejecting the devices Send to lists → `devices`.
- 10xer-mode key variants of these operations → `integration`.
