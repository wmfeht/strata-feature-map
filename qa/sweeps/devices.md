---
title: Devices sweep
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
tools: [docs/preview-sandbox.md, data/udiskie/unlock, install.sh]
---

## Scope

Everything the sidebar's Devices section does with a physical or virtual block device. Discovery and mounting of volumes, mounts, and password drives. Unmount and Eject with the flush, the pending row, and "Safe to remove". Unlock and Lock on LUKS volumes, including saved passphrases. The udiskie hook, `--unlock-volume`, and the install and uninstall flags. Properties, Set label, and Format with Missing tools. The gphoto2 camera Photos view with its ordering and thumbnails.

Left to other sweeps: the Send to lists, device rows as navigation targets, network mounts and their credentials, and the installer's handling of `--with-udiskie-unlock`.

## Setup

- A guest from `~/dev/strata-qemu-testing` (`omarchy-4` and `arch`) with disks attached and detached over QMP `device_add` and `device_del`. Its `guest-tests/smoke-luks-hotplug.sh` and `smoke-udiskie-unlock.sh` show the hotplug and hook wiring. Every format, eject, and config rewrite runs there; the host never serves a destructive device probe.
- USB stick images: `truncate -s 256M` then `mkfs.vfat -n STICK`, attached as removable `usb-storage`. Make a second with the same label, a third with no label, and an ext4 one labeled with raw bytes through `e2label`. A fourth carries three partitions, one unformatted.
- A LUKS image: `truncate -s 128M luks.img && cryptsetup luksFormat --type luks2 luks.img`, attached as its own USB disk, plus one disk holding two LUKS partitions with the same passphrase. Keep a `losetup` twin on the host for detection checks only; never format it from Strata.
- udisks2 running and udiskie installed in the guest; `udisksctl`, `lsblk`, `findmnt`, `udevadm monitor`, and `secret-tool` for ground truth after every action.
- A throwaway HOME as in `qa/README.md`, plus a copy of `~/.config/udiskie` and `~/.local/share/strata` taken before each install probe, to diff the restore.
- A real PTP camera or iPhone passed through with `-device usb-host`; GVfs gphoto2 mounts only USB devices. Without one, record the camera block as not exercised.
- `RUST_LOG=debug` beside `journalctl -f -u udisks2`; a GTK critical at any plug, mount, unmount, or unplug event is a finding.

## Probes

- Run each probe with Strata started before the device appears and after; a second window must show the same rows in the same order.
- Reach each row action by pointer, by the row's button, and by the row menu from the keyboard; compare the outcome with `findmnt`.
- Plug and unplug the same stick twenty times without pause and count rows and separators at the end.

### devices/volumes

- Attach the two same-label sticks, the unlabeled stick, and the raw-byte ext4 image together; open each row and compare mount roots with `findmnt`.
- Attach the three-partition disk and count rows before and after mounting one partition from a shell.
- Unplug a stick while its folder is open in Columns, Icons, and List, and once more while a copy into it is running.
- Start a mount from the row while udiskie is prompting for the same volume. Cancel udiskie's prompt after 3 seconds, then on a fresh attempt after 10.
- Loop-mount an image under `/mnt`, under `/run/media/$USER`, and with `udisksctl mount`; note which appear and which vanish on `umount`.

### devices/volumes/release

- Eject while a copy into the stick runs, while a shell sits inside the mount, and while `sleep` holds a file open there. Read each error.
- Write 500 MB to the stick, press Eject, and detach the disk over QMP while the overlay is still up.
- Eject from one window while a second window browses two levels inside the device; watch where the second pane lands.
- Hide the overlay, switch the theme accent, open Properties on the pending row, and press Eject on it again before GIO resolves.
- Attach an ISO as a CD-ROM and a non-removable virtio ext4 disk; release each and compare the closing overlay.

### devices/volumes/encrypted

- Enter a wrong passphrase three times, then the right one with "Remember forever"; verify the entry with `secret-tool search` under both attribute names.
- Unlock the second of two same-passphrase LUKS partitions on one disk; check which mount point the pane opens.
- Hide the "Unlocking volume" overlay and navigate to Home before unlock completes; then repeat with the pane already inside the mount.
- Lock the login keyring with `secret-tool lock`, then Lock a volume with a saved passphrase; confirm the mount and the secret both survive.
- Open the volume with `cryptsetup open` but no mount, then press Unlock and Lock on its row.

### devices/volumes/udiskie-unlock

- Run `strata --udiskie-hook` with an empty DEVICE, with both operands empty, with an uppercase UUID, and with `device_removed`; log the argv that results.
- Start `strata --unlock-volume /dev/sdX` and attach the disk after 5 seconds, then after 9 seconds; repeat with the plain FAT stick's path.
- Install over no `~/.config/udiskie`, over a commented `config.yml` with its own `event_hook`, and over a symlinked `config.yml`. Repeat over `config.json` only and over both files; diff each restore against the copy.
- Install twice, then uninstall twice; `udiskie` must still start after each step.
- With the handler installed and udiskie stopped, attach the LUKS disk; the stick must not automount and the prompt must name that device.

### devices/volumes/drive-dialogs

- Open Properties on each attached device: unmounted and mounted sticks, locked and unlocked LUKS, the CD-ROM, the loop mount, and the virtio disk. Compare Capacity, Used, and Free with `df -B1`.
- Set label to 255 characters, emoji, RTL text, whitespace only, a pasted tab, and the same text on both same-label sticks. Then relabel one with `fatlabel` from a shell and replug.
- Delete `mkfs.exfat` only and open Format for each filesystem; then format with a label at the exact limit and a lowercase FAT label.
- Open Format Drive, detach the disk before Continue, reattach, and press Format.
- Format while a shell sits inside the mount, and with an Eject pending on the same row. Cancel the polkit prompt at the unmount step, then at the format step.

### devices/volumes/camera

- Switch the camera between PTP and mass-storage mode while Strata is open; both entries may exist at once.
- Scan a store of 5,000 photos across DCIM folders with duplicate names; scroll, press F5, and switch views and sort fields mid-scan.
- Lock the iPhone, then detach it over USB, each during a scan; read the error and the rows left behind.
- Copy 50 photos to the stick during the scan, then Eject the stick; preview one HEIC and delete one of a duplicate pair.
- Add a dot-prefixed folder of photos on the device and toggle hidden files during and after the scan.

## Hand-offs

- Send to entries for mounted and unmounted devices → `operations`.
- The "Writing to device…" flush before a copy to removable media reports success → `operations`.
- Device rows as navigation targets, sidebar keyboard order, and drops onto rows → `browser`.
- SMB, SFTP, and other network mounts with their credential prompts → `remote`.
- `install.sh` step wording, `--with-udiskie-unlock`, and Omarchy detection → `app`.
- Previewing camera photos in the preview panel → `preview`.
- The Settings page shell around the "Unlock encrypted volumes" row → `settings`.
