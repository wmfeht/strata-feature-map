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

It needs x86_64 or aarch64 and glibc 2.39 or newer. It installs missing
packages with `sudo pacman` on Arch and Omarchy, verifies the latest stable
release's checksum, and installs it to `~/.local/bin/strata`. Then it asks
about each integration below.

To install without questions, name the integrations you want. Anything you
leave out stays off:

```bash
curl -fsSL https://raw.githubusercontent.com/lgse/strata/main/install.sh \
  | bash -s -- --with-desktop-entry --with-folder-association
```

`--non-interactive` alone installs only the binary and required packages.
Unattended package installs need passwordless sudo or cached credentials. Pipe
the installer into `bash -s -- --help` to list every flag.

Run `strata --version` to confirm the install.

The Arch packages `strata-bin` (Stable) and `strata-rc-bin` (Preview) are
prepared but not yet published on the AUR. Use the installer until they are.

## Add Strata to your launcher

<!-- node: app/packaging, Desktop entry and icon -->
<!-- node: app/packaging/installer, Desktop entry and folder association -->

Answer Yes to **Add Strata to your desktop application menu?** (the default),
or pass `--with-desktop-entry`. The installer writes
`~/.local/share/applications/io.github.lgse.Strata.desktop` and the icon under
`~/.local/share/icons/hicolor`, so docks and window switchers show the Strata
icon. Log out and back in if your shell caches launcher icons.

## Make Strata the default file manager

<!-- node: integration/portal-file-chooser/setup, Settings row -->
<!-- node: app/packaging/installer, Omarchy keybinds -->
<!-- node: integration/file-manager-interface, Activation and installation -->

The quickest route is in the app. Press Ctrl+, and open **Settings → General**.
The **System file manager** row lists **Open and Save dialogs**, **Opening
folders**, **Reveal in File Manager**, and, on Omarchy, **Keyboard shortcuts**.
Click **Complete setup** to configure all of them. On Omarchy, Super+Shift+F
and Super+Alt+Shift+F then open Strata instead of Nautilus. **Restore default**
undoes it.

To set only the folder handler, use `xdg-mime`:

```bash
xdg-mime default io.github.lgse.Strata.desktop inode/directory
xdg-mime query default inode/directory   # prints io.github.lgse.Strata.desktop
```

Browsers and GTK apps skip that association for "Open file location" and "Show
in Folder". Strata answers those once its D-Bus service is installed. Answer Yes
to **Use Strata for "Open file location" from other applications?**, or pass
`--with-file-manager`. Folder association installs it automatically. The
installer refuses if another per-user service already provides it.

## Use Strata as the system file chooser

<!-- node: integration/portal-file-chooser/setup, Portal installation -->
<!-- node: integration/portal-file-chooser, Requests -->

Strata can draw the Open and Save dialogs of portal-aware apps, for local
files. To switch only the chooser, close any open file dialogs and run:

```bash
strata --install-portal
```

Your current chooser stays listed as the fallback. Run `strata --uninstall-portal` to
restore it. The installer offers this with default No; `--with-file-chooser`
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

To try builds early, change **Release channel** in **Settings → Updates**:

- **Stable**, the default, offers final releases only.
- **Preview** adds alpha, beta, and release-candidate builds.
- **Nightly** adds daily builds.

Switching a prerelease install back to **Stable** offers **Return to stable**,
even when that is a downgrade.

When a package manager installed Strata, Strata never replaces itself. It offers
**Open AUR Update** or **Open Omarchy Update** instead, or tells you to run a
full system update.

**Full detail:** [Installation and desktop integration](../reference/install.md),
[System file chooser](../reference/portal-file-chooser.md),
[Signed updates](../reference/signed-updates.md)
