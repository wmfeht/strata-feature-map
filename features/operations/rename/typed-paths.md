---
title: Typed path names
status: shipped
origin: {issue: lgse/strata#1511, pr: lgse/strata#1512}
branch: null
reviewed_at: 5f17c9fdc8967e1b4ba8aaf8de113b46d824b0dd
review: reviewed
code: [crates/strata-fs/src/adapters/local_operations/place_entry.rs]
tests: [crates/strata-fs/src/adapters/local_operations/tests/place_entry.rs, tests/qa/scenarios/inline_renaming/new-item-named-with-path.jsonl, tests/qa/scenarios/inline_renaming/rename-moves-into-path.jsonl]
docs: [docs/keyboard-navigation.md]
related: [operations/create, operations/undo, integration/10xer-mode/file-verbs, operations/filesystem-compatibility]
---

## Summary

Naming an item in a local folder with a path relative to its folder. It applies in the inline rename editor and to the first name of a New File or New Folder. The path moves the item, making the folders it names. The 10xer `rename ›` prompt takes the same paths; `integration/10xer-mode/file-verbs` describes it.

## Behavior

### Moving into a path

- F2 on a local file and typing `notes/todo.txt` creates `notes` when missing and moves the file into it with its contents. lgse/strata#1512
- When `notes` already exists as a real folder, the file moves into it and nothing there is replaced. lgse/strata#1512
- Typing `../todo.txt` moves the item up one level. lgse/strata#1512
- `.` and `..` resolve as written, without reading the filesystem: `notes/../todo.txt` is a plain rename to `todo.txt`. lgse/strata#1512
- For an item in `work`, typing `../work/todo.txt` is a plain rename to `todo.txt`, undone as a rename. lgse/strata#1512
- A path that climbs past the filesystem root changes nothing and reports "Invalid move destination". lgse/strata#1512 (unverified)
- A folder renamed `docs/` is just named `docs`. lgse/strata#1512

### Naming a new item

- New File named `docs/` becomes the empty folder `docs` in place of the file. lgse/strata#1512
- New File or Ctrl+Shift+N New Folder named `a/b/` becomes the nested folders `a/b`. lgse/strata#1512
- New File named `new file/`, its own default name plus `/`, becomes the folder `new file`. lgse/strata#1512
- New File named `notes/today.txt` becomes an empty `today.txt` inside a new `notes`. lgse/strata#1512
- New Folder with Selection's name is a single name, so a `/` in it is refused. lgse/strata#1512

### Refusals

- F2 on an existing file and typing `docs/` styles the field as an error, with the description "An existing file can’t become a folder". Committing changes nothing. lgse/strata#1512
- New File named `todo.txt/x`, where `todo.txt` is a file, shows "Unable to rename item" with "“todo.txt” is not a folder". The new file keeps its default name. lgse/strata#1512
- `a//b`, `/abs`, or `a/ /b` reads "Enter a name"; `..`, `../`, `a/..`, or `./` reads "That name is reserved". lgse/strata#1512
- A link or a file where a folder of the path should be stops the placement. lgse/strata#1512
- A new file that is no longer empty is not turned into a folder. The error reads "<name> changed while the operation was in progress". lgse/strata#1512 (unverified)
- An existing empty file is never replaced by a folder. lgse/strata#1512
- The move never replaces an item already at the destination name. lgse/strata#1512
- A path onto another file system, such as `../../dev/shm/x/g.txt` from a tmpfs folder, is refused with "The destination is on a different file system". lgse/strata#2030
- Any failed step removes the folders the placement made, if still empty, reports the reason, and leaves the item under its old name. lgse/strata#1512

### After the move

- The outermost item that took the row in the original folder is selected and revealed, such as `notes` for `notes/todo.txt`. lgse/strata#1512
- After `../notes.txt` in Columns, `notes.txt` is selected in the parent column. lgse/strata#1512
- Moving a folder whose child columns are open closes those columns. lgse/strata#1512

### Undo

- Ctrl+Z after naming a new item with a path moves the outermost folder the naming made to Trash. lgse/strata#1512
- When every folder on the path already existed, that Ctrl+Z moves the item itself to Trash. lgse/strata#1512 (unverified)
- Ctrl+Z after a rename into new folders, such as `stash/<name>`, moves the item back and moves `stash` to Trash. lgse/strata#1512
- Ctrl+Z after a rename into existing folders moves the item back, and Ctrl+Shift+Z moves it again. lgse/strata#1512
- A placement superseded by another operation records no undo entry and leaves the view as it is. lgse/strata#1512

## Design

[docs/keyboard-navigation.md](https://github.com/lgse/strata/blob/0f9bb00f02d3923ba009f53e0dbaecb840ee524c/docs/keyboard-navigation.md) ("Creating files and folders") states the path rules for users.

- Issue lgse/strata#1511 asked that `docs/` or `docs/note.txt` typed for a new file make the folder or nested file, instead of "Names cannot contain /".
- Placement is one operation. Folders are made through directory descriptors without following links. The item moves by a no-replace rename, so it keeps its contents and metadata (lgse/strata#1512).
- An earlier delete-then-create version deleted an existing empty file renamed `x/y`, losing its permissions and mtime with no undo. The merged version replaced it from scratch (lgse/strata#1512).
- Only a new item may become a folder, because turning an existing file into one would delete it (lgse/strata#1512).
- Rollback removes only folders that are still empty, so nothing added meanwhile is lost (lgse/strata#1512).
- The create operation still takes one basename. A path typed as the first name runs afterwards as a separate placement (lgse/strata#1512).
- Undo reuses the existing Copy, Group, and Move entries instead of adding new ones (lgse/strata#1512).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-11-01 | lgse/strata#1512 | feat | Let inline renames, the 10xer rename prompt, and a new item's first name take a relative path that moves the item. |

## Known gaps

- Undoing a rename that created folders cannot be redone; only a rename into existing folders undoes as a plain move with redo. lgse/strata#1512
