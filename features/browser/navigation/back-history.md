---
title: Back history menu
status: shipped
origin: {issue: lgse/strata#1976, pr: lgse/strata#1977}
branch: null
reviewed_at: 0f9bb00f02d3923ba009f53e0dbaecb840ee524c
review: reviewed
code: []
tests: [tests/qa/scenarios/keyboard_navigation/back-history-dropdown.jsonl]
related: [browser/view-modes, browser/view-modes/sorting, app/shortcut-reference]
---

## Summary

A menu of a tab's earlier locations, opened from the List and Icons pane-header Back button, for jumping several steps back at once. Its code lives in the shared pane-header module, `src/ui/browser/pane_header.rs`, which `app/infrastructure` owns.

## Behavior

- In List or Icons with back history, right-clicking Back, holding it, or pressing Menu or Shift+F10 on it opens a popover below Back. lgse/strata#1977
- The popover is headed BACK TO and lists the tab's back entries, most recent first. lgse/strata#1976, lgse/strata#1977
- Each entry shows the folder name over its dimmed path. lgse/strata#1977
- An entry's accessible name is the folder name, and its description is the folder's path. lgse/strata#1977
- The home folder's entry is named `~`, and paths under home start with `~`. lgse/strata#1977 (unverified)
- Choosing an entry N steps back opens it in one step. lgse/strata#1977
- The skipped entries and the folder left become Forward history. lgse/strata#1977
- After opening A, pressing Alt+Up, and opening B, choosing A and pressing Alt+Right twice returns to A's parent, then to B. lgse/strata#1977
- A plain click on Back still goes back one step. lgse/strata#1977
- Holding Back until the menu opens and then releasing stays in the current folder; a right-click on Back does not go back either. lgse/strata#1977
- In a fresh tab, with Back disabled, none of these gestures opens a menu. lgse/strata#1977
- A list taller than 400 px scrolls, and arrowing through it keeps the focused entry in view. lgse/strata#1977
- Escape closes the popover. lgse/strata#1977
- Backspace also closes it, and the vim focus keys move between entries, as in the SORT BY menu. lgse/strata#1977 (unverified)
- Back's accessible description reads "Right-click, hold, or press Menu / Shift+F10 to list the back history", naming the current binding. lgse/strata#1977
- Back carries that description even when it is disabled and no menu opens. lgse/strata#1977 (unverified)

## Design

lgse/strata#1976 proposed a split button with a chevron, as in web browsers and Nautilus. lgse/strata#1977 shipped right-click, long press, and the context-menu key on Back instead, so the header gains no new control.

- Skipped entries stay reachable with Forward, as in browsers. `go_back_to(steps)` replaced `go_back` so the forward stack stays consistent when several entries are skipped (lgse/strata#1977).
- Only the back stack is listed; forward entries stay behind Forward (lgse/strata#1976).
- The popover reuses the pane header's popover and menu styling and the SORT BY menu's key handling (lgse/strata#1977).
- The popover is unparented when Back is destroyed, because a plain button does not do it (lgse/strata#1977).
- An earlier attempt, lgse/strata#1232, bundled Back and Forward menus with unrelated changes and was closed unmerged.

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-11-01 | lgse/strata#1977 | feat | Added a back-history menu on the List and Icons Back button to jump several steps back at once. |

## Known gaps

- Columns has no pane header, so it has no back-history menu. lgse/strata#1977
