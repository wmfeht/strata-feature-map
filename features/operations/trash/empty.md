---
title: Empty Trash
status: shipped
origin: {issue: null, pr: lgse/strata#53}
branch: null
reviewed_at: fb7eb0c4ee8bcb681651e56e91031ed95422e8ff
review: draft
code: [src/adapters/trash.rs, src/ui/browser/trash/empty.rs]
tests: [src/adapters/trash/tests.rs]
related: [browser/properties/size, browser/view-modes, operations/filesystem-compatibility/open-files]
---

## Summary

Permanently deleting everything in Trash from the Trash pane header or the sidebar Trash menu, after a measured confirmation. The pane-header button belongs to `browser/view-modes`.

## Behavior

### Entry points

- Choosing Empty Trash while the open Trash pane lists 0 items opens no dialog. lgse/strata#138
- The sidebar Trash menu shows "Empty Trash…" and its separator only after a probe finds an item; an empty Trash or failed probe leaves only Unpin and Properties. lgse/strata#396, lgse/strata#1025
- The sidebar menu state refreshes after trash, restore, delete, transfer, and cancelled operations, when another application changes `trash:///`, and each time the menu opens. lgse/strata#396

### Measuring and deleting

- Choosing Empty Trash shows "Measuring Trash…"; Cancel or Escape closes it and deletes nothing. lgse/strata#72
- The "Empty Trash?" confirmation reads "N items · SIZE will be reclaimed", or "At least N items · at least SIZE will be reclaimed" when measurement was truncated. lgse/strata#72
- Confirming deletes every top-level Trash item, even when measurement was truncated, behind an "Emptying Trash" progress dialog with Cancel. lgse/strata#72
- When some items cannot be deleted, the rest are still deleted and a "Completed with errors" dialog lists up to 8 errors plus a count of the others. lgse/strata#72 (unverified)
- An item whose delete fails with NotFound counts as deleted and adds no line to the "Completed with errors" dialog. lgse/strata#2093
- An item whose delete fails with a generic error but is then gone adds no line to the "Completed with errors" dialog. lgse/strata#2093
- Any item not confirmed missing after a failed or cancelled delete counts as failed and gets a "name: error" line. lgse/strata#2093

## Design

Measurement and deletion are separate passes (lgse/strata#72, lgse/strata#13).

- Measurement uses the shared directory walker, bounded to 64 levels and 300 seconds (lgse/strata#558). It keeps no entry list and is cancellable. A truncated or partly unreadable walk is reported as a lower bound.
- Deletion lists top-level entries afresh when confirmed and deletes them in batches of 64, so a stale or truncated measurement never leaves items behind.
- The sidebar row fails safe: an unknown or failed probe hides it. The probe stops after the first entry (lgse/strata#396).
- gvfs expunges a Trash item by renaming it, and reports a generic failure when the rename errors. On ntfs3, 22 of 150 deleted items were reported as failed. The likely cause is a rename that removes the item and still fails; no one has confirmed it on ntfs3 (lgse/strata#1854, lgse/strata#2093).
- A failed delete therefore counts as deleted only when the item is confirmed absent: NotFound, or a `NOFOLLOW_SYMLINKS` probe returning NotFound. An item still present stays a failure (lgse/strata#1854, lgse/strata#2093).
- Keeping the sidebar row visible but disabled was rejected as clutter; removing it was rejected as inconvenient (lgse/strata#367).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-11-08 | lgse/strata#2093 | fix | Stopped counting Trash items that a failed delete already removed as failures. |
| 2026-09-06 | lgse/strata#396 | feat | Hid Empty Trash… in the sidebar menu until Trash is confirmed non-empty. |
| 2026-09-01 | lgse/strata#138 | fix | Disabled the header button while Trash is empty so the measuring dialog no longer flashes. |
| 2026-09-01 | lgse/strata#72 | perf | Bounded and made cancellable the Trash measurement, and emptied Trash in a separate full pass. |
| 2026-08-31 | lgse/strata#53 | feat | Added an Empty Trash button to the Trash pane header, since the sidebar menu was hard to find. |

## Known gaps

None known.
