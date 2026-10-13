---
proposed: {page: new}
nodes: [settings/themes/icons]
reason: Icon size, stroke weight, file-type icon matching, and the icon texture cache are user-observable Behavior of settings/themes/icons, and no section on reference/themes.md, the only reference page naming that node, covers them.
release: v1.0.0
---

Raw material for a "File and interface icons" reference page, or a section a
person adds to the Themes reference.

## Icon size and stroke weight

- Header-bar and pane action icons draw at 16 logical px at the default text
  size, centered, even when the desktop theme gives buttons extra space.
- Chrome icons rasterize at twice their logical size; file, sidebar, and dialog
  icons rasterize at 96 px or their device-pixel size, whichever is larger.
  Icons rasterize at the display's pixel density, so 2× displays get sharp
  strokes.
- In the Icons view, Lucide outlines draw at half the stroke weight of list,
  toolbar, and sidebar icons at every size.
- Above 64 logical px, strokes scale by (64 ÷ size)^0.35, about 0.62× at
  256 px, so large icons do not read as bold. Catppuccin strokes take the same
  large-size factor and the same Icons-view halving.
- In the Icons view, a Catppuccin icon's strokes match the stroke weight of the
  folder icon beside it. In List rows, they draw at three quarters of the folder
  icon's weight.

## Which icon a file gets

Strata picks a file's icon in this order:

1. **Exact filename**, ignoring case: `Makefile`, `Dockerfile`, `Cargo.lock`,
   `vite.config.ts`, `README`, and `LICENSE` get their own Catppuccin icons, so
   `MAKEFILE` also shows the Makefile icon. Shell rc files such as `.bashrc`,
   `.BASHRC`, and `.zshrc` show the Catppuccin Bash icon.
2. **Name patterns**, case-sensitive: `Dockerfile.*` shows Docker, `.env.*`
   env, `tsconfig.*.json` TypeScript config, `*_history` a terminal file, and
   `*.lock` the Lucide cog. `archive.lock` and other lowercase `.lock` files
   without their own association therefore show the cog, while `ARCHIVE.LOCK`
   shows the Catppuccin config icon.
3. **Longest matching dotted suffix**: `types.d.ts` and `app.test.ts` show
   specific icons, not the `.ts` icon. `docker-compose.override.yml` and
   `compose.yaml` show the Docker Compose icon; `deploy.yml` shows the YAML
   icon.

Examples by extension:

- `.m` shows the MATLAB icon and `.v` the V icon. `boot.s`, `.asm`, and `.nasm`
  show the assembly icon; `run.ps1` the PowerShell icon; `.sv`, `.svh`, and
  `.vhdl` the Verilog icon; `.bat` and `.cmd` the Batch icon.
- `view.qml`, `app.tcl`, `.qrc`, and `.ui` files show the generic code icon.
- `app.apk` shows the Catppuccin Android icon and `app.jar` the Java archive
  icon. `.nupkg` and `.vsix` show Catppuccin icons; `.deb`, `.rpm`, and `.exe`
  keep the Lucide package icon.
- `.mp4`, `.mkv`, `.webm`, `.mov`, `.avi`, `.m4v`, `.mpeg`, `.mpg`, `.ogv`,
  `.3gp`, `.3g2`, `.flv`, `.wmv`, `.asf`, `.m2ts`, and `.vob` files show the
  Lucide clapperboard icon.
- `.zip`, `.7z`, `.tar`, `.gz`, `.tgz`, `.bz2`, `.xz`, `.zst`, `.rar`, `.lz`,
  `.lzma`, `.lzo`, `.rz`, `.sz`, `.cab`, `.arj`, and `.cpio` files show the
  Lucide folder-archive icon, distinct from documents.
- Spreadsheets, presentations, fonts, disk images, and keys each show their own
  Lucide icon. A file with an unrecognized extension shows the document icon.
- Search results use the same file-type icons as the Columns, List, and Icons
  views.

## Icon cache

- The icon texture cache holds 256 textures and evicts only the least recently
  used one when full.
