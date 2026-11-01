---
title: External file providers
status: shipped
origin: {issue: lgse/strata#1356, pr: lgse/strata#1385}
branch: null
reviewed_at: 86df474dc0e8352e0e2098637a017cc4c77a8c44
review: reviewed
code: [src/services/file_providers.rs, src/services/file_providers, src/ui/file_providers.rs, src/ui/file_providers]
tests: [src/services/file_providers/tests.rs, src/services/file_providers/transport/tests.rs, src/ui/file_providers/tests.rs, tests/qa/scenarios/file_providers]
docs: [site/src/reference/file-providers.md, docs/file-providers.md]
related: [integration/custom-actions, browser/thumbnails, operations/clipboard/send-to, remote/file-providers/integrations, remote/file-providers/kde-connect, remote/file-providers/localsend]
---

## Summary

Opt-in, trusted programs that add live status badges, state-dependent context actions, and Send to… destinations to native files, such as cloud offline availability or a phone. Strata talks to each provider over a newline-delimited JSON protocol; Cirrove is the first adapter. Bundled providers install from `remote/file-providers/integrations`.

## Behavior

### Registration

- A provider registers as `<id>/provider.json` under `$XDG_CONFIG_HOME/strata/providers/`, default `~/.config/strata/providers/`, and loads at startup. lgse/strata#1385
- Refresh on Settings → Integrations, or a successful install, update, removal, or switch change there, rediscovers the registrations without a restart. Other edits apply on restart. lgse/strata#1748
- That reload stops every provider at once, except one still owing an answer to an activation, and discards pending queries and menus. lgse/strata#1748, lgse/strata#1878
- During that reload, badges clear until the new providers answer. lgse/strata#1748 (unverified)
- A registration directory holding a file named `disabled` beside `provider.json` is skipped, so its badges and actions do not load. lgse/strata#1748
- A registration whose directory, manifest, or icon is a symlink, is group- or world-writable, or is owned by neither the user nor root is rejected. The executable gets the same ownership and permission check after its symlinks are resolved. lgse/strata#1385
- A manifest whose `id` differs from its directory name, or whose command does not start with an absolute executable, is rejected; no shell or PATH lookup runs. lgse/strata#1385
- At most 8 providers load, from at most 64 directory entries, one child process each. After a reload, a retiring child runs beside its replacement. lgse/strata#1385, lgse/strata#1878
- Icons are PNG files beside the manifest, at most 16, each at most 64 KiB and 256×256. lgse/strata#1385
- A manifest `icon` that names no entry in its `icons` rejects the registration; an absent or `null` `icon` is accepted. lgse/strata#1578 (unverified)

### Badges

- A `query` reply's badge appears on the file's icon in Columns, List, and Icons; an omitted path or `badge: null` draws none. lgse/strata#1385
- When several providers badge one file, the highest `priority` wins, ties going to the lexically first provider id. lgse/strata#1385
- A badge has no tooltip; its accessible description lists every contributing provider's id and text. lgse/strata#1385

### Menus

- Item and background menus show each provider's root actions that are not placed in Send to… in an inline section. Its muted heading shows the registered `name`, or the id. lgse/strata#1385, lgse/strata#1742
- A manifest `icon` is drawn before that heading's name in item and background menus, and on the provider's Send to… submenu or entry; a provider without one keeps the native section title. lgse/strata#1578, lgse/strata#1704
- A background menu sends the current folder as the only path. lgse/strata#1385
- An empty `actions` reply shows neither the section nor its heading. lgse/strata#1385
- A selection over 200 items, or one whose path list exceeds the frame budget, shows no provider actions. lgse/strata#1385
- Paths that are not native or not valid UTF-8 are never sent to a provider. lgse/strata#1385
- Only leaves activate; branches are submenus, at most 64 nodes and four levels deep. lgse/strata#1385
- While a menu is open, a refresh updates labels in place, keeps an open submenu open, and disables withdrawn leaves before removing them. lgse/strata#1385

### Send to…

- In an item menu, a root action with `"placement": "send-to"` appears under Send to… ▸ <provider name> ▸ <label> instead of in the provider's section. lgse/strata#1742, lgse/strata#1704
- Root actions without a placement in the same reply stay in the provider's section, so the section and the Send to… submenu both appear. lgse/strata#1742
- A `placement` on a child action is ignored; the child stays inside its parent. lgse/strata#1742
- In a background menu, or any menu without Send to…, a `send-to` or `send-to-entry` root action stays in the provider's section. lgse/strata#1742, lgse/strata#1756
- An unrecognized `placement` string such as `"float-to-top"`, or `null`, keeps the action in the provider's section. lgse/strata#1742
- A `placement` that is neither a string nor `null`, such as `7`, is an invalid frame and disconnects the provider. lgse/strata#1742 (unverified)
- A placed destination may have `children` within the 64-node, four-level bounds; its leaves activate with the whole selection, the action id, and `context`, with unchanged `feedback` handling. lgse/strata#1742
- A provider's Send to… submenu without a manifest `icon` shows its `category` icon: `cloud` a cloud, `devices` a phone, `version-control` a git branch, and `other`, absent, or unknown a blocks icon. lgse/strata#1704
- An `_` in a provider's name shows literally in its Send to… submenu label instead of marking a mnemonic. lgse/strata#1704 (unverified)
- A provider with one root action placed `"send-to-entry"` and no `children` shows that leaf directly in Send to… with its own label. It shows its own `icon`, else the provider's manifest icon, else its category icon. lgse/strata#1756
- A `send-to-entry` action with `children`, or beside another Send to… action from the same provider, joins that provider's Send to… submenu. lgse/strata#1756
- A provider submenu that holds one `send-to` destination stays a submenu. lgse/strata#1756
- When a refresh turns a single Send to… entry into a submenu, or back, the old item is removed. The new one takes its place in the open menu. lgse/strata#1756 (unverified)

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
- When a reload interrupts a pending activation, the provider keeps running until it replies. Its notice or dialog then appears, as for a live activation; a reply with no feedback shows nothing. lgse/strata#1878
- If that retiring provider exits or goes offline first, the sent action shows the "may already have been accepted" dialog. A still-queued one shows "was not sent". lgse/strata#1878
- A retiring provider's process ends once every activation it owes is settled; no wall-clock cutoff applies beyond the 8-second request timeout. lgse/strata#1878
- After a retiring provider replies, a running provider with the same id has its cached answers invalidated, as after a live activation reply. lgse/strata#1878
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

[docs/file-providers.md](https://github.com/lgse/strata/blob/be3343a5992a2a5497b1a2ee7faa525be18e988f/docs/file-providers.md) is the protocol 1 specification: registration, transport, methods, Send to… placement, activation feedback, revisions, bounds, and failure handling (lgse/strata#1742, lgse/strata#1704, lgse/strata#1756, lgse/strata#1878).

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
- A reload retires a provider owing an activation instead of dropping it. Dropping its client stopped the worker reading, so the reply never matched and nothing appeared (lgse/strata#1857, lgse/strata#1878).
- Retiring has no time cutoff. The 8-second request timeout already settles every waiting action, and a cutoff would end queued activations silently (lgse/strata#1878).
- Caches hold at most 2,048 path answers and 32 menu selections per provider, and track at most 1,024 mapped thumbnail slots (lgse/strata#1385).
- Discovery runs at startup and again on each reload from Settings → Integrations, never by watching the providers directory. With no providers found and none retiring, the hub's 100 ms timer stops and thumbnail slots go untracked. The hub then no longer wakes an idle window. A reload restarts the timer (lgse/strata#1671, lgse/strata#1677, lgse/strata#1748, lgse/strata#1878).
- Some integrations are destinations. A heading section duplicated Send to… and forced label suffixes such as "via KDE Connect", so placed actions sit beside removable drives with bare labels (lgse/strata#1740).
- `placement` is additive with no handshake: older hosts ignore it, and unknown values keep the section. A dedicated Send to… method or device-list reply was rejected as more host code and a second tree model (lgse/strata#1740, lgse/strata#1742).
- Each provider's destinations sit in a submenu named after it, like a removable drive (lgse/strata#1704).
- The provider chooses between one Send to… entry and a submenu; Strata never collapses a submenu itself (lgse/strata#1756).
- Providers must answer from cached service state and never download content to draw a badge or menu. Strata cannot enforce this (lgse/strata#1385).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-25 | lgse/strata#1878 | fix | Kept a provider owing an activation answer running through a Refresh, so the action's notice or dialog still appears. |
| 2026-10-18 | lgse/strata#1704 | feat | Added the KDE Connect integration and gave each provider's Send to… destinations their own submenu with its icon or category icon. |
| 2026-10-18 | lgse/strata#1742 | feat | Let providers place root actions inside Send to… with `placement: "send-to"`, so destinations sit beside removable drives. |
| 2026-10-15 | lgse/strata#1677 | perf | Stopped the 100 ms hub timer and slot tracking once discovery finds no providers, so the provider hub stops waking an idle window. |
| 2026-10-11 | lgse/strata#1578 | feat | Let providers choose dialog, notice, or no feedback for accepted activations, and show a manifest icon before the menu heading. |
| 2026-10-07 | lgse/strata#1385 | feat | Added opt-in external providers for live badges and context actions, with Cirrove as the first adapter. |

## Known gaps

- Remote-only locations and non-UTF-8 filenames get no provider badges or actions. lgse/strata#1385
