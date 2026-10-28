---
title: Catppuccin file-type icons
status: shipped
origin: {issue: lgse/strata#1587, pr: lgse/strata#1588}
branch: null
reviewed_at: 86df474dc0e8352e0e2098637a017cc4c77a8c44
review: draft
code: [src/ui/browser/entry.rs, src/ui/browser/entry/catppuccin.rs, data/icons/catppuccin, scripts/catppuccin_icons.py]
tests: [src/ui/browser/entry/tests.rs]
related: [settings/themes/icons, browser/view-modes/icons]
---

## Summary

The bundled Catppuccin icon set and the mapping from a file's name to its file-type icon. Code and config files get Catppuccin icons; pictures, media, archives, documents, and keys keep Lucide icons. The parent `settings/themes/icons` owns the Lucide set and colors and rasterizes both sets.

## Behavior

### Catppuccin associations

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
- `app.apk` shows the Catppuccin Android icon and `app.jar` the Java archive icon. lgse/strata#1588
- `.nupkg` and `.vsix` show Catppuccin icons; `.deb`, `.rpm`, and `.exe` keep the Lucide package icon. lgse/strata#1588 (unverified)

### Lucide file types

- Pictures, plain text, spreadsheets, and keys keep Lucide icons: `photo.png`, `photo.svg`, `notes.txt`, `report.csv`, `server.pem`, and `id_ed25519`. lgse/strata#1587, lgse/strata#1588
- Search results use the same file-type icons as Columns, List, and Icons views. lgse/strata#1529
- `.mp4`, `.mkv`, `.webm`, `.mov`, `.avi`, `.m4v`, `.mpeg`, `.mpg`, `.ogv`, `.3gp`, `.3g2`, `.flv`, `.wmv`, `.asf`, `.m2ts`, and `.vob` files show the Lucide clapperboard icon. lgse/strata#1589
- `.zip`, `.7z`, `.tar`, `.gz`, `.tgz`, `.bz2`, `.xz`, `.zst`, `.rar`, `.lz`, `.lzma`, `.lzo`, `.rz`, `.sz`, `.cab`, `.arj`, and `.cpio` files show the Lucide folder-archive icon, distinct from documents. lgse/strata#1416, lgse/strata#1589
- Spreadsheets, presentations, fonts, disk images, and keys each show their own Lucide icon. lgse/strata#1416
- A file with an unrecognized extension shows the document icon. lgse/strata#1416

## Design

- Code and config files use the Catppuccin VSCode icon set, v1.26.0, MIT. A uniform monochrome set did not help recognize file types at a glance (lgse/strata#1587, lgse/strata#1588).
- The outlined Simple Icons and Devicons language glyphs from lgse/strata#1529 and lgse/strata#1561, and their outline render path, were removed (lgse/strata#1588).
- `scripts/catppuccin_icons.py` regenerates the SVGs, the gresource entries, and `src/ui/browser/entry/catppuccin.rs` from an upstream checkout, importing 1075 filename and 532 extension associations (lgse/strata#1588).
- Lookup tries the exact file name first, ignoring case, then Strata's case-sensitive name patterns. Next comes the longest dotted suffix in the Catppuccin table, then Strata's own extension table (lgse/strata#1588, unverified).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-12 | lgse/strata#1588 | feat | Replaced the language glyphs with Catppuccin file icons in Mocha and Latte flavors and added a File icon colors preference. |

## Known gaps

None known.
