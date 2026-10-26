---
title: Accessibility
status: shipped
origin: {issue: lgse/strata#341, pr: lgse/strata#415}
branch: null
reviewed_at: be3343a5992a2a5497b1a2ee7faa525be18e988f
review: draft
code: [src/ui/accessibility.rs]
tests: [src/ui/accessibility/tests.rs, tests/qa/scenarios/accessibility]
docs: [docs/testing.md]
related: [browser/navigation/location-bar, browser/sidebar, settings/preferences/language, browser/context-menu, app/dialogs]
---

## Summary

App-wide accessible semantics for screen readers and AT-SPI automation. It covers the names, descriptions, roles, and states of panes, entry lists, entries, menus, and dialogs. It also owns the rule that limits tooltips to icon-only buttons. Accessible labels specific to one feature stay with that feature.

## Behavior

### Browser listing

- In every view, each entry is named with its display name and described as "Folder" or "File". lgse/strata#415
- A symbolic link is described as "Folder link" or "File link", a dangling link as "Broken link", and any other file type as "Other". lgse/strata#415 (unverified)
- Each pane is a group named after its directory and described as "Columns view", "Icons view", or "List view". lgse/strata#415
- The entry list inside a pane is named after its directory and described as "Files". lgse/strata#415
- In an empty, unreadable, or still-loading directory, the focusable pane is named after the directory. lgse/strata#1533
- That focused pane is described as "This directory is empty", the error text, or "Loading", matching what it shows. lgse/strata#1533
- Entries are focusable, and selecting one sets the `selected` state on that entry and on no other. lgse/strata#415
- View, entry kind, list, and "Loading" pane descriptions are shown in the interface language. lgse/strata#1519, lgse/strata#1533 (unverified)

### Chrome, menus, and dialogs

- With default preferences, the window exposes buttons named "Search (Ctrl+K)", "Appearance", "Settings", "Close window", and "Toggle sidebar (Ctrl+B)". lgse/strata#415
- Pressing Tab repeatedly from the window's first control reaches the file listing. lgse/strata#415
- Items in the file, folder, and sidebar right-click menus have the menu item role and are named after the action. lgse/strata#415
- A right-click menu item with a keyboard shortcut carries the shortcut in its accessible description, not its name. lgse/strata#415
- Menu shortcut descriptions use Strata's notation: the Appearance menu's Hidden files option is described as "Ctrl+H", not "Ctrl + H". lgse/strata#1576
- Accessible names and descriptions that name a shortcut use the interface language's key names, such as "Strg" in German. lgse/strata#1576
- Strata's modal dialogs have the dialog role and are named after their title. lgse/strata#415

### Button names

- In List and Icons, the pane header's buttons are named "Back (Alt+←)", "Forward (Alt+→)", and "Parent folder (Alt+↑)". lgse/strata#1895
- The path bar's copy button is named "Copy path"; after a click it is named "Path copied", then "Copy path" again 2 s later. lgse/strata#1895
- The List view's Columns menu button is named "Columns". lgse/strata#1895
- In Customize Folder, the default color swatch is named "Default (Theme color)" and the custom-color view's back button "Back to palette". lgse/strata#1895
- An install command's copy button is named "Copy install command", then "Install command copied" for 2 s after a click. lgse/strata#1895 (unverified)
- The media preview's play button is named "Play/Pause (<shortcut>)" and its mute button "Mute/unmute (<shortcut>)". lgse/strata#1895 (unverified)
- Inside an archive preview's subfolder, the up button is named "Go up one level". lgse/strata#1895 (unverified)
- The file chooser's header close button is named "Cancel file selection (Escape)". lgse/strata#1895 (unverified)
- The Settings theme search's clear button is named "Clear search". lgse/strata#1895 (unverified)
- A sidebar drive's release button is named "Eject" or "Unmount", and an encrypted drive's button "Unlock" or "Lock". lgse/strata#1895 (unverified)

### Field names

- The Ctrl+F filter field is named after its toggle: "Filter this pane (Ctrl+F)" in Columns and "Filter icons (Ctrl+F)" in Icons. lgse/strata#810, lgse/strata#1896
- In List, the filter field is named "Filter list (Ctrl+F)". lgse/strata#1896 (unverified)
- The Ctrl+K search palette field is named "Search files and folders…", and the F1 reference's search field "Search actions or keys…". lgse/strata#1896
- Connect to server's address field is named "Server address". lgse/strata#1896
- Compress's fields are named "Archive name" and, with password protection on, "Password" and "Confirm password". lgse/strata#1896
- The Icons Thumbnail size slider is named "Thumbnail size". lgse/strata#1896
- The mount sign-in dialog's username, domain, and password fields are named after their visible labels. lgse/strata#1896 (unverified)
- A 10xer footer prompt's entry is named after the prompt label it shows, and the name changes with each prompt. lgse/strata#1896 (unverified)
- Open With's search field is named "Search applications…". lgse/strata#1896 (unverified)
- The file chooser's Save and URL name fields are named "Name". lgse/strata#1896 (unverified)
- The theme editor's name field is named "Theme name", and each color picker after its row label. lgse/strata#1896 (unverified)
- The drive Label dialog's field is named "Label shown in Strata", and Format Drive's label field "Filesystem label". lgse/strata#1896 (unverified)

### Tooltips

- Hovering a labelled button, menu item, label, entry, file row, breadcrumb, or status indicator shows no tooltip. The one exception is a truncated name on an Icons-view card (`browser/view-modes/icons`). lgse/strata#1359, lgse/strata#1553
- Hovering an icon-only button shows its tooltip, such as "Search (Ctrl+K)" on the header Search button. lgse/strata#1359
- In the collapsed sidebar rail, each row shows its name as a tooltip; expanding the sidebar removes those tooltips. lgse/strata#1359
- Text that tooltips carried before, such as a sidebar place's or breadcrumb's full path, is now the control's accessible description. lgse/strata#1359

## Design

[docs/testing.md](https://github.com/lgse/strata/blob/c94eeb0020fa1154e11c741888f1b56d92ce70d6/docs/testing.md) ("Accessible names are product surface") states the contract this node owns.

- GUI tests locate controls only by accessible role and name. When one cannot identify a control, the fix is to name it in the application, never a test-only API (lgse/strata#341).
- QA scenarios read those names, descriptions, and states from the app's own widget tree, not AT-SPI. GTK has no public getter for accessible labels, relations, or states. In `qa` builds this node's naming helpers therefore record what they set for the QA reader (lgse/strata#1771).
- A feature's own label always wins over a stand-in label, such as the icon rail's row name (lgse/strata#1771).
- An entry's name and description sit on the list item, not the row content, because the item carries the `list item` or `table cell` role and the selected and focused states (lgse/strata#415).
- Panes use the group role because GTK drops a label set on a plain `GtkBox`, whose generic role ARIA forbids naming (lgse/strata#415).
- The pane, not the entry list, carries the directory and view, because an empty directory replaces the list with a placeholder (lgse/strata#415).
- The focusable pane of an empty, unreadable, or loading directory carries the directory as its name and the shown status as its description (lgse/strata#1466).
- Menu accelerators go in the description so the shortcut text is not read as part of the item's name (lgse/strata#415).
- Tooltips are not a reliable name source. One field exposed its tooltip as its name (lgse/strata#811), while tooltip-only location controls had no name (lgse/strata#1131). Controls get explicit names instead (lgse/strata#1132).
- An icon-only button sets its tooltip and accessible name in one call, so a tooltip that changes, such as "Path copied", keeps the name in step (lgse/strata#1895).
- A field under a visible label is linked to it, so its name follows the label. A field without one takes text it already shows, so no catalog strings were added (lgse/strata#1896).
- A hover delay was requested for tooltips that covered folders (lgse/strata#1337). The owner instead removed tooltips from everything but icon-only buttons, since a delay does not remove redundant text (lgse/strata#1358).
- The tooltip rule lives in the upstream `AGENTS.md`. Switchable controls show tooltips only in icon-only mode, help, errors, and status stay visible, and tooltip text is never data (lgse/strata#1359).
- lgse/strata#1359 also moved names and descriptions that E2E checks read from tooltips into explicit accessible metadata (lgse/strata#1337).
- Exclusive choices are radio menu items and on/off options are check menu items, because screen readers announce their checked state (lgse/strata#1467, lgse/strata#1544).
- Chosen states are product surface too: GUI checks read `checked` or `pressed` as accessible state and never infer them from check-icon children (lgse/strata#1544).
- A menu option's `checked` state mirrors its check icon's own visibility, because a closed popover hides every option's ancestors (lgse/strata#1544, unverified).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-25 | lgse/strata#1896 | fix | Named text fields and the Icons thumbnail slider that had only a placeholder or an unlinked label. |
| 2026-10-25 | lgse/strata#1895 | fix | Gave icon-only buttons that had only a tooltip an accessible name equal to it, kept in step when it changes. |
| 2026-10-10 | lgse/strata#1544 | fix | Added checked and pressed state helpers, and a sync that keeps a menu option's checked state equal to its check icon. |
| 2026-10-09 | lgse/strata#1533 | fix | Named and described the focusable pane of an empty, unreadable, or loading directory so focus is never lost there. |
| 2026-10-01 | lgse/strata#1359 | fix | Limited tooltips to icon-only buttons and moved tooltip text into accessible descriptions. |

## Known gaps

- The inner increment and decrement buttons of a GTK `SpinButton` have no accessible name. lgse/strata#1895
