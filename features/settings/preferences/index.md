---
title: Settings window and general preferences
status: shipped
origin: {issue: lgse/strata#845, pr: lgse/strata#849}
branch: null
reviewed_at: 72b840e69d6f0df9d33fb5583e62a3a2944886a1
review: draft
code: [src/ui/settings.rs, src/ui/settings/general.rs, src/ui/settings/about.rs, src/ui/settings/bindings.rs, src/ui/settings/wrap.rs, src/ui/settings/search.rs, src/ui/window/composition/settings.rs]
tests: [src/ui/settings/search/tests.rs, src/ui/settings/tests/restart.rs, src/ui/window/composition/settings/tests.rs, src/ui/window/tests/preferences.rs, src/app/browser/tests/preferences.rs, tests/e2e/scenarios/test_settings_search.py]
docs: [docs/preferences.md]
related: [settings/themes, app/updates, integration/custom-actions, browser/tabs, browser/tabs/session-restore, integration/10xer-mode]
---

## Summary

The Settings panel: opening and closing it, page navigation, responsive layout, Settings-wide search, and the About page. It also owns the General settings no other feature claims: Show F1 Shortcuts button, default directory, and the hidden-files toggle. Window buttons belong to `app/window`. Feature pages and rows (Appearance, Actions, Updates, search exclusions, thumbnails, desktop integration, Restore open tabs) belong to their features. Children: `settings/preferences/storage` (saving and synchronizing preferences), `settings/preferences/language` (interface language), and `settings/preferences/date-format` (modified-date display).

## Behavior

### Opening and closing

- Ctrl+, or the header Settings button opens Settings over the blurred window; the first open shows General. lgse/strata#849
- While another modal dialog, such as Properties, is visible, Ctrl+, and the Settings button do nothing. lgse/strata#912
- Escape, the Close settings button, or a click outside the panel closes Settings. lgse/strata#107, lgse/strata#849
- Closing Settings returns focus to the file-list cursor row, also when the header Settings button opened it; the next Down moves the cursor. lgse/strata#1430, lgse/strata#1533
- When Ctrl+, opens Settings while a pane-filter field or filter result has focus, closing Settings returns focus to that field or result. lgse/strata#1430, lgse/strata#1533
- The navigation lists General, Appearance, Actions, Updates, and About; choosing one shows that page and its name as the title. lgse/strata#849
- The panel is at most 1400×1024 px and 24 px inside the window, and each page scrolls vertically when it does not fit. lgse/strata#29, lgse/strata#849
- When the panel is narrower than 900 px at the default 13 px text size, the navigation drops its heading and labels and shows icons only. lgse/strata#29, lgse/strata#849 (unverified)
- The Items shown in sidebar chips stay below their title and description at every panel width. lgse/strata#1032
- When the panel is narrower than 1250 px at the default text size, a row's control moves below its title and description; switches stay beside it. lgse/strata#849, lgse/strata#924 (unverified)
- When a dependent row's control stacks below it, the row's dependency arrow stays beside its heading. lgse/strata#924
- Settings has no Keybindings page; the F1 reference is the only keybinding list. lgse/strata#1376

### Choice menus

- A Settings choice button, such as Auto-refresh folder, is named after its row title and described by its shown value, such as "5 min". lgse/strata#1467, lgse/strata#1544
- Choosing another value updates the button's description at once, also in other windows. lgse/strata#1544 (unverified)
- Each option in a Settings choice menu is a radio menu item whose checked state matches its check icon. lgse/strata#1467, lgse/strata#1544
- The Decoding backend button is named "Video preview hardware backend", not its row title. lgse/strata#1544 (unverified)

### Settings search

- Typing in Search settings shows only matching rows, hides navigation entries for pages without matches, and opens the best-matching page. lgse/strata#849
- Queries match row titles and aliases, so "font size" finds Text size. lgse/strata#849
- Query words of four or more letters tolerate one typo, six or more two, so "tezt size" finds Text size. lgse/strata#849 (unverified)
- Queries also match a row's translated title and the current language's keywords. lgse/strata#1519
- A query with no match shows "No settings match your search." under the title Search results. lgse/strata#849
- Escape in a non-empty search field clears the query and restores every row; the next Escape closes Settings. lgse/strata#849
- Searching changes no saved preference. lgse/strata#849
- Searching "keybindings" finds Show F1 Shortcuts button. lgse/strata#1376
- With icon-only navigation, the search field becomes a Search settings button that opens the field in a popover; the query and focus survive resizing. lgse/strata#849
- Rows unavailable on this installation stay hidden when a query is cleared. lgse/strata#849 (unverified)

### About

- About shows Strata's version, build commit, and GTK version, plus Website, Source code, Report an issue, and License (MIT) links. lgse/strata#19, lgse/strata#849
- Copy version info copies the version, description, commit, toolkit, author, and license to the clipboard. lgse/strata#849 (unverified)

### Show F1 Shortcuts button

- Turning off General → Browsing → Show F1 Shortcuts button hides the footer shortcuts button in every open window; F1 still opens the reference. lgse/strata#1376

### Default directory

- With no saved choice, General → Startup → Default directory reads Home directory, and Reset is disabled. lgse/strata#943 (unverified)
- Choosing a folder saves it and shows it with `~/` for paths under home. lgse/strata#943
- A new window without an explicit target or restored tabs opens at the chosen folder; `browser/tabs/session-restore` owns when tabs restore. lgse/strata#943, lgse/strata#1532
- Reset restores the home directory as the default. lgse/strata#943
- If the saved folder no longer exists, a new window opens home and the saved choice is cleared. lgse/strata#943

### Hidden files

- Ctrl+H or Ctrl+. toggles hidden files. lgse/strata#240
- Ctrl+Shift or Ctrl+Alt with H or . does not toggle hidden files. lgse/strata#240 (unverified)
- The Appearance menu's Hidden files row shows the `Ctrl + H` hint and an eye icon reflecting the current state. lgse/strata#240
- That row is a check menu item described as "Ctrl + H"; its checked state follows Ctrl+H and other windows. lgse/strata#1467, lgse/strata#1544
- The folder-background context menu offers Show Hidden Files or Hide Hidden Files, matching the current state. lgse/strata#240
- Toggling shows or hides hidden entries in every open column without reloading the directories. lgse/strata#201
- The choice is saved as `show_hidden` and restored on the next launch. lgse/strata#144
- Toggling in one window applies to every open window and to new columns. lgse/strata#518
- Shown hidden items draw their icon or thumbnail and name at 65% opacity in Columns, Icons, and List. lgse/strata#927

## Design

[docs/preferences.md](https://github.com/lgse/strata/blob/72b840e69d6f0df9d33fb5583e62a3a2944886a1/docs/preferences.md) lists every stored preference, its consumer, and the rules for adding one.

- Settings is a layer inside the window, built on first open. Appearance, Actions, and Updates build on first selection, because Updates starts package-manager detection and network work.
- Settings pages only edit preferences; consumers bind at construction. Opening Settings once had applied saved Folder peeking, which hid the missing startup binding (lgse/strata#515).
- Settings refuses to open while another modal is visible rather than stacking under it, because its lazily added overlay stayed below later dialogs (lgse/strata#865).
- Closing Settings returns focus to the file list, not to the gear or other chrome that opened it. Only a focused filter session gets its field or results back (owner decision, lgse/strata#1430, lgse/strata#1533).
- Settings is hidden rather than removed, so it captures its focus origin on each show and restores focus when the hide completes. Every close route, and the layer unrealizing with its window, runs the same dismissal hooks (lgse/strata#1430, lgse/strata#1457, lgse/strata#1533).
- A choice button's value goes in its description, so its name stays stable for E2E locators and Settings search. Options are radio menu items so screen readers announce the chosen one (lgse/strata#1467, lgse/strata#1544).
- Search filters the existing bound rows instead of building copies, and the query is not saved. Installation-specific availability is tracked apart from search matches so clearing a query cannot reveal it (lgse/strata#849).
- The Settings Keybindings page and the F1 reference were two hand-maintained catalogs that drifted. Generating both from one catalog was rejected; F1 already had mode- and view-aware sections (lgse/strata#1374).
- Hidden entries stay in memory with an `is_hidden` flag and a filter model hides them, instead of re-enumerating every column and reinstalling monitors (lgse/strata#200, lgse/strata#201).
- Ctrl+. was added beside Ctrl+H rather than replacing it, to keep existing habits (lgse/strata#121).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-09 | lgse/strata#1533 | fix | Returned focus to the file-list cursor when Settings closes, so the next key no longer reaches the header. |
| 2026-10-02 | lgse/strata#1376 | feat | Removed the Keybindings page and moved Show F1 Shortcuts button to General, making F1 the only reference. |
| 2026-09-15 | lgse/strata#1032 | fix | Kept the sidebar place chips below their description at every width. |
| 2026-09-14 | lgse/strata#943 | feat | Added the Default directory preference for launches without a target. |
| 2026-09-13 | lgse/strata#924 | fix | Kept controls inline until narrow widths and dependency arrows beside their headings. |
| 2026-09-12 | lgse/strata#912 | fix | Ignored Settings requests while another modal dialog is visible. |
| 2026-09-12 | lgse/strata#849 | feat | Rebuilt the Settings shell and pages to the reference design and added Settings-wide search. |
| 2026-09-07 | lgse/strata#563 | refactor | Split Settings page and control construction into page modules. |
| 2026-09-04 | lgse/strata#240 | feat | Added Ctrl+., the context-menu toggle, and the menu shortcut hint for hidden files. |
| 2026-09-03 | lgse/strata#201 | perf | Toggled hidden files in memory instead of re-reading every open column. |
| 2026-08-31 | lgse/strata#29 | fix | Constrained the Settings panel to the window and made pages scroll. |
| 2026-08-30 | lgse/strata#19 | feat | Added the About page with version, build commit, and project links. |

## Known gaps

- A search that matches only Actions rows hides every navigation entry, and About matches open the Actions page; the fix is unmerged. lgse/strata#1453, lgse/strata#1546
- Render documents by default is not registered for search, so no query finds it, and it stays visible whenever another Browsing row matches; the fix is unmerged. lgse/strata#1454, lgse/strata#1546
