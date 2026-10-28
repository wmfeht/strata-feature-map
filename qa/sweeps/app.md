---
title: App sweep
reviewed_at: 923b39ddf4950227e0779ef5b6216af7f4773727
triggers: [src/ui/window.rs, src/ui/window/keyboard/items.rs, src/ui/frame.rs, src/ui/motion.rs, src/style.css, src/ui/input_ownership.rs, src/ui/window/tests.rs, src/ui/frame/tests.rs]
tools: [scripts/test_installer.py, install.sh, docs/packaging.md, docs/signed-updates.md, docs/keyboard-navigation.md, docs/keyboard-shortcuts.md, tests/qa/keyboard.rs, tests/fixtures/harness.json, scripts/qa-drive.sh]
---

## Scope

The application shell around the browser: accessible names, roles, and states over AT-SPI; the modal dialog shell with its blur, dismissal, focus, and forms; the F1 shortcut reference and the footer with its counts and clipboard badge; window chrome, identity, window buttons, and the capture-phase key dispatcher; how key presses become shortcuts on any keyboard layout or input method, and how shortcuts are labelled; the desktop entry, `--version`, the release installer, and the AUR packages; update checks, release notes, release channels, installing a chosen release, signed in-place install, and package-managed installs. It also covers the shared location model and listing adapter: URI display rules, skipped-entry warnings, media metadata probing, directory-load log privacy, the UI-thread stall watchdog, and the `GDK_DEBUG` re-exec on service activation, plus the absence of the `qa` launch mode from plain builds.

Left to other sweeps: per-mode movement and selection keys, the context menu and Open With, the search palette, the sidebar and the text and layout of its update notice, Settings pages other than Updates, the FileManager1 D-Bus service, Open in Terminal, the portal file chooser, and the content of every individual dialog.

## Setup

- Two builds of the same commit: one plain, one with `STRATA_RELEASE_TAG=v0.0.1-rc.1 STRATA_BUILD_KIND=rc` exported before `cargo build`. The second drives Return to stable and build-kind labels.
- Network control for update checks and downloads. Point `HTTPS_PROXY` at a closed port for a fast failure and at a `nc -l` socket for a stall; run under `unshare -rn` when the proxy is ignored. Live GitHub checks are capped at 60 per hour, so plan them.
- A fake package-managed install: copy the binary to `<prefix>/bin/strata` and write `<prefix>/share/strata/install-source.toml` in the shape `docs/packaging.md` gives. Keep one marker per manager and channel, one with unknown keys, and one made unreadable with `chmod 000`.
- The installer is never run on the host outside the stubs and throwaway `HOME` below. Evidence is `python3 scripts/test_installer.py`, `bash install.sh --help`, and the script read against its Behavior; a fake `omarchy` on `PATH` and `~/.local/share/omarchy/version` under the throwaway `HOME` feed the detection cases.
- Installer menus: drive `install.sh` through a pseudo-terminal in a throwaway `HOME`. Put stub `curl`, `pacman`, `sudo`, and `gdbus` on `PATH`, as the `scripts/test_installer.py` fixture does.
- Set the pseudo-terminal's size with `stty rows N cols M`.
- Cold activation: a private session bus from `dbus-run-session`, with the FileManager1 service file pointing at the build and xdg-desktop-portal 1.22.1 on that bus. Set `GDK_DEBUG` for activated services with `dbus-update-activation-environment`.
- Signed release fixtures: a local release directory served to the stub `curl`, holding a manifest and signatures file signed with a throwaway Ed25519 key. For a full run, copy `install.sh` with the `RELEASE_PUBLIC_KEYS` entry replaced by the fixture key, as `InstallerFixture` in `scripts/test_installer.py` does. Source it with `STRATA_INSTALLER_TESTING=1` only to call single functions.
- Animation and scale: the harness `settings.ini` sets `gtk-enable-animations=false`, so set it `true` for animation probes and toggle `reduce_motion` in `settings.toml`. Set `text_size = 8` and `48` for layout probes.
- AT-SPI dumps from an ad-hoc `gi.repository.Atspi` script under `/tmp`. `./scripts/qa-drive.sh start` in the pinned image opens a separate `--qa` session whose `{"query":"state"}` reads the widget tree, not AT-SPI. Use `xprop WM_CLASS _NET_WM_NAME WM_NAME` for identity. Run a minimal window manager such as `openbox` on the private display before any Maximize, Minimize, or focus-out probe.
- For icon probes, a desktop shell whose dock background can be changed, with Adwaita and an icon theme that ships no Strata icon, such as MacTahoe. Skip those probes and say so when no such shell is available.
- `desktop-file-validate` for the entry, and a second window of the same build for every notice, preference, and dispatch probe.
- Keyboard layouts: load them on the private display with `setxkbmap -display` and an XKB group lock, as `tests/qa/keyboard.rs` does. `tests/fixtures/harness.json` lists the layouts QA scenarios cover. Restore `us` afterwards; never change the desktop's layout.
- For UI-thread stall probes, an sshfs mount of a local folder; stop its daemon with `kill -STOP` and resume it with `kill -CONT`.
- `strace` for counting helper launches; text fixtures named `.mp4` and `.png` generated under `/tmp` with a shell loop.
- A client-decorating compositor for title bar probes: `weston --backend=x11-backend.so` or a nested `mutter --nested` on the private display, with Strata launched against its Wayland socket.
- Input methods: fcitx5 with its pinyin and hangul engines, started on the private display, with `GTK_IM_MODULE=fcitx` exported before launching Strata. Without a daemon, `setxkbmap -display :N -layout cn -variant altgr-pinyin` gives GTK's own dead-key composition.

## Probes

- Repeat each dialog and reference probe in Columns, Icons, and List, with the sidebar shown and hidden, and at text size 8 and 48.
- Run the sweep once with reduce motion on; every animated surface must settle in one frame and still dismiss cleanly.
- Watch the log for GTK criticals while dialogs open, stack, and close and while the window is resized under an open overlay.

### app/accessibility

- Dump the tree in these states: a selection in each mode, an open item menu, a confirmation dialog, each Settings page, the search palette, a rename editor, the F1 reference. Flag unnamed interactive nodes, wrong roles, and missing states.
- Move the keyboard cursor without changing selection and compare which node carries `focused` and which `selected`; repeat after a directory reload and after Trash removes the focused row.
- Tab around the whole window from the sidebar toggle and back; record any control skipped or visited twice, with the sidebar hidden and in an empty directory.
- Switch the interface language to ja and ko and re-read entry, pane, and view descriptions and the menu-item accelerators.
- Hover every header, footer, breadcrumb, and sidebar control for 3 s at each sidebar width and list which tooltips appear.
- Dump the focused node in a `chmod 000` folder and in a folder still loading over a stalled remote mount. Repeat in an empty folder with the interface in ja.
- Empty a folder from a shell while it is open, then add a file back; dump the pane after each step and read its name and description.
- Dump an Icons card with a truncated name while its name tooltip shows, and one whose name fits; compare their names and descriptions.
- Collapse the sidebar to the rail and hover each row: places, pins, a mounted drive, a drive being ejected, and a network location. Expand and collapse it again during the eject.
- With the interface in de and ja, read the names of the pane header buttons, the filter field, and the media buttons against their tooltips.

### app/dialogs

- Stack an error on a paste conflict and a Properties dialog on a drive dialog; dismiss the top one by Escape, backdrop, and close button and read where focus lands and whether the blur remains.
- Click the backdrop ten times during the close animation, then press Enter; nothing must reopen or activate.
- In the Compress dialog, dirty the name, then clear it, and click the backdrop; repeat with a password typed and deleted.
- Shrink the window below each dialog's minimum width plus 84 px, then below the dialog's height; scroll inside, press Enter, and resize back.
- With a dialog open, press Ctrl+K, Ctrl+V, F1, and Ctrl++ in turn and read what each reaches.
- Open Compress or Properties on a row, delete that row from a shell, then close the dialog; repeat in an empty folder and in a second tab after switching back to it.
- Open a dialog from a header button, a sidebar row, and the location field; close each by Escape, backdrop, and close button, then press Down and read where focus lands.
- Run a copy into a read-only folder so an error replaces the progress dialog; close the error and read where focus lands in each mode.
- From Settings, open the action editor; close it by Escape, Enter, backdrop, and close button, and read where focus lands and whether a focus ring shows.
- Open the action editor from an action row in Settings and save an edit so the row re-renders. Then press Tab.
- In Settings → Actions, remove a custom action's folder from a shell, delete its row, confirm, close the error by mouse, and read focus and ring.
- Close a dialog by keyboard, switch to a second window before the 200 ms close animation ends, then return and read the ring.
- In a byte-limited field, paste text whose limit falls inside a multi-byte character. Paste with the cursor at the start, middle, and end, then undo and redo.
- Type into a limited field with an input method composing, and drop text onto it by drag and drop.
- Click an install command's copy button twice within 2 s, then close its dialog before 2 s pass; read the button's name every 500 ms.

### app/shortcut-reference

- Open F1 with a modal open, with a rename editor open, from the location field, and from the sidebar; press Escape twice each time and record where focus returns.
- Type a query, pick a category, scroll, focus another window, and come back; then switch mode with Ctrl+2 while open and reopen.
- Press F1 with Shift, Ctrl, Alt, and Super held, and `~` with type-to-search on and off, in the default and 10xer maps.
- Resize across 1480 px with a query and category active; the footer note must wrap only at a "·".
- Select 1, 64, 65, and all items in a folder holding files of unknown size, a symlink, and 10k entries; read the count and its accessible description, then copy, cut, paste, and clear the clipboard with `wl-copy -c` or `xsel -c`.
- In the default map, run Ctrl+F in each mode on a local folder, a 10k-entry folder, and the SFTP fixture in Columns; read the count while typing, after results land, and after Escape.
- Filter with the default map and select results. Switch to 10xer mode and back with the filter open, then clear the query by Backspace.
- With F1 open in Columns, toggle 10xer mode from a second window, then close and reopen F1 in Icons; repeat with the interface in ja.
- With the interface in German, search F1 for `entf`, `strg+shift`, `bild auf`, `ctrl+−`, and `g-h`; repeat in French with `suppr`.
- In 10xer mode with `us,ru`, press the Ё key and a US `~` in the location field, a footer prompt, F1 search, and the file list.
- In F1 search, type, cut, paste, and select all, then undo and redo past the opening query; repeat on a Russian-only keymap.
- Type an unmatched F1 query at the narrowest window width and with the interface in German, then clear the query and read the results area.
- Read the footer's F1 Shortcuts label and its accessible name with the interface in ja, de, and zh-CN, at text size 8 and 48.
- With fcitx5 pinyin running, open F1, switch to pinyin with Ctrl+Space, and press Ctrl+Left, Ctrl+Backspace, and Ctrl+, while a composition is pending.
- In 10xer mode, type `~` in the global search field, Settings search, a rename field, and the Compress name field.
- Focus an F1 category and press `~`.
- In Icons, search F1 for `ctrl+alt+0`, `+`, and `thumbnail` in both maps, with the interface in English and German.
- Open each 10xer footer prompt in turn, then switch from one prompt to another without closing it; dump the entry after each step.

### app/window

- Launch `strata <dir>` while a window is open, then with a different directory, then with no argument; count windows and read each title with `xprop`.
- Turn each window-button preference on and off with two windows open, restart, and compare the header order in both.
- Maximize, restore, and maximize again by button, by the window manager, and by double-clicking the header; the icon, tooltip, and accessible name must follow the state each time.
- Press Delete, Ctrl+V, Ctrl+1, and Ctrl+Q in three states: a popover menu open; a modal open with focus on the window; the location field focused.
- Navigate by keyboard, park the pointer over another column, press Ctrl+V twice, move the pointer 1 px, and paste again; follow the Input precedence rules in `docs/keyboard-navigation.md`.
- In 10xer mode, open the footer rename with `r` and press Ctrl+K, Ctrl+Shift+K, Ctrl+Alt+T, Ctrl+\\, and F5; then rename in a Columns child column with the palette open.
- On a Russian-only keymap, run Ctrl+Z, Ctrl+Shift+Z, Ctrl+Y, and Ctrl+A in the location field, a rename, the global search field, and Settings search.
- Toggle 10xer mode from a second window while hovering the sidebar toggle, and read its tooltip and accessible name in both windows.
- With a rename open, click the header Search and New tab buttons, and read whether the typed name commits, stays, or is lost.
- With animations on, press Escape on a dialog and at once press each gated key, then Delete and Ctrl+V; repeat with Settings and with a second tab active.
- Under the client-decorating compositor, open a window, a second window, a new tab, and the portal chooser; drag each edge and corner, then maximize, tile, and fullscreen and read the window border each time.
- Under the client-decorating compositor, open a modal dialog and the search palette and check that the blur covers the header.
- With F1 open from Columns, List, and Icons, press F5, Ctrl+K, Ctrl+Alt+T, and Ctrl+\\ with focus on a category, then on the results.
- Close F1 and press the same keys again.

### app/packaging

- Run `desktop-file-validate` on the shipped entry and on the entry a release archive carries, and diff the two.
- Run `strata --version`, `strata --version ~/Documents`, `strata ~/Documents --version`, and `strata --version` with `DISPLAY` unset; compare the output with the prerelease build and check no window appears.
- Build the prerelease build once with `cargo build` and once with `cargo build --release`; compare `strata --version` with the Settings → Updates version line in each.
- Install with `mise run install-local` into a throwaway `HOME`, read `Exec=` in the installed entry, uninstall, and list what remains.
- Read the launcher's generic name and comment in a desktop shell under `LANG=zh_TW.UTF-8`, `zh_HK.UTF-8`, and `zh_MO.UTF-8`.
- View the installed icon at 16, 24, 32, and 48 px on white, mid-grey, and near-black dock backgrounds.
- Compare its size and corners with neighboring icons under Adwaita and under an icon theme with no Strata icon, such as MacTahoe.

### app/packaging/installer

- Run `python3 scripts/test_installer.py` and `bash install.sh --help`; compare the printed flags with the `--with-*` and `--without-*` options the script parses.
- Feed Omarchy detection `dev (b280f130)`, `Omarchy 2.3.1`, `3.10`, `4.0-beta`, and an empty file through the fake `omarchy` and the `~/.local/share/omarchy/version` file.
- Drive the download step against signed release fixtures with two signatures from the pinned key, the first bad and the second good.
- Drive it against a signed release whose archive lacks the icon.
- Serve a manifest of exactly 32,768 bytes and one of 32,769 bytes, and an archive one byte longer than its signed size.
- Run with `openssl` present but lacking Ed25519 support, such as a LibreSSL or an OpenSSL 1.0 build.
- Run `--with-folder-association --without-file-manager` and `--without-desktop-entry --with-folder-association`, in both orders; read the plan's `+` lines.
- Run `--non-interactive` on Arch with `gvfs-smb` and the RAW packages already installed, then the interactive recommended setup on the same system; compare the two plans.
- Write a bindings file with the marker block already present, run the keybind step twice, and diff; then make `hyprctl` report an error and check the backup restores.
- Drive the menus at 23×80, 24×63, and 24×64, with `TERM=dumb`, and with stdout piped to `cat`; press Escape and `q` in each menu.
- In the custom menu, toggle Default file manager, Open file location, and Application launcher in every order, then read the plan's `+` lines.
- In a numbered menu, enter `0`, `99`, `1 2`, `01`, and an empty line in both menus.
- Run with `LANGUAGE=zz`, `LANGUAGE=zh-Hant-TW`, `LANG=zh_SG.UTF-8`, `LC_ALL=POSIX`, and `LC_MESSAGES=ko_KR.UTF-8` with `LANG=fr_FR.UTF-8`; read the banner, menus, and failure lines.
- Install Open file location with the stub `gdbus` exiting 1 and then absent; read the heading and whether the log is kept.
- Repeat with the real `gdbus` and `DBUS_SESSION_BUS_ADDRESS` pointing at a socket that accepts and never answers, such as `socat UNIX-LISTEN:<path> -`.
- On that silent socket, select Default file manager with `XDG_CURRENT_DESKTOP` unset, `Hyprland`, and `GNOME`; read the failure lines, exit status, and leftover `dbus-send` processes.
- Repeat the silent-socket run with Open and Save dialogs and udiskie selected, and time the whole install.
- Point the socket at a peer that answers the handshake after 4 s, and one that answers only after 6 s.
- Remove `timeout` from the stub `PATH`, then run `--help`, `--non-interactive`, and the interactive menu.
- Fail the package step, the desktop-entry step, and the udiskie step in turn; read the failure lines and the retained log.
- Run with `TMPDIR` unset, pointing at a read-only directory, and at a path with spaces.

### app/packaging/aur

- Render both packages with `update_aur.py` for `0.10.0`, `0.10.0-rc.1`, and `0.10.0-nightly.20261001`; compare `pkgver`, `source`, and the refusals.
- Run `namcap` and `makepkg --printsrcinfo` on each rendered `PKGBUILD` and diff against the committed `.SRCINFO`.
- Feed `update_aur.py` a checksum file naming the other architecture, and one naming the previous release.

### app/keyboard-shortcuts

- Run Ctrl+C, Ctrl+V, Ctrl+K, Ctrl+1, and 10xer `j`, `k`, `g g` with `us,gr` and Greek active, then on a Greek-only keymap.
- Repeat the Greek probe on Ukrainian and Hebrew.
- On `ru` and `us,ru`, press Ctrl+Shift+K, Ctrl+Alt+T, and Ctrl+\ with the file list focused.
- On Swiss German, press `t 1`, `g 1`, and `; 1` with the top-row keys, with and without Shift.
- On Icelandic, press the þ, æ, and ö keys in the file list with type-to-search on, off, and in 10xer mode.
- Repeat the Icelandic keys in the location field.
- With Caps Lock on, run Ctrl+A, Ctrl+Shift+N, 10xer `G` and `g g`, Shift+D, and the `~` toggle, on `us` and on `ru`.
- With Num Lock off, then on, press keypad 1, Home, Delete, `+`, and Enter in the file list.
- Repeat the keypad keys in a rename field and in F1 search.
- Press Ctrl+1 and Page Down with Hyper and with Meta held, mapped through `xmodmap` on the private display.
- With a pinyin composition pending in the location field, press Escape, Space, Enter, Tab, and Ctrl+V.
- Repeat the pinyin keys in global search, the footer prompt, F1 search, and Settings search.
- With a pending AltGr dead key on `cn(altgr-pinyin)`, press Shift+AltGr+6 then Escape, AltGr+1 then F1, and AltGr+1 then Ctrl+K.
- Compose a hangul syllable in a rename, then press Down, Ctrl+A, and Tab instead of Escape; read the name and where focus lands.
- Start composing in a Settings search field shown in a popover, and in the file chooser's location field, then press Escape.
- With the interface in ja, read the shortcut labels in the footer and header tooltips.
- With chewing (Zhuyin) active, start syllables with `1`, `-`, and `;` in the location field, a rename, F1 search, and a 10xer footer prompt.
- On `tw` and `tw(indigenous)`, type the AltGr digit-row marks in a rename field, then press `t` and AltGr+1 in 10xer mode.
- With IBus, press Super+Space in a dialog's entry, Settings search, and the Open With search field.

### app/updates

- Start two windows with checks on and the proxy stalled; turn checks off in one window during the stall and watch both sidebars and both Updates pages.
- Launch with a `update-check.toml` under 6 h old for Preview, then with the channel set to Stable, then with the file corrupted; count requests at the proxy.
- Open Settings → Updates on the proxy-failed state, click Check now five times quickly, then restore the network and click once.
- Compare the installed-release expander on the plain build, the prerelease build, and a build tagged with no GitHub release.
- Serve release bodies through the proxy that hold a `<!-->` short form, a comment inside a fenced code block, and `-->` mid-paragraph; read the expander, the Available card, and the update dialog.
- Serve 250 signed releases through the proxy with page 3 answering HTTP 500, then open the release menu.

### app/updates/release-picker

- Open the menu with the network failing, then restore the network and reopen it.
- Switch the channel in a second window while the menu is open, and again while it shows "Loading releases…".
- Pick a release while another install runs from the Updates row or a second window.
- Pick a release, then close Settings before the dialog opens.
- Open the menu on the plain build and on the prerelease build, and compare the check mark and the button label.

### app/updates/release-channels

- On the prerelease build, select Stable with no newer stable release; then select Preview and Nightly and read the button, status, and labels after each change.
- Open the update dialog for a nightly offer, switch the channel to Stable in a second window, and click the dialog's button.
- Repeat with a release candidate chosen from the release list in place of the nightly offer.
- Write `channel = "beta"` and an empty value into `settings.toml` and read the menu after restart.
- Hand-edit the cached release list so a tag reads `v0.10.0-rc.0` and another `0.10.0-RC.1`; neither may be offered.
- Serve a release list holding a stable tag GitHub flags as a prerelease; open the menu on each channel.
- Serve both `v1.0.0` and `1.0.0`, choose the one entry the menu shows, and press Install release; read the tag the dialog names.

### app/updates/install

- Serve a release through the proxy with the manifest tampered against `docs/signed-updates.md`: changed `tag`, an extra field, wrong `source_commit`, an unknown-key signature, and a 33 KiB body.
- Serve an archive 1 byte over its signed size, one with a symlink member, one with a `..` path, and one with 513 entries; after each refusal `~/.local/bin/strata` must be byte-identical.
- Cancel at 10 %, at "Verifying update…", and during "Finalizing update…" from the row and from the dialog; then press Escape and click the backdrop during each phase.
- Run the install with a second window open, a chooser process running, and a copy operation in flight; list which processes receive SIGTERM and whether the restart waits.
- Replace the staged binary with one that exits 1 on `--gvfs-probe`, then one that sleeps 3 s; read the error and check `.strata-update-rollback`.
- Install an older release chosen from the list, then make the relaunched binary exit 1 within 20 s; read which version runs afterwards.

### app/updates/package-managed

- Launch each fake-marker install and read the Updates page: manager row, status suffix, channel menu state, and offered action. Repeat with the helper removed from `PATH`.
- Launch with the unreadable marker and with the marker holding `channel = "preview"` and unknown keys; the page must offer no download.
- Point the AUR check at a package version equal to, below, and above the installed one through the proxy; only the last may show a notice.
- Click "Open AUR Update" with the helper removed from `PATH` after the page rendered.
- On fake AUR and Omarchy installs with no terminal on `PATH`, click the dialog's action twice quickly, then once more after the error.
- On a fake Omarchy install with an update offered, put a stub `omarchy-launch-floating-terminal-with-presentation` on `PATH` that records its arguments; click Open Omarchy Update with the stub present, absent, and not executable, from the Updates row and from the update dialog.

### app/infrastructure

- Browse a native folder, Trash, Recent, and the SFTP fixture once at `RUST_LOG=info` and once at `RUST_LOG=strata=debug`; grep both logs for each path, host, and user name.
- Open `sftp://user:secret@host/dir?token=x#frag` with debug logging on and grep the log for `secret`, `token`, and `frag`.
- Launch `strata` with `sftp://alice@host/f?token=x#frag` and `smb://CORP;alice:pw@host/share` as arguments, with `RUST_LOG` unset and at debug. Open each in a new tab, remove it from Recent, then grep for `alice`, `CORP`, and `pw`.
- Show URIs whose paths hold lowercase `%2f`, a mix of `café` and `%FF`, and `%25` in the location field, Properties, and window title.
- Run Strata under `strace -f -e trace=execve`, open a folder of 200 text files named `.mp4` and `.png` in Icons, and count `ffprobe` launches; repeat with one real clip among them.
- Copy a 2 GiB file into an open folder on tmpfs, ext4, and an NFS or SMB mount, in each mode. Read every row the view shows during the copy.
- With Trash unavailable, paste Replace onto a same-named file in an open folder on tmpfs, vfat, NFS, and an sshfs mount, in each mode. Read the row, size, and date without F5.
- Repeat with the replaced file selected, with a filter active, and with a second tab open on the same folder.
- With the folder open in two tabs and a filter matching the file, swap it with `RENAME_EXCHANGE` from a shell, then delete it at once.
- Start Strata with `STRATA_UI_STALL_MS=250`, open a folder on the sshfs mount, and stop its daemon. Arrow through folders, type a path there, open a context menu, and press Ctrl+Z; read the log after resuming.
- Start Strata with `STRATA_UI_STALL_MS` set to `0`, `-5`, `abc`, and ` 250 `; check for the watchdog thread `strata-ui-stalls`.
- With Strata stopped, call the portal's `org.freedesktop.portal.OpenURI.OpenDirectory` on a file and time the reply. Repeat with activation `GDK_DEBUG` set to `misc` and to `misc:no-portals`, and read `/proc/<pid>/environ`.
- Launch `strata` and `strata <dir>` while the activated process runs, and read the new window's process id.
- Run `strata --qa <dir>`, `strata --qa`, and `strata <dir> --qa` on a plain `cargo build` and a release build; read which window opens and whether stdin is read.

## Hand-offs

- Window title text after a folder opens → `browser`.
- The `GDK_DEBUG` value programs launched from a service-activated Strata see → `integration`.
- Per-mode movement, selection, the keyboard cursor after reloads, and type-to-search → `browser`.
- Context menu items, placement, and Open With → `browser`.
- The sidebar as a navigation surface, the Trash row, and the update notice's text and layout → `browser`.
- Sidebar toggle steps and tooltip text → `browser`.
- Sidebar automatic rail → `preview`.
- Settings layer mechanics and pages other than Updates, including Window buttons and text size controls → `settings`.
- Settings search terms that find "Install a specific release" → `settings`.
- The "Not responding" notice and request lanes on a stalled mount → `browser`.
- The FileManager1 D-Bus service and Open in Terminal → `integration`.
- The portal file chooser, including its identity and refresh after an update → `integration`.
- 10xer-mode key variants and footer prompts → `integration`.
- Tab numbers, view switching, text size, and the filter on other layouts → `browser`.
- Chosen states of sort options and Appearance options other than Hidden files, after changes made while their menus are closed → `browser`.
- Chosen states of Settings choice options and the Hidden files option → `settings`.
- The contents and outcome of operation dialogs such as paste conflicts, Compress, and progress → `operations`.
- The mount authentication dialog and remote paths in the search palette → `remote`.
- Thumbnail size steps and the size notice → `browser`.
- Format Drive label limits and units per filesystem → `devices`.
- The Settings file chooser row on a silent session bus → `integration`.
