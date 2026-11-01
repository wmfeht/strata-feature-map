---
nodes: [remote/file-providers/network-locations, browser/navigation/location-bar, app/infrastructure]
reviewed_at: be3343a5992a2a5497b1a2ee7faa525be18e988f
---

# SFTP locations

Strata reaches `sftp://` locations through GIO/GVfs, the same URI-native path it
uses for every other remote scheme. This page covers what the client supports.

## Addresses

<!-- node: remote/file-providers/network-locations, SFTP -->
<!-- node: browser/navigation/location-bar, Typed paths -->
<!-- node: browser/navigation/location-bar, Editing -->

Press Ctrl+L, type an address, and press Enter. Or right-click **Network** in
the sidebar, choose **Connect to server…**, type the address in **Server
address**, and click **Connect**.

| Address | Meaning |
| --- | --- |
| `sftp://host/path` | Connect as the local user on port 22 |
| `sftp://user@host/path` | Connect as `user` |
| `sftp://user@host:2222/path` | Connect as `user` on port 2222 |

A password typed in the address, such as `sftp://alice:secret@host/path` or
`sftp://alice;password=secret@host/path`, is taken out of the address before
Strata connects. The location bar returns to the breadcrumbs while it connects.
The password is used for that one connection attempt and never saved. If it is
rejected, the normal sign-in dialog opens.

SCP-style addresses such as `user@host:path`, and UNC paths such as
`\\host\share` or `//host/share`, are refused with "UNC paths
(`\\host\share`) and SCP-style addresses (user@host:path) aren't supported.
Use a URI instead, such as smb://host/share, sftp://host/path, ftp://host/path,
or dav://host/path."

A scheme Strata does not handle, such as `ssh://host` or `scp://host`, is
refused with "The ssh:// scheme isn't supported. Use an absolute local path or
one of: smb://, sftp://, ftp://, ftps://, dav://, davs://, or recent:///."
Schemes match regardless of case, so `SFTP://host/path` works. A refused address
opens an **Unable to open location** dialog, and the location bar returns to
the current location. A folder load that ends while the location entry is open
and focused, as in a new tab, leaves the entry open with its text.

### Connect to server

<!-- node: remote/file-providers/network-locations -->

**Connect to server…** sits in the **Network** sidebar row's context menu, so
it opens only from a browser window. The **Connect to server** dialog, "Connect
to a share or remote server", has a focused **Server address** field, a **Pin
to sidebar** checkbox, and **Cancel** and **Connect**. Enter in the field
presses **Connect**.

While it connects, the field, the checkbox, and **Connect** are disabled, and a
"Connecting…" spinner runs through validation, mounting, and sign-in. A sign-in
prompt opens above the dialog; cancelling the sign-in prompt
returns the dialog to its editable state with no error. An address that cannot
be opened, such as `nonsense`, shows its error inline under the field, which is
marked as an error; editing the address clears it. A connection failure, such
as `sftp://nonexistent.invalid/share`, a refused connection, a timeout, or a
missing backend, also shows inline, after at least 1 s, and no second dialog
opens. **Cancel**, the close button, or Escape while connecting closes the
dialog and cancels the pending mount, so nothing opens afterwards. A click
outside the dialog does not close it while it connects or while the address is
not empty.

Without **Pin to sidebar**, a reachable address opens in the active pane once,
as typing it in the location bar does. With it ticked, the dialog closes once
the location opens and a row appears under **PINNED**, labelled with the
location's name; **Unpin** removes it. A failed connection adds no pin, and an
address already pinned adds no second one. Unmounting a pinned location keeps
its row, and clicking the row connects again.

### Browsing an SFTP location

<!-- node: remote/file-providers/network-locations, Mounting and sign-in -->
<!-- node: remote/file-providers/network-locations, Browsing -->
<!-- node: app/infrastructure, URI display -->
<!-- node: app/infrastructure, Listing -->

Opening an `sftp://` address mounts it first if needed, then opens it. Entries
keep their `sftp://` address; Strata never shows the `/run/user/$UID/gvfs/…`
FUSE path.

The location field and Properties show non-ASCII characters decoded, such as
`sftp://host/café`, when the whole path is valid UTF-8 and contains no `%2F`.
Spaces and other reserved characters stay percent-encoded, such as
`sftp://host/My%20Share`. Otherwise the whole path shows percent-encoded, such
as `sftp://host/share/%FF%20name`. Column headings, peek headings, and window
titles show percent-decoded names. Files whose names are not valid UTF-8 are
still listed. An entry whose address Strata cannot convert is left out of the
listing.

A large folder fills in progressively. Loading finishes only after every row
read so far is shown. A load stops after 100,000 entries or 10 seconds. A
warning icon beside the folder's heading then marks a partial listing: "This
directory has more entries than could be loaded; showing a partial listing."
A folder you open by typing a non-ASCII address, such as `sftp://host/café x`,
still refreshes when an entry is created or deleted in it. If you leave a folder before it finishes loading, its remaining
rows never appear in the folder you moved to or in columns that were closed.
Breadcrumbs, history, column descent, and hover peek work as they do on local
folders.

With **Settings → General → PERFORMANCE → Watch network folders** on, the
default, open SFTP folders are checked for changes made on the server, and
re-listed when a check finds one. Checks start every 3 s in a focused window
and every 15 s in a window shown without focus. In power-saver mode, focused
windows check every 12 s and unfocused windows stop checking. After 20
unchanged checks in a row the interval doubles, and after 40 it is four times
as long. Regaining focus checks at once. With the switch off, changes made on
the server show only after F5. You can copy a remote file, drag it out, or open
it in its default application.

Ejecting or unmounting the SFTP mount from its **DEVICES** row while you browse
inside it returns the browser to Home.

## Authentication

<!-- node: remote/file-providers/network-locations, Mounting and sign-in -->
<!-- node: remote/file-providers/network-locations, SFTP -->

The SFTP backend decides which credentials it needs and asks Strata for them:

- **Password** — the backend requests a username and password. Strata shows
  **Authentication required** with only the fields the backend asked for, and a
  **Connect** button. Each field's accessible name is its visible label, such
  as "Username" or "Password". SMB's domain and anonymous options do not appear on an
  SFTP prompt. If the backend can save passwords, the dialog also offers
  **Password storage**: **Don't remember** (the default), **Until logout**, or
  **Forever**. Strata itself stores nothing; the backend and your keyring keep
  the password.
- **SSH key** — the agent or an unencrypted key answers without any prompt.
- **Encrypted key** — `ssh-add` can unlock it in your agent before connecting.
  If GVfs asks Strata for the key's passphrase, the dialog is titled
  **Passphrase required** and its field is labelled **Passphrase**. Not every
  GVfs/OpenSSH configuration sends a key-passphrase request to Strata.

Wrong credentials reopen the dialog with "Those credentials weren’t accepted.
Check … and try again." The message names only the fields the dialog shows,
such as "Check username, password and try again." or, on a key prompt, "Check
passphrase and try again." If the prompt has no fields to name, it says "That
attempt wasn’t accepted. Try again." **Cancel** or
Escape returns to the previous location with no error dialog and no history
entry.

## Host keys

<!-- node: remote/file-providers/network-locations, SFTP -->

An unrecognized or changed host key opens **Verify server identity**. It shows
the backend's question and every choice the backend offers, and Strata never
answers it for you. The dialog warns: "Only continue after verifying the SSH
host key through a trusted source." and "If the server did not provide a
fingerprint, verify it outside Strata before continuing."

The backend may not supply a fingerprint (it can report `???`); verify the
server's SSH host key through a trusted channel before choosing to continue.
The rejecting choice, such as Cancel, comes first and has focus. Declining with
that choice, Escape, or the close button returns to the previous location with
no sign-in dialog and no error.

A changed key may indicate interception; verify it with the server
administrator before accepting. Depending on your GVfs and OpenSSH setup, a
changed key can instead fail at once with the host-key message under
[Failures](#failures). Verify the new fingerprint before you reconnect.

## Failures

<!-- node: remote/file-providers/network-locations, Failures -->
<!-- node: remote/file-providers/network-locations, SFTP -->
<!-- node: remote/file-providers/network-locations, Browsing -->
<!-- node: app/infrastructure, Listing -->
<!-- node: app/infrastructure, Log privacy -->

Each failure has its own message. If the sftp backend isn't installed, opening
an `sftp://` address shows **Unable to open location** with: "The sftp://
backend isn't installed. Install your distribution's GVfs sftp backend,
commonly packaged as gvfs or gvfs-backends, then try again."

A failure while connecting shows it in an **Unable to connect** dialog:

| Failure | Message |
| --- | --- |
| Host not found | "That host couldn’t be found. Check the address and DNS settings." |
| Connection refused | "The host refused the connection. Check the service and port." |
| Timeout | "The connection timed out. Check the host and firewall." |
| Host or network unreachable | "That host is unreachable. Check your network connection." |
| Host key rejected | "The remote computer’s host key could not be verified. Confirm its fingerprint with the server administrator before trying again." |

**Connect to server…** shows any of these messages under its address field
instead of the dialog; only a rejected sign-in reopens the sign-in prompt. A
host-key failure never reopens the sign-in dialog. When a connection or
folder load fails with other backend text, or the backend asks about a host key,
any address in that text is shown with its user info, query, and fragment
removed.

At the default log level, connecting to and listing a remote location never
logs its host, path, username, or password. A mount logs only the backend name,
the mount strategy, and the outcome, with the error domain and code on failure.
A folder load logs a request id, the backend name, entry counts, and elapsed
times, plus the error domain and code or the reason when it fails or stops
early. An entry left out of a listing logs a warning with only the request id
and backend name. Run with `RUST_LOG=strata=debug` to log locations, including
the folder and name of a left-out entry. At every log level, logged URIs omit
user info, authentication parameters, query, and fragment. That covers opening
an unavailable target, opening a location in a new tab or window, and
recording or removing a Recent entry, whose error text is sanitized the same
way.

At startup Strata checks that GVfs (`gvfsd`) answers within 2 seconds. If it
does not, Strata prints "GVFS is unresponsive; using local filesystem and
volume support for this session." to standard error and the window still opens,
with local file and volume support only. `sftp://` and other remote addresses
cannot open until you restart Strata with a working GVfs session.
