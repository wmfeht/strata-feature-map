---
title: Clipboard exchange with other file managers
status: shipped
origin: {issue: lgse/strata#2028, pr: lgse/strata#2040}
branch: null
reviewed_at: bae71c026b94e109b7507c4fe895c3ceed642f8f
review: reviewed
code: [src/ui/browser/clipboard/formats.rs]
tests: [src/ui/browser/clipboard/formats/tests.rs]
related: [app/shortcut-reference, browser/context-menu]
---

## Summary

The clipboard formats Strata offers on copy and cut, and reads back on paste. Files copied or cut in Strata paste in Nautilus, Nemo, Caja, Thunar, Dolphin, and desktop icon extensions. A cut made there stays a move in Strata.

## Behavior

### Offering files

- Ctrl+C or Ctrl+X on a selection offers a GDK file list, `text/uri-list`, `x-special/gnome-copied-files`, and `application/x-kde-cutselection` together. lgse/strata#2040
- The `text/uri-list` payload holds one URI per line, each ending in CRLF. lgse/strata#2040
- After Ctrl+C, the GNOME payload is `copy` followed by one URI per line, with no trailing newline, and the KDE flag is `0`. lgse/strata#2040
- After Ctrl+X, the GNOME payload starts with `cut` and the KDE flag is `1`. lgse/strata#2040
- A file copied in Strata can be pasted in Nemo, Caja, Thunar, and the GNOME Desktop Icons NG extension. lgse/strata#2034, lgse/strata#2040
- A file cut in Strata and pasted in Dolphin or Nautilus is moved, not copied. lgse/strata#2040
- After a paste consumes part of a cut, the clipboard keeps the remaining items with the `cut` header and the KDE flag `1`. lgse/strata#2040 (unverified)

### Reading files

- Ctrl+V on a clipboard whose `x-special/gnome-copied-files` starts with `cut` moves the files; one starting with `copy` copies them. lgse/strata#2040
- Ctrl+V on a `text/uri-list` clipboard with `application/x-kde-cutselection` set to `1` moves the files. With `0`, or with no KDE flag, it copies them. lgse/strata#2040
- When both formats are offered, a GNOME payload whose first line is `cut` or `copy` decides, whatever the KDE flag says. lgse/strata#2040 (unverified)
- A GNOME payload whose first line is neither `cut` nor `copy`, or that names no file, is ignored; the file list and the KDE flag decide. lgse/strata#2040 (unverified)
- A GNOME payload with CRLF line endings or a trailing newline is read the same as one with plain newlines. lgse/strata#2040 (unverified)
- A clipboard offering only `x-special/gnome-copied-files`, with no file list or `text/uri-list`, still pastes on Ctrl+V. lgse/strata#2040 (unverified)
- A cut made in Strata still pastes as a move when the clipboard carries no cut marker, because the paste also checks Strata's own cut list. lgse/strata#2040 (unverified)
- A cut made in another running Strata process pastes as a move. lgse/strata#2040 (unverified)

## Design

- GTK advertises a `GdkFileList` only as `text/uri-list` and plain text. Nemo, Caja, Thunar, and Desktop Icons NG, the version Ubuntu 24.04 and Zorin 18 ship, enable Paste only when `x-special/gnome-copied-files` is offered (lgse/strata#2028, lgse/strata#2034, lgse/strata#2040).
- KDE reads `text/uri-list` but takes its cut flag from `application/x-kde-cutselection`, so a Strata cut pasted in Dolphin as a copy (lgse/strata#2040).
- Nautilus falls back to the file list, which is why stock GNOME never showed the problem (lgse/strata#2040).
- Strata offers the union of all formats so every file manager can paste. Paste reads the GNOME header or the KDE flag first, so a foreign cut moves (lgse/strata#2040).
- The clipboard marker serves other applications. Strata's process-wide cut list stays the source of truth for row marks and its own pastes (lgse/strata#2040).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |

## Known gaps

None known.
