---
title: Rendered document previews
status: shipped
origin: {issue: lgse/strata#89, pr: lgse/strata#187}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [src/services/document.rs, src/services/document_media.rs, src/services/docx.rs, src/services/docx/namespaces.rs, src/services/rtf.rs, src/services/table.rs, src/ui/document_view.rs, src/ui/document_media.rs, src/ui/virtual_preview.rs, src/ui/table_view.rs, src/ui/table_view/selection.rs, src/sandbox_helper/document_media.rs, data/math-renderer.js, packaging/math-renderer]
tests: [src/services/document/tests.rs, src/services/document_media/tests.rs, src/services/docx/tests.rs, src/services/docx/namespaces/tests.rs, src/services/rtf/tests.rs, src/services/table/tests.rs, src/ui/document_media/tests.rs, src/ui/virtual_preview/tests.rs, src/ui/table_view/selection/tests.rs, src/sandbox_helper/document_media/tests.rs, tests/fixtures/spreadsheets]
docs: [docs/document-previews.md]
related: [preview/preview-panel/sandbox, settings/preferences, settings/themes]
---

## Summary

Native GTK rendering of local Markdown, an HTML subset, RTF, CSV, TSV, XLS, XLSX, ODS, and DOCX files in the preview panel. Text formats switch between Rendered and Source; nothing uses a web engine or runs document scripts.

## Behavior

### Rendered and Source

- Selecting a local Markdown, HTML, RTF, CSV, or TSV file with **Render documents by default** on shows the rendered document; with it off, the source. lgse/strata#187, lgse/strata#729, lgse/strata#1086
- **View source** and **View rendered** in the preview header switch the current document without changing the saved preference. lgse/strata#187
- Remote Markdown and HTML files preview as source only. lgse/strata#187
- A remote XLS, XLSX, ODS, or DOCX file shows "Copy this file locally before previewing it" instead of a preview. lgse/strata#729, lgse/strata#1086 (unverified)
- A malformed, truncated, timed-out, or limit-exceeding document opens in Source, hides the view switch, and shows the reason above the source. lgse/strata#187
- Documents over 1 MiB, 20,000 parser events, nesting depth 32, 4 MiB of markup, or 500 ms of parsing fall back to Source. lgse/strata#187
- A Markdown or HTML table row over 256 columns also falls back to Source. lgse/strata#729
- Dragging across headings, paragraphs, lists, code, and tables, then Ctrl+C, copies the selected text with original line breaks. lgse/strata#187
- Fenced code with a known language hint renders with theme syntax highlighting. lgse/strata#187
- Every rendered code block shows a **Copy code** button that copies the whole block. lgse/strata#187

### HTML and links

- HTML scripts, styles, forms, frames, objects, images, and event handlers are omitted, with the notice "Unsupported or active HTML content was omitted." lgse/strata#187
- `u` and `ins` render as underline without the omission notice. lgse/strata#1086
- Clicking an `http` or `https` link opens it externally; other schemes stay inert. lgse/strata#187

### Tables and workbooks

- CSV and TSV files render as a table whose first row is the column titles, with quoted multiline fields and ragged rows parsed. lgse/strata#729
- XLS, XLSX, and ODS files show their first worksheet as a table with no Source view; formulas are not recalculated and macros never run. lgse/strata#729
- Tables open sorted ascending by the first column; clicking a column title toggles ascending and descending. lgse/strata#729
- Sorting puts numbers first, then case-insensitive text, then empty cells, and never changes the file. lgse/strata#729
- Every column, including the last, resizes by dragging its divider. lgse/strata#729
- Tables over 200 rows or 512 cells render in full. lgse/strata#729
- CSV, TSV, and workbook output stops at 100,000 values, 4 MiB of cell text, or 256 columns. lgse/strata#729
- A limited table shows "Table preview reached its text, column, or value budget; open the file to see all data." lgse/strata#729
- Dragging across cells and pressing Ctrl+C copies the range as tab-separated rows in displayed sort order. lgse/strata#729
- With focus on the table, Ctrl+C copies every loaded row in the current sort order, including offscreen rows. lgse/strata#729

### Images, diagrams, and equations

- Markdown images with relative paths render PNG, JPEG, GIF, WebP, BMP, and SVG files inside the document's folder, including percent-encoded names. lgse/strata#1075
- Absolute, `file:`, data, and remote image URLs are not loaded, and the notice "Remote and absolute image URLs are not loaded. Use images inside the document's folder." appears. lgse/strata#1075
- A missing or undecodable image keeps its alt text and the rest of the document renders. lgse/strata#1075
- Fenced `mermaid` blocks render as diagrams in theme colors, with **Copy diagram source**; invalid syntax keeps the source with a fallback notice. lgse/strata#1075
- `$...$`, `$$...$$`, and fenced `latex` or `math` blocks render as equations; display equations offer **Copy equation source**. lgse/strata#1075
- Copying a selection containing inline math keeps its original `$` delimiters. lgse/strata#1075
- Changing the theme while a diagram or equation is open recolors it. lgse/strata#1075

### RTF and DOCX

- RTF renders paragraphs, bold, italic, underline, strikethrough, Windows-1252 `\'hh` escapes, and `\uN` escapes, and keeps its Source view. lgse/strata#1086
- DOCX renders headings, `Title`, `Subtitle`, quotes, inline formatting, nested bulleted and numbered lists, and tables with the first row as sortable titles. lgse/strata#1086
- DOCX has no Source view; images, hyperlink targets, headers, footers, footnotes, and comments are omitted. lgse/strata#1086
- DOCX files with alternate XML namespace prefixes or default namespaces keep their Word content. lgse/strata#1086

## Design

[docs/document-previews.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/document-previews.md) is the maintained contract for formats, limits, tables, and the trust boundary.

- HTML must not turn the preview into a browser. A native renderer for a documented subset was chosen over Chromium, Electron, WebKitGTK, or external converters (lgse/strata#89).
- Markdown, HTML, RTF, CSV, and TSV are parsed in-process by pure-Rust parsers off the GTK thread. They see only the bounded source string and emit escaped Pango markup (lgse/strata#187).
- Calamine and `docx-rs` can allocate whole sheets or decompress every part, so workbooks and DOCX run in the preview sandbox under a 20 MiB input limit. Only validated JSON returns; DOCX HTML is reparsed by the same bounded HTML parser (lgse/strata#729, lgse/strata#1086).
- Large source and rendered views use recycled, virtualized rows, so only visible rows own layouts. Selection is kept in document coordinates and copy reads the model (lgse/strata#187).
- One table renderer serves CSV, TSV, workbooks, Markdown, HTML, and DOCX tables, replacing the 200-row capped grid (lgse/strata#723, lgse/strata#729).
- Images are opened beneath the document directory, copied to private files, and decoded in the sandbox. Mermaid uses `mermaid-svg`; equations use pinned MathJax in QuickJS with no host bindings, as a string argument (lgse/strata#1075).
- `mermaid-rs-renderer` was replaced by `mermaid-svg` to drop the unmaintained `ttf-parser` (lgse/strata#1074).
- RTF uses a hand-written converter, because `rtf-parser` 0.4.3 dropped `\par`, mis-decoded `\'93`, and corrupted `\uN` fallbacks (lgse/strata#1086).
- At most 16 media items are kept per preview and four render at once in the pooled preview worker (lgse/strata#1075, lgse/strata#1222).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-19 | lgse/strata#1086 | feat | Rendered RTF in process and DOCX in the sandbox through the shared document view. |
| 2026-09-17 | lgse/strata#1075 | feat | Rendered relative Markdown images, Mermaid diagrams, and LaTeX equations in the sandbox. |
| 2026-09-17 | lgse/strata#729 | feat | Added sortable, resizable virtual tables for CSV, TSV, workbooks, and document tables. |
| 2026-09-16 | lgse/strata#187 | feat | Added native Rendered and Source previews for Markdown and an HTML subset. |

## Known gaps

- Workbooks preview only their first worksheet; multi-sheet navigation was deferred. lgse/strata#723
- PPTX, PPT, ODP, DOC, and ODT files have no rendered preview. lgse/strata#730, lgse/strata#244
- Markdown cannot be edited or rendered with Pandoc or Quarto from the preview. lgse/strata#1127
