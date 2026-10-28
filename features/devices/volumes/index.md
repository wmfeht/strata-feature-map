---
title: Devices and volumes
status: shipped
origin: {issue: lgse/strata#441, pr: lgse/strata#493}
branch: null
reviewed_at: 86df474dc0e8352e0e2098637a017cc4c77a8c44
review: draft
code: [src/ui/window/devices.rs]
tests: [src/ui/window/devices/tests.rs]
docs: []
related: [browser/sidebar, browser/search, operations/clipboard/send-to, remote/file-providers/network-locations]
---

## Summary

Listing the drives, volumes, and mounts that the desktop volume monitor reports under Devices, and mounting them on demand. It also supplies the removable destinations Send to… offers and the drive roots Ctrl+K searches. Children: `devices/volumes/release` (Unmount and Eject), `devices/volumes/encrypted` (Unlock and Lock), `devices/volumes/udiskie-unlock` (udiskie handoff), `devices/volumes/drive-dialogs` (Format, Set label, Properties), and `devices/volumes/camera` (camera Photos view).

## Behavior

### Discovery

- Devices lists the GIO volume monitor's volumes, password-start drives with no listed volume, and non-shadowed mounts without a listed volume. lgse/strata#536, lgse/strata#935
- A mount the backend hides, such as a Pacman cache subvolume outside `$HOME`, `/media`, and `/run/media/$USER`, does not appear in Devices. lgse/strata#536
- A mounted USB drive appears once under Devices and opens normally. lgse/strata#493
- A mount whose volume is already listed gets no second row. lgse/strata#536
- With no volumes, mounts, password drives, or pending releases, neither the DEVICES heading nor its separator renders. lgse/strata#536
- Plugging in, mounting, unmounting, or removing a device updates Devices without a restart. lgse/strata#536
- A row's udev encryption hint appears once a worker has read it; Devices rebuilds when the hint changes. lgse/strata#1729 (unverified)

### Mounting

- Clicking a mounted volume's row navigates to its mount root. lgse/strata#536 (unverified)
- Clicking an unmounted volume mounts it, then navigates into the mount. lgse/strata#493, lgse/strata#536
- Cancelling a mount's authentication prompt shows no error. lgse/strata#493
- A mount failure other than cancellation, a rejected passphrase, or an in-flight mount shows "Unable to mount volume" with the GIO error text. lgse/strata#493 (unverified)
- When another process is already mounting the volume, Strata shows "Connecting…" and waits up to 8 seconds without cancelling that job, then opens the mount. lgse/strata#935 (unverified)
- If that wait ends with the volume still unmounted, Strata starts its own mount once. lgse/strata#935 (unverified)

### Send to destinations

- Send to… lists a mounted removable device only when its root is a local path and writable. lgse/strata#1278, lgse/strata#1393
- Send to… device rows are sorted by name, ignoring case; devices sharing one identity are left out. lgse/strata#1278 (unverified)
- A recent Send to… folder that no longer exists on the device is left out of its submenu. lgse/strata#1278 (unverified)

### Global search roots

- Ctrl+K search covers Home and every mounted local drive. lgse/strata#222, lgse/strata#493

## Design

- Visibility policy belongs to GIO, GVfs, and udisks2, as in Nautilus, Nemo, Thunar, and Dolphin. lgse/strata#493 added a raw `/proc/self/mountinfo` fallback to surface USB drives (lgse/strata#441). It reinstated mounts the backend hides on purpose, so lgse/strata#536 removed it from the sidebar (lgse/strata#532).
- An empty device list is a valid answer. A union volume monitor does not reveal which backend is active, so Strata does not infer a degraded backend from a short list (lgse/strata#532).
- Global search still reads the raw mount table for its roots; that policy is separate (lgse/strata#533).
- Removable Send To destinations and encryption hints are checked off the UI thread, cached, and refreshed on volume monitor signals. Remembered Send To folders are checked again each time a menu is built. Destination and folder checks run on the mount's request lane, so a stalled mount cannot freeze the menu (lgse/strata#1729).
- Sidebar mounts run through the browser's mount flow, so volumes share the themed authentication prompt, quiet cancellation, and retries used by remote locations (lgse/strata#302, lgse/strata#493).
- A desktop automounter may already own a mount job. Strata waits for it rather than cancelling it, and never disables the user's automounter (lgse/strata#537, lgse/strata#935).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-07 | lgse/strata#536 | fix | Limited Devices to what the volume monitor reports, removing the raw mount-table fallback. |
| 2026-09-06 | lgse/strata#493 | fix | Showed mounted USB drives, mounted sidebar volumes through the themed prompt, and added drives to global search. |

## Known gaps

- NAS shares mounted by the system at native paths, such as NFS under `/mnt`, do not appear in Devices when GIO misses them. lgse/strata#1209
