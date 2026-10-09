---
title: FileManager1 D-Bus interface
status: shipped
origin: {issue: lgse/strata#290, pr: lgse/strata#317}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [src/adapters/file_manager1.rs, data/io.github.lgse.Strata.FileManager1.service]
tests: [src/adapters/file_manager1/tests.rs, tests/e2e/scenarios/test_file_manager_interface.py]
docs: [docs/packaging.md]
related: [integration/portal-file-chooser/setup, browser/navigation, browser/properties]
---

## Summary

Strata's implementation of `org.freedesktop.FileManager1`, which browsers and GTK/GNOME apps call for "Open file location" and "Show in Folder". It answers `ShowFolders`, `ShowItems`, and `ShowItemProperties`, and ships a per-user D-Bus activation service. The Settings row that installs that service is `integration/portal-file-chooser/setup`.

## Behavior

### Methods

- On startup Strata exports `org.freedesktop.FileManager1` at `/org/freedesktop/FileManager1` on its session bus and requests that bus name. lgse/strata#317
- `ShowFolders` with a directory URI opens a new Strata window on that directory with nothing selected. lgse/strata#317
- `ShowItems` with a file URI opens a new window on the file's parent directory with the file selected and focused. lgse/strata#317, lgse/strata#1499
- `ShowItems` URIs that share a directory are selected together in one window; each other directory opens another window, in the order listed. lgse/strata#317
- `ShowItemProperties` opens the parent directory with the item selected and the Properties dialog showing that item. lgse/strata#317, lgse/strata#1499
- With several items in one directory, `ShowItemProperties` shows Properties for the first URI listed. lgse/strata#1499 (unverified)
- `ShowItems` on `file:///` opens `/` with nothing selected. lgse/strata#317 (unverified)
- `ShowItems` on a dotfile while Hidden files is off turns Hidden files on and selects the file. lgse/strata#932
- `ShowItems` on one of two files whose non-UTF-8 names display identically selects only the requested file. lgse/strata#1499
- `ShowItems` on a remote URI such as `sftp://host/dir/file` opens the parent as a remote location and selects the file once it is mounted; a failed or cancelled mount drops the reveal. lgse/strata#1499
- The `StartupId` argument is ignored. lgse/strata#317 (unverified)
- A call whose arguments are not `(as, s)` fails with `org.freedesktop.DBus.Error.InvalidArgs`. lgse/strata#317 (unverified)

### Activation and installation

- With `io.github.lgse.Strata.FileManager1.service` in `~/.local/share/dbus-1/services`, a `ShowItems` call while Strata is not running starts `strata --gapplication-service` and opens the reveal window. lgse/strata#317
- When another file manager already owns `org.freedesktop.FileManager1`, Strata does not take the name and calls keep reaching that owner. lgse/strata#317 (unverified)
- The interactive installer asks about "Open file location" separately from the folder association. lgse/strata#317
- `install.sh --with-file-manager` installs the service unattended with `Exec=` pointing at the installed binary; `--with-folder-association` implies it. lgse/strata#317
- The installer and `mise run install-file-manager` refuse to install when another per-user service in that directory names `org.freedesktop.FileManager1`. lgse/strata#317, lgse/strata#663
- `mise run uninstall-file-manager` removes the per-user service. lgse/strata#663
- AUR packages install the service only as an inactive template, `/usr/share/strata/io.github.lgse.Strata.FileManager1.service`. lgse/strata#317

## Design

[docs/packaging.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/packaging.md) carries the packaging rule for the service file.

- Browsers such as Firefox and Zen, and GTK/GNOME apps, call `org.freedesktop.FileManager1` directly instead of `xdg-open` and `mimeapps.list`. Without it, Nautilus or Dolphin opened even when Strata owned `inode/directory` (lgse/strata#290).
- Activation is an explicit per-user choice. Packages must not install the service into a system directory: several providers of one name in one directory are chosen arbitrarily, and installing Strata must not change the preferred file manager (lgse/strata#317).
- A per-user service takes precedence over the system providers other file managers ship, so the per-user conflict check is the only one needed (lgse/strata#317).
- A call is grouped into one request per directory, so items from one folder share one window and its selection (lgse/strata#317).
- Targets are identified by location, not display name. Each target is rebuilt as `parent.child(name)`, as listings build entries, so URI spellings compare equal. Matching lossy names had selected both of two colliding non-UTF-8 files (lgse/strata#1428, lgse/strata#1499).
- D-Bus reveals share one entry point, `reveal_locations`, with `strata <file>`, Open file location, Ctrl+K Enter, and typed paths (lgse/strata#1499). The hidden-file toggle lives in that shared selection path (lgse/strata#932).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-14 | lgse/strata#932 | fix | Turned on Hidden files when `ShowItems` names a hidden file, so it is shown and selected. |
| 2026-09-05 | lgse/strata#317 | feat | Implemented FileManager1 so "Open file location" in other apps opens Strata instead of Nautilus or Dolphin. |

## Known gaps

- FileManager1 integration is not validated under Flatpak's permission and D-Bus activation model; the third-party FlatPark package does not expose it. lgse/strata#936, lgse/strata#1503
