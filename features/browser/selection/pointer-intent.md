---
title: Pointer intent
status: shipped
origin: {issue: lgse/strata#517, pr: lgse/strata#522}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: reviewed
code: [src/ui/pointer.rs]
tests: [src/ui/pointer/**, tests/e2e/scenarios/test_pointer_intent.py]
related: [operations/drag-and-drop, preview/preview-panel, operations/rename]
---

## Summary

How a press on an entry is read in Columns, Icons, and List: as a click, a file drag, or the start of a marquee. Item content and blank row space have separate hit regions, and previews wait for a completed click.

## Behavior

### Hit regions

- On an unselected entry, a drag from the icon or rendered filename starts a file drag. lgse/strata#522
- On an unselected entry, a drag from blank row space beside the filename starts a marquee. lgse/strata#522, lgse/strata#1336
- In Icons, the gutter beside the thumbnail inside a card is blank space for marquee. lgse/strata#522
- On a selected entry, a drag from blank row or card space starts a file drag of the selection. lgse/strata#1336
- In List, unused Name-column space and its row padding are blank; other column cells count as item content. lgse/strata#838
- Ctrl+click and Shift+click on blank row space still toggle and range. lgse/strata#522

### Clicks and previews

- With single-click previews on, a press held on a file opens no preview; release without dragging opens it. lgse/strata#522
- A press that crosses the drag threshold never opens a preview, even after the drop. lgse/strata#522
- A press that crossed the drag threshold does not activate on release, even if the pointer returns to its start. lgse/strata#522 (unverified)
- A press on an entry whose row was recycled during the press does not activate on release. lgse/strata#522 (unverified)

### Drag selection

- Pressing and dragging an unselected entry selects it on press and deselects the previous selection. lgse/strata#789
- Pressing an entry inside a multi-selection without Ctrl or Shift keeps the group, so the drag carries every selected entry. lgse/strata#789
- Ctrl-drag from an entry's icon or name copies it and adds it to the selection. lgse/strata#623
- Shift-drag from an entry's icon or name moves it. lgse/strata#623

## Design

Before lgse/strata#517, a full column left no blank space to start a marquee, and a file drag opened the one-click preview over its own drop target.

- Labels expand to fill their rows, so only rendered text counts as content; thumbnails, images, and the Icons caption are explicit content regions (lgse/strata#522).
- Selected rows claim their whole allocation for file drag; unselected rows claim only content, leaving blank space for marquee (lgse/strata#1335).
- Rejected: treating the whole row as a drag source, which leaves no marquee origin, and modifier-only selection (lgse/strata#517).
- Activation and previews run on release, never on press, so a press can still become a drag or marquee (lgse/strata#522).
- The modifier-click gesture on content is grouped with the row's drag source. Claiming one would otherwise deny the other and block modifier drags (lgse/strata#623).
- Marquee treats the Icons frame padding as gutter; hover, click focus, and drag treat it as content (lgse/strata#998).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-29 | lgse/strata#1336 | fix | Routed blank-space drags by selection: unselected rows marquee, selected rows drag files. |
| 2026-09-10 | lgse/strata#789 | fix | Selected an unselected entry on press so a drag highlights its real source. |
| 2026-09-07 | lgse/strata#522 | fix | Split content drags from blank-space marquees and deferred previews to completed clicks in every view. |

## Known gaps

None known.
