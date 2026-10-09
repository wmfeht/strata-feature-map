---
title: Audio previews
status: shipped
origin: {issue: lgse/strata#1288, pr: lgse/strata#1289}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [src/ui/preview/audio.rs, src/ui/preview/audio, src/ui/preview/waveform.rs, src/ui/preview/waveform, src/media/peaks.rs, src/media/peaks]
tests: [src/ui/preview/audio/tests.rs, src/ui/preview/audio/analysis/tests.rs, src/ui/preview/audio/details/tests.rs, src/ui/preview/tests/audio.rs, src/ui/preview/waveform/tests.rs, src/media/peaks/tests.rs, src/ui/window/tests/keyboard_dispatch/audio_tracks.rs]
related: [preview/preview-panel/media/video, browser/search, integration/10xer-mode]
---

## Summary

The now-playing view for audio files: artwork, tags, a live spectrum, a waveform scrubber, and previous/next track controls. It replaces the blank video surface audio files used to show.

## Behavior

### Artwork and details

- An audio file with embedded art shows it, preferring the front cover when several pictures are embedded. lgse/strata#1289
- Without embedded art, a local file shows the first `cover`, `folder`, `front`, `album`, or `albumart` image (`.jpg`, `.jpeg`, `.png`, `.webp`) in its folder. lgse/strata#1289
- Without any art, a theme-colored record spins in its place while playing. lgse/strata#1289
- Remote audio files use embedded art only. lgse/strata#1289 (unverified)
- Title, artist, and album come from tags; untagged files show their position as "3 of 12 in folder", or "in results" while filtering. lgse/strata#1289
- Tag and art rows keep their space while loading, so changing tracks does not shift the layout. lgse/strata#1289
- Stepping to a track with the same art keeps it in place; only different art crossfades. lgse/strata#1289
- A pane wider than tall places art beside the controls; otherwise art sits on top. When space runs short the spectrum hides first, then the art. lgse/strata#1289

### Spectrum and waveform

- While playing, spectrum bars follow the audio being heard, and peak caps hold before falling. lgse/strata#1289
- Playback starts on a plain progress line; a waveform overview grows in once the track has stayed selected for 50 ms. lgse/strata#1289
- Hovering the waveform shows the target time and clicking seeks. lgse/strata#1289
- A file with no known duration, or whose waveform decode fails or exceeds 90 seconds, keeps the plain progress line. lgse/strata#1289

### Tracks

- Previous and next step through the folder's audio files, or visible filtered audio results including subfolders, and keep playing. lgse/strata#1289
- Previous and next skip playlists and MIDI files. lgse/strata#1289
- In 10xer mode, `<` and `>` step tracks from the listing or inside the preview; the default key map uses Ctrl+Alt+`<` and Ctrl+Alt+`>`. lgse/strata#1289
- Tracks never advance automatically when one ends. lgse/strata#1289
- Every track starts from the beginning; audio does not resume where it stopped. lgse/strata#1289
- An undecodable track shows its error inside the audio view with previous and next still usable. lgse/strata#1289
- A file named `.ogg` that holds a real video stream opens in the video view. lgse/strata#1289
- Resizing the pane does not restart audio playback. lgse/strata#1289

## Design

Each part is sandboxed or derived from already validated data. "Audio previews" in [docs/preview-sandbox.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/preview-sandbox.md) is the maintained description.

- Songs play through an audio-only `preview-audio` session that ignores attached pictures. Art is no longer decoded into a frame resent 30 times a second, and broken art cannot block playback (lgse/strata#1289).
- Art comes from a separate `audio-cover` operation scaled to at most 800×800 inside the sandbox. Tags come from `audio-tags`, limited to five fields, stripped of control and bidirectional-override characters, and capped at 200 characters (lgse/strata#1289).
- The spectrum is computed in Strata from the PCM it already plays, aligned to the sink's clock, so no extra parser sees the stream (lgse/strata#1289). It keeps 1 s behind the playhead plus everything decoded ahead, so it follows slow sinks (lgse/strata#1411).
- The waveform comes from one `audio-peaks` operation at a time at niceness 10, streaming 1,024 buckets in `STRPEAK1` records that the parent validates. Overviews are cached for 64 tracks (lgse/strata#1289).
- Tags and art wait 50 ms and are cached for 12 tracks, so rapid stepping spawns no work; failed lookups retry on revisit (lgse/strata#1289).
- A 24-band SoundCloud-style spectrum with click-to-play was the request; the shipped view adds art, tags, and a waveform overview (lgse/strata#1288).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-03 | lgse/strata#1289 | feat | Added the now-playing audio view with art, tags, spectrum, waveform scrubber, and track stepping. |

## Known gaps

None known.
