---
title: Network folder change checks
status: shipped
origin: {issue: lgse/strata#1590, pr: lgse/strata#1729}
branch: null
reviewed_at: fd6327265eaa3266f8420fe8bd25e965146344b0
review: draft
code: [src/app/browser/freshness.rs, src/ui/presence.rs]
tests: [src/app/browser/freshness/tests.rs, src/ui/presence/tests.rs]
related: [settings/preferences, browser/view-modes, integration/portal-file-chooser, remote/file-providers/network-locations]
---

## Summary

Periodic checks of shown folders on mounts that other computers or programs change, where file monitors report nothing. A check re-reads the folder's change stamp and re-lists the folder when it moved. The **Watch network folders** setting turns the checks of network folders on or off.

## Behavior

### Which folders are checked

- With **Watch network folders** on, open folders on network and FUSE mounts are checked. That covers NFS, SMB, 9p, and virtiofs, but not `fuseblk`. lgse/strata#1729
- GVfs locations count as network folders too, except `admin://`, `mtp://`, and `gphoto2://`. lgse/strata#1729
- `trash:///` and Recent are never checked. lgse/strata#1729 (unverified)
- With **Watch network folders** off, those folders are never checked or re-listed; changes made on other computers show only after F5. lgse/strata#1729
- A local folder, or one on a mount other computers do not change, such as `fuseblk` or `mtp://`, is checked whatever the switch says while its monitor is not live. lgse/strata#1729
- Columns checks every open column; Icons and List check only the open folder. lgse/strata#1729
- A folder that shows a load error is not checked until it loads again. lgse/strata#1729

### Cadence

- Shown folders are checked every 3 s in a focused window and every 15 s in a window shown without focus. lgse/strata#1729
- Nothing is checked in a hidden, minimized, or compositor-suspended window, or in a tab that is not selected. lgse/strata#1729
- In power-saver mode, focused windows check every 12 s and unfocused windows stop checking. lgse/strata#1729
- After 20 unchanged checks in a row the interval doubles, and after 40 it is four times as long. lgse/strata#1729
- After a listing, the next check of that folder waits at least 10 times as long as the listing took. lgse/strata#1729
- Regaining focus checks shown folders at once. After 30 s or more away they are re-listed, which updates sizes and dates of files edited in place. lgse/strata#1729
- The portal file chooser checks the folders it shows by the same rules, following its own window. lgse/strata#1729

### What a check does

- A file created, deleted, or renamed on another computer in a checked folder appears or leaves at the next check, without F5. lgse/strata#1729
- On sshfs, changes made on the server show up to about 21 s late. lgse/strata#1729
- A check that finds the folder gone or replaced acts as a monitor's report: it follows a rename, reloads, or opens the nearest existing folder. lgse/strata#1729
- A check refused for permission re-lists the folder, so the pane shows the failure. lgse/strata#1729
- A check that fails with another error, such as `EIO` or `EHOSTDOWN`, keeps the listing and checks again 30 s later. lgse/strata#1729
- A folder whose check the backend does not support is not checked again. lgse/strata#1729 (unverified)
- When a mount answers again, a refresh kept on it while it was not answering runs again by itself, still keeping the rows. lgse/strata#1729
- A folder whose load failed while its mount was not answering loads again by itself once the mount answers. lgse/strata#1729
- A background re-list that fails, is refused, or stops at the load's time budget keeps the previous listing, with no error page. lgse/strata#1729
- A background re-list cut at the entry limit is shown, marked as cut. lgse/strata#1729
- A re-list waits while an inline rename is open or being submitted, and while a Strata operation changes or writes into the folder. lgse/strata#1729
- Where a folder's stamp stays put while names change, as on 9p with `cache=loose`, checked folders are re-listed instead, at most every 15 s. lgse/strata#1729

## Design

[docs/filesystem-compatibility.md](https://github.com/lgse/strata/blob/fd6327265eaa3266f8420fe8bd25e965146344b0/docs/filesystem-compatibility.md#changes-made-elsewhere) describes which folders are checked, the cadence, and what a check costs.

- The lab saw no inotify event for 300 changes made elsewhere over NFS, SMB, and sshfs. Monitors alone cannot show them (lgse/strata#1729).
- Every load starts with a forced `statx`, or a GIO query on GVfs. It records the folder's modification and change times, identity, and real mount. A check reads that stamp again (lgse/strata#1729).
- The change time moves even when `rsync -a` or `cp -a` puts a folder's modification time back (lgse/strata#1729).
- A check costs one 212 B `GETATTR` on NFSv3. An SMB folder 4 levels below the share costs about 5 compounds, 4.5 to 5.1 KB (lgse/strata#1729).
- Checks run as background work on the mount's request lane, one job per mount. A busy or stalled lane skips them rather than queuing (lgse/strata#1729).
- On whole-second mounts, a stamp read within its coarse window is confirmed once by a later re-list. On sshfs that waits 21 s, past the daemon's 20 s cache (lgse/strata#1729).
- The owner chose to check visible network folders at once on focus and re-read them after 30 s away (lgse/strata#1729, Q11).
- With the switch off, network folders without a working monitor, such as GVfs SMB and SFTP, go unchecked too. Off thus stops every network check (lgse/strata#1729).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |

## Known gaps

- On a Samba share with directory leases, a change made on the server itself stays hidden while the folder is shown, even after F5. It shows once the lease lapses, 46 to 66 s after its last use. Mounting with `nohandlecache` avoids it. lgse/strata#1729
- After a mount ends its stuck request with an error, as SMB does with `EHOSTDOWN`, "Not responding" stays until F5, Retry, or navigating. lgse/strata#1729
- A window on another workspace counts as hidden only where the compositor reports it suspended; elsewhere it keeps the 15 s interval. lgse/strata#1729
- On whole-second mounts, a server clock behind this computer's by more than the coarse window can hide a change. lgse/strata#1729
