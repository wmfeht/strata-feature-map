---
title: Opening files and Open With
status: shipped
origin: {issue: lgse/strata#174, pr: lgse/strata#421}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [src/ui/open_with.rs, src/ui/browser/desktop.rs]
tests: [src/ui/open_with/tests.rs, src/ui/browser/context_menu/tests/open_with.rs, tests/e2e/scenarios/test_open_with.py]
docs: []
related: [integration/10xer-mode, preview/preview-panel]
---

## Summary

Opening files in their default application, choosing another application from the Open With chooser, setting a new default, and running executable files. Children: `integration/open-with/recent-apps` (the chooser's Recently Used section) and `integration/open-with/terminal` (Open in Terminal).

## Behavior

### Activation

- Activating a file whose type has a default application launches it with no dialog. lgse/strata#1012
- Double-clicking a file in Columns launches its application once, as Enter does. lgse/strata#92
- Activating a file with no default application opens the Open With chooser for it instead of an error. lgse/strata#1012
- When that chooser has no application to offer, it shows "No application is registered for this file" with Open disabled. lgse/strata#1012
- Closing the fallback chooser returns focus to the activated entry. lgse/strata#1012
- Activating an item in Trash shows "Items in Trash cannot be opened" and launches nothing. lgse/strata#995
- A file with no local path, such as a GVfs location without a FUSE path, opens only with a default that accepts URIs (`%u`/`%U`). lgse/strata#578, lgse/strata#784
- A GVfs file with a FUSE path under `/run/user/$UID/gvfs/` also opens with a path-only (`%f`/`%F`) default. lgse/strata#784
- A failed launch shows "Unable to open file" with the error. lgse/strata#1012
- When the preview hands a video to its default player, mpv, VLC, Celluloid, and MPlayer, including their Flatpaks, start at the preview's position. lgse/strata#1474

### Running programs

- Activating a local regular file with an execute bit and no default application asks "Run this program?" instead of opening the chooser. lgse/strata#461, lgse/strata#1012
- The confirmation is danger-toned, names the file, warns "Only run programs you trust.", and focuses Run. lgse/strata#461, lgse/strata#1206
- Cancel in the confirmation runs nothing. lgse/strata#948
- Run starts the program in its own folder with its standard streams discarded. lgse/strata#461
- The item menu shows Run for exactly one local executable file, or a symlink to one, outside Trash, including search results. lgse/strata#948
- Run is absent for folders, non-executable files, remote items, Trash items, and multiple selections. lgse/strata#948
- Running a `.sh` file opens it in a terminal in its folder, then shows "Process exited with status N. Press Enter to close…" and waits for Enter. lgse/strata#1028
- With no terminal found, running a `.sh` file shows "Unable to run program" with the no-terminal message. lgse/strata#1028 (unverified)

### Menu entries

- The item menu offers Open With… for one or several selected files or folders. lgse/strata#421, lgse/strata#625
- While types are looked up, Open With… is insensitive and described "Looking for compatible applications…". lgse/strata#578
- A broken symbolic link in the selection disables Open With… with "Broken symbolic links cannot be opened with an application". lgse/strata#578
- A selection no visible application can open disables Open With… with "No compatible applications were found", or "No application can open all selected file types" for several types. lgse/strata#578
- A multi-selection menu shows Open only when every selected type has the same default; Open launches that application with all items. lgse/strata#578
- Selected types with common handlers but different defaults get Open With… and no Open. lgse/strata#578
- The folder background menu offers Open With… for the current folder, except in Trash and Recent. lgse/strata#821, lgse/strata#1083

### Chooser

- The chooser lists Recommended Applications, the handlers for the type, then Other Applications, every other visible application; none appears twice. lgse/strata#821
- For several types, Recommended holds only handlers shared by every type; with none shared, applications appear under Other Applications only. lgse/strata#578, lgse/strata#821
- A file of unknown type, such as `application/octet-stream`, lists visible applications under Other Applications. lgse/strata#578, lgse/strata#821
- The configured default heads Recommended even when it is `NoDisplay=true`; the remaining rows sort by name, ignoring case. lgse/strata#578
- Other `NoDisplay` applications and those whose `OnlyShowIn` excludes the current desktop are not listed. lgse/strata#578
- For items with no local path, only applications that accept URIs are listed. lgse/strata#578, lgse/strata#784
- The search field has focus on open; typing filters rows by name, description, executable, or desktop id, ignoring case, and hides empty section headings. lgse/strata#821
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
- Type lookups run asynchronously and are discarded when the menu closes or the selection changes (lgse/strata#578, lgse/strata#625).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
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

- Inside a Flatpak sandbox, GIO sees only the runtime's applications, so activating a document opens an empty chooser. lgse/strata#1503
