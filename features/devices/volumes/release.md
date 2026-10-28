---
title: Unmount and eject
status: shipped
origin: {issue: lgse/strata#295, pr: lgse/strata#296}
branch: null
reviewed_at: 86df474dc0e8352e0e2098637a017cc4c77a8c44
review: draft
code: [src/ui/window/device_release.rs]
tests: [src/ui/window/device_release/tests.rs]
docs: [docs/filesystem-compatibility.md]
related: [operations/clipboard, operations/filesystem-compatibility/open-files, remote/file-providers/network-locations, app/accessibility]
---

## Summary

Safely removing a device from its Devices row: Eject or Unmount flushes pending writes, releases the device through GIO, and says when it is safe to unplug. Lock on an encrypted volume reuses the same release path.

## Behavior

### Availability

- A device row shows an eject button and an Eject menu entry when its volume or mount reports `can_eject`. lgse/strata#296
- A row whose mount reports only `can_unmount` shows the same button with the tooltip and menu entry "Unmount". lgse/strata#296
- The eject button's accessible name equals its tooltip, "Eject" or "Unmount". lgse/strata#1895 (unverified)
- A fixed internal disk that reports neither shows no eject button and no Eject or Unmount entry. lgse/strata#296
- The eject button stays visible and clickable when the sidebar's overlay scrollbar is shown. lgse/strata#935

### Releasing

- Eject or Unmount while browsing inside the device navigates the pane Home before the flush starts. lgse/strata#296, lgse/strata#1193
- Ejecting or unmounting a remote mount other than SMB, such as SFTP, from its DEVICES row while browsing inside it also sends the pane Home. lgse/strata#352, lgse/strata#296
- Before the flush, Strata releases its own reads under the mount root, as file operations do. lgse/strata#1729
- Unmount or Eject while the preview reads a file on the device does not fail as busy. lgse/strata#1729
- Strata runs `syncfs` on the mount root off the GTK thread, then calls the GIO eject or unmount. lgse/strata#1193
- If the flush fails, GIO is not called and "Unable to eject device" or "Unable to unmount device" shows the error. lgse/strata#1193 (unverified)
- If the flush or GIO call fails while the volume is still mounted, the pane returns to the folder it left. lgse/strata#1193
- That return is skipped when the user navigated elsewhere after the pane went Home. lgse/strata#1193 (unverified)
- After 350 ms an "Ejecting" or "Unmounting" overlay shows "Writing data to the drive. Do not unplug it. You can hide this and keep working." lgse/strata#1193 (unverified)
- Hide, Close, and Escape dismiss the overlay without cancelling the release. lgse/strata#1193
- Until the release finishes, the row stays in Devices, insensitive, with a spinner, even after GIO drops the device. lgse/strata#1193
- The pending row and its spinner carry the accessible label "Writing data to the drive. Do not unplug it." lgse/strata#1193 (unverified)
- While a release is pending, the header activity spinner runs with the accessible description "Writing to device…". lgse/strata#1193 (unverified)
- The pending spinner uses the theme accent color and follows live theme changes. lgse/strata#1199
- A GIO unmount-progress message replaces the overlay body, followed by "Do not unplug it." lgse/strata#1193 (unverified)
- A second Eject or Unmount on a device with a release pending does nothing. lgse/strata#1193 (unverified)

### Outcome

- When an eject, or an unmount of a removable drive, succeeds with the overlay open, it retitles to "Safe to remove" with "NAME can be unplugged." and a Close button. lgse/strata#1193
- A successful unmount of non-removable storage closes the overlay without "Safe to remove". lgse/strata#1193
- A release cancelled in the authentication dialog shows no error dialog. lgse/strata#296
- A GIO `FailedHandled` error, or one whose message contains "aborted", also shows no error dialog. lgse/strata#296 (unverified)
- Any other GIO failure shows "Unable to eject device" or "Unable to unmount device" with the error and the last progress message. lgse/strata#296, lgse/strata#1193 (unverified)

## Design

- Eject is preferred because USB and optical media need the drive eject, not only an unmount. Unmount is the fallback. Hiding both on fixed disks avoids buttons that always fail (lgse/strata#295).
- A user unmounted an NTFS stick the moment its row vanished and lost a folder still in the page cache (lgse/strata#1182). Release therefore flushes with `syncfs` before GIO and keeps the row pending until GIO resolves, as GNOME Files does.
- The pane leaves the volume before the flush so its directory monitors close and do not hold the mount busy (lgse/strata#1193).
- Strata's own reads under the mount root are released before the flush. An open file makes the unmount fail as busy, and a sandbox that binds a file keeps the filesystem mounted inside it (lgse/strata#1729).
- The flush runs through `gio::spawn_blocking`, because even opening a stalled mount must not block the UI thread (lgse/strata#1193).
- "Safe to remove" requires Eject, or a drive that is removable, media-removable, or ejectable. Lock and fixed-disk unmounts never claim it (lgse/strata#1193).
- The copy-side flush from the same PR, "Writing to device…" before a copy to removable media reports success, belongs to the transfer operations (lgse/strata#1193).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-23 | lgse/strata#1199 | fix | Tinted the pending release spinner with the theme accent to match the eject button. |
| 2026-09-23 | lgse/strata#1193 | feat | Flushed with `syncfs` before unmount or eject and kept the row pending until GIO finished, after a data-loss report. |
| 2026-09-04 | lgse/strata#296 | feat | Added the eject button and Eject/Unmount menu entries for removable media, hidden on fixed disks. |

## Known gaps

None known.
