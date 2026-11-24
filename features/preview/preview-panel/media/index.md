---
title: Media playback
status: shipped
origin: {issue: lgse/strata#824, pr: lgse/strata#839}
branch: null
reviewed_at: ed544cf3bbb3968299ed8223148a65823739d48f
review: draft
code: [crates/strata-preview/src/media.rs, src/ui/media.rs, src/ui/media/audio.rs, src/ui/media/diagnostics.rs, crates/strata-preview/src/sandbox/media.rs, crates/strata-preview/src/sandbox_helper/media.rs, src/ui/preview/ease_in.rs, src/ui/media/history.rs, src/ui/media/playback.rs, src/ui/media/positions.rs, src/ui/preview/media_content.rs, src/ui/preview/media_controls.rs, src/ui/preview/media_render.rs, src/ui/preview/media_session.rs, crates/strata-preview/src/services/webp_animation.rs, crates/strata-preview/src/sandbox/decoders.rs, packaging/media-runtime]
tests: [crates/strata-preview/src/media/tests.rs, src/ui/media/tests.rs, crates/strata-preview/src/sandbox/media/tests.rs, crates/strata-preview/src/sandbox/media/fixtures.rs, crates/strata-preview/src/sandbox_helper/media/**, src/ui/preview/ease_in/tests.rs, src/ui/preview/tests/media_controls.rs, crates/strata-preview/src/services/webp_animation/tests.rs, crates/strata-preview/src/sandbox/decoders/tests.rs]
docs: [site/src/reference/preview-sandbox.md, site/src/reference/keyboard-navigation.md]
related: [preview/preview-panel/sandbox, preview/preview-panel/layout, preview/quick-preview, settings/preferences]
---

## Summary

The player behind audio, video, animated GIF, and animated WebP previews. FFmpeg decodes the original inside bubblewrap and streams validated RGBA frames and PCM to Strata, which presents them with GTK and GStreamer. Children: `preview/preview-panel/media/audio` (now-playing audio view) and `preview/preview-panel/media/video` (now-playing video view).

## Behavior

### Playback

- Previews play the whole source with no 30-second cap; files without a reported duration play to their end with seeking disabled until it is known. lgse/strata#888
- Animated GIFs play and loop instead of showing their first frame. lgse/strata#119
- An animated WebP in the player plays and loops with only a Play/Pause control, no seek bar or volume. lgse/strata#2734
- An animated WebP under 30 s whose frames × width × height × 4 fit 256 MiB loops without restarting the decoder. A larger one plays once. lgse/strata#2734
- Pausing an animated WebP and playing it, or selecting another file and coming back, resumes in phase. lgse/strata#2734
- An animated WebP with over 32,767 frames, zero-length frame durations, or a truncated frame header plays to its end, like a file without a reported duration. lgse/strata#2734 (unverified)
- With FFmpeg 9.1, video and audio playback, waveforms, storyboards, and embedded cover art decode instead of showing "Preview unavailable: The file is truncated or damaged". lgse/strata#2696
- Audio-only files with no video stream, such as a mono `.ogg`, play their audio instead of failing. lgse/strata#817
- Raw H.264 and HEVC elementary streams that reach the player, such as a bare `.h264` file, play from the start and seek. lgse/strata#1346, lgse/strata#1861
- The player detects a raw stream from its probed format, not its file name, so a renamed copy still seeks. lgse/strata#1346
- Video decodes at the pane's size times display scale, capped at 1280 px on either axis and never enlarged beyond the source. lgse/strata#823, lgse/strata#839
- Growing the pane restarts decoding at the current position only when the frame would grow by 8% or more; shrinking never restarts. lgse/strata#839 (unverified)
- Mute and volume are saved and apply live to every open player. lgse/strata#167, lgse/strata#839
- The volume and seek sliders show no focus border when clicked. lgse/strata#962
- In the default key map, Ctrl+Alt+Space plays or pauses, Ctrl+Alt+Left/Right seek 5 s, Ctrl+Alt+Up/Down change volume by 10%, and Ctrl+Alt+M mutes. lgse/strata#888 (unverified)
- On the plain media bar, as for an animated GIF, the play button's tooltip and accessible name read "Play/Pause" and its shortcut in parentheses. lgse/strata#1895 (unverified)
- The mute button's tooltip and accessible name read "Mute/unmute" followed by its shortcut in parentheses. lgse/strata#1895 (unverified)

### Stepping

- Previous and next count and step to a local audio or video file once its metadata probe found media. lgse/strata#2026
- Without a probe answer, a local file joins once its first 8 KiB are not text. Binary bytes under a media name still join. lgse/strata#2026 (unverified)
- A folder holds three real `.h264` streams, a real `clip.mp4`, and text files `fake.mp4` and `notes.h264`. The header reads "of 4", and stepping visits only the four videos. lgse/strata#2026
- That content rule holds in List, Columns, and Icons. lgse/strata#2026
- A file not yet checked stays out of the sequence until it answers. The position and the previous and next buttons update after each chunk of reads. lgse/strata#2026
- The shown file always anchors its own sequence, whether or not its check has answered. lgse/strata#2026
- Checks read outward from the shown file, nearest first, through the mount's request lane. They wait up to 10 s while the mount is busy and give up once it stalls. lgse/strata#2026
- Checks stop when the preview closes or replaces the player with another kind of preview. lgse/strata#2026
- Files on remote (GVfs) locations and route files join the sequence by name. lgse/strata#2026
- An audio entry whose metadata fill found no duration is skipped. lgse/strata#1638, lgse/strata#1901, lgse/strata#2026
- A video entry with neither duration nor known dimensions is skipped. lgse/strata#1638, lgse/strata#1901, lgse/strata#2026
- Previous and next, and the position count, keep a video with known dimensions but no duration, such as a raw `.h264` stream. lgse/strata#1901

### Slider keys

- A focused volume slider steps 0.1 with the arrow keys and 0.2 with Page Up/Down; Home mutes and End sets full volume. lgse/strata#1570, lgse/strata#1451
- Stepped volumes snap to the 0.1 grid, so repeated Down reaches 0 and mutes. lgse/strata#1570
- Dragging the volume slider sets any value, without snapping. lgse/strata#1570 (unverified)
- For media that is neither audio nor video, the seek slider steps 5 s with the arrow keys and 30 s with Page Up/Down. lgse/strata#1570, lgse/strata#1451
- On that seek slider, Home and End jump to the start and the last frame. lgse/strata#1570, lgse/strata#1451
- Keys and the mouse wheel on that seek slider seek at once; a drag seeks on release. lgse/strata#1570, lgse/strata#1451
- That seek slider ignores scroll jumps smaller than one frame. lgse/strata#1570 (unverified)

### Autoplay

- With **Autoplay media previews** off, the default, a selected media file shows paused with a play control. lgse/strata#1106
- With autoplay on, video fades its sound in over 1 s from the first frame and audio over 0.5 s; the saved volume is not changed. lgse/strata#1474
- Clips shorter than 10 s start at full volume, a muted state skips the fade, and any play, pause, seek, volume, or mute input ends it. lgse/strata#1474
- A preview hidden by a narrow window resumes playing when shown again if it was playing, whatever the autoplay setting. lgse/strata#1106

### Start position

- With **Video preview start** at 20, a video of known duration not previewed this session opens at 20% of its length; a 60 s clip opens at 0:12. lgse/strata#2086, lgse/strata#1924
- At the default 0, a preview with no position remembered this session starts at 0:00. lgse/strata#2086, lgse/strata#1924
- The start is saved as `preview_video_start` in `settings.toml`; a file without the key loads as 0. lgse/strata#2086, lgse/strata#1924
- A saved `preview_video_start = 100` or `5000` loads as 99, and setting a value above 99 stores 99. lgse/strata#2086, lgse/strata#1924
- A video with a position remembered this session resumes there, not at the configured start. lgse/strata#2086, lgse/strata#1924
- With the start at 0, a video closed in its first second or at its end later opens at a start set afterwards. lgse/strata#2086, lgse/strata#1924
- With a start set, audio files, animated GIFs and WebPs, and streams of unknown length start at 0:00. lgse/strata#2086, lgse/strata#1924, lgse/strata#2734
- With a start set, a raw stream named `.h264`, `.264`, `.h265`, `.265`, or `.hevc` starts at 0:00. lgse/strata#2086, lgse/strata#1924
- Stepping with Ctrl+Alt+`<`/`>`, or `<`/`>` in 10xer mode, into a video not previewed this session opens it at the configured start. lgse/strata#2086, lgse/strata#1924
- A start that rounds to the first frame, such as a low percent of a short clip, plays from 0:00 without restarting the decoder. lgse/strata#2086, lgse/strata#1924
- The setting is read when a preview opens; changing it leaves an open preview where it is. lgse/strata#2086, lgse/strata#1924

### Seeking and recovery

- An isolated seek restarts at once with the slider at the target; seeks within 200 ms coalesce to the settled position. lgse/strata#1314
- A playback stall mid-play, such as a frozen audio clock or decoder failure, restarts at the last position up to 3 consecutive times without progress, then shows the last error. lgse/strata#1314
- A video closed after more than 1 s and before its end reopens at that position in the same session. lgse/strata#1314
- A video closed within its first second or at its end reopens at 0:00 only when a start was configured as it opened; otherwise its position is forgotten. lgse/strata#1314, lgse/strata#2086, lgse/strata#1924
- On a sink whose start-up delay exceeds 130 ms, such as Bluetooth A2DP over PipeWire-Pulse, audio plays through without stalling at 0:00. lgse/strata#1411
- After a start, seek, or resume, the playhead waits for the audio sink instead of advancing and snapping back. lgse/strata#1411

### Resources and limits

- At most four media previews per process own decoders. A fifth shows "Media previews are busy (four active players). Pause or close another preview and retry." and the others keep playing. lgse/strata#839
- A player paused for 30 seconds releases its decoder and audio output but keeps its frame and position. lgse/strata#839
- Changing selection or closing the preview stops the decoder and its sandbox. lgse/strata#839, lgse/strata#765
- Malformed or truncated decoder output is rejected as a decoder failure, never shown; there is no unsandboxed fallback. lgse/strata#839
- With `STRATA_SANDBOX_PRLIMIT` set to an absolute path and no `prlimit` or `nice` on `STRATA_SANDBOX_PATH`, video playback, waveforms, storyboards, and embedded audio artwork decode. lgse/strata#2098, lgse/strata#2097
- With `STRATA_SANDBOX_PRLIMIT=/usr/bin/false`, a video preview shows "Unable to play this media preview"; restarting with a valid limiter restores playback. lgse/strata#2098
- Waveform and storyboard helpers raise their own niceness by 10, capped at 19, before probing; their decoders inherit it, and playback keeps its priority. lgse/strata#2098

### Hardware acceleration

- With **Hardware-accelerated video previews** on and **Decoding backend** set to Automatic, decoding tries VA-API, then Vulkan, then software; a hardware attempt that fails before its first frame falls back to software. lgse/strata#45, lgse/strata#139
- With no saved choice, a system with an AMD Polaris 10, 11, or 12 GPU decodes in software; the user can still opt in. lgse/strata#139
- Audio-only playback, waveform peaks, and video storyboards decode in software and get no `/dev/dri` or `/dev/nvidia*` device, no `/sys`, and no `/run/opengl-driver`, whatever the acceleration setting. lgse/strata#1289, lgse/strata#1474 (unverified)
- Animated WebP decodes in software whatever the acceleration setting. lgse/strata#2734
- VA-API and Vulkan FFmpeg decoders run without the 512 MiB file-size and 2 GiB address-space limits; software decoders keep both. Every decoder disables core dumps. lgse/strata#2803, lgse/strata#2793
- On an Intel GPU with Mesa ANV and the Vulkan backend, an MP4 preview decodes in hardware instead of FFmpeg dying with `SIGXFSZ` and falling back. lgse/strata#2803, lgse/strata#2793
- Changing the acceleration setting applies to the next preview without interrupting the current one. lgse/strata#139

## Design

[docs/preview-sandbox.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/preview-sandbox.md) ("Incremental media playback" through "Compatibility scope") carries the wire format, budgets, deadlines, and isolation policy.

- Playing the original in GTK or GStreamer, or remuxing it, was rejected because it exposes compressed media to an unsandboxed parser (lgse/strata#824).
- The first design transcoded the first 30 seconds to WebM or MP4 in the sandbox (lgse/strata#17, lgse/strata#37). Hardware encoders sped it up (lgse/strata#38, lgse/strata#45), but a Polaris VCE hang crashed a whole session (lgse/strata#127).
- Incremental decoding replaced that: no re-encode, no second decode, and a first frame in about 1 s instead of 3.3 s (lgse/strata#839).
- The `STRRAW01` wire is untrusted. The parent checks dimensions, strides, tick sequence, and payload lengths before allocating, and EOF without an end record is failure (lgse/strata#839).
- Queues are bounded: three records, three presented frames, and 66 audio blocks. Audio runs 2 s ahead inside the records so slow sinks are primed without pinning frames (lgse/strata#1411).
- Media helpers run outside the driver-wide CPU, address-space, and file-size limits; Intel Vulkan's 1 GiB object hit the inherited `RLIMIT_FSIZE` (lgse/strata#128). Per-record sizes, queue limits, and progress deadlines bound work instead.
- Each FFmpeg process disables core dumps and caps single allocations at 512 MiB. Software decoders also cap files at 512 MiB and address space at 2 GiB (docs/preview-sandbox.md, "Isolation and hardware policy").
- Hardware decoders are exempt from both because GPU drivers reserve sparse memfds and large virtual ranges. Mesa ANV's 1 GiB Vulkan state table hit `EFBIG`, and the kernel killed FFmpeg with `SIGXFSZ` (lgse/strata#2793, lgse/strata#2803).
- lgse/strata#839 had reapplied the file limit to every backend after lgse/strata#119 exempted hardware. Decoded output goes to a pipe, which the file limit never bounded (lgse/strata#2793).
- Hardware decoders stay bounded without it: no outer `prlimit` wraps the media helper, Landlock confines writes to the scratch mounts, and `/tmp` is a size-capped tmpfs ([comment](https://github.com/lgse/strata/pull/2803#issuecomment-7136005380)).
- Audio-only playback, peaks, storyboards, and cover art always decode in software, so they keep both limits (lgse/strata#2803).
- Decoders run the configured absolute limiter instead of `prlimit` by name, and background helpers lower their own priority with `setpriority`. Non-FHS runtimes such as Nix then need no util-linux or coreutils on the sandbox PATH (lgse/strata#2097, lgse/strata#2098).
- Polaris defaults to software because explicit VA-API still hung after 16-pixel alignment; the hang is in VCE encode, not the file (lgse/strata#127).
- Raw elementary streams have no timestamps, so any input `-ss` drops every frame. Their positive seeks use output-side `-ss`, which decodes and discards the prefix (lgse/strata#1346). Detection uses the probed demuxer, never the extension (lgse/strata#1333).
- The volume and seek sliders had zero step and page increments, and the fallback seek slider seeked only on drag end (lgse/strata#1451, lgse/strata#1570).
- Keys stop on the last frame because seeking exactly to the duration ends the stream; stepped volumes snap because float steps stop short of zero (lgse/strata#1570).
- The autoplay fade multiplies a gain on the GStreamer `volume` element, so no audio is processed in Strata and the saved volume is untouched (lgse/strata#1417).
- A preview's audio output is built, started, and changed on one `strata-audio` worker. GStreamer's start-up could scan plugins and rewrite its registry, and state changes could wait on the sound server, all on the UI thread (lgse/strata#1729).
- The preview reads leading bytes before choosing a player, so a sequence trusting names landed on files that preview as text. Sequences now join local files by content (lgse/strata#2003, lgse/strata#2026).
- Content answers belong to one preview and are trimmed to its listing; there is no global cache (lgse/strata#2026).
- Checks run as background work through request lanes, so a stalled mount parks no workers. One 10 s busy wait covers every folder of a run and is never reset within it (lgse/strata#2026).
- FFmpeg's `webp_anim` demuxer reports no duration and cannot seek: `-stream_loop -1` stalls and `-ss` skips to the end. The period is the sum of the ANMF frame durations, read without decoding (lgse/strata#2734).
- Short animated WebPs loop with the `loop` filter, placed before the 30 fps conversion so it holds source frames. Offsets are reached by decoding from the start and trimming (lgse/strata#2734).
- The 256 MiB budget bounds the frames the `loop` filter holds. Its product saturates: 16,384 frames on a 16,777,216-pixel canvas had wrapped to 0 bytes and passed ([comment](https://github.com/lgse/strata/pull/2734#issuecomment-7123582479)).
- Playback depends on FFmpeg 9.0's `webp_anim` decoder. Strata runs the trusted runtime `ffmpeg -hide_banner -decoders`, with no input, once per process and off the main loop. An older FFmpeg keeps the still preview, so nothing regresses (lgse/strata#2734).
- Video preview start is a percentage, not a fixed offset, so one value suits clips of any length (lgse/strata#1910).
- The start applies only with no remembered position, so it complements resume instead of replacing it. It is applied once, when the first header arrives, through the resume restart path; later seeks and resize restarts never reapply it. A first-time video with a start therefore runs two decoder sessions (lgse/strata#1910, lgse/strata#1924).
- Raw streams start at 0:00 because the helper seeks them by decoding up to the target. A late start in a long stream could exceed the first-frame timeout (lgse/strata#1924).
- 0:00 is remembered only when a start was configured. With the default 0, every previewed video and GIF would fill the 128-entry position cache and evict real resume positions (lgse/strata#1924).
- The `packaging/media-runtime` patch kit pins a GStreamer worker-finalization fix and probes. It does not change the shipped binary (lgse/strata#779). The GTK context patch was retired once upstream merged it (lgse/strata#830).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-11-24 | lgse/strata#2803 | fix | Applied the 512 MiB file-size limit only to software FFmpeg, so Vulkan on Mesa ANV is no longer killed by `SIGXFSZ`. |
| 2026-11-24 | lgse/strata#2696 | fix | Dropped the input-side `-thread_queue_size`, which FFmpeg 9.1 rejects, so media previews decode again. |
| 2026-11-07 | lgse/strata#2086 | feat | Added a Video preview start percentage so a video previewed for the first time in a session opens part-way in. |
| 2026-11-02 | lgse/strata#2026 | fix | Built previous/next media sequences from file content, not names, so text files named as videos are skipped. |
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

- Application RSS grows across preview cycles through glibc arena retention; reusable parent-side workers are under investigation. lgse/strata#841
- The volume slider and the plain media bar's seek slider have no accessible name. Naming them needs new strings in every catalog. lgse/strata#1896
- Remote (GVfs) and route files are still placed in a media sequence by name, not content. lgse/strata#2026
- Files not read before the 10 s busy wait ran out stay out of the sequence until the shown file changes. lgse/strata#2026
- The start rule recognizes a raw H.264 or H.265 stream by its extension only. A raw stream named `.mp4` still opens at the configured start. lgse/strata#1924
- Pausing a video with no audio track and pressing Play snaps back to where the decoder session started. With a start of 20, 0:14 jumps to 0:12. The clock base advances only for audio, so Play restarts the wall clock from the old base. lgse/strata#1924
- A video closed before its decoder header arrives forgets its remembered resume position. lgse/strata#1924
- Timing an animated WebP reads every chunk header with no chunk cap, so a multi-GB file of empty chunks is stopped only by the helper's 10 s CPU limit. lgse/strata#2734
