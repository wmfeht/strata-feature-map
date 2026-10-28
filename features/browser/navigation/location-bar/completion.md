---
title: Location path completion
status: shipped
origin: {issue: null, pr: lgse/strata#388}
branch: null
reviewed_at: 86df474dc0e8352e0e2098637a017cc4c77a8c44
review: draft
code: [src/ui/browser/location/completion.rs]
tests: [src/ui/browser/location/completion/tests.rs]
related: []
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
- Tab inserts the highlighted suggestion, the only suggestion, or a longer common prefix and closes the popover; Down reopens it. lgse/strata#388
- When Tab has nothing longer to insert, it highlights the next suggestion instead. lgse/strata#388 (unverified)
- Enter on a highlighted suggestion opens that folder. lgse/strata#388
- Hidden folders are suggested only when hidden files are shown or the typed name starts with `.`. lgse/strata#388 (unverified)
- The popover does not appear while the breadcrumbs are showing. lgse/strata#388
- While the typed folder is being listed, the previous suggestions stay; only the latest text's list replaces them. lgse/strata#1729 (unverified)
- Tab pressed during the listing waits for its list, and so do Down, Up, Page Down, and Page Up while suggestions show. Enter after one of them waits too; they then run in order. lgse/strata#1729

## Design

- Completion scans at most 10,000 entries and lists at most 50 folders (lgse/strata#388).
- Since lgse/strata#1729 a worker lists the folder, one request per text change, so a dead mount cannot freeze typing.

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |

## Known gaps

None known.
