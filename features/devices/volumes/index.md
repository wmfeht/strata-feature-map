---
title: Devices and volumes
status: shipped
origin: {issue: lgse/strata#441, pr: lgse/strata#493}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [src/ui/window/devices.rs]
tests: [src/ui/window/devices/tests.rs]
docs: []
related: [browser/sidebar, browser/search, operations/clipboard]
---

## Summary

Listing the drives, volumes, and mounts that the desktop volume monitor reports under Devices, and mounting them on demand. Children: `devices/volumes/release` (Unmount and Eject), `devices/volumes/encrypted` (Unlock and Lock), `devices/volumes/udiskie-unlock` (udiskie handoff), `devices/volumes/drive-dialogs` (Format, Set label, Properties), and `devices/volumes/camera` (camera Photos view).

## Behavior

### Discovery

- Devices lists the GIO volume monitor's volumes, password-start drives with no listed volume, and non-shadowed mounts without a listed volume. lgse/strata#536, lgse/strata#935
- A mount the backend hides, such as a Pacman cache subvolume outside `$HOME`, `/media`, and `/run/media/$USER`, does not appear in Devices. lgse/strata#536
- A mounted USB drive appears once under Devices and opens normally. lgse/strata#493
- A mount whose volume is already listed gets no second row. lgse/strata#536
- With no volumes, mounts, password drives, or pending releases, neither the DEVICES heading nor its separator renders. lgse/strata#536
- Plugging in, mounting, unmounting, or removing a device updates Devices without a restart. lgse/strata#536

### Mounting

- Clicking a mounted volume's row navigates to its mount root. lgse/strata#536 (unverified)
- Clicking an unmounted volume mounts it, then navigates into the mount. lgse/strata#493, lgse/strata#536
- The row menu offers Mount for an unmounted volume on a removable drive that reports `can_mount`. lgse/strata#1331 (unverified)
- A cancelled mount shows no error; any other failure shows "Unable to mount volume" with the GIO error text. lgse/strata#493 (unverified)
- When another process is already mounting the volume, Strata shows "Connecting…" and waits up to 8 seconds without cancelling that job, then opens the mount. lgse/strata#935 (unverified)
- If that wait ends with the volume still unmounted, Strata starts its own mount once. lgse/strata#935 (unverified)

## Design

- Visibility policy belongs to GIO, GVfs, and udisks2, as in Nautilus, Nemo, Thunar, and Dolphin. lgse/strata#493 added a raw `/proc/self/mountinfo` fallback to surface USB drives (lgse/strata#441). It reinstated mounts the backend hides on purpose, so lgse/strata#536 removed it from the sidebar (lgse/strata#532).
- An empty device list is a valid answer. A union volume monitor does not reveal which backend is active, so Strata does not infer a degraded backend from a short list (lgse/strata#532).
- Global search still reads the raw mount table for its roots; that policy is separate (lgse/strata#533).
- Sidebar mounts run through the browser's mount flow, so volumes share the themed authentication prompt, quiet cancellation, and retries used by remote locations (lgse/strata#302, lgse/strata#493).
- A desktop automounter may already own a mount job. Strata waits for it rather than cancelling it, and never disables the user's automounter (lgse/strata#537, lgse/strata#935).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-07 | lgse/strata#536 | fix | Limited Devices to what the volume monitor reports, removing the raw mount-table fallback. |
| 2026-09-06 | lgse/strata#493 | fix | Showed mounted USB drives, mounted sidebar volumes through the themed prompt, and added drives to global search. |

## Known gaps

- NAS shares mounted by the system at native paths, such as NFS under `/mnt`, do not appear in Devices when GIO misses them. lgse/strata#1209
