---
title: Tab session restore
status: shipped
origin: {issue: lgse/strata#1531, pr: lgse/strata#1532}
branch: null
reviewed_at: aee71335dfecd059b9af23efeac2ed52c43e3b19
review: draft
code: [src/ui/tabs_session.rs]
tests: [src/ui/tabs_session/tests.rs]
docs: [docs/preferences.md]
related: [settings/preferences, settings/preferences/storage, browser/navigation/startup-arguments, integration/file-manager-interface, devices/volumes/udiskie-unlock]
---

## Summary

A plain launch reopens the previous session's tab locations in strip order, with the previously active tab selected. It is for users who keep a working set of folders open across restarts. Settings → General → Startup → Restore open tabs turns it off.

## Behavior

### Saving

- Adding, selecting, closing, or reordering a tab, or navigating inside one, saves the window's tab locations to `$XDG_CONFIG_HOME/strata/tabs.toml`. lgse/strata#1532
- With several plain-launch windows open, `tabs.toml` holds the tabs of the window that changed most recently. lgse/strata#1532
- A tab on a URI with a password or auth parameters, such as `smb://user:secret@server/share`, is never written to `tabs.toml`. lgse/strata#1532
- A tab on a URI with only a user name, such as `smb://user@server/share`, is saved and restored. lgse/strata#1532 (unverified)
- Windows opened for a folder or file argument, a FileManager1 reveal request, or `--unlock-volume` never write `tabs.toml`, even when tabs are added in them. lgse/strata#1532
- Only tab locations are saved; selection, navigation history, and preview state are not restored. lgse/strata#1532

### Restoring

- Launching `strata` with no arguments, with a saved session and the toggle on, reopens the saved tabs in order with the saved active tab selected. lgse/strata#1531, lgse/strata#1532
- A folder or file argument, a FileManager1 reveal request, or `--unlock-volume` skips restore, and the next plain launch still restores the earlier session. lgse/strata#1532
- A saved local folder that no longer exists, or a relative path, is skipped; the other tabs still open. lgse/strata#1532
- Trashed-item children (`trash:///x`) and non-root Recent entries (`recent:///x`) are skipped, while `trash:///` and `recent:///` restore. lgse/strata#1532
- Camera roots such as `gphoto2://` are skipped, and so is every scheme other than `smb`, `sftp`, `ftp`, `ftps`, `dav`, `davs`, `trash`, `network`, and `recent`. lgse/strata#1532 (unverified)
- When a skipped entry precedes the active tab, the restored selection still lands on the saved active location. lgse/strata#1532
- When the saved active entry is itself skipped, the nearest kept tab to its left is selected. lgse/strata#1532 (unverified)
- An active index beyond the last restorable tab selects the last restored tab. lgse/strata#1532 (unverified)
- At most 32 tabs are restored; later entries are ignored. lgse/strata#1532 (unverified)
- With no `tabs.toml`, unparsable TOML, a `version` other than 1, or no restorable entry, the window opens one tab at the default directory. lgse/strata#1531, lgse/strata#1532

### Setting

- Settings → General → Startup → Restore open tabs is on by default and is stored as `restore_tabs` in settings.toml. lgse/strata#1532
- Turning Restore open tabs off deletes `tabs.toml` at once, and later plain launches open one tab at the default directory. lgse/strata#1532
- Searching Settings for "session", "reopen", or "startup" finds Restore open tabs. lgse/strata#1532 (unverified)

## Design

Issue lgse/strata#1531 asked for the working set to survive restarts. It rejected the Default directory, which covers one folder, and sidebar pins, which hold places rather than the current session.

- Restore runs only on a plain launch. Explicit targets keep their behavior and never overwrite the session, so Open file location cannot clobber saved tabs (lgse/strata#1531, lgse/strata#1532).
- Locations are validated on load. Invalid, credential-bearing, and transient ones are skipped, with a fallback to the default directory (lgse/strata#1531).
- Credential-bearing URIs are filtered before the write as well as on load, so secrets never reach disk (lgse/strata#1532).
- The session is a separate store from settings.toml, written with the same atomic temp-and-rename helper (lgse/strata#1532, `docs/preferences.md`).
- Saving hooks the existing add, select, close, reorder, and navigation paths, so the close guards are unchanged (lgse/strata#1531).
- The store carries `version = 1`; another version restores nothing (lgse/strata#1532).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-09 | lgse/strata#1532 | feat | Saved tab locations to `tabs.toml` and restored them on a plain launch, with a Startup toggle to opt out. |

## Known gaps

None known.
