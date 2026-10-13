---
nodes: [remote/file-providers/network-locations, browser/navigation/location-bar, app/infrastructure]
reviewed_at: 0a086aa3bdb251842a1e8413e2a6b35970d0b409
---

# SFTP locations

Strata reaches `sftp://` locations through GIO/GVfs, the same URI-native path it
uses for every other remote scheme. This page covers what the client supports.

## Addresses

<!-- node: remote/file-providers/network-locations, SFTP -->
<!-- node: browser/navigation/location-bar, Typed paths -->

| Address | Meaning |
| --- | --- |
| `sftp://host/path` | Connect as the local user on port 22 |
| `sftp://user@host/path` | Connect as `user` |
| `sftp://user@host:2222/path` | Connect as `user` on port 2222 |

Passwords are never accepted in the address bar. A password typed there is
stripped from the URI, used once for the connection, and never saved.

## Authentication

<!-- node: remote/file-providers/network-locations, Mounting and sign-in -->
<!-- node: remote/file-providers/network-locations, SFTP -->

The SFTP backend decides which credentials it needs and asks Strata for them:

- **Password** — the backend requests a username and password. Strata shows a
  sign-in dialog with only the fields the backend asked for, so SMB's domain and
  anonymous options do not appear on an SFTP prompt.
- **SSH key** — the agent or an unencrypted key answers without any prompt.
- **Encrypted key** — `ssh-add` can unlock it in your agent before connecting.
  If GVfs asks Strata for the key's passphrase, Strata labels that field
  "Passphrase" rather than "Password". Not every GVfs/OpenSSH configuration
  sends a key-passphrase request to Strata.

Wrong credentials reopen the prompt with a message naming only the fields the
prompt is showing. Cancelling returns to the previous location without recording
history.

## Host keys

<!-- node: remote/file-providers/network-locations, SFTP -->

When GVfs asks about an unrecognized or changed host key, Strata's themed trust
dialog presents the backend's question and choices without answering for you.
The backend may not supply a fingerprint (it can report `???`); verify the
server's SSH host key through a trusted channel before choosing to continue.
If you decline, the prior location remains active and no credential retry is
offered. A changed key may indicate interception; verify it with the server
administrator before accepting.

## Failures

<!-- node: remote/file-providers/network-locations, Failures -->
<!-- node: app/infrastructure, Log privacy -->

Missing backends, name-resolution failures, refused connections, timeouts,
unreachable hosts and rejected host keys each map to their own actionable
message. Backend text that reaches a dialog has any URI user-info stripped first.

Logs never carry a host, path, username, or secret at the default level. `INFO`
records only the backend name and outcome; the location is logged at `DEBUG`,
already redacted of user-info, query and fragment.
