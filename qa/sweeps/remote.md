---
title: Remote sweep
reviewed_at: e0f73973926ff67e77c2c56cf288b7b7617bb2e5
tools: [docs/file-providers.md, docs/remote-sftp.md, scripts/sftp-fixture.sh, integrations/README.md, integrations/kdeconnect/tests/mock_service.py]
---

## Scope

Everything that reaches Strata from somewhere other than a local disk. Network locations: GIO/GVfs `smb://`, `sftp://`, and `network:///` with on-demand mounting, and the sign-in, passphrase, and host-key dialogs. They also cover failure messages, log redaction, SMB share lists, progressive remote loading, and the `gvfsd` startup probe. External file providers: registration, reload, and process lifecycle, badges, menu sections and heading icons, and Send to… placement. They also cover activation dialogs and notices, and invalidation. Integrations: the Settings catalog that installs, updates, turns off, and removes bundled providers. KDE Connect and LocalSend: the two bundled providers. `remote/file-providers` itself has no Behavior; its children carry every check.

Left to other sweeps: sidebar rows, the Connect to server dialog, and location-field parsing and history; Settings navigation and search; copy and move semantics once a remote folder is a source or target, previews and thumbnails of remote files, and mounting, unmounting, and ejecting local devices.

## Setup

- `GIO_USE_VFS` must not be `local` and `GIO_USE_VOLUME_MONITOR` must be unset for every probe here. The E2E environment sets `GIO_USE_VFS=local`, which disables GVfs; drop that variable, keep the private D-Bus session, and start `gvfsd` on it before launching Strata.
- `scripts/sftp-fixture.sh --port 2222` for a working `sftp://` location; `--keep` and a second run on the same port for a changed host key; `STRATA_SFTP_PASSWORD` for password prompts. An isolated `known_hosts` and a non-loopback relay for trust questions, per `docs/remote-sftp.md`.
- An `smb://` URI that does not resolve (`smb://no-such-host.invalid/share`), one that refuses (`smb://127.0.0.1:1/share`), and, when Samba is installed, a local share with a guest-readable folder, a password-protected folder, and a 20k-entry folder.
- A fake provider under `$XDG_CONFIG_HOME/strata/providers/<id>/provider.json`: a Python script that answers from a scenario file so delays, malformed frames, oversized frames, silence, and exits can be switched per request without restarting Strata. `docs/file-providers.md` gives the frames.
- A way to cut the network mid-session: `unshare -n` around the whole stack, or an `nft`/`iptables` rule that drops the fixture's port while a listing is in flight.
- `RUST_LOG=info` for one run and `RUST_LOG=debug` for a second; grep both logs for every hostname, username, password, and token used during the sweep.
- Two windows of the same build for mount, disconnect, and provider-restart checks seen from a window that did not trigger them.
- A fixture catalog for `STRATA_INTEGRATION_CATALOG`: entries in at least two categories, one with artwork, one with a missing command requirement that has packages, one with a missing module, and one invalid entry. The bundled catalog's two entries share the `devices` category, so it shows no category chips.
- For KDE Connect, `integrations/kdeconnect/tests/mock_service.py` on the private session bus with scripted devices, or a real paired phone with file sharing on. For LocalSend, the app installed from the AUR or the upstream `.deb`, so `/usr/bin` holds a link into `/opt` or `/usr/lib`.

## Probes

- Enter each remote URI with an embedded password, `sftp://user:secret@host/`, and check the location field, breadcrumbs, window title, tab title, recent history, and both logs for `secret`.
- Watch the log for GTK criticals while a sign-in, passphrase, host-key, or File availability dialog is open and the underlying folder changes or unmounts.
- Repeat each probe once in Columns, once in List, once in Icons, and once from a second window already inside the same remote location.

### remote/file-providers/network-locations

- Cut the network while a 20k-entry share is still filling; then restore it, press F5, and compare row counts with `ls` on the server.
- On the SFTP fixture, delete the cursor file from the server. Press F5 with focus in a Ctrl+F field, in an open dialog, and in the location entry.
- Repeat in Columns with a child column open.
- Cancel a password prompt from a Columns descent two levels deep, from a sidebar DEVICES row, and from a pin; check back history and the sidebar row afterwards.
- Leave the sign-in dialog open for ten minutes, then submit; then submit a correct password while the server is stopped.
- Have the fixture's `sshd` refuse, drop the TCP connection after the banner, and hang without a banner; read the message each produces and how long each takes.
- Open `smb://host/` for a server exposing a share with `%20`, a Unicode name, and an `IPC$`-style hidden share; activate each and look for FUSE paths.
- On the SFTP fixture, create `$(printf 'caf\xe9')`, a file named `a%2Fb`, and `café`; open, rename, and delete each, then read the location field, breadcrumbs, window title, and Properties.
- Drop files onto a remote folder in the file pane and onto its DEVICES row, then search with Ctrl+F inside the remote folder with Include subfolders on and read what the UI says.
- On the SFTP fixture, build a folder holding hidden files, a symlink to a folder, and nested folders. Press Delete on it, then open Properties on it alone and in a multi-selection, watching the log for GLib-GIO criticals.
- Type `network:`, `network://`, and `network:///` in the location bar, then switch Strata's language while the Network column is open; read the heading, breadcrumbs, window title, and tab title.
- Start Strata with `gvfsd` stopped and D-Bus activation masked, then with `gvfsd` running but `gvfsd-sftp` removed; compare startup time and the two failure texts.

### remote/file-providers/external

- Register a provider that answers each request after 7.5 s, then after 8.5 s; watch badge and menu timing, the disconnect, and the 2 s restart from a menu opened at 1 s.
- Return a menu with a duplicate id, a 65-node tree, a five-level tree, an undeclared icon, and a label with an escape sequence; the item menu must still open with the other providers' sections.
- Reply with a frame of exactly 1 MiB plus one byte, then with 1 MiB minus one byte; and reply to a `query` with `actions`.
- Emit `invalidate` 50 times per second for a minute with an open submenu, then stop; the open submenu, labels, and badges must settle without the menu closing.
- Activate a leaf, kill the provider with SIGKILL before it answers, and separately make it exit 0 after writing half a reply line; compare the two dialogs.
- Register nine providers, one with a symlinked `provider.json`, one world-writable, one owned by another user, and one 300×300 icon; the log must name the rejected ids and nothing else about them.
- Reply `"feedback":"notice"` with `accepted` 1/2 and a `job`. Then reply with `"Notice"` and with `null` as the value; read which dialog or notice each produces.
- Run a `notice` action from the item menu, the background menu, a second window, and a file chooser; then close the window or tab before the reply arrives.
- Run a `notice` action from a provider whose `name` is the full 64 bytes, beside a short message.
- Set `icon` to a 256×256 PNG, and on only one of two providers; compare heading and action alignment, then switch to an RTL language.
- With a heading icon set, make the provider's `actions` reply go empty and then return while the item menu stays open.
- Start Strata with no provider registered and browse a folder in Icons for a second. Then register one while it runs; scroll, open item menus, and restart, checking when its badges and sections first appear.
- Press Refresh on Settings → Integrations while an item menu with provider actions is open in another window, and while an activation reply is still pending.
- Create a `disabled` file by hand in a running provider's directory, then press Refresh; then delete it and restart instead.
- Return two `send-to` root actions and one unplaced action; then add a `send-to-entry` action beside them; then reply with only the `send-to-entry` action carrying `children`.
- Flip one provider between a lone `send-to-entry` and a `send-to` destination on every `invalidate` while Send to… is open, with a removable drive mounted and unmounted at the same time.
- Give two providers placed destinations, one with `category` `cloud` and artwork, one with `category` `"Cloud"`, and name one `My_Phone`; read the submenu icons, labels, and their order beside a drive.
- Return a `send-to` action for a file-chooser item menu and for an item menu with an empty selection.

### remote/file-providers/integrations

- Install with `python3` absent from the trusted directories, with the providers directory a symlink, and with it mode 0775; read each error and check that nothing was written.
- Install an entry, edit one installed file, then switch the fixture catalog to a changed copy; compare the rows, the confirmation, and the files after Cancel and after Replace.
- Put a regular file, an empty directory, and a directory with an invalid `provider.json` under the providers directory with slug names; read the INSTALLED rows, then use each switch and Remove.
- Turn a switch off and on rapidly five times, and turn it off while the providers directory is read-only.
- Expand a card's requirements, then press Refresh, switch Settings pages, and come back; then install the missing package from Run in terminal without pressing Refresh.
- Use the fixture catalog's category chips with the window at one-, two-, and three-column widths, with a card expanded in each.
- Open the page in Settings opened from the file chooser, and with `XDG_CONFIG_HOME` pointing at a missing directory.
- Repeat the page in an RTL language and in the compact Settings layout.

### remote/file-providers/kde-connect

- Select 200 regular files, then 201; then a selection with one file that has a non-UTF-8 name.
- Pair two devices with the same name, and one whose name holds a newline or an emoji; read the submenu labels.
- Open the device submenu, then stop the daemon, restart it, and choose the device before and after it reappears.
- Leave the menu open for two minutes before choosing a device; separately, choose one device, then reopen the menu and choose another before the first notice fades.
- Run with `LANG=de_DE.UTF-8` while Strata's language is set to English, and with `LC_ALL=zh_HK.UTF-8`.

### remote/file-providers/localsend

- Send a folder holding a symlink and an unreadable subfolder, and a selection that mixes files from two directories.
- Choose LocalSend twice in quick succession from two windows while LocalSend is closed, then while it sits in the tray.
- Install LocalSend through a link into a directory owned by another user, and through a link inside a group-writable `/opt` subdirectory; compare the Settings requirement check with the Send to… menu.
- Quit Strata within 1.5 seconds of choosing LocalSend, and kill the provider during that wait.

## Hand-offs

- Sidebar Network place, DEVICES rows, pins, the Connect to server dialog, and the location field's parsing and history → `browser`.
- The Send to… row, removable-drive groups beside provider submenus, and copying to a drive → `operations`.
- Settings navigation to Integrations and Settings search aliases for it → `settings`.
- Copy, move, paste, rename, and delete with a remote folder as source or target → `operations`.
- Preview panel and quick preview of remote files, and thumbnails on remote entries → `preview`.
- Mounting, unmounting, and ejecting local volumes and removable media → `devices`.
- How a provider notice stacks with progress cards and replaces another visible notice in the dock → `operations`.
- Thumbnail rendering that provider badges share, and search inside a remote location → `browser`.
- How a non-UTF-8 or `%2F` URI displays, skipped-entry warnings, and directory-load log redaction → `app`.
