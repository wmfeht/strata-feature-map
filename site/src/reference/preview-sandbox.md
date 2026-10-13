---
nodes: [preview/preview-panel/sandbox, preview/preview-panel, preview/preview-panel/documents, preview/preview-panel/media, preview/preview-panel/media/audio, preview/preview-panel/media/video, browser/thumbnails, browser/thumbnails/workers, browser/properties/media, browser/properties/raw-metadata, devices/volumes/camera]
reviewed_at: 0a086aa3bdb251842a1e8413e2a6b35970d0b409
---

# Preview sandbox

Strata treats files shown while browsing as untrusted. Original-file native
parsing and decoding run inside [bubblewrap](https://github.com/containers/bubblewrap),
never in the application. A decoder that crashes, hangs, or is attacked by a
crafted file stays inside a short-lived, resource-limited process with no
network, no desktop session, and no view of your other files. Strata shows the
file's icon or a message instead of the preview.

This page covers what runs in the sandbox, the limits you can run into, and what
you see when a preview fails. How the isolation works (namespaces, Landlock and
seccomp, the worker processes, and the decoder protocol) is documented for
contributors in
[docs/preview-sandbox.md](https://github.com/lgse/strata/blob/main/docs/preview-sandbox.md).

## Providers

<!-- node: preview/preview-panel/sandbox, Decoding -->
<!-- node: preview/preview-panel/sandbox, Output validation -->
<!-- node: preview/preview-panel/documents -->
<!-- node: browser/thumbnails, Formats -->

- GDK Pixbuf/camera RAW, Poppler PDF, ImageMagick, and dcraw fallbacks normalize
  images to dimension- and size-bounded PNG images. A RAW file that GDK Pixbuf
  cannot decode falls back to ImageMagick, then to the embedded camera JPEG.
  Sony ARW files keep their extension inside the sandbox so they decode as RAW.
- An image too large to decode within the sandbox's frame budget (about 134
  megapixels) shows its embedded EXIF thumbnail when it has one, and otherwise
  fails. Full-resolution phone photos fit the limits.
- SVG and gzip-compressed SVGZ files, detected by content rather than by name,
  render with `resvg` inside the sandbox. User SVG previews and thumbnails,
  Markdown SVGs, Mermaid diagrams, and equation output use this path, with image
  references disabled and system font loading enabled only when the document
  contains text.
- `ffmpegthumbnailer` (or the software FFmpeg fallback) produces bounded media
  thumbnails. Browser thumbnails and media details share the reusable sandbox
  workers described below. Duplicate requests share work, and thumbnail failures
  are cached for 30 seconds.
- Audio and video previews decode in the sandbox and stream to Strata, as
  described under [Incremental media playback](#incremental-media-playback).
- Plain text stays in-process, invokes no native format parser, and is capped at
  1 MiB.
- Local XLS, XLSX, and ODS previews run inside the resource-limited helper,
  accepting at most 20 MiB of input. Only validated, bounded cell values cross
  back into the application; macros and formulas are not executed.
- Local DOCX previews run in the same helper under the same 20 MiB input limit.
- Local [Markdown, bounded HTML, RTF, CSV, and TSV previews](document-previews.md)
  are parsed in-process by pure-Rust parsers that receive only the bounded source
  string and cannot initiate filesystem access, network access, JavaScript
  execution, or subresource loading. Relative Markdown images are separately
  confined to the document directory. Their decoders, the Mermaid renderer, and
  the bundled MathJax equation renderer run in the sandbox. User equations are
  passed as data, not evaluated as JavaScript, and only validated PNG output
  returns.

Every image renderer must return a regular PNG file within the operation's
bounds: 800×800 pixels for a still preview, 256×256 for a thumbnail, and at
most 32 MiB. Anything else, such as a symlink, an empty file, or oversized
output, is rejected.

## Local 3D model previews

<!-- node: preview/preview-panel, Models and covers -->
<!-- node: browser/thumbnails, Formats -->

The preview accepts STL, 3MF and FreeCAD (`.FCStd`) files. STL and single-part
3MF geometry use a fixed-angle software render; FreeCAD uses its saved image.
A 3MF package with exactly one usable embedded PNG uses that image, even if other
candidates are corrupt or its geometry spans multiple model parts. Two usable
images are ambiguous: the preview tries geometry, while browser thumbnailing
leaves the normal file icon. Multipart geometry is not rendered: the preview
shows "Multipart model detected. Unable to render preview."

Browser thumbnails extract embedded images only, through the browser worker
pool and its normal cache. There is no geometry thumbnail for STL. Missing or
unusable images leave the file icon, and the failure cache prevents immediate
retries.

Heavy previews (models, PDFs, workbooks and DOCX) take turns, one at a time
across the application, each in its own one-shot sandbox. Geometry renders use
the theme's palette, and open model previews reload when the theme changes.

These limits are built into Strata, not Settings options or environment
variables:

| Limit | Applies to |
| --- | --- |
| 128 MiB (134,217,728 bytes) | Input file, including embedded-thumbnail requests |
| 128 MiB, independently of compressed file size | Unpacked 3MF model XML |
| 256 | All ZIP entries in a 3MF package |
| 4096 | All ZIP entries in a FreeCAD package |
| 1024 | Objects in the 3MF model XML |
| 1024 | Build items in the 3MF model XML |
| 16 | Component nesting below a build item (depth zero) |
| 64 KiB | Unpacked `_rels/.rels` in a 3MF package |
| 2 million | Parsed/emitted triangles |
| 2 million | 3MF vertices |
| 100,000 | Stored component references |
| 100,000 | Expanded objects, including pending expansion work |
| 100 million | Triangle bounding-box pixel visits |

Package entry caps are checked **before looking for an embedded thumbnail**. A
package exceeding its entry cap is rejected even if it contains a usable PNG:
the preview reports "Model package entry limit exceeded" and the browser keeps
the normal file icon. The `_rels/.rels` byte limit also applies before thumbnail
selection in 3MF packages. Object, build-item and component limits apply when
geometry is parsed, not when a usable embedded image is selected. Render output
is at most 800×800 pixels.

**These input-size limits are not RAM limits.** Input, parsed geometry and codec
allocations consume additional memory. The sandbox's CPU, wall-time, and 2-GiB
address-space limits remain a last-resort boundary.

Embedded images are limited to at most 16 candidates, 4 MiB per candidate,
16 MiB total candidate bytes read and 16 megapixels (16×1024×1024 pixels) total
admitted to decoding. Oversized or invalid images are not usable; exhausting a
total inspection budget fails the operation rather than assuming uninspected
candidates are invalid. Thumbnail output remains at most 256×256, in the image's
original colors.

## Browser worker pool

<!-- node: browser/thumbnails/workers -->
<!-- node: preview/preview-panel/sandbox, Pooled preview worker -->
<!-- node: browser/thumbnails, Scheduling -->

Columns, List, and Icons share one process-wide pool of sandboxed decoders,
started on the first thumbnail that misses the caches and kept across
navigation, view changes, and windows. **Thumbnail workers** in
**Settings → General**, under **PERFORMANCE**, sets its maximum live workers
(default: available parallelism capped at four; range 1–16). Click the number
between − and + to reset it to the default. The saved `thumbnail_workers`
preference takes precedence over `STRATA_THUMBNAIL_WORKERS`, which seeds the
default when no count is saved (invalid values use the CPU-based default).
Lowering the limit lets active jobs finish and retires excess idle workers. The
pool also runs browser media-metadata probes, not preview playback or
Properties inspection.

Idle workers stop after **60 seconds without a job**, and the pool can shrink
to zero while Strata stays open. `STRATA_THUMBNAIL_IDLE_SECONDS` overrides this at
startup (positive integer seconds, capped at 86,400; zero/invalid values use 60).
Busy decoders are never interrupted by idle expiry. New misses start workers
again, within the same limit. This releases sandbox process memory, not
thumbnail caches, so displayed and cached thumbnails remain available. When a
worker is killed, the next request starts a replacement.

Each job still runs in a freshly started decoder with its own CPU, memory, and
time limits; only the worker that launches it is reused. No GPU, network,
desktop display, or session bus is available to these workers. On systems
without Landlock ABI 3 (Linux 6.2 or later, with Landlock enabled), each thumbnail runs in
its own one-shot sandbox with the same concurrency budget, and Strata logs
"Landlock ABI 3 unavailable; retaining one-shot sandboxes". It never decodes
without protection.

Scheduling ranks visible items before a small overscan region, and offscreen
requests wait until they are scrolled near. With more than one worker, slow
RAW, PDF, video and embedded-model work leaves capacity for ordinary images. At
most one metadata probe occupies the pool at a time. While both kinds are
waiting, a probe gets a turn after four thumbnail admissions; a one-worker
configuration must serialize decoding and probing.

Still-image previews and document media (images, Mermaid diagrams, equations)
use a **second pool**, so an interactive Space preview never queues behind a
scrolled directory's thumbnail flood. A preview within 60 seconds of the
previous one reuses its worker. Results are cached by file version *and*
operation, so a 256-pixel thumbnail can never satisfy an 800-pixel preview of
the same file.

## Remote still-image previews

<!-- node: preview/preview-panel, Images and PDFs -->
<!-- node: preview/preview-panel, Which files preview -->

Still images on GIO/GVfs locations (including phone camera, AFC, and MTP storage)
can use the preview pane and Space quick preview. The application streams the
selected original to a randomly named mode-0600 temporary file before invoking
the same image sandbox as local files. Remote names never choose a local path.
The displayed entry and its actions retain the original URI.

Still-image transfers have a 64-MiB byte limit and a 30-second total deadline. Known
oversized files are rejected before opening; the stream limit also applies when
size metadata is missing or inaccurate. At most four transfers/staged originals
can be active per process, including ones waiting for cancellation or decoding.
A busy request fails with "Too many remote previews are active; try again
shortly" rather than starting another transfer.

Changing selection or closing the preview cancels the transfer. A backend that is
slow to acknowledge cancellation retains its slot until its worker exits.
Partial files are removed on transfer failure, and staged files are removed when
the decoder exits. Normal cleanup does not guarantee removal after a process
crash or forced termination. Remote previews do not populate the persistent
thumbnail cache or the in-memory rendered-preview cache, and originals are never
modified.

MOV and MP4 previews use the same staging, with a 256-MiB byte limit and
60-second deadline, and share the four-input limit with images. Playback starts
only after download completes.

Remote PDFs, animated GIFs, audio, and other video formats remain unsupported:
copy them locally first. Remote 3D models, workbooks, and DOCX files show a
message asking you to copy the file locally first. Supported still-image formats continue to depend on installed
sandbox decoder tools; HEIC/HEIF can use ImageMagick with libheif inside the
image sandbox.

### Camera file-list thumbnails

<!-- node: devices/volumes/camera, Thumbnails and scrolling -->

Camera thumbnails use the small preview the camera itself provides, not the
original. Missing or failed previews leave the ordinary file icon; Strata does
not fall back to downloading full photos for thumbnails.

Retrieval is asynchronous, limited to 1 MiB and 15 seconds. These jobs share the
browser's thumbnail workers and queues, and scrolling a row away cancels them.
The preview is decoded by the same image-thumbnail sandbox, and only the
normalized PNG reaches Strata. Camera thumbnails are cached in memory only, never
in the persistent thumbnail cache. AFC and MTP file-list thumbnails are not
enabled by this path.

## Media metadata

<!-- node: browser/properties/media -->
<!-- node: browser/properties/raw-metadata -->

File Properties shows available source-media details: image
resolution; audio/video duration and overall bitrate; video codec, frame rate and
HDR system; audio codec, sample rate, and channel count; and subtitle track and
chapter counts. These describe the original file, not the preview's scaled
frames or resampled audio. Attached album artwork is not reported as a video
track, and still images do not show synthetic video timing.
For ordinary images and audio/video, missing individual fields are omitted; an
unsuccessful inspection shows **MEDIA** as "Unavailable" without blocking the
other file information.

Only regular files with a local source are inspected; remote files are not
downloaded for metadata. The inspector runs `ffprobe` inside the software-only
sandbox, with a four-second probe timeout and a 256 KiB output limit. Image
information can fall back to GDK Pixbuf inside that same sandbox. Only validated
numeric fields and bounded codec identifiers reach the UI, not arbitrary
embedded tags. Closing Properties cancels its work and prevents stale results
from appearing. Ordinary image and audio/video previews retain their normal size,
modified date, and type information; they do not run this metadata inspector.

Camera RAW files additionally show **DIMENSIONS, CAMERA, LENS, FOCAL LENGTH,
SHUTTER SPEED, ISO, and GPS COORDINATES**, in that order, in both the preview
panel and Properties. All seven fields remain visible; missing or unreadable
values show `N/A`. Dimensions describe the original image, account for orientation,
and never use an embedded thumbnail's size. GPS is signed decimal latitude,
then longitude; there is no reverse geocoding or network request. Shutter speeds
use `1/N s` for integer reciprocals and decimal seconds otherwise (for example,
`0.3 s`, not `1/3.333 s`).

RAW inspection uses LibRaw's `raw-identify -v` or classic `dcraw -i -v` when
installed, with a three-second limit per identification attempt. A bundled
EXIF reader supplements capture and GPS tags from supported EXIF containers,
including TIFF-based RAW files, without decoding pixels. It is also the fallback
when those optional utilities are absent. Support depends on the format and
available tools; unavailable tags in other RAW containers remain `N/A`.

Both parsers run only inside a short-lived, software-only sandbox with the
512 MiB input limit, memory/CPU/wall-time limits, and a 256 KiB output budget.
Only the seven validated properties reach the UI; camera/lens strings are
bounded plain text. RAW files in Trash show the same values as the original,
even when the stored filename has a collision suffix. Remote RAW files are not
downloaded for metadata and show `N/A`. Selection changes and closing either
surface cancel pending work. RAW preview labels remain in place during
selection changes and metadata loading; only their values reset to `N/A` and
update when inspection completes. Detailed RAW inspection does not run for
browser thumbnails.

## Incremental media playback

<!-- node: preview/preview-panel/media, Playback -->
<!-- node: preview/preview-panel/media, Resources and limits -->

FFmpeg decodes one original local file, read-only, inside the sandbox. Strata
receives only bounded, validated video frames and audio samples, and plays them
itself. No compressed media reaches an unsandboxed parser, and there is no
temporary transcoded copy of the file.

Video timing is normalized **inside the sandbox** to 30 fps. Audio is 48 kHz
stereo.

Previews play **the entire source**, without a 30-second playback cap. Seeking
restarts the sandbox at the requested position, rounded down to the 30-fps
grid. A seek whose decoder dies before its first frame, as happens past the real
end of a truncated download whose header overstates the duration, resumes where
playback was instead of ending the preview. Short GIFs loop without restarting
a process every cycle; longer GIFs play their complete animation before
looping.

Files without a reported duration play until decoded EOF. Their timeline remains
unknown and seeking is disabled until the actual end is established; pause/idle
resume still retains the playback position.

The decode size follows the pane's logical size times display scale, capped
at 1280 pixels on either axis. Frames preserve display aspect ratio, including
rotation, without enlarging small sources. Resizes settle for 250 ms; the
previous frame remains visible. Shrinking the pane never restarts decoding: the
larger frames are downsampled on screen and the next seek or restart adopts the
smaller size. Growing restarts at the current playback position only when the
fitted frame would grow by 8 % or more, so a resize costs at most one restart. A
paused resize/seek stays paused. Mute and volume apply live to every player;
changes to hardware acceleration apply on the next preview.

Decoded output is checked before Strata uses it. Malformed or truncated output
fails the preview as a decoder error and is never shown. Strata holds at most
eight decoded frames for a player (50 MiB at the largest size) plus about two
seconds of audio, so memory does not grow with clip length. There is **no
whole-clip media cache**. Closing or revisiting a file requires a new decode.

## Audio previews

<!-- node: preview/preview-panel/media/audio -->

Audio files open in a now-playing view with artwork, tags, a live spectrum, and a
waveform scrubber. Each part is sandboxed or derived from already-validated data:

- **Playback** ignores attached pictures, so broken or oversized artwork cannot
  prevent playback. A real video stream overrides the filename's audio type: the
  file opens in the video view. Pure audio never restarts on resize.
- **Artwork** comes from one attached picture (tagged front cover first,
  otherwise the first picture), scaled to at most 800×800 inside the sandbox.
  Without embedded art, the first of `cover`, `folder`, `front`, `album`, or
  `albumart` (`.jpg`, `.jpeg`, `.png`, `.webp`) in the same local folder is
  decoded by the sandboxed image-preview pool. Remote files use embedded art
  only. Without any art, a theme-colored record spins in its place while
  playing.
- **Tags** are limited to title, artist, album, album artist, and track
  number/total. Strata removes control and bidirectional-override characters,
  collapses whitespace, caps each value at 200 characters, and shows them as
  plain text.
- **The spectrum** is computed in the application from the audio it already
  plays, aligned to what you hear, so no extra parser sees the stream.
- **The waveform overview** starts only after a track has stayed selected for
  50 ms. One overview decode runs at a time at low priority. Changing tracks
  cancels the decode, a 90-second limit bounds it, and finished overviews are
  cached in memory for 64 tracks. Unknown durations, failures, and timeouts keep
  the plain progress line.

Audio previews always start from the beginning, like a music player, and do not
remember where they stopped. Video previews reopen where they were closed, unless
they had played less than a second or reached the end.

Uncached tags and artwork also wait 50 ms; cache hits are immediate. Completed
lookups are cached for the last 12 tracks, but failed or cancelled lookups are
retried on revisiting. Folder artwork is separately cached for 12 directories.
Consecutive audio files reuse one view. The current artwork stays in place while
details load, and only different artwork crossfades.

Previous/next skip playlists and MIDI. During filtering they follow visible audio
results, including subfolders, and untagged captions read "X of Y in results"
instead of "X of Y in folder". Playback errors remain visible inside the audio
view without disabling track navigation. Tracks never advance automatically.

## Video previews

<!-- node: preview/preview-panel/media/video -->
<!-- node: preview/preview-panel/media, Autoplay -->

Video files open in a now-playing view of their own, laid out like the audio
view: the frame is the hero, the header with the file's position among the
folder's videos, the volume control, the title and the badges sits directly
under it, then the timeline and the same previous/play/next transport. Clicking
the frame toggles playback. Consecutive video files reuse one view, like audio.
Previous/next step to the previous or next file of the same media family, so
audio steps to audio and video to video, following visible search results like
audio does. Playback errors remain visible inside the view without disabling
navigation. The timeline is the audio view's waveform slider, with chapter
starts added as ticks.

Badges under the title summarise the file from the same bounded `ffprobe`
inspection that File Properties uses: resolution class by the long edge (SD,
720p, 1080p, 2K, 4K, 8K), HDR10 or HLG, 10-, 12- or 16-bit, rounded frame
rate, video codec, audio codec with channel layout, and a captions badge
counting embedded subtitle tracks plus subtitle files named after the video
(`clip.srt`, `clip.en.vtt`, and the `ass`, `ssa` and `sub` extensions) in the
original's folder. Chapter starts become ticks on the timeline and chapter
titles join the time in the storyboard bubble; nothing renders subtitles over
the frames. The probe starts after the same 50 ms settle as audio details, is
cancelled when the selection moves on, and completed results are cached for the
last 12 files. Until it answers, empty pills hold the row; a failed probe leaves
the row empty.

The timeline shows a storyboard bubble while the pointer hovers or drags: the
keyframe nearest that time with its timestamp, or an empty cell until one has
arrived. A seek covers the stale frame with the nearest cell until the new frame
is decoded, so scrubbing never shows a frozen picture. Storyboard cells are
decoded in the sandbox only after the first frame is on screen, share the single
low-priority background slot with waveform overviews (storyboard first), and are
cancelled when the selection moves on. A board has 8 to 48 cells, one per two
seconds, 128 pixels on the long edge. Clips under four seconds, animations,
attached pictures, raw elementary streams and unknown durations have no
storyboard. A 90-second limit bounds the decode, and finished or partial boards
are cached in memory for the last 8 clips (at most about 14 MB).

Opening a previewed video externally, with Enter, the header's **Open in default
application** button or activation in the listing, pauses the preview and hands
its position to the default player. A file opened while its preview is still
loading, as the second click of a double-click does, stays paused once that
preview lands instead of autoplaying beside the player; moving to another file
or pressing play lifts the hold. mpv, VLC, Celluloid and MPlayer start at the
preview's position, including through `env` and Flatpak wrappers. Unknown
players, failed timed launches and positions within a second of either end open
the file plainly.

With **Autoplay media previews** on, playback starts silent and rises to the
saved volume, which it never changes: over 1 s from the first frame for video
and over 0.5 s from the first sample for audio. Files shorter than 10 s play at
full volume from the start; unknown durations ease in. A muted saved state skips
the ramp, and any play, pause, seek, volume or mute input, or moving to another
file, ends it immediately.

Ambient light bleeds the frame's border colours into a 24-pixel band around the
picture, sampled from decoded frames at most ten times a second. Nothing updates
while playback is paused. The light follows **Element glow** in
**Settings → Appearance**, stays off under reduced motion, and never runs on the
Cairo software renderer.

The frame area never shows a spinner. Until the first decoded frame it shows the
listing's cached thumbnail dimmed as a poster when that thumbnail is already in
memory, otherwise a plain surface at the probed aspect. A clip that resumes
where it stopped shows the cell of its cached storyboard nearest that point
instead. The first frame fades the stand-in out over 150 ms, or replaces it at
once under reduced motion. Every media stream waits 50 ms before starting its
sandbox session, so a selection that moves on within that window spawns no
decoder.

## Scheduling and deadlines

<!-- node: preview/preview-panel/media, Resources and limits -->
<!-- node: preview/preview-panel/media, Seeking and recovery -->

At most **four media sessions per application process** may own decoders, across
browser windows and file choosers sharing that process. A fifth request shows
"Media previews are busy (four active players). Pause or close another preview
and retry." instead of interrupting another player. Separate application and
file-chooser processes have separate limits, not a machine-global scheduler.

| State | Bound / behavior |
| --- | --- |
| Startup or seek | 22 seconds from request to first frame; includes a 4-second probe, hardware attempts of at most 4 seconds each / 8 seconds combined, and up to 8 seconds for software. Isolated seeks restart at once; bursts within 200 ms coalesce to the settled position. |
| Active decoding | 8 seconds for a complete next frame. A stall mid-playback (frozen audio clock, decoder failure, audio-output error) restarts at the last position up to 3 times, then fails with the last error. |
| Audio clock | Until audio output first advances after a start, seek or resume, the playhead and video hold their position, so a start-up delay, such as Bluetooth audio over PipeWire, never snaps the playhead back. |
| Paused | Keep position, frame and buffers for 30 seconds, then stop the decoder and release audio output. The displayed frame and position remain. Resume or a paused seek starts a new decode. |
| Close / selection change | Cancel promptly and stop the decoder and its sandbox. |
| End / malformed output / failure | Release the decoder; malformed or truncated output, unavailable decoding and unsuccessful exit fail closed. No unsandboxed fallback. |

The limits do not promise instant startup, zero-latency seeking, or a total RAM
plateau for every toolkit/driver.

## Isolation and hardware policy

<!-- node: preview/preview-panel/sandbox, Launching the sandbox -->
<!-- node: preview/preview-panel/sandbox, Isolation and limits -->
<!-- node: preview/preview-panel/media, Hardware acceleration -->

Strata starts bubblewrap only from admin-managed system locations
(`/run/wrappers/bin`, `/usr/bin`, `/usr/sbin`, `/bin`, `/sbin`, and the NixOS and
Guix system profiles), never from your `PATH`. A copy whose real location is
outside the system directories, `/nix/store`, or `/gnu/store` is refused. When
bubblewrap is missing or cannot start, a native-format preview shows **Preview
unavailable** with the reason, and the file is never decoded outside the
sandbox. Packagers of non-FHS distributions can point the sandbox at their
runtime tree when compiling Strata (the default is `/usr`); those settings are
built into the executable, and setting them when launching Strata has no effect.

Each sandboxed helper sees:

- read-only system libraries and tools, the Strata executable, and exactly one
  read-only input file;
- a private output directory for image providers and a size-limited (512 MiB)
  private `/tmp`;
- an empty environment, a nonexistent home, and no network, desktop,
  session-bus, or audio-server sockets. Only the application handles display and
  audio output.

Image/PDF parsing has a 512-MiB input cap, 2-GiB address-space cap, 512-MiB file
cap, 32-MiB output cap, 12-second wall limit and 10-second CPU limit. A larger
input fails with "Preview input exceeds the supported size limit" before any
renderer starts. Changing selection or closing the preview kills the helper and
everything it started. Media has no input-file size cap, playback-duration cap,
or cumulative CPU limit; frame sizes, buffer limits, and the deadlines above
bound active work. Each software FFmpeg process has a 2-GiB address-space limit;
all decoding processes disable core dumps and cap files and individual media
allocations at 512 MiB and source frames at 50 million pixels. Hardware
decoders are exempt from the address-space limit because drivers reserve large
virtual ranges.

Hardware decoding is controlled by **Hardware-accelerated video previews** and
**Decoding backend** (**Automatic**, **VA-API**, or **Vulkan**) in
**Settings → General**, under **PERFORMANCE**. Automatic tries VA-API, then
Vulkan, then software. Explicit VA-API/Vulkan falls directly back to software
when its hardware attempts fail before output begins. A failure after playback
starts fails the preview rather than silently switching decoders mid-stream.
VA-API receives only GPU render nodes (`/dev/dri/renderD*`); Vulkan/Automatic
may also receive NVIDIA device nodes. Accelerated helpers receive read-only
`/sys` for discovery. Software, image, PDF and thumbnail helpers receive no GPU
devices or `/sys` mount. Changing these settings applies to the next preview
without interrupting the current one.

With no saved choice, systems with an AMD Polaris 10, 11, or 12 GPU (PCI IDs
`0x67c0–0x67df`, `0x67e0–0x67ff`, or `0x6980–0x699f`) decode in software.
You can still opt in. GPU access expands the helper's attack surface into
driver code.
