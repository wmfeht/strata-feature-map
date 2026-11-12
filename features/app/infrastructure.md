---
title: Shared location model and listing adapter
status: shipped
origin: {issue: lgse/strata#14, pr: lgse/strata#27}
branch: null
reviewed_at: 5f17c9fdc8967e1b4ba8aaf8de113b46d824b0dd
review: draft
code: [crates/strata-core/src/model/mod.rs, src/ui/settings.rs, crates/strata-fs/src/adapters/local_files.rs, src/ui/mod.rs, src/main.rs, crates/strata-fs/src/app/mod.rs, crates/strata-fs/src/adapters/mod.rs, src/services/mod.rs, src/ui/resize_feedback.rs, src/ui/preferences/trashed.rs, crates/strata-fs/src/adapters/volume/mounts.rs, crates/strata-fs/src/adapters/volume/mount_snapshot.rs, README.md, THIRD_PARTY_LICENSES.md, data/licenses, data/strata.gresource.xml, AGENTS.md, typos.toml, clippy.toml, Cargo.toml, Cargo.lock, mise.toml, mise.lock, scripts/benchmark-scroll.py, crates/strata-desktop/src/build_info.rs, crates/strata-fs/src/services/native_fs.rs, src/ui/keys/bindings.rs, src/ui/keys/bindings/**, build.rs, deny.toml, scripts/quality.sh, scripts/quality_ci.py, scripts/test-headless.py, scripts/integration_tests.py, src/ui/settings/install_command.rs, crates/strata-fs/src/adapters/local_operations/fs_ops.rs, crates/strata-fs/src/adapters/local_operations/native_fs.rs, crates/strata-fs/src/adapters/local_operations/work_queue.rs, crates/strata-core/src/trusted_command.rs, crates/strata-fs/src/adapters/gio_close.rs, crates/strata-fs/src/adapters/volume/mount_watch.rs, crates/strata-fs/src/adapters/volume/mount_lanes.rs, crates/strata-fs/src/adapters/local_operations/probes.rs, crates/strata-core/src/util/ui_thread.rs, crates/strata-core/src/util/ui_thread/**, scripts/trace-main-io.py, tests/qa/main-io-allowlist.toml, .agents/skills, .claude/skills, .gitignore, .cursor/CLOUD.md, .dockerignore, CONTRIBUTING.md, scripts/check.sh, src/qa.rs, src/qa/**, crates/strata-qa/src/**, crates/*/Cargo.toml, crates/*/build.rs, crates/strata-core/src/lib.rs, crates/strata-desktop/src/lib.rs, crates/strata-fs/src/lib.rs, crates/strata-preview/src/lib.rs, crates/strata-desktop/src/services/mod.rs, crates/strata-fs/src/services/mod.rs, crates/strata-preview/src/services/mod.rs, crates/strata-core/src/error_text.rs, crates/strata-core/src/model/load_handle.rs, src/util/mod.rs, src/ui/accessibility/qa.rs, scripts/qa*.sh, scripts/qa_*.py, scripts/lib/qa-container.sh, scripts/headless/**, scripts/image_*.py, tests/container/**, tests/fixtures/harness.json, crates/strata-core/src/logging.rs, crates/strata-core/src/metrics.rs, crates/strata-fs/src/services/listeners.rs, crates/strata-fs/src/services/network_error.rs, src/ui/close_guard.rs, src/ui/browser/paths.rs, src/ui/browser/entry_animation.rs, data/icons/scalable/actions/**, .github, .gitattributes, CLAUDE.md, LICENSE, rustfmt.toml, skills-lock.json, docs/assets, docs/evidence, scripts/discord_triage.py, scripts/profile-fixture.sh, scripts/generate-fixture.sh, scripts/quality-durations.json, scripts/release_version.py, scripts/start-dev.sh, crates/strata-desktop/src/services/package_manager.rs, src/ui/browser/location.rs, src/ui/browser/pane_header.rs, scripts/code-health.sh, crates/strata-fs/src/adapters/local_files/fill.rs, crates/strata-fs/src/adapters/local_files/native.rs, crates/strata-fs/src/adapters/local_files/remote.rs, crates/strata-fs/src/app/browser/activation.rs, crates/strata-fs/src/app/browser/entries.rs, crates/strata-fs/src/app/browser/file_operations.rs, src/ui/browser/events/operations.rs, src/ui/browser/events/reveal.rs, src/ui/browser/view_edit.rs, src/ui/browser/view_setup.rs, src/ui/browser/view_state.rs, src/ui/preferences/appearance_settings.rs, src/ui/preferences/defaults.rs, src/ui/preferences/file_settings.rs, src/ui/preferences/input_settings.rs, src/ui/preferences/stored.rs, src/ui/browser/clipboard.rs, crates/strata-fs/src/app/browser/operation_events.rs]
tests: [crates/strata-fs/src/app/navigation/tests/loading.rs, src/ui/window/tests/keyboard_dispatch/icon_motion.rs, crates/strata-core/src/model/tests.rs, crates/strata-fs/src/adapters/local_files/tests.rs, crates/strata-fs/src/adapters/local_files/tests/browse.rs, crates/strata-fs/src/adapters/volume/mounts/tests.rs, src/test_support.rs, src/test_support/**, crates/strata-test-support/src/**, crates/strata-fs/src/test_support.rs, crates/strata-fs/src/test_support/**, crates/strata-core/src/error_text/tests.rs, scripts/test_benchmark_scroll.py, crates/strata-desktop/src/build_info/tests.rs, scripts/test_quality_ci.py, scripts/test_quality_runner.py, scripts/test_headless_runner.py, scripts/test_integration_tests.py, src/ui/settings/install_command/tests.rs, crates/strata-core/src/trusted_command/tests.rs, crates/strata-fs/src/adapters/gio_close/tests.rs, crates/strata-fs/src/adapters/local_operations/tests/closes.rs, crates/strata-fs/src/adapters/volume/mount_watch/tests.rs, crates/strata-fs/src/adapters/volume/mount_lanes/tests.rs, crates/strata-fs/src/adapters/local_operations/probes/tests.rs, crates/strata-fs/src/adapters/local_operations/fs_ops/tests.rs, crates/strata-fs/src/adapters/volume/mounts/tests/byte_paths.rs, scripts/test_trace_main_io.py, tests/qa.rs, tests/qa/*.rs, tests/qa/foreign_drag_source.py, tests/qa/baselines/**, src/qa/tests.rs, src/qa/tests/**, scripts/test_qa_*.py, scripts/test_image_*.py, tests/qa/scenarios/visual_baselines, crates/strata-core/src/logging/tests.rs, crates/strata-core/src/metrics/tests.rs, crates/strata-fs/src/services/listeners/tests.rs, crates/strata-fs/src/services/network_error/tests.rs, scripts/test_discord_triage.py, scripts/test_makefile.py, scripts/test_release_version.py, src/tests.rs, src/ui/preferences/tests/preferences.rs, src/ui/window/tests/preferences.rs, tests/qa/fixtures/file_drag_source.py, crates/strata-desktop/src/services/package_manager/tests.rs, src/ui/browser/location/tests.rs, crates/strata-fs/src/adapters/local_files/tests/enumeration.rs, crates/strata-fs/src/adapters/local_files/tests/logging.rs, crates/strata-fs/src/adapters/local_files/tests/metadata_fill.rs, crates/strata-fs/src/adapters/local_files/tests/stalled_mounts.rs, crates/strata-fs/src/adapters/local_files/tests/support.rs, crates/strata-fs/src/adapters/local_files/tests/validation.rs, crates/strata-fs/src/app/browser/tests/providers.rs, crates/strata-fs/src/app/browser/tests/scripted.rs, crates/strata-fs/src/app/browser/tests/sources.rs, crates/strata-fs/src/app/browser/tests/support.rs, src/ui/preferences/tests/preferences/relocations.rs, src/ui/window/tests/keyboard_dispatch/window_support.rs, src/ui/window/tests/keyboard_dispatch/jump_keys.rs, src/ui/keys/tests/catalog.rs, src/ui/window/tests/preferences/browsing_prefs.rs, src/ui/window/tests/preferences/sidebar_prefs.rs, tests/qa/scenarios/locations/scrolled-away-crumbs-and-columns-stay-reachable.jsonl, src/ui/browser/clipboard/tests.rs, src/ui/window/tests/keyboard_dispatch/file_commands.rs, src/ui/window/tests/keyboard_dispatch/file_commands/create.rs, src/ui/window/tests/keyboard_dispatch/file_commands/delete.rs, src/ui/window/tests/keyboard_dispatch/file_commands/trashless.rs, tests/qa/scenarios/entry_management/undo-created-folder-trashes.jsonl, tests/qa/scenarios/inline_renaming/rename-and-undo-restores.jsonl]
docs: [docs/performance-baseline.md, docs/hardened-configuration.md, docs/unsafe-code.md, docs/testing.md, docs/packaging.md, docs/workspace.md]
related: [remote/file-providers/integrations, remote/file-providers/network-locations, operations/trash, browser/navigation/location-bar, browser/directory-monitoring, preview/preview-panel, preview/preview-panel/sandbox, app/updates/install, settings/diagnostics, operations/filesystem-compatibility, operations/delete, integration/file-manager-interface/service-activation]
---

## Summary

The location model, URI display and diagnostic rules, and the directory-listing adapter that every feature shares. It also owns the crate and module roots, including the workspace crates' roots and facades. It owns shared helpers, test support, catalogs, the README, third-party notices, and crate manifests. It owns the build scripts, CI workflows and tooling, the bug report template, and lint, dependency-audit, and agent configuration and skills. It owns the `qa` build's in-process QA harness, the `strata-qa` protocol crate, the QA runner, and the pinned test image. It owns the trusted helper lookup, the syscall layer that local operations share, and the Run in terminal control that Diagnostics and Integrations share. It owns the mount-table watcher, per-mount request lanes, off-thread probes and closes, and the UI-thread checks. It owns the List and Icons pane header, shared by the sort controls and the Back history menu. It is the `fallback` node in `scopes.yaml`.

## Behavior

### URI display

- The location field and Properties show a URI location decoded only when its whole path is valid UTF-8 and has no `%2F`. lgse/strata#1424, lgse/strata#1533
- Otherwise the whole path shows percent-encoded, such as `sftp://host/share/%FF%20name`. lgse/strata#1424, lgse/strata#1533

### URI hosts

- An MTP device whose name holds non-ASCII text, such as `mtp://OnePlus_%E4%B8%80%E5%8A%A0_Ace_5_Pro_9d231cfe/`, opens at its mount root instead of reporting "The location is not mounted". Its location keeps the host as GVfs spells it, not `xn--…`, with or without credentials in the URI. lgse/strata#2072
- A URI whose user info holds a second `@`, such as `sftp://a@b@c/x`, becomes `sftp://a@c/x`, a different host, instead of `sftp://a@b%40c/x`. lgse/strata#2072
- A host with a raw space, such as `smb://MY SERVER/share`, keeps the space instead of becoming `smb://MY%20SERVER/share`. lgse/strata#2072

### Listing

- A URI listing, such as Trash or an SMB share, skips an entry whose URI cannot be converted to a location. lgse/strata#1424, lgse/strata#1533 (unverified)
- Each skipped entry logs a warning with only the request id and backend name; the folder and entry name appear only at DEBUG. lgse/strata#1424, lgse/strata#1533

### Media metadata

- In Icons, a file named `clip.mp4` or `photo.png` whose first 8 KiB are text starts no sandboxed metadata probe. lgse/strata#1638
- In Icons, an SVG holding XML text still shows its width×height in its caption. lgse/strata#1638 (unverified)

### Log privacy

- At the default log level, a directory load logs its request id and backend name, never the browsed path or URI. lgse/strata#27
- With `RUST_LOG=strata=debug`, a directory load also logs its location, including the full native path. lgse/strata#27
- Logged URI locations omit user info, authentication parameters, query, and fragment at every log level. lgse/strata#27, lgse/strata#1873

### Log filters

- With `RUST_LOG=strata::sandbox::browser=debug`, opening a preview still prints the sandbox's debug lines, though that module moved to a crate. lgse/strata#2112
- A moved module's log lines carry its crate's target, such as `strata_preview::sandbox::browser`; `RUST_LOG=strata=debug` still shows them. lgse/strata#2112

### UI thread

- With `STRATA_UI_STALL_MS=250`, a UI thread blocked for 250 ms logs "UI thread stalled N ms" and the call it waits in. lgse/strata#1729
- When the blocked UI thread runs again, the log adds "UI thread ran again after N ms". lgse/strata#1729
- A stall that lasts logs again each time it doubles: at 2, 4, and 8 times the limit, and so on. lgse/strata#1729 (unverified)
- The portal file chooser backend starts the same stall watchdog. lgse/strata#1729 (unverified)
- Without `STRATA_UI_STALL_MS`, or with `0` or a non-number, no stall watchdog runs. lgse/strata#1729 (unverified)
- In a debug build, a guarded file call on the UI thread panics with "file calls must not run on the UI thread". Start-up and the exit flush are exempt. lgse/strata#1729 (unverified)
- Guarded calls include reading the install marker, searching `PATH` for helpers, and replacing a settings or state file. lgse/strata#1729 (unverified)

### Working folder

- Once command-line paths are resolved, Strata's working folder is `/`. lgse/strata#1729
- The D-Bus service and the portal backend change their working folder to `/` at start. lgse/strata#1729

### Trusted helper lookup

- A helper present in both a fixed root and a configured directory resolves to the fixed-root copy, unless `resolve_unprivileged` skips that copy. lgse/strata#1746, lgse/strata#2182
- `resolve_unprivileged` skips a candidate whose canonical target has the setuid or setgid bit and tries the next directory. lgse/strata#2182
- A build with an empty or relative `STRATA_TRUSTED_COMMAND_PATH` entry, such as `relative/bin` or a trailing `:`, fails with "must be an absolute directory". lgse/strata#1746
- A configured directory that is missing or does not canonicalize under `/usr/bin`, `/usr/sbin`, `/bin`, `/sbin`, `/run/wrappers/bin`, `/nix/store`, or `/gnu/store` is skipped. lgse/strata#1746
- A helper in a configured directory whose canonical target lies outside those roots is rejected, and the search moves to the next directory. lgse/strata#1746
- With no trusted copy in any directory, the lookup fails closed. lgse/strata#1055, lgse/strata#1746

### Service activation

- Started with `--gapplication-service` before any `--`, or with `--portal` first, Strata re-execs before GTK starts. The re-exec appends `no-portals` to `GDK_DEBUG`, such as `misc:no-portals`. lgse/strata#1811, lgse/strata#2024
- With `GDK_DEBUG` unset, `strata --portal` re-execs with `GDK_DEBUG=no-portals`, and `STRATA_ORIGINAL_GDK_DEBUG` holds the original value, empty when unset. lgse/strata#2024
- `strata --portal` with `GTK_THEME=Adwaita` set re-execs once, both dropping `GTK_THEME` and adding `no-portals`. lgse/strata#2024
- A portal `OpenDirectory` request, such as Chromium's Show in folder, while Strata is not running, opens Strata without the 25 s `ShowItems` timeout. lgse/strata#1810, lgse/strata#1811
- A portal FileChooser `OpenFile` request from Telegram, while `strata --portal` is not running, opens the chooser without the 25 s timeout. lgse/strata#2023, lgse/strata#2024
- `strata`, `strata /tmp`, `strata -- --gapplication-service`, and `--preview-helper` launches add no override and do not re-exec for it. lgse/strata#1811, lgse/strata#2024
- A `GDK_DEBUG` that already holds `no-portals` as any `:`, `;`, `,`, space, or tab-separated flag, in any case, adds nothing and does not re-exec for it. lgse/strata#1811, lgse/strata#2024 (unverified)
- Later `strata` launches open in the activated process, so GTK portals stay off until that process exits. lgse/strata#1811
- The portal backend keeps GTK portals off for its lifetime, until its idle exit. lgse/strata#2024 (unverified)

## Design

[docs/performance-baseline.md](https://github.com/lgse/strata/blob/aee71335dfecd059b9af23efeac2ed52c43e3b19/docs/performance-baseline.md) states the log privacy levels: default logs carry request ids, backend names, counts, and timings only.

- Desktop logs and journals can retain usernames, project names, and mounted locations, so browsed locations need an explicit diagnostic opt-in (lgse/strata#14, lgse/strata#27).
- `Location` display and diagnostic paths once parsed strictly and showed `<invalid-uri>` for non-UTF-8 names in the path bar and Properties. They now share the GIO conversion's parse flags (lgse/strata#1424, lgse/strata#1533).
- Display tries the decoded form first, so valid names such as `smb://host/café` still display decoded (lgse/strata#1533).
- Display decodes only valid UTF-8 without `%2F`: decoding `%2F` would turn a name into a separator once the shown text is edited. Plain `UriFlags::ENCODED` was rejected because it stops userinfo decoding (lgse/strata#1424, lgse/strata#1533).
- The directory loader dropped unconvertible entries without a trace. Logging each skip keeps a future conversion failure visible (lgse/strata#1424, lgse/strata#1533).
- A stopped NFS, SMB, sshfs, or FUSE server gives no timely error, so disk calls run off the UI thread ([docs/filesystem-compatibility.md](https://github.com/lgse/strata/blob/fd6327265eaa3266f8420fe8bd25e965146344b0/docs/filesystem-compatibility.md), "What a dead server does"). Debug assertions, the stall watchdog, and `scripts/trace-main-io.py` check that (lgse/strata#1590, lgse/strata#1729).
- [docs/testing.md](https://github.com/lgse/strata/blob/c94eeb0020fa1154e11c741888f1b56d92ce70d6/docs/testing.md) ("Main-thread I/O audit") describes the trace script. It runs QA scenarios through `scripts/qa.sh`, and `tests/qa/main_io.rs` starts each launch with its UI thread under `strace` (lgse/strata#1729, lgse/strata#1807).
- `tests/qa/main-io-allowlist.toml` lists only documented exceptions. QA mode's own disk reads run on a helper thread, so an audit sees only calls a release build makes (lgse/strata#1729, lgse/strata#1807).
- The selection position cache's comparison against a full listing scan sits behind the `invariant-checks` Cargo feature. `scripts/qa.sh`, `scripts/qa-drive.sh`, and `cargo test --all-features` enable it; plain `cargo build` leaves it off ([docs/testing.md](https://github.com/lgse/strata/blob/c94eeb0020fa1154e11c741888f1b56d92ce70d6/docs/testing.md), lgse/strata#1771, lgse/strata#1792, lgse/strata#1807).
- The `--qa` launch mode, its JSON protocol, and its in-process XTEST or Wayland virtual input sit behind the `qa` Cargo feature, never in releases. Without it, `launch_mode` treats `--qa` as the plain application launch mode (lgse/strata#1771, lgse/strata#1957, unverified).
- CI fails when `x11rb`, `wayland-client`, `wayland-protocols-misc`, `wayland-protocols-wlr`, or `xkbcommon`, the `qa` feature's input clients, are in a default or feature-disabled build. The release workflow fails when a binary contains `usage: strata --qa` (lgse/strata#1771, lgse/strata#1957, unverified).
- `tests/qa.rs` refuses to run without the `STRATA_QA_CONTAINER=1` that `scripts/qa.sh` sets, unless `STRATA_QA_HOST=1` is set ([docs/testing.md](https://github.com/lgse/strata/blob/c94eeb0020fa1154e11c741888f1b56d92ce70d6/docs/testing.md), lgse/strata#1771).
- A host run with `STRATA_QA_DISPLAY=wayland` replaces Xvfb with a private headless sway and launches with `GDK_BACKEND=wayland`. Input goes through a Wayland virtual keyboard and pointer. It exists to reproduce Wayland and input-method bugs such as lgse/strata#1715. A Wayland run is never validation evidence; CI and `scripts/qa.sh` stay X11 ([docs/testing.md](https://github.com/lgse/strata/blob/965bd7ec74400734dbd0a5311ceefa05bea8dd63/docs/testing.md) "Wayland and input methods (host runs)", lgse/strata#1957).
- On that Wayland display, a `layout` step other than `us` and pixel sampling fail with a message; they are X11-only (lgse/strata#1957).
- A scenario header's `input_method` field, which needs `session_bus`, starts a private fcitx5 on the run's display and bus. Scenarios needing it carry a `skip` reason, since the pinned image has no fcitx5 (lgse/strata#1957).
- QA scenarios are the only GUI suite. Keeping the Python E2E suite in parity doubled the cost of every GUI change for no extra coverage (lgse/strata#1806, lgse/strata#1807).
- QA in CI runs only on manual dispatch, and no required check depends on it (lgse/strata#1806, lgse/strata#1807).
- On service activation, xdg-desktop-portal 1.22.1 waits in `OpenDirectory` for the `ShowItems` reply, while GTK's startup queries that portal before FileManager1 is exported. Replying earlier in the handler cannot break that wait (lgse/strata#1810, lgse/strata#1811).
- The portal waits the same way in `OpenFile` for the FileChooser backend, while the backend's GTK startup queries the portal. The backend's 120 s idle exit makes that cold activation routine (lgse/strata#2023, lgse/strata#2024).
- The override is set by re-exec before GTK starts, not by changing the environment after threads may run. It shares the Cairo renderer and `GTK_THEME` restart path (lgse/strata#1811). The FileChooser backend reuses that re-exec instead of a new mechanism (lgse/strata#2023, lgse/strata#2024).
- The override is scoped to service activation and is not a substitute for asynchronous dispatch in the portal. Packagers keep `--gapplication-service` and `--portal` in activation commands and do not set `no-portals` globally (lgse/strata#1811, lgse/strata#2024, docs/packaging.md).
- Mount roots get their shown name from the URI: the percent-decoded last path segment, or the host at a server root. GVfs reports `/` as a mount root's leaf name, even an SMB share's. Only the shown name is decoded; the URI used for I/O is unchanged (lgse/strata#2009, lgse/strata#2027, [docs/architecture.md](https://github.com/lgse/strata/blob/bae71c026b94e109b7507c4fe895c3ceed642f8f/docs/architecture.md)).
- A non-ASCII host keeps the form it was typed in, not punycode (lgse/strata#2027). GVfs matches an MTP device name as text, so `mtp://xn--…` and `mtp://OnePlus_%E4…` are different files to it (lgse/strata#2072).
- Credential sanitizing still parses with DNS host rules, then splices the input's host text back into GLib's output. Parent locations and `display_path` do not, so they still give punycode (lgse/strata#2072).
- `--unlock-volume` usage errors reach the invoking terminal through one `unsafe` call to `g_application_command_line_printerr` with a fixed `"%s"` format. gio-rs binds `printerr_literal` only from GLib 2.80, above the 2.72 Strata supports. [docs/unsafe-code.md](https://github.com/lgse/strata/blob/bae71c026b94e109b7507c4fe895c3ceed642f8f/docs/unsafe-code.md) lists it until Strata requires GLib 2.80 (lgse/strata#2015, lgse/strata#2030).
- CodeScene hotspot health fell from 4.68 to 3.13 between 2026-09-17 and 2026-10-15, because behavior grew "god files" such as a 6,008-line `local_operations.rs` (lgse/strata#1686).
- lgse/strata#2022 split those files into submodules by responsibility and re-exported moved items from their old paths, so callers did not change. Five or more parameters became context or request structs.
- The upstream `AGENTS.md` "Code health" rule: a change must not lower the health of the files it touches. New behavior goes in a new submodule instead of growing a file past about 1,500 lines (lgse/strata#2022).
- `scripts/code-health.sh` runs the CodeScene CLI on named or changed files and needs `CS_ACCESS_TOKEN` (lgse/strata#2022).
- `qa-drive restart --pref` replaces each key whole in the parsed `settings.toml`. It refuses a value TOML cannot hold, or a key that is not a bare TOML key, before the app stops (lgse/strata#2019, lgse/strata#2030).
- The QA driver wheels a clipped pointer target into view, with Shift for horizontal scrollers, and never scrolls a `left_bound` aim. On X11, `type` lends a keysym to an empty keycode for one tap (lgse/strata#2019, lgse/strata#2030).
- The `magick` fixture step checks an `.avif`, `.heic`, or `.heif` output's ISO BMFF brand (lgse/strata#2019, lgse/strata#2070).
- ImageMagick without an encoder writes the input format and still exits 0 ([docs/testing.md](https://github.com/lgse/strata/blob/35ee677ab0a633d5d49055464f2946fcf4995ae7/docs/testing.md), lgse/strata#2019, lgse/strata#2070).
- Rust tests create private main contexts only through `test_support::PrivateContext`; Clippy rejects `glib::MainContext::new` and `with_flags` (lgse/strata#1963, lgse/strata#2070).
- A GIO pool thread could drop a private context's last reference, finalizing its local tasks off their thread and aborting the test process. `PrivateContext` destroys the leftover sources on the owning thread when dropped (lgse/strata#1963, lgse/strata#2070).
- A source attached after that drop is leaked on purpose, so nothing on the context is finalized on another thread. Production uses only the default context ([docs/testing.md](https://github.com/lgse/strata/blob/35ee677ab0a633d5d49055464f2946fcf4995ae7/docs/testing.md), lgse/strata#2070).
- Since lgse/strata#2112 the repository is a Cargo workspace. Code that needs no GTK lives in `crates/strata-{core,preview,fs,desktop,qa,test-support}`, so a second interface can reuse it (lgse/strata#2111, [docs/workspace.md](https://github.com/lgse/strata/blob/5f17c9fdc8967e1b4ba8aaf8de113b46d824b0dd/docs/workspace.md)).
- The crates are layered core, preview, fs, desktop; qa and test-support depend on none. The root `strata` package is the GTK interface (lgse/strata#2112, docs/workspace.md).
- `cargo deny check` keeps `gtk4`, `gdk4`, `sourceview5`, and `gstreamer` out of the crates. `deny.toml` lists, per toolkit and crate, which crates may depend on it directly (lgse/strata#2112, docs/workspace.md).
- The root re-exports every moved module at its old path, so `src/services/mod.rs` and `src/util/mod.rs` are facades and callers kept their paths (lgse/strata#2112, docs/workspace.md).
- An item is `pub` only when another crate names it. `release_channel` stays private, so the interface cannot reach the never-downgrade bypass (lgse/strata#2112, docs/workspace.md).
- Each crate's `test-support` feature exposes test hooks to other crates' tests. The QA runner builds without it, so the driven binary carries no test hooks (lgse/strata#2112, docs/workspace.md).
- `EXTRACTED_CRATES` in `crates/strata-core/src/logging.rs` repeats each `strata::module` filter for the crates, so filters written before the split still select the same code (lgse/strata#2112, docs/workspace.md).
- `crates/strata-desktop/build.rs` sets the build facts and reads the version from the root manifest; the root `build.rs` compiles only the resource bundle (lgse/strata#2112, docs/workspace.md).
- The `fstatat` fallback widens `st_nlink` through a generic helper, because it is `u32` on aarch64 and `u64` on x86_64 (lgse/strata#1753, lgse/strata#1755).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-11-12 | lgse/strata#2120 | build | Added a Fedora RPM built from source and published to stable and preview COPR projects, so Fedora users install and update Strata through dnf. |
| 2026-11-12 | lgse/strata#2112 | refactor | Split the toolkit-free code into workspace crates under `crates/`, so a second interface can reuse it without GTK. |
| 2026-11-06 | lgse/strata#2072 | fix | Kept a GVfs URI's non-ASCII host as given through credential sanitizing, so MTP devices with CJK names open instead of reporting not mounted. |
| 2026-11-06 | lgse/strata#2070 | fix | Installed libheif in the test image, failed unbranded AVIF/HEIC fixtures, and destroyed private test contexts' sources on their own thread. |
| 2026-11-03 | lgse/strata#2041 | perf | Built the Back history menu's rows when it opens, capped at the 50 most recent, instead of on every navigation. |
| 2026-11-02 | lgse/strata#2030 | fix | Printed `--unlock-volume` usage errors to the terminal, joined a new item's typed name to its creation undo, and fixed qa-drive restart and aiming. |
| 2026-11-02 | lgse/strata#2027 | fix | Named remote mount roots by their percent-decoded last segment or host, so headings, breadcrumbs, tab labels, and titles stop showing "/". |
| 2026-11-02 | lgse/strata#2026 | fix | Left Menu and Shift+F10 to a focused Back button, and probed an unresponsive gvfsd before preferences load, so startup waits about 2 s. |
| 2026-11-02 | lgse/strata#2022 | refactor | Split 75 low-health files and their tests into submodules without behavior change; added `scripts/code-health.sh` and an AGENTS.md code-health rule. |
| 2026-11-01 | lgse/strata#1984 | build | Bumped rustix to 1.1.6, querying xattr sizes explicitly and exiting forked sandbox children through `libc::_exit`; no behavior change. |
| 2026-10-31 | lgse/strata#1967 | build | Added a Nix flake and package so Strata installs from source on NixOS or through Home Manager. |
| 2026-10-31 | lgse/strata#1965 | perf | Ran Rust test shards in parallel lanes on private displays, and let a delete finish around a folder kept by an open file. |
| 2026-10-25 | lgse/strata#1890 | fix | Kept an arrival over a later removal of the same name in one monitor batch, so a no-Trash Replace keeps the row. |
| 2026-10-25 | lgse/strata#1873 | fix | Logged open-target, new-tab, and Recent events with scheme, host, and path only, and sanitized their error text. |
| 2026-10-22 | lgse/strata#1807 | test | Removed the Python E2E suite, pruned 134 QA scenarios, and moved the main-thread I/O audit to the QA runner. |
| 2026-10-22 | lgse/strata#1809 | chore | Added the committed pr-review agent skill and documented it in AGENTS.md. |
| 2026-10-22 | lgse/strata#1771 | feat | Added the `qa`-feature `--qa` JSON harness with QA scenarios beside each E2E test, and the qa-scenarios, qa-drive, and qa-quality agent skills. |
| 2026-10-21 | lgse/strata#1792 | perf | Stopped re-sorting type groups on every published chunk and raised the folder listing cap to 250,000 entries. |
| 2026-10-21 | lgse/strata#1794 | docs | Corrected the theme count, default theme, 10xer exit key, and Settings paths in the README and docs so they match the app. |
| 2026-10-18 | lgse/strata#1755 | fix | Widened `st_nlink` in the legacy stat fallback so the aarch64 release builds again. |
| 2026-10-17 | lgse/strata#1737 | ci | Moved the E2E suite to a manual-dispatch workflow and split Rust tests into four shards, since E2E gated every PR. |
| 2026-10-15 | lgse/strata#1701 | test | Made the Open With and release tar test fixtures independent of the host's applications and `tar` location, for Nix builds. |
| 2026-10-15 | lgse/strata#1700 | docs | Added a hardened-configuration guide that lists optional settings shrinking the attack surface. |
| 2026-10-15 | lgse/strata#1676 | fix | Marked debug builds with a `+debug` version suffix and listed the release `install-local` first for source builds, so slow debug builds show in reports. |
| 2026-10-15 | lgse/strata#1672 | test | Added a headless scroll benchmark for Columns, List, and Icons that reports CPU per step, frame times, and idle wakeups. |
| 2026-10-14 | lgse/strata#1647 | fix | Installed cargo-watch through mise's `github:` backend with pinned SHA-512 checksums, since mise rejects its legacy minisign signature. |
| 2026-10-09 | lgse/strata#1533 | fix | Parsed GIO URIs with encoded path flags, displayed non-UTF-8 locations percent-encoded, and logged skipped listing entries. |
| 2026-09-01 | lgse/strata#131 | fix | Made the Columns size badge an opaque chip that stays visible on selected rows and hid it on rows with no size. |
| 2026-08-30 | lgse/strata#27 | fix | Removed browsed locations from default logs and redacted URI credentials from diagnostic ones. |

## Known gaps

- `Location::parent` copies a URI location's credentials into its parent location. lgse/strata#1846, lgse/strata#1873
- Up, breadcrumbs, and reveal in parent on a non-ASCII host go to a punycode parent: `mtp://Phone_%E4%B8%80%E5%8A%A0/DCIM/Camera` gives `mtp://xn--phone_-gn7iw92a/DCIM`, which GVfs does not match. lgse/strata#2072
- The location field and Properties show a non-ASCII host in punycode, such as `sftp://xn--h-bga/x` for `sftp://h%C3%A9/x`. lgse/strata#2072
- A GVfs host that fails IDNA, such as `mtp://Phone%C2%A0X/` or a long Xiaomi device name, is an invalid URI, so the device cannot open. lgse/strata#2072
- A raw UTF-8 host, such as `mtp://OnePlus_一加_Ace/`, stays raw, while GVfs spells it `%E4%B8%80%E5%8A%A0`; locations compare as text. lgse/strata#2072
- The host splice replaces the first match anywhere, so a username equal to the host's punycode form is rewritten instead of the host. lgse/strata#2072
- A camera host GVfs spells with brackets, such as `gphoto2://[usb:001,002]/`, does not parse. lgse/strata#2072
- Per-mount request lanes parse hosts with DNS rules, so devices whose host IDNA rejects share one lane per scheme. lgse/strata#2072
- An `sftp://` or `smb://` non-ASCII host keeps the form it was given, such as `h%C3%A9` or raw UTF-8, not punycode. A resolver without IDN support may fail to resolve it. lgse/strata#2072
- `crates/strata-fs/build.rs` compiles the three-file test resource bundle in every build, not only for tests. lgse/strata#2112
