---
title: Themed icons
status: shipped
origin: {issue: lgse/strata#169, pr: lgse/strata#170}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [src/assets.rs, src/assets/vector.rs, data/icons/scalable/actions/strata-lang-*.svg]
tests: [src/assets/tests.rs, src/assets/vector/tests.rs, src/ui/browser/entry/tests.rs]
related: [browser/view-modes/icons]
---

## Summary

Strata's bundled interface and file-type icons, tinted with the active theme's colors and rasterized at the size and density they are drawn. Covers icon coloring, chrome icon sizing, stroke weight, file-type icon choice, and the icon texture cache.

## Behavior

### Color

- Header, sidebar, settings navigation, and file-type icons draw in the theme's accent color at full opacity. lgse/strata#170
- Changing the theme or Omarchy variant recolors icons in every open window without reopening them. lgse/strata#1482
- Destructive menu items, such as Permanently delete, and danger-tone dialogs draw their icon in the theme's danger color. lgse/strata#1210 (unverified)

### Size and weight

- Header-bar and pane action icons draw at 16 logical px at the default text size, centered, even when the desktop theme gives buttons extra space. lgse/strata#497
- Chrome icons rasterize at twice their logical size; file, sidebar, and dialog icons rasterize at 96 px or their device-pixel size, whichever is larger. lgse/strata#497, lgse/strata#1416
- In the Icons view, outlines draw at half the stroke weight of list, toolbar, and sidebar icons at every size. lgse/strata#1416
- Above 64 logical px, strokes scale by (64 ÷ size)^0.35, about 0.62× at 256 px, so large icons do not read as bold. lgse/strata#1416
- Icons rasterize at the display's pixel density, so 2× displays get sharp strokes. lgse/strata#1416

### File-type icons

- Source files in 42 languages, such as `.rs`, `.py`, `.go`, `.java`, and `.kt`, show a language glyph in the accent color. lgse/strata#1529
- `.m`, `.v`, and brandless languages such as assembly and Tcl keep the generic code icon. lgse/strata#1529
- Search results use the same file-type icons as Columns, List, and Icons views. lgse/strata#1529
- Archives such as `.zip` show an archive icon distinct from folders. lgse/strata#1416
- Spreadsheets, presentations, fonts, databases, disk images, keys, and shell scripts each show their own icon. lgse/strata#1416
- Exact filenames such as `Makefile`, `Dockerfile`, `Cargo.lock`, and `id_ed25519` get the config or key icon regardless of extension. lgse/strata#1416 (unverified)
- A file with an unrecognized extension shows the document icon. lgse/strata#1416

### Cache

- The icon texture cache holds 256 textures and evicts only the least recently used one when full. lgse/strata#1400

## Design

- Icons are bundled SVGs, Lucide except the language glyphs, whose placeholder colors are replaced before rasterizing. They follow Strata's tokens rather than the desktop icon theme (unverified).
- Full-color brand icons were rejected because fixed brand colors break theme sync. The owner approved non-Lucide monochrome language glyphs from Simple Icons and Devicons, plus a custom Java glyph (lgse/strata#1528, lgse/strata#1529).
- Lucide strokes are 8.3% of icon size at every scale, about 21 px at 256 px. The fix compensates stroke width at render time instead of editing icon geometry (lgse/strata#1011, lgse/strata#1416).
- Logical size and context are cached apart from raster resolution, so perceived weight follows logical size while resolution only sets sharpness (lgse/strata#1416).
- Chrome icons were 20 px drawn from 96 px textures, and GtkImage's default fill stretched them in XFCE's larger buttons. They are now 16 px, centered, and rasterized at twice their size (lgse/strata#469, lgse/strata#497).
- The cache key is name, color, and texture size. Folder colors and per-size textures multiplied the keys, so clear-all eviction caused re-rasterization bursts (lgse/strata#1322, lgse/strata#1400).
- Bundled vectors render straight to memory textures, avoiding synchronous GdkPixbuf and Glycin startup while binding list rows (lgse/strata#834).
- The vector renderer rejects sources over 64 KiB and outputs outside 1–768 px, and never resolves external or embedded images (lgse/strata#834) (unverified).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-08 | lgse/strata#1529 | feat | Added 42 accent-tinted language glyphs and used the same icons in search results. |
| 2026-10-05 | lgse/strata#1416 | feat | Mapped more file types to Lucide icons and thinned Icons-view outlines at large sizes. |
| 2026-10-05 | lgse/strata#1400 | perf | Replaced clear-all icon texture eviction with a 256-entry LRU. |
| 2026-09-07 | lgse/strata#497 | fix | Held chrome icons at 16 px, centered, and rasterized them at twice their size. |
| 2026-09-02 | lgse/strata#170 | fix | Drew every interface icon in the accent color at full opacity, with accent hover backgrounds. |

## Known gaps

- Custom themes cannot supply their own icons. lgse/strata#1525
- File-type icons cannot be colored by category; every icon uses the accent. lgse/strata#1510
