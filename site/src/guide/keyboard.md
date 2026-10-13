---
nodes: [app/shortcut-reference, app/keyboard-shortcuts, browser/selection/keyboard-navigation]
reviewed_at: 0a086aa3bdb251842a1e8413e2a6b35970d0b409
---

# Keyboard

Run Strata without touching the mouse. Learn the keys below, press F1 when
you forget one, and use the arrows to move between files, the sidebar, and
the top navigation bar.

## Shortcuts worth memorizing

<!-- node: app/shortcut-reference, Contents -->
<!-- node: browser/selection/keyboard-navigation -->

| Keys | What it does |
| --- | --- |
| F1 | Show or hide the shortcut reference |
| Ctrl+K | Open global search |
| Ctrl+F | Filter the current pane |
| Ctrl+L | Edit the location |
| Enter | Open the current item |
| Space | Preview a file, or open a folder |
| Alt+Left / Alt+Right | Back / forward in history |
| Alt+Up | Go to the parent folder |
| Ctrl+C / Ctrl+X / Ctrl+V | Copy, cut, paste |
| Ctrl+Z / Ctrl+Shift+Z | Undo / redo the last file operation |
| F2 | Rename |
| Delete / Shift+Delete | Move to Trash / delete permanently |
| Ctrl+1 / Ctrl+2 / Ctrl+3 | Switch to Columns, Icons, or List |
| Ctrl+T / Ctrl+W | New tab / close the active tab |

## Look up any shortcut

<!-- node: app/shortcut-reference, Opening and closing -->
<!-- node: app/shortcut-reference, Finding a shortcut -->
<!-- node: app/shortcut-reference, Footer status -->

1. Press F1, or click **F1 Shortcuts** at the bottom left of the window.
2. Type into **Search actions or keys…**: `rename` finds F2, and `ctrl+k`
   finds global search.
3. Press F1 or Escape to close it. Focus returns where it was.

The list shows only the keys that work in the current view.

## Move through views

<!-- node: browser/selection/keyboard-navigation, Within the file list -->
<!-- node: browser/selection/keyboard-navigation, Leaving the file list -->
<!-- node: browser/selection/keyboard-navigation, Tab stops -->

Plain arrows move focus. In Icons and List they never change directory.

- **Columns:** Up and Down move through a column. Right enters the folder,
  Left goes back to the parent column. Right never opens a file; press Enter
  to open it. If the file's preview is showing, Right moves focus into it.
- **Icons:** arrows move one tile in that direction.
- **List:** Up and Down move through rows.

Keep going past the edge to reach the rest of the window:

- Up from the first item focuses the pane header. Left and Right move between
  its buttons, Enter or Space presses one, and Down returns to your file.
- Left focuses the sidebar: from the left edge in Icons, any row in List, or
  the first column in Columns. Up and Down move between places, and Right
  returns to the files.
- Up from the top of the sidebar reaches the top navigation bar.

Home and End jump to the first and last item, and Page Up and Page Down move
one page. Tab leaves the file list in one press, and Shift+Tab back into it
lands on the item you left.

To find a file by name, start typing: **Type to search**, on by default,
opens the pane filter with what you typed and shows only matching items (see
[Find files](search.md)). Turn it off in **Settings → General** and `h`, `j`,
`k`, `l` act as Left, Down, Up, Right instead.

## Good to know

<!-- node: app/keyboard-shortcuts, Matching -->
<!-- node: browser/selection/keyboard-navigation, Keep arrows in file list -->
<!-- node: app/shortcut-reference, Footer status -->
<!-- node: app/shortcut-reference, Contents -->

- Shortcuts work on any keyboard layout and ignore Caps Lock. On Russian,
  Ctrl+C is the key that types с. Digits count by position, so Ctrl+1 works
  on AZERTY without Shift.
- Turn on **Keep arrows in file list** in **Settings → General** to stop
  arrows leaving the files. Ctrl+\ toggles it, and Ctrl+Shift+B jumps to the
  sidebar.
- Hide the **F1 Shortcuts** button with **Show F1 Shortcuts button** in **Settings → General**.
  F1 still opens the reference.
- In [10xer mode](10xer.md) (Ctrl+Shift+M) the keys change, and F1 lists
  only the 10xer keys.

**Full detail:** the [Keyboard navigation reference](../reference/keyboard-navigation.md)
covers every key, view, and focus rule.
