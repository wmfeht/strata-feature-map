---
title: Click modes
status: shipped
origin: {issue: lgse/strata#213, pr: lgse/strata#220}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: []
tests: [tests/e2e/scenarios/test_click_modes.py]
related: [preview/quick-preview, operations/rename, browser/sidebar]
---

## Summary

Whether one or two clicks open a file or a folder, set separately for files and folders in each of Columns, Icons, and List. Also covers which entry is selected after a folder opens by pointer or keyboard.

## Behavior

### Preference

- Settings → General → Opening items offers Single or Double for Files and for Folders in Columns, Icons, and List views. lgse/strata#220
- Files default to Double in every view; folders default to Single in Columns and Double in Icons and List. lgse/strata#220
- A changed click count applies to open windows without restarting and persists across restarts. lgse/strata#220
- Single-click file previews stay a separate preference; a single click may preview a file that needs two clicks to open. lgse/strata#220

### Opening

- With Single set, one click on a folder opens it. lgse/strata#220
- With Double set, one click on a folder only selects it. lgse/strata#220
- With Double set, two clicks slower than the double-click interval select without opening. lgse/strata#220 (unverified)
- With Single set, Ctrl+click or Shift+click on an entry changes the selection without opening it. lgse/strata#220, lgse/strata#203
- With Single set in Columns, one click on a folder in a partly hidden parent column opens it, even if the column scrolls during the press. lgse/strata#1502
- Arrow keys select entries without opening them in single-click mode. lgse/strata#220 (unverified)

### Selection after opening

- Opening a folder with the pointer leaves its entries unselected. lgse/strata#715
- Opening a folder with Enter selects its first entry. lgse/strata#715
- Clicking a sidebar place selects nothing in the new listing; Enter on a sidebar place selects the first entry. lgse/strata#715

## Design

List view, then called Explorer, opened files on the single click meant to select them (lgse/strata#213). Per-view, per-kind counts were chosen over a global double-click switch, which could not separate files from folders (lgse/strata#213).

- GTK's `single_click_activate` also selects rows on hover, which collapsed Ctrl+click, Shift+click, and marquee selections. List therefore stopped using it (lgse/strata#203).
- Pointer folder opening leaves children unselected so the opened folder itself can be chosen, for example in a folder chooser. Keyboard opening selects the first entry so arrows continue (lgse/strata#714).
- Quick preview was kept independent of activation from the start (lgse/strata#213).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-09 | lgse/strata#715 | fix | Selected the first child only when a folder opens from the keyboard. |
| 2026-09-03 | lgse/strata#220 | feat | Added per-view single- or double-click preferences for files and folders, defaulting files to double. |

## Known gaps

- In Columns, a plain click on a folder or file inside a multi-selection collapses the selection without opening or previewing it; the fix is unmerged. lgse/strata#1446, lgse/strata#1546
