---
title: Window key and wheel dispatch
status: shipped
origin: {issue: null, pr: lgse/strata#544}
branch: null
reviewed_at: 86df474dc0e8352e0e2098637a017cc4c77a8c44
review: draft
code: [src/ui/window/keyboard.rs, src/ui/window/keyboard/commands.rs]
tests: [src/ui/window/tests/keyboard_dispatch.rs, tests/qa/scenarios/dialogs_and_menus/modal-dialog-blocks-window-shortcuts.jsonl]
related: [app/keyboard-shortcuts, app/dialogs, app/shortcut-reference, browser/view-modes/text-size, browser/view-modes/thumbnail-size, integration/10xer-mode, preview/preview-panel, browser/sidebar]
---

## Summary

The capture-phase key controller and Ctrl+wheel controller each browser window installs. The key dispatcher runs ordered stages that decide whether a dialog, menu, text field, prompt, or browser command gets a key. The wheel controller turns Ctrl+wheel into text-size steps and Ctrl+Shift+wheel into Icons thumbnail steps. The commands each stage runs belong to their own features.

## Behavior

### Keys

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
- With no dialog or menu open, Escape during a List heading drag cancels only the drag. The file selection stays and the footer chord mark clears. lgse/strata#1900
- With a text field focused, Ctrl+C, Ctrl+X, Ctrl+V, and Ctrl+A act on its text, not on the selected files. lgse/strata#544
- With only a Russian layout configured, Ctrl+C/X/V/A/Z/Y and Ctrl+Shift+Z in a focused text field copy, cut, paste, select all, undo, and redo its text. lgse/strata#1576
- With 10xer mode on, Ctrl+Shift+K and Ctrl+\ do nothing from the file list in every window; turning the mode off restores them. lgse/strata#1271, lgse/strata#1576
- With 10xer mode on, Ctrl+Alt+T in the file list still opens a terminal. lgse/strata#1576

### Sidebar focus

- Outside 10xer mode, Ctrl+Shift+B shows a hidden sidebar and focuses the active row; pressing it again in the sidebar restores the previous focus. lgse/strata#58 (unverified)
- In 10xer mode, Ctrl+Shift+B focuses a visible sidebar and leaves a hidden one hidden. lgse/strata#1284

### Wheel

- Ctrl+wheel changes the text size by 1 px per notch, accumulating smooth touchpad deltas into whole steps. lgse/strata#1069, lgse/strata#1140
- Ctrl+Alt+wheel and Ctrl+Super+wheel leave the text size unchanged and scroll as a plain wheel would. lgse/strata#1069 (unverified)
- Ctrl+Shift+wheel does not change the text size; in Icons it steps the thumbnail size instead. lgse/strata#1721
- In Columns or List, Ctrl+Shift+wheel resizes nothing and passes through to the view. lgse/strata#1721
- The portal file chooser has no wheel zoom: Ctrl+Shift+wheel there does not step the thumbnail size. lgse/strata#1721
- In Icons, each Ctrl+Shift+wheel notch steps the thumbnail size once, up for larger and down for smaller. Smooth touchpad deltas accumulate into whole steps. lgse/strata#1721
- In Icons, a Ctrl+Shift+wheel that arrives as horizontal scrolling steps the thumbnail size the same way. lgse/strata#1721
- Ctrl+wheel never changes the Icons thumbnail size. lgse/strata#1721
- Ctrl+wheel over a PDF preview, including its scrollbars, leaves the text size unchanged and reaches the PDF. lgse/strata#1069, lgse/strata#1622
- Ctrl+wheel over the file listing changes the text size even while a PDF preview holds keyboard focus. lgse/strata#1622

## Design

[docs/architecture.md](https://github.com/lgse/strata/blob/0562724ad97c8e83a4c81b85e556bf275be3b025/docs/architecture.md) carries the design under "Window keyboard routing". [docs/keyboard-shortcuts.md](https://github.com/lgse/strata/blob/0562724ad97c8e83a4c81b85e556bf275be3b025/docs/keyboard-shortcuts.md) describes how the dispatcher reads keys through `ui::keys` (`app/keyboard-shortcuts`).

- Each tab installs one capture-phase key controller on the window, and it acts only while that tab is mapped (lgse/strata#1484). It runs ordered stages: text size, modal and editing ownership, window and file commands, focus traversal, dismissal, then item navigation. `None` tries the next Strata stage; `Some(Propagation::Proceed)` ends dispatch and leaves the key to GTK (lgse/strata#543, lgse/strata#544).
- In the default map, a Tab stage runs after window commands and before inline editing. Tab from a Columns rename field therefore leaves the strip (lgse/strata#1431, lgse/strata#1533).
- Ctrl+K, Ctrl+Shift+K, Ctrl+Alt+T, F5, and Ctrl+\ were GTK accelerators, run only after the dispatcher yielded, so `add_guarded_window_action` gates each action itself (lgse/strata#1554).
- They are now dispatcher bindings, not accelerators: once every stage yields, the dispatcher activates the same guarded `win.*` action. Application accelerators are gone (lgse/strata#1576).
- In the file list, the file commands stage handles Ctrl+Alt+T and F5 first. The `win.*` path serves only keys the stages yield (lgse/strata#1576, unverified).
- While the F1 reference is open, a key every stage yields runs no window action; only a focused text field's editing action may run. The reference's search therefore takes every chord without F5 or Ctrl+K acting behind it (lgse/strata#1714).
- GTK's text bindings miss an editing key that only the layout fallback recognizes. After the window actions, the focused `gtk::Text` or `TextView` runs that action itself (lgse/strata#1576).
- One guard covers dialogs and name fields. It skips the action's own layer, so Ctrl+K still closes the palette it opened (lgse/strata#1432, lgse/strata#1438, lgse/strata#1554).
- Editable controls and native single-pane selection must not fall through to browser commands, which is why a stage can hand a key to GTK (lgse/strata#544).
- Heading-drag cancellation is shared by the browser and the portal chooser, and runs in the ownership stage after the modal and menu checks (lgse/strata#1900).
- Ctrl+wheel is handled in the capture phase so scrolled windows cannot consume it first. The PDF scroll container keeps its own zoom (lgse/strata#1069, lgse/strata#1110).
- The wheel controller accumulates deltas itself instead of using GTK's discrete mode, which consumed every touchpad scroll before descendant scrollers saw it (lgse/strata#1140).
- Scroll events carry no pointer position, so the wheel handler asks the seat where the pointer is and picks the widget under it (lgse/strata#1622).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |

## Known gaps

- In 10xer mode, Ctrl+Alt+T still opens a terminal from the file list, and Ctrl+Shift+K still acts from a non-menu popover. Unbinding them awaits a decision. lgse/strata#1576
- Each stage re-reads and classifies the focused widget, and every key press walks the widget tree for modal layers and open menus. Resolving the input owner once per press is proposed. lgse/strata#1716
- Fifteen call sites cancel an armed 10xer chord by hand; one that forgets leaves a stale chord mark that swallows the next key. lgse/strata#1718
