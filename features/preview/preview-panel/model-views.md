---
title: Model camera views
status: shipped
origin: {issue: lgse/strata#1633, pr: lgse/strata#1644}
branch: null
reviewed_at: e0f73973926ff67e77c2c56cf288b7b7617bb2e5
review: draft
code: [src/ui/preview/model.rs, src/sandbox/model.rs]
tests: [src/ui/preview/model/tests.rs, src/ui/preview/tests/model.rs, src/sandbox/model/tests.rs, tests/e2e/scenarios/test_quick_preview.py]
related: [preview/preview-panel/media/video, preview/preview-panel/layout, preview/quick-preview, settings/themes]
---

## Summary

Camera controls and mesh details for rendered STL and 3MF previews in the drawer and Quick Preview. Users step through four preset views around the model, guided by a top-down orbit indicator, with format and triangle-count badges.

## Behavior

### Camera views

- Opening a rendered model, or another file, starts from the **Front left** view. lgse/strata#1644, lgse/strata#1633
- **Next model view** cycles Front left, Front right, Back right, Back left, and wraps to Front left. lgse/strata#1644
- **Previous model view** from Front left goes to Back left. lgse/strata#1644
- Changing the theme reloads the open model with the new palette and keeps its selected view. lgse/strata#1644, lgse/strata#1633
- Only the two buttons change the view; no key binding does. lgse/strata#1644 (unverified)
- A 3MF with one usable embedded PNG, or a FreeCAD file, shows its saved image with no camera buttons, no indicator, and no badges. lgse/strata#1644, lgse/strata#1633

### Indicator

- Between the buttons, an image named "Camera position" maps the camera from above: a hollow circle for the model, a dot on its edge for the camera. lgse/strata#1644
- Front left puts the dot lower left, Front right lower right, Back right upper right, and Back left upper left. lgse/strata#1644
- The indicator's accessible description is the current view name, such as "Front left"; it shows no visible caption. lgse/strata#1644
- With animations on, the dot sweeps to the new position in 240 ms along the shorter turn. lgse/strata#1644 (unverified)
- With Reduce motion on, system animations off, or the preview unmapped, the dot jumps to the new position. lgse/strata#1644

### Loading and errors

- While another view renders, the last image stays at opacity 0.3 with a wait cursor, and the header shows a spinner left of Open. lgse/strata#1644
- The header spinner's accessible label reads "Loading preview…", then the model stage text, such as "Rendering N triangles…". lgse/strata#1644 (unverified)
- Clicking a camera button during a render is ignored; the button keeps focus and the drawer keeps the keys. lgse/strata#1644
- Selecting another file mid-render stops and hides the header spinner. lgse/strata#1644
- While views change, the header content type stays `model/stl` or `model/3mf`. lgse/strata#1644
- A view render or image decode that fails keeps the previous image, shows an error under the controls, and the buttons can retry. lgse/strata#1644
- A mesh result naming another view than requested, the wrong format, 0 triangles, or over 2 million triangles fails with "The preview renderer produced invalid image data". lgse/strata#1644
- An STL result without mesh details fails with the same message. lgse/strata#1644

### Details

- A badge row above the controls shows "Binary STL", "ASCII STL", or "3MF", and a count such as "1 triangle" or "N triangles". lgse/strata#1644
- Above the file name, an eyebrow such as "2 of 4 in folder" gives the file's position among model files in the sorted, filtered listing. lgse/strata#1644
- FreeCAD and thumbnail-only 3MF files count toward that total. lgse/strata#1644 (unverified)
- The model and its controls form one vertically centred block, so a taller window keeps them together. lgse/strata#1644
- The model picture keeps the grab cursor and file drag. lgse/strata#1633, lgse/strata#1644 (unverified)

## Design

- Preset views replace free rotation. Continuous rotation would need frequent software renders or a new interactive renderer; presets fit the sandboxed renderer (lgse/strata#1633).
- The controls borrow the video player: the play button becomes the camera dot, and previous and next step the camera. The orbit diagram carries the view, so no visible label is shown (lgse/strata#1633, lgse/strata#1644).
- The renderer and the indicator share the camera directions. View names follow the model axes: +X right, −Y front, +Z up (lgse/strata#1644).
- Badges reuse counts from the parse and render pass, so thumbnail previews never parse geometry for them. Dimensions and units are not shown (lgse/strata#1644).
- Review replaced a loading card over the model with a header spinner. The buttons stay sensitive so focus and the keyboard-owner bar survive a render (lgse/strata#1644).
- The sandbox boundary rejects a mesh result that does not identify the requested view, so a stale render cannot show under the wrong camera (lgse/strata#1644).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |

## Known gaps

None known.
