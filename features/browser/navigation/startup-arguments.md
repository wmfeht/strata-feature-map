---
title: Startup location arguments
status: shipped
origin: {issue: lgse/strata#649, pr: lgse/strata#673}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: reviewed
code: [src/ui/window/open_argument.rs]
tests: [src/ui/window/open_argument/tests.rs, tests/e2e/scenarios/test_startup_arguments.py]
related: [integration/file-manager-interface, remote/file-providers]
---

## Summary

Opening the paths and URIs given to `strata` on the command line, for example from a terminal, `xdg-open`, or a launcher's `Exec=strata %U`. Folders open directly and files open in their parent with the file selected.

## Behavior

### Arguments

- Each argument opens its own window, both at launch and when Strata is already running. lgse/strata#673, lgse/strata#725
- A path whose name is not valid UTF-8 opens normally instead of aborting Strata. lgse/strata#673
- `trash:///`, `smb://`, and `sftp://` arguments open the requested location instead of the home folder. lgse/strata#673
- A file argument opens its parent folder with that file selected; a `file://` URI behaves the same. lgse/strata#725
- A broken symlink argument is selected in its parent, and a symlink to a folder opens that folder. lgse/strata#725
- A remote file URI such as `sftp://host/share/file.txt` opens its parent with the file selected. lgse/strata#755
- When two non-UTF-8 file names map to the same displayed name, only the named file is selected. lgse/strata#1499
- An unmounted remote argument is mounted first, using the desktop's sign-in prompt when needed. lgse/strata#755, lgse/strata#726

### Feedback

- The window appears before Strata knows whether the argument is a file or a folder, and stays responsive. lgse/strata#755
- If that check is still running after 1 second, the pane shows a spinner, "Connecting to location…", and Cancel. lgse/strata#755
- Cancel stops waiting, ignores any late result, and opens the home folder. lgse/strata#755, lgse/strata#726 (unverified)
- A missing or unreadable argument shows "The requested location is unavailable" with its path and a Retry button instead of a dialog. lgse/strata#755
- Retry checks the argument again, so a folder created after the failure opens. lgse/strata#755
- An unavailable `sftp://user:secret@host/file.txt` argument shows `sftp://user@host/file.txt` in the error, never the password. lgse/strata#755 (unverified)
- Navigating elsewhere or closing the window during the check abandons it without later navigation or errors. lgse/strata#755
- Launching with stdout or stderr connected to a closed pipe still opens the window instead of aborting. lgse/strata#1399

## Design

Arguments use the same location mapping as the `org.freedesktop.FileManager1` adapter, so remote URIs keep their identity (lgse/strata#649).

- Arguments are read with `args_os`; the launch-mode dispatch is byte-safe, so only internal helper modes require UTF-8 (lgse/strata#649, lgse/strata#673).
- Arguments are never combined, even when they share a parent folder (lgse/strata#725).
- File-or-folder classification runs as an async GIO query, never a blocking `stat`, because an NFS or CIFS path can stall the main thread (lgse/strata#726).
- Feedback is delayed and inline: no status for the first second, then cancellable status. A failure shows an inline error with Retry. Elapsed time alone never fails a request (lgse/strata#726).
- The per-window navigation generation invalidates a pending check. A blocked kernel call cannot be stopped, so late results are ignored rather than assumed to end (lgse/strata#726).
- FileManager1 `ShowItems` and `ShowFolders` skip classification, because the method already says whether the target is a file (lgse/strata#755).
- The activate, open, and command-line handlers catch panics, and log output ignores broken pipes, so no panic crosses the GLib signal boundary (lgse/strata#1391).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-03 | lgse/strata#1399 | fix | Survived closed stdout or stderr pipes at startup by swallowing broken-pipe writes and catching handler panics. |
| 2026-09-10 | lgse/strata#755 | fix | Classified arguments asynchronously with delayed Connecting feedback, Cancel, and inline Retry. |
| 2026-09-10 | lgse/strata#725 | fix | Revealed file arguments in their parent instead of opening them as folders. |
| 2026-09-09 | lgse/strata#673 | fix | Opened every argument, kept non-UTF-8 paths, and kept remote URIs instead of falling back to home. |

## Known gaps

None known.
