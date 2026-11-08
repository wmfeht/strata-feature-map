---
title: Make the focused column first
status: shipped
origin: {issue: lgse/strata#1922, pr: lgse/strata#1925}
branch: null
reviewed_at: 9fb7a36ad4352337f3ada0d43710dc6d4ae838b9
review: draft
code: []
tests: [src/ui/window/tests/keyboard_dispatch/first_column.rs]
docs: [docs/keyboard-navigation.md]
related: [browser/view-modes/columns, browser/selection/keyboard-navigation, browser/context-menu, app/shortcut-reference, app/keyboard-shortcuts/remapping]
---

## Summary

Alt+Down in Columns makes the focused column the first one, re-anchoring a deep strip without Ctrl+L, breadcrumbs, or pins. It is a history step that Back undoes. Its code lives in the parent's `src/app/browser/columns.rs` and `src/app/navigation/history.rs`.

## Behavior

- In Columns, with the file list focused on a column right of the first, Alt+Down closes the columns to its left. The columns to its right stay open. lgse/strata#2086, lgse/strata#1925
- The focused column becomes the first column and keeps focus, with the cursor on the same item. lgse/strata#2086, lgse/strata#1925
- With several items selected in that column and the cursor off the first of them, Alt+Down keeps them all selected. The cursor stays on its item. lgse/strata#2086, lgse/strata#1925
- Alt+Left after Alt+Down brings back the whole earlier strip. lgse/strata#2086, lgse/strata#1925
- Alt+Down with the first column focused changes nothing. lgse/strata#2086, lgse/strata#1925
- In 10xer mode, Alt+Down changes nothing; 10xer keeps its parent, current, and preview strip. lgse/strata#2086, lgse/strata#1925
- In the file chooser, Alt+Down changes nothing. lgse/strata#2086, lgse/strata#1925
- With a text field focused, such as the filter field or the location entry, Alt+Down re-roots nothing. lgse/strata#2086, lgse/strata#1925 (unverified)
- With `make_first_column` bound to another key under `[keymap.default]`, that key makes the focused column first. lgse/strata#2086, lgse/strata#1925

## Design

lgse/strata#1922 asked for a way to re-root a deep Columns strip as "a regular location change". [docs/keyboard-navigation.md](https://github.com/lgse/strata/blob/9fb7a36ad4352337f3ada0d43710dc6d4ae838b9/docs/keyboard-navigation.md) describes the key with Back, Forward, and Parent.

- It records the navigation as Parent does, so Back restores the whole strip. The new strip loads through the same path as Back, Forward, and Parent (lgse/strata#1925).
- It always acts on the focused column. lgse/strata#1922 proposed the selected folder when the cursor is on one. With Mirror columns selection on, that would promote the next column (lgse/strata#1925).
- Shift+Enter and Ctrl+Enter already open in a new window or tab, so the key is Alt+Down, the counterpart of Alt+Up (lgse/strata#1925).
- It sits in the default map only, so 10xer keeps its fixed strip (lgse/strata#1925).
- With a multi-selection, the cursor's item is listed first among the targets. The first target takes the cursor ([comment](https://github.com/lgse/strata/pull/1925#issuecomment-6677107619)).
- The key is consumed only when the strip is re-rooted, so a no-op Alt+Down falls through to other handlers ([comment](https://github.com/lgse/strata/pull/1925#issuecomment-6677107619)).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-11-07 | lgse/strata#2086 | feat | Added Alt+Down to make the focused Columns column the first, as a history step, so a deep strip re-anchors without Ctrl+L. |

## Known gaps

None known.
