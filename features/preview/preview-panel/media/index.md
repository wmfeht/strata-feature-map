---
title: Media playback
status: shipped
origin: {issue: lgse/strata#824, pr: lgse/strata#839}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [src/media.rs, src/ui/media.rs, src/ui/media/audio.rs, src/ui/media/diagnostics.rs, src/sandbox/media.rs, src/sandbox_helper/media.rs, src/ui/preview/ease_in.rs, packaging/media-runtime]
tests: [src/media/tests.rs, src/ui/media/tests.rs, src/sandbox/media/tests.rs, src/sandbox_helper/media/tests.rs, src/ui/preview/ease_in/tests.rs]
docs: [docs/preview-sandbox.md]
related: [preview/preview-panel/sandbox, preview/preview-panel/layout, preview/quick-preview, settings/preferences]
---

## Summary

The player behind audio, video, and animated GIF previews. FFmpeg decodes the original inside bubblewrap and streams validated RGBA frames and PCM to Strata, which presents them with GTK and GStreamer. Children: `preview/preview-panel/media/audio` (now-playing audio view) and `preview/preview-panel/media/video` (now-playing video view).

## Behavior

### Playback

- Previews play the whole source with no 30-second cap; files without a reported duration play to their end with seeking disabled until it is known. lgse/strata#888
- Animated GIFs play and loop instead of showing their first frame. lgse/strata#119
- Audio-only files with no video stream, such as a mono `.ogg`, play their audio instead of failing. lgse/strata#817
- Raw H.264 and HEVC elementary streams, such as a bare `.h264` file, play from the start and seek, even without the extension. lgse/strata#1346
- Video decodes at the pane's size times display scale, capped at 1280 px on either axis and never enlarged beyond the source. lgse/strata#823, lgse/strata#839
- Growing the pane restarts decoding at the current position only when the frame would grow by 8% or more; shrinking never restarts. lgse/strata#839 (unverified)
- Mute and volume are saved and apply live to every open player. lgse/strata#167, lgse/strata#839
- The volume and seek sliders show no focus border when clicked. lgse/strata#962
- In the default key map, Ctrl+Alt+Space plays or pauses, Ctrl+Alt+Left/Right seek 5 s, Ctrl+Alt+Up/Down change volume by 10%, and Ctrl+Alt+M mutes. lgse/strata#888 (unverified)

### Autoplay

- With **Autoplay media previews** off, the default, a selected media file shows paused with a play control. lgse/strata#1106
- With autoplay on, video fades its sound in over 1 s from the first frame and audio over 0.5 s; the saved volume is not changed. lgse/strata#1474
- Clips shorter than 10 s start at full volume, a muted state skips the fade, and any play, pause, seek, volume, or mute input ends it. lgse/strata#1474
- A preview hidden by a narrow window resumes playing when shown again if it was playing, whatever the autoplay setting. lgse/strata#1106

### Seeking and recovery

- An isolated seek restarts at once with the slider at the target; seeks within 200 ms coalesce to the settled position. lgse/strata#1314
- A playback stall mid-play, such as a frozen audio clock or decoder failure, restarts at the last position up to 3 consecutive times without progress, then shows the last error. lgse/strata#1314
- A video closed after more than 1 s and before its end reopens at that position in the same session. lgse/strata#1314
- On a sink whose start-up delay exceeds 130 ms, such as Bluetooth A2DP over PipeWire-Pulse, audio plays through without stalling at 0:00. lgse/strata#1411
- After a start, seek, or resume, the playhead waits for the audio sink instead of advancing and snapping back. lgse/strata#1411

### Resources and limits

- At most four media previews per process own decoders. A fifth shows "Media previews are busy (four active players). Pause or close another preview and retry." and the others keep playing. lgse/strata#839
- A player paused for 30 seconds releases its decoder and audio output but keeps its frame and position. lgse/strata#839
- Changing selection or closing the preview stops the decoder and its sandbox. lgse/strata#839, lgse/strata#765
- Malformed or truncated decoder output is rejected as a decoder failure, never shown; there is no unsandboxed fallback. lgse/strata#839

### Hardware acceleration

- With **Hardware-accelerated video previews** on and **Decoding backend** set to Automatic, decoding tries VA-API, then Vulkan, then software; a hardware attempt that fails before its first frame falls back to software. lgse/strata#45, lgse/strata#139
- With no saved choice, a system with an AMD Polaris 10, 11, or 12 GPU decodes in software; the user can still opt in. lgse/strata#139
- Software decoding receives no GPU device and no `/sys`. lgse/strata#139
- Changing the acceleration setting applies to the next preview without interrupting the current one. lgse/strata#139

## Design

[docs/preview-sandbox.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/preview-sandbox.md) ("Incremental media playback" through "Compatibility scope") carries the wire format, budgets, deadlines, and isolation policy.

- Playing the original in GTK or GStreamer, or remuxing it, was rejected because it exposes compressed media to an unsandboxed parser (lgse/strata#824).
- The first design transcoded the first 30 seconds to WebM or MP4 in the sandbox (lgse/strata#17, lgse/strata#37). Hardware encoders sped it up (lgse/strata#38, lgse/strata#45), but a Polaris VCE hang crashed a whole session (lgse/strata#127).
- Incremental decoding replaced that: no re-encode, no second decode, and a first frame in about 1 s instead of 3.3 s (lgse/strata#839).
- The `STRRAW01` wire is untrusted. The parent checks dimensions, strides, tick sequence, and payload lengths before allocating, and EOF without an end record is failure (lgse/strata#839).
- Queues are bounded: three records, three presented frames, and 66 audio blocks. Audio runs 2 s ahead inside the records so slow sinks are primed without pinning frames (lgse/strata#1411).
- Media helpers run outside the driver-wide CPU, address-space, and file-size limits; Intel Vulkan's 1 GiB object hit the inherited `RLIMIT_FSIZE` (lgse/strata#128). Per-record sizes, queue limits, and progress deadlines bound work instead.
- Each FFmpeg process disables core dumps and caps files and single allocations at 512 MiB. Software decoders also get a 2 GiB address-space limit; hardware decoders are exempt because drivers reserve large virtual ranges (docs/preview-sandbox.md, "Isolation and hardware policy").
- Polaris defaults to software because explicit VA-API still hung after 16-pixel alignment; the hang is in VCE encode, not the file (lgse/strata#127).
- Raw elementary streams have no timestamps, so any input `-ss` drops every frame. Their positive seeks use output-side `-ss`, which decodes and discards the prefix (lgse/strata#1346). Detection uses the probed demuxer, never the extension (lgse/strata#1333).
- The autoplay fade multiplies a gain on the GStreamer `volume` element, so no audio is processed in Strata and the saved volume is untouched (lgse/strata#1417).
- The `packaging/media-runtime` patch kit pins a GStreamer worker-finalization fix and probes. It does not change the shipped binary (lgse/strata#779). The GTK context patch was retired once upstream merged it (lgse/strata#830).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-04 | lgse/strata#1411 | fix | Fed audio by sink capacity with a 2 s lead so slow-starting sinks no longer stall. |
| 2026-10-01 | lgse/strata#1346 | fix | Omitted input seeks for raw H.264 and HEVC streams so they play and seek. |
| 2026-09-29 | lgse/strata#1314 | feat | Recovered stalled playback, coalesced seeks, and resumed videos at their close position. |
| 2026-09-18 | lgse/strata#1106 | feat | Added an autoplay preference, off by default. |
| 2026-09-14 | lgse/strata#962 | fix | Removed the focus border from the volume and seek sliders. |
| 2026-09-12 | lgse/strata#839 | perf | Replaced clip transcoding with incremental sandboxed decoding of raw frames and PCM. |
| 2026-09-11 | lgse/strata#830 | chore | Removed the local GTK context patch after the upstream fix merged. |
| 2026-09-11 | lgse/strata#823 | perf | Fitted video conversion to the pane and preferred fast software H.264. |
| 2026-09-11 | lgse/strata#817 | fix | Normalized audio-only files that have no video stream. |
| 2026-09-10 | lgse/strata#787 | build | Added the private-runtime patch kit for GTK and GStreamer lifetime fixes. |
| 2026-09-10 | lgse/strata#765 | fix | Released the media pipeline when preview content is replaced or closed. |
| 2026-09-03 | lgse/strata#139 | fix | Added acceleration settings and defaulted AMD Polaris GPUs to software. |
| 2026-09-03 | lgse/strata#167 | feat | Replaced GTK's media controls with themed controls and saved mute and volume. |
| 2026-09-01 | lgse/strata#119 | fix | Played GIFs through bounded streamed output and exempted media from driver-wide limits. |
| 2026-08-31 | lgse/strata#45 | perf | Added VA-API and Vulkan acceleration ahead of the software fallback. |
| 2026-08-31 | lgse/strata#37 | fix | Exempted video previews from the CPU-time limit so high-resolution files finish. |

## Known gaps

- Arrow and Page keys do not step the volume or seek sliders; the fix is unmerged. lgse/strata#1451, lgse/strata#1546
- Application RSS grows across preview cycles through glibc arena retention; reusable parent-side workers are under investigation. lgse/strata#841
