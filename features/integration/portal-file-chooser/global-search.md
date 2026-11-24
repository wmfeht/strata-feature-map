---
title: Global search in the file chooser
status: shipped
origin: {issue: lgse/strata#2799, pr: lgse/strata#2802}
branch: null
reviewed_at: ed544cf3bbb3968299ed8223148a65823739d48f
review: draft
code: [src/ui/chooser/search.rs]
tests: [tests/qa/scenarios/chooser_selection/chooser-global-search-reveals-file.jsonl]
related: [browser/search, app/shortcut-reference, integration/10xer-mode/file-chooser]
---

## Summary

The main window's global search palette, opened inside the portal file chooser and its destination choosers. It finds files and folders outside the current folder and moves the chooser to them without accepting the request.

## Behavior

- Ctrl+K in the chooser opens the global search palette over it, in both key maps, including a rebound 10xer search key. lgse/strata#2802
- Pressing the search key again while the palette is open closes it. lgse/strata#2802
- With 10xer mode off, Ctrl+K opens the palette with focus in Name or the location field. lgse/strata#2802
- Ctrl+K with focus in a popover, such as an open dropdown, opens no palette. lgse/strata#2802 (unverified)
- The palette searches Home and the mounted local drives, read again each time it opens. lgse/strata#2802 (unverified)
- Enter on a folder result opens that folder in the chooser. lgse/strata#2802
- Enter on a file result opens its folder with the file highlighted. It neither launches the file nor submits the request. lgse/strata#2802
- After a file is revealed, Open returns that file. lgse/strata#2802
- With "Open search results directly" on, Enter on a file result still only reveals it. lgse/strata#2802 (unverified)
- Alt+Enter or the result menu's Open containing folder reveals the item, file or folder, highlighted in its parent folder, and submits nothing. lgse/strata#2802 (unverified)
- In a Save request, entering a folder from the palette keeps the typed Name, and Save saves into that folder. lgse/strata#2802
- Escape dismisses only the palette; the request stays open and the selection is unchanged. lgse/strata#2802
- In a Send to chooser confined to a device, Ctrl+K opens nothing. lgse/strata#2802
- Ctrl+F still opens the folder-scoped filter. lgse/strata#2802

## Design

- The chooser had Ctrl+F for its folder but nothing for files elsewhere. Opening a browser window and copying a path interrupts the request (lgse/strata#2799).
- A pick must navigate or reveal, never launch a file or submit the request, and Escape returns to the pending request (lgse/strata#2799).
- Window-wide stages never see chooser keys (lgse/strata#1311). The chooser therefore gets its own palette instance and key stage (lgse/strata#2802).
- Results pass the request's own entry check before display, and activation checks it again, so a result the request does not allow is never acted on (lgse/strata#2802).
- Both palette actions, Enter and Open containing folder, go through the chooser's own callbacks, so nothing in the palette can launch a file (lgse/strata#2802).
- A device-confined chooser does not index global roots, so search cannot lead outside the device (lgse/strata#2799).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |

## Known gaps

None known.
