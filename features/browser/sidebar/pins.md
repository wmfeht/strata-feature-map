---
title: Pinned folders
status: shipped
origin: {issue: null, pr: lgse/strata#67}
branch: null
reviewed_at: fd6327265eaa3266f8420fe8bd25e965146344b0
review: draft
code: [src/adapters/bookmarks.rs, src/ui/window/bookmarks.rs, src/ui/window/pinned_drop.rs, src/ui/window/pinned_drop/**, src/adapters/directory_validation.rs]
tests: [src/adapters/bookmarks/tests.rs, src/ui/window/bookmarks/tests.rs, src/ui/window/pinned_drop/tests.rs, src/adapters/directory_validation/tests.rs, tests/e2e/scenarios/test_sidebar_pinning.py, tests/e2e/fixtures/file_drag_source.py]
related: [operations/trash, operations/delete, browser/properties, integration/10xer-mode, operations/drag-and-drop, integration/portal-file-chooser, browser/sidebar/connect-to-server]
---

## Summary

The PINNED section of the sidebar: folders the user pins. They are stored in GTK's shared bookmarks file, `$XDG_CONFIG_HOME/gtk-3.0/bookmarks`, which Nautilus and GTK file choosers also read. Folders are pinned from the item menu, Properties, the `p` key, or by dragging them into a gap in PINNED.

## Behavior

### Pinning and unpinning

- With one folder outside Trash selected, the item context menu shows Pin to sidebar. It is insensitive for pinned folders, Home, and standard folders. lgse/strata#67, lgse/strata#457 (unverified)
- Properties for a folder shows Pin, or Unpin once it is pinned. Either action updates the sidebar and closes the dialog. lgse/strata#457
- Properties shows no pin control for files, Trash, or Home and the standard folders. lgse/strata#457
- Right-clicking a pinned row offers Unpin and Properties, plus Customize… for a local folder. lgse/strata#457, lgse/strata#1370
- In the default key map, with the file list focused and Type to search off, `p` pins the focused folder; Shift+p does not. Caps Lock+p acts as `p`. Files, Trash, and pinned or standard folders are ignored. lgse/strata#230, lgse/strata#1576 (unverified)
- Clicking a pinned remote location that is not mounted, such as an SMB share, mounts it and then opens it. lgse/strata#67

### Dragging folders in

- Dragging folders from Columns, Icons, or List into a PINNED gap pins them at that gap, in selection order. The pins survive a restart. lgse/strata#1690, lgse/strata#1692
- Gaps sit before the first pin, between pins, after the last pin, and in an empty section. lgse/strata#1690, lgse/strata#1692
- Dropping an already pinned folder into a gap adds no duplicate and leaves the order unchanged. lgse/strata#1690, lgse/strata#1692
- A multi-folder drag that includes pinned folders, Home, or standard folders adds only the others, in selection order. lgse/strata#1690
- Dragging a file, or a selection mixing files and folders, over a gap shows no insertion line, and releasing it pins and transfers nothing. lgse/strata#1692
- Holding Shift during a drag from Strata still pins the folder and moves nothing. lgse/strata#1692
- A Move-only drag from another application is rejected by the gaps; a Copy drag from it is accepted. lgse/strata#1692
- A folder dragged from another file manager shows the insertion line only once every item is confirmed to be a directory. lgse/strata#1692
- That check runs one metadata query at a time under a 2 s deadline that includes reading the drag payload. A timeout, a failure, or any non-folder rejects the whole selection. lgse/strata#1692
- A drop on a gap while that check is still running never falls through to a file transfer. lgse/strata#1692
- A trashed folder dragged from the Trash view, or an `http://` or `https://` link, is rejected with no insertion line and no probe of the link. lgse/strata#1692
- A drag-pinned folder is labelled with the entry's display name, as a menu pin is, such as a GVfs display name instead of the URI basename. lgse/strata#1692
- After another window unpins a gap's neighbour, a drop on that gap in a window that has not rebuilt lands beside the following pin, else the preceding one. With both gone it is rejected. lgse/strata#1692
- Directory symlinks and remote folders, such as SMB and SFTP shares, can be drag-pinned. Their locations are stored as spelled, not canonicalized. lgse/strata#1692
- Remote pins have gaps beside them, although their rows accept no file drops. lgse/strata#1692
- In the file chooser, a local folder dragged into a PINNED gap is bookmarked, not moved, and a remote folder is rejected before any probe. lgse/strata#1713
- A folder pin drag that crosses a row's edges and gap, or leaves a spring-loaded row for a gap, keeps one insertion target. lgse/strata#1713 (unverified)
- A folder pin drag keeps its target while the sidebar shrinks to the rail and back. lgse/strata#1713 (unverified)

### Display and order

- Pins appear under a PINNED heading in bookmarks-file order, labelled with the bookmark's label or else the folder name. lgse/strata#202 (unverified)
- With nothing pinned, the sidebar shows no PINNED heading, separator, or gap, in a browser window and in the file chooser. lgse/strata#1726
- With nothing pinned, dragging files or folders over the sidebar shows the empty PINNED section, and dropping a folder on its gap pins it. Leaving the sidebar hides it again. lgse/strata#1726
- A bookmark pointing at Home or a standard folder is not shown under PINNED, and keeps its line in the file. lgse/strata#202
- Dropping a pinned row on the upper or lower half of another pinned row moves it before or after that row. The new order is saved to the bookmarks file. lgse/strata#202
- While a pinned row is dragged over another pin, an accent line shows in the gap where it will land. lgse/strata#1713
- Dropping a pinned row, local or remote, into a PINNED gap moves it there without changing its label or contents, and saves the order. Either gap next to the row is a no-op. lgse/strata#1692
- The file chooser's sidebar lists only pins with local paths. lgse/strata#589 (unverified)
- In the file chooser, pinned rows offer Unpin, Customize…, and Properties, and can be reordered by drag; changes reach every window. lgse/strata#1713

### Shared bookmarks file

- Every pin, unpin, or reorder re-reads the bookmarks file first, so pins made in another Strata window or by Nautilus survive. lgse/strata#674
- A pin, unpin, or reorder in one window updates the PINNED section of every open Strata window. lgse/strata#1729
- A new window shows the pins Strata last read, then re-reads the bookmarks file in the background. lgse/strata#1729
- When another program changes the file between Strata's read and save, Strata rereads it and reapplies the change, at most twice more. lgse/strata#1729
- When the bookmarks file cannot be read or saved, an "Unable to update pinned folders" dialog appears and the shown pins stay unchanged. lgse/strata#674
- With `gtk-3.0/bookmarks` a user-owned symlink, as from a dotfiles manager, a pin, unpin, or reorder writes the link's target and keeps the link. lgse/strata#1455, lgse/strata#1544
- A dangling link, or one owned by another user, still shows "Unable to update pinned folders" and leaves the file unchanged. lgse/strata#1544 (unverified)
- The dialog's detail gives the localized refusal reason, such as a link to a missing target, rather than the raw error. lgse/strata#1544 (unverified)
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

- Pins live in GTK's bookmarks file, not in Strata's preferences, so other GTK applications share them ([docs/preferences.md](https://github.com/lgse/strata/blob/72b840e69d6f0df9d33fb5583e62a3a2944886a1/docs/preferences.md)).
- Saves follow the config-file symlink rules in `settings/preferences/storage`; before, any symlinked bookmarks file was refused (lgse/strata#1455, lgse/strata#1544).
- Each window used to rewrite the whole file from its startup snapshot, deleting pins made elsewhere (lgse/strata#647). Mutations now read the file, apply the change, save atomically, and adopt the result only after the save succeeds (lgse/strata#674). This preserves sequential edits, not simultaneous ones. Since lgse/strata#1729 each change is one job on a background writer that checks the file is unchanged just before its rename.
- Reading with `read_to_string` turned one bad byte into an empty list that the next pin overwrote, so the file is parsed as bytes (lgse/strata#648, lgse/strata#713).
- Pinning uses dedicated gaps, separate from row bodies, which stay file-transfer targets; the two drop targets are visually distinct (lgse/strata#1690). Before, pinning took two steps: the menu, then a drag into place.
- Drags from Strata carry a snapshot of locations, display names, and an all-folders flag, so hovering a gap needs no filesystem probe. Foreign drags are validated once per drag, shared by every gap, so hover never blocks ([docs/architecture.md](https://github.com/lgse/strata/blob/e0f73973926ff67e77c2c56cf288b7b7617bb2e5/docs/architecture.md), lgse/strata#1692).
- Move is accepted only from Strata's own drag sources, whose drag-end handlers never delete. A foreign Move completion could ask the source application to delete the originals (lgse/strata#1692).
- One query in flight and a 2 s deadline bound speculative work on foreign selections such as 100 SFTP folders. Cancelling a GIO query does not interrupt a kernel-blocked call (lgse/strata#1692).
- Each gap remembers both neighbours, because other windows do not watch the bookmarks file (lgse/strata#1692).
- A pinned row's drag payload is `pinned:<index>` into the stored list. The prefix keeps pins and built-in places apart, and the index keeps hidden standard-folder bookmarks in place (lgse/strata#202).
- Home and the standard folders report pin status Unavailable, so they cannot be pinned twice (lgse/strata#67). Where pinning can never apply, the control is hidden rather than insensitive, because some themes render insensitive labels unreadably (lgse/strata#438, lgse/strata#457).
- Deletion cleanup runs in the deletion provider, so it survives the originating window closing. It retries an etag conflict twice and notifies every sidebar through a shared watcher list (lgse/strata#1373).
- Cleanup acts only on confirmed deletions. It does not scan for missing paths, since unavailability is not evidence of deletion (lgse/strata#1372, lgse/strata#1373).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-17 | lgse/strata#1713 | fix | Let pin gaps supply row spacing and showed before/after accent lines while reordering places and pins, in the browser and the file chooser. |
| 2026-10-16 | lgse/strata#1692 | feat | Added insertion gaps to PINNED so dragged folders pin at the drop position and pins reorder through them. |
| 2026-10-02 | lgse/strata#1373 | fix | Removed pins of deleted or trashed folders and their descendants from the file and all sidebars. |
| 2026-09-10 | lgse/strata#713 | fix | Parsed the bookmarks file as bytes so one invalid label no longer drops every pin. |
| 2026-09-09 | lgse/strata#674 | fix | Re-read the shared bookmarks file before each change so other windows' and apps' bookmarks survive. |
| 2026-09-06 | lgse/strata#457 | fix | Offered Unpin in Properties and hid the pin control where pinning cannot apply. |
| 2026-09-03 | lgse/strata#202 | feat | Made pinned folders reorderable by drag and drop within PINNED. |
| 2026-08-31 | lgse/strata#67 | feat | Reflected pinned state in Properties and validated pinned locations on click so unmounted shares mount. |

## Known gaps

- Bookmarks another program changes reach open windows only when Strata next changes a pin or deletes an item. A new window also reads them. There is no file monitor. lgse/strata#647, lgse/strata#674, lgse/strata#1729
- When deleting a parent fails after removing some children, pins to those removed children are kept. lgse/strata#1372
