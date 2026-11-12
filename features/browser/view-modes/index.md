---
title: View modes
status: shipped
origin: {issue: null, pr: lgse/strata#383}
branch: null
reviewed_at: 5f17c9fdc8967e1b4ba8aaf8de113b46d824b0dd
review: draft
code: [src/ui/browser_modes.rs, src/ui/browser_modes/events.rs, src/ui/browser/presentation.rs, src/ui/loading_skeleton.rs, src/ui/loading_skeleton/**, crates/strata-fs/src/app/navigation/preferences.rs, src/ui/browser/view_modes.rs, src/ui/browser_modes/clicks.rs, src/ui/browser_modes/cursor.rs, src/ui/browser_modes/metadata.rs, src/ui/browser_modes/pane.rs, src/ui/browser_modes/pane_header.rs, src/ui/browser_modes/pane_shell.rs, src/ui/browser_modes/pane_state.rs, src/ui/browser_modes/rebuild.rs, src/ui/browser_modes/scroll_settle.rs, src/ui/browser_modes/source_index.rs, src/ui/preferences/layout_settings.rs, src/ui/window/appearance_menu.rs]
tests: [tests/qa/scenarios/view_switching/appearance-menu-switches-view.jsonl, tests/qa/scenarios/view_switching/shortcut-round-trip-keeps-selection.jsonl, tests/qa/scenarios/view_switching/switching-keeps-directory-and-sort.jsonl, tests/qa/scenarios/view_switching/switching-keeps-pane-filter.jsonl, tests/qa/mutations/view-switching.patch, src/ui/loading_skeleton/delay/tests.rs, src/ui/browser_modes/tests.rs, src/ui/browser_modes/tests/counting_model.rs, src/ui/browser/presentation/tests.rs, src/ui/window/tests/preferences/column_prefs.rs, tests/qa/scenarios/locations/unreadable-folder-offers-retry.jsonl]
docs: [docs/architecture.md, site/src/reference/keyboard-navigation.md]
related: [browser/search, preview/preview-panel, browser/view-modes/density, app/accessibility, operations/rename, browser/search/filter, browser/selection, browser/navigation, operations/trash/empty, integration/10xer-mode]
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
- With Mirror columns selection off, a folder selected in List or Icons opens no child column on the switch back to Columns. lgse/strata#2070
- With a 10xer `s` recursive search query showing, the switch back to Columns opens no child column for a selected folder. lgse/strata#2070 (unverified)

### Appearance menu

- Columns, Icons, and List are radio menu items, and Group by file type is a check menu item. lgse/strata#1467, lgse/strata#1544, lgse/strata#1776
- Each option's accessible checked state matches its check icon, including after Ctrl+1 to Ctrl+3 and switches in other windows. lgse/strata#1467, lgse/strata#1544
- With Sort by or Appearance open, a wheel tick outside it closes it and scrolls only the listing under the pointer; over the sidebar or other chrome it only closes. lgse/strata#590
- Wheel ticks inside an open Sort by or Appearance panel keep it open. lgse/strata#590

### Pane header

- In List and Icons, the pane header's Back, Forward, and Parent folder buttons are each insensitive when their target is unavailable. lgse/strata#1895 (unverified)
- In List and Icons, the pane header shows a trash icon button with tooltip "Empty Trash" only at `trash:///`, not in Trash subfolders or other locations. lgse/strata#53
- In List and Icons, the header button is insensitive while the Trash pane lists 0 items and becomes sensitive when an item appears. lgse/strata#138
- With `gvfsd` running, a Trash holding only an item whose name is not valid UTF-8 enables the header button. lgse/strata#1533 (unverified)

### Pane header names

- In List and Icons, the pane header's buttons are named "Back (Alt+←)", "Forward (Alt+→)", and "Parent folder (Alt+↑)". lgse/strata#1895
- The List view's Columns menu button is named "Columns". lgse/strata#1895
- The Ctrl+F filter field is named after its toggle: "Filter this pane (Ctrl+F)" in Columns and "Filter icons (Ctrl+F)" in Icons. lgse/strata#1896
- In List, the filter field is named "Filter list (Ctrl+F)". lgse/strata#1896 (unverified)
- The Icons Thumbnail size slider is named "Thumbnail size". lgse/strata#1896

### Selection

- Click the first of five entries and Ctrl+click the third. Shift+Down in List or Shift+Right in Icons then selects only the third and fourth, as in Columns. lgse/strata#1851, lgse/strata#1871

### Filtered clicks

- One plain click on a folder result opens it, whatever the click-count preferences. lgse/strata#697, lgse/strata#1888
- A plain click on a file result follows the click-count and single-click preview preferences, in Columns, Icons, and List. lgse/strata#1881, lgse/strata#1888
- With files opening on one click, one plain click on a file result opens it once, with no preview. lgse/strata#1888
- With files opening on two clicks and single-click previews on, one plain click selects and previews a previewable file result. A double-click opens it once. lgse/strata#1881, lgse/strata#1888
- With files opening on two clicks and single-click previews on, a plain click on a file result with no quick preview only selects it. lgse/strata#1888 (unverified)
- With files opening on two clicks and single-click previews off, one plain click on a file result only selects it. lgse/strata#1888 (unverified)
- In the file chooser and in Trash, a plain click never opens a file result. It previews a previewable file with single-click previews on, otherwise only selects it. lgse/strata#1888
- A plain click on a selected file result starts no slow-click rename. lgse/strata#1888

### Double-click

- In List and Icons, a double-click opens a folder or launches a file when the second click is released. lgse/strata#2096

### Single clicks on List whitespace

- With List folders on one click, one click on a keyboard-selected folder's metadata cell opens it. lgse/strata#2108
- A single press on a selected List row's whitespace still reaches the row, so click previews open there. lgse/strata#2108

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
- In grouped List, double-click a folder of 300 `a*.txt` and 300 `b*.csv` files. Once loading finishes, `b000.csv`, the first row shown, has focus and nothing is selected. lgse/strata#2070
- That load-finish refocus needs no cursor in the pane and focus in its listing. In Icons, or List without grouping, focus stays on GTK's own row. lgse/strata#2070
- The focused pane draws a 2 px accent focus ring only while GTK shows focus, as after keyboard input. lgse/strata#1466, lgse/strata#1533 (unverified)
- When entries appear in a folder whose pane held focus, focus moves to the keyboard cursor row. lgse/strata#1466, lgse/strata#1533
- F5 keeps focus on the pane while rows are hidden and returns it to the cursor row when they return. lgse/strata#1466, lgse/strata#1533, lgse/strata#1729
- Opening a populated folder that loads within the 150 ms grace period never moves focus to the pane. lgse/strata#1466, lgse/strata#1533 (unverified)
- While entries show, the pane itself is not a Tab stop. lgse/strata#1431, lgse/strata#1533
- A view switch or navigation key drops queued cursor refocus from an earlier focus. Focus never returns to the earlier row. lgse/strata#1900
- In List, cut styling, hidden-file dimming, and live dates of visible rows refresh once scrolling has been still for 25 ms. lgse/strata#1673
- In Icons, cut styling, hidden-file dimming, and accessible descriptions of visible cards refresh once scrolling has been still for 25 ms. lgse/strata#1673 (unverified)
- After 10 s without progress on a folder's mount, "Not responding. This list may be out of date." shows above its listing in Columns, Icons, and List. lgse/strata#1729
- The last listing stays in view under the notice. The notice also shows over a stuck first load, never over an error page. lgse/strata#1729
- The notice clears as soon as a request on that mount answers. lgse/strata#1729
- The notice has the accessible role status. lgse/strata#1729 (unverified)
- In List and Icons, a folder load refused for lack of permission shows "Unable to read this directory" and the reason. Where GIO supports `admin`, an Open as Administrator button sits under it. lgse/strata#1837
- In List and Icons, a folder whose load fails shows a Retry button under the reason, below Open as Administrator where that is offered. An empty folder shows no Retry. lgse/strata#2030
- Clicking Retry reloads the folder; one made readable again lists its entries. lgse/strata#2030
- The folder-error Retry and Open as Administrator buttons use the themed secondary-button style with hover, active, focus, and disabled states, not GTK's default white button. lgse/strata#2030
- Clicking that button opens the folder's `admin://` form. lgse/strata#1837
- In an `admin://` folder, a lock notice reading "Browsing as administrator. New items belong to root, and deleted items skip Trash." shows above the List and Icons listings. lgse/strata#1837
- Long filenames are middle-ellipsized in Columns rows and headings, Icons captions, and the List Name column, so the extension stays visible. lgse/strata#1143

## Design

Columns is the native Miller implementation in `ui/browser/columns.rs`. Icons and List live in `ui/browser_modes.rs`, isolated so they consume the same browser events and emit the same intents as Columns (lgse/strata#398). Collection behavior shared by all three, such as pointer selection, search sessions, and rename leases, is centralized while each mode keeps its own presentation; `docs/architecture.md` records the intentional differences (lgse/strata#1167, lgse/strata#1174).

- Only the active mode is built and updated. Hidden Grid and Explorer views cost up to 44% more enumeration time on 100,000 entries, so a switch rebuilds the target from the browser snapshot instead (lgse/strata#113, lgse/strata#237).
- Inactive panes drop their filename models (lgse/strata#1186). A cached inactive pane is reused only while its location, grouping, and List heading sort still match (lgse/strata#907).
- lgse/strata#266 rebuilt the target before showing it to avoid a blank frame. lgse/strata#310 shows it first, because a ListView rebuilt while hidden measured a one-row viewport.
- Icons and List map displayed positions to source entries through `SourceIndexMap` in O(1), so activation, drag, and selection hit the clicked entry after filtering or sorting (lgse/strata#305).
- A broad model change drops the reverse index, which is rebuilt only when a lookup needs it. Lookups of up to 64 positions map each one directly, so a cursor or small selection never rebuilds the whole index (lgse/strata#1928).
- The List type-group sorter re-sorts only when a sort preference changes. Each row's model value carries its type group, so comparisons neither allocate nor guess MIME types (lgse/strata#1791, lgse/strata#1792). Spliced rows no longer rely on GTK's sorted insertion: List's grouped model places them, recorded on `browser/view-modes/list` (lgse/strata#1928).
- The pane filter query is window-local: it is carried across a switch but never saved (lgse/strata#851).
- A selection made in List or Icons is not an activation. With Mirror columns selection off Columns never opens a child from a selection, so the switch back opens one only while mirroring is on (lgse/strata#2070, commit 2d56db6e).
- A grouped List publishes a large folder's rows in name order, so a group that sorts first arrives above the row GTK focused. A pointer visit has no cursor to hold, so the pane refocuses the first row shown once the listing completes (lgse/strata#2070, commit f9f1104d).
- Focus without a cursor otherwise returns to GTK's own row. Scrolling every List and Icons pane to its first row was reverted (lgse/strata#2070, commit be416388).
- An empty, unreadable, or loading folder focuses the existing page stack rather than its status label. Up, Delete, and the context menu already key off that stack. It is focusable only off the content page, so populated listings gain no unnamed Tab stop (lgse/strata#1466).
- GTK moves focus off a removed or hidden row at the next paint. The pane settles focus first, so a reload never sends it out of the listing (lgse/strata#1466, lgse/strata#1533).
- lgse/strata#1081 moved the deferred row refresh to the next frame, so during continuous scrolling it ran every frame or two and restyled every List row. lgse/strata#1673 settles 25 ms after the last scroll, never sooner than two frames, so a slow machine does not settle between frames of one scroll (lgse/strata#1671, lgse/strata#1673).
- The frame rate counts only when the frame clock's history all follows the scroll's start. `fps()` averages idle gaps, which would stretch the floor by seconds once the clock stops while idle (lgse/strata#1673, lgse/strata#1677).
- A focus request for a pane showing filter or search results goes to the results' cursor, not the hidden listing behind them (lgse/strata#1549, lgse/strata#1611).
- The skeleton waits a 150 ms grace period because fast loads flashed it for a few frames; showing nothing or a spinner was rejected (lgse/strata#283). Skeletons mirror each mode's loaded layout and density (lgse/strata#336).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-11-02 | lgse/strata#2030 | fix | Offered Retry on unreadable List and Icons folders, themed Retry and Open as Administrator, and closed deeper columns on any plain file click. |
| 2026-10-27 | lgse/strata#1900 | fix | Cancelled a List heading drag on Escape without saving an order or clearing the selection, and dropped cursor refocus work a newer focus superseded. |
| 2026-10-25 | lgse/strata#1890 | fix | Dropped stale deferred cursor restores in `browser_modes` once a newer cursor supersedes them, so arrow keys work after a rename re-sorts List. |
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
