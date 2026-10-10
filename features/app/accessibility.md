---
title: Accessibility
status: shipped
origin: {issue: lgse/strata#341, pr: lgse/strata#415}
branch: null
reviewed_at: 72b840e69d6f0df9d33fb5583e62a3a2944886a1
review: draft
code: [src/ui/accessibility.rs]
tests: [src/ui/accessibility/tests.rs, tests/e2e/scenarios/test_accessibility.py]
docs: [docs/e2e-testing.md]
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
- Strata's modal dialogs have the dialog role and are named after their title. lgse/strata#415

### Tooltips

- Hovering a labelled button, menu item, label, entry, file row, breadcrumb, or status indicator shows no tooltip. The one exception is a truncated name on an Icons-view card (`browser/view-modes/icons`). lgse/strata#1359, lgse/strata#1553
- Hovering an icon-only button shows its tooltip, such as "Toggle sidebar (Ctrl+B)" on the header sidebar toggle. lgse/strata#1359
- In the collapsed sidebar rail, each row shows its name as a tooltip; expanding the sidebar removes those tooltips. lgse/strata#1359
- Text that tooltips carried before, such as a sidebar place's or breadcrumb's full path, is now the control's accessible description. lgse/strata#1359

## Design

[docs/e2e-testing.md](https://github.com/lgse/strata/blob/72b840e69d6f0df9d33fb5583e62a3a2944886a1/docs/e2e-testing.md) ("Accessible names are product surface") states the contract this node owns.

- The E2E harness locates controls only by accessible role and name. When it cannot identify a control, the fix is to name it in the application, never a test-only API (lgse/strata#341).
- An entry's name and description sit on the list item, not the row content, because the item carries the `list item` or `table cell` role and the selected and focused states (lgse/strata#415).
- Panes use the group role because GTK drops a label set on a plain `GtkBox`, whose generic role ARIA forbids naming (lgse/strata#415).
- The pane, not the entry list, carries the directory and view, because an empty directory replaces the list with a placeholder (lgse/strata#415).
- The focusable pane of an empty, unreadable, or loading directory carries the directory as its name and the shown status as its description (lgse/strata#1466).
- Menu accelerators go in the description so the shortcut text is not read as part of the item's name (lgse/strata#415).
- Tooltips are not a reliable name source. One field exposed its tooltip as its name (lgse/strata#811), while tooltip-only location controls had no name (lgse/strata#1131). Controls get explicit names instead (lgse/strata#1132).
- A hover delay was requested for tooltips that covered folders (lgse/strata#1337). The owner instead removed tooltips from everything but icon-only buttons, since a delay does not remove redundant text (lgse/strata#1358).
- The tooltip rule lives in the upstream `AGENTS.md`. Switchable controls show tooltips only in icon-only mode, help, errors, and status stay visible, and tooltip text is never data (lgse/strata#1359).
- lgse/strata#1359 also moved names and descriptions that E2E checks read from tooltips into explicit accessible metadata (lgse/strata#1337).
- Exclusive choices are radio menu items and on/off options are check menu items, because screen readers announce their checked state (lgse/strata#1467, lgse/strata#1544).
- Chosen states are product surface too: E2E checks read `checked` or `pressed` from AT-SPI and never infer them from check-icon children (lgse/strata#1544).
- A menu option's `checked` state mirrors its check icon's own visibility, because a closed popover hides every option's ancestors (lgse/strata#1544, unverified).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-10 | lgse/strata#1544 | fix | Added checked and pressed state helpers, and a sync that keeps a menu option's checked state equal to its check icon. |
| 2026-10-09 | lgse/strata#1533 | fix | Named and described the focusable pane of an empty, unreadable, or loading directory so focus is never lost there. |
| 2026-10-01 | lgse/strata#1359 | fix | Limited tooltips to icon-only buttons and moved tooltip text into accessible descriptions. |

## Known gaps

- The Ctrl+F pane filter field has no accessible name; the issue was closed without a fix. lgse/strata#810
