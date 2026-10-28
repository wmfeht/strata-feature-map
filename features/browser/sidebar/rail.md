---
title: Sidebar collapse and icon rail
status: shipped
origin: {issue: lgse/strata#1602, pr: lgse/strata#1606}
branch: null
reviewed_at: 73b3258ff9da7fd5f8b279e442e4fbf576850deb
review: draft
code: [src/ui/sidebar_toggle.rs]
tests: [src/ui/sidebar_toggle/tests.rs, src/ui/window/tests/rail.rs]
related: [preview/preview-panel/layout, app/window, integration/10xer-mode, integration/portal-file-chooser]
---

## Summary

The header toggle and Ctrl+B that step a browser window's sidebar between full, icon rail, and hidden, and how the rail draws its rows. `app/window` saves the step as `sidebar_expanded` and `sidebar_compact`. When space alone rails the sidebar, `preview/preview-panel/layout` decides.

## Behavior

### Stepping

- In a browser window, each press of the header toggle or Ctrl+B steps the sidebar from full to icon rail to hidden, then back to full. lgse/strata#1606
- The toggle's tooltip names the next step: "Compact sidebar (Ctrl+B)" from full, "Hide sidebar (Ctrl+B)" from the rail, "Show sidebar (Ctrl+B)" from hidden. lgse/strata#1606
- In 10xer mode the tooltip names Ctrl+N instead of Ctrl+B. lgse/strata#1576, lgse/strata#1606
- The accessible name is "Toggle sidebar (Ctrl+B)", or "(Ctrl+N)" in 10xer mode, at every step. lgse/strata#1606
- A rail chosen with the toggle stays when the window widens or the preview closes. lgse/strata#1606
- Choosing the rail while space has already railed the sidebar keeps the rail when the window widens again. lgse/strata#1606 (unverified)
- In the window where the step is taken, stepping from hidden to full shows the full sidebar even when too narrow. It stays full until the window or the preview next runs out of room. Another window on an automatic rail keeps its rail unless the step cleared a saved `sidebar_compact`. lgse/strata#1606 (unverified)

### Rail and reopening

- In the icon rail, rows show only icons with name tooltips, and headings and device buttons are hidden. lgse/strata#1181 (unverified)
- At text sizes 9 and 11, rail row icons sit on the header toggle's vertical axis. lgse/strata#1606
- Reopening the sidebar at a 10px text size restores at least its measured minimum width, so row icons are not clipped. lgse/strata#1176

## Design

- Only the toggle's steps are remembered, as `sidebar_expanded` and `sidebar_compact` (lgse/strata#1606). A "Start with sidebar collapsed" switch was left out as unneeded (lgse/strata#1345, lgse/strata#1350); hover-reveal panels were declined (lgse/strata#1282).
- One toggle reaches all three modes because the rail used to be purely automatic: a narrow window could not show the full sidebar, nor a wide one keep the rail (lgse/strata#1602, lgse/strata#1606).
- `RailPolicy` lets an explicit choice override the automatic rail either way. The fit rule that feeds it belongs to `preview/preview-panel/layout` (lgse/strata#1602, lgse/strata#1606).
- Rail rows take the scaled header-control size from code instead of a fixed 24 px CSS minimum. They stay on the toggle's axis below 100 % text size (lgse/strata#1602, lgse/strata#1606).
- The tooltip names the next step while the accessible name stays constant, so assistive technology and GUI tests find the toggle in every mode (lgse/strata#1606).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |

## Known gaps

None known.
