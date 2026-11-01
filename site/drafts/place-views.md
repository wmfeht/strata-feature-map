---
proposed: {page: new}
nodes: [browser/view-modes/density, browser/view-modes/list/column-layout, browser/view-modes/thumbnail-size, browser/selection/marquee, operations/drag-and-drop/column-autoscroll]
reason: 'Content density, List column order and visibility, thumbnail size shortcuts, marquee selection, and Columns drag autoscroll are user-visible, and no reference page names their nodes. The Frame slider already lives in reference/themes.md "### Frame density", so this draft''s Density section links there for what Frame changes and adds only the controls, presets, and saved keys that page lacks. The Views guide covers the thumbnail keys, the Columns button, and both density sliders at guide level, but by rule shows only the common path and at most five tips. A reference page has to hold the detail. Proposed as a "Views reference" page with one `##` section per heading below, linked from the guide.'
release: v1.1.1
---

Raw material for a "Views reference" page. Upstream describes the first three
in docs/preferences.md ("Content and Frame density", "Per-folder sort and
thumbnail size").

## Density

The **Appearance** menu's **DENSITY** section has two sliders. **Frame** sets
the inset of the window's bars, as described under
[Frame density](themes.md#frame-density). **Content** sets the spacing of rows
and Icons cards. Changing one leaves the other alone.

| Slider | Range | Compact | Airy |
| --- | --- | --- | --- |
| Frame | 0–12 px | 0 px, the default | 4 px |
| Content | 0–16 px | 4 px, the default | 8 px |

Each slider has tick marks and **Compact** and **Airy** buttons under its preset
values; clicking one snaps to it. The value label reads "Compact · N px" or
"Airy · N px" on a preset, otherwise "Custom · N px". Dragging or clicking leaves
the menu open, and a change shows in every window at once. **Left** and **Right**
step a focused slider by 1 px, **Page Up** and **Page Down** by 4 px. The wheel
scrolls the menu, not the slider.

Each change is saved at once in `settings.toml` as `frame_density` and
`browser_density`, each `"compact"`, `"airy"`, or `"custom"`, with
`frame_density_custom_px` and `browser_density_custom_px` read only for
`"custom"`. A slider resting on a preset saves the preset: Content at 4 px saves
`browser_density = "compact"`. A custom value above the maximum loads clamped, and
an unknown mode loads as Compact. A file with only `browser_density` loads Frame at
Compact.

## List columns

A List pane header has a **Columns** button. Its popover, headed **COLUMNS**,
lists **Name**, **Mode**, **Size**, **Type** and **Modified** with check marks,
then **Reset to default columns**. Right-clicking the List headings opens the
same popover at the pointer. In List, **Appearance → Customize columns…** opens it
on the headings. The button is hidden in 10xer mode.

- Unchecking **Mode**, **Size**, **Type** or **Modified** hides that column;
  checking it shows it again. **Name** cannot be hidden.
- Drag a heading sideways to move its column. After 10 px of movement the cursor
  grabs and a 3 px accent line marks the drop point; the columns move when you
  release over the headings. Releasing outside the heading row, or cancelling,
  changes nothing. A shorter press stays a sort click, and a press within 8 px of
  a heading's right edge resizes the column.
- **Reset to default columns** restores Name, Mode, Size, Type, Modified, all
  shown.
- Hiding, showing, moving, or resetting columns never changes the sort. A hidden
  sort column stays the active sort; showing it again restores its arrow.
- Every browser window and the system file chooser share the order and
  visibility, and update live. Column widths stay separate for the browser and
  the chooser.
- The order is saved as `list_column_order`, such as `["name", "mode", "size",
  "type", "modified"]`, and hidden columns as `list_hidden_columns`. On load,
  duplicates are dropped and missing columns appended in default order. Reset
  removes both keys.

## Thumbnail size shortcuts

In Icons, these keys step the thumbnail size through 32, 36, 40, 44, 48, 56, 64,
72, 80, 96, 112, 128, 144, 160, 192, 224 and 256 px:

| Input | Effect |
| --- | --- |
| **Ctrl+Alt++** or **Ctrl+Alt+=** | One step larger |
| **Ctrl+Alt+−** | One step smaller |
| **Ctrl+Shift+wheel** | One step per notch |
| **Ctrl+Alt+0** | Reset |
| **+**, **=**, **−** (10xer mode, Icons listing focused) | Step larger or smaller |

From a size between steps, such as 100 px, one step goes to 112 or 96. The size
stops at 32 and 256 px. The keys resize nothing in Columns or List. The system
file chooser accepts the keys but not the wheel.

Each step moves the **Thumbnail size** slider, so it is saved exactly as dragging
the slider saves it: with per-folder sizes on, for the folder; otherwise as the
default. **Ctrl+Alt+0** clears a folder's own size so it follows the default
again; in a folder that is not remembered, such as a remote share, it sets the
slider to the default; with per-folder sizes off it returns the size to 64 px.
Each step or reset shows "Thumbnail size: Npx" in the progress dock for 1.2 s.

## Marquee selection

Drag from blank space to draw a band that selects every entry it crosses, in
Columns, Icons and List.

- The drag may also start on blank sidebar space below the last place, in a pane
  header, on List's heading strip, beside the last column, or on blank preview
  space. It then selects in the nearest pane, or in recursive search results when
  they show.
- Holding **Alt** starts a marquee even on an entry.
- Buttons, text fields, labels, images, sliders, scrollbars and sidebar places
  keep their own behavior, as does a disabled control.
- A plain marquee replaces the selection; **Ctrl** toggles crossed entries and
  **Shift** adds them.
- Holding the pointer near the edge scrolls the listing and extends the
  selection. Wheel scrolling during the drag extends it without moving the
  anchor.
- A marquee never opens or retargets quick preview, and works on **Ctrl+F**
  results. During a marquee started from the sidebar, the target pane takes
  keyboard focus, so **Ctrl+C** copies the marqueed files.
- A plain click on blank preview space keeps the selection while the preview
  shows something. In Columns, a click in the empty reserved preview slot clears
  it.

## Dragging files across columns

While a file drag is held within 44 px of the column strip's left or right edge,
the columns scroll toward that edge; within 44 px of a listing's top or bottom,
that listing scrolls. Scrolling starts slowly and speeds up over 350 ms. The
column under the drag shows an accent wash and ring, including one just revealed
by scrolling. Dropping on a partly visible column moves the files there, and the
strip does not scroll back to the source column.
