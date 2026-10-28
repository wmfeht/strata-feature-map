---
title: Remappable shortcuts per map
status: shipped
origin: {issue: lgse/strata#1884, pr: lgse/strata#1885}
branch: null
reviewed_at: 73b3258ff9da7fd5f8b279e442e4fbf576850deb
review: draft
code: [src/ui/keys/command.rs, src/ui/keys/alias.rs, src/ui/keys/capture.rs, src/ui/keys/conflicts.rs, src/ui/preferences/keymap.rs, src/ui/window/keyboard/direct.rs, src/ui/settings/keyboard.rs]
tests: [src/ui/keys/command/tests.rs, src/ui/keys/alias/tests.rs, src/ui/keys/conflicts/tests.rs, src/ui/preferences/tests/keymap.rs, src/ui/settings/keyboard/tests.rs, src/ui/window/tests/keyboard_dispatch/keymap_overrides.rs, src/ui/window/tests/keyboard_dispatch/keymap_conflicts.rs, src/ui/window/tests/keyboard_dispatch/structural_aliases.rs, src/ui/window/tests/keyboard_dispatch/direct_commands.rs, tests/qa/scenarios/keymap]
docs: [docs/keymap.md]
related: [settings/preferences, integration/custom-actions, integration/10xer-mode, integration/10xer-mode/file-verbs, integration/portal-file-chooser, app/shortcut-reference, app/window/key-dispatch]
---

## Summary

Lets users change, add, or remove the keys of any listed command, separately for the default map and 10xer mode. Changes are made in Settings → Keyboard or under `[keymap.*]` in `settings.toml`. A conflict checker refuses keys that would never fire or would break another key. It is for users whose desktop takes a Strata key, or who want a key for a command their map lacks.

## Behavior

### Saved overrides

- Settings saves only entries that differ from the shipped keys, under `[keymap.default]` and `[keymap.tenxer]` in `settings.toml`. lgse/strata#1885
- With no changed entries, `settings.toml` has no `keymap` table. lgse/strata#1885 (unverified)
- With `[keymap.default] toggle_hidden_files = ["F7"]` saved before launch, F7 toggles hidden files without opening Settings. lgse/strata#1885
- An entry replaces the command's whole entry in that map, primary key first; the other map keeps its own keys. lgse/strata#1885
- An entry with an empty list, such as `duplicate = []`, unbinds the command in that map. lgse/strata#1885
- An unknown id, an entry that is not a list, or a key Strata cannot read is logged once with the file's path. lgse/strata#1885
- Such an entry stays in the file as written after a save, and the command keeps its shipped keys. lgse/strata#1885
- An unquoted id with a dot, such as `go.home = ["<Shift>h"]`, is read as a table, logged, and kept unused. lgse/strata#1885
- An uppercase letter without `<Shift>`, such as `"G"`, binds plain `g` and logs a warning. lgse/strata#1885
- A `[keymap.default]` or `[keymap.tenxer]` value that is not a table is dropped and logged; the other map's entries still apply. lgse/strata#1885
- Tables under `[keymap]` other than `default` and `tenxer` are dropped when Strata saves. lgse/strata#1885
- Keys a hand edit adds are checked when the tables are first built; each finding is logged once with the file, table, id, key, and finding. lgse/strata#1885
- An entry with such a finding still applies. lgse/strata#1885
- A hand edit made while Strata runs applies at the next launch, and a change saved from Settings meanwhile overwrites it. lgse/strata#1885
- A change saved from Settings applies at once in every open window. lgse/strata#1885
- After a rebind, labels, hints, tooltips, accessible labels, context-menu accelerators, the footer, and F1 show the new keys without a restart. lgse/strata#1885

### Matching

- A key in the 10xer table works only in 10xer mode: rebinding 10xer Rename leaves the default map's F2 and Ctrl+R working. lgse/strata#1885
- A rebound command keeps its binding's modifiers required: refresh rebound to Ctrl+R does not run on a plain R. lgse/strata#1885
- A plain printable key a user adds, such as `rename = ["e"]`, types in a focused text field, a popover, and active type-to-search. lgse/strata#1885
- The file chooser's own keys and thumbnail resizing read the default table in both modes. lgse/strata#1885

### Escape, Enter, Tab and the arrows

- A key added to `escape`, `activate`, `focus_next`, `focus_previous`, `up`, `down`, `left`, or `right` acts as that key itself. lgse/strata#1885
- It does so in the file list, the sidebar, dialogs, menus, the file chooser, and Settings. lgse/strata#1885
- With `activate = ["Return", "o"]` and type-to-search off, `o` on a folder in List opens it. lgse/strata#1885
- With `escape = ["Escape", "<Control>bracketleft"]`, Ctrl+[ cancels an inline rename and keeps the old name. lgse/strata#1885
- Physical Escape still cancels when the `escape` entry leaves it out. lgse/strata#1885
- A plain printable alias types in a focused text field or popover, and in the default map while type-to-search is on. lgse/strata#1885
- A plain printable arrow alias moves through the file list, sidebar, header, preview, footer panels, file chooser, and delete confirmations. lgse/strata#1885
- It does not move through other dialogs, Settings, document tables, or the media timeline. lgse/strata#1885
- In a text box with several lines, a key added to `activate` or `focus_next` inserts no new line or tab. lgse/strata#1885
- A key added to `focus_next` completes location paths as Tab does. lgse/strata#1885

### Conflict checks

- In the default table, capturing Ctrl+C on Rename is refused with a note naming Copy, and the entry is unchanged. lgse/strata#1885
- A top-level key equal to a 10xer chord trigger, such as `g`, is refused. lgse/strata#1885
- A Sort step key that holds Shift is refused, since Shift reverses a sort step. lgse/strata#1885
- Ctrl+Space, or Shift with an arrow, Home, End, Page Up, or Page Down, is refused on a command the file list or chooser matches. lgse/strata#1885
- Ctrl+Space or Super+Space is refused on a command that acts while a text field has focus. lgse/strata#1885
- Ctrl+Shift with a tab digit, Backspace, and Space in the 10xer file list are refused as fixed keys. lgse/strata#1885
- A step on its own trigger's key, such as `g g`, `c c`, or `t t`, is valid. lgse/strata#1885
- A plain key in the default map while type-to-search is on saves with a note and a **Turn off type-to-search** button. lgse/strata#1885
- Alt with a letter saves with a note that the file chooser may take it for its accept button. lgse/strata#1885
- A hand-edited entry for a command its map cannot run, such as `yank` under `[keymap.default]`, never blocks another command's key. lgse/strata#1885
- A lone Num Lock or Scroll Lock press during a capture records nothing, and the capture keeps waiting. lgse/strata#1885 (unverified)

### Settings → Keyboard

- Settings lists a **Keyboard** page with a keyboard icon, subtitled "Shortcuts for each mode", whose navigation row is named "Keyboard settings". lgse/strata#1885 (unverified)
- The page has no KEYBINDS heading. The Default / 10xer mode switch comes first, with **Reset all** at the right end of its row. lgse/strata#1885
- **Search keybinds** sits beneath the switch; on a narrow dialog **Reset all** wraps to its own line, right-aligned. lgse/strata#1885
- The switch shows one table at a time and opens on the active mode. lgse/strata#1885
- Typing `rename` in **Search keybinds** lists only the Rename row; text matching no action shows "No matching shortcuts". lgse/strata#1885
- The search also matches a slot row by the name of the custom action it runs. lgse/strata#1885
- A search that matches no row in the shown table but some in the other switches to the other table. lgse/strata#1885 (unverified)
- Rows follow the F1 reference's sections, and each table lists only actions its mode can run. lgse/strata#1885
- The default table leaves out 10xer chord triggers, and the 10xer table lists no custom action slots. lgse/strata#1885
- A 10xer chord step's row shows its trigger's key in front of its own. lgse/strata#1885
- Each key is a chip with a remove button; an action with no key shows **Not bound**. lgse/strata#1885
- **Add** shows "Press a key…"; Escape then cancels, and Backspace removes every key of the action. lgse/strata#1885
- Any other key is checked and appended when no error is found; a refused key keeps the capture waiting and shows why under the row. lgse/strata#1885
- Moving focus outside the capture ends it, and a key the action already has ends it unchanged. lgse/strata#1885 (unverified)
- With Russian active, Ctrl and the key that types у record Ctrl+E, as labels show it. lgse/strata#1885
- A key with a warning is saved with a short note under the row; a key that never fires there is struck through. lgse/strata#1885
- A row's **Reset** appears once its entry differs from the shipped one, and restores the shipped keys. lgse/strata#1885
- **Reset all** opens a "Reset all keybinds?" dialog with the shown mode as subtitle; Reset restores that table, Cancel keeps every change. lgse/strata#1885
- **Reset all** is insensitive while the shown table has no changed entry. lgse/strata#1885 (unverified)
- **Reset all** keeps entries whose ids Strata does not know. lgse/strata#1885
- Changes save at once, and the page follows changes another window makes. lgse/strata#1885
- A keymap row keeps its copy at 20 characters or more; when copy and chips cannot share a line, the chips drop below. lgse/strata#1885
- With Ctrl+E added and the F2 chip removed on default Rename, Ctrl+E starts an inline rename and F2 does nothing. lgse/strata#1885

### Direct commands

- No table binds a direct command by default. lgse/strata#1885
- In the default map, a key bound to Open with, Move to, Copy to, Restore, invert selection, or search subfolders runs it. lgse/strata#1885
- So does one bound to the visited or recent folder jump, half-page up or down, or a Sort, Copy, or Action step. lgse/strata#1885
- In the default map, direct Move to, Copy to, Extract to, search, and folder jumps open the 10xer footer prompts. lgse/strata#1885
- Default-map direct verbs act on the selection only; with the focused row unselected they do nothing, as Copy does. lgse/strata#1885
- A default-map half-page key moves the selection, as Page Down does. lgse/strata#1885
- Escape in the file list ends a search a default-map direct key started. lgse/strata#1885
- Shift does not reverse a direct Sort step key. lgse/strata#1885
- In 10xer mode, a key bound to duplicate, pin, jump to folder, or arrow scope runs it. lgse/strata#1885
- A 10xer direct verb with nothing filled acts on the item under the cursor. lgse/strata#1885
- A 10xer direct pin key over search hits pins the hit under the cursor. lgse/strata#1885
- In 10xer mode, copy path runs on a bound key that types nothing, such as one with Ctrl or an F key. lgse/strata#1885
- Direct commands never run while a text field has focus, or in the portal file chooser. lgse/strata#1885
- A hand-edited key on a command its map cannot run, such as yank or a Go step in the default map, does nothing. lgse/strata#1885

### Custom action slots

- The default table lists **Custom action 1** to **Custom action 10** under **Custom actions**, with no keys shipped. lgse/strata#1885
- Each slot row shows the name of the action it runs under its title, or **No action**. lgse/strata#1885
- The slot name follows actions as they are added, renamed, or removed in Settings → Actions. lgse/strata#1885
- A slot key runs only in the default map, and only with the file list focused. lgse/strata#1885 (unverified)

## Design

[docs/keymap.md](https://github.com/lgse/strata/blob/73b3258ff9da7fd5f8b279e442e4fbf576850deb/docs/keymap.md) is the user guide. [docs/keyboard-shortcuts.md](https://github.com/lgse/strata/blob/73b3258ff9da7fd5f8b279e442e4fbf576850deb/docs/keyboard-shortcuts.md) covers commands, structural keys, the checker, and the Settings page.

- Every shortcut was fixed in code. Users could not move a key that clashed with their desktop, or give a key to a command their map lacked (lgse/strata#1884).
- Each map has its own table. One shared table was rejected because the two maps differ by design and would be forced to stay in step (lgse/strata#1884).
- Overrides store only changes, and unknown ids are kept, so a newer version's entries survive an older version's save (lgse/strata#1884, lgse/strata#1885).
- One action is one `Command` with per-map defaults. The per-map duplicate constants were merged, and handlers, labels, and F1 resolve through the registry, so a shown key always works (lgse/strata#1885).
- `on_press` reads a structural alias as its canonical key, so every surface sees the same press. A last-in-line controller, `install_native_aliases`, gives an unclaimed alias the canonical key's GTK effect (lgse/strata#1885).
- The checker's surface tables copy the dispatchers' stage order by hand. Guard tests press keys through the real dispatchers, so the checker cannot drift from them (lgse/strata#1885).
- The planned `StepEqualsTrigger` rule was dropped: shipped `g g`, `c c`, and `t t` are valid steps on their own trigger (lgse/strata#1885).
- A capture records the key as labels show it. The Russian scenario captures the key that types у, Ctrl+E, because Copy holds Ctrl+C (lgse/strata#1885).
- The direct stage exists for commands only one map had a key for. It runs the handler the other map uses, on the active map's targets (lgse/strata#1884, lgse/strata#1885).
- Custom action slots follow the Settings → Actions order, disabled actions included, so a slot keeps its action when another is turned off (lgse/strata#1885).
- The plan's E2E coverage became QA scenarios in `tests/qa/scenarios/keymap/`, because the E2E suite was replaced (lgse/strata#1885).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-28 | lgse/strata#1885 | feat | Made shortcuts remappable per map in `settings.toml` and Settings → Keyboard, so users can move clashing keys and bind commands their map lacked. |

## Known gaps

- Keys added to the default table for hidden files, page down, last item, preview, and Back also fire in 10xer mode. The 10xer table does not show them. lgse/strata#1885
- On AZERTY, capturing Ctrl+& records `<Control>ampersand` when Ctrl+1 is free. lgse/strata#1885
