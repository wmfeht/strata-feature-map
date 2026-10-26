---
title: Connect to server dialog
status: shipped
origin: {issue: lgse/strata#1725, pr: lgse/strata#1726}
branch: null
reviewed_at: be3343a5992a2a5497b1a2ee7faa525be18e988f
review: draft
code: [src/ui/window/network_location.rs, src/ui/window/network_location/**]
tests: [src/ui/window/network_location/tests.rs]
related: [remote/file-providers/network-locations, browser/navigation/location-bar, browser/sidebar/pins]
---

## Summary

A dialog opened from the sidebar Network row's menu that connects to a share or remote server by address, and optionally pins it to the sidebar. It gives a discoverable route to what typing an `smb://` or `sftp://` URI in the location bar already did.

## Behavior

### Opening

- Right-clicking the Network sidebar row shows "Connect to server…", with a plus icon, above Unpin and Properties. lgse/strata#1726
- The file chooser's sidebar has no Network row, so the dialog opens only from a browser window. lgse/strata#1726 (unverified)
- Choosing it opens a dialog titled "Connect to server", subtitled "Connect to a share or remote server". lgse/strata#1726
- The dialog has a focused "Server address" field, a "Pin to sidebar" checkbox, and Cancel and Connect buttons. lgse/strata#1726
- The address field's placeholder is `smb://server/share` in every language. lgse/strata#1726
- Enter in the address field presses Connect. lgse/strata#1726 (unverified)

### Connecting

- Connect on an address that cannot be opened, such as `nonsense`, shows an inline error under the address. lgse/strata#1726
- That error marks the field as an error and keeps the dialog open. lgse/strata#1726
- Editing the address clears that error. lgse/strata#1726
- While connecting, the address field, the checkbox, and Connect are disabled, and a spinner labelled "Connecting…" runs through validation, mounting, and sign-in. lgse/strata#1726
- A sign-in prompt raised while connecting stacks above the dialog. lgse/strata#1726
- An unknown host such as `sftp://nonexistent.invalid/share`, a refused connection, a timeout, or a missing GVfs backend shows its message inline under the address. No second error dialog opens. lgse/strata#1726
- A connection failure that arrives less than 1 s after Connect keeps the dialog busy until 1 s has passed, then shows the error. lgse/strata#1726
- An address that cannot be opened, such as `nonsense`, shows its error without that wait. lgse/strata#1726 (unverified)
- Cancelling the sign-in prompt returns the dialog to its editable state with no error message. lgse/strata#1726
- Cancel, the close button, or Escape while connecting closes the dialog and cancels the pending validation or mount; nothing opens afterwards. lgse/strata#1726
- A click outside the dialog does not close it while it is connecting or while the address is not empty. lgse/strata#1726 (unverified)

### Opening and pinning

- Without "Pin to sidebar", a reachable address connects once and opens in the active pane, as typing it in the location bar does. lgse/strata#1726
- With "Pin to sidebar" ticked, the dialog closes once the location opens and a row appears under PINNED; Unpin on that row removes it. lgse/strata#1726
- A failed connection or a rejected address adds no pin. lgse/strata#1726
- The pin is stored in the form the bookmarks file reloads, so `smb://host/share` is saved as `smb://host/share/`. lgse/strata#1726
- The pin is labelled with the location's display name, or its display path when the name is empty. lgse/strata#1726 (unverified)
- An address that is already pinned, or that is Home or a standard folder, closes the dialog without adding a pin. lgse/strata#1726 (unverified)
- Disconnecting or unmounting a pinned share keeps its row under PINNED; clicking the row remounts the share. lgse/strata#1726
- After a successful connect, keyboard focus returns to the active browser pane. lgse/strata#1726 (unverified)

## Design

- The pin is written only after the location opens, so a failed mount or rejected address leaves no bookmark. This replaced a tracker that watched browser events for the outcome (lgse/strata#1725, lgse/strata#1726).
- Pins of shares are never removed when the share unmounts or disconnects. The server may be rebooting, and the bookmarks file is shared with Nautilus, so an automatic removal would vanish everywhere unexplained. This reversed lgse/strata#1725's proposal to unpin on Disconnect (lgse/strata#1726).
- One address field was chosen over a server, share, user, and protocol form, and a Network menu item over a header button (lgse/strata#1725).
- Failures are routed to the waiting dialog instead of the location bar's "Unable to open location" dialog, so the user can correct the address in place (lgse/strata#1726).
- Each attempt builds a fresh spinner, because GTK 4.24 leaves a restarted hidden spinner blank. The 1 s minimum covers GTK's spinner fade-in, without which a fast failure looked as if Connect did nothing (lgse/strata#1726).
- "Connect to server…" and "Pin to sidebar" say that the dialog connects and pins only on request, matching the Pinned and Unpin wording (lgse/strata#1726).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |

## Known gaps

None known.
