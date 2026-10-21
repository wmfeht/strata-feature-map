---
title: Model camera views
status: shipped
origin: {issue: lgse/strata#1633, pr: lgse/strata#1644}
branch: null
reviewed_at: 4b9a6ace71017888b3a2124d7d911c5c664cc767
review: draft
code: [src/ui/preview/model.rs, src/sandbox/model.rs]
tests: [src/ui/preview/model/tests.rs, src/ui/preview/tests/model.rs, src/sandbox/model/tests.rs, tests/e2e/scenarios/test_quick_preview.py]
related: [preview/preview-panel/media/video, preview/preview-panel/layout, preview/quick-preview, settings/themes]
---

## Summary

Camera controls and mesh details for rendered STL and 3MF previews in the drawer and Quick Preview. Users step through four preset views around the model, guided by a top-down orbit indicator, with format and triangle-count badges.

## Behavior

### Camera views

- **Next model view** turns the camera clockwise: Front left, Back left, Back right, Front right, then wraps to Front left. lgse/strata#1644, lgse/strata#1764
- **Previous model view** turns it anticlockwise: from Front left it goes to Front right. lgse/strata#1644, lgse/strata#1764
- Only the two buttons change the view; no key binding does. lgse/strata#1644 (unverified)
- Once loaded, a 3MF with one usable embedded PNG, or a FreeCAD file, shows its saved image without camera buttons, indicator, or badges. lgse/strata#1644, lgse/strata#1633, lgse/strata#1764

### Indicator

- Between the buttons, an image named "Camera position" maps the camera from above. lgse/strata#1644
- In that map, a hollow centre circle marks the model, and a dot on the outer ring marks the camera. lgse/strata#1644
- Front left puts the dot lower left, Front right lower right, Back right upper right, and Back left upper left. lgse/strata#1644
- The indicator's accessible description is the current view name, such as "Front left"; it shows no visible caption. lgse/strata#1644
- With animations on, the dot sweeps to the new position in 240 ms along the shorter turn. lgse/strata#1644 (unverified)
- With Reduce motion on, system animations off, or the preview unmapped, the dot jumps to the new position. lgse/strata#1644

### Loading and errors

- Before its first image, an STL or 3MF shows its filename, position eyebrow, and format badge. lgse/strata#1764
- That first-load format badge is the uppercase extension, such as "STL". lgse/strata#1764 (unverified)
- On a first load, the triangle badge appears once rendering reports a count; with the image, the format badge becomes "Binary STL", "ASCII STL", or "3MF". lgse/strata#1764
- Previous and Next are insensitive until the first image is ready; clicking them does nothing. lgse/strata#1764
- A loading FreeCAD file or embedded-image 3MF shows the same details and inactive camera controls, then switches to the plain image. lgse/strata#1764
- A FreeCAD file's loading badge reads "FCSTD". lgse/strata#1764 (unverified)
- No loading card covers the model; the header spinner left of Open is the only indicator, shown at once for first loads and view changes. lgse/strata#1764
- While another view renders, the last image stays at opacity 0.3 with a wait cursor. lgse/strata#1644
- The header spinner's accessible label reads "Loading preview…", then "Reading model…", "Rendering N triangles…", and "Finishing preview…"; embedded images read "Reading thumbnail…" instead of the count. lgse/strata#1276, lgse/strata#1644, lgse/strata#1764
- Clicking a camera button during a render is ignored; the button keeps focus and the drawer keeps the keys. lgse/strata#1644
- Selecting a non-model file mid-render stops and hides the header spinner. lgse/strata#1644 (unverified)
- Selecting another model file mid-render keeps the header spinner showing for that file's first load. lgse/strata#1764 (unverified)
- After the first image, a failed view render or image decode keeps the previous image and shows an error under the controls; the buttons retry. lgse/strata#1644, lgse/strata#1764
- A first load that fails shows "Preview unavailable" and its error in the drawer, with no camera controls. lgse/strata#1764

### Details

- A badge row above the controls shows "Binary STL", "ASCII STL", or "3MF", and a count such as "1 triangle" or "N triangles". lgse/strata#1644
- Above the file name, an eyebrow such as "2 of 4 in folder" gives the file's position among model files. lgse/strata#1644
- That position follows the listing's current sort and filter. lgse/strata#1644
- With search results in place of the listing, the eyebrow reads "N of M in results". lgse/strata#1644 (unverified)
- FreeCAD and thumbnail-only 3MF files count toward that total. lgse/strata#1644 (unverified)
- The model and its controls form one vertically centred block, so a taller window keeps them together. lgse/strata#1644
- The model picture keeps the grab cursor and file drag. lgse/strata#1633, lgse/strata#1644 (unverified)

## Design

- Preset views replace free rotation. Continuous rotation would need frequent software renders or a new interactive renderer; presets fit the sandboxed renderer (lgse/strata#1633).
- The controls borrow the video player: the play button becomes the camera dot, and previous and next step the camera. The orbit diagram carries the view, so no visible label is shown (lgse/strata#1633, lgse/strata#1644).
- The renderer and the indicator share the camera directions. View names follow the model axes: +X right, −Y front, +Z up (lgse/strata#1644).
- Badges reuse counts from the parse and render pass, so thumbnail previews never parse geometry for them. Dimensions and units are not shown (lgse/strata#1644).
- A header spinner replaced a loading card over the model. The buttons stay sensitive during view renders so focus and the keyboard-owner bar survive a render (lgse/strata#1644). They stay insensitive until the first image exists (lgse/strata#1764).
- A centred progress card returned for the first load, then was removed again because it flashed for small models. The header spinner carries the stage in its accessible label (lgse/strata#1764).
- Model badges take their own badge area in the shared player layout instead of the video timeline slot (lgse/strata#1764).
- The sandbox boundary rejects a mesh result that does not identify the requested view, so a stale render cannot show under the wrong camera. It also rejects a format mismatch, 0 triangles, more than 2 million, or an STL without mesh details (lgse/strata#1644).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |

## Known gaps

None known.
