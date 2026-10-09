---
title: Undo and redo
status: shipped
origin: {issue: lgse/strata#298, pr: lgse/strata#301}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: reviewed
code: []
tests: [src/app/browser/tests/undo.rs, src/app/browser/tests/undo_refresh.rs, src/adapters/local_operations/tests/undo.rs]
docs: []
related: [operations/trash, operations/trash/restore, operations/clipboard, operations/clipboard/conflicts, operations/rename, operations/create, operations/archives, operations/progress/dock, app/shortcut-reference]
---

## Summary

One undo history and one redo history for file operations, shared by every Strata window. Ctrl+Z reverts the latest recorded operation and Ctrl+Shift+Z re-applies the latest reverted one. Recorded operations are Move to Trash, moves, copies, renames, New Folder and New File, Restore, compression, Replace, Merge, and New Folder with Selection. Each operation's own undo rules live in its node.

## Behavior

### Keys

- Ctrl+Z undoes the latest recorded file operation; Ctrl+Shift+Z or Ctrl+Y redoes the latest undone one. lgse/strata#301, lgse/strata#1120
- Ctrl+Alt+Z, Ctrl+Shift+Alt+Z, Ctrl+Shift+Y, and Ctrl+Alt+Y neither undo nor redo. lgse/strata#1120 (unverified)
- With focus in a text field, such as the location bar or the rename editor, Ctrl+Z and Ctrl+Shift+Z edit the text and leave the file history unchanged. lgse/strata#228, lgse/strata#1120 (unverified)
- Ctrl+Z and Ctrl+Shift+Z do nothing while the active tab runs a foreground file operation; a job sent to the background does not block them. lgse/strata#228, lgse/strata#1120 (unverified)

### History

- The history is shared across windows: Ctrl+Z in any window undoes the latest operation, wherever it ran. lgse/strata#301
- Redo is shared too: after Ctrl+Z in one window, Ctrl+Shift+Z in another window re-applies that operation. lgse/strata#1120
- Repeated Ctrl+Z undoes earlier operations newest first, up to 32 entries; recording a 33rd drops the oldest. lgse/strata#444
- A paste that created nothing records no entry, so Ctrl+Z still undoes the operation before it. lgse/strata#444
- An undo records no undo entry of its own, so a second Ctrl+Z undoes the previous operation instead of reverting the undo. lgse/strata#301, lgse/strata#444
- While an undo or redo runs, Ctrl+Z or Ctrl+Shift+Z in another window does not start it a second time. lgse/strata#228, lgse/strata#1120 (unverified)
- A completed redo becomes the latest undo entry again, so Ctrl+Z after Ctrl+Shift+Z reverts it once more. lgse/strata#1120
- Any new operation that records an undo entry, such as a rename, clears the redo history; Ctrl+Shift+Z then does nothing. lgse/strata#1120

### Restore

- Ctrl+Z after Restore moves the restored items from where they landed back to Trash. lgse/strata#1097
- After a Restore that partly failed or was cancelled, Ctrl+Z moves only the restored items back to Trash. lgse/strata#1097 (unverified)

### Redo

- Ctrl+Shift+Z after undoing Move to Trash moves the restored items to Trash again. lgse/strata#1120
- Ctrl+Shift+Z after undoing a cut-paste moves the items to the destination again. lgse/strata#1120
- When redoing a move finds the destination name taken, the "File already exists" dialog warns "Redoing the move will overwrite its contents." and offers Replace. lgse/strata#1120
- That dialog offers Skip only when the redo has other items, and Apply to All only when more conflicts remain. lgse/strata#1120 (unverified)
- Ctrl+Shift+Z after undoing a copy restores the trashed copies from Trash. lgse/strata#1120
- Ctrl+Shift+Z after undoing a Restore restores the re-trashed items to the same locations again. lgse/strata#1120
- Ctrl+Shift+Z after undoing New Folder, New File, or a compression into a new archive restores that item from Trash. lgse/strata#1120 (unverified)
- Undoing a Merge or a Replace, including a compression that replaced an archive, offers no redo. lgse/strata#1120
- Undoing New Folder with Selection offers no redo. lgse/strata#1349 (unverified)

### Failures and partial results

- A cancelled or partly failed operation records only the items it completed. lgse/strata#301, lgse/strata#444
- An undo that fails leaves its entry for the next Ctrl+Z and offers no redo. lgse/strata#301, lgse/strata#1120
- An undo that reverts only some items leaves the rest for the next Ctrl+Z. lgse/strata#301
- After a multi-item move undo where one conflict was answered with Skip, Ctrl+Shift+Z moves forward only the items that went back. lgse/strata#1120
- A redo that applies only some items records an undo entry for just those items. lgse/strata#1120
- Undo of a move, copy, create, Restore, or compression skips items no longer where the operation left them. lgse/strata#301, lgse/strata#444 (unverified)
- Redo of a move or Move to Trash skips items no longer where the undo left them. lgse/strata#1120 (unverified)
- When no items remain, that Ctrl+Z or Ctrl+Shift+Z only discards the entry; the next press reaches the entry before it. lgse/strata#444, lgse/strata#1120 (unverified)
- If another operation is recorded while a move undo's conflict dialog is open, answering the dialog reverts nothing. lgse/strata#301 (unverified)

## Design

Undo targets the latest reversible operation process-wide, matching common file managers, instead of a separate shortcut per operation (lgse/strata#298).

- The history lives on the GTK main thread and every window reads it. Entries carry a generation, so an undo applies only to the entry the user inspected, and a claimed entry cannot be started twice (lgse/strata#228, lgse/strata#301).
- The single pending slot became a history of 32 entries because undoing a copy must expose the operation before it (lgse/strata#444).
- Undo never destroys an original. Copy, create, compress, and Restore undos move items to Trash. Replace and Merge undos delete the incoming copy, then restore the original staged in Trash. Permanent deletion stays outside the history by design (lgse/strata#444, lgse/strata#1097).
- An undo never records a new undo entry, so Ctrl+Z cannot toggle an item back and forth (lgse/strata#301). Its applied items feed a parallel redo stack instead (lgse/strata#1120).
- Any new forward operation clears the redo stack, matching Finder. A persistent action journal was rejected as more than platform parity needs (lgse/strata#1117, lgse/strata#1120).
- Each claimed entry keeps a bucket of the items that actually applied. Unapplied items stay on the stack for retry, applied items become the opposite entry, and a replay that applied nothing pushes nothing (lgse/strata#1120).
- Undo and redo share one replay core parameterized by direction and reuse the provider's undo operations, with no new provider API. Copy redo therefore restores the trashed copies rather than copying again (lgse/strata#1117, lgse/strata#1120).
- Merge and Replace undos mix deletions and restores, which no single replay can re-apply, so they offer no redo (lgse/strata#1120).
- History is kept in memory only; persistence across restarts was ruled out of scope (lgse/strata#1059).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-23 | lgse/strata#1120 | feat | Added a shared redo stack on Ctrl+Shift+Z and Ctrl+Y, cleared by new operations and limited to items an undo applied. |
| 2026-09-18 | lgse/strata#1097 | feat | Recorded undo entries for create, copy Replace, Restore, and compression, each reversed through Trash. |

## Known gaps

None known.
