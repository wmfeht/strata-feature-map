---
title: Themes and appearance
status: shipped
origin: {issue: lgse/strata#82, pr: lgse/strata#96}
branch: null
reviewed_at: e0f73973926ff67e77c2c56cf288b7b7617bb2e5
review: draft
code: [src/ui/theme.rs, src/ui/settings/theme.rs, src/ui/settings/theme/editor.rs, data/themes/catalog.toml]
tests: [src/ui/theme/tests.rs, src/ui/theme/tests/syntax.rs, src/ui/settings/theme/editor/tests.rs, src/ui/settings/tests/dismissal.rs]
docs: [site/src/reference/themes.md, docs/preferences.md, docs/themes.md]
related: [browser/view-modes/text-size, preview/preview-panel]
---

## Summary

The Settings → Appearance page and the color system behind it. It covers 95 bundled themes, custom theme files and their editor, syntax palettes, file icon colors, element glow, the interface renderer, font rendering, and an optional user stylesheet. Children: `settings/themes/omarchy` (following the Omarchy Quattro theme), `settings/themes/icons` (bundled Lucide and Catppuccin icons), `settings/themes/corner-roundness` (the corner radius scale), and `settings/themes/interface-font` (the interface typeface). Text size, also on this page, is `browser/view-modes/text-size`.

## Behavior

### Theme library

- Settings → Appearance lists 95 bundled themes in alphabetical order in a scrolling library. lgse/strata#96
- Typing in "Search themes" hides cards whose names do not contain the query, ignoring case. lgse/strata#96
- The All, Light, and Dark filter combines with the search query. lgse/strata#96
- A theme is filed under Light when its background's relative luminance exceeds 0.4, including backgrounds written as `rgb()` or `#fff`. lgse/strata#742
- Every bundled theme's text has at least 4.5:1 contrast on its background and 3:1 on its surface. lgse/strata#1570, lgse/strata#1459
- Every bundled theme's dim text, as loaded, has at least 4.5:1 contrast on its background and 3:1 on its surface. lgse/strata#1724
- Loading a bundled theme whose catalog dim text misses those floors blends it toward its text color in 1/255 steps, stopping at the first that passes. Tokyo Night's #737aa2 loads as #767da6. lgse/strata#1724 (unverified)
- A custom theme file keeps its dim text as written, even below those floors. lgse/strata#1724
- Material Lighter draws text in #455A64, 6.94:1 on its background, and dim text in #5c7785, lifted from its catalog #607D8B. lgse/strata#1570, lgse/strata#1459, lgse/strata#1724 (unverified)
- Material Vivid draws text in #9e9e9e, 6.01:1 on its background. lgse/strata#1570, lgse/strata#1459
- Clicking a card applies that theme immediately and marks the card with a check. lgse/strata#96
- A fresh install without Omarchy starts with Tokyo Night; a saved selection survives restart. lgse/strata#542
- A saved theme id that matches no bundled or custom theme falls back to Azure Glow at startup. lgse/strata#542 (unverified)

### Custom themes

- Valid `.toml` files in `~/.config/strata/themes` load at startup, are re-read when one changes, and appear after the bundled themes, keyed by file stem. lgse/strata#96, lgse/strata#1620 (unverified)
- A custom file whose stem matches a bundled theme id replaces that bundled theme. lgse/strata#96
- A custom file with an invalid color is skipped at startup and on each re-read, unless it is the selected theme. lgse/strata#762, lgse/strata#1620 (unverified)
- A custom file with a GTK-only color form, such as 9-digit hex, loads with colors as `#rrggbb`, or `#rrggbbaa` when translucent; the file is not rewritten. lgse/strata#1554, lgse/strata#1429
- With a custom theme selected, rewriting its `.toml` file, such as changing `accent`, re-applies the new colors in every open window without a restart. lgse/strata#1620
- A live re-apply also recolors interface icons and code-preview syntax colors. lgse/strata#1620
- `.toml` changes in the themes directory less than 75 ms apart trigger one re-read, 75 ms after the last. lgse/strata#1620
- When a selected file whose stem matches no bundled theme is caught mid-write, invalid, or deleted, its colors stay until the next valid write. lgse/strata#1620
- While such a file is unreadable, its theme stays in the theme list. lgse/strata#1620
- Only `.toml` files directly in `~/.config/strata/themes` trigger a re-read; other extensions and subdirectories do not. lgse/strata#1620 (unverified)
- Saving a theme from the editor re-arms the watch, so a themes directory that the save creates is watched. lgse/strata#1620
- When `~/.config/strata/themes` is missing at startup, files created there later are not re-read until an editor save or a restart. lgse/strata#1620 (unverified)
- While following Omarchy, rewriting a custom theme file changes no colors. lgse/strata#1620 (unverified)
- During an editor preview, rewriting the selected file keeps the preview applied. lgse/strata#1620 (unverified)
- Deleting or breaking a selected custom `tokyo-night.toml` applies the bundled theme's colors at once, and the bundled theme replaces it in the list. lgse/strata#1620 (unverified)
- With a bundled theme selected, creating a custom file with its id, such as `dracula.toml`, applies that file's colors without a restart. lgse/strata#1620 (unverified)
- In an open Settings page, a re-read never redraws existing theme cards; a new file's card appears when a re-read changes the selected colors, or at the next theme or preference change. lgse/strata#1620 (unverified)
- Add theme opens an "Add a theme" panel with a name field and 14 color pickers seeded from the selected theme. lgse/strata#762
- Each picker change previews across the interface and open code previews; Cancel restores the selected theme. lgse/strata#762
- Reopening Add theme after Cancel or after Settings closes starts from the selected theme's colors, with an empty name and no error. lgse/strata#1457, lgse/strata#1533 (unverified)
- Pressing Add theme while the editor is open keeps the current draft. lgse/strata#1533 (unverified)
- Closing Settings by Escape, Close settings, a click outside the panel, or closing the window discards an unsaved preview and collapses the editor. lgse/strata#1457, lgse/strata#1533
- Discarding a preview this way re-applies the saved theme in every open window and in windows opened later. lgse/strata#1457, lgse/strata#1533
- While a preview is active, changing text size, toggling Element glow, or an Omarchy theme change while following Omarchy keeps the preview applied. lgse/strata#1457, lgse/strata#1533
- Cancel, or closing Settings, in one window leaves a preview started later in another window applied. lgse/strata#1533
- Clicking a theme card or toggling Follow Omarchy during a preview ends the preview. lgse/strata#1457, lgse/strata#1533
- When followed Omarchy state disappears during a preview, the preview ends and the selected built-in theme applies. lgse/strata#1457, lgse/strata#1533
- Add theme saves the name and all 14 colors to a TOML file in `~/.config/strata/themes` and selects the new theme. lgse/strata#762
- Saving never overwrites a file in `~/.config/strata/themes`. When `<id>.toml` exists, even invalid or a dangling link, the theme saves as the next free `<id>-N.toml`. lgse/strata#1455, lgse/strata#1544
- A new theme file is created owner-only, mode 0600. lgse/strata#39, lgse/strata#1544
- The editor saves a theme under its lowercased name's ASCII letters and digits joined by `-`, so `Ocean Blue` becomes `ocean-blue.toml`. lgse/strata#762
- Saving a theme named `Dracula` creates `dracula-2.toml` and leaves the bundled Dracula in place. lgse/strata#1544, lgse/strata#1570
- A name with no ASCII letters or digits, such as `日本語` or `!!!`, saves as `custom-theme.toml` and is listed under its typed name. lgse/strata#1570, lgse/strata#1458
- A second such name saves as `custom-theme-2.toml`, the next as `custom-theme-3.toml`. lgse/strata#1570, lgse/strata#1458
- Saving with an empty or whitespace-only name shows "Enter a theme name" and writes nothing. lgse/strata#762, lgse/strata#1570 (unverified)
- A swatch's color chooser draws its Cancel and Select buttons, hex entry, sliders, and value popups in the active theme, following live theme changes. lgse/strata#1570, lgse/strata#1460
- Editor color swatches keep rounded corners with no square fragments when normal, hovered, focused, or pressed. lgse/strata#582

### Syntax colors

- Code previews color keywords, strings, constants, types, and preprocessor directives from the active theme; all 95 bundled themes define these five colors. lgse/strata#762
- In a custom file, each `syntax_*` key overrides one role; an omitted key keeps its color derived from accent and text. lgse/strata#762
- Comments use the dim text color and Markdown headings use the accent color. lgse/strata#762
- A custom theme whose colors are written as `rgb()`, short hex, or color names keeps syntax colors in code previews. lgse/strata#742
- The editor saves each picked color as `#rrggbb`. lgse/strata#742 (unverified)

### File icons

- Settings → Appearance has a File icons group with a File icon colors menu: Brand colors, the default, and Theme colors. lgse/strata#1588
- A File icon colors choice applies in every open window at once. lgse/strata#1588
- The choice is saved as `file_icon_colors = "brand"` or `"theme"`; a missing key reads as Brand colors. lgse/strata#1588 (unverified)
- A theme gets Mocha file icons when its background's (299R + 587G + 114B) ÷ 1000 is below 128, otherwise Latte. lgse/strata#1588 (unverified)
- A background that cannot be parsed gets Mocha file icons. lgse/strata#1588 (unverified)
- The File icons group has a Show thumbnails switch after File icon colors, on by default; its choice is saved as `show_thumbnails` and survives restart. lgse/strata#1651
- Searching "Show thumbnails" or "photos", or "Miniaturansichten" under Deutsch, in Search settings shows the Show thumbnails row. lgse/strata#1651 (unverified)

### Styling and effects

- Settings navigation, close, and search icons, and the About and release-notes icons, draw in the accent color at 0.65 opacity, without desaturation. lgse/strata#1724 (unverified)
- The active page's navigation icon draws at full opacity. lgse/strata#1724 (unverified)
- Strata's stylesheet reads the nine tokens as `@strata_bg`, `@strata_surface`, `@strata_text`, `@strata_accent`, `@strata_danger`, `@strata_muted`, `@strata_highlight`, `@strata_border`, and `@strata_dim_text`. lgse/strata#1412
- User CSS that redefines the former `@theme_*` names no longer changes Strata's colors. lgse/strata#1412
- A rule in `~/.config/gtk-4.0/gtk.css` changes no property of Strata's widgets. Examples are `label { color: red }`, `button { min-width: 60px }`, and `* { outline: 3px solid red }`. lgse/strata#1680, lgse/strata#1682
- The user `gtk.css` stays without effect after switching between a light and a dark Strata theme. lgse/strata#1682
- A desktop GTK theme chosen through the settings portal or `settings.ini` does not style Strata; `gtk-theme-name` reads `Default` once Strata starts. lgse/strata#1680
- Launching with `GTK_THEME` set, such as `GTK_THEME=Adwaita:dark`, restarts Strata without that variable, as a browser or as the portal chooser. lgse/strata#1680
- GTK's high-contrast variant is never used, whatever the desktop's contrast setting. lgse/strata#1680
- GTK's built-in dark variant applies when the Strata theme's background (299R + 587G + 114B) ÷ 1000 is below 128 or unparseable. lgse/strata#1680, lgse/strata#1682 (unverified)
- Otherwise the light variant applies; the desktop color scheme is ignored. lgse/strata#1680, lgse/strata#1682
- Element glow, on by default, adds accent glow to dialogs, menus, theme cards, and animated feedback. lgse/strata#920
- Turning Element glow off removes that glow in every window at once, keeps focus outlines and depth shadows, and persists across restart. lgse/strata#920
- Interface renderer offers GTK default and Cairo; choosing a value other than the startup one shows Restart now. lgse/strata#1218
- After restart, Cairo renders the interface; an explicit `GSK_RENDERER` environment variable overrides the saved choice. lgse/strata#1218
- On GTK 4.16 or later, Strata sets `gtk-font-rendering` to manual for its own process at startup; the desktop's setting is unchanged. lgse/strata#1601
- Under GL or Vulkan at text size 10, `text-scaling-factor` 1.1818, and a 1.25× monitor, `T`, `E`, and `I` keep their top pixel row. "Trash" does not read "Irash". lgse/strata#1600, lgse/strata#1601
- Manual font rendering follows the desktop's antialiasing and hint style. lgse/strata#1601
- On GTK older than 4.16, Strata skips the font rendering pin. lgse/strata#1601
- With Reduce motion on, sidebar, column, and preview animations do not play. lgse/strata#458
- Strata's stylesheet has no `prefers-reduced-motion` rule, so that desktop media preference does not shorten CSS transitions. lgse/strata#458
- With GTK's `gtk-enable-animations` set to false, the same animations do not play even when Reduce motion is off. lgse/strata#458 (unverified)

### User stylesheet

- With `~/.config/strata/style.css` present at startup, its rules apply in every window and override Strata's own rules and the active theme. lgse/strata#1758
- The file follows `$XDG_CONFIG_HOME`, so with `XDG_CONFIG_HOME=/tmp/cfg` it is read from `/tmp/cfg/strata/style.css`. lgse/strata#1758 (unverified)
- Rules in the file may use the active theme's `@strata_*` colors; switching themes keeps the override and updates those colors. lgse/strata#1758
- Creating, editing, or deleting the file while Strata runs re-applies it in every open window without a restart. lgse/strata#1758
- Changes to the file less than 75 ms apart trigger one reload, 75 ms after the last. lgse/strata#1758 (unverified)
- Deleting the file, or making it unreadable, restores Strata's default appearance; an unreadable file logs "cannot read user stylesheet". lgse/strata#1758
- A rule GTK cannot parse, such as `label { color: nope; }`, is skipped with an "invalid rule in user stylesheet" warning. Valid rules in the same file still apply. lgse/strata#1758
- Without the file, Strata's appearance is unchanged. lgse/strata#1758
- Corner roundness does not scale radii set in the user stylesheet. lgse/strata#1758 (unverified)

## Design

[docs/themes.md](https://github.com/lgse/strata/blob/e0f73973926ff67e77c2c56cf288b7b7617bb2e5/docs/themes.md) carries the token model, custom file format, Base16 mapping, and Omarchy integration. Its Live updates section covers re-reading custom files on change, and its User stylesheet section covers `style.css`. [docs/preferences.md](https://github.com/lgse/strata/blob/e0f73973926ff67e77c2c56cf288b7b7617bb2e5/docs/preferences.md) covers File icon colors, the interface renderer, and the font rendering pin.

- Every color comes from nine semantic tokens: background, surface, text, accent, danger, muted, highlight, border, and dim text. Bundled themes are the fallback on any Linux desktop.
- lgse/strata#82 weighed a curated catalog, Base16 file import, terminal theme import, and a downloadable catalog. lgse/strata#96 chose an offline curated catalog of Tinted Theming Base16 palettes, recording upstream revision and MIT attribution.
- Base16 slots map `base00` background, `base01` surface, `base05` text, `base0D` accent, `base08` danger, `base02` muted and highlight, `base03` border, `base04` dim text (lgse/strata#96).
- Syntax palettes map `base0E` keywords, `base0B` strings, `base09` constants, `base0A` types, and `base0C` preprocessor. Catppuccin and Tokyo Night use the pinned `catppuccin-mocha` and `tokyo-night-dark` palettes. Azure Glow and Omarchy Light use curated palettes (lgse/strata#762, lgse/strata#1104).
- Colors are parsed through `gdk::RGBA`, so hex, short hex, `rgb()`, and names all work. Hand-rolled hex parsing had misfiled light themes and dropped syntax colors (lgse/strata#655, lgse/strata#742).
- GDK also accepts 9- and 12-digit hex, which GTK CSS and SVG strokes reject. Custom and Omarchy colors are canonicalized on load, in memory only, so dotfiles are never rewritten (lgse/strata#1429, lgse/strata#1554).
- Base16 `base05` maps to text unchanged, except a few catalog entries whose foreground overrides are commented in place for readability. The owner chose the Material Lighter and Material Vivid values and left other weak pairs to lgse/strata#1566 (lgse/strata#1459, lgse/strata#1570).
- Dim text is lifted at load rather than overridden in the catalog. It takes the same floors as body text, and the lift stops at the first passing step so it stays dimmer than text. The lift reuses the Omarchy readability helper (lgse/strata#1711, lgse/strata#1724).
- Settings icons lost their desaturation because their fixed gray differed from the text's and looked the same in every theme (lgse/strata#1711, lgse/strata#1724).
- A name without ASCII letters or digits takes the fallback id `custom-theme`. A Unicode slug would change existing ids and give non-ASCII file names; transliteration adds a dependency (lgse/strata#1458, lgse/strata#1570).
- The `@strata_*` namespace hardens against name collisions; the trigger reported in lgse/strata#1096 was not reproduced (lgse/strata#1412).
- Strata no longer leaves user CSS at GTK's higher user priority, as lgse/strata#1412 did. Desktop themes changed padding, row heights, and spacing, and user `gtk.css` could recolor or resize widgets. Documenting that user stylesheets win was rejected (lgse/strata#1679, lgse/strata#1680).
- An opt-in `~/.config/strata/style.css` restores layout overrides beyond the nine tokens, which `gtk.css` could no longer reach. Unlike `gtk.css`, it exists only when the user creates it, so default isolation stays intact (lgse/strata#1710, lgse/strata#1758).
- The user stylesheet loads one priority above the token provider, so its rules win over every Strata stylesheet. A missing or unreadable file clears it, and its watch debounces 75 ms, as custom themes do (lgse/strata#1758).
- A Floating sidebar toggle in Settings and patching Strata's stylesheet before each build were the alternatives in lgse/strata#1710. Class names are not a stable interface and may change between releases (docs/themes.md).
- The built-in `Default` theme and regular contrast are set as application values, which outrank the settings portal and `settings.ini`. They are set even when they match, because only application values survive later portal updates (lgse/strata#1680).
- `GTK_THEME` bypasses GTK's settings, so startup re-execs without it, through the same path as the Cairo renderer. Editing the environment after threads start was avoided (lgse/strata#1680).
- Stylesheets above user priority win only for properties they set. A reset provider unsets every property just above user priority; the built-in theme, Strata's stylesheet, and its tokens follow in rising priority (lgse/strata#1681, lgse/strata#1682).
- Tokyo Night became the default at the maintainer's request; Azure Glow stayed the missing-theme fallback (lgse/strata#541, lgse/strata#542).
- The editor preview is process-wide: one style provider serves every window. The manager stores the preview tokens, so appearance refreshes re-apply the preview rather than the saved theme (lgse/strata#1457, lgse/strata#1533).
- Every Settings close route, and the layer unrealizing, runs a hook that discards the preview. A closed window never runs `hide` (lgse/strata#1457, lgse/strata#1533).
- Each preview carries a generation number, so an editor cancels only the preview it started, never a newer one from another window (lgse/strata#1533).
- Custom files are re-read on change so theme generators such as matugen work without a restart. lgse/strata#1619 rejected restarting, which loses session state, and re-saving, which is manual and easy to forget. Re-reading on window focus was heavier and still delayed; a built-in matugen integration was too opinionated (lgse/strata#1619).
- The directory watch uses a 75 ms debounce, the pattern of the Omarchy state watcher (lgse/strata#1620).
- A refresh keeps the selected theme's last valid entry while its file is unreadable. Dropping it would leave the saved selection pointing at no theme, so appearance changes such as text size would stop applying (lgse/strata#1620).
- Theme files may be dotfile symlinks. A file that failed to load may be a broken dotfile the user still wants, so saving never replaces an existing file (lgse/strata#1455, lgse/strata#1544).
- Glow got its own switch because changing themes could not tone down dialog glow (lgse/strata#919).
- GTK's GL and Vulkan renderers lose a top glyph pixel at some scales (GTK issue 8395). Cairo avoids it but costs CPU and is inherited by launched apps, so it stays opt-in (lgse/strata#1216, lgse/strata#1218). The manual font rendering pin fixes it on GTK 4.16 and later (lgse/strata#1601).
- GTK's automatic font rendering hints glyphs slightly but not their metrics. GSK sizes GPU atlas slots from the unhinted extents, so the hinted top row lands in padding the quad never samples. Cairo draws glyphs directly (lgse/strata#1600, lgse/strata#1601).
- Manual mode hints metrics too, so the extents match the raster. Application-set GTK settings outrank the settings portal, which on Wayland overrides `settings.ini` (lgse/strata#1310, lgse/strata#1600, lgse/strata#1601).
- lgse/strata#1310 proposed this pin and was closed as not fixable in Strata; lgse/strata#1601 reverses that. The property is looked up by name to keep the GTK 4.12 floor (lgse/strata#1601).
- The `@media (prefers-reduced-motion)` rule was removed because GTK before 4.20 rejects `@media`. Reduced motion now flows through Strata's setting, not a CSS media query (lgse/strata#436, lgse/strata#458).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-18 | lgse/strata#1758 | feat | Loaded an optional `~/.config/strata/style.css` above Strata's stylesheets, re-read live, so users can restyle layout beyond the color tokens. |
| 2026-10-17 | lgse/strata#1724 | fix | Lifted bundled themes' dim text to the body-text contrast floors and stopped desaturating Settings icons, so secondary text no longer reads as disabled. |
| 2026-10-15 | lgse/strata#1651 | feat | Added the Show thumbnails switch to the File icons group and to Settings search. |
| 2026-10-15 | lgse/strata#1682 | fix | Unset every property above GTK's user priority and restated the built-in theme, completing lgse/strata#1680's isolation, so a desktop `gtk.css` cannot restyle any widget property. |
| 2026-10-14 | lgse/strata#1620 | feat | Re-applied the selected custom theme when its file changes on disk, so theme generators work without a restart. |
| 2026-10-11 | lgse/strata#1570 | fix | Saved names without ASCII letters or digits as `custom-theme.toml`, raised Material text contrast, and themed the color chooser. |
| 2026-10-10 | lgse/strata#1554 | fix | Loaded custom and Omarchy colors as CSS hex so GTK-only forms no longer blank icons and styling. |
| 2026-10-10 | lgse/strata#1544 | fix | Saved custom themes under a free file name so an existing theme file is never overwritten. |
| 2026-10-09 | lgse/strata#1533 | fix | Discarded unsaved editor previews on every Settings close route and kept them through appearance refreshes. |
| 2026-10-05 | lgse/strata#1412 | fix | Renamed CSS color tokens to `@strata_*` to avoid collisions with other stylesheets. |
| 2026-09-24 | lgse/strata#1218 | fix | Added an opt-in Cairo interface renderer for GTK glyph artifacts, applied on restart. |
| 2026-09-18 | lgse/strata#762 | feat | Gave every bundled theme a syntax palette and added five syntax pickers to the editor. |
| 2026-09-13 | lgse/strata#920 | feat | Added an Element glow switch so accent glow can be turned off. |
| 2026-09-10 | lgse/strata#742 | fix | Parsed colors in every GTK format so editor themes filter and highlight correctly. |
| 2026-09-08 | lgse/strata#582 | fix | Matched the radii of editor swatches, their overlays, and their buttons. |
| 2026-09-07 | lgse/strata#542 | feat | Made Tokyo Night the default theme on fresh installs. |
| 2026-09-06 | lgse/strata#458 | fix | Removed the reduced-motion `@media` rule that GTK before 4.20 rejects. |
| 2026-09-01 | lgse/strata#96 | feat | Added a catalog of 95 bundled themes with search and Light/Dark filtering. |

## Known gaps

- docs/themes.md still names Azure Glow as the default, but fresh installs start with Tokyo Night. lgse/strata#541
- Theme cards show the selected theme only with a check icon and expose no checked state to assistive technology. lgse/strata#1544
- Text is below 4.5:1 on highlight in 34 bundled themes and on the selected-row fill in 19. lgse/strata#1566
