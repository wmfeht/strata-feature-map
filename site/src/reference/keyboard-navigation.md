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
reviewed_at: 0a086aa3bdb251842a1e8413e2a6b35970d0b409
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

Shortcuts on this page work on any keyboard layout, with the exceptions below.
Letters follow the key's label, or the Latin letter the key carries on Russian and
other non-Latin layouts, so **Ctrl+C** is the key that types **с** in Russian. On
plain Chinese (`cn`), every shortcut is the US one. Digits count by their position
on the top row, so **Ctrl+1** works on AZERTY without Shift. A digit typed off the
top row also counts, such as the Hungarian 0 left of 1. Caps Lock never changes a
shortcut.

The exceptions: where a top-row key types **+** or **−**, Ctrl with that key acts as
**Ctrl++** or **Ctrl+−**, not as the digit. Swiss German types + with Shift+1, so
there **Ctrl+Shift+1** selects no tab. With AltGr held, a top-row key counts only as
a digit it actually types, so AZERTY **Ctrl+AltGr+1** is not **Ctrl+1**.
**Ctrl+\\** also works on German, Swiss, Swedish and Norwegian Mac layouts, where
AltGr types `\` on the top row. After **t** or **;** in 10xer mode, a top-row key
counts by its position even where it types + or −, so on AZERTY **t**, then the −
key selects tab 6.

Letter, digit and symbol shortcuts match Ctrl, Alt, Shift and Super exactly, so
**Ctrl+Alt+C** does not copy. Chord digit steps, such as **t**, then **1** in 10xer
mode, and the media **0** key also accept Shift. Some navigation and dismiss keys
accept extra modifiers: in the file list, **Delete** and **Shift+Delete** still act
with Ctrl, Alt or Super held, and **Escape** closes a dialog whatever else is
held. Hyper and Meta are ignored. A symbol shortcut ignores the Shift
your layout needs to type the symbol. Keypad Enter, arrows, Home, End, Page Up,
Page Down, Insert, Delete, Tab, Space, +, −, \*, / and = act as the main keys;
keypad digits count only with Num Lock on.

Typing is never remapped: type-to-search, the filter, rename fields and footer
prompts receive the characters your layout types, such as Cyrillic. While a text
field shows an unfinished input-method or dead-key composition, keys go to the
composition before any Strata command. A Korean input method such as fcitx5-hangul
commits the syllable on **Escape** and passes the key back, so one press commits the
syllable and cancels a rename. Type-to-search started from the file list does not
use your input method: a pinyin letter arrives as the Latin letter, and a dead key
starts nothing. To search with an input method, open the filter with **Ctrl+F**
(**f** in 10xer mode) and type there.

Every shortcut Strata shows is one that works. Shown shortcuts in F1, menus and
tooltips stay in Latin letters when you switch layouts. Modifiers appear in the
order Ctrl, Alt, Shift, Super, and a letter after a modifier is uppercase, as in
**Ctrl+Shift+N**. Without a modifier, a letter appears as typed (**j**) and Shift
with a letter as the uppercase letter (**J**). Chord steps are separated by a space
(**g h**). Minus is written −, and arrows ↑ ↓ ← →. Key names follow the interface
language, such as **Strg+C**, **Entf** and **Bild auf** for Page Up in German, or
**Suppr** for Delete in French; with the interface in Simplified Chinese they stay
as printed, such as **Ctrl+C**.

## Browser tabs

<!-- node: browser/tabs -->
<!-- node: browser/tabs/session-restore -->
<!-- node: integration/open-with/terminal -->
<!-- node: integration/10xer-mode -->

In regular and 10xer modes, **Ctrl+T** opens a tab at the active location,
**Ctrl+W** closes the active tab, and **Ctrl+Tab / Ctrl+Shift+Tab** cycles tabs.
**Ctrl+Page Up / Ctrl+Page Down** selects the previous / next tab in strip order,
wrapping at either end, like the tab shortcuts in web browsers.
**Ctrl+Shift+Page Up / Ctrl+Shift+Page Down** moves the active tab one position
left / right without switching tabs. Reordering stops at either end of the strip.
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
In a text field, these keys go to the field. On a file, both
open it with its default application, like **Enter**. With the pointer,
middle-click a folder in Columns, Icons or List to open it in a new tab, or
**Ctrl**+middle-click or **Shift**+middle-click to open it in a new window;
middle-clicking a file only selects it. **Open in… → New Tab** or **New Window** in
a folder's menu does the same. Selecting a tab returns focus
to the control that last had it in that tab, or to its file view's cursor when that
control is gone.

Each tab retains its location, selection, navigation history, preview and search
state. Tab locations persist across restarts: a plain launch (no folder
argument, reveal request, or unlock target) reopens the previous tabs in order
with the previously active tab selected, when **Settings → General → Startup →
Restore open tabs** is on (the default). The session is saved in
`$XDG_CONFIG_HOME/strata/tabs.toml`, which turning **Restore open tabs** off
deletes. Missing directories, credential-bearing
URIs, and transient locations such as trashed-item children, non-root Recent
entries, and camera roots are skipped; with nothing restorable the window opens
at the default directory as before. Up to 32 tabs are restored. When the saved
active tab is skipped, the nearest restored tab to its left is selected. Windows opened for an explicit folder,
reveal request, or unlock target never overwrite the saved session; with
several plain-launch windows open the most recently changed one wins. Selection, history, and preview state stay
in-memory. Appearance preferences and the clipboard remain
shared. File operations prevent closing their tab or window until they finish
or are cancelled.

Tab names follow the active directory, not a child column shown only as a keyboard
preview: `~` for your home folder, `/` for the root, and names longer than 22
characters are cut short with an ellipsis. A pending single-click folder activation keeps the previous tab name until
navigation resolves; cancelled clicks and drags restore normal focus-based naming.

The Material-style strip appears when there is more than one tab. The plus and
window-close controls move into it and return to the normal header when only
one tab remains. Scroll the strip horizontally (or use the wheel) when it
outgrows the window; selecting a tab brings it into view without a scrollbar.
Drag a tab label to reorder tabs. Drop files on a tab to transfer into its
current directory, or hover there during a file drag to switch tabs and choose
a folder in its listing. Existing copy/move modifiers and conflict handling apply.

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

The terminal shortcut, **Ctrl+Alt+T**, opens in the selected folder whenever exactly one folder is selected, including a folder selected for you on arrival. After **Alt+Up** from `~/Projects/foo`, **Ctrl+V** pastes into `~/Projects`, but **Ctrl+Alt+T** opens in `~/Projects/foo`. Otherwise it uses the same destination column as paste. New Folder remains keyboard-focus scoped. Context-menu paste and drag-and-drop retain their explicit destinations.

Keyboard navigation suppresses stale row-hover effects and pending folder peeks until deliberate pointer input resumes. It does not erase selection or the open folder path.

## Focus without selection changes

<!-- node: browser/selection -->
<!-- node: browser/selection/keyboard-navigation -->
<!-- node: operations/clipboard -->
<!-- node: operations/delete -->
<!-- node: operations/trash -->

Pressing blank column content focuses that directory, including an empty one. A plain press there clears file selections in every column immediately and closes the columns to its right; releasing it does not clear them again. When returning to an inactive column, it also selects that column's first visible entry as the range anchor. Ctrl/Shift presses keep the selection until marquee intent is resolved, so a drag can extend it. A plain click on blank space or a disabled control in a preview that is showing something leaves the selection alone; the empty reserved preview slot clears like other empty space. Row clicks, controls, scrollbars, context menus, and marquee selection keep their own interactions. Returning to a column by keyboard preserves a multi-selection; Ctrl+A selects the focused column, not the deepest open column.

**Ctrl+click** toggles one item in or out of the selection and makes it the range anchor; **Shift+click** selects every item from the anchor to the clicked item. After a navigation selects the first item, the first Shift+click ranges from that item. Any click re-anchors **Shift+Up/Down**, so keyboard extension continues from the clicked item. A Ctrl+click or Shift+click on an item's name or icon moves the keyboard cursor to that item, so the preview follows it.

**Shift+Up/Down** extends the selection from the range anchor by one item, **Shift+Page Up/Page Down** by one page; the file chooser leaves Shift+Page Up/Page Down to GTK. **Shift+Down** with nothing selected selects only the first item; the next selects two. After Escape clears the selection, the range starts at the cursor. With hidden files off, **Ctrl+A** in Icons, List and the file chooser leaves hidden items unselected.

**Escape** closes one thing at a time. An open menu, Properties, a rename or new-item editor, the location editor, a filter, or quick preview closes first. With none of those open, Escape clears the active pane's selection and keeps the keyboard cursor and the directory, so **Enter** then opens the folder under the cursor. In Columns, Escape clears only the active column; parent selections and open columns stay. Outside 10xer mode, Escape with nothing selected in the active column closes the deepest column.

Copy/cut use the selection in the focused column, never a hovered row. In Columns, **Ctrl+C** or **Ctrl+X** with nothing selected in the focused column acts on the folder that column shows. **Delete** moves the selection to Trash without asking; **Shift+Delete** opens the permanent-deletion confirmation. In Trash, Delete also asks to delete permanently. Items inside a trashed folder cannot be deleted from the keyboard. With a Ctrl+F result selected, Delete moves that result to Trash and leaves the hidden directory selection alone. While the filter input or a text field, such as preview text, has focus, Delete and Shift+Delete never delete files. In Columns, Delete or Shift+Delete with nothing selected acts on the focused column's keyboard cursor row. When that column has neither a selection nor a cursor, such as an empty open folder, it acts on the open folder itself. In List and Icons, Delete acts on the selection only. Delete in a location without Trash support, or after a Trash attempt fails because Trash is unsupported, opens the permanent-deletion confirmation with Cancel focused and the reason stated; Shift+Delete is unchanged.

Background selection updates from directory loading must not move keyboard focus to an inactive column.

When the focused item is deleted, in Strata or by another program, focus moves to the next visible item, or to the previous one when none follows, and the preview follows it. Deleting the last visible item clears focus and selection. Other background changes to an open directory keep the selection and scroll position and never take focus.

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
<!-- node: browser/selection -->

**F5** reloads every open column in Columns, and the active pane in Icons and List.
Each pane header's Refresh button (tooltip **Refresh (F5)**) reloads only that pane.
With an Auto-refresh interval set, each tick runs the same reload as F5.

F5, the pane's Refresh button, Auto-refresh, and the rescan after a burst of
external changes keep the selection, the keyboard cursor and the keyboard focus in
every view: a focused row stays focused, and a focused Ctrl+F field keeps focus and
its text. Icons and List also keep the scroll position. When the item under the
cursor is gone, the cursor moves, without selecting anything, to the next visible
item at its old position, or to the previous visible item when none follows. In
Columns, this does not happen in a column whose child column is open: no other item
takes the cursor there.

A refresh never takes focus from the sidebar, the location entry or a dialog. During
a slow reload, typing in the Ctrl+F field does not stop focus returning there; **Tab**
or pointer input does, and **Escape** that closes the filter sends focus to the
listing instead.

## Creating files and folders

<!-- node: operations/create -->
<!-- node: operations/rename -->
<!-- node: browser/selection/keyboard-navigation -->

In Columns, List, and Icons, **Ctrl+Shift+N** or background menu → **New Folder**
immediately creates `new folder`. Background menu → **New File** immediately
creates an empty `new file`. If the default name is occupied by any item, creation
tries `new folder (1)` / `new file (1)`, then `(2)`, and so on without overwriting
anything. The pane filter is cleared and the entire allocated default name is
selected: one Backspace clears it, and typing replaces it.

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
pane space), or moving keyboard focus away commits a valid name. **Tab** also leaves
the listing, or the strip in Columns. Escape keeps
the original name. Finishing with an empty or invalid name also keeps the
original. Cancelling the initial rename does **not** delete the new item: it
remains under its allocated default name. File contents are preserved.
While a name is being edited, **F5**, **Ctrl+K**, **Ctrl+Shift+K**, **Ctrl+Alt+T**
and **Ctrl+\\** do nothing; finish or cancel the edit first.

Clicking inside the field continues editing. Existing files retain extension-aware
selection (the stem is selected); folder names containing dots are selected in full.

Names containing `/` or NUL, `.`/`..`, and whitespace-only names (including
Unicode whitespace) are invalid. Valid names are used exactly as typed,
including spaces around a nonblank name, hidden-file prefixes, and Unicode.
Name conflicts, filesystem-specific limits, and permission errors retain the
original item and report an error. After a rename onto an existing name, Escape on
that error returns focus to the item's row.

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
and queries containing punctuation remain literal. Indexed results rank literal
matches ahead of typo matches; parent paths do not qualify a result.

Add `*` for a whole-filename pattern without typo tolerance:

- `*.MOV` matches `clip.MOV`, but not `clip.MOV.bak`.
- `IMG*` matches names beginning with `IMG`.
- `IMG*.MOV` combines a prefix and an extension.
- `*holiday*` matches names containing `holiday`; `*` matches any name.

Each `*` stands for zero or more characters. Other punctuation (including `?`,
`[]`, and regex syntax) is literal. Patterns match file and folder names, not
parent paths, in Columns, Icons, List, and the file chooser. Hidden-file visibility
and [Include subfolders](../guide/search.md) still control the scope;
a wildcard does not enable recursive search. Existing result limits still apply.
Clear the input, or press Escape in the input or on a focused result, to restore
the directory listing with focus on its cursor. **Ctrl+K** global fuzzy search is
unchanged.

Results follow the watched folders live: the open folder, and in Columns every open
column. A matching file that another program creates or renames there appears within
about a second, and a deleted one leaves the results as soon as the listing drops it.
With [Include subfolders](../guide/search.md) on, changes in folders below
those reach the results on **F5**, Auto-refresh, the rescan after a burst of external
changes, or when the filter is cleared and opened again.
When another program renames the open folder itself, the view follows it and a filter
typed in that folder ends, while filters and **Ctrl+K** searches rooted above it follow
the rename. When the open folder is deleted or moved into another folder, the view
returns to its nearest parent that still exists, or reloads the folder if it already
exists again; either way the filter ends. Neither adds a history entry.

## Preview while filtering

<!-- node: browser/search/filter -->
<!-- node: preview/quick-preview -->

In the browser and file chooser, **Down** from the Ctrl+F input focuses the selected result, or the first result if none is selected. **Up/Down** then navigate the results; **Up** from the first result returns to the input without clearing the query. **Ctrl+F** also returns to the input. With no matches, Down leaves focus in the input. **Enter** on a focused result opens it, whatever the click-count and preview preferences. **Shift+arrows** and **Ctrl+A** select results. In List and Icons, **Tab** from a focused result leaves the results in one press, and **Shift+Tab** then returns to the result that held the cursor. In Columns, moving focus out of the filtered column closes its filter, while focus in its own results, a popover or a dialog keeps it; opening a filter in one column closes and clears any other column's filter.

**Menu/Shift+F10** on a focused result opens its file menu. While the input itself is focused, its text-editing menu remains available. **Space** toggles quick preview for a selected file result in Columns, Icons, and List, including after returning to the query. Previewing a file keeps the query, selection, and current directory intact; on a selected folder result, Space navigates into the folder instead.

While the input is focused, Space types into the query if no result is selected. **Shift+Space** inserts a space there even with a result selected. Space opens a selected folder in every view without opening or loading the preview pane; unsupported files do not open a preview.

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

Other archive previews start at the archive root with the first member
highlighted. In List and Columns modes, arrow keys act on the focused pane,
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
**Ctrl+Alt+Space** plays or pauses, **Ctrl+Alt+Left/Right** seek 5 s,
**Ctrl+Alt+Up/Down** change the volume by 0.1, **Ctrl+Alt+M** mutes, and
**Ctrl+Alt+<** / **Ctrl+Alt+>** step to the previous or next file of the open
preview's kind: from a video to the adjacent video, skipping audio files, and from
an audio file to the adjacent audio file, skipping videos. In 10xer mode, **<** and
**>** do the same.

Audio and video previews show a timeline; **Tab** or a click focuses it. While
it has focus, **Left/Right** seek 5 s, and **Shift+Left/Right** or **Page
Down/Page Up** seek 30 s. **Home** or **0** returns to the start; **End** or
**G** jumps to the last frame, since seeking to the very end would stop
playback. **+** / **=** and **−**, including the keypad's, change the volume by
0.1; reaching zero mutes and keeps the volume to restore. Unlike **Left/Right**,
the paging, jump and volume keys have no **Ctrl+Alt** form. The volume slider
steps 0.1 with the arrow keys and 0.2 with Page Up/Down; **Home** mutes and
**End** sets full volume. Other playable files show a seek slider instead of a
timeline: the arrow keys step 5 s, Page Up/Down 30 s, and Home/End jump to the
start and the last frame. Keys and the mouse wheel seek at once; a drag seeks
when released. In
[10xer mode](10xer-mode.md#preview-keyboard-ownership), the same keys, plus
**Up/Down** for volume, work whenever the media preview owns the keys.

## Shortcut footer

<!-- node: app/shortcut-reference -->
<!-- node: settings/preferences -->
<!-- node: integration/10xer-mode -->

Every mode has a compact footer with an **F1 Shortcuts** button on the left and clipboard status and the item count on the right. The button toggles the reference and shows as pressed while it is open. **Settings → General → Browsing → Show F1 Shortcuts button** controls the button's visibility (on by default). The preference is saved and updates all open windows immediately. Item counts and clipboard status remain visible when the button is hidden. With the button hidden and no other footer status to show, such as a count, the clipboard badge, or the **10X** tag in 10xer mode, the whole footer hides. F1 opens the **Keyboard shortcuts** panel centered over the dimmed, blurred window; focus cannot leave it until it closes. F1 always opens the complete, mode-specific reference; closing it restores the button's configured visibility. F1, Escape, or a click outside it closes the reference, which blocks file-operation shortcuts while open. It stays open when the window loses focus. The reference is the only complete in-app keybinding list; it shows only the currently active map and live-updates when 10xer mode changes. In 10xer mode, a pending chord's footer panel also lists the keys that can follow it.

The reference opens with focus in **Search actions or keys…**, scrolled to the top. Typing keeps the rows whose keys, key context or action contain the text, ignoring case. Translated text matches, and key names match in English and in the interface language: under German, `strg+c` and `ctrl+c` both find Copy. A query with no match shows **No matching shortcuts**. The category list shows **All** and each section with its row count; choosing one shows only that section. In windows narrower than 1480 px, the header stacks, categories become wrapping pills without counts, and results use one column. In the default map the sections are the current view's navigation (Columns, Icons or List), then Files and selection, Search and tools, and Preview media. In 10xer mode the reference adds Places, Preview and a 10xer mode section for keys the default map lacks. Reopening the reference keeps the previous search text and category. In the search field, typing, **Delete**, **Ctrl+A**, **Ctrl+C**, **Ctrl+V** and **Ctrl+X** edit the query, and **Up**, **Down**, **Page Up** and **Page Down** scroll the results without moving focus, **Ctrl+Z** undoes the last query edit, and **Ctrl+Y** or **Ctrl+Shift+Z** redoes it. **Tab** and **Shift+Tab** cycle the search field, the selected category and the results. **Ctrl+B** jumps to the categories, **Ctrl+F** to the search field and **Ctrl+L** to the results. In the categories, arrows or **h**/**j**/**k**/**l** select the previous or next category, and Home and End the first or last. In the results, arrows, **j**/**k**, Page Up/Page Down and Home/End scroll the list. A line at the bottom summarizes these keys: Ctrl+B categories · Ctrl+F search · Ctrl+L list · j / k / ↑ / ↓ move · Tab cycle · Escape close. In 10xer mode `~` also toggles the reference; in the default map it does not. F1 with Ctrl, Alt, Shift or Super held does not toggle the reference, and while it is open **Ctrl+1**, **Ctrl+2** and **Ctrl+3** do nothing. Closing it returns focus to the control that had it before.

## 10xer mode

<!-- node: integration/10xer-mode -->
<!-- node: integration/10xer-mode/search -->
<!-- node: integration/10xer-mode/file-chooser -->
<!-- node: app/shortcut-reference -->
<!-- node: browser/context-menu -->
<!-- node: operations/clipboard -->

**Settings → General → Browsing → 10xer mode** (off by default,
toggle with **Ctrl+Shift+M**) hides window Search and
pane Close/filter/refresh/sort chrome and installs Yazi-style keys.
**Ctrl+Shift+M** is the only key that leaves the mode. While the mode is on, the footer shows
**10X** in its far right corner, after the item count.
Typed input uses the footer prompt, never the pane filter revealer or the
global search dialog. See [10xer mode](10xer-mode.md) for the keymap.

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

With no selection in the ordinary listing, the footer shows the directory's item count. Selections show a folder/file breakdown, such as **1 folder, 2 files selected (64 MB)**. Selecting every item shows the breakdown without a size, and selecting more than 64 items, but not all, shows **N items selected** without a size. Sizes sum available metadata for selected files only; folder contents are not scanned or included. Missing file sizes are marked incomplete or unavailable.

After copying or cutting files, a highlighted **Files on clipboard** pill appears to the left of the item count. It reflects the file clipboard, including compatible copies from other applications, rather than assuming every clipboard contains files. It stays available after copying/pasting, and disappears when a completed cut consumes the clipboard or it is cleared/replaced with text. The clipboard status and paste shortcut remain available when the F1 Shortcuts button is hidden. Copied listing items show the Lucide copy icon in place of their thumbnail; cut items keep scissors, which wins if both would apply. Clearing the clipboard or unyank removes the copy overlay.

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

In Icons and List, plain arrows move interface focus rather than changing directories:

| Key | Icons | List |
| --- | --- | --- |
| Left | Move one tile left; at the left edge, focus the visible sidebar | Focus the visible sidebar |
| Right | Move one tile right | Stay in the file list; on a file, enter an open preview |
| Up / Down | Move by visual rows | Move through file rows |
| Enter | Open the current item | Open the current item |

Enter on a previewed video, from the listing or inside the preview, pauses the
preview and asks the default player to start where it stopped. mpv, VLC,
Celluloid and MPlayer take the position on their command line; other players
open the file from the beginning, as does a position inside the first or last
second.

Up from the first Icons row or first List item focuses the navigation header, including in empty directories, where the pane itself holds focus. Left/Right traverse its enabled controls without triggering navigation; Enter/Space activates a control. Down returns to the item you left without changing selection. Left from the header's first control can reach the visible sidebar.

In Columns, Up from a column's first item focuses that column's header controls, and Down returns to its list. Left from a column's first header control, or Right from its last, moves into the neighboring column's header. Left in the first column focuses the visible sidebar on the row for the current place.

From the sidebar, Right returns to the item you left (or the current file view if navigation replaced it, or if you entered the sidebar from the header rather than from a file). Up/Down move between places. Up from the first sidebar row (Home by default) continues into the **top navigation bar** instead of stopping. Left/Right traverse its enabled controls without activating them; Down returns to the sidebar row you left. If the sidebar is hidden from the top bar, Down returns to the files instead. Empty file views also support these round trips. If the sidebar is hidden, Left in the file view does not change directories.

In the default map, **Ctrl+B** shows or hides the sidebar. **Ctrl+Shift+B** shows a hidden sidebar and focuses the row for the current place; pressing it again in the sidebar returns focus to where it was. Outside 10xer mode, **Enter** on a sidebar row opens the place with its first item selected; a click opens it with nothing selected. In Icons and List, a folder you left recently restores its remembered position instead.

In the default map each file listing is one **Tab** stop; arrows move inside it. **Tab** from the listing goes to the next interface control (the open preview's controls, then **F1 Shortcuts**), and **Shift+Tab** goes back through the List sort headings, an open filter and the pane header actions, then the sidebar. **Tab** or **Shift+Tab** into a listing lands on the keyboard cursor, so **Enter**, **Space** and **Ctrl+C** act on the item that shows focus. In Columns the whole strip is one stop: **Tab** into it lands on the active column's cursor without changing the active column, **Tab** from any column leaves the strip, and **Shift+Tab** reaches the active column's open filter, then its header actions, then the control before the strip.

Screen readers announce each item by its name, described as Folder, File, Folder link, File link, Broken link or Other. Each pane is a group named after its directory and described as Columns view, Icons view or List view, and the item list inside it is named after the directory and described as Files. Pressing **Tab** repeatedly from the window's first control reaches the listing. Menu items are named after their action and carry their shortcut in their description, not their name. Selecting an item sets the selected state on that item and on no other. With default preferences, the header buttons are named **Search (Ctrl+K)**, **Appearance**, **Settings**, **Close window** and **Toggle sidebar (Ctrl+B)**. Modal dialogs have the dialog role and are named after their title. Item kind, view and list descriptions are in the interface language, and shortcuts in accessible names and descriptions use its key names, such as Strg in German. An icon-only button shows a tooltip, such as **Search (Ctrl+K)**; labelled buttons, menu items, file rows and breadcrumbs show none. A sidebar place's or breadcrumb's full path is its accessible description, not a tooltip.

An empty, unreadable or still-loading directory has no rows to focus, so the pane itself takes focus. It draws the accent focus ring, is named after the directory, and is described by what it shows ("This directory is empty", the error, or "Loading"). **Tab** and **Shift+Tab** leave it as they leave a listing, and **Shift+Tab** from the footer returns to it. In Columns, an unreadable directory's **Retry** button is the next **Tab** stop inside it. When the entries appear, focus moves back to the keyboard cursor.

**Settings → General → Browsing → Keep arrows in file list** (off by default) stops arrow keys from leaving the file list. **Tab**, **Ctrl+Shift+B** and the pointer still reach the header, sidebar and top bar. **Ctrl+\\** toggles it live and updates the Settings switch. The file chooser respects the same preference.

**Alt+Left / Alt+Right / Alt+Up** remain Back / Forward / Parent in every mode, and **Alt+Home** goes to your home folder. **Home** or **Ctrl+Up** and **End** or **Ctrl+Down** jump to the first and last item, **Page Up/Page Down** move a page, **Shift+Home** and **Shift+End** extend the selection to either end, and, in the default map, **Ctrl+Space** toggles the focused item's selection. In the default map, Columns keeps Miller-column navigation: **Right enters folders or moves into an existing pane to the right**. In List, Right stays on the current row. On a focused file, Right never opens the file. On a local ZIP, 7z, TAR or TAR.GZ in Columns, **Right**, **Enter** and **Space** enter the archive preview. In List or Columns with a preview open, Right moves focus into that preview; otherwise it does nothing. **Enter** opens other files. Opening a folder with Enter selects its first item; opening it with the pointer selects nothing. In Icons and List, a folder you left recently restores its remembered position instead. With **Type to search** off, **h** / **j** / **k** / **l** act as the arrow keys in every view and in the file chooser. **Backspace** in List and Icons opens the parent folder. In Columns it closes the focused nested column and those after it; from the first column it opens the parent folder with the folder you left selected. **Ctrl+1**, **Ctrl+2** and **Ctrl+3** switch to Columns, Icons and List, even while typing in the filter, keeping the directory, the selection, the focused item and the sort. In [10xer mode](10xer-mode.md), arrows stay in the Columns, List, and Icons panes. **Tab** moves from the file list to the window header, where **Enter** / **Space** activate the focused control and **h** / **j** return to the files. **Ctrl+Shift+B** focuses a visible sidebar; a hidden sidebar stays hidden until **Ctrl+N** or the header toggle shows it. In the sidebar, **j** / **k** and **Up** / **Down** move between places and device controls, **l** / **Enter** / **Space** activate the focused one, and **h** / **Left** / **Backspace** return to the files without changing the selection. A **Tab** or arrow key from the footer still returns to the file list. List and Columns **l** / **→** open a directory or enter a file's preview when possible. Icons **h** / **j** / **k** / **l** and arrows always move to the next icon in that direction, including across search-result icons; they never preview or change location. On a file, **i** toggles the preview without moving focus. On a directory it opens the next Miller column without focusing it, or toggles the folder-peek popover in List and Icons.

Columns reserves preview space from startup, even before a file is previewed. **Space**, **i**, and the preview's close button dismiss the content without reclaiming that space, so opening or closing a preview does not move the columns under the pointer. Switch **Appearance → Preview panel** off to explicitly reclaim it. This reservation is window-local and does not enable automatic previews on its own. In Columns the preview fills the space right of the focused column, at least 300 px. When less than 240 px would remain beside the focused column, the preview content hides and media pauses, but the reserved slot keeps the remaining width beside the focused column, down to zero. Dragging the divider sets a width of at least 300 px that lasts until the window closes; in Columns the preview still fills wider free space and yields to columns only down to that width. **F8** focuses the divider, and the arrow keys then move it; moving it with the keyboard draws no outline. See [Previews](../guide/previews.md) for the panel itself.

**Space** on a focused supported file opens quick preview, and a second **Space** closes it; Space on an unsupported file opens nothing, and Space on a selected folder enters it without opening the preview. With the preview open, moving the cursor, or extending the selection with **Shift+arrows**, shows the newly focused file. In List, moving onto a folder or a file with no preview hides the preview; in Icons the panel stays and shows **No preview for this selection**. Moving onto a supported file again shows it. With the caret in preview text, **Ctrl+A**, **Ctrl+C**, **Ctrl+V**, **Ctrl+X**, **Ctrl+D** and **Delete** act on the text, not on files.

In Columns, the pane to the right mirrors keyboard selection like Finder: moving with **Up/Down**, **Page Up/Page Down**, **Home/End** or **Ctrl+Up/Ctrl+Down** onto a folder shows its contents in a child column that takes the reserved preview space, onto a previewable file closes that child column and, when **Single-click file previews** is on, opens quick preview in the same space, and onto any other file closes the child pane. The focused column stays where it is throughout. Mirroring waits 75 ms after the last key, so holding Down loads only the folder where the cursor stops. Shift-extended ranges do not mirror, and neither does a column whose filter has a query typed in it. In a column with no keyboard cursor yet, **Home** or **Ctrl+Up** lands on the first item and **End** or **Ctrl+Down** on the last. A preview closed with **Space**, **i**, **Escape**, the close button, or **Appearance → Preview panel** stays closed while mirroring until it is opened explicitly again. Pointer selection keeps the configured click behavior. Clicking a folder whose column is already open focuses that column rather than closing it, and a double-click ends exactly where a single-click open does; a slow click on a selected folder's name still renames it. In every view, a plain click on an item that is part of a multi-selection collapses the selection to that item and then applies its single-click behavior: a folder set to open on one click opens (in Columns, as its child column), and a previewable file is previewed when **Single-click file previews** is on. Pressing a member and dragging still drags the whole selection. **Settings → General → Browsing → Mirror columns selection** (on by default) toggles the mirroring. 10xer mode follows the same preference for its cursor in Columns; see [10xer mode](10xer-mode.md). **l** / **→** enters a directory or a file preview, and **i** toggles a file's preview or opens the next column / toggles folder peek for a directory.

## Closing dialogs and overlays

<!-- node: app/dialogs -->
<!-- node: settings/preferences -->
<!-- node: browser/search -->
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
While a popover menu is open, keys go to the menu rather than to browser shortcuts. In the delete
confirmation, **h** also focuses Cancel and **l** the confirm button. **Enter** in a
single-line text or password field of the Compress, archive password or mount
authentication dialog activates the primary button, unless it is disabled; in a
multi-line field it inserts a newline. In Settings, Escape in a non-empty search
field first clears the query. In Customize, Escape with the emoji picker open closes
only the picker.

Focus cannot leave an open dialog: focus that moves outside it returns to the dialog,
and a key pressed with focus outside it only moves focus back in. While a dialog is
open, browser shortcuts do not act behind it, but **Ctrl++**,
**Ctrl+−** and **Ctrl+0** still change the text size. While a dialog or Settings is
open, **Ctrl+K**, **Ctrl+Shift+K**, **F5**,
**Ctrl+Alt+T** and **Ctrl+\\** do nothing and the dialog keeps focus. **Ctrl+K** and
**Ctrl+Shift+K** still close the search palette they opened. Once a dialog is
animating closed, those five keys act as if no dialog were open.

In **Ctrl+K** search, **Up** and **Down** move the highlight while the caret stays in
the query, and typing edits the query. **Enter** closes search and opens the
highlighted result: a folder opens, and a file is revealed selected in its folder
with quick preview open. With **Settings → General → Search & filtering → Open
search results directly** on, the file launches instead. **Alt+Enter** opens its
containing folder with the result selected and focused.

**Ctrl+Shift+K** opens **Jump to a folder…**, which lists the local folders you have
opened in Strata, most frequently and recently visited first, up to 100. Each
space-separated term may match anywhere in a folder's path, so `dev str` finds
`~/dev/strata`, and terms accept the `'exact`, `^prefix`, `suffix$` and `!excluded`
forms. An exact name ranks first. Arrow keys choose a folder and **Enter** opens it.
Before any folder is recorded it shows **No folder history yet**, and a query that
matches nothing shows **No matching folders**.

## Opening and navigating the context menu

<!-- node: browser/context-menu -->
<!-- node: browser/properties -->

**Menu** (the hardware context-menu key) and **Shift+F10** open the selection-aware
context menu without the pointer. With the keyboard cursor on a selected item, the
menu opens for that item, or for the whole multi-selection if the item is part of
one. With the cursor on an unselected item, or with nothing selected, it opens the
pane's background menu. The menu is anchored to the focused item or pane, never to
the pointer. On a focused Ctrl+F result it opens that result's file menu. With a
text field focused, Menu and Shift+F10 open the field's text-editing menu instead.
With a sidebar place, Trash or drive row focused, they open that row's menu, with
10xer mode on or off. **Ctrl+Shift+F10**, **Shift+Menu** and **Ctrl+Menu** open no
menu. **Alt+Enter** with one item selected opens Properties for the focused item.
A keyboard-opened item menu is anchored to the item's right edge in Columns and
Icons, and to its center in List.

Each action with a shortcut shows it at the right of its row, such as **Ctrl+C**
beside Copy, **Enter** beside Open, **F2 / Ctrl+R** beside Rename and **Alt+Enter**
beside Properties, with key names in the interface language: German shows **Strg+C**
beside Copy and **Entf** beside Move to Trash.

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
