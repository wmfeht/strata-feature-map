---
title: 3D model previews
status: shipped
origin: {issue: lgse/strata#1225, pr: lgse/strata#1276}
branch: null
reviewed_at: 44bfeab305cfb68993bafcf4794fe0bbf7ff1433
review: reviewed
code: [src/ui/preview/model.rs, src/sandbox/model.rs, src/services/model_preview.rs, src/sandbox_helper/model.rs, src/sandbox_helper/model/embedded.rs]
tests: [src/ui/preview/model/tests.rs, src/ui/preview/tests/model.rs, src/sandbox/model/tests.rs, src/adapters/local_preview/tests/model_preview.rs, src/sandbox_helper/model/tests.rs, src/sandbox_helper/model/embedded/tests.rs, tests/qa/scenarios/quick_preview/model-preview-reports-limits.jsonl]
related: [preview/preview-panel/media/video, preview/preview-panel/layout, preview/quick-preview, settings/themes]
---

## Summary

Sandboxed previews of local STL, 3MF, and FreeCAD models in the drawer and Quick Preview, for checking a 3D part without a CAD tool. Geometry renders in software; 3MF and FreeCAD files with a saved thumbnail show that image instead. Rendered models step through four preset camera views, guided by a top-down orbit indicator, with format and triangle-count badges. The node also owns the details header that G-code image previews share, and how a cancelled background STL thumbnail render is reaped.

## Behavior

### Rendering

- An STL file first renders from the Front left camera, looking diagonally down at the model, tinted with the theme accent. lgse/strata#1276, lgse/strata#1644
- Model previews in the drawer and Quick Preview keep the theme's opaque surface behind the model. lgse/strata#1789
- Changing the theme re-renders the open model preview with the new accent and keeps the selected camera view. lgse/strata#1276, lgse/strata#1644
- A 3MF file with exactly one usable embedded PNG shows that image; with none or several, its geometry renders. lgse/strata#1276
- A FreeCAD `.FCStd` file shows its saved thumbnail without FreeCAD installed. lgse/strata#1276
- A FreeCAD file without a usable thumbnail shows "This FreeCAD file has no usable embedded thumbnail" and renders no geometry. lgse/strata#1276 (unverified)
- A 3MF model split across several model parts shows "Multipart model detected. Unable to render preview." unless one usable embedded image exists. lgse/strata#1276
- An STL, 3MF, or FreeCAD model over 128 MiB or 2 million triangles shows a limit message instead of a render. lgse/strata#1276, lgse/strata#1864

### Camera views

- Selecting another file resets the camera view to Front left. lgse/strata#1644, lgse/strata#1633
- While camera views change, the header content type stays `model/stl` or `model/3mf`. lgse/strata#1644
- All four camera views of a model share one bounding-box fit on a square canvas, so switching views never changes its scale or centring. lgse/strata#1644
- Revisiting a camera view of the same model at the same size and theme is served from the preview cache. lgse/strata#1644
- A first visit to a camera view rereads and re-renders the mesh. lgse/strata#1644

- **Next model view** turns the camera clockwise: Front left, Back left, Back right, Front right, then wraps to Front left. lgse/strata#1644, lgse/strata#1764
- **Previous model view** turns it anticlockwise: from Front left it goes to Front right. lgse/strata#1644, lgse/strata#1764
- Only the two buttons change the view; no key binding does. lgse/strata#1644 (unverified)
- Once loaded, a 3MF with one usable embedded PNG, or a FreeCAD file, shows its saved image without camera buttons, indicator, or badges. lgse/strata#1644, lgse/strata#1633, lgse/strata#1764
- A local G-code file with an embedded thumbnail also shows its image without camera buttons, indicator, or badges. lgse/strata#1864

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
- A local G-code file loads with the same details and inactive camera controls; its badge reads "GCODE", "GCO", or "BGCODE". lgse/strata#1864 (unverified)
- No loading card covers the model; the header spinner left of Open is the only indicator, shown at once for first loads and view changes. lgse/strata#1764
- While another view renders, the last image stays at opacity 0.3 with a wait cursor. lgse/strata#1644
- The header spinner's accessible label reads "Loading preview…", then "Reading model…", "Rendering N triangles…", and "Finishing preview…"; embedded images read "Reading thumbnail…" instead of the count. lgse/strata#1276, lgse/strata#1644, lgse/strata#1764
- Clicking a camera button during a render is ignored; the button keeps focus and the drawer keeps the keys. lgse/strata#1644
- Selecting a non-model file mid-render stops and hides the header spinner. lgse/strata#1644 (unverified)
- Selecting another model file mid-render keeps the header spinner showing for that file's first load. lgse/strata#1764 (unverified)
- After the first image, a failed view render or image decode keeps the previous image and shows an error under the controls; the buttons retry. lgse/strata#1644, lgse/strata#1764
- A first load that fails shows "Preview unavailable" and its error in the drawer, with no camera controls. lgse/strata#1764

### Background thumbnail renders

- Cancelling a background STL thumbnail render, or passing its 12 s wall deadline, sends SIGKILL to the helper. The thumbnail worker and STL slot free without waiting for the helper to exit. lgse/strata#1789
- A background STL thumbnail render whose helper cannot be monitored is killed and freed the same way. lgse/strata#1789 (unverified)
- A detached waiter then reaps the helper. The helper's private output and file-operation hold stay alive until reaping and namespace cleanup finish. lgse/strata#1789

### Details

- A badge row above the controls shows "Binary STL", "ASCII STL", or "3MF", and a count such as "1 triangle" or "N triangles". lgse/strata#1644
- Above the file name, an eyebrow such as "2 of 4 in folder" gives the file's position among model files. lgse/strata#1644
- That position follows the listing's current sort and filter. lgse/strata#1644
- With search results in place of the listing, the eyebrow reads "N of M in results". lgse/strata#1644 (unverified)
- FreeCAD and thumbnail-only 3MF files count toward that total. lgse/strata#1644 (unverified)
- Local G-code files count toward that total too. lgse/strata#1864 (unverified)
- The model and its controls form one vertically centred block, so a taller window keeps them together. lgse/strata#1644
- The model picture keeps the grab cursor and file drag. lgse/strata#1633, lgse/strata#1644 (unverified)

## Design

- 3MF and FreeCAD prefer embedded thumbnails at the owner's request; geometry is the fallback (lgse/strata#1225).
- Camera views render on demand and share the 128 MiB preview cache, keyed by view. The single heavy-preview permit keeps four angles from multiplying peak memory (lgse/strata#1644, lgse/strata#1633).
- Preset views replace free rotation. Continuous rotation would need frequent software renders or a new interactive renderer; presets fit the sandboxed renderer (lgse/strata#1633).
- The controls borrow the video player: the play button becomes the camera dot, and previous and next step the camera. The orbit diagram carries the view, so no visible label is shown (lgse/strata#1633, lgse/strata#1644).
- The renderer and the indicator share the camera directions. View names follow the model axes: +X right, −Y front, +Z up (lgse/strata#1644).
- Badges reuse counts from the parse and render pass, so thumbnail previews never parse geometry for them. Dimensions and units are not shown (lgse/strata#1644).
- A header spinner replaced a loading card over the model. The buttons stay sensitive during view renders so focus and the keyboard-owner bar survive a render (lgse/strata#1644). They stay insensitive until the first image exists (lgse/strata#1764).
- A centred progress card returned for the first load, then was removed again because it flashed for small models. The header spinner carries the stage in its accessible label (lgse/strata#1764).
- Model badges take their own badge area in the shared player layout instead of the video timeline slot (lgse/strata#1764).
- Background STL thumbnail renders do not wait for a killed helper to be reaped. Otherwise a helper stuck in uninterruptible I/O on NFS, sshfs, or FUSE would hold the STL slot, a heavy slot, and a worker indefinitely. A brief overlap of two helpers was judged acceptable. Interactive Quick Preview keeps waiting for the helper to exit (lgse/strata#1789).
- The sandbox boundary rejects a mesh result that does not identify the requested view, so a stale render cannot show under the wrong camera. It also rejects a format mismatch, 0 triangles, more than 2 million, or an STL without mesh details (lgse/strata#1644).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |

## Known gaps

- Each first visit to a camera view rereads and reparses the mesh before a full CPU render; parsed meshes are not retained. lgse/strata#1644
- A killed STL thumbnail helper stuck in kernel I/O can overlap a later render until the kernel lets it exit. lgse/strata#1789
- A text G-code file without a thumbnail briefly shows the model loading view, with inactive camera controls, before its text arrives. lgse/strata#1864
