---
title: RAW photo details
status: shipped
origin: {issue: lgse/strata#1168, pr: lgse/strata#1171}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [src/ui/raw_details.rs, src/sandbox/raw_metadata.rs, src/sandbox_helper/raw_metadata.rs]
tests: [src/ui/raw_details/tests.rs, src/sandbox/raw_metadata/tests.rs, src/sandbox_helper/raw_metadata/tests.rs]
docs: [docs/preview-sandbox.md]
related: [preview/preview-panel]
---

## Summary

Capture details for camera RAW files, shown in Properties and in the preview panel: dimensions, camera, lens, focal length, shutter speed, ISO, and GPS coordinates.

## Behavior

- A file whose name ends in a RAW extension such as `.DNG`, `.NEF`, `.CR3`, or `.ARW`, in any case, shows seven RAW rows in place of the media rows. lgse/strata#1171 (unverified)
- The rows read DIMENSIONS, CAMERA, LENS, FOCAL LENGTH, SHUTTER SPEED, ISO, and GPS COORDINATES, in that order, and all seven always appear. lgse/strata#1168, lgse/strata#1171
- A readable RAW shows values such as "600 × 400 pixels", "50 mm", "1/250 s", "400", and "-12.500000, -45.250000". lgse/strata#1171
- A non-reciprocal exposure reads in decimal seconds, such as "0.3 s", not "1/3.333 s". lgse/strata#1171
- DIMENSIONS reports the original image size after orientation, never the size of an embedded thumbnail. lgse/strata#1171
- A field the file does not report reads "N/A"; an unreadable RAW shows "N/A" in all seven rows. lgse/strata#1171
- A remote RAW file is not downloaded and shows "N/A" in all seven rows. lgse/strata#1171
- Properties and the preview panel show identical values for the same file. lgse/strata#1171
- In the preview panel, the rows keep their place while navigating between RAW files; values reset to "N/A" and then load. lgse/strata#1171
- Selecting a non-RAW file removes the RAW rows from the preview panel. lgse/strata#1171
- A RAW file in Trash, including one whose stored name has a collision suffix, shows the same values as the original. lgse/strata#1171

## Design

Metadata is read inside the preview sandbox, described in [docs/preview-sandbox.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/preview-sandbox.md). No pixels are decoded and no external geocoding is done (lgse/strata#1168).

- The sandboxed LibRaw/dcraw identification already used for RAW thumbnails supplies most fields, with a 3-second limit per tool. `kamadak-exif` fills missing fields and supplies GPS, because those tools omit GPS and ImageMagick's DNG output varies by version. It is also the fallback when neither tool is installed (lgse/strata#1171).
- All seven fields stay visible with "N/A" so rows do not shift between files (lgse/strata#1168, lgse/strata#1171). Pixel aspect ratio was considered and excluded.
- Detection checks both the stored and the displayed name, and Trash entries read their local backing file, so collision-suffixed Trash names still work (lgse/strata#1171).
- Parsed values are bounded before display: text fields up to 256 bytes without control or bidirectional characters, dimensions from 1 to 1,000,000 pixels, coordinates within ±90 and ±180 (lgse/strata#1171).
- One `raw_details` module draws the rows for both Properties and the preview panel, so the two surfaces cannot disagree (lgse/strata#1171).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-25 | lgse/strata#1171 | feat | Added RAW capture details to Properties and the preview panel. |

## Known gaps

None known.
