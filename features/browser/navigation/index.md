---
title: Navigation
status: shipped
origin: {issue: lgse/strata#70, pr: lgse/strata#118}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [src/ui/window/composition/input.rs, src/ui/browser_modes/navigation.rs]
tests: [src/app/browser/tests/navigation.rs]
docs: [docs/keyboard-navigation.md]
related: [browser/tabs, browser/view-modes, integration/10xer-mode]
---

## Summary

Moving between locations in a browser pane: Back, Forward, and Parent history from keys, mouse buttons, and pane-header buttons. Children: `browser/navigation/location-bar` (path entry and breadcrumbs), `browser/navigation/recent` (the Recent collection), `browser/navigation/startup-arguments` (locations passed on the command line), and `browser/navigation/folder-jump` (Ctrl+Shift+K over visited folders).

## Behavior

### Back, Forward, and Parent

- Alt+Left, Alt+Right, and Alt+Up go Back, Forward, and to the parent folder in every view mode and key map. lgse/strata#358
- Backspace in Columns closes the focused nested column and its descendants; from the root column it opens the filesystem parent. lgse/strata#58
- Backspace in List and Icons opens the parent folder. lgse/strata#485
- List and Icons pane headers show Back, Forward, and Parent folder buttons, each insensitive when its target is unavailable. lgse/strata#485 (unverified)
- In 10xer mode, List and Icons hide the pane header with the Back, Forward, and Parent buttons. lgse/strata#1304

### Mouse buttons

- Mouse button 8 goes Back and button 9 goes Forward over the header, breadcrumbs, sidebar, file view, and preview. lgse/strata#118
- At the oldest or newest history entry, the button does nothing, and other mouse buttons keep their normal actions. lgse/strata#118
- While a modal overlay is open, buttons 8 and 9 do not navigate the window behind it. lgse/strata#118

### Returning to a List folder

- Back or Up into a List folder restores its previous scroll position, selection, and keyboard cursor once its entries load. lgse/strata#893
- After that restore, Down continues from the restored row rather than the first row. lgse/strata#893
- A restored selection does not make Ctrl+V paste into the selected folder until the user selects it explicitly. lgse/strata#893
- Opening a typed file path, a Ctrl+K result, or Open file location selects that target instead of the remembered row. lgse/strata#1499

## Design

[docs/keyboard-navigation.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/keyboard-navigation.md) carries the key map and the "Returning to an Icons or List directory" rules.

- History lives in each tab's browser, so tabs keep separate Back and Forward stacks (docs/keyboard-navigation.md).
- Alt+arrows stay history keys in every mode because plain arrows move focus between panes, header controls, and the sidebar (lgse/strata#358).
- The mouse-button controller sits in the bubble phase on the window root. It covers every normal region while modal overlays stay isolated, and leaves unavailable actions unclaimed (lgse/strata#118).
- List position memory is temporary browsing state for the last 128 directories, matched by location rather than row number, so deleted entries are never selected by accident (lgse/strata#893).
- An explicit target beats the remembered position because the user named it (lgse/strata#1499).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-02 | lgse/strata#118 | feat | Mapped mouse buttons 8 and 9 to Back and Forward across the window. |

## Known gaps

- Back and Forward have no menu of earlier entries for jumping several steps at once; the change is unmerged. lgse/strata#1232
