---
title: Browser sweep
reviewed_at: 72b840e69d6f0df9d33fb5583e62a3a2944886a1
triggers: [src/ui/browser.rs, src/ui/browser/events.rs, src/ui/browser/preferences.rs, src/ui/entry_list_model.rs, src/app/browser.rs, src/app/navigation.rs]
tools: [scripts/generate-fixture.sh, docs/keyboard-navigation.md, docs/preferences.md, tests/e2e/mutations]
---

## Scope

Everything that shows a folder and moves through it without changing files: selection by pointer and keyboard, with marquee, pointer intent, and click modes; the Columns, Icons, and List views with sorting and text size; Back, Forward, and Parent history, the location bar, Recent, startup arguments, and folder jump; Ctrl+K search, the Ctrl+F filter, and search exclusions; the sidebar places and pins; thumbnails with their disk cache and worker pool; Properties with its media, RAW, and size details; and the context menus, directory loading and monitoring, folder customization, scrolling, and tabs with their session restore.

Left to other sweeps: what happens once a press becomes a file drag, drops on tabs and sidebar rows, and every operation that changes files; the DEVICES rows and remote shares in the sidebar; the modal dialog shell, the shortcut footer, F1, and key precedence; what the preview panel renders; the Settings pages that hold the preferences named here; and the 10xer-mode key variants and the portal file chooser.

## Setup

- `scripts/generate-fixture.sh <root>` builds `1000`, `10000`, and `100000` entry folders, a 256-level `deep` tree, and `edge-cases` with a broken symlink and a non-UTF-8 name. Add dot-files, a `.hidden` file naming one visible entry, a 255-byte name, two names differing only by case, and a symlink to a folder.
- An unreadable folder (`chmod 000`) inside the fixture, and a folder to remove while it is open (`rm -rf` or `mv` from a shell), in every view.
- A slow directory: 2,000 images across every thumbnail format, plus 50 PDFs and 50 videos, with `$XDG_CACHE_HOME/thumbnails` emptied first so decoding is visible.
- Two windows of the same build for sidebar, pins, text size, tabs, monitoring, and Recent checks; open the same folder in both where the probe says so.
- Type to search on and off per probe: it changes what `h`, `j`, `k`, `l`, `p`, `/`, and plain letters do. `docs/keyboard-navigation.md` holds the key rules and `docs/preferences.md` the setting keys.
- Hand-written preferences go in `$XDG_CONFIG_HOME/strata/settings.toml` before launch; read the file back after every probe that saves something.
- An AT-SPI inspector such as Accerciser, or Orca, for probes that read roles, names, and checked or pressed states.
- Tab session probes need a disposable `$XDG_CONFIG_HOME`; read `strata/tabs.toml` back after each quit and before each launch.
- `tests/e2e/mutations/` holds the `click-modes`, `filter-results`, `keyboard-navigation`, `popover-scrolling`, and `view-switching` patches; `./scripts/e2e-mutation-check.sh <name>` is evidence when those areas changed.

## Probes

- Run each probe in Columns, Icons, and List; a difference between views is a finding unless the node names it.
- After each probe read the three signals apart: selection, keyboard cursor, and open-path marker; the preview must follow the cursor.

### browser/selection

- Shift+click across 500 entries in `100000`, Ctrl+click five of them out, scroll to the end, then press Shift+Up; count the selection.
- Press Escape with a rename editor open in one column and a multi-selection in another, then again; note what each press clears.
- Delete the focused entry externally with hidden files off when the next entries are dot-files; check where focus lands and what the preview shows.
- Press F5 during a `100000` load, then after a sort change, each with 20 entries selected across the viewport.
- With hidden files off, put the cursor on the last entry and delete the last three from a shell; dot-files precede them. Then F5.
- In Columns, open a folder's child column, delete the folder's next sibling from a shell, and press F5 on the parent column.

### browser/selection/click-modes

- Set Single for folders in Columns only; double-click a folder in Icons and List and single-click one in Columns; nothing may open twice.
- Two clicks on a file spanning the double-click interval with single-click previews on, then off.
- Change the file click count from a second window's Settings while a folder is open in the first; click without restarting.
- Leave a folder in Icons with three entries selected, then click and Enter its sidebar place; repeat in Columns and after 130 other folders.

### browser/selection/keyboard-navigation

- Hold Down for two seconds in `100000`; when it stops, focus, selection, scroll position, and preview must name the same entry.
- Size the window so the last Icons row holds one tile; press Down from the row above, then Right and Left at both edges.
- With Type to search off press `h` in the sidebar, the pane header, and the location entry; then toggle Keep arrows with Ctrl+\ while the header has focus and press Down.
- In Columns with column 3 active, hover column 1 and Tab in from the header. Then Shift+Tab out with a filter open in column 2, and with none.
- Tab and Shift+Tab around a listing with the preview panel open, closed, and showing a video; then from the unreadable folder's Retry button.
- Start a rename in Columns and press Shift+Tab; then Tab out of a rename whose name collides with a sibling.

### browser/selection/marquee

- Start a marquee from the List heading strip, a Columns header, and preview space at text sizes 13 and 28; the band must stay inside the pane.
- Hold a marquee near the bottom edge of `100000` for ten seconds, then drag back above the anchor; compare the count with the rows crossed.
- Marquee while a rename editor is open, while a context menu is open, and while the folder is still loading.
- Alt-drag from an entry inside a multi-selection, and Ctrl-marquee across a Shift range, releasing outside the window.

### browser/selection/pointer-intent

- Press on a filename, move 3 px, return, and release; repeat moving past the threshold and returning.
- In List, press in the Size and Modified cells of a selected row and an unselected row and drag; note which starts a drag and which a marquee.
- Wheel-scroll during a held press until the row recycles, then release over a different row.

### browser/view-modes

- Cycle Ctrl+1, Ctrl+2, Ctrl+3 while `100000` is loading; the skeleton must never outlive the load or take a click.
- Switch with 500 entries Shift-selected, then with a filter open; compare the selection count and query after each switch.
- Write `browser_mode = "grid"`, then `"explorer"`, then `"tiles"` in settings.toml; start and note the view and the Appearance icon.
- Focus the last row of a folder and delete every entry externally; then add one back. Repeat in the unreadable folder after `chmod 755` and F5.
- Press F5 in `100000` with the cursor on entry 5000, then in a folder that loads within 150 ms. Watch where focus sits during and after.
- Repeat that F5 with focus on the sidebar, the location entry, a filter result, Properties, and the Ctrl+F field holding a query.
- Press F5 in `100000` with the Ctrl+F field focused and type three characters during the reload; repeat pressing Escape, then Tab, mid-reload.
- Leave 130 folders in List, return to the first with Back; then return to a folder that was renamed externally and to one with a filter open. Repeat in Icons.
- Leave a folder, empty it externally, and return with Back, then with Alt+Up from a child that was deleted.
- Leave a folder in Icons scrolled halfway, widen the window by 1 px, then 100 px, and press Alt+Left each time; then leave in Icons and return in List.
- Press Back in `100000` and, before the restore settles, press Down, wheel-scroll, press Ctrl+2, or re-sort by Size.
- Press Alt+Left with the location entry open, with Properties open, and with a filter result focused; then click a breadcrumb with the sidebar focused.
- Let an auto-refresh tick land in a background tab and while a rename is open in the active tab; switch tabs afterwards.

### browser/view-modes/columns

- Open `deep` to 20 columns, click a title eight columns back, press Escape twice, then Backspace; count the columns after each step.
- Hold Down across a folder, a PDF, and a plain file with single-click previews on; time the child column against 75 ms.
- Drag a column edge below 300 px, autofit a column holding the 255-byte name, restart, and read `browser_column_width`.
- Open a context menu in column 2, move the pointer to column 4, press Escape; check which header shows its actions.
- With Mirror columns selection off, then on, press Home on a folder, End on a PDF, and Shift+Home. Then press keypad End with Num Lock on and off.
- Click a row in column 1, then press Ctrl+Down in column 2 without moving the pointer; then press End while Properties opens.
- Open `deep` to column 8, press Alt+Left, Alt+Right, Alt+Up, and click the third crumb; then dot-rename the came-from folder from a shell and press Back.
- Return to an ancestor with a pending FileManager1 reveal in it, and while the ancestor fails to load after `chmod 000`.

### browser/view-modes/icons

- Set the slider to 32 then 256 px in `100000`, scroll fast and stop; count tiles with missing details after two seconds.
- Resize the sidebar and preview panel while details stream in; open the same folder in a second window and move one slider.
- Rest on a truncated card and drift 4 px, then 5 px; rest on the thumbnail frame's margin, the details text, and the blank caption beside a short name.
- Rest on a name at the two-line boundary at 32 px and 256 px thumbnails, then at text size 28; then Tab to the card and wait.
- Click a truncated card and hold still; then wheel-scroll the grid with the pointer resting on a card.

### browser/view-modes/list

- Shrink Name to its minimum, then double-click each heading edge with the 255-byte name and a `drwxrwxrwx  777` row visible.
- Group by file type with hidden files on, sort by Type descending, toggle Folders first; read the group order top to bottom.

### browser/view-modes/sorting

- Sort `a1`, `A1`, `a01`, `a10`, `a2`, `é`, `E`, and the non-UTF-8 name by Name in both directions; then by Modified with two files sharing an mtime.
- Choose Size in `100000` while it loads; watch the pane state until the rows settle.
- Set a sort in column 3, then open a new column from column 1; compare the sort in every column and after a restart.
- Open SORT BY in Recent and in a Camera Photos library and read each option's role and checked state; then change the sort from a second pane.

### browser/view-modes/text-size

- Ctrl+wheel with a smooth touchpad from 13 to 48 and back; the step count must match the accumulated delta.
- Press Ctrl++ with the location entry open, with Ctrl+K open, and in Settings; then set `text_size = 7`, `"huge"`, and `49` and start.

### browser/navigation

- Visit ten folders, press button 8 ten times fast, then button 9 ten times; the breadcrumb must match at each step, including over the sidebar.
- Press Alt+Up at `/`, at `trash:///`, and in a folder whose parent was deleted externally; then Backspace in the root column at `/`.

### browser/navigation/folder-jump

- Visit 120 folders in `deep` and open the palette; count the rows, then query `'level-0 !marker`, `^level`, `000$`, and the non-UTF-8 name.
- Visit a folder, delete it externally, open the palette, and choose it; then press Ctrl+Shift+K, Ctrl+K, Ctrl+Shift+K without closing.
- Open the palette from the sidebar, the location entry, and a rename editor, then press Escape; note where focus lands each time.

### browser/navigation/location-bar

- Type `~/`, `./`, `../`, `  ~/Documents  `, `~root`, `file:///etc`, `trash:///`, and `gopher://x` and record each result.
- Tab-complete in `1000` with hidden files off, then on; click a crumb while the popover is open, and press Escape on a highlighted suggestion.
- Type the path of a file in the open folder, of a dot-file, of a file inside the unreadable folder, and of the non-UTF-8 name.
- Open a 200-level `deep` folder; scroll the overflowing crumbs with the wheel and open the hierarchy menu from the last crumb.
- Type `smb://host/my share`, `smb://alice:pw@host/café`, and `sftp://host/a%2Fb` while the share is unmounted. Read the entry during the mount and the crumbs after.
- Type `sftp://host/share/caf%E9` and `smb://host/share/x%2Fy` for existing remote names, then create and delete an entry in each opened folder.
- In `deep` at level 30, choose level 3 from the hierarchy menu, then from the scrolled crumbs, in each view; then choose the current crumb.

### browser/navigation/recent

- Run `gio open` on five files, delete two externally, and open Recent in two windows; trash a third from one and watch the other.
- Press Ctrl+V, Ctrl+Shift+N, and Remove from Recent on a selection mixing a file and a folder row.
- `gio open` the non-UTF-8 name, open Recent, then rename, Remove from Recent, and Properties on its row.

### browser/navigation/startup-arguments

- Launch with a folder, a file, the broken symlink, and the non-UTF-8 name in one command, then again while the first instance is open; count the windows.
- Launch with the unreadable folder, press Retry after `chmod 755`; then with `sftp://unreachable.invalid/f.txt`, navigate away before Cancel.

### browser/search

- Type and delete a 20-character query rapidly in `100000`; the highlighted row must stay on the same path throughout.
- Search `résumé` typed in NFD, `.cargo`, `level-255`, `/`, and a query ending in a space; then add a `.gitignore` excluding a folder and reopen.
- Press Alt+Enter on a result while a Trash view is open, then while a filter is open; press Ctrl+K with the location entry and a rename editor open.
- Open Ctrl+K from the sidebar, the filter field, and an empty folder, close it by a click outside the panel, and press Down.
- With Ctrl+K open on a query, `touch` a file in a watched Home subfolder every 100 ms for 10 s; type meanwhile and watch the highlight.
- With a filter open in one window, `mv` its folder from a shell, then `mv` a parent of it; read the results and the breadcrumb in each window.

### browser/search/exclusions

- Add `Target`, `~/dev/`, `/tmp/x/../y`, `~user/x`, and an empty string; read each message, then add `target` again.
- Add a rule with Ctrl+K open, remove it, and search before reopening; then edit an invalid rule into settings.toml while Settings is open.

### browser/search/filter

- Type `*`, `entry-0999*`, `trahs`, `?`, and `[a]` in `100000`; count the results and read the status text each time.
- Open a filter in column 2, press Ctrl+1, Ctrl+2, Ctrl+3, click column 1's background, then Ctrl+F in column 4.
- With Include subfolders off in one window and on in another, toggle it while a search is running in each.
- Rename a result to a non-matching name, undo, then delete a result externally; press Space on a folder result and Up past the first result.
- Select several results at `trash:///`, `recent:///`, and an `sftp://` share, then press Escape on one of them.
- Type a query, focus a result, open Appearance, and switch view twice without closing the menu. Then switch from the menu with an empty, open filter.
- Press Ctrl+F at once on opening `100000` in each view and type. Press Ctrl+A and Backspace before and after the load ends; repeat with 10xer `f`.
- With a filter in Columns column 3, create matches in column 1's folder, `target/`, a dot-folder with hidden files off then on, and three levels down.
- Create 500 matching files at once during a `100000` walk, then delete the focused hit; repeat with Include subfolders off.
- Delete the cursor entry from a shell while a 2,000-file copy into the folder runs, with the filter field focused, then a result.

### browser/sidebar

- Drop a row on another row's exact midline, then between the PINNED heading and its first pin; restart and compare the order in a second window.
- Turn off every place chip; collapse with Ctrl+B in one window while the other's sidebar has focus, then press Ctrl+Shift+B there.
- Unset `XDG_MUSIC_DIR` and point Documents at a missing folder in `user-dirs.dirs`; shrink the window to the icon rail and Tab through it.

### browser/sidebar/pins

- Edit the bookmarks file externally with a CRLF line, a duplicate, a `file:///home/<user>` line, and `smb://u:p@h/s`; pin a folder and diff the file.
- Pin a folder, `chmod 444` the bookmarks file, unpin; then pin a folder on `/dev/shm`, trash it from the other window, and press Ctrl+Z.
- With Type to search off press `p` on a file, a pinned folder, a standard folder, and a folder inside Trash.
- Make the bookmarks file a chain of 8, then 9 links, a root-owned target, a dangling link, and a relative link. Pin, then read `ls -l`.

### browser/thumbnails

- Scroll the slow directory to the end and back twice; look for icons left on decoded rows and thumbnails on the `.svgz` and `.ogg` files.
- Rename an image while its decode runs, then overwrite an image's bytes keeping its mtime with `touch -r`.
- Remove the HEIC or JPEG XL decoder package and reopen the folder; open an `smb://` share with `gvfsd-fuse` stopped.

### browser/thumbnails/cache

- Plant entries that are a symlink, a 3 MiB PNG, a 600 px PNG, and a JPEG renamed `.png`, each with matching tags; reopen the folder.
- Delete `thumbnails/large`, make it a `chmod 755` directory, reopen, and read its mode; then point `XDG_CACHE_HOME` at an unwritable path.

### browser/thumbnails/workers

- Set workers to 1 in the slow directory, then 16 mid-load, and count sandbox processes with `pgrep`; kill one with SIGKILL during a scroll.
- Set `STRATA_THUMBNAIL_WORKERS=99`, then `abc`, and `STRATA_THUMBNAIL_IDLE_SECONDS=1`; read the reset value and watch process exit.

### browser/properties

- Open Properties on a file you cannot chmod, on the broken symlink, and on the 255-byte name; toggle a permission bit and press Escape before it applies.
- Press Alt+Enter with nothing selected, with the sidebar focused, and in Recent; set each date format and reread MODIFIED.
- Copy path for a name holding `'` and a space, and for a file in `trash:///`; paste each in a shell.
- With an AT-SPI inspector, toggle a bit on a file you cannot chmod and read its pressed state before and after the error; then open the broken symlink.

### browser/properties/media

- Open Properties on a 0-byte `.mp4`, a WAV renamed `.png`, a rotated phone video, and an MP3 with cover art.
- Close the dialog within 100 ms of opening it on a long video; reopen after rewriting the file externally.

### browser/properties/raw-metadata

- Open a `.dng` with no EXIF, an `.ARW` truncated to 1 KiB, a JPEG renamed `.NEF`, and a RAW on an `sftp://` share.
- Hold Down through five RAW files with the preview panel open; the rows must not reorder or disappear.

### browser/properties/size

- Open Properties on `100000` and on `deep`; watch the counter cadence and read the nesting warning text.
- Select 300 items including the unreadable folder and the symlink to a folder; compare with `du -sb`, close mid-count, and reopen at once.

### browser/context-menu

- Open the menu on a file, folder, archive, symlink, Trash item, Recent row, and empty space in each view; diff the action lists.
- Right-click the last row of `100000` scrolled to the end at text size 28; then open a menu and press F5, Ctrl+2, and resize the window.
- Press Menu with the filter field focused, the location entry focused, and a drive row focused; right-click a second entry while a menu is open.

### browser/directory-monitoring

- Run `touch f{1..5000}` then `rm f*` in the open folder; count the rows afterwards and look for duplicates and lost selection.
- `mv` the open folder in Columns with three descendants open, then `rm -rf` it; repeat in Icons and List.
- Set `auto_refresh_interval = 4294967295`, then `-1`, then `"60"`; start, change another setting, and read the file back.
- Set 1 min and start a rename ten seconds before the tick.

### browser/folder-customization

- Customize a folder, rename it externally, and create a new folder at the old name; then pick a custom color and press Escape at each step, reading settings.toml.
- Write `emoji:` with a 70-byte string and an unknown icon name into `[custom_icons]`; start, then switch theme with the folder visible in two windows.
- Close the custom color dialog by a click outside it, then Customize the same way. Delete the item externally while Customize is open and press Escape.

### browser/scrolling

- Middle-click in `100000`, move 10 px, 50 px, and 300 px; press Escape with a 10xer chord armed, then click a folder row.
- Page Down through Icons with the preview panel open, close it, Page Up; then Ctrl+Down with hidden files off where the last ten entries are dot-files.
- Open Sort by, then wheel over the sidebar, the header, and the second window's listing; middle-click a filter field holding a primary selection.
- Press Home and End with hidden files off where the first and last entries are dot-files. Repeat in filter results and right after a folder opens.

### browser/tabs

- Open 12 tabs, hold Ctrl+Shift and press 0, drag tab 12 to position 1, press Ctrl+Shift+1; read which tab each step selects.
- Press Ctrl+W with Properties open, then close every tab from the last one; change Show hidden files with three tabs on one folder and switch through them.
- Open tabs on `trash:///`, `/`, and a 30-character folder name; press a Columns folder, drag 5 px, release, and read the tab name during and after.
- Focus an empty folder's pane in tab 2, fill the folder from a shell, then switch away and back.

### browser/tabs/session-restore

- Save tabs on `sftp://host/x`, `smb://user@host/share`, `trash:///`, a folder deleted before relaunch, and the `chmod 000` folder; relaunch and read `tabs.toml` before and after.
- Run plain `strata` while a window is already open; count tabs in the new window, then change tabs in each window and quit both.
- Hand-edit `tabs.toml` with 40 entries, an unknown `kind`, and duplicate entries; relaunch after each.
- Open a tab on the non-UTF-8 folder beside two other tabs, select it, quit, and relaunch.
- Replace `tabs.toml` with a symlink to another file and with a directory, then change a tab; make `$XDG_CONFIG_HOME/strata` read-only.
- Turn Restore open tabs off in one window's Settings while a second window changes tabs, then on again, and quit.
- Close tabs down to one, then close the window, and relaunch plainly.
- Open a window through a FileManager1 `ShowItems` call, add tabs there, quit, and relaunch plainly.

## Hand-offs

- Drag and drop once a press is read as a file drag, drops on tabs and sidebar rows, and every file operation → `operations`.
- DEVICES rows, Set label…, mounting, and ejecting → `devices`.
- Remote shares beyond the typed URI rejections and credential masking covered here → `remote`.
- Modal dialog shell, the shortcut footer, F1, and key precedence → `app`.
- What the preview panel and quick preview render → `preview`.
- The Settings pages that hold the preferences named in these probes → `settings`.
- 10xer-mode key variants and the portal file chooser → `integration`.
