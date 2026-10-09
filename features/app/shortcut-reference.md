---
title: Keyboard shortcut reference and footer
status: shipped
origin: {issue: lgse/strata#291, pr: lgse/strata#358}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [src/ui/shortcut_reference.rs, src/ui/shortcut_footer.rs]
tests: [src/ui/shortcut_footer/tests.rs]
docs: [docs/keyboard-navigation.md]
related: [settings/preferences, integration/10xer-mode, integration/10xer-mode/file-chooser, browser/context-menu, operations/clipboard]
---

## Summary

The F1 "Keyboard shortcuts" reference, Strata's only in-app keybinding list, and the window footer that hosts it. The reference shows the active key map for the current view, with search and categories. The footer carries the F1 Shortcuts button, the item and selection count, and the Files on clipboard badge. 10xer prompts, chords, and tags in the same footer belong to `integration/10xer-mode`.

## Behavior

### Opening and closing

- F1 opens the "Keyboard shortcuts" panel centered over a dimmed, blurred window; F1 again closes it. lgse/strata#358, lgse/strata#1296
- F1 with Ctrl, Alt, Super, or Shift held does not toggle the reference. lgse/strata#358 (unverified)
- In 10xer mode, `~` also toggles the reference; in the default map `~` does not open it. lgse/strata#1272
- While a 10xer footer prompt has focus, `~` goes to the prompt and does not open the reference; F1 still opens it. lgse/strata#1272 (unverified)
- The footer's "F1  Shortcuts" button toggles the reference and shows as pressed while it is open. lgse/strata#1034, lgse/strata#1376
- Escape or a click on the backdrop closes the reference. lgse/strata#1376
- Focusing another application window leaves the reference open with its search text, category, and scroll position. lgse/strata#1376
- Closing the reference returns focus to the widget that had it before opening, such as a text field or the file list. lgse/strata#358
- While the reference is open, Delete, Ctrl+V, and other browsing shortcuts do nothing to files, and focus cannot leave the panel. lgse/strata#358, lgse/strata#1296
- In the reference's search field, typing, Delete, and Ctrl+A, Ctrl+C, Ctrl+V, and Ctrl+X edit the query. lgse/strata#1296 (unverified)

### Finding a shortcut

- Opening the reference focuses "Search actions or keys…" and scrolls the list to the top. lgse/strata#1296
- Reopening the reference keeps the previous search text and selected category. lgse/strata#1296 (unverified)
- Typing keeps rows whose keys, key context, or action contain the text, ignoring case and matching translated text; no match shows "No matching shortcuts". lgse/strata#1296, lgse/strata#1519
- The category list shows All and each section with its row count; choosing one shows only that section. lgse/strata#1296
- Tab cycles search, the selected category, and the results; Shift+Tab cycles backwards. lgse/strata#1296
- Ctrl+B focuses the categories, Ctrl+F the search field, and Ctrl+L the results. lgse/strata#1296
- In the categories, arrows and h/j/k/l select the previous or next category, and Home and End the first or last. lgse/strata#1296
- In the results, arrows, j/k, Page Up, Page Down, Home, and End scroll the list. lgse/strata#1296
- With the search field focused, Up, Down, Page Up, and Page Down scroll the results without moving focus. lgse/strata#1296 (unverified)
- In windows narrower than 1480 px, the header stacks, categories become wrapping pills without counts, and results use one column; resizing while open re-lays the panel. lgse/strata#1296
- A note at the bottom reads "Ctrl+B categories · Ctrl+F search · Ctrl+L list · arrows/hjkl move · Tab cycle · Esc close" and wraps only after a "·". lgse/strata#1296, lgse/strata#1519

### Contents

- In the default map, the sections are Columns, Icons, or List navigation for the current view, then Files and selection, Search and tools, and Preview media. lgse/strata#358, lgse/strata#1272
- Switching views with Ctrl+1, 2, or 3 replaces the navigation section with the new view's. While the reference is open, Ctrl+1, 2, and 3 do nothing. lgse/strata#358 (unverified)
- In 10xer mode, the reference lists only the 10xer map, adding Places, Preview, and a "10xer mode" section that collects the keys the default map lacks. lgse/strata#1272
- Turning 10xer mode on or off in any window updates an open reference to the newly active map. lgse/strata#1272
- The default reference lists text size (Ctrl++ / Ctrl+− / Ctrl+0), Ctrl+Space, and Ctrl+\; the 10xer reference lists text size. lgse/strata#1376
- Movement keys are described directly; the `h / j / k / l` row reads "Same as ← ↓ ↑ → (type-to-search off)" and no row names Vim. lgse/strata#826
- In a translated interface, actions and key context such as "on a file" are translated while key names stay as typed. lgse/strata#1519

### Menu hints

- In the default map, the Y (copy path) and P (pin) context-menu hints show only while Type to search is off. lgse/strata#1376
- In 10xer mode, menu hints show 10xer keys, such as `r` for Rename and Shift+D for permanent delete. Duplicate, Copy path, Pin, and terminal show none. lgse/strata#1272, lgse/strata#1340 (unverified)

### Footer status

- In Columns, Icons, and List, the footer shows "F1  Shortcuts" at the left and the clipboard badge and item count at the right. lgse/strata#1034
- With nothing selected, the count reads "N items", and its accessible description gives the file and folder breakdown. lgse/strata#1034
- With a selection, the count shows a folder and file breakdown with the selected files' total size, such as "1 folder, 2 files selected (64 MB)"; folder contents are not counted. lgse/strata#1034
- When some selected file sizes are unknown the size reads "(3 B known; size incomplete)", and when none are known "(size unavailable)". lgse/strata#1034
- Selecting every item shows the folder and file breakdown without a size, such as "1 folder, 2 files selected". lgse/strata#1266 (unverified)
- Selecting more than 64 items, but not all, shows "N items selected" without a size. lgse/strata#1266 (unverified)
- An empty folder shows "0 items", and clearing the selection restores the directory total. lgse/strata#1034
- Copying or cutting files shows a "Files on clipboard" badge left of the count, whose description reads "Press Ctrl+V to paste into a supported directory." lgse/strata#358, lgse/strata#499
- The badge also appears for files copied in other applications, and disappears when the clipboard is cleared, holds text, or holds an empty file list. lgse/strata#358
- The badge stays after pasting a copy and disappears after pasting a cut. lgse/strata#358
- The badge has the 10X tag's pill shape and height, so showing it does not change the footer's height. lgse/strata#1408
- The badge stays visible when keybinding hints are hidden. lgse/strata#1018
- With the F1 button hidden and no other footer status visible, such as the count or clipboard badge, the whole footer hides. lgse/strata#1018

## Design

[docs/keyboard-navigation.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/keyboard-navigation.md) describes the footer and reference under "Shortcut footer" and "10xer mode".

- A keyboard-first user could not discover shortcuts; lgse/strata#291 asked for an accurate shortcut reference. lgse/strata#358 added a compact, mode-aware hint footer whose F1 reference describes the shortcuts each view actually runs.
- lgse/strata#1033 proposed per-column counts and rejected a global status bar, because Columns shows several directories at once. lgse/strata#1034 put counts in the shared footer for all views instead, and replaced the inline hints with one F1 Shortcuts button.
- The catalog is static data in `shortcut_reference.rs`, built per scope: view mode, key map, and portal chooser request. The chooser scope is described in `integration/10xer-mode/file-chooser`.
- The reference shows only the active map, and planned keys are never advertised, so help describes only commands that run (lgse/strata#1272).
- Settings once had its own Keybindings page, and the two catalogs drifted. Generating both from one catalog was rejected; F1 already had mode- and view-aware sections (lgse/strata#1374).
- The reference is drawn in the window's overlay, not a `GtkPopover`. Hyprland sends `xdg_popup.done` when the window deactivates, and no popover setting kept it open (lgse/strata#1375).
- Selection sizes use only selected files' known metadata; folders are not scanned (lgse/strata#1034). Above 64 selected items no per-entry details are read (lgse/strata#1266) (unverified).
- The clipboard badge reads the file list asynchronously, and a newer clipboard change discards an older pending read (unverified).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-03 | lgse/strata#1408 | fix | Gave the Files on clipboard badge the 10X pill style so it no longer shifts the footer height. |
| 2026-09-15 | lgse/strata#1034 | feat | Moved item and selection counts into the shared footer and replaced inline hints with an F1 Shortcuts button. |
| 2026-09-11 | lgse/strata#826 | feat | Described movement keys directly instead of as Vim movement. |

## Known gaps

- In the default map, Ctrl+F results leave the count describing the hidden directory's selection, including on a miss; the fix is unmerged. lgse/strata#1442, lgse/strata#1546
- docs/keyboard-navigation.md says the footer shows the result total in both maps; at `reviewed_at` only 10xer mode does. lgse/strata#1442
