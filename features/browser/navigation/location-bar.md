---
title: Location bar and breadcrumbs
status: shipped
origin: {issue: lgse/strata#149, pr: lgse/strata#242}
branch: null
reviewed_at: aee71335dfecd059b9af23efeac2ed52c43e3b19
review: draft
code: [src/ui/browser/location.rs, src/ui/browser/location/**]
tests: [src/ui/browser/location/tests.rs, src/ui/browser/location/completion/tests.rs, src/app/browser/tests/location_input.rs, tests/e2e/scenarios/test_locations.py]
related: [remote/file-providers, integration/portal-file-chooser, integration/10xer-mode, operations/drag-and-drop]
---

## Summary

The header control that shows the active location as breadcrumbs and switches to a text entry for typing a path or URI. It covers path parsing, folder-name completion, revealing a typed file, and the breadcrumb hierarchy menu.

## Behavior

### Editing

- Ctrl+L replaces the breadcrumbs with an entry holding the current path, with the whole text selected. lgse/strata#316 (unverified)
- Clicking the current crumb, a separator, or empty breadcrumb space opens the entry; crumb buttons and the copy-path button keep their own actions. lgse/strata#316
- While editing, a click outside the entry and its buttons cancels the edit, restores the breadcrumbs, and still performs the click's normal action. lgse/strata#316
- Enter or the Navigate button opens the typed location; Escape or the Cancel button restores the breadcrumbs without navigating. lgse/strata#1132
- The entry and its buttons have the accessible names "Location (Ctrl+L)", "Navigate (Enter)", and "Cancel (Escape)". lgse/strata#1132
- While the entry has focus, Ctrl+K and Ctrl+1–3 reach the entry instead of opening search or switching view mode. lgse/strata#914
- A location that cannot be opened shows an "Unable to open location" dialog and the breadcrumbs return to the current path. lgse/strata#1206 (unverified)

### Typed paths

- `~` opens the home folder and `~/Documents` opens home's Documents, with leading and trailing spaces ignored. lgse/strata#242
- `~other-user/Documents` is rejected with "Only ~ and ~/ paths are supported for the current user's home directory." lgse/strata#242
- A relative path such as `Documents` is rejected with "Enter an absolute path." lgse/strata#242 (unverified)
- UNC paths (`\\host\share`, `//host/share`) and SCP addresses (`user@host:path`) are rejected with a message suggesting `smb://`, `sftp://`, `ftp://`, or `dav://` URIs. lgse/strata#20
- A URI scheme other than smb, sftp, ftp, ftps, dav, davs, trash, network, or recent is rejected with "The <scheme>:// scheme isn't supported." and a list that omits trash and network. lgse/strata#20 (unverified)
- Submitting `smb://alice:secret@host/share` or `smb://alice;password=secret@host/share` shows `smb://alice@host/share` in the entry while mounting and uses the password for that one attempt. lgse/strata#145
- A typed password is never saved; failed credentials open the normal sign-in dialog. lgse/strata#145
- Submitting a non-ASCII URI such as `smb://host/café` keeps the decoded text in the entry while mounting. lgse/strata#1424, lgse/strata#1533
- A submitted `smb://host/share/café x` is stored as `smb://host/share/caf%C3%A9%20x`, so creating or deleting an entry there refreshes the open column. lgse/strata#1424, lgse/strata#1533
- A path naming a file opens its parent folder with that file selected, in the main window and the portal file chooser. lgse/strata#1219
- If that parent is already open, the file is selected in place, after a refresh when the file is new. lgse/strata#1219
- A hidden file target turns on hidden files so the selection is visible. lgse/strata#1219
- A file target missing from the loaded parent shows an "Unable to select file" dialog. lgse/strata#1219

### Path completion

- While editing, a popover under the entry, matching its width, lists child folders whose names start with the typed absolute, `~/`, or relative path, ignoring case. lgse/strata#388
- A relative prefix completes against the current folder and inserts the folder's absolute path. lgse/strata#388 (unverified)
- Down and Up move through suggestions, wrapping at the ends, and Page Down and Page Up move by 5. lgse/strata#388 (unverified)
- Tab inserts the highlighted suggestion, the only suggestion, or a longer common prefix and closes the popover; Down reopens it. lgse/strata#388
- When Tab has nothing longer to insert, it highlights the next suggestion instead. lgse/strata#388 (unverified)
- Enter on a highlighted suggestion opens that folder. lgse/strata#388
- Escape cancels the edit even while suggestions are showing, closing the popover with it. lgse/strata#1206 (unverified)
- Hidden folders are suggested only when hidden files are shown or the typed name starts with `.`. lgse/strata#388 (unverified)
- The popover does not appear while the breadcrumbs are showing. lgse/strata#388
- Closing and reopening the editor shows no stale or flashing suggestion list. lgse/strata#1206

### Breadcrumbs

- Each ancestor crumb is a button that opens that folder. lgse/strata#316
- Right-clicking the breadcrumb bar opens a menu of the current folder and its ancestors, current first; choosing one opens it. lgse/strata#820
- For paths under home, the crumbs and the hierarchy menu start at `~`. lgse/strata#820 (unverified)
- When crumbs overflow, the wheel scrolls them horizontally and edge fades mark the hidden part. lgse/strata#820
- The overflow scrollbar sits in its own row below the crumbs, hidden at rest and shown on hover or scroll, never covering labels. lgse/strata#820
- Crumb labels longer than 32 characters are shortened in the middle. lgse/strata#1143
- The current crumb's Copy path button copies the path and shows a check and "Path copied" for 2 seconds. lgse/strata#316 (unverified)

## Design

The breadcrumbs and the entry are two pages of one stack; the entry is transient chrome.

- An outside click cancels rather than commits, because a half-typed or invalid path would navigate unexpectedly (lgse/strata#246).
- Every area showing the text cursor must start editing, so the edit target is the whole bar except crumb and copy-path buttons (lgse/strata#288).
- `~` expands only for the current user before absolute-path validation; other `~` forms stay errors (lgse/strata#149).
- UNC and SCP shorthand are refused rather than guessed, so a typed URI is never rewritten into another scheme (lgse/strata#20).
- A typed URI is stored in the percent-encoded form its listed children use, so refreshes reach the open column. The entry keeps the decoded text (lgse/strata#1424, lgse/strata#1533).
- URI credentials are parsed with GLib's password and auth-parameter flags (lgse/strata#111, lgse/strata#145). URI credentials leave the text at once. They reach only the pending mount with saving disabled, and are then discarded (lgse/strata#111, lgse/strata#145).
- A file path reuses validation: `NotDirectory` sends the parent through navigation with the file as a pending reveal, matching GTK and KDE choosers (lgse/strata#1139, lgse/strata#1219).
- Completion reads the local folder directly, scanning at most 10,000 entries and listing at most 50 folders (lgse/strata#388).
- Every exit path switches the stack to the breadcrumbs before resetting the text, so the entry's `changed` signal cannot reopen the popover (lgse/strata#1205).
- The scrollbar moved from an overlay inside the 22 px crumb row to its own row, after the shared fixed-scrollbar class still cropped labels (lgse/strata#297, lgse/strata#819).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-09 | lgse/strata#1533 | fix | Stored typed remote URIs in GIO's percent-encoded form so they match their listed children, keeping decoded text in the entry. |
| 2026-09-25 | lgse/strata#1219 | feat | Revealed a typed file path inside its parent instead of rejecting it as not a directory. |
| 2026-09-23 | lgse/strata#1132 | fix | Gave the entry and its confirm and cancel buttons accessible names. |
| 2026-09-22 | lgse/strata#388 | feat | Added folder completion under the entry with keyboard selection and Tab completion. |
| 2026-09-11 | lgse/strata#820 | fix | Moved the crumb scrollbar below the crumbs, added edge fades and a right-click hierarchy menu. |
| 2026-09-04 | lgse/strata#316 | fix | Made any non-button breadcrumb area start editing and an outside click cancel it. |
| 2026-09-04 | lgse/strata#309 | fix | Kept the breadcrumb scrollbar from growing on hover by reusing the fixed-scrollbar style. |
| 2026-09-04 | lgse/strata#242 | feat | Expanded `~` and `~/` and trimmed outer whitespace in typed locations. |
| 2026-09-01 | lgse/strata#145 | fix | Stripped credentials from typed URIs and used them for one mount attempt only. |

## Known gaps

- A typed path containing `..` is opened literally, so breadcrumbs show a `…/documents/..` crumb and Parent can move deeper; the fix is unmerged. lgse/strata#1445, lgse/strata#1546
