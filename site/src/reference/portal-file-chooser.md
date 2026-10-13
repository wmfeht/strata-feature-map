---
nodes:
  - integration/portal-file-chooser
  - integration/portal-file-chooser/setup
  - integration/portal-file-chooser/url-download
  - integration/portal-file-chooser/image-conversion
  - integration/portal-file-chooser/window-placement
  - integration/10xer-mode/file-chooser
  - app/packaging/installer
  - app/updates/install
reviewed_at: 0a086aa3bdb251842a1e8413e2a6b35970d0b409
---

# System file chooser

Strata can serve the XDG Desktop Portal FileChooser interface for portal-aware applications. Native file pickers and applications that do not use the portal are unchanged.

The chooser is deliberately limited to local files and folders. It uses the main app's sidebar, Columns/Icons/List views, List type grouping, filters, metadata, previews, and themed controls. Recent appears when enabled in sidebar preferences and supported by the desktop's recent-files backend; only local targets are listed. Overwrite confirmation uses the same in-window modal as the app.

Strata handles Open, Save, and Save Files requests. A request without a title is titled “Open Files”, “Save File”, or “Save Files”, and one without an accept label uses **Open** or **Save**. Without a usable folder hint, the chooser starts in your Downloads folder (`XDG_DOWNLOAD_DIR`), or Home when that is undefined. A folder hint that is relative, inaccessible, or unanswered within 3 seconds falls back the same way. A Save suggestion naming a file that does not exist yet opens its folder with the full name in **Name**. A Save Files request lists the names being saved in a **Files** row instead of a **Name** field.

File-type filters and application choices share a row beneath the filename that wraps in narrow windows. Application choices appear as checkboxes and dropdowns, and the values you pick go back to the application. Options in the filter and choice dropdowns are radio items, and the selected one is reported as checked. A long filter list scrolls inside its dropdown, which opens toward the side of its button with more room. A request may carry any number of filters and rules. A request fails without opening a window when it would be the 17th open at once, reuses a request handle, carries a string over 4,096 bytes, offers more than 16 choices, or has a glob rule over 256 bytes or with more than 2 wildcard groups. When the application closes its request, the chooser closes.

File-open requests include a **Name** field. Type an existing filename in the current folder, or paste a direct `http://` or `https://` file URL, then click **Open** or press Enter. Typing a folder's name and pressing Enter opens that folder and clears **Name**. A name typed while the folder is still loading is kept when the first row is selected automatically. A name with no matching file shows “Choose an existing, accessible file”, and a file the selected filter rejects shows “The file does not match the selected filter”; the chooser stays open for another try.

A URL downloads to a temporary local file returned to the requesting application. A compact circular progress indicator and cancel button appear at the bottom-left of the action bar; downloads without a known size show a spinner and bytes downloaded. Escape or the cancel button stops the download and leaves the chooser open for another name or URL. A network or HTTP failure, such as a 404, shows “Could not download the file: …” with the error. A download the selected filter rejects shows “The file does not match the selected filter” and is not returned. Chooser validation errors, including Name-field file lookup and URL download failures, appear as plain error text in the action bar rather than adding a row above it. The address bar remains navigation-only, pasting with Ctrl+V never starts a download, and downloads are unavailable in folder and Save requests.

Downloads are named from `Content-Disposition` (`filename*`, then `filename`) or the last URL path segment, or `download` when neither gives a name. They persist under a `strata-download-*` folder in the temp directory after the chooser closes, so the requesting app can still open them. Folders older than a day are swept when the portal starts or a new download begins. URLs with credentials are not downloaded. A URL that answers with a redirect shows “The URL redirects elsewhere; paste the direct file URL instead”.

If a downloaded JPEG, BMP, single-frame GIF or static WebP has no canonical filename matching the **selected filter**, but PNG would match, Strata validates the image in its sandbox and asks “Convert image to PNG?” with **Convert to PNG** / **Cancel**. Detection uses file contents, not the URL extension or HTTP content type. BMP detection requires `BM`, zero reserved bytes in its file header and a known DIB header size (12, 40, 52, 56, 108 or 124 bytes); `BM` alone is not enough.

When the bytes sniff as a JPEG, BMP, GIF, WebP or PNG image and the name lacks that format's extension, but the name with it (such as `.jpg` for JPEG bytes) passes the selected filter, Strata renames the download to that extension and returns it without asking, checking or converting. This extension repair runs even when the original name already passed the filter; a failed rename shows “Could not name the downloaded image: …”. If neither that kind's canonical name nor a PNG name matches, the normal filename filter still judges the download: it can be returned under its original server-provided name, such as JPEG bytes named `attachment.pdf` with a `*.pdf` filter. A `.png` name alone does not satisfy a PNG-only filter: JPEG, BMP, static WebP and single-frame GIF bytes still offer conversion. Under a filter that accepts PNG but not JPEG, a `.png` download whose bytes are not a supported image shows “This download is not a supported image. Choose a JPEG, BMP, static WebP, GIF or PNG image.” Bytes sniffed as PNG that the selected filter accepts under a PNG name open without conversion or sandbox validation, after any filename repair; that includes APNG and corrupt PNG data with a PNG signature.

Conversion preserves full resolution, transparency, orientation and compatible embedded colour profiles. An animated GIF or WebP shows “Animated images cannot be converted to PNG. Choose a static image instead.” during the check, without the conversion prompt. Other conversion inputs (including TIFF, SVG, AVIF and HEIC) are unsupported. An embedded ICC profile recognized by its `acsp` signature must have a colour space matching the decoded image, or conversion aborts. This intentionally rejects grayscale JPEGs carrying RGB profiles and CMYK profiles even when the JPEG decoder has emitted RGB pixels. An unprofiled CMYK JPEG skips that check and can be converted using the decoder's RGB output; Strata does not add colour conversion or strip incompatible profiles.

Image processing is cancellable and limited to 32 MiB input, 16 megapixels, 16,384 pixels per edge and the sandbox's memory/CPU/time limits. The separate 32 MiB encoded PNG output cap also applies: 16 megapixels of RGBA exceeds 32 MiB before compression, so an image within the pixel cap can still fail with “The converted PNG exceeds the 32 MiB output limit”. Either cap can reject conversion. The decoder's 128 MiB allocation budget is best-effort, not a hard memory bound; pre-decode dimensions and sandbox process limits provide the resource boundary.

Cancel, Escape, or a conversion failure leaves the chooser open without returning the incompatible original. Clicking Open again on the same URL reuses the downloaded file while it still exists. Changing the name or selected filter during the check, the conversion prompt, or the conversion stops the job and shows “The name or filter changed. Press Open to try again.” After successful conversion, both the cached original and the returned PNG remain in their temporary folders until the one-day sweep; closing the chooser does not remove either file.

Folder-only requests hide regular files in both directory listings and recursive results. File requests keep folders available for navigation. Changing a file-type filter refreshes the current results without clearing the search query; selection and acceptance follow the new filter. Local drives mounted before the chooser opened appear under **DEVICES** in its sidebar once the dialog has painted; network shares do not.

File Open requests show an **Open files read-only** checkbox; checking it tells the application to open the returned files read-only. In a single-selection request, selecting another item replaces the selection, including with Ctrl or Shift clicks and across grouped List sections, so **Open** returns one item. In Columns, a filter result selected in a column other than the active one is returned on **Open**. In a folder request, accepting while only the automatically selected first row is selected returns the displayed folder; an explicitly selected child folder returns that child.

In Save dialogs, selecting a file copies its name into the name input without accepting the dialog. Names that are not valid UTF-8 display with replacement characters, but Save still targets the selected file's exact name while the name input shows it unchanged. Edited name text is saved literally, replacement characters included; retyping the exact displayed text targets the original file again. The automatic initial selection does not change the suggested name or destination. Selecting a folder changes the destination without changing the name or navigating into it. In Recent, select a file to save in its containing folder, or navigate to a local folder first. Saving over an existing file asks “Replace existing file?” (“Replace existing files?” for several) with **Cancel** focused; **Cancel** keeps the chooser open and **Replace** returns the path. Saving where a folder of the same name exists fails with “A folder named “name” already exists”.

Resizing a Miller column or a List heading in the chooser saves that width as the chooser default, so the next request opens with it. Dragging or double-clicking a Miller column edge stops at the dialog's file area beside the sidebar, and a saved width wider than that area opens narrowed to it. Regular Strata windows also remember widths, using separate browser defaults.

A Wayland application's exported parent handle makes the chooser a transient dialog of that application's window. X11 parent handles are ignored, and those requests open as standalone windows.

### Destination choosers

The same chooser window serves Strata's own **Move to…**, **Copy to…**, **Extract to…**, and **Send to… → device → Choose folder…** commands. It opens as a floating modal folder chooser over the window the command came from. Invoking another destination command while one is open brings the existing chooser forward instead of opening a second. Closing the originating window closes its chooser, and **Cancel** leaves the files and the window's location unchanged.

Move to, Copy to, and Extract to offer **New Folder**. Enter in the path entry navigates there; Ctrl+Enter in the file list or the action button confirms the displayed folder, or a child folder you explicitly selected. For Send to, the sidebar and its toggle are hidden, and Ctrl+B (Ctrl+N in 10xer mode) and Ctrl+Shift+B leave them hidden. Send to also disables **New Folder** in the menu, the toolbar, and Ctrl+Shift+N. Navigating outside the device shows “Choose an existing folder inside this removable device.”

### Initial size

The chooser opens at 80% of its bound's width and 78% of its height, leaving at least 120 px and 100 px. The result is clamped between 640×460 and 1000×680 px. On a bound under 760 px wide or 560 px tall, the 640×460 minimum overrides that clearance; a bound smaller than 640×460 caps the minimum at the bound. The bound is the monitor. With a parent size it is the smaller of the monitor and the parent in each dimension, or the parent alone when monitor geometry is unavailable. With neither, the chooser opens at 920×580. Destination choosers use their originating window's current size as the parent size on any compositor. Moving the chooser to another monitor keeps a manual resize.

### Initial size in split-window layouts

On Hyprland, requests with a Wayland parent and an application ID can use the
requesting application's window size as an initial sizing hint. Strata queries
Hyprland's local IPC socket before loading the requested directory, and uses the
hint only when exactly one window's current or initial class matches the app ID
(case-insensitively). A sole matching window that is unmapped, hidden, or zero-sized
gives no hint. The query is read-only, limited to 100 ms and a 1 MiB reply,
and does not depend on which window has keyboard focus. Monitor dimensions still
cap the result.

The exported Wayland handle does not expose parent geometry. Other compositors,
X11 requests, missing or differently named app IDs, multiple matching windows,
and unavailable IPC retain monitor-based sizing. This is a best-effort improvement,
not guaranteed parent-relative sizing on every desktop. GTK's compositor bounds
and the controls' minimum usable size continue to apply.

### Initial placement on Hyprland

On native Wayland under Hyprland, floating choosers open at the center of their
monitor by default, rather than at the center of the calling application. The portal process identifies its
windows as `io.github.lgse.Strata.FileChooser`, separate from the normal file
manager's `io.github.lgse.Strata` identity.

Before showing a chooser, Strata registers the named runtime rule
`strata-file-chooser-center` through Hyprland's IPC socket. The rule matches only
the chooser identity and sets `center`; it does not force floating, resize the
window, or remove its parent/modal relationship. No Hyprland configuration files
are edited. The same rule is refreshed before each chooser, so it also works
after a compositor configuration reload without accumulating rules.

Both Lua and legacy configurations with named window-rule support are handled.
The entire placement request has a 100 ms deadline; unsupported rules, unavailable
IPC, and other compositors retain compositor-default placement. Centering does
not require identifying the calling application's size. Destination choosers
register the same rule and use the chooser identity, so they open centered too.
Regular Strata windows keep their usual placement.

## Opt in through the app or installer

<!-- node: integration/portal-file-chooser/setup, Portal installation -->
<!-- node: integration/portal-file-chooser/setup, Settings row -->
<!-- node: app/packaging/installer -->

Strata never replaces your Open and Save dialogs on its own. **Nothing changes
without consent.** Enable it in **Settings → General → System file manager**,
during installation, or with `strata --install-portal`.

The Settings row sets the file chooser together with folder opening and Reveal in
File Manager. The installer and the `--install-portal` and `--uninstall-portal`
commands change only the file chooser; the installer asks about folder handling
in its own questions.

The installer asks about the file chooser separately, defaulting to **No**, after
placing the binary at its permanent path. For unattended installation,
`--with-file-chooser` opts in and `--without-file-chooser` keeps your current
chooser. Either flag implies `--non-interactive`, so the installer asks nothing
and declines every integration you do not name. A plain `--non-interactive`
install also leaves the chooser unchanged.
`--with-file-chooser` fails on a release without portal support.

A declined installer question or `--without-file-chooser` runs
`strata --dismiss-portal-prompt`. That command only creates
`${XDG_CONFIG_HOME:-~/.config}/strata/portal-opt-in-v1` and leaves portal
preferences unchanged; Strata itself never asks on launch, whether or not the file
exists.

### System file manager in Settings

**Settings → General → System file manager** lists **Open and Save dialogs**,
**Opening folders**, and **Reveal in File Manager**, each marked configured or not.
On Omarchy it also lists **Keyboard shortcuts**; elsewhere that line is hidden.
Close open file dialogs before changing setup.

**Complete setup** installs the file chooser portal, makes Strata
(`io.github.lgse.Strata.desktop`) the `inode/directory` handler, and installs the
per-user FileManager1 service used by Reveal in File Manager. It is hidden once
every line is configured. It fails with “Another per-user FileManager1 provider is
already installed: …”, followed by the conflicting service file's path, when
another user service already owns that name.

On Omarchy 3 or 4, **Complete setup** also binds Super+Shift+F and
Super+Alt+Shift+F to Strata in `$XDG_CONFIG_HOME/hypr/bindings.conf`, or
`bindings.lua` on Omarchy 4. Each change to the bindings file first keeps a
`strata-keybind-backup-` copy of the previous file beside it, or beside the link
when the bindings file is a symlink. If Hyprland's `hyprctl configerrors` then
reports errors, the previous file is restored and the error names the backup.

A user-owned symlinked bindings file is written through the link, which stays a
link, including during that rollback. An existing bindings file keeps its
permission bits, so a `0644` file stays `0644`. With a dangling link, **Complete
setup** fails with an error naming the missing target and does not create it. The
steps that ran first still apply: the file chooser, the folder handler, and the
FileManager1 service are installed, and an empty `strata-keybind-backup-` file is
left beside the link. A link,
or a target reached through one, owned by another user makes **Complete setup**
and **Restore default** fail and leaves the target unchanged.

**Restore default** appears while any part is installed. It removes the
FileManager1 service and the file chooser portal. It returns `inode/directory` to
the handler recorded at setup, or to Nautilus when none was recorded, and leaves it
alone when it no longer points to Strata. With no recorded handler and no Nautilus,
it fails with “No previous folder handler was recorded and Nautilus was not
detected. Choose another default file manager first, then retry Restore default.”

On Omarchy, **Restore default** replaces the Strata shortcut block with
`nautilus --new-window` bindings. When Nautilus is not detected, it fails with
“Nautilus was not detected; the Strata keyboard shortcuts were left unchanged.”
In that case, and when the shortcut block fails the checks below, the folder
handler step has already run, but the shortcuts, the FileManager1 service, and the
file chooser portal stay installed until you fix the cause and run **Restore
default** again. With a dangling bindings link, it leaves the shortcuts and the
link unchanged.

A hand-edited Strata shortcut block shows **Keyboard shortcuts** as not
configured, and both **Complete setup** and **Restore default** fail with “The
Strata keyboard shortcuts have been customized; restore them manually to avoid
losing your edits.” A start marker without an end marker, or the reverse, or a
repeated marker makes them fail with “The Strata keyboard shortcut block is
ambiguous; restore it manually.”, and an end marker before the start with “The
Strata keyboard shortcut block is malformed; restore it manually.” **Complete setup** leaves the bindings file unchanged in each case, but
the steps that ran first still apply, as with a dangling link.

## Per-user installation

<!-- node: integration/portal-file-chooser/setup, Portal installation -->
<!-- node: integration/portal-file-chooser, Requests -->
<!-- node: integration/portal-file-chooser/setup, Updates -->
<!-- node: app/updates/install -->

Ensure `xdg-desktop-portal` is installed. The Arch/Omarchy installer includes it
when file chooser integration is selected. Close active file dialogs before
enabling or restoring the chooser: setup restarts the portal frontend.

Install Strata at a stable absolute path, then run:

```bash
strata --install-portal
```

This installs the portal metadata and D-Bus activation service below `$XDG_DATA_HOME`, makes Strata the preferred FileChooser while retaining the active backends as fallbacks, stops any running Strata chooser backend, reloads D-Bus, and restarts the portal frontend. If no user portal configuration exists, Strata copies the active desktop configuration before changing the FileChooser preference. The command records whether that user override was created or modified so it can be removed safely later.

The chooser backend is activated on demand and exits after about two minutes without an active request (checked every 10 seconds). An open dialog (including a pending request) keeps it running; closing the last dialog starts the idle countdown again. When Strata is the configured file chooser, an in-app update restarts the portal services so the next dialog runs the new binary. In-app updates also stop your other Strata windows and `strata --portal` chooser processes running the old binary from the same install path: they receive SIGTERM, then SIGKILL after 5 seconds. Processes started with other flags, such as preview helpers or a `strata --gapplication-service` instance started by Reveal in File Manager, other users' processes, and Strata binaries from other install paths keep running. Strata then relaunches the updating window with the replacement binary.

External package-manager updates and manual binary replacements do not run that retirement step. The next time you launch Strata, it restarts the portal services if a running `strata --portal` from the same install path was started from the replaced executable. Other old Strata windows keep running until you close them or log out.

If a stop, reload, or restart step fails, `--install-portal` and `--uninstall-portal` print “Could not reload every portal service. Ensure xdg-desktop-portal is installed, then log out and back in before testing.”

The generated D-Bus service contains the absolute path of the command being run. Move Strata to its permanent location before installing the portal. For safe activation, every component of the canonical executable path must be owned by the current user or root and must not be group- or world-writable. D-Bus service-file argument parsing is not shell quoting, so the installer also rejects executable paths containing whitespace, quotes, or backslashes.

### Manual installation

Run the equivalent commands below from the extracted release archive. They use the default XDG locations and an existing installation at `~/.local/bin/strata`:

```bash
data_home="${XDG_DATA_HOME:-$HOME/.local/share}"
config_home="${XDG_CONFIG_HOME:-$HOME/.config}"
strata_executable="$(readlink -f "$HOME/.local/bin/strata")"
strata_replacement="${strata_executable//\\/\\\\}"
strata_replacement="${strata_replacement//&/\\&}"
strata_replacement="${strata_replacement//|/\\|}"

install -d "$data_home/xdg-desktop-portal/portals" \
  "$data_home/dbus-1/services" \
  "$config_home/xdg-desktop-portal"
install -m 644 portal/strata.portal \
  "$data_home/xdg-desktop-portal/portals/strata.portal"
sed "s|@STRATA_EXECUTABLE@|$strata_replacement|" \
  portal/org.freedesktop.impl.portal.desktop.strata.service.in \
  > "$data_home/dbus-1/services/org.freedesktop.impl.portal.desktop.strata.service"
chmod 644 "$data_home/dbus-1/services/org.freedesktop.impl.portal.desktop.strata.service"
gdbus call --session \
  --dest org.freedesktop.DBus \
  --object-path /org/freedesktop/DBus \
  --method org.freedesktop.DBus.ReloadConfig
```

The generated D-Bus service must contain an absolute `Exec=` path. If that path contains whitespace, quotes, or backslashes, install Strata somewhere else; D-Bus service-file argument parsing is not shell quoting.

Edit the portal configuration the frontend uses for your desktop, as `strata --install-portal` does. In `$config_home/xdg-desktop-portal/`, that is the first existing `<desktop>-portals.conf` for a lowercased name in `XDG_CURRENT_DESKTOP`, such as `hyprland-portals.conf`, otherwise `portals.conf`. If neither exists there, copy the active desktop configuration into that directory, keeping its file name: the first such file in the system directories, usually `/etc/xdg/xdg-desktop-portal/` or `/usr/share/xdg-desktop-portal/`. Create `portals.conf` only when no configuration exists anywhere. A user file outranks the system one, so a file holding only the FileChooser line would drop the desktop's other preferences. Preserve the file's existing `[preferred]` section and settings, and merge Strata into the FileChooser preference:

```ini
[preferred]
org.freedesktop.impl.portal.FileChooser=strata;<existing-backend>;
```

Replace `<existing-backend>` with the backend already configured for the desktop, such as `gtk` or `gnome`. Do not install the placeholder literally and do not replace unrelated portal preferences. The archive's `portal/portals.conf` is an example, not a complete desktop configuration.

Restart the frontend so it rereads portal metadata and preferences:

```bash
systemctl --user restart xdg-desktop-portal.service
```

On a desktop that does not manage the frontend as a systemd user unit, log out and back in instead.

## Keyboard navigation

<!-- node: integration/portal-file-chooser, Browsing -->
<!-- node: integration/portal-file-chooser, Accepting -->
<!-- node: integration/10xer-mode/file-chooser -->

- File selection fills, keyboard cursor outlines, and pointer-hover suppression
  use the main app's shared input-ownership styling, including when switching back
  to keyboard navigation after using the mouse.
- With 10xer mode off, file-open and single-file Save dialogs start with visible
  focus in **Name**; Save selects the suggested filename. Folder and Save Files
  requests start on the sidebar toggle. If focus is lost, an arrow returns it to
  the same place without a click.
- Tab/Shift+Tab traverse controls; arrows move between toolbar icons and options.
  The file list is a single Tab stop (the whole strip in Columns), and Tab into
  it lands on the keyboard cursor.
- Up from the first file row reaches the pane toolbar; Down returns to files.
  With **Keep arrows in file list** on in **Settings → General**, arrows stay in
  the file list: use Tab or Shift+Tab to reach the toolbar and Ctrl+Shift+B to
  reach the sidebar. In 10xer mode, arrows also stay in the file list.
- Icons arrows follow the visual rows and columns. List arrows follow the
  displayed order, including type grouping. Shift+arrows extend or shrink a range
  across groups; plain arrows select only the focused item.
- Space/Enter activate focused buttons and toggles. Down or Enter opens a focused
  dropdown; its arrows and Enter select an option.
- Enter or Shift+Enter on a focused file accepts the request. In a
  multiple-selection request with files selected, it returns every selected file,
  the same as **Open**, even when the focused file is outside the selection. With
  a folder and files selected, it returns only the files. Enter on a folder opens
  it, even with files selected.
- Ctrl+1, Ctrl+2, and Ctrl+3 switch to Columns, Icons, and List. F5 refreshes;
  Ctrl+H or Ctrl+. toggles hidden files. Ctrl+A in the file list selects all only
  in multiple-selection requests.
- With **Type to search** on (the default) and the file view focused, typing a
  printable character opens the filter seeded with it; `/` opens an empty filter.
- Ctrl+click moves focus to the item it toggled, so the preview follows it.
  Dragging from blank space draws a marquee only in multiple-selection requests.
  A blank click in the file list or sidebar clears the selection in every request.
  A plain click on blank space in a preview that is showing something keeps the
  selection; in multiple-selection requests, dragging from it into the file list
  starts a marquee.
- With folders set to open on a single click, a single click on a folder in Icons
  or List opens it, and a single click on a file only selects it. With single-click
  previews on, clicking a previewable file opens the shared preview pane.
- Dragging a Miller column's right edge resizes it; double-clicking the edge fits
  it to its content.
- F2 renames a single selected file or folder. The editor opens with a file's
  name before its last `.` selected, and a folder's whole name selected. Escape
  cancels the name editor without closing the chooser. Right-click an item for Rename, Properties,
  Compress… (local items), Move to Trash and Permanently delete (where the
  location allows them), and Quick preview for one previewable file; right-click
  empty pane space for New Folder. Alt+Enter opens Properties from the file list.
  Properties preserves multi-selection, while Rename is disabled for multiple
  selected items.
- With the file view focused, Delete moves the selection to Trash and Shift+Delete
  asks to delete permanently. Where the open folder has no Trash but allows
  deletion, Delete asks to delete permanently and explains why.
- Text fields keep their cursor keys and Ctrl+A; Ctrl+A in the filename entry
  selects its text, not files. Ctrl+L edits the location; Ctrl+F opens the pane
  filter.
- Ctrl+Shift+N or the **New Folder** button beside Refresh creates `new folder`
  (or the first free `new folder (1)`, `new folder (2)`, and so on) and selects its
  name for editing. Enter or clicking away commits a valid name. Escape or an
  empty or invalid name keeps the default name, and the folder stays.
- Ctrl+B (Ctrl+N in 10xer mode) or the sidebar toggle in the top bar shows or hides
  the sidebar. Unless arrows are kept in the file list, Left from the outer
  file-list edge or a leftmost Icons cell focuses the visible sidebar.
  Ctrl+Shift+B also focuses it, first showing the sidebar if it is hidden; in
  10xer mode it does nothing while the sidebar is hidden. Right returns to files
  without changing selection. Up from the first sidebar row reaches the sidebar toggle.
- Space on a file toggles preview. In a folder-selection request, Ctrl+Enter in
  the file list accepts the same as **Open**: it returns the displayed folder, or
  a child folder you explicitly selected.
- Escape dismisses the innermost menu, dropdown, inline edit, filter, location
  edit, preview, download, or confirmation before cancelling the request. Escape on
  a focused filter result dismisses the filter and keeps the request open.
  The Replace prompt, the image conversion prompt, and the delete confirmation
  for a folder without Trash initially focus Cancel. The Shift+Delete
  “Permanently delete …?” confirmation initially focuses its delete button.

### With 10xer mode on

- With [10xer mode](10xer-mode.md#file-chooser) on, the chooser follows the saved
  preference and live changes to it, and uses that keymap and footer within the
  request's limits. The pane chrome hides; Accept, Cancel, the close button, and
  List headings stay. The sidebar toggle's tooltip names Ctrl+N. Turning the mode
  off restores the chooser's own keys.
- Every request starts with focus in the files. Enter or `o` on a file chooses
  it; in a multiple-file request with a fill, they choose the fill. Enter or `o`
  on a folder opens it. The request takes the fill, or the cursor item when
  nothing is filled; the automatic first-row selection never counts.
- Escape takes one dismissal step (prompt, filter, search, find, range, preview,
  fill) and then cancels the request. `q` neither ends the request nor leaves the
  mode; Ctrl+Shift+M leaves the mode with the request still open.
- F1 shows a reference listing only the keys the request allows; Escape closes
  it without cancelling. The `g` panel leaves out `g t`, `g n`, `g +`, and
  `g −`, and `t` does not start a tab chord. `f` and `s` hits follow the
  request's folder-only and file-type limits.
- Tab moves from the files to the header, then to **Name** when the request has
  one, then back to the files. While **Name** or the location field has focus,
  every key is typed except F1, Ctrl+Shift+M, and Escape. Escape in **Name**
  returns to the files and keeps the edit; Escape in the location field cancels
  the edit and returns to the files.
- In a Save request, Enter in the files saves the name in the current folder,
  whatever the cursor is on; moving the cursor changes neither the name nor the
  folder. In a single-file Save request, `r` or F2 edits **Name** with the part
  before the extension selected, and `o` on a file saves over it after a Replace
  prompt with Cancel focused. Beside Cancel and Save, a single-file Save request
  shows Enter, `r`, and `o` hints; a Save Files request shows only the Enter
  “Save here” hint.
- `y`, `x`, `p`, `P`, `Y`, `X`, `M`, `C`, `R`, `O`, `;`, `i`, `g +`, `g −`,
  `Q`, Ctrl+C, Ctrl+X, and Ctrl+V flash “Not available in the file chooser”.
  In a single-item request, Space, `v`, `V`, Ctrl+A, and Ctrl+R flash “Only one
  item can be chosen”. `g t`, `g n`, and remote pins flash “Only local folders
  can be opened here”. `a`, `d`, `D`, sort chords, `.`, `c c`, and `c n` work as
  in a window, and so do `r` and F2 outside single-file Save requests.

## Verification

<!-- node: integration/portal-file-chooser, Requests -->
<!-- node: integration/portal-file-chooser, Browsing -->
<!-- node: integration/portal-file-chooser/url-download, URLs -->
<!-- node: integration/portal-file-chooser/setup, Portal installation -->

Confirm that D-Bus can activate Strata and that it advertises FileChooser version 4:

```bash
gdbus introspect --session \
  --dest org.freedesktop.impl.portal.desktop.strata \
  --object-path /org/freedesktop/portal/desktop
gdbus call --session \
  --dest org.freedesktop.impl.portal.desktop.strata \
  --object-path /org/freedesktop/portal/desktop \
  --method org.freedesktop.DBus.Properties.Get \
  org.freedesktop.impl.portal.FileChooser version
```

The second command should report `uint32 4`. Then open or save a file from a portal-aware application. Only local locations appear in the picker; entering a remote URI in the address bar shows “The system file chooser supports local files and folders only.” File-open requests accept direct `http(s)` URLs through the Name field.

Portal backend selection happens before a request is sent. Keeping the existing backend after `strata;` lets the frontend choose it when Strata's `.portal` metadata is absent. It does not provide live failover if an already-selected Strata backend crashes during a request.

## Uninstall

<!-- node: integration/portal-file-chooser/setup, Portal installation -->

Run the matching per-user command:

```bash
strata --uninstall-portal
```

It removes Strata's metadata and activation service and restores the previous user portal configuration. If the configuration changed after installation, it preserves those changes and removes only Strata from the FileChooser preference. It then stops any running Strata chooser backend, reloads D-Bus, and restarts the portal frontend. If the frontend cannot be restarted automatically, log out and back in.

For a complete Strata uninstall, also remove the application binary and desktop entry as described in [Update or uninstall](install.md#3-update-or-uninstall).

### Manual uninstall

Remove the Strata metadata and activation service:

```bash
data_home="${XDG_DATA_HOME:-$HOME/.local/share}"
rm -f "$data_home/xdg-desktop-portal/portals/strata.portal" \
  "$data_home/dbus-1/services/org.freedesktop.impl.portal.desktop.strata.service" \
  "$data_home/strata/portal-install/state.toml"
rmdir "$data_home/strata/portal-install" 2>/dev/null || true
gdbus call --session \
  --dest org.freedesktop.DBus \
  --object-path /org/freedesktop/DBus \
  --method org.freedesktop.DBus.ReloadConfig
```

`strata --install-portal` edits the user configuration named after your desktop, such as `hyprland-portals.conf` on Hyprland, and `portals.conf` only when no desktop-specific file applies. Edit each `portals.conf` or `<desktop>-portals.conf` file in `${XDG_CONFIG_HOME:-$HOME/.config}/xdg-desktop-portal/` that lists `strata`, remove `strata;` from the FileChooser preference, and keep the previous backend. If that file did not exist before you installed the portal, delete it instead. Then restart the portal:

```bash
systemctl --user restart xdg-desktop-portal.service
```
