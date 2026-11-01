---
nodes: [settings/themes, settings/themes/omarchy, settings/themes/icons, settings/preferences, preview/preview-panel]
reviewed_at: be3343a5992a2a5497b1a2ee7faa525be18e988f
---

# Themes reference

Strata styles the interface with nine semantic color tokens. Bundled themes are the fallback on any Linux desktop. A fresh install without Omarchy starts with Tokyo Night, and the saved selection survives restart. If the saved theme matches no bundled or custom theme, Strata falls back to Azure Glow at startup.

Open Settings with the header **Settings** button or Ctrl+,, then choose **Appearance**. Under **THEME LIBRARY**, Strata lists the 95 bundled themes in alphabetical order in one scrolling library. Typing in **Search themes** hides cards whose names do not contain the query, ignoring case. In **Search themes**, Ctrl+A selects the query on any keyboard layout; Ctrl+Shift+A, Ctrl+Alt+A, and Ctrl+Super+A do not. The **All**, **Light**, and **Dark** filter combines with the query. A theme counts as Light when its background's relative luminance exceeds 0.4, whatever color form the background is written in.

Clicking a card applies the theme immediately across the interface, marks the card with a check, and keeps that theme active across restarts. While **Follow Omarchy** is on, the library is disabled; turn off Follow Omarchy to pick a theme.

Tinted Base16 entries map colors to Strata tokens as follows: `base00` to background, `base01` to surface, `base05` to text, `base0D` to accent, `base08` to danger, `base02` to muted and highlight, `base03` to border, and `base04` to dim text. Every bundled theme's text and dim text have at least 4.5:1 contrast on its background and 3:1 on its surface. A few bundled entries override the mapped text to meet that: Material Lighter draws text in `#455A64` (6.94:1 on its background), and Material Vivid draws text in `#9e9e9e` (6.01:1). The catalog comments each override next to the value. When a bundled theme's dim text misses those floors, Strata blends it toward the text color at load, in 1/255 steps, and stops at the first step that passes, so it stays dimmer than text. Tokyo Night's `#737aa2` loads as `#767da6`, and Material Lighter's `#607D8B` as `#5c7785`. A custom theme file keeps its dim text as written, even below those floors. Source revision and licensing details are recorded in [`THIRD_PARTY_LICENSES.md`](https://github.com/lgse/strata/blob/v1.1.1/THIRD_PARTY_LICENSES.md).

## GTK CSS precedence

<!-- node: settings/themes, Styling and effects -->
<!-- node: settings/themes/icons, GTK control icons -->

Strata defines its nine named colors as `@strata_bg`, `@strata_surface`,
`@strata_text`, `@strata_accent`, `@strata_danger`, `@strata_muted`,
`@strata_highlight`, `@strata_border`, and `@strata_dim_text`. These replace the former
`@theme_*` names; user stylesheets referencing those names must be updated.
Custom theme TOML keys are unchanged. User CSS that redefines the former
`@theme_*` names no longer changes Strata's colors.

Strata isolates its appearance from desktop GTK styling:

- A rule in `~/.config/gtk-4.0/gtk.css` changes no property of Strata's
  widgets, such as `label { color: red }`, `button { min-width: 60px }`, or
  `* { outline: 3px solid red }`. The file stays without effect after switching
  between a light and a dark Strata theme. To restyle Strata, use the
  [user stylesheet](#user-stylesheet) instead.
- A desktop GTK theme chosen through the settings portal or `settings.ini`
  does not style Strata: once Strata starts, GTK's `gtk-theme-name` reads
  `StrataEmpty`, an empty theme bundled with Strata. A user theme folder of
  that name, such as `~/.local/share/themes/StrataEmpty/gtk-4.0/gtk.css`,
  does not style Strata either.
- Launching with `GTK_THEME` set, such as `GTK_THEME=Adwaita:dark`, restarts
  Strata without that variable, as a browser or as the portal file chooser.
- GTK's built-in dark variant applies when the Strata theme's background
  (299R + 587G + 114B) ÷ 1000 is below 128 or cannot be parsed, and the light
  variant otherwise. The desktop color scheme is ignored, and GTK's
  high-contrast variant is never used, whatever the desktop's contrast setting.
- Every dropdown and menu-button arrow, such as on **Settings → General →
  Language**, draws one bundled chevron under any icon theme. The Text size,
  Corner roundness, and Thumbnail workers steppers, and the spin buttons in the
  **Customize…** custom color editor, draw bundled − and + steps. Those steps
  follow the control's color, including hover and disabled states. Open With
  application icons still come from the desktop icon theme.

### User stylesheet

<!-- node: settings/themes, User stylesheet -->

To restyle Strata itself, create an optional stylesheet:

```text
~/.config/strata/style.css
```

The file follows `$XDG_CONFIG_HOME`, so with `XDG_CONFIG_HOME=/tmp/cfg` Strata
reads `/tmp/cfg/strata/style.css`. Without the file, Strata's appearance is
unchanged. When the file is present at startup, its rules apply in every window
and override Strata's own rules and the active theme. Rules may use the active
theme's `@strata_*` colors; switching themes keeps the override and updates
those colors. The `@strata_*` namespace prevents accidental collisions with
other stylesheets' `@theme_*` colors; it does not stop a deliberate `@strata_*`
redefinition in this file.

```css
/* A floating, rounded sidebar */
.sidebar-shell {
    margin: 8px 0 8px 8px;
    border-right: none;
    border-radius: 14px;
    background: alpha(@strata_surface, 0.6);
}

/* Let the card show through the sidebar's own opaque layers */
.sidebar-shell .sidebar-scroll,
.sidebar-shell .sidebar-scroll viewport,
.sidebar-shell .sidebar {
    background: transparent;
}
```

Creating, editing, or deleting the file while Strata runs re-applies it in
every open window without a restart. Changes less than 75 ms apart trigger one
reload, 75 ms after the last. Deleting the file, or making it unreadable,
restores the default appearance; an unreadable file logs "cannot read user
stylesheet". A rule GTK cannot parse, such as `label { color: nope; }`, is
skipped with an "invalid rule in user stylesheet" warning, and the file's valid
rules still apply. [Corner roundness](#corner-roundness) does not scale radii
the file sets. Class names are not a stable interface and may change between
releases.

### Corner roundness

<!-- node: settings/themes, Styling and effects -->
<!-- node: settings/preferences, Settings search -->

**Settings → Appearance → SHAPE → Corner roundness** is a stepper from 0 to 200
percent in steps of 10, described "Percent of the default corner radius,
0–200. 0 squares every corner." Its accessible name is "Corner roundness in
percent". With no saved value it reads 60; the choice is saved as the integer
`corner_roundness`, and a saved value below 0 or above 200 loads as 0 or 200.
Searching "Corner roundness", "radius", or "rounded" in **Search settings**
finds the row.

The value scales every pixel corner radius in Strata's stylesheet: at 0 each
becomes 0px, and at 200 each doubles, so 5px becomes 10px. A scaled radius is
rounded to 0.01 px, so 9px at 40% becomes 3.6px. Percentage radii, which draw
circles, and radii written as `0` stay unchanged. Radii that GTK's built-in
theme supplied, such as on buttons, entries, popovers, and check boxes, scale
too. A change applies at once in every open window, dialog, menu, and rebuilt
view, and in every open Settings window's stepper; a saved value applies before
Settings opens.

Every switch has a 24px track radius and a 20px knob radius at 100%, so 14.4px
and 12px at the default 60%. At 50% and above both are full circles. Below
50%, the track and knob square off together and stay concentric: at 40% the
track radius is 9.6px and the knob's 8px.

### Interface font

<!-- node: settings/themes, Styling and effects -->
<!-- node: settings/preferences, Settings search -->

**Settings → Appearance → TEXT → Interface font** sits before Text size and
reads "The typeface for menus, file lists, and dialogs. File previews keep a
monospace font." Its button shows the saved family, or "Default" when none is
saved, and follows a change made in any other open Settings window.

The picker lists **Default** first, then the installed font families sorted
without regard to case and without duplicates, each name drawn in the
interface font. The current choice has a check mark. Each time the picker
opens, **Search fonts** is cleared and focused; typing keeps families whose
name contains the query, ignoring case, and "No fonts match" replaces an empty
list. The list is collected the first time a Settings window opens the picker,
so a font installed later appears in a new window's Settings or after a
restart. Searching "font", "typeface", or "family" in **Search settings** finds
the row.

Clicking a family saves `interface_font = "<family>"` in `settings.toml` and
closes the picker; clicking **Default** removes the key. A saved family applies
before Settings opens, and a change applies at once in every open window,
popover, menu, and dialog. Text, source, and command previews keep JetBrains
Mono. A saved family that is not installed falls back to JetBrains Mono, and the
button still shows the saved name. A family name containing `"` or `\` applies
without a stylesheet error. The font is independent of text size.

### Frame density

<!-- node: settings/themes, Frame density -->

The window's Appearance menu has a **DENSITY** section with **Frame** and
**Content** sliders. Frame, from 0 to 12 px, sets one inset shared by the
browser's bars, so their heights stay aligned. At a Frame value N above 0:

- The browser header, tab strip, Icons and List pane header, preview header,
  and sidebar rows get N px top and bottom padding.
- Miller column headers get N px top and N+2 px bottom padding.
- Action buttons in the browser header, tab strip, Miller column headers, pane
  header, and preview header, and List navigation buttons, get an N px left
  margin. The sidebar toggle stays aligned with the sidebar icons.

Frame 0, **Compact**, adds no style, leaving the bars as they were before the
setting existed.

### Element glow, motion, and renderer

<!-- node: settings/themes, Styling and effects -->

**Settings → Appearance → EFFECTS → Element glow** is on by default and saved
as `element_glow = true`. It adds accent glow to dialogs, menus, theme cards,
and animated feedback. The video preview's
[ambient light](preview-sandbox.md#video-previews), and the 24 px band it needs
around the frame, follow the same switch, live in an open preview.
Turning it off removes that glow in every window at once, keeps focus
outlines, depth shadows, and animation movement, and persists across restarts;
use Reduce motion to stop animations. With Element glow off, the path
completion and folder peek popovers draw no shadow, so no white halo shows on
light themes; with it on, each shows only the accent glow.

**Settings → Appearance → MOTION → Reduce motion** stops sidebar, column, and
preview animations. GTK's `gtk-enable-animations` set to false stops the same
animations even when Reduce motion is off. Strata's stylesheet ignores the
desktop's `prefers-reduced-motion` media preference.

**Settings → Appearance → RENDERING → Interface renderer** offers
**GTK default**, the initial choice, and **Cairo**, saved as
`interface_renderer = "system"` or `"cairo"`. Cairo avoids text artifacts on
some displays but can use more CPU. Choosing a value other than the one Strata
started with shows **Restart now**; the change applies only when a new Strata
process starts. **Restart now** closes every Strata window and starts Strata
again; while a file operation or drive format runs, the usual close warning
appears instead and nothing restarts. Without the button, quit Strata by
closing all of its windows, then reopen it: closing one window while others stay
open keeps the old renderer. The choice and **Restart now** stay in step across
open Settings windows. A `GSK_RENDERER` environment variable set before Strata
starts, even to an empty value, overrides the saved choice. When Strata selects
Cairo itself, applications it launches may inherit that renderer; desktop
settings are unchanged.

Whatever the renderer, on GTK 4.16 or later Strata sets GTK's
`gtk-font-rendering` to manual for its own process at startup; the desktop's
setting is unchanged. Under GL or Vulkan, glyphs such as `T`, `E`, and `I` then
keep their top pixel row at sizes where they lost it, so "Trash" no longer
reads "Irash". Manual rendering follows the desktop's antialiasing and hint
style. On GTK older than 4.16, Strata leaves font rendering as it is.

### Icon colors

<!-- node: settings/themes/icons, Color -->
<!-- node: settings/themes, File icon colors -->
<!-- node: settings/preferences, Settings search -->

Interface icons in the header and sidebar, and Lucide file-type icons, draw
in the theme's accent at full opacity. In Settings, the navigation, close, and
search icons, and the About and release-notes icons, draw in the accent at
65% opacity, with no desaturation; the active page's navigation icon draws at
full opacity. The Strata logo on **Settings → About** draws in the theme's text
color on a surface-colored tile with a 1px border in the border color. Destructive menu items, such as **Permanently delete**, and danger-tone
dialogs draw their icon in the danger color. Changing the theme or Omarchy
variant recolors icons, including Catppuccin file icons and the About logo, in
every open window.

**Settings → Appearance → FILE ICONS → File icon colors** offers
**Brand colors**, the default, and **Theme colors**. The choice is saved as
`file_icon_colors = "brand"` or `"theme"`, a missing key reads as Brand colors,
and a change applies in every open window at once. Typing
"catppuccin", "brand palette", or "monochrome" in **Search settings** finds
this row.

- **Brand colors** draws Catppuccin file icons in their own Mocha palette on
  dark backgrounds and Latte on light ones. A background counts as dark when
  (299R + 587G + 114B) ÷ 1000 is below 128, or when it cannot be parsed.
- **Theme colors** draws every color of a Catppuccin icon in the accent and
  gives unfilled shapes a 15% accent fill, like the folder icon.
- Neither choice changes interface icons, Lucide file-type icons, or folders.

A code file such as `main.rs` with a custom color saved in **Customize** and no
custom icon keeps its brand palette under Brand colors; under Theme colors its
icon takes the saved color instead of the accent.

The FILE ICONS group continues with two switches:

- **Show thumbnails**, on by default, reads "Show thumbnails instead of
  file-type icons. The preview panel stays available." Its choice is saved as
  `show_thumbnails` and survives restart. Searching "Show thumbnails" or
  "photos" finds it.
- **STL model thumbnails**, after it and off by default, reads "Render local
  STL models as file thumbnails, one at a time. Requires Show thumbnails." Its
  choice is saved as `stl_thumbnails`, and a missing key reads as off.
  Searching "3d", "mesh", or "printing" finds it. See
  [Local 3D model previews](preview-sandbox.md#local-3d-model-previews).

### File-type icons

<!-- node: settings/themes/icons, File-type icons -->

Code and config files, including JSON, YAML, XML, SQL, database, `.toml`, and
Markdown files, show Catppuccin icons, such as the Rust icon for `main.rs`, the
package-json icon for `package.json`, and the Cargo icon for `Cargo.toml`.
Pictures, plain text, spreadsheets, and keys keep Lucide icons, such as
`photo.png`, `photo.svg`, `notes.txt`, `report.csv`, `server.pem`, and
`id_ed25519`. Search results use the same icons as the Columns, List, and Icons
views.

Strata picks a file's icon in this order:

1. An exact file name, ignoring case. `Makefile`, `MAKEFILE`, `Dockerfile`,
   `Cargo.lock`, `vite.config.ts`, `README`, and `LICENSE` each have their own
   Catppuccin icon. `docker-compose.override.yml` and `compose.yaml` show the
   Docker Compose icon. Shell rc files such as `.zshrc` and `.BASHRC` show the
   Bash icon.
2. A case-sensitive name pattern. `Dockerfile.*` shows Docker, `.env.*` env,
   `tsconfig.*.json` TypeScript config, `*_history` a terminal file, and
   `*.lock` the Lucide cog.
3. The longest matching dotted suffix, so `types.d.ts` and `app.test.ts` show
   specific icons, not the `.ts` icon, and `deploy.yml` shows the YAML icon.
4. A built-in extension list. An unrecognized extension shows the document
   icon.

Some results of that order:

- `archive.lock` shows the Lucide cog, while `ARCHIVE.LOCK` shows the
  Catppuccin config icon.
- `.m` shows MATLAB and `.v` shows V.
- `.s`, `.asm`, and `.nasm` show assembly; `.ps1` PowerShell; `.sv`, `.svh`,
  and `.vhdl` Verilog; `.bat` and `.cmd` Batch. Shell scripts show Bash.
- `.qml`, `.tcl`, `.qrc`, and `.ui` show the generic code icon.
- `app.apk` shows Android and `app.jar` Java archive. `.nupkg` and `.vsix` show
  Catppuccin icons; `.deb`, `.rpm`, and `.exe` keep the Lucide package icon.
- `.mp4`, `.mkv`, `.webm`, `.mov`, `.avi`, `.m4v`, `.mpeg`, `.mpg`, `.ogv`,
  `.3gp`, `.3g2`, `.flv`, `.wmv`, `.asf`, `.m2ts`, and `.vob` show the Lucide
  clapperboard.
- `.zip`, `.7z`, `.tar`, `.gz`, `.tgz`, `.bz2`, `.xz`, `.zst`, `.rar`, `.lz`,
  `.lzma`, `.lzo`, `.rz`, `.sz`, `.cab`, `.arj`, and `.cpio` show the Lucide
  folder-archive icon, distinct from documents.
- Spreadsheets, presentations, fonts, disk images, and keys each show their own
  Lucide icon.

### Icon size and weight

<!-- node: settings/themes/icons, Size and weight -->

Header-bar and pane action icons draw at 16 logical px at the default text
size, centered even when the desktop theme gives buttons extra space. Chrome
icons rasterize at twice their logical size; file, sidebar, and dialog icons
rasterize at 96 px or their device-pixel size, whichever is larger. Icons
rasterize at the display's pixel density, so 2× displays get sharp strokes.

In the Icons view, Lucide outlines draw at half the stroke weight used in List
rows, toolbars, and the sidebar. Above 64 logical px, strokes thin further by
(64 ÷ size)^0.35, about 0.62× at 256 px, so large icons do not read as bold.
Catppuccin file icons take the same factor and halving: in the Icons view their
strokes match the folder icon beside them, and in List rows they draw at three
quarters of its weight.

## Custom theme files

<!-- node: settings/themes, Custom themes -->
<!-- node: settings/themes/icons, Color -->

Custom themes are TOML files in:

```text
~/.config/strata/themes/<theme-id>.toml
```

Under the library, Strata shows "Custom themes live in ~/.config/strata/themes" and an **Add theme** button. **Add theme** opens the **Add a theme** panel with a name field and 14 color pickers seeded from the selected theme: nine for the background, surfaces, text, accent, danger, muted and highlighted elements, borders, and dimmed text, and five for syntax colors. Strata previews edits live. **Add theme** in the panel saves the theme as a new file, created owner-only (mode 0600), and selects it. The new theme also appears in the theme library of Settings open in other windows, without a restart. The name field's accessible name is "Theme name", and each color picker is named after its row label. Saving with an empty or whitespace-only name shows "Enter a theme name" and writes nothing. The editor's color swatches keep rounded corners, with no square fragments, whether normal, hovered, focused, or pressed.

The settings configurator writes the same format, so generated themes can be edited or shared:

```toml
name = "Ocean Blue"
background = "#0c1a2b"
surface = "#122438"
text = "#c9deed"
accent = "#4fd6ff"
danger = "#ff6b7a"
muted = "#1e3a52"
highlight = "#244d68"
border = "#315b75"
dim_text = "#6f8da3"
```

Strata loads valid `.toml` files in this directory at startup, reads them again when one changes (see [Live updates](#live-updates)), and lists them in the theme library after the bundled themes, keyed by file name without `.toml`. If a custom filename matches a bundled theme ID, the custom theme replaces that bundled entry so saved preferences and selection always use the user’s palette. Colors load as `#rrggbb`, or `#rrggbbaa` when translucent, so GTK-only forms such as 9-digit hex still apply; the file is not rewritten. Icons, both interface and file-type, draw an opaque form of the accent, text, or danger color, so a translucent color loses its alpha on icons only.

The configurator derives a new file's ID from the theme name, lowercased, keeping ASCII letters and digits and joining the rest with `-` (for example `Ocean Blue` becomes `ocean-blue.toml`). Names without ASCII letters or digits are saved as `custom-theme.toml`, the next such name as `custom-theme-2.toml`, then `custom-theme-3.toml`. The `name` field keeps the typed name, trimmed of leading and trailing spaces, so names such as `日本語` are still shown as written.

Theme files may be symlinks into a dotfiles repository. The configurator never replaces an existing theme: when the ID matches a bundled theme or a loaded custom theme, or `<theme-id>.toml` already exists, whether it loaded or not (for example an invalid file or a link to a missing or broken dotfile), the new theme is saved as the next free `<theme-id>-2.toml`, `<theme-id>-3.toml`, and so on. Saving a theme named `Dracula` therefore creates `dracula-2.toml` and leaves the bundled Dracula theme in place.

### Live updates

<!-- node: settings/themes, Custom themes -->

While Strata runs, it watches `~/.config/strata/themes`. When a `.toml` file
there changes, Strata reads the custom themes again. With a custom theme
selected, rewriting its file, such as changing `accent`, re-applies the new
colors in every open window without a restart, including interface icons and
code-preview syntax colors. With a bundled theme selected, creating a custom
file with its id, such as `dracula.toml`, applies that file's colors the same
way. Changes less than 75 ms apart trigger one re-read, 75 ms after the last.

- A selected theme's file may be a symlink, such as into `~/dotfiles`.
  Strata also watches the folder of each link's target, so rewriting the target
  re-applies its colors live.
- A `.toml` link whose target does not exist yet stays watched. Once the
  target is written, the theme appears in the list, and later rewrites
  re-apply live. A dangling link whose target's folder does not exist is not
  watched until a later re-read finds that folder.
- Each re-read recomputes the link targets, so links added, removed, or
  repointed take effect from the next re-read. Only the final file of a link
  chain has its folder watched: repointing an intermediate directory link,
  such as `~/.config/omarchy/current/theme`, does not reload the theme.
- Only `.toml` files directly in the themes folder, and the resolved target of
  each `.toml` link there, trigger a re-read. Other extensions, subfolders,
  and other files beside a link target do not.
- When the selected file, whose id matches no bundled theme, is caught
  mid-write, invalid, or deleted, its colors stay, and its theme stays in the
  list, until the next valid write. Deleting or breaking a selected custom
  `tokyo-night.toml` instead applies the bundled Tokyo Night at once.
- A custom file with an invalid color is skipped at startup and on each
  re-read, unless it is the selected theme.
- While following Omarchy, rewriting a custom theme file changes no colors.
  During an editor preview, rewriting the selected file keeps the preview.
- An open Settings page never redraws existing theme cards on a re-read. A new
  file's card appears when the re-read changes the selected colors, or at the
  next theme or preference change.
- When `~/.config/strata/themes` is missing at startup, files and links
  created there later are not read until a save from the editor, which starts
  the watch, or a restart.

### Matugen template

<!-- node: settings/themes, Custom themes -->

[matugen](https://github.com/InioX/matugen) builds a Material You palette from
the wallpaper and fills templates with it. This template, contributed in
[arqueon/strata-extras](https://github.com/arqueon/strata-extras/tree/main/themes/matugen)
(MIT), maps that palette to Strata's interface and syntax colors. It was
written against matugen 4.2; older template syntax may differ.

1. Save it as `~/.config/matugen/templates/strata-theme.toml`:

   ```toml
   name = "Matugen"
   background = "{{colors.surface.default.hex}}"
   surface = "{{colors.surface_container.default.hex}}"
   text = "{{colors.on_surface.default.hex}}"
   accent = "{{colors.primary.default.hex}}"
   danger = "{{colors.error.default.hex}}"
   muted = "{{colors.surface_container_high.default.hex}}"
   highlight = "{{colors.secondary_container.default.hex}}"
   border = "{{colors.outline_variant.default.hex}}"
   dim_text = "{{colors.on_surface_variant.default.hex}}"
   syntax_keyword = "{{colors.tertiary.default.hex}}"
   syntax_string = "{{colors.secondary.default.hex}}"
   syntax_constant = "{{colors.tertiary_fixed_dim.default.hex}}"
   syntax_type = "{{colors.primary.default.hex}}"
   syntax_preprocessor = "{{colors.on_surface_variant.default.hex}}"
   ```

2. Register it in `~/.config/matugen/config.toml`:

   ```toml
   [templates.strata]
   input_path = '~/.config/matugen/templates/strata-theme.toml'
   output_path = '~/.config/strata/themes/matugen.toml'
   ```

3. Run matugen once, for example `matugen image ~/Pictures/wallpaper.png`,
   then select **Matugen** in **Settings → Appearance**, or set
   `theme = "matugen"` in `settings.toml`.

From then on, every matugen run recolors open windows. Shells that run user
matugen templates on each wallpaper change, such as DankMaterialShell, keep
Strata in step with no further setup.

| Strata key | Material color |
| --- | --- |
| `background` | `surface` |
| `surface` | `surface_container` |
| `text` | `on_surface` |
| `accent` | `primary` |
| `danger` | `error` |
| `muted` | `surface_container_high` |
| `highlight` (selection) | `secondary_container` |
| `border` | `outline_variant` |
| `dim_text` | `on_surface_variant` |
| `syntax_keyword` / `syntax_string` / `syntax_constant` / `syntax_type` / `syntax_preprocessor` | `tertiary` / `secondary` / `tertiary_fixed_dim` / `primary` / `on_surface_variant` |

## Syntax colors

<!-- node: settings/themes, Syntax colors -->
<!-- node: settings/themes, Custom themes -->
<!-- node: preview/preview-panel -->

All 95 bundled themes include explicit code-preview palettes. Tinted Base16 palettes map `base0E` to keywords, `base0B` to strings, `base09` to constants, `base0A` to types, and `base0C` to preprocessor directives. Catppuccin and Tokyo Night use the pinned `catppuccin-mocha` and `tokyo-night-dark` syntax palettes; Azure Glow and Omarchy Light have original curated palettes.

Under **Settings → Appearance → Add theme**, the syntax color pickers in the **Add a theme** panel start with the selected theme's colors. Each picker previews changes immediately across the interface and in open code previews; Cancel restores the selected theme, and Add theme saves all five syntax colors with the interface palette. Closing Settings by any route (Escape, Close settings, a click outside it, or closing the window) discards an unsaved preview the same way and collapses the editor. A discarded preview re-applies the saved theme in every open window and in windows opened later. Pressing the library's **Add theme** button again while the editor is open keeps the draft. Opening the editor again starts from the selected theme's colors, with an empty name and no error. Changing text size, toggling Element glow, or an Omarchy theme change while following keeps the preview until it is cancelled or saved. Clicking a theme card or toggling **Follow Omarchy** ends the preview. If followed Omarchy state disappears during a preview, the preview ends and the previously selected bundled or custom theme applies. Cancel, or closing Settings, in one window leaves a preview started later in another window applied. **Dim text / comments** controls comments as well as dim interface text. Markdown headings continue to use the accent color. Rendered 3D model previews, such as STL files, are shaded in the theme's accent on the theme's opaque surface. An open model preview re-renders when the theme changes and keeps its selected camera view. A model or route preview that a narrow window hides reloads with the new theme when the window widens again; see [Local 3D model previews](preview-sandbox.md#local-3d-model-previews).

Each color swatch in the editor opens GTK's color chooser. Its Cancel and Select buttons and its custom color editor (hex entry, hue slider, and the value popups) follow the active theme and update live, as does the same chooser in the custom folder color dialog.

Custom TOML files can override any syntax role independently:

```toml
syntax_keyword = "#ff7b72"
syntax_string = "#7ee787"
syntax_constant = "#79c0ff"
syntax_type = "#ffa657"
syntax_preprocessor = "#d2a8ff"
```

Recognized source languages keep syntax highlighting regardless of the loaded text's byte count, line count, or individual line length. Source text still loads incrementally, and the separate 1 MiB preview-read cap remains in effect. Text without a recognized language opens in a source view, without syntax colors, up to 128 KiB and 512 lines with no line over 2 KiB. Larger files, and files with a longer line, use recycled plain-text rows; see [Document previews](document-previews.md#limits-and-fallback).

Code previews use GtkSourceView's bundled and system language definitions; a language definition in the user's `gtksourceview-5` folder, under the data or home folder, is never read. A style scheme named `strata-current` in the user's GtkSourceView styles folder does not change code-preview colors, and code previews keep their syntax colors when `~/.cache/strata` cannot be written.

All color fields, the interface colors included, accept GTK color formats such as `rgb()`, short hex, and color names; a theme written that way keeps its syntax colors in code previews. An omitted `syntax_*` key uses a color derived from accent and text, and an omitted `danger` uses `#e5484d`. Every other color key and a `name` are required, and the name must contain a non-space character: a file missing one, or with a blank name, is skipped at startup. The editor initializes omitted syntax fields from those derived colors when creating a theme, and writes each picked color as `#rrggbb`. Invalid colors cause a custom file to be excluded at startup. Preview schemes canonicalize colors to opaque `#rrggbb`.

## Omarchy Quattro

<!-- node: settings/themes/omarchy, Following -->
<!-- node: settings/themes/omarchy, Surfaces -->
<!-- node: settings/themes/omarchy, Variants -->
<!-- node: settings/themes/omarchy, Per-theme memory -->

On Omarchy Quattro, turn on **Follow Omarchy** under **Settings → Appearance → THEME**. Strata detects the active theme from:

```text
~/.local/state/omarchy/current/theme.name
~/.local/state/omarchy/current/theme/colors.toml
```

Strata follows Omarchy on first launch, when no `settings.toml` exists. It monitors the current-theme state, so switching Omarchy themes or editing `colors.toml` re-applies the palette in every window without a restart. While following, the theme library is disabled and **Current theme** reads "Managed by Omarchy. Turn off Follow Omarchy to pick a theme manually."

Before the variant applies, Strata maps Quattro's own keys into its tokens:

| Area | Quattro key | When the key is missing |
| --- | --- | --- |
| Window background | `background` | Required |
| Text | `foreground` | Required |
| Dim text | None | `background` blended 62% toward `foreground` |
| Accent | `accent` | Required |
| Panes and headers | `dark_background` | `background` |
| Hover surfaces | `lighter_background` | `background` blended 10% toward `foreground`, also when it equals `background` |
| Selection | `selection` | `background` blended 25% toward `accent` |
| Borders | `muted` | `background` blended 36% toward `foreground` |
| Danger | `color1` | Strata's default danger color |

ANSI `color8` is never read, so changing it in `colors.toml` changes no color. An invalid optional color, such as `selection` or `muted`, is ignored and its fallback used.

Under **Follow Omarchy**, **Omarchy variant** reads "Lighter or darker file columns, or stronger contrast. Keeps following your system theme." It offers:

- **Lighter**: file columns on `background`; the sidebar, headers, and preview on `dark_background`.
- **Darker** (default): file columns also on `dark_background`, so the whole window uses it.
- **Contrast**: the Darker layout with foregrounds raised to contrast targets.

Lighter and Darker keep the theme's colors as authored, so a light palette stays light under Darker. Contrast raises text to 7:1, and dim text, accent, and danger to 4.5:1, against the window, pane, hover, and selection surfaces, and borders to 3:1 against them. It raises code-preview syntax colors to 4.5:1 against the window and pane surfaces. It keeps the theme's surfaces and selection, unless pure white, or black on a light palette, falls below 7:1 on one; that surface then moves toward black, or white on a light palette, until it reaches 7:1. Contrast keeps a palette light with `mode = "light"` in `colors.toml` and dark with `mode = "dark"`. Without `mode`, or with another value, a `background` with relative luminance above 0.45 counts as light. Variants keep palette hues and never change bundled or custom themes or the desktop theme. These are semantic-token targets, not a guarantee for every composited or disabled widget state.

The variant is remembered per Omarchy theme, saved under `[omarchy_variants]` in Strata's `settings.toml` keyed by theme name, such as `tokyo-night = "lighter"`. A `theme.name` with surrounding whitespace or a trailing newline uses the bare name's key. Choosing Darker removes the theme's key, and a theme without a key uses Darker. The saved variant applies before Settings opens and live across windows, menus, dialogs, icons, and previews. Switching themes with `omarchy-theme-set` applies that theme's saved variant, and the dropdown updates in every window. Turning off Follow Omarchy disables the selector but remembers its values.

Saved `original` and `high_contrast` values load as Lighter and Contrast. A legacy global `omarchy_variant = "high_contrast"` becomes Contrast for the Omarchy theme active at the next start. Once an Omarchy theme is detected, any other legacy `omarchy_variant` value is dropped, and the next save removes the key from `settings.toml`; without Omarchy, the key stays. One unrecognized value in `[omarchy_variants]` drops only that key.

Syntax colors follow Quattro's named `magenta`, `green`, `orange`, `cyan`, and `yellow` colors. Older terminal palettes can supply `color5` for keywords, `color2` for strings, `color9` for constants, and `color3` for types. Missing colors retain the existing source-palette or derived fallback. Quattro values load in the same canonical hex form as custom theme files; values GTK cannot parse count as missing.

**Follow Omarchy** and **Omarchy variant** are shown only when both files exist and `colors.toml` has valid `background`, `foreground`, and `accent` colors. If that state disappears while Strata is running, **Follow Omarchy** is hidden, following turns off (saved as `mode = "theme"`), and Strata returns to the previously selected bundled or custom theme. Omarchy's own theme switch, which briefly removes `current/theme`, does not turn following off. If it only becomes invalid, for example midway through an Omarchy theme switch, the last applied Omarchy palette stays in use until the next valid change. Legacy Omarchy theme layouts and alacritty-based color extraction are intentionally unsupported.
