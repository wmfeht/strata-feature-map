---
nodes: [settings/themes, settings/themes/omarchy, settings/themes/icons]
reviewed_at: be3343a5992a2a5497b1a2ee7faa525be18e988f
---

# Themes

Strata ships 95 themes, follows your Omarchy theme if you have one, and reads
your own theme files. Changes restyle every open window at once.

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
<!-- node: settings/themes/omarchy, Per-theme memory -->

On Omarchy Quattro, a fresh install follows your desktop theme. The **Follow Omarchy**
switch sits under **THEME** on the same page. Strata restyles itself whenever you
switch Omarchy themes or edit `colors.toml`, with no restart.

**Omarchy variant** sets how Strata lays out the palette:

- **Lighter** puts file columns on the theme's background and the sidebar,
  headers, and preview on its darker pane color.
- **Darker**, the default, puts the whole window on the darker pane color.
- **Contrast** keeps the Darker layout and raises text, accent, and border
  contrast.

Strata remembers the variant for each Omarchy theme.

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

Restart Strata if the themes folder did not exist when it started. Your theme
appears in the library after the bundled ones; click its card to use it. On
Omarchy, turn off **Follow Omarchy** first. Colors can
be hex (`#rgb`, `#rrggbb`, or `#rrggbbaa` for translucency), `rgb()`, or a color
name. A file with a missing key or an invalid color is skipped without a
message. `danger` is the one color you may leave out.

Once your theme is selected, saving the file recolors every open window, even
through a symlink into your dotfiles, so generators such as matugen work.

Or click **Add theme** below the library. The **Add a theme** panel opens with
a name field and a picker for each color, seeded from your current theme. Every
change previews live; **Cancel** puts your theme back. Click **Add theme** to
save the file and switch to it. `Ocean Blue` saves as `ocean-blue.toml`, or
`ocean-blue-2.toml` if that file exists.

## Syntax colors for code previews

<!-- node: settings/themes, Syntax colors -->
<!-- node: settings/themes/omarchy, Following -->

Add any of these five keys to a theme file to tune code previews. If the theme
is selected, saving the file recolors open previews at once:

```toml
syntax_keyword = "#ff7b72"
syntax_string = "#7ee787"
syntax_constant = "#79c0ff"
syntax_type = "#ffa657"
syntax_preprocessor = "#d2a8ff"
```

A key you leave out keeps a color derived from your accent and text. Comments
use `dim_text`, and Markdown headings use `accent`. The **Add a theme** panel has
a picker for each role. Bundled themes and Omarchy bring their own syntax
colors.

## Good to know

<!-- node: settings/themes, Custom themes -->
<!-- node: settings/themes/icons, Color -->
<!-- node: settings/themes, Styling and effects -->
<!-- node: settings/themes, User stylesheet -->

- Name a file after a bundled theme id, such as `dracula.toml`, and yours
  replaces the bundled one. Saving from the panel never does this: it picks a
  free name such as `dracula-2.toml`.
- Interface icons draw in the accent. Icons for code and config files keep
  their own colors; set **File icon colors** to **Theme colors** to tint them
  too.
- Desktop GTK themes and `~/.config/gtk-4.0/gtk.css` do not change Strata.
  Write rules in `~/.config/strata/style.css` instead; they apply live and can
  use colors such as `@strata_accent`.
- **Corner roundness** squares corners at 0 and softens them up to 200, from a
  default of 60. **Interface font** picks the typeface outside file previews.

**Full detail:** the [Themes reference](../reference/themes.md) covers the
Base16 mapping, desktop isolation, the user stylesheet, live updates, a
matugen template, and Omarchy colors.
