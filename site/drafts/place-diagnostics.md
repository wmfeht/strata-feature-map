---
proposed: {page: new}
nodes: [settings/diagnostics]
reason: 'Settings → Diagnostics, its checks, install commands, and copyable report are user-visible, and no page names the node. The Settings guide covers settings.toml and a few preferences; no section covers troubleshooting. Upstream keeps this in docs/diagnostics.md ("What a run does"). Proposed as a "Diagnostics" reference page.'
release: v1.1.1
---

## Run diagnostics

**Settings → Diagnostics** ("Troubleshooting") checks the runtime pieces that
previews, locations, devices and desktop integration rely on. Opening the page
runs nothing. Select **Run**: rows start at "Checking…" and fill in as each check
finishes, then the summary reads "Passed: N · Warnings: N · Problems: N". No check
installs or changes anything; sample files go to a temporary
`strata-diagnostics-*` folder that is removed afterwards.

A row that is not passing and names a package shows "Install with:" and the
command for your distribution's pacman, apt, dnf or zypper, with **Run in
terminal**. Otherwise it reads "Install \<package> or your distribution's
equivalent." **Run in terminal** opens your terminal running the command; when it
ends the terminal prints "Press Enter to close." With no terminal found, the row
says "No terminal emulator was found." and how to configure one.

**Copy report** copies "Strata diagnostics", the System box, and every result by
group as `[Status] Title: message`, then shows "Copied" for 1.5 s. The System box
lists Version, Commit, Installation, Toolkit, GStreamer, Kernel, Desktop
environment, Display server, Interface renderer and Language.

## Checks

| Group | Check | Not passing when |
| --- | --- | --- |
| PREVIEW SANDBOX | Preview sandbox | No trusted `bwrap`, no `prlimit` at the sandbox's path, or a sample image fails to render (user namespaces may be disabled). Problem. |
| | Sandboxed workers | Landlock ABI 3 missing, so each thumbnail starts its own sandbox: warning. The pooled render fails: problem. |
| PREVIEWS | PDF thumbnails | A sample PDF fails to render. Problem. |
| | Video thumbnails | Neither `ffmpegthumbnailer` nor `ffmpeg`: problem. Only `ffmpeg`: warning that thumbnails load more slowly. |
| | Video and audio previews | `ffmpeg` or `ffprobe` missing. Problem. |
| | Audio playback | A GStreamer element or audio sink missing. Problem. Passing reads "Audio plays through \<sink>." |
| | RAW photos | None of `magick`, `convert`, `dcraw`, `simple_dcraw`: warning that RAW shows only its embedded preview. |
| | AppImage icons | No `unsquashfs`. Warning. |
| | Syntax highlighting | No GtkSourceView language definitions. Warning. |
| | File type detection | `.png` not recognized as `image/png`. Problem. |
| | RAR archives | A build without RAR support. Warning. |
| LOCATIONS AND DEVICES | GVfs | Launched with `GIO_USE_VFS=local`. Problem. |
| | SFTP, Windows shares (SMB), FTP, WebDAV, Android devices (MTP), iPhone and iPad, Cameras | GVfs lacks the backend. Warning; "Unavailable while GVfs isn't running." when GVfs is missing. |
| | Removable drives | UDisks2 or the GVfs UDisks2 volume monitor missing. Warning. |
| | Folder change monitoring | A folder monitor cannot start: problem. `fs.inotify.max_user_watches` below 8192: warning. |
| DESKTOP AND NETWORK | Desktop portal, Password storage | Their D-Bus service missing. Warning. |
| | Update server | `api.github.com` unreachable, so update checks and release notes are unavailable. Problem. |
| | Terminal | No terminal found. Problem. Passing reads "Found: \<program>". |
| | Custom actions | An enabled action cannot run, or an action folder fails to load. Warning. |

Helper tools are looked up on the sandbox's own path, not your `PATH`. **Run**
reloads custom actions first, so one added since startup is checked. A check that
never reports becomes a warning, "This check couldn't run."
