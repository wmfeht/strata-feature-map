---
title: Browser sweep
reviewed_at: 41070b59c09f21eba33918c1e99be2eb3047de7e
triggers: [src/ui/browser.rs, src/ui/browser/events.rs, src/ui/browser/preferences.rs, src/ui/entry_list_model.rs, src/app/browser.rs, src/app/browser/tests.rs, src/app/navigation.rs, src/app/navigation/tests.rs, src/app/browser/tests/events.rs, src/app/browser/tests/reveal.rs, src/ui/entry_list_model/tests.rs]
tools: [scripts/generate-fixture.sh, docs/keyboard-navigation.md, docs/keyboard-shortcuts.md, docs/keymap.md, docs/preferences.md, tests/qa/mutations, tests/qa/keyboard.rs, tests/fixtures/harness.json, tests/qa/fixtures/file_drag_source.py, docs/testing.md, scripts/qa-mutation.sh]
---

## Scope

Everything that shows a folder and moves through it without changing files, in browser windows and in the portal file chooser's shared views. That covers selection by pointer and keyboard, with marquee, pointer intent, and click modes. It covers the Columns, Icons, and List views with sorting, per-folder views, Frame and Content density, text size, thumbnail size shortcuts, and position restore. It covers Back, Forward, and Parent history, the location bar, Recent, startup arguments, folder jump, and opening unreadable folders as administrator. Ctrl+K search, the Ctrl+F filter, and search exclusions belong here too. The sidebar places, the sidebar toggle with its icon rail, pins with drag-to-pin, the Connect to server dialog, and the update notice belong here. So do thumbnails with their disk cache and worker pool, and Properties with its media, RAW, and size details. The context menus, directory loading and monitoring, folder customization, scrolling, and tabs with their session restore complete it. Arrow focus between controls in modal dialogs belongs here too.

Tab-strip drops that open or move tabs belong here. Left to other sweeps: file drags once a press becomes one, except Escape cancellation, file transfers dropped on tabs and sidebar row bodies, and every operation that changes files. The DEVICES rows and remote shares in the sidebar go elsewhere too. So do the modal dialog shell, the shortcut footer, F1, and key precedence. What the preview panel renders, the Settings pages for these preferences, 10xer key variants, and the portal file chooser's own setup and dialogs are also left out.

## Setup

- `scripts/generate-fixture.sh <root>` builds `1000`, `10000`, and `100000` entry folders, a 256-level `deep` tree, and `edge-cases` with a broken symlink and a non-UTF-8 name. Add dot-files, a `.hidden` file naming one visible entry, a 255-byte name, two names differing only by case, and a symlink to a folder.
- Two oversized folders built with `touch`: one of 200,000 entries and one of 260,000.
- An unreadable folder (`chmod 000`) inside the fixture, and a folder to remove while it is open (`rm -rf` or `mv` from a shell), in every view.
- For administrator-access probes: a root-owned `0700` folder on a USB drive, GVfs with `gvfsd-admin`, and a polkit agent in the session. The QA container has no GVfs or polkit agent, so these probes run by hand.
- A slow directory: 2,000 images across every thumbnail format, plus 50 PDFs and 50 videos, with `$XDG_CACHE_HOME/thumbnails` emptied first so decoding is visible.
- Two windows of the same build for sidebar, pins, text size, tabs, monitoring, and Recent checks; open the same folder in both where the probe says so.
- Type to search on and off per probe: it changes what `h`, `j`, `k`, `l`, `p`, `/`, and plain letters do. `docs/keyboard-navigation.md` holds the key rules and `docs/preferences.md` the setting keys.
- Hand-written preferences go in `$XDG_CONFIG_HOME/strata/settings.toml` before launch; read the file back after every probe that saves something.
- Rebinding probes put overrides under `[keymap.default]` and `[keymap.tenxer]` in that file before launch; `docs/keymap.md` lists the command ids.
- Keyboard layouts set with `setxkbmap` for layout probes: `us,ru`, `ru`, `fr`, `de`, `ch` (Swiss German), `cz`, `is`, and `us` with variant `dvorak`. `docs/keyboard-shortcuts.md` holds the matching rules. The QA scenarios cover only the `us`, `ru`, `ru-only`, `fr`, and `de` layouts and the `caps-lock` and `cn-altgr-pinyin` layout entries in `tests/fixtures/harness.json`. So `ch`, `cz`, `is`, and `dvorak` are manual only. `docs/testing.md` "Keyboard layouts" explains the switch.
- fcitx5 with pinyin under `GTK_IM_MODULE=fcitx` on X11 for input-method probes.
- Foreign drags for pin probes: Nautilus or Dolphin, and `tests/qa/fixtures/file_drag_source.py`, which offers chosen locations with chosen actions.
- An SMB share and an SFTP server for Connect to server probes, with one share requiring a password, plus a host name that does not resolve.
- Raw H.264 samples: `ffmpeg -f lavfi -i testsrc2=size=320x180:rate=24:duration=3 -c:v libx264 -pix_fmt yuv420p -an alpha.h264`. Copy it as `.H264`, `.264`, `clip.h264.txt`, and with no extension; encode an HEVC stream as `.h265` and `.hevc`. Put plain text in `notes.h264` and leave an empty `empty.h264`.
- RAW samples: a lossless compressed Fuji `.RAF`, a portrait Pentax `.DNG`, and a GoPro `.GPR`. Toggle `dcraw` and `simple_dcraw` on the sandbox `PATH` per probe.
- Ubuntu 24.04 with GTK 4.14 for context menu teardown probes.
- GNOME Shell, KDE Plasma, and Hyprland Wayland sessions and an X11 session, plus two monitors of different heights, for context menu placement probes.
- Update-notice probes reuse the app sweep's prerelease build and update proxy to make a check find an offer.
- An AT-SPI inspector such as Accerciser, or Orca, for probes that read roles, names, and checked or pressed states.
- Tab session probes need a disposable `$XDG_CONFIG_HOME`; read `strata/tabs.toml` back after each quit and before each launch.
- Network mounts for change-check and stalled-mount probes: NFSv3 and NFSv4.2 exports, a `cifs` SMB share, an `sshfs` mount, and a 9p or virtiofs share. Each must be writable from the server. Stall a mount by stopping its server or sending SIGSTOP to the FUSE daemon. `powerprofilesctl` switches power-saver mode.
- Per-folder view probes need a disposable `$XDG_STATE_HOME`; read `strata/folder-views.toml` back after each probe. Add a USB drive with an ext4 partition, a kernel exFAT partition, and an NTFS partition mounted with ntfs-3g (`fuseblk`), and an `sshfs` mount.
- `tests/qa/mutations/` holds the `click-modes`, `click-mode-preference`, `shift-click-range`, `filter-results`, `keyboard-navigation`, `location-entry`, `popover-scrolling`, and `view-switching` patches; `./scripts/qa-mutation.sh <name>` is evidence when those areas changed.

## Probes

- Run each probe in Columns, Icons, and List; a difference between views is a finding unless the node names it.
- After each probe read the three signals apart: selection, keyboard cursor, and open-path marker; the preview must follow the cursor.

### browser/selection

- Shift+click across 500 entries in `100000`, Ctrl+click five of them out, scroll to the end, then press Shift+Up; count the selection.
- Press Escape with a rename editor open in one column and a multi-selection in another, then again; note what each press clears.
- Delete the focused entry externally with hidden files off when the next entries are dot-files; check where focus lands and what the preview shows.
- Press F5 during a `100000` load, then after a sort change, each with 20 entries selected across the viewport.
- On an `sftp://` share with hidden files off, put the cursor on the last entry and delete the last three server-side; dot-files precede them. Then F5.
- On an `sftp://` share in Columns, open the cursor folder's child column, delete that folder server-side, and press F5.
- In List and Icons, group by type and sort by size descending. Click an entry, Ctrl+click one in another group, then press Shift+arrow toward each neighbour.
- Ctrl+click a selected entry to remove it, then press Shift+arrow; repeat after Ctrl+click on blank row space.
- Middle-click a folder row while a rename editor is open, on a symlink to a folder, and on a Ctrl+F result in another folder. Repeat with Ctrl held, with Ctrl+Shift held, and in the file chooser.

### browser/selection/click-modes

- Set Single for folders in Columns only; double-click a folder in Icons and List and single-click one in Columns; nothing may open twice.
- Two clicks on a file spanning the double-click interval with single-click previews on, then off.
- Change the file click count from a second window's Settings while a folder is open in the first; click without restarting.

### browser/selection/keyboard-navigation

- Hold Down for two seconds in `100000`; when it stops, focus, selection, scroll position, and preview must name the same entry.
- Size the window so the last Icons row holds one tile; press Down from the row above, then Right and Left at both edges.
- With Type to search off press `h` in the sidebar, the pane header, and the location entry; then toggle Keep arrows with Ctrl+\ while the header has focus and press Down.
- In Columns with column 3 active, hover column 1 and Tab in from the header. Then Shift+Tab out with a filter open in column 2, and with none.
- Tab and Shift+Tab around a listing with the preview panel open, closed, and showing a video; then from the unreadable folder's Retry button.
- In Columns, Tab and Shift+Tab across a locked folder's error buttons with and without GVfs `admin` support; press Enter on each.
- Start a rename in Columns and press Shift+Tab; then Tab out of a rename whose name collides with a sibling.
- In Settings → Actions → New action, press Up from the bottom control of each tab's page until focus stops, then Down; repeat after switching tabs with Left and Right from the strip.
- Open a second tab on `100000` and switch back to the first while it loads; press arrows as the hidden load finishes. Then open Properties while the visible Columns folder reloads after an external change.
- Press Down in each view under a light and a dark theme, then move the pointer without clicking and press Down again; note when each focus outline shows and hides.

### browser/selection/marquee

- Start a marquee from the List heading strip, a Columns header, and preview space at text sizes 13 and 28; the band must stay inside the pane.
- Hold a marquee near the bottom edge of `100000` for ten seconds, then drag back above the anchor; compare the count with the rows crossed.
- Marquee while a rename editor is open, while a context menu is open, and while the folder is still loading.
- Alt-drag from an entry inside a multi-selection, and Ctrl-marquee across a Shift range, releasing outside the window.
- Press Ctrl+A in `100000`, then draw a small Ctrl+Alt marquee in Icons and List; compare the footer count with the rows crossed.
- Plain-click blank preview space while a PDF shows, while the placeholder shows, and while the drawer slides in; then drag from there into the listing.
- Click a disabled header button and the gap between the preview header's icon and name. Repeat in the file chooser.
- In the file chooser, Ctrl+click blank preview space with a file previewed, then plain-click the empty Columns preview slot. Repeat for a `single` and a `multiple` request.

### browser/selection/pointer-intent

- Press on a filename, move 3 px, return, and release; repeat moving past the threshold and returning.
- In List, press in the Size and Modified cells of a selected row and an unselected row and drag; note which starts a drag and which a marquee.
- Repeat the List press-and-drag probes with Name moved to the last column and with Size and Type hidden.
- Wheel-scroll during a held press until the row recycles, then release over a different row.

### browser/view-modes

- Cycle Ctrl+1, Ctrl+2, Ctrl+3 while `100000` is loading; then click where the skeleton shows.
- Switch with 500 entries Shift-selected, then with a filter open; compare the selection count and query after each switch.
- Write `browser_mode = "grid"`, then `"explorer"`, then `"tiles"` in settings.toml; start and note the view and the Appearance icon.
- Focus the last row of a folder and delete every entry externally; then add one back. Repeat in the unreadable folder after `chmod 755` and F5.
- With the Appearance menu closed, press Ctrl+2 or switch the mode in a second window. Then open Appearance and read each option's checked state.
- Press Ctrl+1, Ctrl+2, and Ctrl+3 with Russian active beside US, with only Russian configured, on Dvorak, and with Caps Lock on; then with keypad digits and Num Lock on.
- Scroll List and Icons with cut files in view under a 25% CPU quota, and again after the window sat idle for 10 s; stop on cut rows and watch when their styling and dates settle.
- In List and Icons, cancel a Shift+Delete dialog from a filter hit with several hits selected, then change the selection from a second window while results show.
- At Content 0 and 16, drag a marquee in List and Icons and resize the window across the Icons column caps.
- Stall an sshfs mount with three of its columns and one local column open. Wait 10 s, switch views, and resume the daemon; repeat over an error page and a first load.
- In List at the bottom of `1000`, rename a new file to sort first, then press Down right after Enter in one scripted sequence. Repeat in Icons.
- In Columns, Icons, and List, click a filtered file while a result batch is arriving. Then Ctrl+click it and plain-click it again.
- Repeat those clicks on a non-previewable file, at a filtered `trash:///`, and with Include subfolders off.
- In the file chooser, filter to a file and double-click it in Columns and in Icons and List search results; then press Enter.
- With two tabs open, press Ctrl+3 then Down within one frame while `100000` loads in the visible tab; repeat right after a rename commits. Note which row holds focus after 500 ms.
- In List and Icons, `chmod 000` the open folder from a shell and press F5; click Open as Administrator and cancel the prompt. Then open an admin folder and switch views at 400 px wide.

### browser/view-modes/columns

- Open `deep` to 20 columns, click a title eight columns back, press Escape twice, then Backspace; count the columns after each step.
- Hold Down across a folder, a PDF, and a plain file with single-click previews on; time the child column against 75 ms.
- Press Return on a folder on a stalled network mount, then on one the open turns away (`chmod 000`), with Mirror columns selection on; press Down before the open lands.
- Drag a column edge below 300 px, autofit a column holding the 255-byte name, restart, and read `browser_column_width`.
- Open a context menu in column 2, move the pointer to column 4, press Escape; check which header shows its actions.
- With Mirror columns selection off, then on, press Home on a folder, End on a PDF, and Shift+Home. Then press keypad End with Num Lock on and off.
- Click a row in column 1, then press Ctrl+Down in column 2 without moving the pointer; then press End while Properties opens.
- Open `deep` to column 8, press Alt+Left, Alt+Right, Alt+Up, and click the third crumb; then dot-rename the came-from folder from a shell and press Back.
- Return to an ancestor with a pending FileManager1 reveal in it, and while the ancestor fails to load after `chmod 000`.
- Autofit the 255-byte name with the sidebar railed, then expanded, and with the preview open. Drag an edge past the window edge, then press Escape mid-drag.
- Set `browser_column_width = 5000` with text size 28, launch, then return to 13; shrink the window to 400 px and drag an edge.
- Double-click a closed folder in a clipped parent while the strip scrolls under the first press; repeat holding Ctrl on the second press.
- Close a column and click the next one within 220 ms; drop a file on a closing column; switch to Icons mid-close.
- Ctrl-select three folders and plain-click one, moving 3 px before release; repeat in a filtered column and with double-click folders.
- Trash the focused open folder with Delete, Mirror columns selection off then on, where the next entry is a file, a dot-folder, or nothing.
- Start a rename, `touch` a file in that folder from a shell, then press F2, Menu, and Shift+F10 on the row.
- Toggle Show sizes in Columns view from Appearance with Settings open in a second window and a recursive search column open.
- With one entry selected, create 4,200 files in the active column's folder from a shell, then press Down and the 10xer next-entry key.
- With the badge on, hover a folder of only dot-files with hidden files off, the unreadable folder, `100000`, and an `sftp://` folder.
- Hover and select the 255-byte name in a light and a dark theme, and on an open-path folder row.
- Scroll the strip so a parent column is clipped, then press 5 px and 1 px left of its edge and 4 px right of it and drag; repeat after arrow keys moved the strip.
- With badges on, rest the pointer on an unselected row and hold Down through it; then move the pointer 1 px. Hover a row and leave it within 120 ms.
- Wheel-scroll a column with the pointer over it and badges on; then kinetic-scroll the strip so a parent is clipped, stop, and compare its reveal button with its visible width.
- With recursive filter results in a column, cancel a dialog opened from a hit, switch views, and hide the preview with the mouse; note which hit has focus each time.
- In Columns, press a recursive file hit with previews on, drag past the threshold, and release; then slow-click a selected hit.

### browser/view-modes/icons

- Set the slider to 32 then 256 px in `100000`, scroll fast and stop; count tiles with missing details after two seconds.
- Resize the sidebar and preview panel while details stream in; open the same folder in a second window and move one slider.
- Rest on a truncated card and drift 4 px, then 5 px. Rest on the thumbnail frame's margin, the details text, and blank space beside a short details line.
- Rest on a name at the two-line boundary at 32 px and 256 px thumbnails, then at text size 28. Then Tab to the card and wait.
- Wheel-scroll the grid with the pointer resting on a card.
- Move the slider in Trash, Recent, and an `sftp://` folder; leave and return, then switch to Columns and back.

### browser/view-modes/list

- Shrink Name to its minimum, then double-click each heading edge with the 255-byte name and a `drwxrwxrwx  777` row visible.
- Group by file type with hidden files on, sort by Type descending, toggle Folders first; read the group order top to bottom.
- Read the Size cell of a folder holding only dot-files, the unreadable folder, `100000`, and an `sftp://` folder; then sort by Size.
- Group by file type in List and open the 200,000-entry folder; mid-load, change the sort key, flip its direction, and toggle Folders first. Compare the headings with a reload.

### browser/view-modes/list/column-layout

- Hide the sort column with Remember per folder off, then with Group by file type on; hide it in the file chooser while a browser window sorts by it.
- Drag Name to the last position, then press within 8 px of each heading's right edge and drag; then drag a heading 9 px and 11 px and release.
- Drag a heading past two neighbours in one motion and release, then repeat and press Escape mid-drag; read `list_column_order` and the insertion line after each.
- Drag a heading out of the heading row and back in before releasing, then drag it with Size and Type hidden. Repeat in the portal file chooser while a browser window shows List.
- Drag Modified to the end with the List pane scrolled horizontally, and drag a heading while a folder of `100000` loads.
- Press Escape mid-drag with the Columns popover open, with a filter result focused, and with a rename field open; then drag the same heading again and release.
- Write `list_hidden_columns = ["name", "size", "size", "bogus"]` and `list_column_order = ["type", "type"]` in settings.toml and start.
- Hide Mode in one window while a second shows Icons and the portal file chooser shows List; return the second window to List.
- Hide every column but Name, shrink the window to 400 px, and reset; then repeat at text size 8 and 48 with 10xer mode on and off.
- Open the Columns popover from the header, the heading row's right-click, and Appearance in Recent, Trash, and a Camera Photos library; navigate it by keyboard and read it with Orca.

### browser/view-modes/sorting

- Sort `a1`, `A1`, `a01`, `a10`, `a2`, `é`, `E`, and the non-UTF-8 name by Name in both directions; then by Modified with two files sharing an mtime.
- Choose Size in `100000` while it loads; watch the pane state until the rows settle.
- Set a sort in column 3, then open a new column from column 1; compare the sort in every column and after a restart.
- Open SORT BY in Recent and in a Camera Photos library and read each option's role and checked state. Then change the sort from a second pane.
- Turn per-folder views off, sort in column 3, open a new column from column 1, then turn per-folder views back on.
- Toggle Folders first in one window while another shows Recent, a filter, and a Camera Photos library.
- Sort a folder holding `.GPR`, `.ARQ`, `.ORI`, `.DNG`, and extensionless files by Type in List, in both directions.
- Sort by Type a folder holding the `.H264` copy, `clip.h264.txt`, the extensionless copy, and `notes.h264`, in both directions, under German and C locales.

### browser/view-modes/folder-views

- Sort a folder on the ext4 USB partition, eject it, and remount it elsewhere; repeat on the ntfs-3g partition and on the `sshfs` mount.
- Mount the drive from the sidebar and sort a folder on it before the listing settles.
- Write `version = 2`, then `icons_size = 900`, a duplicate `path`, and a relative `path` into `folder-views.toml`; launch, change a sort, and read the file.
- Replace `folder-views.toml` with a symlink, then make the state directory read-only; change a sort twice and count the notices.
- Change the sort of one folder in the portal chooser and the main window within 500 ms; quit both and read the file.
- With the switch off, change the default sort from the portal chooser and watch a main window that never opened Settings.
- Set a folder's sort, make another sort the default, then open the folder's sort menu and read which actions show.
- Change the default sort in the portal chooser while the main window saves text wrap; read both windows and `settings.toml`.
- Change the main window's default icon size, then change the chooser's default sort before the main window's save lands.
- Rename a sorted folder from a shell, then delete it and reopen its parent; repeat for a folder on the unmounted drive.
- Undo a Keep-both move of a sorted folder, then Put back a trashed one after Forget all folder settings.

### browser/view-modes/density

- Drag both sliders across their full range in Columns, Icons, and List, at text size 8 and 48. Watch for jumps at each preset and clipped headers or rows.
- Write `frame_density = "custom"` with `frame_density_custom_px = 200` and `browser_density = "bogus"`; start and read the sliders and the file after one change.
- In a separate run, write `browser_density = "compact"` with `browser_density_custom_px = 3`; start and read the Content slider.
- Set Frame 7 and Content 11, quit, and restart; then open a second window and the portal file chooser and compare their spacing.
- Open Appearance in two windows and drag a slider in one; then press a snap button in the other.
- With the menu scrolled, wheel over each slider; then focus one and press Page Up at the maximum and Page Down at 0.
- Read each slider and snap button with Orca while moving between presets and Custom values.
- In each interface language, open Appearance in Icons and List at text size 8 and 48, with each slider at a Custom value.

### browser/view-modes/text-size

- Press Ctrl++ with the location entry open, with Ctrl+K open, and in Settings; then set `text_size = 7`, `"huge"`, and `49` and start.
- On `ch`, `cz`, and `fr`, press Ctrl with each top-row key that types `+`, `=`, or `-`, with and without Shift; then keypad + with Num Lock off.
- With a PDF's pages focused, press Ctrl++ and Ctrl+−, then Ctrl+keypad 0 with Num Lock on and off.
- Press Ctrl++ at 48 and Ctrl+− at 8, then change the size from the Appearance buttons and from Settings while a size notice still shows.

### browser/view-modes/thumbnail-size

- Press Ctrl+Alt+keypad + and Ctrl+Alt+keypad −, then on `de` and `fr` Ctrl+Alt with the keys that type + and −.
- Drag the slider to 100 px and step up and down; drag it to 33 px and step down twice.
- Press Ctrl+Alt+0 in Trash, an `sftp://` folder, and a remembered local folder, with per-folder sizes on and off; read `folder-views.toml` and `settings.toml` after each.
- Step repeatedly at 32 and 256 px, and while a transfer notice shows; read the notice dock each time.
- In 10xer mode, press +, =, and − with Ctrl+F results in Icons, with the filter field focused, and with the sidebar focused.
- Step the size in the portal file chooser in Icons, then switch it to List and press the same keys.

### browser/view-modes/position-restore

- Press F5 in `100000` with the cursor on entry 5000, then in a folder that loads within 150 ms. Watch where focus sits during and after.
- Repeat that F5 with focus on the sidebar, the location entry, a filter result, Properties, and the Ctrl+F field holding a query.
- Press F5 in `100000` with the Ctrl+F field focused, then press Shift+Tab or click in the field mid-reload.
- Leave 130 folders in List, return to the first with Back; then return to a folder that was renamed externally and to one with a filter open. Repeat in Icons.
- Leave a folder, empty it externally, and return with Back, then with Alt+Up from a child that was deleted.
- Leave a folder in Icons scrolled halfway, widen the window by 1 px, then 100 px, and press Alt+Left each time. Then leave in Icons and return in List.
- Press Back in `100000` and, before the restore settles, press Down, wheel-scroll, press Ctrl+2, or re-sort by Size.
- Press Alt+Left with the location entry open, with Properties open, and with a filter result focused; then click a breadcrumb with the sidebar focused.
- Change an NFS folder from the server while it sits in a background tab, then switch to it with the cursor on entry 500. Press F5 with a rename open in Icons, then in List.
- Leave a folder in Icons with three entries selected, then click and Enter its sidebar place; repeat in Columns and after 130 other folders.
- With one entry selected in Icons and List, create 4,200 files in the open folder from a shell, then press Down and the 10xer next-entry key.

### browser/navigation

- Visit ten folders, press button 8 ten times fast, then button 9 ten times; the breadcrumb must match at each step, including over the sidebar.
- Press Alt+Up at `/`, at `trash:///`, and in a folder whose parent was deleted externally; then Backspace in the root column at `/`.
- Under `[keymap.default]`, bind `parent_folder` to `<Control>e`, `home_folder` to `<Super>h`, and `history_back` to `<Control><Shift>b`. Repeat under `[keymap.tenxer]` in 10xer mode. Press each with the file list, sidebar, location entry, and filter field focused.
- Bind `parent_folder` to a Ctrl key another command already holds, such as `<Control>r`, by hand in the file; press it in each view.

### browser/navigation/administrator-access

- With double-click folders, open the locked folder in each view, cancelling each prompt. Repeat on a folder whose metadata fill has not marked it yet.
- Lock folders named with spaces, `%`, and non-UTF-8 bytes; open each and read the location entry and breadcrumbs.
- Deny access only through an ACL (`setfacl -m u:$USER:---`) on a `0755` folder; lock another through a symlink to a root-owned folder.
- Open the locked folder from a sidebar pin, a bookmark, a command-line argument, and a FileManager1 reveal. Press Escape on each dialog, then retry with Open as Administrator.
- Type `ADMIN:///root`, `admin:///`, `admin:///missing`, and `admin://host/x` in the location bar.
- Run without a polkit agent, then with `gvfsd-admin` removed; open the locked folder and type `admin:///root`.
- Stay in an admin folder past the 5-minute polkit grant, then scroll, press F5, and switch views; note when a prompt appears.
- Press Alt+Up up to the Administrator crumb, then Back and Forward across the boundary between admin and ordinary folders.
- Open the same folder as administrator in two tabs and two windows, close them all, and read `gio mount -l`.

### browser/navigation/folder-jump

- Visit 120 folders in `deep` and open the palette; count the rows, then query `'level-0 !marker`, `^level`, `000$`, and the non-UTF-8 name.
- Visit a folder, delete it externally, open the palette, and choose it; then press Ctrl+Shift+K, Ctrl+K, Ctrl+Shift+K without closing.

### browser/navigation/location-bar

- Type `~/`, `./`, `../`, `  ~/Documents  `, `~root`, `file:///etc`, `trash:///`, and `gopher://x` and record each result.
- Click a crumb while the completion popover is open, and press Escape on a highlighted suggestion.
- Type the path of a file in the open folder, of a dot-file, of a file inside the unreadable folder, and of the non-UTF-8 name.
- Open a 200-level `deep` folder; scroll the overflowing crumbs with the wheel and open the hierarchy menu from the last crumb.
- Type `smb://host/my share`, `smb://alice:pw@host/café`, and `sftp://host/a%2Fb` while the share is unmounted. Read the entry during the mount and the crumbs after.
- Type `sftp://host/share/caf%E9` and `smb://host/share/x%2Fy` for existing remote names, then create and delete an entry in each opened folder.
- In `deep` at level 30, choose level 3 from the hierarchy menu, then from the scrolled crumbs, in each view; then choose the current crumb.
- Type `/tmp/./x/..`, `~/../..`, `/a/b/../../..`, `smb://host/share/../x`, a symlinked folder followed by `/..`, and a file path followed by `/..`; press Alt+Up after each.
- Open a new tab on a stalled sshfs mount and type a path before its first load ends.
- Click the path bar's copy button twice within 2 s, then switch tabs before 2 s pass; read its name every 500 ms.
- Dump a sign-in dialog's fields for an SMB share that asks for a domain and for an SFTP server.
- Type a file path, a folder path, a symlink to a file, and a symlink to a folder; repeat with the parent already open and with Quick Preview dismissed first.
- Type a path to a binary file with no previewer, an empty file, and a 2 GB file.
- Type a file path whose parent is an unmounted share or a stalled sshfs mount. Before it loads, press Back, click a sidebar place, or submit a second path. Then select the file by hand.
- Type a file path and press Back and Forward fast, five times, while the parent loads.
- Type a file path in the portal file chooser's location field.
- Open ten nested folders with 40-character names in a 600 px window. Open, submit, and cancel the entry there, then widen and narrow the window.

### browser/navigation/location-bar/completion

- Tab-complete in `1000` with hidden files off, then on; then type `.` and Tab again.
- Type `/usr`, `/usr/`, `~`, and a folder whose only sibling match is itself; compare each list with `ls`.
- Type a path into a stalled sshfs folder, press Tab, Down, and Enter before its list arrives, then resume the daemon.
- Hold Page Down through 50 suggestions, then Page Up past the first; note where the highlight wraps.
- Rebind `page_down` to `<Control>n`; press it, then Page Down, with suggestions showing and while a list is pending.

### browser/navigation/recent

- Run `gio open` on five files, delete two externally, and open Recent in two windows; trash a third from one and watch the other.
- Press Ctrl+V, Ctrl+Shift+N, and Remove from Recent on a selection mixing a file and a folder row.
- `gio open` the non-UTF-8 name, open Recent, then rename, Remove from Recent, and Properties on its row.
- Trash 65 files listed in Recent while Recent is open in a second window, then restore them with Ctrl+Z.

### browser/navigation/startup-arguments

- Launch with a folder, a file, the broken symlink, and the non-UTF-8 name in one command, then again while the first instance is open; count the windows.
- Launch with the unreadable folder, press Retry after `chmod 755`; then with `sftp://unreachable.invalid/f.txt`, navigate away before Cancel.
- Open a folder on a stopped sshfs mount with Open in New Tab, then with Open in New Window. Press Cancel in one and Retry in the other after resuming the daemon.

### browser/search

- Type and delete a 20-character query rapidly in `100000`; the highlighted row must stay on the same path throughout.
- Search `résumé` typed in NFD, `.cargo`, `level-255`, `/`, and a query ending in a space; then add a `.gitignore` excluding a folder and reopen.
- Press Alt+Enter on a result while a Trash view is open, then while a filter is open; press Ctrl+K with the location entry and a rename editor open.
- Open Ctrl+K from the sidebar, the filter field, and an empty folder, close it by a click outside the panel, and press Down.
- In Ctrl+K, press Down to the third result, type pinyin, pick a candidate with Space, then press Enter. Repeat with a dead key.
- With a Ctrl+K query open, `touch` a file in a watched Home subfolder every 100 ms for 10 s. Type meanwhile and watch the highlight.
- Filter a folder in one window while another shows its parent. `mv` the folder from a shell, then its parent; read results and breadcrumbs.
- Set both search limits to No limit and Ctrl+K over an `sshfs` or rclone mount under Home; then 10 s and 200,000 over two `100000` copies, and hover Partial results.
- Change a search limit while Ctrl+K is open, `touch` a file in a watched folder, then close and reopen it.
- In Ctrl+K, search three terms, a term with one typo such as `quartely txt`, and `配置 txt`.
- In Ctrl+K, separate two terms with a Tab, then a double space; then use a term found only in the searched root's own path.
- Open the Ctrl+Shift+K palette from the sidebar, the location entry, and a rename editor, then press Escape; note where focus lands each time.

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
- With a filter in Columns column 3, create matches in column 1's folder, `target/`, and three levels down. Repeat in a dot-folder with hidden files off, then on.
- Create 500 matching files at once during a `100000` walk, then delete the focused hit from a shell; repeat with Include subfolders off.
- Delete the cursor entry from a shell while a 2,000-file copy into the folder runs, with the filter field focused, then a result.
- Focus a result after Up and Down moved the cursor, Tab out, and Tab back in from the footer. Repeat with the preview open and Include subfolders off.
- Press keypad `/` with Num Lock on and off, and on `is` press the þ key with Type to search on, then off.
- Filter to one match in Icons, then List, and delete it from a shell; repeat in Columns and read the status each time.
- Run a partial-coverage filter that returns results; check whether the status covers the first result row at text size 8 and 48.
- In List and Icons, delete the last hit in sort order, a hit with several hits selected, and a hit through the item menu's Move to Trash. Repeat with Include subfolders off and the preview open.
- Set Search entry limit to 200,000 and filter `100000` plus a second large folder below it; change the limit in another window's Settings and type one more character.
- Select a file hit, then press Space in the location bar, the preview find bar, a sidebar row, and the sidebar toggle; repeat in the file chooser's name and location fields.
- Type `duck  txt` and `txt duck` in Columns with Include subfolders off, then in Icons and List with it on.
- Type `duck *.txt` and `* duck`, then filter `trash:///` and an `sftp://` share with a two-word query.
- Filter an sshfs folder, stall its daemon, and delete a hit from the server; then resume it.
- In Columns, focus a filter result in column 2 and press Ctrl+F, then `/`; repeat with Include subfolders off and with the preview open.
- In Columns, filter with Include subfolders on and off, and with a pointer and a keyboard multi-selection, then choose each sort.

### browser/search/filter/enter-target

- Type a query in `100000` in each view and read which row is outlined as batches arrive; then wheel-scroll once mid-load and keep typing.
- Ctrl+click the top hit, then create a matching file from a shell, and edit the query.
- Filter `trash:///`, `recent:///`, and an `sftp://` share with a selected row, press Enter, then edit the query and press Down.
- Type a query, add and then remove a trailing space, and press Enter; repeat with a case-only edit.
- Turn 10xer mode on, open Ctrl+F, and type; then turn it off with the field still open.

### browser/sidebar

- Drop a row on another row's exact midline, then between the PINNED heading and its first pin; restart and compare the order in a second window.
- Offer a nightly and a release candidate with the interface in ja and with the sidebar at its minimum width; read the notice text and its accessible name.
- With a notice shown, set text size 8 and 48 and compare the notice row's height with an empty sidebar foot. Then step to the rail and on to full at each size.
- Show a notice with the interface in ko, ru, and zh-CN at the default sidebar width, then drag the sidebar to its minimum.
- Unset `XDG_MUSIC_DIR` and point Documents at a missing folder in `user-dirs.dirs`; shrink the window to the icon rail and Tab through it.
- Click an unmounted `sftp://` pin and cancel its password prompt, then enter a wrong password; click Network with `GIO_USE_VFS=local` in tab 2 and switch to tab 1.
- Drag Trash slowly across Home's upper half, the gap below Home, and Home's lower half, releasing at each; restart and read the order in both windows.
- In the file chooser, reorder Home and Downloads, unpin Music, and right-click a pin; then open a browser window and compare.
- Drag files over the Trash row with a selection inside Trash and with one on a read-only mount; then shrink the sidebar to the rail mid-drag.
- Middle-click and choose Open in New Tab on Trash, Recent, Network, an unmounted `sftp://` pin, a mounted USB drive, and an unmounted volume; then do both on the icon rail.
- Double middle-click a sidebar row, and middle-press one and drag past the threshold before release; count the tabs.
- Hover the current row and rows on the icon rail, in a light and a dark theme.

### browser/sidebar/rail

- Turn off every place chip; press Ctrl+B in one window until the sidebar hides while the other's sidebar has focus, then press Ctrl+Shift+B there.
- Open a 1200 px and a 700 px window. Press Ctrl+B through three full cycles in the narrow one, reading both windows and `settings.toml` after each press.
- Choose the rail in a wide window, then narrow it, open and close the preview in Columns, and widen it again.
- Step from hidden to full in a narrow window, then resize by 1 px, by 300 px, and open the preview.
- With the rail showing, set text size 9, 11, 8, and 48 at desktop text scaling 1.0 and 1.18. Compare rail icons and the update notice icon against the header toggle.
- Switch 10xer mode on and off while the sidebar is railed and while hidden, then hover the toggle and read it with Orca.
- Step the sidebar toggle by Space through every mode in the default and 10xer key maps and in `de`. Read its accessible name after each step.

### browser/sidebar/pins

- Edit the bookmarks file externally with a CRLF line, a duplicate, a `file:///home/<user>` line, and `smb://u:p@h/s`; pin a folder and diff the file.
- Pin a folder, `chmod 444` the bookmarks file, unpin; then pin a folder on `/dev/shm`, trash it from the other window, and press Ctrl+Z.
- With Type to search off press `p` on a file, a pinned folder, a standard folder, and a folder inside Trash.
- With the bookmarks file symlinked, delete a pinned folder from the other window; read `ls -l` and the file.
- In Columns, reach a folder by arrows, by Enter, and by a typed path, and press `p` each time.
- Pin from one window while Nautilus rewrites the bookmarks file in a loop; then reorder in a second window and open a third.
- Pin 50 folders, trash them all, cancel midway, and watch PINNED in two windows.

### browser/sidebar/pins/drag-to-pin

- Unpin a pin's neighbour in one window, then drag three folders, one already pinned, into that gap in the other window.
- From the drag-source fixture, offer a Move-only payload, a mixed file and folder payload, and 100 folders on an `sftp://` share; then drag a folder from Nautilus.
- Start a foreign folder drag over a gap and plug in a USB drive before releasing.
- Drag a folder from the Trash view, an `https://` link from a web browser, and a symlink to a folder over the gaps; then drag an SMB pin between two local pins.
- With nothing pinned, drag a file over the sidebar and out again, then drag a folder in; repeat in the file chooser and on the icon rail.

### browser/sidebar/connect-to-server

- Tick Pin to sidebar and connect to a local file path, `~`, `../`, and `sftp://` with no host; read the bookmarks file after each.
- Connect to the unresolvable host and press Escape at once; wait 30 s and check that nothing opens.
- Enter a wrong password, cancel the second prompt, then press Connect again within 1 s.
- With Pin to sidebar ticked, connect to an already mounted `smb://host/share`, to `smb://host/share/`, and to a `davs://` address; unpin each and diff the bookmarks file.
- Open the dialog in two windows and connect both to the same share with Pin to sidebar ticked.
- With the interface in de and zh-TW, show a long connection error at the minimum window width.

### browser/thumbnails

- Scroll the slow directory to the end and back twice; look for icons left on decoded rows and thumbnails on the `.svgz` and `.ogg` files.
- Rename an image while its decode runs, then overwrite an image's bytes keeping its mtime with `touch -r`.
- Remove the HEIC or JPEG XL decoder package and reopen the folder; open an `smb://` share with `gvfsd-fuse` stopped.
- Turn Show thumbnails off mid-load in the slow directory, then on within 200 ms while videos' durations stream into Icons captions; repeat in a folder peek and a Ctrl+K result list.
- With Show thumbnails off, open the portal file chooser and a second window, then turn it on from Settings and scroll each.
- Open a folder of the RAW samples with and without `dcraw` and `simple_dcraw`; compare orientation and Icons captions.
- Turn STL model thumbnails on in a folder of 50 STL files and images, scroll, and turn it off mid-render in a second window.
- Turn STL model thumbnails on with Show thumbnails off, then turn Show thumbnails on. Open the folder in a peek, Ctrl+K results, and the portal file chooser.
- Open `.stl` and `.STL` files on an `smb://` share with `gvfsd-fuse`, on an sshfs mount, and in a camera library; compare with the local copy.
- Render an ASCII STL, a zero-triangle STL, and a 127 MiB binary STL; change a rendered file's bytes and reopen the folder.
- Open a folder of `.gcode`, `.GCO`, and `.bgcode` files with STL model thumbnails off, then on; repeat on an `smb://` share and in the portal file chooser.
- Open the slow directory's images as administrator in each view; compare `$XDG_CACHE_HOME/thumbnails` before and after.
- In each view, `chmod 000` a folder in view from a shell, with and without a custom icon. Watch its icon once its metadata fills.
- Paste 200 files into a folder scrolled just past the margin in the `10000` fixture, start a second paste into it, cancel one, then scroll it into view.

### browser/thumbnails/cache

- Plant entries that are a symlink, a 3 MiB PNG, a 600 px PNG, and a JPEG renamed `.png`, each with matching tags; reopen the folder.
- Delete `thumbnails/large`, make it a `chmod 755` directory, reopen, and read its mode; then point `XDG_CACHE_HOME` at an unwritable path.
- Thumbnail the RAW samples with another file manager first, open the folder twice in Strata, then let the other file manager rewrite the cache and reopen.

### browser/thumbnails/workers

- Set workers to 1 in the slow directory, then 16 mid-load, and count sandbox processes with `pgrep`; kill one with SIGKILL during a scroll.
- Set `STRATA_THUMBNAIL_WORKERS=99`, then `abc`, and `STRATA_THUMBNAIL_IDLE_SECONDS=1`; read the shown default and watch process exit.
- Type 0, 17, `abc`, and an empty value into the Thumbnail workers spin button, pressing Return, then Tab, after each; read `thumbnail_workers` back.
- With workers at 1 and STL thumbnails on, open a folder of 20 STL files beside a folder of PDFs in a second window. Open Quick Preview on an STL meanwhile.
- Put an STL on an NFS or sshfs native path, stall the server mid-render, and scroll on to other STL files.
- With workers at 1, load a 600 MiB `.gcode` with its thumbnail in the header beside a folder of PDFs; then one with no thumbnail, and one stalled on sshfs.
- Hide `magick` and `convert` from Strata and load a folder of PNG, JPEG, WebP, and TIFF files with glycin 2.1 and 2.2 or later; then repeat without Landlock ABI 3.

### browser/properties

- Open Properties on a file you cannot chmod, the broken symlink, and the 255-byte name. Toggle a bit, press Escape before it applies, and read AT-SPI states.
- Press Alt+Enter with nothing selected, with the sidebar focused, and in Recent; set each date format and reread MODIFIED.
- Copy path for a name holding `'` and a space, and for a file in `trash:///`; paste each in a shell.
- Copy path from the empty-space Properties of the current folder, from a symlink to a folder, from a symlink to a file, and from the broken symlink.

### browser/properties/media

- Open Properties on a 0-byte `.mp4`, a WAV renamed `.png`, a rotated phone video, and an MP3 with cover art.
- Close the dialog within 100 ms of opening it on a long video; reopen after rewriting the file externally.
- Open Properties on `notes.h264`, `empty.h264`, the `.H264` and `.264` copies, and the `.h265` and `.hevc` streams.

### browser/properties/raw-metadata

- Open a `.dng` with no EXIF, an `.ARW` truncated to 1 KiB, a JPEG renamed `.NEF`, and a RAW on an `sftp://` share.
- Hold Down through five RAW files with the preview panel open; the rows must not reorder or disappear.
- Open Properties on `IMG.IIQ`, `GOPR0001.GPR`, `a.PTX`, and `b.crf`.

### browser/properties/size

- Open Properties on `100000` and on `deep`; watch the counter cadence and read the nesting warning text.
- Select 300 items including the unreadable folder and the symlink to a folder; compare with `du -sb`, close mid-count, and reopen at once.
- On an `sftp://` share, permanently delete, open Properties on, and multi-select Properties for a folder holding dot-files, a symlink to a folder, and nested folders. Watch the log and compare totals with `du -sb` on the server.

### browser/context-menu

- Open the menu on a file, folder, archive, symlink, Trash item, Recent row, and empty space in each view; diff the action lists.
- Right-click the last row of `100000` scrolled to the end at text size 28; then open a menu and press F5, Ctrl+2, and resize the window.
- Press Menu with the filter field focused, the location entry focused, and a drive row focused; right-click a second entry while a menu is open.
- Press Right on Open in… in a multi-selection of folders, then Left; open the menu on a folder in Trash and a Recent folder row.
- Choose Open in… → New Window on three folders and two files, in Trash and Recent.
- With the interface in German, then Japanese, open a file's, a folder's, and the background menu; compare each hint with its F1 row and press it.
- On niri, quick-right-click on empty space near the bottom edge and where a submenu row lands; then reopen the menu with Menu and click a row.
- Right-click a folder, choose Copy, reopen its menu within one frame, then alternate file, folder, and multi-selection menus while watching the log.
- Under Flatpak, select files of two types with different defaults and with no default, open the multi-selection menu, and choose Open.
- On GTK 4.14, open a file's menu near the window's bottom edge, choose Open With…, pick an application, then reopen the menu and the chooser three times.
- Open the menu on a file on a virtiofs share, a 9p share, and a mergerfs mount.
- Shrink the window to 400×300 and right-click an entry at its right edge; then press Shift+F10 there with nothing selected.
- Move the window against the monitor's bottom edge and right-click the last row, then open the multi-selection menu of 50 entries there.
- With two monitors of different heights, open a long menu near the shorter one's bottom, then with the window straddling both.
- Repeat the edge probes on GNOME, KDE, Hyprland, X11, and GTK 4.14, and in the file chooser and Ctrl+K results.
- Open a file menu in one window, rebind Rename and Copy in Settings → Keyboard from a second window, and read the hints; repeat in 10xer mode and in German.
- In an admin folder, open the menu on a file, a folder, a mixed multi-selection, and empty space.

### browser/directory-monitoring

- Run `touch f{1..5000}` then `rm f*` in the open folder; count the rows afterwards and look for duplicates and lost selection.
- `mv` the open folder in Columns with three descendants open, then `rm -rf` it; repeat in Icons and List.
- Stall an NFS mount, press F5 with an inline rename open in its folder, and resume the server before submitting the rename.
- On a stalled mount, open a 2,000-entry folder, press F5 before all rows show, and resume the server.
- `mv` the open folder during a 2,000-file copy into it. Then `mv` it twice within 100 ms and press Escape during the second.
- `rm -rf` and recreate the open folder within 100 ms; `chmod 000` it; `mv` a dot-named open folder with hidden files off.
- `mv` an open folder on an `sftp://` share, the ntfs-3g partition, an `sshfs` mount, and a kernel exFAT partition; read the pane and history.
- Open the 200,000-entry folder, then the 260,000-entry one, locally, over `sftp://`, and on an `sshfs` mount; read the pane header after each load settles.
- Paste 50 files into an open `sftp://` folder and an sshfs folder, cancel halfway, then repeat to completion; count reloads and rows each time.
- With hidden files on, open `deep` to column 5, press Ctrl+H, and rename the column 3 folder to a dot name; then press Back.
- Rename an open folder to a dot name from a shell with hidden files off, then after Ctrl+H toggled them on and off mid-session.
- Rename a column's only visible entry, an open folder, to a dot name with hidden files off; then press F2 and Down.
- Sort a 2,000-entry folder on a stalled sshfs mount by Size; while sizes load, press F5, go Back, and switch to Icons and List.
- With hidden files off, create, rename, and delete dot-files from a shell, then press Ctrl+H. Do it in each view, on an `sftp://` folder, on an sshfs mount, and in `10000`.
- Drop a file onto a folder shown in two windows, one in Columns with sizes off and one in List; turn sizes on afterwards.
- Merge a same-named folder over one with open subfolders, then undo the merge; read every count in the open columns.
- Drop a file onto a folder in the `100000` fixture while its parent is still loading, and onto an `sftp://` folder.

### browser/directory-monitoring/network-checks

- Change files from the server in a shown NFS folder while the window sits on another workspace; time the appearance.
- Turn Watch network folders off and on in one window while a second window and the portal chooser show the same NFS folder.
- Edit a file in place on the server and leave the window for 29 s. Repeat with 31 s, comparing its size and date on return.
- Run `rsync -a` into a shown SMB folder, which puts its modification time back. Then change a Samba folder from the server itself.
- Change a 9p `cache=loose` share and an rclone bucket twice in one second, with power-saver on, then off.
- Start a rename in a shown NFS folder, change the folder from the server, and wait three checks before Enter. Repeat during a 2,000-file paste into it.
- `chmod 000` a shown NFS folder from the server, then `rm -rf` it, then recreate it under the same name.

### browser/folder-customization

- Customize a folder, rename it externally, and create a new folder at the old name; then pick a custom color and press Escape at each step, reading settings.toml.
- Write `emoji:` with a 70-byte string and an unknown icon name into `[custom_icons]`; start, then switch theme with the folder visible in two windows.
- Close the custom color dialog by a click outside it, then Customize the same way. Delete the item externally while Customize is open and press Escape.
- Customize a folder, move it with Keep both, undo, and redo. Then trash it, trash a new folder from the same path, and Put back both.
- Replace a customized folder by a copy, Merge one into a customized folder, and move one to an `sftp://` share; read settings.toml after each.
- Customize two folders whose non-UTF-8 names decode to the same text, then Clear one; read settings.toml and both icons.
- Open the custom color editor under the Adwaita and Papirus icon themes and compare its spin buttons.

### browser/scrolling

- Middle-click in `100000`, move 10 px, 50 px, and 300 px; press Escape with a 10xer chord armed, then click a folder row.
- Page Down through Icons with the preview panel open, close it, Page Up; then Ctrl+Down with hidden files off where the last ten entries are dot-files.
- Open Sort by, then wheel over the sidebar, the header, and the second window's listing; middle-click a filter field holding a primary selection.
- Press Home and End with hidden files off where the first and last entries are dot-files. Repeat in filter results and right after a folder opens.
- Middle-click the gutter between Icons cards, a card's padding, blank List Name space, and the blank strip beside the last column.

### browser/tabs

- Open 12 tabs, hold Ctrl+Shift and press 0, drag tab 12 to position 1, press Ctrl+Shift+1; read which tab each step selects.
- Press Ctrl+W with Properties open, then close every tab from the last one; change Show hidden files with three tabs on one folder and switch through them.
- Open tabs on `trash:///`, `/`, and a 30-character folder name; press a Columns folder, drag 5 px, release, and read the tab name during and after.
- Focus an empty folder's pane in tab 2, fill the folder from a shell, then switch away and back.
- Press Ctrl+Enter on a folder among Ctrl+F results, then Ctrl+Shift+Enter on a folder in both key maps.
- Open a new tab on the unreadable folder and an unmounted `sftp://` pin.
- Start a 2,000-file copy in tab 2 and select tab 1. Middle-click tab 2, close the window, then cancel the copy and close again.
- With 11 tabs open, press Ctrl+Shift with each digit-row key on `fr`, `cz`, `ru`, and with Caps Lock on. Then show the badges and press Super, and hold Ctrl+Shift+Hyper.
- Close 25 tabs one by one, then press Ctrl+Shift+T 21 times; read each reopened tab's location and position.
- Close a tab with 10xer `t` then `x` and reopen it; then reopen while the location editor is open on another tab.
- Close a tab on an `sftp://` share, unmount it, and reopen; close a tab on `trash:///` and reopen after emptying the Trash.
- Close tab 3 of 5, close two more tabs, reopen once, then drag tabs and reopen again.
- Read the window title with `xprop` on `~`, `/`, `trash:///`, `network:///`, a 60-character folder, and a non-UTF-8 name, in `de` and `ja`.
- Switch tabs with Ctrl+Tab, close the active tab, and navigate a background tab during a long copy; read the title after each.
- With the window idle, rename a tab's folder from a shell and change text size from another window; check the underline matches the new tab bounds.
- With 12 tabs overflowing the strip, drag a sidebar row to the strip's scrolled-off ends and release on each tab's left and right halves; read each new tab's position.
- Drag three folders, then a folder plus a file, from each view onto the strip; drag a folder from Nautilus onto a tab header.
- Drag a sidebar row onto the other window's strip and its New tab button. Then drag a tab onto the other window's strip.
- Start a sidebar drag, close tabs from the keyboard down to one, and release over where the strip was; then press Escape mid-drag with a modal dialog open.
- With a modal dialog open, drag a sidebar row and a folder from another window onto this window's strip and New tab button.
- Press Escape mid-drag on Wayland and on X11: over a tab header, a sidebar row, a breadcrumb, and a spring-opened folder. Release over a folder each time.
- Press Escape during a multi-selection drag, during a drag from another application, and while dragging out to another window.
- Leave a tab with focus on a breadcrumb, the header search button, a 10xer footer prompt, and the update notice; return by click and by Ctrl+Tab.
- Leave a tab from a preview audio timeline and from a sidebar pin, then close that pane in a third tab before returning.
- Restore 5 tabs and visit each by click, then by Ctrl+Shift+<n>, before and after their listings finish loading.

### browser/tabs/session-restore

- Save tabs on `sftp://host/x`, `smb://user@host/share`, `trash:///`, `admin:///root`, a folder deleted before relaunch, and the `chmod 000` folder; relaunch and read `tabs.toml` before and after.
- Run plain `strata` while a window is already open; count tabs in the new window, then change tabs in each window and quit both.
- Hand-edit `tabs.toml` with 40 entries, an unknown `kind`, and duplicate entries; relaunch after each.
- Open a tab on the non-UTF-8 folder beside two other tabs, select it, quit, and relaunch.
- Replace `tabs.toml` with a symlink to another file and with a directory, then change a tab; make `$XDG_CONFIG_HOME/strata` read-only.
- Turn Restore open tabs off in one window's Settings while a second window changes tabs, then on again, and quit.
- Close tabs down to one, then close the window, and relaunch plainly.
- Open a window through a FileManager1 `ShowItems` call, add tabs there, quit, and relaunch plainly.
- Save tabs on a stalled NFS folder, an unplugged USB folder, and a folder replaced by a file; relaunch, then resume the server.

## Hand-offs

- Drag and drop once a press is read as a file drag, except Escape cancellation, which `browser/tabs` owns → `operations`.
- File transfers dropped on tabs and sidebar rows, and every file operation → `operations`.
- Trash, Undo, and Replace inside `admin://` folders, and Trash drops from them → `operations`.
- Open and Open With refusals for files in `admin://` folders → `integration`.
- DEVICES rows, Set label…, mounting, and ejecting → `devices`.
- Remote shares beyond the typed URI rejections and credential masking covered here, including the mounts and sign-in prompts behind Connect to server → `remote`.
- The action editor's tabs, toggles, and footer beyond arrow focus → `integration`.
- Modal dialog shell, the shortcut footer, F1, and key precedence → `app`.
- What the preview panel and quick preview render → `preview`.
- The Settings pages that hold the preferences named in these probes → `settings`.
- 10xer-mode key variants and the portal file chooser → `integration`.
- Sidebar rail fit rule and automatic rail → `preview`.
