---
nodes: [app/packaging/installer]
reviewed_at: 0a086aa3bdb251842a1e8413e2a6b35970d0b409
---

# Start here

Strata is a fast, keyboard-first GTK file manager for Linux. It is built for
Arch Linux and Omarchy, and runs on other GTK4 desktops with glibc 2.39 or newer.

## Install

<!-- node: app/packaging/installer, System checks -->
<!-- node: app/packaging/installer, Dependencies -->
<!-- node: app/packaging/installer, Download and verification -->
<!-- node: app/packaging/installer, Install -->
<!-- node: app/packaging/installer, Desktop entry and folder association -->

Run this in a terminal as your normal user, not root:

```bash
curl -fsSL https://raw.githubusercontent.com/lgse/strata/main/install.sh | bash
```

The installer walks you through five steps:

1. It checks your machine: x86_64 or aarch64, glibc 2.39 or newer, and whether
   you run Omarchy.
2. On Arch or Omarchy, it lists the missing packages and asks before running
   `sudo pacman`. On other distributions, it lists what to install yourself.
3. It downloads the latest stable release and checks its SHA-256 checksum before
   installing anything. With a logged-in `gh`, it also verifies the build's
   provenance.
4. It installs the binary to `~/.local/bin/strata`.
5. It asks about optional extras, one question each: a launcher entry, making
   Strata the default for folders, "Open file location" from other apps, the
   system file chooser, and Omarchy keybinds. Only the launcher entry defaults
   to Yes.

If the summary warns that `~/.local/bin` is not on `PATH`, add it in your shell
configuration, or start Strata from your launcher.

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
Trash, Network, and your standard folders, with **PINNED** and **DEVICES**
below. If Strata finds an Omarchy theme, it follows it; otherwise it starts in
Tokyo Night.

Try these three things first:

1. **Switch views.** Press Ctrl+1 for Columns, Ctrl+2 for Icons, and Ctrl+3 for
   List. Strata remembers your choice.
2. **Preview a file.** Click an image or text file, or select it and press
   Space. Press Space again to close the preview. Double-click opens it.
3. **Search everywhere.** Press Ctrl+K and type part of a name. Search covers
   your home folder and mounted local drives, wherever you are.

Forgot a key? Press F1, or click **Shortcuts** in the footer, to search every
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
