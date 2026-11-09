---
title: Follow system light/dark mode
status: shipped
origin: {issue: lgse/strata#1812, pr: lgse/strata#2094}
branch: null
reviewed_at: fb7eb0c4ee8bcb681651e56e91031ed95422e8ff
review: draft
code: [src/ui/theme/system_appearance.rs]
tests: [src/ui/theme/tests/system_appearance.rs]
related: [settings/themes/omarchy]
---

## Summary

Follow system light/dark mode switches Strata between the light and dark themes of a curated bundled family to match the desktop's light/dark preference. It is for GNOME-schema desktops that change between day and night appearance; Strata keeps its own palettes.

## Behavior

### Switch

- Settings → Appearance shows a Follow system light/dark mode switch before Follow Omarchy. lgse/strata#2094
- Its subtitle reads "Use the light or dark version of the chosen theme to match your desktop's light/dark mode." lgse/strata#2094 (unverified)
- Without the `org.gnome.desktop.interface` schema or its `color-scheme` key, the switch is hidden. lgse/strata#2094
- Without that schema, Settings search for "day night" does not show the switch. lgse/strata#2094 (unverified)
- Without that schema, a saved `mode = "system"` loads as `mode = "theme"` at startup. lgse/strata#2094
- A saved `mode` other than `theme`, `system`, or `omarchy`, such as `"unknown"`, loads as `mode = "theme"`. lgse/strata#2094 (unverified)
- Turning Follow system light/dark mode on turns Follow Omarchy off, and the reverse, in every open Settings window. lgse/strata#2094
- Turning Follow system light/dark mode off saves `mode = "theme"` and keeps the saved `theme`. lgse/strata#2094 (unverified)
- Toggling Follow system light/dark mode during an editor preview ends the preview. lgse/strata#2094 (unverified)

### Following

- While following, `color-scheme = prefer-dark` applies the dark theme of the selected family, such as One Dark. lgse/strata#2094
- While following, `default`, `prefer-light`, or any other `color-scheme` value applies the family's light theme, such as One Light. lgse/strata#2094
- Changing `color-scheme` with `gsettings` while Strata runs re-applies the theme in every window without a restart. lgse/strata#2094
- Strata never writes `color-scheme`, and never loads the desktop's GTK theme, icon theme, or accent color. lgse/strata#2094
- 28 bundled families have a pair, such as One Dark/One Light, Catppuccin Mocha/Latte, and Rosé Pine/Dawn. lgse/strata#2094
- An unpaired theme, such as Tokyo Night or an unpaired custom theme, keeps one palette in both modes. lgse/strata#2094
- A custom `.toml` whose stem overrides a paired bundled id, such as `one-light.toml`, joins that pair. lgse/strata#2094
- A mode change re-applies the GTK light/dark base variant, Strata colors, icons, documents, source highlighting, previews, and open Settings pages. lgse/strata#2094
- Restarting with following on starts in the theme for the current mode. lgse/strata#2094

### Theme library

- The saved `theme` is the family anchor: with One Dark saved and a light desktop, `settings.toml` keeps `theme = "onedark-dark"` and `mode = "system"`. lgse/strata#2094
- Clicking either theme of a pair in the library changes the family and leaves following on. lgse/strata#2094
- Current theme and the checked library card show the theme in use, so One Dark saved under a light desktop checks One Light. lgse/strata#2094
- While following, the Current theme description reads "Following the system light/dark mode. Choose a theme family from the library below." lgse/strata#2094 (unverified)
- While following, Add theme starts from the theme in use, and PDF text selection uses its colors. lgse/strata#2094
- When a custom file supplying the theme in use is deleted, its last colors stay applied. lgse/strata#2094 (unverified)

## Design

[docs/themes.md](https://github.com/lgse/strata/blob/fb7eb0c4ee8bcb681651e56e91031ed95422e8ff/docs/themes.md) describes the switch, the anchor model, and the curated pairs in its System light/dark mode section.

- lgse/strata#1812 asked for theme variants to follow `org.gnome.desktop.interface color-scheme`, as other GTK apps do. Until then only Omarchy users got day and night switching (lgse/strata#1812).
- Only the light/dark preference is followed. Strata keeps its own palettes and reads the key without writing it (lgse/strata#2094).
- The saved theme is the family anchor and the theme in use is derived from it, so following never rewrites `theme` (lgse/strata#2094).
- Pairs are a curated `(dark, light)` list in code. Unpaired ids deliberately resolve to themselves (lgse/strata#2094).
- Following is a third value of the single theme `mode`, so it and Omarchy following cannot both be on (lgse/strata#2094).
- Every consumer of the current palette, such as PDF selection and the Add theme editor, resolves through the theme in use. Reading the saved anchor showed the other side of the pair (lgse/strata#2094).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |

## Known gaps

- The switch reads only GNOME's `color-scheme` key. On desktops that publish it only through the XDG settings portal, such as KDE, the switch shows but has no effect. lgse/strata#2094
