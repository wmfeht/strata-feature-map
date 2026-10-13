---
nodes: [app/packaging, app/packaging/installer, app/packaging/aur, app/updates, app/updates/install, app/updates/package-managed, app/updates/release-channels, integration/file-manager-interface, integration/portal-file-chooser, integration/portal-file-chooser/setup]
reviewed_at: 0a086aa3bdb251842a1e8413e2a6b35970d0b409
---

# Install and integrate

Install Strata with one command, then choose how much of your desktop it takes
over. Every integration is opt-in and reversible.

## Install interactively or unattended

<!-- node: app/packaging/installer -->
<!-- node: app/packaging/aur, Packages -->
<!-- node: app/packaging, Version -->

Run the installer as your normal user:

```bash
curl -fsSL https://raw.githubusercontent.com/lgse/strata/main/install.sh | bash
```

It needs x86_64 or aarch64 and glibc 2.39 or newer. On Arch and Omarchy it
installs missing packages with `sudo pacman`. On other distributions it lists
the libraries to install yourself, then asks you to confirm. It verifies the
latest stable release's checksum, installs it to `~/.local/bin/strata`, and asks
about each integration below.

On Arch or Omarchy, to install without questions, name the integrations you
want. Anything you leave out stays off, except that `--with-folder-association`
also turns on both of these:

```bash
curl -fsSL https://raw.githubusercontent.com/lgse/strata/main/install.sh \
  | bash -s -- --with-desktop-entry --with-file-manager
```

Unattended package installs need passwordless sudo or cached credentials.
`--help` lists every flag. Unattended mode refuses to replace an existing
binary, so to add an integration later, rerun the installer without flags and
answer Yes to replacing it.

Run `~/.local/bin/strata --version` to confirm the install. If the installer
warns that `~/.local/bin` is not on PATH, add it to run `strata` by name.

AUR packages are not yet published; use the installer.

## Add Strata to your launcher

<!-- node: app/packaging, Desktop entry and icon -->
<!-- node: app/packaging/installer, Desktop entry and folder association -->

Answer Yes to **Add Strata to your desktop application menu?** (the default),
or pass `--with-desktop-entry`. The installer writes
`~/.local/share/applications/io.github.lgse.Strata.desktop` and the icon under
`~/.local/share/icons/hicolor`.

## Make Strata the default file manager

<!-- node: integration/portal-file-chooser/setup, Settings row -->
<!-- node: app/packaging/installer, Omarchy keybinds -->
<!-- node: integration/file-manager-interface, Activation and installation -->

With the launcher entry installed, press Ctrl+, and open **Settings → General**.
The **System file manager** row lists **Open and Save dialogs**, **Opening
folders**, **Reveal in File Manager**, and, on Omarchy, **Keyboard shortcuts**.
Close any open file dialogs, then click **Complete setup** to configure all of
them. On Omarchy, Super+Shift+F and Super+Alt+Shift+F then open Strata instead
of Nautilus. **Restore default** undoes it.

To set only the folder handler once the launcher entry is installed, use
`xdg-mime`:

```bash
xdg-mime default io.github.lgse.Strata.desktop inode/directory
xdg-mime query default inode/directory   # prints io.github.lgse.Strata.desktop
```

Browsers and GTK apps skip that association for "Open file location" and "Show
in Folder". Strata answers those once its D-Bus service is installed. Answer Yes
to **Use Strata for "Open file location" from other applications?**, or pass
`--with-file-manager`. Folder association in the installer installs it too.

## Use Strata as the system file chooser

<!-- node: integration/portal-file-chooser/setup, Portal installation -->
<!-- node: integration/portal-file-chooser, Requests -->

Strata can draw portal Open and Save dialogs for local files. To switch only
the chooser, close any open file dialogs and run:

```bash
strata --install-portal
```

Your current chooser stays listed as the fallback. Run
`strata --uninstall-portal` to restore it. The installer offers this with default No; `--with-file-chooser`
opts in unattended, and folder association never turns it on.

## Keep Strata up to date

<!-- node: app/updates, Checking -->
<!-- node: app/updates/install, Starting -->
<!-- node: app/updates/release-channels, Channels -->
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

When a package manager installed Strata, Strata never replaces itself. It offers
**Open Omarchy Update**, **Open AUR Update** (**View on AUR** without an AUR
helper), or tells you to run a full system update.

**Full detail:** [Installation and desktop integration](../reference/install.md),
[System file chooser](../reference/portal-file-chooser.md),
[Signed updates](../reference/signed-updates.md)
