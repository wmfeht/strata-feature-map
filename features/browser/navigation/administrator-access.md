---
title: Administrator access
status: shipped
origin: {issue: lgse/strata#1836, pr: lgse/strata#1837}
branch: null
reviewed_at: 44bfeab305cfb68993bafcf4794fe0bbf7ff1433
review: draft
code: []
tests: [src/app/browser/tests/administrator.rs]
docs: [docs/administrator-access.md]
related: [browser/navigation/location-bar, browser/view-modes, browser/view-modes/columns, browser/thumbnails, browser/context-menu, browser/selection/keyboard-navigation, browser/tabs/session-restore, operations/trash, operations/undo, operations/clipboard/conflicts, integration/open-with, integration/portal-file-chooser, app/accessibility]
---

## Summary

Opening local folders the user can't read or enter through GVfs's `admin://` backend, after a polkit prompt, as GNOME Files does. It covers marking such folders, redirecting opens to `admin://`, offering Open as Administrator on permission errors, and silent refusals. Strata itself never runs as root.

## Behavior

### Marking

- A local folder the user can't read or enter, such as a root-owned `0700` folder, is marked locked with a lock icon. lgse/strata#1837
- A folder link to such a folder is marked locked too. lgse/strata#1837 (unverified)
- The check uses `access(2)`, so a folder readable only through an ACL is not marked. lgse/strata#1837
- The lock icon shows even where GIO has no `admin` scheme. lgse/strata#1837 (unverified)

### Opening

- Where GIO supports `admin`, opening a locked folder switches the tab to its `admin://` form, such as `admin:///run/media/user/drive/backups`. lgse/strata#1837
- Opening means the view's opening click (one click in Columns by default), Enter, →, or the context menu's Open. lgse/strata#1837
- The polkit prompt appears while the current folder stays open; the tab switches only after the first read succeeds. lgse/strata#1837
- A path with spaces, `%`, or non-UTF-8 bytes is percent-escaped in its `admin://` form. lgse/strata#1836, lgse/strata#1837
- Moving the selection onto a locked folder with the arrow keys raises no polkit prompt. lgse/strata#1837
- Where GIO supports `admin`, a typed path to an unreadable folder shows the permission error dialog with an Open as Administrator button. lgse/strata#1837
- A sidebar place, bookmark, pin, or command-line argument to an unreadable folder offers the same button in its dialog, column, or pane. lgse/strata#1837 (unverified)
- Open as Administrator opens the folder's `admin://` form. lgse/strata#1837
- Where GIO has no `admin` scheme, no dialog, column, or pane offers Open as Administrator. lgse/strata#1837
- A folder peek of an unreadable folder offers no Open as Administrator. lgse/strata#1837 (unverified)
- Typing `admin:///path` in the location bar opens that folder as administrator. lgse/strata#1837

### Refusals

- Cancelling or refusing the polkit prompt leaves the previous folder open and shows nothing. lgse/strata#1837
- A mount of an `admin://` location that fails with permission denied is treated like a cancel. Strata never shows its own username and password form for `admin://`. lgse/strata#1837

### Browsing as administrator

- In an `admin://` folder, the breadcrumbs start at an "Administrator" crumb with a lock icon instead of `admin:`. lgse/strata#1837

## Design

[docs/administrator-access.md](https://github.com/lgse/strata/blob/44bfeab305cfb68993bafcf4794fe0bbf7ff1433/docs/administrator-access.md) describes entering, what GVfs does, browsing as root, and what is disabled on purpose.

- Only an explicit open prompts. Columns previews the selected folder, so prompting on selection would let arrow keys raise password prompts. GNOME Files behaves the same (lgse/strata#1836).
- Validation runs the first `admin://` operation, so polkit prompts before the current folder is replaced (lgse/strata#1837).
- GVfs reports a dismissed or refused prompt as `PERMISSION_DENIED`, not as cancelled. The prompt comes from the session's polkit agent, not from `GMountOperation`, so Strata needs no password form (lgse/strata#1836).
- Polkit authorizes each operation for about five minutes. A first visit may therefore prompt twice: once for the `gvfsd-admin` helper and once for the first read (lgse/strata#1836).
- Access is read-write from the start, because writes already use the GIO paths Strata uses for SFTP and SMB (lgse/strata#1836).
- Lock marking uses `access(2)` rather than mode bits, so ACLs count (lgse/strata#1837).
- Running Strata as root, or through `pkexec strata`, was rejected as unsafe for a GUI and unlike other file managers (lgse/strata#1836).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-29 | lgse/strata#1837 | feat | Opened unreadable local folders through `admin://` after a polkit prompt, so root-owned folders on external drives can be browsed. |

## Known gaps

- Strata can't unmount its `admin://` mount: it is private to the process and invisible to GIO's volume monitor. GVfs drops it when Strata exits. lgse/strata#1837
