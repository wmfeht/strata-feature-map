---
title: Preview panel
status: shipped
origin: {issue: null, pr: lgse/strata#17}
branch: null
reviewed_at: 965bd7ec74400734dbd0a5311ceefa05bea8dd63
review: draft
code: [src/ui/preview.rs, src/services/preview.rs, src/adapters/local_preview.rs, src/adapters/local_preview/remote.rs, src/ui/preview/components.rs, src/sandbox_helper/archive_cover.rs]
tests: [src/services/preview/tests.rs, src/adapters/local_preview/tests.rs, src/adapters/local_preview/tests/cover_preview.rs, src/adapters/local_preview/tests/remote_preview.rs, src/adapters/local_preview/remote/tests.rs, src/ui/preview/tests/pdf.rs, src/ui/preview/tests/operations.rs, src/sandbox_helper/archive_cover/tests.rs, tests/fixtures/documents/password-protected.pdf, tests/fixtures/documents/owner-restricted.pdf, tests/qa/scenarios/quick_preview/password-protected-pdf-reports-reason.jsonl, tests/qa/scenarios/quick_preview/pdf-zoom-keeps-text-size.jsonl, tests/qa/scenarios/quick_preview/preview-source-text-copies.jsonl, tests/qa/scenarios/preview_media_layout]
docs: [site/src/reference/preview-sandbox.md]
related: [preview/quick-preview, browser/thumbnails, browser/properties/raw-metadata, operations/archives/preview, operations/drag-and-drop]
---

## Summary

The drawer beside the file views that shows the selected file's contents. It shows text, images, PDFs, 3D models, G-code thumbnails, GPS routes, and comic or EPUB covers, with a header holding the Rendered/Source switch, Find, Open, Wrap, and Close. The browser and the file chooser share it. Children: `preview/preview-panel/layout` (sizing and placement), `preview/preview-panel/documents` (rendered documents), `preview/preview-panel/find` (find in the open preview), `preview/preview-panel/media` (audio and video), `preview/preview-panel/pdf` (PDF text selection), `preview/preview-panel/model-views` (STL, 3MF, and FreeCAD models with camera views), `preview/preview-panel/gcode` (embedded G-code thumbnails), `preview/preview-panel/routes` (GPX, FIT, and KML routes), and `preview/preview-panel/sandbox` (isolation of untrusted parsing).

## Behavior

### Which files preview

- A non-executable extensionless dotfile such as `.steampath` previews as plain text. lgse/strata#224
- On a location that is not sampled, an executable extensionless dotfile does not use this fallback. A local one whose first 8 KiB look like text still previews as text. lgse/strata#224, lgse/strata#1638 (unverified)
- A file whose name gives an uncertain type, such as `some notes`, opens in the preview; text content shows as text and other content shows "No visual preview". lgse/strata#965
- `.yaml`, `.yml`, and other `text/plain` subtypes preview as highlighted text with their type label, not "No visual preview". lgse/strata#1228
- A local file's first 8 KiB decide its preview family: a file named `.png` or `.mp4` holding plain text previews as source text. lgse/strata#1638
- A local `photo.txt` holding PNG bytes previews as an image, and `paper.txt` holding a PDF previews as a PDF. lgse/strata#1638
- A local MPEG transport stream named `recording.ts` previews as video. lgse/strata#1638
- A local raw stream named `.h264` or `.H264` previews as video, even where the MIME database types it `application/octet-stream`. lgse/strata#1901, lgse/strata#1861
- Raw streams named otherwise, such as `.h265`, `.hevc`, `.264`, or extensionless, preview as video only where the MIME database types them as video. lgse/strata#1901 (unverified)
- A text or empty file named `notes.h264` previews as text and is never handed to the media decoder. lgse/strata#1901
- A local binary file named `.json` or `.md` whose bytes match no previewable type shows "No visual preview" instead of text. lgse/strata#1638
- A local file named `.zip` or `.docx` holding text previews as text, not as an archive tree or rendered document. lgse/strata#1638
- A local file named `.odt` or `.ott` holding text also previews as text. lgse/strata#1834 (unverified)
- An SVG previews as an image although its bytes are text. lgse/strata#1638
- Local `app.ts`, `Component.tsx`, and `module.mts` files holding TypeScript preview as highlighted source, whatever the installed MIME database says. lgse/strata#1638, lgse/strata#1631
- A local file with an unsupported binary type previews as text when its first 8 KiB look like text. Workbook, 3D model, route (GPX, FIT, KML), CBZ, CBR, and EPUB names still route by extension. lgse/strata#1638, lgse/strata#1842 (unverified)
- Remote files are not sampled; an uncertain name takes the content type the location reports, otherwise the name decides. lgse/strata#1638 (unverified)
- On remote locations, PDFs, GIF images, audio, and video other than MOV and MP4 are not offered for preview. lgse/strata#834
- A remote `.gcode` file previews as text; only a local G-code file is read for its embedded thumbnail. lgse/strata#1864
- A remote GPX, FIT, or KML file offers no Quick preview; the loader refuses one with "Copy this route file locally before previewing it." lgse/strata#1842 (unverified)
- A local `.kml` or `.gpx` file previews as a route, never as XML text. lgse/strata#1842 (unverified)
- 3D models, comic covers, workbooks, DOCX, ODT, and OTT preview only from local files. lgse/strata#1276, lgse/strata#1325, lgse/strata#1834 (unverified)
- Selecting a remote XLS, XLSX, ODS, DOCX, ODT, or OTT file shows "No preview for this selection". Its context menu has no Quick preview item. lgse/strata#729, lgse/strata#1086, lgse/strata#1834 (unverified)
- Some remote files reveal their type only by content type. When it shows a workbook, DOCX, ODT, or OTT, the preview shows "Copy this file locally before previewing it". lgse/strata#729, lgse/strata#1086, lgse/strata#1834 (unverified)
- A remote file whose content type shows a PDF fails with "Remote PDF previews are not supported; copy the file locally first". lgse/strata#834 (unverified)
- A remote media file other than MOV or MP4 fails with "Copy this media format locally before previewing it". lgse/strata#834 (unverified)
- A remote 3D model fails with "Remote model previews are not supported; copy the file locally first". A remote cover fails with the same message for cover previews. lgse/strata#1276, lgse/strata#1325 (unverified)
- The item menu shows Quick preview only for files the preview supports. lgse/strata#385 (unverified)

### Text

- Text previews show at most the first 1 MiB of the file. lgse/strata#89
- A text preview cut at that limit shows "Preview limited to the first 1 MB". lgse/strata#89 (unverified)
- A text file starting with a UTF-16 LE or BE byte-order mark previews as decoded text. lgse/strata#1638
- **Toggle word wrap** in the header wraps text previews; the choice defaults to off, applies in every open window, and survives restart. lgse/strata#921
- Rendered DOCX, ODT, OTT, and workbook previews hide **Toggle word wrap**. lgse/strata#1086, lgse/strata#1834 (unverified)
- DOCX, ODT, and OTT paragraphs always wrap, with no horizontal scrollbar, whatever the wrap preference. lgse/strata#1834
- Text with a recognized language, or plain text within 128 KiB, 512 lines, and 2 KiB per line, opens in a source view. lgse/strata#187, lgse/strata#762
- That source view shows a caret. lgse/strata#1559, lgse/strata#1557
- In that source view, Shift+arrow keys select text and Ctrl+C copies it; the file stays read-only. lgse/strata#1559, lgse/strata#1557

### Images and PDFs

- Still images on GIO locations, including phone cameras, preview after the original streams to a private temporary file. lgse/strata#834
- A remote image over 64 MiB or a transfer over 30 seconds fails with an explanatory message. lgse/strata#834
- With four remote previews already transferring or decoding, another fails with "Too many remote previews are active; try again shortly". lgse/strata#834
- Changing selection or closing the preview cancels a remote transfer. lgse/strata#834
- Remote MOV and MP4 files up to 256 MiB play only after the download completes, within a 60-second deadline. lgse/strata#834
- A RAW name the MIME database types as `application/octet-stream`, such as `GOPR0001.GPR`, still previews as a RAW image. lgse/strata#1698
- A RAW file on a GIO location previews after the original streams to a private temporary file, like other still images. lgse/strata#1698 (unverified)
- PDF pages render at the preview pane's width, at most 1280 px, one page at a time across previews. lgse/strata#898, lgse/strata#823
- Queued PDF pages that leave the view are cancelled before rendering. lgse/strata#898
- Ctrl+wheel over a PDF, including its scrollbars, zooms its pages between 1× and 4× its fitted width; interface text size does not change. lgse/strata#1069, lgse/strata#1622 (unverified)
- With keyboard focus in a zoomed PDF, Ctrl+0 returns its pages to fitted width on the same page; interface text size does not change. lgse/strata#1622
- With Num Lock on, Ctrl+keypad 0 also resets a focused PDF's zoom. lgse/strata#1622 (unverified)
- Ctrl+0 on a focused PDF already at fitted width is consumed and does not reset interface text size. lgse/strata#1622
- In 10xer mode, Ctrl+0 on a focused zoomed PDF also resets its zoom. lgse/strata#1622
- With focus in a PDF, Ctrl+Alt+0 and Ctrl+Super+0 leave its zoom unchanged. lgse/strata#1576
- A PDF that needs an opening password, such as `password-protected.pdf`, shows "Preview unavailable" and "This PDF is password protected." with no password field. lgse/strata#1840, lgse/strata#1636
- Under that message, an **Open** button hands the PDF to the default application. The file chooser shows the message without the button. lgse/strata#1840
- Other preview failures, such as a damaged PDF, show no Open button under the message. lgse/strata#1840

### Covers and G-code

- CBZ and CBR files show their first naturally ordered image, and EPUB files their declared cover; a file without one shows an error. lgse/strata#1325
- A local text `.gcode` or `.gco` file without a usable embedded thumbnail previews as its text. lgse/strata#1864
- Changing the theme while a narrow window hides a model or route preview reloads it with the new theme when the window widens again. lgse/strata#1842

### Media stepping

- In Icons, media previous and next skip an audio entry whose metadata fill found no duration. lgse/strata#1638, lgse/strata#1901 (unverified)
- In Icons, media previous and next skip a video entry with neither duration nor known dimensions, such as text named `clip.mp4`. lgse/strata#1638, lgse/strata#1901 (unverified)
- Media previous and next, and the position count, keep a video with known dimensions but no duration, such as a raw `.h264` stream. lgse/strata#1901

### Media controls

- On the plain media bar, as for an animated GIF, the play button's tooltip and accessible name read "Play/Pause" and its shortcut in parentheses. lgse/strata#1895 (unverified)
- The mute button's tooltip and accessible name read "Mute/unmute" followed by its shortcut in parentheses. lgse/strata#1895 (unverified)

### File operations

- A file operation that changes the previewed item or a folder holding it clears the preview first, in the browser and the file chooser. lgse/strata#1729
- Renaming or deleting the folder of a song or video playing in the preview stops playback. lgse/strata#1729
- A file operation on a sibling of the previewed file leaves the preview showing and playing. lgse/strata#1729 (unverified)
- After a rename of the previewed item or its folder, the preview shows the item at its new name once the operation ends. lgse/strata#1729
- A preview refused with "This item is being changed by a file operation." after that operation ended loads again at once. lgse/strata#1729
- A preview refused while an operation is still releasing shows "Preview unavailable" with that message, then reloads the focused entry when the operation ends. lgse/strata#1729 (unverified)

### Header

- The close button's tooltip and accessible name read "Close preview (Space)", or "Close preview (i)" in 10xer mode. lgse/strata#1576
- The header has no Print button for any file, including PDFs, images, and text. lgse/strata#1950

## Design

[docs/preview-sandbox.md](https://github.com/lgse/strata/blob/d6c74746cdb27e506a08e8cdefa3bc8cef7d10f9/docs/preview-sandbox.md) documents the providers, the remote still-image boundary, password-protected PDFs, model limits, and route previews. Children inherit it.

- Every browsed file is untrusted. Native parsing runs in the sandbox, and only bounded PNG, text, or validated JSON reaches the drawer (lgse/strata#6).
- Eligibility is guessed from the name so listing stays cheap. An uncertain guess defers to the loader, which queries the content type of the one previewed file; listing and sorting stay name-only (lgse/strata#964).
- The loader also reads the first 8 KiB of every local file, and the bytes override the name's family. shared-mime-info maps `*.ts` to TypeScript, Qt Linguist, and MPEG-TS. A confident name match had skipped sniffing (lgse/strata#1638).
- Special-casing TypeScript would fix one collision only. Quick preview, menus, and the chooser still gate on the name; the loader resolves the final family (lgse/strata#1638).
- The dotfile fallback uses the Unix mode rather than an allowlist of names such as `.steampath`, so arbitrary application dotfiles work (lgse/strata#223).
- Rendered previews are cached in memory, at most 64 entries and 128 MiB with LRU eviction (lgse/strata#318). Remote previews are never cached.
- PDF pages once rendered concurrently per visible row, spawning over 100 helpers while scrolling (lgse/strata#815). Rendering at viewport width and serializing pages cut helper RSS from about 411 to 112 MiB (lgse/strata#898).
- Word processors store each paragraph as one line, so unwrapped DOCX and ODT showed one line per paragraph behind a horizontal scrollbar. Both now always wrap; workbook tables keep their layout (lgse/strata#1834).
- Models, PDFs, workbooks, DOCX, ODT, and routes share one process-wide heavy-preview permit and use one-shot sandboxes (lgse/strata#1276, lgse/strata#1834, lgse/strata#1842). Comic and EPUB covers take the same permit (lgse/strata#1325) (unverified).
- A hidden caret in a read-only GtkSourceView disables native Shift+arrow selection, so source previews show the caret and stay non-editable (lgse/strata#1557).
- PDF zoom reset skips the view-center correction, because the list view re-anchors the visible page itself; correcting it jumped to page 1 (lgse/strata#1622).
- Ctrl+0 on a focused PDF is consumed even at fitted width, so a reset meant for the page never resets the saved text size (lgse/strata#1622).
- A password-protected PDF gets an explanation, not an unlock prompt, at the owner's request. Strata never asks for, stores, or submits PDF passwords, and never writes an unlocked copy (lgse/strata#1636, lgse/strata#1840).
- The Open button reuses the header's Open action, so the file chooser, which never opens files externally, hides it (lgse/strata#1840).
- Remote originals stream to a random mode-0600 file, keeping a short alphanumeric extension only, so remote names never choose a local path. Remote PDFs stay unsupported until a shared document snapshot can serve every page without repeated downloads (lgse/strata#833, lgse/strata#834).
- G-code joined the model formats, which preview only from local files. Remote G-code would have lost its text preview, so it stays text (lgse/strata#1864).
- Route previews use the preview cache keyed by format and theme palette (lgse/strata#1842).
- Audio, video, and model previews share a details header and navigation row; video and model also share a badge row and a player layout with named areas. One universal player was rejected because artwork, the spectrum, and the camera need different content; playback, seeking, camera motion, and loading stay per preview (lgse/strata#1659, lgse/strata#1764).
- `.h264` is recognized by name in the shared filename classifier, before the MIME database. The byte-content guards and the sandboxed decoder are reused, with no new decoder or file reads. One classifier keeps preview, navigation, and Properties in agreement (lgse/strata#1901, lgse/strata#1861).
- Elementary streams can have known dimensions but no duration, so navigation keeps a video with known dimensions even without a duration (lgse/strata#1901).
- Printing was removed: a file's default application prints it. PDF pages had printed rasterized at the pane's on-screen size, at low quality (lgse/strata#1950, lgse/strata#1931).
- The stream-copy video and native GIF paths from lgse/strata#318 were replaced by sandboxed streaming (lgse/strata#839).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-30 | lgse/strata#1950 | feat | Removed printing: the header and item-menu Print, the PDF print-progress dialog and print errors; files print from their default application. |
| 2026-10-27 | lgse/strata#1901 | fix | Broke long rendered paragraphs after whitespace, decoded RTF surrogate pairs, and recognized `.h264` by name so raw streams preview and step. |
| 2026-10-25 | lgse/strata#1842 | feat | Added offline GPX, FIT, and KML route previews with an elevation profile, playback, and a saved Units preference. |
| 2026-10-25 | lgse/strata#1864 | feat | Showed the embedded slicer thumbnail of `.gcode`, `.gco`, and `.bgcode` files in the preview, keeping text for files without one. |
| 2026-10-24 | lgse/strata#1840 | fix | Explained password-protected PDF failures with a translated message and an Open button, instead of the generic renderer error. |
| 2026-10-24 | lgse/strata#1834 | feat | Rendered ODT and OTT documents with a sandboxed `quick-xml` reader feeding the DOCX HTML path, and always wrapped DOCX and ODT paragraphs. |
| 2026-10-20 | lgse/strata#1752 | fix | Tracked document preview scrollbars in document positions so held, dragged, and touchpad-scrolled thumbs stop jumping; deferred hidden rendered rows and cut source and table overhead. |
| 2026-10-20 | lgse/strata#1764 | refactor | Shared the media preview header, navigation, badges, and layout; Next now turns the model camera clockwise and mesh details show during the first render. |
| 2026-10-18 | lgse/strata#1644 | feat | Added four camera views, an orbit indicator, and mesh badges to rendered STL and 3MF previews, so every side of a model can be seen. |
| 2026-10-15 | lgse/strata#1684 | fix | Kept focus in the listing when the cursor moves onto an archive with the preview open; only explicit entry focuses the password field or highlights a member. |
| 2026-10-14 | lgse/strata#1612 | fix | Let unwrapped rendered documents scroll horizontally from the left edge and remeasured rows after live wrap toggles. |
| 2026-10-14 | lgse/strata#1622 | fix | Kept PDF zoom separate from interface text size: Ctrl+wheel over a PDF and Ctrl+0 on a focused PDF now act on the page. |
| 2026-10-14 | lgse/strata#1638 | fix | Chose the preview family from the first 8 KiB of a file, so TypeScript and other misnamed text no longer open as media. |
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

- Images cannot be rotated in the preview. lgse/strata#987
- A growing log file does not update while previewed. lgse/strata#847
- The volume slider and the plain media bar's seek slider have no accessible name. Naming them needs new strings in every catalog. lgse/strata#1896
- Remote PDFs, GIFs, audio, and other video formats must be copied locally to preview. lgse/strata#834
- With a PDF focused, Ctrl++ and Ctrl+− change interface text size, not PDF zoom; PDF zoom for them is a possible follow-up. lgse/strata#1622
