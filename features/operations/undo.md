---
title: Undo and redo
status: shipped
origin: {issue: lgse/strata#298, pr: lgse/strata#301}
branch: null
reviewed_at: 5738aad808ea4cc4671516bc569d85f862664809
review: draft
code: [src/app/browser/replay/**, src/app/browser/undo/**, src/adapters/local_operations/undo_move.rs, src/adapters/local_operations/undo_move/**, src/app/browser/operation_events/replay.rs, src/app/browser/replay.rs, src/app/browser/undo.rs, src/ui/browser/transfer/replay.rs]
tests: [src/app/browser/tests/undo.rs, src/app/browser/tests/undo_refresh.rs, src/adapters/local_operations/tests/undo.rs, tests/qa/scenarios/entry_management/undo-restores-completed-move.jsonl, src/adapters/local_operations/tests/undo/**, src/app/browser/tests/undo/**, src/ui/browser/transfer/tests/undo.rs, src/ui/browser/transfer/tests/replay_kinds.rs]
docs: []
related: [operations/trash, operations/trash/restore, operations/clipboard, operations/clipboard/conflicts, operations/rename, operations/rename/typed-paths, operations/create, operations/archives, operations/progress/dock, app/shortcut-reference, operations/filesystem-compatibility]
---

## Summary

One undo history and one redo history for file operations, shared by every Strata window. Ctrl+Z reverts the latest recorded operation and Ctrl+Shift+Z re-applies the latest reverted one. Recorded operations are Move to Trash, moves, copies, renames, New Folder and New File, Restore, compression, extraction, Replace, Merge, and New Folder with Selection. Each operation's own undo rules live in its node; this node owns the replay and the conflict prompt an undo or redo shows.

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
- A move answered with Merge records no entry for the merged folder, so Ctrl+Z undoes the operation before it. The originals the merge overwrote stay in Trash. lgse/strata#2078
- A copy into a folder opened as administrator records no entry, even when a conflict is answered Replace. So does a New Folder or New File there. Ctrl+Z then undoes the operation before it. lgse/strata#1837
- Such a copy, New Folder, or New File leaves the redo history as it was. lgse/strata#1837 (unverified)
- A rename, or a move into or out of such a folder, still records its entry. lgse/strata#1837
- An undo records no undo entry of its own, so a second Ctrl+Z undoes the previous operation instead of reverting the undo. lgse/strata#301, lgse/strata#444
- While an undo or redo runs, Ctrl+Z or Ctrl+Shift+Z in another window does not start it a second time. lgse/strata#228, lgse/strata#1120 (unverified)
- A completed redo becomes the latest undo entry again, so Ctrl+Z after Ctrl+Shift+Z reverts it once more. lgse/strata#1120
- Any new operation that records an undo entry, such as a rename, clears the redo history; Ctrl+Shift+Z then does nothing. lgse/strata#1120

### Moves

- Ctrl+Z after a move that fixed names for the destination gives the original names back, deepest first, also between native and GVfs locations. lgse/strata#1615
- Ctrl+Shift+Z then fixes those names again. lgse/strata#1615
- Names Undo cannot give back are reported as "“new” could not be renamed back to “old”: <error>". lgse/strata#1615
- A move undo starts from where each item landed, such as a Keep Both number or a fixed name. lgse/strata#1615 (unverified)
- A move whose entries partly stayed at the source leaves that item out of its undo, and the report names it. lgse/strata#1615
- Undoing a cross-volume move deletes the moved items only once their copies back are flushed. lgse/strata#1615 (unverified)
- Ctrl+Z after a move answered with Replace moves the item back and restores the replaced original from Trash, for files and folders. lgse/strata#2080
- If that original is no longer in Trash, the item still moves back. The undo reports "One or more recently trashed items are no longer available". lgse/strata#2080
- The next Ctrl+Z after that report undoes the older entry. lgse/strata#2080
- An item that appears at the vacated path before the restore is kept; its original stays in Trash and the undo reports the failure. lgse/strata#2080
- Cancelling such an undo restores the originals only of items already moved back. A failed or unattempted item leaves its original in Trash. lgse/strata#2080
- After a cross-volume move-back, the original is restored only once the move-back is flushed. lgse/strata#2080
- When undoing a move finds an original name taken by the same kind of item, the dialog offers Replace. It never offers Keep Both or Merge. lgse/strata#301, lgse/strata#708, lgse/strata#2070
- When undo or redo of a move meets an item of the other kind, the dialog offers no Replace. An example is a file where a folder was moved from. lgse/strata#2070
- That prompt explains "An item named “<name>” already exists in <folder>. A file and a folder can’t replace one another." lgse/strata#2070
- A symbolic link met at the replay destination counts as a file, even when it points to a folder. lgse/strata#2070
- An item whose kind the probe cannot read is taken to match, so its prompt still offers Replace. lgse/strata#2070
- Replace with Apply to All replaces only the remaining same-kind conflicts. Each conflict between a file and a folder keeps its own prompt. lgse/strata#2070
- The replay prompt offers Skip and Apply to All only while an answer can still move something. That needs an item already accepted, or a later conflict Replace can resolve. lgse/strata#2070
- Otherwise Skip and Apply to All are hidden. Cancel stays, plus Replace when the item is the same kind. lgse/strata#2070
- Apply to All also shows only while a later conflict remains. lgse/strata#1120 (unverified)
- Skipping a file-and-folder conflict leaves the blocking item in place. lgse/strata#2070
- Skipping one item while undoing a multi-item move still returns the others and leaves the new occupant intact. lgse/strata#708

### Restore

- Ctrl+Z after Restore moves the restored items from where they landed back to Trash. lgse/strata#1097
- After a Restore that partly failed or was cancelled, Ctrl+Z moves only the restored items back to Trash. lgse/strata#1097 (unverified)

### Redo

- Ctrl+Shift+Z after undoing Move to Trash moves the restored items to Trash again. lgse/strata#1120
- Ctrl+Shift+Z after undoing a cut-paste moves the items to the destination again. lgse/strata#1120
- Undoing a Replace move onto a non-local destination, which stages no original in Trash, only moves the item back. lgse/strata#2080
- Ctrl+Shift+Z after undoing a move answered with Replace asks before replacing the restored original. After Replace, the next Ctrl+Z restores that original again. lgse/strata#2080
- When a move undo answers Replace at the original name, Ctrl+Shift+Z moves the item forward and restores the item that undo replaced. lgse/strata#2080 (unverified)
- When redoing a move finds the destination name taken by an item of the same kind, the "File already exists" dialog offers Replace. It warns "Redoing the move will overwrite its contents." lgse/strata#1120, lgse/strata#2070
- Ctrl+Shift+Z after undoing a copy restores the trashed copies from Trash. lgse/strata#1120
- Ctrl+Shift+Z after undoing a Restore restores the re-trashed items to the same locations again. lgse/strata#1120
- Ctrl+Shift+Z after undoing New Folder, New File, or a compression into a new archive restores that item from Trash. lgse/strata#1120 (unverified)
- Undoing a Merge or Replace copy, or a compression that replaced an archive, offers no redo. lgse/strata#1120
- Undoing New Folder with Selection offers no redo. lgse/strata#1349 (unverified)

### Failures and partial results

- A cancelled or partly failed operation records only the items it completed. Extraction is the exception; `operations/archives` owns its rule. lgse/strata#301, lgse/strata#444, lgse/strata#1552
- An undo that fails leaves its entry for the next Ctrl+Z and offers no redo. lgse/strata#301, lgse/strata#1120
- An undo that reverts only some items leaves the rest for the next Ctrl+Z. lgse/strata#301
- After a multi-item move undo where one conflict was answered with Skip, Ctrl+Shift+Z moves forward only the items that went back. lgse/strata#1120
- A redo that applies only some items records an undo entry for just those items. lgse/strata#1120
- Undo of a move, copy, create, Restore, or compression skips items proven gone from where the operation left them. lgse/strata#301, lgse/strata#444, lgse/strata#1729 (unverified)
- Ctrl+Z after moving a dangling symlink moves it back. lgse/strata#1729
- Redo of a move or Move to Trash skips items no longer where the undo left them. lgse/strata#1120 (unverified)
- When no items remain, that Ctrl+Z or Ctrl+Shift+Z only discards the entry; the next press reaches the entry before it. lgse/strata#444, lgse/strata#1120 (unverified)
- A move undo or redo whose every conflict is answered Skip moves nothing. It keeps its entry, as Cancel does, and the next press prompts again. lgse/strata#2070
- If another operation is recorded while a move undo's conflict dialog is open, answering the dialog reverts nothing. lgse/strata#301 (unverified)

## Design

Undo targets the latest reversible operation process-wide, matching common file managers, instead of a separate shortcut per operation (lgse/strata#298).

- The history lives on the GTK main thread and every window reads it. Entries carry a generation, so an undo applies only to the entry the user inspected, and a claimed entry cannot be started twice (lgse/strata#228, lgse/strata#301).
- The single pending slot became a history of 32 entries because undoing a copy must expose the operation before it (lgse/strata#444).
- Undo never destroys an original. Copy, create, compress, and Restore undos move items to Trash. Replace and Merge copy undos delete the incoming copy, then restore the original staged in Trash. Since lgse/strata#1615 an edited incoming item is kept instead. A Replace move undo moves the item back first, then restores the original (lgse/strata#2080). Permanent deletion stays outside the history by design (lgse/strata#444, lgse/strata#1097).
- A move record keeps the Trash identity of the original its Replace staged. Before lgse/strata#2080 the record dropped it, so undoing a replacing move left the original in Trash (lgse/strata#2077).
- That undo looks up all originals in one Trash scan and restores them after the move-back batches settle, so cross-volume flushes stay batched (lgse/strata#2080).
- A failed batch lookup is retried item by item, and a missing original never stops the move-back. A failed undo stays on top of the history, so refusing would block every older entry (lgse/strata#2080).
- Each replay records the original it replaced at its own end, so undo and redo can each restore one (lgse/strata#2080).
- An undo never records a new undo entry, so Ctrl+Z cannot toggle an item back and forth (lgse/strata#301). Its applied items feed a parallel redo stack instead (lgse/strata#1120).
- Any new forward operation clears the redo stack, matching Finder. A persistent action journal was rejected as more than platform parity needs (lgse/strata#1117, lgse/strata#1120).
- Each claimed entry keeps a bucket of the items that actually applied. Unapplied items stay on the stack for retry, applied items become the opposite entry, and a replay that applied nothing pushes nothing (lgse/strata#1120). A move replay whose conflicts were all skipped keeps its entry, as Cancel does. Otherwise Skip, once the only answer besides Cancel, would drop the entry silently (lgse/strata#2070).
- Undo and redo share one replay core parameterized by direction and reuse the provider's undo operations, with no new provider API. Copy redo therefore restores the trashed copies rather than copying again (lgse/strata#1117, lgse/strata#1120).
- Paste and the move replay share one collision rule: a file and a folder never replace one another. The presence probe reports whether an item is a folder, as the paste's own check does. A link counts as a file (lgse/strata#2017, lgse/strata#2070).
- Merge and Replace undos mix deletions and restores, which no single replay can re-apply, so they offer no redo (lgse/strata#1120).
- Copies and new items in admin folders get no entry, because their undo moves items to Trash and `admin://` has none (lgse/strata#1836, lgse/strata#1837).
- History is kept in memory only; persistence across restarts was ruled out of scope (lgse/strata#1059).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-11-07 | lgse/strata#2080 | fix | Restored the Trash-staged original when undoing a move answered with Replace, and kept the move-back when it is gone. |
| 2026-11-06 | lgse/strata#2070 | fix | Stopped undo and redo offering Replace where a file meets a folder, and kept a replay that moves nothing in the history. |
| 2026-09-23 | lgse/strata#1120 | feat | Added a shared redo stack on Ctrl+Shift+Z and Ctrl+Y, cleared by new operations and limited to items an undo applied. |
| 2026-09-18 | lgse/strata#1097 | feat | Recorded undo entries for create, copy Replace, Restore, and compression, each reversed through Trash. |

## Known gaps

- A move replay whose every item meets an item of the other kind offers only Cancel. Ctrl+Z then returns to that entry, blocking older entries until the obstacle is moved by hand. lgse/strata#2070 ([comment](https://github.com/lgse/strata/pull/2070#issuecomment-6677782710))
- A merged move cannot be undone: it adds no Undo entry, and its overwritten originals stay in Trash. lgse/strata#2078
- When the moved item is gone before Ctrl+Z, the replay drops its record, so its original stays in Trash and nothing says so. lgse/strata#2080 ([comment](https://github.com/lgse/strata/pull/2080#issuecomment-6710375362))
- Restore checks run after the move-back. A refusal, such as at a bind-mount boundary, leaves the item moved back and its original in Trash. lgse/strata#2080 ([comment](https://github.com/lgse/strata/pull/2080#issuecomment-6710375362))
- A cross-volume move-back that keeps part of its source reports "something already exists" instead of a kept report. lgse/strata#2080 ([comment](https://github.com/lgse/strata/pull/2080#issuecomment-6710375362))
- Restoring a replaced original ignores Cancel and reports no progress, which matters where a rename is unsupported and it copies. lgse/strata#2080 ([comment](https://github.com/lgse/strata/pull/2080#issuecomment-6710375362))
- After a successful move undo, `trash:///` is not among the refreshed locations, so a Trash column relies on its file monitor. lgse/strata#2080 ([comment](https://github.com/lgse/strata/pull/2080#issuecomment-6710375362))
