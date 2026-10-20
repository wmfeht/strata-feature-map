---
title: Themed icons
status: shipped
origin: {issue: lgse/strata#169, pr: lgse/strata#170}
branch: null
reviewed_at: fd6327265eaa3266f8420fe8bd25e965146344b0
review: draft
code: [src/assets.rs, src/assets/vector.rs, src/ui/browser/entry.rs, src/ui/browser/entry/catppuccin.rs, data/icons/catppuccin/**, scripts/catppuccin_icons.py, data/icons/scalable/actions/strata-video.svg, data/icons/scalable/actions/strata-file-archive.svg, data/icons/scalable/actions/strata-chevron-down-symbolic.svg, data/icons/scalable/actions/strata-minus-symbolic.svg, data/icons/scalable/actions/strata-plus-symbolic.svg]
tests: [src/assets/tests.rs, src/assets/vector/tests.rs, src/ui/browser/entry/tests.rs, src/ui/theme/tests.rs]
related: [browser/view-modes/icons, browser/folder-customization]
---

## Summary

Strata's bundled interface and file-type icons, rasterized at the size and density they are drawn. Interface icons and generic file types are Lucide outlines in the theme's accent; code and config files use Catppuccin icons in their own palette by default, or the accent under Theme colors. Covers icon coloring, bundled GTK control icons, chrome icon sizing, stroke weight, file-type icon choice, and the icon texture cache.

## Behavior

### Color

- Header, sidebar, and settings navigation icons, and Lucide file-type icons, draw in the theme's accent color at full opacity. lgse/strata#170, lgse/strata#1588
- Changing the theme or Omarchy variant recolors icons, including the Catppuccin palette, in every open window without reopening them. lgse/strata#1482, lgse/strata#1588
- Destructive menu items, such as Permanently delete, and danger-tone dialogs draw their icon in the theme's danger color. lgse/strata#1210 (unverified)
- Icons draw in an opaque `#rrggbb` form of the accent, text, or danger color, so a translucent accent loses its alpha on icons only. lgse/strata#1554, lgse/strata#1429
- With File icon colors on Brand colors, a Catppuccin icon draws in its own Mocha or Latte colors, not the accent. lgse/strata#1587, lgse/strata#1588
- With File icon colors on Theme colors, every color of a Catppuccin icon draws in the accent, on dark and light themes alike. lgse/strata#1588
- Under Theme colors, a Catppuccin icon's unfilled shapes get a 15% accent fill, like the folder icon. lgse/strata#1588 (unverified)
- File icon colors leaves interface icons, Lucide file-type icons, and folders unchanged. lgse/strata#1588
- A code file such as `main.rs` with a saved color and no custom icon keeps its brand palette under Brand colors. lgse/strata#1588 (unverified)
- Under Theme colors, that file's icon takes the saved color instead of the accent. lgse/strata#1588 (unverified)
- The Strata logo on Settings → About takes the theme's text color and recolors when the theme changes. lgse/strata#1673 (unverified)

### GTK control icons

- Under the Breeze, Yaru, or Adwaita icon theme, the arrows of Settings dropdowns, such as Language and Release channel, and of the drive format dialog dropdown draw the same thin Lucide chevron. lgse/strata#1777, lgse/strata#1778
- Under any icon theme, the Text size, Corner roundness, and Thumbnail workers spin buttons draw Lucide − and + steps. lgse/strata#1778
- Those steps follow the control's CSS color, including hover and disabled states. lgse/strata#1778
- The spin buttons in the Customize… custom color editor draw the bundled − and + steps. lgse/strata#1778

### Size and weight

- Header-bar and pane action icons draw at 16 logical px at the default text size, centered, even when the desktop theme gives buttons extra space. lgse/strata#497
- Chrome icons rasterize at twice their logical size; file, sidebar, and dialog icons rasterize at 96 px or their device-pixel size, whichever is larger. lgse/strata#497, lgse/strata#1416
- In the Icons view, Lucide outlines draw at half the stroke weight of list, toolbar, and sidebar icons at every size. lgse/strata#1416
- Above 64 logical px, strokes scale by (64 ÷ size)^0.35, about 0.62× at 256 px, so large icons do not read as bold. lgse/strata#1416
- Catppuccin strokes take the same large-size factor and the same Icons-view halving as Lucide outlines. lgse/strata#1588 (unverified)
- In the Icons view, a Catppuccin icon's strokes match the stroke weight of the folder icon beside it. lgse/strata#1588 (unverified)
- In List rows, a Catppuccin icon's strokes draw at three quarters of the folder icon's weight. lgse/strata#1588 (unverified)
- Icons rasterize at the display's pixel density, so 2× displays get sharp strokes. lgse/strata#1416

### File-type icons

- Code and config files show a Catppuccin icon: `main.rs` the Rust icon, `package.json` the package-json icon, `Cargo.toml` the Cargo icon. lgse/strata#1588
- JSON, YAML, XML, SQL, database, `.toml`, and Markdown files show Catppuccin icons. lgse/strata#1588
- An exact filename wins over the extension: `Makefile`, `Dockerfile`, `Cargo.lock`, `vite.config.ts`, `README`, and `LICENSE` get their own Catppuccin icons. lgse/strata#1588
- Exact filename matching ignores case, so `MAKEFILE` shows the Makefile icon. lgse/strata#1588 (unverified)
- Next, case-sensitive name patterns apply: `Dockerfile.*` shows Docker, `.env.*` env, `tsconfig.*.json` TypeScript config, `*_history` a terminal file, and `*.lock` the Lucide cog. lgse/strata#1588 (unverified)
- Otherwise the longest matching dotted suffix wins: `types.d.ts` and `app.test.ts` show specific icons, not the `.ts` icon. lgse/strata#1588
- `docker-compose.override.yml` and `compose.yaml` show the Docker Compose icon; `deploy.yml` shows the YAML icon. lgse/strata#1588
- `archive.lock` and other lowercase `.lock` files without their own association show the Lucide cog icon. lgse/strata#1588
- `ARCHIVE.LOCK` shows the Catppuccin config icon. lgse/strata#1588 (unverified)
- `.m` shows the MATLAB icon and `.v` the V icon. lgse/strata#1588
- `boot.s` shows the assembly icon and `run.ps1` the PowerShell icon. lgse/strata#1588
- `.asm` and `.nasm` show the assembly icon; `.sv`, `.svh`, and `.vhdl` the Verilog icon; `.bat` and `.cmd` the Batch icon. lgse/strata#1588 (unverified)
- Shell rc files such as `.BASHRC` show the Catppuccin Bash icon. lgse/strata#1588
- Shell scripts and `.zshrc` show the Catppuccin Bash icon. lgse/strata#1588 (unverified)
- `view.qml` and `app.tcl` show the generic code icon. lgse/strata#1588
- `.qrc` and `.ui` files show the generic code icon. lgse/strata#1588 (unverified)
- Pictures, plain text, spreadsheets, and keys keep Lucide icons: `photo.png`, `photo.svg`, `notes.txt`, `report.csv`, `server.pem`, and `id_ed25519`. lgse/strata#1587, lgse/strata#1588
- Search results use the same file-type icons as Columns, List, and Icons views. lgse/strata#1529
- `.mp4`, `.mkv`, `.webm`, `.mov`, `.avi`, `.m4v`, `.mpeg`, `.mpg`, `.ogv`, `.3gp`, `.3g2`, `.flv`, `.wmv`, `.asf`, `.m2ts`, and `.vob` files show the Lucide clapperboard icon. lgse/strata#1589
- `.zip`, `.7z`, `.tar`, `.gz`, `.tgz`, `.bz2`, `.xz`, `.zst`, `.rar`, `.lz`, `.lzma`, `.lzo`, `.rz`, `.sz`, `.cab`, `.arj`, and `.cpio` files show the Lucide folder-archive icon, distinct from documents. lgse/strata#1416, lgse/strata#1589
- Spreadsheets, presentations, fonts, disk images, and keys each show their own Lucide icon. lgse/strata#1416
- `app.apk` shows the Catppuccin Android icon and `app.jar` the Java archive icon. lgse/strata#1588
- `.nupkg` and `.vsix` show Catppuccin icons; `.deb`, `.rpm`, and `.exe` keep the Lucide package icon. lgse/strata#1588 (unverified)
- A file with an unrecognized extension shows the document icon. lgse/strata#1416

### Cache

- The icon texture cache holds 256 textures and evicts only the least recently used one when full. lgse/strata#1400

## Design

- Interface icons and generic file categories are bundled Lucide SVGs whose placeholder colors are replaced before rasterizing. They follow Strata's tokens rather than the desktop icon theme; Open With application icons still come from the desktop theme ([docs/themes.md](https://github.com/lgse/strata/blob/fd6327265eaa3266f8420fe8bd25e965146344b0/docs/themes.md), lgse/strata#1777, lgse/strata#1778).
- Dropdown and menu-button arrows and spin-button steps came from the desktop icon theme, so their shape changed with it; Breeze drew a filled triangle (lgse/strata#1777).
- The arrow uses a recolored `-gtk-icon-source`, as the table sort caret does. Spin steps swap their icon names for bundled ones (lgse/strata#1778).
- The control SVGs outline Lucide's 2 px round strokes as filled paths, because older GTK recolors only the fill of symbolic icons. The `-symbolic` suffix and `#2e3436` fill let GTK recolor them to the control's CSS color (lgse/strata#1778).
- Code and config files use the Catppuccin VSCode icon set, v1.26.0, MIT. A uniform monochrome set did not help recognize file types at a glance (lgse/strata#1587, lgse/strata#1588).
- This reverses the earlier rejection of full-color brand icons for breaking theme sync (lgse/strata#1528, lgse/strata#1529). Mocha on dark backgrounds and Latte on light ones keep them legible on built-in, custom, and Omarchy themes; Theme colors keeps the accent-only look (lgse/strata#1587, lgse/strata#1588).
- The outlined Simple Icons and Devicons language glyphs from lgse/strata#1529 and lgse/strata#1561, and their outline render path, were removed (lgse/strata#1588).
- SVGs are copied unchanged from upstream's `icons/css-variables`. Their `var(--vscode-ctp-*)` colors are replaced at render time from 16-color Mocha and Latte tables (lgse/strata#1588).
- `scripts/catppuccin_icons.py` regenerates the SVGs, the gresource entries, and `src/ui/browser/entry/catppuccin.rs` from an upstream checkout, importing 1075 filename and 532 extension associations (lgse/strata#1588).
- Catppuccin draws 1-unit strokes on a 16-unit grid where Lucide draws 2 on 24. Icons-view textures scale Catppuccin strokes by 4/3 so they match the folder (lgse/strata#1588) (unverified).
- Catppuccin textures are cached under the flavor name, or the accent under Theme colors, so a palette change never reuses a stale texture (lgse/strata#1588) (unverified).
- The video and archive icons are Lucide's clapperboard and folder-archive, so archives no longer resemble documents (lgse/strata#1589).
- Lucide strokes are 8.3% of icon size at every scale, about 21 px at 256 px. The fix compensates stroke width at render time instead of editing icon geometry (lgse/strata#1011, lgse/strata#1416).
- Logical size and context are cached apart from raster resolution, so perceived weight follows logical size while resolution only sets sharpness (lgse/strata#1416).
- Chrome icons were 20 px drawn from 96 px textures, and GtkImage's default fill stretched them in XFCE's larger buttons. They are now 16 px, centered, and rasterized at twice their size (lgse/strata#469, lgse/strata#497).
- The cache key is name, color, and texture size. Folder colors and per-size textures multiplied the keys, so clear-all eviction caused re-rasterization bursts (lgse/strata#1322, lgse/strata#1400).
- Bundled vectors render straight to memory textures, avoiding synchronous GdkPixbuf and Glycin startup while binding list rows (lgse/strata#834).
- The vector renderer rejects sources over 64 KiB and outputs outside 1–768 px, and never resolves external or embedded images (lgse/strata#834) (unverified).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-20 | lgse/strata#1778 | fix | Drew dropdown arrows and spin-button steps from bundled Lucide icons, so their shape no longer changes with the desktop icon theme. |
| 2026-10-15 | lgse/strata#1675 | perf | Checked the icon texture cache before loading and recoloring an icon's SVG source. |
| 2026-10-12 | lgse/strata#1589 | fix | Redrew video as a clapperboard and archives as a folder-archive, and mapped 10 more video and 8 more archive extensions. |
| 2026-10-10 | lgse/strata#1561 | fix | Outlined the language glyphs at folder stroke weight in padded view boxes and replaced the custom Java glyph with Devicon's. |
| 2026-10-08 | lgse/strata#1529 | feat | Added 42 accent-tinted language glyphs and used the same icons in search results. |
| 2026-10-05 | lgse/strata#1416 | feat | Mapped more file types to Lucide icons and thinned Icons-view outlines at large sizes. |
| 2026-10-05 | lgse/strata#1400 | perf | Replaced clear-all icon texture eviction with a 256-entry LRU. |
| 2026-09-07 | lgse/strata#497 | fix | Held chrome icons at 16 px, centered, and rasterized them at twice their size. |
| 2026-09-02 | lgse/strata#170 | fix | Drew every interface icon in the accent color at full opacity, with accent hover backgrounds. |

## Known gaps

- Custom themes cannot supply their own icons. lgse/strata#1525
- Generic file-type icons, such as documents, pictures, media, and archives, cannot be colored by category; they use the accent. lgse/strata#1510
