---
title: View modes
status: shipped
origin: {issue: null, pr: lgse/strata#383}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [src/ui/browser_modes.rs, src/ui/browser_modes/events.rs, src/ui/browser/pane_header.rs, src/ui/loading_skeleton.rs, src/ui/loading_skeleton/**]
tests: [tests/e2e/scenarios/test_view_switching.py, src/ui/loading_skeleton/delay/tests.rs]
docs: []
related: [browser/search, preview/preview-panel]
---

## Summary

The three presentations of a folder, Columns, Icons, and List, and the Appearance menu and shortcuts that switch between them. Children: `browser/view-modes/columns` (Miller columns), `browser/view-modes/icons` (the thumbnail grid), `browser/view-modes/list` (the table), `browser/view-modes/sorting` (sort fields, order, and persistence), and `browser/view-modes/text-size` (interface text size).

## Behavior

### Switching

- Appearance → View lists Columns, Icons, and List; choosing one switches the window's view and closes the menu. lgse/strata#383, lgse/strata#168
- Ctrl+1, Ctrl+2, and Ctrl+3 switch to Columns, Icons, and List, including while typing in the pane filter. lgse/strata#531, lgse/strata#925
- The portal file chooser accepts the same Ctrl+1, Ctrl+2, and Ctrl+3 shortcuts. lgse/strata#877
- The Appearance button shows the current mode's icon, and the menu checks the current mode, after both menu and keyboard switches. lgse/strata#531
- The chosen mode is saved as `browser_mode` (`columns`, `icons`, or `list`) and restored at startup; saved `grid` and `explorer` values load as Icons and List. lgse/strata#383
- Choosing the mode already shown changes nothing: selection and scroll position stay. lgse/strata#266
- Switching keeps the open directory, the selection, the focused item, and the sort; leaving Columns lands on the directory Columns had active. lgse/strata#237
- Switching keeps a typed pane filter query, its open filter field, and the narrowed listing. lgse/strata#925
- After a switch the new view shows a full viewport of entries without scrolling first. lgse/strata#310

### Appearance menu

- Appearance → Density offers Compact, the default, and Airy; the choice is saved. lgse/strata#168 (unverified)
- With Sort by or Appearance open, a wheel tick outside it closes it and scrolls only the listing under the pointer; over the sidebar or other chrome it only closes. lgse/strata#590
- Wheel ticks inside an open Sort by or Appearance panel keep it open. lgse/strata#590

### Loading and names

- A directory that loads within 150 ms shows no loading skeleton; a slower load shows a skeleton shaped like the current view. lgse/strata#343, lgse/strata#584
- Skeletons cannot be selected or clicked, and loaded content, empty states, and errors replace them. lgse/strata#343
- A pending skeleton never appears after the load finishes, fails, or navigates away. lgse/strata#584
- Long filenames are middle-ellipsized in Columns rows and headings, Icons captions, and the List Name column, so the extension stays visible. lgse/strata#1143

## Design

Columns is the native Miller implementation in `ui/browser/columns.rs`. Icons and List live in `ui/browser_modes.rs`, isolated so they consume the same browser events and emit the same intents as Columns (lgse/strata#398). Collection behavior shared by all three, such as pointer selection, search sessions, and rename leases, is centralized while each mode keeps its own presentation; `docs/architecture.md` records the intentional differences (lgse/strata#1167, lgse/strata#1174).

- Only the active mode is built and updated. Hidden Grid and Explorer views cost up to 44% more enumeration time on 100,000 entries, so a switch rebuilds the target from the browser snapshot instead (lgse/strata#113, lgse/strata#237).
- Inactive panes drop their filename models (lgse/strata#1186). A cached inactive pane is reused only while its location, grouping, and List heading sort still match (lgse/strata#907).
- lgse/strata#266 rebuilt the target before showing it to avoid a blank frame. lgse/strata#310 shows it first, because a ListView rebuilt while hidden measured a one-row viewport.
- Icons and List map displayed positions to source entries through `SourceIndexMap` in O(1), so activation, drag, and selection hit the clicked entry after filtering or sorting (lgse/strata#305).
- The pane filter query is window-local: it is carried across a switch but never saved (lgse/strata#851).
- The skeleton waits a 150 ms grace period because fast loads flashed it for a few frames; showing nothing or a spinner was rejected (lgse/strata#283). Skeletons mirror each mode's loaded layout and density (lgse/strata#336).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-22 | lgse/strata#1188 | perf | Cached directory counts and released inactive models and reload buffers across modes. |
| 2026-09-22 | lgse/strata#1174 | refactor | Shared pointer selection, search sessions, and rename leases across the three modes. |
| 2026-09-19 | lgse/strata#1143 | fix | Middle-ellipsized filenames in every view so extensions stay visible. |
| 2026-09-11 | lgse/strata#805 | fix | Balanced header, row, and Icons spacing and made selected rows respond to hover. |
| 2026-09-08 | lgse/strata#603 | refactor | Split Icons and List event handling into structural, row, loading, and selection effects. |
| 2026-09-08 | lgse/strata#590 | fix | Closed Sort by and Appearance on an outside wheel tick and forwarded it to the pointed listing. |
| 2026-09-08 | lgse/strata#592 | fix | Matched the Icons and List subheaders to the compact main header. |
| 2026-09-08 | lgse/strata#584 | fix | Delayed loading skeletons by 150 ms so fast loads do not flash them. |
| 2026-09-07 | lgse/strata#531 | fix | Showed the current mode's icon on the Appearance button. |
| 2026-09-05 | lgse/strata#383 | feat | Renamed the modes Columns, Icons, and List, keeping legacy saved values readable. |
| 2026-09-05 | lgse/strata#343 | feat | Replaced the shared placeholder with a loading skeleton per view mode. |
| 2026-09-04 | lgse/strata#310 | perf | Mapped Icons and List positions in O(1) and stopped leaking panes across mode switches. |
| 2026-09-04 | lgse/strata#266 | fix | Made re-selecting the active mode a no-op. |
| 2026-09-04 | lgse/strata#237 | perf | Built and updated only the active view instead of hidden ones. |
| 2026-09-02 | lgse/strata#168 | fix | Closed the Appearance and Sort by menus when an option is chosen. |

## Known gaps

- Switching modes while typing in the pane filter keeps the query but drops keyboard focus; the fix is unmerged. lgse/strata#1441, lgse/strata#1533
- F5 and auto-refresh in Icons and List reset the keyboard cursor and scroll position and drop focus; the fix is unmerged. lgse/strata#1434, lgse/strata#1544
