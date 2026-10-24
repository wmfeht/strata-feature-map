---
title: Corner roundness
status: shipped
origin: {issue: lgse/strata#1678, pr: lgse/strata#1680}
branch: null
reviewed_at: c94eeb0020fa1154e11c741888f1b56d92ce70d6
review: draft
code: [src/ui/preferences/corner_roundness.rs, src/ui/theme/roundness.rs]
tests: [src/ui/theme/roundness/tests.rs, src/ui/theme/tests.rs, src/ui/settings/theme/tests.rs]
related: []
---

## Summary

An app-wide scale for corner radii, set as a percent under Settings → Appearance → Shape. It lets users square the interface at 0 or soften it up to 200, applied to every pixel radius in Strata's stylesheet.

## Behavior

### Control

- Settings → Appearance has a Shape group with a Corner roundness stepper from 0 to 200 in steps of 10. lgse/strata#1680
- The Shape group sits after Text and before File icons, and its stepper's accessible name is "Corner roundness in percent". lgse/strata#1680 (unverified)
- With no `corner_roundness` key in `settings.toml`, the stepper reads 60; a saved value, such as 100, is kept. lgse/strata#1688
- The value is saved as the integer `corner_roundness`; a saved value below 0 or above 200 loads as 0 or 200. lgse/strata#1680 (unverified)
- Changing the stepper in one window updates the stepper in every other open Settings window; building the control writes nothing to `settings.toml`. lgse/strata#1680 (unverified)
- Searching "Corner roundness", "radius", or "rounded" in Search settings shows the row on Appearance. lgse/strata#1680 (unverified)

### Applying the scale

- At 0, every pixel corner radius in Strata's stylesheet becomes 0px; at 200, each doubles, so 5px becomes 10px. lgse/strata#1680
- A change applies at once in every open window, dialog, menu, and rebuilt view; a saved value applies before Settings opens. lgse/strata#1680
- Percentage radii, which draw circles, and radii written as `0` stay unchanged at every value. lgse/strata#1680
- A scaled radius is rounded to 0.01 px, so 9px at 40% becomes 3.6px. lgse/strata#1680 (unverified)
- Radii that GTK's built-in theme supplied, such as on buttons, entries, popovers, and check boxes, scale with the setting. lgse/strata#1680
- Every switch, in Settings or elsewhere, has a 24px track radius and a 20px knob radius at 100%, so 14.4px and 12px at the 60% default. At 50% and above, including the 60% default, both are full circles. lgse/strata#1739
- Below 50%, a switch's track and knob square off together and stay concentric, so at 40% the track radius is 9.6px and the knob's 8px. lgse/strata#1739 (unverified)

## Design

[docs/preferences.md](https://github.com/lgse/strata/blob/e0f73973926ff67e77c2c56cf288b7b7617bb2e5/docs/preferences.md) describes the setting in its Corner roundness row.

- One numeric scale was chosen over named presets, which are no simpler and less flexible, and per-element controls, which add too many settings (lgse/strata#1678).
- ThemeManager reparses the shared stylesheet with scaled radii only when roundness changes; other appearance preferences go through the token provider (lgse/strata#1680).
- Radii that GTK's built-in theme supplied are restated in Strata's stylesheet so the scale reaches them (lgse/strata#1680).
- GTK caps each radius at half its box. The switch knob's radius is 5/6 of the track's, its share of the track height. Both therefore reach a full circle at the same roundness and stay concentric (lgse/strata#1738, lgse/strata#1739). This replaced one shared radius for track and thumb (lgse/strata#1680).
- The default dropped from 100 to 60 because full roundness looked too round; saved values are not migrated (lgse/strata#1687, lgse/strata#1688).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-15 | lgse/strata#1688 | feat | Lowered the default corner roundness from 100% to 60% because full roundness looked too round; saved values are kept. |
| 2026-10-14 | lgse/strata#1680 | feat | Added a 0–200% Corner roundness preference that scales every stylesheet radius, so users can square or soften the interface. |

## Known gaps

None known.
