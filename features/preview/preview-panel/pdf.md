---
title: PDF pages, zoom, and text selection
status: shipped
origin: {issue: lgse/strata#1220, pr: lgse/strata#1223}
branch: null
reviewed_at: bae71c026b94e109b7507c4fe895c3ceed642f8f
review: draft
code: [src/ui/preview/pdf_text.rs, src/ui/preview/pdf.rs, src/ui/preview/pdf/**, src/sandbox_helper/pdf.rs]
tests: [src/ui/preview/pdf_text/tests.rs, src/ui/preview/pdf_ranges_tests.rs, src/adapters/local_preview/tests/pdf.rs, tests/fixtures/documents/text.pdf, tests/qa/scenarios/quick_preview/pdf-preview-copies-text.jsonl, tests/qa/scenarios/quick_preview/pdf-zoom-keeps-text-size.jsonl]
related: [preview/preview-panel/sandbox, preview/quick-preview]
---

## Summary

A text layer over rendered PDF pages, so text can be selected and copied from a PDF preview without opening a PDF viewer. The sandboxed renderer returns each page's glyph layout with its image; the drawer draws the selection and builds the copied text. The node also owns the PDF viewer's page rendering and zoom. Password handling stays on `preview/preview-panel`.

## Behavior

### Pages and zoom

- PDF pages render at the preview pane's width, at most 1280 px, one page at a time across previews. lgse/strata#898, lgse/strata#823
- Queued PDF pages that leave the view are cancelled before rendering. lgse/strata#898
- Ctrl+wheel over a PDF, including its scrollbars, zooms its pages between 1× and 4× its fitted width; interface text size does not change. lgse/strata#1069, lgse/strata#1622 (unverified)
- With keyboard focus in a zoomed PDF, Ctrl+0 returns its pages to fitted width on the same page; interface text size does not change. lgse/strata#1622
- With Num Lock on, Ctrl+keypad 0 also resets a focused PDF's zoom. lgse/strata#1622 (unverified)
- Ctrl+0 on a focused PDF already at fitted width is consumed and does not reset interface text size. lgse/strata#1622
- In 10xer mode, Ctrl+0 on a focused zoomed PDF also resets its zoom. lgse/strata#1622
- With focus in a PDF, Ctrl+Alt+0 and Ctrl+Super+0 leave its zoom unchanged. lgse/strata#1576

### Text selection

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
- PDF pages once rendered concurrently per visible row, spawning over 100 helpers while scrolling (lgse/strata#815). Rendering at viewport width and serializing pages cut helper RSS from about 411 to 112 MiB (lgse/strata#898).
- PDF zoom reset skips the view-center correction, because the list view re-anchors the visible page itself; correcting it jumped to page 1 (lgse/strata#1622).
- Ctrl+0 on a focused PDF is consumed even at fitted width, so a reset meant for the page never resets the saved text size (lgse/strata#1622).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |

## Known gaps

- With a PDF focused, Ctrl++ and Ctrl+− change interface text size, not PDF zoom; PDF zoom for them is a possible follow-up. lgse/strata#1622
