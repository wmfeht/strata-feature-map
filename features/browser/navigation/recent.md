---
title: Recent
status: shipped
origin: {issue: lgse/strata#1082, pr: lgse/strata#1083}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: []
tests: [src/app/browser/tests/recent.rs, tests/e2e/scenarios/test_recent.py]
related: [browser/sidebar, integration/open-with, settings/preferences]
---

## Summary

The `recent:///` collection of recently used files, read from the desktop's GTK and GIO recent-file history. It is a browsable location whose rows act on the real files, opened from the sidebar Recent place or the location bar.

## Behavior

### Availability

- The sidebar shows Recent only when GTK recent files are enabled, GIO supports `recent://`, and "Show Recent in sidebar" is on. lgse/strata#1083
- "Show Recent in sidebar" defaults to on; turning it on cannot add Recent while the backend is missing. lgse/strata#1083
- Without the GVfs recent backend, typing `recent:///` or `recent://` shows "Unable to open location" saying the backend isn't installed, and the current folder stays open. lgse/strata#1083

### Listing

- Recent lists files with the most recently used first, sorted by Recency with folders-first off. lgse/strata#1083
- In Recent, the sort menu hides the Folders first option. lgse/strata#1083 (unverified)
- A history entry whose target file is missing or unreadable is skipped, not listed. lgse/strata#1150
- The Recency sort key is offered only in Recent, in both directions. lgse/strata#1083
- Changing the sort in Recent does not change the sort of ordinary folders. lgse/strata#1083
- An open Recent view reloads when the desktop's recent history changes. lgse/strata#1083
- Deleting or moving a file, from Recent or another pane, removes its row from an open Recent view at once. lgse/strata#1157
- Deleting more than 64 items in one operation reloads an open Recent view instead. lgse/strata#1157 (unverified)
- In Recent, Parent is unavailable, while Back and Forward still move to and from it. lgse/strata#1083

### Actions

- The item menu's Open, Open With…, Quick preview, Rename, Move to…, Move to Trash, Permanently delete, Properties, and Open file location act on each row's real file. lgse/strata#1083
- New File, New Folder, Paste, and dropping files into Recent are unavailable or rejected. lgse/strata#1083
- In Recent, the background menu also hides Open With…, Open in Terminal, and Properties. lgse/strata#1083 (unverified)
- In Recent, the item menu hides New Folder with Selection. lgse/strata#1083 (unverified)
- Launching a file in an application from Strata adds it to the desktop's recent history; folders are not added. lgse/strata#1083, lgse/strata#1150
- In Recent, the item menu offers Remove from Recent when every selected row has a recent-history entry. lgse/strata#1500
- Remove from Recent drops the selected rows from the history without a confirmation, leaves the files untouched, and persists across restarts. lgse/strata#1500
- Remove from Recent is absent from the same file's menu in its real folder. lgse/strata#1500

## Design

Recent uses the platform's recent-file infrastructure instead of a Strata-specific history, and stays separate from saved searches (lgse/strata#1082).

- Each row's location is its resolved target, so ordinary file actions need no Recent special case. The `recent://` URI is kept beside it only for removal (lgse/strata#1500).
- The collection root is not a writable directory, so actions that target the current folder are withheld (lgse/strata#1083).
- Removal deletes the `recent://` URI through GIO, guarded per URI against double requests. Failures are logged, and the next rescan reconciles the list (lgse/strata#1500).
- Only the removal side of a move fans out to Recent, because a moved file's new path is not a Recent member (lgse/strata#1157).
- Recent stays recent-use history: newly downloaded files that were never opened are not added (lgse/strata#1150).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-06 | lgse/strata#1500 | feat | Added Remove from Recent, deleting history entries without touching files. |
| 2026-09-23 | lgse/strata#1157 | fix | Removed deleted and moved files from an open Recent view without a reload. |
| 2026-09-17 | lgse/strata#1083 | feat | Added the Recent collection backed by the desktop's recent-file history. |

## Known gaps

- Recent has no Open Full Path action that opens a row's whole folder hierarchy as columns. lgse/strata#1475
- Recent entries whose names are not valid UTF-8 are not listed; the fix merged after this snapshot. lgse/strata#1424, lgse/strata#1533
- Renaming or moving a file in Strata does not update its recent-history URI, so it drops out of Recent. lgse/strata#1150
