---
title: Recently used applications
status: shipped
origin: {issue: null, pr: lgse/strata#1354}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: reviewed
code: [src/ui/recent_apps]
tests: [src/ui/recent_apps/tests.rs]
related: []
---

## Summary

A Recently Used section at the top of the Open With chooser, listing the applications last used for the selected files' MIME types.

## Behavior

- After an application opens files through Open With, it appears under Recently Used, above Recommended Applications, for files of the same MIME type. lgse/strata#1354
- Opening a file with its default application by activation or Open also records that application. lgse/strata#1354 (unverified)
- Recently Used lists the most recent application first and shows at most 5. lgse/strata#1354
- An application shown under Recently Used is not repeated under Recommended or Other Applications. lgse/strata#1354
- History is shared by files of one MIME type and independent between types. lgse/strata#1354
- History persists across restarts. lgse/strata#1354
- History is stored in `$XDG_DATA_HOME/strata/recent-apps.toml`. lgse/strata#1354 (unverified)
- For a selection of several types, only applications recommended for every type are promoted. lgse/strata#1354 (unverified)
- For a single type, an application previously chosen from Other Applications is also promoted. lgse/strata#1354 (unverified)
- An uninstalled application is dropped from history at the next launch through Strata, unless no applications could be listed at all. lgse/strata#1354 (unverified)
- A missing, malformed, or unsupported-version history file shows no Recently Used section and does not block launching. lgse/strata#1354 (unverified)
- The chooser search filters Recently Used rows and hides the heading when none match. lgse/strata#1354 (unverified)

## Design

History is keyed by MIME type rather than by file path, so one choice serves every file of that type (lgse/strata#1354).

- Entries carry persisted sequence numbers instead of timestamps, so recency survives restarts and merges across the types of a multi-type selection. Exhausted counters are compacted without changing order (lgse/strata#1354) (unverified).
- History is advisory: read or write failures are logged and never prevent a launch (lgse/strata#1354).
- An empty application database leaves history untouched, so a failed discovery cannot erase it. A changed MIME association alone does not prune an installed application (lgse/strata#1354) (unverified).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-03 | lgse/strata#1354 | feat | Added a Recently Used section with the last 5 applications per MIME type. |

## Known gaps

None known.
