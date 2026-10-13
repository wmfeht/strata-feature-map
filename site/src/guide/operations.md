---
nodes: [operations/clipboard, operations/clipboard/conflicts, operations/create, operations/rename, operations/trash, operations/trash/restore, operations/delete, operations/undo, operations/archives, operations/drag-and-drop, operations/drag-and-drop/copy-or-move, operations/progress, operations/progress/jobs]
reviewed_at: 0a086aa3bdb251842a1e8413e2a6b35970d0b409
---

# Everyday operations

Copy, move, rename, and delete files with familiar keys, and press Ctrl+Z when
something goes wrong.

## Copy, move, and paste

<!-- node: operations/clipboard, Copy and cut -->
<!-- node: operations/clipboard, Paste destination -->
<!-- node: operations/clipboard, Same-folder copies and Duplicate -->
<!-- node: operations/clipboard, Move to and Copy to -->
<!-- node: operations/clipboard/conflicts, Dialog -->
<!-- node: operations/clipboard/conflicts, Choices -->

1. Select files and press Ctrl+C to copy or Ctrl+X to cut. Cut items show
   scissors.
2. Go to the destination and press Ctrl+V.

With exactly one folder selected, Ctrl+V pastes into it. Otherwise it pastes
into the folder you are viewing. A copy pasted into its own folder becomes
`report (1).pdf`; Ctrl+D (**Duplicate**) does this without the clipboard.

Prefer a dialog? Right-click and choose **Move to…** or **Copy to…**.

When a name is taken, **File already exists** offers:

- **Replace**: overwrite that item.
- **Keep Both** (copies only): add `name (1).ext` beside it.
- **Merge** (folder copied onto folder): add the incoming contents, replacing
  same-named files.
- **Skip**: keep the existing item, transfer the rest.
- **Cancel**: transfer nothing.

**Apply to All** reuses your answer for the remaining conflicts.

## Create and rename

<!-- node: operations/create, Starting creation -->
<!-- node: operations/create, Naming the new item -->
<!-- node: operations/create, New Folder with Selection -->
<!-- node: operations/rename, Starting a rename -->
<!-- node: operations/rename, Editing -->
<!-- node: operations/rename, Committing and cancelling -->

Press Ctrl+Shift+N for a new folder, type its name, and press Enter.
Right-click empty space for **New Folder** or **New File**. Ctrl+Alt+N
(**New Folder with Selection**) moves the selected items into a new folder.

To rename, press F2 or Ctrl+R, or click the name of a single selected item
again after a pause. Enter, Tab, or clicking elsewhere saves; Escape keeps the
old name.

## Trash, restore, and delete

<!-- node: operations/trash, Moving to Trash -->
<!-- node: operations/trash, Locations without Trash -->
<!-- node: operations/trash, Browsing Trash -->
<!-- node: operations/trash/restore, Lookup and confirmation -->
<!-- node: operations/delete, Entry points -->
<!-- node: operations/delete, Confirmation -->

Press Delete to move the selection to Trash, with no prompt. To get it back
later, open **Trash** in the sidebar, right-click the item, and choose
**Restore**. Strata shows the original path before restoring.

Press Shift+Delete, or choose **Permanently delete**, to delete for good after a
confirmation. This cannot be undone.

Good to know:

- Inside Trash, Delete always deletes permanently, after confirming.
- Locations without Trash, such as `/dev/shm`, ask before deleting permanently.

## Undo a mistake

<!-- node: operations/undo, Keys -->
<!-- node: operations/undo, History -->
<!-- node: operations/clipboard, Undo -->

Press Ctrl+Z to undo the last file operation; Ctrl+Shift+Z or Ctrl+Y redoes it.

| You did | Ctrl+Z |
| --- | --- |
| Move, cut, or Trash | Puts items back |
| Copy | Trashes the copies |
| Rename | Restores the old name |
| New folder or file | Trashes it |

The history holds 32 operations, shared by every window.

## Work with archives

<!-- node: operations/archives, Extracting -->
<!-- node: operations/archives, Activation -->
<!-- node: operations/archives, Extraction output -->
<!-- node: operations/archives, Compressing -->

Right-click an archive and choose **Extract here** or **Extract to…**, or
double-click it. A single top-level entry lands under its own name. Several land
in a folder named after the archive, such as `photos/` for `photos.zip`.
Nothing existing is overwritten.

To create one, select items and choose **Compress…**. Pick **ZIP**, **7Z**,
**TAR.GZ**, or **TAR**; ZIP and 7Z can be **Password protected**.

## Drag and drop

<!-- node: operations/drag-and-drop, Drop targets -->
<!-- node: operations/drag-and-drop, Spring-loaded navigation -->
<!-- node: operations/drag-and-drop/copy-or-move, Choosing the action -->
<!-- node: operations/drag-and-drop/copy-or-move, Copy or move dialog -->

Drop items onto a folder, a sidebar place, or a parent breadcrumb.

| Drop | Result |
| --- | --- |
| Same drive | Move |
| Another drive | **Copy or move?** asks |
| Holding Ctrl | Copy |
| Holding Shift | Move |

Hover over a folder for 750 ms to open it mid-drag. To skip the question, set
**Settings → General → Drag & drop to another device** to **Always copy** or
**Always move**.

## Follow progress in Jobs

<!-- node: operations/progress, Progress dialog -->
<!-- node: operations/progress, Cancellation -->
<!-- node: operations/progress/jobs, Dashboard -->
<!-- node: operations/progress/jobs, Cancellation -->

A file operation that runs past 350 ms, or touches 16 or more items, shows a
progress dialog. **Cancel** stops the rest but keeps what is done.

[Custom actions](actions.md) run in the background and open **Jobs**. Reopen it
from the footer button, such as `1 job running`. **Details** shows a job's
output; **Cancel** stops it. Escape hides Jobs without stopping anything.

**Full detail:** [Archives reference](../reference/archives.md)
