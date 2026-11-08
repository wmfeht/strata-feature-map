---
title: 10xer letter bookmarks
status: shipped
origin: {issue: lgse/strata#1787, pr: lgse/strata#1790}
branch: null
reviewed_at: 9fb7a36ad4352337f3ada0d43710dc6d4ae838b9
review: draft
code: [src/services/letter_bookmarks.rs]
tests: [src/services/letter_bookmarks/tests.rs, src/ui/window/tests/keyboard_dispatch/letter_bookmarks.rs, src/ui/window/tests/keyboard_dispatch/letter_bookmarks/**, tests/qa/scenarios/letter_bookmarks]
related: [browser/sidebar, app/keyboard-shortcuts, app/keyboard-shortcuts/remapping, app/shortcut-reference, integration/10xer-mode/preview-keys, integration/10xer-mode/file-chooser]
---

## Summary

Vim-style marks for 10xer mode: `m` then a letter saves the focused pane's local folder, and `'` then the letter jumps back. Bookmarks are shared by all windows and survive restarts, apart from sidebar pins. They serve keyboard users who return to a few folders often.

## Behavior

### Saving

- With the file listing focused, `m` arms the save chord: the footer pill reads `m-` and the panel shows one row, `a–z` Save bookmark. lgse/strata#2086, lgse/strata#1790
- `m` then a lowercase letter saves the keyboard-focused pane's current folder under that letter and flashes `Saved bookmark <letter>`. A selected child folder is not saved. lgse/strata#1787, lgse/strata#1790
- `m` then a letter already in use replaces that letter's folder and keeps the other letters. lgse/strata#1787, lgse/strata#1790
- `m` then a letter in a folder with no native path, such as Trash or Network, flashes `Only local folders can be bookmarked` and saves nothing. lgse/strata#1790
- A save always reports `Saved bookmark <letter>` or `Could not access bookmarks: …`, even after later keys or navigation during the write. lgse/strata#1790
- When `letter-bookmarks.json` does not parse, `m x` replaces it with a file holding only `x`. lgse/strata#1790
- Any save drops unusable entries: a key that is not one lowercase letter, a non-`file:` URI, or a `file:` URI naming another host. lgse/strata#1790
- When `letter-bookmarks.json` is a symlink, the save fails and the link's target is unchanged. lgse/strata#1790 (unverified)

### Storage

- Bookmarks are stored in `$XDG_DATA_HOME/strata/letter-bookmarks.json`, by default `~/.local/share/strata/letter-bookmarks.json`, as `{"entries":{"<letter>":"file://…"}}`. lgse/strata#1790
- A bookmark saved in one window appears in another window's `'` menu, and bookmarks survive a restart. lgse/strata#1787, lgse/strata#1790
- Unknown fields in the file are ignored on read, so a file a newer version wrote still loads. lgse/strata#1790
- Folder paths that are not UTF-8 save and load unchanged. lgse/strata#1790 (unverified)

### Jump menu

- `'` arms the jump chord with the pill `'-`. Once the file is read, the panel lists each saved letter beside its full folder path, and no unused letter. lgse/strata#2086, lgse/strata#1790
- The `'` panel leaves out entries with an unusable key or a non-local URI. lgse/strata#1790 (unverified)
- `'` with no saved bookmarks shows the `'-` pill and no panel. lgse/strata#1790
- `'` when the file cannot be read or does not parse flashes `Could not access bookmarks: …` and cancels the chord, so the next key runs normally. lgse/strata#1790
- Esc or `m` pressed before the `'` panel loads keeps it from appearing afterwards; `m` shows its own `a–z` panel. lgse/strata#1790 (unverified)

### Jumping

- `'` then a saved letter navigates the focused pane to that folder after a folder check succeeds within 2 s. lgse/strata#1790
- `'` then a letter whose folder is removed, unreadable, or not checked within 2 s flashes `Bookmark <letter> is unavailable`. The folder, selection, and navigation are unchanged. lgse/strata#1790
- `'` then a letter whose entry is not a local `file:` URI, such as `sftp://…` or `file://otherhost/…`, flashes `Bookmark <letter> is unavailable` and stays put. lgse/strata#1790
- `'` then an unsaved letter flashes `No bookmark <letter>`, and a `g c` folder check already running still completes. lgse/strata#1790

### Pending jump

- While a jump's folder check runs, any non-modifier key cancels it without navigating. The key is consumed, so it clears no selection, closes no preview, and runs no command. lgse/strata#1790
- During the check, focus leaving the listing, leaving 10xer mode, a selection or focus change by the user, or navigation cancels the jump without navigating. lgse/strata#1790
- A folder load or rescan during the check also cancels the jump without feedback. lgse/strata#1790
- Another program deleting the focused item during the check does not cancel the jump. lgse/strata#1790

### Second keys

- After `m` or `'`, a digit, a Ctrl-modified letter, or a Shift letter such as `A` cancels with `Unknown chord` and runs no other command. Esc cancels silently. lgse/strata#1787, lgse/strata#1790
- In the default map, `m` and `'` arm nothing, and in the location field they are typed as text. lgse/strata#1790

## Design

- Letters are stable slots, unlike numbered sidebar pins, which follow display order and offer nine keys. The model is Vim and Yazi marks (lgse/strata#1787).
- Bookmarks are kept apart from pins and preferences. Every read and read-modify-write runs on the storage worker, so windows share changes without filesystem work on the GTK thread (lgse/strata#1790).
- The file lives in the data directory, not the state directory, because bookmarks are user-saved, "closer to pins than to state" (lgse/strata#1790).
- A jump navigates only after the folder check succeeds. Treating a folder as missing only when deleted let unreadable or stalled folders replace the listing (lgse/strata#1790).
- A save is never cancelled, so it skips the checks a jump needs and always reports its result (lgse/strata#1790).
- Only `file:` URIs without another host are local. Resolving a URI through GIO mapped gvfs remote URIs to FUSE paths (lgse/strata#1790).
- Reads tolerate unknown fields and bad keys, and saves recover from an unparseable file, as navigation history does (lgse/strata#1790).
- The letters are a fixed catalog range after rebindable `bookmark_set` and `bookmark_go` triggers, like the digits after Go, Action, and Tabs, so remapping and conflict checks see the triggers (lgse/strata#1790).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-11-07 | lgse/strata#2086 | feat | Added persistent letter bookmarks: `m` + a–z saves the focused pane's local folder, `'` + a letter jumps back after a folder check (lgse/strata#1790). |

## Known gaps

- A folder load or rescan cancels a pending `'` jump with no feedback, because loads publish their selection unflagged. lgse/strata#1790
