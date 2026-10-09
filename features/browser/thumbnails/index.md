---
title: Thumbnails
status: shipped
origin: {issue: lgse/strata#41, pr: lgse/strata#43}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: reviewed
code: [src/ui/thumbnail.rs, src/ui/thumbnail/viewport.rs, src/ui/thumbnail/slot.rs, src/sandbox_helper/appimage.rs]
tests: [src/ui/thumbnail/viewport/tests.rs, src/ui/thumbnail/slot/tests.rs, src/sandbox_helper/appimage/tests.rs]
docs: [docs/preview-sandbox.md]
related: [operations/trash, browser/view-modes, browser/search, devices/volumes/camera]
---

## Summary

Image previews in place of file icons in Columns, List, Icons, folder peeks, and search results. Every decode runs in the sandbox, visible rows first. Children: `browser/thumbnails/cache` (the freedesktop disk cache) and `browser/thumbnails/workers` (the sandbox worker pool and its Thumbnail workers setting). Camera photo thumbnails belong to `devices/volumes/camera`.

## Behavior

### Display and fallback

- A file shows its type icon while its thumbnail loads, and keeps it when rendering fails or the type is unsupported. lgse/strata#43
- Folders never get thumbnails and keep their folder icon. lgse/strata#43
- A file or folder with a custom icon shows that icon instead of a thumbnail. lgse/strata#294 (unverified)
- Ctrl+F filter results and recursive search results show thumbnails in Columns, List, and Icons, with none left over when the query changes. lgse/strata#548
- Inline-renaming a file without changing its extension, size, or modification time keeps its thumbnail without decoding again. lgse/strata#1148
- A fresh image decode fills the item's Icons caption with its source dimensions, such as `320×180`. lgse/strata#1081

### Formats

- PNG, JPEG, WebP, GIF, BMP, TIFF, SVG, HEIC, HEIF, AVIF, and JPEG XL files get thumbnails, provided a decoder for the format is installed. lgse/strata#881, lgse/strata#969
- SVG files get thumbnails without a gdk-pixbuf SVG loader: pooled workers render them with resvg, the one-shot fallback with ImageMagick. lgse/strata#881, lgse/strata#1222
- `.svgz` files keep their icon, since the thumbnail extension list omits them. lgse/strata#881 (unverified)
- Camera RAW files, such as `.ARW`, use the embedded camera preview before ImageMagick or gdk-pixbuf. lgse/strata#199
- PDF files and MP4, MKV, WebM, MOV, AVI, M4V, MPEG, MPG, and OGV videos get thumbnails. lgse/strata#57, lgse/strata#274 (unverified)
- MP3, FLAC, M4A, M4B, MKA, AIFF, AIF, and WMA files with embedded cover art show the art at its aspect ratio; files without art keep the audio icon. lgse/strata#1162
- Ogg, Opus, and WAV files never get album-art thumbnails. lgse/strata#1162
- An `.AppImage` shows its embedded `.DirIcon`, else the root `.desktop` entry's `Icon=` image; without `unsquashfs` or an icon it keeps the generic icon. lgse/strata#1077
- 3MF and FreeCAD files with exactly one usable embedded PNG show it; STL files and models with none or several keep their icon. lgse/strata#1276
- CBZ and CBR files show their first image in natural order, and EPUB files their declared cover; missing or damaged covers keep the icon. lgse/strata#1325

### Remote files

- Files on a GVfs share with a `gvfsd-fuse` mirror, such as `smb://`, get thumbnails after metadata loads; the location still shows the remote URI. lgse/strata#1080
- Files on a GVfs location without a local mirror keep their type icons. lgse/strata#1080

### Scheduling

- Only items in the viewport and a 25% margin around it are rendered; items further away wait until scrolled near. lgse/strata#274, lgse/strata#1081
- Visible items render in reading order, top to bottom, and scrolling re-ranks queued work toward the new viewport. lgse/strata#274, lgse/strata#1081
- Scrolling an item away or rebinding its row cancels its pending work, and a late result never appears on a recycled row. lgse/strata#57, lgse/strata#1081
- A file whose render failed is not retried for 30 seconds. lgse/strata#57

## Design

Codecs read attacker-controlled bytes merely by a file becoming visible, so no decoder runs in the Strata process (lgse/strata#6). Thumbnails are decoration after first paint: names and fallback icons paint on bind, and thumbnails never delay the listing (lgse/strata#516). [docs/preview-sandbox.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/preview-sandbox.md) carries the sandbox, limits, and scheduling model.

- Kinds are chosen by file extension. HEIC, AVIF, JPEG XL, and audio art joined that list by reusing existing renderers (lgse/strata#969, lgse/strata#1162). AppImage, model, and cover kinds added sandboxed extractors (lgse/strata#1077, lgse/strata#1276, lgse/strata#1325).
- Strata does not run external freedesktop `.thumbnailer` entries or Tumbler; each provider runs inside its own sandbox (lgse/strata#516, lgse/strata#1275).
- RAW thumbnails take the embedded camera JPEG first, since ImageMagick demosaics; the median fell from 550 ms to 16 ms per file (lgse/strata#199). Quick Preview keeps the demosaic-first order.
- Ogg, Opus, and WAV keep cover art in tags for which FFmpeg exposes no stream, so including them would start a decoder per song that cannot succeed (lgse/strata#1162).
- The in-memory cache keys by path, modification time, size, and the canonical 256 px edge. All views and icon sizes share one texture; it holds at most 256 entries and 64 MiB (lgse/strata#1081).
- Failures are cached for 30 seconds to stop retry loops on malformed files, and identical requests share one job (lgse/strata#57).
- Requests rank visible, then overscan, then offscreen. Offscreen work is demoted rather than run (lgse/strata#274). Ranking runs from idle or the frame clock, never inside GTK bind or layout callbacks (lgse/strata#1081).
- With two or more workers, RAW, PDF, video, audio-art, model, and cover jobs leave one render slot free for ordinary images (lgse/strata#1081).
- A GVfs FUSE path is a render input only; navigation and identity keep the URI (lgse/strata#1080).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
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
