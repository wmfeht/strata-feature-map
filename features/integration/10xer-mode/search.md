---
title: 10xer find, filter, and search
status: shipped
origin: {issue: lgse/strata#1246, pr: lgse/strata#1297}
branch: null
reviewed_at: 72b840e69d6f0df9d33fb5583e62a3a2944886a1
review: draft
code: [src/ui/browser/find.rs, src/ui/browser/listing_filter.rs, src/ui/browser/listing_search.rs, src/ui/browser/result_selection.rs, src/services/path_match.rs]
tests: [src/ui/window/tests/keyboard_dispatch/footer_prompt.rs, src/ui/browser/find/tests.rs, src/services/path_match/tests.rs]
related: [browser/search]
---

## Summary

The three footer name prompts of 10xer mode: `/` and `?` find in the listing without hiding rows, `f` filters the current folder, and `s` searches paths below it the way fzf does.

## Behavior

### Find

- `/` and `?` open a footer find prompt; Enter moves the cursor to the next or previous name containing the text. lgse/strata#1297, lgse/strata#1244
- Find ignores case, searches in display order from the cursor, and wraps at either end. lgse/strata#1297 (unverified)
- After Enter, matching substrings stay highlighted in Columns, Icons, and List and no rows hide; Esc from the listing removes the highlights. lgse/strata#1297, lgse/strata#1244
- Find highlights draw the match on the theme accent and recolor on a live theme change. lgse/strata#1297 (unverified)
- Enter on an empty find prompt changes nothing; Esc from the prompt cancels without leaving highlights. lgse/strata#1297, lgse/strata#1244
- `n` repeats the last find in its direction and `N` reverses it; a miss flashes `No matches for “…”` and leaves the cursor in place. lgse/strata#1297, lgse/strata#1244
- `n` or `N` with no earlier find flashes `No previous find`. lgse/strata#1297 (unverified)
- In the `/`, `?`, `f`, and `s` prompts, Up and Down move the listing cursor while the prompt keeps focus. lgse/strata#1297, lgse/strata#1244
- When another program deletes the cursor's file while the `f` or `s` prompt has focus, focus stays in the prompt. lgse/strata#1439, lgse/strata#1544

### Filter

- `f` opens a `filter:` prompt that hides non-matching items of the current folder as you type. lgse/strata#1297, lgse/strata#1245
- Enter commits the filter and focuses the first result without opening it; empty Enter, Esc from the prompt, or Esc from the listing clears it. lgse/strata#1297, lgse/strata#1245
- Pressing `f` again pre-fills the current filter query. lgse/strata#1297, lgse/strata#1245
- While an `f` filter is active, the footer shows `filter: …` and the displayed result count, including zero. lgse/strata#1297, lgse/strata#1245
- `f` uses the same fuzzy terms as `s` but matches only the folder's own items, even with Include subfolders on, so `rep md` keeps `gamma-report.md`. lgse/strata#1403
- Turning the mode on re-runs an open Ctrl+F filter with `f` matching, and turning it off re-runs it with default matching. lgse/strata#1403
- Leaving the mode clears the find, every `f` filter, and an `s` search in every window. lgse/strata#1244, lgse/strata#1297 (unverified)

### Search

- `s` opens a `search:` prompt that searches paths below the current folder, even with Include subfolders off, and shows at most 100 hits. lgse/strata#1297
- Each space-separated term must fuzzily match the path, in any order, so `git trading readme` finds `git/trading/README.md`. lgse/strata#1403
- Terms accept `'exact`, `^prefix`, `suffix$`, and `!excluded`. lgse/strata#1403
- Wildcard filter patterns do not apply in `f` or `s`. lgse/strata#1403
- Hits whose names match more terms rank first, then by match quality; among similar matches, hits in folders visited often and recently rank higher. lgse/strata#1403
- The characters each `s` hit's or `f` item's name matched are highlighted in the theme accent and follow live theme changes. lgse/strata#1403
- While find highlights show, they replace the `f` and `s` match highlights. lgse/strata#1403
- The footer shows `search: …`, the hit count including zero, and the hit under the cursor as a path relative to the searched folder. lgse/strata#1297
- Enter applies the query and focuses the first hit without opening it; a second Enter opens the hit. lgse/strata#1297
- Esc from a nonempty prompt keeps the hits; Esc from an empty prompt cancels. lgse/strata#1297
- Dismissing the search restores the previous `f` filter, or the plain listing. lgse/strata#1297
- Pressing `s` while hits are showing pre-fills that query. lgse/strata#1297
- A newer query, navigation, leaving the mode, or closing the window drops a slower result stream; changing view keeps the search. lgse/strata#1297
- A folder with no local path, such as Network, flashes `Nothing to search`. lgse/strata#1297
- `S` is unbound, and Ctrl+K global search is unchanged. lgse/strata#1297

### Search results

- With hits showing, `j`/`k` in List and Columns and the direction keys in Icons move among the hits. lgse/strata#1297
- `g g` and `G` reach the first and last hit. lgse/strata#1297
- `g f` opens the folder holding the focused hit, selects it there, and ends the search. lgse/strata#1297
- `i` on a directory hit opens an unfocused column or folder peek, and on a file hit toggles the preview. lgse/strata#1297
- In List and Columns, `h` dismisses the search unless a preview owns the keys. lgse/strata#1297

## Design

- `s` borrows the focused listing's filter with subfolders forced on. The filter's 100-hit cap and stale-work cancellation therefore govern search (lgse/strata#1297).
- Forcing the scope switches matching from the filter's name rules to fuzzy path terms (lgse/strata#1403).
- The saved Include subfolders preference is never changed by `s`, and an earlier `f` filter survives it (lgse/strata#1297).
- Searching stays inside the current folder tree; content search is out of scope (lgse/strata#1152).
- Plain recursive name search did not let users narrow by folder names. Fuzzy path terms, as in fzf, do (lgse/strata#1380).
- Matching uses the MIT `frizbee` crate behind `services::path_match`, which handles Unicode folding, term parsing, ranking tiers, and frecency bias (lgse/strata#1403).
- Frecency adds a capped bias, so it reorders only similar matches and never lifts a hit above one whose name matches more terms (lgse/strata#1403).
- Outside the mode, global search and the default Ctrl+F filter keep their own matching (lgse/strata#1403).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-10 | lgse/strata#1544 | fix | Kept focus in a focused `f` or `s` prompt when files change outside Strata. |
| 2026-10-09 | lgse/strata#1533 | fix | Added the shared check that counts a focused pane-filter result as filter focus; footer `f` filters keep their own Escape order. |
| 2026-10-03 | lgse/strata#1403 | feat | Made `s` and `f` match fuzzy fzf-style terms with frecency ranking, and shared the matcher with the folder picker. |
| 2026-09-27 | lgse/strata#1297 | feat | Added footer find, filter, and a current-tree recursive name search. |

## Known gaps

None known.
