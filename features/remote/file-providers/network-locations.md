---
title: Network locations (SMB, SFTP)
status: shipped
origin: {issue: lgse/strata#20, pr: lgse/strata#31}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: reviewed
code: [src/adapters/gio_location.rs, src/app/browser/remote.rs]
tests: [src/adapters/gio_location/tests.rs, src/app/browser/remote/tests.rs, scripts/sftp-fixture.sh]
docs: [docs/remote-sftp.md]
related: [browser/navigation/location-bar, devices/volumes, browser/sidebar/pins]
---

## Summary

Browsing `smb://`, `sftp://`, and other GIO/GVfs network locations as URI-native folders. Covers mounting on demand, the sign-in and SSH host-key dialogs, and connection failure messages. It also covers the sidebar's Network place and SMB share rows, SMB share lists, and progressive remote loading. Typed-address parsing belongs to `browser/navigation/location-bar`.

## Behavior

### Mounting and sign-in

- Opening an unmounted remote location mounts it, then opens it; descending into an unmounted share from a column does the same. lgse/strata#31
- When the backend asks for credentials, an "Authentication required" dialog shows only the fields the backend requested. lgse/strata#233
- An SMB sign-in can show Username, Domain, Password, a Registered user/Anonymous choice, and Password storage (Don't remember, Until logout, Forever). lgse/strata#31, lgse/strata#233 (unverified)
- Choosing Anonymous disables the credential and Password storage fields. lgse/strata#31 (unverified)
- Wrong credentials reopen the dialog with "Those credentials weren’t accepted. Check … and try again.", naming only the fields it shows. lgse/strata#233
- Cancel or Escape on the sign-in dialog returns to the previous location with no error dialog and no history entry. lgse/strata#31, lgse/strata#233

### SFTP

- `sftp://host/path`, `sftp://user@host/path`, and `sftp://user@host:2222/path` connect as the local user, as `user`, and on port 2222. lgse/strata#233
- With the key in an SSH agent, or an unencrypted key, an SFTP location opens with no prompt. lgse/strata#233
- When GVfs asks Strata for a key passphrase, the dialog is titled "Passphrase required" and its field is labelled "Passphrase". lgse/strata#233
- An unknown or changed SFTP host key opens a "Verify server identity" dialog with the backend's question and every backend choice; Strata never answers it. lgse/strata#233
- The host-key dialog warns that a missing fingerprint must be verified outside Strata. lgse/strata#233
- The host-key dialog opens with the rejecting choice, such as Cancel, focused. lgse/strata#233 (unverified)
- Declining the host key by its rejecting choice, Escape, or close returns to the previous location with no sign-in dialog and no error. lgse/strata#233
- A connection that fails on host-key verification shows "The remote computer’s host key could not be verified…" and does not reopen sign-in. lgse/strata#233
- Trust questions from other schemes and from devices use GTK's native question dialog. lgse/strata#353, lgse/strata#233

### Failures

- An `smb://` location without its GVfs backend fails with a message naming common packages `gvfs-smb` or `gvfs-backends`. lgse/strata#31, lgse/strata#233
- An unresolvable host, refused connection, timeout, or unreachable host each shows its own message, such as "That host couldn’t be found. Check the address and DNS settings." lgse/strata#233
- Backend error text shown in a dialog has URI user info, query, and fragment removed. lgse/strata#233
- At the default log level, a mount logs only the backend name and outcome; the location appears only at DEBUG, without user info. lgse/strata#233

### Sidebar

- The sidebar's Network place opens `network:///`, which lists the hosts and shares GVfs discovers. lgse/strata#31, lgse/strata#62
- A mounted `smb://` share appears under DEVICES with a network icon instead of a drive icon, and clicking it opens the share. lgse/strata#31, lgse/strata#62
- Right-clicking a mounted SMB share's DEVICES row offers Properties and Disconnect. lgse/strata#31, lgse/strata#296 (unverified)
- Disconnect unmounts the share; a failure other than a cancel shows an "Unable to disconnect" dialog. lgse/strata#31 (unverified)

### Browsing

- Entries of a mounted GVfs location keep their `smb://`-style URI and never show the `/run/user/$UID/gvfs/…` FUSE path. lgse/strata#31
- At `smb://host/`, activating a share by mouse or keyboard in Columns, List, or Icons mounts it if needed and opens its contents. lgse/strata#990
- Column headings, peek headings, and window titles show percent-decoded remote names, such as "My Share" for `My%20Share`. lgse/strata#740
- Ejecting or unmounting a non-SMB remote mount, such as SFTP, from its DEVICES row while browsing inside it returns the browser to Home. lgse/strata#352, lgse/strata#296
- A large remote folder fills progressively without lost or duplicated rows, and loading finishes only after every queued row is shown. lgse/strata#661
- Leaving a remote folder before it finishes loading keeps its queued rows out of the new location and of removed columns. lgse/strata#661
- When `gvfsd` does not answer a 2-second startup probe, the window still opens, using local file and volume support for that session. lgse/strata#56

## Design

[docs/remote-sftp.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/remote-sftp.md) carries the SFTP address forms, authentication cases, the disposable OpenSSH fixture, and the manual test matrix.

- Remote locations stay URI-native. A GVfs backend also exposes a FUSE path, so a `gio::File` yields a native path only when GIO reports it native (lgse/strata#5, lgse/strata#31).
- Access is protocol-agnostic through GIO/GVfs. Only SMB and SFTP are verified end to end; FTP, FTPS, WebDAV, and DAVS are accepted untested (lgse/strata#20, lgse/strata#64).
- A location reporting "not mounted" uses `mount_enclosing_volume`; a GVfs mountable entry uses `mount_mountable`. The two are not interchangeable (lgse/strata#31).
- Strata stores no secrets. Credentials go into the mount operation, and Until logout or Forever hands saving to the backend and keyring (lgse/strata#20, lgse/strata#145).
- Strata suppresses GtkMountOperation's password dialog and shows its own. The safe `gio` bindings cannot marshal `ask-question` choices, so trust questions first used GTK's native dialog (lgse/strata#353).
- SFTP host-key questions moved to a Strata dialog at the owner's request. It keeps every backend choice and index; other schemes keep the native dialog (lgse/strata#233).
- Some GVfs SMB versions report rejected credentials as a generic failure, so failure messages are matched for authentication text. Host-key failures are excluded, so they never reopen sign-in (lgse/strata#31, lgse/strata#233).
- `gvfsd-smb-browse` lists shares as shortcut entries whose destination is `standard::target-uri`. The first directory batch requests that attribute, and shortcut and mountable entries open as folders (lgse/strata#960, lgse/strata#990).
- Remote loads publish their first batch at once. Later batches queue per column and flush every 50 ms or at 2,048 entries, at most 512 rows per drain; finish and failure wait for the queue (lgse/strata#274, lgse/strata#661).
- The `gvfsd` probe runs in a subprocess before GTK starts. A timeout restarts with `GIO_USE_VFS=local` and `GIO_USE_VOLUME_MONITOR=unix`; a healthy result is cached per `gvfsd` process set (lgse/strata#52, lgse/strata#56, lgse/strata#274).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-29 | lgse/strata#233 | feat | Completed SFTP: scheme-specific sign-in fields, a Strata host-key dialog, actionable failures, sanitized logs, and a test fixture. |
| 2026-09-14 | lgse/strata#990 | fix | Opened SMB share-list shortcuts as folders, mounting the share, in every view. |
| 2026-09-10 | lgse/strata#740 | fix | Showed percent-decoded names for remote locations. |
| 2026-09-09 | lgse/strata#661 | refactor | Moved remote batch queues, deferred terminal events, and the flush timer into their own module. |
| 2026-09-05 | lgse/strata#353 | feat | Switched to GtkMountOperation so SFTP host-key questions get a trust dialog instead of failing. |
| 2026-09-05 | lgse/strata#352 | fix | Compared URI locations hierarchically so ejecting a browsed remote mount returns Home. |
| 2026-08-31 | lgse/strata#56 | fix | Fell back to local GIO support when `gvfsd` is unresponsive, instead of hanging at startup. |
| 2026-08-31 | lgse/strata#31 | feat | Added URI-native SMB browsing with on-demand mounting, sign-in, and missing-backend guidance. |

## Known gaps

- FTP, FTPS, WebDAV, and DAVS are unverified, with no plaintext-transport warning or explicit certificate trust flow. lgse/strata#64
- There are no saved connections, Connections sidebar section, or Add connection form. lgse/strata#65
- Network discovery failures are generic, non-SMB network mounts appear as drives, and a vanished mount sends the browser Home instead of a retryable column. lgse/strata#62
- SMB rows offer Disconnect even when the mount reports it cannot be unmounted. lgse/strata#62
- Mutating actions on remote locations are not gated by the backend's capabilities. lgse/strata#66
- Recursive search cannot search a remote share and falls back to Home. lgse/strata#87
- Remote entries whose names percent-encode invalid UTF-8 are dropped from listings; lgse/strata#1533 fixes this after `reviewed_at`. lgse/strata#1424, lgse/strata#1533
