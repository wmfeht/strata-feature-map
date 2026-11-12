---
title: Packaging and installation
status: shipped
origin: {issue: lgse/strata#49, pr: lgse/strata#182}
branch: null
reviewed_at: 5f17c9fdc8967e1b4ba8aaf8de113b46d824b0dd
review: draft
code: [data/io.github.lgse.Strata.desktop, data/icons/scalable/apps/io.github.lgse.Strata.svg, flake.nix, flake.lock, package.nix, nix/install-source.toml]
tests: []
docs: [site/src/reference/install.md, docs/packaging.md]
related: [app/updates/install, app/updates/package-managed, app/window, operations/trash]
---

## Summary

How Strata reaches a desktop: the desktop entry and application icon that let shells recognize it, and `strata --version` for checking an install. It also owns the Nix flake that builds Strata from source. Children: `app/packaging/installer` (the `install.sh` release installer), `app/packaging/aur` (the `strata-bin` and `strata-rc-bin` AUR packages), and `app/packaging/fedora` (the Fedora COPR package).

## Behavior

### Desktop entry and icon

- `io.github.lgse.Strata.desktop` sets `Icon=io.github.lgse.Strata` and `StartupWMClass=io.github.lgse.Strata`, matching the GTK application ID. lgse/strata#182
- The entry declares `MimeType=inode/directory;x-scheme-handler/trash;` and `Categories=Utility;FileTools;FileManager;`, so it can be the default folder handler and a `trash:///` handler. lgse/strata#182, lgse/strata#2065
- After `mise run install-local`, `gio mime x-scheme-handler/trash` lists Strata under Registered and Recommended applications. lgse/strata#2065
- When `mimeapps.list` sets another handler as the `x-scheme-handler/trash` default, that handler stays the default and Strata stays a candidate. lgse/strata#2065
- The entry carries translated `GenericName`, `Comment`, and `Keywords` for fr, hu, de, es, ja, pt_BR, ko, vi, it, ru, zh_CN, and zh_TW. lgse/strata#1519, lgse/strata#1583, lgse/strata#1745, lgse/strata#1918 (unverified)
- The application icon is bundled in the GResource and set as GTK's default window icon name. lgse/strata#182
- The application icon draws the logo in blue and violet gradients on a rounded tile. The tile fades from `#414868` at the top to `#1b1c27` at the bottom. lgse/strata#1838 (unverified)
- Release archives contain `io.github.lgse.Strata.desktop` and `io.github.lgse.Strata.svg` beside the `strata` binary. lgse/strata#182
- By default, `mise run install-local` installs the binary to `~/.local/bin`, the icon under `~/.local/share/icons/hicolor`, and the entry under `~/.local/share/applications`. lgse/strata#182, lgse/strata#663
- The entry ships with `Exec=strata %U`; `mise run install-local` rewrites it to the installed binary's absolute path. lgse/strata#182, lgse/strata#663
- `mise run uninstall-local` removes the binary, entry, and icon. lgse/strata#182, lgse/strata#663

### Version

- `strata --version` prints one line, `strata <version>`, and exits successfully without opening a window. lgse/strata#918
- The printed version is the release-tag identity Settings → Updates uses, including a prerelease suffix such as `-rc.1`, before any `+debug` suffix. lgse/strata#918, lgse/strata#1676
- A debug build, such as one from `cargo build` or `mise run dev`, prints `strata <version>+debug`; a release build prints no suffix. lgse/strata#1676
- `strata --version ~/Documents` prints the version; `strata ~/Documents --version` launches the application. lgse/strata#918

### Nix

- `nix run github:lgse/strata` builds Strata from source and runs it; `nix profile add github:lgse/strata` installs it. lgse/strata#1967
- The flake exposes `packages.<system>.strata` and `packages.<system>.default` for `x86_64-linux` and `aarch64-linux`. lgse/strata#1967
- The Nix package compiles with `STRATA_UPDATER=disabled`, so it has no Updates page; updating the flake input and rebuilding upgrades it. lgse/strata#1967
- The Nix package omits UnRAR by default. `pkgs.callPackage "${inputs.strata}/package.nix" { rarSupport = true; }` enables it and adds the `unfreeRedistributable` license. lgse/strata#1967
- The package installs `share/applications/io.github.lgse.Strata.desktop` with `Exec=` set to its own `bin/strata`, and the icon under `share/icons/hicolor/scalable/apps`. lgse/strata#1967
- `LICENSE` and `THIRD_PARTY_LICENSES.md` install under `share/licenses/strata/`. lgse/strata#1967
- The package installs `share/strata/install-source.toml` with `manager = "Nix"` and `package = "strata"`, so Diagnostics reports "Installed by Nix as strata." lgse/strata#1967
- A flake build from a git reference shows the flake's short revision as the Diagnostics build commit; a `path:` build shows `unknown`. lgse/strata#1967
- A flake build from a dirty tree shows the revision with a `-dirty` suffix. lgse/strata#1967 (unverified)
- Bubblewrap and the preview helpers come from the package closure, so image and video previews work without system copies. lgse/strata#1967
- A terminal or Open With program launched from the Nix build keeps the user's `PATH`; the wrapper adds no helper directories to it. lgse/strata#1967
- The Nix package builds with `STRATA_INTEGRATIONS=package`, so the file chooser portal, FileManager1 service, and udiskie hook come from the Nix configuration. lgse/strata#1975
- `strata.fileChooserPortal` holds `strata.portal` and the portal's D-Bus service file; `strata.fileManagerService` holds the FileManager1 service file. lgse/strata#1975
- Each of those service files has `Exec` set to the package's `bin/strata` wrapper, not `bin/.strata-wrapped`. lgse/strata#1975
- The package's own `share/strata/io.github.lgse.Strata.FileManager1.service` is an inactive template whose `Exec` names the package's `bin/strata`. lgse/strata#1967
- `nix flake check` builds the package and both service-file derivations; the Rust test suite does not run in the Nix build. lgse/strata#1967, lgse/strata#1975

## Design

[docs/packaging.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/packaging.md) carries the packaging layout and the rules for desktop metadata.

- Linux has no portable icon-on-a-process property. Shells match the window's application ID to a `.desktop` file and use its `Icon`, so the entry's file name is the application ID (lgse/strata#49).
- The icon keeps fixed colors because shells render application icons outside Strata's theming (lgse/strata#182).
- The earlier white logo nearly vanished on light docks (lgse/strata#1832). lgse/strata#1832 proposed light and dark variants, theme-aware selection, or one SVG that contrasts on both; lgse/strata#1838 shipped one SVG.
- The tile is a gradient with a faint light edge because a flat `#1b1c27` tile blended into dark docks (lgse/strata#1838).
- Linux desktops draw the hicolor SVG unmasked, so the icon rounds its own corners. Icon themes such as MacTahoe reshape only the apps they ship icons for (lgse/strata#1838).
- The tile spans 228 of 284 units per side (about 80%), with a 51-unit corner radius (about 22% of the tile side). These are the usual macOS and Adwaita proportions, so the icon matches neighboring icons in size (lgse/strata#1838).
- The entry declares `x-scheme-handler/trash` because `Exec=strata %U` already opened `trash:///`, but choosers never offered Strata for it. The declaration makes Strata eligible; `mimeapps.list` still picks the default (lgse/strata#2052, lgse/strata#2065).
- Desktop metadata ships inside the release archive, so the installer, packages, and updater always install the copy that matches the binary (lgse/strata#182, docs/packaging.md).
- `--version` prints `build_info::displayed_version()`, built on `installed_version()` rather than `CARGO_PKG_VERSION`, which would drop the prerelease identity carried in `STRATA_RELEASE_TAG` (lgse/strata#917, lgse/strata#1676).
- Debug builds scroll and load noticeably slower, so they carry `+debug` to tell them apart in reports. The suffix is display-only; update checks keep the plain version (lgse/strata#1671, lgse/strata#1676, unverified).
- `--version` joins the existing first-argument launch-mode dispatch; a full `--help` parser was rejected as more than needed (lgse/strata#917).
- The Nix flake lives in the Strata repository, not a personal fork, so other Nix users can install it (lgse/strata#1956, lgse/strata#1967).
- Unlike the AUR packages, the Nix package compiles from source. Its sandbox and trusted helper paths are embedded at build time, pointing into the package closure (lgse/strata#1967, docs/packaging.md).
- The wrapper once prefixed `PATH` with the helper closure. Strata's own lookups already use the embedded paths, so the prefix only leaked pinned tools to launched programs; it was dropped (lgse/strata#1967).
- On Nix the runtime integration installers recorded `bin/.strata-wrapped` of one store path. That skipped the wrapper's environment and went stale on update or garbage collection, so the package ships the files (lgse/strata#1969, lgse/strata#1975).
- The portal and FileManager1 service files are derivations separate from the package. NixOS registers every system package's `share/dbus-1/services`, so shipping them in it would make every install claim FileManager1 (lgse/strata#1975, docs/packaging.md).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-11-05 | lgse/strata#2065 | feat | Declared the `trash` URI scheme handler so `xdg-mime` tools and choosers offer Strata for `trash:///`. |
| 2026-10-24 | lgse/strata#1838 | feat | Put the colored logo on a dark rounded gradient tile so the icon reads on light and dark docks. |
| 2026-09-13 | lgse/strata#918 | feat | Added `--version` so scripts and packaging checks can read the installed version without the GUI. |
| 2026-09-03 | lgse/strata#182 | feat | Added the application icon and a desktop entry named after the application ID, and shipped both in release archives. |

## Known gaps

- No official package exists for distributions other than Arch, Nix, and Fedora. lgse/strata#2120
- The Nix package is built and tested on `x86_64-linux` only; `aarch64-linux` builds are untested. lgse/strata#1967
- On a system with no `x-scheme-handler/trash` default, installing Strata can take over `trash:///` from another file manager through GIO's first-handler fallback. lgse/strata#2065
