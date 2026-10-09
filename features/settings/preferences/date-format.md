---
title: Modified date format
status: shipped
origin: {issue: null, pr: lgse/strata#180}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [src/util/mod.rs]
tests: [src/util/tests.rs]
related: [browser/properties]
---

## Summary

How file modification times read in lists and previews, and the Modified date format preference that chooses between relative labels and two absolute formats.

## Behavior

### Choosing a format

- General → Date & time → Modified date format offers Relative, the default, ISO 8601, and Long; each choice shows an example for five minutes ago. lgse/strata#1102
- ISO 8601 renders `2026-09-17 14:30` and Long renders "September 17, 2026, 14:30". lgse/strata#1102
- Changing the format re-renders open modified-time labels in every window without reloading. lgse/strata#1102
- The choice is saved as `date_format`; `relative`, `iso`, and `long` load, and an unknown value loads as Relative. lgse/strata#1102 (unverified)

### Relative labels

- A time under a minute ago, or up to a minute in the future, reads "Just now". lgse/strata#1102
- A time further in the future shows the absolute date and time. lgse/strata#1102 (unverified)
- Under an hour reads whole minutes, such as "5m ago", and under 24 elapsed hours whole hours, such as "3h ago", even across midnight. lgse/strata#1102, lgse/strata#1264
- Past 24 hours, one to six local calendar days ago reads the full weekday name, such as "Monday". lgse/strata#741, lgse/strata#1264
- Seven to thirty calendar days ago reads whole weeks, such as "2w ago". lgse/strata#1264
- Older times read "Sep 1, 23:30" in the current year and "Sep 1, 2025" in earlier years. lgse/strata#1264
- On a daylight-saving fall-back day, a time earlier that day can read "24h ago". lgse/strata#1264
- Relative labels refresh every 30 seconds while shown. lgse/strata#1102 (unverified)
- Month and weekday names follow Strata's interface language, not the system locale. lgse/strata#1519

## Design

- Minute and hour buckets use elapsed time, so a file saved at 23:59 does not read as a day old at 00:00 (lgse/strata#1101).
- Day buckets compare local midnights, rounding so 23- and 25-hour daylight-saving days count as one day (lgse/strata#656, lgse/strata#741).
- Up to a minute of future time counts as clock skew, common on network mounts, rather than showing a raw timestamp (lgse/strata#1101).
- Following the system locale's date format was rejected because it gives no explicit control (lgse/strata#1101).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-25 | lgse/strata#1264 | fix | Switched relative labels to compact weekday and week buckets that hold across daylight saving and time zones. |
| 2026-09-19 | lgse/strata#1102 | feat | Added the Relative, ISO 8601, and Long preference and made sub-hour times use elapsed time. |
| 2026-09-10 | lgse/strata#741 | fix | Counted relative days by calendar date instead of 24-hour windows. |
| 2026-09-03 | lgse/strata#180 | feat | Replaced fixed timestamps with relative labels for recent modification times. |

## Known gaps

None known.
