---
title: 10xer mode in the file chooser
status: shipped
origin: {issue: lgse/strata#1261, pr: lgse/strata#1311}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [src/ui/window/keyboard/chooser.rs]
tests: [src/ui/chooser/tests/keyboard.rs]
docs: [docs/portal-file-chooser.md]
related: [integration/portal-file-chooser]
---

## Summary

The portal file chooser follows the saved 10xer preference. Its keys run through the 10xer dispatcher, limited by a per-request policy that refuses commands the request does not allow.

## Behavior

### Following the mode

- A chooser follows the saved 10xer preference and live changes to it, without opening Settings. lgse/strata#1311
- While the mode is on, a footer below the files carries prompts, chords, and feedback, and the pane chrome hides; Accept, Cancel, the close button, and List headings stay. lgse/strata#1311
- With the mode off, the chooser's own keys are unchanged. lgse/strata#1311
- `q` does not end the request. lgse/strata#1311
- F1 shows a reference that lists only the keys the request allows, and Esc closes it without cancelling the request. lgse/strata#1376

### Choosing

- Enter or `o` on a file chooses it instead of opening it; in a multiple-file request with a fill, they choose the fill. lgse/strata#1311
- Enter or `o` on a folder opens it; Ctrl+Enter or Accept chooses the folder in a folder request. lgse/strata#1311
- The request takes the fill, or the cursor item when nothing is filled; the automatic first-row selection does not count. lgse/strata#1311
- Esc takes one dismissal step (prompt, filter, search, find, range, preview, fill) and then cancels the request. lgse/strata#1311
- `f` and `s` hits follow the request's folder-only and file-type limits. lgse/strata#1311

### Save requests

- A Save request opens with the files focused. lgse/strata#1311
- Enter in the files saves the name in the current folder, whatever the cursor is on; moving the cursor changes neither the name nor the folder. lgse/strata#1311
- `o` on a file saves over it, and replacing an existing file asks first with Cancel focused. lgse/strata#1311
- `r` and F2 focus the name with the part before the extension selected instead of renaming a file on disk. lgse/strata#1311
- In the name field every key is typed except F1, Ctrl+Shift+M, and Esc, which returns to the files and keeps the edit. lgse/strata#1311
- Tab goes from the files to the header, then to the name, then back to the files. lgse/strata#1311
- Hints for Enter, `r`, and `o` sit beside Cancel and Save while the mode is on. lgse/strata#1311

### Refused commands

- `y`, `x`, `p`, `P`, `Y`, `X`, Ctrl+C, Ctrl+X, Ctrl+V, `O`, `;`, `i`, and Shift+Q flash `Not available in the file chooser`. lgse/strata#1311
- `M`, `C`, `R`, `g +`, and `g -` flash `Not available in the file chooser`. lgse/strata#1340
- In a single-item request, Space, `v`, `V`, Ctrl+A, and Ctrl+R flash `Only one item can be chosen`. lgse/strata#1311
- `g t`, `g n`, and remote pins flash `Only local folders can be opened here`. lgse/strata#1311
- `a`, `d`, `D`, sort chords, `.`, `c c`, and `c n` work as in a window. `r` and F2 do too, outside Save requests. lgse/strata#1311

## Design

- lgse/strata#1152 first kept the chooser's keys and chrome independent, while the later mode spec shared the mode with it. DEC-01 put the chooser in scope (lgse/strata#1261, lgse/strata#1311).
- Reusing the browser dispatcher must not bypass single-selection, folder-only, Save, or local-only request policy. DEC-02 therefore set a per-request allowlist (lgse/strata#1152, lgse/strata#1311).
- Disallowed keys are refused when pressed, with feedback, not only hidden from help (lgse/strata#1311).
- Window-wide stages such as global search, clipboard, and undo never see chooser keys (lgse/strata#1311).
- A Save always targets the current folder; neither the cursor nor Accept redirects it (lgse/strata#1311).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-30 | lgse/strata#1311 | feat | Shared the mode with the portal chooser under a per-request command policy and cleaned up mode exit and window lifetime. |

## Known gaps

None known.
