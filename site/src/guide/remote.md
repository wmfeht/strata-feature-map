---
nodes: [remote/file-providers, remote/file-providers/network-locations, devices/volumes, devices/volumes/camera, devices/volumes/encrypted, devices/volumes/release]
reviewed_at: 0a086aa3bdb251842a1e8413e2a6b35970d0b409
---

# Remote and devices

Open network shares, SFTP servers, phones, cameras, and USB drives in the same
browser as your local files. Strata mounts them through GIO/GVfs on demand.

## Open an SMB share

<!-- node: remote/file-providers -->
<!-- node: remote/file-providers/network-locations, Mounting and sign-in -->
<!-- node: remote/file-providers/network-locations, Sidebar -->
<!-- node: remote/file-providers/network-locations, Failures -->

On Arch or Omarchy, install the SMB backend first:

```bash
sudo pacman -S --needed gvfs-smb
```

Press Ctrl+L, type `smb://server/share`, and press Enter. Strata mounts the
share and opens it.

If the server wants credentials, **Authentication required** shows only the
fields it asks for, such as **Username**, **Domain**, and **Password**. For a
guest share, choose **Anonymous** under **Connect as** when offered. **Password
storage** defaults to **Don't remember**; **Until logout** or **Forever** hands
the password to your desktop keyring. Click **Connect**.

To browse instead, click **Network** in the sidebar, then a host, then a share.
A mounted share appears under **DEVICES**; right-click it and choose
**Disconnect** when done.

## Connect over SFTP

<!-- node: remote/file-providers/network-locations, SFTP -->

Press Ctrl+L and enter one of these:

```text
sftp://host/path
sftp://user@host/path
sftp://user@host:2222/path
```

These connect as your local user on port 22, as `user`, and as `user` on port
2222.

With your key in an SSH agent, or an unencrypted key, the folder opens with no
prompt. Load an encrypted key into the agent first:

```bash
ssh-add ~/.ssh/id_ed25519
```

Otherwise Strata asks for a password, or shows **Passphrase required** when
GVfs requests your key's passphrase.

## Trust a host key

<!-- node: remote/file-providers/network-locations, SFTP -->

On a first connection, or when a server's key changes, Strata shows **Verify
server identity**. It repeats the backend's question and offers the backend's
own buttons. Strata never answers for you.

Verify the fingerprint with the server's administrator, outside Strata,
before you continue. A changed key can mean interception. Decline with the
rejecting button or Escape, and Strata returns to the previous folder.

## Connect a phone or camera

<!-- node: devices/volumes, Discovery -->
<!-- node: devices/volumes/camera, Photos view -->
<!-- node: devices/volumes/camera, Order -->
<!-- node: devices/volumes/camera, Thumbnails and scrolling -->

Phone backends are optional. On Arch or Omarchy, install what you need:

```bash
# iPhone or iPad app documents (AFC):
sudo pacman -S --needed gvfs-afc usbmuxd
# Camera/PTP photo access, including compatible iPhones:
sudo pacman -S --needed gvfs-gphoto2
# Android (MTP):
sudo pacman -S --needed gvfs-mtp
```

Quit every Strata window and reopen it. Unlock the phone and connect a USB data
cable. On an iPhone, accept **Trust This Computer**; on Android, choose file
transfer in the phone's USB preferences. Click the phone under **DEVICES**.

A camera entry opens one flat **Photos** view of every JPEG, HEIC, MOV, MP4,
and recognized RAW file. Android and iPhone app-document entries browse as
normal folders.

Good to know:

- Photos lists files in discovery order. Choose **Name** or **Modified** in the
  sort menu to reorder.
- Copy, preview, and delete act on the originals on the phone.
- Thumbnails are the camera's own previews; without one, the file keeps its icon.
- Some iPhones show an empty photo store until your distribution ships a fixed
  libgphoto2.

## Mount, unlock, and eject drives

<!-- node: devices/volumes, Mounting -->
<!-- node: devices/volumes/encrypted, Unlocking -->
<!-- node: devices/volumes/encrypted, Locking -->
<!-- node: devices/volumes/release, Releasing -->
<!-- node: devices/volumes/release, Outcome -->

Plugged-in drives appear under **DEVICES**. Click an unmounted one to mount and
open it.

An encrypted drive shows a lock button. Click the row or the button, then enter
the passphrase in **Passphrase required**. To lock it, click the open-lock
button, or right-click and choose **Lock**. If its passphrase is saved, Strata
asks **Forget saved password?**; **Forget and lock** removes it and locks.

To remove a drive, click its eject button, or right-click and choose **Eject**
(**Unmount** on drives that cannot eject). Strata flushes pending writes first;
the row shows a spinner until the release finishes. Unplug once the spinner
stops with no error. A slow release opens a progress window; **Hide** dismisses
it without stopping the release. If it is open when an eject finishes, it shows
**Safe to remove**.

**Full detail:** [SFTP locations](../reference/remote-sftp.md),
[Installation and desktop integration](../reference/install.md)
