---
title: Browser tabs
status: shipped
origin: {issue: lgse/strata#108, pr: lgse/strata#1484}
branch: null
reviewed_at: bf26829b4fd74c1f25ac170aad9521a633234a30
review: draft
code: [src/ui/window/composition/tabs.rs, src/ui/window/composition/tabs/**, src/ui/browser/tab_location.rs]
tests: [src/ui/window/composition/tabs/tests.rs, src/ui/window/composition/tabs/tests/reopen.rs, src/ui/browser/tab_location/tests.rs, src/ui/window/tests/keyboard_dispatch/open_in_new.rs, tests/qa/scenarios/tabs]
docs: [site/src/reference/keyboard-navigation.md, site/src/reference/10xer-mode.md]
related: [integration/10xer-mode, operations/drag-and-drop, operations/progress/dock, browser/context-menu, browser/scrolling]
---

## Summary

Tabs within one Strata window, each holding its own browsing context. A tab strip, keyboard shortcuts in both key maps, and drag reordering create, switch, close, reopen, and move tabs. The window title follows the active tab. Folders open in a new tab or window from their menu, a middle-click, or Ctrl+Enter and Shift+Enter. Files dropped on a tab transfer into that tab's directory. Child: `browser/tabs/session-restore` (reopening the previous tabs on a plain launch).

## Behavior

### Creating and closing

- Ctrl+T, the New tab (+) button, or 10xer `t` then `n` opens a tab at the active tab's location and selects it. lgse/strata#1484
- A new tab is added at the right end of the strip. lgse/strata#1484 (unverified)
- Each tab keeps its own location, selection, navigation history, preview, and search state when another tab is selected. lgse/strata#1484
- Changing Show hidden files updates the listings of hidden tabs and of tabs opened later. lgse/strata#108, lgse/strata#1484
- Ctrl+W, a tab's X button, or 10xer `t` then `x` closes that tab; closing the last tab closes the window. lgse/strata#1484
- Middle-clicking a tab closes it. lgse/strata#1484 (unverified)
- Closing the active tab selects its right neighbour, or its left neighbour when it was last. lgse/strata#1484 (unverified)

### Reopening

- Ctrl+Shift+T, or the window action `win.reopen-tab`, reopens the last closed tab at its location and former position, and selects it. lgse/strata#1800
- Repeated Ctrl+Shift+T reopens closed tabs newest first, up to 20; a 21st close drops the oldest entry. lgse/strata#1800
- Ctrl+W, the X button, a middle-click, 10xer `t` then `x`, and closing an inactive tab each record the closed tab. lgse/strata#1800 (unverified)
- Closed tabs belong to their window: Ctrl+Shift+T in another window opens nothing, and closing the window discards them. lgse/strata#1800 (unverified)
- Closed tabs are not saved, so they cannot be reopened after a restart. lgse/strata#1800 (unverified)
- A reopened tab keeps only its location and position; selection, navigation history, and preview start fresh. lgse/strata#1800 (unverified)
- When fewer tabs are open than the former position, the reopened tab stays at the right end. lgse/strata#1800 (unverified)
- With no closed tab recorded, Ctrl+Shift+T opens nothing and the active tab stays selected. lgse/strata#1800
- A close blocked by a modal dialog or by running operations records nothing. lgse/strata#1800
- Closing the last tab closes the window and records nothing. lgse/strata#1800
- While a modal dialog is open, Ctrl+Shift+T does nothing and keeps the history, so it works once the dialog closes. lgse/strata#1800 (unverified)
- Reopening a folder deleted after the close shows the location-unavailable overlay with Retry; Retry loads it once the folder exists again. lgse/strata#1800 (unverified)
- Ctrl+Shift+T works from text fields such as the location editor, in both key maps and on a Russian layout. lgse/strata#1800

### Opening folders in a new tab or window

- Middle-clicking a folder row in Columns, Icons, or List opens that folder in a new tab. lgse/strata#1540, lgse/strata#1543
- Ctrl+middle-click or Shift+middle-click on a folder row opens that folder in a new window. lgse/strata#1543
- Middle-clicking a file row selects the file in its parent folder and opens nothing. lgse/strata#1543
- A double middle-click on a folder opens one tab; a middle press dragged past the drag threshold opens nothing. lgse/strata#1543 (unverified)
- In both key maps, Ctrl+Enter on a focused folder opens it in a new tab and Shift+Enter in a new window. Keypad Enter works too. lgse/strata#1543
- Ctrl+Enter or Shift+Enter on a focused file opens it with its default application, like Enter. lgse/strata#1543
- In the default key map Ctrl+Shift+Enter on a folder opens a tab; in 10xer mode it does nothing. lgse/strata#1543 (unverified)
- Ctrl+Enter or Shift+Enter typed in a text field is left to the field. lgse/strata#1543 (unverified)
- In the portal file chooser with 10xer mode on, Ctrl+Enter on a folder still chooses it and opens no tab. lgse/strata#1543
- Open in… → New Tab or New Window on a multi-selection opens one tab or window per selected folder and skips files. lgse/strata#1543 (unverified)
- A folder opened in a new tab gets a new tab at the right end of the strip. The tab is selected, then navigated there. lgse/strata#1543 (unverified)
- A new window opened for a folder opens at the default size on that folder. lgse/strata#1543 (unverified)
- A target still unresolved after 1 s shows "Connecting to location…" in the new tab or window. lgse/strata#1543 (unverified)
- A missing or unreachable target then shows the location-unavailable overlay with Retry; a missing local folder shows it at once. lgse/strata#1543 (unverified)
- While a modal dialog is open, opening a folder in a new tab does nothing. lgse/strata#1543 (unverified)

### Switching

- Ctrl+Tab and Ctrl+Page Down select the next tab; Ctrl+Shift+Tab and Ctrl+Page Up select the previous one. Each wraps at either end. lgse/strata#1484, lgse/strata#1506
- Ctrl+Shift+1 to Ctrl+Shift+9 select tabs 1 to 9 and Ctrl+Shift+0 selects tab 10, counted in current strip order. lgse/strata#1484
- The tab digit is the key's position in the digit row: on German QWERTZ, Ctrl+Shift+2 selects tab 2. lgse/strata#1576
- Where Shift+1 types `+`, as on Swiss German, Ctrl+Shift+1 selects no tab. lgse/strata#1576
- In 10xer mode, `t` then `1` to `9` or `0` selects tabs 1 to 10, and `t` then `t` selects the previous tab, wrapping from first to last. lgse/strata#1484
- Escape after `t` cancels the pending tab chord. lgse/strata#1484
- Typing `t`, `n`, or `x` in a text field such as the location editor enters literal text. lgse/strata#1484
- Holding Ctrl+Shift without Alt or Super shows number badges `1` to `9` and `0` beside the first ten tab labels. lgse/strata#1484, lgse/strata#1576
- Badges hide when Ctrl or Shift is released or the window loses focus. lgse/strata#1484 (unverified)
- Keypad Page Up and Page Down work like Page Up and Page Down, and Caps Lock does not block the shortcuts. lgse/strata#1506
- Page Up and Page Down tab shortcuts with Alt or Super added do nothing to tabs. lgse/strata#1506, lgse/strata#1576
- Tab shortcuts ignore a held Hyper or Meta, so Ctrl+Hyper+Page Down selects the next tab. lgse/strata#1576
- Selecting a tab returns focus to the widget it last focused. When that widget is gone or can no longer take focus, its file view's cursor gets it. lgse/strata#1484, lgse/strata#1533
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
- The Home, Trash, Recent, Network, and Location names follow the interface language, such as "Papierkorb" in German. lgse/strata#1827
- Names longer than 22 characters are ellipsized. lgse/strata#1484 (unverified)
- In Columns, pressing on a folder keeps the tab's previous name until release, then shows the folder's name with no parent name in between. lgse/strata#1507
- A cancelled click, a folder drag, a folder deleted before release, or a refused navigation restores the active directory's name. lgse/strata#1507
- Moving keyboard focus to a parent column renames the tab to the parent; a child column shown by Up or Down keeps the parent's name. lgse/strata#1507
- On a remote location, the name changes only after the new location validates; a rejected or superseded navigation releases it. lgse/strata#1507

### Window title

- A window whose active tab is at folder `docs` is titled `docs — Strata`, with an em dash. lgse/strata#1824, lgse/strata#1827
- Navigating the active tab, or selecting another tab, retitles the window after the active tab's folder. lgse/strata#1827
- A window with no folder open yet is titled "Strata". lgse/strata#1827
- The title uses the tab's name, so Trash, Recent, and Network titles are translated, such as "Netzwerk — Strata". lgse/strata#1827
- The home folder titles the window `~ — Strata` and the root `/ — Strata`. lgse/strata#1827 (unverified)
- In Columns, pressing on a folder keeps the previous title until release, like the tab name. lgse/strata#1827
- A background tab that navigates leaves the window title unchanged. lgse/strata#1827 (unverified)
- The title shows a folder name over 22 characters in full, though the tab label ellipsizes it. lgse/strata#1827 (unverified)

### File drops

- Dropping files on another tab transfers them into that tab's current directory: a same-volume drop moves, and holding Ctrl copies. lgse/strata#1484
- Holding a file drag over a tab for 450 ms selects it, so the drop can land on a folder in its listing. lgse/strata#1484
- A tab under a file drag accents its label and shows no drop outline. lgse/strata#1484

## Design

Issue lgse/strata#108 asked for tabs that each own a multi-pane workspace, driven by a `Ctrl+S` prefix. The owner instead requested Material-style tabs from a prototype video, with Ctrl+T in both key maps; multi-pane work was deferred (lgse/strata#108, lgse/strata#1300).

- Each tab is a complete window content: header, sidebar, browser, footer, and preview. Tabs sit in one `gtk::Stack`, and only the active tab's actions are installed on the window. Preferences and the clipboard stay window-wide (lgse/strata#1484).
- The first version kept tabs in memory only, leaving out persistence's lifecycle and recovery complexity (lgse/strata#108). Tab locations now persist across restarts; selection, history, and preview stay in memory (lgse/strata#1531, lgse/strata#1532).
- Tab shortcuts run in a capture-phase window controller, and each tab's key handling skips them. They therefore work from text fields and in both key maps (lgse/strata#1484, lgse/strata#1506).
- Ctrl+T previously opened a terminal (lgse/strata#161). That moved to Ctrl+Alt+T, and 10xer keeps `;` then `t` (lgse/strata#1484).
- Ctrl+Page Up and Page Down match web browsers and stay Ctrl-only, like Strata's other Linux shortcuts (lgse/strata#1505). Switching wraps like Ctrl+Tab; moving stops at the edges (lgse/strata#1506).
- A reorder drag carries a random per-window token, so only this window's tab drags reorder and file drags never do (lgse/strata#1484).
- One close guard checks every tab, so a background operation in a hidden tab still blocks closing the window (lgse/strata#1484).
- Closing a tab disposes its content and releases its observers (lgse/strata#108, lgse/strata#1484).
- A closed tab is remembered as only its location and position, so its view is not kept alive. Reopening reuses the new-tab and reorder paths (lgse/strata#1800).
- Windows are titled `<folder> — Strata` so taskbars, switchers, and shortcut scripts can tell them apart, like Nautilus (lgse/strata#1824, [comment](https://github.com/lgse/strata/issues/1824#issuecomment-6361147216)). The title uses the tab strip's name (lgse/strata#1827).
- Ctrl+click was rejected for opening in a new tab because it toggles multi-selection. Ctrl+N was rejected for a new window because 10xer uses it for the sidebar (lgse/strata#1540).
- A folder opened in a new tab or window reuses the startup argument's connecting and unavailable overlays and `present_target`, rather than new windowing (lgse/strata#1540, lgse/strata#1543).
- The helpers are the window actions `win.open-tab-at` and `win.open-window-at`, which take a URI (lgse/strata#1543).
- Choosers have no tabs and Ctrl+Enter there accepts the folder, so chooser key dispatch skips the open-in-new handling (lgse/strata#1543).
- The name hold tracks navigation settlement explicitly rather than using a timer. Cancelled, refused, and same-directory navigation release it, and an older validation completion cannot release a newer click (lgse/strata#1507).
- The underline follows the selected tab from the layout pass. Its tick callback runs only while it moves, so an idle window stops drawing frames (lgse/strata#1671, lgse/strata#1677).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-23 | lgse/strata#1800 | feat | Added Ctrl+Shift+T to reopen up to 20 closed tabs per window at their former positions. |
| 2026-10-15 | lgse/strata#1677 | perf | Moved the tab underline to the layout pass and animated it only while moving, so an idle window stops drawing frames. |
| 2026-10-10 | lgse/strata#1539 | fix | Recorded the folder a pending click opens, so the Columns preview slot lends no width before its column takes focus. |
| 2026-10-10 | lgse/strata#1543 | feat | Opened folders in a new tab or window from the item menu, a middle-click, and Ctrl+Enter or Shift+Enter. |
| 2026-10-10 | lgse/strata#1544 | fix | Registered each tab window for the notice shown when settings cannot be saved. |
| 2026-10-09 | lgse/strata#1533 | fix | Fell back to the file view's cursor when a tab's saved focus can no longer take it, and registered the active tab as the dialog focus fallback. |
| 2026-10-07 | lgse/strata#1506 | feat | Added Ctrl+Page Up/Down switching and Ctrl+Shift+Page Up/Down reordering, like web browsers. |
| 2026-10-07 | lgse/strata#1507 | fix | Held the tab name during a pending folder click so it no longer flickers to the parent. |
| 2026-10-05 | lgse/strata#1484 | feat | Added in-memory tabs with a Material-style strip, shortcuts in both key maps, reordering, and cross-tab drops. |

## Known gaps

- Each tab holds one pane; split or dual-pane browsing is undecided. lgse/strata#47
