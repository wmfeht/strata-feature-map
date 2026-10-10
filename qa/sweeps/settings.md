---
title: Settings sweep
reviewed_at: 72b840e69d6f0df9d33fb5583e62a3a2944886a1
triggers: [src/ui/preferences.rs, src/ui/browser/preferences.rs, data/locales/messages/**]
tools: [docs/preferences.md, docs/themes.md, docs/internationalization.md, tests/e2e/harness/environment.py]
---

## Scope

The Settings panel and the preference lifecycle behind every row. Preferences: opening, navigation, responsive layout, Settings-wide search, About, and the General rows no feature claims (Show F1 Shortcuts button, Default directory, hidden files). Storage: saving, recovery of a damaged `settings.toml`, and live synchronization across windows. Language: the selector, locale detection, and translated text. Date format: the three formats and the relative buckets. Themes: the bundled library, custom theme files and their editor, syntax palettes, `@strata_*` tokens, Element glow, Interface renderer, Reduce motion, theme-tinted icons, and Follow Omarchy with its variants.

For every control this sweep proves the binding: the file changes, the other window follows, a seeded value applies before Settings opens. What a preference does inside the browser (click modes, view mode, density, folder peeking, sort defaults, text size) belongs to `browser`. The system file chooser opt-in, update channels, custom actions, and preview rows belong to the sweeps named under Hand-offs.

## Setup

- Preferences live at `$XDG_CONFIG_HOME/strata/settings.toml` under the throwaway HOME. `DEFAULT_PREFERENCES` in `tests/e2e/harness/environment.py` is the baseline; every seeded file starts from it.
- A seeded file with every key non-default before launch, among them `show_hidden = true`, `date_format = "iso"`, `language = "ja"`, `theme = "gruvbox-dark"`, `element_glow = false`, `text_size = 8`, `omarchy_variant = "darker"`, `interface_renderer = "cairo"`.
- Two windows of one process, Settings open in both on different pages, plus a second process on the same HOME for the cross-process cases.
- Custom themes under `$XDG_CONFIG_HOME/strata/themes/`: `extreme.toml` with `background = "#ff0000"`, `text = "#ffffff"`, and the other 12 colors pure red or white; `bad-color.toml`, `missing-key.toml`, `tokyo-night.toml`, and a file of unparseable TOML.
- A screenshot set per theme with `import` on the private display, repeated in Columns, Icons, and List. It holds a context menu, a modal dialog, a rename editor, a cut item, a focused selection, a hovered row, a code preview, and the Settings panel.
- Locale runs: `LANGUAGE=ar:ja`, `LANGUAGE=pt_PT:fr LANG=C`, `LC_ALL= LC_MESSAGES=ko_KR.UTF-8`, `LANG=de_DE.UTF-8@euro`, `LANG=ru_RU.UTF-8`, and all four empty. Install a CJK font for the ja and ko runs; none of the ten languages is right-to-left.
- A dotfiles folder at `$HOME/dotfiles` and a second on `/dev/shm`, for `settings.toml` and theme files symlinked across filesystems. A root-owned file and link made with `sudo` for the ownership cases.
- A fake Quattro state at `$HOME/.local/state/omarchy/current/theme.name` and `current/theme/colors.toml` under the throwaway HOME. `current/theme` is a symlink, the way Omarchy lays it out. A script renames it away and back with 0, 1, and 5 s gaps.
- Date fixtures made with `touch -d` at 59 s, 61 s, 59 min, 23 h 59 min, 24 h 1 min, 6, 7, 30, and 31 days, 1 year, 1970, 2100, and 30 s and 2 min ahead. Runs use `TZ=UTC`, `TZ=America/New_York` on 2026-03-08 and 2026-11-01, and `TZ=Pacific/Kiritimati`.

## Probes

- For each General and Appearance control: change it, read `settings.toml`, check window B without reopening Settings, restart, then reset; record the key and value written.
- Launch on the fully seeded file and verify each value in the first window before Settings is opened, including lazily built Icons and List panes.
- Flip the same switch in both windows in opposite directions within a second, ten times; both controls and the file must agree at the end.
- Traverse every page with Tab and arrows only; each control's accessible name must match its label in English and in Japanese.
- Read each choice button and option over AT-SPI after changing it from window B, after a hand-edited seed, and under Japanese.
- Watch the log while Appearance, Actions, and Updates build on first selection, and while a search query hits a page that has not built yet.

### settings/preferences

- Open Settings in both windows, close one with a backdrop click and the other with Escape, reopen each; note which page shows.
- Open Settings from the gear and close it by backdrop click with the cursor folder empty, still loading, and deleted from a terminal meanwhile; press Down after each.
- Focus a filter result, open Settings with the gear, and press Escape; repeat with the filter field focused but empty, and with the filter in a non-active Columns pane.
- Resize the window across the 900 and 1250 px panel widths at text size 8 and 48, crossed with compact and airy density. Check the navigation, the search popover with a query typed, and dependent rows with arrows.
- Search "tezt size", "  ", "keybind", "シ" in a Japanese run, and a query matching only an Updates row on a package-managed build; clear each with Escape and count visible rows.
- Set Default directory to a Unicode path, then `rm -rf` it, `chmod 000` it, and replace it with a symlink to `/dev/shm`; open a new window after each and read the row.
- With Restore open tabs on and a `tabs.toml` whose every entry is invalid, plain-launch with the Default directory deleted, then with it `chmod 000`.
- Toggle hidden files with Ctrl+. while a rename editor is open, while a filter is active, in the file chooser, and on a folder of 10k dotfiles; compare Columns, Icons, and List.

### settings/preferences/storage

- Hand-edit while running: `show_hidden = "yes"`, a deleted `theme` key, an unknown key, a trailing `[` on the last line. Restart after each, read the log, change one preference, and diff the file.
- Replace `settings.toml` with a FIFO, and with a 0600 file in a `chmod 555` directory; change a preference and `ls -la` for leftover temporary files.
- Symlink `settings.toml` into `/dev/shm`, through a relative chain of three links, into a `chmod 555` target folder, and to a hard-linked file; change a preference, restart, and `ls -li` every link and target.
- Swap the symlink for one to another file while Strata runs, and make the whole `~/.config/strata` a symlink as well; change a preference and read both files.
- Make the target 0644 with an ACL entry, then 0400; change a preference and compare `getfacl` and `stat` before and after.
- With saves failing, toggle switches by keyboard in window A while B is focused, with Properties open, and during an Omarchy theme change. Count dialogs, then `chmod 755` and fail again.
- Seed a broken `settings.toml`, then make the first change from the file chooser, from window B while A is focused, and from a second Settings page. Count dialogs per session.
- Run the failing-save cases under `language = "ja"` and `"de"` with a 200-character path; check the dialog text wraps and the path stays whole.
- Edit the file externally while running, then change a different preference in Strata; read which values the file holds.
- Change the same preference in two processes sharing one HOME, quit both in each order, and relaunch.
- Loop a switch 50 times from the keyboard and `kill -9` the process midway; the file must parse on the next launch.

### settings/preferences/language

- Run each locale set in Setup and read the selector's initial value, the window title language, and the footer count.
- Seed `language = "FR"`, `"pt-br"`, `"ja "`, and `"zz"`; read the selector and the file after the first change.
- Choose 日本語 in window A, open window B, press Restart now with a rename editor open in B and again during a running copy.
- Select 1, 2, 5, 11, and 21 items under Russian, 0 and 1 under French and Português (Brasil); read the footer count, a 1.5 MB size, and a 1 234 567 byte Properties size.
- Run Deutsch and Русский at the 1250 px panel width and in the destructive-delete dialog; look for clipped labels, broken Hangul in Korean, and missing-glyph boxes without CJK fonts.

### settings/preferences/date-format

- Show the Setup date fixtures in Columns, Icons, List, and a preview under each format; compare the 61 s, 24 h 1 min, 7 day, and 31 day boundaries.
- Run `TZ=America/New_York` on both DST days and `TZ=Pacific/Kiritimati`; compare the weekday and week buckets with `date -d`.
- Change the format in window A while window B is idle for two minutes; watch the 30 s refresh relabel the 59 s and 59 min files.
- Cross each format with ja, de, and ru: month and weekday names, Long format word order, and the separator in `2026-09-17 14:30`.
- Seed `date_format = " ISO-8601 "`, `"LONG"`, and `"yesterday"`; read the menu and the file after one change.
- Keep the format menu open across a minute boundary, then change the language and restart; read each option's AT-SPI description against its visible example.

### settings/themes

- Apply `extreme.toml` and walk the screenshot set in all three modes, the sidebar, footer, search palette, file chooser, progress dialog, scrollbars, and loading skeletons; any pixel not red or white is a lead.
- Drop `bad-color.toml`, `missing-key.toml`, `tokyo-night.toml`, a 0-byte file, a `chmod 000` file, a `.TOML` extension, and a 1 MB file into the themes directory. Do it while running and again before launch; count the cards and read the log.
- In the editor, save a 300-character name, a name equal to a bundled theme, `../escape`, and an emoji-only name.
- Save a theme while its `<id>.toml` is a directory, a `chmod 000` file, and a link to `/dev/shm`; also with `<id>-2.toml` to `<id>-9.toml` present. List the folder after each.
- Make the themes folder a symlink, then `chmod 555` it, and save a theme; read the editor's error and the folder.
- Open the editor in both windows, change swatches in A, then in B, then in A again; close Settings in B, then A, and open a third window. Repeat closing A first.
- Mid-preview, change text size with the keyboard, toggle Element glow from window B, change `xft-dpi`, and rewrite `colors.toml` while following Omarchy; then Cancel and compare every window.
- Mid-preview, close the window with the compositor's close shortcut, quit the last window, and close a window that never opened Settings; relaunch and read the theme.
- Mid-preview, click the selected card, another card, and Follow Omarchy; then press Cancel and Add theme and read the swatches.
- Write a custom theme with background luminance near 0.4 (`#9a9a9a` and `#a0a0a0`) and check its Light/Dark filing with search and filter combined.
- Cross Element glow, Reduce motion, and `gtk-enable-animations` off and on; then choose Cairo with `GSK_RENDERER=` exported empty and press Restart now from window B.

### settings/themes/icons

- Switch themes with an Icons pane at 32 px and at 256 px and a List pane side by side; compare outline weight and color in the same screenshot, then repeat under `GDK_SCALE=2`.
- Under `extreme.toml`, open the item menu on a Trash entry and the Empty Trash dialog; the destructive icon must take the danger color, not the accent.
- Fill a folder with 300 distinct extensions and language files, scroll to the end and back in Icons and List; watch for icon flashes and criticals as the cache evicts.
- Name files `Makefile`, `makefile`, `Dockerfile.dev`, `main.RS`, `.rs`, and a directory `lib.rs`; compare the icon in the listing and in a Ctrl+F result.
- Collapse and expand the sidebar after a theme change; icons in collapsed rows must match the expanded ones.

### settings/themes/omarchy

- With the fake state, enable Follow Omarchy and edit `colors.toml` live: an invalid `background`, a missing `accent`, `selection = "nope"`, only `color5`-style keys, then a light palette. Read both windows after each save.
- Run the rename script at 0, 1, and 5 s gaps, then point the `current/theme` symlink at a missing target, truncate `theme.name` and `colors.toml` to 0 bytes, and `chmod 000` the directory.
- Seed `mode = "omarchy"` with no state, `omarchy_variant = "HIGH_CONTRAST"`, `"darker "`, and `"neon"`; read the Appearance page and the file after one change.
- Apply Darker and High contrast to a pure white and a pure black palette; measure text, border, and accent contrast from screenshots of a menu, a dialog, and a code preview.
- Turn Follow Omarchy off in window A while `colors.toml` is being rewritten, then `rm -rf` the state while the variant row has keyboard focus.

## Hand-offs

- Browsing mode, density, click counts, folder peeking, sort defaults, and text size as they act in the file views → `browser`.
- Properties dialog timestamps and sizes → `browser`.
- System file chooser opt-in under Desktop integration and the chooser itself → `integration`.
- 10xer mode toggle and custom actions pages → `integration`.
- Automatic updates, release channel, and the Updates page → `app`.
- Window buttons rows and the F1 shortcuts reference → `app`.
- Restore open tabs under General → Startup and the tab session it controls → `browser`.
- Focus return after closing dialogs other than Settings → `app`.
- Focus return after closing the search palettes → `browser`.
- Video backend, autoplay, text wrap, render-by-default rows, and syntax highlighting inside the preview panel → `preview`.
- Thumbnail workers and thumbnail rendering → `browser`.
