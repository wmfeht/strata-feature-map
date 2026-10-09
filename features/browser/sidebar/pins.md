---
title: Pinned folders
status: shipped
origin: {issue: null, pr: lgse/strata#67}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: reviewed
code: [src/adapters/bookmarks.rs, src/ui/window/bookmarks.rs]
tests: [src/adapters/bookmarks/tests.rs, src/ui/window/bookmarks/tests.rs]
related: [operations/trash, operations/delete, browser/properties, integration/10xer-mode]
---

## Summary

The PINNED section of the sidebar: folders the user pins. They are stored in GTK's shared bookmarks file, `$XDG_CONFIG_HOME/gtk-3.0/bookmarks`, which Nautilus and GTK file choosers also read.

## Behavior

### Pinning and unpinning

- With one folder outside Trash selected, the item context menu shows Pin to sidebar. It is insensitive for pinned folders, Home, and standard folders. lgse/strata#67, lgse/strata#457 (unverified)
- Properties for a folder shows Pin, or Unpin once it is pinned. Either action updates the sidebar and closes the dialog. lgse/strata#457
- Properties shows no pin control for files, Trash, or Home and the standard folders. lgse/strata#457
- Right-clicking a pinned row offers Unpin and Properties, plus Customize… for a local folder. lgse/strata#457, lgse/strata#1370
- With the file list focused and Type to search off, `p` or `P` pins the focused folder; files, Trash, and pinned or standard folders are ignored. lgse/strata#230 (unverified)
- Clicking a pinned remote location that is not mounted, such as an SMB share, mounts it and then opens it. lgse/strata#67

### Display and order

- Pins appear under a PINNED heading in bookmarks-file order, labelled with the bookmark's label or else the folder name. lgse/strata#202 (unverified)
- A bookmark pointing at Home or a standard folder is not shown under PINNED, and keeps its line in the file. lgse/strata#202
- Dropping a pinned row on the upper or lower half of another pinned row moves it before or after that row. The new order is saved to the bookmarks file. lgse/strata#202
- The file chooser's sidebar lists only pins with local paths, and its rows have no context menu or drag reordering. lgse/strata#589 (unverified)

### Shared bookmarks file

- Every pin, unpin, or reorder re-reads the bookmarks file first, so pins made in another Strata window or by Nautilus survive. lgse/strata#674
- When the bookmarks file cannot be read or saved, an "Unable to update pinned folders" dialog appears and the shown pins stay unchanged. lgse/strata#674
- A label with invalid UTF-8 is shown with U+FFFD, a line whose URI is invalid UTF-8 is skipped, and CRLF line endings are accepted. lgse/strata#713
- A line whose URI cannot be parsed, or that repeats an earlier location, is also skipped. lgse/strata#713 (unverified)
- A pin, unpin, or reorder rewrites the file from the parsed list. Skipped lines are dropped, and unlabelled bookmarks gain the folder name as label. lgse/strata#674 (unverified)
- A bookmark URI with a password or authentication parameters is kept with its username only, on load and on save. lgse/strata#145

### Deleted folders

- Deleting or trashing a folder in Strata removes its pin and every pin inside it from the file and from all open sidebars. lgse/strata#1373
- Items whose deletion failed or was cancelled keep their pins, as do pins on disconnected drives or unavailable network locations. lgse/strata#1373
- Restoring a folder, including with Ctrl+Z, does not restore its pins. lgse/strata#1373
- Deleting a symlink removes pins under the link's path and keeps pins to its target. lgse/strata#1373
- When the bookmarks file cannot be updated after a deletion, an error is reported and the deletion still counts as successful. lgse/strata#1373

## Design

- Pins live in GTK's bookmarks file, not in Strata's preferences, so other GTK applications share them ([docs/preferences.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/preferences.md)).
- Each window used to rewrite the whole file from its startup snapshot, deleting pins made elsewhere (lgse/strata#647). Mutations now read the file, apply the change, save atomically, and adopt the result only after the save succeeds (lgse/strata#674). This preserves sequential edits, not simultaneous ones.
- Reading with `read_to_string` turned one bad byte into an empty list that the next pin overwrote, so the file is parsed as bytes (lgse/strata#648, lgse/strata#713).
- A pinned row's drag payload is `pinned:<index>` into the stored list. The prefix keeps pins and built-in places apart, and the index keeps hidden standard-folder bookmarks in place (lgse/strata#202).
- Home and the standard folders report pin status Unavailable, so they cannot be pinned twice (lgse/strata#67). Where pinning can never apply, the control is hidden rather than insensitive, because some themes render insensitive labels unreadably (lgse/strata#438, lgse/strata#457).
- Deletion cleanup runs in the deletion provider, so it survives the originating window closing. It retries an etag conflict twice and notifies every sidebar through a shared watcher list (lgse/strata#1373).
- Cleanup acts only on confirmed deletions. It does not scan for missing paths, since unavailability is not evidence of deletion (lgse/strata#1372, lgse/strata#1373).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-02 | lgse/strata#1373 | fix | Removed pins of deleted or trashed folders and their descendants from the file and all sidebars. |
| 2026-09-10 | lgse/strata#713 | fix | Parsed the bookmarks file as bytes so one invalid label no longer drops every pin. |
| 2026-09-09 | lgse/strata#674 | fix | Re-read the shared bookmarks file before each change so other windows' and apps' bookmarks survive. |
| 2026-09-06 | lgse/strata#457 | fix | Offered Unpin in Properties and hid the pin control where pinning cannot apply. |
| 2026-09-03 | lgse/strata#202 | feat | Made pinned folders reorderable by drag and drop within PINNED. |
| 2026-08-31 | lgse/strata#67 | feat | Reflected pinned state in Properties and validated pinned locations on click so unmounted shares mount. |

## Known gaps

- A pin made in one window appears in other open windows only after they change a pin or Strata deletes an item; there is no file monitor. lgse/strata#647, lgse/strata#674
- When deleting a parent fails after removing some children, pins to those removed children are kept. lgse/strata#1372
