---
title: udiskie unlock handler
status: shipped
origin: {issue: lgse/strata#537, pr: lgse/strata#1047}
branch: null
reviewed_at: 5f17c9fdc8967e1b4ba8aaf8de113b46d824b0dd
review: draft
code: [src/ui/window/unlock_argument.rs, crates/strata-desktop/src/portal_setup/udiskie.rs, src/ui/udiskie_preferences.rs, data/udiskie/unlock]
tests: [src/ui/window/unlock_argument/tests.rs, crates/strata-desktop/src/portal_setup/udiskie/tests.rs, src/ui/udiskie_preferences/tests.rs]
docs: [docs/packaging.md, docs/preferences.md, docs/internationalization.md]
related: [app/packaging/installer, devices/volumes/encrypted, integration/portal-file-chooser/setup, settings/preferences]
---

## Summary

An integration that makes udiskie open Strata's passphrase prompt when an encrypted drive is plugged in, instead of udiskie's own dialog. Aimed at Omarchy, where udiskie is the automounter. It adds `--udiskie-hook`, `--unlock-volume`, install and uninstall flags, and a Settings row. The installer step is on `app/packaging/installer`; since lgse/strata#1825 it is on by default on an Arch-based system with `udiskie` on `PATH`.

## Behavior

### Hook and command line

- `strata --udiskie-hook device_added crypto DEVICE UUID` replaces itself with `strata --unlock-volume DEVICE`, or with the UUID when DEVICE is empty. lgse/strata#1047
- For any other event or a non-crypto `id_usage`, the hook exits successfully without opening Strata. lgse/strata#1047
- `strata --unlock-volume` with a device path or LUKS UUID opens a window and shows the themed passphrase prompt for that volume. lgse/strata#1047
- If the volume has not appeared after 1 second, the window shows "Waiting for encrypted volume…" with Cancel. lgse/strata#1047 (unverified)
- If no matching volume appears within 8 seconds, the window shows "The encrypted volume was not found". lgse/strata#1047 (unverified)
- A matching volume that is not encrypted shows "This is not an encrypted volume", including one already listed when the window opens. lgse/strata#1047, lgse/strata#2027
- An operand that neither starts with `/` nor parses as a LUKS UUID fails with "invalid --unlock-volume operand". lgse/strata#1047 (unverified)
- `--unlock-volume` combined with file arguments fails with "cannot combine --unlock-volume with file arguments". lgse/strata#1047 (unverified)
- With Strata already running, either usage error prints to the invoking terminal's stderr, not the running instance's log, and the command exits with status 1. lgse/strata#2030

### Install and restore

- The installed udiskie `event_hook` is `strata --udiskie-hook {event} {id_usage} {device_file} {id_uuid}`. lgse/strata#1047
- Plugging in a locked LUKS volume after setup opens Strata's themed password prompt, not udiskie's dialog. lgse/strata#1047
- In a default build, `strata --install-udiskie-unlock` rewrites `~/.config/udiskie/config.yml` with a managed header, a Strata `event_hook`, `password_prompt: false`, and a rule turning off LUKS automount. lgse/strata#1047, lgse/strata#1975
- Install records restore state under `~/.local/share/strata/udiskie-install/` and restarts udiskie. lgse/strata#1047
- Install keeps the original `config.yml` or `config.json` there as `config.yml.bak` or `config.json.bak` until uninstall. lgse/strata#2030
- When only `~/.config/udiskie/config.json` exists, install converts it to `config.yml` and removes it; uninstall writes it back as JSON. lgse/strata#1047 (unverified)
- When no udiskie process is running, install starts `udiskie --automount --no-notify --no-tray`; uninstall restarts udiskie only if it is running. lgse/strata#1047 (unverified)
- In a default build, `strata --uninstall-udiskie-unlock` restores the previous udiskie configuration and removes the restore state. lgse/strata#1047, lgse/strata#1975, lgse/strata#2030
- When the restored settings equal the original file's, uninstall writes the original back byte for byte, comments and formatting included. lgse/strata#2030
- Otherwise uninstall rewrites the settings, keeping the user's later edits and removing only Strata's. lgse/strata#1047, lgse/strata#2030
- A rewritten `config.json` ends with a newline. lgse/strata#2030
- A setup made by a Strata version without the `.bak` backup is rewritten on uninstall, not restored byte for byte. lgse/strata#2030
- Uninstall removes `~/.config/udiskie/` when install created it and it is empty. lgse/strata#2030
- If udiskie cannot be restarted, the command reports "Saved the udiskie configuration. Restart udiskie or log out for it to take effect." lgse/strata#1047 (unverified)
- Install and uninstall print their result in the system locale, such as Hungarian under `LANG=hu_HU.UTF-8`, not the saved app language. lgse/strata#2027
- The restart warning is translated in the same locale. lgse/strata#2027
- Install refuses to edit a configuration whose `program_options` is not a mapping or whose `device_config` is not a sequence. lgse/strata#1047 (unverified)
- Install and uninstall refuse a `config.yml` that is a symlink or other non-regular file, reporting "Refusing to replace non-regular udiskie configuration". lgse/strata#1047 (unverified)
- Neither command installs or removes the `udiskie` package. lgse/strata#1047
- In a `STRATA_INTEGRATIONS=package` build, `--install-udiskie-unlock` and `--uninstall-udiskie-unlock` exit with status 1 and leave udiskie's configuration unchanged. lgse/strata#1975
- Each prints "The package that installed this build provides its desktop integrations. Configure them in your system configuration instead." lgse/strata#1975
- In a package build, `--udiskie-hook` runs as in a default build. lgse/strata#1975

### Settings

- In a default build, Settings → General → Desktop integration shows "Unlock encrypted volumes" only when Omarchy is detected and `udiskie` is on `PATH`. lgse/strata#1047, lgse/strata#1975
- In a default build, the row's Use Strata button installs the integration and Restore default removes it. lgse/strata#1047
- Use Strata shows only while the integration is not configured; Restore default shows only while restore state or a Strata-managed config exists. lgse/strata#1047 (unverified)
- When Use Strata or Restore default saves but udiskie cannot restart, the row shows the "Saved the udiskie configuration…" warning as a non-error message. lgse/strata#2030
- That warning stays until the next change on the row. lgse/strata#2030
- The row's 2-second availability poll runs only while Settings is shown, so availability can lag up to 2 seconds after Settings opens. lgse/strata#2054
- In a package build, the row shows only its title and "The package that installed this build provides the udiskie unlock hook. Configure udiskie in your system configuration as the package documentation describes." lgse/strata#1975
- In a package build, the row has no status line, Use Strata, or Restore default. lgse/strata#1975
- In a package build, the row shows without Omarchy and without `udiskie` on `PATH`. lgse/strata#1975 (unverified)

## Design

The README section "Unlock encrypted volumes on Omarchy" documents setup and restore. [docs/preferences.md](https://github.com/lgse/strata/blob/aee71335dfecd059b9af23efeac2ed52c43e3b19/docs/preferences.md) records that the integration is not a Strata preference. [docs/packaging.md](https://github.com/lgse/strata/blob/aee71335dfecd059b9af23efeac2ed52c43e3b19/docs/packaging.md) forbids packages from running the install flag.

- On Omarchy, plugging in a LUKS drive raised another program's prompt, not Strata's (lgse/strata#537). Disabling the user's automounter was ruled out, so udiskie hands encrypted `device_added` events to Strata and stops automounting LUKS (lgse/strata#1047).
- The hook is classified before GTK starts and execs `--unlock-volume`, so non-crypto events never open a window (lgse/strata#1047).
- The integration edits udiskie's file, not Strata preferences. Install records the previous `event_hook` and `password_prompt` values and whether it added the LUKS rule, so restore reverts only those keys (lgse/strata#1047).
- `--unlock-volume` starts its unlock after the window's first folder opens. That folder's reset clears every open-argument status card, so an unlock resolved earlier lost its card at once (lgse/strata#2007, lgse/strata#2027).
- With a primary instance running, usage errors reach the invoking terminal through `g_application_command_line_printerr`, the FFI call `app/infrastructure` records (lgse/strata#2015, lgse/strata#2030).
- Install backs up the original file so restore can keep its comments and formatting. Uninstall compares parsed settings, so later user edits still win (lgse/strata#2015, lgse/strata#2030).
- Settings used to show only a green check when udiskie could not restart, so the save looked complete (lgse/strata#2015, lgse/strata#2030).
- The install and uninstall modes print in the system locale, as the installer that runs them does (lgse/strata#2027).
- In a default build, Settings is gated to Omarchy; the CLI flags are unattended and not gated (lgse/strata#1047).
- A `STRATA_INTEGRATIONS=package` build drops the Settings actions and refuses the CLI flags. A store-based package configures the hook as a `services.udiskie.settings` entry, and a runtime install would record a stale store path (lgse/strata#1969, lgse/strata#1975).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-11-05 | lgse/strata#2054 | perf | Polled the Settings row's udiskie availability only while Settings is shown, so a pre-built hidden layer does not poll all session. |
| 2026-11-02 | lgse/strata#2027 | fix | Started `--unlock-volume` after the first folder opens so its status card survives, and translated the udiskie setup output. |
| 2026-09-17 | lgse/strata#1047 | feat | Let udiskie hand encrypted-drive events to Strata's passphrase prompt through an opt-in config rewrite. |

## Known gaps

- A first install that fails after creating `~/.config/udiskie/` rolls back the files but leaves the folder, so a later uninstall never removes it. lgse/strata#2030
