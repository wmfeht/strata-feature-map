---
title: Thumbnail workers
status: shipped
origin: {issue: lgse/strata#516, pr: lgse/strata#1081}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: reviewed
code: [src/sandbox/browser.rs, src/sandbox/browser/worker.rs, src/sandbox/browser/wire.rs, src/sandbox/browser/process.rs, src/ui/thumbnail/background.rs]
tests: [src/sandbox/browser/tests.rs, src/ui/thumbnail/background/tests.rs, tests/e2e/scenarios/test_browser_workers.py, tests/e2e/scenarios/test_thumbnail_worker_settings.py]
docs: [docs/preferences.md]
related: [preview/preview-panel/sandbox, settings/preferences]
---

## Summary

The process-wide pool of reusable sandboxed decoders that renders browser thumbnails and media details, and the Thumbnail workers setting that sizes it. Columns, List, and Icons in every window share the pool.

## Behavior

### Thumbnail workers setting

- Settings → General → Performance has a Thumbnail workers −/+ stepper with a range of 1 to 16. lgse/strata#1081
- Typing "thumbnail workers" in Search settings reveals the control. lgse/strata#1081 (unverified)
- Each −/+ click saves `thumbnail_workers` and applies to every window without a restart or interrupting running jobs. lgse/strata#1081
- At 16, Increase thumbnail workers is insensitive; at 1, Decrease thumbnail workers is insensitive. lgse/strata#1081 (unverified)
- The number between − and + shows the count; clicking it, described as "Reset thumbnail workers", restores the default. lgse/strata#1081
- The default is the CPU count capped at 4, or 2 when detection fails. lgse/strata#1081
- With no saved count, `STRATA_THUMBNAIL_WORKERS` sets the default and the reset value; an invalid value falls back to the CPU default. lgse/strata#1081
- Lowering the count lets busy jobs finish, then retires idle workers above the new limit. lgse/strata#1081
- The count also caps the separate pool that renders image and document previews. lgse/strata#1222 (unverified)

### Worker lifecycle

- No worker starts until the first thumbnail misses both caches. lgse/strata#1081
- Navigating between folders, view modes, and windows reuses running workers; no more than the configured count start. lgse/strata#1081
- A worker idle for 60 seconds exits, and the next uncached thumbnail starts a new one. lgse/strata#1081
- `STRATA_THUMBNAIL_IDLE_SECONDS` sets the idle timeout at startup, capped at 86,400; zero or invalid values use 60. lgse/strata#1081
- When a worker is killed, the next request starts one replacement and thumbnails continue. lgse/strata#1081
- Without Landlock ABI 3, each thumbnail runs in a one-shot sandbox and Strata logs "Landlock ABI 3 unavailable; retaining one-shot sandboxes". lgse/strata#1081
- CBZ, CBR, and EPUB cover thumbnails skip the pool and always run in a one-shot sandbox. lgse/strata#1325 (unverified)

### Admission

- RAW, PDF, video, and 3D-model thumbnails and media-detail probes together occupy at most one fewer worker than the limit, minimum 1. lgse/strata#1081
- At most one media-detail probe runs at a time, and it gets a turn after every four thumbnail admissions while both wait. lgse/strata#1081
- A file that changes while it is decoded gets no thumbnail from that run. lgse/strata#1081 (unverified)

## Design

[docs/preview-sandbox.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/preview-sandbox.md#browser-worker-pool) describes the pool and its isolation; [docs/preferences.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/preferences.md#thumbnail-workers) the setting.

Every cache miss used to exec a new bubblewrap sandbox. Process startup, not decoding, dominated thumbnail latency (lgse/strata#516). The pool keeps decoding sandboxed and removes the per-file exec (lgse/strata#1081).

- A persistent bubblewrap supervisor runs only the control protocol and never reads media. Each job forks a disposable decoder in fresh namespaces, with Landlock, seccomp, and per-job limits (lgse/strata#1081).
- The main process opens each source read-only and passes the descriptor. Results return on a per-job pipe, so the supervisor never buffers decoded bytes.
- A launcher thread spawns every supervisor, because bubblewrap's parent-death signal follows the spawning thread, and short-lived threads must not own it (lgse/strata#1081).
- Retirement waits on the next expiry on that thread, with no polling timer. Idle retirement frees sandbox memory, not the thumbnail caches.
- Decoding untrusted files in-process and delegating to Tumbler were rejected (lgse/strata#516).
- Results are cached for 30 seconds, keyed by path, device, inode, size, nanosecond modification and change times, and operation, so a 256 px thumbnail cannot satisfy a larger preview (lgse/strata#1222).
- Space previews use a second pool so a scrolled folder's thumbnails cannot delay them (lgse/strata#516, lgse/strata#1222). Supervisor isolation itself belongs to `preview/preview-panel/sandbox`.

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-18 | lgse/strata#1081 | perf | Replaced per-file sandboxes with a reusable worker pool and added the Thumbnail workers setting. |

## Known gaps

None known.
