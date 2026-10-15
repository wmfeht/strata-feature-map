---
title: Find in preview
status: shipped
origin: {issue: lgse/strata#1558, pr: lgse/strata#1559}
branch: null
reviewed_at: 6e654a7b68fdfeb0a6eec8239a95b16ccfb1cea8
review: draft
code: [src/ui/preview/find.rs]
tests: [src/ui/preview/tests/find.rs, tests/e2e/scenarios/test_quick_preview.py]
docs: [site/src/reference/document-previews.md]
related: [preview/preview-panel/documents, integration/10xer-mode/preview-keys, preview/quick-preview]
---

## Summary

A find bar below the preview header that searches the text loaded in the open preview. It serves source, plain-text, and rendered document previews, and never filters the file listing.

## Behavior

### Opening and closing

- The header shows a **Find in preview** button only while the preview has searchable text. lgse/strata#1559
- The find button sits after View source or View rendered and before Open. lgse/strata#1559 (unverified)
- The button's tooltip reads "Find in preview (Ctrl+F)", or "Find in preview (/)" in 10xer mode. lgse/strata#1559
- Toggling 10xer mode updates the tooltip of an open preview's find button. lgse/strata#1559 (unverified)
- In the default key map, Ctrl+F with focus in the preview opens the find bar with the entry focused and the previous query selected. lgse/strata#1559, lgse/strata#1558
- With focus in the file listing, Ctrl+F still opens the filename filter, not preview find. lgse/strata#1559, lgse/strata#1558
- In 10xer mode, `/` or keypad `/` with a searchable preview owning the keys opens find. lgse/strata#1559
- Escape, or the **Close find** button, hides the bar and returns keys to the document. lgse/strata#1559
- After closing find, the preview stays open and the selected match stays selected for Ctrl+C. lgse/strata#1559

### Searching

- Typing a query selects and reveals the first literal, case-insensitive match, so "éclair" finds "ÉCLAIR". lgse/strata#1559, lgse/strata#1558
- The status reads "Match 1 of N", or "No matches", and is hidden while the query is empty. lgse/strata#1559
- Enter and **Next match** move to the next match, Shift+Enter and **Previous match** to the previous one, wrapping at either end. lgse/strata#1559
- With zero matches, **Next match** and **Previous match** are insensitive. lgse/strata#1559 (unverified)
- Matches do not overlap: "aa" in "aaa" counts 1. lgse/strata#1559 (unverified)
- The query field accepts at most 256 characters. lgse/strata#1559 (unverified)
- An open find re-runs while an incrementally loaded source preview grows. lgse/strata#1559

### Scope

- Find searches small source buffers, large virtualized source, rendered Markdown, HTML, and RTF prose and code, and DOCX prose. lgse/strata#1559, lgse/strata#1558
- Rendered table cells, PDF pages, images, archives, and media are not searched. lgse/strata#1559
- In Rendered view, a document holding only tables shows no find button; its Source view is searchable. lgse/strata#1559
- Switching View source or View rendered keeps the query and runs it on the new view. lgse/strata#1559, lgse/strata#1558
- Previewing another file, or closing the drawer, closes find and clears the query. lgse/strata#1559
- Reloading the same file keeps the query. lgse/strata#1559 (unverified)

## Design

`docs/document-previews.md` ("Text selection and find") is the maintained description.

- Find reuses the virtual document model, its document-coordinate selection, and the existing header-button and entry styles (lgse/strata#1558, lgse/strata#1559).
- Find never changes the file listing or its filename filter (lgse/strata#1558, lgse/strata#1559).
- Matching is literal and case-insensitive over loaded text only (lgse/strata#1559).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-10 | lgse/strata#1559 | fix | Added a find bar for loaded preview text, opened with Ctrl+F or `/` in 10xer mode. |

## Known gaps

None known.
