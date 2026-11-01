---
title: Copy, cut, and paste
status: shipped
origin: {issue: lgse/strata#287, pr: lgse/strata#289}
branch: null
reviewed_at: 44bfeab305cfb68993bafcf4794fe0bbf7ff1433
review: reviewed
code: [src/ui/browser/clipboard.rs, src/ui/browser/transfer.rs, src/adapters/local_operations/transfer_targets.rs]
tests: [src/ui/browser/clipboard/tests.rs, src/ui/browser/transfer/tests.rs, src/adapters/local_operations/tests/copy.rs, src/adapters/local_operations/tests/moves.rs, src/adapters/local_operations/tests/naming.rs, src/adapters/local_operations/tests/paste_results.rs, tests/qa/scenarios/clipboard, tests/qa/mutations/clipboard.patch, tests/qa/mutations/cut.patch, tests/qa/scenarios/dialogs_and_menus/floating-chooser-transfers-files.jsonl, tests/qa/scenarios/cross_volume_drop/cross-volume-enter-choice.jsonl]
docs: [site/src/reference/keyboard-navigation.md]
related: [operations/drag-and-drop, operations/progress, operations/trash, integration/10xer-mode, operations/filesystem-compatibility]
---

## Summary

Copying and cutting files to the system clipboard, pasting them as copies or moves, Duplicate, Move to… and Copy to…. The copy engine, placement, and name rules behind them belong to `operations/filesystem-compatibility`. It also covers copying paths, names, and pasted images, and the cross-device "Copy or move?" drop prompt. The footer's Files on clipboard badge belongs to `app/shortcut-reference`. Children: `operations/clipboard/conflicts` (the "File already exists" dialog and its choices) and `operations/clipboard/send-to` (Send to removable devices).

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
- After going to a parent folder, Ctrl+V pastes into the parent, not into the folder selected on arrival, restored or first. lgse/strata#485, lgse/strata#1436, lgse/strata#1544
- Ctrl+V while viewing Recent does nothing. lgse/strata#1083
- A paste whose destination is slow to answer shows "Preparing items…" with Cancel and no count. lgse/strata#1615
- A copy shows it in its docked row, and a move in a dialog. lgse/strata#1615
- Cancel there abandons the paste with no prompt, and closing the view dismisses the row and copies nothing. lgse/strata#1615
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
- Copy path on a local name with non-UTF-8 bytes, such as `bad\xff.txt`, copies `/path/to/$'bad\xff.txt'`, which bash resolves to the file. lgse/strata#1626
- In a path that is not valid UTF-8, only the `/`-separated components that are not valid UTF-8 or contain a newline are `$'...'`-quoted; others keep backslash escaping. lgse/strata#1626 (unverified)
- Inside `$'...'`, valid UTF-8 characters stay literal, `'` and `\` get a backslash, and each byte of a control character becomes `\xHH`. lgse/strata#1626 (unverified)
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
- In Send to… → Choose folder…, the chooser still lists links leading off the device; confirming one shows "Choose an existing folder inside this removable device." lgse/strata#1729
- After confirming, the window navigates to the destination and selects the transferred items. lgse/strata#125, lgse/strata#1384
- Cancelling a running foreground Move to… from its progress card, then running Extract here, keeps the window in the current folder. lgse/strata#1605

### Cross-device drop prompt

- A plain drop onto another device under Always ask (`operations/drag-and-drop/copy-or-move`) opens "Copy or move?" naming the item count and destination, with Copy focused. lgse/strata#502
- The prompt states "The destination is on a different device.", or "Strata could not determine whether the destination is on the same device." when the lookup did not resolve. lgse/strata#502
- Enter activates the focused Copy, Move, or Cancel button. lgse/strata#502
- Cancel, Escape, the close button, or a click outside the prompt transfers nothing and leaves the source in place. lgse/strata#502
- Copy keeps the source; Move removes it after the transfer. lgse/strata#502
- Closing the prompt returns keyboard focus to the dragged item, in Columns, List, and Icons. This holds for Copy, Cancel, Escape, its close button, and a click outside. lgse/strata#1900
- Up or Left then moves the cursor from the dragged item. lgse/strata#1900

### Undo

- Ctrl+Z after a cut-paste or Move to… returns the moved items to their original folders. lgse/strata#301
- Ctrl+Z after a copy sends only the items that copy created to Trash, including numbered and replaced destinations. lgse/strata#444
- After a copy is undone, the next Ctrl+Z undoes the operation before it. lgse/strata#444
- An item a copy replaced without Trash is left out of that copy's undo. lgse/strata#1615 (unverified)

### Copy and move safety

- A symlink inside a copied folder is recreated as a symlink pointing at the same target, not followed. lgse/strata#254
- Copying a file of 4 GiB or larger to a FAT32 drive fails before copying, with a message suggesting exFAT. lgse/strata#1278
- Copies onto NTFS through ntfs-3g and other FUSE mounts without `RENAME_NOREPLACE` complete without an "Invalid argument" error. lgse/strata#1515
- Cancelling a folder copy onto an ntfs-3g mount after the progress bar fills leaves no partial folder at the destination name. lgse/strata#1515, lgse/strata#1625 (unverified)
- Copying or moving an item out of Trash that came from another drive creates it under its own leaf name. lgse/strata#1524
- Moving a folder into itself or a descendant, including through a symlink alias, does nothing and leaves the source untouched. lgse/strata#1537

## Design

The GDK clipboard carries only a file list with no cut marker. Strata keeps process-wide copy and cut lists, shared by every window, as the source of truth (lgse/strata#289).

- Cut matching also accepts GIO equality, because a clipboard round trip can return an equivalent URI instead of the stored path (lgse/strata#287).
- Row marks are read from an index rebuilt whenever the copy or cut lists change, not by comparing every entry on each row bind. `file://` URIs are keyed by native path so both spellings match (lgse/strata#1671, lgse/strata#1674).
- Copied paths that are not valid UTF-8 use ANSI-C `$'...'` quoting with `\xHH`, the shell syntax that carries arbitrary bytes, instead of lossy U+FFFD (lgse/strata#1594, lgse/strata#1626).
- Strata rewrites or clears the system clipboard only while it still owns the file list it set (lgse/strata#1265).
- Pasting into a single selected folder deliberately diverges from Nautilus, Thunar, and Finder (lgse/strata#449). An auto-selection made on load counts as a cursor, not a choice (lgse/strata#483).
- Same-folder copies use the language-neutral `(n)` suffix. A same-folder cut stays a no-op to prevent accidental renames (lgse/strata#270, lgse/strata#272).
- Duplicate exists so an in-place copy does not overwrite the user's clipboard (lgse/strata#271).
- Undo is one process-wide history of 32 entries. Copy undo trashes rather than deletes, so Ctrl+Z never destroys data (lgse/strata#444).
- Local copies open each source directory through `openat2` and re-read every entry's type before acting (lgse/strata#254).
- Local moves first used one confined `renameat2` with `NOREPLACE` (lgse/strata#365), and a staged copy where the kernel could not rename (lgse/strata#215). The placement ladder of `operations/filesystem-compatibility` replaced both (lgse/strata#1590, lgse/strata#1615).
- FAT names were first sanitized like GNOME Files does, rather than failing the whole staged copy (lgse/strata#1123). Per-mount name rules replaced that (lgse/strata#1615).
- The paste's conflict check runs off the UI thread, so a hung destination cannot freeze the window (lgse/strata#1590, lgse/strata#1615).
- Move to and Copy to reuse Strata's full chooser in a floating window instead of a separate destination picker (lgse/strata#1377, lgse/strata#1383).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-27 | lgse/strata#1900 | fix | Returned keyboard focus to the listing when the cross-device "Copy or move?" prompt closes. |
| 2026-10-15 | lgse/strata#1626 | fix | Escaped non-UTF-8 path bytes with ANSI-C quoting so copied paths name the real file. |
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
- Row marks treat a `file://` URI and its native path as equal, but not other equivalent spellings of a non-`file://` URI. lgse/strata#1674
