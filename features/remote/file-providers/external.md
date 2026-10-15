---
title: External file providers
status: shipped
origin: {issue: lgse/strata#1356, pr: lgse/strata#1385}
branch: null
reviewed_at: 027d6981a69ea7b526a763d3ec563fdecb19c66b
review: draft
code: [src/services/file_providers.rs, src/services/file_providers, src/ui/file_providers.rs, src/ui/file_providers]
tests: [src/services/file_providers/tests.rs, src/services/file_providers/transport/tests.rs, src/ui/file_providers/tests.rs, tests/e2e/scenarios/test_file_providers.py]
docs: [site/src/reference/file-providers.md]
related: [integration/custom-actions, browser/thumbnails]
---

## Summary

Opt-in, trusted programs that add live status badges and state-dependent context actions to native files, such as cloud offline availability. Strata talks to each provider over a newline-delimited JSON protocol; Cirrove is the first adapter.

## Behavior

### Registration

- A provider registers as `<id>/provider.json` under `$XDG_CONFIG_HOME/strata/providers/`, default `~/.config/strata/providers/`, and loads at startup; edits and removals apply on restart. lgse/strata#1385
- A registration whose directory, manifest, or icon is a symlink, is group- or world-writable, or is owned by neither the user nor root is rejected. The executable gets the same ownership and permission check after its symlinks are resolved. lgse/strata#1385
- A manifest whose `id` differs from its directory name, or whose command does not start with an absolute executable, is rejected; no shell or PATH lookup runs. lgse/strata#1385
- At most 8 providers load, from at most 64 directory entries, one child process each. lgse/strata#1385
- Icons are PNG files beside the manifest, at most 16, each at most 64 KiB and 256×256. lgse/strata#1385
- A manifest `icon` that names no entry in its `icons` rejects the registration; an absent or `null` `icon` is accepted. lgse/strata#1578 (unverified)

### Badges

- A `query` reply's badge appears on the file's icon in Columns, List, and Icons; an omitted path or `badge: null` draws none. lgse/strata#1385
- When several providers badge one file, the highest `priority` wins, ties going to the lexically first provider id. lgse/strata#1385
- A badge has no tooltip; its accessible description lists every contributing provider's id and text. lgse/strata#1385

### Menus

- Item and background menus show each provider's actions in an inline section under a muted heading with its registered `name`, or its id. lgse/strata#1385
- A manifest `icon` is drawn before that heading's name in item and background menus; a provider without one keeps the native section title. lgse/strata#1578
- A background menu sends the current folder as the only path. lgse/strata#1385
- An empty `actions` reply shows neither the section nor its heading. lgse/strata#1385
- A selection over 200 items, or one whose path list exceeds the frame budget, shows no provider actions. lgse/strata#1385
- Paths that are not native or not valid UTF-8 are never sent to a provider. lgse/strata#1385
- Only leaves activate; branches are submenus, at most 64 nodes and four levels deep. lgse/strata#1385
- While a menu is open, a refresh updates labels in place, keeps an open submenu open, and disables withdrawn leaves before removing them. lgse/strata#1385

### Activation

- Activating a leaf sends the whole selection, the action id, and its `context` token unchanged. lgse/strata#1385
- Unless an accepted reply requests `notice` or `none`, a "File availability" dialog shows the provider id, status, accepted/total counts, job reference, and message. lgse/strata#1385, lgse/strata#1578
- An `accepted` reply with `feedback` `notice` opens no dialog. A progress-dock notice shows the provider's `name`, or its id, and the message for about 4 seconds. lgse/strata#1578
- An `accepted` reply with `feedback` `none` shows no dialog and no notice. lgse/strata#1578
- `feedback` `notice` or `none` on a `rejected`, `partial`, or `unknown` outcome, or on a reply without `outcome`, still opens the dialog. lgse/strata#1578
- `feedback` `dialog`, an omitted `feedback`, or an unrecognized string such as `"future-style"` opens the dialog. lgse/strata#1578
- A `feedback` that is neither a string nor `null` is an invalid frame and disconnects the provider. So does `feedback` on a `query`, `menu`, or `error` reply or an `invalidate` event. lgse/strata#1578 (unverified)
- An `unknown` outcome shows its counts as "at least N/M accepted". lgse/strata#1385
- If the provider disconnects after an action was sent, the dialog says it may already have been accepted; an unsent action says it was not sent. lgse/strata#1385
- When the provider's queue is full, the dialog says the provider is busy or unavailable and the action was not sent. lgse/strata#1385
- No action is retried automatically, including after a lost reply. lgse/strata#1385
- After an activation reply, Strata re-queries that provider's visible badges and open menus. lgse/strata#1385 (unverified)

### Freshness and failures

- An `invalidate` event refreshes the affected badges and menus; unchanged answers stay visible meanwhile. lgse/strata#1385
- Answers refresh after 5 seconds and expire after 15 seconds if not replaced. lgse/strata#1385
- A reply older than an overlapping invalidation's `revision` is rejected. lgse/strata#1385
- A request unanswered for 8 seconds, an invalid frame, or a reply frame over 1 MiB disconnects the provider and withdraws its badges and actions. lgse/strata#1385
- After a disconnect, the provider restarts on its next request once a 2-second backoff has passed. lgse/strata#1385
- A method `error` reply withdraws that presentation without disconnecting the provider. lgse/strata#1385

## Design

[docs/file-providers.md](https://github.com/lgse/strata/blob/0562724ad97c8e83a4c81b85e556bf275be3b025/docs/file-providers.md) is the protocol 1 specification: registration, transport, methods, activation feedback, revisions, bounds, and failure handling.

- Static custom actions cannot express live eligibility or badges; they would appear for unrelated files and fail only after activation (lgse/strata#1356).
- Embedding a cloud client was rejected as coupling Strata to one project. Strata has no provider-specific code (lgse/strata#1356).
- Providers are trusted programs with the user's permissions, not sandboxes. They are never discovered in browsed folders, and artwork loads only from trusted configuration (lgse/strata#1356, lgse/strata#1385).
- No provider socket or process I/O runs on the GTK thread. Each connection carries one request at a time; 16 query/menu requests and 8 activations queue separately, and activations dispatch first (lgse/strata#1385).
- Menus and activations describe the whole selection, never a filtered subset. Adapters bind `context` to identities and must revalidate on activation (lgse/strata#1385).
- Scoped, monotonic revisions order snapshots against invalidations, so activity in one account does not discard valid replies for another (lgse/strata#1385).
- Feedback is chosen per reply, not in Settings: a preference applies to every action and cannot tell "Share..." from "Copy link" (lgse/strata#1577).
- Only a fully accepted outcome may skip the dialog, so problems are never hidden. The field is additive: older hosts ignore it, and unknown values fall back to the dialog (lgse/strata#1577, lgse/strata#1578).
- Without an ancestor overlay, a notice falls back to the dialog (lgse/strata#1578).
- GTK section titles cannot hold an image, so a heading icon replaces the title with a custom row styled like one (lgse/strata#1578).
- Unsent and uncertain actions are reported differently. A disconnect after submission is not proof that nothing happened, so nothing is replayed (lgse/strata#1385).
- Caches hold at most 2,048 path answers and 32 menu selections per provider, and track at most 1,024 mapped thumbnail slots (lgse/strata#1385).
- Discovery runs once per process. When it finds no providers, the hub's 100 ms timer stops and thumbnail slots are no longer tracked, so an idle window stays idle (lgse/strata#1671, lgse/strata#1677).
- Providers must answer from cached service state and never download content to draw a badge or menu. Strata cannot enforce this (lgse/strata#1385).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-15 | lgse/strata#1677 | perf | Stopped the 100 ms hub timer and slot tracking once discovery finds no providers, so an idle window can stop waking. |
| 2026-10-11 | lgse/strata#1578 | feat | Let providers choose dialog, notice, or no feedback for accepted activations, and show a manifest icon before the menu heading. |
| 2026-10-07 | lgse/strata#1385 | feat | Added opt-in external providers for live badges and context actions, with Cirrove as the first adapter. |

## Known gaps

- Remote-only locations and non-UTF-8 filenames get no provider badges or actions. lgse/strata#1356
