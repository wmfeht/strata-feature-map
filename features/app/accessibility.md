---
title: Accessibility
status: shipped
origin: {issue: lgse/strata#341, pr: lgse/strata#415}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [src/ui/accessibility.rs]
tests: [src/ui/accessibility/tests.rs, tests/e2e/scenarios/test_accessibility.py]
docs: [docs/e2e-testing.md]
related: [browser/navigation/location-bar, browser/sidebar, settings/preferences/language, browser/context-menu, app/dialogs]
---

## Summary

App-wide accessible semantics for screen readers and AT-SPI automation: the names, descriptions, and roles of panes, entry lists, entries, menus, and dialogs, plus the rule that only icon-only buttons show tooltips. Accessible labels specific to one feature stay with that feature.

## Behavior

### Browser listing

- In every view, each entry is named with its display name and described as "Folder" or "File". lgse/strata#415
- A symbolic link is described as "Folder link" or "File link", and a dangling link as "Broken link". lgse/strata#415 (unverified)
- Each pane is a group named after its directory and described as "Columns view", "Icons view", or "List view". lgse/strata#415
- The entry list inside a pane is named after its directory and described as "Files". lgse/strata#415
- Entries are focusable, and selecting one sets the `selected` state on that entry and on no other. lgse/strata#415
- View, entry kind, and list descriptions are shown in the interface language. lgse/strata#1519

### Chrome, menus, and dialogs

- The window exposes buttons named "Search (Ctrl+K)", "Appearance", "Settings", "Close window", and "Toggle sidebar (Ctrl+B)". lgse/strata#415
- Pressing Tab repeatedly from the window's first control reaches the file listing. lgse/strata#415
- Items in Strata's custom menus have the menu item role, are named after the action, and carry the accelerator in their description. lgse/strata#415
- Strata's modal dialogs have the dialog role and are named after their title. lgse/strata#415

### Tooltips

- Hovering a labelled button, menu item, label, entry, file row, breadcrumb, or status indicator shows no tooltip. lgse/strata#1359
- Hovering an icon-only button shows its tooltip, such as "Toggle sidebar (Ctrl+B)" on the header sidebar toggle. lgse/strata#1359
- In the collapsed sidebar rail, each row shows its name as a tooltip; expanding the sidebar removes those tooltips. lgse/strata#1359
- Text that tooltips carried before, such as a sidebar place's or breadcrumb's full path, is now the control's accessible description. lgse/strata#1359

## Design

[docs/e2e-testing.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/e2e-testing.md) ("Accessible names are product surface") states the contract this node owns.

- The E2E harness locates controls only by accessible role and name. When it cannot identify a control, the fix is to name it in the application, never a test-only API (lgse/strata#341).
- An entry's name and description sit on the list item, not the row content, because the item carries the `list item` or `table cell` role and the selected and focused states (lgse/strata#415).
- Panes use the group role because GTK drops a label set on a plain `GtkBox`, whose generic role ARIA forbids naming (lgse/strata#415).
- The pane, not the entry list, carries the directory and view, because an empty directory replaces the list with a placeholder (lgse/strata#415).
- Menu accelerators go in the description so the shortcut text is not read as part of the item's name (lgse/strata#415).
- Tooltips are not a reliable name source. One field exposed its tooltip as its name (lgse/strata#811), while tooltip-only location controls had no name (lgse/strata#1131). Controls get explicit names instead (lgse/strata#1132).
- A hover delay was requested for tooltips that covered folders (lgse/strata#1337). The owner instead removed tooltips from everything but icon-only buttons, since a delay does not remove redundant text (lgse/strata#1358).
- The tooltip rule lives in the upstream `AGENTS.md`. Switchable controls show tooltips only in icon-only mode, help, errors, and status stay visible, and tooltip text is never data (lgse/strata#1359).
- E2E checks that read names or descriptions from tooltips were moved to explicit accessible metadata in the same change (lgse/strata#1337).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-01 | lgse/strata#1359 | fix | Limited tooltips to icon-only buttons and moved tooltip text into accessible descriptions. |

## Known gaps

- Appearance options, Properties permission bits, and Settings choice buttons expose no checked or pressed state or current value; the fix is unmerged. lgse/strata#1467, lgse/strata#1544
- In an empty directory no widget reports focus and Tab does nothing; the fix is unmerged. lgse/strata#1466, lgse/strata#1533
- The Ctrl+F pane filter field has no accessible name; the issue was closed without a fix. lgse/strata#810
