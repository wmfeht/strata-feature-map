---
title: Marquee selection
status: shipped
origin: {issue: lgse/strata#189, pr: lgse/strata#203}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [src/ui/marquee.rs]
tests: [src/ui/marquee/tests.rs, tests/e2e/scenarios/test_marquee_scrolling.py]
related: [integration/portal-file-chooser]
---

## Summary

Rubber-band selection: dragging from blank space draws a band and selects every entry it crosses, in Columns, Icons, and List. The drag may start in the pane or on inert chrome beside it, and auto-scrolls long listings.

## Behavior

### Starting a marquee

- A drag from blank pane space draws a band from the press point and selects every entry it crosses. lgse/strata#203
- A drag from blank sidebar space, below the last place, selects in the pane nearest the sidebar: the Icons or List pane, or the first open column. lgse/strata#203
- A drag from blank space in a pane header, List's heading strip, a Columns header, or beside the last column starts a marquee. lgse/strata#203
- A press on a button, entry, slider, scrollbar, or sidebar place keeps that control's own behavior and starts no marquee. lgse/strata#203
- A drag from a pane corner at text sizes 13 and 28 selects files and leaves the sidebar width unchanged. lgse/strata#838
- During a sidebar-started marquee, the target pane takes keyboard focus, so Ctrl+C copies the marqueed files. lgse/strata#838
- Taking that focus keeps a scrolled list's position rather than jumping to an off-screen cursor. lgse/strata#838
- Holding Alt starts a marquee even when the press lands on an entry. lgse/strata#203 (unverified)

### Selecting

- A plain marquee replaces the selection with the entries under the band. lgse/strata#522 (unverified)
- A Ctrl-marquee toggles each crossed entry relative to the selection at press. lgse/strata#522
- A Shift-marquee adds the crossed entries to the selection at press. lgse/strata#522 (unverified)
- The selection survives pointer movement after release. lgse/strata#203
- Marquee selection never opens or retargets quick preview, including with single-click previews on. lgse/strata#522, lgse/strata#1122
- Marquee selection works on Ctrl+F filter results. lgse/strata#1018

### Scrolling

- Holding the pointer near a viewport edge scrolls the listing and extends the selection each frame. lgse/strata#203
- Wheel scrolling during a held marquee extends the selection without moving the anchor. lgse/strata#522
- Entries selected before they scrolled out of view stay selected; entries above the original anchor stay unselected. lgse/strata#522
- The band is clipped to the pane, so a drag starting above or beside it never paints outside. lgse/strata#203

## Design

One shared module replaced separate Columns and Icons/List implementations so chrome origins could feed any view (lgse/strata#203).

- GTK keeps an event sequence on the widget that claimed it, so a drag begun on chrome continues into the list without rerouting (lgse/strata#203).
- The anchor uses content coordinates and the pointer the scrolled window's, so the band stays on the content while it scrolls (lgse/strata#203).
- Row geometry is kept after virtualization unbinds a row, so scrolling back or retracting still resolves hits on rows no longer bound (lgse/strata#522).
- Auto-scroll starts within 28 px of an edge and steps up to 24 px every 16 ms. Axes that cannot scroll contribute nothing (lgse/strata#203).
- A selection-update flag marks marquee changes so the preview ignores them while keyboard and explicit previews still work (lgse/strata#1122).
- Rejected: a modifier on rows (conflicts with file drag) and permanent blank space in the viewport (wastes space) (lgse/strata#189).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-18 | lgse/strata#1122 | fix | Stopped marquee selection from opening or retargeting quick preview. |
| 2026-09-03 | lgse/strata#203 | feat | Shared the marquee across views and let drags start from sidebar and header chrome, with edge auto-scroll. |

## Known gaps

None known.
