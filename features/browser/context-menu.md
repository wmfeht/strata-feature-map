---
title: Context menus
status: shipped
origin: {issue: lgse/strata#303, pr: lgse/strata#306}
branch: null
reviewed_at: 86df474dc0e8352e0e2098637a017cc4c77a8c44
review: draft
code: [src/ui/browser/context_menu.rs, src/ui/browser/context_menu/actions.rs, src/ui/browser/context_menu/commands.rs, src/ui/browser/context_menu/keyboard.rs, src/ui/browser/context_menu/presentation.rs]
tests: [src/ui/browser/context_menu/tests/menus.rs, src/ui/window/tests/keyboard_dispatch/context_menus.rs, src/ui/browser/context_menu/tests.rs, src/ui/browser/context_menu/tests/open_with.rs, tests/qa/scenarios/dialogs_and_menus/pane-menu-directory-actions.jsonl, tests/qa/scenarios/dialogs_and_menus/secondary-click-retargets-menu.jsonl, tests/qa/scenarios/dialogs_and_menus/submenu-arrows-return-to-parent.jsonl]
docs: [site/src/reference/keyboard-navigation.md]
related: [browser/selection, browser/search/filter, browser/tabs, integration/custom-actions, operations/clipboard/send-to, integration/portal-file-chooser, app/accessibility, browser/navigation/recent, integration/open-with, integration/open-with/terminal, operations/trash, operations/trash/restore, operations/delete]
---

## Summary

The item and background context menus in Columns, Icons, and List. This node covers opening them by pointer and keyboard, navigation, grouping, placement, and styling. The actions inside them belong to their own features.

## Behavior

### Opening

- Right-clicking an unselected entry makes it the only selected entry and the keyboard cursor. lgse/strata#666
- Right-clicking an entry inside a multi-selection keeps the whole selection. lgse/strata#666
- Menu alone or Shift+F10 opens the menu of the focused selected entry in Columns, Icons, and List. lgse/strata#666
- Ctrl+Shift+F10, Shift+Menu, and Ctrl+Menu open no menu. lgse/strata#666 (unverified)
- Menu or Shift+F10 with Hyper or Meta held opens the menu as without them. lgse/strata#1576
- With several entries selected, Menu or Shift+F10 opens the multi-selection menu and keeps the whole selection. lgse/strata#666
- With nothing selected, Menu or Shift+F10 opens the active pane's background menu. lgse/strata#666
- A keyboard-opened item menu anchors to the entry, not the pointer: its right edge in Columns and Icons, its center in List. lgse/strata#666 (unverified)
- On a focused Ctrl+F result, Menu or Shift+F10 opens that result's file menu; Properties targets its real location. lgse/strata#666
- While a text input has focus, Menu and Shift+F10 open the input's text-editing menu instead of a file menu. lgse/strata#666
- With a sidebar place, Trash, or drive row focused, Menu or Shift+F10 opens that row's menu, with 10xer mode on or off. lgse/strata#1331
- With a menu open, a secondary click on another entry closes it and opens that entry's menu in one click. lgse/strata#1155 (unverified)

### Pointer activation

- On niri, a right click held about 250 ms and released over the menu that opened leaves the menu open and runs no row. lgse/strata#1621
- A button release that reaches an item or background menu, or its submenus, before any press inside it is ignored. lgse/strata#1621
- After that, a full click on a menu row runs it. lgse/strata#1621
- Pressing the secondary button, moving onto a menu row, and releasing does not run the row; menu rows need a separate click. lgse/strata#1621
- On Hyprland, wlroots compositors, and X11, a right click released over a menu row behaves as before: the menu stays open. lgse/strata#1621
- On GTK 4.14, choosing Open With… from a file's menu and picking an application keeps the window open. lgse/strata#1642, lgse/strata#1695
- After that, the menu and the chooser open again. lgse/strata#1642, lgse/strata#1695

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
- A folder's menu adds Open in Terminal, then Open in…, to the opening group, and Pin to sidebar before Customize…. lgse/strata#1210, lgse/strata#1543
- Open in… is a submenu of New Tab, shown with Ctrl+Enter, and New Window, shown with Shift+Enter. A file's menu has no Open in…. lgse/strata#1543, lgse/strata#1576
- An archive's menu lists Extract here and Extract to… after the common opening actions. lgse/strata#1210
- A single file result's menu during a filter or search offers **Open file location**, which opens its folder with the file selected. lgse/strata#1041
- A file's menu in Trash never offers Open file location; elsewhere, with no filter or search, it offers it only for a file outside the shown folder. lgse/strata#1041 (unverified)
- The multi-selection menu groups Open With…; Cut, Copy, Duplicate; Move to…, Copy to…; Compress…; Copy paths, Copy names, Properties; then both deletions. lgse/strata#1210
- While the selection's types are looked up, the item and multi-selection menus show Open With… insensitive, described "Looking for compatible applications…". lgse/strata#578
- Outside Flatpak, when every selected item shares a default application, the multi-selection menu adds Open above Open With…. lgse/strata#1155, lgse/strata#1635
- Under Flatpak, once the selected types resolve, the multi-selection menu shows Open above Open With…, even with different or no defaults. lgse/strata#1635 (unverified)
- When the selection holds at least one folder, the multi-selection menu adds Open in… after Open With…. lgse/strata#1543
- Open in… → New Tab or New Window on a multi-selection opens one tab or window per selected folder and skips files. lgse/strata#1543 (unverified)
- The background menu groups New Folder, New File, Paste; Open With…, Open in Terminal; Select All, Refresh, the hidden-files toggle; then Customize…, Properties. lgse/strata#1210
- The background menu offers Open With… and Open in Terminal for the current folder, except in Trash and Recent. lgse/strata#821, lgse/strata#161, lgse/strata#1083
- In the background menu, Open in Terminal is insensitive when the folder has no local path. lgse/strata#161 (unverified)
- The item menu shows Open in Terminal for a single folder with a local path, outside Trash. lgse/strata#161
- In Recent, the background menu hides Open With…, Open in Terminal, and Properties. lgse/strata#1083 (unverified)
- In Recent, the item menu hides New Folder with Selection. lgse/strata#1083 (unverified)
- In Recent, the item menu offers Remove from Recent when every selected row has a recent-history entry. lgse/strata#1500
- Remove from Recent is absent from the same file's menu in its real folder. lgse/strata#1500
- In the background menu of a folder, Open With… stays insensitive, explained "Looking for compatible applications…", until the recent-apps history is read. lgse/strata#1729 (unverified)
- Custom actions sit in their own section after the open, print, and extract commands and before Cut and Copy. lgse/strata#1085
- Actions hidden for the current target leave no empty group or doubled separator. lgse/strata#1210
- Open With… shows AppWindow, Duplicate CopyPlus, Copy path(s) Route, Copy name(s) FileType, Move to… FolderInput, and Copy to… FolderOutput. lgse/strata#1210
- Compress… shows PackagePlus, Extract here PackageOpen, and Extract to… FolderArchive. lgse/strata#1210
- Permanently delete shows CircleX with a red label and icon; Move to Trash keeps the Trash icon. lgse/strata#1210
- Outside Trash, the item menu shows "Permanently delete" with a Shift+Del hint below Move to Trash, for single and multiple selections. lgse/strata#164
- The menu hides "Permanently delete" when `access::can-delete` reports false for the folder's contents, and shows it when the query is unresolved. lgse/strata#361
- In a folder without write permission, such as after `chmod 555`, neither Move to Trash nor Permanently delete appears in the item menu. lgse/strata#361
- Outside Trash, the item context menu hides Move to Trash when the folder's listing reports `access::can-trash` false, and shows it when the value is unknown. lgse/strata#314
- Trash menus omit Rename, Compress, New Folder, New File, and paste destinations. lgse/strata#499
- Top-level Trash items keep Restore, Cut, Move to…, Copy, and permanent deletion in their menus. lgse/strata#499
- Restore appears in the item menu only when every selected item is a top-level Trash item. lgse/strata#499
- Outside Trash, the item and multi-selection menus show "Delete without Trash" in place of Permanently delete when every selected item is remote, as `operations/trash` defines it. lgse/strata#1614
- Delete without Trash has the CircleX icon, a red label, and the Shift+Del hint. A mixed local and remote selection keeps Permanently delete. lgse/strata#1614
- An action with a shortcut shows it at the row's right, such as Ctrl+C beside Copy. lgse/strata#666
- Shortcut hints use one notation: Enter beside Open, "F2 / Ctrl+R" beside Rename, and Alt+Enter beside Properties. lgse/strata#1576
- With the interface in German, hints read Strg+C beside Copy and Entf beside Move to Trash. lgse/strata#1576
- In 10xer mode, hints read lowercase `x`, `y`, and `d` beside Cut, Copy, and Move to Trash, and `D` beside Permanently delete. lgse/strata#1576
- Screen readers get each row's label as its name and its shortcut as its description. lgse/strata#415 (unverified)

### Placement

- Right-clicking an entry anywhere in a long, scrolled list shows its menu at the click. lgse/strata#306, lgse/strata#1894
- In a small window, right-clicking an entry near the bottom edge opens the menu at the click. lgse/strata#1893, lgse/strata#1894
- That menu extends past the window when needed and stays fully on screen. lgse/strata#1893, lgse/strata#1894
- A menu opens below the click, and flips above it when the screen has no room below. lgse/strata#1893, lgse/strata#1894
- A menu with no room on screen above or below the click shrinks and scrolls instead of moving away from the click. lgse/strata#1893, lgse/strata#1894
- A menu opened near the screen's left or right edge slides horizontally to stay on screen. lgse/strata#1893, lgse/strata#1894
- A menu's height is capped at the monitor height less 16 px at each edge; a taller menu scrolls. lgse/strata#1894 (unverified)
- A keyboard-opened background menu is not held inside the window; like a pointer-opened menu, it may extend past it. lgse/strata#1894 (unverified)
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
- Popovers parented to list views vanished for rows mid-list, so menus live in the window overlay (lgse/strata#303, lgse/strata#306).
- Menus are `xdg_popup`s, so Strata anchors them at the click, requests placement below, and caps their height at the monitor. Clamping to the window squeezed or displaced menus in small windows (lgse/strata#1893, lgse/strata#1894).
- GTK and the compositor flip, slide, or shrink the popup to keep it on screen. That covers the mid-list case, so measuring and shifting the anchor (lgse/strata#702) was dropped (lgse/strata#1894).
- Open stays a top-level row and Open in… holds only New Tab and New Window, so the submenu header performs no action. Flat rows were rejected for a compact submenu (lgse/strata#1540, lgse/strata#1543).
- Grouping follows Open, Edit, Transfer, Transform, Organize/Inspect, Destructive, without visible headings to save height. Compress stays a singleton group rather than join an unrelated one (lgse/strata#1207).
- Icons are secondary cues; labels carry meaning. CircleX gives irreversible deletion a distinct shape, not only a color (lgse/strata#1207).
- GTK's text-input menus never receive Strata's classes, so `text > popover.menu` and `textview > popover.menu` selectors style them (lgse/strata#456, lgse/strata#1087).
- Strata adds and removes the Open in… submenu row itself, alone in a nested section that draws no separator. Hiding it with `hidden-when` freed its submenu's trackers while GTK iterated them during teardown, logging GLib-CRITICALs. Clearing the menu model before unparenting was rejected: GTK's rebuild takes the same path (lgse/strata#1569, lgse/strata#1611). A later attempt to clear it on every close still crashed on GTK 4.14 (lgse/strata#1695).
- A quick right click can open the menu under the pointer, and GtkModelButton activates on an unpaired release of any button. Some compositors, such as niri, deliver the opening click's release to the popup (lgse/strata#1618).
- A release with no press inside the menu since `show()` belongs to the opening click and is dropped. The flag resets per presentation, so nothing stays armed on compositors that never deliver that release. A guard armed at the trigger was rejected for that reason; it also covered only the secondary button (lgse/strata#1618, lgse/strata#1621).
- The guard runs with no propagation limit because submenus are separate popover natives (lgse/strata#1621).
- GTK 4.12 to 4.16 leave a position handler on a freed section box when a popover's model is replaced. The item menu therefore starts with no model (lgse/strata#1642, lgse/strata#1695).
- GTK 4.14 can keep the window's pointer focus on a hidden popover. A sensitivity toggle therefore repicks pointer focus before unparenting (lgse/strata#1642, lgse/strata#1695).
- Both workarounds are needed on GTK 4.14; GTK 4.22 fixed both bugs (lgse/strata#1695).
- A dropped menu owner unparents its popover, and preference bindings hold weak references, so navigation releases retired menus (lgse/strata#1353).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-25 | lgse/strata#1894 | fix | Anchored menus at the click and capped their height to the monitor, so they extend past a small window instead of being squeezed or shifted. |
| 2026-10-16 | lgse/strata#1695 | fix | Built the item menu without a model and repicked pointer focus before unparenting, so menu actions no longer crash on GTK 4.14. |
| 2026-10-15 | lgse/strata#1611 | fix | Added and removed the Open in… row in its own nested section, so item-menu teardown no longer logs GLib-CRITICALs. |
| 2026-10-15 | lgse/strata#1621 | fix | Dropped a menu button release that arrives before any press, so a quick right click on niri no longer runs the row under the pointer. |
| 2026-10-10 | lgse/strata#1554 | fix | Looked up only the mapped Columns row when focusing a search result for its menu after a reload. |
| 2026-10-10 | lgse/strata#1539 | fix | Made Columns Open on an open folder focus and reveal its column instead of closing it. |
| 2026-10-02 | lgse/strata#1353 | fix | Released retired panes' context menus and their preference bindings after navigation. |
| 2026-09-25 | lgse/strata#1210 | feat | Grouped menu actions by intent and gave distinct actions distinct Lucide icons. |
| 2026-09-17 | lgse/strata#1087 | fix | Styled text-input menus like file menus across GTK versions and themes. |
| 2026-09-12 | lgse/strata#666 | feat | Opened menus with Menu and Shift+F10 and made every menu keyboard navigable. |
| 2026-09-06 | lgse/strata#459 | feat | Restyled right-click menus as frameless themed popovers without the dark outer frame. |
| 2026-09-05 | lgse/strata#306 | fix | Moved item menus into the window overlay and capped their height so mid-list menus stay visible. |

## Known gaps

- On GTK 4.14, Left in a submenu does not return keyboard control to the parent menu as it does on GTK 4.22. lgse/strata#1695
