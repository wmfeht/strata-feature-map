---
title: View modes
status: shipped
origin: {issue: null, pr: lgse/strata#383}
branch: null
reviewed_at: 72b840e69d6f0df9d33fb5583e62a3a2944886a1
review: draft
code: [src/ui/browser_modes.rs, src/ui/browser_modes/events.rs, src/ui/browser/pane_header.rs, src/ui/browser/presentation.rs, src/ui/loading_skeleton.rs, src/ui/loading_skeleton/**]
tests: [tests/e2e/scenarios/test_view_switching.py, src/ui/loading_skeleton/delay/tests.rs]
docs: [docs/architecture.md, docs/keyboard-navigation.md]
related: [browser/search, preview/preview-panel]
---

## Summary

The three presentations of a folder, Columns, Icons, and List, and the Appearance menu and shortcuts that switch between them. Children: `browser/view-modes/columns` (Miller columns), `browser/view-modes/icons` (the thumbnail grid), `browser/view-modes/list` (the table), `browser/view-modes/sorting` (sort fields, order, and persistence), and `browser/view-modes/text-size` (interface text size). Restoring the position on return and refresh in Icons and List is shared by both views and lives here.

## Behavior

### Switching

- The Appearance menu's VIEW section lists Columns, Icons, and List; choosing one switches the view and closes the menu. lgse/strata#383, lgse/strata#168
- Ctrl+1, Ctrl+2, and Ctrl+3 switch to Columns, Icons, and List, including while typing in the pane filter. lgse/strata#531, lgse/strata#925
- The portal file chooser accepts the same Ctrl+1, Ctrl+2, and Ctrl+3 shortcuts. lgse/strata#877
- The Appearance button shows the current mode's icon, and the menu checks the current mode, after both menu and keyboard switches. lgse/strata#531
- The chosen mode is saved as `browser_mode` (`columns`, `icons`, or `list`) and restored at startup; saved `grid` and `explorer` values load as Icons and List. lgse/strata#383
- Choosing the mode already shown changes nothing: selection and scroll position stay. lgse/strata#266
- Switching keeps the open directory, the selection, the focused item, and the sort; leaving Columns lands on the directory Columns had active. lgse/strata#237
- Switching keeps a typed pane filter query, its open filter field, and the narrowed listing. lgse/strata#925
- After a switch the new view shows a full viewport of entries without scrolling first. lgse/strata#310

### Appearance menu

- The Appearance menu's DENSITY section offers Compact, the default, and Airy; the choice is saved. lgse/strata#168 (unverified)
- Columns, Icons, List, Compact, and Airy are radio menu items, and Group by file type is a check menu item. lgse/strata#1467, lgse/strata#1544
- The checked view option follows Ctrl+1, Ctrl+2, Ctrl+3, and switches made in other windows. lgse/strata#1467, lgse/strata#1544
- With Sort by or Appearance open, a wheel tick outside it closes it and scrolls only the listing under the pointer; over the sidebar or other chrome it only closes. lgse/strata#590
- Wheel ticks inside an open Sort by or Appearance panel keep it open. lgse/strata#590

### Loading and names

- A directory that loads within 150 ms shows no loading skeleton; a slower load shows a skeleton shaped like the current view. lgse/strata#343, lgse/strata#584
- Skeletons cannot be selected or clicked, and loaded content, empty states, and errors replace them. lgse/strata#343
- A pending skeleton never appears after the load finishes, fails, or navigates away. lgse/strata#584
- Entering an empty, unreadable, or still-loading folder gives keyboard focus to the pane itself. lgse/strata#1466, lgse/strata#1533
- The focused pane draws a 2 px accent focus ring only while GTK shows focus, as after keyboard input. lgse/strata#1466, lgse/strata#1533 (unverified)
- When entries appear in a folder whose pane held focus, focus moves to the keyboard cursor row. lgse/strata#1466, lgse/strata#1533
- F5 or auto-refresh keeps focus on the pane while rows are hidden and returns it to the cursor row when they return. lgse/strata#1466, lgse/strata#1533
- Opening a populated folder that loads within the 150 ms grace period never moves focus to the pane. lgse/strata#1466, lgse/strata#1533 (unverified)
- While entries show, the pane itself is not a Tab stop. lgse/strata#1431, lgse/strata#1533
- Long filenames are middle-ellipsized in Columns rows and headings, Icons captions, and the List Name column, so the extension stays visible. lgse/strata#1143

### Returning to a folder

- In Icons and List, returning to one of the last 128 folders left restores its selection, cursor, range anchor, and scroll position after loading. lgse/strata#893, lgse/strata#1436, lgse/strata#1544
- Back, Forward, Alt+Up, Backspace, a breadcrumb, and a path typed after Ctrl+L all restore it; Icons selected the first item before. lgse/strata#1436, lgse/strata#1544
- Opening a remembered folder another way, such as a sidebar place or a double-click, also restores its position. lgse/strata#893, lgse/strata#1544 (unverified)
- Pressing Down after a restore moves from the restored row, not the first row. lgse/strata#893, lgse/strata#1544
- Selection, cursor, and anchor carry between Icons and List: a folder left in Icons and reopened in List has the same entries selected. lgse/strata#1436, lgse/strata#1544
- The exact scroll offset returns only in the view the folder was left in, and for Icons only at the same grid width. Otherwise the view scrolls the cursor into view. lgse/strata#1436, lgse/strata#1544
- With no remembered position, returning to an ancestor selects the folder you came from, as Columns does. lgse/strata#1437, lgse/strata#1544
- Back, Forward, or Up into a remembered folder that is now empty gives keyboard focus to the pane, not the hidden list. lgse/strata#1466, lgse/strata#1533 (unverified)
- A restored selection does not make Ctrl+V paste into the selected folder until the user selects it explicitly. lgse/strata#893
- Opening a typed file path, a Ctrl+K result, Open file location, or a FileManager1 request selects that target instead of the remembered position. lgse/strata#1499
- A click, scroll, or key press in the pane before a restore settles cancels it. So do a view switch and a failed load. lgse/strata#893, lgse/strata#1544 (unverified)

### Focus on return

- In Icons and List, Back, Forward, and Up focus the restored listing only when focus was in the pane left, its Ctrl+F field included, or nowhere. lgse/strata#1436, lgse/strata#1544
- Back from the pane header's Back button keeps focus on the button; with the sidebar focused, focus stays in the sidebar. lgse/strata#1436, lgse/strata#1544
- Sidebar places, breadcrumbs, and typed paths always focus the new listing, as on a first visit. lgse/strata#1544
- A pane in a hidden tab, or in a window with a rename open, never takes focus when its restore applies. lgse/strata#1544 (unverified)

### Refreshing

- In Icons and List, F5, the Refresh button, auto-refresh, or a rescan after over 4,096 queued changes keeps the cursor row, selection, and scroll offset. lgse/strata#1434, lgse/strata#1544
- After End then F5, the last row keeps the cursor at the same position on screen, and Left or Up moves from it. lgse/strata#1434, lgse/strata#1544
- A refresh keeps focus on a focused row, or in a focused Ctrl+F field with its query, including through a slow reload. lgse/strata#1434, lgse/strata#1544
- Typing in the Ctrl+F field during that reload does not stop focus returning to it; Tab, a click, a scroll, or a touch does. lgse/strata#1544
- Escape that closes the filter during the reload sends focus to the listing instead. lgse/strata#1544
- A refresh or restore never takes focus from the sidebar, the location entry, or a dialog. lgse/strata#1434, lgse/strata#1544
- With a filter result focused, a refresh restores the viewport and leaves focus to the filter. lgse/strata#1544 (unverified)

## Design

Columns is the native Miller implementation in `ui/browser/columns.rs`. Icons and List live in `ui/browser_modes.rs`, isolated so they consume the same browser events and emit the same intents as Columns (lgse/strata#398). Collection behavior shared by all three, such as pointer selection, search sessions, and rename leases, is centralized while each mode keeps its own presentation; `docs/architecture.md` records the intentional differences (lgse/strata#1167, lgse/strata#1174).

- Only the active mode is built and updated. Hidden Grid and Explorer views cost up to 44% more enumeration time on 100,000 entries, so a switch rebuilds the target from the browser snapshot instead (lgse/strata#113, lgse/strata#237).
- Inactive panes drop their filename models (lgse/strata#1186). A cached inactive pane is reused only while its location, grouping, and List heading sort still match (lgse/strata#907).
- lgse/strata#266 rebuilt the target before showing it to avoid a blank frame. lgse/strata#310 shows it first, because a ListView rebuilt while hidden measured a one-row viewport.
- Icons and List map displayed positions to source entries through `SourceIndexMap` in O(1), so activation, drag, and selection hit the clicked entry after filtering or sorting (lgse/strata#305).
- The pane filter query is window-local: it is carried across a switch but never saved (lgse/strata#851).
- An empty, unreadable, or loading folder focuses the existing page stack rather than its status label. Up, Delete, and the context menu already key off that stack. It is focusable only off the content page, so populated listings gain no unnamed Tab stop (lgse/strata#1466).
- GTK moves focus off a removed or hidden row at the next paint. The pane settles focus first, so a reload never sends it out of the listing (lgse/strata#1466, lgse/strata#1533).
- Icons and List share one history of positions keyed by folder. Scroll offsets mean different things per view, and an Icons grid of another width wraps differently. The offset is reused only in the same view and width (lgse/strata#1436).
- lgse/strata#893 built the restore for List only; lgse/strata#1267 then described it for Icons and List without code (lgse/strata#1436).
- Restoring matches entries by location, not row number, so a deleted entry is never selected; a restored selection does not redirect paste until it is selected again (lgse/strata#893).
- An explicit target beats the remembered position because the user named it (lgse/strata#1499).
- Focus follows the route. A sidebar place, breadcrumb, or typed path is an explicit visit and focuses the listing. History keys leave focus outside the pane where it is (lgse/strata#1544).
- A reload used to switch the pane to its pending page, which unmapped the rows and reset GTK's cursor, scroll, and focus. The model keeps the selection by identity, and the view restores viewport and focus (lgse/strata#1434).
- Views capture the outgoing position on `NavigationStarting` and `ColumnReloading`, before the model changes ([docs/architecture.md](https://github.com/lgse/strata/blob/72b840e69d6f0df9d33fb5583e62a3a2944886a1/docs/architecture.md), lgse/strata#1544).
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

None known.
