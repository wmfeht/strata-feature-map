---
title: Omarchy theme following
status: shipped
origin: {issue: lgse/strata#1198, pr: lgse/strata#1482}
branch: null
reviewed_at: c94eeb0020fa1154e11c741888f1b56d92ce70d6
review: draft
code: [src/ui/theme/omarchy.rs]
tests: [src/ui/theme/omarchy/tests.rs, src/ui/theme/tests.rs, src/ui/settings/theme/tests.rs]
related: []
---

## Summary

Follow Omarchy applies the active Omarchy Quattro desktop theme to Strata and tracks it as it changes. Strata maps Quattro's own surface keys, and the Omarchy variant, remembered per Omarchy theme, picks the layout: Lighter, Darker, or Contrast.

## Behavior

### Following

- Follow Omarchy is shown only when `~/.local/state/omarchy/current/theme.name` and `current/theme/colors.toml` exist with valid `background`, `foreground`, and `accent` colors. lgse/strata#958, lgse/strata#1482 (unverified)
- On first launch with no `settings.toml` and a valid Quattro state, Strata follows Omarchy. lgse/strata#542
- While following, the theme library is insensitive and the Current theme description reads "Managed by Omarchy. Turn off Follow Omarchy to pick a theme manually." lgse/strata#849 (unverified)
- Switching the Omarchy theme or editing `colors.toml` re-applies the palette in every window without restart. lgse/strata#1482
- A Quattro color in a GTK-only form, such as `accent = "#7a7a2af7f"`, loads as `#rrggbb`; icons stay visible and the accent styling applies. lgse/strata#1554, lgse/strata#1429
- While following, invalid Quattro state midway through a theme switch leaves the Settings preview and new document previews on the last applied palette. lgse/strata#1554, lgse/strata#1429
- Deleting `~/.local/state/omarchy` while Strata runs hides Follow Omarchy, restores the previously selected theme, and saves `mode = "theme"`. lgse/strata#958
- Omarchy's own theme switch, which briefly removes `current/theme`, does not turn following off. lgse/strata#958
- Code previews take keyword, string, constant, type, and preprocessor colors from Quattro's `magenta`, `green`, `orange`, `cyan`, and `yellow`. lgse/strata#762
- Without the named colors, `color5`, `color2`, `color9`, and `color3` supply keywords, strings, constants, and types. lgse/strata#762
- An unparsable Quattro syntax color, such as `green = "invalid"`, counts as missing and its fallback applies; code previews keep their syntax scheme. lgse/strata#1554, lgse/strata#1429
- An invalid optional color such as `selection` or `muted` is ignored and its fallback used. lgse/strata#1482, lgse/strata#1816 (unverified)

### Surfaces

- Panes and headers use Quattro's `dark_background`, or `background` when `dark_background` is missing. lgse/strata#1815, lgse/strata#1816
- Hover surfaces use `lighter_background`. When it is missing or equals `background`, hover is `background` blended 10% toward `foreground`. lgse/strata#1816 (unverified)
- Selection uses `selection`. When it is missing, selection is `background` blended 25% toward `accent`. lgse/strata#1816 (unverified)
- Borders use `muted`. When it is missing, borders are `background` blended 36% toward `foreground`. lgse/strata#1816 (unverified)
- ANSI `color8` is never read: changing it in `colors.toml` changes no color. lgse/strata#1815, lgse/strata#1816

### Variants

- Omarchy variant, beneath Follow Omarchy, offers Lighter, Darker (default), and Contrast. lgse/strata#1815, lgse/strata#1816
- The variant row reads "Lighter or darker file columns, or stronger contrast. Keeps following your system theme." lgse/strata#1816 (unverified)
- The variant row is hidden without a valid Quattro state and insensitive while not following; its value is kept. lgse/strata#1482
- Lighter puts file columns on `background` and the sidebar, headers, and preview on `dark_background`. lgse/strata#1815, lgse/strata#1816
- Darker also puts file columns on `dark_background`, so the whole window uses it. lgse/strata#1815, lgse/strata#1816
- Lighter and Darker keep the theme's colors as authored, so a light palette stays light under Darker. lgse/strata#1816
- Contrast uses the Darker layout and raises text to 7:1 against the window, pane, hover, and selection surfaces. lgse/strata#1815, lgse/strata#1816
- Contrast raises dim text, accent, and danger to 4.5:1, and borders to 3:1, against those four surfaces. lgse/strata#1816
- Contrast raises code-preview syntax colors to 4.5:1 against the window and pane surfaces. lgse/strata#1816 (unverified)
- Contrast keeps the theme's surfaces and selection, unless no foreground reaches 7:1 on one; that surface is darkened or lightened until one does. lgse/strata#1816
- Contrast keeps a palette light with `mode = "light"` in `colors.toml`, and dark with `mode = "dark"`. lgse/strata#1816
- Without `mode`, Contrast treats a background with relative luminance above 0.45 as light. lgse/strata#1816 (unverified)
- Variants never change bundled or custom themes or the desktop theme. lgse/strata#1482

### Per-theme memory

- The variant is saved per Omarchy theme under `[omarchy_variants]` in `settings.toml`, keyed by theme name, such as `tokyo-night = "lighter"`. lgse/strata#1815, lgse/strata#1816
- A `theme.name` with surrounding whitespace or a trailing newline uses the same key as the bare name. lgse/strata#1816 (unverified)
- Choosing Darker removes the theme's key; a theme without a key uses Darker. lgse/strata#1816
- The saved variant applies before Settings opens and updates every open window. lgse/strata#1482, lgse/strata#1816
- Switching to another theme with `omarchy-theme-set` applies that theme's saved variant, and the dropdown updates live in every window. lgse/strata#1815, lgse/strata#1816
- Saved `original` and `high_contrast` values load as Lighter and Contrast. lgse/strata#1816
- A legacy global `omarchy_variant = "high_contrast"` becomes Contrast for the Omarchy theme active at the next start. lgse/strata#1816
- Any other legacy global `omarchy_variant` value is dropped. lgse/strata#1816
- Strata never writes `omarchy_variant` back; after the next save, `settings.toml` has no such key. lgse/strata#1816 (unverified)

## Design

[docs/themes.md](https://github.com/lgse/strata/blob/c94eeb0020fa1154e11c741888f1b56d92ce70d6/docs/themes.md) describes the Quattro mapping and the variants. [docs/preferences.md](https://github.com/lgse/strata/blob/c94eeb0020fa1154e11c741888f1b56d92ce70d6/docs/preferences.md) covers per-theme storage and the legacy migration.

- Only Quattro's current-theme state is read. Legacy Omarchy layouts and alacritty color extraction are intentionally unsupported.
- Surfaces come from Quattro's own keys: `background`, `dark_background`, `lighter_background`, `selection`, and `muted`. Missing ones derive from `background` and `foreground` (lgse/strata#1816).
- ANSI `color8` was dropped. It is not part of Omarchy's `colors.toml` format and varies between themes; where it is bright gray, every surface turned gray (lgse/strata#1815).
- Availability is sampled at startup and re-checked by the state monitor on each change. The re-check accepts `current` plus `theme.name` so Omarchy's staged switch does not flicker following off (lgse/strata#857, lgse/strata#958).
- Variants exist because terminals and Btop draw near-black backgrounds while Strata's mapping drew lighter surfaces from the same palette (lgse/strata#1198).
- When Quattro state is briefly invalid, as midway through an Omarchy theme switch, previews keep the last applied palette. They do not fall back to the built-in theme (lgse/strata#1429, lgse/strata#1554).
- Darker, now the default, only moves file columns onto `dark_background`. It replaced lgse/strata#1482's Darker, which derived near-black surfaces and turned light palettes dark (lgse/strata#1815, lgse/strata#1816).
- Contrast keeps hues and moves only luminance toward black or white, stepping each foreground until its contrast target is met (lgse/strata#1482, lgse/strata#1816).
- The variant is remembered per theme. One global choice made people revisit Settings on every switch between light and dark Omarchy themes (lgse/strata#1815).
- Only a legacy `high_contrast` migrates, because older versions always saved `original` (lgse/strata#1816).
- Contrast targets apply to semantic tokens, not to every composited or disabled widget state.

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-05 | lgse/strata#1482 | feat | Added Original, Darker, and High contrast variants and ignored invalid Quattro colors. |
| 2026-09-14 | lgse/strata#958 | fix | Turned following off and restored the built-in theme when Quattro state disappears. |

## Known gaps

None known.
