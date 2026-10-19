---
title: Shared location model and listing adapter
status: shipped
origin: {issue: lgse/strata#14, pr: lgse/strata#27}
branch: null
reviewed_at: e0f73973926ff67e77c2c56cf288b7b7617bb2e5
review: draft
code: [src/model/mod.rs, src/adapters/local_files.rs, src/ui/mod.rs, src/main.rs, src/app/mod.rs, src/adapters/mod.rs, src/services/mod.rs, src/ui/resize_feedback.rs, src/ui/preferences/trashed.rs, src/adapters/volume/mounts.rs, src/adapters/volume/mount_snapshot.rs, README.md, docs/assets/strata-themes.png, THIRD_PARTY_LICENSES.md, data/licenses, data/strata.gresource.xml, AGENTS.md, typos.toml, clippy.toml, scripts/e2e-native.sh, Cargo.toml, Cargo.lock, mise.toml, mise.lock, scripts/benchmark-scroll.py, src/build_info.rs, src/services/native_fs.rs, src/ui/keys/bindings.rs, src/ui/keys/bindings/**, build.rs, deny.toml, .github/workflows/ci.yml, .github/workflows/e2e.yml, .github/workflows/e2e-cache.yml, .github/workflows/integrations.yml, .github/ISSUE_TEMPLATE/bug_report.yml, scripts/quality.sh, scripts/quality_ci.py, scripts/test-headless.py, scripts/integration_tests.py, src/ui/settings/install_command.rs]
tests: [src/model/tests.rs, src/adapters/local_files/tests.rs, src/adapters/local_files/tests/browse.rs, src/adapters/volume/mounts/tests.rs, src/test_support.rs, src/test_support/**, tests/e2e/harness/**, tests/e2e/baselines/**, tests/e2e/conftest.py, tests/e2e/unit/test_keyboard_layout.py, tests/e2e/unit/test_harness.py, scripts/test_benchmark_scroll.py, src/build_info/tests.rs, scripts/test_quality_ci.py, scripts/test_quality_runner.py, scripts/test_headless_runner.py, scripts/test_e2e_runner.py, scripts/test_integration_tests.py, src/app/browser/tests/operations.rs, src/ui/settings/install_command/tests.rs]
docs: [docs/performance-baseline.md, docs/hardened-configuration.md, docs/unsafe-code.md]
related: [remote/file-providers/network-locations, operations/trash, browser/navigation/location-bar, browser/directory-monitoring, preview/preview-panel]
---

## Summary

The location model, URI display and diagnostic rules, and the directory-listing adapter that every feature shares, plus the crate and module roots. It also owns shared helpers, test support, catalogs, the README, third-party notices, crate manifests, the build script, CI workflows and tooling, the bug report template, and lint, dependency-audit, and agent configuration. It is the `fallback` node in `scopes.yaml`.

## Behavior

### URI display

- The location field and Properties show a URI location decoded only when its whole path is valid UTF-8 and has no `%2F`. lgse/strata#1424, lgse/strata#1533
- Otherwise the whole path shows percent-encoded, such as `sftp://host/share/%FF%20name`. lgse/strata#1424, lgse/strata#1533

### Listing

- A URI listing, such as Trash or an SMB share, skips an entry whose URI cannot be converted to a location. lgse/strata#1424, lgse/strata#1533 (unverified)
- Each skipped entry logs a warning with only the request id and backend name; the folder and entry name appear only at DEBUG. lgse/strata#1424, lgse/strata#1533

### Folder monitoring

- Copying a file into an open local folder shows no `#<inode>` entry while it is written; the file appears once, under its final name. lgse/strata#1615
- A file linked into a watched folder is queried once, not again at the change-done hint that arrives two seconds later. lgse/strata#1615

### Media metadata

- In Icons, a file named `clip.mp4` or `photo.png` whose first 8 KiB are text starts no sandboxed metadata probe. lgse/strata#1638
- In Icons, an SVG holding XML text still shows its width×height in its caption. lgse/strata#1638 (unverified)

### Log privacy

- At the default log level, a directory load logs its request id and backend name, never the browsed path or URI. lgse/strata#27
- With `RUST_LOG=strata=debug`, a directory load also logs its location, including the full native path. lgse/strata#27
- Logged URI locations omit user info, authentication parameters, query, and fragment at every log level. lgse/strata#27

## Design

[docs/performance-baseline.md](https://github.com/lgse/strata/blob/aee71335dfecd059b9af23efeac2ed52c43e3b19/docs/performance-baseline.md) states the log privacy levels: default logs carry request ids, backend names, counts, and timings only.

- Desktop logs and journals can retain usernames, project names, and mounted locations, so browsed locations need an explicit diagnostic opt-in (lgse/strata#14, lgse/strata#27).
- `Location` display and diagnostic paths once parsed strictly and showed `<invalid-uri>` for non-UTF-8 names in the path bar and Properties. They now share the GIO conversion's parse flags (lgse/strata#1424, lgse/strata#1533).
- Display tries the decoded form first, so valid names such as `smb://host/café` still display decoded (lgse/strata#1533).
- Display decodes only valid UTF-8 without `%2F`: decoding `%2F` would turn a name into a separator once the shown text is edited. Plain `UriFlags::ENCODED` was rejected because it stops userinfo decoding (lgse/strata#1424, lgse/strata#1533).
- The directory loader dropped unconvertible entries without a trace. Logging each skip keeps a future conversion failure visible (lgse/strata#1424, lgse/strata#1533).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-17 | lgse/strata#1737 | ci | Moved the E2E suite to a manual-dispatch workflow and split Rust tests into four shards, since E2E gated every PR. |
| 2026-10-15 | lgse/strata#1701 | test | Made the Open With and release tar test fixtures independent of the host's applications and `tar` location, for Nix builds. |
| 2026-10-15 | lgse/strata#1700 | docs | Added a hardened-configuration guide that lists optional settings shrinking the attack surface. |
| 2026-10-15 | lgse/strata#1676 | fix | Marked debug builds with a `+debug` version suffix and listed the release `install-local` first for source builds, so slow debug builds show in reports. |
| 2026-10-15 | lgse/strata#1672 | test | Added a headless scroll benchmark for Columns, List, and Icons that reports CPU per step, frame times, and idle wakeups. |
| 2026-10-14 | lgse/strata#1647 | fix | Installed cargo-watch through mise's `github:` backend with pinned SHA-512 checksums, since mise rejects its legacy minisign signature. |
| 2026-10-13 | lgse/strata#1601 | fix | Pinned GTK font rendering to manual so GL and Vulkan keep glyph top rows, and regenerated screenshot baselines. |
| 2026-10-12 | lgse/strata#1588 | feat | Replaced the language glyphs with Catppuccin file icons in Mocha and Latte flavors and added a File icon colors preference. |
| 2026-10-09 | lgse/strata#1533 | fix | Parsed GIO URIs with encoded path flags, displayed non-UTF-8 locations percent-encoded, and logged skipped listing entries. |
| 2026-08-30 | lgse/strata#27 | fix | Removed browsed locations from default logs and redacted URI credentials from diagnostic ones. |

## Known gaps

None known.
