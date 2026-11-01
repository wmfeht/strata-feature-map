---
title: Drag folders to pin
status: shipped
origin: {issue: lgse/strata#1690, pr: lgse/strata#1692}
branch: null
reviewed_at: 44bfeab305cfb68993bafcf4794fe0bbf7ff1433
review: reviewed
code: [src/ui/window/pinned_drop.rs, src/adapters/directory_validation.rs]
tests: [src/ui/window/pinned_drop/tests.rs, src/adapters/directory_validation/tests.rs, tests/qa/scenarios/sidebar_pinning/folder-pins-order-and-bookmarks.jsonl, tests/qa/scenarios/sidebar_pinning/foreign-folder-drags-validate.jsonl, tests/qa/scenarios/sidebar_pinning/pinned-rows-transfer-and-remote-gaps.jsonl, tests/qa/scenarios/sidebar_pinning/spring-loaded-rows-keep-pin-intent.jsonl, tests/qa/scenarios/sidebar_reordering/pin-insertion-keeps-one-destination.jsonl]
related: [operations/drag-and-drop, integration/portal-file-chooser, browser/sidebar]
---

## Summary

Insertion gaps in the sidebar's PINNED section. Dragging folders from Strata or another file manager into a gap pins them there, and dragging a pinned row into a gap moves it. Row bodies stay file-transfer targets.

## Behavior

### Pinning by drag

- Dragging folders from Columns, Icons, or List into a PINNED gap pins them at that gap, in selection order. The pins survive a restart. lgse/strata#1690, lgse/strata#1692
- Gaps sit before the first pin, between pins, after the last pin, and in an empty section. lgse/strata#1690, lgse/strata#1692
- Dropping an already pinned folder into a gap adds no duplicate and leaves the order unchanged. lgse/strata#1690, lgse/strata#1692
- A multi-folder drag that includes pinned folders, Home, or standard folders adds only the others, in selection order. lgse/strata#1690
- Dragging a file, or a selection mixing files and folders, over a gap shows no insertion line, and releasing it pins and transfers nothing. lgse/strata#1692
- Holding Shift during a drag from Strata still pins the folder and moves nothing. lgse/strata#1692
- A Move-only drag from another application is rejected by the gaps; a Copy drag from it is accepted. lgse/strata#1692
- A folder dragged from another file manager shows the insertion line only once every item is confirmed to be a directory. lgse/strata#1692
- That check runs one metadata query at a time under a 2 s deadline that includes reading the drag payload. A timeout, a failure, or any non-folder rejects the whole selection. lgse/strata#1692
- A drop on a gap while that check is still running never falls through to a file transfer. lgse/strata#1692
- A trashed folder dragged from the Trash view, or an `http://` or `https://` link, is rejected with no insertion line and no probe of the link. lgse/strata#1692
- A drag-pinned folder is labelled with the entry's display name, as a menu pin is, such as a GVfs display name instead of the URI basename. lgse/strata#1692
- After another window unpins a gap's neighbour, a drop on that gap in a window that has not rebuilt lands beside the following pin, else the preceding one. With both gone it is rejected. lgse/strata#1692
- Directory symlinks and remote folders, such as SMB and SFTP shares, can be drag-pinned. Their locations are stored as spelled, not canonicalized. lgse/strata#1692
- Remote pins have gaps beside them, although their rows accept no file drops. lgse/strata#1692
- A folder pin drag that crosses a row's edges and gap, or leaves a spring-loaded row for a gap, keeps one insertion target. lgse/strata#1713 (unverified)
- A folder pin drag keeps its target while the sidebar shrinks to the rail and back. lgse/strata#1713 (unverified)
- With nothing pinned, dragging files or folders over the sidebar shows the empty PINNED section, and dropping a folder on its gap pins it. Leaving the sidebar hides it again. lgse/strata#1726

### Reordering through gaps

- Dropping a pinned row, local or remote, into a PINNED gap moves it there without changing its label or contents, and saves the order. Either gap next to the row is a no-op. lgse/strata#1692

### File chooser

- In the file chooser, a local folder dragged into a PINNED gap is bookmarked, not moved, and a remote folder is rejected before any probe. lgse/strata#1713

## Design

- Pinning uses dedicated gaps, separate from row bodies, which stay file-transfer targets; the two drop targets are visually distinct (lgse/strata#1690). Before, pinning took two steps: the menu, then a drag into place.
- Drags from Strata carry a snapshot of locations, display names, and an all-folders flag, so hovering a gap needs no filesystem probe. Foreign drags are validated once per drag, shared by every gap, so hover never blocks ([docs/architecture.md](https://github.com/lgse/strata/blob/e0f73973926ff67e77c2c56cf288b7b7617bb2e5/docs/architecture.md), lgse/strata#1692).
- Move is accepted only from Strata's own drag sources, whose drag-end handlers never delete. A foreign Move completion could ask the source application to delete the originals (lgse/strata#1692).
- One query in flight and a 2 s deadline bound speculative work on foreign selections such as 100 SFTP folders. Cancelling a GIO query does not interrupt a kernel-blocked call (lgse/strata#1692).
- Each gap remembers both neighbours, because other windows do not watch the bookmarks file (lgse/strata#1692).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |

## Known gaps

- A sidebar rebuild, such as a mount change, while a foreign folder drop is still being validated rejects the drop. lgse/strata#1692
- A network share or other mountable item dragged from another application is rejected, although the same item dragged from Strata pins. lgse/strata#1692
- Each gap is an empty accessible group named "PINNED", so the accessibility tree holds one per gap. lgse/strata#1692
