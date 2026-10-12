---
title: Preview sweep
reviewed_at: 0562724ad97c8e83a4c81b85e556bf275be3b025
tools: [docs/preview-sandbox.md, docs/document-previews.md, docs/preview-panel-layout.md, tests/fixtures/spreadsheets, tests/fixtures/documents]
---

## Scope

Everything the drawer shows for a selected file and how it gets there. The preview panel: which files preview, text, images, PDFs, 3D models, comic and EPUB covers, and Print. Layout covers width, the divider and resize edge, drawer motion, the reserved Columns slot, the shared right pane, and narrow windows. Documents covers Markdown, HTML, RTF, CSV, TSV, workbooks, DOCX, tables, images, diagrams, equations, and text selection. Find covers searching the open preview. Media covers the sandboxed player, autoplay, seeking, media keys, limits, and hardware backends, with the audio and video now-playing views. Sandbox covers bubblewrap launch, limits, decoding fallbacks, output validation, and the preview pool. Quick preview: Space, the menu item, single-click previews, selection following, filter results, and key ownership. Its child folder peek is the hover popover.

Left to other sweeps: thumbnails in the listing and the thumbnail worker pool, archive member listing and the archive preview, and preview keys in 10xer mode. Also media runtime packaging and launch dependencies, the Settings pages as controls, and mounting the remote locations that remote previews read.

## Setup

- Image samples under `/tmp` from ImageMagick: a 200 MP PNG (`magick -size 20000x10000 xc:gray`) and one with an EXIF thumbnail. Also a 12 MP ICC-profiled JPEG and an animated GIF over 30 s.
- Media samples from ffmpeg: a 4K HEVC 10-bit MP4 with chapters and two subtitle streams, an MP4 with `-vn`, one with `-an`, and a bare `.h264` stream. Also a VFR clip, 3.9 s and 4.1 s clips, a 2-hour FLAC, and a truncated faststart MP4 (`head -c`).
- Zero-byte files for every previewed extension. Lying extensions: an MP4 as `.jpg`, a PNG as `.pdf`, a ZIP as `.epub` and `.docx`, an ELF as `notes.txt`, a TIFF as `.ARW`.
- Documents: a 2000-page PDF, a 2 MiB text file (`head -c 2097152 /dev/urandom | base64 -w 76`), and a 20 MiB single-line file. Markdown at 1 MiB minus and plus one byte, a 300-column CSV, a CSV with 100,001 values, and the `any_sheets.*` and `report.docx` fixtures.
- `bwrap` present for the main pass. For fail-closed probes, launch again with `bwrap` dropped from `PATH`, then inside `unshare -rm` with `/dev/null` bound over `/usr/bin/bwrap`.
- Leak baseline before every helper-spawning probe: `pgrep -c bwrap`, `pgrep -fc 'ffmpeg|ffprobe'`, and `ls /proc/$(pgrep -x strata)/fd | wc -l`; repeat after and compare. `RUST_LOG=strata::sandbox::browser=debug` shows supervisor reuse.
- Backend values in `settings.toml`: `video_preview_backend` takes `automatic`, `vaapi`, or `vulkan`; `hardware_accelerated_video_previews = false` forces software. Hardware probes need a VA-API or Vulkan GPU; skip and say so without one.
- Keyboard layouts for key probes: `setxkbmap ru` (no Latin layout), `setxkbmap us,ru` with Russian active, and Caps Lock on; restore `us` afterwards.
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
- In a 600-line `.rs` preview and a plain-text file with a 2 KiB line, type letters, Backspace, Ctrl+V, and Ctrl+X.
- In the same files, press Shift+Down past the last line, then Ctrl+C.
- Zoom a PDF to 3× with Ctrl+wheel, then press Ctrl+keypad 0 with Num Lock on and off, and Ctrl+Shift+0.
- In a PDF, press Ctrl+A then Ctrl+C on the `ru` layout and with Caps Lock on.
- With a preview open, toggle 10xer mode from a second window, then read the close button's tooltip and accessible name in Accerciser.

### preview/preview-panel/layout

- Set a manual width, then toggle the sidebar, switch view mode, change folder, and open a second window; only the first window keeps it.
- In a 700 px window at 2× scaling, step Up and Down across folders and files 20 times and capture; the focused column must not move.
- Drag the divider below 300 px and past the window edge, and resize the window mid-drag.
- Narrow the window until a playing video hides, wait 35 s, widen; check frame, position, and sound.
- Toggle Appearance → Preview panel off and on ten times with overflowing columns; the scrollbar extent must match the real columns each time.
- Preview the 2000-page PDF in a 3000 px wide preview at 2× scaling; Ctrl+wheel to 4×, then narrow the window below 1280 px.
- In Icons and List, rest on the divider grip and drag it; compare the caption and outline with what the drag changes.
- At 1× and 2× scaling, press at 1 px steps from 7 px left to 7 px right of the column–preview line.
- Press Space three times within 260 ms in Icons with reduced motion on, then toggle Appearance → Preview panel mid-slide in Columns.
- With reduced motion off in List, press Space to close, then Space again at about 50 ms, 130 ms, and 250 ms into the slide-out.
- In Columns, drag the divider narrower, then wider, then use F8 and arrows; switch to Icons and back between each step.

### preview/preview-panel/documents

- Open the 1 MiB plus-one Markdown, the 300-column CSV, and the 100,001-value CSV; the fallback reason must be visible and the view switch hidden.
- Reference images from Markdown through a symlink escaping the folder, `../`, a percent-encoded Unicode name, and an 8 MiB plus-one PNG.
- Render a 257-line Mermaid block, a 4 KiB plus-one equation, prose containing `$5 and $10`, and an escaped `\$`.
- Open a 20 MiB plus-one XLSX, an XLSX whose first row has 300 columns, and the ZIP renamed `.docx`.
- Sort a table, drag-select a range, change the theme, then switch Source and Rendered while an image row is still rendering; close mid-render and check for leaked helpers.
- Double-click and triple-click a word split across two virtual rows, an emoji with a skin-tone modifier, a combining accent, and a link; Shift-click from prose into a table.
- Press Shift+End on a 2 KiB pathological line and Ctrl+Shift+Right through CJK text and punctuation runs, then Ctrl+C.
- On the `ru` layout, drag-select a table cell range, click one cell's text, then press Ctrl+C and Ctrl+A; repeat with Caps Lock on and on `us,ru`.
- In a table with a selected range, press Ctrl+Alt+C, Ctrl+Super+C, and keypad arrows, then Ctrl+C.

### preview/preview-panel/find

- Search a query spanning two virtual rows, one at 256 characters, German `ß`, and a lone combining accent.
- With find open, switch to Rendered on a table-only Markdown file and on a CSV, then switch back to Source.
- Search a large text file while it still loads, then Escape and reopen find before loading ends.
- In 10xer, press `/` in a small source, a large plain-text, and a rendered DOCX preview, then type `/` inside the find field.
- Open find in two windows on the same file with different queries; close the drawer in one.

### preview/preview-panel/media

- Play the `-vn` MP4, the `-an` MP4, an MP3 with only an attached picture, the VFR clip, and the truncated MP4; seek past the truncated file's real end.
- Change volume and mute in window A while window B plays; restart; compare `settings.toml` with what both players do.
- Start five players across two windows, pause one for 31 s, retry the fifth, then close a window holding two players.
- Run `automatic`, `vaapi`, `vulkan`, and acceleration off on the 4K HEVC 10-bit file; switch the setting mid-play and count ffmpeg processes per player.
- With autoplay on, select a 9 s clip, an 11 s clip, and a muted state; seek during the fade; let a 40 s GIF loop twice with four players active.
- With the timeline focused, press End then Right, Home then Left, and Page Up within 30 s of the end.
- With the timeline focused and Caps Lock on, press Shift+g and Shift+0, then keypad 0 with Num Lock on and off.
- With the timeline focused on the `ru` layout, press the keys in the `0`, `g`, `+`, and `-` positions.
- Drag the volume slider to 0.05, then press Down; press `-` while muted; press `+` in a second window during playback.
- Press Page Up/Down and Home/End on an animated GIF, a file with no reported duration, and the truncated MP4.
- Scroll the fallback seek slider with a touchpad.

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
- With a filter result selected, press Space, keypad Space, Ctrl+Space, and Alt+Space on the `ru` layout and with Caps Lock on.

### preview/quick-preview/folder-peek

- Hover a 10k-entry folder, a folder of only hidden files, a `chmod 000` folder, a symlink to a folder, and one on a slow sshfs mount.
- Hover with the viewport 250 px and 262 px wide, at 2× scaling, and on a folder at the Icons grid's right edge.
- Sweep folder to popover to an adjacent folder quickly; switch view mode mid-slide; press Escape, F5, and Ctrl+F with a peek open.
- Turn Folder peeking off from a second window's Settings while a peek is open in the first.

## Hand-offs

- Thumbnails in the listing and the thumbnail worker pool → `browser`.
- Selection kept or cleared by clicks on blank preview chrome and disabled preview controls → `browser`.
- F1 reference rows for preview find and media keys → `app`.
- Layout fallback, Caps Lock, keypad, and translated key names for every shortcut → `app`.
- Archive member listing and the archive preview → `operations`.
- Preview keys and track stepping in 10xer mode → `integration`.
- Media runtime packaging and GStreamer launch dependencies → `app`.
- The Settings controls for autoplay, backend, document rendering, and folder peeking → `settings`.
- Mounting the sftp, MTP, and camera locations that remote previews read → `remote`.
