---
title: Follow system light/dark mode
status: shipped
origin: {issue: lgse/strata#1812, pr: lgse/strata#2094}
branch: null
reviewed_at: 5f17c9fdc8967e1b4ba8aaf8de113b46d824b0dd
review: draft
code: [src/ui/theme/system_appearance.rs]
tests: [src/ui/theme/tests/system_appearance.rs]
related: [settings/themes/omarchy]
---

## Summary

Follow system light/dark mode switches Strata between the light and dark themes of a curated bundled family to match the desktop's light/dark preference. It reads the XDG settings portal first, for KDE and Flatpak, and GNOME's `color-scheme` key as fallback. Strata keeps its own palettes.

## Behavior

### Switch

- Settings → Appearance shows a Follow system light/dark mode switch before Follow Omarchy. lgse/strata#2094 (unverified)
- Its subtitle reads "Use the light or dark version of the chosen theme to match your desktop's light/dark mode." lgse/strata#2094 (unverified)
- Without the `org.gnome.desktop.interface` schema, the switch shows while the portal read is pending and stays shown when the portal returns a value. lgse/strata#2113
- The switch is hidden only after the portal read fails and the `org.gnome.desktop.interface` schema or its `color-scheme` key is absent. lgse/strata#2094, lgse/strata#2113
- With no settings portal and no GNOME schema, Settings search for "day night" does not show the switch. lgse/strata#2094, lgse/strata#2113 (unverified)
- With no settings portal and no GNOME schema, a saved `mode = "system"` is saved as `mode = "theme"` once the portal read fails. lgse/strata#2113
- That repair happens after startup, not at load: a pending portal read counts as available when preferences load. lgse/strata#2113 (unverified)
- After a failed portal read, a later portal change signal shows the switch again. lgse/strata#2113
- A `mode` already repaired to `"theme"` stays `"theme"` after that change signal. lgse/strata#2113 (unverified)
- A saved `mode` other than `theme`, `system`, or `omarchy`, such as `"unknown"`, loads as `mode = "theme"`. lgse/strata#2094 (unverified)
- Turning Follow system light/dark mode on turns Follow Omarchy off, and the reverse. lgse/strata#2094
- Turning Follow system light/dark mode off saves `mode = "theme"` and keeps the saved `theme`. lgse/strata#2094 (unverified)
- Toggling Follow system light/dark mode during an editor preview ends the preview. lgse/strata#2094 (unverified)

### Following

- While following, a portal `org.freedesktop.appearance` `color-scheme` of `1` applies the family's dark theme, even when GNOME's key is `prefer-light`. lgse/strata#2113
- While following, a portal `color-scheme` of `2` applies the family's light theme, even when GNOME's key is `prefer-dark`. lgse/strata#2113
- With portal `color-scheme` `0` or no portal, GNOME's `color-scheme = prefer-dark` applies the dark theme of the family, such as One Dark. lgse/strata#2094, lgse/strata#2113
- With portal `0` or no portal, GNOME's `default`, `prefer-light`, or any other value applies the family's light theme, such as One Light. lgse/strata#2094, lgse/strata#2113
- With portal `0` or no portal, changing GNOME's `color-scheme` with `gsettings` while Strata runs re-applies the theme without a restart. lgse/strata#2094, lgse/strata#2113
- A portal `SettingChanged` for `color-scheme` while Strata runs re-applies the theme without a restart, such as One Dark to One Light on `1` to `2`. lgse/strata#2113
- When the portal read fails and GNOME's schema is present, GNOME's value applies and `mode` stays `"system"`. lgse/strata#2113
- Strata never writes `color-scheme` to GNOME or the portal, and never loads the desktop's GTK theme, icon theme, or accent color. lgse/strata#2094, lgse/strata#2113
- 28 bundled families have a pair, such as One Dark/One Light, Catppuccin Mocha/Latte, and Rosé Pine/Dawn. lgse/strata#2094
- An unpaired theme, such as Tokyo Night or an unpaired custom theme, keeps one palette in both modes. lgse/strata#2094
- A custom `.toml` whose stem overrides a paired bundled id, such as `one-light.toml`, joins that pair. lgse/strata#2094
- A mode change re-applies the GTK light/dark base variant, Strata colors, icons, documents, source highlighting, previews, and open Settings pages. lgse/strata#2094
- Launching with `mode = "system"` saved waits up to 500 ms for the first portal value, then opens in the theme for that mode. lgse/strata#2094, lgse/strata#2113
- When that first read times out, fails, or reports `0`, Strata opens in GNOME's mode, or light without GNOME, and switches when a late portal reply arrives. lgse/strata#2113
- Launching with a saved `mode` other than `"system"` does not wait for the portal. lgse/strata#2113
- The D-Bus-activated service and the FileChooser portal backend never wait for the portal, even with `mode = "system"` saved. lgse/strata#2113

### Theme library

- The saved `theme` is the family anchor: with One Dark saved and a light desktop, `settings.toml` keeps `theme = "onedark-dark"` and `mode = "system"`. lgse/strata#2094
- Clicking either theme of a pair in the library changes the family and leaves following on. With a dark desktop, clicking One Light applies One Dark and checks its card. lgse/strata#2094
- Current theme and the checked library card show the theme in use, so One Dark saved under a light desktop checks One Light. lgse/strata#2094
- While following, the Current theme description reads "Following the system light/dark mode. Choose a theme family from the library below." lgse/strata#2094 (unverified)
- While following, PDF text selection uses the colors of the theme in use. lgse/strata#2094
- While following, deleting a custom file that overrides the paired theme in use, such as `one-light.toml`, applies the bundled theme of that id. lgse/strata#2094 (unverified)

## Design

[docs/themes.md](https://github.com/lgse/strata/blob/5f17c9fdc8967e1b4ba8aaf8de113b46d824b0dd/docs/themes.md) describes the switch, its portal and GNOME sources, the startup wait, the anchor model, and the curated pairs in its System light/dark mode section.

- lgse/strata#1812 asked for theme variants to follow `org.gnome.desktop.interface color-scheme`, as other GTK apps do. Until then only Omarchy users got day and night switching (lgse/strata#1812).
- Only the light/dark preference is followed. Strata keeps its own palettes and reads the key without writing it (lgse/strata#2094).
- KDE and some other desktops publish light/dark only through the XDG settings portal, where GNOME's key alone left the switch without effect (https://github.com/lgse/strata/pull/2094#issuecomment-6727770985, lgse/strata#2113).
- The portal is the primary source because it covers KDE and sandboxed Flatpak. GNOME's key is the fallback for `0` or an unavailable portal (lgse/strata#2113).
- The 500 ms startup wait lets Strata open in the right palette. It applies only with `mode = "system"`, so other launches never block on the portal (https://github.com/lgse/strata/pull/2113#issuecomment-6801438693).
- The service and FileChooser processes skip the wait so D-Bus activation never blocks on the portal (lgse/strata#2113).
- ashpd builds the Settings proxy and its change subscription without a running portal. Availability therefore follows the `color-scheme` read, not proxy creation (https://github.com/lgse/strata/pull/2113#issuecomment-6801438693).
- A transient read failure on a desktop without GNOME's schema still resets a saved `system` mode. The maintainer kept this, the policy already applied to a missing schema (https://github.com/lgse/strata/pull/2113#issuecomment-6801438693).
- The saved theme is the family anchor and the theme in use is derived from it, so following never rewrites `theme` (lgse/strata#2094).
- Pairs are a curated `(dark, light)` list in code. Unpaired ids deliberately resolve to themselves (lgse/strata#2094).
- Following is a third value of the single theme `mode`, so it and Omarchy following cannot both be on (lgse/strata#2094).
- Every consumer of the current palette, such as PDF selection and the Add theme editor, resolves through the theme in use. Reading the saved anchor showed the other side of the pair (lgse/strata#2094).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-11-12 | lgse/strata#2113 | fix | Read light/dark mode from the settings portal's `org.freedesktop.appearance` `color-scheme` first, with GNOME's key as fallback, so KDE and Flatpak desktops follow it. |

## Known gaps

- On a desktop without GNOME's schema, a transient portal read failure resets a saved `mode = "system"` to `"theme"`. lgse/strata#2113, https://github.com/lgse/strata/pull/2113#issuecomment-6801438693
