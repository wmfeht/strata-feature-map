---
title: Inline rename
status: shipped
origin: {issue: null, pr: lgse/strata#115}
branch: null
reviewed_at: fd6327265eaa3266f8420fe8bd25e965146344b0
review: draft
code: [src/ui/browser/inline_edit.rs, src/ui/collection_edit.rs]
tests: [tests/e2e/scenarios/test_inline_renaming.py, tests/e2e/scenarios/test_rename_visibility.py, tests/e2e/mutations/rename-caret.patch]
docs: [site/src/reference/keyboard-navigation.md]
related: [operations/create, browser/selection, operations/trash, browser/folder-customization, operations/filesystem-compatibility]
---

## Summary

Renaming one file or folder in place, in Columns, List, and Icons, from the keyboard, a menu, or a slow second click. Covers the editor's validation, how it commits or cancels, Undo, and keeping the edited and renamed row inside the viewport.

## Behavior

### Starting a rename

- Outside 10xer mode, F2 or Ctrl+R on the focused item opens an inline name editor; Ctrl+R no longer refreshes, F5 does. lgse/strata#393, lgse/strata#1308
- F2 or Ctrl+R with Alt, Shift, or Super also held starts no rename, and neither does Ctrl+F2. lgse/strata#393
- While a text field other than the pane filter has focus, F2 and Ctrl+R go to the field and start no second rename. lgse/strata#393
- With the pane filter focused, F2 or Ctrl+R opens the editor on the focused item. lgse/strata#393 (unverified)
- Choosing Rename from an item's context menu selects that item and opens its editor. lgse/strata#115 (unverified)
- In the file chooser, the item menu's Rename and F2 open the same inline editor. lgse/strata#175, lgse/strata#393
- Properties' Rename button closes Properties and opens the inline editor, including for a filter result. lgse/strata#1155
- Clicking the name text of the only selected item again, after the double-click interval, opens the editor. lgse/strata#1042, lgse/strata#1265
- A quick double-click opens the item instead; another click, a drag, any key press, or a selection change before the interval cancels the pending rename. lgse/strata#1042
- With Double click mode set, clicking a folder, pausing, then double-clicking it opens the folder and leaves no rename editor. lgse/strata#1265
- A slow click on the icon, row padding, another List column, or a chevron does not rename; in Icons only the caption band does. lgse/strata#1265
- Slow-click rename does not arm in file choosers, in Trash, with more than one item selected, or with a modifier held. lgse/strata#1042
- In Columns, clicking the name of the folder whose child column is open opens its editor instead of collapsing the column. lgse/strata#1265

### Editing

- A file's editor opens with the name before the last `.` selected; a folder's opens with the whole name selected. lgse/strata#567, lgse/strata#710
- A name whose only `.` is its first character, such as `.bashrc`, opens fully selected. lgse/strata#567 (unverified)
- Ctrl+A in the editor selects only the field's text; the pane selection stays on the edited item. lgse/strata#749
- Ctrl+1, Ctrl+2, and Ctrl+3 reach the editor instead of switching view mode. lgse/strata#914
- Typing a name containing `/` puts the field in the error style and sets its accessible description to "Names cannot contain /"; no tooltip shows. lgse/strata#445, lgse/strata#1359
- For `.` or `..` the description is "That name is reserved", and for a whitespace-only name "Enter a name". lgse/strata#445 (unverified)
- An empty field is not styled as an error. lgse/strata#30
- In Columns, the row's size badge is hidden while editing. When the editor closes, it returns only with Show sizes in Columns view on and a size to show. lgse/strata#443, lgse/strata#1564
- With a long name in a narrow Columns view, End, typing, and arrow keys keep the caret and extension visible. lgse/strata#591
- Editor text is centered in Icons and left-aligned in List and Columns. lgse/strata#1155

### Committing and cancelling

- Enter, Tab, or a click outside the field, including empty pane space or a sidebar place, commits a valid changed name. lgse/strata#567
- Keyboard focus moving to another widget in the same window commits too. lgse/strata#567, lgse/strata#1714
- When another window or an input method switcher takes activation, the editor stays open and nothing is renamed. lgse/strata#1714
- Returning to the window keeps focus in the field, and Enter then commits. lgse/strata#1714
- Clicking inside the field moves the caret and keeps editing. lgse/strata#115, lgse/strata#591
- Escape closes the editor and keeps the original name. lgse/strata#115, lgse/strata#567
- Committing an empty, invalid, or unchanged name closes the editor and leaves the item and its contents as they were. lgse/strata#567
- A click-away onto a sidebar place or another folder commits the rename and still navigates there. lgse/strata#619
- The committed name shows at once and does not flash back to the old name while the listing refreshes. lgse/strata#619
- When the rename fails, an "Unable to rename item" dialog explains why and the old name returns. lgse/strata#619
- After a rename onto an existing name, Escape on that dialog returns focus to the old-name row. Up then moves the cursor. lgse/strata#1533
- Renaming onto an existing name overwrites nothing and reports "“name” already exists". lgse/strata#567 (unverified)
- A local rename never replaces an item created at the new name meanwhile. lgse/strata#1615
- A typed name the location would store as another, such as `x:y` or `notes.` on vfat, is refused before anything changes. lgse/strata#1615
- A refused character reads "Names in this location can’t contain “:”"; a trailing space or period reads "…can’t end with a space or a period". lgse/strata#1615
- A reserved name reads "“CON” is a reserved name in this location", and an overlong one "The name is too long". lgse/strata#1615
- A case-only rename, such as `notes.txt` to `Notes.txt`, succeeds on vfat, exFAT, SMB, casefold ext4, and exfat-fuse, and so does its undo. lgse/strata#1615
- Renaming an `smb://` item with no GVfs backend running fails with the backend's message instead of ending Strata. lgse/strata#1615
- Renaming a folder whose child columns are open keeps them open under the new path. lgse/strata#760
- With hidden files off, renaming a file to `.notes` completes, and F2 then starts a second rename at once. lgse/strata#1554, lgse/strata#1438
- Ctrl+Z after a rename restores the original name, keeping current contents and permissions. lgse/strata#1061
- When the original name is taken by then, Undo fails without overwriting and stays available for retry. lgse/strata#1061
- Undoing a rename never copies the item; where no placement step can place it, the undo is refused. lgse/strata#1615
- Ctrl+Shift+Z after undoing a rename applies it again. lgse/strata#1120

### Visibility

- Opening the editor on a row that is already fully visible does not scroll the listing. lgse/strata#619
- After a commit in Columns or List, the renamed item is selected and scrolled fully into the viewport, even when it now sorts elsewhere. lgse/strata#619
- When the renamed row is still fully visible after sorting, the listing does not scroll. lgse/strata#619
- Icons focuses and reveals a committed rename the same way. lgse/strata#1148
- Scrolling or clicking before the reveal finishes cancels it. lgse/strata#1148

## Design

[docs/keyboard-navigation.md](https://github.com/lgse/strata/blob/e0f73973926ff67e77c2c56cf288b7b7617bb2e5/docs/keyboard-navigation.md) states the commit rule: Enter, click-away, or focus moving away within the window commits; switching windows leaves the edit open; Escape or an invalid name keeps the original.

- Only Escape and an invalid name revert. Focus loss to another window first committed by design (lgse/strata#686).
- lgse/strata#1714 reversed that. GTK sends a focus leave when the window deactivates, including when an input method switcher grabs the keyboard. The edit now ends only on focus moves within the window, as the filter and location bar already did (lgse/strata#1714).
- Local renames go through the placement routine of `operations/filesystem-compatibility` instead of GIO's check-then-rename. A case-only rename takes two steps, with rollback, through a hidden name (lgse/strata#1615); since lgse/strata#1729 that is a `.strata-originals-<id>/` folder holding the item under its old spelling.
- Typed names are refused with the reason, never fixed (lgse/strata#1615).
- Click-away first cancelled the edit (lgse/strata#115). It now commits, so new and existing items share one rename path (lgse/strata#566, lgse/strata#567).
- The rename is dispatched on idle, after GTK's focus walk. Refreshing the model inside that walk destroyed the focused row and froze List and Icons (lgse/strata#566).
- An edit is a lease on an entry's identity, not a row position. Rebinding the row to another item, unbinding, or cancelling revokes it (lgse/strata#1174).
- Labels show the submitted name until the refresh lists the new location. A failure or superseding operation restores the old name (lgse/strata#617, lgse/strata#619).
- The completion reveal runs per frame for up to 5 seconds. It restores the pre-refresh scroll value first, because model splices replace GTK's scroll anchor (lgse/strata#619).
- Columns can be wider than the viewport. The editor is narrowed to the visible slice so GTK scrolls the text inside it (lgse/strata#394, lgse/strata#591).
- Slow-click waits the GTK double-click interval and arms only on the name text, matching Finder (lgse/strata#1057, lgse/strata#1265).
- Ctrl+R was taken from Refresh rather than bound to two actions; F5 remains Refresh (lgse/strata#364).
- Undo restores only the name and location, never older contents or metadata. Batch rename and persistent history were out of scope (lgse/strata#1059).
- A monitor started with hidden files off reports a rename to a dot name only as the old name's removal. The rename therefore completes once the old name leaves the listing (lgse/strata#1438, lgse/strata#1554).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-17 | lgse/strata#1714 | fix | Kept an inline rename open while the window is inactive, so switching input methods no longer commits it. |
| 2026-10-15 | lgse/strata#1675 | perf | Looked up each row's rename editor by list item instead of scanning every bound row on bind and unbind. |
| 2026-10-11 | lgse/strata#1564 | feat | Restored the Columns size badge after a rename only when Show sizes in Columns view is on. |
| 2026-10-10 | lgse/strata#1554 | fix | Finished renames to a dot name with hidden files off; they had blocked the next rename. |
| 2026-09-16 | lgse/strata#1061 | feat | Added single-item rename to the global Undo history. |
| 2026-09-16 | lgse/strata#1042 | feat | Added slow-click rename of an already-selected item in all views, following Finder and Explorer. |
| 2026-09-14 | lgse/strata#914 | fix | Let inline editing claim keys before window chords such as Ctrl+2 and Ctrl+K. |
| 2026-09-10 | lgse/strata#749 | fix | Scoped Ctrl+A to the rename field so it no longer selects every row. |
| 2026-09-09 | lgse/strata#710 | refactor | Separated Columns editor target resolution from activation. |
| 2026-09-09 | lgse/strata#683 | refactor | Split pending-rename transitions and reveal checks into focused helpers. |
| 2026-09-08 | lgse/strata#619 | fix | Kept submitted names visible until completion and revealed the renamed row in the viewport. |
| 2026-09-08 | lgse/strata#591 | fix | Constrained the Columns editor to the visible viewport so the caret stays on screen. |
| 2026-09-07 | lgse/strata#393 | feat | Added Ctrl+R as an alternate rename shortcut and left Refresh on F5 only. |
| 2026-09-06 | lgse/strata#443 | fix | Hid the Columns size badge while renaming so long names stay readable. |
| 2026-09-06 | lgse/strata#445 | fix | Flagged invalid names instead of aborting on a RefCell panic. |
| 2026-09-01 | lgse/strata#115 | fix | Cancelled a rename on click outside, which previously left the field open. |

## Known gaps

- Typing `docs/note.txt` as a new file's name is rejected instead of creating the folder; the feature is unmerged. lgse/strata#1511, lgse/strata#1512
- With fcitx5 through GTK's input method module, the first composed key replaces the preselected stem as a raw character; IBus is unaffected. lgse/strata#1715
