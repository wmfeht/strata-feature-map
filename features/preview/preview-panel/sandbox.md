---
title: Preview sandbox
status: shipped
origin: {issue: lgse/strata#6, pr: lgse/strata#17}
branch: null
reviewed_at: 86df474dc0e8352e0e2098637a017cc4c77a8c44
review: draft
code: [src/sandbox.rs, src/sandbox_helper.rs, src/sandbox/runtime.rs]
tests: [src/sandbox/tests.rs, src/sandbox_helper/tests.rs, src/sandbox/runtime/tests.rs]
docs: [site/src/reference/preview-sandbox.md, docs/preview-sandbox.md]
related: [preview/preview-panel/media, preview/preview-panel/model-views, preview/preview-panel/documents, browser/thumbnails/workers, operations/archives, app/infrastructure]
---

## Summary

The bubblewrap boundary that keeps native parsing of browsed files out of the Strata process. Image, RAW, PDF, SVG, and document-media renders run in resource-limited helpers that return only validated, bounded PNG or metadata.

## Behavior

### Launching the sandbox

- Strata runs `bwrap` only from `/run/wrappers/bin`, `/usr/bin`, `/usr/sbin`, `/bin`, `/sbin`, the NixOS and Guix system profiles, or build-time `STRATA_TRUSTED_COMMAND_PATH` directories, never from `PATH`. lgse/strata#1055, lgse/strata#1746
- A build with `STRATA_TRUSTED_COMMAND_PATH=/nix/store/<bwrap>/bin` and no system bubblewrap finds `bwrap` there, and native previews render. lgse/strata#1746, lgse/strata#1702
- A search hit whose canonical target lies outside FHS, `/run/wrappers/bin`, `/nix/store`, or `/gnu/store` is rejected, and previews fail closed. lgse/strata#1055
- When bubblewrap is missing or cannot start, a native-format preview shows "Preview unavailable" and the file is never decoded outside the sandbox. lgse/strata#17, lgse/strata#1503
- `STRATA_SANDBOX_PATH`, `STRATA_SANDBOX_ROOT`, `STRATA_SANDBOX_PRLIMIT`, and `STRATA_SANDBOX_GDK_PIXBUF_MODULE_FILE` set at launch override the values embedded at build time. lgse/strata#1357, lgse/strata#1746, lgse/strata#1599
- Without launch or build values, helpers run with `PATH=/usr/bin`, a read-only `/usr`, and `/usr/bin/prlimit`. lgse/strata#1357, lgse/strata#1746
- A launch-time `STRATA_SANDBOX_ROOT` must be `/usr`, `/nix/store`, `/gnu/store`, or a path inside one; `/`, `/home/<user>`, `/usrdata`, and `/usr/../home` are ignored. lgse/strata#1746
- A launch-time path that is relative or contains `..` is ignored; `.` components are accepted. lgse/strata#1746
- A launch-time `STRATA_SANDBOX_PATH` that is empty or has an empty or relative entry, such as `/usr/bin:`, is ignored whole. lgse/strata#1746 (unverified)
- An ignored launch-time value logs the warning "ignoring an invalid launch-time sandbox override", and the embedded or default value applies, so previews keep working. lgse/strata#1746
- A launch-time value that is not valid UTF-8 logs "ignoring a launch-time sandbox override that is not valid UTF-8" and is ignored. lgse/strata#1746 (unverified)
- Launch-time values are read once per process; changing them takes effect after a restart. lgse/strata#1746

### Isolation and limits

- A helper sees one read-only input file, a private output directory, a 512 MiB private `/tmp`, a cleared environment with `HOME=/nonexistent`, and no network, session bus, or display. lgse/strata#17
- Image, RAW, and PDF helpers run under a 2 GiB address-space limit, a 10-second CPU limit, a 512 MiB file-size limit, and a 12-second wall deadline. lgse/strata#17, lgse/strata#45, lgse/strata#55
- An image, RAW, or PDF preview input over 512 MiB fails with "Preview input exceeds the supported size limit" before any renderer starts. lgse/strata#17 (unverified)
- A DOCX, ODT, or OTT preview input over 20 MiB fails with "Preview input exceeds the supported size limit" before the helper starts. lgse/strata#1086, lgse/strata#1834 (unverified)
- A DOCX or ODT the helper cannot read, such as a ZIP without `content.xml` named `.odt`, fails with "The sandboxed preview renderer failed". lgse/strata#1834 (unverified)
- A route file over 32 MiB fails with "This route file exceeds the 32 MiB preview limit." before the helper starts. lgse/strata#1842
- A G-code file over 128 MiB is not refused by size; STL, 3MF, and FreeCAD inputs keep the 128 MiB model limit. lgse/strata#1864
- A PDF that needs an opening password fails with "This PDF is password protected." lgse/strata#1840
- A PDF that opens without a password, such as `owner-restricted.pdf` with an empty user password, previews normally. lgse/strata#1840
- A damaged PDF keeps "The sandboxed preview renderer failed", even when its text reads "This PDF is password protected." lgse/strata#1840
- Changing selection or closing the preview kills the helper's whole process tree. lgse/strata#17
- After `bwrap` exits, killed or not, Strata waits on a pidfd, at most 1 s, until the sandbox's namespace releases the input file. lgse/strata#1729
- An image or PDF helper receives no GPU device and no `/sys` mount. lgse/strata#17, lgse/strata#45

### Decoding

- A 12 MP phone JPEG previews and thumbnails without the decoder being killed by `SIGXFSZ`. lgse/strata#55
- An ICC-profiled JPEG on a 64-thread host previews without the helper aborting; image helpers run with `MALLOC_ARENA_MAX=1`. lgse/strata#143
- The input keeps a sanitized extension of 1 to 8 ASCII alphanumerics, such as `/input.ARW`, so Sony ARW files render; other names become `/input`. lgse/strata#166
- A RAW preview renders the embedded camera JPEG via `dcraw` or `simple_dcraw` first, then tries GDK Pixbuf, then ImageMagick. lgse/strata#1698
- A Fuji `.RAF`, including lossless compressed X-T5 files, previews from its embedded JPEG instead of timing out. lgse/strata#1698, lgse/strata#1666
- When GDK Pixbuf sees a RAW image under 800 px, such as a DNG's 160×120 IFD0 thumbnail, previews try ImageMagick before it. lgse/strata#1698
- RAW thumbnails keep the order embedded JPEG, GDK Pixbuf, then ImageMagick; ImageMagick runs only when both earlier steps fail. lgse/strata#1698
- A portrait RAW whose embedded JPEG carries an EXIF orientation previews and thumbnails upright. lgse/strata#1698
- On Debian-family systems where `/usr/bin/magick` and `/usr/bin/convert` link through `/etc/alternatives`, the ImageMagick fallback runs inside the sandbox. lgse/strata#1657
- From `/etc/alternatives`, the sandbox binds only `magick`, `convert`, and BLAS and LAPACK links for media operations, never the whole directory. lgse/strata#1657, lgse/strata#984
- It also binds nine `glx--<library>-<triplet>` GL dispatch links, such as `glx--libGL.so.1-x86_64-linux-gnu`, for x86-64 and ARM64. lgse/strata#1660
- On Debian testing with GDK Pixbuf 2.44, glycin, and ImageMagick installed, JPEG previews render instead of staying empty. lgse/strata#1656, lgse/strata#1657, lgse/strata#1660
- On a Debian-family host whose `libGL.so.1` links through `/etc/alternatives/glx--*`, helpers start: PNG, PDF, and MP4 previews and thumbnails render. lgse/strata#1658, lgse/strata#1660
- On Debian 13 with ImageMagick installed, HEIC previews render through ImageMagick instead of staying empty. lgse/strata#1656, lgse/strata#1657
- An image over the decoded-frame budget (about 134 MP RGBA) uses its EXIF thumbnail when that covers the request. lgse/strata#1277, lgse/strata#1698
- The thumbnail covers the request when its long edge reaches 256 px for a thumbnail or 800 px for a preview. lgse/strata#1698
- An oversized JPEG without such a thumbnail renders through an ImageMagick reduced-scale decode; a 42374×10529 panorama previews at 800×199. lgse/strata#1698
- When that reduced decode fails or ImageMagick is missing, the smaller EXIF thumbnail shows; with none, the render fails without killing any process. lgse/strata#1277, lgse/strata#1698
- An oversized non-JPEG image gets no reduced decode: it shows its EXIF thumbnail at any size or fails. lgse/strata#1698 (unverified)
- Every ImageMagick render runs with `-limit area` at the decoded-frame budget, `-limit disk 0`, and a `jpeg:size` hint. lgse/strata#1698
- Under those limits, a full-size ImageMagick decode of an oversized image fails fast instead of filling the sandbox. lgse/strata#1698
- SVG and gzip-compressed SVGZ files render with resvg inside the sandbox, detected by content rather than by name, with image references disabled. lgse/strata#1222

### Output validation

- An image renderer output that is a symlink, FIFO, directory, empty file, or over 32 MiB is rejected; a symlinked `result.meta` falls back to page `(0, 0)`. lgse/strata#669
- An image renderer must return a PNG within the operation's bounds: 800×800 for a still or RAW preview, 256×256 for a thumbnail. Other output is rejected. lgse/strata#17, lgse/strata#1698 (unverified)

### Private output folders

- The first sandbox output folder a process creates starts a background sweep of the temp directory; that render does not wait for it. lgse/strata#1866
- The sweep removes `strata-preview-<pid>-<n>` folders that the user owns and no running Strata holds, such as those left by `kill -9`. lgse/strata#1866
- It keeps folders a running Strata holds, including one in another pid namespace that shares `/tmp`, such as toolbox or distrobox. lgse/strata#1866
- It keeps files, symlinks, other users' folders, and names other than `strata-preview-<digits>-<digits>`. lgse/strata#1866
- A new output folder skips a leftover folder with the same name instead of failing the preview. lgse/strata#1866

### Pooled preview worker

- Still-image previews, Markdown images, Mermaid diagrams, and equations run on a preview pool separate from the thumbnail pool, so a thumbnail backlog does not delay a Space preview. lgse/strata#1222
- With Landlock ABI 3, an image preview within 60 seconds of the previous one reuses its supervisor rather than starting another bubblewrap. lgse/strata#1222
- A preview render is never served from a cached 256-pixel thumbnail of the same file. lgse/strata#1222

## Design

[docs/preview-sandbox.md](https://github.com/lgse/strata/blob/d6c74746cdb27e506a08e8cdefa3bc8cef7d10f9/docs/preview-sandbox.md) is the maintained contract: providers, isolation, limits, packaging variables, and the worker pools.

- Files become visible by browsing, so any parser reachable from a listing is attacker-facing. Parsing moves out of process, and crashes or timeouts degrade to a fallback icon or message (lgse/strata#6).
- There is no unsandboxed fallback. A hijacked `bwrap` would silently reintroduce one, so host helpers are resolved by trusted absolute path and never through `PATH` (lgse/strata#1045, lgse/strata#1055).
- Packagers may add helper directories at build time, searched after the fixed roots so NixOS wrappers still win. Each directory and each helper target must canonicalize under a trust root, so a build cannot embed a user-writable location. Searching inherited `PATH` was rejected (lgse/strata#1702, lgse/strata#1746).
- `RLIMIT_FSIZE` is process-wide and also covers glycin's memfd for the full decoded frame. It was raised to 512 MiB; the address-space limit is the memory guard, and output size is checked host-side (lgse/strata#54, lgse/strata#55).
- glibc creates up to 8 arenas per CPU, which can exhaust the 2 GiB address space on many-core hosts. One arena keeps the limit intact; media helpers are excluded because they have no address-space limit (lgse/strata#141, lgse/strata#143).
- ImageMagick sniffs TIFF magic and picks its TIFF coder for ARW unless the name keeps `.ARW`, so the extension is preserved, sanitized (lgse/strata#165).
- Oversized images are refused from header dimensions before decoding, rather than ignoring `SIGXFSZ`, so no sandboxed process is killed (lgse/strata#1202, lgse/strata#1277).
- The renderer can write its own output directory, so the parent opens outputs with `O_NOFOLLOW`, checks the descriptor is a regular file, and reads at most the limit plus one byte (lgse/strata#653).
- Debian's ImageMagick commands are `update-alternatives` links that dangled inside the sandbox. Only the two links are bound, mirroring the individual BLAS and LAPACK binds of lgse/strata#984, not all of `/etc/alternatives` (lgse/strata#1656, lgse/strata#1657). Debian's `glx--*` GL dispatch links follow the same rule. They are bound in every sandbox, not only media ones, because the helper binary itself links `libGL.so.1` (lgse/strata#1658, lgse/strata#1660).
- Build-time variables replace `/usr` rather than adding mounts, so Nix and Guix packages need no source patches. Binding `/` or a user tree was rejected because it exposes private files (lgse/strata#1329).
- Launch-time overrides let prebuilt releases run without a rebuild. They are less trusted than a packager's values, so the root is limited to admin-managed trees. An invalid value falls back rather than disabling previews (lgse/strata#1599, lgse/strata#1746).
- A RAF preview timed out because nothing read the container. ImageMagick demosaiced the 40 MP sensor data in about 20 s, against the 12 s wall limit. Previews now take the embedded JPEG first (lgse/strata#1666, lgse/strata#1698).
- Previews promote ImageMagick only when GDK Pixbuf sees a thumbnail-sized image. Thumbnails keep the cheaper order, because ImageMagick would demosaic every RAW in a folder (lgse/strata#1698).
- libjpeg decodes at 1/2, 1/4, or 1/8 scale from compressed data. The `jpeg:size` hint makes ImageMagick use it, so oversized JPEGs fit the budget. The area limit stops any unhinted full decode (lgse/strata#1698).
- The preview pool reuses only the supervisor; each job still runs in a freshly forked decoder with Landlock and seccomp. This removed about 100 ms of spawn cost per SVG preview (lgse/strata#1222).
- Format crosses the sandbox boundary explicitly, including for symlinks (lgse/strata#1276). Document previews pass `docx` or `odt` to the helper the way comic covers pass their format (lgse/strata#1834).
- The PDF helper detects protection from Poppler's typed `Encrypted` error, not message text or file names. It writes a structured code to the existing bounded `result.error` output (lgse/strata#1636, lgse/strata#1840).
- Output folders outlived their process: the browser pools are statics; the media, peaks, storyboard, and model workers detach; and a killed process runs no `Drop` (lgse/strata#1847, lgse/strata#1866).
- Each output folder holds an exclusive `flock`, and the sweep removes only folders it can lock. A pid-based sweep was replaced: it deleted live folders in other pid namespaces, and a recycled pid kept an orphan whose name failed a later preview (lgse/strata#1866).
- The `fchmodat2` denylist entry uses syscall number 452 directly, because libc omits the constant on aarch64 (lgse/strata#1111).
- With bubblewrap 0.12.0 the sandbox's namespace, and its bind of the user's file, outlived `bwrap` after nearly every exit. On NFS, SMB, and FUSE that left hidden leftovers and blocked folder deletes. The wait costs about 2 ms after a kill and 0.1 ms after a normal exit (lgse/strata#1729).
- `bwrap` reports the namespace init's pid through `--info-fd` on stderr, which every sandbox already discarded (lgse/strata#1729).
- The supervisor pool implementation, its sizing, and its Landlock fallback belong to `browser/thumbnails/workers`; media playback isolation belongs to `preview/preview-panel/media`.

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-25 | lgse/strata#1866 | fix | Swept orphaned preview output folders by lock on a process's first sandbox job, so leftovers from exited or killed runs stop piling up in the temp directory. |
| 2026-10-18 | lgse/strata#1746 | feat | Added build-time trusted helper directories and launch-time sandbox paths, so prebuilt releases run the sandbox without a rebuild and Nix packages need no source patch. |
| 2026-10-16 | lgse/strata#1698 | fix | Rendered RAW previews from the embedded camera JPEG and reduced-decoded oversized JPEGs, so RAF previews no longer time out and DNG previews fill the pane. |
| 2026-10-14 | lgse/strata#1660 | fix | Bound Debian's `glx--*` GL dispatch links so helpers start, and let glycin decode inside pooled workers. |
| 2026-10-14 | lgse/strata#1657 | fix | Bound Debian's ImageMagick alternatives links so the ImageMagick fallback runs inside the sandbox. |
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
- Output folders still owned at exit are not removed then; the next process that creates one sweeps them. lgse/strata#1866
