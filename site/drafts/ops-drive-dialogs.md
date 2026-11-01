---
proposed: {page: new}
nodes: [devices/volumes/drive-dialogs]
reason: The Archives reference names devices/volumes/drive-dialogs but covers only the format progress card. In v1.1.1, Properties and Format Drive open at once, exFAT and FAT32 label limits are enforced in their own units, and the fields have accessible names. No section covers the dialogs.
release: v1.1.1
---

Raw material for a "Drive dialogs" reference page, or a section a person adds
beside "Mount, unlock, and eject drives" in the Remote and devices guide.

## Properties

- Properties opens at once with "—" for Filesystem, Capacity, and Used, then
  fills them in once the drive has been read in the background.
- Until then, a target with a known mount shows its Mount point and "Mounted";
  otherwise Status shows "—".

## Set label

- The Set label field is named "Label shown in Strata".

## Format Drive

- Format Drive opens at once with Continue insensitive, then fills in the
  options once the tools and the drive have been checked in the background.
- If `mkfs.fat`, `mkfs.ntfs`/`mkntfs`, or `mkfs.exfat` is missing, Format
  Drive closes and "Missing tools" opens before anything is unmounted.
- A Devices list rebuild while Format Drive waits does not lose the Missing
  tools dialog or the format progress.
- The label field is named "Filesystem label". It stops at 11 bytes on FAT32,
  11 UTF-16 units on exFAT, and 32 UTF-16 units on NTFS.
- Typed or pasted text past the limit is cut to what fits: six emoji on exFAT
  leave five, with Continue enabled. On FAT32, typing `ÉTIQUETTE12` leaves
  `ÉTIQUETTE1`, because `É` counts 2 bytes.
- Switching filesystem trims the label to the new limit: six emoji typed under
  NTFS leave two under FAT32.
- The remaining-count caption under the label counts in the selected
  filesystem's unit.
- An exFAT label containing `*`, `?`, `:`, `/`, `\`, `|`, `<`, `>`, or `"` is
  refused before unmounting, though `mkfs.exfat` accepts them.
