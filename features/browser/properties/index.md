---
title: Properties dialog
status: shipped
origin: {issue: lgse/strata#71, pr: lgse/strata#243}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: reviewed
code: [src/ui/browser/properties.rs]
tests: []
docs: []
related: [browser/sidebar, operations/rename, integration/open-with, settings/preferences/date-format]
---

## Summary

The modal Properties dialog for one file, one folder, or the current folder: location, size, modification date, default application, hidden and pinned state, editable permissions, and Open, Rename, Pin, and Copy path actions. Children: `browser/properties/size` (folder and selection sizes and counts), `browser/properties/media` (audio, video, and image details), and `browser/properties/raw-metadata` (camera RAW details).

## Behavior

### Opening and closing

- Choosing Properties from an item's context menu opens the dialog for that item. lgse/strata#457
- Alt+Enter with one item selected opens Properties for the focused item. lgse/strata#1130
- Properties in the empty-space menu opens the dialog for the current folder. lgse/strata#558
- The empty-space menu hides Properties in Recent, and the current-folder dialog never opens there. lgse/strata#1083 (unverified)
- Escape, the Close button, or a click on the backdrop closes the dialog. lgse/strata#107
- Closing the dialog returns focus to the previously focused item with its selection kept. lgse/strata#175, lgse/strata#666 (unverified)
- When the window is too narrow for the dialog, the actions stack vertically and the execute checkbox reads "Executable (+x)". lgse/strata#1155 (unverified)

### Details

- The header shows the item's icon and name, and the subtitle changes from "File" or "Folder" to the content-type description once it is read. lgse/strata#398 (unverified)
- MODIFIED never shows a relative time. With Relative set it reads, in English, "Sep 1, 2026, 2:30 PM"; with ISO 8601 or Long set it uses that format. lgse/strata#1264 (unverified)
- OPENS WITH shows the default application for the item's content type, or "—" when there is none. lgse/strata#398 (unverified)
- HIDDEN reads "Yes" for an item GIO reports as hidden, such as a dot-file, and "No" otherwise. lgse/strata#398 (unverified)
- PINNED reads "Yes" when the location is pinned in the sidebar. lgse/strata#457 (unverified)

### Permissions

- The PERMISSIONS header shows the mode in symbolic and octal form, such as `-rw-r--r--  644`. lgse/strata#243
- The Owner and Group rows show the owning user and group names, or "—" when GIO reports none. lgse/strata#243 (unverified)
- Owner, Group, and Others rows each have read, write, and execute buttons; clicking one toggles that bit. lgse/strata#243
- A permission button reads "r", "w", or "x" when its bit is set and "—" when clear. lgse/strata#243 (unverified)
- For files, checking "Allow executing file as a program (+x)" turns mode `644` into `755`. lgse/strata#243
- The execute checkbox is checked when any execute bit is set; unchecking it clears all three. lgse/strata#243 (unverified)
- Folders have no execute checkbox. lgse/strata#243 (unverified)
- While a change is applied, the permission buttons and execute checkbox are insensitive. lgse/strata#243 (unverified)
- If GIO rejects a change, the previous mode returns and an "Unable to change permissions" dialog shows the error. lgse/strata#243
- When the item's mode cannot be read, the permission buttons stay insensitive and show "—". lgse/strata#243 (unverified)

### Actions

- For a folder that is not pinned, Pin adds it to the sidebar and closes the dialog. lgse/strata#457
- For a pinned folder, the action reads Unpin, is sensitive, and removes the sidebar row before closing the dialog. lgse/strata#457
- Files, Trash locations, and standard places always in the sidebar show no Pin or Unpin action. lgse/strata#457
- Rename is hidden for Trash locations. lgse/strata#499 (unverified)
- Open opens the item and closes the dialog. lgse/strata#1012 (unverified)
- Copy path copies the shell-escaped native path with a trailing `/`, even for a file such as `/home/u/a.txt/`, and relabels the button "Copied". A non-native location copies its display path without the `/`. lgse/strata#230 (unverified)
- In the portal file chooser, closing Properties leaves the chooser open with the selection kept. lgse/strata#175
- In the portal file chooser, Properties omits Open and Pin. lgse/strata#175 (unverified)

## Design

The dialog is a modal layer over the blurred window, built once and filled in by one asynchronous `query_info` that does not follow symlinks.

- Pin is hidden, not insensitive, wherever pinning cannot apply. An insensitive Pin was unreadable in themes that dim insensitive labels, so unpinning looked impossible (lgse/strata#438, lgse/strata#457).
- Permission edits are optimistic: the grid updates at once and rolls back with an error dialog if GIO rejects `unix::mode`. One change runs at a time (lgse/strata#243).
- Lists may show relative dates, but Properties always shows an absolute Modified timestamp (lgse/strata#1264). The formats belong to `settings/preferences/date-format`.
- Narrow or scaled windows constrain the dialog to the available space, so actions stack rather than overflow (lgse/strata#1155).
- Permissions, Rename, and media details stay single-item; two or more selected items get the compact summary in `browser/properties/size` (lgse/strata#1099).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-04 | lgse/strata#243 | feat | Made the permission grid editable and added an execute checkbox for files. |

## Known gaps

None known.
