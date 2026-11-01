---
proposed: {page: new}
nodes: [integration/open-with, integration/open-with/recent-apps]
reason: 'Opening files in their default application, the Open With chooser and its Recently Used section, setting a default, running executables, and the Flatpak behavior are user-visible, and no page names these nodes. The Keyboard navigation and 10xer references mention Open With only as a menu entry and key. Proposed as an "Opening files and Open With" reference page with one `##` section per heading below.'
release: v1.1.1
---

## Opening a file

Activating a file whose type has a default application launches it with no
dialog. A double-click in Columns launches it once, as **Enter** does. A failed
launch shows "Unable to open file" with the error. After Strata launches a file,
the file joins the desktop's recent-file history and appears in Recent; folders
do not.

When the file's type has no default application, the Open With chooser opens for
it instead. If no application can open it, the chooser shows "No application is
registered for this file" with **Open** disabled. Closing it returns focus to the
file.

- Items in Trash cannot be opened: "Unable to open item" says "Items in Trash
  cannot be opened".
- A file with no local path, such as a GVfs location without a FUSE path, opens
  only in applications that accept URIs. GVfs files under
  `/run/user/$UID/gvfs/` also open in path-only applications.
- When the preview hands a video to its default player, mpv, VLC, Celluloid and
  MPlayer start at the preview's position.

## Running programs

Activating a local file with the execute bit and no default application asks
"Run this program?", danger-toned, with **Run** focused. **Run** starts the program
in its own folder with its output discarded; **Cancel** runs nothing. The item menu
also shows **Run** for exactly one local executable file, or a symlink to one,
outside Trash, including in search results.

Running a `.sh` file opens it in a terminal in its folder. When it ends, the
terminal shows "Process exited with status N. Press Enter to close…" and waits for
**Enter**. With no terminal found, "Unable to run program" explains why.

## The Open With chooser

**Open With…** in the item menu opens the chooser for the selection.

- **Recently Used** lists up to 5 applications last used for files of this type,
  most recent first. Both Open With and opening with the default application
  record an application. History is kept per type, survives restarts, and lives
  in `$XDG_DATA_HOME/strata/recent-apps.toml`.
- **Recommended Applications** lists the handlers for the type, the configured
  default first even when it is hidden from menus; the rest sort by name.
- **Other Applications** lists every other visible application. No application
  appears twice.
- For several types, only handlers shared by every type are recommended. A file
  of unknown type lists applications under Other Applications.
- Applications hidden from menus, or whose `OnlyShowIn` excludes the desktop, are
  not listed. For items with no local path, only URI-capable applications are.

The search field, "Search applications…", has focus on open and filters by name,
description, executable or desktop id, ignoring case. With no match it shows "No
matching applications were found." and disables **Open**. **Up** and **Down** move
the selection while focus stays in the search field; **Enter** opens the selected
application; **Escape** clears a search, then closes the chooser. **Tab** moves to
the list, the toggle, then **Cancel**.

**Always use for this file type** ("for these file types" for several types) is
unchecked by default. Opening with it checked makes the application the default
for each selected type in `mimeapps.list`. Unchecked, or on **Cancel**, nothing
changes. The toggle is hidden when no application is offered.

### Menu entries

- A broken symlink in the selection disables **Open With…**: "Broken symbolic
  links cannot be opened with an application".
- A selection no application can open disables it: "No compatible applications
  were found", or "No application can open all selected file types".
- For several items, **Open** appears only when every type has the same default,
  and launches that application with all of them.

## Inside Flatpak

When Strata runs as a Flatpak (`/.flatpak-info` exists):

- Activating a file without the execute bit opens it in the host's default
  application through the desktop portal; Strata's chooser does not appear.
  Any file with the execute bit asks "Run this program?".
- **Open** hands each file to its host default application.
- **Open With…** shows the desktop's own application chooser, one file at a
  time; dismissing one cancels the rest. It is never disabled for lack of
  applications.
- A video handed from the preview to its player starts at the beginning.
