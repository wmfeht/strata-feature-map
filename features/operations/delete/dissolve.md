---
title: Permanent-delete dissolve animation
status: shipped
origin: {issue: null, pr: lgse/strata#626}
branch: null
reviewed_at: 86df474dc0e8352e0e2098637a017cc4c77a8c44
review: draft
code: [src/ui/browser/dissolve_delete.rs]
tests: [tests/qa/scenarios/drag_animation/delete-animation-keeps-survivors.jsonl]
related: [operations/trash/animation, operations/progress/dock]
---

## Summary

After a successful permanent delete, the deleted rows break into fragments that scatter and fade over the file view. It plays only for a delete that finishes before its progress card appears, so a slow delete never locks the window.

## Behavior

- After a successful permanent delete, the deleted rows that were visible when it began break into fragments that scatter and fade. lgse/strata#626, lgse/strata#899
- A permanent delete that succeeds before its progress card appears dissolves its rows, and no card appears. lgse/strata#1562
- A permanent delete still running when its card appears, after 350 ms or at once for 16 or more items, plays no dissolve. lgse/strata#1562 (unverified)
- While a permanent delete runs in Columns, List, or Icons, clicks reach the file view and navigating to another folder works. lgse/strata#1562
- A foreground operation that fails while a quick permanent delete runs leaves that delete's dissolve to play. lgse/strata#1539
- When a second quick permanent delete finishes while the first dissolve plays, it plays no dissolve, and the view takes clicks again afterwards. lgse/strata#1562 (unverified)
- During the dissolve, surviving rows show at their pre-delete positions, then appear at their new positions. lgse/strata#931, lgse/strata#1562 (unverified)
- "This directory is empty" stays hidden until the dissolve finishes when every item was deleted. lgse/strata#910
- A failed, partial, or cancelled deletion plays no dissolve. lgse/strata#899, lgse/strata#1490
- With animations disabled, no dissolve plays and the updated listing appears at once. lgse/strata#899, lgse/strata#931

## Design

- The dissolve snapshots visible rows before the operation mutates the model, because rows leave the model during progress (lgse/strata#895, lgse/strata#899). It uses 48 fragments per row within an 80 to 192 fragment budget, over 560 ms.
- Docking deletions into the progress dock dropped the prepared dissolve; the background completion now plays or discards it (lgse/strata#1489, lgse/strata#1490).
- Preparing the dissolve only takes the snapshot. The view is hidden and ignores input only during the 560 ms playback, so a slow deletion never locks the window (lgse/strata#1562).
- A deletion whose card is presented drops its dissolve, so a slower deletion never locks the window behind an animation (lgse/strata#1562).
- The fragment drawing shares row capture and frame timing with the Trash flight (`operations/trash/animation`) through `entry_animation.rs`, a shared module (lgse/strata#626).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |

## Known gaps

None known.
