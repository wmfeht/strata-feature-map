---
nodes:
  - app/accessibility
  - app/dialogs
  - app/keyboard-shortcuts
  - app/shortcut-reference
  - app/window
  - browser/context-menu
  - browser/directory-monitoring
  - browser/folder-customization
  - browser/navigation
  - browser/navigation/folder-jump
  - browser/properties
  - browser/search
  - browser/search/filter
  - browser/selection
  - browser/selection/click-modes
  - browser/selection/keyboard-navigation
  - browser/selection/pointer-intent
  - browser/sidebar
  - browser/tabs
  - browser/tabs/session-restore
  - browser/view-modes
  - browser/view-modes/columns
  - browser/view-modes/position-restore
  - integration/10xer-mode
  - integration/10xer-mode/file-chooser
  - integration/10xer-mode/preview-keys
  - integration/10xer-mode/search
  - integration/file-manager-interface
  - integration/open-with/terminal
  - integration/portal-file-chooser
  - operations/archives
  - operations/archives/preview
  - operations/clipboard
  - operations/create
  - operations/delete
  - operations/rename
  - operations/trash
  - preview/preview-panel/layout
  - preview/preview-panel/media
  - preview/preview-panel/media/video
  - preview/quick-preview
  - preview/quick-preview/folder-peek
  - settings/preferences
reviewed_at: be3343a5992a2a5497b1a2ee7faa525be18e988f
---

# Keyboard navigation

Columns have three independent signals:

- **Selection:** filled rows are the items selected in that directory. Other columns retain a quieter selection when you leave them.
- **Keyboard cursor:** a text-contrast outline identifies the current item in the keyboard-focused list. Only that list shows a cursor; range selections can contain several filled rows.
- **Open path:** the chevron identifies the folder whose child column is open, without an extra border. This is navigation context, not another keyboard cursor.

The column that **Ctrl+V** will paste into has an accent rule across its header, including when the directory is empty. It moves to the column under the pointer as soon as you move the pointer. Columns fill the strip's full height.

## Keyboard layouts

<!-- node: app/keyboard-shortcuts -->
<!-- node: browser/tabs -->
<!-- node: browser/search/filter -->

Shortcuts on this page work on any keyboard layout, with the exceptions below.
Letters follow the key's label, or the Latin letter the key carries on Russian and
other non-Latin layouts, so **Ctrl+C** is the key that types **с** in Russian. On
plain Chinese (`cn`), every shortcut is the US one. Digits count by their position
on the top row, so **Ctrl+1** works on AZERTY without Shift. A digit typed off the
top row also counts, such as the Hungarian 0 left of 1. Caps Lock never changes a
shortcut. A symbol shortcut follows the symbol your layout types. A key that types
another ASCII symbol keeps it: on AZERTY, Ctrl and the key in the US **.** position
is not **Ctrl+.**. Where a key types a non-Latin or accented character, it also acts
as the Latin character on that key in another configured layout, or in its US
position when no configured layout is Latin: on Russian, Ctrl and the key that types
**ю** act as **Ctrl+.** and toggle hidden files.

With **Type to search** on, a key that types a letter starts type-to-search with that
letter, even in the US **/** position: on Icelandic the key that types **þ** starts
type-to-search with þ instead of opening an empty filter. Plain-key commands still
read the key's Latin character: in 10xer mode on Russian, the keys that type **о**
and **л** move the cursor like **j** and **k**, and on German **ö** in the file list
arms the actions chord as **;** does.

The exceptions: where a top-row key types **+** or **−**, Ctrl with that key acts as
**Ctrl++** or **Ctrl+−**, not as the digit, and in 10xer mode **g** reads it as + or
− too: on AZERTY **g**, then the − key unpins. Swiss German types + with Shift+1, so
there **Ctrl+Shift+1** selects no tab. With AltGr held, a top-row key counts only as
a digit it actually types, so AZERTY **Ctrl+AltGr+1** is not **Ctrl+1**.
**Ctrl+\\** also works on German, Swiss, Swedish and Norwegian Mac layouts, where
AltGr types `\` on the top row. **t** and **;** in 10xer mode have no + or − step,
so after them a top-row key counts by its position even where it types + or −: on
AZERTY **t**, then the − key selects tab 6, and on Czech **t**, then the + key
selects tab 1.

Letter, digit and symbol shortcuts match Ctrl, Alt, Shift and Super exactly, so
**Ctrl+Alt+C** does not copy. Chord digit steps, such as **t**, then **1** in 10xer
mode, and the media **0** key also accept Shift. Some navigation and dismiss keys
accept extra modifiers: **Delete** and **Shift+Delete** still act
with Ctrl, Alt or Super held, and **Escape** closes a dialog whatever else is
held. Hyper and Meta are ignored. A symbol shortcut ignores the Shift
your layout needs to type the symbol. Keypad Enter, arrows, Home, End, Page Up,
Page Down, Insert, Delete, Tab, Space, +, −, \*, / and = act as the main keys;
keypad digits count only with Num Lock on.

Typing is never remapped: type-to-search, the filter, rename fields and footer
prompts receive the characters your layout types, such as Cyrillic. While a text
field shows an unfinished input-method or dead-key composition, keys go to the
composition before any Strata command. Input method switch keys, **Ctrl+Space** for
fcitx5 and **Super+Space** for IBus, as well as **Shift** and **Shift+Space**, go to
the input method in every text field, the F1 search included; Strata's own
**Ctrl+Space** toggles selection only in a file list. While a text field has focus,
no Strata command takes a plain digit or punctuation key, so a Zhuyin input method
such as chewing receives the first key of each syllable. On the Taiwanese
`tw(saisiyat)` layout, the semicolon key types ː in a rename field, and in 10xer
mode it still arms the **;** chord in the file list. A Korean input method such as fcitx5-hangul
commits the syllable on **Escape** and passes the key back, so one press commits the
syllable and cancels a rename. Type-to-search started from the file list does not
use your input method: a pinyin letter arrives as the Latin letter, a Zhuyin key as
its digit or punctuation, and a dead key starts nothing. Typing in the Open With
list starts its search the same way. To search with an input method, open the
filter with **Ctrl+F** (**f** in 10xer mode), or move into the Open With search
field, and type there.

Every shortcut Strata shows is one that works. Shown shortcuts in F1, menus and
tooltips stay in Latin letters when you switch layouts. Modifiers appear in the
order Ctrl, Alt, Shift, Super, and a letter after a modifier is uppercase, as in
**Ctrl+Shift+N**. Without a modifier, a letter appears as typed (**j**) and Shift
with a letter as the uppercase letter (**J**). Chord steps are separated by a space
(**g h**). Alternatives that share their modifiers write them once, as in
**Ctrl+Alt+← / →** and **Ctrl++ / − / 0**, unless a key is a letter
(**Ctrl+U / Ctrl+D**). Digit ranges read **Ctrl+Shift+1–9 / 0** or **t 1–9 / t 0**. Minus is written −, and arrows ↑ ↓ ← →. Key names follow the interface
language, such as **Strg+C**, **Entf** and **Bild auf** for Page Up in German, or
**Suppr** for Delete in French; with the interface in Simplified Chinese they stay
as printed, such as **Ctrl+C**. In Traditional Chinese the modifiers stay as
printed, while Space, Page Up and Page Down read **空白鍵**, **上一頁** and
**下一頁**.

## Browser tabs

<!-- node: browser/tabs -->
<!-- node: browser/tabs/session-restore -->
<!-- node: browser/sidebar, Opening in a new tab -->
<!-- node: integration/open-with/terminal -->
<!-- node: integration/10xer-mode -->

In regular and 10xer modes, **Ctrl+T** opens a tab at the active location,
**Ctrl+W** closes the active tab, and **Ctrl+Tab / Ctrl+Shift+Tab** cycles tabs.
**Ctrl+Shift+T** reopens the last closed tab at its location and former position,
and selects it; with fewer tabs open than that position, it opens at the right end.
Repeat it to reopen up to 20 closed tabs, newest first. A close blocked by a dialog
or by running operations, or the close of the last tab, records nothing. Closed tabs
belong to their window: **Ctrl+Shift+T** in another window opens nothing, and closing
the window discards them, so they do not survive a restart. A reopened tab starts
with fresh selection, navigation history and preview. With no closed tab recorded,
**Ctrl+Shift+T** does nothing. It also works with focus in a text field, such as the
location editor.
**Ctrl+Page Up / Ctrl+Page Down** selects the previous / next tab in strip order,
wrapping at either end, like the tab shortcuts in web browsers.
**Ctrl+Shift+Page Up / Ctrl+Shift+Page Down** moves the active tab one position
left / right without switching tabs. Reordering stops at either end of the strip.
With Alt or Super also held, these Page Up and Page Down shortcuts leave the tabs alone.
The moved tab keeps its location, selection and focus, including focus in the
location editor.
Hold **Ctrl+Shift**, without Alt or Super, to display numbers beside the first ten
labels; they hide when you release Ctrl or Shift or the window loses focus. Press
**Ctrl+Shift+1–9** to select tabs 1–9 or **Ctrl+Shift+0** for tab 10.
In 10xer mode, **t**, then **n** creates a tab, **t**, then **x** closes it,
and **t**, then **1–9 / 0** selects tabs 1–10. **t**, then **t** selects the
previous tab in strip order, wrapping from first to last. Escape cancels a pending chord.
The last tab's close shortcut closes the window. New tabs are added at the right
end of the strip. Closing the active tab selects the tab to its right, or the one
to its left when it was last.
The regular-mode terminal shortcut is **Ctrl+Alt+T**; 10xer keeps **;**, then **t**.
Tab shortcuts do nothing while a dialog is open.

In both key maps, **Ctrl+Enter** on a focused folder opens it in a new tab and
**Shift+Enter** opens it in a new window; keypad Enter works too. In the default map,
**Ctrl+Shift+Enter** on a folder also opens a tab; in 10xer mode it does nothing.
The file chooser opens no tab or window: there **Ctrl+Enter** from the file list
chooses the folder in a folder request, or confirms the destination in Move to,
Copy to and Extract to.
In a text field, these keys go to the field. On a file, both
open it with its default application, like **Enter**. With the pointer,
middle-click a folder in Columns, Icons or List to open it in a new tab, or
**Ctrl**+middle-click or **Shift**+middle-click to open it in a new window;
middle-clicking a file only selects it. **Open in… → New Tab** or **New Window** in
a folder's menu does the same. With several items selected, including at least one
folder, **Open in… → New Tab** or **New Window** opens one tab or window for each
selected folder and skips files. Selecting a tab returns focus
to the control that last had it in that tab, or to its file view's cursor when that
control is gone.

Each tab retains its location, selection, navigation history, preview and search
state. Tab locations persist across restarts: a plain launch (no folder
argument, reveal request, or unlock target) reopens the previous tabs in order
with the previously active tab selected, when **Settings → General → STARTUP →
Restore open tabs** is on (the default). The session is saved in
`$XDG_CONFIG_HOME/strata/tabs.toml`, which turning **Restore open tabs** off
deletes. Relative paths, local folders whose path is not
valid UTF-8, URIs that carry a
password (a user name alone, as in `smb://user@server/share`, is kept), locations
inside Trash, and Recent entries other than its root are skipped. So is every scheme
other than `smb`, `sftp`, `ftp`, `ftps`, `dav`, `davs`, `trash`, `network` and
`recent`, such as camera roots (`gphoto2://`) and `mtp://` devices. With nothing restorable the window opens
at the default directory as before. Every saved local folder gets its tab at once
and is checked in the background: a folder proven missing, or not a folder, closes
its tab and leaves the others. A folder whose check times out, as on a server that
does not answer, keeps its tab and shows its error, and loads by itself once the
mount answers. Up to 32 tabs are restored. When the saved
active tab is skipped, the nearest restored tab to its left is selected, or the first
tab when none is to its left. A saved active tab beyond the last restored tab selects
the last one. Windows opened for an explicit folder,
reveal request, or unlock target never overwrite the saved session; with
several plain-launch windows open the most recently changed one wins. Selection, history, and preview state stay
in-memory. Appearance preferences and the clipboard remain
shared. File operations prevent closing their tab or window until they finish
or are cancelled.

Tab names follow the active directory, not a child column shown only as a keyboard
preview: `~` for your home folder, `/` for the root, **Trash**, **Recent** and
**Network** for those places, in the interface language (**Papierkorb** in German),
and names longer than 22 characters are cut short with an ellipsis. On a remote location the name changes only once the new location
answers; a refused or replaced navigation keeps the previous name. A pending single-click folder activation keeps the previous tab name until
navigation resolves; cancelled clicks and drags restore normal focus-based naming.

The window title is the active tab's name followed by ` — Strata`, such as
`docs — Strata` or `~ — Strata`, and **Strata** before any folder opens. Navigating
the active tab or selecting another tab retitles the window; a background tab that
navigates does not. Like the tab name, the title keeps the previous folder while a
Columns folder press is pending.

The Material-style strip appears when there is more than one tab. The plus and
window-close controls move into it and return to the normal header when only
one tab remains. Scroll the strip horizontally (or use the wheel) when it
outgrows the window; selecting a tab brings it into view without a scrollbar.
Drag a tab label to reorder tabs: an accent insertion line marks the gap where it
will land, and dropping it on the **New tab** button moves it to the right end.

Middle-click a sidebar place, pin or mounted device row, or choose **Open in New
Tab**, the first item of its menu, to open that location in a new tab; the original
tab keeps its location and selection. Dragging a sidebar row, or only folders from
Columns, Icons, List, the preview header or a Ctrl+F result, marks an insertion line
after the last tab of a strip of two or more tabs. Over the strip the line moves to
the gap nearest the pointer, and releasing opens the location in a new tab there:
one tab per dragged folder, in drag order, with the last one selected. With one tab
the strip stays hidden, and the **New tab** button takes these drops. A folder-only
drag released over a tab header opens a new tab and moves or copies nothing into that
tab. Dropping a sidebar row changes neither the sidebar order nor the pins. Folders
dragged from another application are not opened as tabs. Unmounted device rows and
file choosers offer none of these tab actions.

Drop files, or a mix of files and folders, from a listing on a tab to transfer them
into its current directory: a same-volume drop moves, and holding Ctrl copies. Hover
over a tab during such a drag to switch to it and choose a folder in its listing.
Existing copy/move modifiers and conflict handling apply.

**Escape** cancels a drag in both key maps: a file drag from Columns, Icons, List,
the preview header or a Ctrl+F result, a tab drag, or a sidebar row drag, even before
the pointer reaches a target. Releasing then transfers nothing and opens or moves no
tab, on X11 too. That Escape dismisses nothing else: the selection, an open preview
and the filter stay, and the next Escape clears the selection or closes the
preview.

## Input precedence

<!-- node: operations/clipboard -->
<!-- node: browser/selection/pointer-intent -->
<!-- node: integration/open-with/terminal -->
<!-- node: operations/create -->
<!-- node: app/window -->

With exactly one folder explicitly selected, **Ctrl+V** pastes into that folder. A
folder selected for you when its directory loaded does not count: the folder you
came from after Up, Back or Forward, a restored selection, or the first item
selected on arrival. In those cases, and with a file, several items, or nothing
selected, the last navigation input determines the destination column:

1. Moving, clicking, or scrolling the pointer restores pointer control. Paste targets the directory column under it, not an individual hovered file or folder.
2. Keyboard navigation (arrows, **h**/**j**/**k**/**l**, Tab, page movement, entering/leaving folders) or Select All restores keyboard control. Paste targets the focused column, falling back to the active column when browser widgets do not hold focus.
3. Ctrl+V itself does **not** change ownership. A parked pointer cannot override subsequent keyboard navigation. Layout/scroll changes underneath an unmoving pointer do not count as pointer motion.
4. Outside the columns, pointer mode falls back to the focused/active directory. Stale depths are discarded. Icons and List continue to use their single active directory.

**Ctrl+V** while viewing Recent does nothing. After a paste, the destination is shown with the pasted items selected; in Columns, a pasted-into folder opens and keeps focus. While a text field has focus, **Ctrl+C**, **Ctrl+X**, **Ctrl+V** and **Ctrl+A** act on its text, not on files.

The terminal shortcut, **Ctrl+Alt+T**, opens in the selected folder whenever exactly one folder is selected, including a folder selected for you on arrival. After **Alt+Up** from `~/Projects/foo`, **Ctrl+V** pastes into `~/Projects`, but **Ctrl+Alt+T** opens in `~/Projects/foo`. Otherwise it uses the same destination column as paste, except that in Columns,
when the pointer's column has one folder selected and that folder is open as the
active column to its right, such as a folder just clicked open, it opens in that
folder rather than its hovered parent. When the terminal is Ghostty 1.3 or later, it
opens as a new Ghostty window, even with `gtk-single-instance = true`. New Folder remains keyboard-focus scoped. Context-menu paste and drag-and-drop retain their explicit destinations.

Keyboard navigation suppresses stale row-hover effects and pending folder peeks until deliberate pointer input resumes. It does not erase selection or the open folder path.

## Focus without selection changes

<!-- node: browser/selection -->
<!-- node: browser/selection/keyboard-navigation -->
<!-- node: browser/view-modes, Selection -->
<!-- node: operations/clipboard -->
<!-- node: operations/delete -->
<!-- node: operations/trash -->
<!-- node: operations/trash, Locations without Trash -->
<!-- node: operations/trash, Deletion confirmations -->

Pressing blank column content focuses that directory, including an empty one. A plain press there clears file selections in every column immediately and closes the columns to its right; releasing it does not clear them again. When returning to an inactive column, it also selects that column's first visible entry as the range anchor. Presses with Ctrl or Shift held keep the selection until marquee intent is resolved, so a drag can extend it. A plain click on blank space or a disabled control in a preview that is showing something leaves the selection alone; the empty reserved preview slot clears like other empty space. Row clicks, controls, scrollbars, context menus, and marquee selection keep their own interactions. Returning to a column by keyboard preserves a multi-selection; Ctrl+A selects the focused column, not the deepest open column.

**Ctrl+click** toggles one item in or out of the selection and makes it the range anchor; **Shift+click** selects every item from the anchor to the clicked item. After a navigation selects the first item, the first Shift+click ranges from that item. Any click re-anchors **Shift+Up / Shift+Down**, so keyboard extension continues from the clicked item. A Ctrl+click or Shift+click on an item's name or icon moves the keyboard cursor to that item, so the preview follows it. In List and Icons, as in Columns, a Shift+arrow after a Ctrl+click extends from the Ctrl+clicked item: click the first of five items, Ctrl+click the third, and **Shift+Down** in List or **Shift+Right** in Icons selects only the third and fourth.

**Shift+Up / Shift+Down** extends the selection from the range anchor by one item, **Shift+Page Up / Shift+Page Down** by one page; the file chooser leaves **Shift+Page Up / Shift+Page Down** to GTK. **Shift+Down** with nothing selected selects only the first item; the next selects two. After Escape clears the selection, the range starts at the cursor. With hidden files off, **Ctrl+A** in Icons, List and the file chooser leaves hidden items unselected.

**Escape** closes one thing at a time. An open menu, Properties, a rename or new-item editor, the location editor, a filter, or quick preview closes first. With none of those open, Escape clears the active pane's selection and keeps the keyboard cursor and the directory, so **Enter** then opens the folder under the cursor. In Columns, Escape clears only the active column; parent selections and open columns stay. Outside 10xer mode, Escape with nothing selected in the active column closes the deepest column.

Copy/cut use the selection in the focused column, never a hovered row. In Columns, **Ctrl+C** or **Ctrl+X** with nothing selected in the focused column acts on the folder that column shows. **Delete** moves the selection to Trash without asking; **Shift+Delete** opens the permanent-deletion confirmation. Outside 10xer mode, both act on the selection even when focus is outside the file list, such as on a header button. In Trash, Delete also asks to delete permanently. Items inside a trashed folder cannot be deleted from the keyboard. With a Ctrl+F result selected, Delete moves that result to Trash and leaves the hidden directory selection alone. While the filter input or a text field, such as preview text, has focus, Delete and Shift+Delete never delete files. In Columns, Delete or Shift+Delete with nothing selected acts on the focused column's keyboard cursor row. When that column has neither a selection nor a cursor, such as an empty open folder, it acts on the open folder itself. In List and Icons, Delete acts on the selection only. Delete in a location without Trash support, or after a Trash attempt fails because Trash is unsupported, opens the permanent-deletion confirmation with Cancel focused and the reason stated; Shift+Delete is unchanged. The reason reads **This location doesn't support Trash.**, followed, for a mount that refused Trash, by the mount point and its type, such as **Trash isn't available on /mnt/cloud (fuse.rclone).** Most writable FUSE mounts, such as sshfs, rclone and cloud drives, claim Trash support; once one refuses, Strata remembers it for that mount, so later Deletes there ask first. When every selected item is on a network or cloud location, the confirmation is titled **Delete N items without Trash?**, says Strata can't undo it and that recovery depends on the storage provider, and its button reads **Delete N items**. Local disks, `fuseblk` drives, local FUSE overlays such as mergerfs, and a mixed selection keep the **Permanently delete N items?** title and **Permanently delete N items** button, including after a refused Trash attempt. When a Trash attempt fails partly for other reasons, or a background deletion's Trash attempt fails while another operation runs in the foreground, the error dialog offers a button that opens this confirmation: **Delete without Trash** for remote items, **Delete Permanently** otherwise. For a background deletion, the button first minimizes the operation in progress when it can run in the background, then opens the confirmation. If an operation is still running in the foreground, it shows **Another operation is active** instead, and the failed items are not deleted. After **Shift+Delete**, the confirm button has focus and works while the total is still being calculated.

Background selection updates from directory loading must not move keyboard focus to an inactive column.

When the focused item is deleted, in Strata or by another program, focus moves to the next visible item, or to the previous one when none follows, and the preview follows it. In Columns, deleting the focused open folder scrolls the
item that takes its place, folder or file, into view and, with **Mirror columns
selection** on, mirrors it as keyboard movement does (see
[Arrows, the header, and the sidebar](#arrows-the-header-and-the-sidebar)); with it
off, the item is only revealed. Deleting the last visible item clears focus and selection. Other background changes to an open directory keep the selection and scroll position and never take focus.

## Returning to a visited directory

<!-- node: browser/view-modes/position-restore -->
<!-- node: browser/navigation -->
<!-- node: integration/file-manager-interface -->
<!-- node: browser/view-modes/columns -->

Icons and List remember the selection, range anchor, keyboard cursor, and scroll position of the
last 128 directories left in that browser. Every route back to a visited directory
restores it after its entries load, including nested parents: Back, Forward, Up,
breadcrumbs, and typed paths. Arrow-key navigation continues from the restored row,
and **Shift+arrows** extend from the restored anchor.
Entries are matched by location, not their previous row numbers; deleted entries are
not selected accidentally. The selection and cursor carry over between Icons and
List; the exact scroll position comes back only in the view it was left in (and, for
Icons, at the same width), otherwise the cursor is scrolled into view. This is
temporary browsing state, not a saved preference. A click, scroll or key press in the
file view, a view switch, or a failed load cancels an in-progress restoration. Back, Forward and Up move keyboard focus into the restored
listing only when focus was inside the pane being left (its Ctrl+F field included)
or nowhere:
from a header button or with the sidebar focused, they restore the selection and
leave focus where it is. Sidebar places, breadcrumbs and typed paths focus the
listing, as on a first visit.

In Columns, Back, Forward, Up and breadcrumbs that return to an ancestor of the
current directory select the folder you came from, with the cursor on it, and leave
its column closed. When that folder is gone or hidden, the first visible entry is
selected instead; hidden files stay hidden. Back to a folder that is not an ancestor
selects its first item. Icons and List do the same as Columns for an ancestor when
they have no remembered position for it.

A navigation that names a target — a typed file path, a Ctrl+K result opened with
Enter or Alt+Enter, Open file location, or an `org.freedesktop.FileManager1`
request — selects that target instead of restoring the remembered position.

## Refreshing a directory

<!-- node: browser/view-modes/position-restore -->
<!-- node: browser/directory-monitoring -->
<!-- node: browser/directory-monitoring, Mounts that stop answering -->
<!-- node: browser/view-modes, Loading and names -->
<!-- node: browser/selection -->
<!-- node: browser/view-modes/columns -->

**F5** reloads every open column in Columns, and the active pane in Icons and List.
Each pane header's Refresh button (tooltip **Refresh (F5)**) reloads only that pane.
With **Settings → General → PERFORMANCE → Watch network folders** on (the
default), open folders on network and FUSE mounts are checked every few seconds and
re-read when a check finds a change.

F5, the pane's Refresh button, the rescan after a burst of external changes, and
the re-read after a network-folder check keep the selection, the keyboard cursor and
the keyboard focus in every view: a focused row stays focused, and a focused Ctrl+F
field keeps focus and its text. While the rows are briefly hidden, focus stays on
the pane and returns to the cursor row. Icons and List also keep the scroll position. When the item under the
cursor is gone, the cursor moves, without selecting anything, to the next visible
item at its old position, or to the previous visible item when none follows. In
Columns, this does not happen in a column whose child column is open: no other item
takes the cursor there. When a reload removes an open rename field, **F2** renames that
row again and **Menu** or **Shift+F10** opens its menu.

A refresh never takes focus from the sidebar, the location entry or a dialog. During
a slow reload, typing in the Ctrl+F field does not stop focus returning there; **Tab**
or pointer input does, and **Escape** that closes the filter sends focus to the
listing instead.

When a mount stops answering, after 10 s without progress **Not responding. This
list may be out of date.** shows above the folder's last listing in Columns, Icons
and List, and clears as soon as the mount answers. There, F5, **Retry** and a rescan
keep the shown rows instead of showing an error. Once a request on the mount has
gone 2 s without progress, opening another folder on it fails at once with **The
operation timed out**.

## Creating files and folders

<!-- node: operations/create -->
<!-- node: operations/rename -->
<!-- node: browser/selection/keyboard-navigation -->
<!-- node: browser/directory-monitoring, Renaming to a hidden name -->

In Columns, List, and Icons, **Ctrl+Shift+N** or background menu → **New Folder**
immediately creates `new folder`. Background menu → **New File** immediately
creates an empty `new file`. If the default name is occupied by any item, creation
tries `new folder (1)` / `new file (1)`, then `(2)`, and so on without overwriting
anything. The pane filter is cleared and the entire allocated default name is
selected: one Backspace clears it, and typing replaces it.

In Columns, a new folder opens as the child column, replacing any stale child
column, and the breadcrumb follows it. A new file closes stale child columns,
returns the breadcrumb to the parent, and does not open. In List and Icons, the
view stays in the parent folder and selects the new item without opening it.

Item menu → **New Folder with Selection** (or **Ctrl+Alt+N**) creates `new folder`
in the same directory, moves the selected items into it, and names it in place.
With nothing selected **Ctrl+Alt+N** falls back to a plain `new folder`. The item
is hidden in Trash, Recent, and while a recursive search is open.

Outside 10xer mode, **F2** or **Ctrl+R** on the focused item opens an inline name
editor; with Alt, Shift or Super also held, or as **Ctrl+F2**, neither starts a
rename. While another text field has focus, they go to that field, except that in
the pane filter they rename the focused item. **F5**, not Ctrl+R, refreshes. In the
editor, **Ctrl+A** selects only the field's text, and **Ctrl+1**, **Ctrl+2** and
**Ctrl+3** stay in the field instead of switching views.

For **any file or folder rename**, Enter, Tab, clicking outside the field (even empty
pane space), or moving keyboard focus to another control in the window commits a
valid name. Switching to another window, or an input method switcher taking the
keyboard, leaves the editor open and renames nothing; back in the window, focus is
still in the field and **Enter** commits. **Tab** also leaves
the listing, or the strip in Columns. Escape keeps
the original name. Finishing with an empty or invalid name also keeps the
original. Cancelling the initial rename does **not** delete the new item: it
remains under its allocated default name. File contents are preserved.
While a name is being edited, **F5**, **Ctrl+K**, **Ctrl+Shift+K**, **Ctrl+Alt+T**
and **Ctrl+\\** do nothing; finish or cancel the edit first.

Clicking inside the field continues editing. With a long name in a narrow
column, End, typing, and the arrow keys keep the caret and the extension in view. Existing files retain extension-aware
selection (the stem is selected); folder names containing dots are selected in full.

Names containing `/` or NUL, `.`/`..`, and whitespace-only names (including
Unicode whitespace) are invalid. Valid names are used exactly as typed,
including spaces around a nonblank name, hidden-file prefixes, and Unicode.
While you type, an invalid name puts the field in the error style and sets its
accessible description, with no tooltip: **Names cannot contain /** for a `/`,
**That name is reserved** for `.` or `..`, and **Enter a name** for a
whitespace-only name. An empty field is not styled as an error.
Name conflicts, filesystem-specific limits, and permission errors retain the
original item and report an error. A rename never replaces an item created at the
new name meanwhile. A name the location would store as another, such as `x:y` or
`notes.` on a FAT drive, is refused before anything changes, with **Names in this
location can’t contain “:”**, **Names in this location can’t end with a space or a
period**, **“CON” is a reserved name in this location**, or **The name is too
long**. A case-only rename, such as `notes.txt` to `Notes.txt`, works on FAT,
exFAT, SMB and case-folding ext4, and so does its undo. After a rename onto an existing name, Escape on
that error returns focus to the item's row.

When a rename moves the item in the sort order, **Down** continues from its new
position to the next item. With hidden files off, renaming an item to a dot name
moves the cursor to its visible neighbor in the same folder, so **F2** renames that
one next. In Columns, a folder renamed that way also closes its open column and every
deeper one, without reloading the parent column or adding a Back entry. With hidden
files shown, or a visible new name, the row and its open columns follow the rename.

## Filename patterns while filtering

<!-- node: browser/search/filter -->
<!-- node: browser/directory-monitoring -->

Use **Ctrl+F** to filter a pane; in [10xer mode](10xer-mode.md), **Ctrl+F** pages
down and **f** filters through the footer prompt instead. With **Type to search** on
(the default), typing a printable character in a file view opens the filter with
that character as the query, and **/** opens an empty filter without typing `/`.
**Space** still opens quick preview, not the filter. Plain text matches a substring of the filename,
ignoring case. Queries of at least four letters or digits also allow one inserted,
missing, substituted, or adjacent swapped character within a whole filename word.
Words are separated by punctuation or spaces. For example, `trahs` finds
`strata-trash.svg`, but `trash` does not find `strata-search.svg`. Shorter queries
and queries containing punctuation remain literal. A query with spaces also
matches names that contain every word, in any order: `duck txt` finds `duck.txt` and
`ducks_in_the_pool.txt` but not `only-duck.md`, and `summer holiday` does not find
`holiday.jpg`. Each word of four or more letters or digits allows one typo, so
`abc text` finds `abc_tent.doc` but `abc tex` does not. A trailing space keeps the
matches. Indexed results rank literal matches ahead of typo matches, and a name
containing the whole query ahead of one matching scattered words; parent paths do
not qualify a result.

Add `*` for a whole-filename pattern without typo tolerance:

- `*.MOV` matches `clip.MOV`, but not `clip.MOV.bak`.
- `IMG*` matches names beginning with `IMG`.
- `IMG*.MOV` combines a prefix and an extension.
- `*holiday*` matches names containing `holiday`; `*` matches any name.

Each `*` stands for zero or more characters. Other punctuation (including `?`,
`[]`, and regex syntax) is literal, and so are spaces: `duck *.txt` needs `duck ` at
the start of the name. Patterns match file and folder names, not
parent paths, in Columns, Icons, List, and the file chooser. Hidden-file visibility
and [Include subfolders](../guide/search.md) still control the scope;
a wildcard does not enable recursive search. Existing result limits still apply,
and so do **Search time limit** and **Search entry limit** in **Settings → General →
SEARCH & FILTERING**: the filter reads them at each query, and a walk they stop shows
the same partial-results message as **Ctrl+K**.
Clear the input, or press Escape in the input or on a focused result, to restore
the directory listing with focus on its cursor. **Backspace** in an empty, focused
filter input also closes the filter. **Ctrl+K** global fuzzy search is
unchanged.

Results follow the watched folders live: the open folder, and in Columns every open
column. A matching file that another program creates or renames there appears within
about a second, and one that another computer adds to a network folder appears at
its next check. A deleted one leaves the results as soon as the listing drops it; a
result whose check fails or times out, as on a mount that stopped answering, stays.
With [Include subfolders](../guide/search.md) on, changes in folders below
those reach the results on **F5**, a network-folder re-read, the rescan after a burst
of external changes, or when the filter is cleared and opened again.
When another program renames the open folder itself, the view follows it and a filter
typed in that folder ends, while filters and **Ctrl+K** searches rooted above it follow
the rename. When the open folder is deleted or moved into another folder, the view
returns to its nearest parent that still exists, or reloads the folder if it already
exists again; either way the filter ends. Neither adds a history entry.

## Preview while filtering

<!-- node: browser/search/filter -->
<!-- node: browser/search/filter, Results -->
<!-- node: browser/view-modes, Filtered clicks -->
<!-- node: browser/view-modes/columns, Filter field -->
<!-- node: integration/10xer-mode/search, Focus return to results -->
<!-- node: preview/quick-preview -->

In the browser, **Enter** in the Ctrl+F input opens the top result, in Columns, Icons and List; in the file chooser it chooses it. While the input has focus, the top result has a 1 px accent outline, and the list keeps it scrolled into view as results arrive until you press, scroll, touch or drag over the results. The outline is not a selection: with only the outline showing, Space types a space, and file actions need a selected result. Picking a result, with an arrow key, Down from the input, a click or a Ctrl+click, removes the outline, and Enter then opens the pick; deselecting every result returns Enter to the top result. Editing the query drops the pick and the results' selection, and the outline moves to the new top result. In Trash, Recent or a network share, where the input narrows the listing itself, an edit keeps the folder's selection but still drops the pick. An update for the same query, such as another program creating a matching file, keeps the pick, the selection and its preview, and results that still match keep their rows without flashing. In a column's filter, **Right** moves the caret and never opens the top result. In 10xer mode no result is outlined, and the **f** and **s** prompts keep their own two-step Enter.

In the browser and file chooser, **Down** from the Ctrl+F input focuses the outlined top result, or the result you picked. **Up/Down** then navigate the results; **Up** from the first result returns to the input without clearing the query. **Ctrl+F** also returns to the input. With no matches, Down leaves focus in the input. **Enter** on a focused result opens it, whatever the click-count and preview preferences. **Shift+arrows** and **Ctrl+A** select results. **Ctrl+C** and **Ctrl+X** act on the selected results at their real locations. When the selected result disappears from the results, the next result, or the last remaining one, is selected. In List and Icons, **Delete**, or **Shift+Delete** and confirm, on a focused result moves focus, with a visible focus ring, to the first remaining selected result; with none left selected, to the result now in the deleted one's place, or the last result. Deleting the last remaining result moves focus to the input. **Escape** then closes the filter. After a dialog or overlay opened from a result closes, quick preview included, focus returns to the result under the results' cursor in Columns, Icons and List, without changing the selection; **Tab** into the pane while results show does the same, and a rename in progress keeps focus in its field. In List and Icons, **Tab** from a focused result leaves the results in one press, and **Shift+Tab** then returns to the result that held the cursor. In Columns, moving focus out of the filtered column closes its filter, while focus in its own results, a popover or a dialog keeps it; opening a filter in one column closes and clears any other column's filter.

**Menu / Shift+F10** on a focused result opens its file menu. While the input itself is focused, its text-editing menu remains available. **Space** toggles quick preview for a selected file result in Columns, Icons, and List, including after returning to the query. Previewing a file keeps the query, selection, and current directory intact; on a selected folder result, Space navigates into the folder instead.

While the input is focused, Space types into the query if no result is selected. **Shift+Space** inserts a space there even with a result selected. Space acts on a selected result only from the input and the results: the location bar, the preview find bar, the archive password field and the file chooser's name and location fields type it, and sidebar rows and toolbar buttons keep their own Space. Space opens a selected folder in every view without opening or loading the preview pane; unsupported files do not open a preview.

A plain click on a folder result opens it, whatever the click-count preferences. A plain click on a file result follows them, in Columns, Icons and List: with files opening on one click it opens the file once, with no preview; with two clicks and **Single-click file previews** on, it selects and previews a previewable file, and a double-click opens it once; otherwise it only selects it. In the file chooser and in Trash, a plain click never opens a file result: it previews a previewable one when single-click previews are on, and otherwise selects it. A click on a selected file result starts no slow-click rename.

With a result focused, the first **Escape** dismisses the filter even while its quick preview is open; a second Escape closes the preview. **Ctrl+1**, **Ctrl+2** and **Ctrl+3** keep focus in the filter: in the input with the caret after the query, or on the focused result. When you switch views with a query typed and focus elsewhere, for example from the View menu, the results take focus once they show. Loading or refreshing the folder never moves focus out of the input or its results. Neither does another program changing the folder, and that also holds for the [10xer](10xer-mode.md) **f** and **s** prompts.

## Navigating an archive preview

<!-- node: operations/archives/preview -->

Quick preview (**Space**, or the item menu's **Quick preview**) on a local ZIP, 7z,
TAR, or TAR.GZ/TGZ opens the archive's member tree instead of extracting it. In Columns (**Ctrl+1**), automatically previewing an
archive shows its contents on the right without selecting a member or taking
keyboard focus. **Up/Down** continue through the current column. **Right**,
**Enter**, or **Space** explicitly enter the archive preview and highlight its
first member. Enter opens the preview even when automatic previews are disabled;
double-click and the archive's context menu still offer extraction. In Icons
and List, Enter retains its archive extraction behavior.

In every view, moving the cursor onto an archive while the preview is open updates
the preview without taking keyboard focus: a plain archive shows its members with
none highlighted, and the next arrow keeps moving through the listing. A
password-protected archive shows its password prompt with the field unfocused; in
List and Columns, **Right** then focuses the field. Opening the preview on an
archive with **Space** enters it directly, highlighting the first member or focusing
the password field. In List and Columns modes, arrow keys act on the focused pane,
not merely on an open preview. From the listing, **Right** enters the open
preview. While the preview owns focus, its header shows the accent top border
instead of the Miller column. Returning to the listing restores its cursor
and column header indicator without changing the listing's selection.

Inside the preview, **Up/Down** move the highlight, **Right/Enter** opens the
highlighted folder, and **Left** returns to the parent. With **Type to search** off,
or in 10xer mode, **k/j**, **l** and **h** do the same. Keyboard movement never
reaches the preview's Close button or **F1**, and only the current member is
outlined. A single
click highlights a member and opens a folder; hovering never changes the
highlight or the keyboard cursor. **Left** at the archive root returns focus to
the listing without closing the preview. Up/Down then move through listing
items; Right enters the preview again. In Columns mode, another Left from the
listing moves to the parent column. Right/Enter on a member file does nothing.
Navigating never extracts anything or touches the filesystem; **Space** and
**Escape** still close the preview, which leaves the archive selected in the
listing. In Columns, Escape from inside an entered
archive preview closes it and returns focus to the archive in its column. In
[10xer mode](10xer-mode.md#preview-keyboard-ownership), **h** at the archive root
returns to the listing, **Space** is swallowed, and **Shift+Tab** / **Escape**
return or close.

## Media preview keys

<!-- node: preview/preview-panel/media -->
<!-- node: integration/10xer-mode/preview-keys -->

In the default map, while focus is not in the sidebar, the top bar or a text field,
**Ctrl+Alt+Space** plays or pauses, **Ctrl+Alt+Left / Ctrl+Alt+Right** seek 5 s,
**Ctrl+Alt+Up / Ctrl+Alt+Down** change the volume by 0.1, **Ctrl+Alt+M** mutes, and
**Ctrl+Alt+<** / **Ctrl+Alt+>** step to the previous or next file of the open
preview's kind: from a video to the adjacent video, skipping audio files, and from
an audio file to the adjacent audio file, skipping videos. In 10xer mode, **<** and
**>** do the same.

Audio and video previews show a timeline; **Tab** or a click focuses it. While
it has focus, **Left/Right** seek 5 s, and **Shift+Left / Shift+Right** or **Page
Down / Page Up** seek 30 s. **Home** or **0** returns to the start; **End** or
**G** jumps to the last frame, since seeking to the very end would stop
playback. **+** / **=** and **−**, including the keypad's, change the volume by
0.1; reaching zero mutes and keeps the volume to restore. Unlike **Left/Right**,
the paging, jump and volume keys have no **Ctrl+Alt** form. The volume slider
steps 0.1 with the arrow keys and 0.2 with Page Up/Page Down; **Home** mutes and
**End** sets full volume. Key steps snap to the 0.1 grid, so repeated **Down**
reaches zero and mutes; a drag sets any volume. Other playable files show a seek slider instead of a
timeline: the arrow keys step 5 s, Page Up/Page Down 30 s, and Home/End jump to the
start and the last frame. Keys and the mouse wheel seek at once; a drag seeks
when released. In
[10xer mode](10xer-mode.md#preview-keyboard-ownership), whenever the media preview
owns the keys, **Space** plays or pauses, **m** mutes or unmutes, **Up/Down** change
the volume, **<** and **>** step to the adjacent file of the same kind and keep
playing, and the timeline keys above also work.

## Shortcut footer

<!-- node: app/shortcut-reference -->
<!-- node: settings/preferences -->
<!-- node: integration/10xer-mode -->

Every mode has a compact footer with an **F1 Shortcuts** button on the left and clipboard status and the item count on the right. The button toggles the reference and shows as pressed while it is open. **Settings → General → BROWSING → Show F1 Shortcuts button** controls the button's visibility (on by default). The preference is saved and updates all open windows immediately. Item counts and clipboard status remain visible when the button is hidden. With the button hidden and no other footer status to show, such as a count, the clipboard badge, or the **10X** tag in 10xer mode, the whole footer hides. F1 opens the **Keyboard shortcuts** panel centered over the dimmed, blurred window; focus cannot leave it until it closes. F1 always opens the complete, mode-specific reference; closing it restores the button's configured visibility. F1, Escape, or a click outside it closes the reference, which blocks file operations and commands such as **F5**, **Ctrl+K** and **Ctrl+,** while open. It stays open when the window loses focus. The reference is the only complete in-app keybinding list; it shows only the currently active map and live-updates when 10xer mode changes. In 10xer mode, a pending chord's footer panel also lists the keys that can follow it.

The reference opens with focus in **Search actions or keys…**, scrolled to the top. Typing keeps the rows whose keys, key context or action contain the text, ignoring case. Translated text matches, and key names match in English and in the interface language: under German, `strg+c` and `ctrl+c` both find Copy. Each alternative in a row also matches spelled out in full, so `ctrl+0` finds the **Ctrl++ / − / 0** text-size row. A typed `-` matches the − in labels and the – of digit ranges, so `1-9` finds **Ctrl+Shift+1–9 / 0**. A query with no match shows **No matching shortcuts**, centered in the results area. The category list shows **All** and each section with its row count; choosing one shows only that section. In windows narrower than 1480 px, the header stacks, categories become wrapping pills without counts, and results use one column. In the default map the sections are the current view's navigation (Columns, Icons or List), then Files and selection, Search and tools, and Preview media. In Icons, the navigation section lists **Ctrl+Alt++ / − / 0**, Increase / decrease / reset thumbnail size; in 10xer mode **+** and **−** join the increase and decrease keys, and **Ctrl+Alt+0** has its own row. Search and tools lists **Ctrl+Shift+T**, Reopen the last closed tab. In 10xer mode the reference adds Places, Preview and a 10xer mode section for keys the default map lacks. Reopening the reference keeps the previous search text and category. In the search field, typing, **Delete**, **Ctrl+A**, **Ctrl+C**, **Ctrl+V** and **Ctrl+X** edit the query, and **Up**, **Down**, **Page Up** and **Page Down** scroll the results without moving focus, **Ctrl+Z** undoes the last query edit, and **Ctrl+Y** or **Ctrl+Shift+Z** redoes it. Text-editing and input method keys work there too, such as **Ctrl+Left**, **Ctrl+Backspace** and **Ctrl+Space**; any other Ctrl, Alt or Super chord does nothing, so **Ctrl+,** opens no Settings. **Tab** and **Shift+Tab** cycle the search field, the selected category and the results. **Ctrl+B** jumps to the categories, **Ctrl+F** to the search field and **Ctrl+L** to the results. In the categories, arrows or **h**/**j**/**k**/**l** select the previous or next category, and Home and End the first or last. In the results, arrows, **j**/**k**, Page Up/Page Down and Home/End scroll the list. A line at the bottom summarizes these keys: Ctrl+B categories · Ctrl+F search · Ctrl+L list · j / k / ↑ / ↓ move · Tab cycle · Escape close. In 10xer mode `~` also toggles the reference; in the default map it does not. In 10xer mode a focused footer prompt or text field, such as the location bar, types `~` instead, and F1 still opens the reference; `~` typed in the open reference's search closes it. On the Russian layout the ё key acts as `~` only outside text fields: in a text field, the reference's search included, it types ё or Ё. F1 with Ctrl, Alt, Shift or Super held does not toggle the reference, and while it is open **Ctrl+1**, **Ctrl+2** and **Ctrl+3** do nothing. Closing it returns focus to the control that had it before.

## 10xer mode

<!-- node: integration/10xer-mode -->
<!-- node: integration/10xer-mode/search -->
<!-- node: integration/10xer-mode/file-chooser -->
<!-- node: app/shortcut-reference -->
<!-- node: browser/context-menu -->
<!-- node: operations/clipboard -->

**Settings → General → BROWSING → 10xer mode** (off by default,
toggle with **Ctrl+Shift+M**) hides window Search and
pane Close/filter/refresh/sort chrome and installs Yazi-style keys.
**Ctrl+Shift+M** is the only key that leaves the mode. While the mode is on, the footer shows
**10X** in its far right corner, after the item count.
10xer's typed commands (**f**, **s**, **/** and the other prompts) use the footer
prompt, never the pane filter revealer. **Ctrl+K** still opens global search. See [10xer mode](10xer-mode.md) for the keymap.

**Ctrl+Shift+M** also works while a browser text field has focus. Modal dialogs
retain their own input handling. Leaving 10xer mode clears retained footer
filters/search and forced recursion in all windows, so default **Ctrl+F** obeys
**Include subfolders** again. It ends visual/preview keyboard ownership without
clearing the ordinary listing's fill or closing the preview. **Escape** dismisses
one interaction at a time, including an open preview; recursive results have a
separate order described in [Escape precedence](10xer-mode.md#escape-precedence).

The F1 / `~` reference panel lists the active map and live-updates when the mode
changes. Its navigation section is specific to the current view, and in the
portal file chooser it lists only the keys that request allows.
Context-menu hints use `x`, `y`, `p`, `d` / `D`, `r`, `i`, and `M` / `C` / `R`
(Move to, Copy to, Restore). `i` toggles a file's preview without taking focus, or is the next column or folder peek for a directory.
Rename shows `r` instead of F2 / Ctrl+R. Copy path, Duplicate, Pin to sidebar,
Open in Terminal, and Quick preview in the file chooser show no hint. Other rows
keep their default-map hints, such as Enter beside Open. In the default map, the
`y` (copy path) and `p` (pin) hints show only while **Type to search** is off,
because type-to-search claims those letters otherwise.

While a pane shows its search-results page (including filtered results), the footer
shows the displayed result total in both default and 10xer mode, including
**0 items** on a miss.
Selecting results does not replace that total with the hidden directory's selection;
its accessible description gives the result file/folder breakdown. Dismissing results restores the
ordinary directory count or selection summary. Until the search for a typed query
reports back, the footer keeps describing the directory. The `filter:` / `search:`
mark and the hit path at the footer's left end show only in 10xer mode, which
hides the pane's filter input; the default map shows the total alone.

With no selection in the ordinary listing, the footer shows the directory's item count, such as **12 items**; its accessible description gives the file and folder breakdown. Selections show a folder/file breakdown, such as **1 folder, 2 files selected (64 MB)**. Selecting every item shows the breakdown without a size, and selecting more than 64 items, but not all, shows **N items selected** without a size. Sizes sum available metadata for selected files only; folder contents are not scanned or included. Missing file sizes are marked incomplete or unavailable.

After copying or cutting files, a highlighted **Files on clipboard** pill appears to the left of the item count. Its accessible description reads **Press Ctrl+V to paste into a supported directory.** It reflects the file clipboard, including compatible copies from other applications, rather than assuming every clipboard contains files. It stays available after copying/pasting, and disappears when a completed cut consumes the clipboard or it is cleared/replaced with text. The clipboard status and paste shortcut remain available when the F1 Shortcuts button is hidden. Copied listing items show the Lucide copy icon in place of their thumbnail; cut items keep scissors, which wins if both would apply. Clearing the clipboard or unyank removes the copy overlay.

The hints describe file-view controls; text fields, dialogs, and media previews retain their own keyboard behavior. Mode changes update both the footer and the reference immediately. Closing keyboard-opened help restores the previous focus.

## Arrows, the header, and the sidebar

<!-- node: browser/selection/keyboard-navigation -->
<!-- node: browser/sidebar -->
<!-- node: app/window -->
<!-- node: browser/view-modes -->
<!-- node: app/accessibility -->
<!-- node: browser/view-modes/columns -->
<!-- node: browser/selection/click-modes -->
<!-- node: preview/preview-panel/layout -->
<!-- node: preview/preview-panel/media/video -->
<!-- node: preview/quick-preview/folder-peek -->
<!-- node: integration/portal-file-chooser -->
<!-- node: browser/navigation -->
<!-- node: preview/quick-preview -->
<!-- node: operations/archives/preview -->
<!-- node: integration/10xer-mode -->
<!-- node: integration/10xer-mode/preview-keys -->
<!-- node: app/window, Header -->
<!-- node: app/window, Sidebar state -->
<!-- node: browser/view-modes, Pane header names -->
<!-- node: browser/folder-customization -->
<!-- node: operations/archives -->
<!-- node: browser/search -->

In Icons and List, plain arrows move interface focus rather than changing directories:

| Key | Icons | List |
| --- | --- | --- |
| Left | Move one tile left; at the left edge, focus the visible sidebar | Focus the visible sidebar |
| Right | Move one tile right | Stay in the file list; on a file, enter an open preview |
| Up / Down | Move by visual rows | Move through file rows |
| Enter | Open the current item | Open the current item |

In both views, Up and Down also select the item they land on, replacing the
selection. They never open it, even when single-click opening is on.

Enter on a previewed video, from the listing or inside the preview, pauses the
preview and asks the default player to start where it stopped. mpv, VLC,
Celluloid and MPlayer take the position on their command line; other players
open the file from the beginning, as does a position inside the first or last
second.

Up from the first Icons row or first List item focuses the navigation header, including in empty directories, where the pane itself holds focus. Left/Right traverse its enabled controls without triggering navigation; Enter/Space activates a control. Down returns to the item you left without changing selection. Left from the header's first control can reach the visible sidebar.

In Columns, Up from a column's first item focuses that column's header controls, and Down returns to its list. Left from a column's first header control, or Right from its last, moves into the neighboring column's header. Left in the first column focuses the visible sidebar on the row for the current place.

From the sidebar, Right returns to the item you left (or the current file view if navigation replaced it, or if you entered the sidebar from the header rather than from a file). Up/Down move between places. Up from the first sidebar row (Home by default) continues into the **top navigation bar** instead of stopping. Left/Right traverse its enabled controls without activating them; Down returns to the sidebar row you left. If the sidebar is hidden from the top bar, Down returns to the files instead. Empty file views also support these round trips. If the sidebar is hidden, Left in the file view does not change directories.

In the default map, **Ctrl+B** or the header's sidebar button steps the sidebar from full to the icon rail to hidden, then back to full. Each step applies to every browser window and is saved, so new windows open the same way. The button's tooltip names the next step, **Compact sidebar (Ctrl+B)**, **Hide sidebar (Ctrl+B)** or **Show sidebar (Ctrl+B)**, while its accessible name stays **Toggle sidebar (Ctrl+B)**; in 10xer mode both name **Ctrl+N**. The rail shows each row as an icon with its name as a tooltip. A rail you chose stays when the window widens. When the full sidebar does not fit beside one column, or beside the preview while one is shown, it rails by itself and expands again once there is room; that rail is not saved. Stepping from hidden shows the full sidebar even in a narrow window, until the window or the preview next runs out of room. In the file chooser, the button and **Ctrl+B** step only that dialog's sidebar and are not saved. **Ctrl+Shift+B** shows a hidden sidebar and focuses the row for the current place; pressing it again in the sidebar returns focus to where it was. Outside 10xer mode, **Enter** on a sidebar row opens the place with its first item selected; a click opens it with nothing selected. In Icons and List, a folder you left recently restores its remembered position instead. A place that fails to open, or whose mount fails or is cancelled, leaves the pane and the sidebar highlight on the place already open.

In the default map each file listing is one **Tab** stop; arrows move inside it. **Tab** from the listing goes to the next interface control (the open preview's controls, then **F1 Shortcuts**), and **Shift+Tab** goes back through the List sort headings, an open filter and the pane header actions, then the sidebar. **Tab** or **Shift+Tab** into a listing lands on the keyboard cursor, so **Enter**, **Space** and **Ctrl+C** act on the item that shows focus. In Columns the whole strip is one stop: **Tab** into it lands on the active column's cursor without changing the active column, **Tab** from any column leaves the strip, and **Shift+Tab** reaches the active column's open filter, then its header actions, then the control before the strip.

Screen readers announce each item by its name, described as Folder, File, Folder link, File link, Broken link or Other. Each pane is a group named after its directory and described as Columns view, Icons view or List view, and the item list inside it is named after the directory and described as Files. Pressing **Tab** repeatedly from the window's first control reaches the listing. Menu items are named after their action and carry their shortcut in their description, not their name. Selecting an item sets the selected state on that item and on no other. With default preferences, the header buttons are named **Search (Ctrl+K)**, **Appearance**, **Settings**, **Close window** and **Toggle sidebar (Ctrl+B)**. Modal dialogs have the dialog role and are named after their title. Item kind, view and list descriptions are in the interface language, and shortcuts in accessible names and descriptions use its key names, such as Strg in German. An icon-only button shows a tooltip, such as **Search (Ctrl+K)**; labelled buttons, menu items, file rows and breadcrumbs show none. A sidebar place's or breadcrumb's full path is its accessible description, not a tooltip.

In List and Icons, the pane header's buttons are named **Back (Alt+←)**, **Forward (Alt+→)** and **Parent folder (Alt+↑)**. The Ctrl+F field is named after its toggle: **Filter this pane (Ctrl+F)** in Columns, **Filter icons (Ctrl+F)** in Icons and **Filter list (Ctrl+F)** in List. The Icons slider is named **Thumbnail size**, the List columns button **Columns**, the **Ctrl+K** field **Search files and folders…** and the F1 search field **Search actions or keys…**. Other icon-only buttons carry names too: the file chooser's close button **Cancel file selection (Escape)**, the archive preview's up button **Go up one level**, the clear buttons of Settings searches **Clear search**, and in Customize the default swatch **Default (Theme color)** and the custom color dialog's back button **Back to palette**. Text fields are named after their labels, such as **Archive name**, **Password** and **Confirm password** in Compress and **Server address** in Connect to server, and a 10xer footer prompt's field after the prompt it shows.

An empty, unreadable or still-loading directory has no rows to focus, so the pane itself takes focus. It draws the accent focus ring, is named after the directory, and is described by what it shows ("This directory is empty", the error, or "Loading"). **Tab** and **Shift+Tab** leave it as they leave a listing, and **Shift+Tab** from the footer returns to it. In Columns, an unreadable directory's **Retry** button is the next **Tab** stop inside it. When the entries appear, focus moves back to the keyboard cursor.

**Settings → General → BROWSING → Keep arrows in file list** (off by default) stops arrow keys from leaving the file list. **Tab**, **Ctrl+Shift+B** and the pointer still reach the header, sidebar and top bar. **Ctrl+\\** toggles it live and updates the Settings switch. The file chooser respects the same preference. In 10xer mode the preference is not used, its Settings row reads **Not used in 10xer mode.**, and **Ctrl+\\** does nothing.

**Alt+Left / Alt+Right / Alt+Up** remain Back / Forward / Parent in every mode, and **Alt+Home** goes to your home folder. **Home** or **Ctrl+Up** and **End** or **Ctrl+Down** jump to the first and last item, **Page Up/Page Down** move a page, **Shift+Home** and **Shift+End** extend the selection to either end, and, in the default map, **Ctrl+Space** toggles the focused item's selection. In the default map, Columns keeps Miller-column navigation: **Right enters folders or moves into an existing pane to the right**. In List, Right stays on the current row. On a focused file, Right never opens the file. On a local ZIP, 7z, TAR or TAR.GZ in Columns, **Right**, **Enter** and **Space** enter the archive preview. In List or Columns with a preview open, Right moves focus into that preview; otherwise it does nothing. **Enter** opens other files. Opening a folder with Enter selects its first item; opening it with the pointer selects nothing. In Icons and List, a folder you left recently restores its remembered position instead. With **Type to search** off, **h** / **j** / **k** / **l** act as the arrow keys in every view and in the file chooser. **Backspace** in List and Icons opens the parent folder. In Columns it closes the focused nested column and those after it; from the first column it opens the parent folder with the folder you left selected. **Ctrl+1**, **Ctrl+2** and **Ctrl+3** switch to Columns, Icons and List, even while typing in the filter, keeping the directory, the selection, the focused item and the sort. In [10xer mode](10xer-mode.md), arrows stay in the Columns, List, and Icons panes. **Tab** moves from the file list to the window header, where **Enter** / **Space** activate the focused control and **h** / **j** return to the files. **Ctrl+Shift+B** focuses a visible sidebar; a hidden sidebar stays hidden until **Ctrl+N** or the header toggle shows it. **Ctrl+N** steps the sidebar as **Ctrl+B** does in the default map, and **Ctrl+B** pages up. In the sidebar, **j** / **k** and **Up** / **Down** move between places and device controls, **l** / **Enter** / **Space** activate the focused one, and **h** / **Left** / **Backspace** return to the files without changing the selection. A **Tab** or arrow key from the footer still returns to the file list. List and Columns **l** / **Right** open a directory or enter a file's preview when possible. Icons **h** / **j** / **k** / **l** and arrows always move to the next icon in that direction, including across search-result icons; they never preview or change location. On a file, **i** toggles the preview without moving focus. On a directory it opens the next Miller column without focusing it, or toggles the folder-peek popover in List and Icons.

Columns reserves preview space from startup, even before a file is previewed. **Space**, **i**, and the preview's close button dismiss the content without reclaiming that space, so opening or closing a preview does not move the columns under the pointer. Switch **Appearance → Preview panel** off to explicitly reclaim it. This reservation is window-local and does not enable automatic previews on its own. In Columns the preview fills the space right of the focused column, at least 300 px. When less than 240 px would remain beside the focused column, the preview content hides and media pauses, but the reserved slot keeps the remaining width beside the focused column, down to zero. Dragging the divider sets a width of at least 300 px that lasts until the window closes; in Columns the preview still fills wider free space and yields to columns only down to that width. **F8** focuses the divider, and the arrow keys then move it; moving it with the keyboard sets the same manual width as dragging and draws no outline. See [Previews](../guide/previews.md) for the panel itself.

**Space** on a focused supported file opens quick preview, and a second **Space** closes it; Space on an unsupported file opens nothing, and Space on a selected folder enters it without opening the preview. With the preview open, moving the cursor, or extending the selection with **Shift+arrows**, shows the newly focused file. In List, moving onto a folder or a file with no preview hides the preview; in Icons the panel stays and shows **No preview for this selection**. Moving onto a supported file again shows it. When the preview shows a message with an **Open** button, such as for a password-protected PDF, **Right** from the listing in List or Columns, or **Down** or **Right** from the preview's content, focuses the button, which shows an inset focus ring. There **Enter** opens the file in its default application, **Left** returns focus to the listing, and **Up**, **Down** and **Right** keep focus on the button. In 10xer mode **j** and **l** reach the button and **h** returns. With the caret in preview text, **Ctrl+A**, **Ctrl+C**, **Ctrl+V**, **Ctrl+X**, **Ctrl+D** and **Delete** act on the text, not on files. With a PDF's pages focused, **Ctrl+0** resets the PDF's zoom rather than the text size, in a window and in the file chooser, with 10xer mode on or off.

In Columns, the pane to the right mirrors keyboard selection like Finder: moving with **Up/Down**, **Page Up/Page Down**, **Home/End** or **Ctrl+Up / Ctrl+Down** onto a folder shows its contents in a child column that takes the reserved preview space, onto a previewable file closes that child column and, when **Single-click file previews** is on, opens quick preview in the same space, and onto any other file closes the child pane. The focused column stays where it is throughout. When keyboard movement focuses a column that is clipped at all, even by a few pixels, the strip scrolls until the column is fully visible; a fully visible column stays in place. A column wider than the strip stays put while it fills the strip; otherwise the strip scrolls to its left edge. Mirroring waits 75 ms after the last key, so holding Down loads only the folder where the cursor stops. Shift-extended ranges do not mirror, and neither does a column whose filter has a query typed in it. In a column with no keyboard cursor yet, **Home** or **Ctrl+Up** lands on the first item and **End** or **Ctrl+Down** on the last. A preview closed with **Space**, **i**, **Escape**, the close button, or **Appearance → Preview panel** stays closed while mirroring until it is opened explicitly again. Pointer selection keeps the configured click behavior. Clicking a folder whose column is already open focuses that column rather than closing it, and a double-click ends exactly where a single-click open does; a slow click on a selected folder's name still renames it. In every view, a plain click on an item that is part of a multi-selection collapses the selection to that item and then applies its single-click behavior: a folder set to open on one click opens (in Columns, as its child column), and a previewable file is previewed when **Single-click file previews** is on. Pressing a member and dragging still drags the whole selection. **Settings → General → BROWSING → Mirror columns selection** (on by default) toggles the mirroring. 10xer mode follows the same preference for its cursor in Columns; see [10xer mode](10xer-mode.md). **l** / **Right** enters a directory or a file preview, and **i** toggles a file's preview or opens the next column / toggles folder peek for a directory.

## Closing dialogs and overlays

<!-- node: app/dialogs -->
<!-- node: settings/preferences -->
<!-- node: browser/search -->
<!-- node: browser/search, Search limits -->
<!-- node: browser/sidebar -->
<!-- node: browser/selection/keyboard-navigation, Modal dialogs -->
<!-- node: browser/navigation/folder-jump -->
<!-- node: browser/folder-customization -->
<!-- node: operations/archives -->
<!-- node: app/window -->

Closing an overlay or dialog by any route (Escape, its close or Cancel button, or a
click outside it) returns keyboard focus to the control that opened it. This covers
Ctrl+K search, Ctrl+Shift+K folder jump, Compress, archive conflicts, Customize, and
error dialogs. If that control is gone, for example after the view was rebuilt or an
inline editor closed, focus goes to the file list cursor, or to the pane of an empty or
loading folder. File-operation progress always returns focus to the file list cursor,
because the operation changes the listing. Choosing a search result hands focus to the
browser instead, and a result the browser selects while a dialog closes, such as an
extracted folder, keeps focus.

Closing a dialog over a modal that stays open, such as the action editor over
Settings, returns focus to its opener inside that modal. When that opener is gone,
for example an action row the dialog re-rendered, focus goes to the first focusable
control in the remaining modal. A dialog closed from the keyboard keeps the focus
ring on the control that receives focus, both over a modal that stays open and once
the last modal closes. The exception is a dialog closed from the keyboard that opens
another dialog as it closes: focus lands on the new dialog's default button, which
shows no focus ring.

Closing Settings always returns focus to the file list cursor, even when Settings was
opened with the gear button. The one exception is a filter field or filter result that
had focus when Settings opened, for example with **Ctrl+,**: it gets focus back.

Customize opens with focus on **Done**, so one **Escape** closes it. Closing its
custom color dialog returns focus to the custom color button. In the custom color
dialog, Escape from the color editor returns to the palette, and Escape from the
palette closes the dialog without applying.

Confirmation dialogs open with the confirm button focused, so **Enter** confirms and
**Escape** cancels: Permanently delete, Empty Trash, Restore, paste and archive
Replace, Run, and Forget saved password. The exception is a delete where Trash is
unavailable, which opens with Cancel focused. Outside a text field, an arrow key
moves focus to the nearest button or control in that direction, and **Enter**
activates the focused button, so Enter with Cancel focused cancels. **Enter** also
toggles a focused checkbox or switch, and **Down** on a menu button opens its menu.
In a dialog with tabs, such as the custom action editor, **Up** from the top of a
page focuses the current tab. On the tabs, **Left** and **Right** switch tabs,
**Down** moves into the page, **Up** moves to the control above the tabs, such as the
close button, and **Enter** does not activate the dialog's default button. A tab set
whose tabs are hidden is skipped.
While a popover menu is open, keys go to the menu rather than to browser shortcuts. In the delete
confirmation, **h** also focuses Cancel and **l** the confirm button. **Enter** in a
single-line text or password field of the Compress, archive password or mount
authentication dialog activates the primary button, unless it is disabled; in a
multi-line field it inserts a newline. In Settings, Escape in a non-empty search
field first clears the query. In Customize, Escape with the emoji picker open closes
only the picker. A field with a length limit, such as a drive label, cuts typed or
pasted text to the longest leading part that fits, on a whole character, and its
remaining-characters caption counts in the same unit.

**Connect to server…** in the Network sidebar row's menu opens **Connect to server**
with focus in **Server address**, where **Enter** presses **Connect**. An address that
cannot be opened, or a connection that fails, shows its error under the field and
keeps the dialog open; editing the address clears it. While connecting, the field,
**Pin to sidebar** and **Connect** are disabled, and a sign-in prompt stacks above the
dialog. **Escape**, **Cancel** or the close button closes the dialog and cancels the
connection. A click outside does not close it while it is connecting or the address
is not empty.

Focus cannot leave an open dialog: focus that moves outside it returns to the dialog,
and a key pressed with focus outside it only moves focus back in. While a dialog is
open, browser shortcuts do not act behind it, but **Ctrl++**,
**Ctrl+−** and **Ctrl+0** still change the text size. While a dialog or Settings is
open, **Ctrl+K**, **Ctrl+Shift+K**, **F5**,
**Ctrl+Alt+T** and **Ctrl+\\** do nothing and the dialog keeps focus. **Ctrl+K** and
**Ctrl+Shift+K** still close the search palette they opened. Once a dialog is
animating closed, those five keys act as if no dialog were open; other browser
shortcuts still do nothing until it is gone, and the text-size keys still act.

In **Ctrl+K** search, **Up** and **Down** move the highlight while the caret stays in
the query, and typing edits the query. The first result starts highlighted, so one
**Down** highlights the second. With an input method composing in the query, an
**Enter** that the input method passes back after committing opens the highlighted
result. **Enter** closes search and opens the
highlighted result: a folder opens, and a file is revealed selected in its folder
with quick preview open. With **Settings → General → SEARCH & FILTERING → Open
search results directly** on, the file launches instead. **Alt+Enter** opens its
containing folder with the result selected and focused.
When indexing stops early, the footer shows **Partial results**; hovering it lists
the causes, and when **Search time limit** or **Search entry limit** stopped it, the
text ends **Raise the limits in Settings → General → Search & filtering.** Search
reads the limits each time it opens.

**Ctrl+Shift+K** opens **Jump to a folder…**, which lists the local folders you have
opened in Strata, most frequently and recently visited first, up to 100. Each
space-separated term may match anywhere in a folder's path, so `dev str` finds
`~/dev/strata`, and terms accept the `'exact`, `^prefix`, `suffix$` and `!excluded`
forms; `strata !notes` hides folders whose path matches `notes`. Folders whose names
match more terms rank higher, and an exact name ranks first among them. Arrow keys choose a folder and **Enter** opens it.
Before any folder is recorded it shows **No folder history yet**, and a query that
matches nothing shows **No matching folders**. In 10xer mode **Ctrl+Shift+K** does
nothing; **z** and **Z** jump to visited folders instead (see
[10xer mode](10xer-mode.md#prompts)).

## Opening and navigating the context menu

<!-- node: browser/context-menu -->
<!-- node: browser/context-menu, Placement -->
<!-- node: browser/context-menu, Pointer activation -->
<!-- node: browser/properties -->

**Menu** (the hardware context-menu key) and **Shift+F10** open the selection-aware
context menu without the pointer. With the keyboard cursor on a selected item, the
menu opens for that item, or for the whole multi-selection if the item is part of
one. With the cursor on an unselected item, or with nothing selected, it opens the
pane's background menu. The menu is anchored to the focused item or pane, never to
the pointer, and like a pointer-opened menu it may extend past the window. On a focused Ctrl+F result it opens that result's file menu. With a
text field focused, Menu and Shift+F10 open the field's text-editing menu instead.
With a sidebar place, Trash or drive row focused, they open that row's menu, with
10xer mode on or off. **Ctrl+Shift+F10**, **Shift+Menu** and **Ctrl+Menu** open no
menu. **Alt+Enter** with one item selected opens Properties for the focused item.
A keyboard-opened item menu is anchored to the item's right edge in Columns and
Icons, and to its center in List. In Properties, **Copy path** copies a file's
shell-escaped path with no trailing `/`, and a folder's with one.

A right-clicked menu opens at the click, anywhere in a long scrolled list. It opens
below the click and flips above it when the screen has no room below; with no room
either way it shrinks and scrolls, and near the screen's left or right edge it slides
sideways. Menus may extend past the window but stay on screen, and a menu taller than
the monitor scrolls. A button release that reaches a menu before any press inside it
is ignored, so pressing the secondary button, moving onto a row and releasing runs
nothing; click the row to run it.

Each action with a shortcut shows it at the right of its row, such as **Ctrl+C**
beside Copy, **Enter** beside Open, **F2 / Ctrl+R** beside Rename and **Alt+Enter**
beside Properties, with key names in the interface language: German shows **Strg+C**
beside Copy and **Entf** beside Move to Trash. Outside Trash, when every selected item
is on a network or cloud location, Permanently delete reads **Delete without Trash**,
with the **Shift+Delete** hint.

Right-clicking an item also makes it the keyboard cursor, without opening it.
An already-selected item keeps the existing multi-selection; an unselected item
becomes the only selected item. Escape returns keyboard focus to that clicked item.

A menu opens with keyboard focus on its first visible action, and focus stays there
while Open With entries load, even with the pointer resting over the menu. **Ctrl+A**
leaves an open menu open. Once open: **Up/Down** move between enabled actions, wrapping past the first/last;
**Home/End** jump to the first/last enabled action; separators and disabled actions
are skipped. **Enter/Space** activates the focused action immediately on key press. On a
submenu row such as **Actions** or **Send to…**, **Right**, **Space** or **Enter**
opens the submenu with its first action focused, and **Left** closes only the
submenu and refocuses its row. In the file chooser's menus, **Tab** and
**Shift+Tab** also move between enabled actions.
**Escape** closes the menu without changing the selection and returns keyboard
focus to the item or pane that opened it. This applies in Columns, Icons, List,
Trash, and the file chooser. Closing Properties follows the
[overlay rule](#closing-dialogs-and-overlays); choosing Rename hands focus to the
editor instead.
