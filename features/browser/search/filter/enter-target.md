---
title: Filter Enter target
status: shipped
origin: {issue: lgse/strata#1643, pr: lgse/strata#1822}
branch: null
reviewed_at: 86df474dc0e8352e0e2098637a017cc4c77a8c44
review: reviewed
code: [src/ui/enter_target.rs]
tests: [src/ui/enter_target/tests.rs, tests/qa/scenarios/filter_results/filter-enter-opens-top-match.jsonl]
related: [browser/view-modes, browser/view-modes/columns, integration/10xer-mode]
---

## Summary

While the Ctrl+F filter field has focus, the result Enter would open is outlined and kept in view. Picking another result moves Enter to the pick until the query changes. It serves Columns, Icons, and List, search results and the in-place filter.

## Behavior

- With the field focused and a query with results, the top result has a 1 px accent outline. This holds in Columns, Icons, and List. lgse/strata#1822
- In search results the outline comes with no selection; the in-place filter keeps the listing's selection. lgse/strata#1822
- Moving focus from the field to a result or elsewhere removes the outline. lgse/strata#1822
- In Icons and List, Enter in the field with no pick opens the outlined top result. This holds for search results and for a filter that narrows rows in place. lgse/strata#1822
- A pick, such as Ctrl+click on `old-reports` then a click back in the field, removes the outline; Enter then opens the pick. lgse/strata#1822
- A pick is an arrow key, Down from the field, a click, a Ctrl+click, focus moving into the results, or another user selection change. lgse/strata#1822
- Deselecting every result after a pick returns the outline and Enter to the top result. lgse/strata#1822 (unverified)
- In search results, editing the query text drops the pick and the results' selection; the outline moves to the new top result. lgse/strata#1822
- Editing the query and typing it back, such as adding then removing a trailing space, still counts as a query edit and drops the pick. lgse/strata#1822 (unverified)
- In Trash, Recent, or a network share, where the filter narrows rows in place, a query edit keeps the selection but drops the pick. lgse/strata#1822
- A same-query update, such as another program creating a matching file, keeps the pick, the selection, and its preview. lgse/strata#1822
- While the field has focus, the list keeps the top result scrolled into view as results arrive. lgse/strata#1822
- A button press, wheel scroll, touch, or drag hover on the results stops that scrolling; the next query edit scrolls back to the top result. lgse/strata#1822
- With only the outline showing, Space in the field types a space and opens no preview. lgse/strata#1822
- With 10xer mode on, no result is outlined and a query edit keeps the selected result, in the Ctrl+F field too. lgse/strata#1822 (unverified)
- In the file chooser, Enter in the filter field chooses the top result in Columns, Icons, and List. lgse/strata#1822

## Design

The parent's Design carries the selection rule this replaced: lgse/strata#1628 selected the first match, and lgse/strata#1643 settled on returning to the top on a new query.

- The top result is outlined, not selected. lgse/strata#1765 selected row 0, so Space in the field previewed the hit and multi-word queries broke ([comment](https://github.com/lgse/strata/pull/1765#issuecomment-6304253858), [review](https://github.com/lgse/strata/pull/1765#issuecomment-6307467566)).
- The same review asked that later batches follow row 0, that Columns be covered, and that the Shift-click anchor not go stale. lgse/strata#1822 marks the top on each batch, covers Columns, and drops the anchor with the selection.
- One module, `src/ui/enter_target.rs`, owns the pick rule. Picks are user selection and focus changes; each surface's own writes do not count (lgse/strata#1822).
- The 10xer **f** and **s** prompts keep their own two-step Enter, so the outline and the pick rule do not apply there (lgse/strata#1822).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |

## Known gaps

None known.
