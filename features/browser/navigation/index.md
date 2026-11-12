---
title: Navigation
status: shipped
origin: {issue: lgse/strata#70, pr: lgse/strata#118}
branch: null
reviewed_at: 5f17c9fdc8967e1b4ba8aaf8de113b46d824b0dd
review: draft
code: [src/ui/window/composition/input.rs, crates/strata-fs/src/app/browser/columns.rs, crates/strata-fs/src/app/browser/navigate.rs, crates/strata-fs/src/app/navigation/history.rs]
tests: [crates/strata-fs/src/app/browser/tests/navigation.rs, tests/qa/scenarios/locations/unreadable-location-reports-error.jsonl, crates/strata-fs/src/app/navigation/tests/history.rs, crates/strata-fs/src/app/browser/tests/navigation/returning_columns.rs, tests/qa/scenarios/view_switching/returning-to-columns-follows-selection.jsonl]
docs: [site/src/reference/keyboard-navigation.md]
related: [browser/tabs, browser/view-modes, browser/view-modes/position-restore, integration/10xer-mode, browser/view-modes/columns]
---

## Summary

Moving between locations in a browser pane: Back, Forward, and Parent history from keys, mouse buttons, and pane-header buttons. Children: `browser/navigation/location-bar` (path entry and breadcrumbs), `browser/navigation/recent` (the Recent collection), and `browser/navigation/startup-arguments` (command-line locations). Also `browser/navigation/folder-jump` (Ctrl+Shift+K over visited folders) and `browser/navigation/administrator-access` (unreadable local folders through `admin://`). `browser/navigation/back-history` is the List and Icons Back button's menu of earlier locations. `browser/navigation/first-column` is Alt+Down, which makes the focused Columns column the first. Restoring an Icons or List folder's position on return belongs to `browser/view-modes/position-restore`. Selecting the folder you came from in Columns belongs to `browser/view-modes/columns`, and the List and Icons pane-header history buttons to `browser/view-modes`. This node also covers which Columns child column survives a switch back from List or Icons.

## Behavior

### Back, Forward, and Parent

- Alt+Left, Alt+Right, and Alt+Up go Back, Forward, and to the parent folder in every view mode and key map. lgse/strata#358
- Alt+Home opens the home folder. lgse/strata#1576 (unverified)
- With `parent_folder = ["<Control>e"]` and the file list focused, Ctrl+E opens the parent folder. lgse/strata#1885
- `history_back`, `history_forward`, and `home_folder` bound to a Ctrl or Super key work the same way with the file list focused. lgse/strata#1885
- That Ctrl+E binding also fires on Ctrl+Shift+E, since these jumps ignore Shift. lgse/strata#1885 (unverified)
- In 10xer mode, a key added to `history_back` under `[keymap.default]` also goes Back. lgse/strata#1885
- So does `history_forward`; 10xer's own Back and Forward keys come from `[keymap.tenxer]`. lgse/strata#1885 (unverified)
- Backspace in Columns closes the focused nested column and its descendants. From the root column it opens the parent folder, selecting the root column's folder. lgse/strata#58, lgse/strata#1437, lgse/strata#1544
- Backspace in List and Icons opens the parent folder. lgse/strata#485

### Returning to Columns

- In Columns with `documents` open as the child column, switch to List, press Escape, then Ctrl+1. No child column reopens, and the breadcrumb ends at the active folder. lgse/strata#2070
- On the switch back to Columns, an open child column the List or Icons selection no longer holds closes, with Mirror columns selection on or off. lgse/strata#2070
- With several items selected and the open child not among them, the child column closes and none opens. lgse/strata#2070
- An open child column stays open when it is selected, alone or among several selected items. lgse/strata#2070 (unverified)
- With Mirror columns selection on, select only `pictures` in Icons and press Ctrl+1. `pictures` opens as the child column, and the parent column keeps focus. lgse/strata#2070
- A folder the load selected automatically, as on a first visit, opens no child column on the switch back. lgse/strata#2070
- While a navigation is still validating, such as a remote folder opened in List, the switch back closes and opens no columns. That navigation still opens. lgse/strata#2070
- While the active column is reloading, the switch back neither closes nor opens a child column. lgse/strata#2070
- Closing a stale child column on the switch back adds no Back history entry. lgse/strata#2070 (unverified)

### Unreadable folders

- In Columns, opening an unreadable folder not yet marked locked, or any where GIO has no `admin` scheme, shows an "Unable to open directory" dialog. lgse/strata#1807, lgse/strata#1837 (unverified)

### Mouse buttons

- Mouse button 8 goes Back and button 9 goes Forward over the header, breadcrumbs, sidebar, file view, and preview. lgse/strata#118
- At the oldest or newest history entry, the button does nothing, and other mouse buttons keep their normal actions. lgse/strata#118
- While a modal overlay is open, buttons 8 and 9 do not navigate the window behind it. lgse/strata#118

## Design

[docs/keyboard-navigation.md](https://github.com/lgse/strata/blob/72b840e69d6f0df9d33fb5583e62a3a2944886a1/docs/keyboard-navigation.md) carries the key map and the "Returning to a visited directory" and "Refreshing a directory" rules.

- History lives in each tab's browser, so tabs keep separate Back and Forward stacks (docs/keyboard-navigation.md).
- Alt+arrows stay history keys in every mode because plain arrows move focus between panes, header controls, and the sidebar (lgse/strata#358).
- The mouse-button controller sits in the bubble phase on the window root. It covers every normal region while modal overlays stay isolated, and leaves unavailable actions unclaimed (lgse/strata#118).
- On a return to Columns the selection, not the cursor, drives the child column. Before, the rebuild reopened every column the browser still held, so a child the selection had left reopened with its open-path fill (lgse/strata#2016, lgse/strata#2070, commit 45f1ead8).
- Closing or opening a column bumps the navigation generation, which would drop a navigation still validating, so the step changes nothing while one is pending (lgse/strata#2070, commit 2d56db6e).
- A reloading column is empty until its selection is restored. The step waits, so it never reads an empty selection and closes a child still selected (lgse/strata#2070, commit dc0bc580).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-11-06 | lgse/strata#2070 | fix | Made the Columns child column follow the selection List or Icons left, instead of reopening a stale child on the switch back. |
| 2026-09-02 | lgse/strata#118 | feat | Mapped mouse buttons 8 and 9 to Back and Forward across the window. |

## Known gaps

- With Mirror columns selection off, a round trip through List closes a child column that differs from the selected folder. That happens even if the selection never changed. lgse/strata#2070
