---
title: 10xer file commands
status: shipped
origin: {issue: lgse/strata#1251, pr: lgse/strata#1306}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [src/ui/window/keyboard/files.rs, src/ui/browser/file_commands.rs]
tests: [src/ui/window/tests/keyboard_dispatch/file_commands.rs, src/ui/window/tests/keyboard_dispatch/file_verbs.rs]
related: [operations/clipboard, operations/trash, operations/delete, operations/rename, operations/create, operations/archives, integration/open-with, integration/custom-actions]
---

## Summary

Single-key file commands in 10xer mode: yank, cut, paste, delete, create, rename, move, copy, restore, sort, hidden files, Open With, custom actions, and archive commands. They act on the focused pane's filled selection, or its cursor item when nothing is filled.

## Behavior

### Targets

- `y`, `x`, `d`, `c c`, and `c n` act on the focused pane's fill, or its cursor item when nothing is filled. `f` and `s` results count. lgse/strata#1306
- A hovered row, a parent folder, and a Miller column's open-path marker are never targets. lgse/strata#1306
- In an empty folder, `y`, `x`, `d`, and `r` flash `Nothing to yank`, `Nothing to cut`, `Nothing to delete`, and `Nothing to rename`. lgse/strata#1306, lgse/strata#1308

### Clipboard

- `y` and `x` copy or cut the targets; copied items show the copy icon and cut items show scissors in every view and window. lgse/strata#1306
- Ctrl+C and Ctrl+X keep their default behavior and set the same marks; the marks go away when another application takes the clipboard. lgse/strata#1306
- `Y` and `X` clear the marks and release the clipboard only while Strata still owns it. lgse/strata#1306
- `p` pastes into the same folder as Ctrl+V and focuses Keep Both on conflicts when offered (copies only); otherwise Replace is focused. lgse/strata#1306
- `P` and Ctrl+V paste with Replace focused on conflicts. `p` or `P` with an empty clipboard flashes `Nothing to paste`. lgse/strata#1306
- `c c` and `c n` copy the targets' paths or names through a `c-` chord; `Y` no longer copies a path. lgse/strata#1306

### Delete and restore

- `d` and Delete ask before moving to Trash, and a second `d` confirms that dialog. lgse/strata#1306, lgse/strata#1340
- `D`, Shift+Delete, and `d` inside Trash open the permanent-delete confirmation with Permanently delete focused, and `d` there does not confirm. lgse/strata#1340, lgse/strata#1508
- In Columns, `d` on an open folder whose empty child column has focus asks to trash that folder instead of flashing `Nothing to delete`. lgse/strata#1508
- While an `f` or `s` result list shows no hits, `d` and `D` flash `Nothing to delete` and leave the open folder alone. lgse/strata#1508 (unverified)
- After `d` or `M`, the next item receives the cursor without joining the fill. lgse/strata#1340
- `R` restores the targets from Trash through the usual confirmation; outside Trash it flashes `Only items in Trash can be restored`. lgse/strata#1340

### Create and rename

- `a` opens `create ›`; Enter creates an empty file with exactly the typed name, or a folder when the name ends in `/`. lgse/strata#1306
- An empty, invalid, or taken name, including one taken by a broken link, keeps the `create ›` prompt open with the reason; nothing is renumbered or replaced. lgse/strata#1306
- Ctrl+Shift+N still creates a numbered new folder and renames it in place. lgse/strata#1306
- `r` and F2 open `rename ›` for the cursor item or focused hit, never the fill. A file's stem or a folder's whole name is selected. lgse/strata#1308
- Enter renames the item and keeps its contents; a taken name keeps the prompt open with "“…” already exists" and overwrites nothing. lgse/strata#1308
- Esc, a clicked row, another prompt, or leaving the mode discards a `create ›` or `rename ›` entry. lgse/strata#1306, lgse/strata#1308
- Trash and Recent flash `Can’t create items here`, and Trash items flash `Can’t rename items here`. lgse/strata#1306, lgse/strata#1308 (unverified)

### Move and copy

- `M` and `C` open `move to ›` and `copy to ›` for the targets captured when the prompt opens. lgse/strata#1340
- Enter moves or copies into the chosen folder and stays in the current folder; conflicts ask as `p` does. lgse/strata#1340
- An invalid destination keeps the prompt open with its reason: `No such folder`, `Not a folder`, `Only local folders can be chosen`, `Only ~ and ~/ are supported`, or `Can’t put a folder inside itself`. lgse/strata#1340
- `M` into the folder that already holds every target keeps the prompt open with `Already in this folder`. lgse/strata#1340 (unverified)
- The `M` and `C` lists never show the folders being sent, and `M` skips the folder the items are already in. lgse/strata#1403

### Listing commands

- `, a`, `, m`, `, s`, and `, e` sort the focused pane by name, modified time, size, or type; Shift sorts descending. lgse/strata#1308
- A keyboard sort is saved as the default, keeps the cursor on the same item, and leaves other Miller columns in their order. lgse/strata#1308
- After a keyboard sort, a List heading click reverses the sort that is applied. lgse/strata#1308
- `, n` and `, t` cancel with `Unknown chord`. lgse/strata#1308
- `.`, Ctrl+H, and Ctrl+. toggle the saved hidden-files preference in every window, including over `f` results. lgse/strata#1308

### Open With and actions

- `O` looks up types and applications without blocking keys, then opens Open With for the targets. lgse/strata#1308
- For a mixed selection, Recommended Applications lists only applications that handle every type. lgse/strata#1308
- A newer key, a selection or focus change, navigation, leaving the mode, or closing the window drops an unfinished Open With lookup. lgse/strata#1308
- `;` arms a chord whose panel lists the first ten matching custom actions in context-menu order, then `t`, `c`, `e`, and `E`. lgse/strata#1308, lgse/strata#1340
- `; 1` to `; 9` and `; 0` run that action; a vacant slot flashes `No action N` and runs nothing. lgse/strata#1308
- If the targets or the action list changed since `;`, the digit flashes `Selection changed` or `Actions changed` and runs nothing. lgse/strata#1308
- A confirming action asks first, and a run appears in Jobs as from the context menu. lgse/strata#1308
- `; t` opens a terminal in the keyboard-focused folder. lgse/strata#1340
- `; t` in Trash or a non-local folder flashes `Can’t open a terminal here` and opens no dialog. lgse/strata#1340 (unverified)
- `; c` opens the Compress dialog for the targets. lgse/strata#1340
- `; e` extracts one archive beside itself and selects the result; `; E` extracts it to a folder typed in `extract to ›`. lgse/strata#1340
- `; e` and `; E` flash `Not an archive` for a non-archive or a folder named like one, and `Extract one archive at a time` for several targets. lgse/strata#1340, lgse/strata#1478 (unverified)
- The context menu shows `r` for Rename and Shift+M, Shift+C, and Shift+R beside Move to…, Copy to…, and Restore. lgse/strata#1308, lgse/strata#1340

## Design

- Commands take the fill or the cursor item, never the hovered row, because the mode keeps cursor and fill separate (lgse/strata#1291, lgse/strata#1306).
- `a` creates exactly the typed name. It never renumbers, replaces, or follows a link; Ctrl+Shift+N keeps the numbered default (lgse/strata#1306).
- A footer rename and an `M` / `C` prompt fix their items when they open, so a later cursor move cannot redirect them (lgse/strata#1308, lgse/strata#1340).
- A move made in place hands the cursor to the next item, as a delete does, through `Browser::transfer_replacing_cursor`. Drag-and-drop and paste keep their selection (lgse/strata#1340).
- `; 1` to `; 0` recheck the targets and the catalog at the digit, so a changed selection cannot run an action on other items (lgse/strata#1308).
- The permanent-delete dialog first opened with Cancel focused. That mode-only path was removed so it focuses its confirm button like every other modal (lgse/strata#1306, lgse/strata#1508).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-07 | lgse/strata#1508 | fix | Focused the confirm button in permanent-delete dialogs and let `d` trash an open Columns folder. |
| 2026-10-01 | lgse/strata#1340 | feat | Added pin, move, copy, extract, restore, and `d d` keys, and made Ctrl+Shift+M the only exit. |
| 2026-09-29 | lgse/strata#1308 | feat | Added footer rename, sort chords, hidden-file toggles, Open With, and numbered custom actions. |
| 2026-09-28 | lgse/strata#1306 | feat | Added yank, cut, paste, delete, copy path, and exact-name create. |

## Known gaps

- In Columns, deleting a directory whose child column is open closes the preview without previewing the next entry. lgse/strata#1497
