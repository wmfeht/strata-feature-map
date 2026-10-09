---
title: Folder peek
status: shipped
origin: {issue: null, pr: lgse/strata#132}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [src/app/peek.rs, src/ui/browser/peek.rs]
tests: [src/app/peek/tests.rs, src/ui/browser/peek/tests.rs]
docs: [docs/preferences.md]
related: [settings/preferences, browser/view-modes, operations/drag-and-drop, integration/10xer-mode]
---

## Summary

A transient popover that lists up to 8 entries of a folder when the pointer rests on it in Icons or List. It is controlled by Settings → General → Browsing → Folder peeking, which is off by default.

## Behavior

### Opening

- With Folder peeking on, hovering a folder in Icons or List for 500 ms opens a popover headed by the folder's name. lgse/strata#1480, lgse/strata#1484
- Columns never shows a folder peek, whatever the saved preference, and switching to Columns closes an open or pending peek. lgse/strata#1484
- A fresh installation, or a settings file without `folder_peeking`, starts with Folder peeking off; a saved choice persists across restarts. lgse/strata#99, lgse/strata#1480
- Turning Folder peeking off closes an open peek and cancels a pending one. lgse/strata#1484 (unverified)
- The file chooser never shows hover peeks, whatever the saved preference. lgse/strata#518
- After keyboard navigation, hover peeks stay suppressed until the pointer moves again. lgse/strata#358
- Moving the pointer quickly from one folder to an adjacent folder and stopping opens the second folder's peek. lgse/strata#870
- Leaving a folder before the delay elapses opens no peek. lgse/strata#870

### Contents

- The popover lists at most 8 entries with thumbnails or type icons; folders show a trailing chevron. lgse/strata#43 (unverified)
- Long names are ellipsized in the middle, keeping the extension visible. lgse/strata#1143
- Hidden entries are left out unless hidden files are shown. lgse/strata#201, lgse/strata#1449

### Placement and closing

- The 256 px popover opens 8 px right of the hovered item and slides right; when that side lacks room it opens on the left and slides left. lgse/strata#132, lgse/strata#234
- When neither side fits, the popover overlays the viewport's trailing edge. lgse/strata#1181
- A viewport narrower than 256 px opens no peek. lgse/strata#234, lgse/strata#1181 (unverified)
- Moving the pointer from the folder onto the popover keeps it open; leaving both closes it after 80 ms. lgse/strata#870 (unverified)
- Starting or ending a drag cancels a pending peek and closes an open one, so a cancelled drag never shows a folder's contents. lgse/strata#630

## Design

[docs/preferences.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/preferences.md) records the default and the per-view rules.

- A peek is a separate load with its own request id, so batches from a stale load cannot fill a newer popover (lgse/strata#1449).
- Peek loads stop at 64 entries or 3 seconds, since the popover shows only a handful of items; a huge folder cannot freeze the browser (lgse/strata#154).
- The hover delay rose from 180 ms to 1000 ms when peeking became opt-in (lgse/strata#1479, lgse/strata#1480). It dropped to 500 ms when peeks were limited to Icons and List (lgse/strata#1484).
- Column layout reserves no space for a peek; the focused column and the preview take priority (lgse/strata#1405). Columns stopped showing peeks entirely in lgse/strata#1484.
- A late `leave` from the previous folder only re-arms the close timer. The open timer checks that the anchor is still hovered before opening (lgse/strata#870, lgse/strata#871).
- The popover slides from the side it opens on, with a 150 ms transition, so entry and exit follow one path (lgse/strata#132).
- The peek list is not focusable, keeping it out of keyboard navigation (lgse/strata#410).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-05 | lgse/strata#1480 | fix | Made folder peeking opt-in and lengthened the hover delay to 1000 ms. |
| 2026-09-12 | lgse/strata#870 | fix | Kept a pending peek alive when a late leave event arrives from the previous folder. |
| 2026-09-03 | lgse/strata#234 | fix | Placed peeks outside the source column and slid them toward the chosen side. |
| 2026-09-01 | lgse/strata#132 | fix | Added depth, aligned the header, and replaced the crossfade with a directional slide. |
| 2026-09-01 | lgse/strata#99 | fix | Persisted the Folder peeking preference across restarts. |

## Known gaps

- Entries appear in enumeration order rather than the browser's sort order, so a large folder peeks an arbitrary subset; the issue closed without a fix. lgse/strata#1449
- Hidden entries are filtered after the 64-entry cap, so a folder whose first 64 enumerated entries are hidden peeks as nearly or fully empty. lgse/strata#1449
