---
title: Text size
status: shipped
origin: {issue: lgse/strata#155, pr: lgse/strata#252}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [src/ui/preferences/text_size.rs]
tests: [src/ui/preferences/tests/text_size.rs, src/ui/theme/tests/text_size.rs, tests/e2e/scenarios/test_text_size.py]
docs: [docs/preferences.md]
related: [settings/preferences, settings/themes]
---

## Summary

An app-wide interface text size in logical pixels, set in Settings, in the Appearance menu, or with zoom shortcuts. Every window, view, menu, and dialog scales with it.

## Behavior

### Changing the size

- Settings → Appearance → Text has a "Text size" spin button, accessible name "Text size in pixels", accepting 8 to 48; the default is 13. lgse/strata#838
- The Appearance menu's text-size row has decrease and increase buttons around an "N px" button that resets the size to 13. lgse/strata#951
- Ctrl++, Ctrl+=, or Ctrl+keypad + increases the size by 1 px; Ctrl+− or Ctrl+keypad − decreases it; Ctrl+0 or Ctrl+keypad 0 resets it to 13. lgse/strata#838
- The same keys with Alt or Super held do not change the size. lgse/strata#838
- The shortcuts work while an inline rename editor is open, without submitting it. lgse/strata#838
- Ctrl+wheel changes the size by 1 px per notch, accumulating smooth touchpad deltas into whole steps. lgse/strata#1069, lgse/strata#1140
- Ctrl+wheel over a PDF preview, including its scrollbars, zooms the PDF instead. lgse/strata#1069
- The portal file chooser accepts the same keyboard shortcuts. lgse/strata#838 (unverified)

### Applying the size

- A change applies at once to every open window and to views built afterwards. lgse/strata#838
- The size is saved as an integer `text_size`; saved `"small"`, `"medium"`, and `"large"` load as 11, 13, and 15 px; unknown names load as 13 and out-of-range numbers are clamped. lgse/strata#838
- Desktop text scaling multiplies the size once and the result is rounded to a whole pixel; changing desktop scaling reapplies it live. lgse/strata#495, lgse/strata#838
- Toolbar and row icons scale with the text size; Icons thumbnail size and preview zoom do not. lgse/strata#838

## Design

[docs/preferences.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/preferences.md) describes the setting under "Text size and display scaling".

- The size sets the root `window` font-size through ThemeManager's CSS provider. `style.css` sizes almost everything in `em`, so one value scales the app and keeps its hierarchy (lgse/strata#252). Desktop-wide scaling was rejected because it changes every application (lgse/strata#155).
- CSS pixels bypass GTK's desktop text-scaling DPI, so Strata multiplies the size by that factor once. With slight hinting, fractional results such as 17.73 px dropped the cap-height pixel row, so the product is rounded (lgse/strata#442, lgse/strata#495).
- Small, Medium, and Large were replaced by a number because 15 px was still hard to read on a 4K monitor (lgse/strata#831).
- Monitor scaling is left to GTK to avoid double scaling, so moving a window between monitors never rewrites the saved size (lgse/strata#831).
- Ctrl+wheel is handled in the capture phase so scrolled windows cannot consume it first. The PDF scroll container keeps its own zoom (lgse/strata#1069, lgse/strata#1110).
- The wheel controller accumulates deltas itself instead of using GTK's discrete mode, which consumed every touchpad scroll before descendant scrollers saw it (lgse/strata#1140).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-18 | lgse/strata#1069 | feat | Stepped text size with Ctrl+wheel, leaving PDF zoom to the PDF preview. |
| 2026-09-13 | lgse/strata#951 | feat | Grouped the Appearance controls as minus, current size, and plus. |
| 2026-09-12 | lgse/strata#838 | feat | Replaced the three presets with an 8–48 px size, zoom shortcuts, and scaled layouts. |
| 2026-09-06 | lgse/strata#495 | fix | Rounded desktop-scaled text to whole pixels to stop clipped glyphs. |
| 2026-09-04 | lgse/strata#252 | feat | Added a Small, Medium, and Large text size and unified menu typography. |

## Known gaps

- At desktop text scaling 1.18, the default 13 px rounds to 15 px and glyph tops can still clip. The issue was closed as a GTK rendering problem; the opt-in Cairo renderer avoids it. lgse/strata#1310, lgse/strata#1218
