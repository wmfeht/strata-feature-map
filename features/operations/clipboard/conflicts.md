---
title: Paste name conflicts
status: shipped
origin: {issue: lgse/strata#7, pr: lgse/strata#25}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: reviewed
code: []
tests: [tests/e2e/scenarios/test_copy_conflicts.py, src/adapters/local_operations/tests/conflicts.rs, src/adapters/local_operations/tests/merge.rs, src/adapters/local_operations/tests/replacement.rs]
related: [operations/drag-and-drop]
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
- Dragging a move onto a folder that holds a taken name shows the same dialog without Keep Both. lgse/strata#599
- Dragging a copy onto a folder that holds a taken name shows the same dialog with Keep Both. lgse/strata#599 (unverified)

### Choices

- Replace overwrites only the chosen destination. lgse/strata#708
- Keep Both, offered for copies, creates the first free `name (N).ext` beside the existing item and leaves it untouched. lgse/strata#599
- Conflicts during a cut-paste or Move to… offer no Keep Both. lgse/strata#599
- Merge appears only when copying a folder onto a folder; moves and file conflicts never offer it. lgse/strata#1092
- Merge adds the incoming contents, keeps destination-only items, and overwrites same-named files with the incoming copies. lgse/strata#1092
- Merge with Apply to All merges the remaining folder pairs and still asks about each file conflict. lgse/strata#1092 (unverified)

### Undo

- Ctrl+Z after a copy answered with Replace restores the overwritten original from Trash. lgse/strata#1097
- Ctrl+Z after a Merge removes what the merge created and restores the overwritten originals, leaving destination-only items. lgse/strata#1092, lgse/strata#1097
- When undoing a move finds an original name taken, the dialog offers Replace and Skip but not Keep Both or Merge. lgse/strata#301, lgse/strata#708
- Skipping one item while undoing a multi-item move still returns the others and leaves the new occupant intact. lgse/strata#708

### Failure safety

- A failed, cancelled, or disk-full Replace leaves the existing destination unchanged and removes the partial copy. lgse/strata#25
- An item that appears at the destination after the dialog is answered is not overwritten. lgse/strata#25, lgse/strata#1097
- Replacing a folder swaps the whole folder; none of its old contents remain. lgse/strata#25
- Replace onto a destination without a local path fails with "Safe replacement is unavailable at this destination" and keeps the existing item. lgse/strata#25

## Design

Each item carries its own decision: fail if it exists, Replace, Keep Both, or Merge. A request-wide overwrite flag could replace items that appeared after the check (lgse/strata#7).

- Replace copies into a staged sibling, moves the original to Trash, then publishes the stage without replacing a concurrent arrival (lgse/strata#25, lgse/strata#1097).
- Where Trash is unsupported, Replace keeps an atomic exchange that cannot be undone (lgse/strata#1097).
- Keep Both is copy-only, because move undo and reveal assume a move never renames its destination (lgse/strata#599).
- Merge is copy-only, because undoing a merged move cannot tell which destination contents the source owned (lgse/strata#1092).
- Incoming-wins merging with Trash staging was chosen over per-file prompts or Finder's newer-wins, to keep it predictable and undoable (lgse/strata#1091).
- Same-folder paste never prompts, so pasting where an item already lives stays non-destructive. The engine also treats Replace of an item onto itself as a no-op (lgse/strata#395, lgse/strata#708).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-23 | lgse/strata#1092 | feat | Added Merge for folder-onto-folder copy conflicts, undone through Trash staging. |
| 2026-09-11 | lgse/strata#708 | feat | Showed Skip and Apply to All only when other items depend on them. |
| 2026-09-08 | lgse/strata#599 | fix | Offered Keep Both for cross-folder copy conflicts. |
| 2026-09-06 | lgse/strata#448 | fix | Made the header X cancel the conflict dialog. |
| 2026-08-30 | lgse/strata#25 | fix | Staged replacements and tracked each item's decision so a failure keeps the destination. |

## Known gaps

- The dialog cannot paste an item under a custom name; the fix is unmerged. lgse/strata#1299, lgse/strata#1303
