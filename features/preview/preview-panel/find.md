---
title: Find in preview
status: shipped
origin: {issue: lgse/strata#1558, pr: lgse/strata#1559}
branch: null
reviewed_at: 442d325be108ff95391f0fe76cbd89da8db9e129
review: draft
code: [src/ui/preview/find.rs]
tests: [src/ui/preview/tests/find.rs, tests/e2e/scenarios/test_quick_preview.py]
docs: [docs/document-previews.md]
related: [preview/preview-panel/documents, integration/10xer-mode/preview-keys, preview/quick-preview]
---

## Summary

A find bar below the preview header that searches the text loaded in the open preview. It serves source, plain-text, and rendered document previews, and never filters the file listing.

## Behavior

### Opening and closing

- The header shows a **Find in preview** button, after View source or View rendered and before Open, only while the preview has searchable text. lgse/strata#1559
- The button's tooltip reads "Find in preview (Ctrl+F)", or "Find in preview (/)" in 10xer mode, and updates when 10xer is toggled. lgse/strata#1559
- In the default key map, Ctrl+F with focus in the preview opens the find bar with the entry focused and the previous query selected. lgse/strata#1559, lgse/strata#1558
- With focus in the file listing, Ctrl+F still opens the filename filter, not preview find. lgse/strata#1559, lgse/strata#1558
- In 10xer mode, `/` or keypad `/` with the preview owning the keys opens find; Ctrl+F still pages the document down. lgse/strata#1559
- In 10xer mode, `/` in a preview with no searchable text, such as an archive or media, opens the listing's search prompt. lgse/strata#1559
- Escape, or the **Close find** button, hides the bar and returns keys to the document; the preview stays open and the selected match stays selected for Ctrl+C. lgse/strata#1559

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
- Rendered table cells, PDF pages, images, archives, and media are not searched; a preview holding only tables shows no find button. lgse/strata#1559
- Switching View source or View rendered keeps the query and runs it on the new view. lgse/strata#1559, lgse/strata#1558
- Previewing another file, or closing the drawer, closes find and clears the query; reloading the same file keeps it. lgse/strata#1559

## Design

`docs/document-previews.md` ("Text selection and find") is the maintained description.

- Find reuses the virtual document model, its document-coordinate selection, and the existing header-button and entry styles (lgse/strata#1558, lgse/strata#1559).
- The find bar never changes the listing's selection, entries, or filename filter (lgse/strata#1558).
- 10xer uses `/` because Ctrl+F pages the document there, and Ctrl+Page Down is taken by tab switching. An earlier commit bound Ctrl+F and was reversed (lgse/strata#1559).
- Matching is literal and case-insensitive over loaded text only. Lowercasing keeps a map to original character offsets, so selections land on the original text (lgse/strata#1559).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-10 | lgse/strata#1559 | fix | Added a find bar for loaded preview text, opened with Ctrl+F or `/` in 10xer mode. |

## Known gaps

- Find searches only the open preview; searching file contents across a folder is not shipped. lgse/strata#1211
- Rendered table cells, PDF text, and OCR are out of find's scope and deferred. lgse/strata#1559
