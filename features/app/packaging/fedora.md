---
title: Fedora COPR package
status: shipped
origin: {issue: lgse/strata#2118, pr: lgse/strata#2120}
branch: null
reviewed_at: 5f17c9fdc8967e1b4ba8aaf8de113b46d824b0dd
review: draft
code: [packaging/rpm, scripts/build_srpm.py]
tests: [scripts/test_build_srpm.py]
related: [app/packaging/aur, app/updates, operations/archives/rar, settings/diagnostics, integration/file-manager-interface]
---

## Summary

The Fedora RPM, built from source for stable and preview COPR projects so Fedora users can install and update Strata with dnf. `packaging/rpm/strata.spec.in` is the template; `scripts/build_srpm.py` turns a release tag into a source RPM. How a build without the updater behaves belongs to `app/updates`.

## Behavior

### Install

- The README's Fedora section installs stable releases on x86_64 or aarch64 with `sudo dnf copr enable @lgse/strata`, then `sudo dnf install strata`. lgse/strata#2120
- For alpha, beta, and RC builds, the README says to enable `@lgse/strata-preview` instead, and never both projects. lgse/strata#2120
- The README says a COPR install updates with ordinary system updates; the package has no in-app updater. lgse/strata#2120

### Build

- The spec compiles with `STRATA_UPDATER=disabled`. lgse/strata#2120
- The package installs no `share/strata/install-source.toml` and no file under `/usr/share/dbus-1`. lgse/strata#2120
- The FileManager1 service ships only as the inactive template `/usr/share/strata/io.github.lgse.Strata.FileManager1.service`. lgse/strata#2120
- The spec builds with `--no-default-features`, which leaves out the `rar` feature. lgse/strata#2120
- When `unrar` or `unrar_sys` is vendored with sources, `build_srpm.py` fails with "vendored sources include non-free crates". lgse/strata#2120
- `rpm -q --provides strata` lists a `bundled(crate(…))` entry per vendored crate, and none for a stubbed crate such as `unrar`. lgse/strata#2120
- `STRATA_RELEASE_TAG` and `STRATA_BUILD_KIND` come from `--tag`, and `STRATA_BUILD_COMMIT` from the packaged commit, so `strata --version` and Diagnostics name the release as a release-archive build does. lgse/strata#2120
- The build leaves `STRATA_INTEGRATIONS` unset, so the runtime integration installers stay enabled. lgse/strata#2120
- A vendoring step that changes `Cargo.lock` fails with "Cargo.lock is out of date with Cargo.toml in the packaged source". lgse/strata#2120 (unverified)
- The `License` tag joins the crates' `cargo2rpm` license summary with Apache-2.0, ISC, MIT, and OFL-1.1, deduplicated and joined with ` AND `. lgse/strata#2120 (unverified)
- `%check` runs `desktop-file-validate` on the entry and `strata --version`. lgse/strata#2120 (unverified)

### Dependencies

- The package requires `bubblewrap`, `gvfs`, `hicolor-icon-theme`, and `xdg-utils`. lgse/strata#2120 (unverified)
- It recommends `/usr/bin/ffmpeg`, `dcraw`, `ffmpegthumbnailer`, `gstreamer1-plugin-libav`, `gstreamer1-plugins-good`, `gvfs-smb`, `ImageMagick`, `LibRaw-samples`, `squashfs-tools`, and `xdg-terminal-exec`. lgse/strata#2120 (unverified)
- Codec previews use the installed FFmpeg: Fedora's `ffmpeg-free`, or `ffmpeg` from RPM Fusion. lgse/strata#2120
- The spec sets `ExclusiveArch: x86_64 aarch64`. lgse/strata#2120
- `LICENSE`, `THIRD_PARTY_LICENSES.md`, `LICENSE.dependencies`, `cargo-vendor.txt`, and the five `data/licenses/*` asset licenses install as license files. lgse/strata#2120 (unverified)

### Versions

- A prerelease tag maps to a `~` version: `1.3.0-rc.1` becomes `1.3.0~rc.1`; `v1.2.1` becomes `1.2.1`. lgse/strata#2120
- `build_srpm.py` refuses a nightly with "nightly releases are not packaged", and a malformed tag such as `1.3` or `1.3.0-rc1`. lgse/strata#2120
- A tag whose `build.rs` and `crates/*/build.rs` never name `STRATA_UPDATER` fails with "<tag> predates STRATA_UPDATER and cannot be packaged as an RPM". lgse/strata#2120
- `v1.2.0-rc.1` is the oldest tag that packages; `v1.1.1` is refused. lgse/strata#2120
- `--ref` packages any commit under a tag's identity; `--release 0` is a usage error. lgse/strata#2120 (unverified)

### Publication

- Publishing runs only when the repository variable `COPR_PUBLISH_ENABLED` is exactly `true`. lgse/strata#2120
- A stable version goes to both `COPR_PROJECT` and `COPR_PREVIEW_PROJECT`; an alpha, beta, or RC goes only to the preview project. lgse/strata#2120
- A nightly goes to no project, and an empty `COPR_PREVIEW_PROJECT` publishes stable releases only. lgse/strata#2120
- The Release workflow publishes after each non-nightly release; a manual run takes `version` and `release` to retry, rebuild, or backfill. lgse/strata#2120
- The publish job fails when COPR reports no created builds, and otherwise waits for every build. lgse/strata#2120 (unverified)
- The packaging tools come from the workflow's own revision; only the source archive comes from the tag. lgse/strata#2120

## Design

[docs/packaging.md](https://github.com/lgse/strata/blob/5f17c9fdc8967e1b4ba8aaf8de113b46d824b0dd/docs/packaging.md) ("Fedora COPR") carries the package layout, build changes, channels, and publishing setup.

- Repackaging the release archive like `strata-bin` was rejected: its updater would try to replace the dnf-owned `/usr/bin/strata` (lgse/strata#2118).
- Packit was rejected because it needs a GitHub App and moves release automation to an outside service (lgse/strata#2118).
- COPR's tag webhook was rejected: it expects `PKGNAME-VERSION` tags and gives no control over vendoring or the RAR-free build (lgse/strata#2118).
- Attaching `.rpm` files to releases was rejected: an RPM is built per Fedora release, and without the updater it would never update (lgse/strata#2118).
- COPR builders have no network access, so the source RPM carries the vendored crates and builds offline (lgse/strata#2118, lgse/strata#2120).
- UnRAR's license is not on Fedora's allowed list, and COPR rejects such material even as unused sources in a source RPM (lgse/strata#2118, docs/packaging.md).
- The updater is compiled out, so the package installs no install-source marker. To the updater code, that marker means an AUR install (lgse/strata#2118, docs/packaging.md).
- Unlike the AUR packages, nothing rendered is committed. The source RPM is built from the tagged commit, so only the template and script are reviewed (docs/packaging.md).
- `~` versions make RPM sort a prerelease before its final release (lgse/strata#2118, docs/packaging.md).
- A stable release also goes to the preview project, so that channel never lags behind the latest stable (docs/packaging.md).
- `rpm.yml` builds the RPM on every dependency change, because an update can bring in a license COPR rejects (lgse/strata#2120).
- Helpers Strata executes, such as `bwrap`, are `Requires`: they are run rather than linked, so no automatic dependency covers them (lgse/strata#2120).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |

## Known gaps

- The COPR projects `@lgse/strata` and `@lgse/strata-preview` return 404, so the README's install commands fail. lgse/strata#2120
- Publishing waits on Fedora creating the `lgse` FAS group, and stays off until `COPR_PUBLISH_ENABLED` is `true`. lgse/strata#2120
- Sandboxed previews are untested on real aarch64 hardware; the QEMU test lacked Landlock and user namespaces. lgse/strata#2120
