---
title: KDE Connect integration
status: shipped
origin: {issue: lgse/strata#1703, pr: lgse/strata#1704}
branch: null
reviewed_at: 44bfeab305cfb68993bafcf4794fe0bbf7ff1433
review: draft
code: [integrations/kdeconnect/provider.py, integrations/kdeconnect/messages.json, integrations/kdeconnect/catalog.toml, integrations/kdeconnect/LICENSE]
tests: [integrations/kdeconnect/tests]
docs: [integrations/kdeconnect/README.md]
related: [remote/file-providers/external, remote/file-providers/integrations, operations/clipboard/send-to]
---

## Summary

An opt-in bundled file provider that lists paired KDE Connect devices under Send to… ▸ KDE Connect. It sends the whole selection to the chosen device over D-Bus, with no device-picker window. For users moving from Nautilus who relied on KDE Connect's device-aware context menu. It installs from `remote/file-providers/integrations`.

## Behavior

### Devices

- With the integration installed, every paired, reachable device with the `kdeconnect_share` plugin appears by name under Send to… ▸ KDE Connect, even when there is only one. lgse/strata#1704, lgse/strata#1756
- With no eligible device, the item menu has no KDE Connect submenu, and no Send to… row when nothing else offers a destination. lgse/strata#1704
- Unreachable, unpaired, and share-disabled devices are not listed. lgse/strata#1704
- Devices are sorted by name, ignoring case. lgse/strata#1704 (unverified)
- Two devices with the same name each get " (<first 6 hex digits of the device id's SHA-256>)" after the name. lgse/strata#1704
- A device that connects or disconnects while Send to… ▸ KDE Connect is open is added or removed without closing the menu. lgse/strata#1704
- More than 63 paired, reachable devices, counted before the file-sharing check, show no KDE Connect entry rather than a truncated list. lgse/strata#1704
- The Send to… submenu shows the phone icon of the `devices` category. lgse/strata#1704

### Selection

- A selection containing a folder, a symbolic link, or another non-regular file shows no KDE Connect entry; files are never silently omitted. lgse/strata#1704
- A background (folder) menu shows no KDE Connect entry. lgse/strata#1704

### Sending

- Choosing a device submits the whole selection once through `shareUrls` to that device, pinned to the daemon's unique D-Bus owner. lgse/strata#1704
- Focusing Send to…, pressing Right twice, and pressing Return on a device sends the whole multi-file selection to it. lgse/strata#1704
- An accepted submission opens no dialog and shows the notice "Files submitted to <device>: <N>. KDE Connect handles transfer progress and results." lgse/strata#1704
- A selected file edited or replaced by another regular file after the menu opened rejects the activation with "The selected files changed. Reopen the right-click menu." and sends nothing. lgse/strata#1704
- A selected file removed, or replaced by a symbolic link or folder, rejects the activation with "The selected files are no longer available." and sends nothing. lgse/strata#1704 (unverified)
- An unreadable selected file rejects the activation with "One or more selected files cannot be read." lgse/strata#1704 (unverified)
- A device that disconnected or turned off sharing, or a daemon restart, rejects the activation and sends nothing; it is never redirected to another device. lgse/strata#1704
- When that change has not yet invalidated the open menu, the rejection reads "The selected device disconnected or file sharing was disabled." lgse/strata#1704 (unverified)
- A stale, forged, or reused menu token rejects the activation with "This device menu expired. Reopen the right-click menu." lgse/strata#1704
- A menu token expires 120 seconds after it was first issued; a menu reopened within that window on unchanged files reuses it. Any device change invalidates every token. lgse/strata#1704 (unverified)
- A D-Bus failure while rechecking devices at activation rejects it with "KDE Connect is unavailable or the device list changed.", and a deadline overrun with "KDE Connect did not respond in time." lgse/strata#1704 (unverified)
- A known D-Bus failure of `shareUrls`, such as an unknown object or access denied, rejects the activation with "The device is unavailable or file sharing was disabled." lgse/strata#1704 (unverified)
- A D-Bus error outside the known unavailable cases reports an uncertain outcome, "KDE Connect did not confirm the submission. Check your device before retrying.", and is not retried. lgse/strata#1704

### Catalog entry and messages

- The catalog entry `kdeconnect` is in the `devices` category and requires `kdeconnect-cli` and the Python module `gi`, each with pacman, apt, dnf, and zypper packages. lgse/strata#1704
- Provider messages follow `LC_ALL`, then `LC_MESSAGES`, then `LANG`, not Strata's language preference, with English as the fallback. lgse/strata#1704
- Under `LANG=hu_HU.UTF-8`, provider messages read in Hungarian, such as "A KDE Connect nem válaszolt időben." lgse/strata#1918
- `zh_HK` and `zh_MO` locales get the zh-TW messages. lgse/strata#1704

## Design

`integrations/kdeconnect/README.md` documents discovery, the token, and the failure contract.

- The device choice stays in Strata's context menu. A picker window per transfer breaks the Nautilus workflow (lgse/strata#1703).
- Rejected: a custom action running `kdeconnect-handler`, which opens a picker, and static actions with a hardcoded device, which are not live (lgse/strata#1703).
- Also rejected: removable Send to, which copies to mounted storage, and a built-in integration, which the provider protocol makes unnecessary (lgse/strata#1703).
- The integration is opt-in and adds no KDE or Python dependency to a default install (lgse/strata#1703, lgse/strata#1704).
- Each leaf binds the selection, file metadata, device id, and daemon owner into a short-lived, single-use token that activation revalidates (lgse/strata#1704).
- A successful reply confirms submission, not receipt. A lost reply is uncertain, so nothing is retried (lgse/strata#1704).
- Devices are bare-named `send-to` destinations inside Send to…, not a heading section, so labels need no "via KDE Connect" suffix (lgse/strata#1740, lgse/strata#1704).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |

## Known gaps

- Folders and symbolic links cannot be sent; folder recursion is outside the provider's contract. lgse/strata#1704
- Only D-Bus submission is confirmed, never delivery to the device. lgse/strata#1704
- KDE Connect takes paths, not file descriptors, so a file can change between the final check and the daemon opening it. lgse/strata#1704
