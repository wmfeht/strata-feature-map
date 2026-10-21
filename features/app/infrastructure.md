---
title: Shared location model and listing adapter
status: shipped
origin: {issue: lgse/strata#14, pr: lgse/strata#27}
branch: null
reviewed_at: 4b9a6ace71017888b3a2124d7d911c5c664cc767
review: draft
code: [src/model/mod.rs, src/adapters/local_files.rs, src/ui/mod.rs, src/main.rs, src/app/mod.rs, src/adapters/mod.rs, src/services/mod.rs, src/ui/resize_feedback.rs, src/ui/preferences/trashed.rs, src/adapters/volume/mounts.rs, src/adapters/volume/mount_snapshot.rs, README.md, docs/assets/strata-themes.png, THIRD_PARTY_LICENSES.md, data/licenses, data/strata.gresource.xml, AGENTS.md, typos.toml, clippy.toml, scripts/e2e-native.sh, Cargo.toml, Cargo.lock, mise.toml, mise.lock, scripts/benchmark-scroll.py, src/build_info.rs, src/services/native_fs.rs, src/ui/keys/bindings.rs, src/ui/keys/bindings/**, build.rs, deny.toml, .github/workflows/ci.yml, .github/workflows/e2e.yml, .github/workflows/e2e-cache.yml, .github/workflows/integrations.yml, .github/ISSUE_TEMPLATE/bug_report.yml, scripts/quality.sh, scripts/quality_ci.py, scripts/test-headless.py, scripts/integration_tests.py, src/ui/settings/install_command.rs, src/adapters/local_operations/fs_ops.rs, src/adapters/local_operations/native_fs.rs, src/adapters/local_operations/work_queue.rs, src/trusted_command.rs, src/adapters/gio_close.rs, src/adapters/volume/mount_watch.rs, src/adapters/volume/mount_lanes.rs, src/adapters/local_operations/probes.rs, src/util/ui_thread.rs, src/util/ui_thread/**, scripts/e2e.sh, scripts/e2e-mutation-check.sh, scripts/trace-main-io.py, tests/e2e/Dockerfile, tests/e2e/main-io-allowlist.toml]
tests: [src/model/tests.rs, src/adapters/local_files/tests.rs, src/adapters/local_files/tests/browse.rs, src/adapters/volume/mounts/tests.rs, src/test_support.rs, src/test_support/**, tests/e2e/harness/**, tests/e2e/baselines/**, tests/e2e/conftest.py, tests/e2e/unit/test_keyboard_layout.py, tests/e2e/unit/test_harness.py, scripts/test_benchmark_scroll.py, src/build_info/tests.rs, scripts/test_quality_ci.py, scripts/test_quality_runner.py, scripts/test_headless_runner.py, scripts/test_e2e_runner.py, scripts/test_integration_tests.py, src/ui/settings/install_command/tests.rs, src/trusted_command/tests.rs, src/adapters/gio_close/tests.rs, src/adapters/local_operations/tests/closes.rs, src/adapters/volume/mount_watch/tests.rs, src/adapters/volume/mount_lanes/tests.rs, src/adapters/local_operations/probes/tests.rs, src/adapters/local_operations/fs_ops/tests.rs, src/adapters/volume/mounts/tests/byte_paths.rs, scripts/test_trace_main_io.py]
docs: [docs/performance-baseline.md, docs/hardened-configuration.md, docs/unsafe-code.md, docs/e2e-testing.md]
related: [remote/file-providers/network-locations, operations/trash, browser/navigation/location-bar, browser/directory-monitoring, preview/preview-panel, preview/preview-panel/sandbox, app/updates/install, settings/diagnostics, operations/filesystem-compatibility, operations/delete]
---

## Summary

The location model, URI display and diagnostic rules, and the directory-listing adapter that every feature shares, plus the crate and module roots. It also owns shared helpers, test support, catalogs, the README, third-party notices, and crate manifests. It owns the build script, CI workflows and tooling, the bug report template, and lint, dependency-audit, and agent configuration. It owns the trusted helper lookup and the syscall layer that local operations share. It owns the mount-table watcher, per-mount request lanes, off-thread probes and closes, and the UI-thread checks. It is the `fallback` node in `scopes.yaml`.

## Behavior

### URI display

- The location field and Properties show a URI location decoded only when its whole path is valid UTF-8 and has no `%2F`. lgse/strata#1424, lgse/strata#1533
- Otherwise the whole path shows percent-encoded, such as `sftp://host/share/%FF%20name`. lgse/strata#1424, lgse/strata#1533

### Listing

- A URI listing, such as Trash or an SMB share, skips an entry whose URI cannot be converted to a location. lgse/strata#1424, lgse/strata#1533 (unverified)
- Each skipped entry logs a warning with only the request id and backend name; the folder and entry name appear only at DEBUG. lgse/strata#1424, lgse/strata#1533

### Folder monitoring

- Copying a file into an open local folder shows no `#<inode>` entry while it is written; the file appears once, under its final name. lgse/strata#1615
- A file linked into a watched folder is queried once, so its row updates once. lgse/strata#1615 (unverified)
- Moving a file out of an open folder and creating a file under its old name in the same moment shows the new file. lgse/strata#1615 (unverified)

### Media metadata

- In Icons, a file named `clip.mp4` or `photo.png` whose first 8 KiB are text starts no sandboxed metadata probe. lgse/strata#1638
- In Icons, an SVG holding XML text still shows its width×height in its caption. lgse/strata#1638 (unverified)

### Log privacy

- At the default log level, a directory load logs its request id and backend name, never the browsed path or URI. lgse/strata#27
- With `RUST_LOG=strata=debug`, a directory load also logs its location, including the full native path. lgse/strata#27
- Logged URI locations omit user info, authentication parameters, query, and fragment at every log level. lgse/strata#27

### UI thread

- With `STRATA_UI_STALL_MS=250`, a UI thread blocked for 250 ms logs "UI thread stalled N ms" and the call it waits in. lgse/strata#1729
- When the blocked UI thread runs again, the log adds "UI thread ran again after N ms". lgse/strata#1729
- A stall that lasts logs again each time it doubles: at 2, 4, and 8 times the limit, and so on. lgse/strata#1729 (unverified)
- The portal file chooser backend starts the same stall watchdog. lgse/strata#1729 (unverified)
- Without `STRATA_UI_STALL_MS`, or with `0` or a non-number, no stall watchdog runs. lgse/strata#1729 (unverified)
- In a debug build, a guarded file call on the UI thread panics with "file calls must not run on the UI thread". Start-up and the exit flush are exempt. lgse/strata#1729 (unverified)
- Guarded calls include reading the install marker, searching `PATH` for helpers, and replacing a settings or state file. lgse/strata#1729 (unverified)

### Working folder

- Once command-line paths are resolved, Strata's working folder is `/`. An application it launches without a desktop `Path=` starts in `/`. lgse/strata#1729
- The D-Bus service and the portal backend change their working folder to `/` at start. lgse/strata#1729

### Trusted helper lookup

- A helper present in both a fixed root and a configured directory resolves to the fixed-root copy. lgse/strata#1746
- A build with an empty or relative `STRATA_TRUSTED_COMMAND_PATH` entry, such as `relative/bin` or a trailing `:`, fails with "must be an absolute directory". lgse/strata#1746
- A configured directory that is missing or does not canonicalize under `/usr/bin`, `/usr/sbin`, `/bin`, `/sbin`, `/run/wrappers/bin`, `/nix/store`, or `/gnu/store` is skipped. lgse/strata#1746
- A helper in a configured directory whose canonical target lies outside those roots is rejected, and the search moves to the next directory. lgse/strata#1746
- With no trusted copy in any directory, the lookup fails closed. lgse/strata#1055, lgse/strata#1746

## Design

[docs/performance-baseline.md](https://github.com/lgse/strata/blob/aee71335dfecd059b9af23efeac2ed52c43e3b19/docs/performance-baseline.md) states the log privacy levels: default logs carry request ids, backend names, counts, and timings only.

- Desktop logs and journals can retain usernames, project names, and mounted locations, so browsed locations need an explicit diagnostic opt-in (lgse/strata#14, lgse/strata#27).
- `Location` display and diagnostic paths once parsed strictly and showed `<invalid-uri>` for non-UTF-8 names in the path bar and Properties. They now share the GIO conversion's parse flags (lgse/strata#1424, lgse/strata#1533).
- Display tries the decoded form first, so valid names such as `smb://host/café` still display decoded (lgse/strata#1533).
- Display decodes only valid UTF-8 without `%2F`: decoding `%2F` would turn a name into a separator once the shown text is edited. Plain `UriFlags::ENCODED` was rejected because it stops userinfo decoding (lgse/strata#1424, lgse/strata#1533).
- The directory loader dropped unconvertible entries without a trace. Logging each skip keeps a future conversion failure visible (lgse/strata#1424, lgse/strata#1533).
- A stopped NFS, SMB, sshfs, or FUSE server gives no timely error, so disk calls run off the UI thread ([docs/filesystem-compatibility.md](https://github.com/lgse/strata/blob/fd6327265eaa3266f8420fe8bd25e965146344b0/docs/filesystem-compatibility.md), "What a dead server does"). Debug assertions, the stall watchdog, and `scripts/trace-main-io.py` check that (lgse/strata#1590, lgse/strata#1729).
- [docs/e2e-testing.md](https://github.com/lgse/strata/blob/fd6327265eaa3266f8420fe8bd25e965146344b0/docs/e2e-testing.md) describes the trace script: it runs E2E scenarios with the UI thread under `strace`, and `tests/e2e/main-io-allowlist.toml` lists only documented exceptions (lgse/strata#1729).
- The selection position cache's comparison against a full listing scan sits behind the `invariant-checks` Cargo feature. Both E2E runners and `cargo test --all-features` enable it; plain `cargo build` leaves it off ([docs/e2e-testing.md](https://github.com/lgse/strata/blob/4b9a6ace71017888b3a2124d7d911c5c664cc767/docs/e2e-testing.md), lgse/strata#1792).
- The `fstatat` fallback widens `st_nlink` through a generic helper, because it is `u32` on aarch64 and `u64` on x86_64 (lgse/strata#1753, lgse/strata#1755).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-21 | lgse/strata#1792 | perf | Stopped re-sorting type groups on every published chunk and raised the folder listing cap to 250,000 entries. |
| 2026-10-21 | lgse/strata#1794 | docs | Corrected the theme count, default theme, 10xer exit key, and Settings paths in the README and docs so they match the app. |
| 2026-10-18 | lgse/strata#1755 | fix | Widened `st_nlink` in the legacy stat fallback so the aarch64 release builds again. |
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
