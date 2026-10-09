---
title: Properties dialog
status: shipped
origin: {issue: lgse/strata#71, pr: lgse/strata#243}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [src/ui/browser/properties.rs]
tests: [tests/e2e/scenarios/test_dialogs_and_menus.py]
docs: []
related: [browser/sidebar, operations/rename, integration/open-with]
---

## Summary

The modal Properties dialog for one file, one folder, or the current folder: location, size, modification date, default application, hidden and pinned state, editable permissions, and Open, Rename, Pin, and Copy path actions. Children: `browser/properties/size` (folder and selection sizes and counts), `browser/properties/media` (audio, video, and image details), and `browser/properties/raw-metadata` (camera RAW details).

## Behavior

### Opening and closing

- Choosing Properties from an item's context menu opens the dialog for that item. lgse/strata#457
- Alt+Enter with one item selected opens Properties for the focused item. lgse/strata#1130
- Properties in the empty-space menu opens the dialog for the current folder. lgse/strata#558
- The empty-space menu hides Properties in Recent, and the current-folder dialog never opens there. lgse/strata#1083 (unverified)
- Escape, the Close button, or a click on the backdrop closes the dialog and returns focus to the previously focused item with its selection kept. lgse/strata#666
- When the dialog is too small for its content, the actions stack vertically and the execute checkbox reads "Executable (+x)". lgse/strata#1155

### Details

- The header shows the item's icon and name, and the subtitle changes from "File" or "Folder" to the content-type description once it is read. lgse/strata#398 (unverified)
- MODIFIED always shows the full date, time, and year, never a relative time. lgse/strata#1264
- OPENS WITH shows the default application for the item's content type, or "—" when there is none. lgse/strata#398 (unverified)
- HIDDEN reads "Yes" for an item GIO reports as hidden, such as a dot-file, and "No" otherwise. lgse/strata#398 (unverified)
- PINNED reads "Yes" when the location is pinned in the sidebar. lgse/strata#457 (unverified)

### Permissions

- The PERMISSIONS header shows the mode in symbolic and octal form, such as `-rw-r--r--  644`. lgse/strata#243
- Owner, Group, and Others rows show the owning user and group names and r, w, and x buttons; clicking a button toggles that bit. lgse/strata#243
- For files, checking "Allow executing file as a program (+x)" turns mode `644` into `755`, and unchecking clears all three execute bits. lgse/strata#243
- Folders have no execute checkbox. lgse/strata#243 (unverified)
- While a change is applied, the permission controls are insensitive; if it fails, the previous mode returns and an "Unable to change permissions" dialog shows the error. lgse/strata#243
- When the item's mode cannot be read, the permission buttons stay insensitive and show "—". lgse/strata#243 (unverified)

### Actions

- For a folder that is not pinned, Pin adds it to the sidebar and closes the dialog. lgse/strata#457
- For a pinned folder, the action reads Unpin, is sensitive, and removes the sidebar row before closing the dialog. lgse/strata#457
- Files, Trash locations, and standard places always in the sidebar show no Pin or Unpin action. lgse/strata#457
- Rename closes the dialog and starts inline rename on the item, including on a filtered result. lgse/strata#1155
- Rename is hidden for Trash locations. lgse/strata#499 (unverified)
- Open opens the item and closes the dialog. lgse/strata#1012 (unverified)
- Copy path copies the shell-escaped native path with a trailing `/` and relabels the button "Copied"; this includes files. lgse/strata#230 (unverified)
- In the portal file chooser, Properties omits Open and Pin, and closing it leaves the chooser open with the selection kept. lgse/strata#175 (unverified)

## Design

The dialog is a modal layer over the blurred window, built once and filled in by one asynchronous `query_info` that does not follow symlinks.

- Pin is hidden, not insensitive, wherever pinning cannot apply. An insensitive Pin was unreadable in themes that dim insensitive labels, so unpinning looked impossible (lgse/strata#438, lgse/strata#457).
- Permission edits are optimistic: the grid updates at once and rolls back with an error dialog if GIO rejects `unix::mode`. One change runs at a time (lgse/strata#243).
- Lists may show relative dates, but Properties always shows the full Modified timestamp (lgse/strata#1264).
- Narrow or scaled windows constrain the dialog to the available space, so actions stack rather than overflow (lgse/strata#1155).
- Permissions, Rename, and media details stay single-item; two or more selected items get the compact summary in `browser/properties/size` (lgse/strata#1099).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-04 | lgse/strata#243 | feat | Made the permission grid editable and added an execute checkbox for files. |

## Known gaps

None known.
