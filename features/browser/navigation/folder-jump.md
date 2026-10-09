---
title: Folder jump
status: shipped
origin: {issue: lgse/strata#276, pr: lgse/strata#959}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: reviewed
code: [src/services/navigation_history.rs]
tests: [src/services/navigation_history/tests.rs]
related: [browser/search, integration/10xer-mode]
---

## Summary

A keyboard palette, Ctrl+Shift+K, that reopens folders previously visited in Strata, ranked by how often and how recently each was opened. Strata learns the list from browsing, separately from pinned folders.

## Behavior

- Ctrl+Shift+K opens a "Jump to a folder…" palette; Ctrl+K still opens global file search. lgse/strata#959
- With an empty query, the palette lists visited folders by frequency and recency of visits. lgse/strata#959
- Typing narrows the list to visited folders whose name or path fuzzily matches the text. lgse/strata#959
- Each space-separated term may match anywhere in a folder's full path, so `dev str` finds `~/dev/strata`. lgse/strata#1403
- Terms accept fzf's `'exact`, `^prefix`, `suffix$`, and `!excluded` forms; `strata !notes` hides folders whose path matches `notes`. lgse/strata#1403
- Folders whose names match more terms rank higher, and an exact name ranks first among them. lgse/strata#1403
- Arrow keys choose a row, and Enter opens the chosen folder. lgse/strata#959
- The palette lists at most 100 folders. lgse/strata#959 (unverified)
- Only local folders that finish loading are recorded. lgse/strata#959
- A folder that fails to load is recorded after a successful retry. lgse/strata#959 (unverified)
- Before any folder is recorded, the palette shows "No folder history yet". lgse/strata#959 (unverified)
- A query that matches no visited folder shows "No matching folders". lgse/strata#959 (unverified)
- Pressing Ctrl+Shift+K while the search palette is open closes it. lgse/strata#959 (unverified)

## Design

Strata keeps its own history instead of reading zoxide, to avoid an external dependency and mixing terminal history into Strata (lgse/strata#276). Pins stay explicit favorites; the jump list is learned (lgse/strata#276).

- History is stored as `navigation-history.json` in the user state directory, with paths as URIs so non-UTF-8 names round-trip (lgse/strata#959).
- Each visit adds 1 to a folder's rank. Rank is weighted by last visit: ×4 within an hour, ×2 within a day, ×0.5 within a week, ×0.25 after (lgse/strata#959).
- When total rank passes 10,000, every rank is scaled so the total is 9,000, and folders below 1 are dropped. The list keeps at most 1,000 folders (lgse/strata#959).
- Text relevance outranks frecency, which only orders similar matches (lgse/strata#959, lgse/strata#1403).
- The same history drives 10xer `z` and `Z`, and biases 10xer fuzzy search and the folder picker toward often-visited folders (lgse/strata#1304, lgse/strata#1403).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-17 | lgse/strata#959 | feat | Added Ctrl+Shift+K folder jump ranked by Strata's own visit frecency. |

## Known gaps

None known.
