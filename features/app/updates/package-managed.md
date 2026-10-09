---
title: Package-managed installs
status: shipped
origin: {issue: lgse/strata#195, pr: lgse/strata#196}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [src/services/install_source.rs]
tests: [src/services/install_source/tests.rs]
docs: [docs/packaging.md]
related: [app/packaging/aur]
---

## Summary

Update checks and actions for Strata installed by a package manager: the official AUR packages, the Omarchy Package Repository, and other pacman repositories. These installs keep notices and release notes but never replace their own binary.

## Behavior

### Detection

- A `share/strata/install-source.toml` marker under the binary's install prefix marks the install as package-managed, even when unreadable or unparsable. lgse/strata#183
- Without a marker, a binary owned by pacman is Omarchy-managed when `/etc/os-release` has `ID=omarchy`, and pacman-managed otherwise. lgse/strata#196
- When the pacman ownership query fails for a reason other than pacman being absent, in-place updates are disabled. lgse/strata#196 (unverified)
- A binary no package owns, such as `~/.local/bin/strata`, keeps in-place updates. lgse/strata#196

### Checking

- A marker install checks the AUR for the package the marker names. lgse/strata#183
- An Omarchy install reads the live `omarchy.db` from the server `pacman-conf` lists for the `omarchy` repository. lgse/strata#210
- Another pacman install reads the version its configured sync databases offer. lgse/strata#210
- A notice appears only when the repository version is newer than the installed one, with that exact GitHub release's notes. lgse/strata#210
- A GitHub release the repository does not carry yet produces no notice. lgse/strata#210
- When the repository version is a prerelease, a matching GitHub release flagged prerelease is accepted; a stable version requires a stable release. lgse/strata#744

### Settings and actions

- With a marker, Settings → Updates shows a "Package-managed installation" row naming the manager, package, tracked channel, update instruction, and alternate package. lgse/strata#183
- The status line appends "Managed by Omarchy", "Managed by pacman", or "Managed by" the marker's manager. lgse/strata#196, lgse/strata#183
- With a marker, the Release channel menu is disabled and follows the marker's channel, mapping `rc` and `preview` to Preview. lgse/strata#183
- Without a marker, an Omarchy or pacman install hides the Release channel row. lgse/strata#196 (unverified)
- No package-managed install offers an in-app download, and the installer refuses one before downloading. lgse/strata#196
- With an update available, an Omarchy install offers "Open Omarchy Update", which runs `omarchy update` in the configured terminal. lgse/strata#196
- An AUR install offers "Open AUR Update", running `<helper> -Syu <package>` in a terminal, when a marker-listed helper is on `PATH`. lgse/strata#183 (unverified)
- Without such a helper, an AUR install offers "View on AUR", which opens the package page. lgse/strata#183 (unverified)
- A pacman install says to install through a full system update and offers no install action. lgse/strata#196, lgse/strata#210

## Design

Replacing a pacman-owned `/usr/bin/strata` fails on permissions, and with enough privilege would desynchronize pacman's database (lgse/strata#195).

[docs/packaging.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/packaging.md) carries the marker format and why it names helpers instead of an update command.

- Ownership comes from querying pacman, not from a `/usr/bin` heuristic that misclassifies manual installs (lgse/strata#195).
- Checks and release notes stay; only installation defers. Letting replacement fail late, or disabling checks, were rejected (lgse/strata#195).
- The repository, not GitHub, decides availability, so a notice never promises an update the package manager cannot install yet (lgse/strata#209).
- Omarchy's live database is read instead of pacman's cache, because the same `omarchy update` that installs Strata refreshes that cache (lgse/strata#210).
- The marker is scoped to the official AUR packages, locks the shown channel to the package, and tolerates unknown keys for older binaries (lgse/strata#183).
- The AUR marker lists helpers instead of an `update_command`, because pacman cannot update an AUR package (lgse/strata#183, docs/packaging.md).
- Detection fails safe: an unreadable marker or a failed ownership query keeps in-place replacement off (lgse/strata#183, lgse/strata#196).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-10 | lgse/strata#744 | fix | Let prerelease AUR packages accept their prerelease GitHub releases. |
| 2026-09-03 | lgse/strata#210 | fix | Gated package-managed notices on the version the configured repository offers. |
| 2026-09-03 | lgse/strata#196 | feat | Detected pacman-owned binaries and deferred their installs to Omarchy or pacman. |

## Known gaps

None known.
