---
title: Keyboard navigation in views
status: shipped
origin: {issue: lgse/strata#291, pr: lgse/strata#358}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [src/ui/focus_navigation.rs, src/ui/top_bar_navigation.rs, src/ui/window/keyboard/focus.rs]
tests: [src/ui/focus_navigation/tests.rs, src/ui/top_bar_navigation/tests.rs, src/ui/window/tests/keyboard_policy.rs, tests/e2e/scenarios/test_keyboard_navigation.py]
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
- After Enter on a sidebar place in Icons, the opened folder's first item has focus and selection, so the next arrow or Enter acts on files. lgse/strata#374, lgse/strata#379

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

### Keep arrows in file list

- Settings → General → Browsing → Keep arrows in file list, off by default, stops arrows from leaving the file list. lgse/strata#942
- With it on, Up from the first entry and Left at the left edge keep focus in the file list. lgse/strata#942
- Ctrl+\ toggles the preference live and updates the Settings switch. lgse/strata#942
- With it on, Tab and the pointer still reach the header, sidebar, and top bar. lgse/strata#942
- The file chooser follows the same preference. lgse/strata#942

## Design

[docs/keyboard-navigation.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/keyboard-navigation.md) carries the rules under "Arrows, the header, and the sidebar".

Strata is positioned as keyboard-first; a Yazi user reported needing the trackpad and losing focus to the sidebar (lgse/strata#291). Navigation then moved plain arrows to interface regions and left history to Alt+Left, Alt+Right, and Alt+Up (lgse/strata#358).

- Icons hands arrows to GTK's native spatial movement, so moves follow the rendered grid (lgse/strata#358).
- In Columns, Right enters folders only and never activates a file; Enter stays the explicit open (lgse/strata#291). List keeps Right in the file list (lgse/strata#358).
- `h`/`j`/`k`/`l` follow the arrow paths only with Type to search off, because Type to search claims plain letters. It stays on by default (lgse/strata#552).
- Keep arrows in file list is an opt-out that defaults off, preserving the keyboard-only and accessibility paths it removes (lgse/strata#942).
- The sidebar remembers a return target only while the file view holds focus. A header control as target trapped focus outside the listing (lgse/strata#1053).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-23 | lgse/strata#1088 | fix | Returned Right from the sidebar to the file list when the sidebar was entered from the header. |
| 2026-09-14 | lgse/strata#942 | feat | Added Keep arrows in file list and its Ctrl+\ toggle. |
| 2026-09-05 | lgse/strata#379 | fix | Focused the opened listing after Enter on a sidebar place in Icons. |
| 2026-09-05 | lgse/strata#358 | fix | Routed plain arrows between files, pane header, sidebar, and top bar, and separated cursor, selection, and path visuals. |
| 2026-08-31 | lgse/strata#58 | fix | Extended keyboard focus to column headers, nested columns, the sidebar, and menus. |

## Known gaps

- Tab walks every entry of a listing before leaving it, and an empty directory has no focusable target. The fix merged after `reviewed_at`. lgse/strata#1431, lgse/strata#1466, lgse/strata#1533
- In Columns, Home and End move the cursor without updating the mirrored child column. The fix merged after `reviewed_at`. lgse/strata#1447, lgse/strata#1533
