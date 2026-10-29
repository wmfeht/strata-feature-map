---
title: LocalSend integration
status: shipped
origin: {issue: lgse/strata#1754, pr: lgse/strata#1756}
branch: null
reviewed_at: 44bfeab305cfb68993bafcf4794fe0bbf7ff1433
review: reviewed
code: [integrations/localsend/provider.py, integrations/localsend/messages.json, integrations/localsend/catalog.toml, integrations/localsend/LICENSE]
tests: [integrations/localsend/tests/test_provider.py]
docs: [integrations/localsend/README.md]
related: [remote/file-providers/external, remote/file-providers/integrations, operations/clipboard/send-to]
---

## Summary

An opt-in bundled file provider whose single Send to… ▸ LocalSend entry hands the selected files and folders to the installed LocalSend app. LocalSend then picks the device and sends. For users who would otherwise re-pick the same files in LocalSend's own dialog. It installs from `remote/file-providers/integrations`.

## Behavior

### Menu

- With the integration installed and LocalSend found, an item menu on files, folders, or both shows one Send to… row, LocalSend. It has no submenu arrow and shows the `devices` phone icon. lgse/strata#1756
- A selection containing a symbolic link, a missing path, or an item that is neither a regular file nor a folder shows no LocalSend entry. lgse/strata#1756 (unverified)
- A background (folder) menu shows no LocalSend entry. lgse/strata#1756 (unverified)
- Without LocalSend in a trusted location, no LocalSend entry appears. lgse/strata#1756 (unverified)
- The label "LocalSend" is not translated. lgse/strata#1756 (unverified)

### Hand-over

- Choosing LocalSend runs it once with the literal selected paths as arguments and shows no dialog and no notice; LocalSend opens its Send tab with those items. lgse/strata#1756
- With LocalSend already running, including in the tray, the running instance takes the items over. lgse/strata#1756
- LocalSend started from the menu keeps running after Strata quits. lgse/strata#1756
- LocalSend adds the items to anything already selected in its Send tab. lgse/strata#1756
- LocalSend exiting with a non-zero status within 1.5 seconds rejects the activation with "LocalSend closed before it opened the selection." lgse/strata#1756 (unverified)
- A launch failure rejects the activation with "LocalSend could not be started." lgse/strata#1756 (unverified)
- LocalSend removed while the menu is open rejects the activation with "LocalSend is not installed in a system directory." lgse/strata#1756 (unverified)
- An item edited, or replaced by another regular file or folder, after the menu opened rejects the activation with "The selected items changed. Reopen the right-click menu." lgse/strata#1756
- An item removed, or replaced by a symbolic link, after the menu opened rejects the activation with "The selected items are no longer available." lgse/strata#1756 (unverified)
- An unreadable item, or a folder that cannot be traversed, rejects the activation with "One or more selected items cannot be read." lgse/strata#1756 (unverified)
- A stale, forged, or reused menu token, or one older than 120 seconds, rejects the activation with "This LocalSend menu expired. Reopen the right-click menu." lgse/strata#1756
- The token is consumed before the launch, so a lost reply cannot open the selection twice. lgse/strata#1756

### Executable lookup

- The executable is looked up as `localsend`, then `localsend_app`, in Strata's trusted search directories. lgse/strata#1756
- A link whose target lies under a trusted root runs through the link. lgse/strata#1756
- A link to a target outside the trusted roots runs the target itself, never the link. lgse/strata#1756
- That target runs only when root owns it and every directory above it, and none is group- or world-writable. lgse/strata#1756
- A target with another owner or a group- or world-writable directory above it is refused. lgse/strata#1756

### Catalog entry and messages

- The catalog entry `localsend` is in the `devices` category, runs on python3 with only the standard library, and requires `localsend` or `localsend_app` with no package install command. lgse/strata#1756
- Provider messages follow `LC_ALL`, then `LC_MESSAGES`, then `LANG`, with English as the fallback. lgse/strata#1756 (unverified)

## Design

`integrations/localsend/README.md` documents the lookup, the token, and the hand-over contract.

- Strata hands the selection to the LocalSend app, which handles device discovery, PINs, acceptance, progress, and errors (lgse/strata#1754).
- Rejected: speaking LocalSend protocol v2 from the provider. Strata would announce itself as a peer that cannot receive, and the transfer would outlast the 8-second activation limit and stop when Strata quits (lgse/strata#1754).
- Rejected: `localsend-cli`, which is interactive only and binds LocalSend's port, conflicting with the running app (lgse/strata#1754). lgse/strata#1413 tried it in a terminal and closed unmerged.
- The selection is bound to a single-use token, and LocalSend starts in its own session (lgse/strata#1754).
- The provider runs the resolved target, not the `/usr/bin` link, because the relaxed lookup leaves the link unchecked (lgse/strata#1756).
- LocalSend picks the device, so the provider is a single `send-to-entry` leaf rather than a submenu (lgse/strata#1756).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-18 | lgse/strata#1756 | feat | Added the LocalSend integration, whose single Send to… entry hands the selection to the LocalSend app. |

## Known gaps

- Flatpak, Snap, and AppImage installs of LocalSend are not found, because their launchers sit outside the trusted directories. Flatpak would also need document-portal forwarding. lgse/strata#1756
- Acceptance means LocalSend received the paths, not that anything was sent; LocalSend reads the files when the device is chosen. lgse/strata#1756
