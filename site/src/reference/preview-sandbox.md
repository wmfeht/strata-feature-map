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
[docs/preview-sandbox.md](https://github.com/lgse/strata/blob/v1.0.0/docs/preview-sandbox.md).

## Providers

<!-- node: preview/preview-panel/sandbox, Decoding -->
<!-- node: preview/preview-panel/sandbox, Output validation -->
<!-- node: preview/preview-panel/documents -->
<!-- node: browser/thumbnails, Formats -->
<!-- node: browser/thumbnails, Display and fallback -->
<!-- node: preview/preview-panel, Images and PDFs -->

- GDK Pixbuf/camera RAW, Poppler PDF, ImageMagick, and dcraw fallbacks normalize
  images to dimension- and size-bounded PNG images. A RAW file that GDK Pixbuf
  cannot decode falls back to ImageMagick, then to the embedded camera JPEG.
  Sony ARW files keep their extension inside the sandbox so they decode as RAW.
- An image too large to decode within the sandbox's frame budget (about 134
  megapixels) shows its embedded EXIF thumbnail when it has one, and otherwise
  fails. Full-resolution phone photos fit the limits. Image helpers limit their
  memory allocator's arenas, so a JPEG with an embedded ICC color profile also
  previews on a many-core host, such as one with 64 threads, without the helper
  hitting its address-space limit.
- SVG and gzip-compressed SVGZ files, detected by content rather than by name,
  render with `resvg` inside the sandbox. User SVG and SVGZ previews, SVG
  thumbnails from the worker pool, Markdown SVGs, Mermaid diagrams, and equation
  output use this path, with image references disabled and system font loading
  enabled only when the document contains text. Without the worker pool, SVG
  thumbnails go through GDK Pixbuf or ImageMagick instead. SVGZ files preview but
  keep their file icon in the browser, because `.svgz` is not on the thumbnail
  extension list.
- `ffmpegthumbnailer` (or the software FFmpeg fallback) produces bounded media
  thumbnails. Browser thumbnails and the browser's media-metadata probes (the
  dimension and duration details in Icons view) share the reusable sandbox
  workers described below; File Properties inspection does not. Duplicate requests share work, and thumbnail failures
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
- File-list thumbnails are chosen by file extension. They cover PNG, JPEG,
  WebP, GIF, BMP, TIFF, SVG, HEIC, HEIF, AVIF, and JPEG XL images when a decoder
  for the format is installed; camera RAW files, from the embedded camera
  preview first; PDF; MP4, MKV, WebM, MOV, AVI, M4V, MPEG, MPG, and OGV video;
  cover art in MP3, FLAC, M4A, M4B, MKA, AIFF, AIF, and WMA files, at its aspect
  ratio, but never in Ogg, Opus, or WAV; embedded 3MF and FreeCAD images; and
  CBZ, CBR, and EPUB covers. AppImage files keep their file icon.
- A file shows its type icon while its thumbnail loads, and keeps it when
  rendering fails or the type is unsupported. Folders never get thumbnails, and a
  file or folder with a custom icon shows that icon instead. Ctrl+F filter results
  and recursive search results get thumbnails in Columns, List, and Icons, and
  changing the query leaves no stale thumbnails behind. Renaming a file without
  changing its extension, size, or modification time keeps its thumbnail without
  decoding again.
- A fresh image decode in the worker pool also fills the item's Icons caption
  with the source dimensions, such as `320×180`, without waiting for a metadata
  probe. A thumbnail served from the in-memory cache gets its dimensions from the
  separate metadata probe instead.

Every image renderer must return a regular PNG file of at most 32 MiB within
the operation's bounds: 800×800 pixels for an image, cover, or document-media
preview; 256×256 for a thumbnail; and for a PDF page, the preview pane's width up
to 1280 pixels, at most 1800 pixels tall and 2.5 megapixels. Anything else, such
as a symlink, an empty file, or oversized output, is rejected. PDF pages render
one page at a time across all previews, and queued pages scrolled out of view are
cancelled before rendering.

A small image keeps its own size and is enlarged at most 2× to fit the pane. An
image or PDF preview never uses the file-list thumbnail as a placeholder; it
waits for its own bounded render.

## Local 3D model previews

<!-- node: preview/preview-panel, Models and covers -->
<!-- node: browser/thumbnails, Formats -->

The preview accepts STL, 3MF and FreeCAD (`.FCStd`) files. STL and single-part
3MF geometry use a fixed-angle software render; FreeCAD uses its saved image,
so FreeCAD need not be installed.
A 3MF package with exactly one usable embedded PNG uses that image, even if other
candidates are corrupt or its geometry spans multiple model parts. Two usable
images are ambiguous: the preview tries geometry, while browser thumbnailing
leaves the normal file icon. Multipart geometry is not rendered: the preview
shows "Multipart model detected. Unable to render preview."

While a model loads, the preview shows "Reading model…", "Rendering N
triangles…", then "Finishing preview…"; an embedded image shows "Reading
thumbnail…" instead of the triangle count.

Browser thumbnails extract embedded images only, through the browser worker
pool and its normal cache. There is no geometry thumbnail for STL. Missing or
unusable images leave the file icon, and the failure cache prevents immediate
retries.

Heavy previews (models, PDFs, workbooks, DOCX, and comic and EPUB covers) take
turns, one at a time across the application, each in its own one-shot sandbox. Geometry renders use
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
the preview shows "This model is too complex to draw within the preview
rendering limit. Try a lower-detail version." and the browser keeps the normal
file icon. The `_rels/.rels` byte limit also applies before thumbnail
selection in 3MF packages. Object, build-item and component limits apply when
geometry is parsed, not when a usable embedded image is selected. Render output
is at most 800×800 pixels.

A model over a limit shows a message instead of a render:

| Limit exceeded | Message |
| --- | --- |
| Input file over 128 MiB | "This model file exceeds the 128 MiB preview limit. Try a smaller or lower-detail version." |
| Over 2 million triangles | "This model exceeds the 2 million triangle preview limit. Try a lower-detail version." |
| Over 2 million 3MF vertices | "This 3MF model exceeds the 2 million vertex preview limit. Try a lower-detail version." |
| Unpacked 3MF model XML over 128 MiB | "The unpacked 3MF model exceeds the 128 MiB preview limit." |
| Package entries, objects, build items, components, or embedded-image candidates | "This model is too complex to draw within the preview rendering limit. Try a lower-detail version." |

Other failures show their own message: "This FreeCAD file has no usable
embedded thumbnail", "STL contains no valid triangles", "3MF contains no
printable triangles", "3MF package has no model", "Model has no visible
extent", or "External 3MF model references are not supported". Any other parse
failure shows "This model file is invalid or damaged."

**These input-size limits are not RAM limits.** Input, parsed geometry and codec
allocations consume additional memory. The sandbox's CPU, wall-time, and 2-GiB
address-space limits remain a last-resort boundary.

Embedded images are limited to at most 16 candidates, 4 MiB per candidate,
16 MiB total candidate bytes read and 16 megapixels (16×1024×1024 pixels) total
admitted to decoding. Oversized or invalid images are not usable; exhausting a
total inspection budget fails the operation rather than assuming uninspected
candidates are invalid. Thumbnail output remains at most 256×256, in the image's
original colors.

### Comic and EPUB covers

CBZ and CBR files show their first image in natural order, and EPUB files their
declared cover. A file without one shows an error in the preview and keeps its
icon in the file list, as does a damaged cover. Cover thumbnails always run in a
one-shot sandbox, outside the worker pool. Remote covers show "Remote cover
previews are not supported; copy the file locally first".

## Browser worker pool

<!-- node: browser/thumbnails/workers -->
<!-- node: preview/preview-panel/sandbox, Pooled preview worker -->
<!-- node: browser/thumbnails, Scheduling -->

Columns, List, and Icons share one process-wide pool of sandboxed decoders,
started on the first thumbnail that misses the caches and kept across
navigation, view changes, and windows. **Thumbnail workers** in
**Settings → General**, under **PERFORMANCE**, sets its maximum live workers
(default: available parallelism capped at four, or two when detection fails;
range 1–16). Each click saves the count and applies to every window at once,
without a restart, and the same limit caps the preview pool below. Click the
number between − and + to reset it to the default. At 16, the + button
(**Increase thumbnail workers**) is disabled; at 1, the − button (**Decrease
thumbnail workers**) is. Typing "thumbnail workers", or a term such as
"concurrency" or "decoder pool", in **Search settings** finds the control. The saved `thumbnail_workers`
preference takes precedence over `STRATA_THUMBNAIL_WORKERS`, which seeds the
default when no count is saved. Values outside 1–16 are clamped to that range,
and values that are not a whole number use the CPU-based default.
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

To watch worker reuse, start Strata with
`RUST_LOG=strata::sandbox::browser=debug`. The log records each worker start
("browser sandbox started"), each completed job with its queue and run times,
and idle retirements, without file paths. Opening several uncached files within
the idle timeout should log completed jobs, not a new start line per file.

Each job still runs in a freshly started decoder with its own CPU, memory, and
time limits; only the worker that launches it is reused. No GPU, network,
desktop display, or session bus is available to these workers. On systems
without Landlock ABI 3 (Linux 6.2 or later, with Landlock enabled), each thumbnail runs in
its own one-shot sandbox with the same concurrency budget, and Strata logs
"Landlock ABI 3 unavailable; retaining one-shot sandboxes". It never decodes
without protection.

Scheduling ranks visible items, in reading order, before a margin of 25% around
the viewport, and offscreen requests wait until they are scrolled near.
Scrolling re-ranks queued work toward the new viewport. Scrolling an item out of
range, or reusing its row for another file, cancels its pending thumbnail work,
and a result that arrives late never appears on a reused row. RAW, PDF, video, and
embedded-model thumbnails and metadata probes together use at most one worker
fewer than the limit (minimum one), so ordinary images keep capacity. A file
that changes while it is decoded gets no thumbnail from that run. At
most one metadata probe occupies the pool at a time. While both kinds are
waiting, a probe gets a turn after four thumbnail admissions; a one-worker
configuration must serialize decoding and probing.

Still-image previews and document media (images, Mermaid diagrams, equations)
use a **second pool**, so an interactive Space preview never queues behind a
scrolled directory's thumbnail flood. With Landlock ABI 3, a preview within 60 seconds of the
previous one reuses its worker. Results are cached by file version *and*
operation, so a 256-pixel thumbnail can never satisfy an 800-pixel preview of
the same file.

## Remote still-image previews

<!-- node: preview/preview-panel, Images and PDFs -->
<!-- node: preview/preview-panel, Which files preview -->
<!-- node: browser/thumbnails, Remote files -->

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

Remote PDFs, GIF images (static or animated), audio, and video formats other than
MOV and MP4 remain unsupported: copy them locally first. Remote 3D models, comic
and EPUB covers, workbooks, and DOCX files show a message asking you to copy the
file locally first. Supported still-image formats continue to depend on installed
sandbox decoder tools; HEIC/HEIF can use ImageMagick with libheif inside the
image sandbox.

In the file list, files on a GVfs share that has a local FUSE mirror, such as
`smb://`, get thumbnails once their metadata loads, rendered from the mirror; the
location and the file's actions keep the remote address. Files on a GVfs
location with no local mirror keep their type icons.

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

Thumbnails appear during the Photos scan: after each batch the scan pauses
200 ms, then waits up to 2 seconds for visible thumbnails. Those load top to
bottom and left to right, and re-rank after scrolling. A viewport left at the
top stays there as batches arrive; after you scroll, normal anchoring applies.
Background selection updates during loading do not scroll List, Icons, or
Columns view to the selected photo.

## Media metadata

<!-- node: browser/properties/media -->
<!-- node: browser/properties/raw-metadata -->

File Properties shows available source-media details: image
resolution; audio/video duration and overall bitrate; video codec, frame rate and
HDR system; audio codec, sample rate, and channel count; and subtitle tracks and
chapter counts. These describe the original file, not the preview's scaled
frames or resampled audio. Attached album artwork is not reported as a video
track, and still images do not show synthetic video timing.
For ordinary images and audio/video, missing individual fields are omitted; an
unsuccessful inspection shows **MEDIA** as "Unavailable" without blocking the
other file information.

For a local `image/*`, `audio/*`, or `video/*` file, a **MEDIA** row reads
"Loading…" until inspection finishes. The rows, in order, are:

| Row | Example or format |
| --- | --- |
| **RESOLUTION** | "1600 × 900 pixels"; a video with 90° or 270° rotation shows the displayed orientation |
| **DURATION** | `H:MM:SS` |
| **BITRATE** | Mb/s with two decimals from 1,000,000 bit/s, otherwise whole kb/s |
| **VIDEO CODEC** | "h264" |
| **HDR** | "HDR10" or "HLG" |
| **FRAME RATE** | "24.00 fps" |
| **AUDIO CODEC** | "aac", "pcm_s16le" |
| **SAMPLE RATE** | "48.0 kHz" |
| **CHANNELS** | "1 (Mono)", "2 (Stereo)", or the channel count |
| **SUBTITLES** | The track count, then the known languages in parentheses |
| **CHAPTERS** | The chapter count |

A non-media file such as `readme.md` shows no MEDIA row, and a remote file shows
no media section. The details scroll inside the dialog, so the permission
controls stay reachable below several media rows.

Only regular files with a local source are inspected; remote files are not
downloaded for metadata. The inspector runs `ffprobe` inside the software-only
sandbox, with a four-second probe timeout and a 256 KiB output limit. Image
information can fall back to GDK Pixbuf inside that same sandbox. Only validated
numeric fields and bounded codec identifiers reach the UI, not arbitrary
embedded tags. Closing Properties cancels its work and prevents stale results
from appearing. Image and audio previews keep their normal size, modified date,
and type information and do not run this inspector. Video previews also keep
Size, Modified, and Type. They run the inspector only for their header badges
(see [Video previews](#video-previews)) and show none of the Properties media
rows, such as RESOLUTION or BITRATE.

A file whose name ends in a camera RAW extension, such as `.DNG`, `.NEF`, `.CR3`,
or `.ARW` in any case, shows seven RAW rows in place of the media rows:
**DIMENSIONS, CAMERA, LENS, FOCAL LENGTH, SHUTTER SPEED, ISO, and GPS
COORDINATES**, in that order, in both the preview panel and Properties. A
readable RAW shows values such as `600 × 400 pixels`, `50 mm`, `1/250 s`, `400`,
and `-12.500000, -45.250000`. All seven fields remain visible; missing or
unreadable values show `N/A`. Selecting a non-RAW file removes the RAW rows from
the preview panel. Dimensions describe the original image, account for orientation,
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

Audio-only files with no video stream, such as a mono `.ogg`, play their audio.
Raw H.264 and HEVC elementary streams, such as a bare `.h264` file, play from the
start and can seek, even without the extension.

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
<!-- node: preview/preview-panel/media, Seeking and recovery -->

Audio files open in a now-playing view with artwork, tags, a live spectrum, and a
waveform scrubber. A file without a title tag shows its name without the
extension, and a tagged track number reads "Track 3 of 12". Each part is sandboxed or derived from already-validated data:

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
  cached in memory for 64 tracks. A file with no audio track or no known
  duration keeps the plain progress line. A decode that fails or reaches the
  90-second limit stops and keeps the levels it had received; a failed overview
  is not cached.

Audio previews always start from the beginning, like a music player, and do not
remember where they stopped. Video previews reopen where they were closed while
Strata keeps running, unless they had played less than a second or reached the
end. Positions are kept in memory for the last 128 files and are lost when
Strata quits.

Uncached tags and artwork also wait 50 ms; cache hits are immediate. Completed
lookups are cached for the last 12 tracks, but failed or cancelled lookups are
retried on revisiting. Folder artwork is separately cached for 12 directories.
Consecutive audio files reuse one view. The current artwork stays in place while
details load, and only different artwork crossfades. While the pane is resized,
the artwork scales its cached image, then redraws at the new size 120 ms after
the size stops changing. Tag and art rows keep their
space while loading, so changing tracks does not shift the layout.

A pane at least 1.12 times as wide as tall puts the art beside the controls; at
0.95 or narrower the art returns on top. When height runs short in the stacked
layout, the spectrum hides first, then the art. Clicking the art or the spectrum
plays or pauses. Spectrum peak caps hold before falling. Hovering the waveform
shows the target time in the elapsed label, and clicking or dragging seeks.

Previous/next skip playlists and MIDI. During filtering they follow visible audio
results, including subfolders, and untagged captions read "X of Y in results"
instead of "X of Y in folder". Previous and next keep playing if the track was
playing. Previous is disabled on the first audio file and next on the last;
stepping does not wrap. Playback errors remain visible inside the audio view
without disabling track navigation. Tracks never advance automatically.

## Video previews

<!-- node: preview/preview-panel/media/video -->
<!-- node: preview/preview-panel/media, Autoplay -->

Video files open in a now-playing view of their own, laid out like the audio
view: the frame is the hero, the header with the file's position among the
listing's videos, such as "2 of 5 in folder", or "2 of 5 in results" while
search results replace the listing, the volume control, the title and the badges sits directly
under it, then the timeline and the same previous/play/next transport, with the
whole stack centred in the pane. The frame holds its place from the first paint,
sized by the aspect of its stand-in image, described below, or 16:9 without
one, until the video reports its own size. Clicking the frame toggles playback; there is no separate
play button over the frame. Consecutive video files reuse one view, like audio.
Previous/next step to the previous or next file of the same media family, so
audio steps to audio and video to video, following visible search results like
audio does. Playback errors show their title and detail inside the view; play is
disabled, and previous and next stay usable. The timeline is the audio view's waveform slider, with chapter
starts added as ticks.

Badges under the title summarise the file from the same bounded `ffprobe`
inspection that File Properties uses: resolution class by the long edge (SD,
720p, 1080p, 2K, 4K, 8K), HDR10 or HLG, 10-, 12- or 16-bit, rounded frame
rate, video codec, audio codec with channel layout, and a captions badge,
"CC" or "CC ×N", counting embedded subtitle tracks plus subtitle files named after the video
(`clip.srt`, `clip.en.vtt`, and the `ass`, `ssa` and `sub` extensions) in the
original's folder. Chapter starts become ticks on the timeline and chapter
titles join the time in the storyboard bubble; nothing renders subtitles over
the frames. The probe starts after the same 50 ms settle as audio details, is
cancelled when the selection moves on, and completed results are cached for the
last 12 files. Until it answers, empty pills hold the row; a failed probe leaves
the row empty. Badges fade in with a short stagger once per file, or appear at
once under reduced motion.

The timeline shows a storyboard bubble while the pointer hovers or drags: the
keyframe nearest that time with its timestamp, or an empty cell until one has
arrived. A seek covers the stale frame with the nearest cell until the new frame
is decoded, so scrubbing never shows a frozen picture. Storyboard cells are
decoded in the sandbox only after the first frame is on screen, share the single
low-priority background slot with waveform overviews (storyboard first), and are
cancelled when the selection moves on. A board has 8 to 48 cells, one per two
seconds, 128 pixels on the long edge. Cells arrive middle first, then the
quarters, then the eighths, and so on. Clips under four seconds, animations,
attached pictures, raw elementary streams and unknown durations have no
storyboard. A 90-second limit bounds the decode, and finished or partial boards
are cached in memory for the last 8 clips (about 14 MB for 16:9 video, up to
about 25 MB for square video). A partial board keeps its cells, and the next
visit to the clip decodes the board again.

Opening a previewed video externally, with Enter, the header's **Open in default
application** button or activation in the listing, pauses the preview and hands
its position to the default player. A file opened while its preview is still
loading, as the second click of a double-click does, stays paused once that
preview lands instead of autoplaying beside the player; moving to another file
or pressing play lifts the hold. mpv, VLC, Celluloid and MPlayer start at the
preview's position, including through `env` and Flatpak wrappers. Unknown
players, failed timed launches and positions within a second of either end open
the file plainly.

**Autoplay media previews** (**Settings → General**, under **BROWSING**) is off
by default: a selected media file shows paused with a play control. A playing
preview hidden by a narrow window resumes when shown again, whatever the setting.

With **Autoplay media previews** on, playback starts silent and rises to the
saved volume, which it never changes: over 1 s from the first frame for video
and over 0.5 s from the first sample for audio. Files shorter than 10 s play at
full volume from the start; unknown durations ease in. A muted saved state skips
the ramp, and any play, pause, seek, volume or mute input, or moving to another
file, ends it immediately.

Ambient light bleeds the frame's border colours into a 24-pixel band around the
picture, sampled from decoded frames at most ten times a second. While the
poster stands in, the band takes its colours from the cached thumbnail and eases
to the live frames. Nothing updates while playback is paused. The light follows **Element glow** in
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
and retry." instead of interrupting another player. A player keeps its slot
while it plays out buffered frames, so a fifth player cannot take it between GIF
loops. Separate application and
file-chooser processes have separate limits, not a machine-global scheduler.

| State | Bound / behavior |
| --- | --- |
| Startup or seek | 22 seconds from request to first frame; includes a 4-second probe, hardware attempts of at most 4 seconds each / 8 seconds combined, and up to 8 seconds for software. Isolated seeks restart at once; bursts within 200 ms coalesce to the settled position. |
| Active decoding | 8 seconds for a complete next frame. A stall mid-playback (frozen audio clock, decoder failure, audio-output error) restarts at the last position up to 3 times, then fails with the last error. |
| Audio clock | Until audio output first advances after a start, seek or resume, the playhead and video hold their position, so a start-up delay, such as Bluetooth audio over PipeWire, never snaps the playhead back. After the clock has run, a stalled clock lets video run ahead by at most 2 seconds, and playback restarts after 3 seconds without progress. |
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
sandbox.

Packagers of non-FHS distributions can point the sandbox at their runtime tree
with these variables **when compiling Strata**. They are embedded in the
executable; setting them when launching Strata has no effect.

| Build-time variable | Default | Purpose |
| --- | --- | --- |
| `STRATA_SANDBOX_PATH` | `/usr/bin` | Colon-separated helper binary directories inside the sandbox |
| `STRATA_SANDBOX_ROOT` | `/usr` | System runtime tree, bound read-only at the same path |
| `STRATA_SANDBOX_PRLIMIT` | `/usr/bin/prlimit` | Resource-limit launcher path inside the sandbox |
| `STRATA_SANDBOX_GDK_PIXBUF_MODULE_FILE` | Unset | GDK Pixbuf `loaders.cache` path passed to helpers |

For example, a Nix package can compile with:

```sh
STRATA_SANDBOX_PATH='/nix/store/<ffmpeg>/bin:/nix/store/<imagemagick>/bin' \
STRATA_SANDBOX_ROOT='/nix/store' \
STRATA_SANDBOX_PRLIMIT='/nix/store/<util-linux>/bin/prlimit' \
STRATA_SANDBOX_GDK_PIXBUF_MODULE_FILE='/nix/store/<pixbuf-loaders>/lib/gdk-pixbuf-2.0/2.10.0/loaders.cache' \
cargo build --release --locked
```

Replace the store paths with your package's dependency paths, and include every
helper binary directory. Values are used literally: leave a variable unset to
keep its default, never set it to an empty value. The resource-limit launcher,
the helper binaries, the loaders cache, its modules, and their runtime libraries
must all be reachable inside the sandbox mounts. The variables apply to every
sandbox: one-shot previews, the browser worker pools, media playback, and RAR
extraction.

The root replaces `/usr` rather than adding a mount. Use only admin-managed
runtime trees: binding `/` or a user tree exposes private files to untrusted
decoders.

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
`/sys` for discovery. With hardware acceleration off, and always for audio
previews, waveforms, storyboards, metadata, image, PDF, and thumbnail helpers,
the sandbox receives no GPU devices or `/sys` mount. With it on, a video
preview's sandbox keeps that access even when it decodes in software, such as a
GIF, a file whose only picture is cover art, or a fallback after the hardware
attempts fail. Changing these settings applies to the next preview
without interrupting the current one.

With no saved choice, systems with an AMD Polaris 10, 11, or 12 GPU (PCI IDs
`0x67c0–0x67df`, `0x67e0–0x67ff`, or `0x6980–0x699f`) decode in software.
You can still opt in. GPU access expands the helper's attack surface into
driver code.
