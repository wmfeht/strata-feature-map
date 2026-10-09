---
title: Global search exclusions
status: shipped
origin: {issue: lgse/strata#1062, pr: lgse/strata#1064}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [src/services/search/exclusions.rs, src/ui/settings/exclusions.rs]
tests: [src/services/search/exclusions/tests.rs, src/ui/settings/exclusions/tests.rs]
docs: [docs/preferences.md]
related: [settings/preferences]
---

## Summary

User-defined folder names and directory paths that Ctrl+K global search skips while indexing. They are edited under Settings → General → Search & filtering → **Global search exclusions**.

## Behavior

### Editing

- The row shows a text field, **Browse…** and **Add** buttons, and a scrollable list of saved exclusions below them. lgse/strata#1064
- Pressing Enter in the field, or clicking **Add**, saves the rule and clears the field. lgse/strata#1064
- **Browse…** opens a folder chooser and puts the chosen path, with Home shortened to `~`, in the field without saving it. lgse/strata#1064 (unverified)
- Each saved rule shows its text, a "Folder name" or "Directory" label, and a remove button that deletes it. lgse/strata#1064 (unverified)
- With no rules, the list shows "No custom exclusions added. Common tool caches (.venv, node_modules, target, etc.) are excluded automatically." lgse/strata#1064 (unverified)
- With two Settings windows open, an add or remove in one updates the other without erasing its draft. lgse/strata#1064
- Rules persist after Settings is closed and reopened. lgse/strata#1064
- A rule is saved normalized: `~/LargeData/` is listed as the full path, such as `/home/user/LargeData`. lgse/strata#1064 (unverified)

### Validation

- An empty entry shows "Enter a folder name or directory path." lgse/strata#1064
- `/`, `~`, or the full Home path shows "Cannot exclude root or entire home directory." lgse/strata#1064
- A rule containing `/` or starting with `~`, but starting with neither `/` nor `~/`, such as `project/build` or `~user/dir`, shows "Directory paths must start with / or ~/". lgse/strata#1064
- A path containing a `..` component shows "Directory paths cannot contain .." lgse/strata#1064
- `.` or `..` as a folder name shows "Enter a folder name, not . or .." lgse/strata#1064 (unverified)
- A rule equal to a saved one, ignoring case for folder names, shows "This exclusion has already been added." lgse/strata#1064

### Effect on search

- A folder-name rule such as `private-build` hides every folder of that name, and everything below it, case-insensitively. lgse/strata#1064
- A folder-name rule does not hide a file with the same name. lgse/strata#1064 (unverified)
- A rule starting with `/` or `~/` hides only that subtree, matched case-sensitively by whole path components. lgse/strata#1064
- Each opening of Ctrl+K reads the current rules, including before Settings has been opened; an open search keeps its rules until reopened. lgse/strata#1064
- Removing a rule and reopening Ctrl+K finds files in that subtree again. lgse/strata#1064
- Pane filters, 10xer path search, folder-history search, and destination pickers ignore the rules. lgse/strata#1064
- Invalid rules in the saved preferences are ignored. lgse/strata#1064

## Design

[docs/preferences.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/preferences.md#global-search-exclusions) carries the rule syntax and the preference lifecycle.

- Excluded subtrees are pruned during traversal, so they use neither index memory nor time budget (lgse/strata#1062).
- A separate **Manage…** modal was proposed in lgse/strata#1062. At the owner's request the form sits inline in Settings with a bounded, scrollable list (lgse/strata#1064).
- A rule containing `/` or starting with `~` is a path; anything else is a literal folder name, not a glob (lgse/strata#1064).
- Paths containing `..` are rejected rather than collapsed, because lexical collapsing changes their meaning through symlinks (lgse/strata#1064).
- Rules are normalized before indexing, so equivalent rule lists share one index (lgse/strata#1064).
- Exclusions apply only to global search. Pane filters and destination pickers keep their explicit browsing scope (lgse/strata#1064).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-07 | lgse/strata#1064 | feat | Added folder-name and directory exclusions for global search, edited inline in Settings. |

## Known gaps

None known.
