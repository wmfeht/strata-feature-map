---
title: Browser tabs
status: shipped
origin: {issue: lgse/strata#108, pr: lgse/strata#1484}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: reviewed
code: [src/ui/window/composition/tabs.rs, src/ui/window/composition/tabs/**, src/ui/browser/tab_location.rs]
tests: [src/ui/window/composition/tabs/tests.rs, src/ui/browser/tab_location/tests.rs, tests/e2e/scenarios/test_tabs.py]
docs: [docs/keyboard-navigation.md, docs/10xer-mode.md]
related: [integration/10xer-mode, operations/drag-and-drop, operations/progress/dock]
---

## Summary

In-memory tabs within one Strata window, each holding its own browsing context. A tab strip, keyboard shortcuts in both key maps, and drag reordering create, switch, close, and move tabs. Files dropped on a tab transfer into that tab's directory.

## Behavior

### Creating and closing

- Ctrl+T, the New tab (+) button, or 10xer `t` then `n` opens a tab at the active tab's location and selects it. lgse/strata#1484
- A new tab is added at the right end of the strip. lgse/strata#1484 (unverified)
- Each tab keeps its own location, selection, navigation history, preview, and search state when another tab is selected. lgse/strata#1484
- Changing Show hidden files updates the listings of hidden tabs and of tabs opened later. lgse/strata#108, lgse/strata#1484
- Ctrl+W, a tab's X button, or 10xer `t` then `x` closes that tab; closing the last tab closes the window. lgse/strata#1484
- Middle-clicking a tab closes it. lgse/strata#1484 (unverified)
- Closing the active tab selects its right neighbour, or its left neighbour when it was last. lgse/strata#1484 (unverified)

### Switching

- Ctrl+Tab and Ctrl+Page Down select the next tab; Ctrl+Shift+Tab and Ctrl+Page Up select the previous one. Each wraps at either end. lgse/strata#1484, lgse/strata#1506
- Ctrl+Shift+1 to Ctrl+Shift+9 select tabs 1 to 9 and Ctrl+Shift+0 selects tab 10, counted in current strip order. lgse/strata#1484
- In 10xer mode, `t` then `1` to `9` or `0` selects tabs 1 to 10, and `t` then `t` selects the previous tab, wrapping from first to last. lgse/strata#1484
- Escape after `t` cancels the pending tab chord. lgse/strata#1484
- Typing `t`, `n`, or `x` in a text field such as the location editor enters literal text. lgse/strata#1484
- Holding Ctrl+Shift shows number badges `1` to `9` and `0` beside the first ten tab labels. lgse/strata#1484
- Badges hide when Ctrl or Shift is released or the window loses focus. lgse/strata#1484 (unverified)
- Keypad Page Up and Page Down work like Page Up and Page Down, and Caps Lock does not block the shortcuts. lgse/strata#1506
- Page Up and Page Down tab shortcuts with Alt, Super, Meta, or Hyper added do nothing to tabs. lgse/strata#1506
- Selecting a tab returns focus to the widget it last focused, or to its file view when that widget is gone. lgse/strata#1484 (unverified)
- While a modal dialog is open, tab shortcuts and the New tab button do not create, switch, close, or move tabs. lgse/strata#1506

### Reordering

- Ctrl+Shift+Page Up and Ctrl+Shift+Page Down move the active tab one position left or right without changing the selected tab. lgse/strata#1506
- Moving stops at either end of the strip instead of wrapping. lgse/strata#1506
- Moving keeps the tab's location, selection, and location-editor focus. lgse/strata#1506
- Dragging a tab label onto another tab moves it to that position, and the drag image shows the tab's label. lgse/strata#1484, lgse/strata#1506
- Numbered shortcuts and Ctrl+Page Up and Page Down follow the reordered strip. lgse/strata#1484, lgse/strata#1506
- The F1 shortcut reference lists the tab switching and moving shortcuts in both key maps. lgse/strata#1506

### Strip

- The strip appears only with two or more tabs. The New tab and window-close buttons then move into it and return to the header at one tab. lgse/strata#1484
- With Show close button off, the window-close button stays hidden while tabs are opened, selected, and closed. lgse/strata#1129
- A 3 px accent underline slides to the selected tab, and jumps without sliding when animations are disabled. lgse/strata#1484
- When the strip is wider than the window, the wheel scrolls it horizontally and no scrollbar is shown. lgse/strata#1484
- Selecting a tab scrolls it into view. lgse/strata#1484
- Selecting the last tab also scrolls the New tab button into view. lgse/strata#1484 (unverified)
- Hovering an inactive tab accents its label; its X turns accent only while the pointer is over the X itself. lgse/strata#1484

### Tab names

- A tab is named after its active directory: `~` for the home folder, `/` for the root, and Trash, Recent, or Network for those locations. lgse/strata#1484 (unverified)
- Names longer than 22 characters are ellipsized. lgse/strata#1484 (unverified)
- In Columns, pressing on a folder keeps the tab's previous name until release, then shows the folder's name with no parent name in between. lgse/strata#1507
- A cancelled click, a folder drag, a folder deleted before release, or a refused navigation restores the active directory's name. lgse/strata#1507
- Moving keyboard focus to a parent column renames the tab to the parent; a child column shown by Up or Down keeps the parent's name. lgse/strata#1507
- On a remote location, the name changes only after the new location validates; a rejected or superseded navigation releases it. lgse/strata#1507

### File drops

- Dropping files on another tab transfers them into that tab's current directory: a same-volume drop moves, and holding Ctrl copies. lgse/strata#1484
- Holding a file drag over a tab for 450 ms selects it, so the drop can land on a folder in its listing. lgse/strata#1484
- A tab under a file drag accents its label and shows no drop outline. lgse/strata#1484

## Design

Issue lgse/strata#108 asked for tabs that each own a multi-pane workspace, driven by a `Ctrl+S` prefix. The owner instead requested Material-style tabs from a prototype video, with Ctrl+T in both key maps; multi-pane work was deferred (lgse/strata#108, lgse/strata#1300).

- Each tab is a complete window content: header, sidebar, browser, footer, and preview. Tabs sit in one `gtk::Stack`, and only the active tab's actions are installed on the window. Preferences and the clipboard stay window-wide (lgse/strata#1484).
- Tabs are in memory only. Persistence was left out of the first version as lifecycle and recovery complexity it did not need (lgse/strata#108).
- Tab shortcuts run in a capture-phase window controller, and each tab's key handling skips them. They therefore work from text fields and in both key maps (lgse/strata#1484, lgse/strata#1506).
- Ctrl+T previously opened a terminal (lgse/strata#161). That moved to Ctrl+Alt+T, and 10xer keeps `;` then `t` (lgse/strata#1484).
- Ctrl+Page Up and Page Down match web browsers and stay Ctrl-only, like Strata's other Linux shortcuts (lgse/strata#1505). Switching wraps like Ctrl+Tab; moving stops at the edges (lgse/strata#1506).
- A reorder drag carries a random per-window token, so only this window's tab drags reorder and file drags never do (lgse/strata#1484).
- One close guard checks every tab, so a background operation in a hidden tab still blocks closing the window (lgse/strata#1484).
- Closing a tab disposes its content and releases its observers (lgse/strata#108, lgse/strata#1484).
- The name hold tracks navigation settlement explicitly rather than using a timer. Cancelled, refused, and same-directory navigation release it, and an older validation completion cannot release a newer click (lgse/strata#1507).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-07 | lgse/strata#1506 | feat | Added Ctrl+Page Up/Down switching and Ctrl+Shift+Page Up/Down reordering, like web browsers. |
| 2026-10-07 | lgse/strata#1507 | fix | Held the tab name during a pending folder click so it no longer flickers to the parent. |
| 2026-10-05 | lgse/strata#1484 | feat | Added in-memory tabs with a Material-style strip, shortcuts in both key maps, reordering, and cross-tab drops. |

## Known gaps

- Open tabs are lost when Strata quits; restoring them merged after this snapshot. lgse/strata#1531, lgse/strata#1532
- A folder cannot be opened directly into a new tab or window from its menu, a middle-click, or Ctrl+Enter. lgse/strata#1540, lgse/strata#1543
- Each tab holds one pane; split or dual-pane browsing is undecided. lgse/strata#47
