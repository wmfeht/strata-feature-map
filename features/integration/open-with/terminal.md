---
title: Open in Terminal
status: shipped
origin: {issue: lgse/strata#160, pr: lgse/strata#161}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: reviewed
code: [src/ui/terminal.rs]
tests: [tests/e2e/scenarios/test_terminal.py]
docs: [docs/keyboard-navigation.md]
related: [integration/10xer-mode, browser/tabs, app/updates]
---

## Summary

Opening the user's terminal emulator in a local folder from the context menus or Ctrl+Alt+T. The same terminal resolution runs `.sh` files and the package-manager update rows in Settings.

## Behavior

### Entry points

- Ctrl+Alt+T opens a terminal in the selected folder when exactly one folder is selected, otherwise in the pane's current folder. lgse/strata#161, lgse/strata#1484
- In Columns with no single folder selected, Ctrl+Alt+T uses the Paste destination column: the hovered column after pointer input, otherwise the focused column. lgse/strata#358
- Ctrl+Alt+T with Shift or Super also held does not open a terminal. lgse/strata#1484 (unverified)
- The folder background menu shows Open in Terminal for the current folder, insensitive when the folder is not local. lgse/strata#161 (unverified)
- The background menu omits Open in Terminal in Trash and Recent. lgse/strata#161, lgse/strata#1083
- The item menu shows Open in Terminal for a single local folder outside Trash. lgse/strata#161
- For a location without a local path, the shortcut shows "Unable to open terminal" with "This location is not a local folder". lgse/strata#161
- In Trash, the shortcut shows "Unable to open terminal" with "Terminal cannot be opened in Trash". lgse/strata#161

### Choosing the terminal

- A command in `$TERMINAL`, with its arguments, is used first, even when it is not a known emulator. lgse/strata#967 (unverified)
- Without `$TERMINAL`, `xdg-terminal-exec --dir=<folder>` is used when it is on `PATH`. lgse/strata#161, lgse/strata#967
- Otherwise the first of konsole, gnome-terminal, xfce4-terminal, kitty, ghostty, alacritty, foot, wezterm, tilix, terminator, and xterm on `PATH` is used. lgse/strata#967
- Every terminal starts with the folder as its working directory. Each known emulator except xterm also gets its own directory option, such as kitty's `--working-directory`. lgse/strata#967 (unverified)
- Terminal output does not reach Strata's standard output or error. lgse/strata#161

### Errors

- With no terminal found, the dialog says "No terminal emulator was found", suggests `xdg-terminal-exec` with `~/.config/xdg-terminals.list` or `$TERMINAL`, and lists the fallback emulators. lgse/strata#967
- A resolved terminal that is missing at launch shows "Terminal “<program>” was not found on your PATH". lgse/strata#470, lgse/strata#967
- Any other launch failure shows "Terminal “<program>” could not be started:" followed by the cause. lgse/strata#470, lgse/strata#967

## Design

`xdg-terminal-exec` respects the user's configured terminal, such as Omarchy's `xdg-terminals.list`. Hard-coding one emulator was rejected because it ignores that preference (lgse/strata#160).

- Distributions such as CachyOS and vanilla Arch do not ship `xdg-terminal-exec`, so `$TERMINAL` and a `PATH` probe of known emulators back it up. `xdg-terminal-exec` became an optional package dependency (lgse/strata#966, lgse/strata#967).
- A custom terminal command setting was deferred; `$TERMINAL` and `xdg-terminal-exec` cover preference (lgse/strata#160).
- Errors name the program and where it was looked for, because the raw "No such file or directory (os error 2)" gave nothing to act on (lgse/strata#437).
- One module resolves and builds every terminal command: Open in Terminal, `.sh` runs, and the AUR and Omarchy update rows. All share the no-terminal message; Open in Terminal and the update rows also share the launch-failure messages (lgse/strata#470, lgse/strata#1028).
- Non-local and Trash locations fail closed, since a terminal needs a real directory (lgse/strata#160).
- Ctrl+T moved to tabs, so the terminal moved to Ctrl+Alt+T; 10xer keeps `;` then `t` (lgse/strata#1484).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-14 | lgse/strata#967 | fix | Fell back to `$TERMINAL` and installed emulators when `xdg-terminal-exec` is missing. |
| 2026-09-06 | lgse/strata#470 | fix | Named the missing terminal launcher in the error and shared one command builder. |
| 2026-09-02 | lgse/strata#161 | feat | Added Open in Terminal to folder and item menus with a keyboard shortcut, using `xdg-terminal-exec`. |

## Known gaps

- In Columns, the terminal shortcut opens at the listing root instead of a folder selected in the parent pane. lgse/strata#867
