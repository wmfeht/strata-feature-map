---
nodes: [settings/themes, settings/themes/omarchy, settings/themes/icons]
reviewed_at: 0a086aa3bdb251842a1e8413e2a6b35970d0b409
---

# Themes

Strata ships 95 themes, follows your Omarchy theme if you have one, and reads
your own theme files. Changes restyle every open window at once, including
menus, dialogs, and code previews.

## Pick a bundled theme

<!-- node: settings/themes, Theme library -->
<!-- node: settings/themes/omarchy, Following -->

Press Ctrl+, and open **Appearance**. On Omarchy, first turn off **Follow
Omarchy** under **THEME**; while it is on, the library is greyed out. In **THEME
LIBRARY**, type in **Search themes** or pick **Light** or **Dark**, then click a
card. The theme applies at once, the card gets a check, and Strata remembers it
after a restart.

Without Omarchy Quattro, a fresh install starts with Tokyo Night.

## Follow Omarchy

<!-- node: settings/themes/omarchy, Following -->
<!-- node: settings/themes/omarchy, Variants -->

On Omarchy Quattro, a fresh install follows your desktop theme. The **Follow Omarchy**
switch sits under **THEME** on the same page. Strata reads the active theme from
`~/.local/state/omarchy/current/` and restyles itself whenever you switch
Omarchy themes or edit `colors.toml`, with no restart.

**Omarchy variant** sets how Strata reads the palette:

- **Original**, the default, maps the palette as it is.
- **Darker** draws near-black surfaces from the terminal background. Light
  palettes turn dark too.
- **High contrast** raises text and border contrast and keeps a light palette
  light.

## Write your own theme

<!-- node: settings/themes, Custom themes -->

A theme is a TOML file with a name and nine colors. Create the themes folder:

```sh
mkdir -p ~/.config/strata/themes
```

Then save this as `~/.config/strata/themes/ocean-blue.toml`:

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

Restart Strata. Your theme appears in the library after the bundled ones; click
its card to use it. On Omarchy, turn off **Follow Omarchy** first. Colors can
be hex (`#rgb`, `#rrggbb`, or `#rrggbbaa` for translucency), `rgb()`, or a color
name. A file with a missing key or an invalid color is skipped without a
message, so check the file if your theme is missing. `danger` is the one color
you may leave out.

You do not have to write the file by hand. Click **Add theme** below the
library. The **Add a theme** panel opens with a name field and a picker for
each color, seeded from your current theme. Every change previews live;
**Cancel** puts your theme back. Click **Add theme** to save the file and
switch to it, no restart needed. The file is named after the theme: `Ocean
Blue` saves as `ocean-blue.toml`, or `ocean-blue-2.toml` if that file exists.

## Syntax colors for code previews

<!-- node: settings/themes, Syntax colors -->
<!-- node: settings/themes/omarchy, Following -->

Add any of these five keys to a theme file, then restart Strata, to tune code
previews:

```toml
syntax_keyword = "#ff7b72"
syntax_string = "#7ee787"
syntax_constant = "#79c0ff"
syntax_type = "#ffa657"
syntax_preprocessor = "#d2a8ff"
```

A key you leave out keeps a color derived from your accent and text. Comments
use `dim_text`, and Markdown headings use `accent`. The **Add a theme** panel has
a picker for each of the five roles. Every bundled theme brings its own syntax
colors, and following Omarchy takes them from the Omarchy palette.

## Good to know

<!-- node: settings/themes, Custom themes -->
<!-- node: settings/themes/icons, Color -->
<!-- node: settings/themes, Styling and effects -->

- Name a file after a bundled theme id, such as `dracula.toml`, and yours
  replaces the bundled one. Saving from the panel never does this: it picks a
  free name such as `dracula-2.toml`.
- Interface icons draw in the accent. Icons for code and config files keep
  their own colors; set **File icon colors** to **Theme colors** to tint them
  too.
- You can restyle Strata in `~/.config/gtk-4.0/gtk.css`; its colors are named
  `@strata_bg`, `@strata_accent`, and so on.

**Full detail:** the [Themes reference](../reference/themes.md) covers the
Base16 mapping, GTK CSS precedence, and the Omarchy color mapping.
