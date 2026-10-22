---
title: Window chrome and structure
status: shipped
origin: {issue: null, pr: lgse/strata#580}
branch: null
reviewed_at: c94eeb0020fa1154e11c741888f1b56d92ce70d6
review: draft
code: [src/ui/window/composition.rs, src/ui/window/composition/layout.rs, src/ui/window/keyboard.rs, src/ui/window/keyboard/commands.rs, src/ui/decoration.rs]
tests: [src/ui/decoration/tests.rs, src/ui/window/tests/keyboard_dispatch.rs, src/ui/window/tests/keyboard_dispatch/overlay_focus.rs, tests/qa/scenarios/dialogs_and_menus]
docs: [docs/architecture.md, site/src/reference/keyboard-navigation.md]
related: [browser/tabs, browser/sidebar, settings/preferences, integration/10xer-mode, browser/selection/keyboard-navigation, app/packaging, app/dialogs, app/keyboard-shortcuts, browser/view-modes/text-size, preview/preview-panel, integration/portal-file-chooser]
---

## Summary

The browser window's frame and skeleton: the header with its window buttons, the X11 window identity, the composition of header, sidebar, panes, preview, and footer, and the capture-phase keyboard dispatcher that routes keys to them. Features plugged into the window, such as tabs, the sidebar, and 10xer mode, own their own behavior.

## Behavior

### Window

- A browser window's title is "Strata". lgse/strata#957
- A new browser window opens with a default size of 1200×760. lgse/strata#580 (unverified)
- On X11, `WM_CLASS` instance and class are both `io.github.lgse.Strata`, matching the desktop file's `StartupWMClass` and `_GTK_APPLICATION_ID`. lgse/strata#957
- The file chooser portal keeps its separate identity, `io.github.lgse.Strata.FileChooser`. lgse/strata#957

### Title bar and frame

- On a client-decorating compositor (GNOME Mutter, Weston, WSLg), a browser window shows only Strata's header, with no GTK default title bar. lgse/strata#1680
- The portal file chooser window likewise shows no GTK default title bar. lgse/strata#1680 (unverified)
- Opening a new tab leaves the window without a GTK default title bar. lgse/strata#1680
- A second browser window has no GTK default title bar either. lgse/strata#1680
- On such a compositor, dragging Strata's header moves the window and dragging a window edge resizes it. lgse/strata#1680
- With compositing, a client-decorated window has square corners and a 1 px border in the theme's border color at 60% opacity instead of GTK's shadow. lgse/strata#1680 (unverified)
- A maximized, fullscreen, or tiled client-decorated window draws no border. lgse/strata#1680 (unverified)
- A client-decorated window without compositor alpha (`solid-csd`) draws no border, shadow, or padding. lgse/strata#1680 (unverified)

### Header

- With one tab open, the header holds, left to right, the sidebar toggle, the location bar, and the New tab, Search, Appearance, Settings, Minimize, Maximize, and Close buttons. lgse/strata#580, lgse/strata#1129, lgse/strata#1484 (unverified)
- The sidebar toggle draws its panel icon at 17 px, the same size as the sidebar's Home icon. lgse/strata#636
- Each window whose sidebar mode changes, by a step or the rail engaging or releasing, updates its toggle tooltip to name the next step. lgse/strata#1606 (unverified)
- Switching 10xer mode updates the shortcut in the sidebar toggle's tooltip and accessible name in each open window. lgse/strata#1576, lgse/strata#1606 (unverified)

### Window buttons

- A fresh profile shows only the Close button; Minimize and Maximize are hidden. lgse/strata#1129
- Show minimize button, Show maximize button, and Show close button under Settings → General → Window buttons show or hide those buttons in every open window immediately. lgse/strata#1129
- Saved window-button choices apply when a window is built, before Settings is opened, and survive a restart. lgse/strata#1129
- Maximize maximizes the window; on a maximized window it shows a restore icon and clicking it restores the window. lgse/strata#1129
- On a maximized window the Maximize button's tooltip and accessible name read "Restore window". lgse/strata#1129 (unverified)
- Minimize minimizes the window and Close closes it. lgse/strata#1129 (unverified)

### Keyboard dispatch

- While a modal dialog is open, browser shortcuts do not act behind it. lgse/strata#544
- With a modal dialog or Settings open, Ctrl+K, Ctrl+Shift+K, F5, Ctrl+Alt+T, and Ctrl+\ do nothing, and the dialog keeps focus. lgse/strata#1554, lgse/strata#1432
- With a rename field or new-entry field open, F5, Ctrl+K, Ctrl+Shift+K, Ctrl+Alt+T, and Ctrl+\ do nothing; the field keeps its text, and Return commits it. lgse/strata#1554, lgse/strata#1438
- With the F1 reference open, F5, Ctrl+K, Ctrl+Shift+K, Ctrl+Alt+T, and Ctrl+\ do nothing; F5 does not refresh the folder behind it. lgse/strata#1714
- Ctrl+K, Ctrl+Shift+K, F5, Ctrl+Alt+T, and Ctrl+\ pressed while a dialog animates closed act as with no dialog open. lgse/strata#1554
- While only a closing dialog is visible, other browser shortcuts do nothing and the key goes to GTK; text-size keys still act. lgse/strata#1554 (unverified)
- The text-size keys Ctrl++, Ctrl+−, and Ctrl+0 still change the text size while a modal dialog is open. lgse/strata#838 (unverified)
- With a 10xer chord armed, Ctrl+0 on a focused PDF drops the chord before resetting the page zoom. lgse/strata#1622
- A key pressed while a modal is open and focus is outside it moves focus into the modal and does nothing else. lgse/strata#544 (unverified)
- While a popover menu has focus or is visible, keys go to the menu rather than to browser shortcuts. lgse/strata#544 (unverified)
- With a text field focused, Ctrl+C, Ctrl+X, Ctrl+V, and Ctrl+A act on its text, not on the selected files. lgse/strata#544
- With only a Russian layout configured, Ctrl+C/X/V/A/Z/Y and Ctrl+Shift+Z in a focused text field copy, cut, paste, select all, undo, and redo its text. lgse/strata#1576

## Design

[docs/architecture.md](https://github.com/lgse/strata/blob/0562724ad97c8e83a4c81b85e556bf275be3b025/docs/architecture.md) carries the design under "Window composition" and "Window keyboard routing". [docs/keyboard-shortcuts.md](https://github.com/lgse/strata/blob/0562724ad97c8e83a4c81b85e556bf275be3b025/docs/keyboard-shortcuts.md) describes how the dispatcher reads keys through `ui::keys` (`app/keyboard-shortcuts`).

- The header is a GTK `HeaderBar` with its title buttons hidden. Strata draws Minimize, Maximize, and Close as its own header actions, so their visibility is a preference rather than a window-manager decision (lgse/strata#1100).
- Tiling window managers make in-app window buttons redundant; stacking desktops expect all three. Always restoring GTK title buttons and detecting the window manager were rejected: the first suits only stacking desktops, the second is brittle and still needs an override (lgse/strata#1100).
- The default keeps the earlier close-only header, so no layout changes until a user opts in (lgse/strata#1129).
- Window buttons bind through the shared preference path, so they apply at construction and live across windows; Settings only edits the preference (lgse/strata#1100).
- The outer window frame drawn by the desktop is a separate concern from the header buttons (lgse/strata#1100, lgse/strata#1098).
- On a client-decorating compositor, GTK adds its default title bar to a window with no registered titlebar. Each Strata window registers a hidden placeholder, so GTK adds only invisible resize edges, and Strata draws a hairline (lgse/strata#1679, lgse/strata#1680).
- The header stays inside the window content rather than in the titlebar slot, so overlays and the modal blur still cover it (lgse/strata#1679, lgse/strata#1680).
- A preference to show GTK's title bar was rejected: two title bars help no one, and the window-button toggles cover its controls (lgse/strata#1679).
- Startup runs in a fixed order: theme and styles, compose and bind, arm first-paint work and cleanup, present, then navigate. Sidebar device discovery waits until after the first paint (lgse/strata#580).
- `composition.rs` coordinates the window's parts. Its `layout` module assembles the header, the sidebar, browser, and preview splits, and the shortcut footer. Each tab builds its own Settings layer lazily, once (lgse/strata#580, lgse/strata#1484).
- `gtk_window_destroy()` frees a window only with its last reference, which its own closures can hold. Key controllers and preference bindings are therefore released on unrealize, not on destroy (lgse/strata#580).
- Each tab installs one capture-phase key controller on the window, and it acts only while that tab is mapped (lgse/strata#1484). It runs ordered stages: text size, modal and editing ownership, window and file commands, focus traversal, dismissal, then item navigation. `None` tries the next Strata stage; `Some(Propagation::Proceed)` ends dispatch and leaves the key to GTK (lgse/strata#543, lgse/strata#544).
- In the default map, a Tab stage runs after window commands and before inline editing. Tab from a Columns rename field therefore leaves the strip (lgse/strata#1431, lgse/strata#1533).
- Ctrl+K, Ctrl+Shift+K, Ctrl+Alt+T, F5, and Ctrl+\ were GTK accelerators, run only after the dispatcher yielded, so `add_guarded_window_action` gates each action itself (lgse/strata#1554).
- They are now dispatcher bindings, not accelerators: once every stage yields, the dispatcher activates the same guarded `win.*` action. Application accelerators are gone (lgse/strata#1576).
- In the file list, the file commands stage handles Ctrl+Alt+T and F5 first. The `win.*` path serves only keys the stages yield (lgse/strata#1576, unverified).
- While the F1 reference is open, a key every stage yields runs no window action; only a focused text field's editing action may run. The reference's search therefore takes every chord without F5 or Ctrl+K acting behind it (lgse/strata#1714).
- GTK's text bindings miss an editing key that only the layout fallback recognizes. After the window actions, the focused `gtk::Text` or `TextView` runs that action itself (lgse/strata#1576).
- One guard covers dialogs and name fields. It skips the action's own layer, so Ctrl+K still closes the palette it opened (lgse/strata#1432, lgse/strata#1438, lgse/strata#1554).
- Editable controls and native single-pane selection must not fall through to browser commands, which is why a stage can hand a key to GTK (lgse/strata#544).
- The file-manager launch path sets the GLib prgname and X11 program class to the application id. The portal chooser keeps its own id. AT-SPI reports the application under the prgname, `io.github.lgse.Strata`; the removed E2E harness found it by that name (lgse/strata#812, lgse/strata#957, lgse/strata#1807).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-17 | lgse/strata#1714 | fix | Stopped window actions such as F5 behind an open F1 reference, and limited Space on a selected filter hit to the filter. |
| 2026-10-14 | lgse/strata#1680 | feat | Registered a hidden titlebar so GTK stops adding its default title bar on client-decorated desktops, and drew a hairline in place of its shadow. |
| 2026-10-11 | lgse/strata#1570 | fix | Gave the preview and sidebar marquee origins click policies, so a click in the preview keeps the selection. |
| 2026-10-10 | lgse/strata#1559 | fix | Added a preview find-key stage to the dispatcher and bound the find shortcut when the preview is built. |
| 2026-10-10 | lgse/strata#1554 | fix | Gated Ctrl+K, Ctrl+Shift+K, F5, Ctrl+Alt+T, and Ctrl+\ so they do nothing over dialogs, Settings, and open name fields. |
| 2026-10-10 | lgse/strata#1539 | fix | Widened the preview split's handle so the column beside the divider keeps its resize edge. |
| 2026-10-10 | lgse/strata#1544 | fix | Reported a focused 10xer Filter or Search footer prompt to the browser, so outside folder changes leave focus in the prompt. |
| 2026-10-09 | lgse/strata#1533 | fix | Added a default-map Tab stage before inline editing and registered the browser as the window's dialog focus fallback. |
| 2026-10-09 | lgse/strata#1129 | feat | Added saved Show close, minimize, and maximize button preferences so tiling and stacking desktops each get fitting header buttons. |
| 2026-09-16 | lgse/strata#957 | fix | Set the prgname and X11 program class to the application id so `WM_CLASS` matches `StartupWMClass`. |
| 2026-09-08 | lgse/strata#636 | fix | Matched the sidebar toggle icon to the Home icon and removed excess header spacing. |
| 2026-09-08 | lgse/strata#580 | refactor | Split window setup into explicit startup sequencing and private layout, search, input, and Settings modules. |
| 2026-09-08 | lgse/strata#579 | feat | Reduced the top bar's minimum height from 54 to 46 px, keeping icon sizes and button targets. |
| 2026-09-08 | lgse/strata#544 | refactor | Replaced the 473-line window key callback with ordered dispatch stages for input ownership, commands, focus, and items. |
| 2026-09-02 | lgse/strata#157 | fix | Removed the header's horizontal padding so the sidebar toggle and close button sat flush with the window edges. |

## Known gaps

- Every key press walks the window's whole widget tree for an open menu; replacing the walk is deferred. lgse/strata#1671
- The window's remaining complex keyboard handlers, particularly command dispatch, are still due for simplification. lgse/strata#763
