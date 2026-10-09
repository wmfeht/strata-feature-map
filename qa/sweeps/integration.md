---
title: Integration sweep
reviewed_at: aee71335dfecd059b9af23efeac2ed52c43e3b19
tools: [docs/portal-file-chooser.md, docs/10xer-mode.md, docs/custom-actions.md, scripts/chooser-dev.sh, scripts/portal-test.py, scripts/portal_test_environment.py, scripts/portal-test.html, tests/e2e/harness/portal.py]
---

## Scope

Every seam between Strata and the rest of the desktop. The portal file chooser: request handling, browsing and accepting in each request kind, the destination choosers for Move to, Copy to, Extract to, and Send to, install and restore of the portal and file-manager roles, Name field filenames and URL downloads, PNG conversion of downloads, and initial size and placement. 10xer mode: the saved preference, keymap ownership, movement, selection, Escape, preview key ownership, place chords and the folder picker, find, filter, and search, the file commands and their chords, and the mode inside the chooser. Open With: activation, the Run confirmation, the application chooser, Always use, Recently Used, and Open in Terminal. Custom actions: manifests, matching, invocation, the Settings editor, and the recipe library. The FileManager1 D-Bus interface.

Left to other sweeps: the installer, `.desktop` entries, and single-instance activation, the composition of the context menus, what Move to, Copy to, Extract to, Trash, delete, and Compress do on disk, the Jobs dashboard, views, selection, and tabs inside the chooser, preview rendering, and external file providers.

## Setup

- `mise run chooser-dev`, or `scripts/portal-test.py <case> --binary target/debug/strata`, gives a private bus and backend with disposable settings. Cases: `single`, `multiple`, `directory`, `filters`, `png`, `save`, `savefiles`; `--view`, `--choices`, `--filter-count N`, `--cancel-after S`, and `--folder` vary them. The client prints the response code and URIs. Never run `--install-portal` against the VM's real session.
- `python3 -m http.server 8765 --bind 127.0.0.1` over a folder of download fixtures: JPEG, BMP, static and animated WebP and GIF, APNG, a CMYK JPEG, an EXIF-rotated JPEG, a 17-megapixel JPEG, a 33 MiB BMP, a 301 redirect, and a 404. `scripts/portal-test.html` covers frontend routing only when a portal-aware browser is installed on the VM.
- `busctl --user call org.freedesktop.FileManager1 /org/freedesktop/FileManager1 org.freedesktop.FileManager1 ShowItems ass N <uris> ""` on the private bus. A copy of `data/io.github.lgse.Strata.FileManager1.service` with `Exec=` pointing at the build goes in the throwaway `$XDG_DATA_HOME/dbus-1/services` for activation probes.
- A fake `xdg-terminal-exec` first on `PATH` that appends its argv and cwd to a log; a second `PATH` without it and without any known emulator; fake `kitty` and `$TERMINAL` scripts that exit 127.
- A fake `.desktop` default handler under `$XDG_DATA_HOME/applications` that logs its argv, in `%f` and `%u` variants, plus `NoDisplay=true` and `OnlyShowIn=KDE` twins; `mimeapps.list` in the throwaway `$XDG_CONFIG_HOME`.
- `$XDG_CONFIG_HOME/strata/actions` with a Python action, a Bash action, and a command action: one with `confirm = true`, one per-item, one naming a missing interpreter, one broken manifest, and one that emits progress and output events.
- A folder under `/dev/shm`, whose listing reports no Trash support, beside a regular Home folder.
- 10xer mode toggled through Settings → General → Browsing or `tenxer_mode = true` in `settings.toml`; two windows of the same build.
- A keyboard-only session: no pointer input, footer text read over AT-SPI. Window-placement probes need a nested Hyprland with two monitors; skip them under Xvfb and say so.

## Probes

- Run each chooser probe in Columns, Icons, and List through `--view`; the printed response and URIs must not depend on the view.
- Run each 10xer probe with the mode on, then off, in the same window, and read the footer after every key.
- Watch the log while a chooser closes, the backend exits idle after 120 seconds, and a window closes with the mode on.

### integration/portal-file-chooser

- Return a non-UTF-8 name, a 255-byte name, and a name containing a newline from each request kind; compare the URIs byte for byte against `ls -b`.
- Send 17 concurrent requests, reuse a handle, and send a 4,097-byte title; then `--filter-count 33`, `129`, and one filter with 1,025 rules.
- Save into a read-only folder, with an empty name, with `a/b`, and with a suggested name that is an existing folder.
- Run `--cancel-after 1` while a Replace prompt, a download, and an inline rename are open; read the response code and the `strata-download-*` folder.
- Under `multiple`, fill two files and press Enter in Icons, on a focused filter result, with Shift held, and after Ctrl+A over a folder and files.
- Under `save`, select a non-UTF-8 file, type a character into Name and delete it, then Save; repeat after selecting two files whose names render alike.
- Open a Space preview and the filter, press Down onto a result, then press Escape three times; read the response code after each.
- Press Tab and Shift+Tab around the file list in each view, in an empty folder, with a filter open, and under `save` with Name present.
- Open Move to… from two windows, invoke Copy to… in each while open, then close an originating window with its chooser's New Folder editor active; in Send to, type a path outside the device with Ctrl+L.

### integration/portal-file-chooser/setup

- Run `--install-portal` with `portals.conf` already listing `strata;` last, with no `xdg-desktop-portal` on the system, and from a binary path containing a space; diff the config directory and `state.toml` after each.
- Edit `portals.conf` by hand after installing, then `--uninstall-portal`; repeat with the file untouched and with a hand-made config present before install.
- Complete setup with a foreign per-user FileManager1 service present, then Restore default with no Nautilus on `PATH` and no recorded handler; read each message.
- Run Complete setup twice and Restore default twice; diff the data and config directories between the two runs of each.
- On an Omarchy VM, edit the Strata shortcut block by hand before Restore default, and break `bindings.conf` before Complete setup; skip elsewhere.

### integration/portal-file-chooser/url-download

- Serve `Content-Disposition` with a percent-encoded `filename*`, a 300-byte name, a name containing `/` and `..`, and no name; read the saved name and extension.
- Paste the 301, the 404, a server that stalls after its headers, `http://user:pw@127.0.0.1:8765/a.txt`, and a `file://` URL; watch the ring and the action bar.
- Paste the same URL twice, delete its folder from a shell, paste again; then backdate a `strata-download-*` folder 25 hours and start a download.
- In a 10k-file fixture, type a folder name, a hidden file's name with hidden files off, and a filter-rejected name before the listing finishes.

### integration/portal-file-chooser/image-conversion

- Under `png`, download a JPEG named `.png`, a PNG named `.jpg`, a `BM` file with a 64-byte DIB header, an APNG, and an animated WebP. Then the CMYK JPEG with and without its ICC profile, the EXIF-rotated JPEG, the 17-megapixel JPEG, and the 33 MiB BMP.
- Switch the filter to All files, then edit Name, while a conversion is running; press Open again after each.
- Compare the converted PNG with `identify -verbose` and `exiftool`: dimensions, alpha, orientation, and profile.
- Repeat the JPEG download under `filters` with Images, then Text files, selected.

### integration/portal-file-chooser/window-placement

- On nested Hyprland, request from a client whose app ID matches two windows, one unmapped window, and a mixed-case class; read the chooser size with `hyprctl clients`.
- Use a 1152×720 monitor with a bar and a 3840×2160 monitor at scale 2; move the chooser between them after a manual resize.
- Reload the Hyprland config between two requests and count `strata-file-chooser-center` in `hyprctl rules`; then stop the IPC socket and request again.
- Open Move to… from a Strata window resized to 500×400, and from one maximized on the large monitor.
- Under Xvfb, request at `xrandr` sizes 800×600 and 2560×1440 with no parent; measure the window.

### integration/10xer-mode

- Press Ctrl+Shift+M over a modal, in the location field, in an inline rename, in the sidebar, in Settings, and in a chooser; toggle twice within 1.5 seconds.
- Toggle the mode with a pane filter, a subfolder Ctrl+F scope, a `v` range, a folder peek, and an open preview active at once; toggle back and compare each pane.
- With three windows open, toggle in one; read the F1 reference, menu hints, and Open in Terminal accelerator in the others; close one and check again.
- In Columns, press `g g` and `G` in a newly opened column before any other key, with type grouping on and with hidden files shown.
- Press `G` in an empty folder, Ctrl+U in a 10k folder, and `h` at `/`. Press `l` on a folder symlink and on a broken symlink, in each view.
- Stack a peek, filter, find highlights, range, preview, and selection; count Esc presses to an empty state from the listing, the sidebar, and the header.

### integration/10xer-mode/preview-keys

- Press `l` on a document with the drawer hidden for lack of width, widen the window; repeat moving the cursor before widening.
- In a 50k-member archive press `G`, `h` at the root, then type `hjkl` into its password prompt before Esc; open a member that is itself an archive.
- Press `<` and `>` at the first and last media file, over `s` hits, and with the sidebar focused; press `m`, then Enter, and read the player's start position.
- From inside the preview press `g 3` with no pin 3, `; 1`, `t n`, F2, and Ctrl+1 to Ctrl+3; then click the listing and press `j`.

### integration/10xer-mode/places

- Press `g` then keypad `+` on Trash, on a hidden pin, and as the tenth pin; press `g 9` after unpinning pin 3; press `g -` with a pinned folder open and a file under the cursor.
- In `go ›` submit `~//x`, `/etc//`, `smb:x`, `user@host:` with no network, a pasted path ending in a newline, and a password URI followed by Ctrl+Z.
- Type a path under a 50k-folder tree and press Enter before the search settles; Tab on `.alc` with hidden files off; query `10:30` and a path containing `:`.
- Open `z` with an empty history, `Z` with 200 entries, press Up past the last candidate, and press Enter twice while the list is still updating.
- Arm `g`, then open and close Settings from the gear, Alt+Tab to another window, and press F5; read the footer after each.

### integration/10xer-mode/search

- Find `ß`, `İ`, a regex metacharacter, and a non-UTF-8 name; press `n` after navigating away and `?` from the first row in each view.
- Filter with `!` alone, `'`, `^`, `$`, a 300-character query, with Include subfolders on, and in Trash and Recent; change the theme mid-filter.
- Search from `/`, from a 100k-file tree with navigation mid-stream, over a symlink loop, and to zero hits followed by `g f`; press Ctrl+1 to Ctrl+3 mid-search.
- Create and delete files from a shell while an `f` prompt and then an `s` prompt has focus; press Up and Down in each prompt in Icons.
- With an `f` filter active press Ctrl+F, Down onto a result, and Escape; with a Ctrl+F filter focused on a result, press `f`.
- Leave the mode with an `f` filter in one window and `s` hits in another; re-enter and press `f` and `s`.

### integration/10xer-mode/file-verbs

- Press `y` then `p` across two windows and after a restart; take the clipboard with `xclip` on the private display, then press `Y` and `p`.
- In the `/dev/shm` folder press `d`, then `d`, Enter, Esc, and `y`; repeat on `s` hits spanning it and Home, and on a `v` range.
- Press `d d` on a 10k-item fill, `d` on a range inside Trash, and `D` on `s` hits from several folders. Press `R` on a search selection mixing Trash and non-Trash items.
- In `create ›` type `name/`, `./x`, `../x`, a 256-byte name, a broken link's name, and `.hidden` with hidden files off; `r` on a non-UTF-8 name, in Recent, and on an `s` hit.
- In `move to ›` type a path with trailing spaces, `~user`, a folder symlink, and a child of a target; `C` into a read-only folder; `M` a selection with one item already there.
- Match 11 actions, press `;`, rename an action folder from a shell, then press the digit; `; t` from Network, `; e` on a folder named `x.tar.gz`, `; E` into a typed folder that does not exist.

### integration/10xer-mode/file-chooser

- Toggle the mode from the main window with a chooser open, and from the chooser mid-`create ›`; read footer, chrome, and hints in both.
- Press every refused key under `single`, `multiple`, `directory`, `save`, and `savefiles`; compare each F1 list with what each request refuses.
- Under `savefiles` press `r`, `o` on a file, and Tab around; under `save` press Enter with Name empty, `o` on a folder, and Enter with a Recent file selected.
- Stack a filter, `s` hits, a preview, and a fill, count Esc presses to cancel, and read the response code; repeat with the automatic first row only.
- Press `g t`, `g n`, `g 1` on a remote pin, `g d` with no Downloads, `z` into a folder outside the hint, and `t n`.

### integration/open-with

- Activate a file whose default is the `%u`, `%f`, `NoDisplay`, and `OnlyShowIn=KDE` fake; by Enter, double-click, and Space, in each view; then a type with no handler.
- Run a `.sh` without a shebang, with CRLF endings, with a space in its path, an executable symlink to a non-executable, and an AppImage with a registered type; with no terminal on `PATH`.
- Install 300 fake `.desktop` files; search by desktop id, wrap Up and Down, Tab with a non-empty search, press Escape twice; select three types sharing one handler, and a broken symlink plus a file.
- Check Always use for two types at once, with `mimeapps.list` at mode 444, and cancel with it checked; compare with `xdg-mime query default`.
- On a GVfs FUSE mount, open with a `%f` handler and a `%u` handler; skip when no mount exists and say so.

### integration/open-with/recent-apps

- Open `.txt` files with six different applications, count the rows and order, restart, then corrupt `recent-apps.toml` with bad TOML, a future version, and mode 000.
- Delete a listed fake `.desktop` and reopen the chooser; point `XDG_DATA_DIRS` at an empty directory and reopen.
- Build separate histories for `.txt` and `.png`, then open the chooser on a mixed selection and on each type alone after choosing from Other Applications.

### integration/open-with/terminal

- With the fake `xdg-terminal-exec`, trigger from each view with one folder, one file, two folders, nothing, a sidebar place, and a search hit. Repeat in Trash, Network, a hovered Columns column, and a folder named with spaces and non-UTF-8 bytes; read the logged cwd.
- Set `$TERMINAL` to `footerm --title x`, to the failing fake, and to an empty string; then empty `PATH` of emulators, then add the fake `kitty` that exits 127; read each dialog.
- Press Ctrl+Alt+T with Shift and with Super held, in the location field, during an inline rename, in a chooser, and with the mode on.
- Remove `xdg-terminal-exec` from `PATH` mid-session and run a `.sh` file from Run; compare its dialog with Open in Terminal's.

### integration/custom-actions

- Load manifests with `schema_version = 2`, an unknown key, `entrypoint = "../x.py"`, id `A-b`, a 65-character id, and a folder name unlike its id. Add a symlinked folder, a Python script with `#!/bin/bash`, `program = "bin/tool"`, and a missing interpreter; read Problems and each insensitive item's description.
- Match `extensions = ["JPG"]` against `a.jpg`, `a.JPG`, and `a.jpg.bak`; `image/*` against `.svg` and an extensionless PNG; `min_items` and `max_items` at 0, 1, and 50; the background menu in Trash, Recent, a FUSE folder, and over `s` hits spanning folders.
- Run on 1,000 selected files with newline and non-UTF-8 names in per-item and whole modes; check `STRATA_ACTION_PATHS` bytes, `RUN_DIR` mode and removal, each cwd choice, a forked child, `processed > total`, malformed JSON, and a relative output path.
- Cancel a per-item run at item 3 of 10 with a script ignoring SIGTERM, then close the last window while jobs are queued; hand-edit `prefix-{path}` and `{paths}` in per-item mode into a manifest and reload.
- Derive Id from `Ünïcode Name!!`, switch runtimes three times with edits, and apply a recipe over an edited draft. Duplicate three times, Export into an existing folder, and Import a folder with extra files and a symlinked entrypoint. Run Batch rename with a colliding target and one created between check and rename.

### integration/file-manager-interface

- Call `ShowItems` with three URIs across two folders plus a missing file, and with a percent-encoded non-UTF-8 name beside its lossy twin. Call it with `file:///`, a dotfile with hidden files off, a folder URI, a file URI with a trailing slash, and 200 URIs in one folder.
- Call with argument signature `as` alone, `s` alone, and `StartupId` set to `x`; call while a chooser, a modal, and a Properties dialog are open.
- Install the service copy, call with Strata not running, then twice within one second; run a stub owning the name first and call again; read `busctl --user status org.freedesktop.FileManager1`.
- Call `ShowItemProperties` with two files in one folder, with a folder, and with a Trash URI; call `ShowFolders` on a folder already open in a window and with the mode on.
- Call `ShowItems` on `sftp://localhost/…`, cancel the password, then repeat and accept it; skip without GVfs and say so.

## Hand-offs

- The installer, `.desktop` entries, application ID, single-instance activation, and the modal dialog shell → `app`.
- Composition of the item and background context menus, and views, selection, and tabs inside the chooser → `browser`.
- What Move to, Copy to, Extract to, Trash, delete, and Compress do on disk, and the Jobs dashboard → `operations`.
- Preview rendering, archive and media surfaces, and the player start position handed to the default player → `preview`.
- External file providers, their asynchronous actions and badges, and remote mounts → `remote`.
- The Settings pages hosting the System file manager, 10xer mode, and Actions rows → `settings`.
- The Devices rows in the chooser sidebar and the Send to device list → `devices`.
