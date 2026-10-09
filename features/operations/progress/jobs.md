---
title: Job queue and Jobs dashboard
status: shipped
origin: {issue: lgse/strata#36, pr: lgse/strata#1085}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [src/services/jobs.rs, src/ui/jobs.rs, src/adapters/local_jobs.rs]
tests: [src/services/jobs/tests.rs, src/ui/jobs/tests.rs, src/adapters/local_jobs/tests.rs, src/adapters/local_jobs/tests/lifecycle.rs]
docs: [docs/custom-actions.md]
related: [integration/custom-actions]
---

## Summary

The background queue that runs custom actions, and the Jobs dashboard in the footer that shows it. Jobs are shared by every window, survive navigation, and stay in a session history after they finish.

## Behavior

### Queue

- At most 2 jobs run at once; later jobs wait as Queued and start when a slot frees. lgse/strata#1085
- A per-item job runs one input at a time; a whole-selection job runs once with every input. lgse/strata#1085
- With `on_error = "stop"`, a per-item job ends at its first failure; otherwise it continues and reports how many items failed. lgse/strata#1085
- An invocation succeeds only when its process exits with status 0; a reported 100% does not count as success. lgse/strata#1085
- Up to 20 finished jobs are kept; the oldest finished jobs are evicted first, and active jobs are never evicted. lgse/strata#1085 (unverified)
- Each invocation keeps the newest 8 KiB of its output, prefixed with "…" when trimmed; a job keeps the newest 64 KiB across invocations. lgse/strata#1085 (unverified)

### Cancellation

- Remove on a queued job ends it as Cancelled with "Removed before starting", without running it. lgse/strata#1085
- Cancel on a running job shows "Cancelling…" and sends SIGTERM to its process group, then SIGKILL after 2 seconds. lgse/strata#1085
- A job still cancelling after 10 seconds is marked Cancelled with "Cancelled; the action did not stop cleanly", freeing its slot. lgse/strata#1085 (unverified)
- Closing the last application window while jobs are queued, running, or cancelling shows "Background jobs are still active" and keeps it open; other windows close. lgse/strata#1085

### Dashboard

- The footer shows a Jobs button only when jobs exist: it reads "2 jobs running · 1 queued", otherwise "3 jobs finished", with "· failures" when any failed. lgse/strata#1085
- Launching an action opens Jobs in the launching window with the new job first. lgse/strata#1085
- Minimize, Escape, or a click outside hides the dashboard without cancelling jobs; progress updates do not reopen it. lgse/strata#1085
- A row shows the action name and icon, a status with elapsed time ("Running for", "Done in", "Failed after", "Cancelled after"), item counts, and the invoking folder. lgse/strata#1085
- An active whole-selection job whose script reports no total shows a pulsing progress bar instead of a percentage. lgse/strata#1085
- An active per-item job's bar fills by completed items plus the current item's reported fraction. lgse/strata#1085 (unverified)
- Details expands a job's captured output and Hide collapses it; a job with no output shows "No output yet.". lgse/strata#1085
- Details on a running job shows output as it arrives, follows the bottom until scrolled up, and follows again once scrolled back down. lgse/strata#1274
- Terminal colour and control sequences are stripped from the shown output. lgse/strata#1274
- Dismiss removes one finished job; Clear finished removes every finished job and leaves active ones. lgse/strata#1085
- The dashboard lists at most 12 jobs, then shows "<n> older jobs are hidden". lgse/strata#1085 (unverified)

## Design

[docs/custom-actions.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/custom-actions.md) "Jobs and cancellation" carries the user contract. The dashboard design was agreed in lgse/strata#36.

- Job state is application-owned and observed by each window's footer, not owned by a menu, dashboard, or browser view. Navigating or closing that UI never cancels work (lgse/strata#36).
- `services::jobs` owns the queue, per-item iteration, progress, cancellation bookkeeping, bounded logs, and history. `adapters::local_jobs` starts one invocation as a child process, and `ui/jobs.rs` only observes ([docs/architecture.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/architecture.md)).
- Cancel is its own control. Minimize, Escape, and outside clicks only hide, unlike the browser's progress dialog, where Escape cancels (lgse/strata#36).
- Percentages are never invented. Scripts without progress show elapsed time and an indeterminate bar, and exit status decides success (lgse/strata#36).
- History is bounded and session-local. There is no pause, resume, restart, or automatic retry of possibly destructive work (lgse/strata#36).
- A cancelling job keeps its slot until its process exits or the 10-second deadline passes, so cancelling never admits a third job early (lgse/strata#1085).
- Copy, move, and archive operations were left to a later migration (lgse/strata#36). lgse/strata#1393 gave them the progress dock instead of Jobs.

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-26 | lgse/strata#1274 | feat | Showed custom-action output live in Details, following the bottom until scrolled up. |

## Known gaps

- Per-item invocations run one at a time; parallel per-item runs, restart, and resume were deferred from the first release. lgse/strata#36, lgse/strata#1085
