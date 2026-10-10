---
title: App sweep
reviewed_at: 72b840e69d6f0df9d33fb5583e62a3a2944886a1
triggers: [src/ui/window.rs, src/ui/window/keyboard/items.rs, src/ui/frame.rs, src/ui/motion.rs, src/style.css, src/ui/input_ownership.rs]
tools: [scripts/test_installer.py, install.sh, docs/packaging.md, docs/signed-updates.md, docs/keyboard-navigation.md]
---

## Scope

The application shell around the browser: accessible names, roles, and states over AT-SPI; the modal dialog shell with its blur, dismissal, focus, and forms; the F1 shortcut reference and the footer with its counts and clipboard badge; window chrome, identity, window buttons, and the capture-phase key dispatcher; the desktop entry, `--version`, the release installer, and the AUR packages; update checks, release notes, the sidebar notice, release channels, signed in-place install, and package-managed installs. It also covers the shared location model and listing adapter: URI display rules, skipped-entry warnings, and directory-load log privacy.

Left to other sweeps: per-mode movement and selection keys, the context menu and Open With, the search palette, the sidebar and its update notice as a navigation surface, Settings pages other than Updates, the FileManager1 D-Bus service, Open in Terminal, the portal file chooser, and the content of every individual dialog.

## Setup

- Two builds of the same commit: one plain, one with `STRATA_RELEASE_TAG=v0.0.1-rc.1 STRATA_BUILD_KIND=rc` exported before `cargo build`. The second drives Return to stable and build-kind labels.
- Network control for update checks and downloads. Point `HTTPS_PROXY` at a closed port for a fast failure and at a `nc -l` socket for a stall; run under `unshare -rn` when the proxy is ignored. Live GitHub checks are capped at 60 per hour, so plan them.
- A fake package-managed install: copy the binary to `<prefix>/bin/strata` and write `<prefix>/share/strata/install-source.toml` in the shape `docs/packaging.md` gives. Keep one marker per manager and channel, one with unknown keys, and one made unreadable with `chmod 000`.
- The installer is never run on the host. Evidence is `python3 scripts/test_installer.py`, `bash install.sh --help`, and the script read against its Behavior; a fake `omarchy` on `PATH` and `~/.local/share/omarchy/version` under the throwaway `HOME` feed the detection cases.
- Animation and scale: the harness `settings.ini` sets `gtk-enable-animations=false`, so set it `true` for animation probes and toggle `reduce_motion` in `settings.toml`. Set `text_size = 8` and `48` for layout probes.
- AT-SPI dumps from `tests/e2e/harness/tree.py` or an ad-hoc `gi.repository.Atspi` script under `/tmp`; `xprop WM_CLASS _NET_WM_NAME WM_NAME` for identity. Run a minimal window manager such as `openbox` on the private display before any Maximize, Minimize, or focus-out probe.
- `desktop-file-validate` for the entry, and a second window of the same build for every notice, preference, and dispatch probe.

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
- With the Appearance menu, a sort menu, and a Settings choice menu each closed, change the choice by shortcut, from a second window, and by hand-editing `settings.toml`; reopen each menu and dump every option's role and `checked` state.
- Toggle Properties permission bits on a file you own, on a read-only mount, and on a file owned by root; dump each bit's `pressed` state after every click.
- Dump an Icons card with a truncated name while its name tooltip shows, and one whose name fits; compare their names and descriptions.

### app/dialogs

- Stack an error on a paste conflict and a Properties dialog on a drive dialog; dismiss the top one by Escape, backdrop, and close button and read where focus lands and whether the blur remains.
- Click the backdrop ten times during the close animation, then press Enter; nothing must reopen or activate.
- In the Compress dialog, dirty the name, then clear it, and click the backdrop; repeat with a password typed and deleted.
- Shrink the window below each dialog's minimum width plus 84 px, then below the dialog's height; scroll inside, press Enter, and resize back.
- With a dialog open, press Ctrl+K, Ctrl+V, F1, and Ctrl++ in turn and read what each reaches.
- Open Compress or Properties on a row, delete that row from a shell, then close the dialog; repeat in an empty folder and in a second tab after switching back to it.
- Open a dialog from a header button, a sidebar row, and the location field; close each by Escape, backdrop, and close button, then press Down and read where focus lands.
- Run a copy into a read-only folder so an error replaces the progress dialog; close the error and read where focus lands in each mode.
- From Settings, open the action editor, a delete confirmation, and an error over it; close each by Escape, Enter, backdrop, and close button, and read where focus lands and whether a focus ring shows.
- Open a dialog over Settings from an action row, edit or delete that action so the row re-renders, close the dialog by keyboard, then press Tab.
- Confirm a delete over Settings into a failure error, close the error by mouse, then repeat by keyboard; read focus and ring each time.
- Close a dialog by keyboard while a second window has focus, then return to the first window and read the ring.

### app/shortcut-reference

- Open F1 with a modal open, with a rename editor open, from the location field, and from the sidebar; press Escape twice each time and record where focus returns.
- Type a query, pick a category, scroll, focus another window, and come back; then switch mode with Ctrl+2 while open and reopen.
- Press F1 with Shift, Ctrl, Alt, and Super held, and `~` with type-to-search on and off, in the default and 10xer maps.
- Resize across 1480 px with a query and category active; the footer note must wrap only at a "·".
- Select 1, 64, 65, and all items in a folder holding files of unknown size, a symlink, and 10k entries; read the count and its accessible description, then copy, cut, paste, and clear the clipboard with `wl-copy -c` or `xsel -c`.

### app/window

- Launch `strata <dir>` while a window is open, then with a different directory, then with no argument; count windows and read each title with `xprop`.
- Turn each window-button preference on and off with two windows open, restart, and compare the header order in both.
- Maximize, restore, and maximize again by button, by the window manager, and by double-clicking the header; the icon, tooltip, and accessible name must follow the state each time.
- Press Delete, Ctrl+V, Ctrl+1, and Ctrl+Q in three states: a popover menu open; a modal open with focus on the window; the location field focused.
- Navigate by keyboard, park the pointer over another column, press Ctrl+V twice, move the pointer 1 px, and paste again; follow the Input precedence rules in `docs/keyboard-navigation.md`.

### app/packaging

- Run `desktop-file-validate` on the shipped entry and on the entry a release archive carries, and diff the two.
- Run `strata --version`, `strata --version ~/Documents`, `strata ~/Documents --version`, and `strata --version` with `DISPLAY` unset; compare the output with the prerelease build and check no window appears.
- Install with `mise run install-local` into a throwaway `HOME`, read `Exec=` in the installed entry, uninstall, and list what remains.

### app/packaging/installer

- Run `python3 scripts/test_installer.py` and `bash install.sh --help`; compare the printed flags with the `--with-*` and `--without-*` options the script parses.
- Feed Omarchy detection `dev (b280f130)`, `Omarchy 2.3.1`, `3.10`, `4.0-beta`, and an empty file through the fake `omarchy` and the `~/.local/share/omarchy/version` file.
- Drive the download step against a local copy of a release with a wrong `.sha256`, a missing `.sha256`, and an archive lacking the icon; nothing may land in `~/.local/bin`.
- Write a bindings file with the marker block already present, run the keybind step twice, and diff; then make `hyprctl` report an error and check the backup restores.

### app/packaging/aur

- Render both packages with `update_aur.py` for `0.10.0`, `0.10.0-rc.1`, and `0.10.0-nightly.20261001`; compare `pkgver`, `source`, and the refusals.
- Run `namcap` and `makepkg --printsrcinfo` on each rendered `PKGBUILD` and diff against the committed `.SRCINFO`.
- Feed `update_aur.py` a checksum file naming the other architecture, and one naming the previous release.

### app/updates

- Start two windows with checks on and the proxy stalled; turn checks off in one window during the stall and watch both sidebars and both Updates pages.
- Launch with a `update-check.toml` under 6 h old for Preview, then with the channel set to Stable, then with the file corrupted; count requests at the proxy.
- Open Settings → Updates on the proxy-failed state, click Check now five times quickly, then restore the network and click once.
- Compare the installed-release expander on the plain build, the prerelease build, and a build tagged with no GitHub release.

### app/updates/release-channels

- On the prerelease build, select Stable with no newer stable release; then select Preview and Nightly and read the button, status, and labels after each change.
- Open the update dialog for a nightly, switch the channel to Stable in a second window, and click the dialog's button.
- Write `channel = "beta"` and an empty value into `settings.toml` and read the menu after restart.
- Hand-edit the cached release list so a tag reads `v0.10.0-rc.0` and another `0.10.0-RC.1`; neither may be offered.

### app/updates/install

- Serve a release through the proxy with the manifest tampered against `docs/signed-updates.md`: changed `tag`, an extra field, wrong `source_commit`, an unknown-key signature, and a 33 KiB body.
- Serve an archive 1 byte over its signed size, one with a symlink member, one with a `..` path, and one with 513 entries; after each refusal `~/.local/bin/strata` must be byte-identical.
- Cancel at 10 %, at "Verifying update…", and during "Finalizing update…" from the row and from the dialog; then press Escape and click the backdrop during each phase.
- Run the install with a second window open, a chooser process running, and a copy operation in flight; list which processes receive SIGTERM and whether the restart waits.
- Replace the staged binary with one that exits 1 on `--gvfs-probe`, then one that sleeps 3 s; read the error and check `.strata-update-rollback`.

### app/updates/package-managed

- Launch each fake-marker install and read the Updates page: manager row, status suffix, channel menu state, and offered action. Repeat with the helper removed from `PATH`.
- Launch with the unreadable marker and with the marker holding `channel = "preview"` and unknown keys; the page must offer no download.
- Point the AUR check at a package version equal to, below, and above the installed one through the proxy; only the last may show a notice.
- Click "Open AUR Update" with the helper removed from `PATH` after the page rendered.

### app/infrastructure

- Browse a native folder, Trash, Recent, and the SFTP fixture once at `RUST_LOG=info` and once at `RUST_LOG=strata=debug`; grep both logs for each path, host, and user name.
- Open `sftp://user:secret@host/dir?token=x#frag` with debug logging on and grep the log for `secret`, `token`, and `frag`.
- Show URIs whose paths hold lowercase `%2f`, a mix of `café` and `%FF`, and `%25` in the location field, Properties, and window title.

## Hand-offs

- Per-mode movement, selection, the keyboard cursor after reloads, and type-to-search → `browser`.
- Context menu items, placement, and Open With → `browser`.
- The sidebar as a navigation surface and the Trash row → `browser`.
- Settings layer mechanics and pages other than Updates, including Window buttons and text size controls → `settings`.
- The FileManager1 D-Bus service and Open in Terminal → `integration`.
- The portal file chooser, including its identity and refresh after an update → `integration`.
- 10xer-mode key variants and footer prompts → `integration`.
- The contents and outcome of operation dialogs such as paste conflicts, Compress, and progress → `operations`.
- The mount authentication dialog and remote paths in the search palette → `remote`.
