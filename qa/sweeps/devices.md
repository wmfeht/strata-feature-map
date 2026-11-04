---
title: Devices sweep
reviewed_at: ad6d14fe532db7b49b966fd120ac899f8b6b4214
tools: [docs/preview-sandbox.md, data/udiskie/unlock, scripts/sftp-fixture.sh]
---

## Scope

Everything the sidebar's Devices section does with a device or mount listed under DEVICES. Discovery and mounting of volumes, mounts, and password drives. Unmount and Eject with the flush, the pending row, and "Safe to remove", including the network row and Disconnect of a mounted GVfs share. Unlock and Lock on LUKS volumes, including saved passphrases. The udiskie hook, `--unlock-volume`, and the install and uninstall flags. Properties, Set label, and Format with Missing tools. The gphoto2 camera Photos view with its ordering and thumbnails. Which mounted devices Send to… offers, and the drives Ctrl+K searches.

Left to other sweeps: the Send to… submenu rows, Choose folder…, and copying to a device, device rows as navigation targets, network mounts and their credentials, and the installer's default selection and its `--with-udiskie-unlock` and `--without-udiskie-unlock` flags.

## Setup

- A guest from `~/dev/strata-qemu-testing` (`omarchy-4` and `arch`) with disks attached and detached over QMP `device_add` and `device_del`. Its `guest-tests/smoke-luks-hotplug.sh` and `smoke-udiskie-unlock.sh` show the hotplug and hook wiring. Every format, eject, and config rewrite runs there; the host never serves a destructive device probe.
- USB stick images: `truncate -s 256M` then `mkfs.vfat -n STICK`, attached as removable `usb-storage`. Make a second with the same label, a third with no label, and an ext4 one labeled with raw bytes through `e2label`. A fourth carries three partitions, one unformatted.
- A LUKS image: `truncate -s 128M luks.img && cryptsetup luksFormat --type luks2 luks.img`, attached as its own USB disk, plus one disk holding two LUKS partitions with the same passphrase. Attach a LUKS partition on a non-removable virtio disk too, and a `dd` clone of it, for Lock without a stoppable drive. Give that volume an fstab `noauto,user,x-gvfs-show` entry, and add a second guest user to open its mapping. Keep a `losetup` twin on the host for detection checks only; never format it from Strata.
- udisks2 running and udiskie installed in the guest; `udisksctl`, `lsblk`, `findmnt`, `udevadm monitor`, and `secret-tool` for ground truth after every action.
- A throwaway HOME as in `qa/README.md`, plus a copy of `~/.config/udiskie` and `~/.local/share/strata` taken before each install probe, to diff the restore.
- A real PTP camera or iPhone passed through with `-device usb-host`; GVfs gphoto2 mounts only USB devices. Without one, record the camera block as not exercised.
- An Android phone in MTP mode passed through the same way, for the MTP row probes.
- `RUST_LOG=debug` beside `journalctl -f -u udisks2`; a GTK critical at any plug, mount, unmount, or unplug event is a finding.
- A second build made with `STRATA_INTEGRATIONS=package`, copied into the guest beside the default build.
- `scripts/sftp-fixture.sh --port 2222` with GVfs running, as in `qa/sweeps/remote.md`, for the SFTP share's network row and Disconnect. Mount `davs://` and `afp://` locations too where a server is at hand.

## Probes

- Run each probe with Strata started before the device appears and after; a second window must show the same rows in the same order.
- Reach each row action by pointer, by the row's button, and by the row menu from the keyboard; compare the outcome with `findmnt`.
- Plug and unplug the same stick twenty times without pause and count rows and separators at the end.

### devices/volumes

- Attach the two same-label sticks, the unlabeled stick, and the raw-byte ext4 image together; open each row and compare mount roots with `findmnt`.
- Attach the three-partition disk and count rows before and after mounting one partition from a shell.
- Unplug a stick while its folder is open in Columns, Icons, and List, and once more while a copy into it is running.
- Start a mount from the row while udiskie is prompting for the same volume. Cancel udiskie's prompt after 3 seconds, then on a fresh attempt after 10.
- Hover a device row while its folder is the current location, then after Alt+Up leaves the pointer on it; repeat in a light and a dark theme.
- Loop-mount an image under `/mnt`, under `/run/media/$USER`, and with `udisksctl mount`; note which appear and which vanish on `umount`.
- Mount one stick read-only with `mount -o ro` beside a writable one, then open Send to…. Remount it read-write from a shell and reopen the menu.
- Clone a stick with `dd` so two carry one UUID, attach both, and open Send to….
- Send a file to a stick folder through Choose folder…, delete that folder from a shell, and reopen the stick's submenu.
- Loop-mount an image under `/mnt` and inside a mounted stick, and open an SMB share so it appears under `/run/user/$UID/gvfs`. Search Ctrl+K for a file on each.
- Mount the SFTP fixture as `SFTP://` in upper case, then `davs://` and `afp://` where reachable, beside an MTP phone and a camera; compare each row's icon and buttons.
- Read each row's accessible description over AT-SPI. Cover a mounted and an unmounted stick, the CD-ROM with a disc, an MTP phone, and the fstab virtio volume.

### devices/volumes/release

- Eject while a copy into the stick runs, while a shell sits inside the mount, and while `sleep` holds a file open there. Read each error.
- Write 500 MB to the stick, press Eject, and detach the disk over QMP while the overlay is still up.
- Eject from one window while a second window browses two levels inside the device; watch where the second pane lands.
- Hide the overlay, switch the theme accent, open Properties on the pending row, and press Eject on it again before GIO resolves.
- Attach an ISO as a CD-ROM and a non-removable virtio ext4 disk; release each and compare the closing overlay.
- Eject while the preview plays audio from the stick, while a PDF preview's sandbox holds a file there, and while Icons thumbnails load; then select a stick file before GIO resolves.
- Dump the sidebar with a removable drive, expanded and as the rail.
- Mount the SFTP fixture, browse two levels inside it in one window and at its root in a second. Disconnect it from its DEVICES row; repeat with the fixture stopped first.
- Open two windows with two tabs each, two inside the stick, one at its root, and one elsewhere, plus a portal file chooser inside it. Eject from the window browsing elsewhere.
- Hold the stick busy with a shell, Eject, and navigate one of the windows that went Home before the error shows.
- Disconnect the SFTP share while a shell sits inside its `/run/user/$UID/gvfs` path; dismiss GVfs's busy dialog, then retry and choose to unmount anyway.
- Click Disconnect twice quickly on the SFTP row, then open its row menu again while the first unmount runs.
- Set a Strata label with emoji on a stick, then Eject and Unmount it with the overlay open and hidden.

### devices/volumes/encrypted

- Enter a wrong passphrase three times, then the right one with "Remember forever"; verify the entry with `secret-tool search` under both attribute names.
- Unlock the second of two same-passphrase LUKS partitions on one disk; check which mount point the pane opens.
- Hide the "Unlocking volume" overlay and navigate to Home before unlock completes; then repeat with the pane already inside the mount.
- Lock the login keyring with `secret-tool lock`, then Lock a volume with a saved passphrase; confirm the mount and the secret both survive.
- Open the volume with `cryptsetup open` but no mount, then press Unlock and Lock on its row.
- Unmount the virtio LUKS filesystem with `udisksctl unmount`, then Lock from the row menu by keyboard instead of the row button.
- Mount the virtio LUKS volume through an fstab `noauto,user,x-gvfs-show` entry, then Lock it with and without a saved passphrase.
- Dump the sidebar with an unmounted encrypted drive and an unlocked one, expanded and as the rail.

### devices/volumes/udiskie-unlock

- Run `strata --udiskie-hook` with an empty DEVICE, with both operands empty, with an uppercase UUID, and with `device_removed`; log the argv that results.
- Start `strata --unlock-volume /dev/sdX` and attach the disk after 5 seconds, then after 9 seconds; repeat with the plain FAT stick's path.
- Install over no `~/.config/udiskie`, over a commented `config.yml` with its own `event_hook`, and over a symlinked `config.yml`. Repeat over `config.json` only and over both files; diff each restore against the copy.
- Install twice, then uninstall twice; `udiskie` must still start after each step.
- Install over a commented `config.yml`, edit one udiskie key by hand, then uninstall; repeat editing only the comments. Diff each against the copy.
- Install over a hand-indented `config.json` without a trailing newline, then uninstall with and without editing it in between.
- Install over no `~/.config/udiskie`, add an unrelated file to it, and uninstall; then repeat without adding one.
- Make udiskie unrestartable by replacing it on `PATH` with a script that exits 1, then press Use Strata and Restore default in Settings; switch pages and return.
- Run the install and uninstall flags under `LANG=hu_HU.UTF-8`, under `LANGUAGE=de` with `LANG=hu_HU.UTF-8`, and with Strata's saved language set to French.
- With a Strata window open, run `strata --unlock-volume nonsense` and `strata --unlock-volume /dev/sdX file.txt` from a second terminal; read both terminals and the journal.
- Start `strata --unlock-volume` for the plain FAT stick with it already mounted, and again from a cold start with Strata closed.
- With the handler installed and udiskie stopped, attach the LUKS disk; the stick must not automount and the prompt must name that device.
- Install with the default build, then run the package build's install and uninstall flags; diff `~/.config/udiskie` and `~/.local/share/strata` against the copy.
- Open Settings → General in the package build on the `arch` guest with `udiskie` removed from `PATH`, then on `omarchy-4`; search Settings for "udiskie" and "encrypted".
- With the package build's `--udiskie-hook` in udiskie's `event_hook`, attach the LUKS disk.

### devices/volumes/drive-dialogs

- Open the row menu on the three-partition disk's unmounted and unformatted partitions, on the CD-ROM with no disc, and on the virtio disk. Note which offer Mount, then mount one from a shell and reopen its menu.
- Open Properties on each attached device: unmounted and mounted sticks, locked and unlocked LUKS, the CD-ROM, the loop mount, and the virtio disk. Compare Capacity, Used, and Free with `df -B1`.
- Open Properties from the row menu by keyboard on each of those devices, then press Enter at once; repeat with Space and with Tab then Enter.
- Compare the Properties release button with the row's eject tooltip on a stick, the SFTP share, the virtio disk, and the CD-ROM.
- Set a label while Properties is open in a second window, then clear it; watch both subtitles.
- Add fstab `noauto` entries for the stick as `vfat`, `auto`, `exfat`, and `fuse.sshfs`, and with the type column blank; open Properties unmounted after each.
- Set label to 255 characters, emoji, RTL text, whitespace only, a pasted tab, and the same text on both same-label sticks. Then relabel one with `fatlabel` from a shell and replug.
- Delete `mkfs.exfat` only and open Format for each filesystem; then format with a label at the exact limit and a lowercase FAT label.
- On exFAT, NTFS, and FAT32, type, then paste, labels of emoji, accented Latin, CJK, and a flag sequence, at and past the limit. Paste into the middle of a label. Read the field, the caption, and `lsblk -o LABEL` after formatting.
- Type a long emoji label under NTFS, then switch to FAT32, exFAT, and NTFS. Read the field, the caption, and Continue after each switch.
- Open Format Drive, detach the disk before Continue, reattach, and press Format.
- Format while a shell sits inside the mount, and with an Eject pending on the same row. Cancel the polkit prompt at the unmount step, then at the format step.
- Open the unlocked LUKS volume's Properties and Format Drive after `dmsetup suspend` on its mapping; close each before its facts arrive, then `dmsetup resume`.
- Replug another stick while Format Drive loads its facts, and again while it formats.
- Dump the tree with the drive Label and Format Drive dialogs open.
- Attach the virtio LUKS disk and its `dd` clone, unlock one, unmount its filesystem from a shell, and Lock it. Check which mapping `lsblk` shows closed.
- Open the virtio LUKS mapping as another user with `udisksctl unlock`, then Lock it in Strata. Dismiss the polkit prompt with Escape, then with its close button, then let it time out; finally authorize.
- Unmount the virtio LUKS filesystem from a shell, then restart udisks2 and Lock at once; repeat with udisks2 stopped.

### devices/volumes/camera

- Switch the camera between PTP and mass-storage mode while Strata is open; both entries may exist at once.
- Scan a store of 5,000 photos across DCIM folders with duplicate names; scroll, press F5, and switch views and sort fields mid-scan.
- Lock the iPhone, then detach it over USB, each during a scan; read the error and the rows left behind.
- Copy 50 photos to the stick during the scan, then Eject the stick; preview one HEIC and delete one of a duplicate pair.
- Add a dot-prefixed folder of photos on the device and toggle hidden files during and after the scan.
- Put `.CRW`, `.Arq`, and `.k25` files, a `.GPR` beside its `.JPG`, and a `.ptx` in one DCIM folder on the device; compare the Photos rows with `gio list`.

## Hand-offs

- The Send to… submenu rows, Choose folder…, and copying to a device → `operations`.
- The "Writing to device…" flush before a copy to removable media reports success → `operations`.
- Device rows as navigation targets, sidebar keyboard order, and drops onto rows → `browser`.
- SMB, SFTP, and other network mounts with their credential prompts → `remote`.
- `install.sh` step wording, its default selection, `--with-udiskie-unlock`, `--without-udiskie-unlock`, and Omarchy detection → `app`.
- Previewing camera photos in the preview panel → `preview`.
- The Settings page shell around the "Unlock encrypted volumes" row → `settings`.
