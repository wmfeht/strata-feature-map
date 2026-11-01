---
proposed: {page: new}
nodes: [browser/properties/size]
reason: 'The SIZE and CONTAINS rows of Properties, their incomplete-total warnings, and the multi-item Properties dialog are user-visible, and no page names the node. Its parent appears on the Keyboard navigation reference only for keys, and on the Preview sandbox page only for media metadata; no section covers measuring folders. Proposed as a "Properties" reference page, or a section a person adds to an existing page.'
release: v1.1.1
---

## Folder size and contents

Properties for a folder shows **SIZE** as a running total, with a spinner at the
row's right edge, until the measurement ends. **CONTAINS** shows recursive counts,
such as "4 files, 1 folder". An empty folder shows "0 B" and "0 files,
0 folders". Properties for Trash (`trash:///`) measures it the same way. A file's
Properties shows its own size, with no spinner and no CONTAINS row. Closing the
dialog stops the measurement.

- SIZE counts hidden files and files inside hidden folders. CONTAINS leaves out
  hidden entries and everything below a hidden folder, whatever the browser's
  hidden-files toggle says.
- Symlinks inside the folder are not followed, add 0 bytes, and count as files.
- Entries a remote location reports without size or hidden attributes count as
  visible, not symlinks, and 0 bytes.

### Incomplete totals

A total that could not be completed is a lower bound: SIZE and each count gain a
"≥" prefix, such as "≥ 15 B" and "≥ 4 files, ≥ 1 folder", and a warning icon
appears. Its accessible label begins "Totals are incomplete." and gives the
reasons:

| Reason | Text |
| --- | --- |
| A subfolder or entry could not be read | "Some folders or entries couldn't be read." |
| The measurement ran for five minutes | "The five-minute calculation limit was reached." |
| Folders nested deeper than 64 levels | "Some folders exceeded the 64-level nesting limit." |

When the folder itself cannot be read, SIZE and CONTAINS read "Unavailable" and
the warning reads "Folder contents couldn't be read." A file operation on the
measured folder, or on an item inside it, stops the measurement and leaves an
incomplete total.

## Several items

With two or more items selected, **Alt+Enter** or **Properties** in the item menu
opens an "N items selected" dialog that shows only SIZE and CONTAINS. SIZE
adds the selected files' sizes to the contents of the selected folders. CONTAINS
counts the selected files plus the files and folders inside selected folders, not
the selected folders themselves. An unreadable folder in the selection makes the
totals incomplete, as above. With one item selected, Properties shows the full
dialog.
