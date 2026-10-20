---
title: Settings window and general preferences
status: shipped
origin: {issue: lgse/strata#845, pr: lgse/strata#849}
branch: null
reviewed_at: fd6327265eaa3266f8420fe8bd25e965146344b0
review: draft
code: [src/ui/settings.rs, src/ui/settings/general.rs, src/ui/settings/about.rs, src/ui/settings/bindings.rs, src/ui/settings/wrap.rs, src/ui/settings/search.rs, src/ui/window/composition/settings.rs]
tests: [src/ui/settings/tests.rs, src/ui/settings/tests/general.rs, src/ui/settings/search/tests.rs, src/ui/settings/tests/restart.rs, src/ui/window/composition/settings/tests.rs, src/ui/window/tests/preferences.rs, src/app/browser/tests/preferences.rs, tests/e2e/scenarios/test_settings_search.py]
docs: [docs/preferences.md]
related: [settings/themes, settings/diagnostics, remote/file-providers/integrations, browser/search, app/updates, integration/custom-actions, browser/tabs, browser/tabs/session-restore, integration/10xer-mode, browser/directory-monitoring]
---

## Summary

The Settings panel: opening and closing it, page navigation, responsive layout, Settings-wide search, and the About page. It also owns the General settings no other feature claims: Show F1 Shortcuts button, Watch network folders, default directory, and the hidden-files toggle. Window buttons belong to `app/window`. Feature pages and rows belong to their features. They are Appearance, Actions, Integrations, Updates, Diagnostics, search exclusions, thumbnails, desktop integration, Restore open tabs, and Remember sort and icon size per folder. Children: `settings/preferences/storage` (saving and synchronizing preferences), `settings/preferences/language` (interface language), and `settings/preferences/date-format` (modified-date display).

## Behavior

### Opening and closing

- Ctrl+, or the header Settings button opens Settings over the blurred window; the first open shows General. lgse/strata#849
- Ctrl+Alt+, and Ctrl+Super+, do not open Settings. lgse/strata#1576
- While another modal dialog, such as Properties, is visible, Ctrl+, and the Settings button do nothing. lgse/strata#912
- Escape, the Close settings button, or a click outside the panel closes Settings. lgse/strata#107, lgse/strata#849
- Closing Settings returns focus to the file-list cursor row, also when the header Settings button opened it; the next Down moves the cursor. lgse/strata#1430, lgse/strata#1533
- When Ctrl+, opens Settings while a pane-filter field or filter result has focus, closing Settings returns focus to that field or result. lgse/strata#1430, lgse/strata#1533
- The navigation lists General, Appearance, Actions, Integrations, Updates, Diagnostics, and About; choosing one shows that page and its name as the title. lgse/strata#849, lgse/strata#1735, lgse/strata#1748
- The panel is at most 1400×1024 px and 24 px inside the window, and each page scrolls vertically when it does not fit. lgse/strata#29, lgse/strata#849
- A sideways touchpad swipe or Shift+wheel over a Settings page does not move the page horizontally. lgse/strata#1719
- Scrolling past the top or bottom of a Settings page, or of any scroller inside the Settings panel, draws no dark band at the edge. lgse/strata#1719
- At text size 32 in a narrow window, a Settings page fits the panel width with nothing clipped on the right and still scrolls vertically. lgse/strata#1719
- A page with wrapped descriptions scrolls to its last row, so General's desktop integration section and its Complete setup button are reachable. lgse/strata#1719 (unverified)
- When the panel is narrower than 900 px at the default 13 px text size, the navigation drops its heading and labels and shows icons only. lgse/strata#29, lgse/strata#849 (unverified)
- The Items shown in sidebar chips stay below their title and description at every panel width. lgse/strata#1032
- When the panel is narrower than 1250 px at the default text size, a row's control moves below its title and description; switches stay beside it. lgse/strata#849, lgse/strata#924 (unverified)
- When a dependent row's control stacks below it, the row's dependency arrow stays beside its heading. lgse/strata#924
- Settings has no Keybindings page; the F1 reference is the only keybinding list. lgse/strata#1376

### Restart

- Pressing Restart now twice quickly relaunches Strata once; a restart requested while one is starting is ignored. lgse/strata#1729
- When a window refuses to close for a restart, Strata keeps running and does not relaunch. lgse/strata#1519, lgse/strata#1729

### Choice menus

- A Settings choice button, such as Search time limit, is named after its row title and described by its shown value, such as "5 min". lgse/strata#1467, lgse/strata#1544, lgse/strata#1667
- The Decoding backend button is the exception: its name is "Video preview hardware backend", not its row title. lgse/strata#1467
- Choosing another value updates the button's description at once, also in other windows. lgse/strata#1544 (unverified)
- Each option in a Settings choice menu is a radio menu item whose checked state matches its check icon. lgse/strata#1467, lgse/strata#1544

### Settings search

- Typing in Search settings shows only matching rows, hides navigation entries for pages without matches, and opens the best-matching page. lgse/strata#849
- Queries match row titles and aliases, so "font size" finds Text size. lgse/strata#849
- Query words of four or more letters tolerate one typo, six or more two, so "tezt size" finds Text size. lgse/strata#849 (unverified)
- Queries also match a row's translated title and the current language's keywords. lgse/strata#1519
- A query word of two or more characters with a Han or kana character matches inside a title, keyword, or alias word. Under 简体中文, 视频预览 finds 硬件加速视频预览; under 正體中文, 快捷鍵按鈕 finds 顯示 F1 快捷鍵按鈕. lgse/strata#1583, lgse/strata#1745 (unverified)
- A single Han or kana character does not match inside a word, so の under 日本語 does not find デフォルトのディレクトリ. lgse/strata#1583
- A query also matches the translated title with its spaces removed, so Omarchy主题变体 finds Omarchy 主题变体, and Omarchy變體 finds Omarchy 變體 under 正體中文. lgse/strata#1583, lgse/strata#1745
- In Search settings, Search themes, and Search templates, Ctrl+A selects the query on any keyboard layout. Ctrl+Shift+A, Ctrl+Alt+A, and Ctrl+Super+A do not. lgse/strata#1576
- A query with no match shows "No settings match your search." under the title Search results. lgse/strata#849
- Escape in a non-empty search field clears the query and restores every row; the next Escape closes Settings. lgse/strata#849
- Searching changes no saved preference. lgse/strata#849
- Searching "keybindings" finds Show F1 Shortcuts button. lgse/strata#1376
- Searching "license" opens About with the License row; searching "custom actions" opens Actions with the custom-actions list. lgse/strata#1554, lgse/strata#1453
- Searching "render documents" or "markdown" shows General's Render documents by default row; a query it does not match hides it. lgse/strata#1554, lgse/strata#1454
- A query that does not match Custom actions hides the installed-actions list and the broken-action problems, so "import" hides the list. lgse/strata#1554, lgse/strata#1453
- On a package-managed install, the managed-install row shows only for queries matching Check for updates, so "channel" hides it. lgse/strata#1554, lgse/strata#1453
- Searching "miller" finds Show sizes in Columns view. lgse/strata#1564 (unverified)
- Searching "catppuccin", "brand palette", or "monochrome" finds Appearance's File icon colors row. lgse/strata#1588 (unverified)
- Searching "font" shows Appearance's Interface font row. lgse/strata#1696
- Searching "typeface" or "family" shows the Interface font row. lgse/strata#1696 (unverified)
- Searching "troubleshoot" or "ffmpeg" opens Diagnostics with its Run diagnostics row. lgse/strata#1735
- Searching "add-ons" or "plugins" opens the Integrations page. lgse/strata#1748
- On an in-place install, searching "rollback", "downgrade", or "previous version" opens Updates with the Install a specific release row. lgse/strata#1781 (unverified)
- Searching "nfs", "smb", or "monitor" shows the Watch network folders row. lgse/strata#1729 (unverified)
- With icon-only navigation, the search field becomes a Search settings button that opens the field in a popover; the query and focus survive resizing. lgse/strata#849
- Rows unavailable on this installation stay hidden when a query is cleared. lgse/strata#849 (unverified)

### Watch network folders

- Settings → General → Performance shows a Watch network folders switch before Thumbnail workers, on by default; the Auto-refresh folder row is gone. lgse/strata#1729
- The row reads "Check open folders on network shares every few seconds for changes made on other computers. When off, those changes show only after a refresh." lgse/strata#1729
- The choice saves as `watch_network_folders`; a saved `auto_refresh_interval` is ignored and dropped from `settings.toml` on the next save. lgse/strata#1729

### Show sizes in Columns view

- General → Browsing has a Show sizes in Columns view switch, on by default. lgse/strata#1564
- Changing the switch in one window updates the open Settings switch in every other window. lgse/strata#1564

### Search limits

- Settings → General → Search & filtering shows Search time limit and Search entry limit after Open search results directly and before Global search exclusions. lgse/strata#1667
- Search time limit offers 10 s, the default, 30 s, 1 min, 5 min, 15 min, and No limit. lgse/strata#1667
- Search entry limit offers 200,000, the default, 500,000, 1,000,000, 5,000,000, and No limit. lgse/strata#1667
- The time row reads "Stop indexing a search after this long. Slow or network mounts need longer to list every folder." lgse/strata#1667
- The entry row reads "Stop indexing a search after this many files and folders. Higher limits use more memory." lgse/strata#1667
- The choices save as `search_time_limit`, in seconds, and `search_entry_limit` in `settings.toml`; 0 means No limit. lgse/strata#1667
- A hand-edited `search_time_limit = 45` shows 1 min, and `search_entry_limit = 300000` shows 500,000. lgse/strata#1667
- A saved value above 900 seconds or 5,000,000 entries loads as No limit. lgse/strata#1667 (unverified)
- Changing a limit in one window's Settings shows the same choice in another window's Settings. lgse/strata#1667
- Searching "timeout" finds Search time limit, and "memory" finds Search entry limit. lgse/strata#1667 (unverified)

### About

- About shows Strata's version, build commit, and GTK version, plus Website, Source code, Report an issue, and License (MIT) links. lgse/strata#19, lgse/strata#849
- Copy version info copies the version, description, commit, toolkit, author, and license to the clipboard. lgse/strata#849 (unverified)
- In a debug build, the BUILD group's Version row ends in `+debug`, such as `1.0.0+debug`. So does the first line of the copied version info. lgse/strata#1676
- In a release build, the Version row and the copied version info show no suffix. lgse/strata#1676
- The About description, and the second line of the copied version info, read "Navigate every layer.", translated in every language. lgse/strata#1673 (unverified)
- The About logo tile fills with the theme's surface color inside a 1px border in the theme's border color. lgse/strata#1673 (unverified)

### Show F1 Shortcuts button

- Turning off General → Browsing → Show F1 Shortcuts button hides the footer shortcuts button in every open window; F1 still opens the reference. lgse/strata#1376

### Default directory

- With no saved choice, General → Startup → Default directory reads Home directory, and Reset is disabled. lgse/strata#943 (unverified)
- Choosing a folder saves it and shows it with `~/` for paths under home. lgse/strata#943
- A new window without an explicit target or restored tabs opens at the chosen folder; `browser/tabs/session-restore` owns when tabs restore. lgse/strata#943, lgse/strata#1532
- Reset restores the home directory as the default. lgse/strata#943
- A saved folder counts as gone when it is not a folder, or when it is missing beside other entries in a parent with no mount points. lgse/strata#1729
- If the saved folder is gone, a new window opens home and the saved choice is cleared. lgse/strata#943, lgse/strata#1729
- A missing folder on an unplugged drive, an unmounted share, or in an empty or unreadable parent is not gone. The window opens it and keeps the choice. lgse/strata#1729
- If the check has not finished after 2 s, the window opens the saved folder and keeps the choice. A stopped NFS or FUSE mount does this. lgse/strata#1729
- That folder loads by itself once the mount answers. lgse/strata#1729

### Hidden files

- Ctrl+H or Ctrl+. toggles hidden files. lgse/strata#240
- Ctrl+Shift, Ctrl+Alt, or Ctrl+Super with H or . does not toggle hidden files. lgse/strata#240, lgse/strata#1576 (unverified)
- The Appearance menu's Hidden files row shows the `Ctrl+H` hint in English and an eye icon reflecting the current state. lgse/strata#240, lgse/strata#1576
- That row is a check menu item whose checked state follows Ctrl+H and other windows. lgse/strata#1467, lgse/strata#1544
- The folder-background context menu offers Show Hidden Files or Hide Hidden Files, matching the current state. lgse/strata#240
- Toggling shows or hides hidden entries in every open column without reloading the directories. lgse/strata#201
- The choice is saved as `show_hidden` and restored on the next launch. lgse/strata#144
- Toggling in one window applies to every open window and to new columns. lgse/strata#518
- Shown hidden items draw their icon or thumbnail and name at 65% opacity in Columns, Icons, and List. lgse/strata#927

## Design

[docs/preferences.md](https://github.com/lgse/strata/blob/fd6327265eaa3266f8420fe8bd25e965146344b0/docs/preferences.md) lists every stored preference, its consumer, and the rules for adding one.

- Settings is a layer inside the window, built on first open. Appearance, Actions, and Updates build on first selection, because Updates starts package-manager detection and network work. Integrations joined them (lgse/strata#1748). Diagnostics builds with the panel but runs no check until Run, following the same rule (lgse/strata#1735).
- Settings pages only edit preferences; consumers bind at construction. Opening Settings once had applied saved Folder peeking, which hid the missing startup binding (lgse/strata#515).
- Settings refuses to open while another modal is visible rather than stacking under it, because its lazily added overlay stayed below later dialogs (lgse/strata#865).
- Closing Settings returns focus to the file list, not to the gear or other chrome that opened it. Only a focused filter session gets its field or results back (owner decision, lgse/strata#1430, lgse/strata#1533).
- Settings is hidden rather than removed, so it captures its focus origin on each show and restores focus when the hide completes. Every close route, and the layer unrealizing with its window, runs the same dismissal hooks (lgse/strata#1430, lgse/strata#1457, lgse/strata#1533).
- A choice button's value goes in its description, so its name stays stable for E2E locators and Settings search. Options are radio menu items so screen readers announce the chosen one (lgse/strata#1467, lgse/strata#1544).
- Navigation buttons, page titles, and search routing come from one `NAVIGATION` table keyed by page id. Matching label strings with an About fall-through had sent Actions and About matches to the wrong page (lgse/strata#1453, lgse/strata#1554).
- Every row or section needs a search target, and a test fails on any without one. docs/preferences.md asks for keywords in every catalog. Status-only content takes its section's target instead of an exemption (lgse/strata#1454, lgse/strata#1554).
- Chinese and Japanese titles have no spaces between words but do around Latin words, so unspaced queries match inside words and against joined titles (lgse/strata#1583).
- Search filters the existing bound rows instead of building copies, and the query is not saved. Installation-specific availability is tracked apart from search matches so clearing a query cannot reveal it (lgse/strata#849).
- The Settings Keybindings page and the F1 reference were two hand-maintained catalogs that drifted. Generating both from one catalog was rejected; F1 already had mode- and view-aware sections (lgse/strata#1374).
- Page scrollers refuse horizontal scrolling. GTK treats an `External` horizontal policy as scrollable, so sideways deltas panned the page with up to 100 px of overshoot even with no horizontal range (lgse/strata#1712, lgse/strata#1719).
- A page bin reports no horizontal minimum and gives its content the viewport width. A content minimum can then neither restore the pan nor clip the right edge. It passes its child's request mode through, because a fixed one cached a single-line height for wrapped text (lgse/strata#1719).
- The dark band at scroll walls was GTK's default overshoot gradient; Settings clears it as context menus and popovers already did (lgse/strata#1719).
- The default directory is checked on a worker after the window opens, instead of with `is_dir()` on the UI thread. Any failed check once cleared the choice; now only a folder proven missing or not a folder does (lgse/strata#1729).
- Hidden entries stay in memory with an `is_hidden` flag and a filter model hides them, instead of re-enumerating every column and reinstalling monitors (lgse/strata#200, lgse/strata#201).
- Ctrl+. was added beside Ctrl+H rather than replacing it, to keep existing habits (lgse/strata#121).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-17 | lgse/strata#1719 | fix | Made Settings pages scroll vertically only and cleared the overshoot bands, so pages no longer pan sideways or draw dark stripes at scroll walls. |
| 2026-10-15 | lgse/strata#1673 | perf | Drew the About logo in theme colors, so it no longer sits on a near-black tile in light themes, and changed the tagline to "Navigate every layer." |
| 2026-10-11 | lgse/strata#1564 | feat | Added the Show sizes in Columns view switch to General → Browsing and to Settings search. |
| 2026-10-11 | lgse/strata#1570 | fix | Showed the empty-notes message for comment-only release notes and reaped the AUR and Omarchy update launchers. |
| 2026-10-10 | lgse/strata#1554 | fix | Routed Settings search by page id and registered Render documents, the custom-actions list and problems, and the managed-install row. |
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

None known.
