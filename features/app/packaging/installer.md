---
title: Release installer
status: shipped
origin: {issue: lgse/strata#329, pr: lgse/strata#330}
branch: null
reviewed_at: e0f73973926ff67e77c2c56cf288b7b7617bb2e5
review: draft
code: [install.sh, data/locales/installer.json, scripts/installer_messages.py]
tests: [scripts/test_installer.py]
docs: [docs/internationalization.md]
related: [integration/file-manager-interface, integration/portal-file-chooser/setup, devices/volumes/udiskie-unlock, settings/preferences/language]
---

## Summary

`install.sh`, a localized Bash installer for the latest verified stable release, installed to `~/.local/bin/strata`. It checks the system and offers a recommended setup or a menu of the integrations the system supports. It runs interactively or unattended with `--with-*` flags. What the "Open file location", file chooser, and udiskie unlock steps install belongs to `integration/file-manager-interface`, `integration/portal-file-chooser/setup`, and `devices/volumes/udiskie-unlock`.

## Behavior

### System checks

- Run as root, the installer exits with "Run this installer as your normal desktop user, not as root." lgse/strata#330 (unverified)
- Run interactively without a readable and writable `/dev/tty`, it exits with "This interactive installer needs a terminal." lgse/strata#330 (unverified)
- A machine other than x86_64 or aarch64 exits with "Strata has no prebuilt release for <machine>." lgse/strata#330
- glibc older than 2.39 exits with "Strata requires glibc 2.39 or newer (found <version>)." lgse/strata#330
- Before the setup menu, it prints one dim line, `<PRETTY_NAME or ID> · <arch>`, such as `Manjaro Linux · x86_64`. lgse/strata#1730 (unverified)
- It prints no glibc or Omarchy line. lgse/strata#1730 (unverified)
- The Omarchy major is the first `3.N` or `4.N` token, not after a digit or dot, in `omarchy version`, `/usr/share/omarchy/version`, then `~/.local/share/omarchy/version`. lgse/strata#743
- `omarchy version` output of `dev (b280f130)` or `Omarchy 2.3.1` is not detected as Omarchy 3. lgse/strata#743

### Setup menu

- An interactive run shows "Choose your setup" with "Install Strata (recommended)" and "Customize installation". lgse/strata#1730
- The recommended setup selects only the application launcher. On Arch it still installs missing required packages, and the plan reads "Your default apps and shortcuts will stay unchanged." lgse/strata#1730
- "Customize installation" opens "Make Strata yours": Application launcher checked, and Default file manager, Open file location, and Open and Save dialogs unchecked. lgse/strata#1730
- On an Arch-based system, the menu adds Windows network shares when `gvfs-smb` is missing, and Camera RAW support when `imagemagick`, `libraw`, or `dcraw` is missing. lgse/strata#1730
- Omarchy file-manager shortcuts is offered only when Omarchy 3 or 4 is detected. lgse/strata#1727, lgse/strata#1730
- Encrypted-drive unlock is offered, unchecked, only on an Arch-based system or Omarchy with `udiskie` on `PATH`. lgse/strata#1047, lgse/strata#1730
- Every option the menu adds for the system starts unchecked, so the recommended setup leaves them all off. lgse/strata#1730 (unverified)
- Checking Default file manager also checks Application launcher and Open file location; unchecking either of those unchecks Default file manager. lgse/strata#1730 (unverified)
- In a terminal of at least 24 rows and 64 columns, menus take keys. Up and Down or `k` and `j` move with wrapping. lgse/strata#1730
- In such a menu, Space toggles an option and Enter continues or installs. lgse/strata#1730
- Escape or `q` in a menu prints "Installation cancelled. No changes made." and exits with status 0, leaving an existing install untouched. lgse/strata#1730
- When stdout is not a terminal, `TERM=dumb`, or the terminal is smaller, menus are numbered. lgse/strata#1730
- In a numbered menu, a number chooses or toggles an option, Enter installs or picks option 1, and `q` cancels. lgse/strata#1730
- In a numbered menu, an entry that names no option prints "Choose one of the listed options." lgse/strata#1730 (unverified)
- With stdout redirected to a file, the menus still draw on the terminal and the file holds no terminal control sequences. lgse/strata#1730 (unverified)
- `NO_COLOR=1` keeps arrow-key navigation and prints no color. lgse/strata#1730
- The banner shows the block-art logo in pale-blue, blue, and violet truecolor, "S T R A T A", "Navigate every layer.", and "Interactive installer". lgse/strata#1730
- Before downloading, "Installation plan" lists "Install to <path>" and a "+ <option>" line for each selected integration. lgse/strata#1730 (unverified)

### Dependencies

- Arch, an `ID_LIKE` containing `arch`, and Omarchy count as Arch-based. lgse/strata#330
- On an Arch-based system, missing required packages and the selected `gvfs-smb`, RAW packages, and `xdg-desktop-portal` install in one `sudo pacman -S --needed` transaction. lgse/strata#1730
- Interactively, that transaction uses pacman's own confirmation. lgse/strata#1730
- An Arch-based or Omarchy system without `pacman` exits with "This Arch-based system does not provide pacman." lgse/strata#1730 (unverified)
- The package transaction runs after the release is downloaded, verified, and unpacked, and before the binary is installed. lgse/strata#1730
- The step prints "Packages to install: <packages>", or "All selected runtime packages are already installed." when none are missing. lgse/strata#1730 (unverified)
- Under `curl … | bash`, pacman's own confirmation reads from the terminal rather than the script pipe. lgse/strata#748
- pacman's output shows live and is kept in the log; the sudo password typed at its prompt is not recorded. lgse/strata#1730
- On other distributions it lists the required libraries, including the GVfs UDisks2 volume monitor, and exits unless the user confirms they are installed. lgse/strata#330, lgse/strata#536

### Download and verification

- The installer downloads the latest stable release only; a latest tag not shaped `vX.Y.Z` exits with an error. lgse/strata#330 (unverified)
- The archive must pass `sha256sum --check` against its published `.sha256` file before anything is extracted. lgse/strata#330, lgse/strata#775
- Without `gh`, it notes "GitHub CLI is unavailable; continuing after HTTPS download and checksum verification." and continues. lgse/strata#775, lgse/strata#1730
- With `gh` logged out, the note reads "GitHub CLI is not authenticated; …". lgse/strata#775, lgse/strata#1730
- The missing or logged-out `gh` note does not count as a warning, so the summary can still read "Ready to explore". lgse/strata#1730
- With an authenticated `gh`, it runs `gh attestation verify`, and a failed verification stops the install. lgse/strata#775
- A failed checksum or provenance check installs no package and writes nothing to `~/.local/bin`. lgse/strata#1730
- Ctrl+C during the download stops the transfer and exits with status 130, installing no package and no binary. lgse/strata#1730 (unverified)
- An archive without an executable `strata`, the desktop entry, or the icon exits before installing. lgse/strata#330 (unverified)
- With Open and Save dialogs selected, a release without `portal/strata.portal` exits with "This release does not include file chooser integration. Install a newer release." before installing. lgse/strata#1730 (unverified)
- With Encrypted-drive unlock selected, a release without `udiskie/unlock` exits with "This release does not include encrypted-volume integration. Install a newer release." before installing packages or the binary. lgse/strata#1047, lgse/strata#1730 (unverified)
- In a full-size terminal, the download shows a 27-cell bar with curl's real percentage, ending in a green ✓. lgse/strata#1730
- While the download total is unknown, a spinner replaces the bar. lgse/strata#1730
- In a full-size terminal, other steps show a spinner beside their label, then "✓ <label>". lgse/strata#1730
- `--verbose` shows each step's full download and verification output. lgse/strata#1730

### Install

- The binary is installed to `~/.local/bin/strata`. lgse/strata#330
- When that file exists, the interactive installer prints "This replaces <path>. Your saved settings are kept." and asks nothing more; the unattended installer exits before downloading. lgse/strata#332, lgse/strata#1730 (unverified)
- The summary heading reads "Ready to explore", "Installed with warnings", or "Installed — review setup details". lgse/strata#1730 (unverified)
- The summary then reads "Strata <version> is installed." and "Run <path> to get started." lgse/strata#1730 (unverified)
- When `~/.local/bin` is not on `PATH`, a warning says so and the heading reads "Installed with warnings". lgse/strata#330, lgse/strata#1730 (unverified)

### Logs and failures

- Every step's output goes to `${TMPDIR:-/tmp}/strata-install.XXXXXX.log`, deleted after a clean success and kept after a failure, a warning, or an integration notice. lgse/strata#1730
- After a warning or a notice, the summary ends with "Detailed output: <log>". lgse/strata#1730 (unverified)
- A failed step prints its output and "Failed: <step>", then "Installation did not finish." and "Detailed output: <log>". lgse/strata#1730
- A failure after the binary is installed reads "Strata is installed, but setup did not finish." instead. lgse/strata#1730
- Output from the file chooser and udiskie steps, such as service-restart notices, stays on screen and in the retained log. lgse/strata#1730
- After such a notice and no warning, the heading reads "Installed — review setup details". lgse/strata#1730 (unverified)
- When the udiskie step fails, the installer exits with "Encrypted-volume unlock setup failed. Strata is installed; retry with: <path> --install-udiskie-unlock". lgse/strata#1047, lgse/strata#1730 (unverified)

### Language

- When the first set of `LC_ALL`, `LC_MESSAGES`, and `LANG` is exactly `C` or `POSIX`, or when none is set, catalog text is English. lgse/strata#1730
- Otherwise catalog text follows the first supported `LANGUAGE` entry, then the `LC_ALL`, `LC_MESSAGES`, or `LANG` value. lgse/strata#1730
- Error lines such as "Unknown option: …" and the `gh` notes stay English in every locale. lgse/strata#1730 (unverified)
- With `LANGUAGE=zz:fr` and `LC_ALL=C.UTF-8`, the plan reads "Installer dans <path>". lgse/strata#1730 (unverified)
- With `LANGUAGE=fr` and `LC_ALL=C`, the plan reads "Install to <path>". lgse/strata#1730 (unverified)
- `zh_TW`, `zh_HK`, `zh_MO`, and `zh-Hant…` show Traditional Chinese messages; every other `zh` locale shows Simplified Chinese. lgse/strata#1745
- Paths in messages show literally, even when they hold `&` or `%{version}`. lgse/strata#1730 (unverified)
- The installer ignores the language saved in Strata's Settings. lgse/strata#1730

### Desktop integrations

- Application launcher installs the icon and entry under `$XDG_DATA_HOME`, with `Exec` set to the installed binary. lgse/strata#330, lgse/strata#1730
- Default file manager sets Strata as the `inode/directory` default and exits with an error if `xdg-mime query` then reports another handler. lgse/strata#330 (unverified)
- Open file location writes `$XDG_DATA_HOME/dbus-1/services/io.github.lgse.Strata.FileManager1.service` with `Exec=` pointing at the installed binary. lgse/strata#317, lgse/strata#1730
- After writing the "Open file location" service, the installer calls `org.freedesktop.DBus.ReloadConfig` on the session bus with a 5 s timeout. lgse/strata#1728
- Strata then answers reveal requests in that session without a re-login. lgse/strata#1699, lgse/strata#1728
- A successful reload prints `Strata now handles "Open file location" requests.` lgse/strata#1728
- When the reload fails, times out, or `gdbus` is missing, the service stays installed and the installer warns "…could not reload the session bus. Log out and back in…" and continues. lgse/strata#1728
- A failed service write, or another per-user FileManager1 provider, exits the installer before any reload; later integrations do not run. lgse/strata#1728
- Checking Open and Save dialogs, or passing `--with-file-chooser`, runs the installed binary with `--install-portal`. lgse/strata#175, lgse/strata#1730
- The recommended setup, the option left unchecked, or `--without-file-chooser` runs `--dismiss-portal-prompt` when the release ships `portal/strata.portal`. lgse/strata#1730

### Omarchy keybinds

- Selecting Omarchy file-manager shortcuts appends a marked block that rebinds Super+Shift+F and Super+Alt+Shift+F to Strata, in `~/.config/hypr/bindings.conf` on Omarchy 3 or `bindings.lua` on Omarchy 4. lgse/strata#330, lgse/strata#743, lgse/strata#1730
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
- `--with-omarchy-keybinds` without Omarchy 3 or 4 exits with "--with-omarchy-keybinds requires Omarchy 3 or 4." before any download or package install. lgse/strata#332, lgse/strata#1730
- On an Arch-based system or Omarchy without `udiskie` on `PATH`, `--with-udiskie-unlock` exits with "--with-udiskie-unlock requires an Arch-based system with udiskie on PATH." before any download. lgse/strata#1730
- `--non-interactive` leaves Encrypted-drive unlock declined unless `--with-udiskie-unlock` is passed. lgse/strata#1047
- `--help` prints the options, including `--verbose`; an unknown option exits with "Unknown option: <option> (run with --help for usage)." lgse/strata#332, lgse/strata#1730 (unverified)

## Design

The manual archive steps were accurate but hard to follow safely: pick the architecture, install dependencies, find the release, verify it, place desktop metadata, and edit two Omarchy keybind formats. One verified installer was chosen over an unverified curl-only script or separate scripts per Omarchy version (lgse/strata#329).

- Optional integrations stay opt-in. Unattended mode enabling every integration was rejected because associations and keybinds would be too invasive (lgse/strata#331).
- The installer offers only integrations the system supports and rejects unsupported explicit flags before changing anything, so an unsupported integration never fails after the install has begun. On Manjaro without Omarchy, accepting the keybind question aborted after everything else was installed (lgse/strata#1727, lgse/strata#1730).
- Packages install in one transaction, after the release is verified, with the package manager's own confirmation (lgse/strata#1730).
- Installer strings live in `data/locales/installer.json`, and `scripts/installer_messages.py --write` embeds them into `install.sh`. The installer needs no translation files, Python, or Strata binary at run time (lgse/strata#1730, docs/internationalization.md).
- The SHA-256 check is mandatory. Attestation runs only with an authenticated `gh`, because `gh attestation verify` needs a login even for a public repository. Dropping attestation was rejected: it proves CI built the release (lgse/strata#731).
- The session bus reads service directories only at startup or on `ReloadConfig`, so the installer reloads it as the Settings path already did. The call is bounded to 5 s, and a failure does not stop the install: the service still works after the next login (lgse/strata#1699, lgse/strata#1728).
- Omarchy detection prints nothing rather than guess. Taking any `3` or `4` read a dev build's commit hash as Omarchy 3 and wrote bindings Omarchy 4 never loads (lgse/strata#652).
- Prompts, including pacman's, read from `/dev/tty`, because `curl … | bash` binds stdin to the script (lgse/strata#682).
- Keybind changes are backed up, validated by Hyprland, and rolled back on error (lgse/strata#330).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-17 | lgse/strata#1728 | fix | Reloaded the session bus after installing the FileManager1 service, so "Open file location" uses Strata without a re-login. |
| 2026-10-17 | lgse/strata#1730 | fix | Replaced per-step questions with a recommended setup or a menu of supported integrations, and rejected unsupported flags up front. |
| 2026-09-13 | lgse/strata#743 | fix | Required a whole version token for the Omarchy major so dev-build hashes no longer select Omarchy 3. |
| 2026-09-10 | lgse/strata#775 | fix | Made GitHub CLI and attestation optional, keeping checksum verification mandatory. |
| 2026-09-10 | lgse/strata#748 | fix | Read pacman's interactive prompt from the terminal when the installer is piped into Bash. |
| 2026-09-05 | lgse/strata#332 | feat | Added the RAW dependency prompt and `--non-interactive` and `--with-*` flags that enable only named integrations. |
| 2026-09-05 | lgse/strata#330 | feat | Added the interactive installer for verified stable releases with dependency, desktop, and Omarchy keybind steps. |

## Known gaps

- The README pipes `install.sh` from the mutable `main` branch, so the installer runs before anything authenticates it. lgse/strata#334
