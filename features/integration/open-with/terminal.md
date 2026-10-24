---
title: Open in Terminal
status: shipped
origin: {issue: lgse/strata#160, pr: lgse/strata#161}
branch: null
reviewed_at: bf26829b4fd74c1f25ac170aad9521a633234a30
review: draft
code: [src/ui/terminal.rs]
tests: [src/ui/terminal/tests.rs, tests/qa/scenarios/terminal/**]
docs: [site/src/reference/keyboard-navigation.md]
related: [integration/10xer-mode, browser/tabs, app/updates]
---

## Summary

Opening the user's terminal emulator in a local folder from the context menus or Ctrl+Alt+T. The same terminal resolution runs `.sh` files and the package-manager update rows in Settings.

## Behavior

### Entry points

- Ctrl+Alt+T opens a terminal in the selected folder when exactly one folder is selected, otherwise in the pane's current folder. lgse/strata#161, lgse/strata#1484
- In Columns with no single folder selected, Ctrl+Alt+T uses the Paste destination column: the hovered column after pointer input, otherwise the focused column. lgse/strata#358, lgse/strata#1605
- When that column's one selected folder is open as the active column to its right, Ctrl+Alt+T opens in that folder. A just-clicked folder thus wins over its hovered parent. lgse/strata#1605, lgse/strata#867
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
- After Ctrl+Alt+T starts a launcher that exits at once, no `<defunct>` launcher process stays a child of Strata. lgse/strata#1570, lgse/strata#1465
- Open in Terminal from a menu and the Settings AUR and Omarchy update rows also reap their launcher after it exits. lgse/strata#1570, lgse/strata#1465

### Ghostty

- When the resolved program is named `ghostty` and `ghostty --version` reports 1.3 or later, Open in Terminal runs `ghostty +new-window --working-directory=<folder>`. lgse/strata#1763
- With Ghostty 1.3 or later running under `gtk-single-instance = true`, Open in Terminal opens a new Ghostty window in the selected folder. lgse/strata#1763, lgse/strata#1762
- Ghostty 1.2 or 1.1, or a first version line not starting with `Ghostty `, gets the plain `ghostty --working-directory=<folder>` launch. lgse/strata#1763
- Extra words in `$TERMINAL`, such as `ghostty --class=x`, follow `+new-window`. lgse/strata#1763
- `.sh` runs, the AUR update row, and the Omarchy row without Omarchy's presentation launcher start Ghostty with `-e` and no `+new-window`. lgse/strata#1763
- Strata runs `ghostty --version` at most once per program path per session, and never for other terminals or `xdg-terminal-exec`. lgse/strata#1763
- An `xdg-terminal-exec` that starts Ghostty itself gets no `+new-window`. lgse/strata#1763 (unverified)

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
- A click opens a folder as the active column while the pointer still rests on its parent, so the opened folder is preferred there. Hovering an ancestor further up still uses that ancestor's folder (lgse/strata#867, lgse/strata#1605).
- One spawn-and-reap helper waits on each launched child from its own thread. The owner chose it over a GLib child watch or a double fork (lgse/strata#1465, lgse/strata#1570).
- A long-lived terminal keeps one parked thread. Run already waited on its program this way (lgse/strata#1465, lgse/strata#1570).
- A reaper thread that cannot start is logged instead of panicking the UI thread (lgse/strata#1570).
- The reaper thread also resolves the terminal and spawns it, and the error returns to the UI thread for the dialog. A `PATH` entry or folder on a dead mount thus no longer freezes the window (lgse/strata#1729).
- A single-instance Ghostty hands a plain launch to the running instance, which ignores the folder; `+new-window` forwards it (lgse/strata#1762, lgse/strata#1763).
- `+new-window` is limited to directory launches on 1.3 or later. Ghostty 1.1 has no `+new-window`, and 1.2's drops `--working-directory`. `-e` launches already force a separate instance (lgse/strata#1763).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-20 | lgse/strata#1763 | fix | Opened Ghostty 1.3+ through `+new-window` so single-instance Ghostty honors the selected folder. |
| 2026-10-15 | lgse/strata#1605 | fix | Opened the terminal in a Columns folder just clicked open while the pointer stays over its parent. |
| 2026-10-11 | lgse/strata#1570 | fix | Reaped Open in Terminal and the AUR and Omarchy update launchers on a background thread so no defunct children remain. |
| 2026-09-14 | lgse/strata#967 | fix | Fell back to `$TERMINAL` and installed emulators when `xdg-terminal-exec` is missing. |
| 2026-09-06 | lgse/strata#470 | fix | Named the missing terminal launcher in the error and shared one command builder. |
| 2026-09-02 | lgse/strata#161 | feat | Added Open in Terminal to folder and item menus with a keyboard shortcut, using `xdg-terminal-exec`. |

## Known gaps

- On Ghostty 1.3 or later without its D-Bus service `com.mitchellh.ghostty.service`, `+new-window` opens no window when no Ghostty is running. lgse/strata#1763
