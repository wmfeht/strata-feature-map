---
title: View modes
status: shipped
origin: {issue: null, pr: lgse/strata#383}
branch: null
reviewed_at: be3343a5992a2a5497b1a2ee7faa525be18e988f
review: draft
code: [src/ui/browser_modes.rs, src/ui/browser_modes/events.rs, src/ui/browser/pane_header.rs, src/ui/browser/presentation.rs, src/ui/loading_skeleton.rs, src/ui/loading_skeleton/**]
tests: [tests/qa/scenarios/view_switching, tests/qa/mutations/view-switching.patch, src/ui/loading_skeleton/delay/tests.rs, src/ui/browser_modes/tests.rs, src/ui/browser/presentation/tests.rs]
docs: [docs/architecture.md, site/src/reference/keyboard-navigation.md]
related: [browser/search, preview/preview-panel, browser/view-modes/density]
---

## Summary

The three presentations of a folder, Columns, Icons, and List, and the Appearance menu and shortcuts that switch between them. Children: `browser/view-modes/columns` (Miller columns), `browser/view-modes/icons` (the thumbnail grid), `browser/view-modes/list` (the table, with its column layout), `browser/view-modes/sorting` (sort fields, order, and persistence), and `browser/view-modes/folder-views` (per-folder sort and thumbnail size). `browser/view-modes/density` covers the Frame and Content density sliders. `browser/view-modes/text-size` covers interface text size, `browser/view-modes/thumbnail-size` the Icons thumbnail size shortcuts, and `browser/view-modes/position-restore` the Icons and List position on return and refresh.

## Behavior

### Switching

- The Appearance menu's VIEW section lists Columns, Icons, and List; choosing one switches the view and closes the menu. lgse/strata#383, lgse/strata#168
- Ctrl+1, Ctrl+2, and Ctrl+3 switch to Columns, Icons, and List, including while typing in the pane filter. lgse/strata#531, lgse/strata#925
- Ctrl+1, Ctrl+2, and Ctrl+3 count the digit row by position: on French AZERTY, Ctrl+&, Ctrl+é, and Ctrl+" switch views. lgse/strata#1576
- Ctrl+Super+1, Ctrl+Super+2, or Ctrl+Super+3 does not switch views. lgse/strata#1576
- The portal file chooser accepts the same Ctrl+1, Ctrl+2, and Ctrl+3 shortcuts. lgse/strata#877
- The Appearance button shows the current mode's icon, and the menu checks the current mode, after both menu and keyboard switches. lgse/strata#531
- The chosen mode is saved as `browser_mode` (`columns`, `icons`, or `list`) and restored at startup; saved `grid` and `explorer` values load as Icons and List. lgse/strata#383
- Choosing the mode already shown changes nothing: selection and scroll position stay. lgse/strata#266
- Switching keeps the open directory, the selection, the focused item, and the sort; leaving Columns lands on the directory Columns had active. lgse/strata#237
- Switching keeps a typed pane filter query, its open filter field, and the narrowed listing. lgse/strata#925
- After a switch the new view shows a full viewport of entries without scrolling first. lgse/strata#310

### Appearance menu

- Columns, Icons, and List are radio menu items, and Group by file type is a check menu item. lgse/strata#1467, lgse/strata#1544, lgse/strata#1776
- Each option's accessible checked state matches its check icon, including after Ctrl+1 to Ctrl+3 and switches in other windows. lgse/strata#1467, lgse/strata#1544
- With Sort by or Appearance open, a wheel tick outside it closes it and scrolls only the listing under the pointer; over the sidebar or other chrome it only closes. lgse/strata#590
- Wheel ticks inside an open Sort by or Appearance panel keep it open. lgse/strata#590

### Content density

- At Content Airy, Columns and List rows have a 42 px minimum height and 8 px vertical margins; Columns row content keeps 4 px. lgse/strata#168 (unverified)
- At Content Airy, Icons has 5 px grid padding, 3 px cell margins, and 5 by 7 px card padding. lgse/strata#168, lgse/strata#747 (unverified)
- A Custom Content value N sets N px vertical margins on Columns and List row children, and min(N, 4) px on Columns row content. lgse/strata#1776 (unverified)
- A Custom Content value scales row minimum height, Icons grid padding, cell margins, and card padding linearly through the Compact and Airy values. Results clamp at 0 and round. lgse/strata#1776
- Icons shows at most 20 columns at Content Compact and at most 16 at Airy. lgse/strata#1776
- A Custom Content value below 8 px caps Icons at 20 columns; 8 px or more caps it at 16. lgse/strata#1776 (unverified)

### Loading and names

- A directory that loads within 150 ms shows no loading skeleton; a slower load shows a skeleton shaped like the current view. lgse/strata#343, lgse/strata#584
- Skeletons cannot be selected or clicked, and loaded content, empty states, and errors replace them. lgse/strata#343
- A pending skeleton never appears after the load finishes, fails, or navigates away. lgse/strata#584
- Entering an empty, unreadable, or still-loading folder gives keyboard focus to the pane itself. lgse/strata#1466, lgse/strata#1533
- The focused pane draws a 2 px accent focus ring only while GTK shows focus, as after keyboard input. lgse/strata#1466, lgse/strata#1533 (unverified)
- When entries appear in a folder whose pane held focus, focus moves to the keyboard cursor row. lgse/strata#1466, lgse/strata#1533
- F5 keeps focus on the pane while rows are hidden and returns it to the cursor row when they return. lgse/strata#1466, lgse/strata#1533, lgse/strata#1729
- In a scrolled List, after a rename moves a file from the bottom to near the top, each Down advances selection and focus. lgse/strata#1890
- In List and Icons, a deferred cursor restore after a row splice or Page Down is dropped once a key moves the cursor. lgse/strata#1890 (unverified)
- In List and Icons, after Ctrl+H hides hidden files, renaming the focused file to a dot name moves the cursor to its visible neighbor. lgse/strata#1874 (unverified)
- Opening a populated folder that loads within the 150 ms grace period never moves focus to the pane. lgse/strata#1466, lgse/strata#1533 (unverified)
- While entries show, the pane itself is not a Tab stop. lgse/strata#1431, lgse/strata#1533
- In List, cut styling, hidden-file dimming, and live dates of visible rows refresh once scrolling has been still for 25 ms. lgse/strata#1673
- In Icons, cut styling, hidden-file dimming, and accessible descriptions of visible cards refresh once scrolling has been still for 25 ms. lgse/strata#1673 (unverified)
- After 10 s without progress on a folder's mount, "Not responding. This list may be out of date." shows above its listing in Columns, Icons, and List. lgse/strata#1729
- The last listing stays in view under the notice. The notice also shows over a stuck first load, never over an error page. lgse/strata#1729
- The notice clears as soon as a request on that mount answers. lgse/strata#1729
- The notice has the accessible role status. lgse/strata#1729 (unverified)
- Long filenames are middle-ellipsized in Columns rows and headings, Icons captions, and the List Name column, so the extension stays visible. lgse/strata#1143

## Design

Columns is the native Miller implementation in `ui/browser/columns.rs`. Icons and List live in `ui/browser_modes.rs`, isolated so they consume the same browser events and emit the same intents as Columns (lgse/strata#398). Collection behavior shared by all three, such as pointer selection, search sessions, and rename leases, is centralized while each mode keeps its own presentation; `docs/architecture.md` records the intentional differences (lgse/strata#1167, lgse/strata#1174).

- Only the active mode is built and updated. Hidden Grid and Explorer views cost up to 44% more enumeration time on 100,000 entries, so a switch rebuilds the target from the browser snapshot instead (lgse/strata#113, lgse/strata#237).
- Inactive panes drop their filename models (lgse/strata#1186). A cached inactive pane is reused only while its location, grouping, and List heading sort still match (lgse/strata#907).
- lgse/strata#266 rebuilt the target before showing it to avoid a blank frame. lgse/strata#310 shows it first, because a ListView rebuilt while hidden measured a one-row viewport.
- Icons and List map displayed positions to source entries through `SourceIndexMap` in O(1), so activation, drag, and selection hit the clicked entry after filtering or sorting (lgse/strata#305).
- The List type-group sorter re-sorts only when a sort preference changes. Spliced rows rely on GTK's sorted insertion, and each row's model value carries its type group, so comparisons neither allocate nor guess MIME types (lgse/strata#1791, lgse/strata#1792).
- The pane filter query is window-local: it is carried across a switch but never saved (lgse/strata#851).
- An empty, unreadable, or loading folder focuses the existing page stack rather than its status label. Up, Delete, and the context menu already key off that stack. It is focusable only off the content page, so populated listings gain no unnamed Tab stop (lgse/strata#1466).
- GTK moves focus off a removed or hidden row at the next paint. The pane settles focus first, so a reload never sends it out of the listing (lgse/strata#1466, lgse/strata#1533).
- lgse/strata#1081 moved the deferred row refresh to the next frame, so during continuous scrolling it ran every frame or two and restyled every List row. lgse/strata#1673 settles 25 ms after the last scroll, never sooner than two frames, so a slow machine does not settle between frames of one scroll (lgse/strata#1671, lgse/strata#1673).
- The frame rate counts only when the frame clock's history all follows the scroll's start. `fps()` averages idle gaps, which would stretch the floor by seconds once the clock stops while idle (lgse/strata#1673, lgse/strata#1677).
- A focus request for a pane showing filter or search results goes to the results' cursor, not the hidden listing behind them (lgse/strata#1549, lgse/strata#1611).
- The skeleton waits a 150 ms grace period because fast loads flashed it for a few frames; showing nothing or a spinner was rejected (lgse/strata#283). Skeletons mirror each mode's loaded layout and density (lgse/strata#336).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-25 | lgse/strata#1890 | fix | Dropped a deferred cursor restore once a key press moves the cursor, so arrow keys work after a rename re-sorts the list. |
| 2026-10-23 | lgse/strata#1800 | feat | Previewed List heading drags with an insertion line and applied the column move once, on release. |
| 2026-10-15 | lgse/strata#1673 | perf | Settled List and Icons row refreshes 25 ms after the last scroll instead of every frame, and dropped the `list-fast-scroll` class. |
| 2026-10-15 | lgse/strata#1611 | fix | Routed a focus request for a pane showing results to their cursor hit instead of the hidden listing. |
| 2026-10-11 | lgse/strata#1568 | fix | Cached Icons and List view-to-source maps and selected listing positions, so marquee changes no longer rescan large folders. |
| 2026-10-10 | lgse/strata#1544 | fix | Restored Icons positions on return, kept cursor, viewport, and focus through reloads, and exposed menu roles. |
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

- In List and Icons, a selection change that takes focus while filter results show still focuses the hidden listing. lgse/strata#1611
- In List and Icons, programmatic selection updates by position leave GTK's range origin in place. A following Shift+arrow can extend from a stale entry. lgse/strata#1871
