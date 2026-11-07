---
title: Sorting
status: shipped
origin: {issue: lgse/strata#40, pr: lgse/strata#44}
branch: null
reviewed_at: 5738aad808ea4cc4671516bc569d85f862664809
review: draft
code: [src/app/browser/sorting.rs, src/services/mime_type.rs, src/app/browser/sort_settings.rs, src/app/navigation/ordering.rs, src/ui/browser/pane_header/sort_menu.rs]
tests: [src/app/browser/sorting/tests.rs, src/services/mime_type/tests.rs, tests/qa/scenarios/search_filter_sort/sorting-by-size.jsonl, tests/qa/scenarios/search_filter_sort/reversing-sort-direction.jsonl, src/app/navigation/tests/sorting.rs, tests/qa/scenarios/search_filter_sort/additional-sort-choices.jsonl]
docs: [docs/preferences.md]
related: [browser/view-modes/folder-views, browser/view-modes/list, browser/navigation/recent, devices/volumes/camera]
---

## Summary

Ordering a folder's entries by Name, Size, Modified, Type, Extension, or Created, ascending or descending, or leaving them Unsorted, in all three view modes. Names compare in Natural or Alphabetical order, optionally case-sensitive, and folders can come first. The default sort is shared and saved; per-folder sorts belong to `browser/view-modes/folder-views`.

## Behavior

### Controls

- Columns, Icons, and List pane headers have a "Choose sort field" button that opens one flat sort menu. lgse/strata#168, lgse/strata#2029
- The menu's SORT BY section lists Name, Size, Modified, Type, Extension, and Created as radio menu items. lgse/strata#1467, lgse/strata#2029
- In Recent the menu adds Recency, which sorts in either direction, after Created. In Camera Photos it adds Device order there. Both are radio menu items too. lgse/strata#1029, lgse/strata#1083, lgse/strata#1467, lgse/strata#2029 (unverified)
- Unsorted has no row. Choosing the checked field again, Name included, switches to Unsorted. lgse/strata#2029
- A NAME ORDER section holds the radio items Natural and Alphabetical, then the check item "Case-sensitive names". lgse/strata#2029
- Folders first is a check menu item in its own section after NAME ORDER. lgse/strata#1544, lgse/strata#2029
- In List the menu adds an Ascending and Descending radio section after SORT BY. Columns and Icons keep the direction button instead. lgse/strata#2029
- The last section holds "Make default" and "Reset to default sort", each hidden while it does not apply. lgse/strata#1565, lgse/strata#2029
- Choosing any row, by a click, Enter, or Space, applies it and leaves the menu open with its checkmarks updated. Escape or a click outside closes it. lgse/strata#2029
- Under Unsorted, the direction rows and the three NAME ORDER rows are disabled. lgse/strata#2029
- Under Device order, the direction and NAME ORDER rows are disabled. Under Recency, the NAME ORDER rows and Folders first are. lgse/strata#2029 (unverified)
- In Recent the Folders first row is present; it is disabled only under Recency. lgse/strata#2029 (unverified)
- In Recent under another sort, choosing Folders first leaves the row enabled. The saved setting and every pane's order stay unchanged, as with the 10xer `, f` chord. lgse/strata#2074
- "Make default" shows in a remembered folder whose current sort, including direction and name order, differs from the default. It saves a choice still waiting to apply. lgse/strata#1565, lgse/strata#2029
- Under Device order or Recency, "Make default" stays hidden. lgse/strata#2029 (unverified)
- "Reset to default sort" shows only for a folder with its own saved sort. It also cancels a sort choice still waiting to apply. lgse/strata#1565, lgse/strata#2029
- The menu's top inset matches its bottom inset. lgse/strata#2029
- The direction button beside Sort by has the tooltip "Ascending — click to reverse" or "Descending — click to reverse" and reverses that pane's order when clicked. lgse/strata#40 (unverified)
- While Device order is active, the direction button is disabled with the tooltip "Device order follows discovery; choose a sort field to reverse its direction". lgse/strata#1029 (unverified)
- While Unsorted is active, the direction button is disabled with the tooltip "Unsorted". lgse/strata#2029 (unverified)
- While Unsorted is active, direction and name-order changes from any control do nothing, including Shift with the 10xer Unsorted chord. lgse/strata#2029

### List label

- In List, the sort button is icon-only with the tooltip "Choose sort field" under Unsorted or Device order. lgse/strata#2029
- It is also icon-only when the field's column (Name, Size, Type, or Modified) is shown and, for Name, the order is Natural and case-insensitive. lgse/strata#2029
- Otherwise it reads "Sort: <field>" and an arrow, such as "Sort: Extension ↑" or "Sort: Created ↓". lgse/strata#2029
- Sorted by Name in Alphabetical order, it reads "Sort: Name · Alphabetical ↑". Case-sensitive adds " · case-sensitive", as in "Sort: Name · Natural · case-sensitive ↑". lgse/strata#2029
- Hiding the sorted field's column shows the label at once; showing the column again returns the icon. lgse/strata#2029
- In Recent, the List button reads "Sort: Recency ↑" or "Sort: Recency ↓", since Recency has no column. lgse/strata#2029 (unverified)

### Order

- By default, name sorting ignores case: `apple`, `Banana`, `cherry`, `Date` sort in that order. lgse/strata#232, lgse/strata#2029
- Names differing only in case are ordered by their original spelling, so the order is stable. lgse/strata#232
- In Natural order, the default, digit runs compare by value: `File 2` sorts before `File 10`. lgse/strata#879, lgse/strata#2029
- In Alphabetical order, digits compare one character at a time: `file1`, `file10`, `file2`. lgse/strata#2029
- With Case-sensitive names on, uppercase sorts before lowercase: Natural order gives `Z2`, `Z10`, `a2`, `a10`. lgse/strata#2029 (unverified)
- Type sorts by the MIME description guessed from the filename; ascending puts unrecognized files last, descending puts them first, with names A–Z within each type. lgse/strata#946
- A RAW file that shared-mime-info does not type as an image, such as `GOPR0001.GPR`, is typed `image/x-dcraw` instead of Other. lgse/strata#1698
- Its Type shows that type's description, "Digital raw image" in English. lgse/strata#1698
- A `.h264` file's Type reads "video/h264 type" instead of Other. lgse/strata#1901
- The type comes from the name alone, so text or empty files named `.h264` read the same. lgse/strata#1901 (unverified)
- Sorted by Type, `.h264` files sort among the known types rather than with Other. lgse/strata#1901 (unverified)
- Extension sorts by the final suffix: `archive.tar.gz` sorts under `gz`. Dotfiles such as `.gitignore` and names without a suffix have no extension. lgse/strata#2029
- Extension ascending puts names without an extension first: `.gitignore`, `readme`, `archive.tar.gz`, `file2.md`, `file10.md`, `z.rs`. Suffixes compare in the selected name order. lgse/strata#2029 (unverified)
- Created sorts by birth time, with entries whose birth time is missing last in both directions. lgse/strata#2029
- Unsorted keeps the order the directory listed its entries and ignores direction. With Folders first on, folders lead, each group in listed order. lgse/strata#2029
- Unsorted order stays the same while a large folder's rows stream in. lgse/strata#2029
- Choosing Unsorted reloads the folder. lgse/strata#2029
- Toggling Folders first while Unsorted also reloads the folder. lgse/strata#2029 (unverified)
- With Folders first on, the default, folders stay ahead of files in both directions. lgse/strata#946
- Under every field, entries tied on it are ordered by name in the selected name order. lgse/strata#946, lgse/strata#2029
- That name tie-break stays ascending when the field is descending. With Folders first on and `folder` a directory, Extension descending gives `folder`, `a.rs`, `file2.md`, `file10.md`, `Z.md`, `z.csv`. lgse/strata#2029
- Choosing Size, Modified, or Created loads any missing sizes, dates, or birth times for that folder before reordering. lgse/strata#274, lgse/strata#2029 (unverified)
- A folder that finishes loading under Size, Modified, or Created with values missing shows rows by name, then fills and reorders them. lgse/strata#274, lgse/strata#2029 (unverified)

### Defaults

- With Remember sort and icon size per folder off, a field sort chosen outside Recent reorders that pane and becomes the default for later folders. lgse/strata#40, lgse/strata#1565
- With that switch off, other open columns keep their own sort. lgse/strata#40, lgse/strata#1520, lgse/strata#1565
- The default field and direction are saved and restored before the first folder loads; missing or invalid saved values fall back to Name ascending. lgse/strata#44
- Name order and case sensitivity are saved with the default sort. With Remember sort and icon size per folder off, changing either makes it the default. lgse/strata#2029
- In Columns, a sort change or Make default in a folder starts from that folder's sort. The last choice at that depth elsewhere does not carry over. lgse/strata#2029
- The Folders first setting is saved and restored after a restart. lgse/strata#144
- Toggling Folders first in any pane outside Recent re-sorts every open column in every window; Recent's order is unaffected. lgse/strata#1563, lgse/strata#1565, lgse/strata#2074
- A folder of more than 2,048 entries is sorted off the UI thread and stays in its loading state until the sorted rows are shown. lgse/strata#1030
- If the background sort fails, the pane shows the error "Sorting the directory failed." lgse/strata#1030 (unverified)

## Design

One sort default is shared by Columns, Icons, and List, so a change in any mode survives mode switches and restarts (lgse/strata#40). With per-folder values off, existing columns keep their local sort and only new columns inherit the default (lgse/strata#1520, lgse/strata#1565). Folders first is application-wide in either case (lgse/strata#1565). The menu and the 10xer chord share `Browser::toggle_folders_first`, which ignores Recent rather than change the setting for other folders (lgse/strata#2074). Recent and Camera Photos force their own sort, which never changes the default field or direction (lgse/strata#1083, lgse/strata#1029).

- Case-insensitive order matches GNOME Files, Dolphin, Windows Explorer, and Finder (lgse/strata#216).
- Type uses `content_type_guess` on the name only. Sniffing contents like Dolphin was rejected: it needs I/O on every file and fights streaming, incremental sorting (lgse/strata#508).
- The Type guess is shared with the preview, custom-action MIME matching, and chooser filters, so all four treat RAW names alike. The RAW override applies only when GIO does not already return an image type, and stays name-only (lgse/strata#1698).
- Full sorts and batch merges compute case-folded keys once per entry instead of inside the comparator, with a zero-allocation path for ASCII names (lgse/strata#1318, lgse/strata#1401).
- A superseded sort worker is rejected before it can remove pending state; otherwise it discarded the replacement load's monitor changes (lgse/strata#1030).
- The 2,048-entry inline limit was measured and kept; the cost seen with CJK names was case folding, not the threshold (lgse/strata#1319).
- Extension was added because Type sorts by MIME description, not suffix (lgse/strata#1652).
- lgse/strata#1652 first chose flyouts showing their value on the right. A dot or asterisk marker was rejected: it says something changed, not what ([comment](https://github.com/lgse/strata/issues/1652#issuecomment-6528591816)). The owner then chose one flat menu ([comment](https://github.com/lgse/strata/pull/2029#issuecomment-6612311272)), so no choice hides in a flyout opening over the listing at the window edge (lgse/strata#2029, commit 5d52fc0f).
- Unsorted has no row because unchecking the active field already turns sorting off ([comment](https://github.com/lgse/strata/pull/2029#issuecomment-6612311272)).
- lgse/strata#1652 asked for the menu to stay open while options change, and for the name order to break ties under other fields too ([comment](https://github.com/lgse/strata/issues/1652#issuecomment-6528591816)).
- In List, the label shows only when no visible column header carries the sort. Ascending and Descending let Extension and Created reverse without one ([comment](https://github.com/lgse/strata/issues/1652#issuecomment-6528591816)).
- Open sort menus are tracked while mapped and refreshed from the tab's event dispatch. A `Browser::observe` per menu build leaked observers, 6 to 26 over 18 navigations ([comment](https://github.com/lgse/strata/pull/2029#issuecomment-6612311272)).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-11-03 | lgse/strata#2029 | feat | Added Extension, Created, Unsorted, and name-order choices in a flat menu that stays open, and an always-present List sort control (lgse/strata#1652). |
| 2026-10-05 | lgse/strata#1401 | perf | Precomputed case-folded sort keys once per entry. |
| 2026-09-15 | lgse/strata#1030 | refactor | Isolated staged sort completion and rejected superseded workers before removing pending state. |
| 2026-09-15 | lgse/strata#946 | feat | Sorted Type by filename MIME description instead of entry kind. |
| 2026-09-12 | lgse/strata#879 | fix | Compared digit runs by value so numeric suffixes sort naturally. |
| 2026-09-03 | lgse/strata#232 | feat | Sorted names case-insensitively with a stable tie-break. |
| 2026-08-31 | lgse/strata#44 | feat | Saved the sort field and direction and restored them before the first load. |

## Known gaps

- Filenames sort by code point, not by pinyin. lgse/strata#1583
- Random sort and transliterated name order are left out of the first version. lgse/strata#2029
- In Recent under a sort other than Recency, the Folders first row stays enabled though choosing it does nothing. lgse/strata#2074
