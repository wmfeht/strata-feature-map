---
title: Packaging and installation
status: shipped
origin: {issue: lgse/strata#49, pr: lgse/strata#182}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: reviewed
code: [data/io.github.lgse.Strata.desktop, data/icons/scalable/apps/io.github.lgse.Strata.svg]
tests: [src/tests.rs]
docs: [docs/packaging.md]
related: [app/updates/install, app/updates/package-managed, app/window]
---

## Summary

How Strata reaches a desktop: the desktop entry and application icon that let shells recognize it, and `strata --version` for checking an install. Children: `app/packaging/installer` (the `install.sh` release installer) and `app/packaging/aur` (the `strata-bin` and `strata-rc-bin` AUR packages).

## Behavior

### Desktop entry and icon

- `io.github.lgse.Strata.desktop` sets `Icon=io.github.lgse.Strata` and `StartupWMClass=io.github.lgse.Strata`, matching the GTK application ID. lgse/strata#182
- The entry declares `MimeType=inode/directory;` and `Categories=Utility;FileTools;FileManager;`, so it can be the default folder handler. lgse/strata#182
- The entry carries translated `GenericName`, `Comment`, and `Keywords` for fr, de, es, ja, pt_BR, ko, vi, it, and ru. lgse/strata#1519 (unverified)
- The application icon is bundled in the GResource and set as GTK's default window icon name. lgse/strata#182
- Release archives contain `io.github.lgse.Strata.desktop` and `io.github.lgse.Strata.svg` beside the `strata` binary. lgse/strata#182
- By default, `mise run install-local` installs the binary to `~/.local/bin`, the icon under `~/.local/share/icons/hicolor`, and the entry under `~/.local/share/applications`. lgse/strata#182, lgse/strata#663
- The entry ships with `Exec=strata %U`; `mise run install-local` rewrites it to the installed binary's absolute path. lgse/strata#182, lgse/strata#663
- `mise run uninstall-local` removes the binary, entry, and icon. lgse/strata#182, lgse/strata#663

### Version

- `strata --version` prints one line, `strata <version>`, and exits successfully without opening a window. lgse/strata#918
- The printed version is the release-tag identity Settings → Updates uses, including a prerelease suffix such as `-rc.1`. lgse/strata#918
- `strata --version ~/Documents` prints the version; `strata ~/Documents --version` launches the application. lgse/strata#918

## Design

[docs/packaging.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/packaging.md) carries the packaging layout and the rules for desktop metadata.

- Linux has no portable icon-on-a-process property. Shells match the window's application ID to a `.desktop` file and use its `Icon`, so the entry's file name is the application ID (lgse/strata#49).
- The icon is the Lucide `layers` glyph on a backdrop original to Strata. It keeps fixed colors because shells render application icons outside Strata's theming (lgse/strata#182).
- Desktop metadata ships inside the release archive, so the installer, packages, and updater always install the copy that matches the binary (lgse/strata#182, docs/packaging.md).
- `--version` prints `build_info::installed_version()` rather than `CARGO_PKG_VERSION`, which would drop the prerelease identity carried in `STRATA_RELEASE_TAG` (lgse/strata#917).
- `--version` joins the existing first-argument launch-mode dispatch; a full `--help` parser was rejected as more than needed (lgse/strata#917).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-13 | lgse/strata#918 | feat | Added `--version` so scripts and packaging checks can read the installed version without the GUI. |
| 2026-09-03 | lgse/strata#182 | feat | Added the application icon and a desktop entry named after the application ID, and shipped both in release archives. |

## Known gaps

- No official package exists for distributions other than Arch; an official Flatpak is proposed. lgse/strata#936
