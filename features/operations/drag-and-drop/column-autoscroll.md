---
title: Columns drag autoscroll
status: shipped
origin: {issue: lgse/strata#1108, pr: lgse/strata#1095}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: reviewed
code: [src/ui/browser/columns/drag_scroll.rs]
tests: [src/ui/browser/columns/drag_scroll/tests.rs]
related: []
---

## Summary

Edge autoscrolling while a file drag is held over Columns view, so off-screen columns and listing entries can be reached without ending the drag, and the column under the drag is highlighted as the destination.

## Behavior

- Holding a file drag within 44 px of the column strip's left or right edge scrolls the columns toward that edge. lgse/strata#1095
- Holding a file drag within 44 px of the top or bottom edge of the listing under the pointer scrolls that listing. lgse/strata#1095
- Only drags offering a file list or `text/uri-list` autoscroll or highlight a column. lgse/strata#1095 (unverified)
- Scroll speed peaks within 16 px of the edge, at 720 px/s horizontally and 520 px/s vertically. lgse/strata#1095 (unverified)
- Scrolling starts at 35% of that speed and reaches full speed after 350 ms in the same direction. lgse/strata#1095 (unverified)
- Autoscroll stops when the drag leaves the strip, drops, or ends, or the content cannot scroll further. lgse/strata#1095 (unverified)
- The column under a held file drag shows an accent wash and ring, including a column just revealed by autoscroll. lgse/strata#1208
- The highlight stays while autoscroll is at its limit and clears when the drag leaves the column. lgse/strata#1208
- Dropping onto a partially visible column moves the file there, and the strip does not scroll back to the source column. lgse/strata#1095

## Design

Blank strip space has no drop target, so a drop motion controller on the columns scroller tracks the drag instead (lgse/strata#1095).

- Scroll-to-focus is disabled on the columns scroller, so drops and filesystem notifications do not jump back to the source column (lgse/strata#1095).
- Column peek targets check the drag threshold, so a drag released over a peeked column is not treated as a reveal click (lgse/strata#1095).
- GTK does not re-evaluate drop targets when content scrolls under a parked pointer, so the autoscroll tracks and highlights the hovered column itself (lgse/strata#1208).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-18 | lgse/strata#1095 | feat | Added horizontal and vertical edge autoscroll during Columns file drags. |

## Known gaps

None known.
