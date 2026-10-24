---
title: Preview panel layout
status: shipped
origin: {issue: lgse/strata#885, pr: lgse/strata#888}
branch: null
reviewed_at: 2218357c2e91c0c3e6cd02638356f7a91c08bcae
review: draft
code: [src/ui/preview/layout.rs, src/ui/preview/session.rs, src/ui/preview/media_layout.rs, src/ui/preview/player_layout.rs, src/ui/browser/preview.rs]
tests: [tests/qa/scenarios/preview_session, tests/qa/scenarios/quick_preview, src/ui/preview/tests.rs]
docs: [docs/preview-panel-layout.md]
related: [preview/quick-preview, browser/view-modes, browser/sidebar]
---

## Summary

How the preview panel shares the window with the file views: its width, the reserved slot in Columns, the right pane shared with child columns, and narrow-window behavior. Applies to Columns, Icons, List, and the file chooser.

## Behavior

### Width

- With a manual width, resizing the window keeps the preview's width; the file views absorb the difference. lgse/strata#888, lgse/strata#1502
- In Columns, the automatic width fills the space right of the focused column, with a 300 px minimum (one standard column). lgse/strata#888, lgse/strata#1539
- That minimum yields to keep the focused column fully visible. lgse/strata#888
- In Icons and List, the automatic width is 90% of half the content width, between 240 px and 3000 px. lgse/strata#888, lgse/strata#1181
- Dragging the divider, or moving it with the keyboard, sets a manual width of at least 300 px that survives closing, reopening, and folder changes, and is forgotten when the window closes. lgse/strata#888
- In Columns, a dragged width becomes the session minimum: the preview still fills wider free space and yields to columns only down to that width. lgse/strata#1539
- In Icons and List, a dragged width is the preview's width. lgse/strata#1539
- Narrowing a filled preview, by pointer drag or F8 and the arrow keys, lowers the Columns session minimum and leaves the panel in place. lgse/strata#1539
- Pointer-dragging the divider shows a dashed outline from the pointer to the right edge, captioned "Preview panel minimum width", which fades on release. lgse/strata#1539
- Moving the divider with the keyboard shows no outline. lgse/strata#1539 (unverified)
- In Columns with an automatic width, widening or narrowing the window resizes the preview or empty slot in one frame, without the boundary jumping back and forth. lgse/strata#1502
- Images, GIFs, and video are centered within 1280 px and enlarged at most 2× their native size. lgse/strata#888
- In a preview wider than 1280 px, PDF pages and wrapped rendered Markdown, HTML, and RTF stop at 1280 px, centered; Ctrl+wheel PDF zoom scales from that width. lgse/strata#1539, lgse/strata#1612
- In a preview wider than 1280 px, DOCX, ODT, and OTT text stops at 1280 px, centered, whatever the wrap setting. lgse/strata#1834 (unverified)
- With word wrap off, every row of a rendered Markdown, HTML, or RTF document starts at the left edge. This holds in previews wider than 1280 px too. lgse/strata#1612, lgse/strata#1834
- XLS, XLSX, and ODS previews start at the left edge instead of centering at 1280 px. lgse/strata#1612, lgse/strata#1834 (unverified)
- Source views and standalone tables keep the full preview width. lgse/strata#1539
- The preview header uses 16 px icons and compact buttons, and its close button lines up with the header bar's close button. lgse/strata#829

### Divider and resize edge

- At the column–preview boundary, the 6 px inside the preview's left edge move the divider. lgse/strata#1539
- At that boundary, the column's last 6 px, except the 1 px line, resize the column. lgse/strata#1539
- Hovering the grip or divider line lights the line and tints the grip; after 400 ms, "Preview panel minimum width" appears. lgse/strata#1539
- Crossing between the divider line and the grip keeps the caption; pressing hides it in favor of the outline. lgse/strata#1539
- With the preview hidden, such as with a folder selected, the grip and the divider's resize cursor are absent and only the column resizes. lgse/strata#1539

### Drawer motion

- In Icons, List, and Columns with **Appearance → Preview panel** off, the drawer slides open and closed over 260 ms. lgse/strata#1539
- A reserved Columns slot never slides. lgse/strata#1539
- Closing the preview mid-slide returns keyboard focus to the files at once; only content teardown waits for the slide. lgse/strata#1539
- Reopening the preview during its slide-out, such as Space twice quickly in List, turns the drawer back from its current position. lgse/strata#1539

### Reserved slot

- Columns reserves the preview slot from startup, so opening or closing a preview never moves the columns. lgse/strata#1382
- Space, **i**, Esc, and the close button dismiss the preview content and keep the slot; **Appearance → Preview panel** off releases it. lgse/strata#1382
- The reserved slot alone loads no preview and is not saved as a preference. lgse/strata#1382
- In Icons, the slot stays reserved while the preview is enabled; folders and empty selections show "No preview for this selection", and the grid does not reflow. lgse/strata#888
- In List, selecting a folder or a file with no preview hides the drawer. lgse/strata#888
- When Icons or List starts with the preview disabled, no empty preview area is shown. lgse/strata#1382
- When the preview space is released while columns overflow, the columns slide into the freed space and the scrollbar covers only real columns. lgse/strata#1078

### Right pane in Columns

- Keyboard focus on a folder hands the right pane to its child column with no placeholder, and the focused column does not move. lgse/strata#1405
- Keyboard focus on a previewable file closes the child column and the preview fills the same space, starting at the focused column's right edge. lgse/strata#1405
- Files with no preview and empty selections keep the "No preview for this selection" placeholder in the slot. lgse/strata#1405
- Previewing a file in a parent column with the pointer closes the deeper columns first. lgse/strata#1405
- A preview closed with Space, **i**, Esc, the close button, or **Appearance → Preview panel** stays closed while keyboard focus moves onto other files, until opened explicitly. lgse/strata#1405
- A trailing child column wider than the slot is clipped at the right edge instead of scrolling the focused column. lgse/strata#1405
- Clicking the visible strip of a clipped column reveals it without activating its rows or toolbar actions. lgse/strata#888, lgse/strata#1405

### Narrow windows

- When less than 240 px would remain beside the focused column, the preview content hides, media pauses, and loading is deferred. lgse/strata#888, lgse/strata#1405
- Widening the window again restores the same file at the previous manual width. lgse/strata#888
- In Columns, the reserved slot shrinks down to zero instead of disappearing, so the columns keep their offset. lgse/strata#1405
- While a preview is present, an expanded sidebar rails once when the window is narrower than a sum. The sum is the full sidebar width, the focused column, and the preview width. The column counts at most 300 px in Columns and 300 px in Icons and List; the preview counts its manual width, at least 240 px. lgse/strata#1181, lgse/strata#1606 (unverified)
- An automatic rail from that rule releases only when the window is 24 px wider than that sum. lgse/strata#1181, lgse/strata#1606
- In Columns, the empty reserved slot, and in Icons the empty placeholder, also apply that rule. lgse/strata#888, lgse/strata#1382, lgse/strata#1606
- With no preview, placeholder, or reserved slot, an expanded sidebar rails once when the window narrows to at most the preferred sidebar width plus one standard column. lgse/strata#1606
- In that state, widening the window past that width releases an automatic rail. lgse/strata#1606
- An automatic rail leaves `sidebar_compact` false in `settings.toml`. lgse/strata#1606
- With the sidebar on an automatic rail in Columns three levels deep, clicking Home in the rail does not expand the sidebar and snap back. lgse/strata#1602, lgse/strata#1606
- The sidebar returns to the user's chosen width once the content has room; a width pinned by the narrow window is never saved. lgse/strata#1181, lgse/strata#1405
- Dragging a column's resize edge across the threshold does not toggle the sidebar rail; it settles at most once on release. lgse/strata#1305
- Previewing a file for the first time in a 700 px window rails the sidebar and loads the title, metadata, and content at once. lgse/strata#1396
- At 4× display scaling the preview stays in place without alternating between layouts. lgse/strata#1149

## Design

[docs/preview-panel-layout.md](https://github.com/lgse/strata/blob/442d325be108ff95391f0fe76cbd89da8db9e129/docs/preview-panel-layout.md) is the contract. Every rule there names its owning test, and geometry is verified by manual captures rather than layout assertions (lgse/strata#1404).

- Finder's column view is the reference. Wide windows give the preview the free space; a fixed width wasted it, and shrinking columns hid filenames (lgse/strata#885).
- Manual width is window- and session-local, not a saved setting; persistent or per-folder sizing was left for later (lgse/strata#885).
- While the drawer is enabled or reserving space, `sync_split` ticks for 60 frames after a layout pass or an input event in the split (lgse/strata#1671, lgse/strata#1677). It no longer keeps the frame clock running in an idle window. It owns the slot's visibility, minimum width, and divider position; besides the user's drag, only the open animation and hiding the panel move it.
- The Columns slot is separate from preview content, because dismissing a preview shifted the deep column chain under the pointer (lgse/strata#1381, lgse/strata#1382).
- The child column used to sit inside the scroller beside the slot, so each folder-to-file step bounced the focused column by one column width. The slot now lends trailing columns its width, and the scroll offset never changes (lgse/strata#1404, lgse/strata#1405).
- Priority is focused column, then preview, then peek. A reserved peek budget depended on viewport size and neighbor count, so it toggled with the panel and moved columns by 48 px; it was removed (lgse/strata#1405).
- Unwrapped rendered rows start at the left edge, because centering each row in the widened list scattered shorter rows far to the right (lgse/strata#1612).
- Columns keeps its reservation: without one, opening a preview moved the columns 51 px in a 1200 px window (lgse/strata#1539).
- Resize edges show captions rather than tooltips, because tooltips are allowed only on icon-only buttons (lgse/strata#1539).
- The hide threshold is 240 px, independent of the 300 px column width. A 300 px floor hid the preview in 780 px windows at 1.6× scaling (lgse/strata#1145).
- One fit rule, `PreviewDrawer::sidebar_fit`, serves the header toggle and the preview tick, which the chooser shares. Four callers with two thresholds made the sidebar expand, then snap back to the rail (lgse/strata#1602, lgse/strata#1606).
- The automatic rail is edge-triggered: only a change in fit compacts or releases it. A chosen rail holds at any width; a chosen full sidebar holds until the fit next changes (lgse/strata#1602, lgse/strata#1606).
- The preview rule measures only the split's parent width, not the content paned. The slot re-budgets a frame after the sidebar shows, and a one-frame shortage would latch the rail (lgse/strata#1606).
- An unallocated window counts as unknown, not short, so a hidden sidebar in a second window does not rail before it is first shown (lgse/strata#1606).
- Fit decisions read the sidebar's own `visible` property. Ancestor visibility dropped the sidebar from the next calculation and caused a flicker loop at 4× (lgse/strata#1145).
- The minimum width went from 280 to 560 px at the owner's request (lgse/strata#828), then to two standard columns in Columns (lgse/strata#888). lgse/strata#1181 lowered the Icons and List minimum to 240 px. lgse/strata#1539 lowered the Columns minimum to one column.

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-15 | lgse/strata#1677 | perf | Ran the split sync only for about a second after a layout pass or input, so an idle window stops drawing frames. |
| 2026-10-11 | lgse/strata#1570 | fix | Published the visible browser area as the Miller column width limit and narrowed oversized open columns once. |
| 2026-10-10 | lgse/strata#1559 | fix | Cleared the preview find query when the preview target is cleared. |
| 2026-10-10 | lgse/strata#1539 | fix | Lowered the Columns minimum to 300 px, kept dragged widths as a minimum, split the shared resize edge, and capped documents at 1280 px. |
| 2026-10-06 | lgse/strata#1502 | fix | Let the free-space preview absorb window resizing in one frame to stop divider jitter. |
| 2026-10-03 | lgse/strata#1405 | fix | Shared the Columns right pane between child columns and the preview so the focused column stays put. |
| 2026-10-03 | lgse/strata#1396 | fix | Loaded the deferred file when the drawer first opens in a narrow split. |
| 2026-10-02 | lgse/strata#1382 | fix | Reserved the Columns preview slot from startup so toggling a preview never moves columns. |
| 2026-09-27 | lgse/strata#1305 | fix | Froze the sidebar rail during column resize drags. |
| 2026-09-23 | lgse/strata#1181 | fix | Kept the file list visible in narrow windows by collapsing the sidebar to a rail instead of a full-window preview. |
| 2026-09-21 | lgse/strata#1173 | fix | Restored breadcrumb scrolling after dismissing a full-window preview. |
| 2026-09-19 | lgse/strata#1149 | fix | Adapted the drawer to scaled and narrow windows and fixed the 4× sidebar flicker loop. |
| 2026-09-17 | lgse/strata#1078 | fix | Released preserved column scroll space after the preview closes. |
| 2026-09-13 | lgse/strata#888 | feat | Filled free space in Columns, added session-local manual width, Icons reservation, and media size caps. |
| 2026-09-11 | lgse/strata#829 | fix | Aligned header controls with the navigation and doubled the minimum width to 560 px. |

## Known gaps

- After a filter query edit drops a previewed pick, Columns and Icons keep the drawer open with "No preview for this selection"; List closes it. lgse/strata#1822
