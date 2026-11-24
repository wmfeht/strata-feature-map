---
title: Location bar and breadcrumbs
status: shipped
origin: {issue: lgse/strata#149, pr: lgse/strata#242}
branch: null
reviewed_at: ed544cf3bbb3968299ed8223148a65823739d48f
review: draft
code: [crates/strata-fs/src/app/browser/location_input.rs, crates/strata-fs/src/app/browser/location_input/**, src/ui/browser/location/breadcrumbs.rs]
tests: [crates/strata-fs/src/app/browser/tests/location_input.rs, tests/qa/scenarios/locations/breadcrumb-returns-to-parent.jsonl, tests/qa/scenarios/locations/named-location-controls.jsonl, tests/qa/scenarios/locations/typed-path-navigates.jsonl, tests/qa/scenarios/keyboard_navigation/list-typed-file-path.jsonl, tests/qa/mutations/location-entry.patch, tests/qa/scenarios/view_switching/leaving-columns-names-the-shown-folder.jsonl]
docs: [docs/keyboard-navigation.md]
related: [remote/file-providers, integration/portal-file-chooser, integration/10xer-mode, operations/drag-and-drop, app/accessibility, preview/quick-preview, browser/tabs, browser/view-modes/columns, browser/selection/keyboard-navigation]
---

## Summary

The header control that shows the active location as breadcrumbs and switches to a text entry for typing a path or URI. It covers path parsing, pasted shell paths and `file://` URIs, and revealing a typed file. It also covers the breadcrumb hierarchy menu and opening crumbs in a new tab or window. Child: `browser/navigation/location-bar/completion` (the folder suggestions under the entry).

## Behavior

### Editing

- Ctrl+L replaces the breadcrumbs with an entry holding the current path, with the whole text selected. lgse/strata#316 (unverified)
- Clicking the current crumb, a separator, or empty breadcrumb space opens the entry; crumb buttons and the copy-path button keep their own actions. lgse/strata#316
- Enter or the Navigate button opens the typed location; Escape or the Cancel button restores the breadcrumbs without navigating. lgse/strata#1132
- Escape in the entry restores the folder the breadcrumbs name. lgse/strata#2026
- With an input method composing in the location field, Escape cancels only the composition and the editor stays open. lgse/strata#1583
- The entry and its buttons have the accessible names "Location (Ctrl+L)", "Navigate (Enter)", and "Cancel (Escape)". lgse/strata#1132
- While the entry has focus, Ctrl+K and Ctrl+1–3 reach the entry instead of opening search or switching view mode. lgse/strata#914
- A location that cannot be opened shows an "Unable to open location" dialog and the breadcrumbs return to the current path. lgse/strata#1206 (unverified)
- Escape cancels the edit even while suggestions are showing, closing the popover with it. lgse/strata#1206 (unverified)
- Closing and reopening the editor shows no stale or flashing suggestion list. lgse/strata#1206
- A folder load that ends while the entry is open and focused, as in a new tab, leaves the entry open with its text. lgse/strata#1729

### Typed paths

- `~` opens the home folder and `~/Documents` opens home's Documents, with leading and trailing spaces ignored. lgse/strata#242
- `~other-user/Documents` is rejected with "Only ~ and ~/ paths are supported for the current user's home directory." lgse/strata#242
- `/home/a@b:c` is rejected with the UNC and SCP message. lgse/strata#2692
- A relative path such as `Documents` is rejected with "Enter an absolute path." lgse/strata#242 (unverified)
- UNC paths (`\\host\share`, `//host/share`) and SCP addresses (`user@host:path`) are rejected with a message suggesting `smb://`, `sftp://`, `ftp://`, or `dav://` URIs. lgse/strata#20
- Accepted URI schemes are file, smb, sftp, ftp, ftps, dav, davs, admin, trash, network, and recent. Any other is rejected with "The <scheme>:// scheme isn't supported." lgse/strata#20, lgse/strata#1837, lgse/strata#2692 (unverified)
- That message lists the accepted schemes except file, trash, and network. lgse/strata#20, lgse/strata#1837, lgse/strata#2692 (unverified)
- Typing `network:`, `network://`, or `network:///` opens the Network root. `trash:` and `trash://` open Trash, and `recent:` and `recent://` open Recent. Scheme case is ignored. lgse/strata#2030
- A typed `network://` names the location "Network" in the heading and breadcrumbs, as the sidebar does. lgse/strata#2030
- A virtual-root scheme followed by more than three slashes, or by text after them, is parsed as an ordinary URI. lgse/strata#2030 (unverified)
- Submitting a typed remote URI such as `sftp://host/served?tok=QTOKEN#frag` opens `sftp://host/served`. The user and port are kept. lgse/strata#2030
- A literal `?` or `#` in a remote name is typed as `%3F` or `%23`. Typed local paths keep `?` and `#`. lgse/strata#2030
- Submitting `smb://alice:secret@host/share` or `smb://alice;password=secret@host/share` shows `smb://alice@host/share` in the entry while mounting and uses the password for that one attempt. lgse/strata#145
- A typed password is never saved; failed credentials open the normal sign-in dialog. lgse/strata#145
- The sign-in dialog's fields are named after their visible labels: "Username", "Domain", and "Password" or "Passphrase". lgse/strata#1896 (unverified)
- Submitting a non-ASCII URI such as `smb://host/café` keeps the decoded text in the entry while mounting. lgse/strata#1424, lgse/strata#1533
- A submitted `smb://host/share/café x` is stored as `smb://host/share/caf%C3%A9%20x`, so creating or deleting an entry there refreshes the open column. lgse/strata#1424, lgse/strata#1533
- Ctrl+L with `<dir>/sub/../other` opens `<dir>/other`, and the breadcrumbs show no `..` crumb; Alt+Up then opens `<dir>`. lgse/strata#1445, lgse/strata#1570
- `~/../` and `~/a/../b` resolve `..` the same way. lgse/strata#1570
- `.` and `..` resolve as text without a filesystem check: `/missing/../tmp` opens `/tmp`, and `..` stops at `/`. lgse/strata#1570
- A file path through `..`, such as `<dir>/a/../report.pdf`, selects the file in its folder. lgse/strata#1570
- A URI keeps its `.` and `..` segments as typed. lgse/strata#1570 (unverified)
- A path naming a file opens its parent folder with that file selected, in the main window and the portal file chooser. lgse/strata#1219
- If that parent is already open, the file is selected in place, after a refresh when the file is new. lgse/strata#1219
- Enter on a typed file path focuses the file and opens Quick Preview on it, whether or not its parent was already open. lgse/strata#1912
- The portal file chooser opens its preview drawer on a typed file path the same way. lgse/strata#1912 (unverified)
- That preview opens even after the user dismissed Quick Preview. lgse/strata#1912 (unverified)
- With Quick Preview closed, a typed folder path opens no preview. lgse/strata#1912 (unverified)
- Back, Forward, a sidebar place, another typed path, or opening a subfolder before the file is selected cancels its preview. Selecting the file later, with Quick Preview closed, does not open it. lgse/strata#1912
- A typed file path whose parent fails to open, for a reason other than being unmounted, leaves no pending preview. lgse/strata#1912
- A typed file missing from its loaded parent leaves no pending preview after the "Unable to select file" dialog. lgse/strata#1912 (unverified)
- A hidden file target turns on hidden files so the selection is visible. lgse/strata#1219
- A file target missing from the loaded parent shows an "Unable to select file" dialog. lgse/strata#1219

### Pasted paths

- Ctrl+L with `~/My\ Documents/report\ \(1\).pdf` opens `My Documents` with `report (1).pdf` selected. lgse/strata#2692, lgse/strata#2670
- `'~/My Documents'` opens the folder, and `"<home>/My Documents/report (1).pdf"` selects the file in it. lgse/strata#2692, lgse/strata#2670
- `' /path/with spaces/file.txt '` opens `/path/with spaces` with `file.txt` selected; spaces inside the quotes are trimmed. lgse/strata#2670, lgse/strata#2692
- `'/tmp/it'\''s here'` and `'/tmp/it'"'"'s here'` both open `/tmp/it's here`. lgse/strata#2692
- Inside double quotes, `\$`, `` \` ``, `\"`, `\\`, and `\` before a newline lose their backslash; another backslash stays, so `"/tmp/\$d \"v2\" \final"` opens `/tmp/$d "v2" \final`. lgse/strata#2692 (unverified)
- A newline inside quotes is kept in the path. lgse/strata#2670, lgse/strata#2692
- `$'…'` quoting decodes ANSI-C escapes, and `\xHH` gives a raw byte, so `/tmp/$'bad\xff.txt'` names a non-UTF-8 file. lgse/strata#2692
- `file:///path/with%20spaces/file.txt` opens `/path/with spaces` with `file.txt` selected; `file://localhost/…` works the same. lgse/strata#2692, lgse/strata#2670
- A `file://` URI is percent-decoded to raw bytes, and scheme case is ignored: `FILE:///tmp/bad%FF/` opens the non-UTF-8 folder. lgse/strata#2692 (unverified)
- `file://otherhost/tmp` shows "A file:// URI must name a file on this computer. Use smb:// or sftp:// for another computer." The current folder stays open. lgse/strata#2692
- A `file://` URI holding `%2F` in a name is rejected with "Enter a valid URI." lgse/strata#2692 (unverified)
- `~` expands after unquoting: `~/folder\ name` and `'~/folder name'` open `folder name` under home. lgse/strata#2692, lgse/strata#2670
- `'~other-user/Documents'` and `'user@host:path'` are still rejected with the `~` and SCP messages. lgse/strata#2692 (unverified)
- A backslash before a character no shell escapes makes the whole text literal: `/tmp/My\ Documents\notes` keeps both backslashes. lgse/strata#2692
- An unquoted `$`, backtick, `&`, `;`, `<`, `>`, `(`, `)`, `|`, or whitespace makes the text literal: `/tmp/report\ (1).txt` keeps its backslash. lgse/strata#2692 (unverified)
- A quote that opens inside a name is an apostrophe: `/srv/Mom's and Dad's` and `/home/me/bob's notes` open as typed. lgse/strata#2692
- A `$'…'` escape that decodes to a NUL byte, as in `$'/tmp/nul\0byte'`, leaves the text literal. lgse/strata#2692
- `''` is rejected with "Enter a location." lgse/strata#2692 (unverified)
- A URI with another scheme loses only one pair of outer quotes, with no unescaping: `'SMB://host/share'` opens `smb://host/share`. lgse/strata#2692, lgse/strata#2670
- A quoted `'smb://alice:secret@host/share'` mounts `smb://alice@host/share`, using the password for that attempt only. lgse/strata#2692 (unverified)
- A quoted `"https://example.com/files"` is rejected as an unsupported scheme. lgse/strata#2692 (unverified)
- A quoted relative path such as `'Documents'`, or nested quotes such as `"'/tmp/nested'"`, is rejected with "Enter an absolute path." lgse/strata#2670, lgse/strata#2692 (unverified)

### Breadcrumbs

- Each ancestor crumb is a button that opens that folder. lgse/strata#316
- Clicking an ancestor crumb, or choosing an ancestor in the hierarchy menu, selects the folder on the path you came from. In Icons and List a remembered position wins. lgse/strata#1437, lgse/strata#1544
- Right-clicking the breadcrumb bar opens a menu of the current folder and its ancestors, current first; choosing one opens it. lgse/strata#820
- The hierarchy menu has no arrow. It opens below the crumb bar at the click's x position, so it never covers the crumbs. lgse/strata#2030
- The hierarchy menu marks as current the folder the bar names. lgse/strata#2026
- In Columns with a child folder mirrored beside the focused column, the breadcrumbs, Ctrl+L, the Escape or failed-submit refill, and the hierarchy menu name the deepest column. lgse/strata#2026
- Switching from Columns to List or Icons makes the breadcrumbs name the folder the pane shows. Ctrl+L then prefills it, and Enter does not enter the mirrored child. lgse/strata#2026
- Switching back to Columns names the mirrored child again. lgse/strata#2026
- Middle-clicking an ancestor crumb, such as `Documents` in `~/Documents/projects`, opens it in a new, active tab. The first tab stays in `projects`. lgse/strata#2038
- Ctrl+middle-click or Shift+middle-click on an ancestor crumb opens that folder in a new window. lgse/strata#2038
- In a file chooser, middle-clicking a crumb opens nothing. lgse/strata#2038
- Middle-clicking the current crumb opens no tab. lgse/strata#2038 (unverified)
- Parent breadcrumbs accept file drops. lgse/strata#1487
- Dropping onto a breadcrumb before 750 ms transfers into it without navigating. lgse/strata#1487
- Holding a file drag over a parent breadcrumb for 750 ms navigates there, and the drag stays held. lgse/strata#1487
- A breadcrumb under a file drag shows an accent tint and an accent inset ring, not GTK's green border. lgse/strata#1831
- For paths under home, the crumbs and the hierarchy menu start at `~`. lgse/strata#820 (unverified)
- When crumbs overflow, the wheel scrolls them horizontally and edge fades mark the hidden part. lgse/strata#820
- The overflow scrollbar sits in its own row below the crumbs, hidden at rest and shown on hover or scroll, never covering labels. lgse/strata#820
- Crumb labels longer than 32 characters are shortened in the middle. lgse/strata#1143
- Deep paths keep each crumb label at its text width, up to 32 characters. The crumb row scrolls instead of shrinking labels to "l…". lgse/strata#1909
- After navigation, or after submitting or cancelling the entry, the crumbs scroll to show the current crumb. lgse/strata#1909
- The current crumb's Copy path button copies the path and shows a check and "Path copied" for 2 seconds. lgse/strata#316 (unverified)
- The Copy path button is named "Copy path"; after a click it is named "Path copied", then "Copy path" again 2 s later. lgse/strata#1895

## Design

The breadcrumbs and the entry are two pages of one stack; the entry is transient chrome.

- An outside click cancels rather than commits, because a half-typed or invalid path would navigate unexpectedly (lgse/strata#246).
- Every area showing the text cursor must start editing, so the edit target is the whole bar except crumb and copy-path buttons (lgse/strata#288).
- `~` expands only for the current user before absolute-path validation; other `~` forms stay errors (lgse/strata#149).
- Typed paths resolve `.` and `..` as text, like GIO, `cd`, and the folder picker. The visible path stays, symlinks are not followed, and no I/O blocks (lgse/strata#1445, lgse/strata#1570).
- UNC and SCP shorthand are refused rather than guessed, so a typed URI is never rewritten into another scheme (lgse/strata#20).
- Pasted text is read as one shell word, as a terminal or the former Copy path wrote it. It names the same path as the plain spelling. UNC and SCP shorthand stay refused (lgse/strata#2669, lgse/strata#2670, lgse/strata#2692).
- A fixed rule, not a filesystem probe, decides whether a backslash or quote is shell syntax or part of the name. A probe would block the main thread (lgse/strata#2692).
- Shells and terminals open a quote only at the start of a path component or next to other quoting. A quote inside a name is therefore literal, so a path Copy path produces opens again (lgse/strata#2692, commit 76cd64b8).
- A `$'…'` escape that decodes to NUL leaves the text literal: no path holds one, and glib-rs panics converting one. The maintainer treats this as hardening ([comment](https://github.com/lgse/strata/pull/2692#issuecomment-7122150882)).
- Shell escapes inside a URI are left alone, so remote URIs keep their parsing (lgse/strata#2670).
- A `file://` URI becomes a native path through GLib. One that names another host is an error rather than a remote location (lgse/strata#2670, lgse/strata#2692).
- A typed URI is stored in the percent-encoded form its listed children use, so refreshes reach the open column. The entry keeps the decoded text (lgse/strata#1424, lgse/strata#1533).
- URI credentials are parsed with GLib's password and auth-parameter flags and leave the text at once. They reach only the pending mount with saving disabled, and are then discarded (lgse/strata#111, lgse/strata#145).
- A file path reuses validation: `NotDirectory` sends the parent through navigation with the file as a pending reveal, matching GTK and KDE choosers (lgse/strata#1139, lgse/strata#1219). The file is also recorded as a preview target, consumed when the reveal focuses it (lgse/strata#1912).
- That preview target is a field beside the reveal, so every navigation path must clear it. Carrying it on the reveal selection is a possible follow-up (lgse/strata#1912).
- Every exit path switches the stack to the breadcrumbs before resetting the text, so the entry's `changed` signal cannot reopen the popover (lgse/strata#1205).
- The breadcrumbs, Ctrl+L, the Escape refill, and the hierarchy menu share one mode-aware rule. It names the deepest column in Columns and the active folder in Icons and List (lgse/strata#1999, lgse/strata#2026).
- Typed bare `network:`, `trash:`, and `recent:` roots are normalized to GIO's canonical `scheme:///` form, which the sidebar opens and labels (lgse/strata#2016, lgse/strata#2030).
- The hierarchy menu is arrowless, like the popovers of lgse/strata#1912, and anchored to the bar's full height to stay clear of the crumbs it lists (lgse/strata#2016, lgse/strata#2030).
- GVfs folds a URI's query and fragment into the mount spec, so SFTP mounted a spec the location never matched. No accepted scheme addresses files with either, so typed addresses drop both (lgse/strata#2030).
- Crumb middle-clicks reuse the folder rows' middle-click rule, and choosers skip them like the other tab actions (lgse/strata#2037, lgse/strata#2038).
- The scrollbar moved from an overlay inside the 22 px crumb row to its own row, after the shared fixed-scrollbar class still cropped labels (lgse/strata#297, lgse/strata#819).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-11-24 | lgse/strata#2692 | feat | Read pasted shell-escaped and quoted paths and `file://` URIs as the literal path, so a terminal's or Copy path's text opens. |
| 2026-11-02 | lgse/strata#2030 | fix | Read `network:`, `network://`, `trash:` and `recent:` as their roots, dropped typed query and fragment, and opened the arrowless hierarchy menu below the bar. |
| 2026-11-02 | lgse/strata#2026 | fix | Named the folder List and Icons show in the breadcrumbs, Ctrl+L, Esc refill and hierarchy menu after leaving Columns. |
| 2026-10-29 | lgse/strata#1909 | fix | Gave crumb labels a minimum width so deep paths scroll, and revealed the current crumb after layout and after editing. |
| 2026-10-28 | lgse/strata#1912 | fix | Opened Quick Preview on a file revealed from a typed path, and dropped that request when navigation moves on first. |
| 2026-10-11 | lgse/strata#1570 | fix | Resolved `.` and `..` as text in typed paths, so crumbs and Parent follow the resolved path. |
| 2026-10-10 | lgse/strata#1544 | fix | Made crumbs and the hierarchy menu select the folder you came from when they open an ancestor. |
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

- A typed path to a file with no previewer still opens the preview drawer, as Space on it does. lgse/strata#1912
- A typed `mtp://` address is rejected as an unsupported scheme, so editing the path bar on a phone fails. lgse/strata#2072
- Without a filesystem probe, a literal name starting with a balanced quote is read as quoted: `/music/"Heroes"` opens `/music/Heroes`. A literal backslash before a shell-escapable character is also unescaped. lgse/strata#2692 ([comment](https://github.com/lgse/strata/pull/2692#issuecomment-7122150882))
- A password URI wrapped as `$'smb://…'` is not recognized as a URI. It is read as a local path, which fails to open. lgse/strata#2692 ([comment](https://github.com/lgse/strata/pull/2692#issuecomment-7122150882))
- An absolute local path holding `@` then `:`, such as `/home/a@b:c`, is rejected as SCP shorthand. lgse/strata#2692 ([comment](https://github.com/lgse/strata/pull/2692#issuecomment-7122150882))
- A typed address with a query or fragment and a non-ASCII host is rebuilt with its host in punycode: `sftp://h%C3%A9/x?q` opens `sftp://xn--h-bga/x`. lgse/strata#2072
