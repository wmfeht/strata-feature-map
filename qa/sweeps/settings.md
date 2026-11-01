---
title: Settings sweep
reviewed_at: 44bfeab305cfb68993bafcf4794fe0bbf7ff1433
triggers: [src/ui/preferences.rs, src/ui/browser/preferences.rs, data/locales/messages/**, data/locales/de.json, data/locales/en.json, data/locales/es.json, data/locales/fr.json, data/locales/hu.json, data/locales/it.json, data/locales/ja.json, data/locales/ko.json, data/locales/pt-BR.json, data/locales/ru.json, data/locales/vi.json, data/locales/zh-CN.json, data/locales/zh-TW.json]
tools: [docs/preferences.md, docs/themes.md, docs/internationalization.md, docs/diagnostics.md, scripts/headless/environment.py, tests/fixtures/harness.json]
---

## Scope

The Settings panel and the preference lifecycle behind every row. Preferences: opening, navigation, responsive layout, Settings-wide search (including Keyboard rows), About, page scrolling, and the General rows no feature claims (Units, Show F1 Shortcuts button, Watch network folders, Default directory, hidden files). Storage: saving, recovery of a damaged `settings.toml`, and live synchronization across windows. Language: the selector, locale detection, and translated text. Date format: the three formats and the relative buckets. Diagnostics: the on-demand dependency checks, install commands with Run in terminal on Diagnostics and Integrations, and the copied report. Themes: the bundled library, custom theme files and their editor, syntax palettes, `@strata_*` tokens, isolation from desktop GTK styling, Element glow, Interface renderer, font rendering, Reduce motion, File icon colors, the Show thumbnails and STL model thumbnails switches, the user stylesheet, the uncomposited popup fallback, Interface font, Corner roundness, Frame density bar spacing, theme-tinted and Catppuccin file icons, and Follow Omarchy with its variants.

For every control this sweep proves the binding: the file changes, the other window follows, a seeded value applies before Settings opens. What a preference does inside the browser (click modes, view mode, density, folder peeking, sort defaults, text size) belongs to `browser`. The system file chooser opt-in, update channels, custom actions, the Integrations page, and preview rows belong to the sweeps named under Hand-offs. Diagnostics proves each check's verdict and fix text; the features it checks belong to their own sweeps.

## Setup

- Preferences live at `$XDG_CONFIG_HOME/strata/settings.toml` under the throwaway HOME. `DEFAULT_PREFERENCES` in `scripts/headless/environment.py`, read from the `preferences` table of `tests/fixtures/harness.json`, is the baseline; every seeded file starts from it.
- A seeded file sets every key non-default before launch. Among them: `show_hidden = true`, `date_format = "iso"`, `language = "ja"`, `theme = "gruvbox-dark"`, `element_glow = false`, `text_size = 8`, `omarchy_variants = { <fake theme name> = "lighter" }`, `interface_renderer = "cairo"`, `columns_show_sizes = false`, `file_icon_colors = "theme"`, `show_thumbnails = false`, `stl_thumbnails = true`, `corner_roundness = 0`, `interface_font = "DejaVu Serif"`, `search_time_limit = 0`, `search_entry_limit = 5000000`, `unit_system = "imperial"`.
- Two windows of one process, Settings open in both on different pages, plus a second process on the same HOME for the cross-process cases. The portal chooser runs on that HOME through `scripts/chooser-dev.sh`.
- Custom themes under `$XDG_CONFIG_HOME/strata/themes/`: `extreme.toml` with `background = "#ff0000"`, `text = "#ffffff"`, and the other 12 colors pure red or white; `bad-color.toml`, `missing-key.toml`, `tokyo-night.toml`, and a file of unparseable TOML.
- A screenshot set per theme with `import` on the private display, repeated in Columns, Icons, and List. It holds a context menu, a modal dialog, a rename editor, a cut item, a focused selection, a hovered row, a code preview, and the Settings panel.
- Locale runs: `LANGUAGE=ar:ja`, `LANGUAGE=pt_PT:fr LANG=C`, `LC_ALL= LC_MESSAGES=ko_KR.UTF-8`, `LANG=de_DE.UTF-8@euro`, `LANG=ru_RU.UTF-8`, `LC_MESSAGES=hu_HU.UTF-8 LANG=C`, `LANGUAGE=hu`, `LANG=zh_TW.UTF-8`, `LANGUAGE=zh-Hant:ja`, `LC_ALL=zh_MO.UTF-8`, `LANG=zh_MY.UTF-8`, `LANGUAGE=zh-Hans-TW`, `LANGUAGE=zh-Hant-HK`, and all four empty. Install CJK fonts with Simplified and Traditional Chinese glyphs, such as Noto Sans CJK SC and TC, for the ja, ko, and zh runs; none of the thirteen languages is right-to-left.
- A hostile desktop GTK setup under the throwaway HOME: `~/.config/gtk-4.0/gtk.css` with `* { outline: 3px solid red; font-family: serif; }`, `label { letter-spacing: 1px; color: red; }`, `button { min-width: 60px; padding: 12px; }`, `scrollbar { -gtk-icon-size: 40px; }`, and `@define-color strata_accent red;`; a `settings.ini` naming an installed desktop theme with `gtk-application-prefer-dark-theme=1`; and `~/.local/share/themes/StrataEmpty/gtk-4.0/gtk.css` holding the same rules.
- A dotfiles folder at `$HOME/dotfiles` and a second on `/dev/shm`, for `settings.toml` and theme files symlinked across filesystems. A root-owned file and link made with `sudo` for the ownership cases.
- A fake Quattro state at `$HOME/.local/state/omarchy/current/theme.name` and `current/theme/colors.toml` under the throwaway HOME. `current/theme` is a symlink, the way Omarchy lays it out. A script renames it away and back with 0, 1, and 5 s gaps.
- A user stylesheet at `$XDG_CONFIG_HOME/strata/style.css` with a valid rule using `@strata_accent`, a rule GTK rejects such as `label { color: nope; }`, and a layout rule such as `.sidebar-shell { margin: 12px; }`; a 1 MB copy and a non-UTF-8 copy beside it.
- An uncomposited X11 session: the private Xvfb alone, then Xvfb with openbox and no compositor. No client owns the `_NET_WM_CM_S0` selection, as python-xlib's `get_selection_owner` reports. `picom` or `xcompmgr`, installed but not started, so a script can start and stop it while Strata runs.
- Icon themes for the control icons: Breeze, Yaru, and Adwaita installed, plus a theme without symbolic icons, each selected through `settings.ini` before launch.
- A user GtkSourceView setup: `~/.local/share/gtksourceview-5/styles/strata-current.xml` and a `rust.lang` under `~/.local/share/gtksourceview-5/language-specs/`, and a `chmod 555` `~/.cache/strata`.
- An sshfs mount whose daemon a script stops with `kill -STOP` and resumes with `kill -CONT`, for the Default directory and save cases.
- Fonts for Interface font: a family with a quoted name, a family with no Latin glyphs, a bitmap-only family, and a family installed with `fc-cache` while Strata runs, then removed.
- For Diagnostics: a container or bind mounts that mask `bwrap`, `prlimit`, `ffmpeg`, `ffmpegthumbnailer`, `ffprobe`, and `unsquashfs` one at a time, plus `os-release` files for Arch, Debian, Fedora, openSUSE, and an unknown `ID`.
- Date fixtures made with `touch -d` at 59 s, 61 s, 59 min, 23 h 59 min, 24 h 1 min, 6, 7, 30, and 31 days, 1 year, 1970, 2100, and 30 s and 2 min ahead. Runs use `TZ=UTC`, `TZ=America/New_York` on 2026-03-08 and 2026-11-01, and `TZ=Pacific/Kiritimati`.

## Probes

- For each General and Appearance control: change it, read `settings.toml`, check window B without reopening Settings, restart, then reset; record the key and value written.
- Launch on the fully seeded file and verify each value in the first window before Settings is opened, including lazily built Icons and List panes.
- Flip the same switch in both windows in opposite directions within a second, ten times; both controls and the file must agree at the end.
- Traverse every page with Tab and arrows only; each control's accessible name must match its row label in English and in Japanese, except where a node's Behavior names another accessible name.
- Read each choice button and option over AT-SPI after changing it from window B, after a hand-edited seed, and under Japanese.
- Watch the log while Appearance, Actions, and Updates build on first selection, and while a search query hits a page that has not built yet.

### settings/preferences

- Open Settings in both windows, close one with a backdrop click and the other with Escape, reopen each; note which page shows.
- Open Settings from the gear and close it by backdrop click with the cursor folder empty, still loading, and deleted from a terminal meanwhile; press Down after each.
- Focus a filter result, open Settings with the gear, and press Escape; repeat with the filter field focused but empty, and with the filter in a non-active Columns pane.
- Search settings for "3d", "mesh", and "printing", then switch Language to Deutsch and Japanese and search again; read which rows show.
- Resize the window across the 900 and 1250 px panel widths at text size 8 and 48, crossed with Frame 0 and 12 px and Content 0 and 16 px. Check the navigation, the search popover with a query typed, and dependent rows with arrows.
- In a debug and a release build, compare the About Version row, the Copy version info clipboard text under `language = "ja"`, and the Updates page's version text.
- Search "tezt size", "  ", "keybind", "シ" in a Japanese run, and a query matching only an Updates row on a package-managed build; clear each with Escape and count visible rows.
- Set Default directory to a Unicode path, then `rm -rf` it, `chmod 000` it, and replace it with a symlink to `/dev/shm`; open a new window after each and read the row.
- With Restore open tabs on and a `tabs.toml` whose every entry is invalid, plain-launch with the Default directory deleted, then with it `chmod 000`.
- Under 简体中文 search 隐, `F1快捷键`, `隐藏 文件`, and 硬解, which only a keyword holds; under 日本語 search カラム. Count visible rows and read the opened page.
- On a `us,ru` layout with Russian active, and again with Caps Lock on, press Ctrl+A and Ctrl+Shift+A in Search themes and Search templates with a query typed; read the selection.
- With icon-only navigation and before Actions or Updates has been built, search "license", "custom actions", "markdown", and "preview". Read the opened page, its title, and the visible navigation entries.
- Repeat those searches under `language = "ja"` with the Japanese keywords, and with no custom actions installed but one broken action file present.
- Hand-edit `search_time_limit = -10`, `= 30.5`, and `= "5 min"`, then `search_entry_limit = 4294967296`; launch after each, read both Search limits rows and the log, change one other preference, and diff `settings.toml`.
- Flip Show sizes in Columns view in window A three times. Window B shows List, then has the Appearance menu open, then has Settings open on General.
- On every Settings page, swipe sideways on a touchpad, Shift+wheel, and drag-scroll past both ends at text size 8, 32, and 48 in a 640 px wide window; read the right edge and the scroll walls.
- At text size 48 and the narrowest window, open General, Appearance, Integrations, and Diagnostics after a Run; watch the log for allocation warnings and scroll to each last row.
- Seed `auto_refresh_interval = 300` with no `watch_network_folders`, then with `"yes"`, then `"no"`; launch, read the switch, change one other preference, and diff `settings.toml`.
- Set Default directory to a folder on the sshfs mount, stop the daemon, and open a new window. Resume after 1 s and after 30 s; then delete the folder on the server while stopped and resume.
- Set Default directory to a folder, then delete it from an otherwise empty parent, and again from a parent that also holds a mount point; open a new window after each and read the row.
- Click Restart now five times within a second after a renderer change, then with Properties open in another window; count Strata processes after the relaunch.
- Switch Units in window A before window B has ever opened Settings, then open B's General page and read its buttons and `settings.toml`.
- Seed `unit_system = "nautical"`, `unit_system = 1`, and `unit_system = "Imperial"`; launch, read the Units row, change another preference, and diff `settings.toml`.
- Search "kilometres", "kml", and "feet" under English and `language = "ja"`; read which rows show and which page opens.
- Toggle hidden files with Ctrl+. while a rename editor is open, while a filter is active, in the file chooser, and on a folder of 10k dotfiles; compare Columns, Icons, and List.
- Press Ctrl+, and click the gear over Properties, Compress, a delete confirmation, Customize…, and a dialog animating closed. Repeat over a dialog in another tab of the same window. Read Settings and the focused control each time.
- With Settings opened on General and the Keyboard page not yet built, then after it is built, search "rename", "Ctrl+E", and "remap"; read the opened page and which table shows.
- Search a key only the 10xer map gives, and a word shared by a General row and an action name; then clear with Escape and count visible rows on Keyboard.
- Rebind an action in `settings.toml` before launch, then search its old and new keys under English and `language = "ja"`.
- Compare the navigation's icon column with the search field's icon at text size 8 and 48, labelled and icon-only.
- Click the backdrop at each corner and edge strip around the Settings panel. Do it in a 640 px and a maximized window, at text size 8 and 48. Then click the panel padding, the navigation gap, and a scrollbar.
- In a `STRATA_UPDATER=disabled` build, search "update", "rollback", "release notes", and "channel" with labelled and icon-only navigation. Repeat on a pacman-owned prefix, reading the visible rows and navigation entries.

### settings/preferences/storage

- Write `stl_thumbnails = "yes"` and `stl_thumbnails = 1` into `settings.toml` before launch; read the switch and whether other keys survive.
- Hand-edit while running: `show_hidden = "yes"`, a deleted `theme` key, an unknown key, a trailing `[` on the last line. Restart after each, read the log, change one preference, and diff the file.
- Replace `settings.toml` with a FIFO, and with a 0600 file in a `chmod 555` directory; change a preference and `ls -la` for leftover temporary files.
- Symlink `settings.toml` into `/dev/shm`, through a relative chain of three links, into a `chmod 555` target folder, and to a hard-linked file. Change a preference, restart, and `ls -li` every link and target.
- Swap the symlink for one to another file while Strata runs, and make the whole `~/.config/strata` a symlink as well; change a preference and read both files.
- Make the target 0644 with an ACL entry, then 0400; change a preference and compare `getfacl` and `stat` before and after.
- With saves failing, toggle switches by keyboard in window A while B is focused, with Properties open, and during an Omarchy theme change. Count dialogs, then `chmod 755` and fail again.
- Seed a broken `settings.toml`, then make the first change from the file chooser, from window B while A is focused, and from a second Settings page. Count dialogs per session.
- Run the failing-save cases under `language = "ja"` and `"de"` with a 200-character path; check the dialog text wraps and the path stays whole.
- Seed `sidebar_order`, `folder_colors`, and `custom_icons` each with one bad entry among valid ones, then with only bad entries. Launch, change one preference, and diff `settings.toml`.
- Seed `send_to_recent_destinations` with one device whose value is a table and one whose list holds an integer; launch, open Send to, and diff after one change.
- Seed `chooser_list_columns` with `size = "wide"` beside valid `browser_list_columns`; open the file chooser and a List pane and read both widths.
- Seed a 5,000-entry `folder_colors` table with one bad value; time startup to the first painted window and read the colors.
- Edit the file externally while running, then change a different preference in Strata; read which values the file holds.
- Change the same preference in two processes sharing one HOME, quit both in each order, and relaunch.
- Run the browser and the portal chooser on one HOME. Edit `send_to_recent_destinations` and `omarchy_variants` in both, and `chooser_list_columns` from the real chooser. Diff `settings.toml` after each save.
- Make `settings.toml` invalid TOML while two processes run, change a preference in each, then repair the file and change another.
- Hold a `flock` on `~/.config/strata` from a shell, change preferences in two processes, release it, and diff `settings.toml`; repeat with `XDG_CONFIG_HOME` on the sshfs mount.
- In two windows, sort the Trash and an SFTP folder differently in each. Read each window's sort, then restart and read them again.
- Loop a switch 50 times from the keyboard and `kill -9` the process midway; the file must parse on the next launch.
- Change ten preferences within one second and quit at once; relaunch and diff `settings.toml` against the last values shown.
- Symlink `settings.toml` onto the sshfs mount, stop the daemon, change a preference, and quit; time the quit and read the log.

### settings/preferences/language

- Run each locale set in Setup and read the selector's initial value, the window title language, and the footer count.
- Seed `language = "FR"`, `"pt-br"`, `"ja "`, and `"zz"`; read the selector and the file after the first change.
- Choose 日本語 in window A, open window B, press Restart now with a rename editor open in B and again during a running copy.
- Select 1, 2, 5, 11, and 21 items under Russian, 0 and 1 under French and Português (Brasil); read the footer count, a 1.5 MB size, and a 1 234 567 byte Properties size.
- Seed `language = "zh-cn"`, `"zh"`, `"zh-tw"`, `"ZH-TW"`, and `"zh-HK"`; read the selector and the file after the first change.
- Under 简体中文, 日本語, and English, fail an archive extraction into a read-only folder and copy a 5 GB file to a FAT32 stick; read the spacing and stop between the two sentences.
- Under 正體中文, select 1, 2, and 3,000 items and read the footer count, a transfer duration, and a list of mixed item kinds; repeat under 简体中文 and compare.
- Under 正體中文 on an `en_US` system, with only Noto Sans CJK SC installed, then only TC, read Settings and a file list for mixed glyph forms.
- Under 简体中文, read the sidebar toggle tooltip in full, compact, and hidden states, and the password remember choices in a mount dialog.
- Under 简体中文, read the Tasks icon name in Customize… and the Danger color label in Add theme.
- Under Magyar, select 1, 2, and 3,000 items and read the footer count. Read a 1.5 MB size, a 1 234 567 byte Properties size, and a transfer rate. Fail a copy into a read-only folder and read the case after the colon.
- Run Deutsch, Magyar, and Русский at the 1250 px panel width and in the destructive-delete dialog. Look for clipped labels, broken Hangul in Korean, and missing-glyph boxes without CJK fonts.

### settings/preferences/date-format

- Show the Setup date fixtures in Columns, Icons, List, and a preview under each format; compare the 61 s, 24 h 1 min, 7 day, and 31 day boundaries.
- Run `TZ=America/New_York` on both DST days and `TZ=Pacific/Kiritimati`; compare the weekday and week buckets with `date -d`.
- Change the format in window A while window B is idle for two minutes; watch the 30 s refresh relabel the 59 s and 59 min files.
- Cross each format with ja, zh-CN, de, hu, and ru: month and weekday names, Long format word order, and the separator in `2026-09-17 14:30`.
- Seed `date_format = " ISO-8601 "`, `"LONG"`, and `"yesterday"`; read the menu and the file after one change.
- Keep the format menu open across a minute boundary, then change the language and restart; read each option's AT-SPI description against its visible example.

### settings/diagnostics

- Run under `GIO_USE_VFS=local`, with no session bus (`env -u DBUS_SESSION_BUS_ADDRESS`), with no network (`unshare -rn`), and with `fs.inotify.max_user_watches=4096`; read each row and the summary.
- Run with each Setup tool masked in turn, and with each `os-release`; read the install command, then use Run in terminal and run diagnostics again.
- Press Run twice quickly, close Settings mid-run, then reopen Diagnostics and run again; watch the log and the temporary directory.
- Close the window mid-run and quit the last window mid-run; list `$TMPDIR` for leftover `strata-diagnostics-*` directories.
- Copy the report under `language = "ja"` and `"zh-TW"` and paste it into a text editor; compare section names, statuses, and the System fields with the page.
- Run with no terminal resolvable, then with a terminal that exits at once; press Run in terminal and read the row under each install command.
- Repeat both on an Integrations install command, and with `$TERMINAL` set to a missing program. Press the button twice quickly and read the row and the process list.
- On Integrations, press Run in terminal with `$TERMINAL` unset, no `xdg-terminal-exec`, and no listed terminal on `PATH`. Install one and press it again without Refresh.
- Run with one custom action that cannot run and one broken action file, then with neither; compare with Settings → Actions.
- Run a `STRATA_UPDATER=disabled` build with and without network. Repeat with an install marker under its prefix, then on a pacman-owned prefix with no marker. Read Installation, Update server, and the copied report.

### settings/themes

- Apply `extreme.toml` and walk the screenshot set in all three modes, the sidebar, footer, search palette, file chooser, progress dialog, scrollbars, and loading skeletons; any pixel not red or white is a lead.
- Drop `bad-color.toml`, `missing-key.toml`, `tokyo-night.toml`, a 0-byte file, a `chmod 000` file, a `.TOML` extension, and a 1 MB file into the themes directory. Do it while running and again before launch; count the cards and read the log.
- In the editor, save a 300-character name, a name equal to a bundled theme, `../escape`, and an emoji-only name.
- Save a theme while its `<id>.toml` is a directory, a `chmod 000` file, and a link to `/dev/shm`; also with `<id>-2.toml` to `<id>-9.toml` present. List the folder after each.
- Save names that slug to nothing (`日本語`, `!!!`, ` - `) three times. Repeat with `custom-theme.toml` as a dangling link, then as a directory; list the folder and read each card's name.
- Make the themes folder a symlink, then `chmod 555` it, and save a theme; read the editor's error and the folder.
- Open the editor in both windows, change swatches in A, then in B, then in A again; close Settings in B, then A, and open a third window. Repeat closing A first.
- Mid-preview, change text size with the keyboard, toggle Element glow from window B, change `xft-dpi`, and rewrite `colors.toml` while following Omarchy; then Cancel and compare every window.
- Mid-preview, close the window with the compositor's close shortcut, quit the last window, and close a window that never opened Settings; relaunch and read the theme.
- Under `extreme.toml`, open a swatch's color chooser and switch to its custom editor. Change the theme from window B while it is open, then press Tab through every control.
- Mid-preview, click the selected card, another card, and Follow Omarchy; then press Cancel and Add theme and read the swatches.
- Apply a custom theme with a translucent `accent` such as `rgba(79,214,255,0.5)`; compare focus outlines and the editor swatches seeded from it.
- Apply Material Lighter and Material Vivid and screenshot a selected row, a hovered row, the footer, dim column details, and a disabled menu item.
- Write a custom theme with background luminance near 0.4 (`#9a9a9a` and `#a0a0a0`) and check its Light/Dark filing with search and filter combined.
- Cross Element glow, Reduce motion, and `gtk-enable-animations` off and on; then choose Cairo with `GSK_RENDERER=` exported empty and press Restart now from window B.
- Cross `GSK_RENDERER=gl`, `vulkan`, and `cairo` with text sizes 8, 10, and 13 and `text-scaling-factor` 1.0, 1.1818, and 1.25 on a 1.25× monitor. Repeat under hint style none and full and with antialiasing off; zoom on `T`, `E`, and `I` in the sidebar and file list.
- Preset the desktop `font-rendering` key to manual, then automatic, before launch; change it while Strata runs; repeat the glyph checks, then on a GTK 4.14 build.
- Write custom themes with mid-gray backgrounds on either side of the flavor threshold, such as `#7f7f7f` and `#828282`, and a background GTK rejects; compare the file icon palette with the Light/Dark filing.
- With a custom theme selected, rewrite its file by atomic rename, then by in-place truncate-and-write; read both windows after each.
- Link the selected theme file to a target on `/dev/shm`, through a relative link, and to a target without `.toml`. Edit each target and read the window.
- Link the selected theme through a two-hop chain, then repoint the middle link at another file; rewrite both files and read the window.
- Point a link into a folder that does not exist yet, then create the folder and the target while Strata runs; read the theme list.
- Link two themes into one dotfiles folder and remove one link. Rewrite the other target and a sibling file beside it, then read the window and the log.
- Under a light theme with Element glow off, then on, open path completion, a folder peek, and the 10xer candidates popover. Zoom on each popover's edge.
- With the hostile `gtk.css` and `settings.ini`, walk the screenshot set in all three modes under a light and a dark theme, then compare against a run without them; any difference is a lead.
- With the hostile setup, launch under `GTK_THEME=Adwaita:dark`, under `GTK_THEME=HighContrast`, and as the portal chooser, then with desktop high contrast and the dark color scheme on; read the log and the window.
- Edit `~/.config/gtk-4.0/gtk.css` while Strata runs, then switch themes and open a new window; read Settings, a context menu, and a modal dialog.
- Rewrite the selected file during an editor preview and while following Omarchy; then Cancel, or turn Follow Omarchy off, and read every window.
- Select the custom `tokyo-night.toml`, delete it, then recreate it with new colors; read the theme cards in an open Settings page.
- With bundled Dracula selected, create and then delete `dracula.toml`; read both windows after each.
- Make `~/.config/strata/themes` a symlink to a dotfiles directory, then delete and recreate that directory while Strata runs; rewrite the selected file.
- Write 20 theme files 10 ms apart, the selected one last, then read the window colors and the log.
- With Settings open in two windows, rewrite the selected file and a non-selected file; read the cards and swatches in each window.
- In Tokyo Night, Catppuccin Latte, and Material Lighter, measure dim text on a hovered row, the highlight, and the selected-row fill; repeat with a custom theme copied from Catppuccin Mocha's catalog values.
- Save a custom file named after a bundled theme with that theme's catalog dim text; compare it with the bundled theme's loaded dim text.
- Under a light and a dark theme, read the Settings navigation, close, and search icons, and the About and release-notes icons, beside page text; repeat at Corner roundness 0.
- Create the user stylesheet from Setup while running, then edit it ten times 10 ms apart, replace it by atomic rename, make it a symlink into `/dev/shm`, `chmod 000` it, and delete it; read every window and the log after each.
- With the user stylesheet present, switch theme, follow Omarchy, open an editor preview, and change Corner roundness; read the overridden rules in each state.
- Launch with the 1 MB and the non-UTF-8 stylesheets, and as the portal chooser; read the window and the log.
- With `XDG_CONFIG_HOME` unset, then set to another directory, create `style.css` in each place; read which one applies.
- With the hostile setup, also name `StrataEmpty` in `settings.ini` and launch under `GTK_THEME=StrataEmpty`; walk the screenshot set and compare with a clean run.
- With the user GtkSourceView setup, open a Rust, Markdown, and shell preview, switch themes twice, and follow Omarchy; compare syntax colors with a run without it and read the log.
- With a user stylesheet that sets `.sidebar-row` padding, set Frame 7 px and Content Custom 11 px. Then switch theme, follow Omarchy, and open and Cancel an editor preview. Read bar and row spacing in both windows after each.
- At Frame 12, rail the sidebar, open the preview, open eight tabs, and open a Miller column with its header actions. Check that the bars line up.
- Dump the tree with the theme editor open, which the naming scenarios skip.
- In the uncomposited session, open a file context menu, the Appearance menu, a tooltip, path completion, a breadcrumb popover, and a folder peek; zoom on each edge. Repeat under openbox.
- With one of those popups open, start the compositor, then stop it; reopen each popup after each change and read a second window too.
- Uncomposited, add `popover contents { border-radius: 12px; box-shadow: 0 0 8px black; }` to the user stylesheet while running, then delete it; zoom on a context menu after each.
- Uncomposited, cross Element glow on and off with a light and a dark theme; open the 10xer candidates popover and a modal dialog.
- Launch the portal chooser uncomposited and open its context menu and path completion.

### settings/themes/icons

- Switch themes with an Icons pane at 32 px and at 256 px and a List pane side by side; compare outline weight and color in the same screenshot, then repeat under `GDK_SCALE=2`.
- Under `extreme.toml`, open the item menu on a Trash entry and the Empty Trash dialog; the destructive icon must take the danger color, not the accent.
- Fill a folder with 300 distinct extensions and language files, scroll to the end and back in Icons and List; watch for icon flashes and criticals as the cache evicts.
- Put a folder beside Catppuccin and Lucide file icons in List and in Icons at 32, 64, 128, and 256 px. Repeat at text size 8 and 48 and under `GDK_SCALE=2`; compare stroke weight and edge clipping.
- Give `main.rs` a saved custom color with no custom icon, then switch File icon colors between Brand and Theme colors; compare its icon in the listing and in Customize… preview.
- Follow Omarchy and switch the variant and `colors.toml` between light and dark palettes with Catppuccin icons visible under both File icon colors choices; read both windows.
- Switch File icon colors from window B while window A scrolls a folder of 300 code files in Icons view.
- Switch File icon colors from window B while window A drags a code file.
- Open About under a light custom theme, then switch to a dark one and Follow Omarchy while it stays open; compare the logo with a fresh About page.
- Collapse and expand the sidebar after a theme change; icons in collapsed rows must match the expanded ones.
- Under each Setup icon theme, compare every Settings dropdown arrow, the Appearance menu buttons, and the drive format dialog dropdown; repeat under `GDK_SCALE=2` and at text size 48.
- Step Text size, Corner roundness, and Thumbnail workers to each end so one step is disabled; hover each step under a light and a dark theme and read the icon color.
- Open Customize… → Custom color… and switch to the custom editor under each Setup icon theme; read its spin-button steps, then change the theme while it is open.

### settings/themes/icons/catppuccin

- Name files `Makefile`, `MAKEFILE`, `dockerfile.dev`, `Dockerfile.dev`, `.rs`, `Foo.D.TS`, `ARCHIVE.TAR.GZ`, `clip.MKV`, and a directory `lib.rs`; compare the icon in the listing, a Ctrl+F result, folder peek, and an archive preview.
- Name files `backup.tbz2`, `backup.txz`, `backup.tar.zst`, `movie.ts`, and `notes.m`; read which icon each takes.
- Name files `Cargo.TOML`, `.env.local`, `.ENV.LOCAL`, `tsconfig.app.json`, `TSCONFIG.APP.JSON`, `bash_history`, `x.d.ts.bak`, and a name ending in a dot; read which icon each takes.

### settings/themes/corner-roundness

- Seed `corner_roundness = 50.5`, `"60"`, `-10`, `250`, and no key; launch, read the stepper and the log, change one other preference, and diff `settings.toml`.
- Type 0, 15, 200, and 999 into the stepper, then use its buttons and arrow keys from 0 and 200; read the value and the file after each.
- Step from 0 to 200 in window A while window B shows Icons with a context menu, a modal dialog, and a rename editor open; screenshot each at 0, 60, and 200.
- At 0 and 200, look at switches, check boxes, tooltips, popovers, the search palette, progress dialogs, the file chooser, and the theme cards' swatches; note any corner that keeps its shape.
- At 0, 40, 50, 60, and 200, compare a switch on a Settings page with the Confirm switch in the action editor and a switch in a menu; read the track and knob corner shapes, on and off.
- At 0 and 200, cross text size 8 and 48 with Frame 0 and 12 px and Content 0 and 16 px; look for clipped corners and mismatched switch thumbs.
- Change roundness during an editor preview and while following Omarchy; then Cancel and compare every window.
- In the uncomposited session, step roundness from 0 to 200 with a context menu, a tooltip, and a folder peek open; start the compositor at 200 and reopen each.

### settings/themes/interface-font

- Choose each Setup font, then open a context menu, a modal dialog, a rename editor, the search palette, the file chooser, and a text, source, and command preview; read the family in each.
- Seed `interface_font = ""`, `"   "`, `"Missing Family"`, and a 300-character name; launch, read the button, the check mark, and the log, change one other preference, and diff `settings.toml`.
- Choose a font in window A while window B has the picker open with a query typed; read B's button, list, and check mark.
- Install a family with `fc-cache` while Settings is open, then uninstall the chosen one; reopen the picker and read the list and the window.
- Cross a chosen family with text size 8 and 48, Cairo and GL renderers, and the user stylesheet; zoom on clipped glyphs and row heights.
- Search fonts with a leading space, mixed case, and a translated "Default" under `language = "ja"`; read the list.

### settings/themes/omarchy

- With the fake state, enable Follow Omarchy and edit `colors.toml` live: an invalid `background`, a missing `accent`, `selection = "nope"`, only `color5`-style keys, then a light palette. Read both windows after each save.
- Run the rename script at 0, 1, and 5 s gaps, then point the `current/theme` symlink at a missing target, truncate `theme.name` and `colors.toml` to 0 bytes, and `chmod 000` the directory.
- Seed `mode = "omarchy"` with no state, beside a valid `theme` and `text_size`. In `[omarchy_variants]`, give one theme a valid variant and another `"HIGH_CONTRAST"`, `"darker "`, or `"neon"`.
- After that seeding, restart and read both themes' variants on the Appearance page and in the file, then again after one change.
- Apply Contrast to a pure white and a pure black palette, and to a mid-gray `background` with no `mode`; measure text, border, and accent contrast from screenshots of a menu, a dialog, and a code preview.
- Set `lighter_background` equal to `background`, then drop `dark_background`, `muted`, `lighter_background`, and `selection` one at a time.
- For each of those surface-key cases, under each variant, screenshot a hovered row, a selected row, a border, and a pane header.
- Under Contrast, set `mode = "light"` on a dark `background` and `mode = "dark"` on a light one, then `mode = "LIGHT"` and a numeric `mode`.
- Give three fake themes Lighter, Darker, and Contrast, then switch among them in varied order with Settings open in both windows; read `settings.toml` and both dropdowns after each switch.
- Write `theme.name` with a leading tab, then with an inner space, then with different letter case, then empty; read which `[omarchy_variants]` key each switch reads and writes.
- Start with a legacy global `omarchy_variant = "high_contrast"` and no Quattro state, change an unrelated preference, then create the state; repeat with an `[omarchy_variants]` entry already present for the active theme.
- While following, write a 12-digit hex `foreground`, `magenta = "#fff0000ff"`, an 8-digit `#rrggbbaa` `accent`, and an `rgba()` `selection` into `colors.toml`; open a new code preview and the Settings preview after each save.
- Truncate `colors.toml` mid-switch while window B opens a Markdown preview and window A opens Appearance; then restart with the state still invalid and read both.
- Turn Follow Omarchy off in window A while `colors.toml` is being rewritten, then `rm -rf` the state while the variant row has keyboard focus.
- Repoint `current/theme` with `ln -sfn`, by rename, and to a theme folder that is itself a symlink. After each, edit `colors.toml`, replace it by rename, and edit the old target; read both windows.

## Hand-offs

- Browsing mode, click counts, folder peeking, sort defaults, and text size as they act in the file views → `browser`.
- Frame and Content sliders in the titlebar Appearance menu, and Content spacing in file views → `browser`.
- Properties dialog timestamps and sizes → `browser`.
- System file chooser opt-in under Desktop integration and the chooser itself → `integration`.
- 10xer mode toggle and custom actions pages, including the action editor's toggles, tabs, and footer → `integration`.
- The Integrations page, its catalog, and installed providers → `remote`.
- The sandbox and previews behind a failing Diagnostics check → `preview`.
- GVfs and network backends behind a failing Diagnostics check → `remote`.
- Drives, phones, and cameras behind a failing Diagnostics check → `devices`.
- Terminal launch and custom actions behind a failing Diagnostics check → `integration`.
- Automatic updates, release channel, and the Updates page → `app`.
- Window buttons rows and the F1 shortcuts reference → `app`.
- The Keyboard page's tables, key capture, conflict notes, and Reset all → `app`.
- Input-method and dead-key composition in Settings fields → `app`.
- Restore open tabs under General → Startup and the tab session it controls → `browser`.
- Focus return after closing dialogs other than Settings → `app`.
- Focus return after closing the search palettes → `browser`.
- Units as it acts on route previews, open and new, in the browser and the chooser → `preview`.
- Video backend, autoplay, text wrap, render-by-default rows, and syntax highlighting inside the preview panel → `preview`.
- What Watch network folders checks and re-reads in open folders → `browser`.
- Dot-file changes made while hidden files are off → `browser`.
- Thumbnail workers, thumbnail rendering, and what Show thumbnails and STL model thumbnails change in the file views → `browser`.
- Remember sort and icon size per folder, Default sort, Forget all folder settings, and `folder-views.toml` → `browser`.
- Show sizes in Columns view as it acts on the Columns badge → `browser`.
- Search time limit and Search entry limit as they act on global search, pane filters, and the Partial results hint → `browser`.
