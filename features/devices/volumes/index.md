---
title: Devices and volumes
status: shipped
origin: {issue: lgse/strata#441, pr: lgse/strata#493}
branch: null
reviewed_at: 5738aad808ea4cc4671516bc569d85f862664809
review: draft
code: [src/ui/window/devices.rs, src/ui/window/sidebar_devices.rs, src/ui/window/device_menu.rs, src/ui/window/gio_devices.rs, src/ui/browser/location/devices.rs, src/ui/browser/location/volumes.rs]
tests: [src/ui/window/devices/tests.rs]
docs: []
related: [browser/sidebar, browser/search, operations/clipboard/send-to, remote/file-providers/network-locations]
---

## Summary

Listing the drives, volumes, and mounts that the desktop volume monitor reports under Devices, and mounting them on demand. Mounted GVfs network shares get a network row with Disconnect. It also supplies the removable destinations Send to… offers and the drive roots Ctrl+K searches. Children: `devices/volumes/release` (Unmount and Eject), `devices/volumes/encrypted` (Unlock and Lock), `devices/volumes/udiskie-unlock` (udiskie handoff), `devices/volumes/drive-dialogs` (Format, Set label, Properties), `devices/volumes/camera` (camera Photos view), and `devices/volumes/drive-order` (row order and drive dividers).

## Behavior

### Discovery

- Devices lists the GIO volume monitor's volumes, password-start drives with no listed volume, and non-shadowed mounts without a listed volume. lgse/strata#536, lgse/strata#935
- A mount the backend hides, such as a Pacman cache subvolume outside `$HOME`, `/media`, and `/run/media/$USER`, does not appear in Devices. lgse/strata#536
- A mounted USB drive appears once under Devices and opens normally. lgse/strata#493
- A mount whose volume is already listed gets no second row. lgse/strata#536
- With no volumes, mounts, password drives, or pending releases, neither the DEVICES heading nor its separator renders. lgse/strata#536
- Plugging in, mounting, unmounting, or removing a device updates Devices without a restart. lgse/strata#536
- A row's udev encryption hint appears once a worker has read it; Devices rebuilds when the hint changes. lgse/strata#1729 (unverified)
- Hovering a device row tints it with the text color at 6%; only the current location's row keeps the accent fill. lgse/strata#1909 (unverified)
- A volume row's accessible description is its mount path when mounted, otherwise its device path, such as `/dev/sdb1`. lgse/strata#2030

### Row buttons

- In the full-width sidebar, a drive's eject triangle tip sits under the expanded DEVICES chevron's tip at every text size. lgse/strata#2060
- On a row with only a Lock or Unlock button, its icon takes the eject column; beside an eject button it sits one action slot to the left. lgse/strata#2060 (unverified)
- Hovering the eject icon brightens it with no pill, while the row highlight runs behind it to the row's right edge. lgse/strata#2060
- Clicking the eject button with the mouse leaves no focus ring. lgse/strata#2060
- Tabbing to the eject button shows one ring around the icon, not around the 24 px button. lgse/strata#2060
- Clicking the Lock or Unlock button with the mouse leaves no focus ring; tabbing to it shows one ring around the icon. lgse/strata#2060 (unverified)

### Mounting

- Clicking a mounted volume's row navigates to its mount root. lgse/strata#536 (unverified)
- Clicking an unmounted volume mounts it, then navigates into the mount. lgse/strata#493, lgse/strata#536
- Cancelling a mount's authentication prompt shows no error. lgse/strata#493
- A mount failure other than cancellation, a rejected passphrase, or an in-flight mount shows "Unable to mount volume" with the GIO error text. lgse/strata#493 (unverified)
- When another process is already mounting the volume, Strata shows "Connecting…" and waits up to 8 seconds without cancelling that job, then opens the mount. lgse/strata#935 (unverified)
- If that wait ends with the volume still unmounted, Strata starts its own mount once. lgse/strata#935 (unverified)

### Network shares

- A mounted SMB, SFTP, FTP, WebDAV, AFP, or NFS share appears under DEVICES with a network icon and no eject button. lgse/strata#31, lgse/strata#62, lgse/strata#2030
- `ftps://` and `davs://` mounts also take the network row, and the scheme match ignores case. lgse/strata#2030 (unverified)
- Clicking a network share's row opens the share. lgse/strata#31, lgse/strata#62
- Right-clicking a network share's row offers Properties and Disconnect. lgse/strata#31, lgse/strata#296, lgse/strata#2030

### Send to destinations

- Send to… lists a mounted removable device only when its root is a local path and writable. lgse/strata#1278, lgse/strata#1393
- Send to… device rows are sorted by name, ignoring case; devices sharing one identity are left out. lgse/strata#1278 (unverified)
- A recent Send to… folder that no longer exists on the device is left out of its submenu. lgse/strata#1278 (unverified)

### Global search roots

- Ctrl+K search covers Home plus the native roots of the volumes and volume-less mounts Devices lists, so files on listed drives are found. lgse/strata#222, lgse/strata#2070
- With a btrfs subvolume that Devices does not list mounted at `/var/cache/pacman/pkg`, Ctrl+K for a name that exists only inside it finds nothing. lgse/strata#2070
- A kernel network mount that Devices lists is still searched. lgse/strata#2070
- A listed mount whose root has a path but is not native, such as a GVfs FUSE mirror of a remote share, adds no search root. lgse/strata#2070

## Design

- Visibility policy belongs to GIO, GVfs, and udisks2, as in Nautilus, Nemo, Thunar, and Dolphin. lgse/strata#493 added a raw `/proc/self/mountinfo` fallback to surface USB drives (lgse/strata#441). It reinstated mounts the backend hides on purpose, so lgse/strata#536 removed it from the sidebar (lgse/strata#532).
- An empty device list is a valid answer. A union volume monitor does not reveal which backend is active, so Strata does not infer a degraded backend from a short list (lgse/strata#532).
- Global search follows the backend too, the policy lgse/strata#533 asked to decide. It once added every `/dev`-backed mount from the raw mount table, so it walked mounts Devices hides. Its roots now come from the same volume-monitor enumeration and own-row rule as the sidebar (lgse/strata#2070).
- Removable Send To destinations and encryption hints are checked off the UI thread, cached, and refreshed on volume monitor signals. Remembered Send To folders are checked again each time a menu is built. Destination and folder checks run on the mount's request lane, so a stalled mount cannot freeze the menu (lgse/strata#1729).
- Sidebar mounts run through the browser's mount flow, so volumes share the themed authentication prompt, quiet cancellation, and retries used by remote locations (lgse/strata#302, lgse/strata#493).
- GVfs network mounts are shares to disconnect, not drives to eject. Before lgse/strata#2030, only SMB got the network row, and an SFTP share showed a drive icon with eject (lgse/strata#2016).
- A volume row is described like a mount row, by its path. GIO sets no activation root for an fstab volume, and cdda and MTP volumes have a raw URI one, so the description skips it (lgse/strata#2012, lgse/strata#2030).
- Device action icons share the section chevron's size and inset, so both tips stay in one column at every text size. The icon sits off-centre in its 24 px button, so the focus ring wraps the icon (lgse/strata#2059, lgse/strata#2060).
- A desktop automounter may already own a mount job. Strata waits for it rather than cancelling it, and never disables the user's automounter (lgse/strata#537, lgse/strata#935).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-11-06 | lgse/strata#2070 | fix | Limited Ctrl+K search roots to Home plus the local mounts Devices lists, so hidden system mounts are no longer scanned. |
| 2026-11-02 | lgse/strata#2030 | fix | Described volume rows by path, gave GVfs shares network rows, sent every window off released devices, and fixed Properties and udiskie restore polish. |
| 2026-09-07 | lgse/strata#536 | fix | Limited Devices to what the volume monitor reports, removing the raw mount-table fallback. |
| 2026-09-06 | lgse/strata#493 | fix | Showed mounted USB drives, mounted sidebar volumes through the themed prompt, and added drives to global search. |

## Known gaps

- NAS shares mounted by the system at native paths, such as NFS under `/mnt`, do not appear in Devices when GIO misses them. lgse/strata#1209
- An unmounted fstab volume's row is described by its device path, not its fstab mount point. lgse/strata#2030
- Network share rows offer Disconnect even when the mount reports it cannot be unmounted. lgse/strata#62
- An internal disk mounted through fstab at `/mnt/data` without `x-gvfs-show` is left out of Ctrl+K search. No warning shows and no setting adds it back. lgse/strata#2070 ([comment](https://github.com/lgse/strata/pull/2070#issuecomment-6677782710))
