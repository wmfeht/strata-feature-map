---
title: Chooser PNG conversion
status: shipped
origin: {issue: lgse/strata#1386, pr: lgse/strata#1387}
branch: null
reviewed_at: aee71335dfecd059b9af23efeac2ed52c43e3b19
review: reviewed
code: [src/ui/chooser/image_conversion.rs, src/services/image_conversion.rs, src/sandbox_helper/image_conversion.rs]
tests: [src/ui/chooser/tests/image_conversion.rs, src/services/image_conversion/tests.rs, src/sandbox_helper/image_conversion/tests.rs, tests/e2e/scenarios/test_chooser_image_conversion.py]
related: [integration/portal-file-chooser/url-download, preview/preview-panel]
---

## Summary

An opt-in conversion to PNG for images downloaded through the chooser's Name field when the selected filter accepts PNG but not the downloaded format. It covers JPEG, BMP, static WebP, and single-frame GIF, decoded in the preview sandbox.

## Behavior

### Detection

- A downloaded JPEG, BMP, single-frame GIF, or static WebP that the selected filter rejects, while it accepts PNG, is checked in the sandbox, then opens "Convert image to PNG?" with Convert to PNG and Cancel. lgse/strata#1387
- The format is detected from file contents, not the URL extension or HTTP content type. lgse/strata#1387
- A file starting with `BM` counts as BMP only with zero reserved bytes and a DIB header size of 12, 40, 52, 56, 108, or 124. lgse/strata#1387
- A supported image with the wrong extension is renamed to that format's extension when the renamed file passes the filter, without conversion. lgse/strata#1387
- When neither the detected format's name nor a PNG name passes the filter, the ordinary filename filter decides, under the server-provided name. lgse/strata#1387
- PNG bytes that the filter accepts under a PNG name, including APNG and corrupt data with a PNG signature, are returned without conversion or sandbox validation. lgse/strata#1387
- A `.png` download whose bytes are not a supported image shows "This download is not a supported image. Choose a JPEG, BMP, static WebP, GIF or PNG image." under a filter that accepts PNG but not JPEG. lgse/strata#1387

### Conversion

- Convert to PNG returns a PNG with the original dimensions, transparency, orientation, and compatible colour profile. lgse/strata#1387
- An animated GIF or WebP shows "Animated images cannot be converted to PNG. Choose a static image instead." during the check, without the conversion prompt. lgse/strata#1387
- An embedded ICC profile whose colour space does not match the decoded image aborts conversion; an unprofiled CMYK JPEG converts from the decoder's RGB output. lgse/strata#1387
- Inputs over 32 MiB or 16 megapixels, or a PNG output over 32 MiB, fail with the limit named in the error. lgse/strata#1387
- Cancel, Escape, or a failed conversion leaves the chooser open and returns nothing. lgse/strata#1387
- Changing Name or the selected filter while checking or converting stops the job and shows "The name or filter changed. Press Open to try again." lgse/strata#1387
- The converted PNG is written to a new `strata-download-*` folder and kept, with the original, until the one-day sweep. lgse/strata#1387

## Design

[docs/portal-file-chooser.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/portal-file-chooser.md) carries the detection and limit rules.

- Conversion needs consent, follows only the active filter, and never silently flattens animation (lgse/strata#1387).
- Silent conversion, extension-based detection, other output formats, and TIFF, SVG, AVIF, or HEIC inputs were excluded (lgse/strata#1386).
- Only a 32-byte signature is read outside the sandbox; decoding and encoding run in the bounded helper (lgse/strata#1387).
- Incompatible colour profiles abort conversion rather than being stripped or colour-converted (lgse/strata#1387).
- The 128 MiB decoder allocation budget is best-effort. Pre-decode dimension checks and sandbox process limits bound resources (lgse/strata#1387).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-03 | lgse/strata#1387 | feat | Offered sandboxed PNG conversion for downloaded images that the selected filter rejects. |

## Known gaps

None known.
