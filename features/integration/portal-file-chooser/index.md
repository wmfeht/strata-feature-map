---
title: System file chooser
status: shipped
origin: {issue: lgse/strata#120, pr: lgse/strata#175}
branch: null
reviewed_at: 86df474dc0e8352e0e2098637a017cc4c77a8c44
review: draft
code: [src/portal.rs, src/portal/dbus.rs, src/ui/chooser.rs, src/ui/browser/chooser_context.rs]
tests: [src/portal/tests.rs, src/portal/dbus/tests.rs, src/ui/chooser/tests.rs, src/ui/chooser/tests/acceptance.rs, src/ui/chooser/tests/column_widths.rs, src/ui/chooser/tests/confined.rs, src/ui/chooser/tests/filtered_preview.rs, src/ui/chooser/tests/sizing.rs, tests/qa/scenarios/chooser_selection/**, scripts/portal-test.py, scripts/portal-test.html, scripts/portal_test_environment.py, scripts/test_portal_test_environment.py, scripts/chooser-dev.sh]
docs: [site/src/reference/portal-file-chooser.md, docs/portal-file-chooser.md]
related: [integration/10xer-mode, operations/clipboard, operations/archives, operations/trash, browser/sidebar, preview/preview-panel/layout, browser/search/filter, browser/view-modes, browser/view-modes/columns, browser/view-modes/list]
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
- Options in the file-type filter and caller choice dropdowns are radio menu items, and the selected option reports the checked state. lgse/strata#1467, lgse/strata#1544
- `Request.Close` from the caller closes the chooser and the request returns response 1. lgse/strata#175
- Without a usable folder hint, Open, SaveFile, and SaveFiles start in `XDG_DOWNLOAD_DIR`, or Home when it is undefined. lgse/strata#993
- A folder hint that is relative, inaccessible, or unanswered within 3 seconds falls back to the same default folder. lgse/strata#993 (unverified)
- A Wayland parent handle makes the chooser transient for the caller; an X11 parent handle is ignored and the chooser opens standalone. lgse/strata#175
- The backend exits once no request has been active for 120 seconds, checked every 10 seconds; an open chooser keeps it running. lgse/strata#1201

### Browsing

- The chooser's header bar has the same height and button and icon sizes as a browser window's header. lgse/strata#1696
- Entering a remote URI in the address bar shows "The system file chooser supports local files and folders only." lgse/strata#175
- Folder-only requests hide regular files in folder listings and in recursive filter results. lgse/strata#1155
- Changing the file-type filter refreshes the results and keeps an active filter query; only files the new filter accepts can be returned. lgse/strata#1155
- Local drives mounted before the chooser opened appear under Devices in its sidebar once the dialog has painted; network shares do not. lgse/strata#1070
- `browser/directory-monitoring` owns how the chooser follows an open folder renamed, moved, or deleted outside Strata. lgse/strata#1554
- The header toggle and Ctrl+B (Ctrl+N in 10xer mode) step the chooser sidebar full, rail, hidden, full, except in Send to. lgse/strata#1606
- In a chooser too narrow for the full sidebar, stepping from hidden shows the full sidebar until the fit next changes. lgse/strata#1606 (unverified)
- Chooser sidebar steps apply to that dialog only and are not saved. lgse/strata#1606
- A saved `sidebar_compact = true` does not start a chooser on the rail. lgse/strata#1606 (unverified)
- The chooser's toggle tooltip follows the dialog's own sidebar mode and updates when the rail engages or releases or 10xer mode changes. lgse/strata#1606
- The chooser sidebar follows the automatic rail rule owned by `preview/preview-panel/layout`. lgse/strata#1606
- Recent appears in the chooser sidebar when enabled in sidebar preferences and supported by the desktop, listing only local targets. lgse/strata#1138
- Ctrl+1, Ctrl+2, and Ctrl+3 switch the chooser to Columns, Icons, and List. lgse/strata#877
- With the file view focused and type-to-search on (the default), a printable character opens the filter seeded with it; `/` opens an empty filter. lgse/strata#1164
- Ctrl+click on a file focuses the item just toggled, so the preview follows it. lgse/strata#1164
- In Columns, Right on a focused file behaves as in a browser window: it moves into the open child column, or does nothing. lgse/strata#382
- Dragging from blank space draws a marquee only in multiple-selection requests. A blank click in the file list or sidebar clears the selection in every request. lgse/strata#1164
- A plain click inside a preview that shows a file keeps the selection; a click in the empty preview slot still clears it. lgse/strata#1570
- With folders set to single-click in Icons or List, a single click on a folder opens it; a single click on a file only selects it. lgse/strata#1196
- With the single-click preview preference on, clicking a previewable file opens the shared preview pane; Space toggles it. lgse/strata#385
- Ctrl+0 on a focused PDF page in the chooser's preview resets its zoom, not the saved text size, with 10xer mode on or off. lgse/strata#1622
- Dragging a Miller column's right edge in the chooser resizes it, and double-clicking the edge fits it to its content. lgse/strata#1315
- With a preview open in Columns, the column beside the preview keeps its own resize edge; the divider has a wide handle. lgse/strata#1539 (unverified)
- `browser/view-modes/columns` and `browser/view-modes/list` own the chooser's saved column widths, kept apart from browser windows' widths. lgse/strata#1339
- The item menu offers Rename, Properties, and, for one previewable file, Quick preview; empty-space right-click offers New Folder. lgse/strata#175, lgse/strata#385
- The item menu also offers Compress… for native entries, plus Move to Trash and Permanently delete where the location allows them. lgse/strata#950, lgse/strata#1352
- When every selected item is on a network or cloud mount, Permanently delete in the item menu reads Delete without Trash. A `fuseblk` mount or a local FUSE overlay such as mergerfs keeps Permanently delete. lgse/strata#1614
- With the file view focused, Shift+Delete asks to delete permanently. Delete moves the selection to Trash, except as below. lgse/strata#950, lgse/strata#1533
- Where every selected item's open folder reports no Trash support but allows deletion, Delete opens the `operations/trash` explained permanent confirmation instead. lgse/strata#1533
- F5 refreshes, Ctrl+H or Ctrl+. toggles hidden files, and Ctrl+A selects all only in multiple-selection requests. lgse/strata#175 (unverified)
- With the file view focused and no text field active, F2 or Ctrl+R renames the one selected item, and Alt+Enter opens Properties for the focused item. lgse/strata#175, lgse/strata#393 (unverified)
- The Menu key or Shift+F10 opens the item menu for the focused item, except in a text field or popover. lgse/strata#666 (unverified)
- Ctrl+F opens the filter, Ctrl+L edits the location, and Ctrl+Shift+N creates a folder. lgse/strata#175 (unverified)
- Ctrl+Shift+B moves focus to the active sidebar place, opening a hidden sidebar first; pressed again, it returns focus to where it was. lgse/strata#175 (unverified)
- A shortcut reference can stay open after 10xer mode is turned off in another window. Then F5, Ctrl+H, Ctrl+., Ctrl+1/2/3, and Alt+Up/Left/Home leave the folder, view, and hidden files unchanged. lgse/strata#1714
- In that state, Escape closes the reference and keeps the request open. lgse/strata#1714
- In that state, text-size and thumbnail-size shortcuts still apply to the chooser. lgse/strata#1714, lgse/strata#1721 (unverified)
- With a filter result selected, Space in the Name or location entry types a space and opens no preview. lgse/strata#1714
- Escape first dismisses an open menu, dropdown, inline edit, filter, location edit, preview, or download, and only then cancels the request. lgse/strata#175, lgse/strata#1285
- In List, Escape during a column heading drag cancels the drag, keeps the request open, and keeps the file selection; a later heading drag still works. lgse/strata#1900
- The header close button is named "Cancel file selection (Escape)". lgse/strata#1895 (unverified)
- Escape on a focused filter result dismisses the filter and keeps the request open. lgse/strata#1440, lgse/strata#1533
- With 10xer mode off, the file list is one Tab stop, the whole strip in Columns, and Tab into it lands on the keyboard cursor row. lgse/strata#1431, lgse/strata#1533

### Saving

- A SaveFile `current_file` naming a file that does not exist yet, in an accessible folder, opens that folder with the full name in Name. lgse/strata#700
- With 10xer mode off, a SaveFile request with `current_name` `report.draft.pdf` opens with focus in Name and only `report.draft` selected. lgse/strata#1898
- That selection survives the idle focus restore after the window presents, so typing replaces `report.draft` and keeps `.pdf`. lgse/strata#1898
- The selection ends at the last dot after the first character, as in rename: `archive.tar.gz` selects `archive.tar`; `.bashrc` and `notes` select all. lgse/strata#1898 (unverified)
- With 10xer mode on, Tab from the header into Name in a SaveFile request selects only the part before the last dot. lgse/strata#1898
- In a Save request, accepting without clicking a row saves into the displayed folder, not its first subfolder. lgse/strata#1138
- In a Save request, a single-clicked folder becomes the destination without the chooser navigating into it. lgse/strata#892
- The Name field of a Save request and of a file Open request, where a URL can be typed, is named "Name". lgse/strata#1896 (unverified)
- In a Save request, selecting a file copies its name into Name without accepting; selecting a folder leaves Name unchanged. lgse/strata#1138
- In a Save request, clicking the file row highlighted automatically on load replaces Name with that file's name, in List, Columns, and Icons. The request stays open. lgse/strata#1785, lgse/strata#1786
- In a Save request, editing Name and then clicking the file still selected replaces the edit with that file's name. lgse/strata#1785, lgse/strata#1786
- In a Save request, the automatic highlight on load alone leaves the suggested name in Name. lgse/strata#1785, lgse/strata#1786
- With 10xer mode on, clicking a file in a Save request leaves Name unchanged. lgse/strata#1311, lgse/strata#1786
- In a Save request, after selecting or activating a file with a non-UTF-8 name, Save with Name unedited opens Replace for that exact file. lgse/strata#1427, lgse/strata#1533
- In a Save request, edited Name text is saved literally, so an edited lossy name keeps its U+FFFD characters; retyping the exact lossy text targets the original file again. lgse/strata#1427, lgse/strata#1533
- Saving with a file selected in Recent uses that file's containing folder as the destination. lgse/strata#1138
- Saving over an existing file opens "Replace existing file?" with Cancel focused; Cancel keeps the chooser open and Replace returns the path. lgse/strata#175, lgse/strata#1311
- Saving where a folder of the same name exists fails with "A folder named “name” already exists". lgse/strata#175 (unverified)

### Accepting

- In a single-selection request, selecting another item replaces the selection, so Open returns one item. lgse/strata#175 (unverified)
- File Open requests show an "Open files read-only" checkbox; checking it returns `writable` false. lgse/strata#175 (unverified)
- In Columns, a selected filter result in a column other than the active one is returned on Open, not "Choose a file". lgse/strata#1004
- In a folder request, accepting with only the automatic first-row selection returns the displayed folder; an explicitly selected child returns that child. lgse/strata#1016
- Ctrl+Enter from the file list accepts a folder request. lgse/strata#175
- In a multiple-selection Open request with files selected, Enter or Shift+Enter on a focused file returns every selected file, in every view. lgse/strata#1426, lgse/strata#1533
- In a multiple-selection Open request, Enter on a focused file outside the selection returns the selection, not the focused file. lgse/strata#1426, lgse/strata#1533
- In a multiple-selection Open request, Enter on a focused folder opens it, even with files selected. lgse/strata#1426, lgse/strata#1533
- In a multiple-selection Open request, Enter with a file focused on a selection of a folder and files returns only the files. lgse/strata#1533 (unverified)

### Destination choosers

- Move to…, Copy to…, Extract to…, and Send to… → device → Choose folder… open a folder chooser as a floating modal window over the originating window. lgse/strata#1384
- Invoking another destination command while one is open presents the existing chooser instead of opening a second. lgse/strata#1384 (unverified)
- Closing the originating window closes its chooser; Cancel leaves the files and the window's location unchanged. lgse/strata#1384
- For Send to, the sidebar and its toggle are hidden, and Ctrl+B or Ctrl+N in 10xer mode leaves the sidebar hidden. Navigating outside the device shows "Choose an existing folder inside this removable device." lgse/strata#1384 (unverified)
- In Send to, a link on the device to a folder off the device stays listed. Opening it shows "Choose an existing folder inside this removable device." lgse/strata#1729
- Move to, Copy to, and Extract to offer New Folder. Enter in the path entry navigates; Ctrl+Enter in the file list or the action button confirms. lgse/strata#1384
- Send to disables New Folder in the menu, the toolbar, and Ctrl+Shift+N. lgse/strata#1384 (unverified)

## Design

[docs/portal-file-chooser.md](https://github.com/lgse/strata/blob/4b9a6ace71017888b3a2124d7d911c5c664cc767/docs/portal-file-chooser.md) carries the user-facing contract, installation, keyboard map, and local test tools.

- The chooser is local-only because the backend contract returns normalized `file://` URIs. Resolving GVfs locations to their FUSE paths is deferred (lgse/strata#176).
- Requests come from other applications, so strings, globs, and choices are bounded. Filter-list size is not treated as abuse: count and rule budgets warn instead of refusing, since refusal left uploads silently broken (lgse/strata#465, lgse/strata#498).
- The chooser reuses the browser view, sidebar, and preview drawer. Differences from the main window were treated as bugs and aligned (lgse/strata#384, lgse/strata#1163, lgse/strata#1195).
- The automatic first-row selection is a keyboard cursor, not a choice. Destination resolution ignores it, because callers such as Chromium persist the returned folder and the error compounds (lgse/strata#1137, lgse/strata#1015).
- Name holds only lossy UTF-8 text. The chooser records the exact name it filled from the filesystem and uses it while Name still shows that text unchanged (lgse/strata#1427, lgse/strata#1533).
- That check compares text, not an edited flag, so an edit that restores the text still targets the original. Rebuilding bytes from an edited name would be guesswork, so edits save literally (lgse/strata#1427).
- GTK emits no selection change when a click keeps the same row selected, and the Name cache ignores unchanged selections to keep typed names. So an explicit primary press on a file row clears the cache after the row's own handler runs. Focus and selection echoes still pass through the cache (lgse/strata#1785, lgse/strata#1786).
- Default-map Enter shares the confirm path of Open and the 10xer map. Routing only activation would still return one file, because List and Icons collapse the selection first (lgse/strata#1426, lgse/strata#1533).
- GTK's text focus handler selects all text on a plain focus grab. The chooser focuses Name without selecting, then selects the stem, also in the idle focus restore (lgse/strata#1897, lgse/strata#1898).
- The stem rule is rename's, so a Save name and a rename select the same part (lgse/strata#1898).
- `current_file` for a nonexistent file is accepted for Qt interoperability, though the specification describes existing files (lgse/strata#699).
- The backend is D-Bus activated and exits when idle. A request arriving during shutdown is refused rather than raced (lgse/strata#1200).
- Move to and Copy to reuse the floating chooser rather than a separate in-window picker. The in-window variant in lgse/strata#1377 was set aside for the floating build in lgse/strata#1383.
- The chooser's 10xer key map and command allowlist belong to `integration/10xer-mode`.
- The chooser keeps its sidebar steps for the dialog only and does not save them (lgse/strata#1606).
- A device chooser checks containment by path on the UI thread and where a folder really leads on a worker. Its listing, monitor, and search start only once that check places the folder inside the device (lgse/strata#1729).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-27 | lgse/strata#1898 | fix | Selected only the suggested name's stem in Save, at build, on present, and in the idle focus restore, which had selected it whole. |
| 2026-10-20 | lgse/strata#1786 | fix | Refilled Save names on clicks that keep a file selected, which GTK reports as no selection change. |
| 2026-10-17 | lgse/strata#1714 | fix | Yielded chooser shortcuts to an open reference and typed Space in the Name and location entries with a hit selected. |
| 2026-10-11 | lgse/strata#1570 | fix | Kept the selection on plain clicks in the chooser's showing preview; sidebar clicks still clear it. |
| 2026-10-10 | lgse/strata#1554 | fix | Delegated folder identity lookups so the chooser follows an open folder renamed or removed outside the app. |
| 2026-10-10 | lgse/strata#1539 | fix | Gave the chooser's preview divider a wide handle so the column beside it keeps its resize edge. |
| 2026-10-09 | lgse/strata#1533 | fix | Returned the whole selection on Enter, kept exact non-UTF-8 Save names, and kept requests open on filter Escape. |
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
| 2026-09-05 | lgse/strata#382 | fix | Moved Right on a file in Columns into the already open child column, and gave the chooser the same Right behavior. |
| 2026-09-05 | lgse/strata#385 | feat | Shared single-click and Quick preview behavior with the main window. |
| 2026-09-05 | lgse/strata#175 | feat | Added the FileChooser v4 backend with Open, Save, Save Files, filters, choices, and previews. |

## Known gaps

- Remote locations such as `smb://` cannot be browsed or returned, even when GVfs exposes a local FUSE path. lgse/strata#176
