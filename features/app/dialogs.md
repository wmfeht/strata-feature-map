---
title: Modal dialogs
status: shipped
origin: {issue: lgse/strata#88, pr: lgse/strata#91}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: reviewed
code: [src/ui/modal.rs, src/ui/modal/layout.rs, src/ui/controls.rs, src/ui/blur.rs]
tests: [src/ui/modal/tests.rs, src/ui/controls/tests.rs, tests/e2e/scenarios/test_dialogs_and_menus.py]
docs: []
related: [operations/progress, app/window, settings/preferences]
---

## Summary

The shared shell behind Strata's action dialogs: the blurred backdrop, open and close animation, backdrop dismissal, initial focus, Enter and Escape handling, form submission, and sizing within the window. Individual dialogs supply their content and actions; this node owns what they have in common.

## Behavior

### Opening and closing

- While a dialog is open, the window content behind it is blurred; closing one of two stacked dialogs keeps the blur until the last one closes. lgse/strata#147
- Opening a dialog fades in the backdrop and fades the dialog in from 96% scale over 200 ms; closing reverses it over 200 ms. lgse/strata#112 (unverified)
- Clicking the backdrop outside a dialog dismisses it without confirming, like Cancel or Escape. lgse/strata#107
- A dialog in a non-cancellable in-progress state, such as file operation progress, ignores backdrop clicks. lgse/strata#107, lgse/strata#491
- The mount authentication dialog ignores backdrop clicks once its username, domain, or password field has text. lgse/strata#105 (unverified)
- The Compress dialog ignores backdrop clicks once its name differs from the default or either password field has text. lgse/strata#105 (unverified)
- The archive password dialog ignores backdrop clicks once its password field has text. lgse/strata#105 (unverified)
- Clicking the backdrop repeatedly during the close animation dismisses the dialog once and leaves no overlay behind. lgse/strata#112

### Keyboard

- Confirmation dialogs open with the confirm button focused, so Enter confirms and Escape cancels: Permanently delete, Empty Trash, Restore, paste and archive Replace, Run, and Forget saved password. lgse/strata#1206
- With focus outside a text field, Enter activates the focused button and toggles a focused checkbox or switch, so Enter with Cancel focused cancels. lgse/strata#1052, lgse/strata#175 (unverified)
- With focus outside a text field, an unmodified arrow key moves focus to the nearest button, menu button, checkbox, switch, or entry in that direction; Down on a menu button opens its menu. lgse/strata#175 (unverified)
- While a dialog is open, focus that moves outside it is returned to the dialog's layer, not to a button inside it. lgse/strata#1432
- After the last of a chain of drive, Properties, or error dialogs closes, focus returns to the widget focused before the first one opened. lgse/strata#1331

### Forms

- Enter in a single-line text or password field of the Compress, archive password, or mount authentication dialog activates the primary button. lgse/strata#464
- Enter in a form field does nothing while the primary button is disabled. lgse/strata#464
- Enter with an invalid Compress name such as `../escape` keeps the dialog open and writes no archive. lgse/strata#464
- Enter in a multi-line text field inserts a newline instead of submitting. lgse/strata#464

### Layout

- A dialog's shadow fades past its rounded edges with no hard cutoff, and a click in the shadow dismisses like a backdrop click. lgse/strata#909
- A dialog larger than the window scrolls inside the window instead of enlarging it. lgse/strata#838
- When the window is narrower than a dialog's minimum width plus 84 px, the dialog fills the width with 12 px margins. lgse/strata#1155 (unverified)
- Message dialog text keeps Korean words of up to 12 characters whole when wrapping, instead of breaking between syllables, and never inserts hyphens. lgse/strata#1519 (unverified)

## Design

Dialogs are overlay layers on the window's `GtkOverlay`, not `GtkWindow`s, so GTK's default-widget and modality do not apply and Strata supplies both (lgse/strata#439, lgse/strata#1432). [docs/architecture.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/architecture.md) records the split: `ui/modal.rs` owns hosting, animation, and dismissal; each dialog owns its cancel, close, backdrop, and submission policies.

- One shell builds every action dialog: header with an accent or danger icon bezel, title, subtitle, close button, body, and Cancel and confirm actions. It replaced one-off widgets and CSS that drifted across themes (lgse/strata#88, lgse/strata#91). The search palette and Settings stay specialized, and native choosers stay native.
- Animation toggles a `modal-hidden` CSS class: opening removes it 16 ms after mapping, and closing removes the layer 200 ms after adding it. The earlier timer called `allocate()` against GTK's own layout, broke centering, and stacked handlers. A `dismissing` class plus an insensitive layer stops a second dismissal (lgse/strata#112).
- Backdrop clicks are hit-tested against the dialog and its viewport, not spacer widgets (lgse/strata#909). A click outside both calls the shared `dismiss_modal_layer` unless the dialog's `block_dismiss` guard returns true (lgse/strata#107). The owner held that a dirty form should not dismiss (lgse/strata#105); Compress, archive password, and mount authentication apply that guard.
- `ScrolledWindow` clips its child, CSS shadows included, so the layout reserves 42 px for the largest shadow, the Settings panel's 28 px blur (lgse/strata#909). The layer measures 1×1 so a dialog never grows the window (lgse/strata#838).
- Confirmation dialogs set initial focus through one `focus_button` helper. About 12 hand-rolled focus grabs had let an idle callback refocus Cancel in the permanent-delete dialog; Enter confirms and Escape cancels, matching Finder (lgse/strata#1204).
- `submit_on_enter` walks a form and wires `activate` on each `gtk::Entry` and `gtk::PasswordEntry` to the primary button, standing in for a window default widget. It replaced per-field handlers in Copy to and mount authentication (lgse/strata#439, lgse/strata#464).
- A chained dialog inherits the original browser focus origin, not the focus inside the dialog before it (lgse/strata#1331).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-23 | lgse/strata#1206 | fix | Focused the confirm action in dialogs and stopped the path-completion popover flashing. |
| 2026-09-12 | lgse/strata#909 | fix | Reserved shadow space inside the modal scroller and kept shadow clicks dismissing the dialog. |
| 2026-09-06 | lgse/strata#464 | fix | Added one Enter-to-submit pattern for single-line fields in modal forms. |
| 2026-09-01 | lgse/strata#117 | fix | Focused the confirm button so Enter confirms the paste conflict and delete dialogs. |
| 2026-09-01 | lgse/strata#112 | fix | Replaced timer-driven modal animation with CSS transitions and guarded repeated dismissal. |
| 2026-09-01 | lgse/strata#107 | fix | Dismissed modal dialogs on backdrop clicks, except during in-progress states. |
| 2026-09-01 | lgse/strata#91 | refactor | Moved action dialogs onto the shared modal shell and themed form controls. |

## Known gaps

- Ctrl+K and Ctrl+Shift+K open the search palette beneath an open dialog and take its focus; the fix is planned, not merged. lgse/strata#1432, lgse/strata#1546
- A dialog closed over another dialog does not return focus to its opener, and a keyboard-closed dialog loses the focus ring; the fix is unmerged. lgse/strata#1544
