---
title: Frame and content density
status: shipped
origin: {issue: lgse/strata#1774, pr: lgse/strata#1776}
branch: null
reviewed_at: be3343a5992a2a5497b1a2ee7faa525be18e988f
review: draft
code: [src/ui/window/density_slider.rs]
tests: [src/ui/window/tests/appearance_density.rs, src/ui/theme/tests/density.rs, src/ui/preferences/tests/preferences.rs]
docs: [docs/preferences.md]
related: [settings/themes, browser/view-modes/columns, browser/view-modes/icons, browser/view-modes/list, browser/sidebar, browser/tabs, preview/preview-panel/layout, settings/preferences/storage]
---

## Summary

Two spacing settings in the Appearance menu's DENSITY section. Frame is the vertical inset of the window's bars, and Content the spacing of rows and Icons cards. Each is a px slider with Compact and Airy snap points.

## Behavior

### Sliders

- The Appearance menu's DENSITY section shows a "Frame" slider above a "Content" slider. lgse/strata#1776
- Frame runs from 0 to 12 px, with Compact 0, the default, and Airy 4. lgse/strata#1776
- Content runs from 0 to 16 px, with Compact 4, the default, and Airy 8. lgse/strata#1776
- Each slider's value label reads "Compact · N px" or "Airy · N px" at a preset, otherwise "Custom · N px". lgse/strata#1776
- Each slider has tick marks at its Compact and Airy values, with "Compact" and "Airy" buttons under them. lgse/strata#1776
- Clicking "Compact" or "Airy" snaps that slider to the preset; the label of the current preset shows in the accent color. lgse/strata#1776 (unverified)
- Dragging a slider or clicking a snap button leaves the Appearance menu open. lgse/strata#1776
- Changing one slider leaves the other area's spacing unchanged. lgse/strata#1774, lgse/strata#1776
- A change in one window moves the slider, value label, and snap highlight in every other open window. lgse/strata#1776
- A mouse wheel over a slider scrolls the menu and leaves the value unchanged. lgse/strata#1776 (unverified)
- Left and Right step a focused slider by 1 px; Page Up and Page Down step it by 4 px. lgse/strata#1776 (unverified)
- Each slider's accessible label is "Frame" or "Content", and its accessible value text is its value label. lgse/strata#1776 (unverified)
- The snap button of the current preset exposes the accessible pressed state. lgse/strata#1776 (unverified)

### Saved settings

- `frame_density` and `browser_density` hold `"compact"`, `"airy"`, or `"custom"`; `frame_density_custom_px` and `browser_density_custom_px` are read only for `"custom"`. lgse/strata#1776
- A slider resting on a preset's value saves the preset. Content at 4 px saves `browser_density = "compact"`; Frame at 4 px saves `frame_density = "airy"`. lgse/strata#1776
- Each change is saved immediately. lgse/strata#1776
- A Custom value above the maximum loads clamped: 200 loads as Frame 12 or Content 16. lgse/strata#1776 (unverified)
- A settings file with only `browser_density` loads, with Frame at Compact, 0 px. lgse/strata#1776
- An unrecognized mode such as `browser_density = "bogus"` loads as Compact. lgse/strata#1776 (unverified)

## Design

[docs/preferences.md](https://github.com/lgse/strata/blob/4b9a6ace71017888b3a2124d7d911c5c664cc767/docs/preferences.md) describes the setting under "Content and Frame density".

- Frame and content density are separate settings. The issue, lgse/strata#1774, rejected widening the single density setting, presets without a custom value, and a control per component.
- The issue asked for accordion rows, each with Compact, Airy, and a custom pixel control. The PR shipped two sliders with preset ticks instead (lgse/strata#1774, lgse/strata#1776).
- One Frame inset applies in lock step to every bar. The header, tab strip, sidebar rows, and Miller, Icons/List, and preview headers keep aligned heights (lgse/strata#1776).
- Both settings implement `DensityScale`, whose Compact and Airy values are snap points. `from_px` maps a snap value to its preset, so a slider on a preset saves the preset (lgse/strata#1776).
- Custom Content values extrapolate linearly through the static Compact and Airy rules, so the slider never jumps at a preset (lgse/strata#1776).
- `settings/themes` records how the generated density CSS is loaded and reloaded (lgse/strata#1776).
- Frame uses padding and `margin-left` only, so fixed minimum heights and button widths still hold (lgse/strata#1776).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-21 | lgse/strata#1776 | feat | Replaced the Appearance menu's Compact and Airy radios with Frame (0–12 px) and Content (0–16 px) sliders, so chrome and file-view spacing are set separately. |

## Known gaps

None known.
