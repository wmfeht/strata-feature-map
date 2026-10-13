---
nodes:
  - app/packaging
  - app/packaging/installer
  - app/packaging/aur
  - app/updates
  - app/updates/install
  - app/updates/package-managed
  - app/updates/release-channels
  - integration/file-manager-interface
  - integration/portal-file-chooser/setup
  - devices/volumes
  - devices/volumes/udiskie-unlock
  - devices/volumes/camera
  - browser/navigation
  - browser/navigation/startup-arguments
  - browser/navigation/location-bar
  - browser/search
  - browser/search/filter
  - browser/view-modes/list
  - operations/undo
  - operations/rename
  - preview/quick-preview
  - preview/preview-panel
  - preview/preview-panel/layout
  - integration/10xer-mode
  - integration/10xer-mode/preview-keys
  - remote/file-providers/network-locations
reviewed_at: 0a086aa3bdb251842a1e8413e2a6b35970d0b409
---

# Installation and desktop integration

## Installation

<!-- node: app/packaging/installer -->
<!-- node: integration/portal-file-chooser/setup -->
<!-- node: devices/volumes/udiskie-unlock, Settings and installer -->
<!-- node: devices/volumes, Discovery -->
<!-- node: integration/file-manager-interface, Activation and installation -->
<!-- node: app/packaging, Desktop entry and icon -->
<!-- node: app/updates/install -->
<!-- node: app/updates/package-managed -->

Arch Linux and Omarchy are the primary supported environments. Current binaries require **glibc 2.39 or newer** and the runtime libraries listed below.

### Interactive installation

The interactive installer detects the Linux architecture, glibc version, Arch
Linux, and Omarchy 3 or 4. It installs the latest verified stable release and
offers optional desktop-menu, default-folder-handler, "Open file location", system
file chooser, encrypted-volume unlock, SMB, broader image/RAW, and Omarchy keybind
integration:

```bash
curl -fsSL https://raw.githubusercontent.com/lgse/strata/main/install.sh | bash
```

The installer shows every privileged package operation before asking to run it.
It verifies both the published SHA-256 digest and GitHub Actions provenance before
installing anything from the release archive. The binary is installed per-user at
`~/.local/bin/strata`.

For an unattended Arch or Omarchy installation, pass `--non-interactive`. This
installs required dependencies and the binary without prompting; optional
integrations remain disabled unless explicitly selected:

```bash
curl -fsSL https://raw.githubusercontent.com/lgse/strata/main/install.sh \
  | bash -s -- --non-interactive \
      --with-smb \
      --with-raw \
      --with-desktop-entry \
      --with-folder-association \
      --with-omarchy-keybinds \
      --with-udiskie-unlock
```

Each `--with-*` flag implies `--non-interactive`, and folder association implies
the desktop entry and `--with-file-manager`. Use `--with-file-manager` by itself
to enable only "Open file location" integration. File chooser replacement is
separate: use `--with-file-chooser` to opt in, or `--without-file-chooser` to keep
your current chooser and dismiss the one-time in-app offer. Neither folder
association nor an unattended install enables the chooser automatically.
Encrypted-volume unlock is offered on Omarchy 3 or 4 (the installer asks; default
No), and on generic Arch only when `udiskie` is already on `PATH`. The installer
never installs the `udiskie` package. Unattended installs need
`--with-udiskie-unlock`; `--non-interactive` alone and other `--with-*` flags
leave it declined. Restore on Arch with `strata --uninstall-udiskie-unlock`, not
Settings.

Non-interactive package installation requires passwordless sudo or cached credentials. Run `./install.sh --help` for the full option list.

Phone backends are not installed by the script. For optional iPhone/iPad or Android
access, follow [Connecting phones](#connecting-phones) after installation.

### AI-assisted installation

Use this option to have a coding agent install and verify the latest release archive.

Give this prompt to a coding agent with terminal access:

```text
Install the latest stable Strata release from https://github.com/lgse/strata safely.

Before changing anything:
1. Confirm this is a glibc-based Linux system with a graphical GTK4 environment.
2. Detect whether the machine is x86_64 or aarch64 and select only the matching
   *-unknown-linux-gnu archive from the canonical lgse/strata GitHub release.
3. Show me the runtime packages you need and ask before using sudo or changing
   my default file-manager association.

Then:
- Install the required GTK4, GtkSourceView 5, Poppler GLib, Fontconfig, Bubblewrap,
  FFmpeg/GStreamer, and desktop-integration runtime dependencies using the system
  package manager. Add gvfs-smb only if I want SMB support.
- Ask whether I want phone access. On Arch/Omarchy, add gvfs-afc and usbmuxd for
  iPhone/iPad app documents, gvfs-gphoto2 for camera/PTP photo access, or gvfs-mtp
  for Android file transfers, only if requested. Other distributions need their
  equivalent GVfs backends.
- Download the archive and its matching .sha256 file from the latest GitHub release.
- Verify the checksum with sha256sum --check. If GitHub CLI is installed and
  authenticated, also verify GitHub Actions provenance with
  `gh attestation verify <archive> --repo lgse/strata`. Stop if either attempted
  verification fails; never install a binary with an invalid checksum.
- Extract it and install `strata` to ~/.local/bin/strata without overwriting an
  unrelated file. Ensure ~/.local/bin is on PATH.
- Ask whether I want a per-user desktop entry and inode/directory association;
  if yes, install the archive's io.github.lgse.Strata.desktop and io.github.lgse.Strata.svg
  under ~/.local/share, pointing Exec at the installed binary, then refresh the
  desktop database and icon cache.
- Separately ask whether Strata should handle "Open file location" requests. If
  yes, verify no other per-user service provides org.freedesktop.FileManager1,
  then install the archive's io.github.lgse.Strata.FileManager1.service under
  ~/.local/share/dbus-1/services with Exec pointing at the installed binary.
- Ask before editing udiskie config to use Strata for encrypted-volume unlock.
  Do not install the udiskie package. Do not send Arch users to Settings for
  this row; restore on Arch with `strata --uninstall-udiskie-unlock`.
- Launch `strata`, report its installed version/source release, and verify the
  desktop association if one was requested. Do not weaken the preview sandbox.
```

### Manual installation

Install the release archive directly if you prefer to perform each step yourself.

#### 1. Check the architecture and install dependencies

```bash
case "$(uname -m)" in
  x86_64)  target=x86_64-unknown-linux-gnu ;;
  aarch64) target=aarch64-unknown-linux-gnu ;;
  *) echo "Strata has no prebuilt release for $(uname -m)" >&2; exit 1 ;;
esac
printf 'Use the %s release archive.\n' "$target"
getconf GNU_LIBC_VERSION   # must report glibc 2.39 or newer
```

On Arch Linux or Omarchy:

```bash
sudo pacman -S --needed bubblewrap ffmpeg ffmpegthumbnailer fontconfig \
  gstreamer gst-libav gst-plugins-base gst-plugins-good gtk4 gtksourceview5 gvfs poppler-glib
# Optional SMB, AppImage icon, and broader camera RAW support:
sudo pacman -S --needed gvfs-smb imagemagick libraw dcraw squashfs-tools
```

GTK **4.12 or newer** and glibc **2.39 or newer** are required. Other glibc-based distributions may work when they provide equivalent runtime libraries, but their package names and binary compatibility vary. Systems with an older glibc must [build Strata from source](https://github.com/lgse/strata/blob/main/README.md#development-and-documentation).

Device discovery requires the GVfs UDisks2 volume monitor (`gvfs` on Arch and
Fedora; `gvfs-daemons` on Debian/Ubuntu). Without that backend, removable drives
may be absent from Devices. SMB support remains optional. Phones need additional
backends; see [Connecting phones](#connecting-phones).

#### 2. Download and verify

From the [latest release](https://github.com/lgse/strata/releases/latest), download the `.tar.gz` matching `$target` and its identically named `.sha256` file over HTTPS. Then verify its digest:

```bash
cd ~/Downloads
archive="strata-<version>-${target}.tar.gz"
sha256sum --check "${archive}.sha256"
```

If GitHub CLI is installed and authenticated, you can additionally verify the
archive's signed GitHub Actions provenance before extracting it:

```bash
gh attestation verify "$archive" --repo lgse/strata
```

Every verification you run must succeed. Extract the archive, install the binary,
and confirm it starts:

```bash
tar -xzf "$archive"
install -Dm755 "${archive%.tar.gz}/strata" "$HOME/.local/bin/strata"
command -v strata
strata
```

If `command -v` fails, add `$HOME/.local/bin` to your shell's `PATH`. Every archive contains `SOURCE_COMMIT`, identifying the exact source revision used by GitHub Actions.

#### Debug a release crash

Download the matching `strata-<version>-<target>.debug` asset from the same release and place it beside the installed `strata` binary, keeping its filename unchanged. Then run `coredumpctl debug strata`; GDB will load its Rust function names and source lines.

#### 3. Update or uninstall

In-app updates verify [signed release manifests](signed-updates.md) inside Strata, without `gh`, a GitHub account, or a token. Releases published before signed manifests were introduced require manual installation; the updater never falls back to checksum-only verification.

For a manual installation, use **Settings → Updates** for verified in-app updates, or repeat the download, verification, and `install` steps for a newer release. An in-app update also refreshes an already installed desktop entry and application icon from the new archive; it never creates desktop metadata that was not installed before. If the user opted into Strata's system file chooser, the update restarts the portal frontend so subsequent dialogs use the newly installed build. Package-managed installations are updated only by their system package manager. To remove a per-user installation, run `strata --uninstall-udiskie-unlock` before deleting the binary if you opted into encrypted-volume unlock, then:

```bash
rm -f ~/.local/bin/strata \
  ~/.local/share/applications/io.github.lgse.Strata.desktop \
  ~/.local/share/dbus-1/services/io.github.lgse.Strata.FileManager1.service \
  ~/.local/share/icons/hicolor/scalable/apps/io.github.lgse.Strata.svg
update-desktop-database ~/.local/share/applications 2>/dev/null || true
gtk-update-icon-cache -qtf ~/.local/share/icons/hicolor 2>/dev/null || true
```

User preferences and custom themes remain under the XDG configuration directories so an uninstall does not destroy personal settings.

## Usage and desktop integration

<!-- node: browser/navigation/startup-arguments -->
<!-- node: app/packaging, Version -->
<!-- node: browser/search -->
<!-- node: browser/search/filter -->
<!-- node: browser/navigation/location-bar -->
<!-- node: operations/undo -->
<!-- node: preview/quick-preview -->
<!-- node: operations/rename -->
<!-- node: browser/navigation, Back, Forward, and Parent -->
<!-- node: integration/10xer-mode, Entering and leaving -->
<!-- node: integration/10xer-mode/preview-keys, Opening and leaving -->
<!-- node: preview/preview-panel/layout, Narrow windows -->
<!-- node: app/packaging, Desktop entry and icon -->
<!-- node: integration/file-manager-interface -->
<!-- node: app/packaging/aur, Packages -->
<!-- node: app/packaging/installer, Omarchy keybinds -->
<!-- node: devices/volumes/udiskie-unlock -->
<!-- node: devices/volumes, Discovery -->
<!-- node: devices/volumes/camera -->
<!-- node: preview/preview-panel, Images and PDFs -->
<!-- node: browser/view-modes/list -->
<!-- node: remote/file-providers/network-locations -->

Launch Strata with an optional local directory:

```bash
strata                      # home directory
strata ~/Documents          # a specific directory
strata --unlock-volume DEVICE  # unlock an encrypted volume
strata --install-udiskie-unlock   # install Strata as the udiskie unlock handler
strata --uninstall-udiskie-unlock # restore the previous udiskie configuration
strata --version            # print the installed version
```

In the default map, useful shortcuts include Ctrl+K for recursive search, Ctrl+L for a path or URI, Ctrl+F to filter the current pane, Ctrl+Z to undo or Ctrl+Shift+Z to redo the latest reversible file operation, Space for preview, F2 to rename, and Alt+arrow keys for history and parent navigation.

Toggle [10xer mode](10xer-mode.md) with Ctrl+Shift+M for Yazi-style navigation and footer prompts; `q` returns to the default map. In 10xer mode, `l`/→ enters preview, `h` returns to the listing without closing it, and `i` toggles it.

In narrow or highly scaled windows, the file view takes priority: the preview shrinks, then hides when there is not enough room for both. Widening the window restores the preview and its session width automatically. Hidden previews pause playback and defer loading new selections; unchanged previews return without reloading the file.

### Desktop entry

Every release archive ships `io.github.lgse.Strata.desktop` and the Strata application icon `io.github.lgse.Strata.svg`. Install both to give Strata a per-user launcher with its own icon in launchers, docks, task switchers, and window overviews, and optionally make Strata the default directory handler:

```bash
cd ~/Downloads/"${archive%.tar.gz}"
install -Dm644 io.github.lgse.Strata.svg \
  ~/.local/share/icons/hicolor/scalable/apps/io.github.lgse.Strata.svg
install -d ~/.local/share/applications
sed "s|^Exec=strata |Exec=$HOME/.local/bin/strata |" io.github.lgse.Strata.desktop \
  > ~/.local/share/applications/io.github.lgse.Strata.desktop
update-desktop-database ~/.local/share/applications
gtk-update-icon-cache -qtf ~/.local/share/icons/hicolor 2>/dev/null || true
xdg-mime default io.github.lgse.Strata.desktop inode/directory
xdg-mime query default inode/directory
```

The final command should print `io.github.lgse.Strata.desktop`. The desktop entry's filename matches the `io.github.lgse.Strata` application ID that Strata's windows report, so desktop shells match a running window to this entry and draw its `Icon` value. Log out and back in if a shell caches launcher icons.

When building from source, `mise run install-local` installs the binary, icon, and desktop entry in the same locations, and `mise run uninstall-local` removes them.

### "Open file location" from other applications

Browsers and GTK/GNOME applications reveal a file by calling the `org.freedesktop.FileManager1` D-Bus interface instead of consulting the `inode/directory` association. The interactive installer offers this separately; for unattended installation, pass `--with-file-manager`. Folder association enables it automatically.

For a source installation, enable Strata as the per-user activatable provider explicitly:

```bash
mise run install-file-manager
```

For an AUR package, copy its inactive service template into your per-user service directory:

```bash
install -Dm644 /usr/share/strata/io.github.lgse.Strata.FileManager1.service \
  ~/.local/share/dbus-1/services/io.github.lgse.Strata.FileManager1.service
```

For a release archive installation, install the included service manually instead:

```bash
cd ~/Downloads/"${archive%.tar.gz}"
install -d ~/.local/share/dbus-1/services
sed "s|^Exec=/usr/bin/strata |Exec=$HOME/.local/bin/strata |" \
  io.github.lgse.Strata.FileManager1.service \
  > ~/.local/share/dbus-1/services/io.github.lgse.Strata.FileManager1.service
```

A per-user provider takes precedence over system providers shipped by other file managers. Before enabling Strata manually, remove any other per-user service whose `Name` is `org.freedesktop.FileManager1`; two providers for the same name in one service directory are chosen arbitrarily. If another file manager already owns the bus name, exit it before testing. Use `mise run uninstall-file-manager` for a source installation, or remove the per-user service file, to disable Strata again.

Strata then answers `ShowFolders`, `ShowItems`, and `ShowItemProperties`, opening the directory that holds the named items with those items selected:

```bash
busctl --user call org.freedesktop.FileManager1 /org/freedesktop/FileManager1 \
  org.freedesktop.FileManager1 ShowItems ass 1 "file://$HOME/Downloads" ""
```

### Make Strata the Omarchy file manager

The XDG association above handles folders opened by applications. On current Lua-based Omarchy releases, also override the stock Nautilus shortcuts in `~/.config/hypr/bindings.lua` so Omarchy launches Strata directly.

First inspect the active bindings and back up your user configuration:

```bash
omarchy menu keybindings --print | grep -i "file manager"
cp ~/.config/hypr/bindings.lua ~/.config/hypr/bindings.lua.bak.$(date +%s)
```

Append these overrides to `~/.config/hypr/bindings.lua`:

```lua
-- Use Strata instead of Nautilus for Omarchy's file-manager shortcuts.
hl.unbind("SUPER + SHIFT + F")
hl.unbind("SUPER + ALT + SHIFT + F")
o.bind("SUPER + SHIFT + F", "File manager", { launch = "strata" })
o.bind("SUPER + ALT + SHIFT + F", "File manager (cwd)",
  "uwsm-app -- strata \"$(omarchy-cmd-terminal-cwd)\"")
```

The stock shortcut is Super+Shift+F, not Ctrl+Shift+F. To support the Ctrl chord too, first confirm that it is not assigned to another action, then optionally append:

```lua
o.bind("CTRL + SHIFT + F", "File manager", { launch = "strata" })
```

Apply and validate the configuration:

```bash
hyprctl reload
hyprctl configerrors
omarchy menu keybindings --print | grep -i "file manager"
```

`hyprctl configerrors` should produce no errors. These user overrides survive Omarchy updates; do not edit files under `/usr/share/omarchy/`.

### Unlock encrypted volumes on Omarchy

On Omarchy 3 or 4, the installer asks whether to use Strata for encrypted-volume unlock (default No). **Settings → General → Desktop integration** includes **Unlock encrypted volumes**. Choose **Use Strata** so plugging in an encrypted drive opens Strata's password prompt instead of udiskie's dialog. **Restore default** returns udiskie to its previous configuration.

On generic Arch, the installer offers the same step only when `udiskie` is already on `PATH`. Restore there with `strata --uninstall-udiskie-unlock`; Settings for this row stays Omarchy-only.

The same setup is available unattended:

```bash
strata --install-udiskie-unlock
strata --uninstall-udiskie-unlock
```

This edits `~/.config/udiskie/config.yml` and records restore state in `~/.local/share/strata/udiskie-install/state.toml`. It is not a saved Strata preference. The Settings row appears only when Omarchy is detected and `udiskie` is on your `PATH`; the CLI flags are unattended and are not Omarchy-gated. Unattended installer opt-in is `--with-udiskie-unlock`.

### Connecting phones

Strata discovers and mounts phones through GIO/GVfs. The required phone backends
are optional and are not installed by `install.sh`. On Arch Linux or Omarchy,
install only the support you need:

```bash
# iPhone or iPad app documents (AFC):
sudo pacman -S --needed gvfs-afc usbmuxd
# Camera/PTP photo access, including compatible iPhones:
sudo pacman -S --needed gvfs-gphoto2
# Android (MTP):
sudo pacman -S --needed gvfs-mtp
```

Other distributions need equivalent GVfs AFC, gphoto2/PTP, or MTP backends;
package names vary.

- **iPhone/iPad:** unlock the device, connect it with a USB data cable, and accept
  **Trust This Computer** (enter the device passcode if requested). AFC can expose
  an app document-sharing view containing folders named after apps; this is not
  the photo library. For photos, install the gphoto2 backend and look for a
  separate camera/device entry with **DCIM**, if exposed by the phone. Accept any
  photo-access prompt. Photos stored only in iCloud may not be available over USB.
  Access depends on the iOS version and backend support; iOS does not expose
  unrestricted internal storage.
- **Android:** unlock the device, connect it with a USB data cable, and select
  **File transfer / Android Auto** or **MTP** in its USB preferences rather than
  charging-only mode. Accept any file-access prompt. Only storage exposed by the
  phone is available, not protected system files or private app data.

After installing a backend, fully quit Strata (all windows) and reopen it.
Reconnect the unlocked phone if necessary, then click its entry under **Devices**.
The camera/PTP entry opens a single **Photos** view: files appear progressively
from storage/date folders, prioritizing newer date-folder names, without requiring
you to open each folder. The backend may finish a folder's metadata before
returning its first batch. This is
a virtual listing of JPEG, HEIC/HEIF, MOV, MP4, and recognized camera RAW files,
not a reorganization of the phone. Sidecars such as `.AAE` and other formats are
hidden only from this Photos view; their originals remain untouched and visible
in normal folder browsing. Duplicate filenames remain
separate files with their original locations; use **Copy path** or **Properties**
to distinguish their sources. Preview, copy, and delete act on those originals.
This is the USB-exposed collection, not iOS's Albums hierarchy. The current
backend does not provide album membership for a reliable Albums/Camera Roll split.

Camera batches yield to interface input and redraws. In List view, file-type
grouping is applied after discovery finishes; the saved grouping setting is
preserved while the live listing stays ungrouped.

Discovery reads metadata, not every photo's contents. It skips symlinks, avoids
revisiting discovered directories, and preserves hidden-file filtering. Photos
keeps loading in batches until the whole exposed library is indexed, you navigate
away or refresh, or the device reports an error. There is no overall scan
deadline or fixed file, folder, or nesting limit. Refresh to rescan after a
phone-side change; not every device supports live change notifications.

Android MTP and iPhone app-document/AFC entries retain normal folder browsing.
For Android, open **Internal storage** (the label varies by device).

Still photos (including HEIC) and MOV/MP4 videos can use the preview pane or
Space quick preview directly from the phone, without a manual copy.
Strata first downloads a private temporary input for sandboxed decoding: up to
64 MiB in 30 seconds for images or 256 MiB in 60 seconds for videos, with at most
four staged inputs per process. Video playback waits for that download, then
reuses it for seeking and resizing. Closing or changing the preview cancels the
request; temporary files are removed after the player and its workers release
them. Remote PDFs, animated GIFs, audio, and other video formats still need a
local copy for preview. HEIC decoding requires an installed HEIC-capable image
decoder, such as ImageMagick with libheif. Camera/PTP thumbnails use small previews
provided by the camera, with bounded retrieval and sandboxed decoding; if the
camera cannot supply a thumbnail, Strata keeps the file icon instead of downloading
the original. Camera thumbnails are cached only in memory. See
[Remote previews](preview-sandbox.md#remote-still-image-previews)
for cleanup, caching, and sandbox details.

If the phone is missing, check the backend package, try another data cable or USB
port, and confirm the trust/file-transfer setting. On Arch/Omarchy, `lsusb` (from
`usbutils`) can confirm USB detection, but detection alone does not establish file
access. For iPhone/iPad, also check `systemctl status usbmuxd.service` while the
phone is connected. If the newly installed backend still is not discovered after
restarting Strata, log out and back in to refresh the desktop's GVfs services.

#### iPhone appears but photo storage is empty

Some recent iPhones can expose an empty camera/PTP store with libgphoto2 2.5.34,
even when unlocked, trusted, and holding locally stored photos. This is a known
[upstream libgphoto2 issue](https://github.com/gphoto/libgphoto2/issues/1254), not
necessarily an empty photo library or a Strata display problem. The backend
mishandles the folder-parent information returned by these devices.

A read-only test with an iPhone reporting iOS 26.6.1 reproduced the problem:
unmodified libgphoto2 2.5.34 listed **0 folders**, while the same version with
[upstream fix `9f5d4f9`](https://github.com/gphoto/libgphoto2/commit/9f5d4f9ca0a7f58bac7987180a48154ea07c090f)
listed **117 folders**. Both builds were temporary, with their actual library
loading verified; no photos were downloaded or modified. This confirms folder
listing with the fix on that device, not complete transfer or Strata GUI coverage.

Use a distribution libgphoto2 update or backport containing that fix when
available. Merely reinstalling `gvfs-gphoto2` or restarting Strata will not fix an
affected libgphoto2 build. Strata's GVfs camera backend must load the corrected
library; setting library paths only for Strata may not affect the separately
launched GVfs process. This documentation change does **not** bundle or install
the fix. Avoid replacing system libraries manually; any locally built workaround
should be isolated and reversible.

### Network shares

Press Ctrl+L, enter an address such as `smb://server/share` or `sftp://user@host:2222/path`, and press Enter. Strata uses GIO/GVfs and prompts for credentials when required. Remote protocols need their GVfs backend installed; distributions split these up differently, so check yours for the SMB backend (`gvfs-smb` on Arch) and the SFTP backend (part of `gvfs` on Arch, `gvfs-backends` on Debian and Ubuntu).

SFTP accepts password and SSH-key authentication. Encrypted keys can be unlocked in your SSH agent; if GVfs asks Strata for a key passphrase or host-key decision, Strata presents the request without deciding for you. See [SFTP locations](remote-sftp.md).

## Release channels

<!-- node: app/updates/release-channels -->
<!-- node: app/updates, Checking -->
<!-- node: app/updates/package-managed, Checking -->

Strata defaults to the **Stable** channel: only final tagged releases are ever offered, and a Stable install never receives, sees, or is notified about a prerelease.

Strata checks for updates automatically by default: each time it starts, once its first window opens, and again when a window or **Settings → Updates** opens if no check has completed in the last 24 hours. Turning **Check for updates automatically** back on, or changing the channel, also runs a check. The check asks the update source for your installation: GitHub for release binaries and source builds, the AUR for AUR packages, the Omarchy package repository for Omarchy packages, or the local pacman sync database for other pacman packages. When a newer version is found, Strata also fetches that release's details from GitHub. Turning the switch off stops the automatic checks, discards the result of a check still running, hides any update notice already shown, and locks the channel. **Check now** still checks on demand, and the Updates page's release-notes card asks GitHub for the current version's notes when they are not already cached. Strata never downloads or installs an update without your confirmation.

To try upcoming changes early, choose a channel in **Settings → Updates** (the channel is locked while automatic checks are off). **Preview** receives curated alpha, beta, and release-candidate builds but excludes nightlies. **Nightly** receives every recognised prerelease, including daily development builds. The update dialog and release notes always identify the exact build kind.

When a prerelease installation selects **Stable**, the Updates card immediately offers the newest stable release as the channel target—even when that requires a semantic downgrade—and labels the action **Return to stable**. Preview and Nightly selections use the same card for ordinary forward updates, so channel changes never create a separate competing rollback card.

See [Releasing](https://github.com/lgse/strata/blob/main/docs/releasing.md) for the tag grammar these channels rely on and, for maintainers, how a release candidate is cut and promoted.
