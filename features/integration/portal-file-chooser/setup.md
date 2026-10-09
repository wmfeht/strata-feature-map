---
title: File chooser and file manager setup
status: shipped
origin: {issue: lgse/strata#120, pr: lgse/strata#175}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [src/portal_setup.rs, src/portal_setup/omarchy.rs, src/ui/portal_preferences.rs, src/ui/desktop_integration.rs, data/portal]
tests: [src/portal_setup/tests.rs, src/portal_setup/omarchy/tests.rs, src/ui/portal_preferences/tests.rs]
related: [integration/file-manager-interface, settings/preferences, app/updates]
---

## Summary

Making Strata the per-user FileChooser portal backend and default file manager, and restoring the previous setup. It runs from the `--install-portal` and `--uninstall-portal` commands, the installer, and the Settings → General "System file manager" row, which also sets Omarchy shortcuts.

## Behavior

### Portal installation

- `strata --install-portal` writes `strata.portal` under `$XDG_DATA_HOME/xdg-desktop-portal/portals` and a D-Bus service under `$XDG_DATA_HOME/dbus-1/services` running `<resolved path> --portal`. lgse/strata#175
- Installation puts `strata;` first in the `org.freedesktop.impl.portal.FileChooser` preference and keeps the backends already listed as fallbacks. lgse/strata#175
- With no user portal configuration, installation copies the active desktop configuration into `$XDG_CONFIG_HOME/xdg-desktop-portal` before editing it. lgse/strata#175
- Installation records what it changed in `$XDG_DATA_HOME/strata/portal-install/state.toml`. lgse/strata#175
- After installing or removing, Strata stops its backend unit, reloads D-Bus, and restarts `xdg-desktop-portal.service`. lgse/strata#175
- When a stop, reload, or restart step fails, `--install-portal` and `--uninstall-portal` print "Could not reload every portal service. Ensure xdg-desktop-portal is installed, then log out and back in before testing." lgse/strata#175 (unverified)
- An executable path containing whitespace, quotes, or backslashes is refused as unsupported by D-Bus activation. lgse/strata#175
- An executable path with a component not owned by the user or root, or writable by other users, is refused. lgse/strata#175
- `strata --uninstall-portal` restores the original configuration, or deletes the copy it created, when the file is unchanged since installation; otherwise it removes only `strata` from the preference. lgse/strata#175
- `strata --dismiss-portal-prompt` creates `$XDG_CONFIG_HOME/strata/portal-opt-in-v1` and leaves portal preferences unchanged. lgse/strata#175
- The installer asks about the file chooser with default No; `--with-file-chooser` runs `--install-portal`, and a decline or `--without-file-chooser` runs `--dismiss-portal-prompt`. lgse/strata#175

### Settings row

- Settings → General → "System file manager" lists Open and Save dialogs, Opening folders, and Reveal in File Manager, each marked configured or not. lgse/strata#947
- On Omarchy the row also lists Keyboard shortcuts; elsewhere that line is hidden. lgse/strata#947 (unverified)
- Complete setup installs the portal, sets `io.github.lgse.Strata.desktop` as the `inode/directory` handler, and installs the per-user FileManager1 service. lgse/strata#947
- On Omarchy 3 or 4, Complete setup also binds Super+Shift+F and Super+Alt+Shift+F to Strata in `$XDG_CONFIG_HOME/hypr/bindings.conf`, or `bindings.lua` on Omarchy 4. lgse/strata#947 (unverified)
- When `hyprctl configerrors` reports errors after the shortcut edit, Complete setup restores the previous bindings file and keeps a `strata-keybind-backup-` copy. lgse/strata#947 (unverified)
- Complete setup is hidden once every line is configured, and Restore default appears while any part is installed. lgse/strata#947 (unverified)
- Complete setup fails with "Another per-user FileManager1 provider is already installed" when another user service owns that name. lgse/strata#947 (unverified)
- Restore default removes the FileManager1 service and portal, and returns `inode/directory` to the recorded handler, or Nautilus when none was recorded. lgse/strata#947
- Restore default leaves `inode/directory` unchanged when it no longer points to Strata. lgse/strata#947 (unverified)
- With no recorded handler and no Nautilus, Restore default fails with "No previous folder handler was recorded and Nautilus was not detected." lgse/strata#947 (unverified)
- On Omarchy, Restore default replaces the Strata shortcut block with `nautilus --new-window` bindings. lgse/strata#947 (unverified)
- When Nautilus is not detected, Restore default keeps the Strata shortcuts and reports "Nautilus was not detected; the Strata keyboard shortcuts were left unchanged." lgse/strata#947 (unverified)
- When the Strata shortcut block was edited by hand, Restore default fails and leaves it unchanged. lgse/strata#947 (unverified)

### Updates

- After an in-app update, Strata restarts portal services only when Strata is the configured FileChooser. lgse/strata#475
- On launch, a running `strata --portal` started from the same install path but from a replaced executable makes Strata restart portal services. lgse/strata#475

## Design

- Replacement is opt-in and reversible. Setup keeps the previous backends listed after `strata` and records enough state to undo only its own edits (lgse/strata#175).
- The D-Bus service runs whatever path it names, so the executable path must be trusted and must parse without shell quoting (lgse/strata#175).
- Portal selection happens before a request reaches Strata. The fallback backends cover a missing Strata install, not a crash mid-request (lgse/strata#175).
- Open and Save dialogs, folder opening, and Reveal are separate XDG mechanisms. Users enabling the chooser expected Reveal to follow (lgse/strata#632).
- lgse/strata#632 proposed independent controls. The owner chose one combined opt-in instead, so one row sets all three (lgse/strata#947).
- The first-launch offer and the Configure… dialog were replaced by the inline status list in lgse/strata#947. No launch path reads the `portal-opt-in-v1` marker since then.
- A stale backend is detected by comparing the running process's executable inode with the installed file. A backend from another Strata installation is left alone (lgse/strata#474).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-14 | lgse/strata#947 | feat | Made System file manager also set the folder handler, FileManager1 service, and Omarchy shortcuts. |

## Known gaps

- docs/portal-file-chooser.md still describes a first-launch offer and a Settings "System file chooser → Configure…" dialog, both removed. lgse/strata#947
