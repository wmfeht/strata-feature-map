---
title: Undoing a replacing move
status: shipped
origin: {issue: lgse/strata#2077, pr: lgse/strata#2080}
branch: null
reviewed_at: 5738aad808ea4cc4671516bc569d85f862664809
review: draft
code: [src/adapters/local_operations/undo_move/replaced.rs]
tests: [src/adapters/local_operations/tests/undo/replacements.rs, src/adapters/local_operations/tests/undo/replacements/**]
related: [operations/clipboard/conflicts, operations/trash/restore]
---

## Summary

How undo and redo bring back the original that a move answered with Replace sent to Trash. Before this, Ctrl+Z moved the item back and left the original in Trash, which the issue reported as data loss. It serves anyone who undoes a move after answering Replace.

## Behavior

### Undo

- Ctrl+Z after a move answered with Replace moves the item back and restores the replaced original from Trash, for files and folders. lgse/strata#2080
- If that original is no longer in Trash, the item still moves back. The undo reports "One or more recently trashed items are no longer available". lgse/strata#2080
- The next Ctrl+Z after that report undoes the older entry. lgse/strata#2080
- An item that appears at the vacated path before the restore is kept; its original stays in Trash and the undo reports the failure. lgse/strata#2080
- Cancelling such an undo restores the originals only of items already moved back. A failed or unattempted item leaves its original in Trash. lgse/strata#2080
- After a cross-volume move-back, the original is restored only once the move-back is flushed. lgse/strata#2080
- Undoing a Replace move onto a non-local destination, which stages no original in Trash, only moves the item back. lgse/strata#2080

### Redo

- Ctrl+Shift+Z after undoing a move answered with Replace asks before replacing the restored original. After Replace, the next Ctrl+Z restores that original again. lgse/strata#2080
- When a move undo answers Replace at the original name, Ctrl+Shift+Z moves the item forward and restores the item that undo replaced. lgse/strata#2080 (unverified)

## Design

- A move record keeps the Trash identity of the original its Replace staged. Before lgse/strata#2080 the record dropped it, so undoing a replacing move left the original in Trash (lgse/strata#2077).
- That undo looks up all originals in one Trash scan and restores them after the move-back batches settle, so cross-volume flushes stay batched (lgse/strata#2080).
- A failed batch lookup is retried item by item, and a missing original never stops the move-back. A failed undo stays on top of the history, so refusing would block every older entry (lgse/strata#2080).
- Each replay records the original it replaced at its own end, so undo and redo can each restore one (lgse/strata#2080).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |

## Known gaps

- Restore checks run after the move-back. A refusal, such as at a bind-mount boundary, leaves the item moved back and its original in Trash. lgse/strata#2080 ([comment](https://github.com/lgse/strata/pull/2080#issuecomment-6710375362))
- Restoring a replaced original ignores Cancel and reports no progress, which matters where a rename is unsupported and it copies. lgse/strata#2080 ([comment](https://github.com/lgse/strata/pull/2080#issuecomment-6710375362))
