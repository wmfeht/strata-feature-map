---
nodes: [settings/preferences, settings/preferences/storage, settings/preferences/date-format, settings/preferences/language]
reviewed_at: 0a086aa3bdb251842a1e8413e2a6b35970d0b409
---

# Settings

Change how Strata looks and behaves from one panel, and keep most settings in one
TOML file you can track with your dotfiles.

## Open Settings

<!-- node: settings/preferences, Opening and closing -->
<!-- node: settings/preferences, Settings search -->

Press Ctrl+, or click the gear (**Settings**) in the window header. The panel
first opens on **General**; the other pages are **Appearance**, **Actions**,
**Updates**, and **About**.

Type in **Search settings** to jump to a row: "font" finds **Text size**.
Escape clears the search; press it again, or click outside the panel, to close
Settings.

## Find settings.toml

<!-- node: settings/preferences/storage, Saving -->
<!-- node: settings/preferences/storage, Loading and recovery -->

Every preference change is saved at once to `~/.config/strata/settings.toml`, or
`$XDG_CONFIG_HOME/strata/settings.toml` when you set that variable. A fresh
install has no file until your first change.

To edit it by hand, close every Strata window, change values in place (a key
written twice makes the file invalid), and reopen Strata:

```toml
language = "fr"
date_format = "iso"
show_hidden = true
```

## Keep settings in your dotfiles

<!-- node: settings/preferences/storage, Symlinked settings file -->
<!-- node: settings/preferences/storage, Loading and recovery -->

Change any setting once so the file exists. Then close Strata, move the file
into your repository, and link it back:

```sh
mkdir -p ~/dotfiles/strata
mv ~/.config/strata/settings.toml ~/dotfiles/strata/settings.toml
ln -s ~/dotfiles/strata/settings.toml ~/.config/strata/settings.toml
```

On another machine, close Strata and remove any `~/.config/strata/settings.toml`
there. Then run `mkdir -p ~/.config/strata` and the same `ln -s` line.
Strata writes through the link and keeps the file's permissions. The link and
the file must both be yours, and the file must exist.

Strata loads the file at startup. Pull dotfiles changes while Strata is
closed: a change made in a running Strata saves its own copy of every setting
over them.

Link the file, not `~/.config/strata`: `tabs.toml` there changes as you work.
Custom themes live in its `themes/` folder; link that too. Otherwise a missing
custom theme falls back to Azure Glow, and your next change saves that into your
dotfiles. Copy custom actions into `actions/` rather than linking it: Strata
cannot create, edit, import, or toggle an action in a linked `actions/`.

## Settings worth changing

<!-- node: settings/preferences/language, Language setting -->
<!-- node: settings/preferences/date-format, Choosing a format -->
<!-- node: settings/preferences/date-format, Relative labels -->
<!-- node: settings/preferences, Default directory -->
<!-- node: settings/preferences, Hidden files -->

### Language

**General → Language** offers **Auto-detect**, which follows your system
language, and 11 languages listed by their own names, such as **Français**. Click
**Restart now** to apply the change. Japanese, Korean, and Chinese need a CJK
font such as Noto Sans CJK.

In the file, write `language = "auto"` or a code: `en`, `fr`, `de`, `es`, `it`,
`pt-BR`, `ru`, `vi`, `ja`, `ko`, or `zh-CN`.

### Modified date format

**General → Modified date format** sets how file times read in lists and
previews.

| Choice | Looks like | `date_format =` |
| --- | --- | --- |
| **Relative** (default) | "Just now", "5m ago", "Monday", "2w ago" | `"relative"` |
| **ISO 8601** | `2026-09-17 14:30` | `"iso"` |
| **Long** | "September 17, 2026, 14:30" | `"long"` |

### Where new windows open

Under **General → Default directory**, click **Home directory** and pick a
folder. A new window opens there unless it has a folder to open or tabs to
restore; turn off **Restore open tabs** to always start there. **Reset** returns
to home.

### Hidden files

Press Ctrl+H or Ctrl+. to show or hide hidden files in every window. Strata
remembers the choice.

## Good to know

<!-- node: settings/preferences/storage, Synchronization -->
<!-- node: settings/preferences/storage, Loading and recovery -->
<!-- node: settings/preferences/storage, Save notices -->
<!-- node: settings/preferences/storage, Saving -->

- A change in one window applies to every open window at once, except
  **Language** and **Appearance → Interface renderer**, which wait for a restart.
- Opening Settings never writes to `settings.toml`; only a change does.
- A bad value, such as `show_hidden = "yes"`, falls back to its default alone.
- If the file is not valid TOML, Strata starts with defaults and never saves
  over it. Your first change shows **Settings file can't be read**. Fix the file
  and restart Strata.
- If a save fails, **Settings can't be saved** appears. Changes last until
  Strata closes; each new change retries the save.

**Full detail:** the [Themes reference](../reference/themes.md) covers
**Appearance**; [Browser tabs](../reference/keyboard-navigation.md#browser-tabs)
covers **Restore open tabs**.
