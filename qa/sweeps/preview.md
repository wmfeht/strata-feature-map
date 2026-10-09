---
title: Preview sweep
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
tools: [docs/preview-sandbox.md, docs/document-previews.md, docs/preview-panel-layout.md, tests/fixtures/spreadsheets, tests/fixtures/documents]
---

## Scope

Everything the drawer shows for a selected file and how it gets there. The preview panel: which files preview, text, images, PDFs, 3D models, comic and EPUB covers, and Print. Layout covers width, the reserved Columns slot, the shared right pane, and narrow windows. Documents covers Markdown, HTML, RTF, CSV, TSV, workbooks, DOCX, tables, images, diagrams, and equations. Media covers the sandboxed player, autoplay, seeking, limits, and hardware backends, with the audio and video now-playing views. Sandbox covers bubblewrap launch, limits, decoding fallbacks, output validation, and the preview pool. Quick preview: Space, the menu item, single-click previews, selection following, filter results, and key ownership. Its child folder peek is the hover popover.

Left to other sweeps: thumbnails in the listing and the thumbnail worker pool, archive member listing and the archive preview, and preview keys in 10xer mode. Also media runtime packaging and launch dependencies, the Settings pages as controls, and mounting the remote locations that remote previews read.

## Setup

- Image samples under `/tmp` from ImageMagick: a 200 MP PNG (`magick -size 20000x10000 xc:gray`) and one with an EXIF thumbnail. Also a 12 MP ICC-profiled JPEG and an animated GIF over 30 s.
- Media samples from ffmpeg: a 4K HEVC 10-bit MP4 with chapters and two subtitle streams, an MP4 with `-vn`, one with `-an`, and a bare `.h264` stream. Also a VFR clip, 3.9 s and 4.1 s clips, a 2-hour FLAC, and a truncated faststart MP4 (`head -c`).
- Zero-byte files for every previewed extension. Lying extensions: an MP4 as `.jpg`, a PNG as `.pdf`, a ZIP as `.epub` and `.docx`, an ELF as `notes.txt`, a TIFF as `.ARW`.
- Documents: a 2000-page PDF, a 2 MiB text file (`head -c 2097152 /dev/urandom | base64 -w 76`), and a 20 MiB single-line file. Markdown at 1 MiB minus and plus one byte, a 300-column CSV, a CSV with 100,001 values, and the `any_sheets.*` and `report.docx` fixtures.
- `bwrap` present for the main pass. For fail-closed probes, launch again with `bwrap` dropped from `PATH`, then inside `unshare -rm` with `/dev/null` bound over `/usr/bin/bwrap`.
- Leak baseline before every helper-spawning probe: `pgrep -c bwrap`, `pgrep -fc 'ffmpeg|ffprobe'`, and `ls /proc/$(pgrep -x strata)/fd | wc -l`; repeat after and compare. `RUST_LOG=strata::sandbox::browser=debug` shows supervisor reuse.
- Backend values in `settings.toml`: `video_preview_backend` takes `automatic`, `vaapi`, or `vulkan`; `hardware_accelerated_video_previews = false` forces software. Hardware probes need a VA-API or Vulkan GPU; skip and say so without one.
- Reduce motion and Element glow each on and off, under the GL renderer and `GSK_RENDERER=cairo`. Two windows of the same build on one media folder for volume sync, the four-player cap, and width isolation.

## Probes

- Run each probe in Columns, Icons, and List, and once in the file chooser, which shares the drawer.
- After each probe that spawned a helper, compare `pgrep bwrap` and the fd count with the baseline; a helper outliving its preview is a finding.
- Move the selection faster than the 75 ms debounce across 200 mixed files and watch for GTK criticals and stale frames.

### preview/preview-panel

- Select each zero-byte sample; every one must settle to empty text or a message, never a spinner or a crash.
- Select each lying-extension sample; nothing may render as the extension claims, and the ELF named `notes.txt` must not be executed or previewed as a binary dump.
- Open the 2000-page PDF, press End, scroll back fast, Ctrl+A then Ctrl+C, then Print and cancel near page 500.
- Toggle word wrap on the 20 MiB single-line file in one window while the other shows the 2 MiB text file; check the 1 MiB cap in both.
- Preview the 200 MP PNG with and without an EXIF thumbnail, a 3MF with two usable PNGs, and a CBZ whose first entry is a folder.

### preview/preview-panel/layout

- Set a manual width, then toggle the sidebar, switch view mode, change folder, and open a second window; only the first window keeps it.
- In a 700 px window at 2× scaling, step Up and Down across folders and files 20 times and capture; the focused column must not move.
- Drag the divider below 300 px and past the window edge, and resize the window mid-drag.
- Narrow the window until a playing video hides, wait 35 s, widen; check frame, position, and sound.
- Toggle Appearance → Preview panel off and on ten times with overflowing columns; the scrollbar extent must match the real columns each time.

### preview/preview-panel/documents

- Open the 1 MiB plus-one Markdown, the 300-column CSV, and the 100,001-value CSV; the fallback reason must be visible and the view switch hidden.
- Reference images from Markdown through a symlink escaping the folder, `../`, a percent-encoded Unicode name, and an 8 MiB plus-one PNG.
- Render a 257-line Mermaid block, a 4 KiB plus-one equation, prose containing `$5 and $10`, and an escaped `\$`.
- Open a 20 MiB plus-one XLSX, an XLSX whose first row has 300 columns, and the ZIP renamed `.docx`.
- Sort a table, drag-select a range, change the theme, then switch Source and Rendered while an image row is still rendering; close mid-render and check for leaked helpers.

### preview/preview-panel/media

- Play the `-vn` MP4, the `-an` MP4, an MP3 with only an attached picture, the VFR clip, and the truncated MP4; seek past the truncated file's real end.
- Change volume and mute in window A while window B plays; restart; compare `settings.toml` with what both players do.
- Start five players across two windows, pause one for 31 s, retry the fifth, then close a window holding two players.
- Run `automatic`, `vaapi`, `vulkan`, and acceleration off on the 4K HEVC 10-bit file; switch the setting mid-play and count ffmpeg processes per player.
- With autoplay on, select a 9 s clip, an 11 s clip, and a muted state; seek during the fade; let a 40 s GIF loop twice with four players active.

### preview/preview-panel/media/audio

- In a 1000-track folder, hold `>` for 10 s; then check `pgrep -f audio-peaks`, the bwrap count, the fd count, and that the caption matches where it stopped.
- Art precedence: embedded back cover only, `Folder.JPG` in uppercase, `cover.webp` beside `albumart.png`, a zero-byte `cover.jpg`, and a `cover.jpg` that is an MP4.
- Tags with a 300-character title, bidirectional override characters, embedded newlines, and a track number with no total.
- Drag the divider slowly through the 0.95 to 1.12 aspect band while playing; no restart, no layout thrash.
- Play the 2-hour FLAC, seek past the decoded waveform, then select an `.ogg` carrying a real video stream.

### preview/preview-panel/media/video

- Sidecars `clip.en.vtt`, `clip.srt`, `CLIP.SRT`, `clip.en.forced.ass`, and a directory named `clip.sub`; compare the badge count with `ffprobe`.
- Storyboard on the 3.9 s and 4.1 s clips, a 2-hour clip, and a clip with one keyframe; scrub while cells arrive and hover a chapter with a 200-character title.
- Hand off at 0:00, at 0:00.5, 1 s before the end, and mid-clip, with mpv, VLC, a non-listed player, and no default player.
- Element glow on and off under Cairo and GL; toggle reduce motion mid-fade; pause and confirm the band freezes.
- Double-click a video in Icons while another video's preview is mid-load, then press play in the preview.

### preview/preview-panel/sandbox

- With `bwrap` dropped from `PATH`, every native preview must still work; with `/dev/null` over `/usr/bin/bwrap`, image, PDF, SVG, DOCX, model, video, and GIF must each fail closed with no decoder in `ps`.
- Place a `bwrap` symlink earlier in the trusted roots pointing under `/home`; it must be rejected.
- Feed a 512 MiB plus-one PNG, a header claiming 100000×100000, an SVGZ with external image references, a gzip bomb as `.svgz`, and the TIFF named `.ARW`.
- Open and close a RAW preview 50 times within 1 ms of each other; compare the bwrap count and the fd list with the baseline.
- Preview 20 images inside 60 s under the debug log and count `browser sandbox started` lines; wait 61 s and preview once more.

### preview/quick-preview

- Press Space with the caret in the filter input and a result selected, then on a mixed file-and-folder selection. Press Space on a symlink to a folder and on a broken symlink.
- Hold Down through 500 files for 5 s with the preview open; only the landing file may load, per the log.
- `rm` the previewed file from a shell while a video plays, while a PDF print dialog is open, and remove its parent folder.
- With Single-click file previews off, click, double-click, and start a drag on a supported file; no preview may open.
- Press Right into a PDF preview in List, then Ctrl+A, Ctrl+C, Delete, and Ctrl+X; the folder's file count must not change.

### preview/quick-preview/folder-peek

- Hover a 10k-entry folder, a folder of only hidden files, a `chmod 000` folder, a symlink to a folder, and one on a slow sshfs mount.
- Hover with the viewport 250 px and 262 px wide, at 2× scaling, and on a folder at the Icons grid's right edge.
- Sweep folder to popover to an adjacent folder quickly; switch view mode mid-slide; press Escape, F5, and Ctrl+F with a peek open.
- Turn Folder peeking off from a second window's Settings while a peek is open in the first.

## Hand-offs

- Thumbnails in the listing and the thumbnail worker pool → `browser`.
- Archive member listing and the archive preview → `operations`.
- Preview keys and track stepping in 10xer mode → `integration`.
- Media runtime packaging and GStreamer launch dependencies → `app`.
- The Settings controls for autoplay, backend, document rendering, and folder peeking → `settings`.
- Mounting the sftp, MTP, and camera locations that remote previews read → `remote`.
