---
title: Entry hover tooltips
status: shipped
origin: {issue: lgse/strata#2462, pr: lgse/strata#2533}
branch: null
reviewed_at: 7cc1543e9c4bc00e68f1525b0b3d47f4624bc375
review: draft
code: [src/ui/entry_tooltip.rs]
tests: [src/ui/entry_tooltip/tests.rs]
related: [browser/view-modes/icons, browser/view-modes/columns, browser/view-modes/list, app/accessibility, settings/preferences/date-format]
---

## Summary

The shared hover tooltip that shows an entry's full name once the pointer rests on an Icons card, a Columns row, or a List name cell. In Icons and Columns it adds the modified date. It is for reading names the views truncate. Each view decides where on its card or row the tooltip applies.

## Behavior

### Rest delay

- An entry tooltip shows only after the pointer rests 900 ms on the card, row, or name cell. lgse/strata#1553, lgse/strata#2533
- Moving more than 4 px or leaving the card, row, or cell restarts the wait. Sweeping across the grid or the rows shows no tooltips. lgse/strata#1553, lgse/strata#2533
- Pressing any mouse button cancels the wait until the pointer moves again, so a click then holding still shows no tooltip. lgse/strata#1553, lgse/strata#2533 (unverified)
- Keyboard focus on a card or row shows no entry tooltip, including during 10xer `j`/`k` and arrow navigation. lgse/strata#1553, lgse/strata#2533

### Text

- With a modified date to show, the tooltip reads the name over the date as the Date format preference renders it. This holds whether or not the name is truncated. lgse/strata#2533
- With no date to show, a truncated name shows alone in the tooltip, and a name that fits shows none. lgse/strata#2533

## Design

The issue asked for a way to read truncated names without F2 or Properties. A contributor offered a hover or the name in the footer ([comment](https://github.com/lgse/strata/issues/2462#issuecomment-6889915109)). lgse/strata#2533 did both; the footer half belongs to `app/shortcut-reference`.

- Upstream AGENTS.md allows tooltips only on icon-only buttons. lgse/strata#1553 made Icons names an exception on condition of a longer delay than GTK's. The owner extended it to List and Columns rows, noting 10xer mode may need a different one ([comment](https://github.com/lgse/strata/issues/2462#issuecomment-6908936616)).
- The pointer must rest because GTK4's own hover delay drops to 60 ms once any tooltip shows. That would flash names entry by entry while sweeping a listing (lgse/strata#1553, lgse/strata#2533).
- One installer and one text rule serve all three views. The Icons card's private rest state never saw pointer motion, so only the shared installer now checks the rest ([comment](https://github.com/lgse/strata/pull/2533#issuecomment-6920830360)).
- A view supplies the text when GTK queries the tooltip. The date comes from a hidden label filled by the existing date formatting, which is reused rather than duplicated (lgse/strata#2533).
- Only views without a Modified column add the date. List shows the name alone, without metadata its row already shows (lgse/strata#2533).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-11-16 | lgse/strata#2533 | feat | Shared the Icons rest-delay tooltip with Columns rows and List names, adding the modified date in Icons and Columns, so truncated names can be read. |

## Known gaps

None known.
