---
title: New Folder and New File
status: shipped
origin: {issue: null, pr: lgse/strata#4}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: reviewed
code: [src/adapters/local_operations/create_entry.rs]
tests: [src/adapters/local_operations/tests/create_entry.rs, tests/e2e/scenarios/test_created_entry_columns.py, tests/e2e/scenarios/test_entry_management.py]
docs: [docs/keyboard-navigation.md]
related: [operations/rename, integration/10xer-mode, integration/portal-file-chooser]
---

## Summary

Creating an empty file or folder in the current directory from the background menu or Ctrl+Shift+N, then naming it in place. It also covers New Folder with Selection, which groups selected items into a new folder. The file chooser's header button reuses this flow, and the 10xer footer create prompt reuses the creation operation; both are described in their own nodes.

## Behavior

### Starting creation

- The folder background menu shows New Folder and New File. lgse/strata#4
- In Trash and Recent, the background menu omits New Folder and New File. lgse/strata#499, lgse/strata#1083
- Ctrl+Shift+N starts New Folder in Columns, List, and Icons. lgse/strata#567
- In Columns, Ctrl+Shift+N creates in the keyboard-focused pane, then the active pane, then the deepest pane, whatever pane the pointer rests over. lgse/strata#238
- Starting creation clears the pane's filter text. lgse/strata#567

### Allocation

- New Folder creates `new folder` on disk before any name is typed; New File creates an empty `new file`. lgse/strata#567
- When the default name is taken by any item, creation uses the first free `new folder (1)`, `(2)`, and so on, without overwriting. lgse/strata#567
- A creation failure reports "Could not create “name”:" followed by the error. lgse/strata#567 (unverified)

### Naming the new item

- The new item is selected and its rename editor opens with the whole default name selected, so typing replaces it. lgse/strata#567, lgse/strata#760
- Enter or a click outside the field commits a valid name; a click inside the field keeps editing, and leading and trailing spaces are kept. lgse/strata#567
- Escape, an empty name, or an invalid name such as `bad/name` closes the editor and keeps the item under its default name. lgse/strata#567
- A name already in use shows "Unable to rename item"; after Close, the existing item and the new default item are unchanged. lgse/strata#567, lgse/strata#760
- Going Home or Back before the editor opens leaves the item named by default and opens no late editor. lgse/strata#760
- If the created row is not listed within 5 seconds, no editor opens. lgse/strata#567 (unverified)
- On GTK 4.14 in Columns, a new file that sorts after 2,000 entries still gets its editor. lgse/strata#635

### Where the new item appears

- In Columns, a new folder opens as the child column, replacing any stale child, and the breadcrumb follows it. lgse/strata#760
- In Columns, a new file closes stale child columns, returns the breadcrumb to the parent, and does not open the file. lgse/strata#760
- In Columns, after Enter renames a new folder, the child column header shows the new name and F2 reopens the editor on the same parent item. lgse/strata#760
- In Columns, clicking a sibling to end the edit commits the name and leaves the sibling selected as the F2 target. lgse/strata#760
- In List and Icons, the view stays in the parent directory and selects the new item without opening it. lgse/strata#760
- In a 420-pixel-wide Columns window, the new folder's editor stays within the window. lgse/strata#760

### Undo

- Ctrl+Z after New Folder or New File moves the created item to Trash. lgse/strata#1097

### New Folder with Selection

- With one or more items selected, the item menu shows New Folder with Selection; Trash, Recent, and recursive search results omit it. lgse/strata#1349
- The item is also omitted when any selected item cannot be removed. lgse/strata#1349 (unverified)
- Choosing it, or Ctrl+Alt+N, creates a numbered `new folder` beside the selection, moves the selected items into it, and opens rename on the folder. lgse/strata#1349
- Ctrl+Alt+N with nothing selected creates a plain `new folder`. lgse/strata#1349
- One Ctrl+Z moves the items back and moves the created folder to Trash. lgse/strata#1349

## Design

[docs/keyboard-navigation.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/keyboard-navigation.md) ("Creating files and folders") carries the user-facing rules.

- Items are created first and then renamed with the normal editor. Temporary creation rows were removed: destroying the focused row inside GTK's focus-out handling froze List and Icons at 100% CPU (lgse/strata#566, lgse/strata#567).
- Cancelling the first rename keeps the item, because the item already exists. An earlier cancellation-only policy was replaced by this rule (lgse/strata#566).
- Numbered alternatives are retried only when atomic creation reports that the name exists, never after a separate existence check. An empty file is closed before its creation is published (lgse/strata#567).
- A name must be one basename. The UI and the operation provider both reject `..`, `nested/child`, and absolute paths, so creation stays a direct child of the shown directory (lgse/strata#10, lgse/strata#23).
- Keyboard creation ignores the pointer, so a resting mouse cannot redirect a folder into a pane the keyboard never visited (lgse/strata#236, lgse/strata#238).
- In Columns, revealing the created entry does not start a second asynchronous navigation, which could cancel its rename editor (lgse/strata#690, lgse/strata#760).
- Create undo trashes rather than deletes, so it is reversible (lgse/strata#1097).
- New Folder with Selection records one composite undo entry instead of three stacked ones, so the gesture reverts atomically (lgse/strata#1347). Fusion happens when entries are pushed, because Columns truncation could otherwise consume the pending entry first (lgse/strata#1349).
- New Folder with Selection is hidden in recursive search, whose result model never shows the created row, so the move and rename would never start (lgse/strata#1349).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-01 | lgse/strata#1349 | feat | Added New Folder with Selection and Ctrl+Alt+N, grouping the selection in one undoable gesture. |
| 2026-09-12 | lgse/strata#760 | fix | Revealed created entries in Columns without a second navigation, keeping selection, focus, and child columns consistent. |
| 2026-09-08 | lgse/strata#635 | ci | Requested the created row's reveal before requiring its editor allocation, so GTK 4.14 opens the editor. |
| 2026-09-08 | lgse/strata#567 | fix | Created items immediately and renamed them in place, replacing temporary creation rows that froze List and Icons. |
| 2026-09-04 | lgse/strata#238 | fix | Created folders from Ctrl+Shift+N in the focused pane instead of the pane under the pointer. |
| 2026-08-31 | lgse/strata#30 | fix | Stopped styling an empty New Folder or New File name field as an error. |
| 2026-08-30 | lgse/strata#4 | feat | Added New File to the folder background menu, sharing the New Folder entry row. |
| 2026-08-30 | lgse/strata#23 | fix | Validated new folder names as single basenames in the UI and the provider. |

## Known gaps

- Typing `docs/` or `docs/note.txt` as a new file's name is rejected instead of creating the folder or nested file; the fix is unmerged. lgse/strata#1511, lgse/strata#1512
