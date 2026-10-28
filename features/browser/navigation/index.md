---
title: Navigation
status: shipped
origin: {issue: lgse/strata#70, pr: lgse/strata#118}
branch: null
reviewed_at: 73b3258ff9da7fd5f8b279e442e4fbf576850deb
review: draft
code: [src/ui/window/composition/input.rs]
tests: [src/app/browser/tests/navigation.rs, tests/qa/scenarios/locations/unreadable-location-reports-error.jsonl]
docs: [site/src/reference/keyboard-navigation.md]
related: [browser/tabs, browser/view-modes, browser/view-modes/position-restore, integration/10xer-mode]
---

## Summary

Moving between locations in a browser pane: Back, Forward, and Parent history from keys, mouse buttons, and pane-header buttons. Children: `browser/navigation/location-bar` (path entry and breadcrumbs), `browser/navigation/recent` (the Recent collection), `browser/navigation/startup-arguments` (locations passed on the command line), and `browser/navigation/folder-jump` (Ctrl+Shift+K over visited folders). Restoring an Icons or List folder's position on return belongs to `browser/view-modes/position-restore`. Selecting the folder you came from in Columns belongs to `browser/view-modes/columns`, and the List and Icons pane-header history buttons to `browser/view-modes`.

## Behavior

### Back, Forward, and Parent

- Alt+Left, Alt+Right, and Alt+Up go Back, Forward, and to the parent folder in every view mode and key map. lgse/strata#358
- Alt+Home opens the home folder. lgse/strata#1576 (unverified)
- With `history_back`, `history_forward`, `parent_folder`, or `home_folder` bound to a Ctrl or Super key, such as `parent_folder = ["<Control>e"]`, that key performs its jump in a browser window. lgse/strata#1885
- Backspace in Columns closes the focused nested column and its descendants. From the root column it opens the parent folder, selecting the root column's folder. lgse/strata#58, lgse/strata#1437, lgse/strata#1544
- Backspace in List and Icons opens the parent folder. lgse/strata#485

### Unreadable folders

- Selecting or opening a folder Strata may not read, such as after `chmod 000`, shows an "Unable to open directory" dialog saying you do not have permission. lgse/strata#1807 (unverified)

### Mouse buttons

- Mouse button 8 goes Back and button 9 goes Forward over the header, breadcrumbs, sidebar, file view, and preview. lgse/strata#118
- At the oldest or newest history entry, the button does nothing, and other mouse buttons keep their normal actions. lgse/strata#118
- While a modal overlay is open, buttons 8 and 9 do not navigate the window behind it. lgse/strata#118

## Design

[docs/keyboard-navigation.md](https://github.com/lgse/strata/blob/72b840e69d6f0df9d33fb5583e62a3a2944886a1/docs/keyboard-navigation.md) carries the key map and the "Returning to a visited directory" and "Refreshing a directory" rules.

- History lives in each tab's browser, so tabs keep separate Back and Forward stacks (docs/keyboard-navigation.md).
- Alt+arrows stay history keys in every mode because plain arrows move focus between panes, header controls, and the sidebar (lgse/strata#358).
- The mouse-button controller sits in the bubble phase on the window root. It covers every normal region while modal overlays stay isolated, and leaves unavailable actions unclaimed (lgse/strata#118).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-02 | lgse/strata#118 | feat | Mapped mouse buttons 8 and 9 to Back and Forward across the window. |

## Known gaps

- Back and Forward have no menu of earlier entries for jumping several steps at once. The first attempt was closed because it broke the existing arrows. lgse/strata#1232
