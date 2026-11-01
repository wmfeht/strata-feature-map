---
nodes: [preview/preview-panel, preview/preview-panel/layout, preview/preview-panel/documents, preview/preview-panel/find, preview/preview-panel/media, preview/preview-panel/media/audio, preview/preview-panel/media/video, preview/preview-panel/sandbox, preview/quick-preview, preview/quick-preview/folder-peek]
reviewed_at: be3343a5992a2a5497b1a2ee7faa525be18e988f
---

# Previews

See inside a file without opening it. Strata previews text, code, images,
PDFs, documents, spreadsheets, 3D models, GPS routes, audio, and video in a
panel beside your files.

## Show the preview panel

<!-- node: preview/preview-panel/layout -->
<!-- node: preview/preview-panel -->

In Columns, the default view, the panel is already on. In Icons and List it
starts hidden: click the view button in the header bar (your current view's icon,
tooltip **Appearance**) and click **Preview panel**. Click it again to hide
it.

Drag the divider to resize the panel. In a narrow window the preview hides
and media pauses until you widen it.

## Take a quick look

<!-- node: preview/quick-preview, Opening and closing -->
<!-- node: preview/quick-preview, Following the selection -->
<!-- node: preview/quick-preview, Keyboard ownership -->

Click a supported file and its preview opens (**Single-click file previews**
is on by default); in Columns, arrowing onto a file does too. Press Space to
close the preview, and again to reopen it.

- **Menu.** Right-click a file and choose **Quick preview**.
- **Follow.** With the preview open, arrow to another file and the preview
  follows.
- **Step inside.** In List or Columns, press Right to move focus into the
  preview. Ctrl+C then copies selected text, not files.

Space on a folder opens the folder instead.

## Peek into a folder

<!-- node: preview/quick-preview/folder-peek -->

Turn on **Settings → General → BROWSING → Folder peeking**; it is off by
default. Rest the pointer on a folder in Icons or List for half a second, and
a popover lists up to eight of its entries. Columns never peeks.

## Play media and read documents

<!-- node: preview/preview-panel/media -->
<!-- node: preview/preview-panel/media/audio -->
<!-- node: preview/preview-panel/media/video -->

Audio, video, and GIF previews open paused. To start them at once, turn on
**Settings → General → BROWSING → Autoplay media previews**.

| Keys | Action |
| --- | --- |
| Ctrl+Alt+Space | Play or pause |
| Ctrl+Alt+Left, Ctrl+Alt+Right | Seek 5 seconds |
| Ctrl+Alt+Up, Ctrl+Alt+Down | Volume up or down |
| Ctrl+Alt+M | Mute |
| Ctrl+Alt+<, Ctrl+Alt+> | Previous or next file of the same type |

On a video, press Enter to open it in your default player. Unless Strata runs
as a Flatpak, mpv, VLC, Celluloid, and MPlayer start where the preview stopped.

<!-- node: preview/preview-panel/documents, Rendered and Source -->
<!-- node: preview/preview-panel/documents, Tables and workbooks -->

Local Markdown, HTML, RTF, CSV, and TSV files open rendered. Click **View
source** for the raw text, and **View rendered** to go back. To
start in source, turn off **Render documents by default** in the same
BROWSING group. Local XLS, XLSX, and ODS files show their first sheet as a
sortable table, and local DOCX, ODT, and OTT documents render too.

<!-- node: preview/preview-panel, Images and PDFs -->

Ctrl+wheel over a PDF zooms its pages, and Ctrl+0 on a focused PDF resets
them; text size stays put. A password-protected PDF says so and
offers **Open** to unlock it in your PDF reader.

<!-- node: preview/preview-panel -->

Rendered STL and 3MF models turn through four camera views with **Previous
model view** and **Next model view**. GPX, FIT, and KML files draw their route
and elevation offline. **Settings → General → Units** switches between
kilometres and miles.

<!-- node: preview/preview-panel/find -->

To search a preview:

1. Move focus into the preview and press Ctrl+F, or click **Find in
   preview**.
2. Type your text.
3. Press Enter for the next match, Shift+Enter for the previous.
4. Press Escape to close find. The match stays selected for Ctrl+C.

Find skips rendered tables, PDFs, and media. With focus in the file list, Ctrl+F
filters filenames instead.

## Why previews are sandboxed

<!-- node: preview/preview-panel/sandbox -->

A file can be crafted to attack the program that reads it. So Strata decodes
images, PDFs, office documents, models, routes, and media in a helper process
inside [Bubblewrap](https://github.com/containers/bubblewrap). The helper sees
only that one file, has no network, and is killed when you move on. Plain text
is read directly, up to the first 1 MiB.

If Bubblewrap is missing, these previews show **Preview unavailable**; Strata
never decodes them outside the sandbox. To find what is missing, open
**Settings → Diagnostics** and click **Run**: a missing package shows its
install command.

**Full detail:** [Document previews](../reference/document-previews.md),
[Preview sandbox](../reference/preview-sandbox.md), and
[Keyboard navigation](../reference/keyboard-navigation.md#media-preview-keys).
