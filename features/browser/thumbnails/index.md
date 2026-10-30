---
title: Thumbnails
status: shipped
origin: {issue: lgse/strata#41, pr: lgse/strata#43}
branch: null
reviewed_at: 41070b59c09f21eba33918c1e99be2eb3047de7e
review: draft
code: [src/ui/thumbnail.rs, src/ui/thumbnail/viewport.rs, src/ui/thumbnail/slot.rs, src/sandbox_helper/appimage.rs]
tests: [src/ui/thumbnail/tests.rs, tests/qa/mutations/stl-thumbnails-live-preference.patch, src/ui/thumbnail/viewport/tests.rs, src/ui/thumbnail/viewport/tests/folder_counts.rs, src/ui/thumbnail/slot/tests.rs, src/sandbox_helper/appimage/tests.rs]
docs: [site/src/reference/preview-sandbox.md, docs/preview-sandbox.md]
related: [operations/trash, browser/view-modes, browser/search, devices/volumes/camera, browser/properties/raw-metadata, preview/preview-panel/sandbox, preview/preview-panel/gcode]
---

## Summary

Image previews in place of file icons in Columns, List, Icons, folder peeks, and search results. Every decode runs in the sandbox, visible rows first. Children: `browser/thumbnails/cache` (the freedesktop disk cache) and `browser/thumbnails/workers` (the sandbox worker pool and its Thumbnail workers setting). Camera photo thumbnails belong to `devices/volumes/camera`.

## Behavior

### Display and fallback

- A file shows its type icon while its thumbnail loads, and keeps it when rendering fails or the type is unsupported. lgse/strata#43
- Folders never get thumbnails and keep their folder icon. lgse/strata#43
- A file or folder with a custom icon shows that icon instead of a thumbnail. lgse/strata#294 (unverified)
- Files in a folder opened through `admin://` get no thumbnail and show their type icon. lgse/strata#1837
- A metadata fill can find a shown folder locked. Its row in Columns, List, or Icons then swaps to the lock icon in place. lgse/strata#1837
- A locked folder with a custom icon keeps that icon. lgse/strata#1837 (unverified)
- Ctrl+F filter results and recursive search results show thumbnails in Columns, List, and Icons, with none left over when the query changes. lgse/strata#548
- Inline-renaming a file without changing its extension, size, or modification time keeps its thumbnail without decoding again. lgse/strata#1148
- A fresh image decode fills the item's Icons caption with its source dimensions, such as `320×180`. lgse/strata#1081
- A RAW file's Icons caption shows the full image size after orientation, not the size of its embedded 160×120 thumbnail. lgse/strata#1698
- A portrait DNG with a 6016×4000 crop shows `4000×6016`. lgse/strata#1698

### Show thumbnails off

- With **Show thumbnails** off, files show their file-type icons instead of thumbnails in Columns, List, Icons, search and filter results, folder peeks, and the portal chooser. lgse/strata#1651
- Turning it off updates open windows and rebuilt views at once; the saved choice applies before Settings opens. lgse/strata#1651
- Turning it off cancels pending thumbnail requests; new requests read no cache and decode nothing. lgse/strata#1651
- Turning it back on restores thumbnails for rows still bound. lgse/strata#1651
- Toggling it, even off and on quickly, keeps pending dimension and duration updates such as the Icons caption `320×180`. lgse/strata#1651
- After a toggle, rebinding or unbinding a row still discards that row's stale updates. lgse/strata#1651
- Custom icons and the preview panel are unchanged: Space still opens a preview with thumbnails off. lgse/strata#1651

### Formats

- PNG, JPEG, WebP, GIF, BMP, TIFF, SVG, HEIC, HEIF, AVIF, and JPEG XL files get thumbnails, provided a decoder for the format is installed. lgse/strata#881, lgse/strata#969
- SVG files get thumbnails without a gdk-pixbuf SVG loader: pooled workers render them with resvg, the one-shot fallback with ImageMagick. lgse/strata#881, lgse/strata#1222
- `.svgz` files keep their icon, since the thumbnail extension list omits them. lgse/strata#881 (unverified)
- Camera RAW thumbnails, such as for `.ARW`, use the embedded camera preview first, then gdk-pixbuf, then ImageMagick. lgse/strata#199 (unverified)
- RAW thumbnails of portrait shots are upright in Columns, List, and Icons. lgse/strata#1698
- Every extension `browser/properties/raw-metadata` recognizes as RAW gets a RAW thumbnail in any case, including `.RAF`, `.GPR`, `.IIQ`, and `.CRW`. lgse/strata#1698
- PDF files and MP4, MKV, WebM, MOV, AVI, M4V, MPEG, MPG, and OGV videos get thumbnails. lgse/strata#57, lgse/strata#274 (unverified)
- MP3, FLAC, M4A, M4B, MKA, AIFF, AIF, and WMA files with embedded cover art show the art at its aspect ratio; files without art keep the audio icon. lgse/strata#1162
- Ogg, Opus, and WAV files never get album-art thumbnails. lgse/strata#1162
- An `.AppImage` shows its embedded `.DirIcon`, else the root `.desktop` entry's `Icon=` image; without `unsquashfs` or an icon it keeps the generic icon. lgse/strata#1077
- 3MF and FreeCAD files with exactly one usable embedded PNG show it; models with none or several keep their icon. lgse/strata#1276, lgse/strata#1789
- With Show thumbnails on, `.gcode`, `.gco`, and `.bgcode` files show their embedded PNG, JPEG, or QOI slicer thumbnail as the file icon. lgse/strata#1864
- G-code thumbnails appear whenever Show thumbnails is on, whether STL model thumbnails is on or off. lgse/strata#1864
- A G-code file with no usable embedded image keeps its file icon. lgse/strata#1864
- CBZ and CBR files show their first image in natural order, and EPUB files their declared cover; missing or damaged covers keep the icon. lgse/strata#1325

### STL model thumbnails

- With default settings, a local `.stl` file keeps its file-type icon, and nothing is rendered or cached. lgse/strata#1789
- With **Show thumbnails** and **STL model thumbnails** both on, a local `.stl` file shows a 256×256 rendered model in its tile. lgse/strata#1789
- The render has a transparent background and is written to the shared `thumbnails/large` cache. lgse/strata#1789
- The render uses the default camera view and neutral `#cccccc` shading, whatever the theme. lgse/strata#1789 (unverified)
- The extension match ignores case, so `.STL` files render too. lgse/strata#1789 (unverified)
- The rendered model shows in Columns, List, Icons, search and filter results, folder peeks, and the portal chooser. lgse/strata#1789
- Turning **STL model thumbnails** off hides STL artwork in every open window at once and cancels pending STL requests; turning it on restores it. lgse/strata#1789
- Turning **STL model thumbnails** off leaves image and other thumbnails shown. lgse/strata#1789
- Turning **STL model thumbnails** off leaves rendered PNGs in `thumbnails/large`, where other freedesktop clients can still show them. lgse/strata#1789
- An STL file on a GVfs share with a FUSE mirror, or on a gphoto2 camera, keeps its icon with both switches on. lgse/strata#1789
- A truncated binary STL, an STL over 128 MiB, or one over 2,000,000 triangles keeps its icon and stays listed. lgse/strata#1789

### Remote files

- Files on a GVfs share with a `gvfsd-fuse` mirror, such as `smb://`, get thumbnails after metadata loads; the location still shows the remote URI. lgse/strata#1080
- Files on a GVfs location without a local mirror keep their type icons. lgse/strata#1080

### Scheduling

- Only items in the viewport and a 25% margin around it are rendered; items further away wait until scrolled near. lgse/strata#274, lgse/strata#1081
- Visible items render in reading order, top to bottom, and scrolling re-ranks queued work toward the new viewport. lgse/strata#274, lgse/strata#1081
- Scrolling an item away or rebinding its row cancels its pending work, and a late result never appears on a recycled row. lgse/strata#57, lgse/strata#1081
- A file whose render failed is not retried for 30 seconds. lgse/strata#57
- A thumbnail that a file operation stopped is not cached as failed; it is requested again once the operation ends. lgse/strata#1729
- When a file operation ends, only folders in the viewport and its margin are recounted; offscreen folders are not. lgse/strata#1937
- An offscreen folder whose count an operation changed is recounted once scrolled into view. lgse/strata#1937 (unverified)
- A folder that two overlapping operations write into is recounted only after the last one ends. lgse/strata#1937
- After a sibling sorting before the target is created or removed, a drop still updates the target's own count. lgse/strata#1937

## Design

Codecs read attacker-controlled bytes merely by a file becoming visible, so no decoder runs in the Strata process (lgse/strata#6). Thumbnails are decoration after first paint: names and fallback icons paint on bind, and thumbnails never delay the listing (lgse/strata#516). [docs/preview-sandbox.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/preview-sandbox.md) carries the sandbox, limits, and scheduling model.

- Kinds are chosen by file extension. HEIC, AVIF, JPEG XL, and audio art joined that list by reusing existing renderers (lgse/strata#969, lgse/strata#1162). AppImage, model, and cover kinds added sandboxed extractors (lgse/strata#1077, lgse/strata#1276, lgse/strata#1325).
- Strata does not run external freedesktop `.thumbnailer` entries or Tumbler; each provider runs inside its own sandbox (lgse/strata#516, lgse/strata#1275).
- RAW thumbnails take the embedded camera JPEG first, since ImageMagick demosaics; the median fell from 550 ms to 16 ms per file (lgse/strata#199). Thumbnails keep gdk-pixbuf ahead of ImageMagick, because ImageMagick would demosaic every RAW in a folder. Previews now also take the embedded JPEG first (lgse/strata#1666, lgse/strata#1698).
- Ogg, Opus, and WAV keep cover art in tags for which FFmpeg exposes no stream, so including them would start a decoder per song that cannot succeed (lgse/strata#1162).
- The in-memory cache keys by path, modification time, size, and the canonical 256 px edge. All views and icon sizes share one texture; it holds at most 256 entries and 64 MiB (lgse/strata#1081).
- Failures are cached for 30 seconds to stop retry loops on malformed files, and identical requests share one job (lgse/strata#57).
- Requests rank visible, then overscan, then offscreen. Offscreen work is demoted rather than run (lgse/strata#274). Ranking runs from idle or the frame clock, never inside GTK bind or layout callbacks (lgse/strata#1081).
- With two or more workers, RAW, PDF, video, audio-art, model, and cover jobs leave one render slot free for ordinary images (lgse/strata#1081).
- STL rendering in file tiles is opt-in. lgse/strata#1276 kept geometry out of browser thumbnails; lgse/strata#1788 proposed a bounded opt-in extension that reuses the sandboxed software renderer and the PNG cache.
- External thumbnailers were rejected: they need installing and do not fit Strata's provider architecture (lgse/strata#1788).
- STL renders have a transparent background because the shared freedesktop cache must not depend on the theme ([review](https://github.com/lgse/strata/pull/1789#issuecomment-6306979921)).
- Disabling the switch keeps cached PNGs, like **Show thumbnails**. A private cache was offered only if renders had to be hidden from other clients, and not adopted ([review](https://github.com/lgse/strata/pull/1789#issuecomment-6306979921)).
- **Show thumbnails** is an explicit switch. Zero workers as a hidden off switch and deleting cached files were rejected as workarounds (lgse/strata#1664).
- Files in `admin://` folders get no thumbnails. A root-only image would persist in `~/.cache/thumbnails`, readable by any user process, and background reads could raise an unasked polkit prompt (lgse/strata#1836, lgse/strata#1837).
- A fallback icon's height scale is cached per texture, weakly keyed and pruned at 512 entries, instead of scanning the texture on each icon change (lgse/strata#1675).
- A GVfs FUSE path is a render input only; navigation and identity keep the URI (lgse/strata#1080).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-15 | lgse/strata#1651 | feat | Added the saved Show thumbnails switch, which shows file-type icons and stops thumbnail work while keeping previews. |
| 2026-10-15 | lgse/strata#1675 | perf | Cached a fallback icon's height scale per texture instead of scanning the texture on each icon change. |
| 2026-10-10 | lgse/strata#1554 | fix | Refreshed customized icons under relocated folders, so colors and icons follow moves made in Strata. |
| 2026-09-29 | lgse/strata#1325 | feat | Added CBZ, CBR, and EPUB cover thumbnails, extracted inside the sandbox. |
| 2026-09-23 | lgse/strata#1162 | feat | Added album-art thumbnails for audio containers whose art FFmpeg exposes. |
| 2026-09-17 | lgse/strata#1080 | fix | Rendered GVfs-backed files through their local FUSE mirror when one exists. |
| 2026-09-17 | lgse/strata#1077 | feat | Rendered AppImage embedded icons as thumbnails, since many icon themes lack an AppImage icon. |
| 2026-09-13 | lgse/strata#969 | fix | Added HEIC, HEIF, AVIF, and JPEG XL to the thumbnail extensions. |
| 2026-09-12 | lgse/strata#881 | fix | Added SVG to the thumbnail extensions and routed image thumbnails through the fallback chain. |
| 2026-09-07 | lgse/strata#548 | fix | Restored thumbnails in Ctrl+F filter and search results in every view mode. |
| 2026-09-03 | lgse/strata#199 | perf | Tried the embedded camera preview first for RAW thumbnails. |
| 2026-08-31 | lgse/strata#57 | perf | Bounded the thumbnail queue, cancelled offscreen work, and cached failures for 30 seconds. |
| 2026-08-31 | lgse/strata#43 | feat | Showed thumbnails in folder peek popovers and search results. |

## Known gaps

- Under Flatpak the sandbox helper cannot create namespaces, so no native-format thumbnails render. lgse/strata#1503
- Thumbnail reads bypass the mount request lanes. A thumbnail of a file on a dead mount waits until the server answers. lgse/strata#1729
