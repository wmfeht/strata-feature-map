---
title: Delete error blockers and Show in Folder
status: shipped
origin: {issue: lgse/strata#2829, pr: lgse/strata#2837}
branch: null
reviewed_at: 53fbf4034631a59da34fa904a63e5d319ac5734d
review: draft
code: [crates/strata-fs/src/adapters/delete_blocker.rs, src/ui/browser/trash/delete_error.rs]
tests: [crates/strata-fs/src/adapters/delete_blocker/tests.rs, src/ui/browser/trash/delete_error/tests.rs, tests/qa/scenarios/entry_management/delete-failure-reveals-blocker.jsonl]
related: [operations/delete, operations/trash/fuse-refusals, app/dialogs, operations/progress/dock]
---

## Summary

When Move to Trash or a permanent delete fails on a nested entry, the error dialog names that entry and offers Show in Folder to reveal it. It is for users who must find the one file that keeps a folder in place. The error line's format is built by `operations/delete`; the dialog shell is `app/dialogs`'s.

## Behavior

### Naming the blocker

- Move to Trash of `to-delete` fails with `to-delete/nested/blocked.txt: Permission denied` when GIO refuses `nested/blocked.txt` and that file is itself not removable. lgse/strata#2829, lgse/strata#2837
- A listed entry is not removable when its folder lacks write or search permission, or the folder is sticky and the user owns neither. lgse/strata#2837 (unverified)
- When the entry GIO lists is removable, the error names its folder instead, such as `to-delete/nested: Permission denied`. lgse/strata#2837
- When that folder is the selected item itself, the error reads `to-delete: Permission denied` and offers no Show in Folder. lgse/strata#2837
- Move to Trash of `to-delete` holding a `chmod 000` folder `nested` fails with `to-delete/nested: Permission denied`. lgse/strata#2837
- The child is taken only from GLib's "Unable to trash child file" and "Error opening directory" messages with permission denied, and only when it lies inside the selected folder. lgse/strata#2837 (unverified)

### Show in Folder

- The "Completed with errors" dialog offers Show in Folder only when the blocker's path resolves within 2 s. lgse/strata#2837
- Resolving follows symlinks above the deleted folder but never a symlink from the deleted folder down. lgse/strata#2837
- The blocker itself may be a symlink; revealing it does not open it. lgse/strata#2837 (unverified)
- When a folder on the way to the blocker cannot be entered, Show in Folder reveals the nearest such folder instead. lgse/strata#2837
- In the `chmod 000` case, Show in Folder opens `to-delete` and selects `nested`. lgse/strata#2837
- Any other error resolving the path offers no Show in Folder. lgse/strata#2837 (unverified)
- When several items failed, the first blocker that still resolves is offered, and the button reads `Show “<name>” in Folder`. lgse/strata#2837
- With one failure, the button reads "Show in Folder". lgse/strata#2837
- Clicking it opens the blocker's folder in the tab and selects the blocker. lgse/strata#2837
- On a mount that stops answering, resolution gives up after 2 s and the failure is still reported, without Show in Folder. lgse/strata#2837
- The path is checked again on click; if it no longer resolves, an "Unable to open location" dialog reads "The item's location could not be verified." lgse/strata#2837 (unverified)
- If the tab navigated elsewhere before that check finished, the click does nothing. lgse/strata#2837 (unverified)
- A docked deletion's error dialog offers the same Show in Folder. lgse/strata#2837 (unverified)
- Revealing the blocker leaves it unchanged on disk. lgse/strata#2837 (unverified)

## Design

lgse/strata#2829 asked for the blocking path and reason, a Show in Folder for a path that resolves safely, and no change to permissions, no elevation, and no retry. lgse/strata#2837 keeps all three non-goals.

- Local GIO exposes the refused child only in its error text. Only GLib's own "Unable to trash child file %s" format, including the `%1$s` form, and the unlocalized "Error opening directory" text are matched, not any path a Trash backend mentions (lgse/strata#2837).
- A maintainer checked that "Error opening directory" stays untranslated under a French locale on GLib 2.90 (lgse/strata#2837).
- GIO names the first entry it lists in a folder the user does not own, removable or not. The folder is blamed unless that entry is blocked too (lgse/strata#2837).
- Reveal follows symlinks above the deleted folder, as the delete does, and never below it (lgse/strata#2837).
- Verification has a 2 s budget so a hung mount cannot suppress the failure report (lgse/strata#2837).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-11-27 | lgse/strata#2837 | fix | Named the nested entry that blocks a failed delete and offered Show in Folder for a verified path, since a bare folder name hid the cause. |

## Known gaps

- The blocker is resolved before the failure is reported, so on a stalled native mount the error dialog can wait up to 2 s, and a blocking thread stays stuck after the timeout. lgse/strata#2837
