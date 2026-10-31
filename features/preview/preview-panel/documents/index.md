---
title: Rendered document previews
status: shipped
origin: {issue: lgse/strata#89, pr: lgse/strata#187}
branch: null
reviewed_at: 965bd7ec74400734dbd0a5311ceefa05bea8dd63
review: draft
code: [src/services/document.rs, src/services/document_media.rs, src/services/docx.rs, src/services/docx/namespaces.rs, src/services/rtf.rs, src/services/table.rs, src/ui/document_view.rs, src/ui/document_media.rs, src/ui/virtual_preview.rs, src/ui/virtual_preview/selection.rs, src/ui/virtual_preview/line_numbers.rs, src/ui/table_view.rs, src/ui/table_view/selection.rs, src/ui/table_view/model.rs, src/sandbox_helper/document_media.rs, data/math-renderer.js, packaging/math-renderer]
tests: [src/services/document/tests.rs, src/services/document_media/tests.rs, src/services/docx/tests.rs, src/services/docx/namespaces/tests.rs, src/services/rtf/tests.rs, src/services/table/tests.rs, src/ui/document_media/tests.rs, src/ui/virtual_preview/tests.rs, src/ui/virtual_preview/selection/tests.rs, src/ui/table_view/tests.rs, src/ui/table_view/selection/tests.rs, src/sandbox_helper/document_media/tests.rs, tests/fixtures/spreadsheets, tests/fixtures/documents/report.docx, tests/fixtures/documents/README.md, tests/qa/scenarios/quick_preview/markdown-equations-keep-prose.jsonl, tests/qa/scenarios/quick_preview/markdown-preview-renders-media.jsonl, tests/qa/scenarios/quick_preview/rendered-document-word-selection.jsonl, tests/qa/scenarios/quick_preview/sandboxed-office-shared-preview.jsonl, tests/qa/scenarios/quick_preview/table-preview-keeps-secondary-sorts.jsonl]
docs: [site/src/reference/document-previews.md, docs/document-previews.md]
related: [preview/preview-panel/sandbox, preview/preview-panel/find, settings/preferences, settings/themes]
---

## Summary

Native GTK rendering of local Markdown, an HTML subset, RTF, CSV, TSV, XLS, XLSX, ODS, DOCX, ODT, and OTT files in the preview panel. Text formats switch between Rendered and Source; nothing uses a web engine or runs document scripts. Children: `preview/preview-panel/documents/odt` (OpenDocument text and templates) and `preview/preview-panel/documents/scrollbar` (the document-position scrollbar).

## Behavior

### Rendered and Source

- Selecting a local Markdown, HTML, RTF, CSV, or TSV file with **Render documents by default** on shows the rendered document; with it off, the source. lgse/strata#187, lgse/strata#729, lgse/strata#1086
- **View source** and **View rendered** in the preview header switch the current document without changing the saved preference. lgse/strata#187
- Remote Markdown, HTML, RTF, CSV, and TSV files preview as source only. lgse/strata#187, lgse/strata#729, lgse/strata#1086 (unverified)
- A malformed, truncated, timed-out, or limit-exceeding document opens in Source, hides the view switch, and shows the reason above the source. lgse/strata#187
- Documents over 1 MiB, 20,000 parser events, nesting depth 32, 4 MiB of markup, or 500 ms of parsing fall back to Source. lgse/strata#187
- A Markdown or HTML table row over 256 columns also falls back to Source. lgse/strata#729
- Dragging across headings, paragraphs, lists, code, and tables, then Ctrl+C, copies the selected text with original line breaks. lgse/strata#187
- In rendered or large source documents, double-click selects a word and triple-click its logical line, a whole paragraph in prose; Ctrl+C copies exactly that text. lgse/strata#1559, lgse/strata#1557
- A click, then a Shift-click farther along, selects from the first click to the second. lgse/strata#1559, lgse/strata#1557
- With focus in a rendered or large source document, Shift+Left/Right, Shift+Up/Down, Shift+Home/End, and Ctrl+Shift+Left/Right extend the selection by character, line, line edge, or word. lgse/strata#1559, lgse/strata#1557
- Ctrl+Home and Ctrl+End move the caret to the start and end of the loaded document. lgse/strata#1559
- In the default key map, Home and End still move the caret to the line's start and end after `first_item` or `last_item` is rebound. lgse/strata#1885
- With focus in a rendered or large source document, Ctrl+A selects the whole loaded document. lgse/strata#187, lgse/strata#1576 (unverified)
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
- A rendered line over 2 KiB containing whitespace, in a paragraph, heading, list item, quote, or code block, breaks into rows of at most 2 KiB. lgse/strata#1901 (unverified)
- Each such row ends just after whitespace when its window holds any. lgse/strata#1901
- A row ends just after the last ASCII space in its window; without one, after the last other whitespace, such as a tab. lgse/strata#1901 (unverified)
- CJK text whose only separators are U+3000 ideographic spaces breaks just after a U+3000. lgse/strata#1901
- A row whose window holds no whitespace ends at the window's end. lgse/strata#1901
- A whitespace-free token over 2 KiB breaks on character boundaries into rows of at most 2 KiB. lgse/strata#1901, lgse/strata#187
- Once under 4 KiB of a line remains, each window is half the remainder, so the last two rows split it about evenly. lgse/strata#187 (unverified)
- In a rendered line over 2 KiB that holds whitespace, a word under 1,000 bytes is never split across rows. lgse/strata#1901 (unverified)
- Copying a line broken this way returns its plain text unchanged, including text inside bold spans. lgse/strata#1901
- Fenced code with a known language hint renders with theme syntax highlighting. lgse/strata#187
- A fenced block split across several rows, over about 32 KiB or holding a line over 2 KiB, renders without highlighting. lgse/strata#187 (unverified)
- Every rendered code block shows a **Copy code** button that copies the whole block. lgse/strata#187
- After a click, **Copy code** shows a check icon and reads "Code copied" for 2 s, then "Copy code" again. lgse/strata#187 (unverified)

### Scrolling

- After smooth scrolling, a click, drag selection, or link hover acts on the row under the pointer. lgse/strata#1752 (unverified)

### HTML and links

- HTML scripts, styles, forms, frames, objects, images, and event handlers are omitted, with the notice "Unsupported or active HTML content was omitted." lgse/strata#187
- `u` and `ins` render as underline without the omission notice. lgse/strata#1086
- Clicking an `http` or `https` link opens it externally; other schemes stay inert. lgse/strata#187

### Tables and workbooks

- CSV and TSV files render as a table whose first row is the column titles, with quoted multiline fields and ragged rows parsed. lgse/strata#729
- XLS, XLSX, and ODS files show their first worksheet as a table with no Source view; formulas are not recalculated and macros never run. lgse/strata#729
- Tables open sorted ascending by the first column; clicking a column title toggles ascending and descending. lgse/strata#729
- Clicking a second column title sorts by it; rows with equal values keep the earlier sort columns' order and direction, most recent first, then source order. lgse/strata#1946
- Clicking the primary title again reverses its value groups. Rows within a group, such as `a` and `A`, keep their secondary and source order. lgse/strata#1946
- After a Markdown, HTML, DOCX, or ODT table sorted by two columns scrolls away and back, clicking the primary title sorts ties in source order. lgse/strata#1946 (unverified)
- While an 18,000-row, 4-column XLSX preview loads after a single click, the window keeps repainting and accepting clicks. lgse/strata#1946, lgse/strata#1939 (unverified)
- Ascending sort puts numbers first, then case-insensitive text, then empty cells; descending reverses that order. Sorting never changes the file. lgse/strata#729 (unverified)
- Changing the sort clears a selected cell range and scrolls the table to the top. lgse/strata#729 (unverified)
- A table cell over 512 bytes shows shortened with "…"; copying the table keeps its full text. lgse/strata#187 (unverified)
- Every column, including the last, resizes by dragging its divider. lgse/strata#729
- Tables over 200 rows or 512 cells render in full. lgse/strata#729
- CSV, TSV, and workbook output stops at 100,000 values, 4 MiB of cell text, or 256 columns. lgse/strata#729
- A limited table shows "Table preview reached its text, column, or value budget; open the file to see all data." lgse/strata#729
- Dragging across cells and pressing Ctrl+C copies the range as tab-separated rows in displayed sort order. lgse/strata#729
- Closing the preview during a table cell drag ends the drag and its autoscroll. lgse/strata#1752 (unverified)
- With focus on the table, Ctrl+C copies every loaded row in the current sort order, including offscreen rows. lgse/strata#729
- With focus on the table, Ctrl+Shift+C, Ctrl+Alt+C, and Ctrl+Super+C copy nothing. lgse/strata#1576
- With a cell range selected, Ctrl+A or Ctrl+Shift+A clears the range; Ctrl+Alt+A leaves it. lgse/strata#729, lgse/strata#1576
- With a cell range selected, Escape, an arrow key, Home, or End also clears it. lgse/strata#729 (unverified)
- With a non-Latin layout such as Russian active, Ctrl+A in a focused table cell selects that cell's text. lgse/strata#1576
- With a non-Latin layout active and no cell range selected, Ctrl+C in a focused table cell copies its own selection, not the whole table. lgse/strata#1576

### Images, diagrams, and equations

- Markdown images with relative paths render PNG, JPEG, GIF, WebP, BMP, and SVG files inside the document's folder, including percent-encoded names. lgse/strata#1075
- Absolute, `file:`, data, and remote image URLs are not loaded, and the notice "Remote and absolute image URLs are not loaded. Use images inside the document's folder." appears. lgse/strata#1075
- A missing or undecodable image keeps its alt text and the rest of the document renders. lgse/strata#1075
- A Markdown image inside a table cell is never loaded and shows as "[Image: alt]". lgse/strata#1075 (unverified)
- Images over 8 MiB, Mermaid blocks over 16 KiB or 256 lines, and equations over 4 KiB are not rendered. lgse/strata#1075 (unverified)
- Fenced `mermaid` blocks render as diagrams in theme colors, with **Copy diagram source**; invalid syntax keeps the source with a fallback notice. lgse/strata#1075
- `$...$`, `$$...$$`, and fenced `latex` or `math` blocks render as equations; display equations offer **Copy equation source**. lgse/strata#1075
- Copying a selection containing inline math keeps its original `$` delimiters. lgse/strata#1075
- Changing the theme while a diagram or equation is open recolors it. lgse/strata#1075

### RTF and DOCX

- RTF renders paragraphs, bold, italic, underline, strikethrough, Windows-1252 `\'hh` escapes, and `\uN` escapes, and keeps its Source view. lgse/strata#1086
- RTF `{\rtf1\ansi\uc1 A [\u-10179?\u-8704?] B}` renders `A [😀] B`; a surrogate pair takes the style of its high unit. lgse/strata#1901
- An unpaired RTF surrogate, including a high unit followed by text, `\line`, `\par`, or the document end, renders as U+FFFD instead of being dropped. lgse/strata#1901
- An RTF `\uN` value outside -32768 to 65535, such as `\u65536` or `\u-32769`, renders as U+FFFD. lgse/strata#1901
- An escaped newline inside an ignored `{\*…}` destination does not end the open RTF paragraph. lgse/strata#1901
- DOCX renders headings, `Title`, `Subtitle`, quotes, inline formatting, nested bulleted and numbered lists, and tables with the first row as sortable titles. lgse/strata#1086
- DOCX has no Source view; images, hyperlink targets, headers, footers, footnotes, and comments are omitted. lgse/strata#1086
- DOCX files with alternate XML namespace prefixes or default namespaces keep their Word content. lgse/strata#1086

## Design

[docs/document-previews.md](https://github.com/lgse/strata/blob/2218357c2e91c0c3e6cd02638356f7a91c08bcae/docs/document-previews.md) is the maintained contract for formats, limits, tables, and the trust boundary.

- HTML must not turn the preview into a browser. A native renderer for a documented subset was chosen over Chromium, Electron, WebKitGTK, or external converters (lgse/strata#89).
- Markdown, HTML, RTF, CSV, and TSV are parsed in-process by pure-Rust parsers off the GTK thread. They see only the bounded source string and emit escaped Pango markup (lgse/strata#187).
- Calamine and `docx-rs` can allocate whole sheets or decompress every part, so workbooks and DOCX run in the preview sandbox under a 20 MiB input limit. Only validated JSON returns; DOCX HTML is reparsed by the same bounded HTML parser (lgse/strata#729, lgse/strata#1086).
- Large source and rendered views use recycled, virtualized rows. Selection is kept in document coordinates and copy reads the model (lgse/strata#187). Rendered rows build their text, tables, and media only once mapped, and visited widgets may stay in GTK's bounded recycling pool. Source rows bind eagerly so thumb seeking uses measured heights (lgse/strata#1752).
- Unwrapped source rows already widened to their text, but rendered rows only got a height and clipped at the pane edge. Unwrapped rendered rows now widen to their longest line (lgse/strata#1610, lgse/strata#1612).
- Wrap toggles remeasure rows after GTK has re-laid them out, because measuring right after `set_wrap_mode` returned the previous mode's height (lgse/strata#1612).
- Virtual rows cannot take native input, so word, line, and Shift selection is computed in the document model. The selector had ignored click count and modifiers (lgse/strata#1557).
- One table renderer serves CSV, TSV, workbooks, Markdown, HTML, DOCX, and ODT tables, replacing the 200-row capped grid (lgse/strata#723, lgse/strata#729, lgse/strata#1834).
- GTK's `SortListModel` and `CustomSorter` sorted on the main thread through FFI, with GObject type checks and `RefCell` borrows per comparison. Sorting 25,000 rows took about 4.5 s (lgse/strata#1939, lgse/strata#1946).
- Tables now sort a Rust index permutation that display, copy, and selection share. Ties follow GTK's `GtkColumnViewSorter`: secondary columns, then source order (lgse/strata#1946).
- Sort keys are built per column on its first sort. A column with cells in at least half the rows is stored densely, otherwise as row and key pairs (lgse/strata#1946).
- A table-local list model creates row objects on first access and caches them by source row without eviction. A re-sort replaces no row objects (lgse/strata#1946).
- A direction-only change reverses primary-key groups in linear time instead of re-sorting (lgse/strata#1946).
- Images are opened beneath the document directory, copied to private files, and decoded in the sandbox. Mermaid uses `mermaid-svg`; equations use pinned MathJax in QuickJS with no host bindings, as a string argument (lgse/strata#1075).
- `mermaid-rs-renderer` was replaced by `mermaid-svg` to drop the unmaintained `ttf-parser` (lgse/strata#1074).
- RTF uses a hand-written converter, because `rtf-parser` 0.4.3 dropped `\par`, mis-decoded `\'93`, and corrupted `\uN` fallbacks (lgse/strata#1086).
- Long paragraphs keep the 2 KiB row bound and the 1 MiB input bound; whitespace is only preferred. A line is checked for whitespace once, so unbroken tokens are not rescanned per row (lgse/strata#1901, lgse/strata#1861).
- RTF `\uN` values are UTF-16 units. Pairs go through the standard UTF-16 decoder, and malformed units are replaced rather than lost (lgse/strata#1901, lgse/strata#1861).
- At most 16 media items are kept per preview and four render at once in the pooled preview worker (lgse/strata#1075, lgse/strata#1222).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-30 | lgse/strata#1946 | fix | Sorted tables in Rust over a lazy row model, removing a 5 s freeze on large spreadsheets, and kept earlier columns as tie-breakers. |
| 2026-10-11 | lgse/strata#1570 | fix | Hid HTML comments in release-notes Markdown through a separate parser profile; document previews are unchanged. |
| 2026-10-10 | lgse/strata#1559 | fix | Restored word, line, Shift-click, and Shift+key selection in virtualized document previews. |
| 2026-10-10 | lgse/strata#1539 | fix | Stopped rendered documents at the 1280 px content width, centered in wider previews. |
| 2026-09-19 | lgse/strata#1086 | feat | Rendered RTF in process and DOCX in the sandbox through the shared document view. |
| 2026-09-17 | lgse/strata#1075 | feat | Rendered relative Markdown images, Mermaid diagrams, and LaTeX equations in the sandbox. |
| 2026-09-17 | lgse/strata#729 | feat | Added sortable, resizable virtual tables for CSV, TSV, workbooks, and document tables. |
| 2026-09-16 | lgse/strata#187 | feat | Added native Rendered and Source previews for Markdown and an HTML subset. |

## Known gaps

- Workbooks preview only their first worksheet. lgse/strata#729
- A far jump in a rendered preview, such as a thumb drag, can show the previous content for one frame while mapped rows rebuild. lgse/strata#1752
- Large rendered previews have an initial-loading delay, where GTK/Pango layout and mixed-table construction remain significant costs. lgse/strata#1752
- A document-embedded table rebuilt after scrolling restores only its primary sort column, so the next header click drops secondary tie-breaking. lgse/strata#1946
