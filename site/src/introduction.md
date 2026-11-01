---
nodes: [app/packaging/installer]
reviewed_at: be3343a5992a2a5497b1a2ee7faa525be18e988f
---

# Start here

Strata is a fast, keyboard-first GTK file manager for Linux. It is built for
Arch Linux and Omarchy, and may also run on other x86_64 or aarch64 Linux
systems with GTK 4.12 or newer and glibc 2.39 or newer.

## Install

<!-- node: app/packaging/installer, System checks -->
<!-- node: app/packaging/installer, Setup menu -->
<!-- node: app/packaging/installer, Dependencies -->
<!-- node: app/packaging/installer, Download and verification -->
<!-- node: app/packaging/installer, Install -->
<!-- node: app/packaging/installer, Desktop integrations -->

Run this in a terminal as your normal user, not root:

```bash
curl -fsSL https://raw.githubusercontent.com/lgse/strata/main/install.sh | bash
```

The installer walks you through five steps:

1. It checks your machine: x86_64 or aarch64 and glibc 2.39 or newer. It prints
   your distribution and architecture, such as `Arch Linux · x86_64`.
2. Under **Choose your setup**, pick **Install Strata (recommended)** to get
   every integration your system supports: the application launcher, Strata as
   the default file manager and for "Open file location", and the Open and Save
   dialogs. On Arch-based systems it adds SMB share and camera RAW support when
   they are missing, on Omarchy the file-manager shortcuts, and with udiskie
   encrypted-drive unlock. Pick **Customize installation** to uncheck any of
   them. On other distributions, it lists the libraries to install and stops
   unless you confirm they are installed.
3. It downloads the latest stable release's signed manifest, verifies its
   signature, and checks the archive's size and SHA-256 against it before
   extracting anything. It needs no GitHub account or `gh`.
4. On Arch-based systems, including Omarchy, it installs the missing packages in
   one `sudo pacman` transaction, with pacman's own confirmation.
5. It installs the binary to `~/.local/bin/strata`, then sets up the
   integrations you chose.

Press `q` in a menu to cancel without changing anything (Escape also works in
the arrow-key menu). If the summary
warns that `~/.local/bin` is not on `PATH`, add it in your shell configuration, or
start Strata from your launcher.

## First launch

<!-- node: app/packaging/installer, Install -->

Start Strata from your launcher, or run:

```bash
strata
```

<!-- Screenshot: introduction-first-launch.png. Strata just after first launch:
Home open in Columns view, sidebar on the left, footer showing "F1  Shortcuts". -->

Strata opens your home folder in Columns view. Each folder you open adds a
column to the right, so the path you took stays visible. The sidebar lists Home,
Trash, Network, and your standard folders. Folders you pin appear under
**PINNED**, and drives under **DEVICES**. On Omarchy Quattro, Strata follows your
desktop theme; otherwise it starts in Tokyo Night.

Try these three things first:

1. **Switch views.** Press Ctrl+1 for Columns, Ctrl+2 for Icons, and Ctrl+3 for
   List. Strata remembers your choice.
2. **Preview a file.** Click an image or text file, or select it and press
   Space. Press Space again to close the preview. Double-click opens it.
3. **Search everywhere.** Press Ctrl+K and type part of a name. Search covers
   your home folder and mounted local drives, wherever you are.

Forgot a key? Press F1, or click **F1 Shortcuts** in the footer, to search every
shortcut. Ctrl+, opens **Settings**.

## Where to go next

<!-- node: app/packaging/installer -->

- [Install and integrate](guide/install.md): unattended installs, default file
  manager, system file chooser, and updates.
- [Views](guide/views.md): Columns, Icons, and List, sorting, and per-folder
  settings.
- [Keyboard](guide/keyboard.md): the shortcuts worth learning and how to look up
  the rest.
- [Find files](guide/search.md): filter a folder or search everywhere.
- [Previews](guide/previews.md): the preview panel, quick looks, media, and
  documents.
- [Everyday operations](guide/operations.md): copy, move, rename, trash, undo,
  archives, and jobs.
- [Custom actions](guide/actions.md): add your own scripts to the right-click
  menu.
- [Themes](guide/themes.md): bundled themes, Omarchy, and your own colors.
- [Settings](guide/settings.md): where settings live and which to change.
- [Remote and devices](guide/remote.md): SMB, SFTP, phones, cameras, and drives.
- [10xer mode](guide/10xer.md): a Yazi-style key map for keyboard-only work.

**Full detail:** [Installation and desktop integration](reference/install.md)
covers every installer option, manual installation, and uninstalling.
