---
title: Operation progress and cancellation
status: shipped
origin: {issue: lgse/strata#11, pr: lgse/strata#75}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [src/ui/browser/progress.rs, src/ui/browser/progress/context.rs, src/ui/browser/progress/presentation.rs]
tests: [src/ui/browser/progress/tests.rs, src/app/browser/operation_events/tests.rs, src/adapters/local_operations/tests/progress.rs, src/adapters/local_operations/tests/sync.rs]
docs: []
related: [operations/clipboard, operations/delete, operations/archives]
---

## Summary

The progress and cancellation UI shared by file operations: the blocking progress dialog, transfer byte and speed reporting, and the result shown after Cancel. Children: `operations/progress/dock` (non-blocking cards for copy, compression, and deletion) and `operations/progress/jobs` (the custom-action job queue and Jobs dashboard).

## Behavior

### Progress dialog

- An operation on fewer than 16 items shows no progress dialog for its first 350 ms, and none at all if it finishes sooner. lgse/strata#228
- An operation on 16 or more items, or with an unknown item count, shows its progress dialog immediately. lgse/strata#228
- The progress dialog's subtitle reads "Cancelling will not undo completed changes". lgse/strata#75
- Clicking outside the progress dialog leaves the dialog, its progress, and Cancel visible until the operation finishes or cancellation completes. lgse/strata#491
- Escape in the progress dialog acts as Cancel. lgse/strata#491 (unverified)

### Transfer progress

- During a copy or move with a known byte total, the bar advances as bytes are written, not only after each item. lgse/strata#369
- When the byte total is unknown, the bar pulses and reads "Preparing…" until bytes move, then "Transferring…". lgse/strata#369
- A tree of only empty files or folders advances by item count and reaches 100% only when every item is copied. lgse/strata#369
- The transfer view shows the percentage, transferred and total bytes, "N of M files" with the current file name, and the speed with time left. lgse/strata#1278
- Until a speed is measured, the speed field reads "Calculating speed…". lgse/strata#1278
- A copy onto removable media shows "Writing to device…" and is not reported done until the filesystem flush returns. lgse/strata#1193

### Cancellation

- Cancel during a transfer retitles the dialog "Cancelling transfer…", warns that the device may still be writing, and disables the button as "Cancellation requested". lgse/strata#1278
- If the transfer has not stopped 8 seconds after Cancel, the title becomes "Device not responding" and the subtitle warns not to unplug the device. lgse/strata#1278
- While a transfer cancellation is pending, starting another file operation shows "Transfer cancellation pending" and the operation does not start. lgse/strata#1278
- Cancel on an operation that is not a transfer retitles the dialog "Cancelling operation…" and disables Cancel. lgse/strata#1393 (unverified)
- After cancellation, an "Operation cancelled" dialog gives the counts of items completed, failed, and not attempted, then "Completed changes were not reverted." lgse/strata#75
- After cancellation, every affected source and destination folder refreshes to its on-disk state. lgse/strata#75
- An item that GIO completes as Cancel arrives is counted as completed, not cancelled. lgse/strata#75

## Design

The modal progress dialog predates the PR history. lgse/strata#398 moved it out of the browser view into `src/ui/browser/progress.rs`.

- Cancellation uses explicit GIO cancellables instead of aborting the task, so every operation reports completed, failed, and not-attempted items. The UI must never imply that completed destructive changes were reverted (lgse/strata#11, lgse/strata#75).
- Quick operations wait 350 ms before showing progress so the dialog does not flash. Large and unbounded operations show it at once (lgse/strata#228).
- Progress is owned by the operation until a terminal event. Click-away dismissal had hidden a running operation and its only Cancel (lgse/strata#250, lgse/strata#412, lgse/strata#491).
- Byte progress comes from GIO callbacks. When totals are unknown the bar pulses rather than showing an invented fraction (lgse/strata#249, lgse/strata#369).
- Speed is a weighted average of samples at least 250 ms apart: 60% previous, 40% new (lgse/strata#1278). Transfer redraws are throttled to one per 33 ms (lgse/strata#1266).
- Stopping Strata's writes does not make earlier writes safe to unplug. A stalled cancel therefore never claims the device is safe, and new file operations are refused until the pending transfer resolves (lgse/strata#1278).
- Copy, compression, and deletion leave this dialog for the progress dock; other operations keep it (lgse/strata#1393).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-07 | lgse/strata#491 | fix | Kept progress and Cancel visible after backdrop clicks until the operation ends. |
| 2026-09-05 | lgse/strata#369 | fix | Reported live byte progress for copies and moves, pulsing when totals are unknown. |
| 2026-09-02 | lgse/strata#75 | fix | Replaced task abort with GIO cancellation and reported completed, failed, and unattempted items. |

## Known gaps

- Closing the progress dialog does not return keyboard focus to the file list; the fix merged after `reviewed_at`. lgse/strata#1430, lgse/strata#1533
