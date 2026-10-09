---
title: Encrypted volumes
status: shipped
origin: {issue: null, pr: lgse/strata#935}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [src/ui/window/volume_password.rs]
tests: [src/ui/window/volume_password/tests.rs]
related: [devices/volumes/udiskie-unlock]
---

## Summary

Unlocking and locking LUKS volumes from their Devices rows with Strata's themed passphrase prompt, and forgetting a saved passphrase when locking. For users who keep encrypted USB drives or partitions.

## Behavior

### Detection

- A volume counts as encrypted when GVfs marks it with a padlock emblem, its icon name contains "encrypted", its drive starts with a password, or udev reports a crypto device. lgse/strata#935 (unverified)
- An encrypted device stays listed in Devices while locked, including a password-start drive with no listed volume. lgse/strata#935
- A locked encrypted row shows a lock button and an Unlock menu entry; an unlocked one shows an open-lock button and Lock. lgse/strata#935
- Rows for non-encrypted devices have no lock button. lgse/strata#935

### Unlocking

- Clicking a locked row, its lock button, or Unlock opens the themed "Authenticate to access this volume or location" prompt with a Passphrase field and a password-storage choice. lgse/strata#493, lgse/strata#935
- Cancel in the prompt closes it with no error and keeps the current folder. lgse/strata#493
- A rejected passphrase reopens the prompt with a retry message instead of an error dialog. lgse/strata#493
- A correct passphrase unlocks and mounts the volume, then navigates into it. lgse/strata#493
- 350 ms after the unlock starts, an "Unlocking volume" overlay appears; Hide, Close, or Escape dismiss it and unlocking continues. lgse/strata#935 (unverified)
- If that overlay was hidden, completion does not navigate away from the current folder. lgse/strata#935
- If the pane is already inside the volume's mount when unlock completes, the folder reloads without F5. lgse/strata#935
- After unlock, Strata opens only the volume matching the unlocked device's GIO object or LUKS UUID, not another encrypted partition on the same drive. lgse/strata#935

### Locking

- Lock on a mounted encrypted volume flushes and unmounts it, then stops its password drive, under a "Locking volume" overlay. lgse/strata#935, lgse/strata#1193
- When the volume's passphrase is saved, Lock first asks "Forget saved password?"; Cancel or Escape leaves both the password and the mount. lgse/strata#935
- "Forget and lock" deletes the saved passphrase, then locks. lgse/strata#935
- If the keyring needs a confirmation Strata cannot display, Lock stops with "Couldn't forget the saved password" and asks the user to remove it in the password manager. lgse/strata#935
- Lock on an unlocked but unmounted volume with no stop operation shows "Unable to lock device" and keeps the saved passphrase. lgse/strata#935
- A successful Lock never shows "Safe to remove". lgse/strata#1193

## Design

- Mounts Strata starts present Strata's own prompt rather than GTK's default dialog or another file manager's (lgse/strata#302, lgse/strata#537). Desktop automounters may still prompt on their own; `devices/volumes/udiskie-unlock` is the opt-in handoff.
- Successor matching uses exact GIO object identity and the LUKS UUID. Accepting any encrypted partition on the same physical drive could open the wrong volume (lgse/strata#935).
- An unlocked volume exposes its filesystem UUID, not the LUKS UUID that keys the saved passphrase. Strata recovers the LUKS UUID from the dm UUID, a `luks-<uuid>` device name, or udev data (lgse/strata#935).
- Saved passphrases are searched in the Secret Service under both `gvfs-luks-uuid` and `gvfs.crypto.luks.uuid`, because GVfs and GNOME Disks use different attribute names (lgse/strata#935).
- Unsupported locks fail before any saved passphrase is deleted, so an error never costs the user the passphrase (lgse/strata#935).
- Mounted GVfs crypto volumes lock through unmount; the release path supplies the flush and pending row (lgse/strata#935, lgse/strata#1193).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-14 | lgse/strata#935 | fix | Kept encrypted devices listed, added Lock/Unlock controls and saved-password confirmation, and matched unlocked volumes by identity. |

## Known gaps

- Deleting a saved passphrase whose password manager requires its own deletion prompt is unsupported; the user must remove it manually. lgse/strata#935
