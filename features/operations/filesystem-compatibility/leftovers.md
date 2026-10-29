---
title: Leftovers after a crash or unplug
status: shipped
origin: {issue: lgse/strata#1590, pr: lgse/strata#1729}
branch: null
reviewed_at: 86df474dc0e8352e0e2098637a017cc4c77a8c44
review: reviewed
code: [src/adapters/local_operations/leftovers.rs, src/app/browser/leftovers.rs, src/ui/browser/leftovers.rs]
tests: [src/adapters/local_operations/tests/leftovers.rs, src/app/browser/tests/leftovers.rs, src/ui/browser/leftovers/tests.rs]
related: [operations/clipboard/conflicts, operations/archives, operations/delete]
---

## Summary

Recognising the hidden `.strata-*` names a crash, kill, or unplug leaves in a folder, and offering to restore what may be the user's data. A pane-header button and a dock card open a review with Restore, Show, and Delete…. Strata removes nothing on its own except its own stale empty probes.

## Behavior

### Detection

- A folder holding `.strata-originals-*`, `.strata-merge-*`, `.strata-copy-*`, `.strata-extraction-*`, or older builds' hidden names gets a pane-header button. lgse/strata#1729
- The icon-only button is labelled "Items left by an interrupted operation". lgse/strata#1729
- The button shows in every column in Columns and in the List and Icons pane, and opens the review. lgse/strata#1729
- A name counts only as a known prefix followed by a UUID, so `.strata-copy-notes` is an ordinary file. lgse/strata#1729
- Older `.strata-compression-` and `.strata-replacement-` names also count with a 6-character suffix, such as `.strata-replacement-ab12Cd`. lgse/strata#1729
- While an operation of this Strata process changes the folder, no leftover button, card, or Restore shows for its hidden names. They appear when it ends. lgse/strata#1729
- `.nfs…`, `.fuse_hidden…`, and `.__smbfile_silly…` files never count as leftovers. lgse/strata#1729
- The portal file chooser, Trash, and Recent show no leftover button. lgse/strata#1729
- The first time per session a shown folder holds possible originals, a dock card reads "“%{folder}” holds originals that an interrupted operation set aside." with Review. lgse/strata#1729
- Review on the card opens the folder when it was closed meanwhile; its header button then opens the review. lgse/strata#1729
- The card closes after 15 s unless pinned. A folder holding only an incomplete copy shows the button but no card. lgse/strata#1729
- With hidden files shown, the context menu of a single originals, merge, or older-build leftover row offers Restore. lgse/strata#1729

### Review

- The review lists each item with its kind, contents, date, and hidden name, above "Another program or computer may still be using these items. Restore never replaces an existing item." lgse/strata#1729
- The review's item list has square corners at corner roundness 0, 1.8px corners at the default 60, and 6px at 200. lgse/strata#1906, lgse/strata#1908
- Originals and merge folders, older builds' originals, and possible originals offer Restore and Show. Incomplete copies offer Show and Delete…. lgse/strata#1729
- An item still held open by another program, or gone, shows no Restore; a gone item reads "No longer here". lgse/strata#1729
- Show reveals the item and turns hidden files on. lgse/strata#1729
- An incomplete copy reads "A copy that never finished. Its source was not changed." lgse/strata#1729
- Restore puts originals back under their own names, selects them, and removes the emptied hidden folder. It adds nothing to Undo. lgse/strata#1729
- A name taken meanwhile gets the next Keep Both number, such as `song (1).flac`, listed under "This name was already taken", or "These names were already taken" for several. lgse/strata#1729
- An older build's flat hidden name restores as "Recovered item", numbered if taken, with the name editor open. lgse/strata#1729
- Delete… runs the usual confirmed Delete, to Trash where the folder has one. lgse/strata#1729
- Restore or Delete… while an operation runs in the folder reports "Wait for the running operation to finish, then try again." Show still works. lgse/strata#1729
- On a read-only ntfs3 volume, Restore reports "The drive is read-only. It may need to be checked for errors after it was unplugged without being ejected." lgse/strata#1729
- On GVfs locations, an originals or merge folder offers no Restore. lgse/strata#1729

### Stale probes

- An empty `.strata-probe-*` file or folder over 1 hour old in a listed folder is removed in the background; errors are ignored. lgse/strata#1729
- Each folder and name is swept once per session. lgse/strata#1729
- A probe modified within the last hour stays. lgse/strata#1729

## Design

- Current builds leave five kinds of hidden names: probe, copy, extraction, originals, and merge. The name alone says what each holds (lgse/strata#1729).
- A stage only ever holds a copy. An original set aside sits in `.strata-originals-<id>/` under its own name, so Restore needs nothing but the folder (lgse/strata#1729).
- Leftovers are recognised from the listing Strata already makes, with no extra file call, so a folder nobody opens is never checked (lgse/strata#1729).
- Owner decisions: Delete… only for incomplete copies, confirmed, through the normal Delete; a pane-header button plus one card per session (lgse/strata#1729).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |

## Known gaps

- Leftovers in a folder nobody opens stay. lgse/strata#1729
- Leftovers at visible names, such as a reserved-name placeholder or a cut-off restore copy, carry no marker. lgse/strata#1729
- Another process's live hidden names can show as leftovers. lgse/strata#1729
- On vfat, a probe written in another time zone can look up to 26 h old and be removed while live. lgse/strata#1729
