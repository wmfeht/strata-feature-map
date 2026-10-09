---
title: External file providers
status: shipped
origin: {issue: lgse/strata#1356, pr: lgse/strata#1385}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [src/services/file_providers.rs, src/services/file_providers, src/ui/file_providers.rs, src/ui/file_providers]
tests: [src/services/file_providers/tests.rs, src/services/file_providers/transport/tests.rs, src/ui/file_providers/tests.rs, tests/e2e/scenarios/test_file_providers.py]
docs: [docs/file-providers.md]
related: [integration/custom-actions, browser/thumbnails]
---

## Summary

Opt-in, trusted programs that add live status badges and state-dependent context actions to native files, such as cloud offline availability. Strata talks to each provider over a newline-delimited JSON protocol; Cirrove is the first adapter.

## Behavior

### Registration

- A provider registers as `<id>/provider.json` under `$XDG_CONFIG_HOME/strata/providers/`, default `~/.config/strata/providers/`, and loads at startup; edits and removals apply on restart. lgse/strata#1385
- A registration whose directory, manifest, or icon is a symlink, is group- or world-writable, or is owned by neither the user nor root is rejected. lgse/strata#1385
- A manifest whose `id` differs from its directory name, or whose command does not start with an absolute executable, is rejected; no shell or PATH lookup runs. lgse/strata#1385
- At most 8 providers load, from at most 64 directory entries, one child process each. lgse/strata#1385
- Icons are PNG files beside the manifest, at most 16, each at most 64 KiB and 256×256. lgse/strata#1385

### Badges

- A `query` reply's badge appears on the file's icon in Columns, List, and Icons; an omitted path or `badge: null` draws none. lgse/strata#1385
- When several providers badge one file, the highest `priority` wins, ties going to the lexically first provider id. lgse/strata#1385
- A badge has no tooltip; its accessible description lists every contributing provider's id and text. lgse/strata#1385

### Menus

- Item and background menus show each provider's actions in an inline section under a muted heading with its registered `name`, or its id. lgse/strata#1385
- A background menu sends the current folder as the only path. lgse/strata#1385
- An empty `actions` reply shows neither the section nor its heading. lgse/strata#1385
- A selection over 200 items, or one whose path list exceeds the frame budget, shows no provider actions. lgse/strata#1385
- Paths that are not native or not valid UTF-8 are never sent to a provider. lgse/strata#1385
- Only leaves activate; branches are submenus, at most 64 nodes and four levels deep. lgse/strata#1385
- While a menu is open, a refresh updates labels in place, keeps an open submenu open, and disables withdrawn leaves before removing them. lgse/strata#1385

### Activation

- Activating a leaf sends the whole selection, the action id, and its `context` token unchanged. lgse/strata#1385
- The reply appears in a "File availability" dialog prefixed with the provider id, with status, accepted/total counts, job reference, and message. lgse/strata#1385
- An `unknown` outcome shows its counts as "at least N/M accepted". lgse/strata#1385
- If the provider disconnects after an action was sent, the dialog says it may already have been accepted; an unsent action says it was not sent. lgse/strata#1385
- When the provider's queue is full, the dialog says the provider is busy or unavailable and the action was not sent. lgse/strata#1385
- No action is retried automatically, including after a lost reply. lgse/strata#1385

### Freshness and failures

- An `invalidate` event refreshes the affected badges and menus; unchanged answers stay visible meanwhile. lgse/strata#1385
- Answers refresh after 5 seconds and expire after 15 seconds if not replaced. lgse/strata#1385
- A reply older than an overlapping invalidation's `revision` is rejected. lgse/strata#1385
- A request unanswered for 8 seconds, an invalid frame, or excess output disconnects the provider, withdraws its badges and actions, and restarts it after 2 seconds. lgse/strata#1385
- A method `error` reply withdraws that presentation without disconnecting the provider. lgse/strata#1385

## Design

[docs/file-providers.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/file-providers.md) is the protocol 1 specification: registration, transport, methods, revisions, bounds, and failure handling.

- Static custom actions cannot express live eligibility or badges; they would appear for unrelated files and fail only after activation (lgse/strata#1356).
- Embedding a cloud client was rejected as coupling Strata to one project. Strata has no provider-specific code (lgse/strata#1356).
- Providers are trusted programs with the user's permissions, not sandboxes. They are never discovered in browsed folders, and artwork loads only from trusted configuration (lgse/strata#1356, lgse/strata#1385).
- No provider socket or process I/O runs on the GTK thread. Each connection carries one request at a time; 16 query/menu requests and 8 activations queue separately, and activations dispatch first (lgse/strata#1385).
- Menus and activations describe the whole selection, never a filtered subset. Adapters bind `context` to identities and must revalidate on activation (lgse/strata#1385).
- Scoped, monotonic revisions order snapshots against invalidations, so activity in one account does not discard valid replies for another (lgse/strata#1385).
- Unsent and uncertain actions are reported differently. A disconnect after submission is not proof that nothing happened, so nothing is replayed (lgse/strata#1385).
- Caches hold at most 2,048 path answers and 32 menu selections per provider, and track at most 1,024 mapped thumbnail slots (lgse/strata#1385).
- Providers must answer from cached service state and never download content to draw a badge or menu. Strata cannot enforce this (lgse/strata#1385).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-07 | lgse/strata#1385 | feat | Added opt-in external providers for live badges and context actions, with Cirrove as the first adapter. |

## Known gaps

- Remote-only locations and non-UTF-8 filenames get no provider badges or actions. lgse/strata#1356
