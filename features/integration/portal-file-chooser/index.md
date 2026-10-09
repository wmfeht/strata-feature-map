---
title: System file chooser
status: shipped
origin: {issue: lgse/strata#120, pr: lgse/strata#175}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [src/portal.rs, src/portal/dbus.rs, src/ui/chooser.rs, src/ui/browser/chooser_context.rs]
tests: [src/portal/tests.rs, src/portal/dbus/tests.rs, src/ui/chooser/tests.rs, src/ui/chooser/tests/acceptance.rs, src/ui/chooser/tests/column_widths.rs, src/ui/chooser/tests/filtered_preview.rs, src/ui/chooser/tests/sizing.rs]
docs: [docs/portal-file-chooser.md]
related: [integration/10xer-mode, operations/clipboard, operations/archives]
---

## Summary

Strata as the XDG Desktop Portal FileChooser backend: Open, Save, and Save Files dialogs for portal-aware applications, drawn with Strata's sidebar, views, filters, and previews. The same chooser window also serves Strata's own Move to, Copy to, Extract to, and Send to destinations. Children: `integration/portal-file-chooser/setup` (enabling and restoring the integration), `integration/portal-file-chooser/url-download` (Name field filenames and URLs), `integration/portal-file-chooser/image-conversion` (PNG conversion of downloads), and `integration/portal-file-chooser/window-placement` (initial size and centering).

## Behavior

### Requests

- `strata --portal` serves `org.freedesktop.impl.portal.FileChooser` version 4 on the bus name `org.freedesktop.impl.portal.desktop.strata`, handling OpenFile, SaveFile, and SaveFiles. lgse/strata#175
- A request with an empty title is titled "Open Files", "Save File", or "Save Files"; a missing accept label becomes Open or Save. lgse/strata#175 (unverified)
- A 17th concurrent request, a reused request handle, or a request string over 4,096 bytes fails with a portal error and no window. lgse/strata#175 (unverified)
- A request with more than 32 file filters, or one filter with more than 100 rules, opens the chooser instead of failing. lgse/strata#466, lgse/strata#504
- More than 128 filters, or more than 1,024 rules across all filters, logs a warning and still opens the chooser. lgse/strata#466, lgse/strata#504 (unverified)
- A glob rule with more than 2 wildcard groups or over 256 bytes, or more than 16 choices, still fails the request. lgse/strata#466, lgse/strata#504 (unverified)
- A long filter list scrolls inside its dropdown, which opens toward the side of the button with more room. lgse/strata#504
- Caller choices appear as checkboxes and dropdowns beside the filter, and the selected values are returned with the result. lgse/strata#175
- `Request.Close` from the caller closes the chooser and the request returns response 1. lgse/strata#175
- Without a usable folder hint, Open, SaveFile, and SaveFiles start in `XDG_DOWNLOAD_DIR`, or Home when it is undefined. lgse/strata#993
- A folder hint that is relative, inaccessible, or unanswered within 3 seconds falls back to the same default folder. lgse/strata#993 (unverified)
- A SaveFile `current_file` naming a file that does not exist yet, in an accessible folder, opens that folder with the full name in Name. lgse/strata#700
- A Wayland parent handle makes the chooser transient for the caller; an X11 parent handle is ignored and the chooser opens standalone. lgse/strata#175
- The backend exits once no request has been active for 120 seconds, checked every 10 seconds; an open chooser keeps it running. lgse/strata#1201

### Browsing

- Entering a remote URI in the address bar shows "The system file chooser supports local files and folders only." lgse/strata#175
- Folder-only requests hide regular files in folder listings and in recursive filter results. lgse/strata#1155
- Changing the file-type filter refreshes the results and keeps an active filter query; only files the new filter accepts can be returned. lgse/strata#1155
- Local drives mounted before the chooser opened appear under Devices in its sidebar once the dialog has painted; network shares do not. lgse/strata#1070
- Recent appears in the chooser sidebar when enabled in sidebar preferences and supported by the desktop, listing only local targets. lgse/strata#1138
- Ctrl+1, Ctrl+2, and Ctrl+3 switch the chooser to Columns, Icons, and List. lgse/strata#877
- With the file view focused and type-to-search on (the default), a printable character opens the filter seeded with it; `/` opens an empty filter. lgse/strata#1164
- Ctrl+click on a file focuses the item just toggled, so the preview follows it. lgse/strata#1164
- Dragging from blank space draws a marquee only in multiple-selection requests; a blank click clears the selection in every request. lgse/strata#1164
- With folders set to single-click in Icons or List, a single click on a folder opens it; a single click on a file only selects it. lgse/strata#1196
- With the single-click preview preference on, clicking a previewable file opens the shared preview pane; Space toggles it. lgse/strata#385
- Dragging a Miller column's right edge resizes it, and double-clicking the edge fits it to its content. lgse/strata#1315
- A resized Miller column or List heading becomes the default for the next chooser, stored apart from browser windows' defaults. lgse/strata#1339
- The item menu offers Rename, Properties, and, for one previewable file, Quick preview; empty-space right-click offers New Folder. lgse/strata#175, lgse/strata#385
- The item menu also offers Compress… for native entries, plus Move to Trash and Permanently delete where the location allows them. lgse/strata#950, lgse/strata#1352
- With the file view focused, Delete moves the selection to Trash and Shift+Delete asks to delete permanently. lgse/strata#950
- F5 refreshes, Ctrl+H or Ctrl+. toggles hidden files, and Ctrl+A selects all only in multiple-selection requests. lgse/strata#175 (unverified)
- Escape first dismisses an open menu, dropdown, inline edit, filter, location edit, preview, or download, and only then cancels the request. lgse/strata#175, lgse/strata#1285

### Accepting

- In a single-selection request, selecting another item replaces the selection, so Open returns one item. lgse/strata#175 (unverified)
- File Open requests show an "Open files read-only" checkbox; checking it returns `writable` false. lgse/strata#175 (unverified)
- In Columns, a selected filter result in a column other than the active one is returned on Open, not "Choose a file". lgse/strata#1004
- In a folder request, accepting with only the automatic first-row selection returns the displayed folder; an explicitly selected child returns that child. lgse/strata#1016
- Ctrl+Enter from the file list accepts a folder request. lgse/strata#175
- In a Save request, accepting without clicking a row saves into the displayed folder, not its first subfolder. lgse/strata#1138
- In a Save request, a single-clicked folder becomes the destination without the chooser navigating into it. lgse/strata#892
- In a Save request, selecting a file copies its name into Name without accepting; selecting a folder leaves Name unchanged. lgse/strata#1138
- Saving with a file selected in Recent uses that file's containing folder as the destination. lgse/strata#1138
- Saving over an existing file opens "Replace existing file?" with Cancel focused; Cancel keeps the chooser open and Replace returns the path. lgse/strata#175, lgse/strata#1311
- Saving where a folder of the same name exists fails with "A folder named “name” already exists". lgse/strata#175 (unverified)

### Destination choosers

- Move to…, Copy to…, Extract to…, and Send to… → device → Choose folder… open a folder chooser as a floating modal window over the originating window. lgse/strata#1384
- Invoking another destination command while one is open presents the existing chooser instead of opening a second. lgse/strata#1384 (unverified)
- Closing the originating window closes its chooser; Cancel leaves the files and the window's location unchanged. lgse/strata#1384
- For Send to, the sidebar is hidden and navigating outside the device shows "Choose an existing folder inside this removable device." lgse/strata#1384
- Move to, Copy to, and Extract to offer New Folder. Enter in the path entry navigates; Ctrl+Enter in the file list or the action button confirms. lgse/strata#1384
- Send to disables New Folder in the menu, the toolbar, and Ctrl+Shift+N. lgse/strata#1384 (unverified)

## Design

[docs/portal-file-chooser.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/portal-file-chooser.md) carries the user-facing contract, installation, keyboard map, and local test tools.

- The chooser is local-only because the backend contract returns normalized `file://` URIs. Resolving GVfs locations to their FUSE paths is deferred (lgse/strata#176).
- Requests come from other applications, so strings, globs, and choices are bounded. Filter-list size is not treated as abuse: count and rule budgets warn instead of refusing, since refusal left uploads silently broken (lgse/strata#465, lgse/strata#498).
- The chooser reuses the browser view, sidebar, and preview drawer. Differences from the main window were treated as bugs and aligned (lgse/strata#384, lgse/strata#1163, lgse/strata#1195).
- The automatic first-row selection is a keyboard cursor, not a choice. Destination resolution ignores it, because callers such as Chromium persist the returned folder and the error compounds (lgse/strata#1137, lgse/strata#1015).
- `current_file` for a nonexistent file is accepted for Qt interoperability, though the specification describes existing files (lgse/strata#699).
- The backend is D-Bus activated and exits when idle. A request arriving during shutdown is refused rather than raced (lgse/strata#1200).
- Move to and Copy to reuse the floating chooser rather than a separate in-window picker. The in-window variant in lgse/strata#1377 was set aside for the floating build in lgse/strata#1383.
- The chooser's 10xer key map and command allowlist belong to `integration/10xer-mode`.

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-02 | lgse/strata#1384 | feat | Replaced the separate destination picker with the floating folder chooser for Move, Copy, Extract, and Send to. |
| 2026-10-01 | lgse/strata#1352 | feat | Offered Compress… for native entries in the chooser item menu. |
| 2026-09-30 | lgse/strata#1339 | fix | Saved resized Miller columns and List headings as chooser defaults, separate from browser defaults. |
| 2026-09-28 | lgse/strata#1315 | fix | Attached column resize handles in the chooser, which previously ignored resize drags. |
| 2026-09-23 | lgse/strata#1201 | fix | Exited the backend after two idle minutes and retired old chooser processes on in-app update. |
| 2026-09-23 | lgse/strata#1164 | fix | Aligned Ctrl+click focus, type-to-search, and marquee rules with the main browser. |
| 2026-09-23 | lgse/strata#1196 | fix | Opened folders on single click in Icons and List when the click preference asks for it. |
| 2026-09-19 | lgse/strata#1138 | fix | Ignored the load cursor for Save destinations, copied selected file names into Name, and added Recent. |
| 2026-09-17 | lgse/strata#1070 | fix | Discovered local devices after first paint so mounted drives appear in the chooser sidebar. |
| 2026-09-15 | lgse/strata#1016 | fix | Returned the displayed folder when only the automatic first row was selected. |
| 2026-09-14 | lgse/strata#993 | fix | Defaulted requests without a folder hint to Downloads instead of Home. |
| 2026-09-14 | lgse/strata#1004 | fix | Accepted filter results selected in a non-active Miller column. |
| 2026-09-13 | lgse/strata#950 | feat | Added Move to Trash and Permanently delete to the chooser menu and keyboard. |
| 2026-09-12 | lgse/strata#877 | feat | Added Ctrl+1/2/3 view shortcuts and reused compatible panes when switching views. |
| 2026-09-12 | lgse/strata#892 | fix | Let a selected folder be the Save destination without navigating into it. |
| 2026-09-09 | lgse/strata#700 | fix | Kept Qt's `current_file` suggestion for a file that does not exist yet. |
| 2026-09-07 | lgse/strata#504 | fix | Accepted more than 32 filters and made the filter dropdown scroll. |
| 2026-09-06 | lgse/strata#466 | fix | Accepted filters with many rules, which GitHub's attach button sends. |
| 2026-09-05 | lgse/strata#385 | feat | Shared single-click and Quick preview behavior with the main window. |
| 2026-09-05 | lgse/strata#175 | feat | Added the FileChooser v4 backend with Open, Save, Save Files, filters, choices, and previews. |

## Known gaps

- Remote locations such as `smb://` cannot be browsed or returned, even when GVfs exposes a local FUSE path. lgse/strata#176
- In a multiple-selection Open request, Enter returns only the focused file instead of the selection; fixed upstream after this snapshot. lgse/strata#1426, lgse/strata#1533
- In a Save request, clicking a file whose name is not valid UTF-8 saves to a lossy copy of the name without the Replace prompt; fixed upstream after this snapshot. lgse/strata#1427, lgse/strata#1533
