---
title: Rendered document previews
status: shipped
origin: {issue: lgse/strata#89, pr: lgse/strata#187}
branch: null
reviewed_at: 2218357c2e91c0c3e6cd02638356f7a91c08bcae
review: draft
code: [src/services/document.rs, src/services/document_media.rs, src/services/docx.rs, src/services/docx/namespaces.rs, src/services/odt.rs, src/services/rtf.rs, src/services/table.rs, src/ui/document_view.rs, src/ui/document_media.rs, src/ui/virtual_preview.rs, src/ui/virtual_preview/selection.rs, src/ui/virtual_preview/scrollbar.rs, src/ui/virtual_preview/scrollbar/position.rs, src/ui/virtual_preview/line_numbers.rs, src/ui/table_view.rs, src/ui/table_view/selection.rs, src/sandbox_helper/document_media.rs, data/math-renderer.js, packaging/math-renderer]
tests: [src/services/document/tests.rs, src/services/document_media/tests.rs, src/services/docx/tests.rs, src/services/docx/namespaces/tests.rs, src/services/odt/tests.rs, src/services/rtf/tests.rs, src/services/table/tests.rs, src/ui/document_media/tests.rs, src/ui/virtual_preview/tests.rs, src/ui/virtual_preview/selection/tests.rs, src/ui/virtual_preview/scrollbar/tests.rs, src/ui/table_view/selection/tests.rs, src/sandbox_helper/document_media/tests.rs, tests/fixtures/spreadsheets, tests/fixtures/documents/report.docx, tests/fixtures/documents/report.odt, tests/qa/scenarios/quick_preview]
docs: [site/src/reference/document-previews.md, docs/document-previews.md]
related: [preview/preview-panel/sandbox, preview/preview-panel/find, settings/preferences, settings/themes]
---

## Summary

Native GTK rendering of local Markdown, an HTML subset, RTF, CSV, TSV, XLS, XLSX, ODS, DOCX, ODT, and OTT files in the preview panel. Text formats switch between Rendered and Source; nothing uses a web engine or runs document scripts.

## Behavior

### Rendered and Source

- Selecting a local Markdown, HTML, RTF, CSV, or TSV file with **Render documents by default** on shows the rendered document; with it off, the source. lgse/strata#187, lgse/strata#729, lgse/strata#1086
- **View source** and **View rendered** in the preview header switch the current document without changing the saved preference. lgse/strata#187
- Remote Markdown and HTML files preview as source only. lgse/strata#187
- A malformed, truncated, timed-out, or limit-exceeding document opens in Source, hides the view switch, and shows the reason above the source. lgse/strata#187
- Documents over 1 MiB, 20,000 parser events, nesting depth 32, 4 MiB of markup, or 500 ms of parsing fall back to Source. lgse/strata#187
- A Markdown or HTML table row over 256 columns also falls back to Source. lgse/strata#729
- Dragging across headings, paragraphs, lists, code, and tables, then Ctrl+C, copies the selected text with original line breaks. lgse/strata#187
- In rendered or large source documents, double-click selects a word and triple-click its logical line, a whole paragraph in prose; Ctrl+C copies exactly that text. lgse/strata#1559, lgse/strata#1557
- A click, then a Shift-click farther along, selects from the first click to the second. lgse/strata#1559, lgse/strata#1557
- With focus in a rendered or large source document, Shift+Left/Right, Shift+Up/Down, Shift+Home/End, and Ctrl+Shift+Left/Right extend the selection by character, line, line edge, or word. lgse/strata#1559, lgse/strata#1557
- Ctrl+Home and Ctrl+End move the caret to the start and end of the loaded document. lgse/strata#1559
- Keyboard selection crosses recycled rows and does not change the listing's selection. lgse/strata#1559
- Shift+Left/Right steps over a whole grapheme cluster, such as an emoji with a skin-tone modifier. lgse/strata#1559 (unverified)
- Right with a selection collapses it to its end. lgse/strata#1559 (unverified)
- In the default key map, plain Left in a document returns focus to the listing. lgse/strata#1559 (unverified)
- A click past the end of a wrapped line places the caret at that display line's end. lgse/strata#1559 (unverified)
- A Shift-click or double-click on a link selects text without opening the link; only a plain single click opens it. lgse/strata#1559 (unverified)
- With word wrap off, each rendered Markdown, HTML, or RTF row widens to its longest line, so the horizontal scrollbar reaches every line. lgse/strata#1612, lgse/strata#1610, lgse/strata#1834
- Touchpad, Shift+wheel, and the scrollbar all scroll an unwrapped rendered Markdown, HTML, or RTF document sideways. lgse/strata#1612, lgse/strata#1834
- Turning wrap on while a rendered Markdown, HTML, or RTF document is open reflows each paragraph to its full wrapped height without reopening. lgse/strata#1612, lgse/strata#1610, lgse/strata#1834
- Turning wrap off while a rendered Markdown, HTML, or RTF document is open returns rows to their unwrapped height, with no gaps. lgse/strata#1612, lgse/strata#1610, lgse/strata#1834
- Fenced code with a known language hint renders with theme syntax highlighting. lgse/strata#187
- Every rendered code block shows a **Copy code** button that copies the whole block. lgse/strata#187

### Scrolling

- In a rendered document or a large plain-text Source preview, holding the scrollbar thumb still keeps the content at one position. lgse/strata#1752, lgse/strata#1749
- Dragging the thumb downward never moves the content backward, and the content passes through interior positions on the way. lgse/strata#1752
- Dragging the thumb to the top or bottom of the track shows the document's first or last line, even while new rows are measured. lgse/strata#1752
- Releasing the thumb, even with the pointer over the content, leaves the content in place. The next wheel input scrolls it and the thumb follows. lgse/strata#1752
- Closing the preview while holding the thumb ends the drag; after reopening, the thumb follows scrolling again. lgse/strata#1752 (unverified)
- Setting the scrollbar to its minimum or maximum from the keyboard or an accessibility tool shows the document's exact start or end. lgse/strata#1752
- Wheel or touchpad scrolling forward over the content never moves the thumb backward; scrolling backward never moves it forward; stopping leaves it still. lgse/strata#1752
- With the first row's top in view the thumb sits at the top of the track; with the last row's end in view, at the bottom. lgse/strata#1752 (unverified)
- Touchpad momentum stops when the scroll range changes or the content origin shifts by 2 px or more. lgse/strata#1752
- After smooth scrolling, a click, drag selection, or link hover acts on the row under the pointer. lgse/strata#1752 (unverified)
- Document previews in the Open and Save file chooser scroll the same way as in the browser. lgse/strata#1752
- The vertical scrollbar sits beside the content instead of overlaying it, and hides when the whole document fits. lgse/strata#1752 (unverified)

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
- Closing the preview during a table cell drag ends the drag and its autoscroll. lgse/strata#1752 (unverified)
- With focus on the table, Ctrl+C copies every loaded row in the current sort order, including offscreen rows. lgse/strata#729
- With focus on the table, Ctrl+Shift+C, Ctrl+Alt+C, and Ctrl+Super+C copy nothing. lgse/strata#1576
- With a cell range selected, Ctrl+A or Ctrl+Shift+A clears the range; Ctrl+Alt+A leaves it. lgse/strata#729, lgse/strata#1576
- With a non-Latin layout such as Russian active, Ctrl+A in a focused table cell selects that cell's text. lgse/strata#1576
- With a non-Latin layout active and no cell range selected, Ctrl+C in a focused table cell copies its own selection, not the whole table. lgse/strata#1576

### Images, diagrams, and equations

- Markdown images with relative paths render PNG, JPEG, GIF, WebP, BMP, and SVG files inside the document's folder, including percent-encoded names. lgse/strata#1075
- Absolute, `file:`, data, and remote image URLs are not loaded, and the notice "Remote and absolute image URLs are not loaded. Use images inside the document's folder." appears. lgse/strata#1075
- A missing or undecodable image keeps its alt text and the rest of the document renders. lgse/strata#1075
- Fenced `mermaid` blocks render as diagrams in theme colors, with **Copy diagram source**; invalid syntax keeps the source with a fallback notice. lgse/strata#1075
- `$...$`, `$$...$$`, and fenced `latex` or `math` blocks render as equations; display equations offer **Copy equation source**. lgse/strata#1075
- Copying a selection containing inline math keeps its original `$` delimiters. lgse/strata#1075
- Changing the theme while a diagram or equation is open recolors it. lgse/strata#1075

### RTF, DOCX, and ODT

- RTF renders paragraphs, bold, italic, underline, strikethrough, Windows-1252 `\'hh` escapes, and `\uN` escapes, and keeps its Source view. lgse/strata#1086
- DOCX renders headings, `Title`, `Subtitle`, quotes, inline formatting, nested bulleted and numbered lists, and tables with the first row as sortable titles. lgse/strata#1086
- DOCX has no Source view; images, hyperlink targets, headers, footers, footnotes, and comments are omitted. lgse/strata#1086
- DOCX files with alternate XML namespace prefixes or default namespaces keep their Word content. lgse/strata#1086
- DOCX, ODT, and OTT paragraphs always wrap, with no horizontal scrollbar, whatever the wrap preference. lgse/strata#1834
- Selecting a local `.odt` or `.ott` file shows its rendered document with no Source view, instead of "No preview for this selection". lgse/strata#1834
- An uppercase `REPORT.ODT` or `REPORT.OTT` renders the same way. lgse/strata#1834 (unverified)
- An ODT copied without an extension, which GIO types `application/vnd.oasis.opendocument.text`, also renders. lgse/strata#1834 (unverified)
- ODT renders `text:h` headings at their outline level, and paragraphs styled `Title`, `Subtitle`, or `Heading N` as headings. lgse/strata#1834
- An ODT outline level above 6 renders as a level-6 heading; `Title` renders at level 1 and `Subtitle` at level 2. lgse/strata#1834 (unverified)
- ODT paragraphs styled `Quotations`, `Quote`, or `Intense Quote` render as quotations. lgse/strata#1834
- Consecutive ODT `Preformatted Text` paragraphs render as one code block that keeps their indentation. lgse/strata#1834
- That code block drops bold, italic, and other inline formatting. lgse/strata#1834 (unverified)
- ODT bold, italic, underline, strikethrough, and `Source Text` or `Teletype` monospace render from automatic styles, named styles, and their parents. lgse/strata#1834
- Emphasis set on a whole paragraph's style renders on plain and quotation paragraphs. lgse/strata#1834
- Paragraph-style emphasis is ignored on headings and preformatted text; table cells keep it. lgse/strata#1834 (unverified)
- In ODT, `http` and `https` links are clickable outside `Preformatted Text`. Links inside it, and links with other schemes, keep only their text. lgse/strata#1834 (unverified)
- ODT nested bulleted and numbered lists keep their nesting; lists deeper than eight levels continue at the eighth. lgse/strata#1834
- The first row of an ODT table's `table:table-header-rows` group becomes the column titles. Later header rows stay in the table as bold, sortable rows. A merged cell leaves an empty cell so the columns stay aligned. lgse/strata#1834 (unverified)
- An ODT table cell joins its paragraphs with a space, and a nested table's or list's text flattens into the cell. lgse/strata#1834
- An ODT table row over 256 cells (`TABLE_COLUMN_LIMIT`) truncates the document with the size-budget notice instead of falling back to Source. lgse/strata#1834 (unverified)
- In ODT, `text:line-break` renders as a line break, and `text:list-header` as a list item. lgse/strata#1834 (unverified)
- A heading inside an ODT table cell renders as cell text, not a heading; its style's emphasis still applies. lgse/strata#1834 (unverified)
- An ODT table without a header-row group shows "Column 1", "Column 2", and onward as titles, where DOCX would use its first row. lgse/strata#1834 (unverified)
- ODT images, drawings, text boxes, footnotes, comments, tracked deletions, headers, and footers are omitted. lgse/strata#1834
- Omitted ODT content shows no omission notice. lgse/strata#1834 (unverified)
- An ODT over the parser's size or event budget renders only its start. It shows "Document preview reached its size budget; open the file to see all content." lgse/strata#1834

## Design

[docs/document-previews.md](https://github.com/lgse/strata/blob/2218357c2e91c0c3e6cd02638356f7a91c08bcae/docs/document-previews.md) is the maintained contract for formats, limits, tables, and the trust boundary.

- HTML must not turn the preview into a browser. A native renderer for a documented subset was chosen over Chromium, Electron, WebKitGTK, or external converters (lgse/strata#89).
- Markdown, HTML, RTF, CSV, and TSV are parsed in-process by pure-Rust parsers off the GTK thread. They see only the bounded source string and emit escaped Pango markup (lgse/strata#187).
- Calamine and `docx-rs` can allocate whole sheets or decompress every part, so workbooks and DOCX run in the preview sandbox under a 20 MiB input limit. Only validated JSON returns; DOCX HTML is reparsed by the same bounded HTML parser (lgse/strata#729, lgse/strata#1086).
- Large source and rendered views use recycled, virtualized rows. Selection is kept in document coordinates and copy reads the model (lgse/strata#187). Rendered rows build their text, tables, and media only once mapped, and visited widgets may stay in GTK's bounded recycling pool. Source rows bind eagerly so thumb seeking uses measured heights (lgse/strata#1752).
- GTK estimates unmeasured row heights and re-anchors its pixel value, so a thumb mirroring those pixels jumped. The thumb now follows a separate document position, rows plus a text-offset fraction, while GTK's pixel adjustment still drives native input and kinetic scrolling (lgse/strata#1749, lgse/strata#1752).
- GTK's kinetic trajectory stores an absolute pixel origin, so stale momentum is cancelled rather than corrected. A 2 px tolerance absorbs GTK's integer rounding. A second scroll engine, disabled momentum, and two-frame `scroll_to` corrections were rejected (lgse/strata#1752).
- Unwrapped source rows already widened to their text, but rendered rows only got a height and clipped at the pane edge. Unwrapped rendered rows now widen to their longest line (lgse/strata#1610, lgse/strata#1612).
- Wrap toggles remeasure rows after GTK has re-laid them out, because measuring right after `set_wrap_mode` returned the previous mode's height (lgse/strata#1612).
- Virtual rows cannot take native input, so word, line, and Shift selection is computed in the document model. The selector had ignored click count and modifiers (lgse/strata#1557).
- One table renderer serves CSV, TSV, workbooks, Markdown, HTML, DOCX, and ODT tables, replacing the 200-row capped grid (lgse/strata#723, lgse/strata#729, lgse/strata#1834).
- Images are opened beneath the document directory, copied to private files, and decoded in the sandbox. Mermaid uses `mermaid-svg`; equations use pinned MathJax in QuickJS with no host bindings, as a string argument (lgse/strata#1075).
- `mermaid-rs-renderer` was replaced by `mermaid-svg` to drop the unmaintained `ttf-parser` (lgse/strata#1074).
- ODT has its own streaming `quick-xml` reader, which reads only `content.xml` and `styles.xml` in the sandbox under the same 20 MiB limit (lgse/strata#1813, lgse/strata#1834).
- That reader emits the DOCX HTML subset, so the HTML parser, layout, and size notice are shared with DOCX (lgse/strata#1834).
- LibreOffice headless conversion was rejected as too slow and a heavy dependency; the embedded thumbnail alone shows only the first page (lgse/strata#1813).
- Word processors store each paragraph as one line, so unwrapped DOCX and ODT showed one line per paragraph behind a horizontal scrollbar. Both now always wrap; workbook tables keep their layout (lgse/strata#1834).
- RTF uses a hand-written converter, because `rtf-parser` 0.4.3 dropped `\par`, mis-decoded `\'93`, and corrupted `\uN` fallbacks (lgse/strata#1086).
- At most 16 media items are kept per preview and four render at once in the pooled preview worker (lgse/strata#1075, lgse/strata#1222).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-11 | lgse/strata#1570 | fix | Hid HTML comments in release-notes Markdown through a separate parser profile; document previews are unchanged. |
| 2026-10-10 | lgse/strata#1559 | fix | Restored word, line, Shift-click, and Shift+key selection in virtualized document previews. |
| 2026-10-10 | lgse/strata#1539 | fix | Stopped rendered documents at the 1280 px content width, centered in wider previews. |
| 2026-09-19 | lgse/strata#1086 | feat | Rendered RTF in process and DOCX in the sandbox through the shared document view. |
| 2026-09-17 | lgse/strata#1075 | feat | Rendered relative Markdown images, Mermaid diagrams, and LaTeX equations in the sandbox. |
| 2026-09-17 | lgse/strata#729 | feat | Added sortable, resizable virtual tables for CSV, TSV, workbooks, and document tables. |
| 2026-09-16 | lgse/strata#187 | feat | Added native Rendered and Source previews for Markdown and an HTML subset. |

## Known gaps

- Workbooks preview only their first worksheet; multi-sheet navigation was deferred. lgse/strata#723
- PPTX, PPT, ODP, and DOC files have no rendered preview. lgse/strata#730, lgse/strata#244
- ODT images from `Pictures/` and the `Thumbnails/thumbnail.png` fallback for unreadable files are not shown. lgse/strata#1834, lgse/strata#1813
- Flat XML `.fodt` documents have no rendered preview. lgse/strata#1834
- Rendered documents break paragraphs over 2 KiB mid-word, which now shows in every long DOCX or ODT paragraph. lgse/strata#1861
- RTF emoji written as surrogate-pair `\uN` escapes are dropped. lgse/strata#1861
- Markdown cannot be edited or rendered with Pandoc or Quarto from the preview. lgse/strata#1127
- A touchpad flick can end early when newly measured rows change the scroll range or content origin. lgse/strata#1752
- A far jump in a rendered preview, such as a thumb drag, can show the previous content for one frame while mapped rows rebuild. lgse/strata#1752
- Large rendered previews have an initial-loading delay, where GTK/Pango layout and mixed-table construction remain significant costs. lgse/strata#1752
