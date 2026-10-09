---
title: Inline rename
status: shipped
origin: {issue: null, pr: lgse/strata#115}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [src/ui/browser/inline_edit.rs, src/ui/collection_edit.rs]
tests: [tests/e2e/scenarios/test_inline_renaming.py, tests/e2e/scenarios/test_rename_visibility.py, tests/e2e/mutations/rename-caret.patch]
docs: [docs/keyboard-navigation.md]
related: [operations/create, browser/selection]
---

## Summary

Renaming one file or folder in place, in Columns, List, and Icons, from the keyboard, a menu, or a slow second click. Covers the editor's validation, how it commits or cancels, Undo, and keeping the edited and renamed row inside the viewport.

## Behavior

### Starting a rename

- F2 or Ctrl+R on the focused item opens an inline name editor; Ctrl+R no longer refreshes, F5 does. lgse/strata#393
- Ctrl+R with Alt, Shift, or Super also held starts no rename. lgse/strata#393
- While a text field has focus, F2 and Ctrl+R go to the field and start no second rename. lgse/strata#393
- Choosing Rename from an item's context menu selects that item and opens its editor. lgse/strata#115 (unverified)
- Items in Trash have no Rename in the context menu. lgse/strata#499
- In the file chooser, the item menu's Rename and F2 open the same inline editor. lgse/strata#175, lgse/strata#393
- Properties' Rename button closes Properties and opens the inline editor, including for a filter result. lgse/strata#1155
- Clicking the name text of the only selected item again, after the double-click interval, opens the editor. lgse/strata#1042, lgse/strata#1265
- A quick double-click opens the item instead; a drag, a selection change, or Escape before the interval cancels the pending rename. lgse/strata#1042
- A slow click on the icon, row padding, another List column, or a chevron does not rename; in Icons only the caption band does. lgse/strata#1265
- Slow-click rename does not arm in file choosers, in Trash, with more than one item selected, or with a modifier held. lgse/strata#1042
- In Columns, clicking the name of the folder whose child column is open opens its editor instead of collapsing the column. lgse/strata#1265

### Editing

- A file's editor opens with the name before the last `.` selected; a folder's opens with the whole name selected. lgse/strata#567, lgse/strata#710
- A name whose only `.` is its first character, such as `.bashrc`, opens fully selected. lgse/strata#567 (unverified)
- Ctrl+A in the editor selects only the field's text; the pane selection stays on the edited item. lgse/strata#749
- Ctrl+1, Ctrl+2, Ctrl+3, and Ctrl+K reach the editor instead of switching view mode or opening global search. lgse/strata#914
- Typing a name containing `/` puts the field in the error style with the reason "Names cannot contain /". lgse/strata#445
- `.` or `..` shows "That name is reserved", and a spaces-only name shows "Enter a name". lgse/strata#445 (unverified)
- An empty field is not styled as an error. lgse/strata#30
- In Columns, the row's size badge is hidden while editing and returns when the editor closes. lgse/strata#443
- With a long name in a narrow Columns view, End, typing, and arrow keys keep the caret and extension visible. lgse/strata#591
- Editor text is centered in Icons and left-aligned in List and Columns. lgse/strata#1155

### Committing and cancelling

- Enter, Tab, or a click outside the field, including empty pane space or a sidebar place, commits a valid changed name. lgse/strata#567
- Keyboard focus leaving the field commits too, including when the window becomes inactive. lgse/strata#567, lgse/strata#686
- Clicking inside the field moves the caret and keeps editing. lgse/strata#115, lgse/strata#591
- Escape closes the editor and keeps the original name. lgse/strata#115, lgse/strata#567
- Committing an empty, invalid, or unchanged name closes the editor and leaves the item and its contents as they were. lgse/strata#567
- A click-away onto a sidebar place or another folder commits the rename and still navigates there. lgse/strata#619
- The committed name shows at once and does not flash back to the old name while the listing refreshes. lgse/strata#619
- When the rename fails, an "Unable to rename item" dialog explains why and the old name returns. lgse/strata#619
- Renaming onto an existing name overwrites nothing and reports "“name” already exists". lgse/strata#567 (unverified)
- Renaming a folder whose child columns are open keeps them open under the new path. lgse/strata#760
- Ctrl+Z after a rename restores the original name, keeping current contents and permissions. lgse/strata#1061
- When the original name is taken by then, Undo fails without overwriting and stays available for retry. lgse/strata#1061
- Ctrl+Shift+Z after undoing a rename applies it again. lgse/strata#1120

### Visibility

- Opening the editor on a row that is already fully visible does not scroll the listing. lgse/strata#619
- After a commit in Columns or List, the renamed item is selected and scrolled fully into the viewport, even when it now sorts elsewhere. lgse/strata#619
- When the renamed row is still fully visible after sorting, the listing does not scroll. lgse/strata#619
- Icons focuses and reveals a committed rename the same way. lgse/strata#1148
- Scrolling or clicking before the reveal finishes cancels it. lgse/strata#1148

## Design

[docs/keyboard-navigation.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/keyboard-navigation.md) states the commit rule: Enter, click-away, or focus loss commits; Escape or an invalid name keeps the original.

- Only Escape and an invalid name revert. Focus loss to another window commits by design, not as a regression (lgse/strata#686).
- Click-away first cancelled the edit (lgse/strata#115). It now commits, so new and existing items share one rename path (lgse/strata#566, lgse/strata#567).
- The rename is dispatched on idle, after GTK's focus walk. Refreshing the model inside that walk destroyed the focused row and froze List and Icons (lgse/strata#566).
- An edit is a lease on an entry's identity, not a row position. Rebinding the row to another item, unbinding, or cancelling revokes it (lgse/strata#1174).
- Labels show the submitted name until the refresh lists the new location. A failure or superseding operation restores the old name (lgse/strata#617, lgse/strata#619).
- The completion reveal runs per frame for up to 5 seconds. It restores the pre-refresh scroll value first, because model splices replace GTK's scroll anchor (lgse/strata#619).
- Columns can be wider than the viewport. The editor is narrowed to the visible slice so GTK scrolls the text inside it (lgse/strata#394, lgse/strata#591).
- Slow-click waits the GTK double-click interval and arms only on the name text, matching Finder (lgse/strata#1057, lgse/strata#1265).
- Ctrl+R was taken from Refresh rather than bound to two actions; F5 remains Refresh (lgse/strata#364).
- Undo restores only the name and location, never older contents or metadata. Batch rename and persistent history were out of scope (lgse/strata#1059).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
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

- F5 while editing discards the typed name, and in Columns F2 then does nothing on that item; the fix is unmerged. lgse/strata#1438, lgse/strata#1546
- Folder colors and custom icons stay on the old path after a rename; the fix is unmerged. lgse/strata#1452, lgse/strata#1546
- Typing `docs/note.txt` as a new file's name is rejected instead of creating the folder; the feature is unmerged. lgse/strata#1511, lgse/strata#1512
