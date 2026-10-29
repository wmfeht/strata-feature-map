---
title: Updates
status: shipped
origin: {issue: null, pr: lgse/strata#22}
branch: null
reviewed_at: 44bfeab305cfb68993bafcf4794fe0bbf7ff1433
review: draft
code: [src/services/update_check.rs, src/ui/settings/update_status.rs]
tests: [src/services/update_check/tests.rs, src/ui/settings/tests/updates.rs]
docs: [docs/preferences.md, docs/packaging.md]
related: [browser/sidebar]
---

## Summary

Checking GitHub for a newer Strata release, the Settings → Updates page, release notes, and the sidebar update notice. A build made with `STRATA_UPDATER=disabled` leaves the updater out. Children: `app/updates/release-channels` (Stable, Preview, Nightly, and Return to stable), `app/updates/install` (signed in-place install, rollback, and restart), `app/updates/release-picker` (installing a chosen release), and `app/updates/package-managed` (AUR, Omarchy, and pacman installs).

## Behavior

### Builds without the updater

- A build made with `STRATA_UPDATER=disabled` has no Updates entry in the Settings navigation and no Updates page. lgse/strata#1934
- Such a build never starts an automatic check, so the sidebar update notice never appears. lgse/strata#1934
- A build with `STRATA_UPDATER` unset or `enabled` keeps the Updates page and update checks. lgse/strata#1934

### Checking

- In a build with the updater, with "Check for updates automatically" on, a window's first themed frame starts a check unless one completed in this process within 24 hours. lgse/strata#944, lgse/strata#326
- Automatic checks are on in a new profile. lgse/strata#1461
- The first visit to Settings → Updates in a window starts an automatic check when one is due. lgse/strata#944
- The first automatic check of a session ignores the on-disk cache. lgse/strata#326
- Later automatic checks, and the check run by turning automatic checks on, reuse a cached result under 6 hours old for the same channel from `~/.cache/strata/update-check.toml`. lgse/strata#197, lgse/strata#326
- Check now always queries GitHub, regardless of the cache. lgse/strata#197
- A check sends the cached ETag in `If-None-Match` and reuses the cached release list on `304 Not Modified`. lgse/strata#197
- A GitHub 403 or 429 reports "GitHub API rate limit reached"; other statuses report "GitHub API returned HTTP N". lgse/strata#51

### Release list

- The "Install a specific release" list keeps only releases with this architecture's archive, `strata-update-manifest.json`, and `strata-update-manifest.signatures.json`. lgse/strata#1781
- Releases before `v0.22.0-nightly.20261005` have no signed manifest, so the list omits them. lgse/strata#1781
- The list reads GitHub's releases in pages of 100. It stops after a page shorter than 100, a page whose last release is unsigned, or 5 requests. lgse/strata#1781
- A failed page fails the whole list, with no partial list. lgse/strata#1781

### Settings → Updates

- Before a check, the status row reads "Version X", adding the build kind, such as "Release candidate", for a prerelease build. lgse/strata#97
- After a check, the row title reads "Strata is up to date", "An update is available", or "Couldn’t check for updates". lgse/strata#51 (unverified)
- A failed check shows its reason and a "View releases on GitHub" link. lgse/strata#22 (unverified)
- A check whose worker ends without a result fails with the reason "An unexpected system error occurred". lgse/strata#1909 (unverified)
- Settings → Updates opened after the startup check completed shows that check's result, without Check now or another request. lgse/strata#1909
- When a startup or manual check completes, every open Settings → Updates row shows its result. lgse/strata#1909
- Check now in one Settings window leaves other windows' rows, including an offer's Install button, unchanged until its result lands. lgse/strata#1909
- On a pacman or Omarchy install with a Preview or Nightly preference, a startup offer shows on the row with its package-managed action, such as "Check again". lgse/strata#1909
- Turning automatic checks off or changing the channel resets every open row to "Check for updates" and Check now, except a row mid-check or with an install underway. lgse/strata#1909 (unverified)
- An available update shows its notes inline, titled "Available release · vX" with its change count and publication date. lgse/strata#51
- Turning automatic checks off clears the sidebar notice in every window; turning them on runs a check. lgse/strata#944, lgse/strata#1554
- The Release channel menu is insensitive while automatic checks are off. lgse/strata#97 (unverified)

### Release notes

- The Release notes section holds a collapsed "What's new in vX" expander with the notes of the installed build's exact tag. lgse/strata#51, lgse/strata#849
- Installed-release notes are fetched once per tag and kept in `~/.cache/strata/release-notes.toml`. lgse/strata#197
- Without a GitHub release for the installed tag, the expander reads "Release notes are unavailable because this version’s tag was not found." and links to GitHub. lgse/strata#51
- A release with empty notes, or notes holding only HTML comments, shows "No release notes were provided for this release." lgse/strata#51, lgse/strata#1570, lgse/strata#1464
- A release body starting with `<!-- Release notes generated … -->` shows its notes from the first heading, without the comment. lgse/strata#1570, lgse/strata#1464
- Multi-line and inline HTML comments in notes are hidden; other raw HTML, such as `<b>x</b>`, shows as escaped text. lgse/strata#1570
- When a comment starts a line, text after `-->` on its closing line is hidden with it; an inline comment hides only the comment. lgse/strata#1570
- Notes render headings, paragraphs, lists, code, and rules; images, tables, and block quotes are omitted. lgse/strata#51, lgse/strata#48 (unverified)

### Sidebar notice

- A window opened after the check shows the cached notice without another request. lgse/strata#944
- An automatic result that lands after checks were disabled or the channel changed is discarded. lgse/strata#944
- Clicking the notice opens the update dialog for that release. lgse/strata#51

### Update dialog

- For an update offer, the dialog is titled "Strata vX is available" and shows "Installed vA  →  Available vB". lgse/strata#51, lgse/strata#1781
- For a chosen release, the dialog is titled "Install Strata vX" and shows "Installed vA  →  Selected vB". Its button reads "Install release". lgse/strata#1781
- The chosen-release dialog's status reads "Review the release notes before installing this release." lgse/strata#1781 (unverified)
- The release's notes appear under "What’s new" in a scrolling area above the action button, with a "View release on GitHub" link. lgse/strata#51, lgse/strata#1781
- Empty or comment-only notes read "No release notes were provided. Review this release on GitHub before continuing." lgse/strata#51, lgse/strata#1570

## Design

Update checks use GitHub's unauthenticated REST API, limited to 60 requests per hour per address. Users behind shared NAT or VPN exits hit that limit (lgse/strata#181).

- Strata caches instead of changing the source. A published `latest.json` was heavier, `releases.atom` carries HTML notes, and shipping an API token was rejected (lgse/strata#181).
- GitHub answers unauthenticated conditional requests with `200`, so the 6-hour floor and the per-tag notes cache do the actual saving (lgse/strata#197).
- The first automatic check of each session bypasses the cache so a fresh launch never shows stale release information. Disabling the cache for every check was rejected as wasteful (lgse/strata#325).
- Results are broadcast to every window (lgse/strata#866). The last completed result, whether an offer, up to date, or a failure, is one shared snapshot. Every Settings → Updates row renders it, including rows opened later (lgse/strata#1909).
- Check now drops the shared snapshot and the sidebar notice, but other rows keep their rendering until the new result lands (lgse/strata#1909).
- Each check carries a generation number. A result superseded by a newer check is dropped, so a Preview result cannot land after a switch to Stable (lgse/strata#97).
- Checks and package-manager detection run off the GTK thread, after the first frame rather than on a fixed 8-second delay (lgse/strata#944).
- A release-notes failure never blocks an eligible update; the GitHub release page stays available as a fallback (lgse/strata#48).
- The release list hides unsigned releases, because they would fail install verification (lgse/strata#1779, lgse/strata#1781).
- One 100-release page let older signed stable releases fall off, since nightlies are never pruned. Paging stops where signed history ends, and 5 requests stay inside the unauthenticated rate limit (lgse/strata#1781).
- Distributions whose packages deliver updates build with `STRATA_UPDATER=disabled`. Reusing the AUR `install-source.toml` marker was rejected, because its update check and wording are AUR-specific (lgse/strata#1933).
- The switch accepts only `enabled` and `disabled`, so a typo fails the build instead of shipping an updater (lgse/strata#1934).
- HTML comments are stripped only in the client, and only from release notes. Published releases already carry the comment, and `--generate-notes` adds it to every body. Markdown file previews still show comments (lgse/strata#1464, lgse/strata#1570).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-29 | lgse/strata#1909 | fix | Shared one completed update-check result with every Settings → Updates row, so a page opened after the startup check shows it. |
| 2026-10-29 | lgse/strata#1934 | feat | Added the `STRATA_UPDATER=disabled` build switch, which leaves the updater out for distributions whose packages deliver updates. |
| 2026-10-20 | lgse/strata#1781 | feat | Added "Install a specific release", listing the channel's signed releases so users can roll back or switch builds. |
| 2026-10-15 | lgse/strata#1609 | fix | Opened Omarchy Update in Omarchy's floating presentation terminal, so its output stays open after the update ends or fails. |
| 2026-09-16 | lgse/strata#1068 | fix | Removed the horizontal inset from the sidebar update notice. |
| 2026-09-15 | lgse/strata#944 | fix | Broadcast check results to every window and started the automatic check after the first frame. |
| 2026-09-04 | lgse/strata#326 | fix | Forced the first automatic check of a session past the on-disk cache. |
| 2026-09-03 | lgse/strata#197 | feat | Cached update checks for 6 hours and installed-release notes per tag to ease GitHub rate limits. |
| 2026-08-31 | lgse/strata#51 | feat | Added the Updates page and release notes shown before upgrading. |
| 2026-08-30 | lgse/strata#22 | feat | Added automatic and manual update checks with a sidebar notice. |

## Known gaps

- A Settings → Updates row with an install underway ignores newer check results. A cancelled or failed install keeps its status until the next check result. lgse/strata#1909
- Releases older than the 500 newest on GitHub are not listed, because the release list is capped at 5 requests of 100. lgse/strata#1781
