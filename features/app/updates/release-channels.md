---
title: Release channels
status: shipped
origin: {issue: lgse/strata#61, pr: lgse/strata#97}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: reviewed
code: [src/services/release_channel.rs]
tests: [src/services/release_channel/tests.rs]
docs: [docs/releasing.md]
related: []
---

## Summary

The Stable, Preview, and Nightly update channels, release ordering, and the Return to stable path off a prerelease build. Stable users never see a prerelease offer.

## Behavior

### Channels

- The Release channel menu in Settings → Updates offers Stable, Preview, and Nightly; Stable is the default. lgse/strata#97
- An unrecognized saved channel value is read as Stable. lgse/strata#97
- Stable offers only releases whose tag has no prerelease suffix and whose GitHub prerelease flag is false. lgse/strata#97
- Stable checks read only GitHub's `/releases/latest`; Preview and Nightly checks read the 30 newest releases. lgse/strata#97 (unverified)
- Preview offers stable, alpha, beta, and release-candidate builds but not nightlies. lgse/strata#97
- Nightly offers every recognized build kind. lgse/strata#97
- Drafts, releases without this architecture's archive, and tags outside `v?MAJOR.MINOR.PATCH` with an optional `-alpha.N`, `-beta.N`, `-rc.N` (N ≥ 1), or `-nightly.YYYYMMDD[.N]` suffix are never offered. lgse/strata#97
- Outside Return to stable, only a release newer than the installed build is offered. For one core version, nightly sorts below alpha, beta, rc, then the final release. lgse/strata#97
- A Preview user on `0.5.0-rc.2` is offered the final `0.5.0`. lgse/strata#97

### Return to stable

- On an in-place install, selecting Stable while running a prerelease offers the newest stable release, even when older, and the row's button reads "Return to stable". lgse/strata#97
- The status then reads "Stable channel target: vX", linking to the release. The download reads "Downloading stable release…"; success reads "Stable release installed — restart to apply". lgse/strata#97 (unverified)

### Channel changes

- Changing the channel clears the sidebar notice in every window and re-runs the check on every open Updates page. lgse/strata#126
- An Updates row that is installing or waiting to restart is not re-checked on a channel change. lgse/strata#126
- An open update dialog whose build the new channel excludes, before installing starts, reads "This build is no longer offered on your update channel — check for updates again." Its button becomes Close. lgse/strata#126
- Clicking Install update on an offer the current channel excludes runs a new check instead of installing. lgse/strata#97

### Labels

- A prerelease offer shows its build kind as a badge in the notes and the update dialog. lgse/strata#97
- The dialog for a prerelease shows "Channel", "Tag", "Commit", and "Published" rows above its notes. lgse/strata#97

## Design

[README.md's Release channels section](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/README.md) states the user-facing contract. [docs/releasing.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/releasing.md) defines the tag grammar and build ordering.

- The updater once zero-filled unparsable segments, so `0.5.0-rc.1` read as `0.5.0`. `Version::parse` is now the only place tags are interpreted, with semver precedence (lgse/strata#97).
- Channel logic is a pure module with no I/O, so "Stable never sees a prerelease" is provable in unit tests (lgse/strata#97).
- Stable uses a separate fetch path that never enumerates prereleases. Both the tag and GitHub's prerelease flag must say final, so one mislabelled signal is still caught (lgse/strata#61).
- Every parse fails closed to Stable: unknown config values, missing keys, and unparsable build metadata (lgse/strata#97).
- RC outranks nightly at equal core version, matching semver's ordering of `nightly` before `rc` (lgse/strata#97).
- Return to stable is gated on the running build being a prerelease, not on the selected channel. Otherwise a user who already chose Stable would be stranded on an RC (lgse/strata#97).
- The transition reuses the ordinary update card rather than a separate rollback card, so the two never compete (lgse/strata#97).
- The channel is re-tested at the click, which holds however many views cached an offer. The change broadcast only keeps those views current (lgse/strata#123).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-03 | lgse/strata#126 | feat | Refreshed every open update view when the release channel changes. |
| 2026-09-02 | lgse/strata#97 | feat | Added Stable, Preview, and Nightly channels with semver ordering and Return to stable. |

## Known gaps

None known.
