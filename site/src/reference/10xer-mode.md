---
nodes:
  - integration/10xer-mode
  - integration/10xer-mode/file-verbs
  - integration/10xer-mode/places
  - integration/10xer-mode/search
  - integration/10xer-mode/preview-keys
  - integration/10xer-mode/file-chooser
  - app/keyboard-shortcuts
  - app/shortcut-reference
  - browser/tabs
  - browser/context-menu
  - browser/scrolling
  - browser/view-modes/folder-views
  - preview/preview-panel/find
  - preview/preview-panel/media/audio
  - preview/preview-panel/media/video
reviewed_at: 0a086aa3bdb251842a1e8413e2a6b35970d0b409
---

# 10xer mode reference

10xer mode is an opt-in Yazi-style browsing map. In **Settings → General → BROWSING** the row is titled **10xer mode** and its subtitle is **Opinionated keyboard-centric mode with Yazi-style navigation. Disables some features. Toggle with Ctrl+Shift+M.** The footer shows a compact **10X** pill in its far right corner, after the item count, while the mode is on. It hides window Search, the pane
Close, filter, refresh, and sort controls, and the List and Icons pane header (back,
forward, and up buttons with the folder title) in interactive browsers, disables
type-to-search, and uses the footer as the typed-command surface. The window's
own close button and the clickable List column headings stay. The portal file chooser follows the same preference:
it hides the same pane chrome, uses this keymap and the footer
prompt, and keeps Accept, Cancel, and the header close control. **Enter** / **o**
confirm a file. **Escape** is the way out: it cancels the dialog after dismissing
a prompt, filter, or preview. The chooser
continues to disallow folder peeking and column mirroring, so **i** does not
open a peek or an extra Miller column there.

Turn it on in **Settings → General → BROWSING → 10xer mode**, or with
**Ctrl+Shift+M**. The choice is saved and live-updates every window. **F1** or
**~** opens the in-app table of commands that currently run; it is the only
in-app keybinding reference. While the mode is on, the reference lists only the
10xer map, in these sections: the current view's navigation (such as **Columns
navigation**), **File chooser** (in the file chooser only), **Places**, **Files
and selection**, **Preview**, **10xer mode** (the keys the default map lacks),
**Search and tools**, and **Preview media**. Turning the mode on or off, in any window, switches
an open reference to the newly active map. While the mode is on, the Settings row shows
**(experimental feature, under active development)** under its subtitle. The
footer shows only the **10X** pill; the experimental note is in its accessible
name and description.

Paste destinations, cursor versus filled selection, and pointer ownership stay
as in [keyboard navigation](keyboard-navigation.md).

The keys work on every keyboard layout. On Russian and other non-Latin layouts a
letter key acts as the Latin letter it carries, so the key that types **о** is
**j**. Digits count by their position on the top row, and Caps Lock never changes
a command. On a German layout, **ö** in the file list arms the **;** chord, as
**;** does. See [keyboard layouts](keyboard-navigation.md#keyboard-layouts) for
the full rules.

## Enter and leave

<!-- node: integration/10xer-mode, Entering and leaving -->
<!-- node: integration/10xer-mode, Chrome and Settings -->
<!-- node: integration/10xer-mode, Leaving the mode -->
<!-- node: app/shortcut-reference, Opening and closing -->
<!-- node: app/shortcut-reference, Contents -->

| Key | Action |
| --- | --- |
| **Ctrl+Shift+M** | Toggle 10xer mode. The only key that leaves the mode. |
| **Q** | Close the current window through the normal close path, so a running custom-action job still blocks closing the last window. Lowercase **q** does nothing. |
| **F1** / **~** | Show or hide the in-app shortcut reference |
| **Ctrl+,** | Open Settings, canceling any armed chord |

**Ctrl+Shift+M** also works while a browser text field has focus; modal dialogs
keep their own input handling.
With the Russian layout active and a text field focused, Shift and the **ё**
key type **Ё** rather than toggling the reference.

Turning the mode on in an open window shows a centered 10xer splash for about
1.5 seconds. It takes no focus or clicks, and with reduced motion it appears
without animation. A saved choice applies at launch in every window, before
Settings opens, and launching with the mode already saved shows no splash. The
footer keeps its height when the **10X** pill appears.

Turning the mode on hides an open pane filter bar and re-runs its query with
**f** matching. Turning the mode off shows the bar again and re-runs the query
with default matching.

**Type to search**, **Keep arrows in file list**, and **Include subfolders**
stay saved and editable. While the mode is on they are unused, and those
Settings rows show **Not used in 10xer mode.**
**Mirror columns selection** stays in effect and drives the Columns cursor.

Leaving the mode clears footer prompts (including typed credentials), chords,
find highlights, retained filters/search results, a keyboard folder peek, and
preview keyboard ownership in every open browser window. It leaves the ordinary
listing's filled selection, any Miller column already opened, and any open preview
intact. Default **Ctrl+F** again follows
the saved **Include subfolders** preference; a previous **s** search does not
force it to recurse.

## Navigation

<!-- node: integration/10xer-mode, Movement -->
<!-- node: integration/10xer-mode/preview-keys, Opening and leaving -->
<!-- node: integration/10xer-mode/preview-keys, Surfaces -->
<!-- node: integration/10xer-mode/preview-keys, Handing keys back -->
<!-- node: preview/preview-panel/find, Opening and closing -->
<!-- node: preview/preview-panel/media/audio, Tracks -->
<!-- node: preview/preview-panel/media/video, Stepping and handoff -->
<!-- node: browser/tabs -->

Arrows stay in the file list. In List and Columns, **h** is parent, never the
sidebar. In Icons, **h** / **j** / **k** / **l** and arrows move among tiles.

| Key | Action |
| --- | --- |
| **h** / **Left** | List and Columns: leave the preview, or parent folder, closing the Miller child pane |
| **l** / **Right** | List and Columns: open a directory, or enter a file's preview when possible |
| **h** / **j** / **k** / **l** / arrows | Icons: move spatially among tiles. Do not enter a folder, leave the folder, or open preview. |
| **Enter** | Open the focused item, including files |
| **j** / **k** / **Up** / **Down** | List and Columns: next / previous item in listing order |
| **g g** / **Home** | First item |
| **G** / **End** | Last item |
| **Ctrl+U** / **Ctrl+D** | Half page up / down |
| **Ctrl+B** / **Ctrl+F** / **Page Up** / **Page Down** | Full page up / down |
| **H** / **L** / **Alt+Left** / **Alt+Right** | Back / forward in history |
| **Backspace** / **Alt+Up** | Parent folder |
| **i** | On a file: toggle the preview drawer without moving focus into it. On a directory: in Columns, open the next Miller column without moving focus into it (mirroring usually has already); in List and Icons, toggle the folder-peek popover. |
| **J** / **K** | Scroll the open preview without taking focus |
| **<** / **>** | While the open preview shows audio or video: move to the previous / next file of the same type, still playing if it was playing, without taking focus |

In Columns, the saved **Mirror columns selection** preference (on by default)
applies to the cursor: shortly after **j** / **k** / arrows land on a directory,
its contents open in the next Miller column without moving focus. On a file the
child column closes, and a previewable file opens the preview drawer when
**Single-click file previews** is also on; focus stays in the listing. With mirroring
off, cursor keys only move the cursor. While a **v** / **V** range is active,
mirroring waits, so walking the range never opens or closes a column. In List and Icons, cursor keys never open
a child column or a preview. **l** / **Right** enters a directory or a file preview.
In Columns, **i** on a directory opens the next column and leaves focus where it
is, even with mirroring off. A second press does not move focus. In List and Icons, **i** toggles
the existing folder-peek popover for the focused directory. That popover is the
directory peek, not the saved Folder peeking switch and not a file preview.
Pressing **i** again, or **Escape**, closes the popover. **Escape** does not close a
Miller column. **i** on a file opens the preview drawer if it is closed and
closes it if it is open; keys stay in the listing, so **j** / **k** keep moving
the cursor and the preview follows it. Use **l** / **Right** (List and Columns) or
**J** / **K** to read it. An unpreviewable file flashes `Nothing to preview`. In
an empty folder **i** does nothing.

In **List** and **Columns**, **l** / **Right** on a previewable file opens the
preview if it is closed and moves keys into that pane. A further **l** / **Right**
stays there and does not open the file. Then **j** / **k** / arrows,
**g g** / **Home**, **G** / **End**, **Ctrl+U** / **Ctrl+D** / **Ctrl+B** / **Ctrl+F**, and
**Page Up** / **Page Down** scroll the document instead of the listing. **h** / **Left**
returns to the miller column or folder without closing the preview or going to
the parent; a following **h** still goes to the parent. Unpreviewable files and
empty folders flash `Nothing to preview`. Icons have no preview-entry key.
While the preview owns keys, an accent bar runs across the top of its header,
like the Miller column destination bar, and no column shows that bar. The listing
keeps its fill and location, and its cursor returns with the keys. Leaving the mode, clicking the listing, or
closing the drawer releases ownership; ownership never outlives the drawer.

### Preview keyboard ownership

Each preview surface owns a fixed set of keys (below). It also swallows the
listing's motion and selection keys (**j** / **k**, arrows, paging, **Space**,
**v** / **V**, **Ctrl+A**, **Ctrl+R**), so they never move or fill the listing
behind the drawer.

Listing commands no surface uses hand the keys back to the listing, with the
drawer still open, and run there on the previewed item:

- Folders: **Backspace**, **H** / **L**, **Alt+Left** / **Alt+Right** / **Alt+Up**, **g** places
  and **g +** / **g −**, **z** / **Z**. In a document or archive **g g** still goes to the top, and
  every other valid **g** step runs from the listing; an unknown second key
  flashes `Unknown chord` and leaves the keys in the preview.
- Prompts: **/** (except in a searchable document, where it opens find), **?**,
  **n** / **N**, **f**, **s**.
- Files: **o** / **Enter** (except where the surface uses **Enter**), **y**,
  **x**, **p** / **P**, **Y** / **X**, **d** / **D** / **Delete**, **a**,
  **r** / **F2**, **c**, **,**, **.**, **;**, **O**, **M** / **C**, **R**,
  **Ctrl+C** / **Ctrl+X** / **Ctrl+V**
  (a document or archive tree keeps **Ctrl+C**), **Ctrl+Shift+N**,
  **Alt+Enter**, and **Menu** / **Shift+F10**.

Window commands (**Q**, **F1**, **~**, **F5**, **Ctrl+K**, **Ctrl+L**, **Ctrl+,**,
**Ctrl+1** / **Ctrl+2** / **Ctrl+3**, **Ctrl+H**, **Ctrl+N**, **Ctrl+Shift+B**,
**Ctrl+Shift+M**, undo / redo, text size, and the Ctrl tab shortcuts) work
without moving the keys. The exception is a text or source preview shown in
SourceView rather than in recycled rows (see
[limits and fallback](document-previews.md#limits-and-fallback)): while it has the
keys, **Ctrl+1** / **Ctrl+2** / **Ctrl+3** and undo / redo do nothing. Return the
keys to the listing first, for example with **Shift+Tab**. Any other key is swallowed. Inside a text field,
**F1**, **Ctrl+Shift+M**, **Escape**, **Shift+Tab**, **F5**, **Ctrl+K**, **Ctrl+,**,
the Ctrl tab shortcuts, and text size still work; every other key is typed or
edits the text.

| Key | Document | Archive tree | Password field | Media |
| --- | --- | --- | --- | --- |
| **j** / **k** / **Up** / **Down** | Scroll | Move the member highlight | Typed / text editing | **Up** / **Down** volume; **j** / **k** swallowed |
| **h** / **Left** | Return to the listing | Archive parent; at the archive root, return to the listing | Typed / caret | **h** returns to the listing; **Left** seeks −5 s, **Shift+Left** −30 s |
| **l** / **Right** | Swallowed | Open the highlighted folder; a member file does nothing | Typed / caret | **Right** seeks +5 s, **Shift+Right** +30 s; **l** swallowed |
| **Enter** | Open the file from the listing | Same as **l** | Unlock | Open the file from the listing. A video opens in the default player; mpv, VLC, Celluloid, and MPlayer start where the preview stopped. |
| **Space** | Swallowed | Swallowed | Typed | Play / pause |
| **i** | Close the drawer | Close the drawer | Typed | Close the drawer |
| **Home** / **G** / **End** | Top / bottom | First / last member | Caret (**G** typed) | Seek to the start / the last frame |
| Paging keys | Scroll half / full page | Swallowed | Text editing | **Page Up** / **Page Down** seek +30 / −30 s; **Ctrl+U** / **Ctrl+D** / **Ctrl+B** / **Ctrl+F** swallowed |
| **/** | Find in the document; see [document previews](document-previews.md#text-selection-and-find) | Listing find prompt, as **/** from the listing | Typed | Listing find prompt, as **/** from the listing |
| **0** | Swallowed | Swallowed | Typed | Seek to the start |
| **+** / **=** / **−** | Swallowed | Swallowed | Typed | Volume up / down |
| **m** | Swallowed | Swallowed | Typed | Mute / unmute |
| **<** / **>** | Swallowed | Swallowed | Typed | Previous / next file of the same type in the listing; playback continues if it was playing |
| **J** / **K** | Scroll | Scroll | Typed | Swallowed |
| **Shift+Tab** | Return to the listing | Return to the listing | Return to the listing | Return to the listing |
| **Escape** | Close find if it is open, otherwise close the drawer | Close the drawer | Close the drawer | Close the drawer |

Returning to the listing keeps the drawer open and lands on the same cursor.
Closing with **Escape** or **i** also returns the keys to the listing, so the
Miller column regains its destination bar. **i** therefore toggles the preview
from either side: open from the listing, closed from the preview. A focused
media timeline takes the Media keys above. A focused preview button or slider
(reached with **Tab** or the pointer) keeps GTK's own **Space** / **Enter** /
arrow handling; **Shift+Tab** and **Escape** still return or close. The volume
slider steps 0.1 with the arrows and 0.2 with **Page Up** / **Page Down**; **Home**
mutes and **End** sets full volume. Browsing archive members never extracts them, opens a listing
file, or changes the listing's cursor or fill. Unlocking a password-protected
archive hands the keys to its member tree. **Ctrl+A** / **Ctrl+C** select all
and copy the document's text, never listing items; with **l** the keys go to the
document itself (text, source, or PDF) once it has rendered. In a document,
**Shift+Left** / **Shift+Right** / **Shift+Up** / **Shift+Down**, **Shift+Home**,
and **Shift+End** select text instead of scrolling, and **Ctrl+Home** /
**Ctrl+End** move the text caret to the start / end of the document. Keypad **/**
opens find like **/**. The find button's tooltip reads
**Find in preview (/)** while the mode is on and **Find in preview (Ctrl+F)**
while it is off; toggling the mode updates the tooltip of a preview that is
already open. In media, keypad **+** / **−** also step the volume.

A password prompt takes focus as soon as it appears, including when **i** or
cursor movement shows a locked archive. It then owns the keys like any other
surface: the header shows the owner bar, the Miller column drops its bar, and
**i**, **h**, **j**, **k**, and **l** are typed into the password until **Escape**,
**Shift+Tab**, or unlocking moves focus. If the drawer is hidden for lack of room
when **l** is pressed, it takes the keys when it reappears for the same file;
moving the cursor first cancels that.

With 10xer mode off the default map is unchanged: an archive tree keeps its
arrow, **k** / **j** / **h** / **l**, **Enter**, **Space**, and **Escape** keys
described in [keyboard navigation](keyboard-navigation.md#navigating-an-archive-preview),
and media keys stay on **Ctrl+Alt**.

In **Icons**, **h** / **j** / **k** / **l** and arrows (including keypad) always
move to the next icon in that direction, including while the icons on screen are
search results. They stay in the current folder. They never open the preview
drawer, dismiss search, or transfer keyboard ownership into a preview. **Enter** /
**o** still open the focused item. **Backspace** / **Alt+Up** still go to the
parent.

**g g** is first item. **g h** is Home. In Columns, **g g** and **G** in a
column with no cursor land on its first and last entry.

## Selection

<!-- node: integration/10xer-mode, Selection -->
<!-- node: integration/10xer-mode, Escape -->
<!-- node: browser/scrolling, Middle-click autoscroll -->

**Space** toggles the keyboard cursor, not pointer hover, and does not preview.
**i** toggles a file's preview without moving focus; in List and Columns,
**l** / **Right** enter it. On a directory **i** opens a column or toggles folder
peek.

| Key | Action |
| --- | --- |
| **Space** | Toggle the focused item and move down |
| **v** / **V** | Visual select / visual unset |
| **Ctrl+A** | Select all in the focused pane |
| **Ctrl+R** | Invert the selection |
| **Escape** | Dismiss the current interaction, one step per press; see the precedence below |

On a cursor-only row, **Space** adds that item and moves down; it does not
deselect it. After **Space**, **Ctrl+A**, **Ctrl+R**, or leaving visual,
**j** / **k** / **g g** / **G** / paging move the cursor without rewriting the
fill. **v** then motion starts a new range from the cursor. **V** subtracts the
walked span. In visual mode, **Space** toggles the cursor item without moving it.

A range walks the pane in displayed order, including List type groups, and only
rewrites the fill of that pane. Walking back toward the anchor restores the items
the range had covered; items toggled with **Space** stay toggled. The footer shows
**VISUAL** or **UNSET** while a range is active. Pressing the same key again or
**Escape** leaves visual mode and keeps the fill; the other key starts a new range
at the cursor. Opening another folder, moving to another pane, changing the view,
a pointer selection, **Ctrl+A**, **Ctrl+R**, or leaving 10xer mode also end the
range. In an empty folder **v** / **V**, **Space**, **Ctrl+A**, and **Ctrl+R**
flash `Nothing to select`.

**v** / **V** are the only way to select a range. Shift+arrow keys and
**Shift+Page Up** / **Shift+Page Down** do nothing in the listing; to select while paging,
start a range and use **Page Up** / **Page Down** or **Ctrl+D** / **Ctrl+U** /
**Ctrl+F** / **Ctrl+B**, which extend it like **j** / **k**.

### Escape precedence

Dialogs, the shortcut reference, text editors, and an open folder-peek popover
handle **Escape** before browsing; active autoscroll also stops before listing
dismissal. Closing the peek does not close a Miller column. In a footer prompt it
cancels that prompt: **f** clears its filter, **/** / **?** clear find highlights,
and a nonempty **s** keeps its results. An armed chord is canceled before any
listing action.

With no prompt or chord, each press takes the first applicable step:

- **Recursive `s` results:** leave visual mode (keep the fill), dismiss find
  highlights, close an open preview, then dismiss the results. Dismissal
  restores an earlier committed **f** filter if one existed; otherwise it
  restores the directory listing.
- **Ordinary listing or `f` results:** leave visual mode over the `f` results
  (keep the fill), dismiss the hidden filter, dismiss find highlights, leave
  visual mode (keep the fill), close an open preview, then clear the selection.
  A fill made on the `f` results goes away with them.

While the preview owns keys, **Escape** closes an open find bar, then the drawer,
before any other step, and closing the drawer returns keys to the listing. Unlike **h** while the preview owns keys, the
preview-close step actually closes the drawer. Leaving visual mode or closing a
preview can therefore require an extra **Escape** before retained search results
disappear. Once nothing is left to
dismiss, **Escape** does nothing: it never closes a Miller column or the window.
The sidebar and header controls take the same steps; clearing a filter or
closing the preview from there returns focus to the file list.

## Tabs

<!-- node: browser/tabs, Creating and closing -->
<!-- node: browser/tabs, Switching -->
<!-- node: browser/tabs, Reordering -->
<!-- node: browser/tabs, Opening folders in a new tab or window -->
<!-- node: app/keyboard-shortcuts, Matching -->

From the listing, press **t**, then a second key. The footer shows **t-** and
its available commands. **Escape** cancels the chord; text fields, menus, and
file-chooser requests do not arm it.

| Chord | Action |
| --- | --- |
| **t n** | Open a new tab at the current location |
| **t x** | Close the active tab (the last tab closes the window) |
| **t t** | Select the previous tab in strip order, wrapping from first to last |
| **t 1–9** | Select tabs 1–9 in their current order |
| **t 0** | Select tab 10 |

The digit step also accepts Shift with the digit.

The shared Ctrl-based tab shortcuts also remain available: **Ctrl+T** creates a
tab, **Ctrl+W** closes it, **Ctrl+Tab** / **Ctrl+Shift+Tab** cycle tabs, and
**Ctrl+Page Up** / **Ctrl+Page Down** select the previous / next tab, wrapping
at either end. **Ctrl+Shift+Page Up** / **Ctrl+Shift+Page Down** move the
active tab left / right, stopping at either end of the strip.
**Ctrl+Shift+1** to **Ctrl+Shift+9** and **Ctrl+Shift+0** select a tab directly. Hold **Ctrl+Shift** to
show square number badges; **0** identifies the tenth tab. See
[browser tabs](keyboard-navigation.md#browser-tabs).

**Ctrl+Enter** on a focused folder opens it in a new tab and **Shift+Enter** in
a new window; keypad **Enter** works too. **Ctrl+Shift+Enter** does nothing,
although the default map opens a new tab with it. On a file, **Ctrl+Enter** and
**Shift+Enter** open it like **Enter**. The file chooser opens no tab or window; in a folder request
**Ctrl+Enter** chooses the folder (see [File chooser](#file-chooser)).

## Files

<!-- node: integration/10xer-mode/file-verbs, Targets -->
<!-- node: integration/10xer-mode/file-verbs, Clipboard -->
<!-- node: integration/10xer-mode/file-verbs, Delete and restore -->
<!-- node: integration/10xer-mode/file-verbs, Create and rename -->
<!-- node: integration/10xer-mode/file-verbs, Move and copy -->
<!-- node: integration/10xer-mode/file-verbs, Listing commands -->
<!-- node: integration/10xer-mode/file-verbs, Open With and actions -->
<!-- node: browser/view-modes/folder-views, Remembering values -->
<!-- node: app/keyboard-shortcuts, Matching -->

With an empty fill, **y** / **x** / **d** act on the focused item. Typical flow:
cursor or **v** then motion → **y** / **x** → **h** / **l** / **g h** / **g 1**
→ **p**.

| Key | Action |
| --- | --- |
| **y** / **x** | Yank / cut the selection (or the focused item) |
| **p** | Paste. Keep Both is focused on conflicts when that button is offered; otherwise Replace is. |
| **P** | Paste. Replace is focused on conflicts. **Ctrl+V** does the same. |
| **Y** / **X** | Clear copy/cut marks and this process's clipboard payload. Does not wipe another application's clipboard. |
| **d** / **Delete** | Move to Trash with confirmation; **d d** confirms |
| **D** / **Shift+Delete** | Delete permanently with confirmation. Its **Permanently delete …** button is focused. |
| **r** / **F2** | Rename the focused item in the footer prompt |
| **a** | Create a file. A trailing `/` makes a folder (stripped before validation). Conflicts error instead of uniquifying. |
| **o** / **O** | Open / Open With |
| **M** / **C** | Move / copy the selection (or the focused item) to a folder typed in the footer |
| **R** | Restore the selection (or the focused item) from Trash, with confirmation |
| **c c** / **c n** | Copy path / name |
| **; 1**–**; 9** / **; 0** | Run the first 10 matching custom actions |
| **; t** | Open a terminal in the keyboard-focused folder |
| **; c** | Compress the selection (or the focused item) |
| **; e** / **; E** | Extract the archive here / to a folder typed in the footer |
| **.** / **Ctrl+H** / **Ctrl+.** | Show or hide hidden files |
| **, a** / **, m** / **, s** / **, e** | Sort by name / modified / size / type. Shift reverses. |
| **Ctrl+Z** | Undo the last file operation |

Press **;**, then **1**–**9** or **0** (tenth slot) to run one of the first ten
custom actions that match the focused item, or the filled selection when one
exists; Shift with the digit works too. The panel over the **;-** pill lists them. Matching, order, and
confirmation follow the context-menu catalog: top-level actions come before the
**Actions** submenu's, and disabled or unavailable actions, filter misses,
non-native locations, and an 11th match are omitted. A vacant slot flashes
`No action N` and does not run a different action. The digit checks the catalog
and targets again: if the targets changed since **;**, it flashes
`Selection changed`, and if the slot now holds another action, `Actions changed`;
neither runs anything. A confirming action asks first, and a run shows in Jobs
like one started from the context menu. See [custom actions](custom-actions.md).

**; t** opens a terminal in the keyboard-focused folder, the pane holding the
cursor, whatever the cursor or selection is on. The panel lists it, then
**; c**, **; e**, and **; E**, after the actions. In Trash and other non-local places it flashes
`Can’t open a terminal here`. **Ctrl+Alt+T** keeps its own rule and prefers a
single selected folder; see [Not bound](#not-bound) for where it still works in this mode.

**; c** opens the Compress dialog for the fill, or the cursor item when nothing
is filled; items without a local path flash `Can’t compress these items`.
**; e** extracts one archive beside itself, as the context menu's
**Extract here** does, and selects the result: a single top-level entry lands
as-is, and several land in a folder named after the archive. **; E** opens `extract to ›` for
that archive. Both take the one-item fill or the cursor item: a larger fill
flashes `Extract one archive at a time`, and anything that is not a local
archive flashes `Not an archive`. Empty folders flash `Nothing to compress` /
`Nothing to extract`.

**M** (`move to ›`) and **C** (`copy to ›`) fix the fill, or the cursor item
when nothing is filled, when the prompt opens; **Up** / **Down** choose among the
listed folders and never move the cursor away from them. Typing lists
destination folders through the [folder picker](#folder-picker). **Enter**
moves or copies into the chosen folder and keeps you in the current one; a moved
cursor item hands the cursor to its neighbor, as **d** does, without adding the
neighbor to the fill. Conflicts ask as **p** does, with Keep Both focused when it
is offered. Neither prompt lists the folders being sent or anything inside them,
and **M** does not list the folder the items are already in. A typed path is
still checked: a path ending in `/` that does not exist (`No such folder`), a
file (`Not a folder`), a move back into the source folder
(`Already in this folder`), or a folder inside one of the moved or copied
folders (`Can’t put a folder inside itself`) keeps the prompt open with the
reason. Text that names no existing folder, such as `/tmp/newdir` or `nowhere`,
does not show `No such folder`: **Enter** acts on the chosen match from the
list, or shows `No matching folders` when nothing is listed. Empty **Enter**
closes the prompt. **Escape**, focus
leaving the prompt, another prompt, leaving the mode, or closing the window
discard it. Items that cannot be moved flash `Can’t move these items`; an empty
folder flashes `Nothing to move` / `Nothing to copy`. **; E**'s `extract to ›`
uses the same picker and rules and also stays in the current folder.

**R** restores the fill, or the cursor item, from Trash through the same
confirmation as the context menu's **Restore**. Outside Trash it flashes
`Only items in Trash can be restored`; an empty Trash flashes
`Nothing to restore`.

**, a** / **, m** / **, s** / **, e** sort the focused pane by name, modified
time, size, or type, ascending; with Shift (**, A** / **, M** / **, S** / **, E**)
descending. The pane keeps its cursor and fill, other open Miller columns keep
their order, and the choice is saved like a sort chosen from the pane menu or a
List heading: for this folder when **Remember sort and icon size per folder** is
on (the default), otherwise as the default sort. In Trash, Recent, remote
shares, and other folders that are not remembered, it lasts while the column is
open. List headings show the new sort, so clicking
one afterwards reverses what is actually applied. **.** / **Ctrl+H** /
**Ctrl+.** change the saved hidden-files preference in every window, including
over **f** results; clearing a filter never reveals hidden files on its own.

**y** / **x** / **d** / **c c** / **c n** take the focused pane's fill, or its
cursor item when nothing is filled, including on **f** and **s** results. A
hovered row, a parent folder, and a Miller column's open-path marker are never
targets. **y** and **Ctrl+C** show the copy icon on those items, and **x** and
**Ctrl+X** show scissors; cut wins when both could apply. The marks follow
view changes and every window, and go away when another application takes the
clipboard. Nothing moves until a paste completes, and a completed cut move
clears its marks.

**p** / **P** / **Ctrl+V** paste into the same directory as the default map's
**Ctrl+V** (see [keyboard navigation](keyboard-navigation.md#input-precedence)),
and pasting never changes pointer or keyboard ownership. Focusing a conflict
button does not choose it: nothing changes until you accept, and Cancel or
**Escape** leaves both items untouched. Keep Both is offered only for copies.

**d** / **Delete** show a **Move … to Trash?** confirmation (for example
**Move 3 items to Trash?**) with its confirm button focused; pressing **d** again confirms it, so **d d** trashes. **D** / **Shift+Delete**, and **d** inside Trash, show the permanent
deletion confirmation with its confirm button focused, so **Enter** confirms, and **d**
there does nothing. In a folder whose listing reports no Trash support (such as
a tmpfs), **d** / **Delete** open a permanent confirmation instead, stating
that the location doesn't support Trash, with Cancel focused, so **d d** does
not delete there. Errors appear in
the usual operation dialogs, and **Ctrl+Z** undoes what the default map can undo.
In Columns, **d** with focus in an open folder's empty child column asks to
trash that folder. While **f** or **s** results show no hits, **d** and **D**
flash `Nothing to delete` and leave the open folder alone.

**a** opens `create ›` in the footer. **Enter** creates an empty file with exactly
the typed name in the keyboard-focused folder; spaces and Unicode are kept. A
trailing `/` makes a folder instead and is removed before the name is checked. An
empty name, `.`, `..`, or a name containing `/` keeps the prompt open with the
reason, and so does a name already taken (including by a broken link), which
shows `“…” already exists`, so you can fix it. Nothing is renumbered, replaced, or followed. **Escape**, focus leaving
the prompt, a clicked row, another prompt, leaving the mode, or closing the
window discard the name. **Ctrl+Shift+N** still adds a numbered **new folder**
and renames it in place. Trash and Recent flash `Can’t create items here`.

**r** / **F2** open `rename ›` in the footer for the focused item: the cursor
item, or the focused **f** / **s** hit, never the fill, a hovered row, or an
open-path marker. The current name is filled in with a file's stem (or a
folder's whole name) selected, as inline rename selects it. The item is fixed
when the prompt opens; **Up** / **Down** do not move the cursor while it is open.
**Enter** renames the item to exactly the typed name and keeps its contents; an
unchanged name does nothing. An invalid name keeps the prompt open with the
reason, and a name already taken shows `“…” already exists`; nothing is replaced. Permission errors and
filesystem limits leave the original name and show the usual rename error.
**Escape**, focus leaving the prompt, a clicked row (which keeps its selection),
another prompt, leaving the mode, or closing the window discard the typed name.
Trash items flash `Can’t rename items here`. The context menu's **Rename** and a
new folder from **Ctrl+Shift+N** still edit the name in place.

Empty folder: **y** / **x** / **d** / **r** / **Space** flash
`Nothing to yank` / `cut` / `delete` / `rename` / `select`, and **c c** /
**c n** flash `Nothing to copy`. **i** in an empty
folder does nothing; on an unpreviewable file it flashes `Nothing to preview`. In
List and Columns, empty-folder and unpreviewable-file **l** / **Right** flash
`Nothing to preview`. With an empty clipboard, **p** and **P** flash
`Nothing to paste`. **x** on items that cannot be cut flashes
`Can’t cut these items`.

**O** looks up file types and application choices asynchronously for the fill,
or the focused item, and opens the Open With chooser without launching anything
itself. For a mixed selection, Recommended Applications contains handlers shared
by every selected type; Other Applications remains available for an explicit
choice. A new key, selection/focus change, navigation, mode exit, or closed
window prevents an older lookup from opening a chooser over the new interaction.
Unreadable files and broken links flash an error instead of guessing a type from
the first item, and so does a selection no application can open. An empty
folder flashes `Nothing to open`.

## Places

<!-- node: integration/10xer-mode/places, The `g` chord -->
<!-- node: integration/10xer-mode/places, Pins -->
<!-- node: integration/10xer-mode/places, `go ›` -->
<!-- node: app/keyboard-shortcuts, Matching -->

Press **g**, then a second key. The chord stays armed while the footer **g-**
pill is showing beside the **10X** pill, and a panel over the pill lists the valid second keys; it
never takes focus, so the next key still completes the chord. While the sidebar
shows full rows, not the narrow icon rail it collapses to when the window runs
short of room, keycaps appear on Home (**h**), Downloads (**d**), Trash (**t**), Network (**n**),
Recent (**r**), Documents (**k**), Music (**m**), Pictures (**p**), Videos (**v**), and
visible PINNED rows (**1**–**9** in display order). **,**, **c**, and **;** show
the same kind of list (sort options / copy path or name / matching custom
actions) while armed. The second key completes only that chord: **, a** /
**, m** / **, s** / **, e** sort instead of create / search, and search-result
**j** / **h** cannot steal a pending **g**, **c**, **;**, or **t**. Sort-chord **, n** /
**, t** cancel with `Unknown chord`.

| Second key | Destination |
| --- | --- |
| **g** | First item |
| **f** | Follow search result: open the folder holding the hit under the cursor, with that item selected. Ends the search. Without hits: `Nothing to reveal`. |
| **h** | Home |
| **d** | Downloads. Missing: `No Downloads folder`. |
| **c** | Config (`~/.config`). Missing: `No .config folder`. |
| **t** | Trash |
| **n** | Network |
| **r** | Recent |
| **k** | Documents. Missing: `No Documents folder`. |
| **m** | Music. Missing: `No Music folder`. |
| **p** | Pictures. Missing: `No Pictures folder`. |
| **v** | Videos. Missing: `No Videos folder`. |
| **1**–**9** | Visible PINNED rows in sidebar order. Missing: `No pin N`. |
| **+** / **−** | Pin / unpin the folder under the cursor, or the focused pane's folder when the cursor is on a file or the pane is empty |
| **Space** | Footer `go ›` — pick a folder with the [folder picker](#folder-picker), or type a path or URI |
| **Escape** | Cancel |

An unknown second key cancels with `Unknown chord`.

**g +** (also keypad **+**) adds the folder to PINNED and reports its **g**
digit when it is among the first nine visible pins, for example
`Pinned “Projects” as g 3`; a pin beyond the first nine flashes
`Pinned “Projects”` with no digit. **g −** (also keypad **−**) removes it and
flashes `Unpinned “Projects”`. A folder already pinned flashes
`“Projects” is already pinned`; unpinning one that is not pinned flashes
`“Projects” isn’t pinned`. **g** then Shift+keypad **+** or Shift+keypad **−**
neither pins nor unpins. Where a top-row key types **+** or **−**, as on
AZERTY, **g** then that key pins or unpins instead of opening a pin. The digit
steps also accept Shift with the digit. Home, the standard folders, Trash, and
other places with their own sidebar rows flash `Can’t pin “…”`.

**g Space** opens **go ›** in the footer instead of toggling the selection.
Typing never navigates; it lists matching folders through the
[folder picker](#folder-picker). **Enter**, or a click, opens the chosen folder.
When nothing is listed, such as for a URI or a path no folder matches, or when
the typed path names an existing file or folder, **Enter** submits the text through the same navigation as the location bar
(**Ctrl+L**). `.` and `..` in a local path resolve as text, without checking the
filesystem. A path naming a file opens its folder with the file selected, and
URI input is submitted unchanged, except that a password typed in the URI moves
into the mount operation instead of the location. A missing or unreachable
destination shows the location bar's error and leaves the current folder open.
Empty **Enter** just closes the prompt. **Escape** cancels without navigating;
clicking a listing row ends the prompt and keeps the clicked selection. The
entry is cleared on submit, **Escape**, focus loss, a replacing prompt, and mode
exit, and it keeps no undo history, so reopening the prompt or another window
cannot recover typed credentials. Anything that looks like a URI (`scheme://`,
a scheme the location bar opens such as `sftp:`, `//host`, `\\host`, or
`user@host:`) lists nothing and is never searched,
mounted, or probed before **Enter**.

## Prompts

<!-- node: integration/10xer-mode/search, Find -->
<!-- node: integration/10xer-mode/search, Filter -->
<!-- node: integration/10xer-mode/search, Search -->
<!-- node: integration/10xer-mode/places, `z` and `Z` -->
<!-- node: integration/10xer-mode/places, Folder picker -->
<!-- node: integration/10xer-mode/file-verbs, Create and rename -->
<!-- node: integration/10xer-mode/file-verbs, Move and copy -->
<!-- node: integration/10xer-mode, Keymap ownership -->
<!-- node: app/shortcut-reference, Opening and closing -->

Typed commands use the footer, never the pane filter revealer or the global
search dialog. **Enter** submits, **Escape** cancels. **Up** / **Down** move the
listing or pick a history candidate without leaving the prompt. Clicking a
listing row closes the prompt and keeps that selection. An **Enter** that an
input method uses while composing does not submit the prompt; one it passes
back does. While a footer prompt has focus, **~** is typed into it; **F1**
still opens the reference.

| Key | Action |
| --- | --- |
| **/** / **?** | Find next / previous name in this listing. Does not hide rows. Enter keeps matching substring highlights; **Escape** from the listing dismisses them. |
| **n** / **N** | Repeat the last find. **N** reverses. |
| **f** | Fuzzy name filter for this folder (hides non-matches). The footer shows `filter: …` until dismissed. |
| **s** | Fuzzy path search below the current folder (cap 100). The footer shows `search: …` until dismissed. Prompt **Escape** keeps hits; listing **Escape** follows the precedence above. |
| **z** | Jump to a visited folder (name match, then frecency) |
| **Z** | Jump to a recently visited folder (last visit first) |
| **a** | Create |
| **r** | Rename |
| **M** / **C** | Move / copy to a typed folder (`move to ›` / `copy to ›`) |
| **; E** | Extract the archive to a typed folder (`extract to ›`) |
| **Up** / **Down** | Choose a listed folder in the go, jump, recent, move, copy, and extract prompts |
| **Tab** | Write the chosen folder into the go, move, copy, or extract prompt |

**/** is a cursor jump; **f** hides non-matches. The prompt covers the footer and
stays focused while you type. Matching is a case-insensitive substring of the
name, searched in display order from the cursor and wrapping at either end.
Matching substrings stay highlighted in the theme's accent color after Enter in
Columns, Icons, and List. **Escape** from the listing dismisses those highlights without hiding rows.
Empty **/** with Enter closes the prompt and changes nothing. **Escape** from the
prompt cancels without leaving highlights. Pressing **/** again shows the
prompt. **n** repeats the last query, including multi-character input, in its
original direction; **N** reverses it, and either shows the highlights again.
A miss reports `No matches for “…”` and leaves the cursor where it was.
**n** / **N** before any find flashes `No previous find`. Moving
focus out of the prompt (clicking a row, another pane) discards it; the
committed query is kept per tab and forgotten when the mode is left.

**f** filters as you type. Enter on **f** commits the filter, closes the prompt,
and returns keyboard focus to the filtered listing (its first result once the
results arrive) without opening an item. A following **Enter** opens the
focused item. Opening **f** again pre-fills the current query. Empty Enter,
**Escape** from the prompt, or **Escape** from the list clears it. Moving focus out of
the prompt keeps what was typed. View rebuilds keep the filter and the funnel
collapsed. While a filter is active, the footer count is the displayed result
count, including zero, with a file/folder breakdown in its accessible description; motion,
**Enter**, and **Ctrl+R** act on the results, never on the hidden directory's
cursor or fill.

**s** always searches the current folder tree, not every indexed root, and
matches paths below it the way fzf does: each space-separated term must match
somewhere in a hit's path, in any order, as a fuzzy subsequence, so
`git trading readme` finds `git/trading/README.md`. Each term is tried
against the hit's name first, then against its whole path. A term written
`'term` must appear as one unbroken run of characters, `^term` must start the
hit's name or its path, `term$` must end it, and `!term` excludes paths that
contain it. Hits whose names match more terms rank
first, then closer matches; among similar matches, folders visited often and
recently, and files inside them, rank higher. The characters a hit's name
matched stay highlighted in the theme's accent color; while find highlights
show, they replace them. Find, **f**, and **s** highlights recolor at once
when the theme changes. **f** uses the same terms and highlights, but never
recurses: it ignores **Include subfolders** and matches only the names of the
folder's own items, so `rep md` keeps `gamma-report.md`. Wildcard filter
patterns do not apply in either. **S** is unbound; there is no content search.
**Enter** on **s** applies the query, closes the prompt, and returns keyboard focus to the results,
on the first hit when there is one. It does not open that hit. A following
**Enter** opens it through ordinary item activation, not **Open search results
directly**. **Ctrl+K** global search is unchanged. **Escape** from the prompt keeps
the hits so **v** / **V** / Space / **i** can use them (and **Right** in List and
Columns). From those results, **Escape** dismisses visual mode, find highlights, and an open
preview before dismissing search, as described above. In List and Columns, **h** dismisses
search directly unless the preview owns keys, in which case it first returns to
the hits without closing the preview. In Icons, **h** / **j** / **k** / **l** and
arrows move among the result icons and do not dismiss search or open an item.
Search dismissal restores a previously committed **f** filter, or the unfiltered
directory otherwise. Empty **Escape** cancels without retaining search results.
The footer count is the displayed hit count, not the hidden directory's fill.
If another program deletes the cursor's file while the **f** or **s** prompt has
focus, focus stays in the prompt. If another program renames or moves the
searched folder, the **s** search ends; a search in a shallower Columns column
stays.
At its left end, the footer shows the search hit under the cursor as a path
relative to the searched folder. When space is short, an ellipsis replaces the
end of its folder part so the file name stays readable; the accessible name has
the full path. While focus is outside the hits, such as in a menu, the sidebar, or **F1**, the
footer keeps the last hit the cursor rested on. **f** filters show no path. Pressing **s** again while hits are showing
pre-fills their query. A new query,
navigation (including opening a directory hit), leaving the mode, or closing the
window discards the previous query's pending hits; a view change keeps the
search. A folder without a local path, such as Network, flashes
`Nothing to search`.

**z** (`jump ›`) and **Z** (`recent ›`) pick from the folders Strata has
opened, the same saved history as the default map's **Ctrl+Shift+K**, not a
zoxide database. They match each folder's full path with the same terms as
**s**: space-separated fuzzy terms in any order, `'term`, `^term`,
`term$`, and `!term`, so `z dev str` finds `~/dev/strata`. **z** ranks
folders whose names match more terms first, a name typed exactly first among
those, then by how often and how recently each folder was opened; **Z** keeps
matching folders in last-visit order. The folder already open is left out. Candidates list above the footer
as you type, including for empty input, with the first one chosen. **Up** /
**Down** choose another row (wrapping) while the entry keeps focus, and the
footer shows the position, such as `2 of 5`. **Enter** or a click opens the
chosen folder once. Editing the text lists
fresh candidates and chooses the first again. A miss shows
`No matching folders`, and **Enter** then leaves the prompt open without
navigating. **Escape**, focus loss, a replacing prompt, and leaving the mode close
the prompt without opening a candidate.

### Folder picker

**g Space**, **M**, **C**, and **; E** pick a folder from a list above the
footer, like **z**. Typed text is matched against the paths of folders below the
open folder with the same terms and ranking as **s**, but only folders are
listed (up to 100). Folders that `.gitignore` or `.ignore` files exclude, and
generated trees such as `node_modules/`, `target/`, and `.cache/`, are not
listed; type their path to choose them. A folder the whole query names outright comes first: one at
exactly that path below the searched folder, then any with exactly that name,
however often other folders were visited. Hidden folders are listed when the
listing shows them or a term starts with `.`. Searches from `/` skip `/proc`,
`/sys`, and `/dev`, and a search below a typed path starts once typing pauses.
Other text with a colon, such as `10:30`, is an ordinary query.

Text that starts as a path (`/`, `~`, `~/`, `./`, `../`, or just `..`) moves the
search: everything through its last `/` names the folder to search below, and
the rest is the query, so `/etc/ss` searches below `/etc` for `ss` and
`~/dev/ str` searches `~/dev`. `.` and `..` resolve as text. With
nothing after the last `/`, as in `/etc/`, the list starts with that folder
itself (unless a move or copy would refuse it), then the listed folders below
it, the most visited first and then the shallowest. Without an open local folder, such
as in Trash, only absolute paths and `~` / `~/` paths work. Other text,
including `./` and `../`, shows `Type a full path here`. Another user's home (`~name`)
shows `Only ~ and ~/ are supported`, and **M**, **C**, and **; E** show
`Only local folders can be chosen` for a URI.

The first folder is chosen. **Up** / **Down** choose another (wrapping) and the
footer shows the position (`2 of 5`); results that arrive later keep that
choice while it is still listed. **Tab** writes the chosen folder into the
prompt as `./…/` below the open folder, `~/…/` below home, or an absolute path,
always ending in `/`. That lists the folder first and searches inside it as you
type more; **Tab** never acts on it. **Enter** or a click acts on the chosen
folder. When the typed path names an existing item, **Enter** acts on it at once
unless another folder was chosen with **Up** / **Down**. Otherwise **Enter**
before the search finishes waits for it, so a better match found late still
wins. While nothing is found yet the footer shows `Searching…`,
and a finished search with no folder shows `No matching folders`. Editing the
text, **Escape**, focus loss, a replacing prompt, leaving the mode, and closing the
window cancel a search, and a late result never changes the list.

## Search results

<!-- node: integration/10xer-mode/search, Search results -->

While **s** results are showing:

| Key | Action |
| --- | --- |
| **j** / **k** | List and Columns: move the result list. Icons: move to the next result icon in that direction. |
| **l** / **Right** | List and Columns: open a directory hit, or enter a file hit's preview when possible. Icons: move to the next result icon. |
| **Enter** | With focus already on the results, activate the focused hit once through ordinary open. **Enter** in the **f** or **s** prompt only applies that prompt. |
| **i** | Directory hit: open an unfocused Miller column, or toggle folder peek. File hit: toggle the preview. Neither takes preview ownership. |
| **h** | List and Columns: leave preview keyboard ownership, or dismiss search (restoring an earlier **f** filter if present). Icons: move to the next result icon. |
| **g f** | Follow search result: open the folder holding the focused hit and select it there. Ends the search without restoring an **f** filter, so the item is visible; **H** returns. |

**Space** does not preview search rows. Use **g g** / **G** to reach the first /
last result; **Home** / **End** and paging keys are swallowed on result lists
rather than moving the hidden directory cursor. **Ctrl+R** inverts **f** matches,
but is inactive for recursive **s** hits. Once the preview owns keys, its scrolling
map takes precedence.

## Sidebar and surrounding controls

<!-- node: integration/10xer-mode, Sidebar and header -->
<!-- node: integration/10xer-mode, Keymap ownership -->
<!-- node: browser/context-menu, Opening -->

Arrows and **h** / **j** / **k** / **l** stay in the Columns, List, and Icons
panes. **Tab** moves from the file list to the window header. **Shift+Tab**
stays with the files. From the footer or other chrome outside the header and
sidebar, the next **Tab** or arrow key returns to the file list.

**Ctrl+N** shows or hides the sidebar, like the header toggle, and passes
through while the preview owns the keys. **Ctrl+B** pages up instead of
toggling it. **Ctrl+Shift+B** focuses the sidebar when it is visible; a hidden
sidebar stays hidden. Pressing **Ctrl+Shift+B** again returns to the files.
The sidebar toggle's tooltip reads **Toggle sidebar (Ctrl+N)** while the mode is
on and **Toggle sidebar (Ctrl+B)** while it is off, in windows and in the file
chooser.

In the sidebar, **j** / **k** and **Up** / **Down** move between places and
device controls. **l**, **Enter**, and **Space** activate the focused place or
device control. **h**, **Left**, and **Backspace** return to the files. Returning
without activating keeps the file selection. After a place opens another folder,
focus is on that listing. **Menu** or **Shift+F10** on a focused sidebar place,
Trash, or drive row opens that row's context menu.

On a header control, **Enter** and **Space** activate it. **h** and **j** return
to the files and do not change directory or run a file operation.

After you return from another window, **g**, **f**, and **s** act on the
listing without first clicking a row.

**Ctrl+L** still edits the location bar. Menus, dialogs, text fields, and the
shortcut reference keep their own keys. The file chooser uses these same
round trips.

## File chooser

<!-- node: integration/10xer-mode/file-chooser, Following the mode -->
<!-- node: integration/10xer-mode/file-chooser, Choosing -->
<!-- node: integration/10xer-mode/file-chooser, Save requests -->
<!-- node: integration/10xer-mode/file-chooser, Refused commands -->

The portal file chooser follows the saved preference, and live changes to it,
without opening Settings. While the mode is on, a footer under the files carries
the same prompts, chords, and feedback, and the pane chrome hides as in a window.
Accept, Cancel, the header close control, and List headings stay.
**Ctrl+Shift+M** works in the chooser, even from the name or location field.
Turning the mode off there keeps the request open, hides the footer, and
restores the chooser's own keys. Lowercase **q** neither ends the request nor
leaves the mode.

The chooser uses this map within the request's limits. A key the request does not
allow is refused when it is pressed, not only hidden:

| Key | In the chooser |
| --- | --- |
| **Enter** / **o** on a file | Choose the file instead of opening it. In a multiple-file request with a fill, choose the fill. |
| **Enter** / **o** on a folder | Open it. **Ctrl+Enter** or **Accept** chooses a folder in a folder request. |
| **Enter** in a Save request | Save in the current folder, whatever the cursor is on. In Recent, save in the folder of the filled or cursor file. An existing file asks first. |
| **o** on a file in a single-file Save request | Save over that file. It asks first. |
| **r** / **F2** in a single-file Save request | Edit the name, with the part before the extension selected. **Enter** saves; **Escape** returns to the files and keeps the edit. |
| **Escape** | Take one dismissal step from [Escape precedence](#escape-precedence), then cancel the request. The automatic first-row selection is not a step. |
| **Space**, **v** / **V**, **Ctrl+A**, **Ctrl+R** | Only in requests that let you choose several files or folders. Otherwise, Save requests included, `Only one item can be chosen`. |
| **a**, **r** / **F2**, **d** / **D** / **Delete**, **,** sorts, **.**, **c c** / **c n** | As in a window, except **r** / **F2** in a single-file Save request. |
| **g** places, **g Space**, **z** / **Z** | Local folders and Recent only. Trash, Network, and remote pins flash `Only local folders can be opened here`; a typed remote location shows the unsupported-location error. |
| **y**, **x**, **p** / **P**, **Y** / **X**, **M** / **C**, **R**, **g +** / **g −**, **Ctrl+C** / **Ctrl+X** / **Ctrl+V**, **O**, **;**, **i**, **Q** | `Not available in the file chooser`. The chooser does not copy, move, or restore files, change pins, open them with an application, run custom actions, peek folders, or open an extra Miller column, and **Q** does not close the chooser: cancel with **Escape**, Cancel, or the close control. |
| **Ctrl+K**, **Ctrl+Shift+K**, **Ctrl+,**, **Ctrl+Z** | Unbound. |

The request takes the fill, or the cursor item when nothing is filled; the
automatic first-row selection never counts. A Save request saves in the current
folder; in Recent, which has no folder of its own, it saves in the folder of the
filled or cursor file. Outside Recent, moving the cursor changes neither the
name nor the destination. While the name or location field has focus, every key but **F1**,
**Ctrl+Shift+M**, and **Escape** is left to the field; **Ctrl+A** selects the text.
Every request starts with focus in the files. **Tab** goes from the files to the
header, and from the header to the **Name** field when the request has one (a
single-file Save request or a file Open request). From the **Name** field,
**Tab** follows the dialog's ordinary focus order to the next control, and
**Escape** returns to the files with the edit kept.
Saving over an existing file asks first with Cancel focused. Beside Cancel and
Save, a Save request shows hints for **Enter**, plus **r** and **o** when it
saves one named file.

**f** and **s** hits follow the request's folder-only and file-type limits.
**F1** shows a reference listing only the keys the request allows; **Escape**
closes it without canceling the request. The **g** panel leaves out **g t**,
**g n**, **g +**, and **g −**.

## Still bound

<!-- node: integration/10xer-mode, Keymap ownership -->
<!-- node: browser/context-menu, Contents and grouping -->
<!-- node: app/shortcut-reference, Menu hints -->

These GUI conventions stay available alongside the Yazi verbs:

| Key | Action |
| --- | --- |
| **Ctrl+C** / **Ctrl+X** / **Ctrl+V** | Copy / cut / paste the selection as in the default map. **Ctrl+V** focuses Replace on conflicts, like **P**. |
| **Delete** / **Shift+Delete** | Trash / permanent delete (same as **d** / **D**, with confirmation) |
| **F2** | Footer rename (same as **r**) |
| **F5** | Refresh |
| **Ctrl+L** | Edit the location bar |
| **Ctrl+K** | Global search |
| **Ctrl+1** / **Ctrl+2** / **Ctrl+3** | Columns / Icons / List |
| **Ctrl+Shift+N** | New folder |
| **Ctrl+Alt+N** | New folder containing the selection |
| **Alt+Enter** | Properties |
| **Menu** / **Shift+F10** | Context menu |
| **Ctrl++** / **Ctrl+−** / **Ctrl+0** | Text size |

Context-menu shortcut hints follow this map (**x** cut, **y** yank, **p** paste,
**d** / **D** trash / delete, **r** rename, **M** / **C** move / copy to, **R**
restore, **i** quick preview, next column, or folder peek). The file chooser has no **i** preview, so its Quick preview item
shows no hint. **Duplicate**, **Copy path**, **Pin to sidebar**, and **Open in
Terminal** show no hint, because their default keys (**Ctrl+D**, **y**, **p**,
**Ctrl+Alt+T**) are remapped or not part of this map; **Space** for preview and **Ctrl+R**
for rename are hidden too. Use **c c** to copy a path and **g +** to pin.
Properties keeps **Alt+Enter**.

## Not bound

<!-- node: integration/10xer-mode, Keymap ownership -->

These default-map shortcuts are unbound or remapped while the mode is on:

| Default-map key | In 10xer mode |
| --- | --- |
| **Ctrl+Shift+K** | Unbound. Use **z** / **Z**. |
| **Ctrl+Alt+T** | Does nothing while a text field such as the location bar has focus, or while search results are listed. From the file list or the sidebar it still opens a terminal, as in regular mode. Use **; t** or the context menu. |
| **Ctrl+\\** | Unbound. Arrows never leave the file list. |
| **Ctrl+D** | Half page down. Duplicate has no key; use **Duplicate** in the context menu. |
| **Ctrl+F** | Full page down. Filter is **f**. |
| **Ctrl+B** | Full page up. Sidebar toggle is **Ctrl+N**. |
| **Ctrl+R** | Invert selection. Rename is **r** / **F2**. |
| **y** / **p** (default map) | Yank / paste. Path copy is **c c**; pin with **g +** and jump to a pin with **g** then a digit. |
| **Space** | Toggle selection. Preview is **i** on a file; in List and Columns, **l** / **Right** also open it and move the keys into it. |
