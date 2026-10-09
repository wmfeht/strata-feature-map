---
title: Audio previews
status: shipped
origin: {issue: lgse/strata#1288, pr: lgse/strata#1289}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: reviewed
code: [src/ui/preview/audio.rs, src/ui/preview/audio, src/ui/preview/waveform.rs, src/ui/preview/waveform, src/media/peaks.rs, src/media/peaks]
tests: [src/ui/preview/audio/tests.rs, src/ui/preview/audio/analysis/tests.rs, src/ui/preview/audio/details/tests.rs, src/ui/preview/tests/audio.rs, src/ui/preview/waveform/tests.rs, src/media/peaks/tests.rs, src/ui/window/tests/keyboard_dispatch/audio_tracks.rs]
related: [preview/preview-panel/media/video, browser/search, integration/10xer-mode]
---

## Summary

The now-playing view for audio files: artwork, tags, a live spectrum, a waveform scrubber, and previous/next track controls. It replaces the blank video surface audio files used to show.

## Behavior

### Artwork and details

- An audio file with embedded art shows it, preferring the front cover when several pictures are embedded. lgse/strata#1289
- Without embedded art, a local file shows a `cover`, `folder`, `front`, `album`, or `albumart` image (`.jpg`, `.jpeg`, `.png`, `.webp`) from its folder, preferring names in that order. lgse/strata#1289
- Without any art, a theme-colored record spins in its place while playing. lgse/strata#1289
- Remote audio files use embedded art only. lgse/strata#1289 (unverified)
- Title, artist, and album come from tags; a file without a title tag shows its name without the extension. lgse/strata#1289
- The caption shows the tagged track number, such as "Track 3 of 12"; without one it shows "3 of 12 in folder", or "3 of 12 in results" while filtered results replace the listing. lgse/strata#1289
- Tag and art rows keep their space while loading, so changing tracks does not shift the layout. lgse/strata#1289
- Stepping to a track with the same art keeps it in place; only different art crossfades. lgse/strata#1289
- A pane at least 1.12 times as wide as tall places art beside the controls; at 0.95 or below, art returns on top. lgse/strata#1289 (unverified)
- In the stacked layout, when height runs short the spectrum hides first, then the art. lgse/strata#1289
- Clicking the art or the spectrum toggles play and pause. lgse/strata#1289 (unverified)

### Spectrum and waveform

- While playing, spectrum bars follow the audio being heard, and peak caps hold before falling. lgse/strata#1289
- Playback starts on a plain progress line; a waveform overview grows in once the track has stayed selected for 50 ms. lgse/strata#1289
- Hovering the waveform shows the target time in the elapsed label, and clicking or dragging seeks. lgse/strata#1289
- A file with no audio track or no known duration keeps the plain progress line. lgse/strata#1289
- A waveform decode that fails or runs past 90 seconds stops and keeps only the levels received so far. lgse/strata#1289 (unverified)

### Tracks

- Previous and next step through the folder's audio files, or visible filtered audio results including subfolders, and keep playing if the current track was playing. lgse/strata#1289
- Previous is disabled on the first audio file and next on the last; stepping does not wrap. lgse/strata#1289 (unverified)
- Previous and next skip playlists and MIDI files. lgse/strata#1289
- In 10xer mode, `<` and `>` step tracks from the listing or inside the preview; the default key map uses Ctrl+Alt+`<` and Ctrl+Alt+`>`. lgse/strata#1289
- Tracks never advance automatically when one ends. lgse/strata#1289
- Every track starts from the beginning; audio does not resume where it stopped. lgse/strata#1289
- An undecodable track shows its error inside the audio view with previous and next still usable. lgse/strata#1289
- An audio-typed file, such as `.ogg`, that holds a non-cover video stream switches to the video view once prepared. lgse/strata#1289
- Resizing the pane does not restart audio playback. lgse/strata#1289

## Design

Each part is sandboxed or derived from already validated data. "Audio previews" in [docs/preview-sandbox.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/preview-sandbox.md) is the maintained description.

- Songs play through an audio-only `preview-audio` session that ignores attached pictures. Art is no longer decoded into a frame resent 30 times a second, and broken art cannot block playback (lgse/strata#1289).
- Art comes from a separate `audio-cover` operation scaled to at most 800×800 inside the sandbox. Tags come from `audio-tags`, limited to five fields, stripped of control and bidirectional-override characters, and capped at 200 characters (lgse/strata#1289).
- The spectrum is computed in Strata from the PCM it already plays, aligned to the sink's clock, so no extra parser sees the stream (lgse/strata#1289). It keeps 1 s behind the playhead plus everything decoded ahead, so it follows slow sinks (lgse/strata#1411).
- The waveform comes from an `audio-peaks` operation at niceness 10, streaming 1,024 buckets in `STRPEAK1` records that the parent validates. Overviews are cached for 64 tracks (lgse/strata#1289).
- Only one background decode runs at a time; waveform overviews share that slot with video storyboards (lgse/strata#1474).
- Tags and art wait 50 ms and are cached for 12 tracks, so rapid stepping spawns no work; failed lookups retry on revisit (lgse/strata#1289).
- A 24-band SoundCloud-style spectrum with click-to-play was the request; the shipped view adds art, tags, and a waveform overview (lgse/strata#1288).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-03 | lgse/strata#1289 | feat | Added the now-playing audio view with art, tags, spectrum, waveform scrubber, and track stepping. |

## Known gaps

None known.
