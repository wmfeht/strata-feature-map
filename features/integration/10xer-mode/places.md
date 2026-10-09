---
title: 10xer place chords and folder picker
status: shipped
origin: {issue: lgse/strata#1243, pr: lgse/strata#1296}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [src/ui/window/keyboard/chords.rs, src/ui/folder_picker.rs]
tests: [src/ui/window/tests/keyboard_dispatch/place_chords.rs, src/ui/window/tests/keyboard_dispatch/go_prompt.rs, src/ui/window/tests/keyboard_dispatch/folder_jump.rs, src/ui/folder_picker/tests.rs]
related: [browser/sidebar, browser/navigation]
---

## Summary

Keyboard jumps to places and folders in 10xer mode: the `g` chord, pins, the `go ›` path prompt, `z` / `Z` history jumps, and the shared fuzzy folder picker that `go ›`, `move to ›`, `copy to ›`, and `extract to ›` use.

## Behavior

### The `g` chord

- `g` arms a chord: the footer shows a `g-` pill with a panel listing each valid second key, and the panel never takes focus. lgse/strata#1296, lgse/strata#1304
- While `g` is armed, the sidebar shows keycaps on Home, Downloads, Documents, Pictures, Videos, Trash, Network, Recent, and visible pins. lgse/strata#1296
- `g g` moves to the first item. lgse/strata#1296
- `g h`, `g c`, `g d`, `g t`, `g n`, `g r`, `g k`, `g p`, and `g v` open Home, `~/.config`, Downloads, Trash, Network, Recent, Documents, Pictures, and Videos. lgse/strata#1296
- `g m` opens the XDG Music folder. lgse/strata#1342
- A missing user folder flashes `No Downloads folder`, `No Documents folder`, `No Pictures folder`, or `No Videos folder` and stays put. lgse/strata#1296
- `g 1` to `g 9` open the visible PINNED rows in sidebar order, skipping bookmarks that are standard places; a missing pin flashes `No pin N`. lgse/strata#1296
- Esc cancels an armed chord, and any other unknown second key cancels it with `Unknown chord`. lgse/strata#1296
- Opening Settings, leaving the mode, or closing the window drops an armed chord. lgse/strata#1296

### Pins

- `g +` or keypad `+` pins the folder under the cursor, or the current folder from a file. It flashes `Pinned “Name” as g N`. lgse/strata#1340
- `g -` or keypad `-` unpins it and flashes `Unpinned “Name”`; pinning twice flashes `“Name” is already pinned`. lgse/strata#1340
- Standard places and Trash flash `Can’t pin “Name”`. lgse/strata#1340

### `go ›`

- `g Space` opens a footer `go ›` prompt; typing never navigates. lgse/strata#1302
- Enter submits through location-bar navigation: absolute, `~`, and relative paths work, with `.` and `..` resolved like `cd`. lgse/strata#1302
- A path naming a file opens its folder with that file selected. lgse/strata#1302, lgse/strata#1403
- A URI is submitted unchanged, and a password typed in it moves into the mount operation instead of the location. lgse/strata#1302
- A missing or unreachable destination shows the location bar's error and keeps the current folder open. lgse/strata#1302
- The entry is cleared on submit, Esc, focus loss, a replacing prompt, and mode exit, and it keeps no undo history. lgse/strata#1302
- Text that looks like a URI (`scheme://`, `//host`, `\\host`, `user@host:`) lists no folders and is never searched, mounted, or probed before Enter. lgse/strata#1302, lgse/strata#1403

### `z` and `Z`

- `z` opens `jump ›` and Shift+Z opens `recent ›`, both listing folders from Strata's own navigation history above the footer. lgse/strata#1304
- `z` ranks folders whose names match first, then by how often and how recently each was opened; `Z` keeps last-visit order. lgse/strata#1304, lgse/strata#1403
- Both match each folder's full path with fuzzy terms in any order, so `z dev str` finds `~/dev/strata`. lgse/strata#1403
- The folder already open is left out, and the first candidate is chosen, including for empty input. lgse/strata#1304
- Up/Down choose another candidate, wrapping, while the entry keeps focus; Enter or a click opens the chosen folder once. lgse/strata#1304
- A miss shows `No matching folders`, and Enter then leaves the prompt open without navigating. lgse/strata#1304
- Esc, focus loss, a replacing prompt, a clicked listing row, and leaving the mode close the prompt without opening a candidate. lgse/strata#1304

### Folder picker

- In `go ›`, `move to ›`, `copy to ›`, and `extract to ›`, typing lists up to 100 matching folders below the open folder. lgse/strata#1403
- A folder the whole query names exactly, by path and then by name, is listed first. lgse/strata#1403
- Text starting with `/`, `~`, `./`, or `../` searches below the folder it names, and the rest is the query, so `~/dev/str` searches `~/dev`. lgse/strata#1403
- A typed path ending in `/`, such as `/etc/`, lists that folder first, then the folders below it, most visited first. lgse/strata#1403
- Tab writes the chosen folder into the prompt as `./…/`, `~/…/`, or an absolute path, and never acts on it. lgse/strata#1403
- Enter on a typed path that exists acts on it at once; otherwise Enter waits for the search to finish. lgse/strata#1403
- A search from `/` skips `/proc`, `/sys`, and `/dev`. lgse/strata#1403
- Text with a colon that is not a URI, such as `10:30`, is an ordinary query. lgse/strata#1403
- In `go ›`, a URI or a path that matches no folder still opens through location-bar navigation. lgse/strata#1403

## Design

- `g` is the shared armed-chord interaction that the copy, sort, action, and tab chords reuse. A pending chord has one consumer, so a cancelled chord leaves no key that later acts alone (lgse/strata#1296).
- Ctrl+Shift+B is the fallback route to the sidebar; `g` chords are the main one (lgse/strata#1284).
- `go ›` exists because typed credentials must not be retained: the entry is cleared on every exit path and keeps no undo history (lgse/strata#1248, lgse/strata#1302).
- `z` and `Z` read Strata's saved navigation history, the same as Ctrl+Shift+K, rather than a zoxide database, which is out of scope (lgse/strata#1152, lgse/strata#1304).
- The fuzzy folder picker replaced Tab folder completion and its `go_completion` module (lgse/strata#1403).
- Enter waits for a running picker search so a better match found late still wins (lgse/strata#1403).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-28 | lgse/strata#1304 | feat | Added `z` and `Z` jumps over navigation history and the chord key panel. |
| 2026-09-27 | lgse/strata#1302 | feat | Added the `go ›` prompt with folder completion and no retained credentials. |
| 2026-09-27 | lgse/strata#1296 | feat | Added the armed `g` chord, place jumps, and pin jumps. |

## Known gaps

None known.
