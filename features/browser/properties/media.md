---
title: Media details in Properties
status: shipped
origin: {issue: lgse/strata#979, pr: lgse/strata#984}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [src/ui/browser/properties/media.rs]
tests: [src/ui/browser/properties/media/tests.rs, tests/e2e/scenarios/test_properties_media.py]
docs: [docs/preview-sandbox.md]
related: [preview/preview-panel]
---

## Summary

Source-media details for a single local image, audio, or video file in Properties: resolution, duration, bitrate, codecs, frame rate, sample rate, channels, HDR format, subtitles, and chapters. Camera RAW files get `browser/properties/raw-metadata` instead.

## Behavior

- For a local file whose MIME type is `image/*`, `audio/*`, or `video/*`, Properties shows a MEDIA row reading "Loading…" until inspection finishes. lgse/strata#984 (unverified)
- A PNG of 1600 × 900 shows RESOLUTION "1600 × 900 pixels" and no DURATION, FRAME RATE, or AUDIO CODEC. lgse/strata#984
- An H.264/AAC MP4 shows RESOLUTION, DURATION as `H:MM:SS`, BITRATE, VIDEO CODEC "h264", FRAME RATE "24.00 fps", AUDIO CODEC "aac", SAMPLE RATE "48.0 kHz", and CHANNELS "2 (Stereo)". lgse/strata#984
- A mono WAV shows DURATION, AUDIO CODEC "pcm_s16le", SAMPLE RATE "44.1 kHz", CHANNELS "1 (Mono)", and BITRATE, with no RESOLUTION or VIDEO CODEC. lgse/strata#984
- BITRATE reads in Mb/s with two decimals from 1,000,000 bit/s, otherwise in kb/s. lgse/strata#984 (unverified)
- Fields the file does not report are omitted. lgse/strata#984
- A video with SMPTE 2084 or ARIB STD-B67 transfer shows HDR "HDR10" or "HLG". lgse/strata#1474 (unverified)
- A video with subtitle tracks shows SUBTITLES as the track count followed by known languages in parentheses, and CHAPTERS as the chapter count. lgse/strata#1474 (unverified)
- A damaged or unrecognised media file shows MEDIA "Unavailable", and the other details and permissions stay usable. lgse/strata#984
- A non-media file such as `readme.md` shows no MEDIA row. lgse/strata#984
- Remote files are not downloaded for inspection and show no media section. lgse/strata#984
- Closing Properties cancels a running inspection. lgse/strata#984
- The details scroll inside the dialog, so the permission controls stay reachable and usable below several media rows. lgse/strata#984
- The preview panel keeps only Size, Modified, and Type for media and shows none of these fields. lgse/strata#984

## Design

Inspection runs in the preview sandbox; [docs/preview-sandbox.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/preview-sandbox.md) carries its isolation model. Properties inspection is not counted against the browser worker limit.

- Values come from the source file, not the scaled or resampled preview, so images report no synthetic timing (lgse/strata#984).
- The sandbox stays network-isolated and gets no GPU access for metadata; only the BLAS/LAPACK files FFmpeg needs on Debian were added (lgse/strata#984).
- The scope first included the preview pane. The owner then kept detailed media metadata in Properties only, to keep the preview uncluttered (lgse/strata#979 comments).
- Unavailable fields are omitted rather than shown empty (lgse/strata#979).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-14 | lgse/strata#984 | feat | Added sandboxed source-media details to file Properties, kept out of the preview pane. |

## Known gaps

None known.
