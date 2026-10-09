---
title: Remote sweep
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
tools: [docs/file-providers.md, docs/remote-sftp.md, scripts/sftp-fixture.sh]
---

## Scope

Everything that reaches Strata from somewhere other than a local disk: network locations over GIO/GVfs (`smb://`, `sftp://`, `network:///`) with on-demand mounting, the sign-in, passphrase, and host-key dialogs, failure messages, log redaction, SMB share lists, progressive remote loading, and the `gvfsd` startup probe; and external file providers, from registration and process lifecycle to badges, menu sections, activation dialogs, and invalidation. `remote/file-providers` itself has no Behavior; its two children carry every check.

Left to other sweeps: sidebar rows and location-field parsing and history, copy and move semantics once a remote folder is a source or target, previews and thumbnails of remote files, and mounting, unmounting, and ejecting local devices.

## Setup

- `GIO_USE_VFS` must not be `local` and `GIO_USE_VOLUME_MONITOR` must be unset for every probe here. The E2E environment sets `GIO_USE_VFS=local`, which disables GVfs; drop that variable, keep the private D-Bus session, and start `gvfsd` on it before launching Strata.
- `scripts/sftp-fixture.sh --port 2222` for a working `sftp://` location; `--keep` and a second run on the same port for a changed host key; `STRATA_SFTP_PASSWORD` for password prompts. An isolated `known_hosts` and a non-loopback relay for trust questions, per `docs/remote-sftp.md`.
- An `smb://` URI that does not resolve (`smb://no-such-host.invalid/share`), one that refuses (`smb://127.0.0.1:1/share`), and, when Samba is installed, a local share with a guest-readable folder, a password-protected folder, and a 20k-entry folder.
- A fake provider under `$XDG_CONFIG_HOME/strata/providers/<id>/provider.json`: a Python script that answers from a scenario file so delays, malformed frames, oversized frames, silence, and exits can be switched per request without restarting Strata. `docs/file-providers.md` gives the frames.
- A way to cut the network mid-session: `unshare -n` around the whole stack, or an `nft`/`iptables` rule that drops the fixture's port while a listing is in flight.
- `RUST_LOG=info` for one run and `RUST_LOG=debug` for a second; grep both logs for every hostname, username, password, and token used during the sweep.
- Two windows of the same build for mount, disconnect, and provider-restart checks seen from a window that did not trigger them.

## Probes

- Enter each remote URI with an embedded password, `sftp://user:secret@host/`, and check the location field, breadcrumbs, window title, tab title, recent history, and both logs for `secret`.
- Watch the log for GTK criticals while a sign-in, passphrase, host-key, or File availability dialog is open and the underlying folder changes or unmounts.
- Repeat each probe once in Columns, once in List, once in Icons, and once from a second window already inside the same remote location.

### remote/file-providers/network-locations

- Cut the network while a 20k-entry share is still filling; then restore it, press F5, and compare row counts with `ls` on the server.
- Cancel a password prompt from a Columns descent two levels deep, from a sidebar DEVICES row, and from a pin; check back history and the sidebar row afterwards.
- Leave the sign-in dialog open for ten minutes, then submit; then submit a correct password while the server is stopped.
- Have the fixture's `sshd` refuse, drop the TCP connection after the banner, and hang without a banner; read the message each produces and how long each takes.
- Open `smb://host/` for a server exposing a share with `%20`, a Unicode name, and an `IPC$`-style hidden share; activate each and look for FUSE paths.
- Drop files onto a remote folder in the file pane and onto its DEVICES row, then search with Ctrl+F inside the remote folder with Include subfolders on and read what the UI says.
- Start Strata with `gvfsd` stopped and D-Bus activation masked, then with `gvfsd` running but `gvfsd-sftp` removed; compare startup time and the two failure texts.

### remote/file-providers/external

- Register a provider that answers each request after 7.5 s, then after 8.5 s; watch badge and menu timing, the disconnect, and the 2 s restart from a menu opened at 1 s.
- Return a menu with a duplicate id, a 65-node tree, a five-level tree, an undeclared icon, and a label with an escape sequence; the item menu must still open with the other providers' sections.
- Reply with a frame of exactly 1 MiB plus one byte, then with 1 MiB minus one byte; and reply to a `query` with `actions`.
- Emit `invalidate` 50 times per second for a minute with an open submenu, then stop; the open submenu, labels, and badges must settle without the menu closing.
- Activate a leaf, kill the provider with SIGKILL before it answers, and separately make it exit 0 after writing half a reply line; compare the two dialogs.
- Register nine providers, one with a symlinked `provider.json`, one world-writable, one owned by another user, and one 300×300 icon; the log must name the rejected ids and nothing else about them.

## Hand-offs

- Sidebar Network place, DEVICES rows, pins, and the location field's parsing and history → `browser`.
- Copy, move, paste, rename, and delete with a remote folder as source or target → `operations`.
- Preview panel and quick preview of remote files, and thumbnails on remote entries → `preview`.
- Mounting, unmounting, and ejecting local volumes and removable media → `devices`.
- Thumbnail rendering that provider badges share, and search inside a remote location → `browser`.
