---
title: Opening files and Open With
status: shipped
origin: {issue: lgse/strata#174, pr: lgse/strata#421}
branch: null
reviewed_at: 86df474dc0e8352e0e2098637a017cc4c77a8c44
review: draft
code: [src/ui/open_with.rs, src/ui/browser/desktop.rs]
tests: [src/ui/open_with/tests.rs, src/ui/browser/desktop/tests.rs, tests/qa/scenarios/open_with/**, tests/qa/scenarios/dialogs_and_menus/executable-menu-confirmed-run.jsonl, tests/qa/scenarios/dialogs_and_menus/executable-requires-confirmation.jsonl]
docs: []
related: [integration/10xer-mode, preview/preview-panel, browser/context-menu, browser/navigation/recent]
---

## Summary

Opening files in their default application, choosing another application from the Open With chooser, setting a new default, and running executable files. Children: `integration/open-with/recent-apps` (the chooser's Recently Used section) and `integration/open-with/terminal` (Open in Terminal). The menus that offer these commands belong to `browser/context-menu`.

## Behavior

### Activation

- Activating a file whose type has a default application launches it with no dialog. lgse/strata#1012
- Double-clicking a file in Columns launches its application once, as Enter does. lgse/strata#92
- Outside Flatpak, activating a file with no default application opens the Open With chooser for it instead of an error. lgse/strata#1012, lgse/strata#1635
- When that chooser has no application to offer, it shows "No application is registered for this file" with Open disabled. lgse/strata#1012
- Closing the fallback chooser returns focus to the activated entry. lgse/strata#1012
- The fallback chooser opens only if the window is visible and shows no other dialog when the Recently Used history read finishes. Pressing Enter twice on such a file opens one chooser. lgse/strata#1729
- Activating an item in Trash shows "Unable to open item" with "Items in Trash cannot be opened" and launches nothing. lgse/strata#995
- A file with no local path, such as a GVfs location without a FUSE path, opens only with a handler that accepts URIs (`%u`/`%U`). lgse/strata#578, lgse/strata#784
- A GVfs file with a FUSE path under `/run/user/$UID/gvfs/` also opens with a path-only (`%f`/`%F`) default. lgse/strata#784
- A failed launch shows "Unable to open file" with the error. lgse/strata#1012
- After Strata launches a file in an application, the file is added to the desktop's recent-file history, so it appears in Recent. lgse/strata#1083
- Launching a folder in an application adds nothing to the recent-file history. lgse/strata#1083 (unverified)
- Outside Flatpak, when the preview hands a video to its default player, mpv, VLC, Celluloid, and MPlayer start at the preview's position. lgse/strata#1474, lgse/strata#1635
- When Strata runs outside Flatpak, Flatpak installs of mpv, VLC, and Celluloid also start at the preview's position; an MPlayer Flatpak and other players start at the beginning. lgse/strata#1474, lgse/strata#1635 (unverified)

### Running programs

- Activating a local regular file with an execute bit and no default application asks "Run this program?" instead of opening the chooser. lgse/strata#461, lgse/strata#1012
- The confirmation is danger-toned, names the file, reads "“%{name}” is an executable file. Only run programs you trust.", and focuses Run. lgse/strata#461, lgse/strata#1206
- Cancel in the confirmation runs nothing. lgse/strata#948
- Run starts the program in its own folder with its standard streams discarded. lgse/strata#461
- The item menu shows Run for exactly one local executable file, or a symlink to one, outside Trash, including search results. lgse/strata#948
- Run is absent for folders, non-executable files, remote items, Trash items, and multiple selections. lgse/strata#948
- Running a `.sh` file opens it in a terminal in its folder, then shows "Process exited with status N. Press Enter to close…" and waits for Enter. lgse/strata#1028
- With no terminal found, running a `.sh` file shows "Unable to run program" with the no-terminal message. lgse/strata#1028 (unverified)

### Menu entries

- A broken symbolic link in the selection disables Open With… with "Broken symbolic links cannot be opened with an application". lgse/strata#578
- Outside Flatpak, a selection no visible application can open disables Open With… with "No compatible applications were found", or "No application can open all selected file types" for several types. lgse/strata#578, lgse/strata#1635
- Outside Flatpak, a multi-selection menu shows Open only when every selected type has the same default; Open launches that application with all items. lgse/strata#578, lgse/strata#1635
- Outside Flatpak, selected types with common handlers but different defaults get Open With… and no Open. lgse/strata#578, lgse/strata#1635

### Chooser

- The chooser lists Recommended Applications, the handlers for the type, then Other Applications, every other visible application; none appears twice. lgse/strata#821
- For several types, Recommended holds only handlers shared by every type; with none shared, applications appear under Other Applications only. lgse/strata#578, lgse/strata#821
- A file of unknown type, such as `application/octet-stream`, lists visible applications under Other Applications. lgse/strata#578, lgse/strata#821
- The configured default heads Recommended even when it is `NoDisplay=true`; the remaining rows sort by name, ignoring case. lgse/strata#578
- Other `NoDisplay` applications and those whose `OnlyShowIn` excludes the current desktop are not listed. lgse/strata#578
- For items with no local path, only applications that accept URIs are listed. lgse/strata#578, lgse/strata#784
- The search field has focus on open; typing filters rows by name, description, executable, or desktop id, ignoring case, and hides empty section headings. lgse/strata#821
- The search field is named "Search applications…". lgse/strata#1896 (unverified)
- A search with no match shows "No matching applications were found." and disables Open. lgse/strata#821
- Up and Down in the search field move the selected row while focus stays in the field. lgse/strata#821
- Enter opens the selected application with the items and closes the chooser. lgse/strata#421
- Escape clears a non-empty search first, then closes the chooser. lgse/strata#821
- Tab moves from the search field to the selected row, then the Always use toggle, then Cancel; the list is one Tab stop. lgse/strata#578, lgse/strata#1298
- Each row's accessible name is the application name, and an icon the theme cannot resolve shows Strata's fallback icon. lgse/strata#578
- A failed launch closes the chooser and shows "Unable to open file" with the error. lgse/strata#421 (unverified)
- Launching an application without URI support on an item with no local path fails with "This application cannot open files at this location". lgse/strata#578

### Default application

- The chooser shows an unchecked "Always use for this file type" toggle, or "Always use for these file types" for several types. lgse/strata#1298
- Opening with the toggle checked makes the application the default for every selected content type in `mimeapps.list`, then launches it. lgse/strata#1298
- Opening with the toggle unchecked, or cancelling with it checked, leaves `mimeapps.list` unchanged. lgse/strata#421, lgse/strata#1298
- The toggle is hidden when the chooser has no application to offer. lgse/strata#1298
- If writing the default fails, the file still opens and a warning is logged. lgse/strata#1298

### Flatpak

- Inside a Flatpak sandbox (`/.flatpak-info` exists), activating a file without an execute bit opens it in the host's default application through the OpenURI portal. Strata's chooser does not appear. lgse/strata#1635
- Inside Flatpak, activating any local regular file with an execute bit asks "Run this program?", whatever its type. lgse/strata#1635 (unverified)
- Inside Flatpak, a video handed from the preview to its player starts at the beginning. lgse/strata#1635 (unverified)
- Inside Flatpak, the item menu's Open hands each selected file to its host default handler. lgse/strata#1635
- Inside Flatpak, Open With… shows the desktop's own app chooser instead of Strata's chooser. lgse/strata#1635
- Inside Flatpak, Open With… on several files shows one desktop chooser per file in turn. Dismissing one opens none of the rest and shows no error. lgse/strata#1635
- Inside Flatpak, Open With… is never disabled for lack of compatible applications. lgse/strata#1635 (unverified)
- Inside Flatpak, a portal failure other than a dismissal shows "Unable to open file" with the error and opens none of the remaining files. lgse/strata#1635 (unverified)
- Without `/.flatpak-info`, Open With… shows Strata's chooser. lgse/strata#1635

## Design

Applications come from GIO metadata; Strata does not parse `.desktop` files (lgse/strata#174). Choosing an application never changes the system default unless Always use is checked (lgse/strata#174, lgse/strata#1290).

- A submenu listing every handler was rejected as a duplicate of the chooser that lengthens the menu. Custom actions do not replace MIME integration (lgse/strata#174).
- GIO expands `%f`/`%F` with a local path and silently drops files that lack one, so URI-capable handlers are required only when an item has no path. Trash has none; GVfs FUSE mounts do (lgse/strata#569, lgse/strata#688).
- A hidden default is kept in the list because Open launches it anyway; `OnlyShowIn` filtering otherwise follows the spec (lgse/strata#572).
- Mixed types intersect their handlers instead of requiring equal types, and Open appears only for a shared default. A disabled entry always states why (lgse/strata#571, lgse/strata#575).
- An empty chooser was a dead end, so Other Applications lists every visible application (lgse/strata#570, lgse/strata#792).
- Activation falls back to the chooser rather than an error, matching Nautilus and Dolphin; always showing it was rejected because it slows associated files (lgse/strata#842).
- Executables without a handler are confirmed before running because they may be untrusted (lgse/strata#460). Run is also an explicit menu item, because AppImages and other executables with a registered type never reach that fallback (lgse/strata#844).
- A `.sh` script receives its path as an argument to `/bin/sh -c`, not as shell text, to keep its shebang and avoid injection (lgse/strata#1028).
- Inside Flatpak, GIO sees only the runtime's desktop entries, so files go to the OpenURI portal through `gtk::FileLauncher`. Open With sets `always_ask`, so the desktop's chooser picks the application (lgse/strata#1503, lgse/strata#1635).
- Portal launches run one file at a time so desktop choosers do not stack (lgse/strata#1635).
- Type lookups run asynchronously and are discarded when the menu closes or the selection changes (lgse/strata#578, lgse/strata#625).
- The chooser waits for the Recently Used history read before it opens (lgse/strata#1729).
- Run takes the file's type and mode from its asynchronous query. It spawns the program on the reaper thread, so a dead mount cannot freeze the window (lgse/strata#1729).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-15 | lgse/strata#1635 | fix | Opened files through the OpenURI portal under Flatpak, where GIO sees only the runtime's apps. |
| 2026-09-27 | lgse/strata#1298 | feat | Added "Always use for this file type" to set the default from the chooser. |
| 2026-09-15 | lgse/strata#1028 | fix | Ran `.sh` files in a terminal that keeps output and exit status until Enter. |
| 2026-09-14 | lgse/strata#1012 | feat | Opened the chooser when activating a file with no default application. |
| 2026-09-13 | lgse/strata#948 | fix | Added a Run menu item for single local executables, including search results. |
| 2026-09-11 | lgse/strata#821 | feat | Split the chooser into Recommended and Other, added search, and added Open With to the folder background menu. |
| 2026-09-11 | lgse/strata#784 | fix | Required URI handlers only for items without a local path, so GVfs FUSE files accept `%f`/`%F` apps. |
| 2026-09-08 | lgse/strata#625 | feat | Allowed Open With on folders and folder selections. |
| 2026-09-08 | lgse/strata#578 | fix | Required URI handlers off local paths, kept hidden defaults, intersected mixed types, and fixed chooser keyboard and accessibility issues. |
| 2026-09-07 | lgse/strata#421 | feat | Added Open With… and an application chooser that launches without changing the default. |
| 2026-09-06 | lgse/strata#461 | fix | Offered to run executables with no handler instead of a dead-end error. |
| 2026-09-01 | lgse/strata#92 | fix | Let the list view alone handle double-click activation so a file opens once. |

## Known gaps

None known.
