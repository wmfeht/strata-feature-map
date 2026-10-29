---
title: Diagnostics
status: shipped
origin: {issue: lgse/strata#1734, pr: lgse/strata#1735}
branch: null
reviewed_at: 86df474dc0e8352e0e2098637a017cc4c77a8c44
review: reviewed
code: [src/services/diagnostics.rs, src/ui/settings/diagnostics.rs, data/icons/scalable/actions/strata-stethoscope.svg]
tests: [src/services/diagnostics/tests.rs, src/ui/settings/diagnostics/tests.rs]
docs: [docs/diagnostics.md]
related: [settings/preferences, app/infrastructure, preview/preview-panel/sandbox, browser/thumbnails/workers, preview/preview-panel/media, operations/archives/rar, app/updates, devices/volumes/drive-dialogs, integration/open-with/terminal, integration/custom-actions]
---

## Summary

Settings → Diagnostics, an on-demand page that checks the runtime pieces previews, locations, devices, and desktop integration rely on. Each check reports passed, warning, or problem with an install command for the detected distribution, and the results copy as a report for bug reports.

## Behavior

### Page and run

- Diagnostics appears in the Settings navigation with the subtitle "Troubleshooting" and a stethoscope icon. lgse/strata#1735
- Opening Diagnostics runs no check; it shows the Run diagnostics row with its description, a disabled Copy report button, and a Run button. lgse/strata#1735
- Selecting Run disables Run and Copy report and shows "Running checks…". lgse/strata#1735
- Run builds a System box and four groups: PREVIEW SANDBOX, PREVIEWS, LOCATIONS AND DEVICES, and DESKTOP AND NETWORK. lgse/strata#1735 (unverified)
- Run reloads the custom-action catalog, so an action added since startup is checked. lgse/strata#1735 (unverified)
- Every row starts at "Checking…" and fills in as its check finishes. lgse/strata#1735
- When all checks end, the summary reads "Passed: N · Warnings: N · Problems: N", and Run and Copy report are enabled again. lgse/strata#1735
- A check that never reports a result becomes a warning reading "This check couldn't run." lgse/strata#1735 (unverified)
- When the sample directory cannot be created, the five sample-based checks read "This check couldn't run." with the I/O error. They are Preview sandbox, Sandboxed workers, PDF thumbnails, Video thumbnails, and Video and audio previews. lgse/strata#1735 (unverified)
- No check changes or installs anything; sample files go to a temporary `strata-diagnostics-*` directory that is removed afterwards. lgse/strata#1735

### Preview checks

- With no trusted `bwrap`, Preview sandbox is a problem naming Bubblewrap, with the bubblewrap package. lgse/strata#1735
- With `prlimit` missing at the sandbox's path, Preview sandbox is a problem naming that path, with the util-linux package. lgse/strata#1735, lgse/strata#1746
- Otherwise a generated PNG renders through a one-shot sandbox; a failure reports that unprivileged user namespaces may be disabled or restricted. lgse/strata#1735
- Without Landlock ABI 3, Sandboxed workers is a warning that each thumbnail starts its own sandbox; otherwise the PNG renders through the pooled workers. lgse/strata#1735
- When the pooled render fails, Sandboxed workers is a problem reading "A sandboxed worker couldn't render a sample image." lgse/strata#1735 (unverified)
- PDF thumbnails passes with "A sample file was processed correctly." when a sample PDF renders through the pooled thumbnail path. Otherwise it is a problem with the error as detail. lgse/strata#1735
- With neither `ffmpegthumbnailer` nor `ffmpeg` on the sandbox path, Video thumbnails is a problem. lgse/strata#1735
- With only `ffmpeg`, a passing render makes Video thumbnails a warning that video thumbnails load more slowly. A failing render is a problem; both offer the ffmpegthumbnailer package. lgse/strata#1735 (unverified)
- With `ffmpeg` or `ffprobe` missing, Video and audio previews is a problem naming each missing tool; otherwise FFprobe reads a sample WAV. lgse/strata#1735
- A missing GStreamer element among `appsrc`, `audioconvert`, `audioresample`, `volume`, and `autoaudiosink`, or no audio sink, makes Audio playback a problem. lgse/strata#1735
- When GStreamer fails to start, Audio playback is a problem reading "GStreamer couldn't start." with the GStreamer base plugins package. lgse/strata#1735 (unverified)
- When Audio playback passes, it reads "Audio plays through <sink>." with the highest-ranked sink. lgse/strata#1735
- With none of `magick`, `convert`, `dcraw`, or `simple_dcraw`, RAW photos is a warning that RAW photos show only their embedded preview. lgse/strata#1735
- Without `unsquashfs`, AppImage icons is a warning with the squashfs-tools package. lgse/strata#1735
- With no GtkSourceView language definitions, Syntax highlighting is a warning that code previews show plain text. lgse/strata#1735
- When a `.png` name is not recognized as `image/png`, File type detection is a problem with the shared-mime-info package. lgse/strata#1735
- In a build without RAR support, RAR archives is a warning reading "This build doesn't include RAR support." lgse/strata#1735

### Location, device, and desktop checks

- Launched with `GIO_USE_VFS=local`, GVfs is a problem saying the session uses local files only, with no install command. lgse/strata#1735
- SFTP, Windows shares (SMB), FTP, WebDAV, Android devices (MTP), iPhone and iPad, and Cameras pass when GVfs lists their URI scheme. Otherwise each is a warning with its backend package. lgse/strata#1735
- While GVfs is bypassed or missing, each of those backends is a warning reading "Unavailable while GVfs isn't running." lgse/strata#1735
- With `org.freedesktop.UDisks2` absent from the system bus, Removable drives is a warning with the udisks2 package. lgse/strata#1735
- With UDisks2 present but the GVfs UDisks2 volume monitor absent from the session bus, Removable drives is a warning with the GVfs daemons package. lgse/strata#1735
- With `org.freedesktop.portal.Desktop` or `org.freedesktop.secrets` absent from the session bus, Desktop portal or Password storage is a warning. lgse/strata#1735
- With no D-Bus session bus, Desktop portal and Password storage, and Removable drives when UDisks2 is present, are warnings reading "The D-Bus session bus isn't available." lgse/strata#1735 (unverified)
- When a folder monitor cannot start, Folder change monitoring is a problem; with `fs.inotify.max_user_watches` below 8192, it is a warning naming the limit. lgse/strata#1735 (unverified)
- Update server passes as "Connected to GitHub." when `api.github.com/rate_limit` answers. Otherwise it is a problem saying update checks and release notes are unavailable, with the network error. lgse/strata#1735
- With no terminal found, Terminal is a problem; otherwise it reads "Found: <program>". lgse/strata#1735
- An enabled custom action that cannot run, or an action directory that fails to load, makes Custom actions a warning. With none installed it passes. lgse/strata#1735

### Fixes and report

- A non-passing row with a package shows "Install with:" and the install command for the distribution in `os-release`: pacman, apt, dnf, or zypper. lgse/strata#1735
- When the distribution has no known command, the row reads "Install <package> or your distribution's equivalent." with the Arch package name. lgse/strata#1735
- After Run in terminal opens a row's install command, the row reads "The command opened in your terminal. Run diagnostics again when it finishes." lgse/strata#1735, lgse/strata#1704
- Copy report copies "Strata diagnostics", the System fields, and every result by group as `[Status] Title: message`, then shows "Copied" for 1.5 s. lgse/strata#1735 (unverified)
- The System box lists Version, Commit, Installation, Toolkit, GStreamer, Kernel, Desktop environment, Display server, Interface renderer, and Language. lgse/strata#1735

### Run in terminal

- Every install command on Settings → Diagnostics and Settings → Integrations shows a Run in terminal button, with or without a terminal emulator. lgse/strata#1729
- Run in terminal opens the user's terminal running the install command. lgse/strata#1735, lgse/strata#1704
- With no terminal emulator found, Run in terminal shows "No terminal emulator was found." under the command. It suggests `xdg-terminal-exec` with `~/.config/xdg-terminals.list`, setting `$TERMINAL`, or a listed terminal. lgse/strata#1729 (unverified)
- When the install command ends, the terminal prints "Press Enter to close." and stays open until Enter. lgse/strata#1735, lgse/strata#1704

## Design

[docs/diagnostics.md](https://github.com/lgse/strata/blob/fd6327265eaa3266f8420fe8bd25e965146344b0/docs/diagnostics.md) describes the checks and how to add one.

- A missing runtime piece used to show only as "Preview unavailable", a plain icon, or a missing entry, with no cause in the app (lgse/strata#1734).
- Checks exercise the feature itself, such as a real sandbox, the worker pool, and the thumbnail path, rather than only looking for binaries (lgse/strata#1734, lgse/strata#1735).
- Helper tools are looked up on the sandbox's configured `STRATA_SANDBOX_PATH`, not the user's `PATH`, because helpers run inside the sandbox (lgse/strata#1735, lgse/strata#1746).
- The update check uses `api.github.com/rate_limit` because that request does not count against the rate limit (lgse/strata#1735).
- Run in terminal passes the prompt and the command's words as positional arguments to a fixed `sh -c` script. The shell never parses them as syntax. Package names with options or shell syntax therefore get no install command (lgse/strata#1735, lgse/strata#1704).
- Linked libraries such as GTK, Poppler, and GStreamer core cannot be checked in-app, because the loader fails first (docs/diagnostics.md).
- The package manager and the terminal are resolved on a blocking worker when Run starts, and the copied report reuses that package manager (lgse/strata#1729).
- Checks that need GTK objects run on the GTK thread. The rest run on workers that a timer polls through a weak page reference (lgse/strata#1735).
- A `--diagnose` command-line flag was rejected as less discoverable, and docs-only troubleshooting because it cannot see the environment or the sandbox (lgse/strata#1734).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-17 | lgse/strata#1735 | feat | Added a Diagnostics page that checks runtime dependencies and copies a report, so missing pieces have an in-app cause and fix. |

## Known gaps

None known.
