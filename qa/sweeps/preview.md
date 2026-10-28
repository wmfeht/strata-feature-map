---
title: Preview sweep
reviewed_at: 73b3258ff9da7fd5f8b279e442e4fbf576850deb
tools: [docs/preview-sandbox.md, docs/document-previews.md, docs/preview-panel-layout.md, tests/fixtures/spreadsheets, tests/fixtures/documents, docs/testing.md, tests/qa/keyboard.rs, tests/fixtures/harness.json]
---

## Scope

Everything the drawer shows for a selected file and how it gets there. The preview panel: which files preview, text, images, PDFs including password-protected ones and zoom, comic and EPUB covers, and Print. PDF text selection is its own child. G-code covers embedded slicer thumbnails. Routes cover GPX, FIT, and KML playback, the elevation profile, and units. Layout covers width, the divider and resize edge, drawer motion, the reserved Columns slot, the shared right pane, and narrow windows. Documents covers Markdown, HTML, RTF, CSV, TSV, workbooks, DOCX, ODT, tables, images, diagrams, equations, and text selection. Its scrollbar child covers the document-position thumb and momentum. Find covers searching the open preview. Media covers the sandboxed player, autoplay, seeking, media keys, limits, and hardware backends, with the audio and video now-playing views. Model views cover STL, 3MF, and FreeCAD rendering, embedded thumbnails, model limits, the camera controls, orbit indicator, and mesh badges. Sandbox covers bubblewrap launch, trusted helper directories, launch-time runtime paths, limits, decoding fallbacks, output validation, the orphaned output-folder sweep, and the preview pool. Quick preview: Space, the menu item, single-click previews, selection following, filter results, and key ownership. Its child folder peek is the hover popover.

Left to other sweeps: thumbnails in the listing and the thumbnail worker pool, archive member listing and the archive preview, and preview keys in 10xer mode. Also media runtime packaging and launch dependencies, the Settings pages as controls, and mounting the remote locations that remote previews read.

## Setup

- Image samples under `/tmp` from ImageMagick: a 200 MP PNG (`magick -size 20000x10000 xc:gray`) and one with an EXIF thumbnail. Also a 12 MP ICC-profiled JPEG and an animated GIF over 30 s.
- Media samples from ffmpeg: a 4K HEVC 10-bit MP4 with chapters and two subtitle streams, an MP4 with `-vn`, one with `-an`, and a bare `.h264` stream. Copy the raw stream as `.H264`, `.264`, `clip.h264.txt`, and with no extension; encode an HEVC stream with `-c:v libx265` as `.h265` and `.hevc`. Put plain text in `notes.h264`. Also a VFR clip, 3.9 s and 4.1 s clips, a 2-hour FLAC, and a truncated faststart MP4 (`head -c`).
- Byte-sniffing samples: an MPEG-TS clip (`ffmpeg -f lavfi -i testsrc2=duration=3 -f mpegts recording.ts`) and TypeScript as `app.ts` and `Component.tsx`. Also a UTF-16 BE text file with and without a BOM, and text files named `.xlsx` and `.odt`.
- RAW samples: a lossless compressed Fuji X-T5 `.RAF`, a Pentax portrait `.DNG`, a GoPro `.GPR`, and an uppercase `.ARQ`. Also a JPEG panorama over 134 MP (`magick -size 42374x10529 xc:gray pano.jpg`) with and without a small EXIF thumbnail. Hide `dcraw`, `simple_dcraw`, and ImageMagick in turn by bind-mounting `/dev/null` over them inside `unshare -rm`.
- Model samples: a binary STL, a one-triangle ASCII STL, and an STL just under 2 million triangles. Also a geometry-only 3MF, a 3MF with one embedded PNG, one with two, and a FreeCAD file with and without a thumbnail. Pad an STL to 128 MiB and to 128 MiB plus one byte.
- PDF text samples: `tests/fixtures/documents/text.pdf`, a PDF mixing scanned and text pages, and a right-to-left PDF.
- G-code samples: the `mini_cube_*` `.gcode` and `.bgcode` files from `prusa3d/libbgcode` `tests/data`, a text G-code with no thumbnail, and one appending 2 GiB of toolpath. Also one whose thumbnail block starts just before 2 MiB, one with a 5 MiB thumbnail, and a `.bgcode` with a compressed thumbnail block.
- Route samples, synthetic only, never personal activity files: a timed GPX with altitude, a GPX crossing the date line, one at 89° latitude, and one with 250,001 points. Also a 32 MiB plus one byte GPX, a KML of only polygons, a KMZ, a GPX with a DOCTYPE entity, and a FITS image named `.fit`.
- PDFs from `tests/fixtures/documents` with `qpdf`: `password-protected.pdf`, `owner-restricted.pdf`, and an RC4 40-bit copy needing the password `preview`.
- For the output-folder sweep, a toolbox or distrobox container sharing `/tmp` with a second Strata build, and a `strata-preview-<pid>-<n>` folder owned by another user.
- Zero-byte files for every previewed extension. Lying extensions: an MP4 as `.jpg`, a PNG as `.pdf`, a ZIP as `.epub`, `.docx`, and `.odt`, an ELF as `notes.txt`, a TIFF as `.ARW`.
- Documents: a 2000-page PDF, a 2 MiB text file (`head -c 2097152 /dev/urandom | base64 -w 76`), and a 20 MiB single-line file. Markdown at 1 MiB minus and plus one byte, a 300-column CSV, a CSV with 100,001 values, and the `any_sheets.*`, `report.docx`, and `report.odt` fixtures. Generated Markdown of 400 blocks cycling headings, prose, fenced code, tables, and lists, plus a copy with relative PNGs beside it.
- ODT samples: `report.odt` copied as `report.ott` and `REPORT.ODT`. From LibreOffice Writer, a table without a header-row group, and one with two header rows and a merged cell. Also an ODT with a 5,000-character paragraph, and one with a heading at outline level 9 and lists nested 8, 9, and 10 levels. Also a link inside `Preformatted Text`, a `mailto:` link, and a file over 20 MiB. From pandoc, an ODT whose tables hold many short bold paragraphs per cell.
- A second build with `STRATA_TRUSTED_COMMAND_PATH` set, and a prebuilt binary to launch with `STRATA_SANDBOX_*` variables; `RUST_LOG=strata::sandbox=warn` shows ignored overrides.
- `bwrap` present for the main pass. For fail-closed probes, launch again with `bwrap` dropped from `PATH`, then inside `unshare -rm` with `/dev/null` bound over `/usr/bin/bwrap`.
- Leak baseline before every helper-spawning probe: `pgrep -c bwrap`, `pgrep -fc 'ffmpeg|ffprobe'`, and `ls /proc/$(pgrep -x strata)/fd | wc -l`; repeat after and compare. `RUST_LOG=strata::sandbox::browser=debug` shows supervisor reuse.
- Backend values in `settings.toml`: `video_preview_backend` takes `automatic`, `vaapi`, or `vulkan`; `hardware_accelerated_video_previews = false` forces software. Hardware probes need a VA-API or Vulkan GPU; skip and say so without one.
- Keyboard layouts for key probes, on the test display only, never the desktop: `setxkbmap -display :N ru` (no Latin layout), `setxkbmap -display :N -layout us,ru` with the group locked to Russian, and Caps Lock on. In a QA scenario, `{"layout":"ru-only"}`, `{"layout":"ru"}`, and `{"layout":"caps-lock"}` steps match those three setups through `tests/qa/keyboard.rs`. They read the layouts in `tests/fixtures/harness.json`, and `us` is restored afterwards. `docs/testing.md` "Keyboard layouts" has the rules.
- An NFS or SMB mount holding a music folder, a RAW folder, and a model folder with the FreeCAD file and the embedded-PNG 3MF, for probes that rename or delete what the preview reads.
- For STL model thumbnails, a folder of 20 STLs on an NFS mount at a native path, not a GVfs SMB share. Also a local folder of 20 STLs.
- Reduce motion and Element glow each on and off, under the GL renderer and `GSK_RENDERER=cairo`. Two windows of the same build on one media folder for volume sync, the four-player cap, and width isolation.

## Probes

- Run each probe in Columns, Icons, and List, and once in the file chooser, which shares the drawer.
- After each probe that spawned a helper, compare `pgrep bwrap` and the fd count with the baseline; a helper outliving its preview is a finding.
- Move the selection faster than the 75 ms debounce across 200 mixed files and watch for GTK criticals and stale frames.

### preview/preview-panel

- Select each zero-byte sample; every one must settle to empty text or a message, never a spinner or a crash.
- Preview the text named `.odt`.
- Preview `report.odt`, `report.ott`, and `REPORT.ODT` from a remote mount.
- Open the 5,000-character ODT paragraph in one window, then toggle wrap 10 times from a text preview in a second window.
- Select each lying-extension sample; nothing may render as the extension claims, and the ELF named `notes.txt` must not be executed or previewed as a binary dump.
- Open the 2000-page PDF, press End, scroll back fast, Ctrl+A then Ctrl+C, then Print and cancel near page 500.
- Toggle word wrap on the 20 MiB single-line file in one window while the other shows the 2 MiB text file; check the 1 MiB cap in both.
- Preview the 200 MP PNG with and without an EXIF thumbnail, and a CBZ whose first entry is a folder.
- In a 600-line `.rs` preview and a plain-text file with a 2 KiB line, type letters, Backspace, Ctrl+V, and Ctrl+X.
- In the same files, press Shift+Down past the last line, then Ctrl+C.
- Zoom a PDF to 3× with Ctrl+wheel, then press Ctrl+keypad 0 with Num Lock on and off, and Ctrl+Shift+0.
- Preview the UTF-16 BE samples with and without a BOM, and the text named `.xlsx`.
- Preview a Latin-1 file whose control bytes are just over 1 in 32, and one just under.
- Preview MP4 and Ogg bytes named `.txt` and `.md`.
- Arm a 10xer chord, then press Ctrl+0 in a zoomed PDF in the main window.
- Ctrl+wheel with a touchpad over a PDF's scrollbar, on X11 and on Wayland.
- With a preview open, toggle 10xer mode from a second window, then read the close button's tooltip and accessible name in Accerciser.
- Preview the `.GPR` and `.ARQ` samples from a local folder and from an sftp mount.
- Play a song from a folder on the network mount, reached once directly and once through a symlinked folder; rename the folder from a second window, then Shift+Delete it.
- With a video playing, paste a large file into the same folder, then rename a sibling of the playing file.
- Move the cursor onto a file in a folder that a slow move to another disk is copying, during and after the move.
- Preview `password-protected.pdf` from an sftp mount, and its RC4 copy.
- Preview the text G-code without a thumbnail and a `.bgcode` from an sftp mount.
- With a model in one window and a route in another, narrow both until their previews hide, change the theme twice, then widen both.
- Dump the media bar in a playing video and in an audio preview, which the naming scenarios skip.
- Preview the raw stream copies and `notes.h264`, on a host whose MIME database types `.h264` as video and on one that types it `application/octet-stream`.
- Open the item menu on the `.H264`, `.hevc`, and `clip.h264.txt` copies and on `notes.h264`; compare Print and Quick preview with what each preview shows.
- Preview the `.h264` stream from an sftp mount.

### preview/preview-panel/pdf

- In a PDF, press Ctrl+A then Ctrl+C on the `ru` layout and with Caps Lock on.
- Select from page 1 to page 3 of the 2000-page PDF, scroll to page 1500, then press Ctrl+C.
- Double-click, then drag across a page break; triple-click the last line of a page that has no trailing line break.
- Drag from a scanned page onto a text page in a PDF that mixes both, and from a page margin onto text.
- Select text at 1× zoom and Ctrl+wheel to 4×. Compare the highlight bands with the glyphs on lines with and without descenders and on accented text.
- Select text in a right-to-left or vertical-script PDF and copy it.

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
- Show a rendered Markdown file, a DOCX, and the 5,000-character ODT paragraph in a 3000 px preview. Set wrap on, then off, from the Markdown preview between them. Then narrow the window below 1280 px.
- In Columns, drag the divider narrower, then wider, then use F8 and arrows; switch to Icons and back between each step.
- With an automatic rail and a preview open, narrow and widen the window across the threshold, then close and reopen the preview in List and in Icons.
- With an automatic rail in Columns three levels deep, click Home, a deeper folder, and Back in the rail, at the rail threshold and 24 px above it.
- With a preview open, move the window width 1 px at a time through the 24 px band above the rail threshold, both directions.
- In Icons or List with Appearance → Preview panel off, resize across the preferred sidebar width plus one column at text sizes 10, 13, and 16.
- Hide the sidebar in a short window, open a second window, then show the sidebar in each.
- Leave the window idle 2 s, then toggle Appearance → Preview panel from the Settings window.
- Leave it idle 2 s, then let a slow remote preview finish loading.
- Narrow the window below the hide threshold, idle 2 s, then let a preview load finish and widen.

### preview/preview-panel/documents

- Open the 1 MiB plus-one Markdown, the 300-column CSV, and the 100,001-value CSV; the fallback reason must be visible and the view switch hidden.
- Reference images from Markdown through a symlink escaping the folder, `../`, a percent-encoded Unicode name, and an 8 MiB plus-one PNG.
- Render a 257-line Mermaid block, a 4 KiB plus-one equation, prose containing `$5 and $10`, and an escaped `\$`.
- Open a 20 MiB plus-one XLSX, an XLSX whose first row has 300 columns, and the ZIP renamed `.docx`.
- Sort a table, drag-select a range, change the theme, then switch Source and Rendered while an image row is still rendering; close mid-render and check for leaked helpers.
- Double-click and triple-click a whitespace-free token over 2 KiB split across two rows, an emoji with a skin-tone modifier, a combining accent, and a link.
- Shift-click from prose into a table.
- Press Shift+End on a 2 KiB pathological line and Ctrl+Shift+Right through CJK text and punctuation runs, then Ctrl+C.
- On the `ru` layout, drag-select a table cell range, click one cell's text, then press Ctrl+C and Ctrl+A; repeat with Caps Lock on and on `us,ru`.
- In a table with a selected range, press Ctrl+Alt+C, Ctrl+Super+C, and keypad arrows, then Ctrl+C.
- With wrap off, open Markdown holding a 5,000-character prose line, a long list item, a long fenced code block, and an inline equation; toggle wrap 10 times quickly, then scroll to the right end.
- Toggle wrap while a long row is scrolled out of view and recycled, then scroll back to it.
- Close the preview during a table cell drag at the bottom edge, reopen it, and rest the pointer at the bottom edge with no button held.
- Change interface text size up and back with the 2 MiB text file open in Source and compare line numbers with their lines.
- In the 5,000-character ODT paragraph, double-click and Shift+End across its 2 KiB row boundaries.
- Render paragraphs over 2 KiB whose only separators are tabs, no-break spaces, or thin spaces; copy each whole.
- Render a paragraph with one early space before a 5 KiB unbroken token; copy it whole.
- Place an emoji, a combining accent, and a skin-tone sequence right where a whitespace-free token reaches 2 KiB.
- End a paragraph of 2 to 4 KiB with a 1 to 2 KiB word, and copy the paragraph.
- In RTF, put `\tab` or `\cell` between a surrogate pair's two units, and place a pair inside a paragraph over 2 KiB.
- In RTF, nest an escaped newline inside a `{\*…}` destination within bold text, then continue the paragraph.
- Under `[keymap.default]`, set `first_item = ["F7"]` and `last_item = ["F8"]`. In a rendered document, a Source view, and a table with a selected range, press Home, End, Shift+Home, and Ctrl+End.

### preview/preview-panel/documents/scrollbar

- Hold the scrollbar thumb at ten interior positions in both copies of the generated 400-block Markdown and in the 2 MiB text file. Repeat with wrap off and on, then in a file chooser preview.
- Release a touchpad flick into a region of tall code blocks, tables, and images still loading, in both directions.
- Drag the thumb to each end, release over the content, then press Page Down and Page Up.
- Focus the scrollbar and press Home and End, then set its value from Accerciser to the minimum, the maximum, and an interior value.
- Close the drawer mid-drag, reopen a different document or switch to Source, then drag the thumb again.
- Shrink a document until it fits while holding the thumb, by toggling wrap from a second window.

### preview/preview-panel/documents/odt

- Open the ODT tables without a header-row group and with two header rows and a merged cell; sort each column and copy a range.
- Open the ODT with the outline-level-9 heading, and compare the indentation of list levels 9 and 10 with level 8.
- Open the ODT holding a link inside `Preformatted Text` and a `mailto:` link, and click each link.
- Open the pandoc ODT, growing its tables until the size notice appears.

### preview/preview-panel/find

- Search a query spanning two virtual rows, one at 256 characters, German `ß`, and a lone combining accent.
- With find open, switch to Rendered on a table-only Markdown file and on a CSV, then switch back to Source.
- Search a large text file while it still loads, then Escape and reopen find before loading ends.
- In 10xer, press `/` in a small source, a large plain-text, and a rendered DOCX preview, then type `/` inside the find field.
- Open find in two windows on the same file with different queries; close the drawer in one.
- In `report.odt`, search for words that appear only in its footnote, comment, text box, and header.

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
- Under `[keymap.default]`, set `last_item = ["F8"]`, `media_seek_end = ["F9"]`, and `media_volume_step_up = ["F10"]`. On a focused playing timeline, press End, `G`, F8, F9, `+`, `=`, and F10.
- Scroll the fallback seek slider with a touchpad.
- Play a song with `~/.cache/gstreamer-1.0` removed, then with the sound server stopped mid-play.

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
- Step through a folder holding a remote MP4, a bare `.h264` stream, and source text named `.mp4`, in Icons and then in List.

### preview/preview-panel/model-views

- Pick Back right, change the theme twice, then select the next model file and come back.
- Preview a 3MF with one usable and one corrupt PNG, a 3MF with one PNG plus geometry, and a FreeCAD file with no thumbnail.
- Preview an STL of exactly 128 MiB and one byte over, and an ASCII STL just over 2 million triangles.
- Step through all four views on the STL near 2 million triangles, clicking Next again before each render ends; watch the bwrap count.
- Pick a view, then switch view mode between Columns, Icons, and List with the preview open.
- With a filter typed and a reversed sort, read the position eyebrow over a folder mixing STL, 3MF, FreeCAD, and non-model files.
- Toggle Reduce motion mid-sweep of the indicator, and close the drawer mid-sweep.
- Read the buttons, the indicator, and the header spinner in Accerciser while a view renders.
- Open the same model in two windows, pick different views, then change the theme.
- Make a view render fail by replacing the file with garbage between clicks, then restore it and retry.
- During the first render of the STL near 2 million triangles, press Previous and Next with the pointer, then focus them with Tab and press Space and Enter.
- Preview the FreeCAD file and the embedded-PNG 3MF from the network mount; read the header and badges before the image lands.
- Switch from a model to a text file mid-render; watch the header spinner.
- Preview a garbage file named `.stl` on a first load, then compare with a failure after the first image.
- With STL model thumbnails on, open Quick Preview on the near-2-million-triangle STL while a folder of STLs builds thumbnails. Step views and watch the bwrap count.
- With STL model thumbnails on, hang the NFS mount with an `iptables` drop while its STL folder renders. Open the local STL folder, and compare the bwrap count before and after the mount recovers.
- Toggle STL model thumbnails off while the near-2-million-triangle STL thumbnail renders, then on again; check for a second helper and a leftover private output directory.

### preview/preview-panel/gcode

- Preview each G-code sample; time the 2 GiB toolpath file against the text G-code without a thumbnail.
- Preview a `.gcode` whose only thumbnail uses `; thumbnail_JPEG begin`, and a `.bgcode` whose header declares a version other than 1.

### preview/preview-panel/routes

- Open each route sample, then a symlink to the timed GPX and the timed GPX on an sftp mount.
- Press Ctrl+Alt+Space repeatedly while sweeping the pointer across both images, then press Ctrl+Alt+Left and Right at the route ends.
- Play a route, minimise the window for 10 s, and restore it.
- Change Units from a second window's Settings during playback, with a route also open in a file chooser.
- Read both images and the play button in Accerciser during playback, then at rest.
- Step through a folder mixing GPX, FIT, KML, and text files with the arrow keys while a route plays.

### preview/preview-panel/sandbox

- With `bwrap` dropped from `PATH`, every native preview must still work. With `/dev/null` over `/usr/bin/bwrap`, image, PDF, SVG, DOCX, ODT, model, video, and GIF must each fail closed. No decoder may appear in `ps`.
- Open the ODT over 20 MiB and the ZIP renamed `.odt`.
- Place a `bwrap` symlink earlier in the trusted roots pointing under `/home`; it must be rejected.
- Feed a 512 MiB plus-one PNG, a header claiming 100000×100000, an SVGZ with external image references, a gzip bomb as `.svgz`, and the TIFF named `.ARW`.
- Open and close a RAW preview 50 times within 1 ms of each other; compare the bwrap count and the fd list with the baseline.
- On Debian testing with ImageMagick through `update-alternatives` and a glycin-only GDK Pixbuf, preview a HEIC and a JPEG; remove `/etc/alternatives/magick` and preview again. Repeat on a kernel without Landlock ABI 3, where previews use one-shot helpers.
- On Debian-family hosts with glx-diversions and with the NVIDIA GL alternative, preview a PNG, a PDF, and an MP4, and let a folder of thumbnails complete. Repeat where `glx--libGL.so.1-x86_64-linux-gnu` chains to an `nvidia--` alternative.
- Preview 20 images inside 60 s under the debug log and count `browser sandbox started` lines; wait 61 s and preview once more.
- Launch a real session with `STRATA_SANDBOX_ROOT` set to `/usr/./share`, then to `/nix/store` on a non-Nix host; preview a PNG each time and read the log.
- Launch with `STRATA_SANDBOX_PATH=:/usr/bin`, then with `STRATA_SANDBOX_PRLIMIT` set to a missing absolute path; preview a PNG and a PDF.
- Change a `STRATA_SANDBOX_*` variable in the running session, then open a second window and preview.
- Build with `STRATA_TRUSTED_COMMAND_PATH` naming a `/home` symlink that points into `/nix/store`, a store directory holding a `bwrap` symlink into `/home`, and `/usr/bin` listed twice.
- Preview the DNG with `dcraw` and `simple_dcraw` hidden, then with ImageMagick hidden too; repeat as Icons thumbnails.
- Preview the RAF with ImageMagick hidden, and step through a folder of 50 RAF files with the preview open.
- Preview and thumbnail the panorama with ImageMagick hidden, with and without its EXIF thumbnail.
- On the network mount, preview a RAW file, move the selection mid-render, and delete its folder at once; look for `.nfs…` or `.__smbfile_silly…` files in the parent.
- Preview media, then `kill -9` Strata. Start the container's Strata and preview there, then start the host Strata, preview once, and `ls -ld /tmp/strata-preview-*`.
- With the other user's `strata-preview-<pid>-<n>` folder present and `TMPDIR` on a filesystem without `flock` support, preview a PNG.

### preview/quick-preview

- Press Space with the caret in the filter input and a result selected, then on a mixed file-and-folder selection. Press Space on a symlink to a folder and on a broken symlink.
- Hold Down through 500 files for 5 s with the preview open; only the landing file may load, per the log.
- `rm` the previewed file from a shell while a video plays, while a PDF print dialog is open, and remove its parent folder.
- With Single-click file previews off, click, double-click, and start a drag on a supported file; no preview may open.
- Press Right into a PDF preview in List, then Ctrl+A, Ctrl+C, Delete, and Ctrl+X; the folder's file count must not change.
- On the Open button under a password-protected PDF, press Tab, Shift+Tab, Space, and Escape; repeat in Columns.
- With a filter result selected, press Space, keypad Space, Ctrl+Space, and Alt+Space on the `ru` layout and with Caps Lock on.

### preview/quick-preview/folder-peek

- Hover a 10k-entry folder, a folder of only hidden files, a `chmod 000` folder, a symlink to a folder, and one on a slow sshfs mount.
- Hover with the viewport 250 px and 262 px wide, at 2× scaling, and on a folder at the Icons grid's right edge.
- Sweep folder to popover to an adjacent folder quickly; switch view mode mid-slide; press Escape, F5, and Ctrl+F with a peek open.
- Turn Folder peeking off from a second window's Settings while a peek is open in the first.

## Hand-offs

- Thumbnails in the listing, including STL model and G-code thumbnails, and the thumbnail worker pool → `browser`.
- The RAW extension list, including `.ptx` and `.crf` → `browser`.
- Header toggle steps, a chosen rail, and a sidebar stepped to full in a short window → `browser`.
- Columns keyboard mirroring, including whether Up or Down onto a file opens a preview → `browser`.
- Selection kept or cleared by clicks on blank preview chrome and disabled preview controls → `browser`.
- F1 reference rows for preview find and media keys → `app`.
- Layout fallback, Caps Lock, keypad, and translated key names for every shortcut → `app`.
- Archive member listing and the archive preview → `operations`.
- Releasing Strata's reads before an operation, and leftovers on network mounts → `operations`.
- Unmounting a drive while a preview reads a file on it → `devices`.
- Preview keys and track stepping in 10xer mode → `integration`.
- Quick Preview opened by Enter on a typed file path → `browser`.
- A rebound document zoom reset and other `[keymap.*]` overrides while a preview has focus → `app`.
- Media runtime packaging and GStreamer launch dependencies → `app`.
- The Settings controls for autoplay, backend, document rendering, units, and folder peeking → `settings`.
- Mounting the sftp, MTP, and camera locations that remote previews read → `remote`.
