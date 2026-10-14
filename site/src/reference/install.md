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
<!-- node: app/packaging/aur -->

Arch Linux and Omarchy are the primary supported environments. Current binaries require **glibc 2.39 or newer** and the runtime libraries listed below. Strata targets 64-bit Linux on Wayland. GTK may use another display backend the host provides, but Wayland is the primary display stack.

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
It always checks the archive against its published `.sha256` file before
extracting anything. When GitHub CLI is installed and logged in, it also runs
`gh attestation verify`, and a failed check stops the install. Without `gh`, or
with `gh` logged out, it warns ("continuing after HTTPS download and checksum
verification") and continues. The binary is installed per-user at
`~/.local/bin/strata`.

For an unattended Arch or Omarchy installation, pass `--non-interactive`. This
installs required dependencies and the binary without prompting; optional
integrations remain disabled unless explicitly selected. For example, on Omarchy:

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

`--with-omarchy-keybinds` requires Omarchy 3 or 4, and `--with-udiskie-unlock`
requires `udiskie` on `PATH`. On generic Arch, leave out the flags that do not
apply. Otherwise the installer exits with an error after it has installed the
binary and any integration it set up before that flag's step.

Each `--with-*` flag and `--without-file-chooser` implies `--non-interactive`,
and integrations you do not name are declined. An unknown option exits with
"Unknown option: \<option> (run with --help for usage)." Folder association implies
the desktop entry and `--with-file-manager`. Use `--with-file-manager` by itself
to enable only "Open file location" integration. File chooser replacement is
separate: use `--with-file-chooser` to opt in, or `--without-file-chooser` to keep
your current chooser. You can set it up later in **Settings → General → DESKTOP
INTEGRATION → System file manager** (see [Set up from Settings](#set-up-from-settings)). Neither folder
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

#### System checks and dependencies

Run the installer as your normal desktop user. Run as root, it exits with "Run
this installer as your normal desktop user, not as root." An interactive run
needs a terminal; without one it exits with "This interactive installer needs a
terminal." Under `curl … | bash`, every prompt, including pacman's, reads from
the terminal. On a system other than Linux it exits with "The prebuilt Strata
release supports Linux only." On a machine other than x86_64 or aarch64 it exits
with "Strata has no prebuilt release for \<machine>." On a Linux system without
glibc it exits with "Strata requires a glibc-based Linux system." With glibc
older than 2.39 it exits with "Strata requires glibc 2.39 or newer (found
\<version>)."

It then prints the detected Linux distribution, the architecture (as the release
target), the glibc version, and "Omarchy: major version N" or "Omarchy: not
detected". The Omarchy major version is the first `3.N` or `4.N` in the output of
`omarchy version`, then in `/usr/share/omarchy/version`, then in
`~/.local/share/omarchy/version`. Output such as `dev (b280f130)` or `Omarchy
2.3.1` counts as not detected.

On Arch, an Arch derivative, or Omarchy, it lists missing required packages and
asks "Install these packages with sudo pacman?" (default Yes). It then asks
separately about SMB support (`gvfs-smb`) and broader image and camera RAW support
(`imagemagick`, `libraw`, `dcraw`), each defaulting to No. On other distributions
it lists the required libraries, including the GVfs UDisks2 volume monitor, and
exits unless you confirm they are installed. `--non-interactive` exits there with
"Non-interactive dependency installation currently supports Arch-based systems
only."

#### Install and integration prompts

The installer always installs the latest stable release. If GitHub's latest
release tag is not shaped `vX.Y.Z`, it exits with "GitHub returned an unexpected
stable release tag: \<tag>". An archive missing the
`strata` binary, the desktop entry, or the icon is rejected before installation.
If `~/.local/bin/strata` already exists, it asks "Replace the existing …?"
(default No). An unattended run exits instead: "… already exists; remove it or
run the interactive installer to replace it."

"Add Strata to your desktop application menu?" defaults to Yes. The installer
writes the entry, the icon, and the "Open file location" service under
`${XDG_DATA_HOME:-~/.local/share}`, in `applications/`,
`icons/hicolor/scalable/apps/`, and `dbus-1/services/`, with `Exec=` set to
`~/.local/bin/strata`. Only after a Yes
does it ask "Make Strata the default application for opening folders?", which
defaults to No. Accepting it also installs the "Open file location" service
without asking. If `xdg-mime` still reports another folder handler afterwards,
the installer exits with an error. When you decline the menu entry or folder
association, it asks separately 'Use Strata for "Open file location" from other
applications?' (default No).

The questions about the system file chooser, Omarchy keybinds, and
encrypted-volume unlock each default to No. The Omarchy keybind question is asked
even when Omarchy is not detected; answering Yes there exits with
"--with-omarchy-keybinds requires Omarchy 3 or 4."

The file chooser question reads "Replace your current Open/Save chooser with
Strata in portal-aware apps? (Restarts the portal service; close open file
dialogs first.)" Accepting it, or passing `--with-file-chooser`, restarts the
portal service. On Arch, an Arch derivative, or Omarchy, it first installs
`xdg-desktop-portal` if that package is missing.

The installer finishes by printing the installed version, the archive's source
commit, and the binary path. It warns when `~/.local/bin` is not on `PATH`.

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
sudo pacman -S --needed bubblewrap desktop-file-utils ffmpeg ffmpegthumbnailer fontconfig \
  gstreamer gst-libav gst-plugins-base gst-plugins-good gtk4 gtksourceview5 gvfs poppler-glib \
  xdg-utils
# Optional SMB and broader camera RAW support, plus squashfs-tools:
sudo pacman -S --needed gvfs-smb imagemagick libraw dcraw squashfs-tools
```

GTK **4.12 or newer** and glibc **2.39 or newer** are required. Other glibc-based distributions may work when they provide equivalent runtime libraries, but their package names and binary compatibility vary. Systems with an older glibc must [build Strata from source](https://github.com/lgse/strata/blob/v1.0.0/README.md#development-and-documentation).

Device discovery requires the GVfs UDisks2 volume monitor (`gvfs` on Arch and
Fedora; `gvfs-daemons` on Debian/Ubuntu). Without that backend, removable drives
may be absent from **DEVICES**. SMB support remains optional. Phones need additional
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

For a manual installation, use **Settings → Updates** for verified in-app updates, or repeat the download, verification, and `install` steps for a newer release. When `${XDG_DATA_HOME:-~/.local/share}/applications/io.github.lgse.Strata.desktop` exists, an in-app update rewrites it and `${XDG_DATA_HOME:-~/.local/share}/icons/hicolor/scalable/apps/io.github.lgse.Strata.svg` from the new archive. Without that entry it writes neither file. The rewritten `Exec=` line points at the installed binary's path, quoted when the path has spaces or shell characters, with `%` doubled and the `%U` field code kept. This holds even when the running binary was already replaced on disk. If the user opted into Strata's system file chooser, the update restarts the portal frontend so subsequent dialogs use the newly installed build. Package-managed installations are updated only by their system package manager (see [Package-managed installations](#package-managed-installations)). To remove a per-user installation, first run `strata --uninstall-portal` if you opted into the system file chooser, and `strata --uninstall-udiskie-unlock` if you opted into encrypted-volume unlock. Then:

```bash
data="${XDG_DATA_HOME:-$HOME/.local/share}"
rm -f ~/.local/bin/strata \
  "$data"/applications/io.github.lgse.Strata.desktop \
  "$data"/dbus-1/services/io.github.lgse.Strata.FileManager1.service \
  "$data"/icons/hicolor/scalable/apps/io.github.lgse.Strata.svg
update-desktop-database "$data"/applications 2>/dev/null || true
gtk-update-icon-cache -qtf "$data"/icons/hicolor 2>/dev/null || true
```

User preferences and custom themes remain under the XDG configuration directories so an uninstall does not destroy personal settings.

### Arch packages

The Arch packages `strata-bin` (latest stable release) and `strata-rc-bin`
(newest stable, alpha, beta, or release-candidate release) are prepared but not
yet published on the AUR. Each repackages the release archive for x86_64 or
aarch64, each architecture with its own pinned SHA-256, and installs the
archive's `strata` binary byte for byte as `/usr/bin/strata`, without stripping
it again. Debug symbols are in the release's separate `.debug` asset (see [Debug
a release crash](#debug-a-release-crash)). Each package provides
`strata=<pkgver>`, conflicts with `strata` and with the other package, and is
licensed `MIT` and `LicenseRef-UnRAR`. A prerelease version drops only its
hyphen: `0.10.0-rc.1` is packaged as `0.10.0rc.1`. Nightly builds have no
package; install them from the release archive and update in the app. A
package's channel is fixed, so to change channel, install the other package.

- The desktop entry goes to `/usr/share/applications` and the icon to
  `/usr/share/icons/hicolor/scalable/apps`. An archive without them still
  packages, with a warning and no launcher.
- The "Open file location" service goes only to `/usr/share/strata` as an
  inactive template; see ["Open file location" from other
  applications](#open-file-location-from-other-applications).
- `LICENSE` and `THIRD_PARTY_LICENSES.md`, plus `UnRAR.txt` when the archive has
  it, go under `/usr/share/licenses/<pkgname>/`.
- Required: `bubblewrap`, `fontconfig`, `glibc>=2.39`, `gstreamer>=1.20`,
  `gst-plugins-base`, `gtk4>=4.12`, `gtksourceview5`, `gvfs`, and `poppler-glib`.
- Optional: `ffmpeg`, `ffmpegthumbnailer`, `gst-libav`, `gst-plugins-good`,
  `gvfs-smb`, `imagemagick`, `libraw`, `squashfs-tools` (listed for
  AppImage icons, which Strata does not show), and `xdg-terminal-exec` (Open in Terminal).

### In-app updates

**Install update** on the **Settings → Updates** row, or **Download update** in
the update dialog, starts the install at once. Only one install runs at a time;
starting another shows "Another install is already running — try again shortly."

- The row reads "Verifying update…" while the signed manifest is fetched, then
  "Downloading update… N%", "Verifying update…", "Installing update…", and
  "Finalizing update…". Its button reads **Cancel**.
- **Cancel** during a download stops it within about a second, shows "Update
  cancelled", and leaves the installed binary unchanged. In the dialog,
  **Cancel**, the close button, Escape, and a click outside it do the same and close
  the dialog.
- Once finalizing begins, the row's **Cancel** is disabled and the dialog cannot
  be dismissed until the install ends.
- A failure shows "Couldn't install update: \<reason>". The row's button becomes
  **Check now**, and the dialog's becomes **Close**.
- A download fails after 30 seconds to connect ("Could not reach the download
  server — check your connection and try again"), or after 30 seconds without
  receiving any bytes, the wait for the server's first reply included ("The
  download stalled — check your connection and try again"). Sending the request
  and receiving the response headers must each finish within 60 seconds. There
  is no total time limit; see [Signed updates](signed-updates.md#download-and-verification).
- On success the status reads "Update installed — restart to apply". Strata
  sends SIGTERM to your other Strata processes started without a flag, or with
  `--portal`, that still run the old binary from the same install path, and
  SIGKILL to any still running 5 seconds later. Only your own user's processes
  are affected. Processes started with other flags keep running: preview
  helpers, an `--unlock-volume` window, and a `strata --gapplication-service`
  instance started by "Open file location". Strata binaries installed at other
  paths also keep running. Strata then closes
  its windows and relaunches the new binary. A running file operation that
  guards closing blocks the restart and shows its close warning.
- The previous binary is kept beside the new one as `.strata-update-rollback`.
  It is restored if the new binary fails its startup probe or exits with an error
  within 20 seconds, and deleted 60 seconds after a successful start.

See [Signed updates](signed-updates.md) for manifest and archive checks.

### Package-managed installations

Strata treats itself as package-managed when its install prefix has
`share/strata/install-source.toml`, which the Arch packages write, or when pacman
owns the binary. The marker counts even when it cannot be read or parsed. A
pacman-owned binary on a system whose `/etc/os-release` has `ID=omarchy` is
Omarchy-managed. If pacman is installed but the ownership query cannot run,
Strata also disables in-place updates. The Omarchy and pacman classification
applies only without the marker. With the marker, Strata follows the marker's
AUR package, even on Omarchy or when pacman owns the binary. A binary no package owns, such as
`~/.local/bin/strata`, keeps in-place updates.

- A package-managed install never downloads an update in the app. Its status
  line adds "Managed by Omarchy", "Managed by pacman", or "Managed by" the
  package's manager.
- With the marker file, a **Package-managed installation** row names the manager,
  package, tracked channel, update instruction, and alternate package. The
  **Release channel** menu is disabled and follows the package's channel; `rc`
  and `preview` show as Preview.
- An Omarchy or pacman install without the marker hides the **Release channel**
  row.
- Update checks ask the AUR for the marker's package, the Omarchy repository for
  an Omarchy install, or the pacman sync databases otherwise. A notice appears
  only when that version is newer and its GitHub release exists. A stable
  package version must match a GitHub release not marked prerelease; a
  prerelease version may match either kind.
- With an update available, Omarchy offers **Open Omarchy Update**, which runs
  `omarchy update` in your terminal. An AUR install offers **Open AUR Update**,
  which runs `<helper> -Syu <package>` with `yay`, `paru`, `pikaur`, or `trizen`
  when one is on `PATH`, or **View on AUR** without one. A pacman install tells
  you to install it through a full system update.

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
<!-- node: integration/portal-file-chooser/setup, Settings row -->
<!-- node: app/packaging/aur, Packages -->
<!-- node: app/packaging/installer, Omarchy keybinds -->
<!-- node: devices/volumes/udiskie-unlock -->
<!-- node: devices/volumes, Discovery -->
<!-- node: devices/volumes, Mounting -->
<!-- node: devices/volumes/camera -->
<!-- node: preview/preview-panel, Images and PDFs -->
<!-- node: browser/view-modes/list -->
<!-- node: remote/file-providers/network-locations -->

Launch Strata with optional paths or URIs:

```bash
strata                      # reopen the last session's tabs, or the default directory
strata ~/Documents          # a specific directory
strata ~/notes.txt          # its folder, with the file selected
strata sftp://host/dir      # a remote location
strata --unlock-volume DEVICE  # unlock an encrypted volume
strata --install-udiskie-unlock   # install Strata as the udiskie unlock handler
strata --uninstall-udiskie-unlock # restore the previous udiskie configuration
strata --version            # print the installed version
```

With no arguments, Strata reopens the tabs saved from the last session while
**Settings → General → STARTUP → Restore open tabs** is on, which is the
default. Without a saved session, or with that switch off, it opens the default
directory.

Each argument opens its own window, whether or not Strata is already running. A
file argument, or a `file://` URI, opens its parent folder with that file
selected. A symlink to a folder opens the folder, and a broken symlink is
selected in its parent. `trash:///`, `smb://`, and `sftp://` arguments open that
location; a remote file URI opens its parent with the file selected. An unmounted
remote is mounted first, with the desktop's sign-in prompt when needed. Paths
whose names are not valid UTF-8 open normally, and a file argument selects only
that file even when another name displays the same.

The window appears at once and stays responsive while Strata checks the
argument. If the check takes over 1 second, the pane shows a spinner,
"Connecting to location…", and **Cancel**, which opens the home folder. A missing
or unreadable argument shows "The requested location is unavailable" with its
path and a **Retry** button, never a password from the URI. **Retry** checks
again, so a folder created after the failure opens. If you navigate elsewhere or
close the window while Strata is still checking, the check is dropped and nothing
navigates or reports an error later. Strata also opens normally when launched
with its output going to a closed pipe.

`strata --version` prints one line, such as `strata 1.0.0`, and exits without
opening a window. Prerelease builds include their suffix, such as `-rc.1`,
matching **Settings → Updates**. The flag must come first: `strata ~/Documents
--version` launches Strata instead.

In the default map, useful shortcuts include Ctrl+K to search Home and mounted local drives from any folder, Ctrl+L for a path or URI, Ctrl+F to filter the current pane, Ctrl+Z to undo or Ctrl+Shift+Z to redo the latest reversible file operation, Space for preview, F2 to rename, Alt+Left and Alt+Right for Back and Forward, and Alt+Up for the parent folder.

Toggle [10xer mode](10xer-mode.md) with Ctrl+Shift+M for Yazi-style navigation and footer prompts; press Ctrl+Shift+M again to return to the default map. In 10xer mode, **q** in the file list does nothing, and **Q** closes the current window. In List and Columns, **l** / **Right** on a previewable file moves the keys into its preview, **h** returns them to the listing without closing the preview, and **i** toggles the preview.

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

The final command should print `io.github.lgse.Strata.desktop`. The desktop entry's filename matches the `io.github.lgse.Strata` application ID that Strata's windows report, so desktop shells match a running window to this entry and draw its `Icon` value. The entry sets `Icon=io.github.lgse.Strata` and `StartupWMClass=io.github.lgse.Strata`. Log out and back in if a shell caches launcher icons.

The entry declares `MimeType=inode/directory;` and
`Categories=Utility;FileTools;FileManager;`, so launchers list it as a file
manager and it can be the default folder handler. Its generic name, comment, and
keywords are translated into French, German, Spanish, Japanese, Brazilian
Portuguese, Korean, Vietnamese, Italian, Russian, and Simplified Chinese. It
ships with `Exec=strata %U`; the commands above, the installer, and `mise run
install-local` rewrite that to the installed binary's absolute path. Strata also
bundles its icon and sets it as the GTK default window icon.

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

A per-user provider takes precedence over system providers shipped by other file managers. Before enabling Strata manually, remove any other per-user service whose `Name` is `org.freedesktop.FileManager1`; two providers for the same name in one service directory are chosen arbitrarily. The installer and `mise run install-file-manager` refuse to install while another per-user service in that directory provides `org.freedesktop.FileManager1`. If another file manager already owns the bus name, exit it before testing. Use `mise run uninstall-file-manager` for a source installation, or remove the per-user service file, to disable Strata again.

While Strata is running, it claims `org.freedesktop.FileManager1` on the session bus unless another program already owns that name. The service file lets a call start Strata (`strata --gapplication-service`) when it is not running. If another file manager already owns the bus name, calls keep reaching that file manager. Strata then answers `ShowFolders`, `ShowItems`, and `ShowItemProperties`, and each call opens a new Strata window:

- `ShowFolders` opens each named folder with nothing selected.
- `ShowItems` opens the folder that holds each named item, with the item selected and focused. Items that share a folder open in one window; each other folder opens its own window, in the order listed. `ShowItems` on `file:///` opens `/` with nothing selected.
- `ShowItemProperties` does the same as `ShowItems` and also opens **Properties** for the first item listed.
- Revealing a dotfile while hidden files are off turns hidden files on and selects it.
- When two files' names are not valid UTF-8 and display the same, `ShowItems` selects only the file the URI names.
- A remote URI such as `sftp://host/dir/file` is mounted first, then revealed. If the mount fails or is cancelled, nothing is revealed.
- Each method takes a list of URIs and a startup ID (`as`, `s`). Strata ignores the startup ID, and a call with other arguments fails with `org.freedesktop.DBus.Error.InvalidArgs`.

For example:

```bash
busctl --user call org.freedesktop.FileManager1 /org/freedesktop/FileManager1 \
  org.freedesktop.FileManager1 ShowItems ass 1 "file://$HOME/Downloads" ""
```

### Set up from Settings

**Settings → General → DESKTOP INTEGRATION → System file manager** lists **Open
and Save dialogs**, **Opening folders**, and **Reveal in File Manager**, each
marked configured or not. On Omarchy it also lists **Keyboard shortcuts**. Close
open file dialogs before changing setup.

- **Complete setup** installs the system file chooser, makes
  `io.github.lgse.Strata.desktop` the `inode/directory` handler, and installs the
  per-user "Open file location" service. On Omarchy 3 or 4 it also binds
  Super+Shift+F and Super+Alt+Shift+F to Strata in `~/.config/hypr/bindings.conf`,
  or `bindings.lua` on Omarchy 4.
- If `hyprctl configerrors` reports errors after that edit, Complete setup
  restores the previous bindings file and keeps a `strata-keybind-backup-` copy.
- A bindings file that is a symlink you own is written through, and the link is
  kept. A dangling link, or a link or target owned by another user, makes setup
  fail without writing. Existing permission bits are kept.
- With a symlinked bindings file, the `strata-keybind-backup-` copy is written in
  the link's directory. With a dangling link, Complete setup fails naming the
  missing target, and Restore default leaves the shortcuts and the link
  unchanged.
- Complete setup fails with "Another per-user FileManager1 provider is already
  installed: \<path>" when another service owns that name. The button is hidden
  once every line is configured.
- **Restore default** appears while any part is installed. It removes the
  service and the chooser, and returns `inode/directory` to the handler recorded
  before setup, or Nautilus. It leaves the folder handler alone when it no
  longer points to Strata. With no recorded handler and no Nautilus, it fails
  with "No previous folder handler was recorded and Nautilus was not detected.
  Choose another default file manager first, then retry Restore default."
- On Omarchy, Restore default replaces Strata's shortcut block with `nautilus
  --new-window` bindings. Without Nautilus, it reports "Nautilus was not
  detected; the Strata keyboard shortcuts were left unchanged." It refuses to
  change a Strata shortcut block you edited by hand.

### Make Strata the Omarchy file manager

The XDG association above handles folders opened by applications. On current Lua-based Omarchy releases, also override the stock Nautilus shortcuts in `~/.config/hypr/bindings.lua` so Omarchy launches Strata directly.

The installer's "Replace Omarchy's Nautilus file-manager keybinds with Strata?"
(default No), or `--with-omarchy-keybinds`, does this for you. It appends a
marked block that rebinds Super+Shift+F and Super+Alt+Shift+F to Strata, in
`~/.config/hypr/bindings.conf` on Omarchy 3 or `~/.config/hypr/bindings.lua` on
Omarchy 4. It first backs up an existing file as `<file>.bak.<timestamp>`. If
`hyprctl configerrors` reports errors after the reload, it restores the previous
file and exits with Hyprland's errors. If the block is already present, it
changes nothing. Without a running Hyprland, it writes the block and warns that
the file could not be reloaded.

To make the change by hand on Omarchy 3, append this to
`~/.config/hypr/bindings.conf`:

```ini
unbind = SUPER SHIFT, F
unbind = SUPER ALT SHIFT, F
bindd = SUPER SHIFT, F, File manager, exec, uwsm-app -- strata
bindd = SUPER ALT SHIFT, F, File manager (cwd), exec, uwsm-app -- strata "$(omarchy-cmd-terminal-cwd)"
```

On Omarchy 4, follow the steps below.

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

On Omarchy 3 or 4, the installer asks whether to use Strata for encrypted-volume unlock (default No). **Settings → General → DESKTOP INTEGRATION** includes **Unlock encrypted volumes**. Choose **Use Strata** so plugging in an encrypted drive opens Strata's password prompt instead of udiskie's dialog. **Restore default** returns udiskie to its previous configuration. Restoring also deletes the restore state in `~/.local/share/strata/udiskie-install/`.

On generic Arch, the installer offers the same step only when `udiskie` is already on `PATH`. Restore there with `strata --uninstall-udiskie-unlock`; Settings for this row stays Omarchy-only.

The same setup is available unattended:

```bash
strata --install-udiskie-unlock
strata --uninstall-udiskie-unlock
```

This edits `~/.config/udiskie/config.yml` and records restore state in `~/.local/share/strata/udiskie-install/state.toml`. It is not a saved Strata preference. The Settings row appears only when Omarchy is detected and `udiskie` is on your `PATH`; the CLI flags are unattended and are not Omarchy-gated. Unattended installer opt-in is `--with-udiskie-unlock`.

Setup rewrites `config.yml` with a managed header, sets udiskie's `event_hook` to
a list of the installed binary's absolute path followed by `--udiskie-hook
{event} {id_usage} {device_file} {id_uuid}`, sets
`password_prompt: false`, and turns off LUKS automount. When only `config.json`
exists, setup converts it to `config.yml`, and restore writes it back as JSON.
Setup then restarts udiskie, or starts `udiskie --automount --no-notify
--no-tray` if none is running; restore restarts udiskie only if it is running.
If udiskie cannot be restarted, the command reports "Saved the udiskie
configuration. Restart udiskie or log out for it to take effect." A `config.yml`
that is a symlink or other non-regular file is refused with "Refusing to replace
non-regular udiskie configuration \<path>". Setup also refuses a configuration
that is not a YAML mapping, whose `program_options` is not a mapping, whose
`device_config` is not a list, or whose existing `event_hook` or
`password_prompt` is not a boolean, string, or list of strings. It reports
"Refusing to change udiskie configuration: …" and leaves the file unchanged.
Neither command installs or removes the
`udiskie` package. **Use Strata** shows only while the integration is not
configured, and **Restore default** only while there is something to restore.

On Omarchy without `udiskie` on `PATH`, the installer warns and skips this step;
with `--with-udiskie-unlock` it exits with "udiskie is not on PATH;
--with-udiskie-unlock requires udiskie." On any other system that does not
qualify, `--with-udiskie-unlock` exits with "--with-udiskie-unlock requires
Omarchy 3 or 4, or an Arch-based system with udiskie on PATH."


For an added encrypted volume, the hook runs `strata --unlock-volume DEVICE`, or
passes the volume's UUID when udiskie reports no device file. It ignores every
other event. `--unlock-volume` takes a device path or LUKS UUID and
opens Strata's password prompt for that volume. If the volume has not appeared
after 1 second, the window shows "Waiting for encrypted volume…" with **Cancel**.
After 8 seconds without a match it shows "The encrypted volume was not found",
and an unencrypted volume shows "This is not an encrypted volume". Any other
operand fails with "invalid --unlock-volume operand", and combining it with file
arguments fails with "cannot combine --unlock-volume with file arguments".

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

**DEVICES** in the sidebar lists the volumes GVfs reports, drives that need a
password before they show a volume, and mounts that have no listed volume. A
mount whose volume is already listed gets no second row. Mounts the system
hides do not appear, such as a Pacman cache subvolume mounted somewhere other
than your home folder, `/media`, or `/run/media/$USER`. Plugging in, mounting, unmounting, or removing a device updates it without a
restart, and with nothing to list the DEVICES heading is hidden. Clicking a
mounted volume opens it. Clicking an unmounted volume mounts it, then opens it.
Right-clicking an unmounted volume on a removable drive offers **Mount** when the
system reports that the volume can be mounted.
Cancelling its password prompt shows no error. Any other failure, apart from a
rejected passphrase or a mount already in progress, shows "Unable to mount
volume" with the system's reason. When another program is already
mounting the volume, Strata shows "Connecting…" and waits up to 8 seconds, then
opens the mount or starts its own mount once.

After installing a backend, fully quit Strata (all windows) and reopen it.
Reconnect the unlocked phone if necessary, then click its entry under **DEVICES**.
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
Deleting a photo removes only its row; a same-named photo from another folder
stays listed.
This is the USB-exposed collection, not iOS's Albums hierarchy. The current
backend does not provide album membership for a reliable Albums/Camera Roll split.

Camera batches yield to interface input and redraws. Photos sorts by **Device
order** by default: batches append in discovery order and are never re-sorted.
Device order appears in the sort menu only at a camera root, and there its
direction button is disabled ("Device order follows discovery; choose a sort
field to reverse its direction"). Choosing Name or Modified sorts the listing;
choosing Device order again reloads it in discovery order. The selected photo
stays selected while batches arrive. In List view, file-type grouping stays off
while Photos loads and while it is in Device order; your saved grouping setting
is kept.

Visible thumbnails load top to bottom while the scan runs and are reprioritized
after you scroll. A Photos view you have not scrolled stays at the top as
batches arrive. While loading, selection updates do not scroll List, Icons, or
Columns to the selected photo.

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
them. Remote PDFs, GIF images, audio, and video formats other than MOV and MP4
still need a local copy for preview. HEIC decoding requires an installed HEIC-capable image
decoder, such as ImageMagick with libheif. Camera/PTP thumbnails use small previews
provided by the camera, up to 1 MiB within 15 seconds, with sandboxed decoding; if the
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

Upstream libgphoto2 commit
[`9f5d4f9`](https://github.com/gphoto/libgphoto2/commit/9f5d4f9ca0a7f58bac7987180a48154ea07c090f)
fixes it. Use a distribution libgphoto2 update or backport containing that fix when
available. Merely reinstalling `gvfs-gphoto2` or restarting Strata will not fix an
affected libgphoto2 build. Strata's GVfs camera backend must load the corrected
library; setting library paths only for Strata may not affect the separately
launched GVfs process. Strata does **not** bundle or install the fix. Avoid replacing system libraries manually; any locally built workaround
should be isolated and reversible.

### Network shares

Press Ctrl+L, enter an address such as `smb://server/share` or `sftp://user@host:2222/path`, and press Enter. Strata uses GIO/GVfs and prompts for credentials when required. If GVfs does not respond within 2 seconds at launch, Strata still opens and prints "GVFS is unresponsive; using local filesystem and volume support for this session." Remote locations are then unavailable until you restart Strata with GVfs responding. Remote protocols need their GVfs backend installed; distributions split these up differently, so check yours for the SMB backend (`gvfs-smb` on Arch) and the SFTP backend (part of `gvfs` on Arch, `gvfs-backends` on Debian and Ubuntu).

When the backend needs credentials, an "Authentication required" dialog shows only
the fields it requests. For SMB that can be Username, Domain, Password, a
Registered user or Anonymous choice, and Password storage (Don't remember, Until
logout, Forever). Anonymous disables the credential and storage fields. Wrong
credentials reopen the dialog with "Those credentials weren’t accepted. Check …
and try again." Cancel or Escape returns to the previous location with no error and
no history entry.

The sidebar's **Network** place opens `network:///`, which lists the hosts and
shares GVfs discovers. At `smb://host/`, opening a share mounts it if needed. A
mounted SMB share appears under DEVICES with a network icon; its menu offers
**Properties** and **Disconnect**, and a failed disconnect shows "Unable to
disconnect". An `smb://` address without its backend fails with a message naming
`gvfs-smb` or `gvfs-backends`. An unknown host, refused connection, timeout, or
unreachable host each shows its own message. Remote entries keep their URI, never
a `/run/user/…/gvfs` path, and remote names are shown percent-decoded, such as
"My Share" for `My%20Share`.

SFTP accepts password and SSH-key authentication. Encrypted keys can be unlocked in your SSH agent; if GVfs asks Strata for a key passphrase or host-key decision, Strata presents the request without deciding for you. Trust questions from SMB, other remote schemes, and devices appear in GTK's standard question dialog, not Strata's own. See [SFTP locations](remote-sftp.md).

## Release channels

<!-- node: app/updates/release-channels -->
<!-- node: app/updates -->
<!-- node: app/updates/package-managed, Checking -->

Strata defaults to the **Stable** channel. For release binaries and source builds, only final tagged releases are offered, and a Stable install never receives, sees, or is notified about a prerelease. Package-managed installs follow their package source instead (see [Package-managed installations](#package-managed-installations)). Stable offers a release only when its tag has no prerelease suffix and GitHub does not mark it as a prerelease. A saved channel value Strata does not recognize is read as Stable.

Strata checks for updates automatically by default: each time it starts, once its first window opens, and again when a window or **Settings → Updates** opens if no check has completed in the last 24 hours. Turning **Check for updates automatically** back on, or changing the channel, also runs a check. The check asks the update source for your installation: GitHub for release binaries and source builds, the AUR for AUR packages, the Omarchy package repository for Omarchy packages, or the local pacman sync database for other pacman packages. When a newer version is found, Strata also fetches that release's details from GitHub. Turning the switch off stops the automatic checks, discards the result of an automatic check still running, hides any update notice already shown, and locks the channel. **Check now** still checks on demand, and the Updates page's release-notes card asks GitHub for the current version's notes when they are not already cached. The installed version's notes are fetched once per tag and kept in `~/.cache/strata/release-notes.toml`. Strata never downloads or installs an update without your confirmation.

For release binaries and source builds, the first automatic check of a session
always asks GitHub. Later automatic checks, and the check run by turning
automatic checks on, reuse a result under 6 hours old for the same channel,
stored in `~/.cache/strata/update-check.toml`, and
**Check now** always asks GitHub. Package-managed installs skip this cache and
query their package source on every check. A GitHub 403 or 429 reports "GitHub
API rate limit reached", and any other HTTP error reports "GitHub API returned
HTTP N". A request that gets no response, for example when you are offline,
reports "Network request failed:" followed by the cause.

### Update status and notices

- Before a check, the **Settings → Updates** status row reads "Version X",
  adding the build kind, such as "Release candidate", for a prerelease build.
- After a check it reads "Strata is up to date", "An update is available", or
  "Couldn’t check for updates". A failure shows its reason and a "View releases
  on GitHub" link.
- An available update shows its notes inline, titled "Available release · vX"
  with its change count and publication date.
- **Release notes** holds a collapsed "What's new in vX" expander for the
  installed version, showing "Loading release notes…" until they arrive.
  Without a GitHub release for that tag, its summary reads "Release notes
  unavailable for this build", the expander reads "Release notes are unavailable
  because this version’s tag was not found.", and a **View on GitHub** link
  appears. A failed request reads "Couldn’t load release notes: \<reason>".
  Empty notes, or notes holding only HTML comments, read "No release notes were
  provided for this release."
- Notes show headings, paragraphs, lists, code, and rules. Images, tables, and
  block quotes are left out, and raw HTML other than comments, such as
  `<b>x</b>`, shows as text.
- HTML comments in notes are hidden, whether inline or spanning several lines.
  A body starting with GitHub's `<!-- Release notes generated … -->` comment
  shows from its first heading. When a comment starts a line, any text after
  `-->` on its closing line is hidden with it; an inline comment hides only
  itself. A comment that is never closed hides the rest of the notes.
- An available update shows a notice in the sidebar of every window, including
  windows opened later. Clicking it opens the update dialog, titled "Strata vX is
  available", with "Installed vA → Available vB", the notes under "What’s new",
  a "View release on GitHub" link, and an action button: **Download update**
  for in-place installs, **Open Omarchy Update** on Omarchy, **Open AUR Update**
  or **View on AUR** for an AUR package, and **Close** for a pacman install. If
  the release has no notes, or only HTML comments, the dialog reads "No release
  notes were provided. Review this release on GitHub before continuing."

To try upcoming changes early, choose a channel in **Settings → Updates** (the channel is locked while automatic checks are off). **Preview** receives stable releases plus alpha, beta, and release-candidate builds, but not nightlies. **Nightly** receives every recognised build, including nightly development builds. For release binaries and source builds, a Stable check reads only GitHub's latest release; Preview and Nightly checks consider the 30 newest releases. The update dialog and release notes always identify the exact build kind.

When a prerelease installation selects **Stable**, the Updates card immediately offers the newest stable release as the channel target—even when that requires a semantic downgrade—and labels the action **Return to stable**. Preview and Nightly selections use the same card for ordinary forward updates, so channel changes never create a separate competing rollback card.

Strata offers only tags of the form `MAJOR.MINOR.PATCH`, with an optional
leading `v`, optionally followed by `-alpha.N`, `-beta.N`, `-rc.N` (N ≥ 1), or
`-nightly.YYYYMMDD[.N]`. Drafts and releases
without your architecture's archive are never offered. Outside Return to stable,
only a newer build is offered; for one version, nightly ranks below alpha, beta,
rc, then the final release. A Preview user on `0.5.0-rc.2` is offered `0.5.0`.

**Return to stable** applies only to in-place installs. Its status reads "Stable
channel target: vX", the download reads "Downloading stable release…", and
success reads "Stable release installed — restart to apply".

Changing the channel clears the sidebar notice in every window and re-checks
every open Updates page, except one that is installing or waiting to restart. An
open update dialog whose build the new channel excludes reads "This build is no
longer offered on your update channel — check for updates again.", and its button
becomes **Close**. **Install update** on an offer the current channel excludes
runs a new check instead.

A prerelease offer shows its build kind as a badge in its notes and in the update
dialog, which also lists Channel, Tag, Commit, and Published.

See [Releasing](https://github.com/lgse/strata/blob/v1.0.0/docs/releasing.md) for the tag grammar these channels rely on and, for maintainers, how a release candidate is cut and promoted.
