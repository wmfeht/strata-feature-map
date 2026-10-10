---
title: Icons view
status: shipped
origin: {issue: lgse/strata#322, pr: lgse/strata#328}
branch: null
reviewed_at: 72b840e69d6f0df9d33fb5583e62a3a2944886a1
review: draft
code: [src/ui/icons_cell.rs, src/ui/icons_cell/**]
tests: [src/ui/icons_cell/tests.rs]
related: [browser/thumbnails, operations/rename]
---

## Summary

A single-pane grid of thumbnail tiles for the current folder, with a per-tile details line and an adjustable thumbnail size. Formerly called Grid.

## Behavior

### Grid

- Icons shows one grid with no file-type groups. lgse/strata#510
- The number of tile columns follows the viewport width and reflows when the window, sidebar, or preview panel changes width. lgse/strata#510
- Each tile has a fixed-size thumbnail slot, a two-line filename, and one details line. lgse/strata#328, lgse/strata#1148
- Filenames start directly below the thumbnail, top-aligned in their two-line area. lgse/strata#747
- Airy density adds modest padding around tiles compared with Compact. lgse/strata#747
- Hover feedback appears only over a tile's thumbnail and caption, not the gutters between tiles. lgse/strata#998

### Details line

- Folders show "No items" or their item count, audio and video show their duration, images show width×height, and other files show their size. lgse/strata#998
- Details stream into visible tiles after the folder renders, and revisiting an unchanged folder shows them from cache. lgse/strata#998
- Details arriving do not change tile size or move the grid. lgse/strata#1148
- After a fast scroll stops, visible tiles fill their thumbnails and details without further input. lgse/strata#1148

### Thumbnail size

- The pane header's Thumbnail size popover holds a slider from 32 to 256 px, default 64, labelled with the current value, such as "64 px". lgse/strata#328, lgse/strata#805, lgse/strata#1133
- A wheel notch over the slider moves it 1 px; a wheel tick over the listing closes the popover and scrolls the grid, and over the sidebar or other chrome it only closes. lgse/strata#328
- Moving the slider scales existing thumbnails in place without flashing generic icons. lgse/strata#328
- The size is saved as `icons_thumbnail_size` and used from the first frame after restart; other windows' Icons panes follow a change. lgse/strata#1133

### Name tooltip

- Resting the pointer about a second (900 ms) on a card whose name is middle-ellipsized shows the full name in a tooltip. lgse/strata#1553
- A name that fits in its two caption lines shows no tooltip. lgse/strata#1553
- The tooltip appears only over the card's thumbnail or caption, not its padding. lgse/strata#1553
- Over the caption, only the name and details text count, not blank space beside a short centered name. lgse/strata#1553 (unverified)
- Moving more than 4 px or leaving the card restarts the wait. Sweeping across the grid shows no tooltips. lgse/strata#1553
- Pressing a mouse button cancels the wait until the pointer moves again, so a click then holding still shows no tooltip. lgse/strata#1553 (unverified)
- After a rename commits, the tooltip shows the new name; while the rename field is open, none appears. lgse/strata#1553
- Ctrl+F results shown in Icons use the same cards and show the same tooltip. lgse/strata#1553
- Keyboard focus on a card shows no name tooltip. lgse/strata#1553 (unverified)

### Scrolling

- Tiles bound mid-scroll set their name and request thumbnail and details at once; cut styling and accessible descriptions refresh on the next frame. lgse/strata#328, lgse/strata#1081 (unverified)

## Design

GTK's GridView estimates layout from cell sizes, so flexible image and label cards made large folders hitch. Tiles therefore use a fixed `ThumbnailSlot` and a `GtkInscription` caption (lgse/strata#322, lgse/strata#509). Cards are built without a rename field, but the grid factory adds a hidden one at setup (lgse/strata#1174).

- The column cap is pinned on the next idle, because GridView ignores a resize queued during its own allocation, so a grow would keep the old cap (lgse/strata#510).
- Grouping per file type first stacked one GridView per type, which made rows viewport-tall and could abort GTK (lgse/strata#372). One GridView with a sticky heading followed (lgse/strata#373), then grouping became List-only (lgse/strata#509).
- Details come from bounded workers and an in-memory LRU validated by mtime and ctime. A persistent disk cache was rejected as unnecessary for small values (lgse/strata#996).
- Visible requests displace queued offscreen work in the 1,024-entry metadata backlog instead of raising the limit (lgse/strata#1146).
- The slider's long-press fine-tune is removed because it snapped the thumb to 64 and 256 (lgse/strata#328).
- Tile proportions follow Finder and Windows Explorer: compact by default, Airy modestly roomier (lgse/strata#737).
- Middle ellipsis hides the part of names like `2026-10-07-release-candidate-build-final-v3.tar.gz` that tells them apart. Wider cards, a smaller font, end ellipsis, and a status-bar name were rejected (lgse/strata#1522).
- Cards run their own rest timer. GTK4's hover delay drops to 60 ms once any tooltip shows, which would flash names card by card while sweeping the grid (lgse/strata#1553).
- Upstream AGENTS.md allows tooltips only on icon-only buttons. The owner approved this exception for Icons names on condition of a longer delay than GTK's default (lgse/strata#1553).
- The tooltip reads the caption when GTK asks for it, so it follows a pending rename (lgse/strata#1553).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-10 | lgse/strata#1553 | feat | Showed the full name in a tooltip after the pointer rests on a card whose name is truncated. |
| 2026-09-19 | lgse/strata#1133 | feat | Saved the thumbnail size across restarts and synced it between windows. |
| 2026-09-19 | lgse/strata#1148 | fix | Reserved the details line, resumed fills after fast scrolls, and kept focus on renamed items. |
| 2026-09-15 | lgse/strata#998 | feat | Streamed size, dimensions, duration, and item counts into tiles and limited hover to tile content. |
| 2026-09-10 | lgse/strata#747 | fix | Narrowed tiles and placed filenames directly below thumbnails. |
| 2026-09-08 | lgse/strata#610 | fix | Balanced vertical padding inside hovered tiles. |
| 2026-09-07 | lgse/strata#510 | perf | Gave tiles fixed sizes, pinned the column count, and removed Icons type grouping. |
| 2026-09-06 | lgse/strata#373 | fix | Rendered grouped Grid as one virtualized grid with a sticky heading. |
| 2026-09-06 | lgse/strata#425 | fix | Let arrow keys cross grouped Grid sections that hold only hidden entries. |
| 2026-09-05 | lgse/strata#328 | perf | Deferred tile work during thumb drags and steadied the thumbnail-size slider. |

## Known gaps

None known.
