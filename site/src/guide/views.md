---
nodes: [browser/view-modes, browser/view-modes/columns, browser/view-modes/icons, browser/view-modes/list, browser/view-modes/sorting, browser/view-modes/folder-views, browser/view-modes/text-size, browser/view-modes/position-restore]
reviewed_at: 0a086aa3bdb251842a1e8413e2a6b35970d0b409
---

# Views

Show any folder as Columns, Icons, or List, and switch with one key. Sort each
folder its own way, and set the text size for the whole app.

## Switch between Columns, Icons, and List

<!-- node: browser/view-modes, Switching -->
<!-- node: browser/view-modes/columns -->
<!-- node: browser/view-modes/icons -->
<!-- node: browser/view-modes/list -->

| Press | View | What you get |
| --- | --- | --- |
| Ctrl+1 | Columns | One column per open folder, so the whole path stays visible. The default. |
| Ctrl+2 | Icons | A grid of thumbnails, with size, dimensions, duration, or item count under each name. |
| Ctrl+3 | List | A table with Name, Mode, Size, Type, and Modified columns. |

Or click **Appearance** in the window header and pick a view under **VIEW**.
Switching keeps your folder, selection, and filter. Strata reopens in the view
you used last.

In Columns, click a folder to open it as the next column. Drag a column's right
edge to resize it. When you let go, the window's other open columns match that
width, and new columns open at it. Double-click the edge to fit one column to its
contents.

In Icons, click **Thumbnail size** in the pane header and drag the slider
between 32 and 256 px.

## Sort a folder

<!-- node: browser/view-modes/sorting, Controls -->
<!-- node: browser/view-modes/sorting, Order -->
<!-- node: browser/view-modes/list, Headings -->

- **Columns and Icons:** click **Choose sort field** in the pane header and pick
  **Name**, **Size**, **Modified**, or **Type**. The arrow button beside it
  reverses the order.
- **List:** click the **Name**, **Size**, **Type**, or **Modified** heading to
  sort by it. Click it again to reverse.

Name sorting ignores case and reads numbers by value, so `File 2` comes before
`File 10`. **Folders first**, in the Columns and Icons sort menu, is on by
default and keeps folders ahead of files in both directions, in every view.

## Keep settings per folder

<!-- node: browser/view-modes/folder-views, Remembering values -->
<!-- node: browser/view-modes/folder-views, Settings -->
<!-- node: browser/view-modes/folder-views, Pane menus -->

Each local folder remembers the sort you choose in it and its Icons thumbnail
size. Remote shares, Trash, and Recent do not.
Sort `~/Downloads` by **Modified**, descending, and only `~/Downloads` changes,
even after a restart. Other folders keep the default.

Once a folder has its own sort, its sort menu in Columns or Icons offers
**Make this the default sort** and **Reset to default sort**. Once you move a
folder's thumbnail slider off the default, the popover offers **Make this the
default size** and **Reset to default size**.

Press Ctrl+, and open **General**. Under **BROWSING** you find:

- **Remember sort and icon size per folder**, on by default. Turn it off and the
  last sort you choose becomes the default for later folders.
- **Default sort**, a field and a direction, Name ascending at first.
- **Forget all folder settings**, whose **Clear** button returns every folder to
  the defaults.

## Change the text size

<!-- node: browser/view-modes/text-size, Changing the size -->
<!-- node: browser/view-modes/text-size, Applying the size -->

| Press | Effect |
| --- | --- |
| Ctrl++ or Ctrl+= | 1 px larger |
| Ctrl+− | 1 px smaller |
| Ctrl+0 | Back to 13 px |
| Ctrl+wheel | 1 px per notch |

The **Appearance** menu has the same buttons under **TEXT SIZE**; the middle
one shows the current size and resets it. To type a size from 8 to 48, use
**Text size** in **Settings → Appearance**. Every window follows at once.

## Good to know

<!-- node: browser/view-modes/position-restore, Returning to a folder -->
<!-- node: browser/view-modes/columns, Returning to an ancestor -->
<!-- node: browser/view-modes/list, Grouping -->
<!-- node: browser/view-modes/folder-views, Storage file -->
<!-- node: browser/view-modes/text-size, Applying the size -->

- In Icons and List, going back to a folder restores its selection and scroll
  position. In Columns, going back up selects the folder you came from.
- **Group by file type** in the **Appearance** menu groups List rows under
  headings such as Folder and JSON document. It works only in List.
- Per-folder values live in `~/.local/state/strata/folder-views.toml`, not in
  `settings.toml` or in the folders themselves.
- A subfolder does not inherit its parent's sort or size.
- Ctrl+wheel over a PDF preview zooms the PDF instead of the text. Text size
  never changes thumbnail size or preview zoom.

**Full detail:** [Returning to a visited directory](../reference/keyboard-navigation.md#returning-to-a-visited-directory)
in the Keyboard navigation reference.
