---
title: PDF text selection
status: shipped
origin: {issue: lgse/strata#1220, pr: lgse/strata#1223}
branch: null
reviewed_at: 86df474dc0e8352e0e2098637a017cc4c77a8c44
review: draft
code: [src/ui/preview/pdf_text.rs]
tests: [src/ui/preview/pdf_text/tests.rs, src/ui/preview/pdf_ranges_tests.rs, tests/fixtures/documents/text.pdf, tests/qa/scenarios/quick_preview/pdf-preview-copies-text.jsonl]
related: [preview/preview-panel/sandbox, preview/quick-preview]
---

## Summary

A text layer over rendered PDF pages, so text can be selected and copied from a PDF preview without opening a PDF viewer. The sandboxed renderer returns each page's glyph layout with its image; the drawer draws the selection and builds the copied text. Page rendering, zoom, and password handling stay on `preview/preview-panel`.

## Behavior

- Dragging across PDF text highlights it in the theme accent; Ctrl+C then copies it in page order with the document's line breaks. lgse/strata#1223
- Double-click selects a word, and triple-click selects a line without its line break. lgse/strata#1223
- Dragging after a double-click extends the selection word by word; after a triple-click, line by line. lgse/strata#1223
- Shift+click extends the selection, across pages. lgse/strata#1223
- A drag that ends on a later page selects every page between its ends. lgse/strata#1223 (unverified)
- With focus in a PDF, Ctrl+A selects the text of every loaded page. lgse/strata#1223
- With no text selected, Ctrl+C on a focused PDF copies nothing and leaves the clipboard unchanged. lgse/strata#1576 (unverified)
- On a focused PDF, plain A, Ctrl+Shift+A, Ctrl+Alt+A, Ctrl+Shift+C, and Ctrl+Alt+C neither select nor copy. lgse/strata#1576 (unverified)
- Dragging on a page margin, or on a page without a text layer such as a scan, pans the view instead of selecting. lgse/strata#1223
- Highlight bands cover each line's box, but stop short below the baseline on runs without descender glyphs. lgse/strata#1223
- Selected text on a page scrolled out of view stays copyable until the selection changes. lgse/strata#1223 (unverified)

## Design

- PDFs render in the sandbox, so the text layer travels with each page as a bounded `result.text` sidecar to the PNG. It follows the `result.meta` pattern (lgse/strata#1220, lgse/strata#1223).
- Selection flows through the text like a document viewer. Rectangular block selection was rejected because it copies in visual order (lgse/strata#1220).
- The existing pan gesture decides per press: a press near glyphs selects, any other press pans (lgse/strata#1223).
- Ctrl+A and Ctrl+C reuse the preview's focus and keyboard dispatch (lgse/strata#1223).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |

## Known gaps

None known.
