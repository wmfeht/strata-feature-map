---
title: G-code thumbnail previews
status: shipped
origin: {issue: lgse/strata#1863, pr: lgse/strata#1864}
branch: null
reviewed_at: 86df474dc0e8352e0e2098637a017cc4c77a8c44
review: reviewed
code: [src/sandbox_helper/model/gcode.rs]
tests: [src/sandbox_helper/model/gcode/tests.rs]
related: [preview/preview-panel/model-views, preview/preview-panel/sandbox, browser/thumbnails]
---

## Summary

Previews of sliced 3D-printer files from the image the slicer embedded in them, for recognizing a print job without a slicer. A sandboxed reader takes the largest decodable thumbnail from text `.gcode` and `.gco` comments or binary `.bgcode` blocks; the toolpath is never drawn.

## Behavior

- A local text `.gcode` or `.gco` file shows the base64 image between its `; thumbnail begin` and `; thumbnail end` comments. lgse/strata#1864
- The `thumbnail_PNG`, `thumbnail_JPG`, and `thumbnail_QOI` comment forms are read the same way. lgse/strata#1864
- The `thumbnail_JPEG` comment form is also read. lgse/strata#1864 (unverified)
- PNG, JPEG, and QOI thumbnails decode. lgse/strata#1864
- A local binary `.bgcode` file shows the image from its thumbnail blocks. lgse/strata#1864
- A binary `.bgcode` file without a usable thumbnail shows "This G-code file has no usable embedded thumbnail". lgse/strata#1864
- With several thumbnails, the preview shows the largest one that decodes. lgse/strata#1864
- When the largest thumbnail is corrupt, the next largest shows. lgse/strata#1864
- Thumbnail comments with CRLF line endings decode. lgse/strata#1864
- In the drawer, the thumbnail scales down to fit the pane and is never enlarged. lgse/strata#1864 (unverified)
- Text reading stops at the first command, or after 2 MiB (`MAX_GCODE_HEADER_BYTES`). A thumbnail block already started is read to its end. lgse/strata#1864
- Binary reading stops at the first G-code block, and a compressed thumbnail block is skipped. lgse/strata#1864
- A very large G-code file shows its thumbnail without its toolpath being read. lgse/strata#1864
- A thumbnail over 4 MiB or 16 megapixels is not used. lgse/strata#1864

## Design

- Rendering the toolpath, as gcodeThumb does, needs a different viewer and was left out. STEP and STP have no embedded image and need a CAD kernel, so they are out of scope (lgse/strata#1863).
- Several thumbnail sizes are normal in G-code, unlike two usable PNGs in a 3MF, so the largest decodable image wins rather than counting as ambiguous (lgse/strata#1864).
- The reader reuses the embedded-image limits of `src/sandbox_helper/model/embedded.rs`: candidates, bytes per image, total bytes, and total pixels (lgse/strata#1864).
- Reading only the header lets G-code skip the 128 MiB model input cap (lgse/strata#1864).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |

## Known gaps

None known.
