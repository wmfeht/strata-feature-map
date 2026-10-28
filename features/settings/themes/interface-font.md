---
title: Interface font
status: shipped
origin: {issue: lgse/strata#1217, pr: lgse/strata#1696}
branch: null
reviewed_at: be3343a5992a2a5497b1a2ee7faa525be18e988f
review: draft
code: [src/ui/theme/font.rs]
tests: [src/ui/theme/tests.rs, src/ui/settings/theme/tests.rs]
related: [browser/view-modes/text-size]
---

## Summary

An Interface font preference under Settings → Appearance → Text that picks the typeface for menus, file lists, and dialogs. It is for users who want a different interface font than the bundled JetBrains Mono, independent of text size.

## Behavior

### Control

- Settings → Appearance → Text shows an Interface font row before Text size, described "The typeface for menus, file lists, and dialogs. File previews keep a monospace font." lgse/strata#1696
- The row's button shows the saved family name, or "Default" when none is saved, and follows a change made in any other open Settings window. lgse/strata#1696
- Opening the picker lists Default first, then the installed font families sorted case-insensitively without duplicates, each name drawn in the interface font. lgse/strata#1696
- The family list is collected on the picker's first open. A font installed later does not appear until a new window opens Settings or Strata restarts. lgse/strata#1696 (unverified)
- The chosen family, or Default when none is saved, shows a check mark in the list. lgse/strata#1696 (unverified)
- Typing in Search fonts keeps families whose name contains the query, ignoring case; with no match, "No fonts match" replaces the list. lgse/strata#1696
- Each time the picker opens, Search fonts is cleared and focused. lgse/strata#1696 (unverified)
- Clicking a family saves `interface_font = "<family>"` in `settings.toml` and closes the picker; clicking Default removes the key. lgse/strata#1696
- Building the control writes nothing to `settings.toml`. lgse/strata#1696

### Applying the font

- A saved family applies at startup before Settings opens, and a change applies at once in every open window, popover, menu, and dialog. lgse/strata#1696
- Text, source, and command previews keep JetBrains Mono whatever family is chosen. lgse/strata#1696
- A saved family that is not installed falls back to JetBrains Mono, and the row's button still shows the saved name. lgse/strata#1696 (unverified)
- GTK's `gtk-font-name` is set to the chosen family followed by JetBrains Mono and JetBrainsMono Nerd Font, at the current text size in pixels. lgse/strata#1696 (unverified)
- A family name containing `"` or `\`, such as `Other "Quoted" Sans`, applies without a stylesheet parse error. lgse/strata#1696

## Design

[docs/preferences.md](https://github.com/lgse/strata/blob/e0f73973926ff67e77c2c56cf288b7b7617bb2e5/docs/preferences.md) describes the setting in its Interface font row.

- The font is independent of text size. Changing the desktop-wide font was rejected because it affects other apps (lgse/strata#1217).
- Font rules live in their own stylesheet, loaded below Strata's, so the explicit monospace rules of previews still win and the default look is unchanged (lgse/strata#1696).
- Popovers restate the family because GTK's built-in theme resets their font with `font: initial` (lgse/strata#1696).
- The bundled families follow the chosen one in the font stack, so text keeps the default look if the family is uninstalled (lgse/strata#1696).
- The picker draws names in the interface font, not in their own face. Loading a font per row took about 0.5 s to open and stalled scrolling; a filtered list view opens in about 20 ms (lgse/strata#1696).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-15 | lgse/strata#1696 | feat | Added an Interface font preference so users can choose the interface typeface independently of text size. |

## Known gaps

None known.
