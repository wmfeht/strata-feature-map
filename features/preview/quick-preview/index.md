---
title: Quick preview
status: shipped
origin: {issue: null, pr: lgse/strata#135}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: reviewed
code: [src/ui/preview/keyboard.rs]
tests: [tests/e2e/scenarios/test_quick_preview.py]
docs: [docs/keyboard-navigation.md]
related: [preview/preview-panel, integration/10xer-mode, browser/search, browser/selection]
---

## Summary

Opening, closing, and retargeting the file preview from the listing: Space, the Quick preview menu item, single-click previews, and selection following. It also covers default-keymap key ownership while a preview is open; 10xer preview keys belong to `integration/10xer-mode/preview-keys`. The drawer's layout and renderers belong to `preview/preview-panel`. Child: `preview/quick-preview/folder-peek` (the hover popover listing a folder's contents).

## Behavior

### Opening and closing

- With a supported file focused, Space opens its preview in the drawer and a second Space closes it, in Columns, Icons, and List. lgse/strata#416
- With Type to search on, Space on a focused file opens the preview instead of starting a search. lgse/strata#416
- Space on an unsupported file opens no preview. lgse/strata#416
- Space on a selected folder enters it in every view without opening or loading the preview. lgse/strata#1231
- The item menu shows Quick preview only for files the preview supports. lgse/strata#385 (unverified)
- With Single-click file previews on, the default, a single click on a supported file opens its preview without Space. lgse/strata#385 (unverified)

### Following the selection

- With the preview open, moving the selection to another supported file by keyboard or pointer shows that file, in every view. lgse/strata#614
- Shift+arrow extends the selection without collapsing it, and the preview shows the newly focused file. lgse/strata#614
- Focusing a folder hides the preview in Columns and List and shows "No preview for this selection" in Icons; focusing a supported file again resumes it. lgse/strata#614, lgse/strata#1405 (unverified)
- Deleting the previewed file, in Strata or by another process, retargets the preview to the newly focused supported file, or closes it when there is none. lgse/strata#135, lgse/strata#884
- Deleting a file other than the previewed one leaves the preview on its file. lgse/strata#135

### Filter results

- With a file result selected in the Ctrl+F filter, Space toggles its preview without changing the query, selection, or directory, in all three views and in file choosers. lgse/strata#585
- With no result selected, Space in the filter input types a space; Shift+Space types one even with a result selected. lgse/strata#585
- Space on a selected folder result navigates into the folder. lgse/strata#1231

### Keyboard ownership

- With the caret in preview text, Ctrl+A, Ctrl+C, Ctrl+V, Ctrl+X, Ctrl+D, and Delete act on the text, not on files. lgse/strata#670
- With a file focused in List or Columns and the preview open, Right moves focus into the preview. Its header shows an accent top border while it holds focus. lgse/strata#1343

## Design

[docs/keyboard-navigation.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/keyboard-navigation.md) carries the Space, filter, and preview key rules. Quick preview only decides the drawer's target; `preview/preview-panel` decides its size and contents.

- Requests are explicit (Space, the menu item, a single-click preview, `i`, entering with `l`) or automatic (Columns keyboard mirroring). Only automatic requests respect a dismissal (lgse/strata#1179, lgse/strata#1405).
- Following is debounced by 75 ms, so held arrow keys load only the file where the cursor lands (lgse/strata#1179).
- Native selection changes notify the preview without reapplying GTK selection or moving focus, so multi-selection survives (lgse/strata#614).
- Deletions are detected from model splices rather than focus events. A focus event would grab keyboard focus on background monitor changes (lgse/strata#884).
- Marquee updates run inside a tracked scope that the preview ignores (lgse/strata#1122).
- Space is reserved for quick preview and never starts type-to-search; focused text fields keep their own spaces (lgse/strata#416).
- The window key controller runs in the capture phase, so file shortcuts must yield to a focused text widget explicitly (lgse/strata#650).
- The focused pane owns the keys. Keys held by the drawer never change the listing's selection, location, or files (lgse/strata#1295).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-24 | lgse/strata#1231 | fix | Made Space enter a selected folder in every view without loading the preview. |
| 2026-09-12 | lgse/strata#884 | fix | Closed the preview when its file leaves the model, including deletions by other processes. |
| 2026-09-09 | lgse/strata#670 | fix | Let clipboard and Delete shortcuts reach focused preview text instead of acting on files. |
| 2026-09-08 | lgse/strata#614 | fix | Made an open preview follow native selection changes in List and Icons. |
| 2026-09-08 | lgse/strata#585 | fix | Let Space toggle the preview of a selected filter result without dismissing the filter. |
| 2026-09-06 | lgse/strata#416 | fix | Kept Space out of type-to-search so it reaches quick preview. |
| 2026-09-01 | lgse/strata#135 | fix | Closed or retargeted the preview after deleting the previewed file. |

## Known gaps

- Deleting a folder whose child column is open closes the preview instead of previewing the next sibling. lgse/strata#1497
- A floating Finder-style Quick Look popup, separate from the docked drawer, is proposed but unmerged. lgse/strata#999, lgse/strata#1183
