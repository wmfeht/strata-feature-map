---
title: Trash flight animation
status: shipped
origin: {issue: null, pr: lgse/strata#626}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [src/ui/browser/fly_to_trash.rs]
tests: [src/ui/browser/fly_to_trash/tests.rs]
related: []
---

## Summary

File icons that fly between their rows and the sidebar Trash button when items are restored from Trash. Move to Trash still prepares an inbound flight into the Trash button, but the docked deletion discards it.

## Behavior

- Move to Trash plays no flight into the Trash button. The deletion docks as a progress card when it starts, which discards the prepared flight. lgse/strata#626, lgse/strata#1393, lgse/strata#1266 (unverified)
- When a restore fails, no flight plays. lgse/strata#1266 (unverified)
- Restoring while viewing Trash lifts the icons off their rows and launches them upward with a burst. lgse/strata#1119
- Restoring into a normal folder, including Ctrl+Z, flies icons from the Trash button onto the restored rows. lgse/strata#1119
- During that flight the pre-restore listing stays frozen, and the restored rows appear when the icons land. lgse/strata#1266
- The restore flight starts only after the restore confirmation is accepted; cancelling plays nothing. lgse/strata#1119
- When restore icons leave the Trash button, the button plays a 280 ms release pulse; restores in Trash shake it instead. lgse/strata#626, lgse/strata#1119 (unverified)
- With animations disabled, no flight plays and the operation still completes. lgse/strata#1119

## Design

Flights are prepared from the rows' positions before the operation and played after its progress dialog closes, so the rows can be gone by then (lgse/strata#1266).

- At most 7 icons, sampled across the selection, fly per operation, staggered 12 ms apart up to 36 ms (lgse/strata#626).
- When every item is in Trash, the destination folder is not visible, so the icons leave upward instead of flying toward disappearing rows (lgse/strata#1118).
- Flyers are bare icons. The ring, disc, and count badge from lgse/strata#626 read as a crosshair and were removed (lgse/strata#1118).
- Fill-level and open-lid Trash icons added in lgse/strata#1119 were replaced by the single Lucide trash icon in lgse/strata#1155.
- Docking a deletion discards its prepared flight (lgse/strata#1266). Deletions dock at start since lgse/strata#1393, so only restore flights play.
- The permanent-delete dissolve added alongside this in lgse/strata#626 belongs to permanent deletion, not to Trash.

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-05 | lgse/strata#1266 | perf | Started flights only after progress closes and froze the listing until outbound restore flights land. |
| 2026-09-19 | lgse/strata#1119 | fix | Launched restores in Trash upward, played restore flights only after confirmation, and removed flyer chrome. |
| 2026-09-11 | lgse/strata#626 | feat | Added flights from rows into the sidebar Trash button and back on restore. |

## Known gaps

None known.
