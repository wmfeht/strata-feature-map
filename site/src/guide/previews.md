---
nodes: [preview/preview-panel, preview/preview-panel/layout, preview/preview-panel/documents, preview/preview-panel/find, preview/preview-panel/media, preview/preview-panel/media/audio, preview/preview-panel/media/video, preview/preview-panel/sandbox, preview/quick-preview, preview/quick-preview/folder-peek]
reviewed_at: 0a086aa3bdb251842a1e8413e2a6b35970d0b409
---

# Previews

See inside a file without opening it. Strata previews text, code, images,
PDFs, documents, spreadsheets, audio, and video in a panel beside your files.

## Show the preview panel

<!-- node: preview/preview-panel/layout -->
<!-- node: preview/preview-panel -->

Open the **Appearance** menu in the header bar and click **Preview panel**. In
Columns the panel is on from the start, holding a slot right of your columns
so previews never move them. In Icons and List it starts hidden.

Drag the divider to resize the panel; the width lasts until you close the
window. When the window gets too narrow, the preview hides and media pauses.
Widen the window and it returns.

## Take a quick look

<!-- node: preview/quick-preview, Opening and closing -->
<!-- node: preview/quick-preview, Following the selection -->
<!-- node: preview/quick-preview, Keyboard ownership -->

Select a file and press Space. Press Space again to close the preview.

- **Click.** With **Single-click file previews** on, the default, one click on
  a supported file previews it.
- **Menu.** Right-click a file and choose **Quick preview**.
- **Follow.** With the preview open, arrow to another file and the preview
  follows.
- **Step inside.** In List or Columns, press Right to move focus into the
  preview. Ctrl+C then copies selected text, not files.

Space on a folder opens the folder instead.

## Peek into a folder

<!-- node: preview/quick-preview/folder-peek -->

Turn on **Settings → General → Browsing → Folder peeking**; it is off by
default. Rest the pointer on a folder in Icons or List for half a second, and
a popover lists up to eight of its entries. Columns never peeks.

## Play media and read documents

<!-- node: preview/preview-panel/media -->
<!-- node: preview/preview-panel/media/audio -->
<!-- node: preview/preview-panel/media/video -->

Audio, video, and GIF previews open paused. To start them at once, turn on
**Settings → General → Browsing → Autoplay media previews**.

| Keys | Action |
| --- | --- |
| Ctrl+Alt+Space | Play or pause |
| Ctrl+Alt+Left, Ctrl+Alt+Right | Seek 5 seconds |
| Ctrl+Alt+Up, Ctrl+Alt+Down | Volume up or down |
| Ctrl+Alt+M | Mute |
| Ctrl+Alt+<, Ctrl+Alt+> | Previous or next file of the same type |

Audio shows cover art, tags, a live spectrum, and a waveform you click to
seek. On a video, press Enter to continue in your default player; mpv, VLC,
Celluloid, and MPlayer pick up where the preview stopped.

<!-- node: preview/preview-panel/documents, Rendered and Source -->
<!-- node: preview/preview-panel/documents, Tables and workbooks -->

Local Markdown, HTML, RTF, CSV, and TSV files open rendered. Click **View
source** in the header for the raw text, and **View rendered** to go back. To
start in source, turn off **Render documents by default** in the same
Browsing group. Local XLS, XLSX, and ODS files show
their first sheet as a sortable table, and local DOCX files render too.

<!-- node: preview/preview-panel/find -->

To search a preview:

1. Move focus into the preview and press Ctrl+F, or click **Find in
   preview**.
2. Type your text. Case is ignored.
3. Press Enter for the next match, Shift+Enter for the previous.
4. Press Escape to close find. The match stays selected for Ctrl+C.

Find skips rendered tables, PDFs, and media. With focus in the file list, Ctrl+F
filters filenames instead.

## Why previews are sandboxed

<!-- node: preview/preview-panel/sandbox -->

A file can be crafted to attack the program that reads it. So Strata decodes
images, RAW photos, PDFs, spreadsheets, DOCX, and media in a helper process
inside [Bubblewrap](https://github.com/containers/bubblewrap). The helper sees
only that one file, has no network, and is killed when you move on. Plain text
is read directly, up to the first 1 MiB.

If Bubblewrap is missing, these previews show **Preview unavailable**; Strata
never decodes them outside the sandbox. Install your distribution's
`bubblewrap` package.

**Full detail:** [Document previews](../reference/document-previews.md) and
[Preview sandbox](../reference/preview-sandbox.md).
