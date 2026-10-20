---
title: Sidebar
status: shipped
origin: {issue: lgse/strata#104, pr: lgse/strata#106}
branch: null
reviewed_at: e0f73973926ff67e77c2c56cf288b7b7617bb2e5
review: draft
code: [src/ui/window/sidebar.rs, src/ui/window/sidebar_drop_feedback.rs, src/ui/window/keyboard/sidebar.rs, src/ui/sidebar_toggle.rs]
tests: [src/ui/window/tests/bookmarks.rs, src/ui/window/tests/sidebar.rs, src/ui/window/sidebar_drop_feedback/tests.rs, src/ui/sidebar_toggle/tests.rs, src/ui/window/tests/rail.rs, src/ui/window/tests/preferences.rs, tests/e2e/scenarios/test_sidebar_reordering.py]
docs: [docs/preferences.md, site/src/reference/keyboard-navigation.md]
related: [operations/trash, devices/volumes, operations/drag-and-drop, preview/preview-panel, preview/preview-panel/layout, integration/10xer-mode, integration/portal-file-chooser, settings/preferences, app/updates, app/window]
---

## Summary

The left panel of every browser window and the file chooser: built-in places, the PINNED section, and the DEVICES section. Users reorder and hide places, step the panel between full, icon rail, and hidden, and reach it from the keyboard. Children: `browser/sidebar/pins` (pinned folders stored in the GTK bookmarks file, including drag-to-pin) and `browser/sidebar/connect-to-server` (the Network row's Connect to server dialog). Which devices DEVICES lists, and when, belongs to `devices/volumes`.

## Behavior

### Places

- By default the sidebar lists Home, Trash, Network, Recent, Desktop, Documents, Downloads, Music, Pictures, and Videos in one block, followed by PINNED and DEVICES. lgse/strata#1161, lgse/strata#1342
- Desktop, Documents, Downloads, Music, Pictures, and Videos open the folders set in `user-dirs.dirs`; Music follows `XDG_MUSIC_DIR`. lgse/strata#1342
- Recent appears only when GTK recent-file tracking is enabled and GIO supports the `recent` scheme. lgse/strata#1083
- The row for the current location shows an 18% accent tint and an accent-coloured icon. lgse/strata#106
- Clicking a place that fails to open, such as Network with `GIO_USE_VFS=local`, and dismissing the error leaves the pane and the highlight on the open place. lgse/strata#1605
- While a place mounts before opening, the highlight stays on the open place; a failed or cancelled mount leaves it there. lgse/strata#1605
- Home, standard folders, and local pins show the folder's saved colour and custom icon, and update in every open window when it changes. lgse/strata#1370
- Right-clicking a local folder row offers Customize…; clearing the customization restores the place's default icon. lgse/strata#1370
- In the file chooser, the sidebar omits Trash and Network. lgse/strata#1025 (unverified)
- In the file chooser, built-in place rows offer the same context menus as in a browser window and can be reordered by drag. lgse/strata#1713
- Unpinning Home or a standard folder in the file chooser hides it in every window, and a reorder there is saved for every window. lgse/strata#1713

### Visibility

- Settings → General → Sidebar has one chip per built-in place; turning a chip off hides that place in every open window and survives a restart. lgse/strata#1025, lgse/strata#1342
- Hiding a built-in place leaves pins and devices unchanged. lgse/strata#1025
- Right-clicking Home, Network, or a standard folder offers Unpin and Properties; Unpin hides the place and turns its chip off. lgse/strata#1025
- The Trash row's menu offers Unpin and Properties, plus Empty Trash… only while Trash holds items. lgse/strata#1025

### Reordering

- Dragging a row and releasing it on the upper half of another row places it before that row; the lower half places it after. lgse/strata#202, lgse/strata#1161
- Home, Trash, Network, Recent, and the standard folders can be dragged into any order, which is saved and restored after a restart. lgse/strata#1161
- A reorder in one window reorders the sidebar in every other open window. lgse/strata#589
- A plain click on a row navigates and never reorders. lgse/strata#1161
- Dropping a built-in place on a pinned row, or a pinned row on a built-in place, changes nothing and shows no insertion line. lgse/strata#202, lgse/strata#1713
- While a built-in place is dragged over the upper or lower half of another built-in row, an accent line shows in the gap before or after that row. lgse/strata#1713
- Dropping a built-in place on the gap just before or after another built-in row moves it to that side; dropping a row on its own adjacent gap changes nothing. lgse/strata#1713
- A saved order that lacks a newer place gains it beside its default neighbour, so Music appears after Downloads. lgse/strata#1161, lgse/strata#1342

### Spacing and drag feedback

- Pinned rows have the same 2 px spacing as built-in places and devices, in the full sidebar and the icon rail. lgse/strata#1707, lgse/strata#1713
- Dragging files over a pinned folder's row body shows a highlight and an accent outline, and dropping still moves or copies into that folder. lgse/strata#1692, lgse/strata#1713
- The row-body highlight does not scale the row. lgse/strata#1713 (unverified)
- While a pin insertion line shows, other rows and devices show no hover background; the focus outline is hidden during any drag over the sidebar. lgse/strata#1713
- Only one sidebar drop site shows an indicator at a time, and moving from a folder row onto a gap cancels that row's spring-load. lgse/strata#1713
- Dragging files over the Trash row highlights it only when the selection can be trashed. lgse/strata#1713 (unverified)

### Devices

- A Strata label saved with Set label… replaces the system name on the device row in every open window; clearing it restores the system name. lgse/strata#1393

### Collapsing

- In a browser window, each press of the header toggle or Ctrl+B steps the sidebar from full to icon rail to hidden, then back to full. lgse/strata#1606
- Each step applies to every open browser window, and new windows open in the saved state. lgse/strata#1350, lgse/strata#1304, lgse/strata#1606
- The sidebar is expanded and `sidebar_compact` is off by default. lgse/strata#1350, lgse/strata#1606
- With `sidebar_compact = true` saved and the sidebar shown, every new window starts on the icon rail at any width. lgse/strata#1606
- With `sidebar_compact = true` and `sidebar_expanded = false` saved, a new window starts hidden; the next step shows the full sidebar and clears `sidebar_compact`. lgse/strata#1606 (unverified)
- In the window where the step is taken, stepping from hidden to full shows the full sidebar even when too narrow. It stays full until the window or the preview next runs out of room. Another window on an automatic rail keeps its rail unless the step cleared a saved `sidebar_compact`. lgse/strata#1606 (unverified)
- The toggle's tooltip names the next step: "Compact sidebar (Ctrl+B)" from full, "Hide sidebar (Ctrl+B)" from the rail, "Show sidebar (Ctrl+B)" from hidden. lgse/strata#1606
- In 10xer mode the tooltip names Ctrl+N instead of Ctrl+B. lgse/strata#1576, lgse/strata#1606
- The accessible name is "Toggle sidebar (Ctrl+B)", or "(Ctrl+N)" in 10xer mode, at every step. lgse/strata#1606
- A rail chosen with the toggle stays when the window widens or the preview closes. lgse/strata#1606
- At text sizes 9 and 11, rail row icons sit on the header toggle's vertical axis. lgse/strata#1606
- Reopening the sidebar at a 10px text size restores at least its measured minimum width, so row icons are not clipped. lgse/strata#1176
- In the icon rail, rows show only icons with name tooltips, and headings and device buttons are hidden. lgse/strata#1181 (unverified)

### Keyboard

- Outside 10xer mode, Ctrl+Shift+B shows a hidden sidebar and focuses the active row; pressing it again in the sidebar restores the previous focus. lgse/strata#58 (unverified)
- Outside 10xer mode, Enter on a focused row opens the place with its first item selected; a pointer click opens it with nothing selected. lgse/strata#715
### Update notice

- When a check finds an update, every open window shows "Update available" over "vX", with a download icon, at the foot of its sidebar. lgse/strata#26, lgse/strata#944, lgse/strata#1581
- The headline follows the interface language, such as "Update verfügbar" in German and "Nouvelle version" in French. lgse/strata#1581
- A prerelease and a stable offer show the same headline; only the version line, such as `v0.5.0-rc.1`, marks a prerelease. lgse/strata#1581 (unverified)
- In a sidebar too narrow for either line, that line stays on one line and is ellipsized at its end. lgse/strata#1581 (unverified)
- In the collapsed sidebar rail the notice shows only its download icon; expanding the sidebar restores both lines. lgse/strata#1581
- The two-line notice row is at least 38 px tall. lgse/strata#1581 (unverified)

## Design

[docs/preferences.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/preferences.md) carries the sidebar order, place visibility, expanded and compact state, folder customization, and device label preferences.

- The sidebar is a list of buttons rebuilt wholesale from preferences, pins, and the volume monitor. Monitor events are coalesced into one idle rebuild that restores the scroll position (lgse/strata#589).
- Trash, Recent, and standard folders navigate directly. Other rows go through `navigate_location`, which validates only non-local locations such as Network and SMB pins, mounting them first when needed (lgse/strata#67, lgse/strata#589). Volume rows mount an unmounted volume on click.
- Built-in places share one saved `sidebar_order` list of ids. Unknown ids are dropped, and a missing id is inserted after its nearest earlier default neighbour so upgraded sidebars look unchanged (lgse/strata#1161).
- Specials and standard folders became one block once both were reorderable; the separator between them was removed (lgse/strata#1161).
- Built-in places are not pins, so their Unpin writes the visibility preference rather than the bookmarks file (lgse/strata#1024, lgse/strata#1025).
- DEVICES shows exactly what GIO reports. A raw `/proc/self/mountinfo` fallback surfaced mounts the backend hides on purpose, so it was removed; visibility policy stays with GIO, GVfs, and udisks2, as in Nautilus (lgse/strata#532, lgse/strata#536).
- Device discovery waits until after first paint so a window never blocks on D-Bus, GVfs, or udisks2 before appearing (lgse/strata#1070).
- Only the toggle's steps are remembered, as `sidebar_expanded` and `sidebar_compact` (lgse/strata#1606). A "Start with sidebar collapsed" switch was left out as unneeded (lgse/strata#1345, lgse/strata#1350); hover-reveal panels were declined (lgse/strata#1282).
- A row highlights on click, before its location is validated. A rejected navigation resyncs the highlight to the open location rather than deferring it until validation (lgse/strata#860, lgse/strata#1605).
- Pin gaps supply the spacing between rows, so each row boundary has one spacer. The sidebar box's own 2 px spacing had doubled it around every pin gap (lgse/strata#1707, lgse/strata#1713).
- One drop-feedback owner per sidebar decides which site shows an indicator, so a late validation or a stale leave cannot restore or clear another site's line. The general file-drop outline no longer overrides the row indicator (lgse/strata#1707, lgse/strata#1713).
- The file chooser shares the browser's place reordering, menus, and drag-to-pin. Its sidebar visibility and compact state stay local to the dialog ([docs/portal-file-chooser.md](https://github.com/lgse/strata/blob/e0f73973926ff67e77c2c56cf288b7b7617bb2e5/docs/portal-file-chooser.md), lgse/strata#1713).
- The selected row uses a direct accent tint because tinting the existing highlight token stayed too faint on dark themes (lgse/strata#104, lgse/strata#106).
- The fit rule and `RailPolicy` that rail the sidebar automatically belong to `preview/preview-panel/layout` (lgse/strata#1602, lgse/strata#1606).
- Rail rows take the scaled header-control size from code instead of a fixed 24 px CSS minimum. They stay on the toggle's axis below 100 % text size (lgse/strata#1602, lgse/strata#1606).
- The tooltip names the next step while the accessible name stays constant, so assistive technology and E2E tests find the toggle in every mode (lgse/strata#1606).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-17 | lgse/strata#1726 | feat | Added Connect to server… to the Network row's menu, with an address field and an optional pin, so network locations can be added without typing in the location bar. |
| 2026-10-15 | lgse/strata#1605 | fix | Returned the highlight to the open place after a rejected place click. |
| 2026-10-13 | lgse/strata#1606 | fix | Made the header toggle step full, rail, hidden, saved the rail as `sidebar_compact`, and made the automatic rail edge-triggered under one fit rule. |
| 2026-10-12 | lgse/strata#1581 | fix | Split the update notice into an "Update available" headline over the version, so it fits the default width in every language. |
| 2026-10-11 | lgse/strata#1564 | feat | Kept the update notice on one line, middle-ellipsized, with a prerelease kind before the version. |
| 2026-10-02 | lgse/strata#1370 | fix | Showed saved folder colours and custom icons on sidebar rows and added Customize… to local rows. |
| 2026-10-02 | lgse/strata#1350 | feat | Persisted the collapsed state and synchronized it across windows so new windows open as last left. |
| 2026-09-30 | lgse/strata#1342 | feat | Added XDG Music as a standard place with its own visibility chip. |
| 2026-09-23 | lgse/strata#1161 | feat | Made Home, Trash, Network, and Recent reorderable with the standard folders in one saved order. |
| 2026-09-22 | lgse/strata#1176 | fix | Clamped the reopen width to the measured minimum so icons are not clipped at small text sizes. |
| 2026-09-15 | lgse/strata#1025 | feat | Added per-place visibility chips and Unpin and Properties menus on built-in places. |
| 2026-09-08 | lgse/strata#589 | refactor | Separated sidebar assembly from window policy and shared place-row bindings. |
| 2026-09-01 | lgse/strata#106 | fix | Raised the selected-row contrast with a direct accent tint and accent icon. |

## Known gaps

- NAS shares mounted by the system at native paths do not appear unless GIO reports them. lgse/strata#1209
- PINNED and DEVICES cannot be collapsed; the implementation is unmerged. lgse/strata#1389, lgse/strata#1390
