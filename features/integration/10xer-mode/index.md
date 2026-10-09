---
title: 10xer mode
status: shipped
origin: {issue: lgse/strata#1152, pr: lgse/strata#1267}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: reviewed
code: [src/ui/tenxer_mode.rs, src/ui/window/keyboard/escape.rs, src/ui/window/keyboard/prompts.rs, src/ui/window/composition/tenxer_splash.rs]
tests: [src/ui/window/tests/keyboard_dispatch/escape_precedence.rs, src/ui/window/tests/keyboard_dispatch/mode_exit.rs, src/ui/window/composition/tenxer_splash/tests.rs]
docs: [docs/10xer-mode.md]
related: [browser/selection, browser/tabs, settings/preferences]
---

## Summary

An opt-in, saved Yazi-style keymap for keyboard-first users. It replaces the default map, hides pane chrome, and uses the footer for typed commands. Children: `integration/10xer-mode/preview-keys` (keys inside an open preview), `integration/10xer-mode/places` (`g` chords, `go ›`, `z` / `Z`, the folder picker), `integration/10xer-mode/search` (`/`, `f`, `s`), `integration/10xer-mode/file-verbs` (file commands and their chords), and `integration/10xer-mode/file-chooser` (the mode in the portal file chooser).

## Behavior

### Entering and leaving

- With no `tenxer_mode` in `settings.toml`, the default keymap and chrome are unchanged. lgse/strata#1267
- Settings → General → Browsing → 10xer mode and Ctrl+Shift+M change the same saved preference and update every open window. lgse/strata#1267
- A saved `tenxer_mode = true` applies at launch before Settings opens, including in a second window and lazily built views. lgse/strata#1267
- Ctrl+Shift+M toggles the mode from a browser text field but not over a modal dialog. lgse/strata#1271
- Ctrl+Shift+M is the only key that leaves the mode; `q` does nothing. lgse/strata#1340
- Shift+Q closes only the current window through the normal close path, so a running custom-action job still blocks closing the last window. lgse/strata#1267
- Turning the mode on in a mapped window shows a centered, non-focusable splash for about 1.5 seconds; launching with the mode saved shows none. lgse/strata#1393 (unverified)
- With reduced motion on, the splash appears without animation. lgse/strata#1393

### Chrome and Settings

- While the mode is on, window Search and pane Close, filter, refresh, and sort controls hide; window Close and clickable List headings stay. lgse/strata#1267
- While the mode is on, List and Icons hide their pane header with back, forward, and up buttons; List keeps its column headings. lgse/strata#1304
- Turning the mode on hides an open pane filter, and turning it off shows that filter again. lgse/strata#1267
- The footer shows a `10X` pill in its far right corner while the mode is on, and the footer height does not change. lgse/strata#1304, lgse/strata#1393
- While the mode is on, the 10xer mode Settings row shows "(experimental feature, under active development)" under its subtitle. lgse/strata#1272
- The `10X` pill's accessible name is "10xer mode (experimental feature, under active development)". lgse/strata#1272 (unverified)
- While the mode is on, the Type to search, Keep arrows in file list, and Include subfolders rows stay editable. They read "Not used in 10xer mode." lgse/strata#1267, lgse/strata#1403
- Mirror columns selection and Single-click previews apply to the Columns cursor while the mode is on. lgse/strata#1340

### Keymap ownership

- With the file list focused, `h`/`j`/`k`/`l`, other letters, Space, Ctrl+D, Ctrl+F, Ctrl+B, and Ctrl+R never also run their default-map action. lgse/strata#1271
- Ctrl+C/X/V, Delete, Shift+Delete, F2, F5, Ctrl+L, Ctrl+K, Ctrl+1/2/3, Ctrl+Shift+N, Alt+Enter, Menu, and text-size keys keep working. lgse/strata#1271
- In the location field or an inline rename, letters such as `q`, `d`, and `p` are typed and no file command runs. lgse/strata#1271
- Turning the mode on removes the folder jump, Open Terminal, and arrow-scope accelerators in every window; turning it off restores them. lgse/strata#1271
- Ctrl+N shows or hides the sidebar, and Ctrl+B pages up. lgse/strata#1304
- F1 or `~` toggles the shortcut reference, which lists only the commands of the active map and switches live with the mode. lgse/strata#1272
- Context-menu hints hide the default `Y` copy path, Space preview, and Ctrl+R rename hints while the mode is on. lgse/strata#1272
- After returning from another window, `g`, `f`, and `s` act on the listing without first clicking a row. lgse/strata#1393

### Movement

- In List and Columns, `j`/`k`, Up/Down, Home, End, and `G` move the cursor in displayed order, including sorted and type-grouped lists. lgse/strata#1273
- Ctrl+U/Ctrl+D move half a page, and Ctrl+B/Ctrl+F or Page Up/Page Down a full page, without filtering, toggling the sidebar, or duplicating. lgse/strata#1273
- In List and Columns, `l` or Right enters a directory and never launches a file; `h` or Left opens the parent. lgse/strata#1273
- Enter and `o` open the focused item, including files. lgse/strata#1273
- `H`/`L` and Alt+Left/Alt+Right move back and forward in history; Backspace and Alt+Up open the parent. lgse/strata#1273
- In Columns, `i` on a directory opens the next Miller column and leaves focus in the current column. lgse/strata#1273
- In Icons, `h`/`j`/`k`/`l` and the arrows move to the next tile in that direction, also over search results. They never open, leave a folder, or enter a preview. lgse/strata#1280
- In Icons and List, `i` on a directory toggles the folder peek without moving focus; on a file or empty folder it opens no peek. lgse/strata#1280 (unverified)

### Sidebar and header

- Ctrl+Shift+B focuses a visible sidebar and leaves a hidden one hidden. lgse/strata#1284
- In the sidebar, `j`/`k` and Up/Down move between places, `l`/Enter/Space activate, and `h`/Left/Backspace return to the files with the selection kept. lgse/strata#1284
- After a sidebar place opens another folder, focus is on that folder's listing. lgse/strata#1284
- Tab from the file list focuses the window header; Enter and Space activate the header control, and `h` or `j` return to the files. lgse/strata#1284

### Selection

- Space toggles the focused item in the selection and moves the cursor down, without previewing and without using the hovered row. lgse/strata#1291, wmfeht/strata#41
- Ctrl+A selects every item in the focused pane, and Ctrl+R inverts that pane's selection instead of renaming. lgse/strata#1291
- After Space, Ctrl+A, or Ctrl+R, Home, End, and paging move the cursor and keep the selection. lgse/strata#1291
- `v` starts a range from the cursor and `V` starts an unselect range; the footer shows `VISUAL` or `UNSET` while it is active. lgse/strata#1291, wmfeht/strata#42 (unverified)
- `v` and `V` are the only range keys: Shift+arrows do nothing in the listing, and paging extends an active range. lgse/strata#1340
- In Columns, mirroring waits while a `v` or `V` range is active, so walking the range opens or closes no column. lgse/strata#1340
- In an empty folder, Space, `v`, `V`, Ctrl+A, and Ctrl+R flash `Nothing to select`. lgse/strata#1291

### Escape

- Dialogs, the reference, text fields, footer prompts, armed chords, and preview key ownership take Esc before any listing step. lgse/strata#1307
- An open folder peek closes before any filter, search, highlight, range, or preview step. lgse/strata#1307
- In an ordinary listing, Esc steps through a range over `f` results, the filter, find highlights, the range, the preview, then the selection. lgse/strata#1307
- Over `s` results, Esc steps through the range, find highlights, the preview, then the results, which restores an earlier `f` filter. lgse/strata#1307
- Esc from the sidebar or a header control takes the same steps. Clearing a filter or closing the preview from there refocuses the file list. lgse/strata#1307
- With nothing left to dismiss, Esc does nothing: it closes no Miller column and never the window. lgse/strata#1307

### Leaving the mode

- Leaving the mode closes footer prompts, armed chords, a keyboard folder peek, and preview key ownership, and ends ranges over results and the listing. lgse/strata#1311
- After leaving the mode, every pane returns to the saved Include subfolders scope, so a default Ctrl+F does not search subfolders. lgse/strata#1311
- A closed window releases its preference bindings and key controllers instead of staying in memory. lgse/strata#1311

## Design

[docs/10xer-mode.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/10xer-mode.md) is the target product specification and keymap contract; each PR updates it as keys ship.

- Keyboard browsing shared the default map with type-to-search and dense pane controls. Yazi- and Ranger-style users needed an explicit opt-in map instead (lgse/strata#1152).
- The scope is not full Yazi compatibility: no content search (`S`), zoxide integration, keybinding editor, or live cross-process preference sync (lgse/strata#1152).
- The feature was split into 31 OMA stories, lgse/strata#1233 to lgse/strata#1263, later tracked as wmfeht/strata#35 to wmfeht/strata#65. Each story ships its own help text and cleanup (lgse/strata#1152).
- Mode keys are consumed before the default command chain, so one key never runs both maps. Text fields, modals, native menus, and the reference keep their input (lgse/strata#1271).
- Conflicting application accelerators follow the saved mode, not a window, so closing one window cannot restore them (lgse/strata#1271).
- Help, Settings, and menu hints describe only commands that currently run; unfinished keys are not advertised (lgse/strata#1152, lgse/strata#1272).
- The keyboard cursor and the filled selection are distinct, and the pointer never chooses the pane or row those keys act on (lgse/strata#1291).
- One precedence chain handles every listing Escape, so each press ends exactly one state (lgse/strata#1307).
- `gtk_window_destroy()` only unrealizes a window, and its own closures kept it alive. Cleanup now runs on unrealize (lgse/strata#1311).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-29 | lgse/strata#1307 | feat | Made each Escape end exactly one interaction through one precedence chain. |
| 2026-09-27 | lgse/strata#1291 | feat | Separated the keyboard cursor from the filled selection with Space, Ctrl+A, Ctrl+R, and `v`/`V` ranges. |
| 2026-09-26 | lgse/strata#1284 | feat | Added keyboard round trips to the sidebar and window header. |
| 2026-09-26 | lgse/strata#1280 | feat | Added tile movement and folder peek to Icons. |
| 2026-09-26 | lgse/strata#1273 | feat | Added home-row movement, directory entry, and history in List and Columns. |
| 2026-09-26 | lgse/strata#1272 | feat | Limited the reference, Settings, and menu hints to the active map and added the experimental label. |
| 2026-09-26 | lgse/strata#1271 | feat | Stopped the default map from also handling mode keys and made accelerators follow the saved mode. |
| 2026-09-26 | lgse/strata#1267 | feat | Added the saved preference, Ctrl+Shift+M, reduced chrome, and the `10X` footer tag. |

## Known gaps

- In Columns, `g g` or `G` from a column with no cursor can land on the wrong end; the fix merged after `reviewed_at`. lgse/strata#1447, lgse/strata#1533
