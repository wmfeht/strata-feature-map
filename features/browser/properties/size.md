---
title: Folder and selection size
status: shipped
origin: {issue: lgse/strata#556, pr: lgse/strata#558}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [src/adapters/directory_summary.rs]
tests: [src/adapters/directory_summary/**, tests/e2e/scenarios/test_properties_size.py]
related: [operations/trash/empty]
---

## Summary

The SIZE and CONTAINS rows of Properties: a recursive, bounded, cancellable measurement of a folder, of Trash, or of a multi-item selection. The same walker measures Trash for Empty Trash.

## Behavior

### Single folder

- Folder Properties shows SIZE as a running total with a spinner at the row's right edge, updated at most every 150 ms; the final total appears at once. lgse/strata#558
- SIZE includes bytes of hidden files and of files inside hidden folders. lgse/strata#558, lgse/strata#886
- Symlinks inside the folder are not followed, add 0 bytes, and count as files. lgse/strata#558, lgse/strata#886
- CONTAINS shows recursive counts such as "4 files, 1 folder", excluding hidden entries and everything below a hidden folder. lgse/strata#886
- CONTAINS ignores the browser's show-hidden-files toggle. lgse/strata#886
- An empty folder shows "0 B" and "0 files, 0 folders", and the spinner disappears. lgse/strata#558, lgse/strata#886
- A file's Properties shows its own size, with no spinner and no CONTAINS row. lgse/strata#558
- Properties for `trash:///` measures Trash recursively and shows SIZE and CONTAINS as for a folder. lgse/strata#556, lgse/strata#558
- Closing the dialog stops the measurement. lgse/strata#558

### Incomplete measurements

- When a subfolder cannot be read, SIZE and each count gain a "≥" prefix, such as "≥ 15 B" and "≥ 4 files, ≥ 1 folder". lgse/strata#558, lgse/strata#886
- An incomplete total shows a warning icon whose accessible label begins "Totals are incomplete." and lists "Some folders or entries couldn't be read." lgse/strata#886
- Reaching the five-minute limit adds "The five-minute calculation limit was reached." to the warning. lgse/strata#558 (unverified)
- Folders nested deeper than 64 levels are not entered and add "Some folders exceeded the 64-level nesting limit." to the warning. lgse/strata#558 (unverified)
- When the folder itself cannot be read, SIZE and CONTAINS read "Unavailable" and the warning reads "Folder contents couldn't be read." lgse/strata#558, lgse/strata#886

### Multi-item selection

- With two or more items selected, Alt+Enter or Properties in the multi-item context menu opens an "N items selected" dialog with only SIZE and CONTAINS. lgse/strata#1130
- Selection SIZE adds the selected files' sizes to the recursive contents of the selected folders. lgse/strata#1130
- Selection CONTAINS counts the selected files plus the files and folders inside selected folders, not the selected folders themselves. lgse/strata#1130
- An unreadable folder in the selection gives the selection totals a "≥" prefix and the incomplete warning. lgse/strata#1130
- Opening Properties with one item selected shows the full single-item dialog. lgse/strata#1130

## Design

[src/adapters/directory_summary.rs](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/src/adapters/directory_summary.rs) is a GIO walker with no widget dependencies, moved out of Trash so folders and Trash share it (lgse/strata#558).

- Budgets: 64 levels and 300 seconds per walk. A truncated walk is a lower bound, marked "≥", never shown as exact (lgse/strata#556, lgse/strata#558).
- An unreadable or vanished branch marks the result incomplete but does not stop its siblings. Only an unreadable root fails the walk (lgse/strata#558).
- The SIZE value uses tabular digits in a fixed-width field, and progress is throttled to 150 ms, so the row does not jitter while counting (lgse/strata#556 comments).
- Counts follow a fixed non-hidden policy rather than the browser toggle. Hidden bytes still count because they occupy disk (lgse/strata#886). The issue proposed immediate children only; recursive counts were chosen instead (lgse/strata#604, lgse/strata#886).
- The selection dialog reuses the walker per selected folder and keeps permissions, rename, and media single-item (lgse/strata#1099).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-22 | lgse/strata#1130 | feat | Added a Properties summary for multi-item selections with combined size and nested counts. |
| 2026-09-12 | lgse/strata#886 | feat | Added a CONTAINS row with recursive visible file and folder counts. |
| 2026-09-07 | lgse/strata#558 | fix | Calculated folder sizes recursively with a running total, sharing the bounded walker with Trash. |

## Known gaps

- Subfolders are measured one at a time, and each selected folder gets its own 300-second budget; bounded concurrency was closed as not planned. lgse/strata#1324
