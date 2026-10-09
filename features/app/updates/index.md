---
title: Updates
status: shipped
origin: {issue: null, pr: lgse/strata#22}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [src/services/update_check.rs]
tests: [src/services/update_check/tests.rs, src/ui/settings/tests/updates.rs]
docs: []
related: []
---

## Summary

Checking GitHub for a newer Strata release, the Settings → Updates page, release notes, and the sidebar update notice. Children: `app/updates/release-channels` (Stable, Preview, Nightly, and Return to stable), `app/updates/install` (signed in-place install, rollback, and restart), and `app/updates/package-managed` (AUR, Omarchy, and pacman installs).

## Behavior

### Checking

- With "Check for updates automatically" on, a check starts after a window's first themed frame, at most once per 24 hours per process. lgse/strata#944, lgse/strata#326
- Automatic checks are on in a new profile. lgse/strata#1461
- Opening Settings → Updates starts an automatic check when one is due. lgse/strata#944
- The first automatic check of a session ignores the on-disk cache. lgse/strata#326
- Later automatic checks reuse a cached result younger than 6 hours for the same channel from `~/.cache/strata/update-check.toml`. lgse/strata#197
- Check now always queries GitHub, regardless of the cache. lgse/strata#197
- A check sends the cached ETag in `If-None-Match` and reuses the cached release list on `304 Not Modified`. lgse/strata#197
- A GitHub 403 or 429 reports "GitHub API rate limit reached"; other statuses report "GitHub API returned HTTP N". lgse/strata#51

### Settings → Updates

- Before a check, the status row reads "Version X", adding the build kind, such as "Release candidate", for a prerelease build. lgse/strata#97
- After a check, the row title reads "Strata is up to date", "An update is available", or "Couldn’t check for updates". lgse/strata#51 (unverified)
- A failed check shows its reason and a "View releases on GitHub" link. lgse/strata#22 (unverified)
- An available update shows its notes inline, titled "Available release · vX" with its change count and publication date. lgse/strata#51
- Turning automatic checks off clears the sidebar notice in every window; turning them on runs a check. lgse/strata#944 (unverified)
- The Release channel menu is insensitive while automatic checks are off. lgse/strata#97 (unverified)

### Release notes

- The Release notes section holds a collapsed "What's new in vX" expander with the notes of the installed build's exact tag. lgse/strata#51, lgse/strata#849
- Installed-release notes are fetched once per tag and kept in `~/.cache/strata/release-notes.toml`. lgse/strata#197
- Without a GitHub release for the installed tag, the expander reads "Release notes are unavailable because this version’s tag was not found." and links to GitHub. lgse/strata#51
- A release with empty notes shows "No release notes were provided for this release." lgse/strata#51
- Notes render headings, paragraphs, lists, code, and rules; images, tables, and block quotes are omitted. lgse/strata#51 (unverified)

### Sidebar notice

- When a check finds an update, every open window shows "vX available" with a download icon at the foot of its sidebar. lgse/strata#26, lgse/strata#944
- A prerelease offer adds its build kind, such as "Nightly", on a second line of the notice. lgse/strata#97
- A window opened after the check shows the cached notice without another request. lgse/strata#944
- An automatic result that lands after checks were disabled or the channel changed is discarded. lgse/strata#944
- Clicking the notice opens the update dialog for that release. lgse/strata#51

### Update dialog

- The dialog is titled "Strata vX is available" and shows "Installed vA → Available vB". lgse/strata#51
- The release's notes appear under "What’s new" in a scrolling area above the Download update button, with a "View release on GitHub" link. lgse/strata#51
- Empty notes read "No release notes were provided. Review this release on GitHub before continuing." lgse/strata#51

## Design

Update checks use GitHub's unauthenticated REST API, limited to 60 requests per hour per address. Users behind shared NAT or VPN exits hit that limit (lgse/strata#181).

- Strata caches instead of changing the source. A published `latest.json` was heavier, `releases.atom` carries HTML notes, and shipping an API token was rejected (lgse/strata#181).
- GitHub answers unauthenticated conditional requests with `200`, so the 6-hour floor and the per-tag notes cache do the actual saving (lgse/strata#197).
- The first automatic check of each session bypasses the cache so a fresh launch never shows stale release information. Disabling the cache for every check was rejected as wasteful (lgse/strata#325).
- Results are broadcast to every window, and the last offer is cached for windows opened later (lgse/strata#866).
- Each check carries a generation number. A result superseded by a newer check is dropped, so a Preview result cannot land after a switch to Stable (lgse/strata#97).
- Checks and package-manager detection run off the GTK thread, after the first frame rather than on a fixed 8-second delay (lgse/strata#944).
- A release-notes failure never blocks an eligible update; the GitHub release page stays available as a fallback (lgse/strata#48).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-16 | lgse/strata#1068 | fix | Removed the horizontal inset from the sidebar update notice. |
| 2026-09-15 | lgse/strata#944 | fix | Broadcast check results to every window and started the automatic check after the first frame. |
| 2026-09-04 | lgse/strata#326 | fix | Forced the first automatic check of a session past the on-disk cache. |
| 2026-09-03 | lgse/strata#197 | feat | Cached update checks for 6 hours and installed-release notes per tag to ease GitHub rate limits. |
| 2026-08-31 | lgse/strata#51 | feat | Added the Updates page and release notes shown before upgrading. |
| 2026-08-30 | lgse/strata#22 | feat | Added automatic and manual update checks with a sidebar notice. |

## Known gaps

- The README describes automatic checks as opt-in, but they are on by default; the fix is scheduled in a triage batch. lgse/strata#1461, lgse/strata#1546
