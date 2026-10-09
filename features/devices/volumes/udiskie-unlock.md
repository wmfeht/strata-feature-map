---
title: udiskie unlock handler
status: shipped
origin: {issue: lgse/strata#537, pr: lgse/strata#1047}
branch: null
reviewed_at: aee71335dfecd059b9af23efeac2ed52c43e3b19
review: reviewed
code: [src/ui/window/unlock_argument.rs, src/portal_setup/udiskie.rs, src/ui/udiskie_preferences.rs, data/udiskie/unlock]
tests: [src/ui/window/unlock_argument/tests.rs, src/portal_setup/udiskie/tests.rs, src/ui/udiskie_preferences/tests.rs]
docs: [docs/packaging.md, docs/preferences.md]
related: [devices/volumes/encrypted, integration/portal-file-chooser/setup, settings/preferences]
---

## Summary

An opt-in integration that makes udiskie open Strata's passphrase prompt when an encrypted drive is plugged in, instead of udiskie's own dialog. Aimed at Omarchy, where udiskie is the automounter. It adds `--udiskie-hook`, `--unlock-volume`, install and uninstall flags, an installer step, and a Settings row.

## Behavior

### Hook and command line

- `strata --udiskie-hook device_added crypto DEVICE UUID` replaces itself with `strata --unlock-volume DEVICE`, or with the UUID when DEVICE is empty. lgse/strata#1047
- For any other event or a non-crypto `id_usage`, the hook exits successfully without opening Strata. lgse/strata#1047
- `strata --unlock-volume` with a device path or LUKS UUID opens a window and shows the themed passphrase prompt for that volume. lgse/strata#1047
- If the volume has not appeared after 1 second, the window shows "Waiting for encrypted volume…" with Cancel. lgse/strata#1047 (unverified)
- If no matching volume appears within 8 seconds, the window shows "The encrypted volume was not found". lgse/strata#1047 (unverified)
- A matching volume that is not encrypted shows "This is not an encrypted volume". lgse/strata#1047 (unverified)
- An operand that neither starts with `/` nor parses as a LUKS UUID fails with "invalid --unlock-volume operand". lgse/strata#1047 (unverified)
- `--unlock-volume` combined with file arguments fails with "cannot combine --unlock-volume with file arguments". lgse/strata#1047 (unverified)

### Install and restore

- The installed udiskie `event_hook` is `strata --udiskie-hook {event} {id_usage} {device_file} {id_uuid}`. lgse/strata#1047
- Plugging in a locked LUKS volume after setup opens Strata's themed password prompt, not udiskie's dialog. lgse/strata#1047
- `strata --install-udiskie-unlock` rewrites `~/.config/udiskie/config.yml` with a managed header, a Strata `event_hook`, `password_prompt: false`, and a rule turning off LUKS automount. lgse/strata#1047
- Install records restore state under `~/.local/share/strata/udiskie-install/` and restarts udiskie. lgse/strata#1047
- When only `~/.config/udiskie/config.json` exists, install converts it to `config.yml` and removes it; uninstall writes it back as JSON. lgse/strata#1047 (unverified)
- When no udiskie process is running, install starts `udiskie --automount --no-notify --no-tray`; uninstall restarts udiskie only if it is running. lgse/strata#1047 (unverified)
- `strata --uninstall-udiskie-unlock` restores the previous udiskie configuration and removes the restore state. lgse/strata#1047
- If udiskie cannot be restarted, the command reports "Saved the udiskie configuration. Restart udiskie or log out for it to take effect." lgse/strata#1047 (unverified)
- Install refuses to edit a configuration whose `program_options` is not a mapping or whose `device_config` is not a sequence. lgse/strata#1047 (unverified)
- Install and uninstall refuse a `config.yml` that is a symlink or other non-regular file, reporting "Refusing to replace non-regular udiskie configuration". lgse/strata#1047 (unverified)
- Neither command installs or removes the `udiskie` package. lgse/strata#1047

### Settings and installer

- Settings → General → Desktop integration shows "Unlock encrypted volumes" only when Omarchy is detected and `udiskie` is on `PATH`. lgse/strata#1047
- The row's Use Strata button installs the integration and Restore default removes it. lgse/strata#1047
- Use Strata shows only while the integration is not configured; Restore default shows only while restore state or a Strata-managed config exists. lgse/strata#1047 (unverified)
- `install.sh` offers the step on Omarchy 3 or 4 with default No, and on generic Arch only when `udiskie` is on `PATH`. lgse/strata#1047
- On Omarchy without `udiskie` on `PATH`, `install.sh` warns and skips the step; `--with-udiskie-unlock` makes it abort instead. lgse/strata#1047 (unverified)
- `install.sh` skips the step when the release archive lacks the `udiskie/unlock` marker; with `--with-udiskie-unlock` it aborts. lgse/strata#1047 (unverified)
- `install.sh --non-interactive` leaves the step declined unless `--with-udiskie-unlock` is passed. lgse/strata#1047

## Design

The README section "Unlock encrypted volumes on Omarchy" documents setup and restore. [docs/preferences.md](https://github.com/lgse/strata/blob/aee71335dfecd059b9af23efeac2ed52c43e3b19/docs/preferences.md) records that the integration is not a Strata preference. [docs/packaging.md](https://github.com/lgse/strata/blob/aee71335dfecd059b9af23efeac2ed52c43e3b19/docs/packaging.md) forbids packages from running the install flag.

- On Omarchy, plugging in a LUKS drive raised another program's prompt, not Strata's (lgse/strata#537). Disabling the user's automounter was ruled out, so udiskie hands encrypted `device_added` events to Strata and stops automounting LUKS (lgse/strata#1047).
- The hook is classified before GTK starts and execs `--unlock-volume`, so non-crypto events never open a window (lgse/strata#1047).
- The integration edits udiskie's file, not Strata preferences. Install records the previous `event_hook` and `password_prompt` values and whether it added the LUKS rule, so restore reverts only those keys (lgse/strata#1047).
- Settings is gated to Omarchy; the CLI flags are unattended and not gated (lgse/strata#1047).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-17 | lgse/strata#1047 | feat | Let udiskie hand encrypted-drive events to Strata's passphrase prompt through an opt-in config rewrite. |

## Known gaps

None known.
