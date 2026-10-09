---
title: Drive format, label, and properties
status: shipped
origin: {issue: lgse/strata#1293, pr: lgse/strata#1331}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: reviewed
code: [src/ui/window/drive_dialogs.rs, src/ui/window/drive_dialogs/**, src/ui/window/drive_ops.rs, src/ui/window/device_labels.rs, src/ui/missing_tools.rs, src/services/package_manager.rs]
tests: [src/ui/window/drive_dialogs/tests.rs, src/ui/window/drive_ops/tests.rs, src/ui/window/device_labels/tests.rs, src/ui/missing_tools/tests.rs, src/services/package_manager/tests.rs]
related: [browser/sidebar, operations/progress]
---

## Summary

Dialogs opened from a device row's menu: Properties for any listed storage, Set label… for a Strata-only display name, and Format… for removable drives. Formatting asks twice and names the exact target before erasing anything.

## Behavior

### Properties

- Properties opens from the menu of a volume or a mount-only entry, including fixed storage. lgse/strata#1393
- It lists System name, Strata label, Device, Filesystem, and Status; a mounted volume adds Mount point, Capacity, Used, and Free. lgse/strata#1331, lgse/strata#1393
- For an unmounted volume it shows "Not mounted", the device size when known, and "Unavailable (not mounted)" for Used, without mounting. lgse/strata#1393
- The footer offers Set label, Eject, and Format; Format appears only for removable drives. lgse/strata#1331, lgse/strata#1393
- The footer shows Eject for a removable drive or a row with Eject or Unmount; it is insensitive without either action. lgse/strata#1393 (unverified)

### Set label

- Set label… saves a display label in Strata preferences; the filesystem label and mount state stay unchanged. lgse/strata#1393
- A saved label replaces the row name in Devices in every open window and in Properties. lgse/strata#1393
- Saving an empty label restores the system name. lgse/strata#1393
- The label field stops at 255 characters; a control character shows "Labels cannot contain control characters." inline and disables Save label. lgse/strata#1393 (unverified)
- Save label is disabled while the text matches the saved label. lgse/strata#1393 (unverified)
- Set label is offered only for devices with a volume UUID or a mount root URI. lgse/strata#1393 (unverified)

### Format

- Format… appears only for volumes on a removable drive; fixed disks and network shares never offer it. lgse/strata#1331, lgse/strata#1393
- If `mkfs.fat`, `mkfs.ntfs`/`mkntfs`, or `mkfs.exfat` is missing, Format opens "Missing tools" before unmounting anything. lgse/strata#1331
- Missing tools shows a copyable pacman, apt, dnf, or zypper install command, or generic guidance on an unrecognized distribution. lgse/strata#1331
- On Arch and Omarchy the suggested NTFS package is `ntfsprogs`. lgse/strata#1331
- The Format Drive dialog offers FAT32, NTFS, and exFAT, preselects the current filesystem marked "(current)", and checks Quick format. lgse/strata#1331, lgse/strata#1393
- The label field stops at 11 characters on FAT32 and 32 on NTFS and exFAT. lgse/strata#1393 (unverified)
- A label with a character the filesystem forbids fails with "Invalid label: …" before unmounting. lgse/strata#1393
- Continue shows a summary and "This permanently erases ALL DATA on this volume. This cannot be undone."; formatting starts only when Format is pressed. lgse/strata#1331
- Cancel before Format changes nothing. lgse/strata#1331
- Format unmounts a mounted volume first; dismissing the authorization prompt shows no error. lgse/strata#1331
- Any other failure shows "Unable to update NAME (DEVICE)" with the error. lgse/strata#1331 (unverified)
- While formatting, a progress card reads "Formatting drive" and "Do not unplug until formatting finishes." and offers no cancel. lgse/strata#1393
- Success shows "Format complete" and "The drive was formatted successfully." lgse/strata#1331, lgse/strata#1393
- Closing the window while formatting is blocked with "Drive formatting is still active". lgse/strata#1393

### Focus

- Closing a drive dialog returns focus to the file pane, so `g` works without clicking a row. lgse/strata#1331

## Design

- Actions are volume-level only. Whole-disk and partition-table changes are out of scope, and destructive actions are never offered for network shares or internal volumes (lgse/strata#1293).
- lgse/strata#1331 shipped Rename as a filesystem relabel. lgse/strata#1393 replaced it with a Strata display label keyed by volume UUID or mount root URI, which never mounts, unmounts, or edits system configuration.
- lgse/strata#1331 ran mkfs tools through `pkexec`. lgse/strata#1393 replaced that with UDisks2 `Block.Format` and `update-partition-type`, so the partition type and reprobe change together. Quick format skips zeroing; FAT32 passes `-F 32`.
- Progress is indeterminate because the supported tools report no consistent percentage (lgse/strata#1331).
- Tools and labels are checked before unmounting, so a refusal never leaves a drive unmounted (lgse/strata#1331, lgse/strata#1393).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-30 | lgse/strata#1331 | feat | Added Format, Rename, and Properties for removable drives, with missing-tool install guidance. |

## Known gaps

None known.
