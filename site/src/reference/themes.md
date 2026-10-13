---
nodes: [settings/themes, settings/themes/omarchy, settings/themes/icons, settings/preferences, preview/preview-panel]
reviewed_at: 0a086aa3bdb251842a1e8413e2a6b35970d0b409
---

# Themes reference

Strata styles the interface with nine semantic color tokens. Bundled themes are the fallback on any Linux desktop. A fresh install without Omarchy starts with Tokyo Night, and the saved selection survives restart. If the saved theme matches no bundled or custom theme, Strata falls back to Azure Glow at startup.

Open Settings with the header **Settings** button or Ctrl+,, then choose **Appearance**. Under **THEME LIBRARY**, Strata lists the 95 bundled themes in alphabetical order in one scrolling library. Typing in **Search themes** hides cards whose names do not contain the query, ignoring case. In **Search themes**, Ctrl+A selects the query on any keyboard layout; Ctrl+Shift+A, Ctrl+Alt+A, and Ctrl+Super+A do not. The **All**, **Light**, and **Dark** filter combines with the query. A theme counts as Light when its background's relative luminance exceeds 0.4, whatever color form the background is written in.

Clicking a card applies the theme immediately across the interface, marks the card with a check, and keeps that theme active across restarts. While **Follow Omarchy** is on, the library is disabled; turn off Follow Omarchy to pick a theme.

Tinted Base16 entries map colors to Strata tokens as follows: `base00` to background, `base01` to surface, `base05` to text, `base0D` to accent, `base08` to danger, `base02` to muted and highlight, `base03` to border, and `base04` to dim text. Every bundled theme's text has at least 4.5:1 contrast on its background and 3:1 on its surface. A few bundled entries override the mapped foreground values to meet that: Material Lighter draws text in `#455A64` (6.94:1 on its background) and dim text in `#607D8B`, and Material Vivid draws text in `#9e9e9e` (6.01:1). Where the upstream dim text is also unreadable, it is adjusted to stay legible while remaining dimmer than text. The catalog comments each override next to the value. Source revision and licensing details are recorded in [`THIRD_PARTY_LICENSES.md`](https://github.com/lgse/strata/blob/v1.0.0/THIRD_PARTY_LICENSES.md).

## GTK CSS precedence

<!-- node: settings/themes, Styling and effects -->

Strata defines its nine named colors as `@strata_bg`, `@strata_surface`,
`@strata_text`, `@strata_accent`, `@strata_danger`, `@strata_muted`,
`@strata_highlight`, `@strata_border`, and `@strata_dim_text`. These replace the former
`@theme_*` names; user stylesheets referencing those names must be updated.
Custom theme TOML keys are unchanged.

Strata's token provider takes precedence over GTK theme defaults, but user
`~/.config/gtk-4.0/gtk.css` retains GTK's higher user priority. The namespace
prevents accidental collisions with other stylesheets' `@theme_*` colors;
it does not override deliberate user selectors or `@strata_*` definitions.
User CSS that redefines the former `@theme_*` names no longer changes Strata's
colors.

### Element glow, motion, and renderer

**Settings → Appearance → EFFECTS → Element glow** is on by default and saved
as `element_glow = true`. It adds accent glow to dialogs, menus, theme cards,
and animated feedback. The video preview's
[ambient light](preview-sandbox.md#video-previews) follows the same switch.
Turning it off removes that glow in every window at once, keeps focus
outlines, depth shadows, and animation movement, and persists across restarts;
use Reduce motion to stop animations.

**Settings → Appearance → MOTION → Reduce motion** stops sidebar, column, and
preview animations. GTK's `gtk-enable-animations` set to false stops the same
animations even when Reduce motion is off. Strata's stylesheet ignores the
desktop's `prefers-reduced-motion` media preference.

**Settings → Appearance → RENDERING → Interface renderer** offers
**GTK default**, the initial choice, and **Cairo**, saved as
`interface_renderer = "system"` or `"cairo"`. Cairo avoids text artifacts on
some displays but can use more CPU. Choosing a value other than the one Strata
started with shows **Restart now**; the change applies after a restart. A
`GSK_RENDERER` environment variable set before Strata starts, even to an empty
value, overrides the saved choice. When Strata selects Cairo itself,
applications it launches may inherit that renderer; desktop settings are
unchanged.

### Icon colors

<!-- node: settings/themes/icons, Color -->
<!-- node: settings/themes, File icon colors -->
<!-- node: settings/preferences, Settings search -->

Interface icons in the header, sidebar, and Settings navigation, and Lucide
file-type icons, draw in the theme's accent at full opacity. Destructive menu
items, such as **Permanently delete**, and danger-tone dialogs draw their icon
in the danger color. Changing the theme or Omarchy variant recolors icons,
including Catppuccin file icons, in every open window.

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

Under the library, Strata shows "Custom themes live in ~/.config/strata/themes" and an **Add theme** button. **Add theme** opens the **Add a theme** panel with a name field and 14 color pickers seeded from the selected theme: nine for the background, surfaces, text, accent, danger, muted and highlighted elements, borders, and dimmed text, and five for syntax colors. Strata previews edits live. **Add theme** in the panel saves the theme as a new file, created owner-only (mode 0600), and selects it. The new theme also appears in the theme library of Settings open in other windows, without a restart. Saving with an empty or whitespace-only name shows "Enter a theme name" and writes nothing. The editor's color swatches keep rounded corners, with no square fragments, whether normal, hovered, focused, or pressed.

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

Strata loads valid `.toml` files in this directory at startup and lists them in the theme library after the bundled themes, keyed by file name without `.toml`. If a custom filename matches a bundled theme ID, the custom theme replaces that bundled entry so saved preferences and selection always use the user’s palette. Colors load as `#rrggbb`, or `#rrggbbaa` when translucent, so GTK-only forms such as 9-digit hex still apply; the file is not rewritten. Icons, both interface and file-type, draw an opaque form of the accent, text, or danger color, so a translucent color loses its alpha on icons only.

The configurator derives a new file's ID from the theme name, lowercased, keeping ASCII letters and digits and joining the rest with `-` (for example `Ocean Blue` becomes `ocean-blue.toml`). Names without ASCII letters or digits are saved as `custom-theme.toml`, the next such name as `custom-theme-2.toml`, then `custom-theme-3.toml`. The `name` field keeps the typed name, trimmed of leading and trailing spaces, so names such as `日本語` are still shown as written.

Theme files may be symlinks into a dotfiles repository. The configurator never replaces an existing theme: when the ID matches a bundled theme or a loaded custom theme, or `<theme-id>.toml` already exists, whether it loaded or not (for example an invalid file or a link to a missing or broken dotfile), the new theme is saved as the next free `<theme-id>-2.toml`, `<theme-id>-3.toml`, and so on. Saving a theme named `Dracula` therefore creates `dracula-2.toml` and leaves the bundled Dracula theme in place.

## Syntax colors

<!-- node: settings/themes, Syntax colors -->
<!-- node: settings/themes, Custom themes -->
<!-- node: preview/preview-panel -->

All 95 bundled themes include explicit code-preview palettes. Tinted Base16 palettes map `base0E` to keywords, `base0B` to strings, `base09` to constants, `base0A` to types, and `base0C` to preprocessor directives. Catppuccin and Tokyo Night use the pinned `catppuccin-mocha` and `tokyo-night-dark` syntax palettes; Azure Glow and Omarchy Light have original curated palettes.

Under **Settings → Appearance → Add theme**, the syntax color pickers in the **Add a theme** panel start with the selected theme's colors. Each picker previews changes immediately across the interface and in open code previews; Cancel restores the selected theme, and Add theme saves all five syntax colors with the interface palette. Closing Settings by any route (Escape, Close settings, a click outside it, or closing the window) discards an unsaved preview the same way and collapses the editor. A discarded preview re-applies the saved theme in every open window and in windows opened later. Pressing **Add theme** while the editor is open keeps the draft. Opening the editor again starts from the selected theme's colors, with an empty name and no error. Changing text size, toggling Element glow, or an Omarchy theme change while following keeps the preview until it is cancelled or saved. Clicking a theme card or toggling **Follow Omarchy** ends the preview. If followed Omarchy state disappears during a preview, the preview ends and the previously selected bundled or custom theme applies. Cancel, or closing Settings, in one window leaves a preview started later in another window applied. **Dim text / comments** controls comments as well as dim interface text. Markdown headings continue to use the accent color. Rendered 3D model previews, such as STL files, are shaded in the theme's accent, and an open model preview re-renders when the theme changes; see [Local 3D model previews](preview-sandbox.md#local-3d-model-previews).

Each color swatch in the editor opens GTK's color chooser. Its Cancel and Select buttons and its custom color editor (hex entry, hue slider, and the value popups) follow the active theme and update live, as does the same chooser in the custom folder color dialog.

Custom TOML files can override any syntax role independently:

```toml
syntax_keyword = "#ff7b72"
syntax_string = "#7ee787"
syntax_constant = "#79c0ff"
syntax_type = "#ffa657"
syntax_preprocessor = "#d2a8ff"
```

Recognized source languages keep syntax highlighting regardless of the loaded text's byte count, line count, or individual line length. Source text still loads incrementally, and the separate 1 MiB preview-read cap remains in effect. Large plain-text files without a recognized language can still use virtualized rendering.

All color fields, the interface colors included, accept GTK color formats such as `rgb()`, short hex, and color names; a theme written that way keeps its syntax colors in code previews. An omitted `syntax_*` key uses a color derived from accent and text, and an omitted `danger` uses `#e5484d`. Every other color key and a non-empty `name` are required: a file missing one is skipped at startup. The editor initializes omitted syntax fields from those derived colors when creating a theme, and writes each picked color as `#rrggbb`. Invalid colors cause a custom file to be excluded at startup. Preview schemes canonicalize colors to opaque `#rrggbb`.

## Omarchy Quattro

<!-- node: settings/themes/omarchy, Following -->
<!-- node: settings/themes/omarchy, Variants -->

On Omarchy Quattro, turn on **Follow Omarchy** under **Settings → Appearance**. Strata detects the active theme from:

```text
~/.local/state/omarchy/current/theme.name
~/.local/state/omarchy/current/theme/colors.toml
```

The application maps Quattro's `background`, `foreground`, `accent`, `selection`, `color8`, and `color1` values into its semantic tokens and monitors the current-theme state for changes, including edits to `colors.toml`. It defaults to following Omarchy on first launch, when no `settings.toml` exists. While following, the theme library is disabled and **Current theme** reads "Managed by Omarchy. Turn off Follow Omarchy to pick a theme manually."

Under **Settings → Appearance → Follow Omarchy**, **Omarchy variant** offers:

- **Original** (default): the existing palette mapping, unchanged.
- **Darker**: dark surfaces based on the terminal background instead of the brighter ANSI gray, with readable text and accents. Light palettes also become dark interpretations.
- **High contrast**: stronger text and boundary contrast, retaining a light palette's light appearance or a dark palette's dark appearance.

The variants keep palette hues and adjust brightness where necessary; they do not invert colors or substitute another theme. Darker and High contrast derive muted/hover surfaces from the same palette, adjust semantic foregrounds for at least 4.5:1 contrast against those surfaces, and adapt preview syntax colors. High contrast targets 7:1 for primary text and 3:1 for borders. These are semantic-token targets, not a guarantee for every composited or disabled widget state.

The choice is saved as `omarchy_variant = "original"`, `"darker"`, or `"high_contrast"` in Strata's `settings.toml`. It applies before Settings opens and live across windows, menus, dialogs, icons, and previews. Changing the active Omarchy theme retains the variant. Turning off Follow Omarchy disables the selector but remembers its value. Variants never change bundled or custom themes or the desktop theme.

Syntax colors follow Quattro's named `magenta`, `green`, `orange`, `cyan`, and `yellow` colors. Older terminal palettes can supply `color5` for keywords, `color2` for strings, `color9` for constants, and `color3` for types. Missing colors retain the existing source-palette or derived fallback. Quattro values load in the same canonical hex form as custom theme files; values GTK cannot parse count as missing.

**Follow Omarchy** and **Omarchy variant** are shown only when both files exist and `colors.toml` has valid `background`, `foreground`, and `accent` colors. An invalid optional `selection` or `color8` is ignored and its fallback used. If that state disappears while Strata is running, **Follow Omarchy** is hidden, following turns off (saved as `mode = "theme"`), and Strata returns to the previously selected bundled or custom theme. Omarchy's own theme switch, which briefly removes `current/theme`, does not turn following off. If it only becomes invalid, for example midway through an Omarchy theme switch, the last applied Omarchy palette stays in use until the next valid change. Legacy Omarchy theme layouts and alacritty-based color extraction are intentionally unsupported.
