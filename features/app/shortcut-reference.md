---
title: Keyboard shortcut reference and footer
status: shipped
origin: {issue: lgse/strata#291, pr: lgse/strata#358}
branch: null
reviewed_at: 73b3258ff9da7fd5f8b279e442e4fbf576850deb
review: draft
code: [src/ui/shortcut_reference.rs, src/ui/shortcut_footer.rs]
tests: [src/ui/shortcut_footer/tests.rs, tests/qa/scenarios/dialogs_and_menus/shortcut-reference-search-keeps-editing-chords.jsonl]
docs: [site/src/reference/keyboard-navigation.md]
related: [settings/preferences, integration/10xer-mode, integration/10xer-mode/file-chooser, browser/context-menu, operations/clipboard, app/keyboard-shortcuts]
---

## Summary

The F1 "Keyboard shortcuts" reference, Strata's only in-app keybinding list, and the window footer that hosts it. The reference shows the active key map for the current view, with search and categories. The footer carries the F1 Shortcuts button, the item and selection count, and the Files on clipboard badge. 10xer prompts, chords, and tags in the same footer belong to `integration/10xer-mode`.

## Behavior

### Opening and closing

- F1 opens the "Keyboard shortcuts" panel centered over a dimmed, blurred window; F1 again closes it. lgse/strata#358, lgse/strata#1296
- F1 with Ctrl, Alt, Super, or Shift held does not toggle the reference. lgse/strata#358 (unverified)
- In 10xer mode, `~` also toggles the reference; in the default map `~` does not open it. lgse/strata#1272
- In 10xer mode, `~` in a focused footer prompt or text field, such as the location bar, types into it and opens no reference. lgse/strata#1272, lgse/strata#1714
- F1 still opens the reference from a footer prompt or text field. lgse/strata#1272 (unverified)
- In 10xer mode, `~` typed in the open reference's search closes the reference. lgse/strata#1714
- In 10xer mode with Russian active and a text field focused, Shift and the ё key type Ё instead of toggling the reference. lgse/strata#1576
- In 10xer mode, Russian ё reads as `~` only through the layout fallback. In the open reference's search it types itself instead of closing it. lgse/strata#1576, lgse/strata#1714
- The footer's "F1 Shortcuts" button toggles the reference and shows as pressed while it is open. lgse/strata#1034, lgse/strata#1376, lgse/strata#1688
- Escape or a click on the backdrop closes the reference. lgse/strata#1376
- Focusing another application window leaves the reference open with its search text, category, and scroll position. lgse/strata#1376
- Closing the reference returns focus to the widget that had it before opening, such as a text field or the file list. lgse/strata#358
- While the reference is open, Delete, Ctrl+V, and other browsing shortcuts do nothing to files, and focus cannot leave the panel. lgse/strata#358, lgse/strata#1296
- In the reference's search field, typing, Delete, and Ctrl+A, Ctrl+C, Ctrl+V, and Ctrl+X edit the query. lgse/strata#1296 (unverified)
- In the reference's search field, Ctrl+Z undoes and Ctrl+Y or Ctrl+Shift+Z redoes the last query edit. lgse/strata#1576
- In the reference's search field holding `open tab`, Ctrl+Left then typing `new ` gives `open new tab`; Ctrl+Backspace deletes a word. lgse/strata#1714
- With fcitx5 loaded through `GTK_IM_MODULE=fcitx`, Ctrl+Space in the reference's search switches the input method, and Chinese can be typed there. lgse/strata#1714
- In the reference's search, a Ctrl, Alt, or Super chord the field does not use reaches nothing else: Ctrl+, opens no Settings, and typing stays in the search. lgse/strata#1714

### Finding a shortcut

- Opening the reference focuses "Search actions or keys…" and scrolls the list to the top. lgse/strata#1296
- The reference's search field is named "Search actions or keys…". lgse/strata#1896
- Reopening the reference keeps the previous search text and selected category. lgse/strata#1296 (unverified)
- Typing keeps rows whose keys, key context, or action contain the text, ignoring case and matching translated text; no match shows "No matching shortcuts". lgse/strata#1296, lgse/strata#1519
- With no match, "No matching shortcuts" wraps and sits centered in the results area. lgse/strata#1648
- Key names match in English and in the interface language: under German, `strg+c` and `ctrl+c` both find Copy. lgse/strata#1576
- Searching `ctrl+0` finds the "Ctrl++ / − / 0" text-size row, and `1-9` finds "Ctrl+Shift+1–9 / 0". lgse/strata#1576
- The category list shows All and each section with its row count; choosing one shows only that section. lgse/strata#1296
- Tab cycles search, the selected category, and the results; Shift+Tab cycles backwards. lgse/strata#1296
- Ctrl+B focuses the categories, Ctrl+F the search field, and Ctrl+L the results. lgse/strata#1296
- In the categories, arrows and h/j/k/l select the previous or next category, and Home and End the first or last. lgse/strata#1296
- In the results, arrows, j/k, Page Up, Page Down, Home, and End scroll the list. lgse/strata#1296
- With the search field focused, Up, Down, Page Up, and Page Down scroll the results without moving focus. lgse/strata#1296 (unverified)
- In windows narrower than 1480 px, the header stacks, categories become wrapping pills without counts, and results use one column; resizing while open re-lays the panel. lgse/strata#1296
- A note at the bottom reads "Ctrl+B categories · Ctrl+F search · Ctrl+L list · j / k / ↑ / ↓ move · Tab cycle · Escape close". lgse/strata#1296, lgse/strata#1576 (unverified)
- The note wraps only after a "·". lgse/strata#1296, lgse/strata#1519
- After the reference's category, search, or list key is rebound, the note names the new key. lgse/strata#1885 (unverified)

### Contents

- In the default map, the sections are Columns, Icons, or List navigation for the current view, then Files and selection, Search and tools, and Preview media. lgse/strata#358, lgse/strata#1272
- Search and tools lists Ctrl+Shift+T, "Reopen the last closed tab", in the default map. lgse/strata#1800
- In 10xer mode the reference lists it outside the file chooser only. lgse/strata#1800 (unverified)
- Switching views with Ctrl+1, 2, or 3 replaces the navigation section with the new view's. While the reference is open, Ctrl+1, 2, and 3 do nothing. lgse/strata#358 (unverified)
- In 10xer mode, the reference lists only the 10xer map, adding Places, Preview, and a "10xer mode" section that collects the keys the default map lacks. lgse/strata#1272
- Turning 10xer mode on or off in any window updates an open reference to the newly active map. lgse/strata#1272
- Outside the file chooser, in both maps, "Files and selection" lists "Ctrl+Enter / Shift+Enter — Open the focused folder in a new tab / window". lgse/strata#1543
- In 10xer mode in Columns or List, outside the file chooser, the reference lists "`/` in the preview — Find in preview"; Icons omits it. lgse/strata#1559
- In 10xer mode in Columns or List, the reference lists "Shift+← / Shift+→ / Page Down / Page Up" in media as "Seek −30 / +30 seconds". lgse/strata#1570, lgse/strata#1451, lgse/strata#1576 (unverified)
- In 10xer mode in Columns or List, the reference lists "0 / Home / G / End" in media as "Seek to the start / end". lgse/strata#1570, lgse/strata#1451
- In 10xer mode in Columns or List, the reference lists "↑ / ↓ / + / −" in media as "Volume up / down". lgse/strata#1570, lgse/strata#1451, lgse/strata#1576 (unverified)
- The default reference lists text size as "Ctrl++ / − / 0", Ctrl+Space, and Ctrl+\; the 10xer reference lists text size. lgse/strata#1376, lgse/strata#1576
- In the default map in Icons, the reference lists Ctrl+Alt++ / − / 0 as "Increase / decrease / reset thumbnail size". lgse/strata#1721
- In 10xer mode in Icons, "Increase / decrease thumbnail size" lists +, −, Ctrl+Alt++, and Ctrl+Alt+−, and "Reset thumbnail size" lists Ctrl+Alt+0. lgse/strata#1721 (unverified)
- A row lists every key the active map gives its command, keys a user added included; a command with no key has no row. lgse/strata#1885
- With F1 open, unbinding Ctrl+K for global search removes its row without reopening the reference. lgse/strata#1885
- With `[keymap.default] toggle_hidden_files = ["F7"]`, F1 lists F7 for toggling hidden files. lgse/strata#1885
- In the default map, a "Custom actions" section lists each custom action slot that has a key, as "Custom action N". lgse/strata#1885
- With Close tab unbound, its tooltip and accessible label read "Close tab", not "Close tab ()". lgse/strata#1885
- With its keys unbound, a legend hint such as "%{keys} navigate" is hidden. lgse/strata#1885 (unverified)
- Movement keys are described directly; the `h / j / k / l` row reads "Same as ← ↓ ↑ → (type-to-search off)" and no row names Vim. lgse/strata#826
- In a translated interface, actions and key context such as "on a file" are translated, and key names follow the interface language: German shows Strg+B and Rücktaste. lgse/strata#1519, lgse/strata#1576

### Menu hints

- In the default map, the `y` (copy path) and `p` (pin) context-menu hints show only while Type to search is off. lgse/strata#1376, lgse/strata#1576
- In 10xer mode, menu hints show 10xer keys, such as `r` for Rename. Duplicate, Copy path, Pin, and terminal show none. lgse/strata#1272, lgse/strata#1340 (unverified)

### Footer status

- In Columns, Icons, and List, the footer shows "F1 Shortcuts" at the left and the clipboard badge and item count at the right. lgse/strata#1034, lgse/strata#1688
- The hovered F1 Shortcuts button's highlight is inset equally from the footer's left, top, and bottom edges. lgse/strata#1680
- With nothing selected, the count reads "N items", and its accessible description gives the file and folder breakdown. lgse/strata#1034
- With 2 of 5 items selected, the count's accessible description reads "2 of 5 items selected. Size includes selected files only; folder contents are not counted." lgse/strata#1034, lgse/strata#1519 (unverified)
- With a selection, the count shows a folder and file breakdown with the selected files' total size, such as "1 folder, 2 files selected (64 MB)"; folder contents are not counted. lgse/strata#1034
- When some selected file sizes are unknown the size reads "(3 B known; size incomplete)", and when none are known "(size unavailable)". lgse/strata#1034
- With a file symlink selected, the selection size counts its target's size, as the size column shows it. lgse/strata#1034, lgse/strata#1880 (unverified)
- Selecting every item shows the folder and file breakdown without a size, such as "1 folder, 2 files selected". lgse/strata#1266 (unverified)
- Selecting more than 64 items, but not all, shows "N items selected" without a size. lgse/strata#1266 (unverified)
- An empty folder shows "0 items", and clearing the selection restores the directory total. lgse/strata#1034
- In the default map, a Ctrl+F query shows the displayed result total, such as "1 item", and "0 items" on a miss. lgse/strata#1554, lgse/strata#1442
- Selecting results keeps the result total; its accessible description gives the results' file and folder breakdown. lgse/strata#1554, lgse/strata#1442
- Escape clearing the filter restores the directory count or selection summary. lgse/strata#1554 (unverified)
- A 10xer footer prompt's entry is named after the prompt label it shows, and the name changes with each prompt. lgse/strata#1896 (unverified)
- While a typed query's search has not reported back, the count keeps describing the directory instead of reading "0 items". lgse/strata#1554
- In the default map, the footer shows no `filter:` or `search:` mark and no hit path; those appear only in 10xer mode. lgse/strata#1554, lgse/strata#1442
- Copying or cutting files shows a "Files on clipboard" badge left of the count, whose description reads "Press Ctrl+V to paste into a supported directory." lgse/strata#358, lgse/strata#499
- The badge also appears for files copied in other applications, and disappears when the clipboard is cleared, holds text, or holds an empty file list. lgse/strata#358
- The badge stays after pasting a copy and disappears after pasting a cut. lgse/strata#358
- The badge has the 10X tag's pill shape and height, so showing it does not change the footer's height. lgse/strata#1408
- The badge stays visible when keybinding hints are hidden. lgse/strata#1018
- With the F1 button hidden and no other footer status visible, such as the count or clipboard badge, the whole footer hides. lgse/strata#1018

## Design

[docs/keyboard-navigation.md](https://github.com/lgse/strata/blob/442d325be108ff95391f0fe76cbd89da8db9e129/docs/keyboard-navigation.md) describes the footer and reference under "Shortcut footer" and "10xer mode".

- A keyboard-first user could not discover shortcuts; lgse/strata#291 asked for an accurate shortcut reference. lgse/strata#358 added a compact, mode-aware hint footer whose F1 reference describes the shortcuts each view actually runs.
- lgse/strata#1033 proposed per-column counts and rejected a global status bar, because Columns shows several directories at once. lgse/strata#1034 put counts in the shared footer for all views instead, and replaced the inline hints with one F1 Shortcuts button.
- The catalog is static data in `shortcut_reference.rs`, built per scope: view mode, key map, and portal chooser request. The chooser scope is described in `integration/10xer-mode/file-chooser`.
- Rows hold binding constants from `ui::keys::bindings`, the ones handlers match, and render through one label formatter; no row carries a typed key label (lgse/strata#1576, `app/keyboard-shortcuts`).
- The search field once let through only an allow-list of text-editing chords, which also blocked input-method switch keys and word movement. It now takes every key the reference does not use; a bubble-phase guard on the field stops unused Ctrl, Alt, and Super chords there (lgse/strata#1714).
- In 10xer mode, `~` opens the reference only when no prompt or typing widget has focus. Text fields such as the location bar can then type it (lgse/strata#1714).
- The reference shows only the active map, and planned keys are never advertised, so help describes only commands that run (lgse/strata#1272).
- Settings once had its own Keybindings page, and the two catalogs drifted. Generating both from one catalog was rejected; F1 already had mode- and view-aware sections (lgse/strata#1374).
- The reference is drawn in the window's overlay, not a `GtkPopover`. Hyprland sends `xdg_popup.done` when the window deactivates, and no popover setting kept it open (lgse/strata#1375).
- Selection sizes use only selected files' known metadata; folders are not scanned (lgse/strata#1034). Above 64 selected items no per-entry details are read (lgse/strata#1266) (unverified).
- The default map shows the result total alone. 10xer adds the `filter:` or `search:` mark because it hides the pane's filter field (lgse/strata#1442, lgse/strata#1554).
- The clipboard badge reads the file list asynchronously, and a newer clipboard change discards an older pending read (unverified).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-17 | lgse/strata#1714 | fix | Let the F1 search take input-method and word-editing chords, and let 10xer text fields type `~`, so Chinese input works there. |
| 2026-10-15 | lgse/strata#1688 | feat | Removed the double space from the footer's F1 Shortcuts label in all 11 catalogs, which left a wide gap in the monospace font. |
| 2026-10-14 | lgse/strata#1648 | fix | Wrapped and centered "No matching shortcuts" in the reference results area. |
| 2026-10-11 | lgse/strata#1570 | fix | Listed the 10xer media seek-30 s, start/end, and volume keys in the F1 reference. |
| 2026-10-10 | lgse/strata#1559 | fix | Listed `/` as Find in preview in the 10xer F1 reference for Columns and List. |
| 2026-10-10 | lgse/strata#1554 | fix | Showed the filter or search result total in the default-map footer instead of the hidden folder's selection. |
| 2026-10-03 | lgse/strata#1408 | fix | Gave the Files on clipboard badge the 10X pill style so it no longer shifts the footer height. |
| 2026-09-15 | lgse/strata#1034 | feat | Moved item and selection counts into the shared footer and replaced inline hints with an F1 Shortcuts button. |
| 2026-09-11 | lgse/strata#826 | feat | Described movement keys directly instead of as Vim movement. |

## Known gaps

- The note at the bottom has no keyless form for an unbound command, such as a categories key removed in Settings → Keyboard. lgse/strata#1885
