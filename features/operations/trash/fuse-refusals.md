---
title: FUSE mounts that refuse Trash
status: shipped
origin: {issue: null, pr: lgse/strata#1614}
branch: null
reviewed_at: 86df474dc0e8352e0e2098637a017cc4c77a8c44
review: reviewed
code: [src/adapters/trash_support.rs]
tests: [src/adapters/trash_support/tests.rs]
related: [operations/filesystem-compatibility]
---

## Summary

Recognising a FUSE mount, such as sshfs, rclone, s3fs, or mergerfs, that reports Trash support but refuses the trash move partway. A confirmed refusal counts as "Trash unsupported", is remembered for that mount until Reload, and the empty Trash folders the attempt left are removed. The dialogs it leads to are the parent's (`operations/trash`).

## Behavior

### Classifying a refusal

- On a FUSE mount, including `fuseblk`, a trash move failing with permission denied, failed, or invalid argument counts as Trash unsupported. lgse/strata#1614
- So does an error writing the `.trashinfo` file, other than a full disk, a missing path, a read-only mount, or a name too long. lgse/strata#1614
- It counts only while the item is still present and the mount root answers `stat`. lgse/strata#1614
- The parent must also be off the home device, and the user must be allowed to remove the item. lgse/strata#1614
- On other local disks, only a not-supported error counts as Trash unsupported. lgse/strata#1614
- A disconnected FUSE mount, whose root `stat` fails, keeps the raw error instead of "doesn't support Trash". lgse/strata#1614

### Remembering a refusal

- After a counted refusal, the mount is remembered in every window, keyed by mount instance; a remount starts fresh. lgse/strata#1614
- After that failed delete, the parent folders reload, and the next Delete there opens the explained dialog without a trash attempt. lgse/strata#1614
- A folder on a FUSE mount that already refused Trash lists `access::can-trash` false, so Move to Trash is hidden there until Reload. lgse/strata#1614
- F5 forgets every remembered mount, so the next Delete tries Trash again. lgse/strata#1614
- The pane refresh button, the folder menu's reload, and F5 in the file chooser also forget them. lgse/strata#1614 (unverified)

### Cleanup

- After a batch whose trash moves on a FUSE mount were refused as unsupported, new empty `.Trash-$uid` or `.Trash/$uid` folders are removed from its root. lgse/strata#1614
- That cleanup is skipped on a mount where any item in the batch was trashed. lgse/strata#1614
- Cleanup never recurses, and leaves a Trash folder that existed before the batch, holds anything, or is a symlink. lgse/strata#1614 (unverified)

## Design

GIO reports `can-trash` on writable FUSE roots, so a refusal shows only mid-attempt (lgse/strata#1614).

- `access()` is not trusted, because sshfs answers success without `default_permissions`; mode and sticky bits are read (lgse/strata#1614).
- The check creates nothing and runs off the main thread (lgse/strata#1614).
- A refusal is remembered per mount instance so a remount retries, and Reload clears every record rather than probe a possibly hung folder (lgse/strata#1614).
- A failure in the home Trash says nothing about the mount, so items on the home device are excluded (lgse/strata#1614).
- The dialog's mount sentence looks only at the path as shown, so the main thread never touches a possibly hung mount. The classifier and cleanup resolve the real mount off the main thread (lgse/strata#1614).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |

## Known gaps

- A persistent or per-mount "Use Trash" setting, and recovery declared by a provider, are deferred. lgse/strata#1614
