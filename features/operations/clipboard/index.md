---
title: Copy, cut, and paste
status: shipped
origin: {issue: lgse/strata#287, pr: lgse/strata#289}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [src/ui/browser/clipboard.rs, src/ui/browser/transfer.rs]
tests: [src/ui/browser/clipboard/tests.rs, src/ui/browser/transfer/tests.rs, src/adapters/local_operations/tests/copy.rs, src/adapters/local_operations/tests/moves.rs, src/adapters/local_operations/tests/naming.rs, src/adapters/local_operations/tests/paste_results.rs, tests/e2e/scenarios/test_clipboard.py]
docs: [docs/keyboard-navigation.md]
related: [operations/drag-and-drop, operations/progress, operations/trash, integration/10xer-mode]
---

## Summary

Copying and cutting files to the system clipboard, pasting them as copies or moves, Duplicate, Move to… and Copy to…, and the copy engine behind them. It also covers copying paths, names, and pasted images. The footer's Files on clipboard badge belongs to `app/shortcut-reference`. Children: `operations/clipboard/conflicts` (the "File already exists" dialog and its choices) and `operations/clipboard/send-to` (Send to removable devices).

## Behavior

### Copy and cut

- Ctrl+C or the item menu's Copy puts the selection on the clipboard as a file list; pasting copies it and leaves the sources in place. lgse/strata#289
- Ctrl+X or the item menu's Cut leaves the selection in place until a paste moves it. lgse/strata#289
- Cut items show a scissors icon in place of their icon or thumbnail and are drawn at 65% opacity, in Columns, Icons, and List. lgse/strata#927, lgse/strata#1018
- Copied items show a copy icon in place of their icon or thumbnail; scissors wins when both apply. lgse/strata#1306
- A cut in one Strata window pastes as a move in another window. lgse/strata#289
- A cut still pastes as a move when the clipboard returns the file as a `file://` URI instead of a native path. lgse/strata#289
- When another application takes the clipboard, copy and cut marks clear in every window. lgse/strata#1306
- With a Ctrl+F filter open, Ctrl+C and Ctrl+X act on the selected results, and cut results show scissors in every window. lgse/strata#1018
- In Columns, Ctrl+C or Ctrl+X with nothing selected in the focused column acts on the folder that column shows. lgse/strata#1092
- With the caret in a text widget, such as preview text, Ctrl+C, Ctrl+X, Ctrl+V, Ctrl+D, and Ctrl+A act on the text. lgse/strata#670

### Paste destination

- Ctrl+V with exactly one folder explicitly selected pastes into that folder. lgse/strata#454
- With a file, several items, or nothing selected, Ctrl+V pastes into the destination column. lgse/strata#454
- The destination column follows the last pointer or keyboard navigation; pressing Ctrl+V does not change it. lgse/strata#358
- After going to a parent folder in Icons or List, Ctrl+V pastes into the parent, not its auto-selected first folder. lgse/strata#485
- Ctrl+V while viewing Recent does nothing. lgse/strata#1083
- After a paste, the destination is shown with the pasted items selected; a pasted-into folder in Columns opens and keeps focus. lgse/strata#524
- Completing a cut-paste removes the moved items from the clipboard; text copied after the cut stays on the clipboard. lgse/strata#1265
- Completing a drag move or Move to… leaves unrelated clipboard contents, such as copied text, intact. lgse/strata#1265

### Same-folder copies and Duplicate

- Pasting a copied file into its own folder creates `name (1).ext`, then `name (2).ext`, with no dialog. lgse/strata#272, lgse/strata#708
- Pasting `document (1).txt` into its own folder creates `document (2).txt`; a folder becomes `folder (1)`. lgse/strata#272
- Cut and paste into the same folder does nothing. lgse/strata#272
- Ctrl+D or the item menu's Duplicate copies each selected item into its own folder with a numbered name and leaves the clipboard unchanged. lgse/strata#272, lgse/strata#945
- Ctrl+D does nothing when the selected items are in different folders or in Trash. lgse/strata#272 (unverified)

### Paths, names, and images

- Outside 10xer mode, `y` or Copy path copies the shell-escaped native path; folders get a trailing `/`, and URIs are copied unescaped. lgse/strata#230, lgse/strata#1306
- With several items selected, Copy paths copies one path per line. lgse/strata#230 (unverified)
- Copy name and Copy names copy the display names, one per line. lgse/strata#704
- Pasting while the clipboard holds an image and no files writes `image.png`, then `image (1).png`, into a local destination. lgse/strata#882
- The folder menu's Paste is sensitive only while the clipboard holds files or a PNG image. lgse/strata#882

### Move to and Copy to

- Move to… and Copy to… in the item menu open a floating folder chooser titled "Move to" or "Copy to" over the originating window. lgse/strata#1384
- The chooser starts in the current folder when it is local, otherwise in Home. lgse/strata#1384 (unverified)
- New Folder in the chooser creates a destination; "Move here" or "Copy here", or Ctrl+Enter from the file list, confirms. lgse/strata#1384
- Cancelling the chooser or closing its parent window leaves the files and the parent's location unchanged. lgse/strata#1384
- A window opens at most one chooser at a time. lgse/strata#1384
- After confirming, the window navigates to the destination and selects the transferred items. lgse/strata#125, lgse/strata#1384

### Undo

- Ctrl+Z after a cut-paste or Move to… returns the moved items to their original folders. lgse/strata#301
- Ctrl+Z after a copy sends only the items that copy created to Trash, including numbered and replaced destinations. lgse/strata#444
- After a copy is undone, the next Ctrl+Z undoes the operation before it. lgse/strata#444

### Copy and move safety

- Moving a non-empty folder to another filesystem copies it, then deletes the source only after the copy succeeds. lgse/strata#215
- A symlink inside a copied folder is recreated as a symlink pointing at the same target, not followed. lgse/strata#254
- Copying a folder that contains a FIFO or other special file fails promptly with an error naming that entry. lgse/strata#707
- On FAT, vfat, and exFAT destinations, `" * / : < > ? \ |` and control characters become `_`, and trailing dots and spaces are trimmed. lgse/strata#1126
- Names that collide after that sanitizing get a numbered suffix instead of overwriting each other. lgse/strata#1126
- Copying a file of 4 GiB or larger to a FAT32 drive fails before copying, with a message suggesting exFAT. lgse/strata#1278
- Copies onto NTFS through ntfs-3g and other FUSE mounts without `RENAME_NOREPLACE` complete without an "Invalid argument" error. lgse/strata#1515
- Copying or moving an item out of Trash that came from another drive creates it under its own leaf name. lgse/strata#1524
- Moving a folder into itself or a descendant, including through a symlink alias, does nothing and leaves the source untouched. lgse/strata#1537

## Design

The GDK clipboard carries only a file list with no cut marker. Strata keeps process-wide copy and cut lists, shared by every window, as the source of truth (lgse/strata#289).

- Cut matching also accepts GIO equality, because a clipboard round trip can return an equivalent URI instead of the stored path (lgse/strata#287).
- Strata rewrites or clears the system clipboard only while it still owns the file list it set (lgse/strata#1265).
- Pasting into a single selected folder deliberately diverges from Nautilus, Thunar, and Finder (lgse/strata#449). An auto-selection made on load counts as a cursor, not a choice (lgse/strata#483).
- Same-folder copies use the language-neutral `(n)` suffix. A same-folder cut stays a no-op to prevent accidental renames (lgse/strata#270, lgse/strata#272).
- Duplicate exists so an in-place copy does not overwrite the user's clipboard (lgse/strata#271).
- Undo is one process-wide history of 32 entries. Copy undo trashes rather than deletes, so Ctrl+Z never destroys data (lgse/strata#444).
- Local copies open each source directory through `openat2` and re-read every entry's type before acting (lgse/strata#254). Local moves use one confined `renameat2` with `NOREPLACE` (lgse/strata#365).
- A move the kernel cannot rename falls back to a staged copy, and the source is deleted only after it succeeds (lgse/strata#215).
- FAT names are sanitized like GNOME Files does, rather than failing and discarding the whole staged copy (lgse/strata#1123).
- Move to and Copy to reuse Strata's full chooser in a floating window instead of a separate destination picker (lgse/strata#1377, lgse/strata#1383).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-09 | lgse/strata#1537 | fix | Rejected self-nesting moves that reach the source through a symlink alias. |
| 2026-10-08 | lgse/strata#1524 | fix | Used the leaf name for items transferred out of another drive's Trash. |
| 2026-10-07 | lgse/strata#1515 | fix | Fell back to exclusive-create copies where `RENAME_NOREPLACE` is unsupported, such as ntfs-3g. |
| 2026-09-24 | lgse/strata#1265 | fix | Kept the clipboard after unrelated moves by rewriting it only when a tracked cut was consumed. |
| 2026-09-19 | lgse/strata#1126 | fix | Sanitized FAT-invalid names instead of discarding the whole staged copy. |
| 2026-09-13 | lgse/strata#927 | feat | Marked cut items with a scissors icon instead of reduced opacity. |
| 2026-09-13 | lgse/strata#945 | feat | Added Duplicate to the item menus. |
| 2026-09-12 | lgse/strata#882 | feat | Pasted clipboard images as PNG files. |
| 2026-09-09 | lgse/strata#707 | fix | Failed fast on special files instead of blocking the copy worker. |
| 2026-09-09 | lgse/strata#704 | feat | Added Copy name and Copy names to the item menus. |
| 2026-09-07 | lgse/strata#524 | fix | Kept focus on the destination column after a cut-paste. |
| 2026-09-07 | lgse/strata#485 | fix | Pasted into the current folder after going up, ignoring the auto-selected folder. |
| 2026-09-06 | lgse/strata#444 | fix | Made copies undoable and kept a bounded undo history. |
| 2026-09-06 | lgse/strata#454 | fix | Pasted into a single selected folder. |
| 2026-09-05 | lgse/strata#365 | fix | Moved local items with one confined `renameat2` against symlink races. |
| 2026-09-04 | lgse/strata#301 | feat | Added Ctrl+Z undo for completed moves. |
| 2026-09-04 | lgse/strata#255 | fix | Re-read entry types during replace and move cleanup instead of trusting earlier checks. |
| 2026-09-04 | lgse/strata#289 | fix | Shared cut intent across windows and matched equivalent clipboard locations. |
| 2026-09-04 | lgse/strata#254 | fix | Copied local trees through verified descriptors so symlinks are never followed. |
| 2026-09-04 | lgse/strata#272 | feat | Allowed same-folder copies with numbered names and added Ctrl+D. |
| 2026-09-04 | lgse/strata#215 | fix | Moved folders across filesystems through a staged copy. |
| 2026-09-03 | lgse/strata#230 | fix | Bound `y` to Copy path and shell-escaped copied paths. |
| 2026-09-01 | lgse/strata#125 | feat | Searched destination folders by name in Copy to and Move to. |

## Known gaps

- Cut intent is not exchanged through `x-special/gnome-copied-files`, so cuts between Strata and other file managers paste as copies. lgse/strata#289
- On NFS, same-share moves fall back to copy and delete, and replacing where Trash is unsupported may still fail. lgse/strata#1530
