---
title: Empty Trash
status: shipped
origin: {issue: null, pr: lgse/strata#53}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [src/adapters/trash.rs]
tests: [src/adapters/trash/tests.rs]
related: []
---

## Summary

Permanently deleting everything in Trash from the Trash pane header or the sidebar Trash menu, after a measured confirmation.

## Behavior

### Entry points

- The pane header shows an Empty Trash button only at `trash:///`, not in Trash subfolders or other locations. lgse/strata#53
- The header button is insensitive while the Trash pane lists 0 items and becomes sensitive when an item appears. lgse/strata#138
- Choosing Empty Trash while the open Trash pane lists 0 items opens no dialog. lgse/strata#138
- The sidebar Trash menu shows "Empty Trash…" and its separator only after a probe finds an item; an empty Trash or failed probe leaves only Properties. lgse/strata#396
- The sidebar menu state refreshes after trash, restore, delete, transfer, and cancelled operations, and each time the menu opens. lgse/strata#396

### Measuring and deleting

- Choosing Empty Trash shows "Measuring Trash…"; Cancel or Escape closes it and deletes nothing. lgse/strata#72
- The "Empty Trash?" confirmation shows the item count and size to be reclaimed, prefixed "At least" when measurement was truncated. lgse/strata#72
- Confirming deletes every top-level Trash item, even when measurement was truncated, behind a progress dialog with Cancel. lgse/strata#72
- When some items cannot be deleted, the rest are still deleted and a dialog lists up to 8 errors plus a count of the others. lgse/strata#72 (unverified)

## Design

Measurement and deletion are separate passes (lgse/strata#72, lgse/strata#13).

- Measurement walks the tree within depth and time budgets, keeps no entry list, and is cancellable. A truncated walk is reported as a lower bound.
- Deletion lists top-level entries afresh when confirmed and deletes them in batches of 64, so a stale or truncated measurement never leaves items behind.
- The sidebar row fails safe: an unknown or failed probe hides it. The probe stops after the first entry (lgse/strata#396).
- Keeping the sidebar row visible but disabled was rejected as clutter; removing it was rejected as inconvenient (lgse/strata#367).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-06 | lgse/strata#396 | feat | Hid Empty Trash… in the sidebar menu until Trash is confirmed non-empty. |
| 2026-09-01 | lgse/strata#138 | fix | Disabled the header button while Trash is empty so the measuring dialog no longer flashes. |
| 2026-09-01 | lgse/strata#72 | perf | Bounded and made cancellable the Trash measurement, and emptied Trash in a separate full pass. |
| 2026-08-31 | lgse/strata#53 | feat | Added an Empty Trash button to the Trash pane header, since the sidebar menu was hard to find. |

## Known gaps

None known.
