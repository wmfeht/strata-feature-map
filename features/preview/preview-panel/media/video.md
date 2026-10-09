---
title: Video previews
status: shipped
origin: {issue: lgse/strata#1417, pr: lgse/strata#1474}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: reviewed
code: [src/ui/preview/video.rs, src/ui/preview/video, src/media/storyboard.rs, src/media/storyboard, src/ui/media/ambient.rs, src/ui/media/ambient]
tests: [src/ui/preview/tests/video.rs, src/ui/preview/video/badges/tests.rs, src/ui/preview/video/details/tests.rs, src/ui/preview/video/storyboard/tests.rs, src/media/storyboard/tests.rs, src/ui/media/ambient/tests.rs, src/ui/window/tests/keyboard_dispatch/video_clips.rs, tests/e2e/scenarios/test_preview_video.py]
related: [preview/preview-panel/media/audio, browser/properties, integration/open-with, settings/themes]
---

## Summary

The now-playing view for video files: the frame, a header with technical badges, a waveform timeline with chapter ticks and storyboard scrubbing, and previous/next controls. It also hands playback to the default player at the current position.

## Behavior

### Frame

- Before the first decoded frame, the frame area shows the listing's cached thumbnail dimmed, or a plain surface at the probed aspect; it never shows a spinner. lgse/strata#1474
- A video resuming where it stopped shows its nearest cached storyboard cell instead of the opening thumbnail. lgse/strata#1474
- The first frame fades the stand-in out over 150 ms, or replaces it at once under reduced motion. lgse/strata#1474
- Clicking the frame toggles playback. lgse/strata#1474
- With **Element glow** on and a GPU renderer, the frame's edge colors bleed into a 24 px band around it; it is off under reduced motion or Cairo and frozen while paused. lgse/strata#1474

### Header and badges

- The header shows the file's position among the listing's videos, such as "2 of 5 in folder", or "in results" while search results replace the listing. lgse/strata#1474
- A playback error shows its title and detail inside the view; play is disabled and previous and next stay usable. lgse/strata#1474
- Badges under the title show resolution class (SD to 8K), HDR10 or HLG, bit depth, rounded frame rate, video codec, and audio codec with channel layout. lgse/strata#1474
- A captions badge, "CC" or "CC ×N", counts embedded subtitle tracks plus `srt`, `vtt`, `ass`, `ssa`, or `sub` sidecars named after the video, such as `clip.en.vtt`. lgse/strata#1474
- Subtitles are never drawn on the frame. lgse/strata#1474
- Until the probe answers, empty pills hold the row; a failed probe leaves it empty. lgse/strata#1474

### Timeline

- The timeline is the audio waveform slider, with chapter starts as ticks. lgse/strata#1474
- Hovering or dragging the timeline shows a bubble with the nearest storyboard cell, the pointer's time, and that time's chapter title. lgse/strata#1474
- During a seek, the nearest storyboard cell covers the old frame until the new one is decoded. lgse/strata#1474
- Clips under four seconds, animations, attached pictures, raw elementary streams, and unknown durations have no storyboard. lgse/strata#1474

### Stepping and handoff

- Previous and next, Ctrl+Alt+`<` and Ctrl+Alt+`>`, or `<` and `>` in 10xer mode step to the previous or next video, skipping audio files. lgse/strata#1474
- Enter, the header's Open button, or activating the file in the listing pauses the preview and opens the default player. lgse/strata#1474
- mpv, VLC, Celluloid, and MPlayer start at the preview's position; other players, and positions within 1 s of either end, open the file plainly. lgse/strata#1474
- A video double-clicked while its preview is loading stays paused when the preview lands; moving to another file or pressing play lifts the hold. lgse/strata#1474

## Design

"Video previews" in [docs/preview-sandbox.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/preview-sandbox.md) is the maintained description. The view mirrors the audio view: skeletons instead of spinners, no idle animation, and reduced motion respected (lgse/strata#1417).

- Every media stream waits 50 ms before starting its sandbox session, so a selection that moves on within that window spawns no decoder (lgse/strata#1474).
- Badges reuse the bounded `media-metadata` `ffprobe` operation that File Properties uses. Results are cached for 12 files and the sidecar scan runs off the GTK thread (lgse/strata#1474).
- Storyboards run one software `ffmpeg` per keyframe cell rather than a single-pass sprite sheet, so cost scales with the 8 to 48 cells, not file length. VA-API per cell was slower because each process initializes the device (lgse/strata#1417).
- Cells arrive in binary-subdivision order as raw RGBA in `STRSTB01` records the parent validates. Boards are cached in memory for 8 clips, about 14 MB for 16:9 video (lgse/strata#1474).
- The storyboard and the waveform share one niceness-10 background slot; the bounded storyboard goes first so scrubbing never waits on the length-proportional audio decode (lgse/strata#1474).
- Ambient light samples a 6×4 grid at most ten times a second and lets the GPU scale it. Blur-based glow was rejected for cost (lgse/strata#1417).
- Subtitle rendering was rejected because it needs libass in the sandbox and a re-decode. Position handoff uses each player's start flag, because URI fragments cannot pass through `gio::AppInfo::launch` (lgse/strata#1417).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-05 | lgse/strata#1474 | feat | Added the now-playing video view with badges, storyboard scrubbing, ambient light, and position handoff. |

## Known gaps

None known.
