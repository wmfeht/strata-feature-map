---
title: Shortcuts on any keyboard layout
status: shipped
origin: {issue: lgse/strata#1538, pr: lgse/strata#1576}
branch: null
reviewed_at: 73b3258ff9da7fd5f8b279e442e4fbf576850deb
review: draft
code: [src/ui/keys.rs, src/ui/keys/label.rs, src/ui/keys/composition.rs]
tests: [src/ui/keys/tests.rs]
docs: [docs/keyboard-shortcuts.md]
related: [app/window, app/shortcut-reference, integration/10xer-mode, settings/preferences/language, browser/selection/keyboard-navigation]
---

## Summary

Turns each key event into a shortcut the same way on every keyboard layout. Letters follow the key's label, non-Latin keys fall back to a Latin key, and digits count by position. It also owns the label formatter and yielding to an input-method composition; the F1 panel (`app/shortcut-reference`) and dispatcher (`app/window`) consume it. Its child `app/keyboard-shortcuts/remapping` lets users rebind keys per map.

## Behavior

### Matching

- With `us,ru` configured and Russian active, Ctrl+C on a selected file then Ctrl+V in another folder copies it. lgse/strata#1576, lgse/strata#1538
- With only a Russian layout configured, Ctrl with the keys that type с, л and ф acts as Ctrl+C, Ctrl+K and Ctrl+A. lgse/strata#1576
- In 10xer mode with Russian active, the keys that type о and л move the cursor like `j` and `k`. lgse/strata#1576
- The top digit row counts by position: Ctrl with a top-row key acts as Ctrl with the digit at that key's position. lgse/strata#1576
- Where a top-row key types `+` or `−`, Ctrl with that key reads the symbol, not the digit at the key's position. lgse/strata#1576
- After `t` or `;`, a top-row key counts as its position: on AZERTY, `t` then the `−` key selects tab 6. lgse/strata#1576
- A chord's digit step (`t 1`, `g 1`, `; 1`) also accepts Shift with the digit. lgse/strata#1576
- With AltGr held, a top-row key counts only as a digit it types: AZERTY Ctrl+AltGr+1 is not Ctrl+1. lgse/strata#1576
- Ctrl+\ works on German, Swiss, Swedish and Norwegian Mac layouts, where AltGr types `\` on the top row. lgse/strata#1576
- A digit typed off the digit row counts, such as the Hungarian 0 left of 1. lgse/strata#1576
- With Caps Lock on, Ctrl+C/V/X/A and h/j/k/l act as with it off, and Caps Lock+g acts as `g`, not `G`. lgse/strata#1576
- Keypad Enter, arrows, Home, End, Page Up, Page Down, Insert, Delete, Tab, Space, `+`, `−`, `*`, `/` and `=` act as the main keys. Keypad digits count only with Num Lock on. lgse/strata#1576
- Letter, symbol and digit shortcuts match Ctrl, Alt, Shift and Super exactly: Ctrl+Alt+C does not copy. Chord digit steps and media `0` are the exceptions; they accept Shift. lgse/strata#1576
- Symbol shortcuts ignore the Shift the layout needs to type the symbol. lgse/strata#1576
- With Russian active, Ctrl and the key that types ю act as Ctrl+. and toggle hidden files. lgse/strata#1576
- In 10xer mode on German, ö in the file list arms the actions chord, as `;` does. lgse/strata#1576
- Hyper and Meta are not shortcut modifiers: a shortcut pressed with either held acts as without it. lgse/strata#1576
- In 10xer mode with a chord such as `g` armed, pressing AltGr alone leaves the chord armed. lgse/strata#1885
- A lone layout-switch press, such as `ISO_Next_Group`, also leaves an armed 10xer chord armed. lgse/strata#1885 (unverified)
- On plain `cn`, every shortcut is the US one. lgse/strata#1583

### Typing and input methods

- With Russian active, type-to-search, filters, rename fields and footer prompts still receive Cyrillic characters. lgse/strata#1576
- While the focused text field shows an unfinished input-method or dead-key composition, each key goes to the composition before any Strata command. lgse/strata#1583
- On `cn(altgr-pinyin)` in a rename field, `m`, AltGr+1, `a` types `mā`. lgse/strata#1583
- On `cn(altgr-pinyin)` in a rename field, AltGr+1 then Escape cancels only the pending tone mark; the rename stays open. lgse/strata#1583
- With fcitx5-hangul composing 보고 in a rename, one Escape commits the syllable and cancels the rename. lgse/strata#1583
- With fcitx5 (Ctrl+Space) or IBus (Super+Space), the switch key in a rename field, the location bar, or a footer prompt reaches the input method. lgse/strata#1714
- With a Zhuyin input method such as chewing in a text field, a plain digit, `-`, `,`, `.`, `/`, or `;` starts no Strata command. lgse/strata#1714
- The first key of a Zhuyin syllable therefore reaches the input method. lgse/strata#1714
- On `tw(saisiyat)`, the semicolon key types ː in a rename field; in 10xer mode the same key in the file list arms the `;` chord. lgse/strata#1714
- On `cn(altgr-pinyin)`, digit keys without AltGr act as on US: Ctrl+1 switches to Columns, and 10xer `t 1` selects tab 1. Ctrl+AltGr+1 and `t` then AltGr+1 do neither. lgse/strata#1583

### Labels

- With Russian active, F1, menus and tooltips still show Latin keys such as Ctrl+C; labels do not change on a layout switch. lgse/strata#1576
- Shown key names follow the interface language: German shows Bild auf for Page Up, French Suppr for Delete. lgse/strata#1576
- With the interface in Simplified Chinese, key names stay as printed, such as Ctrl+C. lgse/strata#1583
- Shown shortcuts list modifiers in the order Ctrl, Alt, Shift, Super, and an uppercase letter after a modifier, such as Ctrl+Shift+N. lgse/strata#1576
- A plain letter shows as typed (`j`), Shift+letter as the uppercase letter (`J`), and chord steps are separated by a space (`g h`). lgse/strata#1576
- Shown shortcuts write minus as −, and arrows as ↑ ↓ ← →. lgse/strata#1576

## Design

[docs/keyboard-shortcuts.md](https://github.com/lgse/strata/blob/0562724ad97c8e83a4c81b85e556bf275be3b025/docs/keyboard-shortcuts.md) is the spec: normalization, labels, input methods, and how code must read key input.

- Handlers compared the typed character with Latin letters, so Cyrillic с never matched Ctrl+C. GTK accelerators were unaffected because GTK falls back to the physical key (lgse/strata#1538).
- One adapter, `ui::keys`, normalizes each event once into a `KeyPress`. `clippy.toml` bans `connect_key_pressed`, `connect_key_released` and `set_accels_for_action` outside it (lgse/strata#1576).
- Every shortcut is a named constant in one binding catalog. Handlers, the F1 reference, menus and hints refer to the same constants, so a shown shortcut always works (lgse/strata#1576).
- Each catalog shortcut is now a `Command` with a stable id and its own keys per map, so it can be rebound; see `app/keyboard-shortcuts/remapping` (lgse/strata#1885).
- GDK does not flag AltGr or a layout switch as a modifier on every backend. `KeyPress` therefore counts those keys as modifier presses itself (lgse/strata#1885, unverified).
- The adapter is built on GDK: `KeyEvent::match_()` handles Caps Lock, consumed modifiers and case, and `Display::map_keycode` gives other layouts' characters. A roughly 50-entry US table covers keymaps with no Latin layout; no crate was added (lgse/strata#1576).
- `KeyEvent::matches()` per binding was rejected. In the ordered dispatcher a physical-key match could beat a later exact match, and each check queries the keymap again (lgse/strata#1576).
- The fallback reads the level Shift selects, because Caps Lock raises the event's level for letters (lgse/strata#1576).
- The ASCII path is one `match_()` call and a range check. Nothing is cached, so no keymap-change listeners are needed (lgse/strata#1576).
- Labels never come from `gtk::accelerator_get_label` or `GtkShortcutLabel`. GTK puts Shift first, capitalizes `j`, and translates with the system locale rather than Strata's setting (lgse/strata#1576).
- Menus carry `Binding::accelerator()` for GTK's accessible shortcut but show Strata's label (lgse/strata#1576).
- Accented Latin letters such as German ö also use the fallback, so ö acts as `;` in 10xer. The owner kept this because Thai and Arabic have no `;` key; only typing destinations escape the fallback (lgse/strata#1576).
- GTK runs a field's input method only after every capture-phase handler. `keys::on_press` therefore forwards keys to a composing field first, as GtkSearchEntry's key capture does; with nothing composing the cost is one empty-list check (lgse/strata#1583).
- A field that submits on Enter must also submit from `activate`, which is how Enter arrives after an input method passes it back (lgse/strata#1583).
- No command takes a plain digit or punctuation key while a text field has focus, so Zhuyin syllables reach the input method; new bindings must keep it that way (lgse/strata#1714).
- On Wayland the input method runs in the compositor, so the keys it uses never reach Strata (lgse/strata#1583).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-12 | lgse/strata#1583 | feat | Forwarded keys to a field's unfinished input-method or dead-key composition first, so shortcuts no longer interrupt composing. |
| 2026-10-11 | lgse/strata#1576 | fix | Matched shortcuts by key label, then physical key, and rendered every shown shortcut from one binding catalog. |

## Known gaps

- Type-to-search started from the file list begins without the input method, so a pinyin letter arrives as Latin and a dead key starts nothing. lgse/strata#1583
