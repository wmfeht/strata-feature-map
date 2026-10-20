---
title: Install a specific release
status: shipped
origin: {issue: lgse/strata#1779, pr: lgse/strata#1781}
branch: null
reviewed_at: fd6327265eaa3266f8420fe8bd25e965146344b0
review: draft
code: [src/ui/settings/release_picker.rs]
tests: [src/ui/settings/tests/release_picker.rs]
related: [app/updates/install, app/updates/release-channels]
---

## Summary

The "Install a specific release" menu in Settings → Updates. It lists the releases the selected channel offers, older or newer than the installed one. Users roll back after a regression or switch builds. Only in-place installs show it.

## Behavior

### Row

- On an in-place install, Settings → Updates shows "Install a specific release" with "Roll back or switch to another release your channel offers." lgse/strata#1781
- AUR, Omarchy, and pacman installs show no "Install a specific release" row. lgse/strata#1779, lgse/strata#1781
- The row's menu button shows the installed version, such as "v1.0.0". lgse/strata#1781 (unverified)
- With automatic checks off, the menu stays usable while the Release channel menu is insensitive. lgse/strata#1781 (unverified)

### Loading

- Opening Settings → Updates requests no release list; opening the menu shows "Loading releases…", then the list. lgse/strata#1781
- Reopening the menu on the same channel reuses the loaded list without a new request. lgse/strata#1781
- After a failed load, the next opening of the menu requests the list again. lgse/strata#1781
- Changing the release channel discards the list. An open menu reloads at once; a closed one reloads when next opened. lgse/strata#1781 (unverified)
- A channel with no installable release shows "No releases are available on this channel." lgse/strata#1781 (unverified)
- A failed request shows "Couldn't load releases: <reason>"; a list worker that stops without an answer shows "Couldn't load releases" once. lgse/strata#1781 (unverified)

### Choosing

- Each entry shows "vX" above "<build kind> · <date>", such as "Stable · <date>"; the installed release has a check mark. lgse/strata#1781
- A release with no publication date shows its build kind alone on the second line. lgse/strata#1781 (unverified)
- Over AT-SPI each entry is a radio menu item named "vX", checked only for the installed release. lgse/strata#1781 (unverified)
- Choosing the installed release closes the menu and opens nothing. lgse/strata#1781
- Choosing another release closes the menu and opens the update dialog for that release once its commit is resolved. lgse/strata#1781
- The menu button is insensitive while the chosen release's commit is resolved. lgse/strata#1781 (unverified)

## Design

The list is fetched only when the menu opens, so opening Settings alone never calls GitHub (lgse/strata#1781). Which releases it holds, and why it ignores the installed version, is in `app/updates/release-channels`.

- Package-managed installs get no menu, because their package manager decides the version (lgse/strata#1779).
- A chosen release reuses the update dialog and its verified, install-guarded flow rather than a separate install path (lgse/strata#1781).
- Downloading an older archive by hand was the rejected alternative: it skips manifest verification and the rollback safety net (lgse/strata#1779).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |

## Known gaps

None known.
