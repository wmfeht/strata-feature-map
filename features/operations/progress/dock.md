---
title: Progress dock
status: shipped
origin: {issue: lgse/strata#1360, pr: lgse/strata#1393}
branch: null
reviewed_at: aee71335dfecd059b9af23efeac2ed52c43e3b19
review: reviewed
code: [src/ui/progress_dock.rs, src/ui/progress_dock/**, src/app/browser/operation_events/background.rs]
tests: [src/ui/progress_dock/tests.rs, src/ui/browser/progress/tests/minimization.rs, src/app/browser/tests/background_operations.rs]
related: [operations/delete, devices/volumes]
---

## Summary

Non-blocking progress cards in the bottom-right corner of the window for copy, compression, and deletion, so browsing continues while they run. Each card cancels only its own operation and becomes a completion notification that closes itself.

## Behavior

### Docked operations

- Copying, compressing, and deleting, to Trash or permanently, show a card in the bottom-right corner instead of a progress dialog, and the window stays usable. lgse/strata#1393
- Moving, extracting, restoring, emptying Trash, and undo or redo keep the blocking progress dialog. lgse/strata#1393 (unverified)
- A card shows the operation title, percentage, current file or first item name, destination, speed or status, and a progress bar. lgse/strata#1393
- A docked copy also shows files done of total; a compression card names the archive instead of the first item. lgse/strata#1393 (unverified)
- The destination reads "→ <path>" for a folder, "→ Trash" for Move to Trash, and "Permanent deletion" for permanent deletion. lgse/strata#1393 (unverified)
- Long file names, statuses, and destinations wrap instead of being cut off. lgse/strata#1393
- Several cards stack and update independently; the stack scrolls once it reaches 320 px. lgse/strata#1393 (unverified)
- A docked card does not blur or unblur the window, including while another dialog is open. lgse/strata#1393 (unverified)

### Cancellation

- A card's X cancels only that card's operation; other cards and the foreground operation continue. lgse/strata#1393
- After X, the card retitles to "Cancelling transfer…" for a copy or "Cancelling operation…" otherwise, and X is disabled. lgse/strata#1393 (unverified)
- Cancelling a docked transfer shows "Device may still be writing. Do not unplug until the operation stops." inside the card, with no banner or Return to browser action. lgse/strata#1393
- When a docked operation is cancelled, its card closes and an "Operation cancelled" dialog gives the completed, failed, and not-attempted counts. lgse/strata#1393 (unverified)
- When a docked operation fails, its card closes and an "Unable to complete operation" dialog shows the error. lgse/strata#1393 (unverified)
- Choosing Delete Permanently after a docked deletion partly fails, while another operation runs, shows "Another operation is active" and deletes nothing more. lgse/strata#1393 (unverified)
- Closing a tab with a docked operation running, or the window while any tab has one, shows "File operations are still active" and closes nothing. lgse/strata#1393, lgse/strata#1484

### Completion

- A finished copy, compression, or deletion retitles its card "Copy complete", "Compression complete", or "Deletion complete", with a check icon, 100%, and a Complete button. lgse/strata#1393
- A completed card counts down 5 seconds with a shrinking bar and "closing in" text, then fades out and closes. lgse/strata#1393
- Hovering or focusing a completed card pauses its countdown and shows "paused"; leaving resumes the remaining time. lgse/strata#1393
- The pin button, "Keep notification", keeps a completed card open and shows "pinned" until it is dismissed. lgse/strata#1393
- Complete or X on a completed card dismisses only that card and leaves running cards unaffected. lgse/strata#1393
- If another operation starts before a docked copy or compression finishes, the finished one does not reveal or select its result. lgse/strata#1393 (unverified)

## Design

Modal progress made the whole window unusable during long archive work. Routine progress should not stop unrelated browsing (lgse/strata#1360). lgse/strata#250 had already asked for a persistent surface that a click elsewhere cannot hide.

- lgse/strata#1360 proposed folding all progress into the Jobs dashboard. lgse/strata#1393 built a separate card dock instead, and Jobs still tracks only custom actions.
- Docking moves an operation from the browser's single foreground slot into a table keyed by request id. Another operation can then start, and late events from the docked one reach only its own card (lgse/strata#1393).
- Background completion still records copy, compression, and Trash undo, including partial and grouped undo (lgse/strata#1393).
- Docking must carry per-operation animation state. Dropping the pending dissolve broke the Shift+Delete animation until lgse/strata#1490 kept it.
- Pending-write warnings stay inside the card; the separate banner and Return to browser action from lgse/strata#1278 were removed (lgse/strata#1393).
- Drive formatting reuses the card with no Cancel; formatting cannot be aborted through it (lgse/strata#1393).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-03 | lgse/strata#1393 | fix | Moved copy, compress, and delete progress into non-blocking cards with per-card cancel. |

## Known gaps

None known.
