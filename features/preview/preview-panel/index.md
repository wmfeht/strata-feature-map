---
title: Preview panel
status: shipped
origin: {issue: null, pr: lgse/strata#17}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: reviewed
code: [src/ui/preview.rs, src/services/preview.rs, src/adapters/local_preview.rs, src/adapters/local_preview/remote.rs, src/ui/preview/pdf_text.rs, src/services/model_preview.rs, src/sandbox_helper/model.rs, src/sandbox_helper/model/embedded.rs, src/sandbox_helper/archive_cover.rs]
tests: [src/services/preview/tests.rs, src/adapters/local_preview/tests.rs, src/adapters/local_preview/tests/model_preview.rs, src/adapters/local_preview/tests/cover_preview.rs, src/adapters/local_preview/tests/remote_preview.rs, src/adapters/local_preview/remote/tests.rs, src/ui/preview/pdf_text/tests.rs, src/ui/preview/pdf_ranges_tests.rs, src/sandbox_helper/model/tests.rs, src/sandbox_helper/model/embedded/tests.rs, src/sandbox_helper/archive_cover/tests.rs, tests/e2e/scenarios/test_preview_media_layout.py]
docs: [docs/preview-sandbox.md]
related: [preview/quick-preview, browser/thumbnails, browser/properties/raw-metadata, operations/archives/preview, operations/drag-and-drop]
---

## Summary

The drawer beside the file views that shows the selected file's contents: text, images, PDFs, 3D models, and comic or EPUB covers, with a header for print and close. The browser and the file chooser share it. Children: `preview/preview-panel/layout` (sizing and placement), `preview/preview-panel/documents` (rendered documents), `preview/preview-panel/media` (audio and video), and `preview/preview-panel/sandbox` (isolation of untrusted parsing).

## Behavior

### Which files preview

- A non-executable extensionless dotfile such as `.steampath` previews as plain text; an executable one does not use this fallback. lgse/strata#224
- A file whose name gives an uncertain type, such as `some notes`, opens in the preview; text content shows as text and other content shows "No visual preview". lgse/strata#965
- `.yaml`, `.yml`, and other `text/plain` subtypes preview as highlighted text with their type label, not "No visual preview". lgse/strata#1228
- On remote locations, PDFs, GIF images, audio, and video other than MOV and MP4 are not offered for preview. lgse/strata#834
- 3D models, comic covers, workbooks, and DOCX preview only from local files. lgse/strata#1276, lgse/strata#1325 (unverified)

### Text

- Text previews show at most the first 1 MiB of the file. lgse/strata#89
- **Toggle word wrap** in the header wraps text previews; the choice defaults to off, applies in every open window, and survives restart. lgse/strata#921

### Images and PDFs

- Still images on GIO locations, including phone cameras, preview after the original streams to a private temporary file. lgse/strata#834
- A remote image over 64 MiB or a transfer over 30 seconds fails with an explanatory message. lgse/strata#834
- With four remote previews already transferring or decoding, another fails with "Too many remote previews are active; try again shortly". lgse/strata#834
- Changing selection or closing the preview cancels a remote transfer. lgse/strata#834
- Remote MOV and MP4 files up to 256 MiB play only after the download completes, within a 60-second deadline. lgse/strata#834
- PDF pages render at the preview's width, one at a time, and pages scrolled out of view before rendering are cancelled. lgse/strata#898
- Dragging across PDF text selects it, and Ctrl+C copies it in page order with its line breaks. lgse/strata#1223
- In a PDF, double-click selects a word, triple-click a line, Shift+click extends across pages, and Ctrl+A selects all loaded pages. lgse/strata#1223
- Dragging on a PDF margin or a page without a text layer, such as a scan, pans instead of selecting. lgse/strata#1223
- Ctrl+wheel over a PDF zooms its pages between 1× and 4× its fitted width, and Ctrl+0 resets the zoom. lgse/strata#1069 (unverified)

### Models and covers

- An STL file renders at a fixed three-quarter angle, tinted with the theme accent; changing the theme re-renders the open preview. lgse/strata#1276
- A 3MF file with exactly one usable embedded PNG shows that image; with none or several, its geometry renders. lgse/strata#1276
- A FreeCAD `.FCStd` file shows its saved thumbnail without FreeCAD installed. lgse/strata#1276
- A 3MF model split across several model parts shows "Multipart model detected. Unable to render preview." unless one usable embedded image exists. lgse/strata#1276
- A model over 128 MiB or 2 million triangles shows a limit message instead of a render. lgse/strata#1276
- While a model loads, the drawer shows "Reading model…", "Rendering N triangles…", then "Finishing preview…"; embedded images show "Reading thumbnail…" instead of the count. lgse/strata#1276
- CBZ and CBR files show their first naturally ordered image, and EPUB files their declared cover; a file without one shows an error. lgse/strata#1325

### Printing

- **Print** in the preview header and the item menu opens the system print dialog for that file. lgse/strata#286
- Print on an extensionless file the loader cannot render shows "This file type cannot be printed." lgse/strata#965
- Printing a PDF shows "Preparing PDF" with page progress while every page renders; Cancel or Escape stops it. lgse/strata#286 (unverified)
- Printing a text file over 16 MiB shows "This text file is too large to print safely." lgse/strata#286 (unverified)

## Design

[docs/preview-sandbox.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/preview-sandbox.md) documents the providers, the remote still-image boundary, and model limits. Children inherit it.

- Every browsed file is untrusted. Native parsing runs in the sandbox, and only bounded PNG, text, or validated JSON reaches the drawer (lgse/strata#6).
- Eligibility is guessed from the name so listing stays cheap. An uncertain guess defers to the loader, which queries the content type of the one previewed file; listing and sorting stay name-only (lgse/strata#964).
- The dotfile fallback uses the Unix mode rather than an allowlist of names such as `.steampath`, so arbitrary application dotfiles work (lgse/strata#223).
- Rendered previews are cached in memory, at most 64 entries and 128 MiB with LRU eviction (lgse/strata#318). Remote previews are never cached.
- PDF pages once rendered concurrently per visible row, spawning over 100 helpers while scrolling (lgse/strata#815). Rendering at viewport width and serializing pages cut helper RSS from about 411 to 112 MiB (lgse/strata#898).
- Models, PDFs, workbooks, and DOCX share one process-wide heavy-preview permit and use one-shot sandboxes (lgse/strata#1276). Comic and EPUB covers take the same permit (lgse/strata#1325) (unverified).
- PDFs render in the sandbox, so the text layer travels with each page as a bounded sidecar to the PNG (lgse/strata#1220, lgse/strata#1223).
- Remote originals stream to a random mode-0600 file, keeping a short alphanumeric extension only, so remote names never choose a local path. Remote PDFs stay unsupported until a shared document snapshot can serve every page without repeated downloads (lgse/strata#833).
- 3MF and FreeCAD prefer embedded thumbnails at the owner's request; geometry is the fallback (lgse/strata#1225).
- The stream-copy video and native GIF paths from lgse/strata#318 were replaced by sandboxed streaming (lgse/strata#839).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-27 | lgse/strata#1276 | feat | Added sandboxed STL, 3MF, and FreeCAD previews with staged progress text. |
| 2026-09-26 | lgse/strata#1228 | fix | Rendered YAML and other `text/plain` subtypes as text previews. |
| 2026-09-25 | lgse/strata#1223 | feat | Added a sandbox-extracted text layer so PDF text can be selected and copied. |
| 2026-09-14 | lgse/strata#965 | fix | Let files with uncertain name-based types reach the preview loader and Print. |
| 2026-09-13 | lgse/strata#921 | feat | Added a saved word-wrap toggle for text previews. |
| 2026-09-12 | lgse/strata#898 | perf | Rendered PDF pages at viewport width and serialized sandboxed page renders. |
| 2026-09-10 | lgse/strata#318 | perf | Sped up preview loading with faster PNG encoding and a bounded 128 MiB preview cache. |
| 2026-09-04 | lgse/strata#286 | feat | Added Print to the preview header and item menu. |
| 2026-09-03 | lgse/strata#224 | feat | Previewed non-executable extensionless dotfiles as text. |

## Known gaps

- Images cannot be rotated in the preview; the change is unmerged. lgse/strata#987, lgse/strata#1388
- A click on empty space or a disabled control in the preview pane deselects the file and blanks the preview; the fix is unmerged. lgse/strata#1450, lgse/strata#1546
- A growing log file does not update while previewed. lgse/strata#847
- Remote PDFs, GIFs, audio, and other video formats must be copied locally to preview. lgse/strata#833
