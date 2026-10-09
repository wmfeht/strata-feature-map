---
title: Context menus
status: shipped
origin: {issue: lgse/strata#303, pr: lgse/strata#306}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: reviewed
code: [src/ui/browser/context_menu.rs, src/ui/browser/context_menu/**]
tests: [src/ui/browser/context_menu/tests/menus.rs, src/ui/window/tests/keyboard_dispatch/context_menus.rs]
docs: [docs/keyboard-navigation.md]
related: [browser/selection, integration/custom-actions, operations/clipboard/send-to, integration/portal-file-chooser, app/accessibility]
---

## Summary

The item and background context menus in Columns, Icons, and List. This node covers opening them by pointer and keyboard, navigation, grouping, placement, and styling. The actions inside them belong to their own features.

## Behavior

### Opening

- Menu alone or Shift+F10 opens the menu of the focused selected entry in Columns, Icons, and List. lgse/strata#666
- Ctrl+Shift+F10, Shift+Menu, and Ctrl+Menu open no menu. lgse/strata#666 (unverified)
- With several entries selected, Menu or Shift+F10 opens the multi-selection menu and keeps the whole selection. lgse/strata#666
- With nothing selected, Menu or Shift+F10 opens the active pane's background menu. lgse/strata#666
- A keyboard-opened item menu anchors to the entry, not the pointer: its right edge in Columns and Icons, its center in List. lgse/strata#666 (unverified)
- On a focused Ctrl+F result, Menu or Shift+F10 opens that result's file menu; Properties targets its real location. lgse/strata#666
- While a text input has focus, Menu and Shift+F10 open the input's text-editing menu instead of a file menu. lgse/strata#666
- With a sidebar place, Trash, or drive row focused, Menu or Shift+F10 opens that row's menu, with 10xer mode on or off. lgse/strata#1331
- With a menu open, a secondary click on another entry closes it and opens that entry's menu in one click. lgse/strata#1155 (unverified)

### Keyboard navigation

- A menu opens with keyboard focus on its first visible action; focus stays there while Open With lookup finishes, even with the pointer resting over the menu. lgse/strata#1155
- Up and Down move between enabled actions, skipping separators and wrapping at either end; Home and End jump to the first and last action. lgse/strata#666
- Enter or Space activates the focused action and closes the menu. lgse/strata#666
- Escape closes the menu, keeps the selection, and returns focus to the entry or pane that opened it. lgse/strata#666
- Ctrl+A while a menu is open leaves the menu open. lgse/strata#666 (unverified)
- On a submenu row such as Actions or Send to…, Right, Space, or Enter opens the submenu with its first action focused. lgse/strata#1155
- Left in a submenu closes only the submenu and refocuses its row; Up and Down then move within the parent menu. lgse/strata#1155
- In the file chooser's menus, Up, Down, Tab, and Shift+Tab move between enabled actions and wrap at either end. lgse/strata#666

### Contents and grouping

- A single item's menu opens with a header showing its name and compact path, middle-ellipsized at 30 characters. lgse/strata#1143 (unverified)
- A multi-selection header reads "N items selected" above the first three names, followed by ", …" when there are more, cut to 30 characters. lgse/strata#1143 (unverified)
- When shown, New Folder with Selection sits alone at the top of the item and multi-selection menus, above the opening group. lgse/strata#1349
- A regular file's menu groups Open, Open With…, Quick preview, Print; then Cut, Copy, Duplicate, Rename; then Move to…, Copy to…. lgse/strata#1210
- After those come Compress… alone; then Customize…, Copy path, Copy name, Properties; then Move to Trash and Permanently delete. lgse/strata#1210
- A folder's menu adds Open in Terminal to the opening group and Pin to sidebar before Customize…. lgse/strata#1210
- An archive's menu lists Extract here and Extract to… after the common opening actions. lgse/strata#1210
- The multi-selection menu groups Open With…; Cut, Copy, Duplicate; Move to…, Copy to…; Compress…; Copy paths, Copy names, Properties; then both deletions. lgse/strata#1210
- When every selected item shares a default application, the multi-selection menu adds Open above Open With…. lgse/strata#1155
- The background menu groups New Folder, New File, Paste; Open With…, Open in Terminal; Select All, Refresh, the hidden-files toggle; then Customize…, Properties. lgse/strata#1210
- Custom action rows appear after the opening group and before Cut. lgse/strata#1085 (unverified)
- Actions hidden for the current target leave no empty group or doubled separator. lgse/strata#1210
- Open With… shows AppWindow, Duplicate CopyPlus, Copy path(s) Route, Copy name(s) FileType, Move to… FolderInput, and Copy to… FolderOutput. lgse/strata#1210
- Compress… shows PackagePlus, Extract here PackageOpen, and Extract to… FolderArchive. lgse/strata#1210
- Permanently delete shows CircleX with a red label and icon; Move to Trash keeps the Trash icon. lgse/strata#1210
- An action with a shortcut shows it at the row's right, such as Ctrl+C beside Copy. lgse/strata#666
- Screen readers get each row's label as its name and its shortcut as its description. lgse/strata#415 (unverified)

### Placement

- Right-clicking an entry anywhere in a long, scrolled list shows a menu that fits inside the window. lgse/strata#306
- A menu opens below the click when there is at least as much room below as above, otherwise above it. lgse/strata#306
- A menu taller than the room on its side shifts toward the other side instead of scrolling. lgse/strata#702
- A menu scrolls only when it is taller than the window less 16 px at each edge. lgse/strata#702
- A keyboard-opened background menu stays inside the window. lgse/strata#1155
- In Columns, the entries targeted by an open menu stay highlighted as selected while the column lacks focus. lgse/strata#616

### Appearance

- Menu rows are frameless on the theme surface, framed by a 1 px border, 9 px corners, and an accent glow, with no dark outer frame. lgse/strata#459
- Right-click menus in text inputs use the same surface, border, corners, font, and separators as file menus, and follow live theme changes. lgse/strata#1087
- Text-input menu styling covers the filter and search fields, location entry, inline rename, dialog fields, settings fields, and text previews. lgse/strata#1087

## Design

Context menus predate the PR history. lgse/strata#398 moved them out of `src/ui/browser.rs` into `src/ui/browser/context_menu.rs`. [docs/keyboard-navigation.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/keyboard-navigation.md) describes the keyboard route to filter results.

- Item and background menus are declared as Strata button rows and mirrored into a native `GtkPopoverMenu` model. Each row becomes an action enabled by the button's sensitivity and removed when the row is hidden; separators become sections (lgse/strata#1085).
- lgse/strata#456 rejected `GtkPopoverMenu` because it would drop icons, shortcuts, and the header. Native menus arrived with custom action submenus (lgse/strata#1085), so Strata reapplies icons, descriptions, the header, and danger styling to generated rows.
- The file chooser and app search results keep an overlay `gtk::Popover` with Strata's own key handling (lgse/strata#666).
- Menu and Shift+F10 follow platform convention, Shift+F10 covering keyboards without a Menu key. Dedicated shortcuts per action were rejected: extension actions would stay undiscoverable (lgse/strata#583).
- Keyboard menus anchor to the focused entry because the pointer may be elsewhere or absent (lgse/strata#583).
- A popup appearing under a stationary pointer is not pointer movement. The keyboard keeps ownership until the pointer actually moves, so a resting pointer cannot steal initial focus (lgse/strata#1155).
- Focusing a submenu's owner row alone left arrows routed to the hidden branch. Left therefore hides the submenu and clears GTK's open-submenu state (lgse/strata#1155).
- Popovers parented to list views vanished for rows mid-list, so menus live in the window overlay (lgse/strata#303, lgse/strata#306). GTK never shifts a popover's anchor, so Strata measures the menu and shifts it (lgse/strata#702).
- Grouping follows Open, Edit, Transfer, Transform, Organize/Inspect, Destructive, without visible headings to save height. Compress stays a singleton group rather than join an unrelated one (lgse/strata#1207).
- Icons are secondary cues; labels carry meaning. CircleX gives irreversible deletion a distinct shape, not only a color (lgse/strata#1207).
- GTK's text-input menus never receive Strata's classes, so `text > popover.menu` and `textview > popover.menu` selectors style them (lgse/strata#456, lgse/strata#1087).
- A dropped menu owner unparents its popover, and preference bindings hold weak references, so navigation releases retired menus (lgse/strata#1353).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-02 | lgse/strata#1353 | fix | Released retired panes' context menus and their preference bindings after navigation. |
| 2026-09-25 | lgse/strata#1210 | feat | Grouped menu actions by intent and gave distinct actions distinct Lucide icons. |
| 2026-09-17 | lgse/strata#1087 | fix | Styled text-input menus like file menus across GTK versions and themes. |
| 2026-09-12 | lgse/strata#666 | feat | Opened menus with Menu and Shift+F10 and made every menu keyboard navigable. |
| 2026-09-06 | lgse/strata#459 | feat | Restyled right-click menus as frameless themed popovers without the dark outer frame. |
| 2026-09-05 | lgse/strata#306 | fix | Moved item menus into the window overlay and capped their height so mid-list menus stay visible. |

## Known gaps

None known.
