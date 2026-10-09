---
title: Window chrome and structure
status: shipped
origin: {issue: null, pr: lgse/strata#580}
branch: null
reviewed_at: aee71335dfecd059b9af23efeac2ed52c43e3b19
review: draft
code: [src/ui/window/composition.rs, src/ui/window/composition/layout.rs, src/ui/window/keyboard.rs, src/ui/window/keyboard/commands.rs]
tests: [src/ui/window/tests/keyboard_dispatch.rs]
docs: [docs/architecture.md]
related: [browser/tabs, browser/sidebar, settings/preferences, integration/10xer-mode, browser/selection/keyboard-navigation, app/packaging, app/dialogs]
---

## Summary

The browser window's frame and skeleton: the header with its window buttons, the X11 window identity, the composition of header, sidebar, panes, preview, and footer, and the capture-phase keyboard dispatcher that routes keys to them. Features plugged into the window, such as tabs, the sidebar, and 10xer mode, own their own behavior.

## Behavior

### Window

- A browser window's title is "Strata". lgse/strata#957
- A new browser window opens with a default size of 1200×760. lgse/strata#580 (unverified)
- On X11, `WM_CLASS` instance and class are both `io.github.lgse.Strata`, matching the desktop file's `StartupWMClass` and `_GTK_APPLICATION_ID`. lgse/strata#957
- The file chooser portal keeps its separate identity, `io.github.lgse.Strata.FileChooser`. lgse/strata#957

### Header

- With one tab open, the header holds, left to right, the sidebar toggle, the location bar, and the New tab, Search, Appearance, Settings, Minimize, Maximize, and Close buttons. lgse/strata#580, lgse/strata#1129, lgse/strata#1484 (unverified)
- The sidebar toggle draws its panel icon at 17 px, the same size as the sidebar's Home icon. lgse/strata#636

### Window buttons

- A fresh profile shows only the Close button; Minimize and Maximize are hidden. lgse/strata#1129
- Show minimize button, Show maximize button, and Show close button under Settings → General → Window buttons show or hide those buttons in every open window immediately. lgse/strata#1129
- Saved window-button choices apply when a window is built, before Settings is opened, and survive a restart. lgse/strata#1129
- Maximize maximizes the window; on a maximized window it shows a restore icon and clicking it restores the window. lgse/strata#1129
- On a maximized window the Maximize button's tooltip and accessible name read "Restore window". lgse/strata#1129 (unverified)
- Minimize minimizes the window and Close closes it. lgse/strata#1129 (unverified)

### Keyboard dispatch

- While a modal dialog is open, browser shortcuts do not act behind it. lgse/strata#544
- The text-size keys Ctrl++, Ctrl+−, and Ctrl+0 still change the text size while a modal dialog is open. lgse/strata#838 (unverified)
- A key pressed while a modal is open and focus is outside it moves focus into the modal and does nothing else. lgse/strata#544 (unverified)
- While a popover menu has focus or is visible, keys go to the menu rather than to browser shortcuts. lgse/strata#544 (unverified)
- With a text field focused, Ctrl+C, Ctrl+X, Ctrl+V, and Ctrl+A act on its text, not on the selected files. lgse/strata#544

## Design

[docs/architecture.md](https://github.com/lgse/strata/blob/aee71335dfecd059b9af23efeac2ed52c43e3b19/docs/architecture.md) carries the window composition and keyboard routing design under "Window composition" and "Window keyboard routing".

- The header is a GTK `HeaderBar` with its title buttons hidden. Strata draws Minimize, Maximize, and Close as its own header actions, so their visibility is a preference rather than a window-manager decision (lgse/strata#1100).
- Tiling window managers make in-app window buttons redundant; stacking desktops expect all three. Always restoring GTK title buttons and detecting the window manager were rejected: the first suits only stacking desktops, the second is brittle and still needs an override (lgse/strata#1100).
- The default keeps the earlier close-only header, so no layout changes until a user opts in (lgse/strata#1129).
- Window buttons bind through the shared preference path, so they apply at construction and live across windows; Settings only edits the preference (lgse/strata#1100).
- The outer window frame drawn by the desktop is a separate concern from the header buttons (lgse/strata#1100, lgse/strata#1098).
- Startup runs in a fixed order: theme and styles, compose and bind, arm first-paint work and cleanup, present, then navigate. Sidebar device discovery waits until after the first paint (lgse/strata#580).
- `composition.rs` coordinates the window's parts. Its `layout` module assembles the header, the sidebar, browser, and preview splits, and the shortcut footer. Each tab builds its own Settings layer lazily, once (lgse/strata#580, lgse/strata#1484).
- `gtk_window_destroy()` frees a window only with its last reference, which its own closures can hold. Key controllers and preference bindings are therefore released on unrealize, not on destroy (lgse/strata#580).
- Each tab installs one capture-phase key controller on the window, and it acts only while that tab is mapped (lgse/strata#1484). It runs ordered stages: text size, modal and editing ownership, window and file commands, focus traversal, dismissal, then item navigation. `None` tries the next Strata stage; `Some(Propagation::Proceed)` ends dispatch and leaves the key to GTK (lgse/strata#543, lgse/strata#544).
- In the default map, a Tab stage runs right after window commands and before inline editing, so Tab from a rename field leaves the listing (lgse/strata#1431, lgse/strata#1533).
- Editable controls and native single-pane selection must not fall through to browser commands, which is why a stage can hand a key to GTK (lgse/strata#544).
- The file-manager launch path sets the GLib prgname and X11 program class to the application id. The portal chooser keeps its own id. AT-SPI reports the application under the prgname, so the E2E harness looks for `io.github.lgse.Strata` (lgse/strata#812, lgse/strata#957).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-09 | lgse/strata#1533 | fix | Added a default-map Tab stage before inline editing and registered the browser as the window's dialog focus fallback. |
| 2026-10-09 | lgse/strata#1129 | feat | Added saved Show close, minimize, and maximize button preferences so tiling and stacking desktops each get fitting header buttons. |
| 2026-09-16 | lgse/strata#957 | fix | Set the prgname and X11 program class to the application id so `WM_CLASS` matches `StartupWMClass`. |
| 2026-09-08 | lgse/strata#636 | fix | Matched the sidebar toggle icon to the Home icon and removed excess header spacing. |
| 2026-09-08 | lgse/strata#580 | refactor | Split window setup into explicit startup sequencing and private layout, search, input, and Settings modules. |
| 2026-09-08 | lgse/strata#579 | feat | Reduced the top bar's minimum height from 54 to 46 px, keeping icon sizes and button targets. |
| 2026-09-08 | lgse/strata#544 | refactor | Replaced the 473-line window key callback with ordered dispatch stages for input ownership, commands, focus, and items. |
| 2026-09-02 | lgse/strata#157 | fix | Removed the header's horizontal padding so the sidebar toggle and close button sat flush with the window edges. |

## Known gaps

- On stacking desktops the window still gets the desktop's outer border and decorations; dropping them is unimplemented. lgse/strata#1098
- The window's remaining complex keyboard handlers, particularly command dispatch, are still due for simplification. lgse/strata#763
