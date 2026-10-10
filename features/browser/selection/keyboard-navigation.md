---
title: Keyboard navigation in views
status: shipped
origin: {issue: lgse/strata#291, pr: lgse/strata#358}
branch: null
reviewed_at: 72b840e69d6f0df9d33fb5583e62a3a2944886a1
review: draft
code: [src/ui/focus_navigation.rs, src/ui/top_bar_navigation.rs, src/ui/window/keyboard/focus.rs, src/ui/browser/tab_stops.rs]
tests: [src/ui/focus_navigation/tests.rs, src/ui/top_bar_navigation/tests.rs, src/ui/window/tests/keyboard_policy.rs, src/ui/window/tests/keyboard_dispatch/pane_focus.rs, tests/e2e/scenarios/test_keyboard_navigation.py]
related: [browser/sidebar, browser/navigation, integration/10xer-mode]
---

## Summary

Moving keyboard focus with plain arrows and `h`/`j`/`k`/`l` through the file list, pane header, sidebar, and top bar in the default key map. Arrows move between interface regions rather than changing directories.

## Behavior

### Within the file list

- In Icons, arrows move one tile in that direction, using rows as laid out. lgse/strata#358
- In Icons and List, Up and Down move focus and selection through entries without changing directory. lgse/strata#358
- In List, Right keeps focus on the current entry and never opens it or changes directory. lgse/strata#358
- In Columns, Right on a folder enters it or moves into its already open child column. lgse/strata#58, lgse/strata#358
- In Columns, Right on a focused file does not open it; Enter opens it. lgse/strata#358
- With Type to search off, `h`, `j`, `k`, and `l` act as Left, Down, Up, and Right in every view and the file chooser. lgse/strata#555
- With Type to search on, `h`, `j`, `k`, and `l` pressed in the file list start a search instead of moving. lgse/strata#555 (unverified)
- Enter on a sidebar place in Icons, for a folder not remembered by Icons or List, gives its first item focus and selection. lgse/strata#374, lgse/strata#379

### Leaving the file list

- In Icons, Left at the left edge focuses the visible sidebar; in List, Left from any entry does. lgse/strata#358
- In Columns, Left in the first column focuses the visible sidebar's row for the current place. lgse/strata#58
- With the sidebar hidden, Left in Icons or List does not change directory. lgse/strata#358
- Up from the first Icons row or first List entry focuses the pane header, including in an empty directory. lgse/strata#358
- In Columns, Up from a column's first entry focuses that column's header controls, and Down returns to that column's list. lgse/strata#58
- In the pane header, Left and Right move between enabled controls without activating them; Enter or Space activates one. lgse/strata#358
- In Icons or List, Left from the pane header's first control focuses the visible sidebar. lgse/strata#1088
- In Columns, Left or Right past the end of a column's header controls moves into the neighboring column's header. lgse/strata#555
- Down from the Icons or List pane header returns to the entry left, without changing selection. lgse/strata#358
- In the sidebar, Up and Down move between places, and Up from the first row (Home by default) focuses the top navigation bar. lgse/strata#358
- In the top navigation bar, Left and Right move between enabled controls; Down returns to the sidebar row left, or to the files when the sidebar is hidden. lgse/strata#358
- Outside 10xer mode, Right from the sidebar returns to the entry left, or to the active entry when the sidebar was entered from the header. lgse/strata#358, lgse/strata#1088

### Tab stops

- In the default key map, Tab from a focused row in any view leaves the listing in one press. Focus goes to the next control, such as F1 Shortcuts. lgse/strata#1431, lgse/strata#1533
- Tab or Shift+Tab into a listing lands on the keyboard cursor row, so Enter, Space, and Ctrl+C act on the row showing focus. lgse/strata#1431, lgse/strata#1533
- Shift+Tab from a row goes to the control before the rows. In List that is the sort headings; then come an open filter, the header actions, and the sidebar. lgse/strata#1431, lgse/strata#1533
- In Columns, Tab into the strip lands on the active column's cursor without changing the active column. Tab from any column leaves the strip. lgse/strata#1431, lgse/strata#1533
- In Columns, Shift+Tab from a column goes to its open filter, then its header actions, then the control before the strip. lgse/strata#1431, lgse/strata#1533
- In Columns, an unreadable folder's Retry button is the next Tab stop inside its column. lgse/strata#1466, lgse/strata#1533
- Tab from an inline rename field commits the rename and leaves the listing; in Columns it leaves the strip. lgse/strata#1431, lgse/strata#1533
- In an empty, unreadable, or loading folder, Tab and Shift+Tab leave the focused pane as they leave a listing. Shift+Tab from the footer returns to it. lgse/strata#1466, lgse/strata#1533
- 10xer mode keeps its own Tab handling. lgse/strata#1431, lgse/strata#1533 (unverified)

### Keep arrows in file list

- Settings → General → Browsing → Keep arrows in file list, off by default, stops arrows from leaving the file list. lgse/strata#942
- With it on, Up from the first entry and Left at the left edge keep focus in the file list. lgse/strata#942
- Ctrl+\ toggles the preference live and updates the Settings switch. lgse/strata#942
- With it on, Tab and the pointer still reach the header, sidebar, and top bar. lgse/strata#942
- The file chooser follows the same preference. lgse/strata#942

## Design

[docs/keyboard-navigation.md](https://github.com/lgse/strata/blob/72b840e69d6f0df9d33fb5583e62a3a2944886a1/docs/keyboard-navigation.md) carries the rules under "Arrows, the header, and the sidebar", including Tab stops.

Strata is positioned as keyboard-first; a Yazi user reported needing the trackpad and losing focus to the sidebar (lgse/strata#291). Navigation then moved plain arrows to interface regions and left history to Alt+Left, Alt+Right, and Alt+Up (lgse/strata#358).

- Icons hands arrows to GTK's native spatial movement, so moves follow the rendered grid (lgse/strata#358).
- In Columns, Right enters folders only and never activates a file; Enter stays the explicit open (lgse/strata#291). List keeps Right in the file list (lgse/strata#358).
- `h`/`j`/`k`/`l` follow the arrow paths only with Type to search off, because Type to search claims plain letters. It stays on by default (lgse/strata#552).
- Keep arrows in file list is an opt-out that defaults off, preserving the keyboard-only and accessibility paths it removes (lgse/strata#942).
- Each listing is one Tab stop because walking every row took 120 or more presses in a 120-entry folder (lgse/strata#1431).
- The Columns strip is one stop that lands on the active column. Per-column stops were rejected because entering a column would change the paste and New Folder destination (lgse/strata#1431).
- The List sort headings stay Tab stops: they are real controls and cost five stops, not one per row (lgse/strata#1431).
- The sidebar remembers a return target only while the file view holds focus. A header control as target trapped focus outside the listing (lgse/strata#1053).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-09 | lgse/strata#1533 | fix | Made each listing one Tab stop that lands on the keyboard cursor, with a focusable pane in empty folders. |
| 2026-09-23 | lgse/strata#1088 | fix | Returned Right from the sidebar to the file list when the sidebar was entered from the header. |
| 2026-09-14 | lgse/strata#942 | feat | Added Keep arrows in file list and its Ctrl+\ toggle. |
| 2026-09-05 | lgse/strata#379 | fix | Focused the opened listing after Enter on a sidebar place in Icons. |
| 2026-09-05 | lgse/strata#358 | fix | Routed plain arrows between files, pane header, sidebar, and top bar, and separated cursor, selection, and path visuals. |
| 2026-08-31 | lgse/strata#58 | fix | Extended keyboard focus to column headers, nested columns, the sidebar, and menus. |

## Known gaps

None known.
