---
title: Slash enters filtered folders
status: shipped
origin: {issue: lgse/strata#1744, pr: lgse/strata#1802}
branch: null
reviewed_at: fb7eb0c4ee8bcb681651e56e91031ed95422e8ff
review: draft
code: []
tests: [src/ui/window/tests/keyboard_dispatch/footer_prompt/filter_slash.rs, src/ui/window/tests/keyboard_dispatch/filter_focus/filter_slash.rs, tests/qa/scenarios/filter_results/filter-slash-enters-folder.jsonl]
related: [browser/search/filter, integration/10xer-mode/file-chooser, app/shortcut-reference]
---

## Summary

`/` typed in the Ctrl+F filter field or the 10xer `f` prompt enters the matching folder, clears the query, and keeps filtering in the new folder, so `doc/proj/` walks down two levels. It serves keyboard users who filter a folder and then step into a result. The Ctrl+F field always enters the first result; the `f` prompt follows the result cursor.

## Behavior

### Entering a folder

- With the Ctrl+F field or the 10xer `f` prompt focused, `/` after a query whose first displayed result is a folder opens that folder. lgse/strata#2086, lgse/strata#1802
- That holds in Columns, Icons, List, and the file chooser, with Include subfolders on or off. lgse/strata#2086, lgse/strata#1802
- After `/` enters a folder, the query clears and the field or prompt stays focused there with the listing unfiltered: `doc` `/` `proj` `/` reaches Documents/Projects. lgse/strata#2086, lgse/strata#1802
- In the `f` prompt, once Up or Down has moved the result cursor since the query last changed, `/` enters the highlighted result instead of the first. lgse/strata#2086, lgse/strata#1802
- In the `f` prompt, editing the query or reopening `f` makes `/` enter the first result again. lgse/strata#2086, lgse/strata#1802
- In the Ctrl+F field, `/` enters the first displayed result even after Up or Down. lgse/strata#2086, lgse/strata#1802
- On a remote share filtered in place, Ctrl+F `/` enters the first result, and `f` `/` after Up or Down enters the folder under the listing cursor. lgse/strata#2086, lgse/strata#1802
- A fuzzy `f` match counts: the first result need only match the query's terms. lgse/strata#2086, lgse/strata#1802
- In the file chooser, `/` enters the folder without accepting the request. lgse/strata#2086, lgse/strata#1802
- In the chooser, Escape after that closes the filter, and a second Escape cancels the request. lgse/strata#2086, lgse/strata#1802 (unverified)
- `/` typed into the 10xer `s`, `/`, or `?` prompt is ordinary text and enters no folder. lgse/strata#2086, lgse/strata#1802
- With 10xer mode on, a `/` typed into a Ctrl+F field is typed as text; only the `f` prompt descends. lgse/strata#2086, lgse/strata#1802 (unverified)

### When nothing happens

- With an empty query, a query with no match, or a file as that result, `/` leaves the folder, the query, and the focus unchanged and is not typed. lgse/strata#2086, lgse/strata#1802
- A query of only spaces counts as empty, so `/` enters nothing and is not typed. lgse/strata#2086, lgse/strata#1802 (unverified)

### Typing and input methods

- In either field, `/` over a selected query, such as after Ctrl+A, enters the folder; the query is not deleted first. lgse/strata#2086, lgse/strata#1802
- In overwrite mode, `/` puts the overwritten character back and leaves the cursor where it was. lgse/strata#2086, lgse/strata#1802
- A layout that types `/` with Shift, such as German Shift+7, enters the folder too. lgse/strata#2086, lgse/strata#1802
- A Zhuyin, Array30, or Boshiamy code that starts with `/` still composes; only a lone committed `/` enters a folder. lgse/strata#2086, lgse/strata#1802
- Pasting a lone `/` enters the folder; pasting longer text such as `/Projects` types it and navigates nowhere. lgse/strata#2086, lgse/strata#1802

### Waiting and cancelling

- While the query's results are pending, `/` waits and enters the first result once it is a folder. With recursive results it waits through empty indexing batches. lgse/strata#2086, lgse/strata#1802
- Indexing ends the wait at the first match, or when indexing finishes: a file arriving first ends it without navigating. lgse/strata#2086, lgse/strata#1802
- In a folder still listing, `/` waits until a folder is the first match, or the listing ends or fails. lgse/strata#2086, lgse/strata#1802
- Editing the query, Escape, focus leaving the field or prompt, or navigation elsewhere cancels a waiting `/`, which then never navigates. lgse/strata#2086, lgse/strata#1802
- Focus leaving the `f` prompt cancels a waiting `/` even when focus returns before the prompt closes. lgse/strata#2086, lgse/strata#1802 (unverified)

## Design

- `/` cannot appear in a file name, so a filter never matches it. That makes it a safe "go inside the first match" key, the "ENTER, ENTER, f" of lgse/strata#1744.
- `/` is read from the field's committed text, not the key press. Catching the press swallowed a `/` that starts a Zhuyin, Array30, or Boshiamy syllable (lgse/strata#1802). [docs/keyboard-shortcuts.md](https://github.com/lgse/strata/blob/9fb7a36ad4352337f3ada0d43710dc6d4ae838b9/docs/keyboard-shortcuts.md) records it as the one exception to commands coming from key presses.
- The 10xer `f` prompt follows the result cursor because Enter, Enter opens the highlighted result; Ctrl+F keeps the first result (lgse/strata#1744, lgse/strata#1802).
- The wait is asymmetric: indexing waits for any first match, while a folder still listing waits only while no folder is first (lgse/strata#1802).
- A GTK `changed` that leaves the text unchanged, as after a selection restore, keeps a waiting `/` (lgse/strata#1802).
- The F1 label comes from a fixed, non-rebindable catalog entry, since the key is the filter's path separator (lgse/strata#1802).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-11-07 | lgse/strata#2086 | feat | Made `/` in a filter enter the matching folder and keep filtering there, as lgse/strata#1744 asked (lgse/strata#1802). |

## Known gaps

- `/` in the `/` and `?` find prompts does not enter folders; it waits on on-the-fly find highlighting. lgse/strata#1744
- An input method that shows `/` as preedit before committing it still deletes a selected query, because GTK deletes the selection when preedit starts. lgse/strata#1802
