---
title: Preview sandbox
status: shipped
origin: {issue: lgse/strata#6, pr: lgse/strata#17}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: reviewed
code: [src/sandbox.rs, src/sandbox_helper.rs]
tests: [src/sandbox/tests.rs, src/sandbox_helper/tests.rs, src/trusted_command/tests.rs]
docs: [docs/preview-sandbox.md]
related: [preview/preview-panel/media, preview/preview-panel/documents, browser/thumbnails/workers, operations/archives]
---

## Summary

The bubblewrap boundary that keeps native parsing of browsed files out of the Strata process. Image, RAW, PDF, SVG, and document-media renders run in resource-limited helpers that return only validated, bounded PNG or metadata.

## Behavior

### Launching the sandbox

- Strata runs `bwrap` only from `/run/wrappers/bin`, `/usr/bin`, `/usr/sbin`, `/bin`, `/sbin`, or the NixOS and Guix system profiles, never from `PATH`. lgse/strata#1055
- A search hit whose canonical target lies outside FHS, `/run/wrappers/bin`, `/nix/store`, or `/gnu/store` is rejected, and previews fail closed. lgse/strata#1055
- When bubblewrap is missing or cannot start, a native-format preview shows "Preview unavailable" and the file is never decoded outside the sandbox. lgse/strata#17, lgse/strata#1503
- Builds compiled with `STRATA_SANDBOX_PATH`, `STRATA_SANDBOX_ROOT`, `STRATA_SANDBOX_PRLIMIT`, or `STRATA_SANDBOX_GDK_PIXBUF_MODULE_FILE` use those paths inside the sandbox; setting them at launch has no effect. lgse/strata#1357
- Without those build variables, helpers run with `PATH=/usr/bin`, a read-only `/usr`, and `/usr/bin/prlimit`. lgse/strata#1357

### Isolation and limits

- A helper sees one read-only input file, a private output directory, a 512 MiB private `/tmp`, a cleared environment with `HOME=/nonexistent`, and no network, session bus, or display. lgse/strata#17
- Image, RAW, and PDF helpers run under a 2 GiB address-space limit, a 10-second CPU limit, a 512 MiB file-size limit, and a 12-second wall deadline. lgse/strata#17, lgse/strata#45, lgse/strata#55
- An image, RAW, or PDF preview input over 512 MiB fails with "Preview input exceeds the supported size limit" before any renderer starts. lgse/strata#17 (unverified)
- Changing selection or closing the preview kills the helper's whole process tree. lgse/strata#17
- An image or PDF helper receives no GPU device and no `/sys` mount. lgse/strata#17, lgse/strata#45

### Decoding

- A 12 MP phone JPEG previews and thumbnails without the decoder being killed by `SIGXFSZ`. lgse/strata#55
- An ICC-profiled JPEG on a 64-thread host previews without the helper aborting; image helpers run with `MALLOC_ARENA_MAX=1`. lgse/strata#143
- The input keeps a sanitized extension of 1 to 8 ASCII alphanumerics, such as `/input.ARW`, so Sony ARW files render; other names become `/input`. lgse/strata#166
- A RAW preview that GDK Pixbuf cannot decode falls back to ImageMagick, then to the embedded camera JPEG via `dcraw` or `simple_dcraw`. lgse/strata#166
- An image over the decoded-frame budget (about 134 MP RGBA) renders its embedded EXIF thumbnail when it has one, and otherwise fails without killing any process. lgse/strata#1277
- SVG and gzip-compressed SVGZ files render with resvg inside the sandbox, detected by content rather than by name, with image references disabled. lgse/strata#1222

### Output validation

- An image renderer output that is a symlink, FIFO, directory, empty file, or over 32 MiB is rejected; a symlinked `result.meta` falls back to page `(0, 0)`. lgse/strata#669
- An image renderer must return a PNG within the operation's bounds, 800×800 for a still preview and 256×256 for a thumbnail; other output is rejected. lgse/strata#17 (unverified)

### Pooled preview worker

- Still-image previews, Markdown images, Mermaid diagrams, and equations run on a preview pool separate from the thumbnail pool, so a thumbnail backlog does not delay a Space preview. lgse/strata#1222
- With Landlock ABI 3, an image preview within 60 seconds of the previous one reuses its supervisor rather than starting another bubblewrap. lgse/strata#1222
- A preview render is never served from a cached 256-pixel thumbnail of the same file. lgse/strata#1222

## Design

[docs/preview-sandbox.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/preview-sandbox.md) is the maintained contract: providers, isolation, limits, packaging variables, and the worker pools.

- Files become visible by browsing, so any parser reachable from a listing is attacker-facing. Parsing moves out of process, and crashes or timeouts degrade to a fallback icon or message (lgse/strata#6).
- There is no unsandboxed fallback. A hijacked `bwrap` would silently reintroduce one, so host helpers are resolved by trusted absolute path and never through `PATH` (lgse/strata#1045, lgse/strata#1055).
- `RLIMIT_FSIZE` is process-wide and also covers glycin's memfd for the full decoded frame. It was raised to 512 MiB; the address-space limit is the memory guard, and output size is checked host-side (lgse/strata#54, lgse/strata#55).
- glibc creates up to 8 arenas per CPU, which can exhaust the 2 GiB address space on many-core hosts. One arena keeps the limit intact; media helpers are excluded because they have no address-space limit (lgse/strata#141, lgse/strata#143).
- ImageMagick sniffs TIFF magic and picks its TIFF coder for ARW unless the name keeps `.ARW`, so the extension is preserved, sanitized (lgse/strata#165).
- Oversized images are refused from header dimensions before decoding, rather than ignoring `SIGXFSZ`, so no sandboxed process is killed (lgse/strata#1202, lgse/strata#1277).
- The renderer can write its own output directory, so the parent opens outputs with `O_NOFOLLOW`, checks the descriptor is a regular file, and reads at most the limit plus one byte (lgse/strata#653).
- Build-time variables replace `/usr` rather than adding mounts, so Nix and Guix packages need no source patches. Binding `/` or a user tree was rejected because it exposes private files (lgse/strata#1329).
- The preview pool reuses only the supervisor; each job still runs in a freshly forked decoder with Landlock and seccomp. This removed about 100 ms of spawn cost per SVG preview (lgse/strata#1222).
- The `fchmodat2` denylist entry uses syscall number 452 directly, because libc omits the constant on aarch64 (lgse/strata#1111).
- The supervisor pool implementation, its sizing, and its Landlock fallback belong to `browser/thumbnails/workers`; media playback isolation belongs to `preview/preview-panel/media`.

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-01 | lgse/strata#1357 | fix | Embedded optional build-time sandbox paths for non-FHS distributions. |
| 2026-09-26 | lgse/strata#1277 | fix | Fell back to EXIF thumbnails for images over the decoded-frame budget instead of letting `SIGXFSZ` kill decoders. |
| 2026-09-25 | lgse/strata#1222 | perf | Rendered SVG with resvg and served previews and document media from a pooled sandbox worker. |
| 2026-09-18 | lgse/strata#1111 | fix | Used the raw `fchmodat2` syscall number so ARM64 release builds compile. |
| 2026-09-18 | lgse/strata#1055 | fix | Resolved `bwrap` and other host helpers under trusted roots without `PATH`. |
| 2026-09-09 | lgse/strata#669 | fix | Rejected symlinked and non-regular renderer outputs. |
| 2026-09-02 | lgse/strata#166 | fix | Kept a sanitized input extension and added RAW fallbacks so Sony ARW files decode. |
| 2026-09-01 | lgse/strata#143 | fix | Limited image helpers to one malloc arena so glycin threads fit the address-space limit. |
| 2026-08-31 | lgse/strata#55 | fix | Raised the file-size limit to 512 MiB so decoders can hold a full-resolution frame. |
| 2026-08-30 | lgse/strata#17 | feat | Moved image, RAW, PDF, and media parsing into short-lived bubblewrap helpers. |

## Known gaps

- Inside Flatpak, bubblewrap cannot create namespaces, so native-format previews and thumbnails show "Preview unavailable". lgse/strata#1503, lgse/strata#936
