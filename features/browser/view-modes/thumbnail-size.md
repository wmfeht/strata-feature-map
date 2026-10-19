---
title: Thumbnail size shortcuts
status: shipped
origin: {issue: lgse/strata#1720, pr: lgse/strata#1721}
branch: null
reviewed_at: e0f73973926ff67e77c2c56cf288b7b7617bb2e5
review: draft
code: [src/ui/browser_modes/thumbnail_size.rs]
tests: [src/ui/browser_modes/thumbnail_size/tests.rs, src/ui/window/tests/keyboard_dispatch/thumbnail_size.rs, tests/e2e/scenarios/test_thumbnail_size.py]
docs: [docs/preferences.md, docs/10xer-mode.md]
related: [browser/view-modes/icons, browser/view-modes/folder-views, browser/view-modes/text-size, integration/10xer-mode, integration/portal-file-chooser, app/shortcut-reference, operations/progress/dock]
---

## Summary

Keyboard and wheel shortcuts that step the Icons thumbnail size along a fixed ladder of sizes, and reset it. They are for users who resize thumbnails more often than the interface text. The slider they move belongs to `browser/view-modes/icons`, and per-folder sizes to `browser/view-modes/folder-views`.

## Behavior

### Stepping

- The size steps through 32, 36, 40, 44, 48, 56, 64, 72, 80, 96, 112, 128, 144, 160, 192, 224, and 256 px. lgse/strata#1721
- In Icons, Ctrl+Alt++ or Ctrl+Alt+= moves the size one step larger. lgse/strata#1721
- In Icons, Ctrl+Alt+− moves the size one step smaller along the same sizes. lgse/strata#1721
- From a size between two steps, such as 100 px, one step up lands on 112 and one step down on 96. lgse/strata#1721
- A step up at 256 px stays at 256, and a step down at 32 px stays at 32. lgse/strata#1721 (unverified)
- In Icons, each Ctrl+Shift+wheel notch steps the size once, up for larger and down for smaller. Smooth touchpad deltas accumulate into whole steps. lgse/strata#1721
- In Icons, a Ctrl+Shift+wheel that arrives as horizontal scrolling steps the size the same way. lgse/strata#1721
- In 10xer mode, with the Icons listing focused, plain +, =, or − steps the size; Ctrl+Alt++ and Ctrl+Alt+− still work. lgse/strata#1721
- In Columns or List, none of these keys resizes anything, and Ctrl+Shift+wheel passes through to the view. lgse/strata#1721
- The portal file chooser accepts the key shortcuts but not Ctrl+Shift+wheel. lgse/strata#1721

### Reset

- In a folder with its own remembered size, Ctrl+Alt+0 clears that size, so the folder follows the default again. lgse/strata#1721
- With Remember sort and icon size per folder on, Ctrl+Alt+0 in a folder that is not remembered, such as a remote share, sets the slider to the default size. lgse/strata#1721
- With Remember sort and icon size per folder off, Ctrl+Alt+0 returns the size, which is the default, to 64 px. lgse/strata#1721

### Saving and notice

- Every step and reset moves the Thumbnail size popover's slider, so sizes are saved exactly as dragging the slider saves them. lgse/strata#1721
- With per-folder sizes on, a step changes the folder's size and leaves the default unchanged; with them off, it changes the default. lgse/strata#1721
- Each step or reset shows "Thumbnail size: Npx" in the bottom-right notice dock. lgse/strata#1721
- The notice lasts 1.2 s and shows no check icon. lgse/strata#1721 (unverified)

## Design

[docs/preferences.md](https://github.com/lgse/strata/blob/e0f73973926ff67e77c2c56cf288b7b7617bb2e5/docs/preferences.md) describes the shortcuts under "Per-folder sort and thumbnail size". [docs/10xer-mode.md](https://github.com/lgse/strata/blob/e0f73973926ff67e77c2c56cf288b7b7617bb2e5/docs/10xer-mode.md) lists the 10xer keys.

- Ctrl+wheel and Ctrl+± stay interface zoom, as in browsers and the PDF preview. Thumbnails take Ctrl+Shift+wheel and their own key family instead (lgse/strata#1720).
- The keys were chosen so they collide with nothing in the default or 10xer key maps (lgse/strata#1721).
- Every input drives the existing slider, so per-folder saving is shared with dragging and not duplicated (lgse/strata#1721).
- The ladder is finer at small sizes, where one step is a larger share of the size (lgse/strata#1721) (unverified).
- In 10xer mode the size keys are checked before the search-results keys, because the Shift that types + counts as held there (lgse/strata#1721) (unverified).
- The size notice drops the success check because it reports a value as it changes (lgse/strata#1721) (unverified).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-17 | lgse/strata#1721 | feat | Added Ctrl+Alt++/−/0, Ctrl+Shift+wheel, and 10xer +/− to step the Icons thumbnail size, with a brief size notice. |

## Known gaps

None known.
