---
title: Themes and appearance
status: shipped
origin: {issue: lgse/strata#82, pr: lgse/strata#96}
branch: null
reviewed_at: aee71335dfecd059b9af23efeac2ed52c43e3b19
review: draft
code: [src/ui/theme.rs, src/ui/settings/theme.rs, src/ui/settings/theme/editor.rs, data/themes/catalog.toml]
tests: [src/ui/theme/tests.rs, src/ui/theme/tests/syntax.rs, src/ui/settings/theme/editor/tests.rs, src/ui/settings/tests/dismissal.rs]
docs: [docs/themes.md]
related: [browser/view-modes/text-size, preview/preview-panel]
---

## Summary

The Settings → Appearance page and the color system behind it: 95 bundled themes, custom theme files and their editor, code-preview syntax palettes, element glow, and the interface renderer. Children: `settings/themes/omarchy` (following the Omarchy Quattro theme) and `settings/themes/icons` (theme-tinted bundled icons). Text size, also on this page, is `browser/view-modes/text-size`.

## Behavior

### Theme library

- Settings → Appearance lists 95 bundled themes in alphabetical order in a scrolling library. lgse/strata#96
- Typing in "Search themes" hides cards whose names do not contain the query, ignoring case. lgse/strata#96
- The All, Light, and Dark filter combines with the search query. lgse/strata#96
- A theme is filed under Light when its background's relative luminance exceeds 0.4, including backgrounds written as `rgb()` or `#fff`. lgse/strata#742
- Clicking a card applies that theme immediately and marks the card with a check. lgse/strata#96
- A fresh install without Omarchy starts with Tokyo Night; a saved selection survives restart. lgse/strata#542
- A saved theme id that matches no bundled or custom theme falls back to Azure Glow at startup. lgse/strata#542 (unverified)

### Custom themes

- Valid `.toml` files in `~/.config/strata/themes` load at startup and appear after the bundled themes, keyed by file stem. lgse/strata#96 (unverified)
- A custom file whose stem matches a bundled theme id replaces that bundled theme. lgse/strata#96
- A custom file with an invalid color is skipped at startup. lgse/strata#762
- Add theme opens an "Add a theme" panel with a name field and 14 color pickers seeded from the selected theme. lgse/strata#762
- Each picker change previews across the interface and open code previews; Cancel restores the selected theme. lgse/strata#762
- Reopening Add theme after Cancel or after Settings closes starts from the selected theme's colors, with an empty name and no error. lgse/strata#1457, lgse/strata#1533
- Pressing Add theme while the editor is open keeps the current draft. lgse/strata#1533 (unverified)
- Closing Settings by Escape, Close settings, a click outside the panel, or closing the window discards an unsaved preview and collapses the editor. lgse/strata#1457, lgse/strata#1533
- Discarding a preview this way re-applies the saved theme in every open window and in windows opened later. lgse/strata#1457, lgse/strata#1533
- While a preview is active, changing text size, toggling Element glow, or an Omarchy theme change while following Omarchy keeps the preview applied. lgse/strata#1457, lgse/strata#1533
- Closing Settings in one window leaves a preview started later in another window applied. lgse/strata#1457, lgse/strata#1533
- Clicking a theme card or toggling Follow Omarchy during a preview ends the preview. lgse/strata#762 (unverified)
- Add theme saves the name and all 14 colors to a TOML file in `~/.config/strata/themes` and selects the new theme. lgse/strata#762
- Saving with an empty name, or one with no ASCII letters or digits, shows "Enter a theme name" and writes nothing. lgse/strata#762 (unverified)
- Editor color swatches keep rounded corners with no square fragments when normal, hovered, focused, or pressed. lgse/strata#582

### Syntax colors

- Code previews color keywords, strings, constants, types, and preprocessor directives from the active theme; all 95 bundled themes define these five colors. lgse/strata#762
- In a custom file, each `syntax_*` key overrides one role; an omitted key keeps its color derived from accent and text. lgse/strata#762
- Comments use the dim text color and Markdown headings use the accent color. lgse/strata#762
- A custom theme whose colors are written as `rgb()`, short hex, or color names keeps syntax colors in code previews. lgse/strata#742
- The editor saves each picked color as `#rrggbb`. lgse/strata#742 (unverified)

### Styling and effects

- Strata's stylesheet reads the nine tokens as `@strata_bg`, `@strata_surface`, `@strata_text`, `@strata_accent`, `@strata_danger`, `@strata_muted`, `@strata_highlight`, `@strata_border`, and `@strata_dim_text`. lgse/strata#1412
- User CSS that redefines the former `@theme_*` names no longer changes Strata's colors. lgse/strata#1412
- Selectors and `@strata_*` definitions in `~/.config/gtk-4.0/gtk.css` still override Strata's styling. lgse/strata#1412
- Element glow, on by default, adds accent glow to dialogs, menus, theme cards, and animated feedback. lgse/strata#920
- Turning Element glow off removes that glow in every window at once, keeps focus outlines and depth shadows, and persists across restart. lgse/strata#920
- Interface renderer offers GTK default and Cairo; choosing a value other than the startup one shows Restart now. lgse/strata#1218
- After restart, Cairo renders the interface; an explicit `GSK_RENDERER` environment variable overrides the saved choice. lgse/strata#1218
- With Reduce motion on, sidebar, column, and preview animations do not play. lgse/strata#458
- Strata's stylesheet has no `prefers-reduced-motion` rule, so that desktop media preference does not shorten CSS transitions. lgse/strata#458
- With GTK's `gtk-enable-animations` set to false, the same animations do not play even when Reduce motion is off. lgse/strata#458 (unverified)

## Design

[docs/themes.md](https://github.com/lgse/strata/blob/aee71335dfecd059b9af23efeac2ed52c43e3b19/docs/themes.md) carries the token model, custom file format, Base16 mapping, and Omarchy integration.

- Every color comes from nine semantic tokens: background, surface, text, accent, danger, muted, highlight, border, and dim text. Bundled themes are the fallback on any Linux desktop.
- lgse/strata#82 weighed a curated catalog, Base16 file import, terminal theme import, and a downloadable catalog. lgse/strata#96 chose an offline curated catalog of Tinted Theming Base16 palettes, recording upstream revision and MIT attribution.
- Base16 slots map `base00` background, `base01` surface, `base05` text, `base0D` accent, `base08` danger, `base02` muted and highlight, `base03` border, `base04` dim text (lgse/strata#96).
- Syntax palettes map `base0E` keywords, `base0B` strings, `base09` constants, `base0A` types, and `base0C` preprocessor. Catppuccin and Tokyo Night use the pinned `catppuccin-mocha` and `tokyo-night-dark` palettes. Azure Glow and Omarchy Light use curated palettes (lgse/strata#762, lgse/strata#1104).
- Colors are parsed through `gdk::RGBA`, so hex, short hex, `rgb()`, and names all work. Hand-rolled hex parsing had misfiled light themes and dropped syntax colors (lgse/strata#655, lgse/strata#742).
- The token provider sits above GTK theme priority, so GTK themes cannot shadow it, while user CSS keeps GTK's higher user priority by design. The `@strata_*` namespace hardens against name collisions; the trigger reported in lgse/strata#1096 was not reproduced (lgse/strata#1412).
- Tokyo Night became the default at the maintainer's request; Azure Glow stayed the missing-theme fallback (lgse/strata#541, lgse/strata#542).
- The editor preview is process-wide: one style provider serves every window. The manager stores the preview tokens, so appearance refreshes re-apply the preview rather than the saved theme (lgse/strata#1457, lgse/strata#1533).
- Every Settings close route, and the layer unrealizing, runs a hook that discards the preview. A closed window never runs `hide` (lgse/strata#1457, lgse/strata#1533).
- Each preview carries a generation number, so an editor cancels only the preview it started, never a newer one from another window (lgse/strata#1533).
- Glow got its own switch because changing themes could not tone down dialog glow (lgse/strata#919).
- GTK's GL and Vulkan renderers lose a top glyph pixel at some scales (GTK issue 8395). Cairo avoids it but costs CPU and is inherited by launched apps, so it stays opt-in (lgse/strata#1216, lgse/strata#1218).
- The `@media (prefers-reduced-motion)` rule was removed because GTK before 4.20 rejects `@media`. Reduced motion now flows through Strata's setting, not a CSS media query (lgse/strata#436, lgse/strata#458).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
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

- Omarchy becoming unavailable while it is followed drops an active preview. lgse/strata#1533
- docs/themes.md still names Azure Glow as the default, but fresh installs start with Tokyo Night. lgse/strata#541
- The interface font is fixed to JetBrains Mono. lgse/strata#1217
