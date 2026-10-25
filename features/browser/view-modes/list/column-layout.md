---
title: List column order and visibility
status: shipped
origin: {issue: lgse/strata#1597, pr: lgse/strata#1651}
branch: null
reviewed_at: d6c74746cdb27e506a08e8cdefa3bc8cef7d10f9
review: draft
code: [src/ui/browser_modes/column_options.rs]
tests: [src/ui/preferences/tests/preferences.rs, src/ui/window/tests/preferences.rs, src/ui/chooser/tests/column_widths.rs, tests/qa/scenarios/view_switching]
docs: [docs/preferences.md]
related: [browser/view-modes, browser/view-modes/sorting, browser/view-modes/folder-views, browser/selection/pointer-intent, integration/portal-file-chooser]
---

## Summary

Choosing which List columns show and in what order, for narrow windows where Mode and Type squeeze Name. Headings reorder by dragging, and a Columns popover toggles visibility. The choice is shared by every browser window and the portal file chooser, and never changes the sort.

## Behavior

### Columns popover

- A List pane header has a Columns menu button with the tooltip "Columns". lgse/strata#1651
- The popover is headed COLUMNS and lists check items Name, Mode, Size, Type, and Modified, a separator, then "Reset to default columns". lgse/strata#1651
- The Columns button is hidden while 10xer mode is on. lgse/strata#1651 (unverified)
- Right-clicking the List heading row opens the same popover at the pointer. lgse/strata#1651
- Appearance has a "Customize columns…" item after Group by file type, visible only in List. Choosing it closes Appearance and opens the Columns popover on the headings. lgse/strata#1651
- After switching to List from Columns, including the first switch, "Customize columns…" is visible and opens the popover. lgse/strata#1651

### Visibility

- Clicking a checked Mode, Size, Type, or Modified item hides that column's heading and cells in every row; clicking it again shows them. The check mark follows the saved state. lgse/strata#1651
- The Name item is checked and insensitive, with the accessible description "The Name column cannot be hidden". lgse/strata#1651 (unverified)
- A hand-edited `list_hidden_columns` that names `name` loads with Name shown. lgse/strata#1651 (unverified)
- "Reset to default columns" restores Name, Mode, Size, Type, Modified, shows every column, and removes `list_hidden_columns` and `list_column_order` from `settings.toml`. lgse/strata#1651
- The List loading skeleton follows the saved order and leaves out hidden columns. lgse/strata#1651 (unverified)

### Reordering

- Pressing a heading and dragging it horizontally shows a grabbing cursor and a 3 px accent inset line at the drop point. The headings do not move during the drag. lgse/strata#1651, lgse/strata#1800
- The line sits on the left edge of the heading the column would precede. lgse/strata#1800 (unverified)
- For a drop at the end, the line sits on the last heading's right edge. lgse/strata#1800 (unverified)
- Releasing over the headings moves the column to the marked point; one drag can move it several positions. lgse/strata#1800
- A drop on the column's current position shows no line and changes nothing. lgse/strata#1800 (unverified)
- Moving the pointer outside the heading row hides the line, and releasing there leaves the order unchanged. lgse/strata#1800
- A cancelled drag, or headings unmapped mid-drag, leaves the order unchanged and clears the line and cursor. lgse/strata#1800
- Moving the Name heading does not change the sort. lgse/strata#1800
- A drag only starts after 10 px of horizontal movement; a shorter press and release stays a sort click. lgse/strata#1651 (unverified)
- A press within 8 px of a heading's right edge resizes the column and never reorders it. lgse/strata#1651 (unverified)
- Dragging Mode 180 px to the right and releasing gives the order Name, Size, Mode, Type, Modified. lgse/strata#1651, lgse/strata#1800
- A drag saves `list_column_order` once, on release, and every window and the chooser then update. lgse/strata#1800

### Saving and sharing

- Order saves as `list_column_order`, such as `["name", "mode", "size", "type", "modified"]`, and hidden columns as `list_hidden_columns`. lgse/strata#1651
- On load, duplicate columns are dropped and missing ones are appended in default order. lgse/strata#1651 (unverified)
- The saved order and visibility apply before Settings opens and survive restarts. lgse/strata#1651
- Every browser window and the portal file chooser share order and visibility, and update live. lgse/strata#1651
- A List pane cached while another view shows also updates. lgse/strata#1651
- With window A showing Icons, hide Size in window B; A's List has Size hidden on return. lgse/strata#1651
- Column widths keep their separate browser and chooser scopes, `browser_list_columns` and `chooser_list_columns`. lgse/strata#1651

### Sorting

- Hiding, showing, reordering, or resetting columns never changes the sort key, direction, or file order. lgse/strata#1651
- A hidden sort column stays the active sort, including for saved folder sorts, newly opened folders, and view switches. lgse/strata#1651
- Showing the hidden sort column again restores its arrow; clicking it then reverses the existing direction. lgse/strata#1651

## Design

[docs/preferences.md](https://github.com/lgse/strata/blob/027d6981a69ea7b526a763d3ec563fdecb19c66b/docs/preferences.md) records the "List column order and visibility" preference.

- Column presentation is independent of sorting. Earlier revisions fell back to sorting by Name when the sort column was hidden; that was removed so file order never jumps (lgse/strata#1651).
- Changing the layout also updates a cached inactive List pane, because returning to List reuses it (lgse/strata#1651).
- Columns move only on release, with one shared preference update, instead of rearranging and saving on every swap (lgse/strata#1800).
- Reordering moves Name off the first child, so rows and pointer hit testing find cells by CSS class (lgse/strata#1651).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-15 | lgse/strata#1651 | feat | Added List column reordering by heading drag and visibility toggles, shared across windows and the chooser, without touching the sort. |

## Known gaps

None known.
