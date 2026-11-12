---
title: Pointer intent
status: shipped
origin: {issue: lgse/strata#517, pr: lgse/strata#522}
branch: null
reviewed_at: 5f17c9fdc8967e1b4ba8aaf8de113b46d824b0dd
review: draft
code: [src/ui/pointer.rs, src/ui/collection_interaction/double_press.rs]
tests: [src/ui/pointer/**, tests/qa/scenarios/pointer_intent]
related: [operations/drag-and-drop, preview/preview-panel, operations/rename]
---

## Summary

How a press on an entry is read in Columns, Icons, and List: as a click, a file drag, or the start of a marquee. Item content and blank row space have separate hit regions, and previews wait for a completed click.

## Behavior

### Hit regions

- On an unselected entry, a drag from the icon or rendered filename starts a file drag. lgse/strata#522
- On an unselected entry, a drag from blank row space beside the filename starts a marquee. lgse/strata#522, lgse/strata#1336
- In Icons, the gutter beside the thumbnail inside a card is blank space for marquee. lgse/strata#522
- In List, only the icon and rendered filename are item content. Metadata cells, unused Name space, and row padding are blank, wherever Name sits. lgse/strata#838, lgse/strata#1651, lgse/strata#2108
- Ctrl+click and Shift+click on blank row space still toggle and range. lgse/strata#522

### Clicks and previews

- With single-click previews on, a press held on a file opens no preview; release without dragging opens it. lgse/strata#522
- A press that crosses the drag threshold never opens a preview, even after the drop. lgse/strata#522
- A press that crossed the drag threshold does not activate on release, including a double-click's second press. lgse/strata#522, lgse/strata#2096
- That holds even if the pointer returns to its start before release. lgse/strata#522 (unverified)
- A press on an entry whose row was recycled during the press does not activate on release, including a second press. lgse/strata#522, lgse/strata#2096

### Second press

- With double-click activation, tap a file or folder's icon or filename once, then hold the second press there: nothing opens or launches while it is held. lgse/strata#2095, lgse/strata#2096, lgse/strata#2108
- Moving that held second press past the drag threshold starts a file drag; dropping it on a folder moves the item there and opens nothing. lgse/strata#2095, lgse/strata#2096
- A Ctrl or Shift double-click on an entry still opens a folder or launches a file. lgse/strata#2096

### Drag selection

- Pressing and dragging an unselected entry selects it on press and deselects the previous selection. lgse/strata#789
- Pressing an entry inside a multi-selection without Ctrl or Shift keeps the group, so the drag carries every selected entry. lgse/strata#789
- Ctrl-drag from an entry's icon or name copies it and adds it to the selection. lgse/strata#623
- Shift-drag from an entry's icon or name moves it. lgse/strata#623

## Design

Before lgse/strata#517, a full column left no blank space to start a marquee, and a file drag opened the one-click preview over its own drop target.

- Labels expand to fill their rows, so only rendered text counts as content; thumbnails, images, and the Icons caption are explicit content regions (lgse/strata#522).
- Unselected rows claim only content for file drag, leaving blank space for marquee (lgse/strata#1335). Outside List, a selected row claims its whole allocation, but only when it hosts a drag source (lgse/strata#2108, `docs/architecture.md`).
- List keeps one content-only region before and after selection. Drag sources and marquee ownership share that test, and reordered columns keep it (lgse/strata#2108, `docs/architecture.md`).
- Rejected: treating the whole row as a drag source, which leaves no marquee origin, and modifier-only selection (lgse/strata#517).
- Activation and previews run on release, never on press, so a press can still become a drag or marquee (lgse/strata#522). That now holds for a double-click's second press too (lgse/strata#2096). Release activation rejects cancelled gestures, drag motion, and recycled items (`docs/architecture.md`).
- GTK's item widget activated and claimed the second press before drag intent was known. The row's own gesture group, shared with its drag source and release activation, now claims it (lgse/strata#2095, lgse/strata#2096, `docs/architecture.md`).
- Native collection activation bypassed the movement-aware release guards, so a held second tap launched on press (lgse/strata#2095).
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
