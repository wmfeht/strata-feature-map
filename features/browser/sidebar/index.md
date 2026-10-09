---
title: Sidebar
status: shipped
origin: {issue: lgse/strata#104, pr: lgse/strata#106}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [src/ui/window/sidebar.rs]
tests: [src/ui/window/tests/bookmarks.rs, tests/e2e/scenarios/test_sidebar_reordering.py]
docs: [docs/preferences.md, docs/keyboard-navigation.md]
related: [operations/trash, devices/volumes, operations/drag-and-drop, preview/preview-panel, integration/10xer-mode, integration/portal-file-chooser, settings/preferences]
---

## Summary

The left panel of every browser window and the file chooser: built-in places, the PINNED section, and the DEVICES section. Users reorder and hide places, collapse the panel, and reach it from the keyboard. Child: `browser/sidebar/pins` (pinned folders stored in the GTK bookmarks file).

## Behavior

### Places

- By default the sidebar lists Home, Trash, Network, Recent, Desktop, Documents, Downloads, Music, Pictures, and Videos in one block, followed by PINNED and DEVICES. lgse/strata#1161, lgse/strata#1342
- Desktop, Documents, Downloads, Music, Pictures, and Videos open the folders set in `user-dirs.dirs`; Music follows `XDG_MUSIC_DIR`. lgse/strata#1342
- Recent appears only when GTK recent-file tracking is enabled and GIO supports the `recent` scheme. lgse/strata#1083
- The row for the current location shows an 18% accent tint and an accent-coloured icon. lgse/strata#106
- Home, standard folders, and local pins show the folder's saved colour and custom icon, and update in every open window when it changes. lgse/strata#1370
- Right-clicking a local folder row offers Customize…; clearing the customization restores the place's default icon. lgse/strata#1370

### Visibility

- Settings → General → Sidebar has one chip per built-in place; turning a chip off hides that place in every open window and survives a restart. lgse/strata#1025, lgse/strata#1342
- Hiding a built-in place leaves pins and devices unchanged. lgse/strata#1025
- Right-clicking Home, Network, or a standard folder offers Unpin and Properties; Unpin hides the place and turns its chip off. lgse/strata#1025
- The Trash row's menu offers Unpin and Properties alongside Empty Trash…. lgse/strata#1025

### Reordering

- Dragging a row and releasing it on the upper half of another row places it before that row; the lower half places it after. lgse/strata#202, lgse/strata#1161
- Home, Trash, Network, Recent, and the standard folders can be dragged into any order, which is saved and restored after a restart. lgse/strata#1161
- A reorder in one window reorders the sidebar in every other open window. lgse/strata#589
- A plain click on a row navigates and never reorders. lgse/strata#1161
- Dropping a built-in place on a pinned row, or a pinned row on a built-in place, changes nothing. lgse/strata#202
- A saved order that lacks a newer place gains it beside its default neighbour, so Music appears after Downloads. lgse/strata#1161, lgse/strata#1342

### Devices

- DEVICES lists the volumes GIO's volume monitor reports, plus unshadowed mounts that have no volume. lgse/strata#536
- Mounts the volume-monitor backend hides, such as a Pacman cache subvolume, do not appear in DEVICES. lgse/strata#536
- With no volumes, mounts, or pending releases, neither the DEVICES heading nor its separator is shown. lgse/strata#536
- Inserting, mounting, unmounting, or removing a drive updates DEVICES without a restart. lgse/strata#536
- A Strata label saved with Set label… replaces the system name on the device row in every open window; clearing it restores the system name. lgse/strata#1393
- The file chooser's sidebar lists drives mounted before it opened, once the dialog has painted, and omits network shares. lgse/strata#1070

### Collapsing

- Ctrl+B or the header toggle collapses or expands the sidebar in every open browser window, and new windows open in the saved state. lgse/strata#1350
- The sidebar is expanded by default, and the file chooser keeps its own unsaved state. lgse/strata#1350
- Reopening the sidebar at a 10px text size restores at least its measured minimum width, so row icons are not clipped. lgse/strata#1176
- In the narrow-window icon rail, rows show only icons with name tooltips, and headings and device buttons are hidden. lgse/strata#1181 (unverified)

### Keyboard

- Outside 10xer mode, Ctrl+Shift+B shows a hidden sidebar and focuses the active row; pressing it again in the sidebar restores the previous focus. lgse/strata#58 (unverified)
- In single-click mode, Enter on a focused row opens the place with its first item selected; a pointer click opens it with nothing selected. lgse/strata#715
- Right from the sidebar refocuses the file row it left, or the active item when the sidebar was entered from the header. lgse/strata#1088

## Design

[docs/preferences.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/preferences.md) carries the sidebar order, place visibility, expanded state, folder customization, and device label preferences.

- The sidebar is a list of buttons rebuilt wholesale from preferences, pins, and the volume monitor. Monitor events are coalesced into one idle rebuild that restores the scroll position (lgse/strata#589).
- Trash, Recent, and standard folders navigate directly. Other rows, including pins and mounts, go through location validation, which can mount an unmounted location first (lgse/strata#67, lgse/strata#589).
- Built-in places share one saved `sidebar_order` list of ids. Unknown ids are dropped, and a missing id is inserted after its nearest earlier default neighbour so upgraded sidebars look unchanged (lgse/strata#1161).
- Specials and standard folders became one block once both were reorderable; the separator between them was removed (lgse/strata#1161).
- Built-in places are not pins, so their Unpin writes the visibility preference rather than the bookmarks file (lgse/strata#1024, lgse/strata#1025).
- DEVICES shows exactly what GIO reports. A raw `/proc/self/mountinfo` fallback surfaced mounts the backend hides on purpose, so it was removed; visibility policy stays with GIO, GVfs, and udisks2, as in Nautilus (lgse/strata#532, lgse/strata#536).
- Device discovery waits until after first paint so a window never blocks on D-Bus, GVfs, or udisks2 before appearing (lgse/strata#1070).
- Only the collapsed state is remembered. A "Start with sidebar collapsed" switch was left out as unneeded (lgse/strata#1345, lgse/strata#1350); hover-reveal panels were declined (lgse/strata#1282).
- The selected row uses a direct accent tint because tinting the existing highlight token stayed too faint on dark themes (lgse/strata#104, lgse/strata#106).
- The narrow-window icon rail is owned by the preview layout; see `preview/preview-panel` (lgse/strata#1181).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-02 | lgse/strata#1370 | fix | Showed saved folder colours and custom icons on sidebar rows and added Customize… to local rows. |
| 2026-10-02 | lgse/strata#1350 | feat | Persisted the collapsed state and synchronized it across windows so new windows open as last left. |
| 2026-09-30 | lgse/strata#1342 | feat | Added XDG Music as a standard place with its own visibility chip. |
| 2026-09-23 | lgse/strata#1161 | feat | Made Home, Trash, Network, and Recent reorderable with the standard folders in one saved order. |
| 2026-09-22 | lgse/strata#1176 | fix | Clamped the reopen width to the measured minimum so icons are not clipped at small text sizes. |
| 2026-09-15 | lgse/strata#1025 | feat | Added per-place visibility chips and Unpin and Properties menus on built-in places. |
| 2026-09-08 | lgse/strata#589 | refactor | Separated sidebar assembly from window policy and shared place-row bindings. |
| 2026-09-01 | lgse/strata#106 | fix | Raised the selected-row contrast with a direct accent tint and accent icon. |

## Known gaps

- Clicking a place that fails to open, such as Network without its backend, leaves that row highlighted while the pane stays put. lgse/strata#860
- NAS shares mounted by the system at native paths do not appear unless GIO reports them. lgse/strata#1209
- PINNED and DEVICES cannot be collapsed; the implementation is unmerged. lgse/strata#1389, lgse/strata#1390
