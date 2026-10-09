---
title: Directory loading and monitoring
status: shipped
origin: {issue: lgse/strata#137, pr: lgse/strata#154}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [src/app/browser/loading.rs, src/app/browser/loading/metadata.rs, src/app/browser/directory_changes.rs, src/app/browser/publication.rs, src/app/browser/deferred.rs, src/app/browser/operation_updates.rs, src/app/browser/operation_events.rs]
tests: [src/app/browser/loading/tests.rs, src/app/browser/loading/metadata/tests.rs, src/app/browser/directory_changes/tests.rs, src/app/browser/publication/tests.rs, src/app/browser/deferred/tests.rs, src/app/browser/operation_updates/tests.rs, src/app/browser/tests/monitor.rs]
docs: [docs/performance-baseline.md]
related: [browser/selection, browser/view-modes, operations/progress, operations/trash, browser/navigation/recent, remote/file-providers/network-locations]
---

## Summary

How an open folder's listing is loaded, published to the view, and kept in step with the filesystem. Covers bounded loads, live updates from file monitors, F5 and the pane Refresh button, the auto-refresh timer, and how changes made by Strata's own file operations reach the listing.

## Behavior

### Loading

- A folder load stops at 100,000 entries or 10 seconds; the pane header then shows a warning icon described "This directory has more entries than could be loaded; showing a partial listing." lgse/strata#154
- Refreshing or navigating away while a folder is loading discards the rows still arriving for the old request; they never appear in the new listing. lgse/strata#593
- A load that fails discards its staged rows and shows the error instead of a partial listing. lgse/strata#593 (unverified)
- An SMB or other GVfs folder whose entries lack `standard::is-hidden` or `standard::is-symlink` loads them as not hidden and not symlinks, without GLib critical warnings. lgse/strata#74
- Alternating dozens of times between a folder of several hundred files and a small folder keeps load time flat instead of slowing with each switch. lgse/strata#1187, lgse/strata#1353

### Row publication

- A folder of up to 512 entries is shown in one update; a larger one shows its first 128 rows at once and adds the rest after each redraw. lgse/strata#601 (unverified)
- Selection restoration and the end of the loading indicator wait until the last row of a staged load is shown. lgse/strata#601

### Live external changes

- Files created, deleted, renamed, or modified by another program appear, disappear, or update in the open folder within about 100 ms, without F5. lgse/strata#803 (unverified)
- A file modified in place whose sort position is unchanged keeps its row; the row is updated without the appear animation. lgse/strata#803
- A temporary file created and then renamed to its target within one 100 ms batch appears once, under the target name. lgse/strata#803
- With hidden files off, changes to dot-files are ignored, and a dot-file renamed to a visible name appears as a new entry. lgse/strata#1266 (unverified)
- More than 4,096 pending changes in one batch, an unmount, or an unrecognized monitor event reload the whole folder instead. lgse/strata#75, lgse/strata#1266 (unverified)
- Files created, renamed, or removed externally while a large folder is still loading are not overridden by late enumeration rows. lgse/strata#1037
- Renaming an open folder externally in Columns re-points its column and every open descendant to the new path. lgse/strata#1036, lgse/strata#1037
- Deleting an open folder externally in Columns closes its column and every descendant column. lgse/strata#1036, lgse/strata#1037
- URI locations such as `trash:///` and mounted GVfs shares receive live changes through GIO monitors. lgse/strata#463

### Manual refresh and auto-refresh

- F5 reloads every open column in Columns, and the active pane in Icons and List. lgse/strata#173, lgse/strata#393
- Each pane header has a Refresh button, tooltip "Refresh (F5)", that reloads only that pane. lgse/strata#173 (unverified)
- Settings → General → Performance → "Auto-refresh folder" offers Off, 1 min, 5 min, and 10 min, saved as `auto_refresh_interval` = 0, 60, 300, or 600. lgse/strata#173
- With an interval set, each tick runs the same reload as F5; Off stops the timer. lgse/strata#173
- An auto-refresh tick is skipped while a new item is being named or a rename is in progress. lgse/strata#567 (unverified)

### Changes from Strata's own operations

- While a delete, restore, copy, or move runs, monitor changes for open folders are held back instead of applied one by one. lgse/strata#1036
- Once 512 changes are held, the next progress update applies them, so completed files appear during a bulk transfer without a reload. lgse/strata#1266 (unverified)
- When the operation finishes, the held changes apply in one batch per folder, parent folders before their children. lgse/strata#1036
- If a monitor asked for a full reload during the operation, that folder reloads after the progress dialog closes, keeping its rows on screen until the new listing replaces them. lgse/strata#1266, lgse/strata#1036
- Non-native locations, such as SFTP folders, reload after a rename, create, or paste that touches them. lgse/strata#1035 (unverified)

## Design

Loading and file monitoring predate the PR history; the original monitor already watched moves and coalesced events per path. [docs/architecture.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/architecture.md) documents directory-event routing and staged publication. [docs/performance-baseline.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/performance-baseline.md) carries the 100,000-entry fixtures and load timings.

- An unbounded load of 200,000 entries froze the UI for minutes (lgse/strata#137). The 100,000-entry and 10-second caps match the published baseline, past which per-batch merging stops feeling responsive (lgse/strata#154).
- Native folders are enumerated off the GTK thread, staged, and published after redraw in bounded slices; remote folders keep a first-batch-then-coalesced path (lgse/strata#274, lgse/strata#593).
- Publication tails run at idle priority 130, after GDK redraw (120) and before default idle (200), within 8 ms slices. Chunks start at 512 rows and adapt between 128 and 2,048 against a 12 ms budget (lgse/strata#601).
- Before a live change or operation batch splices rows, any unpublished tail is drained, so positional updates always land on rows the view already has (lgse/strata#1037).
- Monitor events are debounced for 100 ms and keyed by location. A burst past the cap collapses to one rescan rather than thousands of splices (lgse/strata#75); lgse/strata#1266 raised the cap from 256 to 4,096.
- Background changes emit selection updates without taking focus, so scrolling is not reset by a busy folder such as `/tmp` (lgse/strata#767, lgse/strata#803).
- Changes are held during delete, restore, and transfer operations so the listing does not churn per item. Rescan requests run once, after progress closes, as a refresh that keeps existing rows (lgse/strata#1036, lgse/strata#1266).
- After Strata's own operations, native folders rely on their monitor and only non-native locations reload, avoiding needless reloads (lgse/strata#1035).
- Auto-refresh exists because monitors can miss changes on network shares or after errors (lgse/strata#172). It defaults to Off.
- lgse/strata#173 also bound Ctrl+R to refresh. lgse/strata#393 gave Ctrl+R to Rename, leaving F5 as the only refresh key.
- Retired views once stayed alive through autoscroll, menu, and preference-listener cycles, so each folder switch added work (lgse/strata#1185, lgse/strata#1187, lgse/strata#1353).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-16 | lgse/strata#1054 | refactor | Separated deferred metadata, sort, and publication cleanup; released a borrow that panicked when a sorting column closed. |
| 2026-09-15 | lgse/strata#1037 | refactor | Separated live directory-change routing into staging, queueing, path reconciliation, and publication. |
| 2026-09-15 | lgse/strata#1036 | refactor | Separated the deferred file-operation update policy from state updates and publication. |
| 2026-09-15 | lgse/strata#1035 | refactor | Split the operation-event callback into context, progress, completion, undo, and outcome steps. |
| 2026-09-11 | lgse/strata#803 | fix | Stopped background changes from resetting scroll, updated unchanged-position rows in place, and coalesced atomic writes. |
| 2026-09-08 | lgse/strata#601 | refactor | Moved staged row publication into its own module with an owned publication plan. |
| 2026-09-08 | lgse/strata#593 | refactor | Separated directory-event and metadata routing from the browser controller. |
| 2026-09-03 | lgse/strata#173 | feat | Added F5, the Refresh button, and an optional auto-refresh interval for when monitors miss changes. |
| 2026-09-02 | lgse/strata#154 | fix | Capped folder loads at 100,000 entries or 10 seconds and flagged partial listings. |
| 2026-08-31 | lgse/strata#74 | fix | Guarded optional GFileInfo attributes so GVfs listings no longer log critical warnings. |

## Known gaps

- An `auto_refresh_interval` other than 0, 60, 300, or 600 runs its timer while Settings shows "Off"; the fix is unmerged. lgse/strata#1456, lgse/strata#1544
- A pane filter's results do not follow files created or deleted outside Strata; the fix is unmerged. lgse/strata#1439, lgse/strata#1544
- A metadata-only change replaces the whole row, rebinding its icon or thumbnail, instead of updating the changed labels. lgse/strata#902
