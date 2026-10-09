---
title: Release installer
status: shipped
origin: {issue: lgse/strata#329, pr: lgse/strata#330}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [install.sh]
tests: [scripts/test_installer.py]
related: [integration/file-manager-interface, integration/portal-file-chooser/setup, devices/volumes/udiskie-unlock]
---

## Summary

`install.sh`, a Bash installer that checks the system, installs runtime dependencies on Arch-based systems, and installs the latest verified stable release to `~/.local/bin/strata`. It runs interactively or unattended with `--with-*` flags. Its "Open file location", file chooser, and udiskie unlock steps belong to `integration/file-manager-interface`, `integration/portal-file-chooser/setup`, and `devices/volumes/udiskie-unlock`.

## Behavior

### System checks

- Run as root, the installer exits with "Run this installer as your normal desktop user, not as root." lgse/strata#330 (unverified)
- Run interactively without a readable and writable `/dev/tty`, it exits with "This interactive installer needs a terminal." lgse/strata#330 (unverified)
- A machine other than x86_64 or aarch64 exits with "Strata has no prebuilt release for <machine>." lgse/strata#330
- glibc older than 2.39 exits with "Strata requires glibc 2.39 or newer (found <version>)." lgse/strata#330
- Before installing, it prints "Linux distribution:", "Architecture:" (the release target triple), "glibc:", and "Omarchy: major version N" or "Omarchy: not detected". lgse/strata#330
- The Omarchy major is the first `3.N` or `4.N` token, not after a digit or dot, in `omarchy version`, `/usr/share/omarchy/version`, then `~/.local/share/omarchy/version`. lgse/strata#743
- `omarchy version` output of `dev (b280f130)` or `Omarchy 2.3.1` is not detected as Omarchy 3. lgse/strata#743

### Dependencies

- On Arch, an `ID_LIKE` containing `arch`, or Omarchy, missing required packages are listed and installed with `sudo pacman -S --needed` after "Install these packages with sudo pacman?" [Y/n]. lgse/strata#330
- Under `curl … | bash`, pacman's own confirmation reads from the terminal rather than the script pipe. lgse/strata#748
- On those systems it asks separately whether to install SMB support (`gvfs-smb`) and RAW support (`imagemagick`, `libraw`, `dcraw`), both defaulting to No. lgse/strata#332
- On other distributions it lists the required libraries, including the GVfs UDisks2 volume monitor, and exits unless the user confirms they are installed. lgse/strata#330, lgse/strata#536

### Download and verification

- The installer downloads the latest stable release only; a latest tag not shaped `vX.Y.Z` exits with an error. lgse/strata#330 (unverified)
- The archive must pass `sha256sum --check` against its published `.sha256` file before anything is extracted. lgse/strata#330, lgse/strata#775
- Without `gh`, or with `gh` logged out, it warns and continues after the checksum check without asking for a GitHub login. lgse/strata#775
- With an authenticated `gh`, it runs `gh attestation verify`, and a failed verification stops the install. lgse/strata#775
- An archive without an executable `strata`, the desktop entry, or the icon exits before installing. lgse/strata#330 (unverified)

### Install

- The binary is installed to `~/.local/bin/strata`. lgse/strata#330
- When that file exists, the interactive installer asks "Replace the existing …?" with default No; the unattended installer exits instead. lgse/strata#332 (unverified)
- The summary prints the installed version, the archive's `SOURCE_COMMIT` when present, the binary path, and a warning when `~/.local/bin` is not on `PATH`. lgse/strata#330 (unverified)

### Desktop entry and folder association

- "Add Strata to your desktop application menu?" defaults to Yes and installs the icon and entry under `$XDG_DATA_HOME`, with `Exec` set to the installed binary. lgse/strata#330
- After a Yes there, "Make Strata the default application for opening folders?" defaults to No. lgse/strata#330
- Accepting the folder association sets Strata as the `inode/directory` default and exits with an error if `xdg-mime query` then reports another handler. lgse/strata#330 (unverified)
- Accepting the folder association also installs the "Open file location" service without asking. lgse/strata#317

### Omarchy keybinds

- "Replace Omarchy's Nautilus file-manager keybinds with Strata?" defaults to No. lgse/strata#330
- The interactive installer asks that question even when Omarchy is not detected; answering Yes then exits with an error. lgse/strata#330 (unverified)
- Accepting appends a marked block that rebinds Super+Shift+F and Super+Alt+Shift+F to Strata, in `~/.config/hypr/bindings.conf` on Omarchy 3 or `bindings.lua` on Omarchy 4. lgse/strata#330, lgse/strata#743
- An existing bindings file is backed up as `<file>.bak.<timestamp>` before the block is appended. lgse/strata#330
- When `hyprctl configerrors` reports errors after reload, the previous file is restored and the installer exits with Hyprland's errors. lgse/strata#330
- Running the installer again with the block present leaves the file unchanged. lgse/strata#330 (unverified)
- Without a running Hyprland, the block is written and a warning says the file could not be reloaded. lgse/strata#330 (unverified)

### Unattended mode

- `--non-interactive` never prompts and installs only required packages and the binary. lgse/strata#332
- Any `--with-*` or `--without-file-chooser` flag implies `--non-interactive`; integrations not named are declined. lgse/strata#332
- `--with-folder-association` also selects `--with-desktop-entry` and `--with-file-manager`. lgse/strata#332, lgse/strata#317
- Unattended package installs run `sudo -n pacman --noconfirm`; when that fails, the error says passwordless sudo or cached credentials may be required. lgse/strata#332
- Unattended mode on a non-Arch system exits with "Non-interactive dependency installation currently supports Arch-based systems only." lgse/strata#332 (unverified)
- `--with-omarchy-keybinds` without Omarchy 3 or 4 exits with "--with-omarchy-keybinds requires Omarchy 3 or 4." lgse/strata#332 (unverified)
- `--help` prints the options; an unknown option exits with "Unknown option: <option> (run with --help for usage)." lgse/strata#332 (unverified)

## Design

The manual archive steps were accurate but hard to follow safely: pick the architecture, install dependencies, find the release, verify it, place desktop metadata, and edit two Omarchy keybind formats. One verified installer was chosen over an unverified curl-only script or separate scripts per Omarchy version (lgse/strata#329).

- Optional integrations stay opt-in. Unattended mode enabling every integration was rejected because associations and keybinds would be too invasive (lgse/strata#331).
- The SHA-256 check is mandatory. Attestation runs only with an authenticated `gh`, because `gh attestation verify` needs a login even for a public repository. Dropping attestation was rejected: it proves CI built the release (lgse/strata#731).
- Omarchy detection prints nothing rather than guess. Taking any `3` or `4` read a dev build's commit hash as Omarchy 3 and wrote bindings Omarchy 4 never loads (lgse/strata#652).
- Prompts, including pacman's, read from `/dev/tty`, because `curl … | bash` binds stdin to the script (lgse/strata#682).
- Keybind changes are backed up, validated by Hyprland, and rolled back on error (lgse/strata#330).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-13 | lgse/strata#743 | fix | Required a whole version token for the Omarchy major so dev-build hashes no longer select Omarchy 3. |
| 2026-09-10 | lgse/strata#775 | fix | Made GitHub CLI and attestation optional, keeping checksum verification mandatory. |
| 2026-09-10 | lgse/strata#748 | fix | Read pacman's interactive prompt from the terminal when the installer is piped into Bash. |
| 2026-09-05 | lgse/strata#332 | feat | Added the RAW dependency prompt and `--non-interactive` and `--with-*` flags that enable only named integrations. |
| 2026-09-05 | lgse/strata#330 | feat | Added the interactive installer for verified stable releases with dependency, desktop, and Omarchy keybind steps. |

## Known gaps

- The README pipes `install.sh` from the mutable `main` branch, so the installer runs before anything authenticates it. lgse/strata#334
