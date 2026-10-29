---
title: ODT and OTT document previews
status: shipped
origin: {issue: lgse/strata#1813, pr: lgse/strata#1834}
branch: null
reviewed_at: 86df474dc0e8352e0e2098637a017cc4c77a8c44
review: reviewed
code: [src/services/odt.rs]
tests: [src/services/odt/tests.rs, tests/fixtures/documents/report.odt]
related: [preview/preview-panel/sandbox, preview/preview-panel/find]
---

## Summary

Rendered previews of local OpenDocument text files (`.odt`) and templates (`.ott`), for checking a Writer document without an office suite. A sandboxed reader converts them to the DOCX HTML subset that the parent renders.

## Behavior

- Selecting a local `.odt` or `.ott` file shows its rendered document with no Source view, instead of "No preview for this selection". lgse/strata#1834
- An uppercase `REPORT.ODT` or `REPORT.OTT` renders the same way. lgse/strata#1834 (unverified)
- An ODT copied without an extension, which GIO types `application/vnd.oasis.opendocument.text`, also renders. lgse/strata#1834 (unverified)
- ODT renders `text:h` headings at their outline level, and paragraphs styled `Title`, `Subtitle`, or `Heading N` as headings. lgse/strata#1834
- An ODT outline level above 6 renders as a level-6 heading; `Title` renders at level 1 and `Subtitle` at level 2. lgse/strata#1834 (unverified)
- ODT paragraphs styled `Quotations`, `Quote`, or `Intense Quote` render as quotations. lgse/strata#1834
- Consecutive ODT `Preformatted Text` paragraphs render as one code block that keeps their indentation. lgse/strata#1834
- That code block drops bold, italic, and other inline formatting. lgse/strata#1834 (unverified)
- Outside `Preformatted Text`, runs of spaces, tabs, `text:s`, and line feeds collapse to one space; inside it, `text:s` and tabs keep their width. lgse/strata#1834 (unverified)
- Empty `Preformatted Text` paragraphs between code paragraphs become blank lines in the block; trailing ones are dropped. lgse/strata#1834 (unverified)
- ODT bold, italic, underline, strikethrough, and `Source Text` or `Teletype` monospace render from automatic styles, named styles, and their parents. lgse/strata#1834
- Emphasis set on a whole paragraph's style renders on plain and quotation paragraphs. lgse/strata#1834
- Paragraph-style emphasis is ignored on headings and preformatted text; table cells keep it. lgse/strata#1834 (unverified)
- In ODT, `http` and `https` links are clickable outside `Preformatted Text`. Links inside it, and links with other schemes, keep only their text. lgse/strata#1834 (unverified)
- ODT nested bulleted and numbered lists keep their nesting; lists deeper than eight levels continue at the eighth. lgse/strata#1834
- The first row of an ODT table's `table:table-header-rows` group becomes the column titles. Later header rows stay in the table as bold, sortable rows. A merged cell leaves an empty cell so the columns stay aligned. lgse/strata#1834 (unverified)
- An ODT table without a header-row group shows "Column 1", "Column 2", and onward as titles, where DOCX would use its first row. lgse/strata#1834 (unverified)
- An ODT table cell joins its paragraphs with a space, and a nested table's or list's text flattens into the cell. lgse/strata#1834
- An ODT table row over 256 cells (`TABLE_COLUMN_LIMIT`) truncates the document with the size-budget notice instead of falling back to Source. lgse/strata#1834 (unverified)
- In ODT, `text:line-break` renders as a line break, and `text:list-header` as a list item. lgse/strata#1834 (unverified)
- A heading inside an ODT table cell renders as cell text, not a heading; its style's emphasis still applies. lgse/strata#1834 (unverified)
- Only the outermost ODT table renders as a table; a nested table's rows never become table rows. lgse/strata#1834 (unverified)
- An ODT whose `content.xml` or `styles.xml` unpacks to over 64 MiB, or whose XML declares a DTD, fails with "The sandboxed preview renderer failed". lgse/strata#1834 (unverified)
- ODT images, drawings, text boxes, footnotes, comments, tracked deletions, headers, and footers are omitted. lgse/strata#1834
- Omitted ODT content shows no omission notice. lgse/strata#1834 (unverified)
- An ODT over the parser's size or event budget renders only its start. It shows "Document preview reached its size budget; open the file to see all content." lgse/strata#1834

## Design

- ODT has its own streaming `quick-xml` reader, which reads only `content.xml` and `styles.xml` in the sandbox under the 20 MiB limit DOCX uses (`ODT_BYTE_LIMIT`) (lgse/strata#1813, lgse/strata#1834).
- That reader emits the DOCX HTML subset, so the HTML parser, layout, and size notice are shared with DOCX (lgse/strata#1834).
- The reader returns the DOCX `RichTextData` from `src/services/docx.rs`, so the size-budget notice text comes from the parent's code (lgse/strata#1834).
- LibreOffice headless conversion was rejected as too slow and a heavy dependency; the embedded thumbnail alone shows only the first page (lgse/strata#1813).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |

## Known gaps

- ODT images from `Pictures/` and the `Thumbnails/thumbnail.png` fallback for unreadable files are not shown. lgse/strata#1834
- Flat XML `.fodt` documents have no rendered preview. lgse/strata#1834
