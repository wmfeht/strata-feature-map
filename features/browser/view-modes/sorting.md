---
title: Sorting
status: shipped
origin: {issue: lgse/strata#40, pr: lgse/strata#44}
branch: null
reviewed_at: 72b840e69d6f0df9d33fb5583e62a3a2944886a1
review: draft
code: [src/app/browser/sorting.rs]
tests: [src/app/browser/sorting/tests.rs]
docs: [docs/preferences.md]
related: [browser/view-modes/list, browser/navigation/recent, devices/volumes/camera]
---

## Summary

Ordering a folder's entries by Name, Size, Modified, or Type, ascending or descending, with folders optionally first, in all three view modes. The default sort is shared and saved.

## Behavior

### Controls

- Columns and Icons pane headers have a "Choose sort field" button whose SORT BY menu lists Name, Size, Modified, Type, and Folders first; choosing an option applies it and closes the menu. lgse/strata#168
- In the SORT BY menu, the sort fields, Recency and Device order included, are radio menu items. Folders first is a check menu item. lgse/strata#1467, lgse/strata#1544
- The direction button beside Sort by has the tooltip "Ascending — click to reverse" or "Descending — click to reverse" and reverses that pane's order when clicked. lgse/strata#40 (unverified)
- In Recent the menu adds Recency and omits Folders first; in Camera Photos it adds Device order. lgse/strata#1029, lgse/strata#1083 (unverified)
- While Device order is active, the direction button is disabled with the tooltip "Device order follows discovery; choose a sort field to reverse its direction". lgse/strata#1029 (unverified)

### Order

- Name sorting ignores case: `apple`, `Banana`, `cherry`, `Date` sort in that order. lgse/strata#232
- Names differing only in case are ordered by their original spelling, so the order is stable. lgse/strata#232
- Digit runs compare by value: `File 2` sorts before `File 10`. lgse/strata#879
- Type sorts by the MIME description guessed from the filename; ascending puts unrecognized files last, descending puts them first, with names A–Z within each type. lgse/strata#946
- With Folders first on, the default, folders stay ahead of files in both directions. lgse/strata#946
- Entries tied on Size, Modified, or Type are ordered by name. lgse/strata#946 (unverified)
- Choosing Size or Modified loads any missing sizes or dates for that folder before reordering. lgse/strata#274 (unverified)
- A folder that finishes loading under Size or Modified with sizes or dates missing shows its rows by name, then fills them and reorders. lgse/strata#274 (unverified)

### Defaults

- Choosing a field sort outside Recent reorders that pane and becomes the default for folders opened afterwards; other open columns keep their own sort. lgse/strata#40, lgse/strata#1520
- The default field and direction are saved and restored before the first folder loads; missing or invalid saved values fall back to Name ascending. lgse/strata#44
- The Folders first setting is saved and restored after a restart. lgse/strata#144
- A folder of more than 2,048 entries is sorted off the UI thread and stays in its loading state until the sorted rows are shown. lgse/strata#1030
- If the background sort fails, the pane shows the error "Sorting the directory failed." lgse/strata#1030 (unverified)

## Design

One sort default is shared by Columns, Icons, and List, so a change in any mode survives mode switches and restarts (lgse/strata#40). Existing columns keep their local sort; only newly opened columns inherit the default (lgse/strata#1520, `docs/preferences.md`). Recent and Camera Photos force their own sort, which never changes the default field or direction (lgse/strata#1083, lgse/strata#1029).

- Case-insensitive order matches GNOME Files, Dolphin, Windows Explorer, and Finder (lgse/strata#216).
- Type uses `content_type_guess` on the name only. Sniffing contents like Dolphin was rejected: it needs I/O on every file and fights streaming, incremental sorting (lgse/strata#508).
- Full sorts and batch merges compute case-folded keys once per entry instead of inside the comparator, with a zero-allocation path for ASCII names (lgse/strata#1318, lgse/strata#1401).
- A superseded sort worker is rejected before it can remove pending state; otherwise it discarded the replacement load's monitor changes (lgse/strata#1030).
- The 2,048-entry inline limit was measured and kept; the cost seen with CJK names was case folding, not the threshold (lgse/strata#1319).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-05 | lgse/strata#1401 | perf | Precomputed case-folded sort keys once per entry. |
| 2026-09-15 | lgse/strata#1030 | refactor | Isolated staged sort completion and rejected superseded workers before removing pending state. |
| 2026-09-15 | lgse/strata#946 | feat | Sorted Type by filename MIME description instead of entry kind. |
| 2026-09-12 | lgse/strata#879 | fix | Compared digit runs by value so numeric suffixes sort naturally. |
| 2026-09-03 | lgse/strata#232 | feat | Sorted names case-insensitively with a stable tie-break. |
| 2026-08-31 | lgse/strata#44 | feat | Saved the sort field and direction and restored them before the first load. |

## Known gaps

- Sort is one global default, so a folder's own sort is not remembered after leaving it. lgse/strata#1520
