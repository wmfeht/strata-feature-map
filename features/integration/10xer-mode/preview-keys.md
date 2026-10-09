---
title: 10xer preview key ownership
status: shipped
origin: {issue: lgse/strata#1242, pr: lgse/strata#1295}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
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
- `h`, Left, or Shift+Tab returns the keys to the same cursor without closing the drawer; the next `h` opens the parent folder. lgse/strata#1295
- Esc or `i` inside the preview closes the drawer and returns the keys to the listing. lgse/strata#1295
- `i` or `l` on a file Strata cannot preview flashes `Nothing to preview`. lgse/strata#1295
- While the preview owns the keys, an accent bar runs across the top of its header. lgse/strata#1295
- Leaving the mode, clicking the listing, or closing the drawer releases key ownership. lgse/strata#1295
- `J`/`K` scroll an open preview from the listing without moving focus. lgse/strata#1295

### Surfaces

- In a document, `j`/`k`, Home, End, `G`, Ctrl+U/D/B/F, and paging scroll the document, and the listing does not move. lgse/strata#1295
- In a document or archive, `g g` goes to the top of the preview; other `g` chords run from the listing. lgse/strata#1296
- In an archive tree, `j`/`k` move between members and `l` or Enter opens a member folder; nothing is extracted and no listing file opens. lgse/strata#1295
- In an archive tree, `h` at the archive root returns the keys to the listing. lgse/strata#1295
- A password field takes typed letters, including `h` and `j`, and its text-editing shortcuts until unlocked. lgse/strata#1295
- In a media preview, Space plays or pauses, Left/Right seek, Up/Down change volume, and `m` mutes. lgse/strata#1295 (unverified)
- With an audio or video preview open, `<` and `>` step to the previous or next file of that type and keep playing. They work from the listing too. lgse/strata#1289, lgse/strata#1474
- Enter in a document or media preview opens the file through the listing. lgse/strata#1340

### Handing keys back

- While the preview owns the keys, `j`/`k`, Space, `v`/`V`, Ctrl+A, and Ctrl+R never move or fill the listing behind the drawer. lgse/strata#1295
- File and folder commands such as `d`, `y`, `M`, `z`, and Backspace return the keys to the listing and run there. The drawer stays open. lgse/strata#1340

## Design

- Interactive previews already had input owners: archive trees, password entries, and media controls. Document scrolling could ship first, but those surfaces waited for a published precedence table (lgse/strata#1242).
- The rule for every surface: no ambiguous key may trigger a listing mutation or a file launch (lgse/strata#1242).
- Each surface owns a fixed set of keys and swallows the listing's motion and selection keys; listing commands it does not use go back to the listing (lgse/strata#1340).
- Ownership never outlives the drawer, so no key can target a destroyed control (lgse/strata#1242, lgse/strata#1295).
- With the mode off, archive and media keys stay on the default map (lgse/strata#1295).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-27 | lgse/strata#1295 | feat | Gave the preview its own key owner so preview keys cannot launch, move, or select listing items. |

## Known gaps

None known.
