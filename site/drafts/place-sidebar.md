---
proposed: {page: new}
nodes: [browser/sidebar/pins, browser/sidebar/pins/drag-to-pin, browser/sidebar/rail, browser/sidebar/connect-to-server, browser/navigation/recent]
reason: 'Pinned folders and the shared bookmarks file, drag-to-pin gaps, and the Recent location are user-visible, and no page describes them. The sidebar toggle and icon rail are now on the Keyboard navigation reference ("Arrows, the header, and the sidebar"), and the Connect to server dialog on the SFTP locations reference ("Addresses") and Keyboard navigation reference; this draft keeps only the one fact each lacks. Proposed as a "Sidebar and places" reference page for pins, drag-to-pin, and Recent. The rail and Connect to server nodes could instead be added to the pages that already describe them.'
release: v1.1.1
---

Raw material for a "Sidebar and places" reference page.

## Pinned folders

Pinned folders appear under a **PINNED** heading, in the order of GTK's shared
bookmarks file, `$XDG_CONFIG_HOME/gtk-3.0/bookmarks`, which Nautilus and GTK file
choosers also read. Each pin shows its bookmark label, or else the folder name.
With nothing pinned, the sidebar shows no PINNED heading, separator, or gap. A
bookmark for Home or a standard folder is not shown and keeps its line in the
file.

Ways to pin and unpin:

- With one folder outside Trash selected, the item menu shows **Pin to sidebar**,
  insensitive for pinned folders, Home and the standard folders.
- Properties for a folder shows **Pin**, or **Unpin** once it is pinned; either
  updates the sidebar and closes the dialog. Files, Trash, Home and the standard
  folders show no pin control.
- In the default map, with the file list focused and **Type to search** off,
  **p** pins the focused folder. **Shift+p** does not; Caps Lock+**p** acts as
  **p**.
- Right-clicking a pinned row offers **Unpin** and **Properties**, plus
  **Customize…** for a local folder.

Clicking a pinned remote location that is not mounted, such as an SMB share,
mounts it and then opens it. Disconnecting or unmounting a pinned share keeps its
row.

To reorder, drag a pinned row onto the upper or lower half of another pin, or
into a gap between pins. An accent line shows where it will land, and the new
order is saved to the bookmarks file. The system file chooser lists only pins
with local paths; there pinned rows offer **Unpin**, **Customize…** and
**Properties**, and reorder by drag.

### Shared bookmarks file

- Every pin, unpin, or reorder reads the bookmarks file first, so pins made in
  another Strata window or by Nautilus survive, and updates PINNED in every open
  Strata window.
- When another program changes the file between Strata's read and save, Strata
  reads it again and reapplies the change, at most twice more.
- Bookmarks another program changes reach open windows only when Strata next
  changes a pin or deletes an item; a new window also reads them.
- When the file cannot be read or saved, "Unable to update pinned folders"
  appears with the reason, and the shown pins stay unchanged.
- A user-owned symlink at `gtk-3.0/bookmarks`, as from a dotfiles manager, is
  kept: Strata writes the link's target. A dangling link, or one owned by another
  user, is refused.
- A label with invalid UTF-8 shows U+FFFD. A line whose URI is invalid UTF-8,
  cannot be parsed, or repeats an earlier location is skipped, and CRLF line
  endings are accepted. The next change rewrites the file from what was read:
  skipped lines are dropped, and unlabelled bookmarks gain the folder name as
  label.
- A bookmark URI with a password or authentication parameters is kept with its
  username only.

### Deleted folders

Deleting or trashing a folder in Strata removes its pin, and every pin inside it,
from the file and from every sidebar when the operation ends, also when it is
cancelled. Items whose deletion failed or was cancelled keep their pins, as do
pins on disconnected drives or unavailable network locations. Restoring a folder,
including with **Ctrl+Z**, does not restore its pins. Deleting a symlink removes
pins under the link's path and keeps pins to its target. When the bookmarks file
cannot be updated, an error is reported and the deletion still succeeds.

## Drag folders to pin

PINNED has insertion gaps before the first pin, between pins, after the last pin,
and in an empty section. Drag folders from Columns, Icons, or List into a gap to
pin them there, in selection order. Row bodies stay file-transfer targets. With
nothing pinned, dragging files or folders over the sidebar shows the empty PINNED
section until the drag leaves the sidebar.

- An already pinned folder, Home, and the standard folders are skipped; the rest
  of the selection is pinned.
- A file, or a selection mixing files and folders, shows no insertion line and
  pins nothing.
- Holding **Shift** still pins and moves nothing.
- Directory symlinks and remote folders, such as SMB and SFTP shares, can be
  pinned and are stored as spelled. Remote pins have gaps beside them, although
  their rows accept no file drops.
- A drag-pinned folder is labelled with its display name, as a menu pin is.
- A folder dragged from another file manager shows the insertion line once every
  item is confirmed to be a folder, within 2 s. A timeout, a failure, or any
  non-folder rejects the whole drag. Move-only drags from other applications are
  rejected; Copy drags are accepted. A network share dragged from another
  application is rejected, although the same share dragged from Strata pins.
- A trashed folder or an `http://` or `https://` link is rejected.
- In the system file chooser, a local folder dropped in a gap is pinned, not
  moved, and a remote folder is rejected.

## Collapse the sidebar

In the icon rail, section headings and the drives' action buttons, such as eject,
are hidden as well as row names.

## Connect to server

The **Server address** field's placeholder is `smb://server/share` in every
language.

## Recent

**Recent** (`recent:///`) lists the files in the desktop's recent-file history,
most recently used first. Open it from the sidebar or the location bar.
**Settings → General → SIDEBAR → Show Recent in sidebar** is on by default.
Without the GVfs recent backend, typing `recent:///` shows "Unable to open
location" saying the backend isn't installed.

- Entries whose file is missing or unreadable are skipped. Names that are not
  valid UTF-8 are listed.
- Recent has its own sort; changing it leaves ordinary folders alone.
- An open Recent view reloads when the history changes. Deleting or moving a file
  removes its row at once.
- Opening a file in an application from Strata adds it to the history; opening a
  folder does not. Renaming or moving a file in Strata drops it from Recent.
- Parent is unavailable in Recent; Back and Forward still work.
- Open, **Open With…**, Quick preview, Rename, **Move to…**, Move to Trash,
  Permanently delete, Properties, and **Open file location** act on each row's
  real file. New File, New Folder, Paste and drops are unavailable.
- **Remove from Recent** drops the selected rows from the history at once,
  without confirmation, and leaves the files untouched.
