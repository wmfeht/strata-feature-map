---
title: Paste name conflicts
status: shipped
origin: {issue: lgse/strata#7, pr: lgse/strata#25}
branch: null
reviewed_at: be3343a5992a2a5497b1a2ee7faa525be18e988f
review: draft
code: [src/adapters/local_operations/replacement.rs, src/adapters/local_operations/merge_aside.rs]
tests: [tests/qa/scenarios/copy_conflicts, src/adapters/local_operations/tests/conflicts.rs, src/adapters/local_operations/tests/merge.rs, src/adapters/local_operations/tests/replacement.rs, tests/qa/mutations/keep-both.patch]
related: [operations/drag-and-drop, operations/filesystem-compatibility, operations/filesystem-compatibility/leftovers]
---

## Summary

The "File already exists" dialog shown when a paste, Move to…, Copy to…, or move undo meets a taken name. It covers the Replace, Keep Both, Merge, and Skip transfers behind the dialog and their undo.

## Behavior

### Dialog

- Pasting into a folder that already holds an item of the same name opens "File already exists", naming the item and the folder. lgse/strata#708
- When Ctrl+V, a drop, or Move to… opens the dialog, Replace has focus. Enter or keypad Enter activates the focused button. lgse/strata#1206, lgse/strata#1052
- Cancel, Escape, and the header X abandon the whole paste, and no file is written. lgse/strata#448, lgse/strata#708
- Skip appears only when other items are accepted or further conflicts remain; it keeps the existing item and transfers the rest. lgse/strata#708
- The Apply to All checkbox appears only while further conflicts remain; when checked, the chosen action applies to all of them. lgse/strata#708
- Dragging a move or a copy onto a folder that holds a taken name shows the same dialog with Keep Both. lgse/strata#599, lgse/strata#1615 (unverified)
- A paste whose name the destination stores differently prompts on that stored name. lgse/strata#1615
- For example, `10:00` pasted onto FAT holding `10_00` explains "“10:00” will be saved as “10_00” in this location." lgse/strata#1615
- The folder prompt then adds "Items whose names change to suit this location overwrite items with the new name." lgse/strata#1615
- On a mount that already refused Trash, the conflict prompt adds "Replaced items can't be moved to Trash here and will be deleted." lgse/strata#1614

### Choices

- Replace overwrites only the chosen destination. lgse/strata#708
- Keep Both creates the first free `name (N).ext` beside the existing item and leaves it untouched. lgse/strata#599
- Keep Both is offered for a cut-paste or Move to… too; Ctrl+Z moves the item back from its numbered name. lgse/strata#1615
- Keep Both picks its number when the copy is placed, so a name taken meanwhile gets the next number. lgse/strata#1615
- A long name numbered by Keep Both is cut so ` (N)` fits the mount's name limit. lgse/strata#1615
- Merge appears only when copying a folder onto a folder; moves and file conflicts never offer it. lgse/strata#1092
- Merge adds the incoming contents, keeps destination-only items, and overwrites same-named files with the incoming copies. lgse/strata#1092
- Merge with Apply to All merges the remaining folder pairs and still asks about each file conflict. lgse/strata#1092 (unverified)
- Merge never writes into the live folder: incoming items are built in a hidden stage and renamed in. lgse/strata#1615
- A name taken inside a merged folder meanwhile gets the next number and is reported; a stopped merge leaves nothing partial. lgse/strata#1615
- A same-filesystem move answered with Replace renames the source into place without copying it. lgse/strata#1615

### Undo

- Ctrl+Z after a copy answered with Replace restores the overwritten original from Trash. lgse/strata#1097
- Ctrl+Z after a Merge removes what the merge created and restores the overwritten originals, leaving destination-only items. lgse/strata#1092, lgse/strata#1097
- An item edited since the Merge or Replace stays on undo, its original stays in Trash, and the dialog says so. lgse/strata#1615
- Where Trash is unavailable, a Merge undo deletes only created items it recorded and finds unchanged, and reports the rest. lgse/strata#1615
- Undoing such a Merge that placed `0555` folders completes without "Permission denied"; a placed folder that stays gets its mode back. lgse/strata#1729
- When undoing a move finds an original name taken, the dialog offers Replace and Skip but not Keep Both or Merge. lgse/strata#301, lgse/strata#708
- Skipping one item while undoing a multi-item move still returns the others and leaves the new occupant intact. lgse/strata#708

### Failure safety

- A failed, cancelled, or disk-full Replace leaves the existing destination unchanged and removes the partial copy. lgse/strata#25
- An item that appears at the destination after the dialog is answered is not overwritten. lgse/strata#25, lgse/strata#1097
- Replacing a folder swaps the whole folder; none of its old contents remain. lgse/strata#25
- Replace onto a destination without a local path fails with "Safe replacement is unavailable at this destination" and keeps the existing item. lgse/strata#25
- Without Trash, Replace moves the original into a hidden `.strata-originals-<id>/` folder under its own name, then deletes it after the flush. lgse/strata#1615, lgse/strata#1729
- An exchange Replace also runs through that folder, so a `.strata-copy-*` stage only ever holds a copy. lgse/strata#1729
- A failure there puts the original back; Replace is refused before copying when no strategy is safe. lgse/strata#1615
- An original that cannot be removed after the new item is placed no longer fails the paste. It completes with any Undo it has and reports "“%{name}” was replaced, but its original could not be removed from “%{kept}”: %{error}". lgse/strata#1729
- Where Trash is unavailable, Merge sets originals aside in a hidden `.strata-merge-<id>` folder and removes it once the merge is flushed. lgse/strata#1615
- A name taken since the check ends such a merge, keeping the aside folder and naming it. lgse/strata#1615
- On kernel exFAT, a Merge without Trash removes its `.strata-merge-*` folder once it finishes. lgse/strata#1729
- Cancelling such a merge after it placed an item ends as Cancelled, with the originals back and no `.strata-merge-*` folder left. lgse/strata#1729
- A merge whose aside folder only another program's open file keeps completes and reports the folder as still open. lgse/strata#1729
- A Trash move that reports success without moving the original falls back to setting it aside. lgse/strata#1615

## Design

Each item carries its own decision: fail if it exists, Replace, Keep Both, or Merge. A request-wide overwrite flag could replace items that appeared after the check (lgse/strata#7).

- Replace copies into a staged sibling, moves the original to Trash, then publishes the stage without replacing a concurrent arrival (lgse/strata#25, lgse/strata#1097).
- Where Trash is unsupported, Replace first kept an atomic exchange that cannot be undone (lgse/strata#1097). Exchange is now used only on in-kernel local filesystems; elsewhere the original is set aside (lgse/strata#1590, lgse/strata#1615).
- A set-aside original goes into a `.strata-originals-<id>/` folder under its own name, so a crash leaves it restorable by its name alone (lgse/strata#1729).
- Keep Both was copy-only, because move undo and reveal assumed a move never renames its destination (lgse/strata#599). Undo now starts from where each item landed, so Keep Both is offered for moves (lgse/strata#1615).
- The prompt works out the name the paste will use, off the main thread, so fixed names conflict as the user will see them (lgse/strata#1615).
- Undo of a Merge or Replace records what it placed, up to 100,000 entries, and deletes only unchanged items, so later edits survive (lgse/strata#1615).
- Merge is copy-only, because undoing a merged move cannot tell which destination contents the source owned (lgse/strata#1092).
- Incoming-wins merging with Trash staging was chosen over per-file prompts or Finder's newer-wins, to keep it predictable and undoable (lgse/strata#1091).
- Same-folder paste never prompts, so pasting where an item already lives stays non-destructive. The engine also treats Replace of an item onto itself as a no-op (lgse/strata#395, lgse/strata#708).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-20 | lgse/strata#1729 | fix | Set Replace originals aside in an originals folder and fixed merge cancel and undo without Trash. |
| 2026-09-23 | lgse/strata#1092 | feat | Added Merge for folder-onto-folder copy conflicts, undone through Trash staging. |
| 2026-09-11 | lgse/strata#708 | feat | Showed Skip and Apply to All only when other items depend on them. |
| 2026-09-08 | lgse/strata#599 | fix | Offered Keep Both for cross-folder copy conflicts. |
| 2026-09-06 | lgse/strata#448 | fix | Made the header X cancel the conflict dialog. |
| 2026-08-30 | lgse/strata#25 | fix | Staged replacements and tracked each item's decision so a failure keeps the destination. |

## Known gaps

- The dialog cannot paste an item under a custom name; the fix is unmerged. lgse/strata#1299, lgse/strata#1303
