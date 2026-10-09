---
title: Drop copy-or-move policy
status: shipped
origin: {issue: lgse/strata#248, pr: lgse/strata#502}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [src/services/transfer_action.rs, src/adapters/volume.rs]
tests: [src/services/transfer_action/tests.rs, src/adapters/volume/tests.rs, src/adapters/volume/tests/lookup_regressions.rs, tests/e2e/scenarios/test_cross_volume_drop.py]
related: []
---

## Summary

How a drop chooses between copying and moving. Plain drops on the same filesystem move, plain drops onto another device follow the Copy, Move, or Ask strategy, and Ctrl or Shift overrides both.

## Behavior

### Choosing the action

- A plain drop onto a folder on the same filesystem moves the items. lgse/strata#502
- Holding Ctrl at the drop copies and holding Shift moves, on the same or another device. lgse/strata#502
- Settings → General → File transfers → Drag & drop to another device offers Always copy, Always move, and Always ask; Always ask is the default. lgse/strata#502
- With Always copy, a plain drop onto another device copies without a dialog and keeps the source. lgse/strata#502
- With Always move, a plain drop onto another device moves without a dialog. lgse/strata#502
- The drag cursor shows copy or move for the hovered destination before release. lgse/strata#248, lgse/strata#502
- When the dragging application does not offer move, the drop copies. lgse/strata#502 (unverified)

### Copy or move dialog

- With Always ask, a plain drop onto another device opens "Copy or move?" naming the item count and destination, with Copy focused. lgse/strata#502
- The dialog states "The destination is on a different device.", or "Strata could not determine whether the destination is on the same device." when the lookup did not resolve. lgse/strata#502
- Enter activates the focused Copy, Move, or Cancel button. lgse/strata#502
- Cancel, Escape, or the close button transfers nothing. lgse/strata#502
- Copy keeps the source; Move removes it after the transfer. lgse/strata#502

### Volume detection

- A folder reached through a symlink alias of a network mount counts as the same volume as the mount, so plain drops between them move. lgse/strata#761
- Hovering a drag over a destination beneath an autofs mount does not block the UI; its volume is looked up asynchronously. lgse/strata#846
- A drop released while the volume lookup is still pending follows the cross-device strategy. lgse/strata#502
- A volume lookup still unresolved after 2 seconds counts as unknown, so the drop follows the cross-device strategy. lgse/strata#502

## Design

Moving across devices silently removes the only copy from a USB stick or network share, so a cross-device drop needs a safer default (lgse/strata#248). Always moving, always prompting, and copying on the same volume were each rejected there. lgse/strata#502 shipped Always ask as the default with a configurable strategy, superseding lgse/strata#338.

- A volume is a GIO `id::filesystem` plus the URI scheme. Native paths, including network mounts and their symlink aliases, share the `file` namespace; other URI backends stay distinct (lgse/strata#734, lgse/strata#761).
- The destination is compared with each source's parent folder, or with the source itself when it is a mount point. Any unresolved identity makes the relation unknown, which follows the cross-device strategy but is never described as a confirmed device difference (lgse/strata#502).
- Blocking risk is kept separate from identity. Ordinary local paths resolve on the GTK thread; remote, symlinked, and autofs paths are queried asynchronously with a 2-second timeout (lgse/strata#732, lgse/strata#846).
- The timeout exists because cancelling cannot unblock a stat already stuck on a dead mount. Autofs scheduling alone never declares two filesystems different (lgse/strata#846).
- One classification per hovered destination drives both the cursor and the committed transfer, so the dialog matches the feedback shown (lgse/strata#502).
- Cut and Paste is unaffected by this policy (lgse/strata#502).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-12 | lgse/strata#846 | fix | Detected autofs ancestors from mountinfo so drop volume lookups beneath them run off the GTK thread. |
| 2026-09-10 | lgse/strata#761 | fix | Compared volumes by GIO backend instead of lexical remoteness, so network-mount aliases count as one volume. |

## Known gaps

None known.
