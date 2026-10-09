---
title: Folder and file customization
status: shipped
origin: {issue: lgse/strata#211, pr: lgse/strata#294}
branch: null
reviewed_at: aee71335dfecd059b9af23efeac2ed52c43e3b19
review: draft
code: [src/ui/browser/customization.rs]
tests: [src/model/tests.rs]
docs: [docs/preferences.md]
related: [browser/sidebar, browser/thumbnails, browser/properties, settings/themes/icons, settings/preferences/storage, operations/rename, browser/context-menu]
---

## Summary

Per-item colors and icons for local folders and files, chosen in the Customize dialog and saved in `settings.toml`. Customized icons replace the default icon wherever Strata draws that path. Sidebar rows and their Customize… action belong to `browser/sidebar`.

## Behavior

### Opening Customize

- Right-clicking one local file or folder outside Trash offers Customize…, which opens "Customize Folder" or "Customize File" with the item's name as subtitle. lgse/strata#294
- The item menu hides Customize… for multiple selections, Trash items, and locations without a native path. lgse/strata#294 (unverified)
- Right-clicking the background of a folder in Icons, List, or Columns offers Customize… for the folder that pane shows. lgse/strata#754
- In Columns, Customize… from the background of a non-active ancestor column customizes that ancestor, not the active descendant. lgse/strata#754
- The background menu omits Customize… in Trash, Recent, and locations without a native path. lgse/strata#754 (unverified)
- Customize opens with focus on Done, so one Escape closes it. lgse/strata#1433, lgse/strata#1533
- Closing Customize returns focus to the control that opened it. lgse/strata#1433, lgse/strata#1533
- With the emoji picker open, Escape closes only the picker; a second Escape closes Customize. lgse/strata#1433, lgse/strata#1533

### Choosing a color

- The COLOR row offers a "Default (Theme color)" button, seven presets (Red, Orange, Yellow, Green, Blue, Purple, Gray), and a "Custom color…" button. lgse/strata#294
- Clicking a preset applies it at once and checks it; clicking the checked preset or the Theme button removes the saved color. lgse/strata#294
- The custom-color button opens "Custom Folder Color" or "Custom File Color" with a color chooser that recolors the dialog's header icon live. lgse/strata#294
- Apply saves the chosen color as `#rrggbb`; the custom button then shows that color with a check and the tooltip "Custom (#rrggbb)". lgse/strata#294 (unverified)
- In the custom color dialog, Escape from the editor returns to the palette, and Escape from the palette closes the dialog without applying. lgse/strata#294 (unverified)
- Closing the custom color dialog by Apply, Cancel, Escape, or a click outside it returns focus to the custom color button. lgse/strata#1433, lgse/strata#1533
- The custom color button's accessible name follows its tooltip: "Custom color…" or "Custom (#rrggbb)". lgse/strata#1433, lgse/strata#1533

### Choosing an icon

- The ICON grid offers 16 bundled icons: Documents, Downloads, Code, Archive, Pictures, Videos, Terminal, Home, Storage, Network, Computer, Private, Pinned, Media, Settings, and Tasks. lgse/strata#294
- Choose Emoji… opens an emoji picker; the picked emoji becomes the item's icon and the button reads "Emoji" followed by it. lgse/strata#294
- Each choice updates the dialog's 56 px preview and the item's icons immediately; Done only closes the dialog. lgse/strata#294
- Clear starts disabled for an uncustomized item and becomes enabled after any color or icon choice. lgse/strata#294 (unverified)
- Clear removes both the saved color and icon and restores the default icon. lgse/strata#294

### Rendering

- A folder with a custom icon or emoji shows it as a badge on a filled folder, in the saved color or the theme accent. lgse/strata#294
- A file with a custom icon shows that icon in the saved color or the theme accent; a file with an emoji shows the emoji alone. lgse/strata#294 (unverified)
- An item with a color and no custom icon shows its default icon in that color. lgse/strata#294
- Customized icons appear in Columns, List, Icons, search result rows, and the Properties header. lgse/strata#294
- Changing a customization redraws every visible icon for that path without reloading the folder. lgse/strata#294
- Changing the theme redraws customized icons that have no saved color in the new accent. lgse/strata#294

### Storage

- Customizations persist across restarts in `settings.toml`, under `[folder_colors]` and `[custom_icons]`, keyed by absolute path. lgse/strata#294
- Colors are saved as a lowercase preset name or a hex value; icons as a bundled icon name or `emoji:` followed by the emoji. lgse/strata#294 (unverified)
- A saved icon that is not one of the 16 choices, or an emoji over 64 bytes or containing control characters, is ignored. lgse/strata#294 (unverified)

## Design

The request was Finder's folder labels (lgse/strata#211). Folders follow the theme accent by default, and a color is an explicit per-path override, so uncolored folders keep tracking theme changes (lgse/strata#294).

- The first version put a color bar in the item menu and the Properties dialog. Before merge it became one Customize dialog, with color and icon together and no controls left in Properties (lgse/strata#294).
- Choices apply as they are picked, with a live preview. The dialog has Clear and Done but no Cancel; Clear is the way back (lgse/strata#294).
- Folders render a chosen icon as a badge over the colored folder, so a customized folder still reads as a folder. Files take the icon itself (lgse/strata#294).
- Icon names are checked against the 16-icon whitelist and emoji are length- and character-bounded on read and write. A hand-edited `settings.toml` therefore cannot name arbitrary icon resources (lgse/strata#294) (unverified).
- Rendered icons register their path. A change refreshes only the icons for that path. When the path now has a custom icon, pending thumbnail work is cancelled, so a late thumbnail cannot overwrite it (lgse/strata#294). Thumbnail suppression for custom icons is described in `browser/thumbnails`.
- Customize opens on Done rather than the layer or a swatch, so Enter does something useful. Edits apply at once, so Done is safe (lgse/strata#1433).
- The custom color dialog restores focus itself, because the shared restore waits for the last open dialog to close (lgse/strata#1433).
- The background menu reuses the item dialog. In Columns it targets the location of the pane that was clicked, since several columns are visible at once (lgse/strata#746, lgse/strata#754).
- Storage is keyed by the item's path string. Nothing rebases keys when Strata renames, moves, or deletes the item (lgse/strata#1452).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-09 | lgse/strata#1533 | fix | Opened Customize with focus on Done and returned focus to the opener when it and its color dialog close. |
| 2026-09-10 | lgse/strata#754 | feat | Added Customize… to folder-background menus, targeting the clicked column's folder in Columns. |
| 2026-09-04 | lgse/strata#294 | feat | Added per-item colors, bundled and emoji icons, and the Customize dialog, saved in `settings.toml`. |

## Known gaps

- Renaming or moving a customized item in Strata drops its customization, and a new item created at the old path inherits it; the fix is unmerged. lgse/strata#1452, lgse/strata#1546
- Keys are lossy UTF-8 paths, so non-UTF-8 names that decode to the same text share one customization. lgse/strata#1452
