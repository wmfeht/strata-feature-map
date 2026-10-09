---
title: AUR packages
status: shipped
origin: {issue: lgse/strata#50, pr: lgse/strata#183}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [packaging/aur, scripts/update_aur.py, .github/workflows/packaging.yml, .github/workflows/publish-aur.yml]
tests: [scripts/test_update_aur.py]
related: [app/updates/package-managed, integration/file-manager-interface]
---

## Summary

The `strata-bin` and `strata-rc-bin` Arch packages, rendered from one `PKGBUILD.in` template and committed for publication to the AUR. Both repackage the prebuilt release archive as `/usr/bin/strata`. docs/packaging.md states they are not yet published. How a packaged install handles updates belongs to `app/updates/package-managed`.

## Behavior

### Packages

- `strata-bin` tracks the latest stable release; `strata-rc-bin` tracks the newest stable, alpha, beta, or RC release. lgse/strata#183
- Each package provides `strata=<pkgver>` and conflicts with `strata` and with the other package. lgse/strata#183
- Each architecture, x86_64 and aarch64, downloads its own release archive with its own pinned SHA-256. lgse/strata#183
- `package()` installs the archive's `strata` binary unstripped as `/usr/bin/strata`. lgse/strata#183
- Each package declares `license=('MIT' 'LicenseRef-UnRAR')`. lgse/strata#664, lgse/strata#832
- `LICENSE` and `THIRD_PARTY_LICENSES.md` install under `/usr/share/licenses/<pkgname>/`, plus `UnRAR.txt` when the archive has it. lgse/strata#183, lgse/strata#832
- The desktop entry installs to `/usr/share/applications` and the icon to `/usr/share/icons/hicolor/scalable/apps`. lgse/strata#183
- An archive without desktop metadata still packages, printing a warning and installing no launcher. lgse/strata#183
- When the archive ships `io.github.lgse.Strata.FileManager1.service`, it installs as an inactive template in `/usr/share/strata`, not a D-Bus services directory. lgse/strata#317
- `package()` writes `/usr/share/strata/install-source.toml` with the manager, package, channel (`stable` or `rc`), AUR helpers `yay`, `paru`, `pikaur`, `trizen`, and the alternate package. lgse/strata#183

### Dependencies

- `gvfs` is a required dependency, because the Devices sidebar relies on its volume monitor. lgse/strata#536
- `gstreamer>=1.20` and `gst-plugins-base` are required dependencies. lgse/strata#839
- `ffmpeg`, `ffmpegthumbnailer`, `gst-libav`, `gst-plugins-good`, `gvfs-smb`, `imagemagick`, and `libraw` are optional dependencies for previews, thumbnails, and SMB. lgse/strata#183
- `squashfs-tools` is an optional dependency for AppImage icon thumbnails. lgse/strata#1077
- `xdg-terminal-exec` is an optional dependency for Open in Terminal. lgse/strata#967

### Versions

- A prerelease `pkgver` drops only the hyphen and keeps the dots: `0.10.0-rc.1` becomes `0.10.0rc.1`. lgse/strata#183
- The download URL uses the real release tag, never the mangled `pkgver`. lgse/strata#183
- `update_aur.py --stable <version>` renders only `strata-bin` and refuses a prerelease version. lgse/strata#183
- `update_aur.py --preview <version>` renders only `strata-rc-bin`, accepting final, alpha, beta, or RC versions and refusing nightlies. lgse/strata#183
- `update_aur.py` refuses a release checksum file that names another release's or architecture's archive. lgse/strata#183
- `update_aur.py --check` writes nothing and fails when a committed `PKGBUILD` or `.SRCINFO` differs from a fresh render. lgse/strata#183

### Publication

- With `AUR_PUBLISH_ENABLED` set to `true`, each non-nightly release regenerates the packages and opens a review PR. lgse/strata#183, lgse/strata#247
- A release updates `strata-rc-bin` only when its `pkgver` is not older than the packaged one by `vercmp`. lgse/strata#183
- With publication enabled, merging a changed `PKGBUILD` or `.SRCINFO` to `main` pushes both packages to the AUR, skipping any already current. lgse/strata#183

## Design

[docs/packaging.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/packaging.md) carries the package layout, channel rules, and validation steps.

- Arch was the first distribution, packaged as `strata-bin` from release archives; a source-built `strata` package is left for later demand (lgse/strata#50). The `strata` name is therefore reserved through `conflicts`.
- Packages do not strip, so the installed binary stays byte-identical to the release artifact its attestation covers (docs/packaging.md).
- Nightlies are not packaged. `makepkg` fetches sources before `pkgver()` runs, so a package cannot discover the newest nightly; pinning each one would need an AUR push per nightly (docs/packaging.md).
- Rendered `PKGBUILD` and `.SRCINFO` files are committed because the AUR requires self-contained files. This repository is the source of truth, not the AUR checkout (docs/packaging.md).
- The marker exists because pacman owns `/usr/bin/strata`. Replacing it would mark the package modified, and the next upgrade would overwrite it silently (lgse/strata#50, docs/packaging.md).
- The marker names no update command: pacman cannot update an AUR package, and the right helper depends on what is installed (docs/packaging.md).
- The channel is a property of the package, not a preference; switching channels means installing the other package (docs/packaging.md).
- The marker is scoped to these two packages, not a cross-distribution API. Other formats need their own design for ownership, availability, and updates (lgse/strata#183, docs/packaging.md).
- `pkgver` keeps dots so `vercmp` compares prerelease parts as separate segments. Without them `0.8.0-nightly.20260901.2` would sort above the next day's nightly (docs/packaging.md).
- Packages must not install the FileManager1 service into a system directory. Several providers there are picked arbitrarily, and installing Strata must not change the preferred file manager (lgse/strata#317).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-04 | lgse/strata#183 | build | Added the `strata-bin` and `strata-rc-bin` packages from one template, with the install-source marker. |

## Known gaps

None known.
