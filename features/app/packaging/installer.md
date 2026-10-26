---
title: Release installer
status: shipped
origin: {issue: lgse/strata#329, pr: lgse/strata#330}
branch: null
reviewed_at: be3343a5992a2a5497b1a2ee7faa525be18e988f
review: draft
code: [install.sh, data/locales/installer.json, scripts/installer_messages.py]
tests: [scripts/test_installer.py]
docs: [docs/internationalization.md, docs/signed-updates.md]
related: [integration/file-manager-interface, integration/portal-file-chooser/setup, devices/volumes/udiskie-unlock, settings/preferences/language]
---

## Summary

`install.sh`, a localized Bash installer for the latest stable release, installed to `~/.local/bin/strata`. It authenticates the release through its signed update manifest. It checks the system and installs every integration the system supports, or a custom selection from a menu. It runs interactively or unattended with `--with-*` and `--without-*` flags. What the "Open file location", file chooser, and udiskie unlock steps install belongs to `integration/file-manager-interface`, `integration/portal-file-chooser/setup`, and `devices/volumes/udiskie-unlock`.

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
- The recommended setup's hint reads "Everything this system supports: launcher, folders, file chooser, and optional integrations." lgse/strata#1825
- The recommended setup selects every option the menu offers for the system. lgse/strata#1825
- "Customize installation" opens "Make Strata yours" with every offered option checked; unchecking an option declines it. lgse/strata#1825
- The plan reads "Your default apps and shortcuts will stay unchanged." only when nothing beyond Application launcher, Windows network shares, and Camera RAW support is selected. lgse/strata#1825 (unverified)
- On an Arch-based system, the menu adds Windows network shares when `gvfs-smb` is missing, and Camera RAW support when `imagemagick`, `libraw`, or `dcraw` is missing. lgse/strata#1730
- Omarchy file-manager shortcuts is offered only when Omarchy 3 or 4 is detected. lgse/strata#1727, lgse/strata#1730
- Encrypted-drive unlock is offered only on an Arch-based system or Omarchy with `udiskie` on `PATH`. lgse/strata#1047, lgse/strata#1730, lgse/strata#1825
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
- Without `openssl` on `PATH`, the installer exits with "Required command not found: openssl" before downloading anything. lgse/strata#1825
- A missing `curl`, `tar`, `sha256sum`, `wc`, `install`, or `sed` exits the same way. lgse/strata#1825 (unverified)
- A missing `timeout` exits with "Required command not found: timeout" at the same check. lgse/strata#1876
- Before the archive, it downloads `strata-update-manifest.json` (at most 32,768 bytes) and `strata-update-manifest.signatures.json` (at most 8,192 bytes) from the release. lgse/strata#1825
- curl refuses a larger manifest or signatures file, failing its download step. lgse/strata#1825
- A release with no manifest or signatures file fails "Download the signed release manifest" or "Download the release signatures" before the archive is requested. lgse/strata#1825
- When no signature verifies against a key pinned in `RELEASE_PUBLIC_KEYS`, the step "Verify the release signature" fails with "No trusted release key signed strata-update-manifest.json." lgse/strata#1825
- One valid signature from any pinned key is enough. lgse/strata#1825
- A signed manifest for another repository or tag stops the install with "The signed manifest does not describe Strata <version> from lgse/strata." lgse/strata#1825
- A signed manifest without the archive for the detected target stops it with "The signed manifest does not list <archive> for <target>." lgse/strata#1825
- A signed archive size over 134,217,728 bytes stops it with "The signed manifest lists an archive larger than 134217728 bytes." lgse/strata#1825 (unverified)
- An archive larger than its signed size fails the download step, because curl caps the download at that size. lgse/strata#1825
- A shorter or altered archive fails "Verify the signed SHA-256 digest" before extraction. lgse/strata#1825
- That step prints "<archive> is <n> bytes; the signed manifest expects <m>." or "<archive> has SHA-256 <d>; the signed manifest expects <e>." lgse/strata#1825
- The installer never uses `gh`, the release's `.sha256` file, or `gh attestation verify`, and prints no GitHub CLI note. lgse/strata#1825
- A failed download, signature, or digest check installs no package and writes nothing to `~/.local/bin`. lgse/strata#1730, lgse/strata#1825
- Ctrl+C during the download stops the transfer and exits with status 130, installing no package and no binary. lgse/strata#1730 (unverified)
- An archive without an executable `strata`, the desktop entry, or the icon exits before installing. lgse/strata#330 (unverified)
- With `--with-file-chooser`, a release without `portal/strata.portal` exits with "This release does not include file chooser integration. Install a newer release." before installing. lgse/strata#1730, lgse/strata#1825 (unverified)
- With `--with-udiskie-unlock`, a release without `udiskie/unlock` exits with "This release does not include encrypted-volume integration. Install a newer release." before installing packages or the binary. lgse/strata#1047, lgse/strata#1730, lgse/strata#1825 (unverified)
- When either integration was selected without its `--with-*` flag, including from the menus, the installer skips it instead. lgse/strata#1825 (unverified)
- It then warns "This release does not include <file chooser or encrypted-volume> integration; skipping it.", and the heading reads "Installed with warnings". lgse/strata#1825 (unverified)
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
- Error lines such as "Unknown option: …" and the signature and digest errors stay English in every locale. lgse/strata#1730, lgse/strata#1825 (unverified)
- With `LANGUAGE=zz:fr` and `LC_ALL=C.UTF-8`, the plan reads "Installer dans <path>". lgse/strata#1730 (unverified)
- With `LANGUAGE=fr` and `LC_ALL=C`, the plan reads "Install to <path>". lgse/strata#1730 (unverified)
- `zh_TW`, `zh_HK`, `zh_MO`, and `zh-Hant…` show Traditional Chinese messages; every other `zh` locale shows Simplified Chinese. lgse/strata#1745
- Paths in messages show literally, even when they hold `&` or `%{version}`. lgse/strata#1730 (unverified)
- The installer ignores the language saved in Strata's Settings. lgse/strata#1730

### Desktop integrations

- Application launcher installs the icon and entry under `$XDG_DATA_HOME`, with `Exec` set to the installed binary. lgse/strata#330, lgse/strata#1730
- Default file manager sets Strata as the `inode/directory` default and exits with an error if `xdg-mime query` then reports another handler. lgse/strata#330 (unverified)
- An `xdg-mime default` or `query` call that runs past 5 s fails the step with status 124. The installer prints "Strata is installed, but setup did not finish." lgse/strata#1876
- Open file location writes `$XDG_DATA_HOME/dbus-1/services/io.github.lgse.Strata.FileManager1.service` with `Exec=` pointing at the installed binary. lgse/strata#317, lgse/strata#1730
- After writing the "Open file location" service, the installer calls `org.freedesktop.DBus.ReloadConfig` on the session bus with a 5 s timeout. lgse/strata#1728
- That call runs under `timeout 5`, so a session bus socket that accepts the connection and never answers ends it after 5 s. lgse/strata#1876
- Strata then answers reveal requests in that session without a re-login. lgse/strata#1699, lgse/strata#1728
- A successful reload prints `Strata now handles "Open file location" requests.` lgse/strata#1728
- When the reload fails, times out, or `gdbus` is missing, the service stays installed and the installer warns "…could not reload the session bus. Log out and back in…" and continues. lgse/strata#1728, lgse/strata#1876
- When `xdg-mime` returns, the file chooser, Omarchy keybind, and udiskie steps and the summary still run after that warning. lgse/strata#1876
- Folder association runs before the reload, so an `xdg-mime` blocked on a silent bus stops the install there with status 124. lgse/strata#1876
- A failed service write, or another per-user FileManager1 provider, exits the installer before any reload; later integrations do not run. lgse/strata#1728
- Checking Open and Save dialogs, or passing `--with-file-chooser`, runs the installed binary with `--install-portal`. lgse/strata#175, lgse/strata#1730
- Open and Save dialogs left unchecked, or `--without-file-chooser`, runs `--dismiss-portal-prompt` when the release ships `portal/strata.portal`. lgse/strata#1730, lgse/strata#1825

### Omarchy keybinds

- Selecting Omarchy file-manager shortcuts appends a marked block that rebinds Super+Shift+F and Super+Alt+Shift+F to Strata, in `~/.config/hypr/bindings.conf` on Omarchy 3 or `bindings.lua` on Omarchy 4. lgse/strata#330, lgse/strata#743, lgse/strata#1730
- An existing bindings file is backed up as `<file>.bak.<timestamp>` before the block is appended. lgse/strata#330
- When `hyprctl configerrors` reports errors after reload, the previous file is restored and the installer exits with Hyprland's errors. lgse/strata#330
- Running the installer again with the block present leaves the file unchanged. lgse/strata#330 (unverified)
- Without a running Hyprland, the block is written and a warning says the file could not be reloaded. lgse/strata#330 (unverified)

### Unattended mode

- `--non-interactive` never prompts and installs every integration the system supports. lgse/strata#1825
- Any `--with-*` or `--without-*` flag implies `--non-interactive`. lgse/strata#332, lgse/strata#1825
- `--without-smb`, `--without-raw`, `--without-desktop-entry`, `--without-folder-association`, `--without-file-manager`, `--without-file-chooser`, `--without-omarchy-keybinds`, and `--without-udiskie-unlock` each decline one integration. lgse/strata#1825
- `--without-desktop-entry` and `--without-file-manager` also decline folder association. lgse/strata#1825
- Unattended on an Arch-based system, Windows network shares and Camera RAW support are planned even when their packages are already installed. lgse/strata#1825 (unverified)
- `--with-folder-association` also selects `--with-desktop-entry` and `--with-file-manager`. lgse/strata#332, lgse/strata#317
- Unattended package installs run `sudo -n pacman --noconfirm`; when that fails, the error says passwordless sudo or cached credentials may be required. lgse/strata#332
- Unattended mode on a non-Arch system exits with "Non-interactive dependency installation currently supports Arch-based systems only." lgse/strata#332 (unverified)
- `--with-omarchy-keybinds` without Omarchy 3 or 4 exits with "--with-omarchy-keybinds requires Omarchy 3 or 4." before any download or package install. lgse/strata#332, lgse/strata#1730
- On an Arch-based system or Omarchy without `udiskie` on `PATH`, `--with-udiskie-unlock` exits with "--with-udiskie-unlock requires an Arch-based system with udiskie on PATH." before any download. lgse/strata#1730
- `--non-interactive` on an Arch-based system with `udiskie` on `PATH` installs Encrypted-drive unlock unless `--without-udiskie-unlock` is passed. lgse/strata#1825
- `--help` prints the options, including `--verbose`; an unknown option exits with "Unknown option: <option> (run with --help for usage)." lgse/strata#332, lgse/strata#1730 (unverified)

## Design

The manual archive steps were accurate but hard to follow safely: pick the architecture, install dependencies, find the release, verify it, place desktop metadata, and edit two Omarchy keybind formats. One verified installer was chosen over an unverified curl-only script or separate scripts per Omarchy version (lgse/strata#329).

- Every supported integration installs by default, with a `--without-*` flag to decline each one, at the owner's request (lgse/strata#1825). This reverses the earlier opt-in rule, which held associations and keybinds too invasive (lgse/strata#331).
- The installer offers only integrations the system supports and rejects unsupported explicit flags before changing anything, so an unsupported integration never fails after the install has begun. On Manjaro without Omarchy, accepting the keybind question aborted after everything else was installed (lgse/strata#1727, lgse/strata#1730).
- Packages install in one transaction, after the release is verified, with the package manager's own confirmation (lgse/strata#1730).
- Installer strings live in `data/locales/installer.json`, and `scripts/installer_messages.py --write` embeds them into `install.sh`. The installer needs no translation files, Python, or Strata binary at run time (lgse/strata#1730, docs/internationalization.md).
- A `.sha256` file from the same release proves integrity but not authenticity, and most first installs have no authenticated `gh` for attestation. Making `gh` mandatory was rejected (lgse/strata#1817, https://github.com/lgse/strata/issues/1817#issuecomment-6366875203). This replaces the SHA-256-plus-optional-attestation check (lgse/strata#731).
- Reusing the updater's Ed25519-signed manifest leaves one trust root to rotate, and rotation already supports overlapping signatures (https://github.com/lgse/strata/issues/1817#issuecomment-6366875203, docs/signed-updates.md). A rotation updates `data/update-keys.json` and `RELEASE_PUBLIC_KEYS` together (lgse/strata#1825).
- Bash has no Ed25519 and a bespoke implementation was ruled out (https://github.com/lgse/strata/issues/1817#issuecomment-6366875203). The planned `python3` fallback was dropped because its standard library cannot verify Ed25519 (https://github.com/lgse/strata/issues/1817#issuecomment-6367178656).
- Every integrity failure stops the install before the archive is unpacked (lgse/strata#1825, docs/signed-updates.md).
- The session bus reads service directories only at startup or on `ReloadConfig`, so the installer reloads it as the Settings path already did. The call is bounded to 5 s, and a failure does not stop the install: the service still works after the next login (lgse/strata#1699, lgse/strata#1728, lgse/strata#1876).
- `gdbus --timeout` counts only the method call, which starts after connect, authentication, and `Hello`. A peer that never answers `AUTH` blocks it forever, so the 5 s deadline is on the process (lgse/strata#1850, lgse/strata#1876).
- `xdg-mime` on a desktop it does not recognize, such as Hyprland, calls `dbus-send`, which blocks on a silent bus the same way. Both `xdg-mime` calls are bounded too (lgse/strata#1876).
- Omarchy detection prints nothing rather than guess. Taking any `3` or `4` read a dev build's commit hash as Omarchy 3 and wrote bindings Omarchy 4 never loads (lgse/strata#652).
- Prompts, including pacman's, read from `/dev/tty`, because `curl … | bash` binds stdin to the script (lgse/strata#682).
- Keybind changes are backed up, validated by Hyprland, and rolled back on error (lgse/strata#330).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-25 | lgse/strata#1876 | fix | Bounded the ReloadConfig and xdg-mime calls with a 5 s process deadline, so a session bus that never answers no longer hangs the installer. |
| 2026-10-23 | lgse/strata#1825 | feat | Verified releases through the signed update manifest instead of `gh`, and installed every supported integration by default with `--without-*` flags. |
| 2026-10-17 | lgse/strata#1728 | fix | Reloaded the session bus after installing the FileManager1 service, so "Open file location" uses Strata without a re-login. |
| 2026-10-17 | lgse/strata#1730 | fix | Replaced per-step questions with a recommended setup or a menu of supported integrations, and rejected unsupported flags up front. |
| 2026-09-13 | lgse/strata#743 | fix | Required a whole version token for the Omarchy major so dev-build hashes no longer select Omarchy 3. |
| 2026-09-10 | lgse/strata#775 | fix | Made GitHub CLI and attestation optional, keeping checksum verification mandatory. |
| 2026-09-10 | lgse/strata#748 | fix | Read pacman's interactive prompt from the terminal when the installer is piped into Bash. |
| 2026-09-05 | lgse/strata#332 | feat | Added the RAW dependency prompt and `--non-interactive` and `--with-*` flags that enable only named integrations. |
| 2026-09-05 | lgse/strata#330 | feat | Added the interactive installer for verified stable releases with dependency, desktop, and Omarchy keybind steps. |

## Known gaps

None known.
