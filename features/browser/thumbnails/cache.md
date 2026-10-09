---
title: Thumbnail disk cache
status: shipped
origin: {issue: lgse/strata#273, pr: lgse/strata#274}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [src/ui/thumbnail_cache.rs]
tests: [src/ui/thumbnail_cache/tests.rs]
related: []
---

## Summary

Persisting rendered thumbnails in the freedesktop shared cache, `$XDG_CACHE_HOME/thumbnails/large`, and reading them back on later visits. Strata reads entries written by other spec-following applications and treats every cached byte as untrusted.

## Behavior

- After rendering a local file with a known modification time, Strata writes `thumbnails/large/<MD5 of the file URI>.png` under `$XDG_CACHE_HOME`, or `$HOME/.cache` when it is unset or empty. lgse/strata#274
- The stored PNG has a 256 px long edge and `Thumb::URI` and `Thumb::MTime` tags, whatever icon size the view used. lgse/strata#274
- After a restart, revisiting a folder shows thumbnails from the disk cache without rendering the files again. lgse/strata#274
- An entry written by another application is used when its `Thumb::URI` and `Thumb::MTime` match the file. lgse/strata#274 (unverified)
- An entry whose `Thumb::URI` or `Thumb::MTime` differs from the file's URI or modification time is ignored and the file is rendered again. lgse/strata#274 (unverified)
- An entry that is a symlink, a FIFO, larger than 2 MiB, not a PNG, zero-sized, or wider or taller than 512 px is treated as a miss. lgse/strata#274 (unverified)
- Failed renders are never written to the disk cache. lgse/strata#274 (unverified)
- Files on a gphoto2 camera are neither looked up in nor written to the disk cache. lgse/strata#274 (unverified)
- Strata creates the `large` directory with mode 0700, and resets an existing directory to 0700 before writing. lgse/strata#274 (unverified)
- Entries are written atomically with mode 0600; a symlink at the entry path is left in place and its target is not modified. lgse/strata#274 (unverified)
- Rendering an image, or page 1 of a PDF, in the preview panel also writes the 256 px entry for a local file. lgse/strata#318 (unverified)

## Design

The cache follows the freedesktop thumbnail specification so Strata and other file managers share work (lgse/strata#273). Cache keys use GLib's MD5 of the URI; MD5's weakness does not matter for a file name (lgse/strata#274).

- Entries are untrusted: they are opened without following symlinks and bounded in size and dimensions before allocation. Every hit revalidates the URI and modification-time tags.
- Writes are normalized to the canonical `large` size so a small view cannot poison the shared bucket. Only files with a known modification time touch the disk.
- Persistence is best effort and asynchronous. At most 32 writes queue; the oldest drops first, so slow disks never delay display.
- Disk lookups run on their own executor rather than in a render slot, so a cache hit never waits behind a decoder (lgse/strata#516, lgse/strata#1081).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-04 | lgse/strata#274 | perf | Read and wrote the freedesktop `large` cache, hardened against hostile entries and normalized to 256 px. |

## Known gaps

None known.
