---
nodes: [app/packaging, app/packaging/installer, app/packaging/aur, app/updates, app/updates/install, app/updates/package-managed, app/updates/release-channels, integration/file-manager-interface, integration/portal-file-chooser, integration/portal-file-chooser/setup]
reviewed_at: be3343a5992a2a5497b1a2ee7faa525be18e988f
---

# Install and integrate

Install Strata with one command, then choose how much of your desktop it takes
over. The recommended setup turns on every integration your system supports;
you can leave any of them out, and each one is reversible.

## Install interactively or unattended

<!-- node: app/packaging/installer -->
<!-- node: app/packaging/aur, Packages -->
<!-- node: app/packaging, Version -->

Run the installer as your normal user:

```bash
curl -fsSL https://raw.githubusercontent.com/lgse/strata/main/install.sh | bash
```

It needs x86_64 or aarch64 and glibc 2.39 or newer. Pick **Install Strata
(recommended)** for every integration your system supports, or **Customize
installation** to uncheck some:

| Option | Offered | Decline unattended with |
| --- | --- | --- |
| **Application launcher** | Always | `--without-desktop-entry` |
| **Default file manager** | Always | `--without-folder-association` |
| **Open file location** | Always | `--without-file-manager` |
| **Open and Save dialogs** | Always | `--without-file-chooser` |
| **Windows network shares** | Arch-based, when `gvfs-smb` is missing | `--without-smb` |
| **Camera RAW support** | Arch-based, when a RAW decoder is missing | `--without-raw` |
| **Omarchy file-manager shortcuts** | Omarchy 3 or 4 | `--without-omarchy-keybinds` |
| **Encrypted-drive unlock** | Arch-based, with `udiskie` installed | `--without-udiskie-unlock` |

**Default file manager** also checks the launcher and **Open file location**.
The installer then verifies the release's signature, installs missing packages
with `sudo pacman` on Arch and Omarchy, and installs Strata to
`~/.local/bin/strata`. On other distributions it lists the libraries to install
yourself, then asks you to confirm.

On Arch or Omarchy, `--non-interactive` installs every supported integration
without questions; add a `--without-*` flag for each one to leave out:

```bash
curl -fsSL https://raw.githubusercontent.com/lgse/strata/main/install.sh \
  | bash -s -- --non-interactive --without-file-chooser --without-smb
```

Unattended package installs need passwordless sudo or cached credentials.
`--help` lists every flag. Unattended mode refuses to replace an existing
binary; to add an integration later, rerun the installer without flags.

Run `~/.local/bin/strata --version` to confirm the install. If the installer
warns that `~/.local/bin` is not on PATH, add it to run `strata` by name. If
previews or drives don't work, open **Settings → Diagnostics** and click
**Run** to see which package is missing.

AUR packages are not yet published; use the installer.

## Add Strata to your launcher

<!-- node: app/packaging, Desktop entry and icon -->
<!-- node: app/packaging/installer, Desktop integrations -->

**Application launcher** puts Strata in your launcher, with its icon. The
installer writes
`~/.local/share/applications/io.github.lgse.Strata.desktop` and the icon under
`~/.local/share/icons/hicolor`. To add it by hand, see
[Desktop entry](../reference/install.md#desktop-entry).

## Make Strata the default file manager

<!-- node: integration/portal-file-chooser/setup, Settings row -->
<!-- node: app/packaging/installer, Omarchy keybinds -->
<!-- node: integration/file-manager-interface, Activation and installation -->

The recommended install does this. To set it up later, press Ctrl+, and open
**Settings → General**. The **System file manager** row
lists **Open and Save dialogs**, **Opening
folders**, **Reveal in File Manager**, and, on Omarchy, **Keyboard shortcuts**.
Close any open file dialogs, then click **Complete setup** to configure all of
them. On Omarchy, Super+Shift+F and Super+Alt+Shift+F then open Strata instead
of Nautilus. **Restore default** undoes it.

To set these up by hand, see
[Usage and desktop integration](../reference/install.md#usage-and-desktop-integration).

## Use Strata as the system file chooser

<!-- node: integration/portal-file-chooser/setup, Portal installation -->
<!-- node: integration/portal-file-chooser, Requests -->

Strata can draw portal Open and Save dialogs for local files. The recommended
install turns this on and restarts the portal service, so close open file
dialogs first. **Complete setup** in **Settings → General** also turns it on.
Your current chooser stays listed as the fallback, and **Restore default** brings
it back.

To switch only the chooser by hand, see
[Per-user installation](../reference/portal-file-chooser.md#per-user-installation).

## Keep Strata up to date

<!-- node: app/updates, Checking -->
<!-- node: app/updates/install, Starting -->
<!-- node: app/updates/release-channels, Channels -->
<!-- node: app/updates/release-channels, Release list -->
<!-- node: app/updates/package-managed, Settings and actions -->

Strata checks for a newer release automatically. When one exists, an
**Update available** notice appears in the sidebar. Click it to read the release
notes, then click **Download update**. You can also open **Settings → Updates**
and click **Check now** or **Install update**.

Strata verifies the release's signature, replaces the binary, and restarts. If
the new build fails to start, it restores the previous one.

To try builds early, set **Release channel** in **Settings → Updates** from
**Stable** to **Preview** (alpha, beta, and release candidates) or **Nightly**
(daily builds). Switching a prerelease install back to **Stable** offers
**Return to stable**.

To roll back or switch builds, open **Install a specific release** in
**Settings → Updates**, pick a release your channel offers, and click **Install
release**.

When a package manager installed Strata, Strata never replaces itself. It offers
**Open Omarchy Update**, **Open AUR Update** (**View on AUR** without an AUR
helper), or tells you to run a full system update.

**Full detail:** [Installation and desktop integration](../reference/install.md),
[System file chooser](../reference/portal-file-chooser.md),
[Signed updates](../reference/signed-updates.md)
