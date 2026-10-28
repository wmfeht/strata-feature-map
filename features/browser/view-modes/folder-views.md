---
title: Per-folder sort and thumbnail size
status: shipped
origin: {issue: lgse/strata#1563, pr: lgse/strata#1565}
branch: null
reviewed_at: 86df474dc0e8352e0e2098637a017cc4c77a8c44
review: draft
code: [src/ui/preferences/folder_view_settings.rs, src/ui/preferences/folder_views.rs, src/ui/preferences/folder_views/**, src/app/browser/folder_sorts.rs]
tests: [src/ui/preferences/folder_views/tests.rs, src/app/browser/tests/folder_sorts.rs]
docs: [docs/preferences.md]
related: [browser/view-modes/sorting, browser/view-modes/icons, settings/preferences/storage, browser/folder-customization, integration/portal-file-chooser, integration/10xer-mode/file-verbs]
---

## Summary

Each local folder remembers the sort chosen in it and its Icons thumbnail size, in a state file outside `settings.toml`. Folders without their own values use a default sort and the default size, both set in Settings. With the switch off, `browser/view-modes/sorting` and `browser/view-modes/icons` describe how sorts and sizes set the defaults.

## Behavior

### Remembering values

- With Remember sort and icon size per folder on, choosing a sort field or direction in a local folder applies to that folder only. Other folders keep the default. lgse/strata#1563, lgse/strata#1565
- The sort menu, a List heading, and the 10xer sort chord all choose a sort this way. lgse/strata#1565
- A remembered sort survives leaving the folder, restarting, and opening new windows. lgse/strata#1563, lgse/strata#1565
- Moving the Icons slider in a folder keeps that size for it; another folder opens at the default size. lgse/strata#1563, lgse/strata#1565
- A value equal to the current default is not stored. Choosing the default sort clears the folder's saved sort, so it follows later default changes. lgse/strata#1563, lgse/strata#1565
- Saved values apply to that exact folder; subfolders do not inherit them. lgse/strata#1563, lgse/strata#1565
- A sort change in one window re-sorts every open column, tab, and window showing that folder at once. lgse/strata#1563, lgse/strata#1565
- Remote shares, Trash, Recent, Camera Photos, non-UTF-8 paths, and FUSE filesystems other than `fuseblk` are not remembered. lgse/strata#1563, lgse/strata#1565
- In such a folder the sort stays with the open column, and a changed Icons size lasts while the folder is shown. lgse/strata#1565
- Device order and Recency are never stored. lgse/strata#1565 (unverified)

### Settings

- Settings → General → Browsing has the switch "Remember sort and icon size per folder", on by default, saved as `remember_folder_views`. lgse/strata#1563, lgse/strata#1565
- Saved values stay stored but unused while the switch is off. Turning it back on drops saved values equal to the current defaults. lgse/strata#1565
- The Default sort row has a "Default sort" menu (Name, Size, Modified, Type) and a "Default sort direction" menu (Ascending, Descending). lgse/strata#1563, lgse/strata#1565
- Changing the default sort re-sorts every open folder without its own sort, in every window. With the switch on, it also drops saved sorts equal to the new default. lgse/strata#1565
- The "Forget all folder settings" row has a Clear button, insensitive while nothing is saved, that clears every saved value. lgse/strata#1565
- Clear also removes values another Strata process saved that this one has not merged yet. lgse/strata#1565
- Settings search finds the three rows by words such as "per folder", "default sort", and "reset". lgse/strata#1565 (unverified)

### Pane menus

- In a remembered folder, the sort menu shows "Make this the default sort" when the column's sort differs from the default. lgse/strata#1563, lgse/strata#1565
- "Reset to default sort" shows only when the folder has its own saved sort, and returns it to the default. lgse/strata#1563, lgse/strata#1565
- When the thumbnail slider differs from the default size, the popover shows "Make this the default size" and "Reset to default size". lgse/strata#1563, lgse/strata#1565
- Each of these actions closes its menu or popover. They are hidden in folders that are not remembered and while the switch is off. lgse/strata#1565

### Keys and limits

- A local folder is keyed by its absolute path. A folder on a removable drive is keyed by filesystem UUID and its path inside the drive. lgse/strata#1565
- Values on a removable drive survive unmounting and remounting it. lgse/strata#1565
- `fuseblk` drives, such as ntfs-3g and exfat-fuse, count as local. lgse/strata#1565
- At most 5,000 folders are kept, least recently used evicted first. Opening a folder counts as a use; re-sorting open columns does not. lgse/strata#1563, lgse/strata#1565

### Following file operations

- Renaming or moving a folder in Strata, including undo and redo, moves its values and those of folders inside it to the new path. lgse/strata#1563, lgse/strata#1565
- A Merge into an existing folder keeps that folder's own values; a move to a place that is not remembered drops them. lgse/strata#1565
- Values follow renames and moves whether or not the switch is on. lgse/strata#1565
- Moving a folder to Trash in Strata drops its values; Put back or undo restores them for the session. A permanent delete drops them. lgse/strata#1565
- On vfat, a folder the kernel renumbered in Trash still gets its values back on Put back or undo. On exFAT, it gets them back only if its inode number is unchanged. lgse/strata#1729
- Opening a deleted local folder drops its values only when its parent lists other entries and holds no mount points. A drive root keeps them. lgse/strata#1565

### Storage file

- Values live in `$XDG_STATE_HOME/strata/folder-views.toml`, never in `settings.toml` or in the folders themselves. lgse/strata#1563, lgse/strata#1565
- A slider drag produces one write, and pending changes are written when Strata or the portal chooser quits. lgse/strata#1565
- Writes land 500 ms after the last change, and refuse to follow a symlink in place of the file. lgse/strata#1565 (unverified)
- When another Strata process, such as the portal chooser, saves, this process merges those values instead of overwriting them, and open views follow. lgse/strata#1565
- Each process also follows a default sort and size another process saves to `settings.toml`, even while an unrelated save of its own is in flight. lgse/strata#1565, lgse/strata#1877
- An unsaved change of its own to any of the default sort, direction, or icon size keeps all three of this process's values. lgse/strata#1877 (unverified)
- A missing file starts empty, and the first change creates it. lgse/strata#1563, lgse/strata#1565
- An unreadable file, invalid TOML, or an unknown `version` loads no values and is never overwritten that session. lgse/strata#1563, lgse/strata#1565
- The first change in a browser window then shows the notice "Folder settings file can't be read" once. lgse/strata#1563, lgse/strata#1565
- Invalid entries or fields are skipped and valid ones kept; sizes outside 32 to 256 px are clamped. The next save drops the invalid rest. lgse/strata#1563, lgse/strata#1565
- A failed write keeps changes in memory, retries on the next change, and shows "Folder settings can't be saved" once per failure streak. lgse/strata#1565

## Design

[docs/preferences.md](https://github.com/lgse/strata/blob/442d325be108ff95391f0fe76cbd89da8db9e129/docs/preferences.md#per-folder-sort-and-thumbnail-size) documents per-folder sort and thumbnail size. Before this, the last sort chosen anywhere became the global default and reordered every folder (lgse/strata#1563).

- One versioned state file was chosen because `settings.toml` is often kept in dotfiles (lgse/strata#1563).
- Rejected stores: hidden per-folder files, which pollute folders and repositories; SQLite, a bundled C dependency for a few thousand records; one file per folder; and GIO metadata, which depends on `gvfsd-metadata` (lgse/strata#1563).
- View mode per folder was rejected because switching layouts while browsing Columns is jarring. Inheriting a parent's values was deferred; exact matching is predictable and cheap (lgse/strata#1563).
- Only differences from the defaults are stored, so a folder follows later default changes (lgse/strata#1563).
- Thumbnails decode once at 256 px, so a per-folder size never re-decodes (lgse/strata#1563, lgse/strata#1565).
- Only chosen sorts are saved. A followed sort, from a saved value, the default, or a re-sync, saves nothing, so a re-sync never reverts another window's choice (lgse/strata#1565).
- The portal chooser is a separate process. Saves therefore merge first and lock the state directory, closing the lost-update window (lgse/strata#1565).
- Relocation follows the folder-color rules for Merge, Trash, and undo, but the storage is separate from `browser/folder-customization` (lgse/strata#1565).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-11 | lgse/strata#1565 | feat | Remembered sort and Icons size per folder, with a default sort, reset actions, and app-wide Folders first. |

## Known gaps

None known.
