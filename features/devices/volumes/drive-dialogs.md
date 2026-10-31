---
title: Drive format, label, and properties
status: shipped
origin: {issue: lgse/strata#1293, pr: lgse/strata#1331}
branch: null
reviewed_at: 965bd7ec74400734dbd0a5311ceefa05bea8dd63
review: draft
code: [src/ui/window/drive_dialogs.rs, src/ui/window/drive_dialogs/**, src/ui/window/drive_ops.rs, src/ui/window/device_labels.rs, src/ui/missing_tools.rs]
tests: [src/ui/window/drive_dialogs/tests.rs, src/ui/window/drive_ops/tests.rs, src/ui/window/device_labels/tests.rs, src/ui/missing_tools/tests.rs]
related: [browser/sidebar, operations/progress, app/dialogs, devices/volumes/encrypted]
---

## Summary

Dialogs opened from a device row's menu: Properties for any listed storage, Set label… for a Strata-only display name, and Format… for removable drives. It also decides when the row menu offers Mount. Formatting asks twice and names the exact target before erasing anything. Its drive operations also close a LUKS container through UDisks when Lock has no stoppable drive.

## Behavior

### Mount entry

- The row menu offers Mount for an unmounted volume on a removable or media-removable drive that reports `can_mount`. lgse/strata#1331 (unverified)

### Properties

- Properties opens from the menu of a volume or a mount-only entry, including fixed storage. lgse/strata#1393
- It lists System name, Strata label, Device, Filesystem, and Status; a mounted volume adds Mount point, Capacity, Used, and Free. lgse/strata#1331, lgse/strata#1393
- Properties opens at once with "—" for Filesystem, Capacity, and Used, then fills them in when a worker has read the drive. lgse/strata#1729
- Until then, a target with a known mount shows its Mount point and "Mounted"; otherwise Status shows "—". lgse/strata#1729 (unverified)
- For an unmounted volume it shows "Not mounted", the device size when known, and "Unavailable (not mounted)" for Used, without mounting. lgse/strata#1393
- The footer offers Set label, Eject, and Format; Format appears only for removable drives. lgse/strata#1331, lgse/strata#1393
- The footer shows Eject for a removable drive or a row with Eject or Unmount; it is insensitive without either action. lgse/strata#1393 (unverified)

### Set label

- Set label… saves a display label in Strata preferences; the filesystem label and mount state stay unchanged. lgse/strata#1393
- A saved label replaces the row name in Devices in every open window and in Properties. lgse/strata#1393
- Saving an empty label restores the system name. lgse/strata#1393
- The label field stops at 255 characters; a control character shows "Labels cannot contain control characters." inline and disables Save label. lgse/strata#1393 (unverified)
- The Set label field is named "Label shown in Strata". lgse/strata#1896 (unverified)
- Save label is disabled while the text matches the saved label. lgse/strata#1393 (unverified)
- Set label is offered only for devices with a volume UUID or a mount root URI. lgse/strata#1393 (unverified)

### Format

- Format… appears only for volumes on a removable drive; fixed disks and network shares never offer it. lgse/strata#1331, lgse/strata#1393
- Format Drive opens at once with Continue insensitive; a worker checks the tools and the drive, then fills in the options. lgse/strata#1729
- A Devices rebuild while Format Drive waits does not lose the Missing tools dialog or the format progress. lgse/strata#1729
- If `mkfs.fat`, `mkfs.ntfs`/`mkntfs`, or `mkfs.exfat` is missing, Format Drive closes and "Missing tools" opens before anything is unmounted. lgse/strata#1331, lgse/strata#1729
- Missing tools shows a copyable pacman, apt, dnf, or zypper install command, or generic guidance on an unrecognized distribution. lgse/strata#1331
- On Arch and Omarchy the suggested NTFS package is `ntfsprogs`. lgse/strata#1331
- The Format Drive dialog offers FAT32, NTFS, and exFAT, preselects the current filesystem marked "(current)", and checks Quick format. lgse/strata#1331, lgse/strata#1393
- The label field stops at 11 bytes on FAT32, 11 UTF-16 units on exFAT, and 32 UTF-16 units on NTFS. lgse/strata#1393, lgse/strata#1875
- Format Drive's label field is named "Filesystem label". lgse/strata#1896 (unverified)
- Typed or pasted label text past the limit is cut to what fits: six emoji on exFAT leave five, with Continue enabled. lgse/strata#1875
- On FAT32, typing `ÉTIQUETTE12` leaves `ÉTIQUETTE1`, because `É` counts 2 bytes. lgse/strata#1875
- Switching filesystem trims the label to the new limit in its unit: six emoji typed under NTFS leave two under FAT32. lgse/strata#1875
- The remaining-count caption under the label counts in the selected filesystem's unit. lgse/strata#1875
- A label with a character the filesystem forbids fails with "Invalid label: …" before unmounting. lgse/strata#1393
- Continue shows a summary and "This permanently erases ALL DATA on this volume. This cannot be undone."; formatting starts only when Format is pressed. lgse/strata#1331
- Cancel before Format changes nothing. lgse/strata#1331
- Format unmounts a mounted volume first; dismissing the authorization prompt shows no error. lgse/strata#1331
- Any other failure shows "Unable to update NAME (DEVICE)" with the error. lgse/strata#1331 (unverified)
- While formatting, a progress card reads "Formatting drive" and "Do not unplug until formatting finishes." and offers no cancel. lgse/strata#1393
- Success shows "Format complete" and "The drive was formatted successfully." lgse/strata#1331, lgse/strata#1393
- Closing the window while formatting is blocked with "Drive formatting is still active". lgse/strata#1393

### Container lock

- When Lock has no stoppable drive, it finds the LUKS container from the volume's device path, then from its LUKS UUID. lgse/strata#1952
- A device path naming the open mapping leads to its container. lgse/strata#1952
- Lock calls UDisks `Encrypted.Lock` only on a block carrying the `Encrypted` interface. lgse/strata#1952
- Lock on a container that is already closed succeeds without calling `Encrypted.Lock`. lgse/strata#1952
- A LUKS UUID shared by several blocks, as on cloned disks, matches none; a unique device-path match still locks. lgse/strata#1952
- With no unique device-path or UUID match, Lock shows "Could not identify the drive's block device". lgse/strata#1952
- A mapping opened by another user or through fstab asks for polkit authorization; dismissing the prompt shows no error. lgse/strata#1952
- Any other UDisks failure shows its message without the D-Bus error prefix. lgse/strata#1952
- A D-Bus failure reading the container's `CleartextDevice`, such as a udisksd restart, shows that failure, not "Could not identify the drive's block device". lgse/strata#1952

### Focus

- Closing a drive dialog returns focus to the file pane, so `g` works without clicking a row. lgse/strata#1331

## Design

- Actions are volume-level only. Whole-disk and partition-table changes are out of scope, and destructive actions are never offered for network shares or internal volumes (lgse/strata#1293).
- lgse/strata#1331 shipped Rename as a filesystem relabel. lgse/strata#1393 replaced it with a Strata display label keyed by volume UUID or mount root URI, which never mounts, unmounts, or edits system configuration.
- lgse/strata#1331 ran mkfs tools through `pkexec`. lgse/strata#1393 replaced that with UDisks2 `Block.Format` and `update-partition-type`, so the partition type and reprobe change together. Quick format skips zeroing; FAT32 passes `-F 32`.
- Tool lookups, the package manager, the mount table, and drive facts are read on a worker, so a stalled mount cannot freeze the window (lgse/strata#1729).
- Progress is indeterminate because the supported tools report no consistent percentage (lgse/strata#1331).
- Tools and labels are checked before unmounting, so a refusal never leaves a drive unmounted (lgse/strata#1331, lgse/strata#1393). Until lgse/strata#1875, an exFAT label of 12 to 32 characters passed, unmounted the drive, then failed in UDisks (lgse/strata#1849, lgse/strata#1875).
- Label limits and units match the libblockdev checks UDisks runs before wiping: 11 UTF-16 units for exFAT, 11 bytes for FAT32. Strata's NTFS limit of 32 units is below the backend's 128 (lgse/strata#1849, lgse/strata#1875).
- The field trims in the filesystem's unit through the shared form field limit that `app/dialogs` records (lgse/strata#1875).
- Container lock skips a block only when UDisks answers `InvalidArgs`, `UnknownInterface`, or `UnknownProperty`. Treating every read error as "not encrypted" hid real failures behind "device not found" after the unmount (lgse/strata#1952).
- Only `Encrypted.Lock` waits indefinitely, for the polkit prompt; lookups keep the default timeout so a hung udisksd fails instead of leaving Lock in flight (lgse/strata#1952).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-31 | lgse/strata#1952 | fix | Closed the LUKS container through UDisks `Encrypted.Lock` when Lock has no stoppable drive, so internal volumes no longer stay open. |
| 2026-10-25 | lgse/strata#1875 | fix | Limited exFAT labels to 11 UTF-16 units and FAT32 to 11 bytes, so a long label no longer unmounts the drive then fails. |
| 2026-09-30 | lgse/strata#1331 | feat | Added Format, Rename, and Properties for removable drives, with missing-tool install guidance. |

## Known gaps

- An exFAT label containing `*`, `?`, `:`, `/`, `\`, `|`, `<`, `>`, or `"` is refused, though `mkfs.exfat` accepts each of them. lgse/strata#1875
