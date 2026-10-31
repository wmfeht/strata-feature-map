---
title: Location path completion
status: shipped
origin: {issue: null, pr: lgse/strata#388}
branch: null
reviewed_at: 965bd7ec74400734dbd0a5311ceefa05bea8dd63
review: draft
code: [src/ui/browser/location/completion.rs]
tests: [src/ui/browser/location/completion/tests.rs, tests/qa/scenarios/locations/path-completion-dismisses-on-window-switch.jsonl]
related: [app/keyboard-shortcuts/remapping]
---

## Summary

The folder suggestions shown under the location entry while a path is typed. They are picked with the keyboard and completed with Tab, and a worker lists them so a slow mount does not block typing.

## Behavior

- While editing, a popover under the entry, matching its width, lists child folders whose names start with the typed absolute, `~/`, or relative path, ignoring case. lgse/strata#388
- A relative prefix completes against the current folder and inserts the folder's absolute path. lgse/strata#388 (unverified)
- Typing only `~` suggests `~/`. lgse/strata#388 (unverified)
- When the typed text names an existing folder and at most one sibling matches it, the popover lists that folder's children instead. lgse/strata#388 (unverified)
- Each suggestion shows a folder icon, the name with the typed prefix highlighted, and its parent folder, with home shortened to `~`. lgse/strata#388 (unverified)
- Down and Up move through suggestions, wrapping at the ends, and Page Down and Page Up move by 5. lgse/strata#388 (unverified)
- Page Down and Page Up still move by 5 after `page_down` or `page_up` is rebound, since completion reads the physical keys. lgse/strata#1885 (unverified)
- Tab inserts the highlighted suggestion, the only suggestion, or a longer common prefix and closes the popover; Down reopens it. lgse/strata#388
- A key added to `focus_next` or `focus_previous`, such as F7 or Ctrl+F7, completes the path as Tab does. lgse/strata#1885
- When Tab has nothing longer to insert, it highlights the next suggestion instead. lgse/strata#388 (unverified)
- Enter on a highlighted suggestion opens that folder. lgse/strata#388
- Hidden folders are suggested only when hidden files are shown or the typed name starts with `.`. lgse/strata#388 (unverified)
- The popover does not appear while the breadcrumbs are showing. lgse/strata#388
- While the typed folder is being listed, the previous suggestions stay; only the latest text's list replaces them. lgse/strata#1729 (unverified)
- Tab pressed during the listing waits for its list, and so do Down, Up, Page Down, and Page Up while suggestions show. Enter after one of them waits too; they then run in order. lgse/strata#1729
- Switching to another window, minimising, or hiding Strata while suggestions show closes the popover. The typed path and location editing stay. lgse/strata#1943
- A listing still pending when the window loses focus is cancelled, so its result does not reopen the popover. lgse/strata#1943
- Editing the entry text while the window is not focused shows no suggestions. lgse/strata#1943 (unverified)
- Refocusing the window does not reopen suggestions; the next text change shows them again. lgse/strata#1943
- Hiding the location entry closes the popover and cancels a pending listing. lgse/strata#1943 (unverified)
- Switching tabs closes the previous tab's suggestions, since background tabs count as hidden. lgse/strata#1943 (unverified)
- In the portal file chooser, focusing another window closes the location field's suggestions. lgse/strata#1943 (unverified)

## Design

- Completion scans at most 10,000 entries and lists at most 50 folders (lgse/strata#388).
- Since lgse/strata#1729 a worker lists the folder, one request per text change, so a dead mount cannot freeze typing.
- Suggestions close on any focus loss, not only on minimise or hide. Wayland does not tell GTK a window is minimised, and minimising does not unmap the entry (lgse/strata#1940, lgse/strata#1943).
- The popover waits for the entry to be mapped before showing, so the first reveal after leaving the breadcrumbs still works (lgse/strata#1943).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-31 | lgse/strata#1943 | fix | Dismissed suggestions and cancelled pending listings when the window loses focus, so no dropdown outlives a minimise. |

## Known gaps

None known.
