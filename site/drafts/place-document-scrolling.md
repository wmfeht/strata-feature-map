---
proposed: {page: reference/document-previews.md, section: Text selection and find}
nodes: [preview/preview-panel/pdf, preview/preview-panel/documents/scrollbar]
reason: 'Selecting and copying PDF text is user-visible and no section describes it; "Text selection and find" covers selection in rendered documents, so it belongs beside that. The document scrollbar is already described under "Limits and fallback". Add both nodes to the page''s nodes in site/pagemap.yaml and merge the PDF text below as a `###` subsection.'
release: v1.1.1
---

### Selecting text in a PDF

Drag across PDF text to highlight it in the theme accent, then press **Ctrl+C** to
copy it in page order with the document's line breaks. Double-click selects a
word and triple-click a line; dragging after either extends by words or lines.
**Shift+click** extends the selection, across pages. With focus in the PDF,
**Ctrl+A** selects the text of every loaded page. With nothing selected,
**Ctrl+C** leaves the clipboard unchanged.

Dragging on a page margin, or on a page with no text layer such as a scan, pans
the view instead. Selected text on a page scrolled out of view stays copyable
until the selection changes.
