---
title: 10xer preview key ownership
status: shipped
origin: {issue: lgse/strata#1242, pr: lgse/strata#1295}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: reviewed
code: [src/ui/window/keyboard/preview.rs]
tests: [src/ui/window/tests/keyboard_dispatch/preview_ownership.rs]
related: [preview/preview-panel]
---

## Summary

In 10xer mode an open file preview can take the keys, so motion scrolls or operates the preview instead of the listing behind it. It covers opening, entering, leaving, and closing the preview drawer, and each preview surface's keys.

## Behavior

### Opening and leaving

- `i` on a file toggles the preview drawer and leaves focus in the listing, so `j`/`k` move the cursor and the preview follows. lgse/strata#1295
- In List and Columns, `l` or Right on a previewable file opens the drawer if needed and moves the keys into it. lgse/strata#1295
- With the preview owning the keys, a further `l` or Right does not open the file. lgse/strata#1295
- In a document, `h` or Left returns the keys to the same cursor without closing the drawer. In a media preview, `h` does so. lgse/strata#1295
- Shift+Tab on any preview surface returns the keys to the same cursor with the drawer still open. lgse/strata#1295
- After the keys return, the next `h` opens the parent folder. lgse/strata#1295
- Esc or `i` inside the preview closes the drawer and returns the keys to the listing. lgse/strata#1295
- `i` or `l` on a file Strata cannot preview flashes `Nothing to preview`. lgse/strata#1295
- While the preview owns the keys, an accent bar runs across the top of its header, and no Miller column shows its destination bar. lgse/strata#1295, lgse/strata#1343
- Leaving the mode, clicking the listing, or closing the drawer releases key ownership. lgse/strata#1295
- If the drawer is hidden for lack of room when `l` is pressed, it takes the keys when shown again for the same file. Moving the cursor first cancels that. lgse/strata#1295
- `J`/`K` scroll an open preview from the listing without moving focus. lgse/strata#1295

### Surfaces

- In a document, `j`/`k`, Up/Down, Home, End, `G`, Ctrl+U/D/B/F, and Page Up/Down scroll the document, and the listing does not move. lgse/strata#1295
- In a document, Ctrl+A selects all and Ctrl+C copies the document's own text, never listing items. lgse/strata#1295
- In a document or archive, `g g` goes to the top of the preview. lgse/strata#1296
- In an archive tree, `j`/`k` or Up/Down move between members, and `l`, Right, or Enter opens a member folder. Nothing is extracted and no listing file opens. lgse/strata#1295
- In an archive tree, Home and End or `G` move to the first and last member. lgse/strata#1295
- In an archive tree, `h` or Left goes up one member level; at the archive root it returns the keys to the listing with the drawer open. lgse/strata#1295, lgse/strata#1343
- A password prompt takes focus when it appears, including when `i` or cursor movement shows a locked archive. lgse/strata#1295
- A password field takes typed letters, including `h` and `j`, and its text-editing shortcuts until unlocked. Esc and Shift+Tab still close or return. lgse/strata#1295
- In a media preview, Space plays or pauses, Left/Right seek 5 seconds, Up/Down change volume, and `m` mutes or unmutes. lgse/strata#1295, lgse/strata#1289
- With an audio or video preview open, `<` and `>` step to the previous or next file of that type and keep playing. They work from the listing too. lgse/strata#1289, lgse/strata#1474
- A focused preview button or slider keeps GTK's own Space, Enter, and arrow handling. lgse/strata#1295
- Enter or `o` in a document or media preview returns the keys to the listing and opens the file there; the drawer stays open. lgse/strata#1340
- Enter on a video preview opens it in the default player where the preview stopped. lgse/strata#1474

### Handing keys back

- While the preview owns the keys, `j`/`k`, Space, `v`/`V`, Ctrl+A, and Ctrl+R never move or fill the listing behind the drawer. lgse/strata#1295, lgse/strata#1340
- File and folder commands such as `d`, `y`, `M`, `z`, `/`, and Backspace return the keys to the listing and run there. The drawer stays open. lgse/strata#1340
- A `g` place chord such as `g 3` returns the keys to the listing and runs there; `g z` flashes `Unknown chord` and keeps the keys in the preview. lgse/strata#1296, lgse/strata#1340
- Window commands such as F1, F5, Ctrl+L, Ctrl+1 to Ctrl+3, and Ctrl+N work without moving the keys out of the preview. lgse/strata#1304, lgse/strata#1340

## Design

- Issue lgse/strata#1242 required a published precedence table naming each surface's Space, `i`, `h`, `l`, Enter, and Esc owner. It barred inferring archive keys from document scrolling. The table is in `docs/10xer-mode.md`.
- Keys held by the drawer must not launch, move, rename, delete, paste, or select listing items (lgse/strata#1242, lgse/strata#1295).
- Each surface owns a fixed set of keys and swallows the listing's motion and selection keys; listing commands it does not use go back to the listing (lgse/strata#1340).
- Ownership never outlives the drawer, so no key can target a destroyed control (lgse/strata#1242, lgse/strata#1295).
- With the mode off, archive and media keys stay on the default map (lgse/strata#1295).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-27 | lgse/strata#1295 | feat | Gave the preview its own key owner so preview keys cannot launch, move, or select listing items. |

## Known gaps

None known.
