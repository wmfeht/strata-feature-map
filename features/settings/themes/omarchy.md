---
title: Omarchy theme following
status: shipped
origin: {issue: lgse/strata#1198, pr: lgse/strata#1482}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [src/ui/theme/omarchy.rs]
tests: [src/ui/theme/omarchy/tests.rs, src/ui/settings/theme/tests.rs]
related: []
---

## Summary

Follow Omarchy applies the active Omarchy Quattro desktop theme to Strata and tracks it as it changes. The Omarchy variant setting picks how the palette is interpreted: Original, Darker, or High contrast.

## Behavior

### Following

- Follow Omarchy is shown only when `~/.local/state/omarchy/current/theme.name` and `current/theme/colors.toml` exist with valid `background`, `foreground`, and `accent` colors. lgse/strata#958, lgse/strata#1482 (unverified)
- On first launch with no `settings.toml` and a valid Quattro state, Strata follows Omarchy. lgse/strata#542
- While following, the theme library is insensitive and the Current theme description reads "Managed by Omarchy. Turn off Follow Omarchy to pick a theme manually." lgse/strata#849 (unverified)
- Switching the Omarchy theme or editing `colors.toml` re-applies the palette in every window without restart. lgse/strata#1482
- Deleting `~/.local/state/omarchy` while Strata runs hides Follow Omarchy, restores the previously selected theme, and saves `mode = "theme"`. lgse/strata#958
- Omarchy's own theme switch, which briefly removes `current/theme`, does not turn following off. lgse/strata#958
- Code previews take keyword, string, constant, type, and preprocessor colors from Quattro's `magenta`, `green`, `orange`, `cyan`, and `yellow`. lgse/strata#762
- Without the named colors, `color5`, `color2`, `color9`, and `color3` supply keywords, strings, constants, and types. lgse/strata#762
- An invalid optional color such as `selection` or `color8` is ignored and its fallback used. lgse/strata#1482 (unverified)

### Variants

- Omarchy variant, beneath Follow Omarchy, offers Original (default), Darker, and High contrast. lgse/strata#1482
- The variant row is hidden without a valid Quattro state and insensitive while not following; its value is kept. lgse/strata#1482
- The choice is saved as `omarchy_variant` in `settings.toml`, applies before Settings opens, and updates every open window. lgse/strata#1482
- Changing the active Omarchy theme keeps the chosen variant. lgse/strata#1482
- Darker derives near-black surfaces from the terminal background, and light palettes also become dark. lgse/strata#1482
- Darker and High contrast give text, dim text, accent, danger, and syntax colors at least 4.5:1 contrast against their surfaces. lgse/strata#1482
- High contrast raises primary text to 7:1 and borders to 3:1, keeping a light palette light. lgse/strata#1482
- Variants never change bundled or custom themes or the desktop theme. lgse/strata#1482

## Design

[docs/themes.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/themes.md) describes the Quattro mapping and the variants.

- Only Quattro's current-theme state is read. Legacy Omarchy layouts and alacritty color extraction are intentionally unsupported.
- Tokens derive from Quattro's `background`, `foreground`, `accent`, `selection`, `color8`, and `color1`; surfaces blend the background toward `color8`.
- Availability is sampled at startup and re-checked by the state monitor on each change. The re-check accepts `current` plus `theme.name` so Omarchy's staged switch does not flicker following off (lgse/strata#857, lgse/strata#958).
- Variants exist because terminals and Btop draw near-black backgrounds while Strata's mapping drew lighter surfaces from the same palette (lgse/strata#1198).
- Darker uses the terminal background, not ANSI `color8`, because bright gray washed out every surface (lgse/strata#1482).
- Variants keep hues and move only luminance toward black or white, stepping each foreground until its contrast target is met (lgse/strata#1482).
- Contrast targets apply to semantic tokens, not to every composited or disabled widget state.

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-05 | lgse/strata#1482 | feat | Added Original, Darker, and High contrast variants and ignored invalid Quattro colors. |
| 2026-09-14 | lgse/strata#958 | fix | Turned following off and restored the built-in theme when Quattro state disappears. |

## Known gaps

- Omarchy icon colors are not canonicalized and the Quattro syntax palette is not validated. lgse/strata#1429, lgse/strata#1546
