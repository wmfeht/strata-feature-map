---
title: Preference storage and synchronization
status: shipped
origin: {issue: lgse/strata#212, pr: lgse/strata#518}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: reviewed
code: [src/ui/preferences/bindings.rs, src/storage.rs]
tests: [src/ui/preferences/tests.rs, src/ui/preferences/tests/preferences.rs, src/ui/preferences/bindings/tests.rs, src/ui/preferences/fixtures.rs, src/storage/tests.rs, tests/e2e/scenarios/test_preferences.py]
related: []
---

## Summary

How application-wide preferences are loaded, saved to `settings.toml`, recovered from damaged files, and kept in step across every window of one Strata process. Every Settings row and every preference consumer goes through this store.

## Behavior

### Saving

- Each preference change is saved to `$XDG_CONFIG_HOME/strata/settings.toml`, normally `~/.config/strata/settings.toml`. lgse/strata#518
- A save writes a mode-0600 temporary file beside `settings.toml`, syncs it, and renames it into place. lgse/strata#39
- A failed write leaves the previous `settings.toml` intact and removes the temporary file. lgse/strata#39
- A `settings.toml` that is a symlink or not a regular file is never replaced, and the symlink target is not touched. lgse/strata#39
- A change whose save fails still applies in memory and is retried on the next save. lgse/strata#518
- Setting a preference to its current value notifies no consumer, and writes nothing unless an earlier save failed. lgse/strata#518
- Opening Settings writes nothing to `settings.toml`. lgse/strata#518

### Loading and recovery

- Saved non-default values govern behavior from the first interaction after launch, before Settings is opened. lgse/strata#518
- A missing `settings.toml` starts with defaults and saves normally on the first change. lgse/strata#728
- A value of the wrong type, such as `show_hidden = "yes"`, or a missing required key falls back to its default alone; every other entry loads. lgse/strata#671
- Startup does not rewrite a file with invalid entries; the next change saves the recovered values. lgse/strata#671
- A `settings.toml` that cannot be read or is not valid TOML logs a warning, and Strata starts with defaults. lgse/strata#728
- After such a load failure, changes apply in memory but the file is never written until it is repaired and Strata restarts. lgse/strata#728

### Synchronization

- Changing a preference in one window updates the matching Settings controls and behavior in every open window of the same process. lgse/strata#518
- Location, selection, history, each column's sort, and the filter query stay local to their window. lgse/strata#518

## Design

[docs/preferences.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/preferences.md) carries the lifecycle, the consumer table, and the steps for adding a preference.

- One binding call applies the current value at once and then each change, so there is no separate startup initializer to drift from the change handler (lgse/strata#518).
- Settings only edits preferences. Folder peeking once applied only when the General page was built, so a saved choice was ignored until Settings opened (lgse/strata#515).
- One general notification mechanism replaced per-preference broadcasts such as the release-channel one. Per-preference broadcasts duplicate listener lifecycle and loop prevention (lgse/strata#212).
- Bindings hold weak widget anchors and drop their listeners when the anchor is destroyed. Reentrant changes are delivered in a second pass without holding borrows across callbacks (lgse/strata#518).
- Settings controls ignore programmatic synchronization instead of writing it back, so two open windows cannot loop (lgse/strata#518).
- Synchronization covers windows of one process only. Separate processes and external edits while Strata runs are read on the next launch (lgse/strata#212).
- `PreferenceManager` owns the schema, persistence, and notifications; `ThemeManager` only applies themes and CSS. This leaves one writer of `settings.toml` (lgse/strata#1107).
- Writes are atomic and refuse a substituted final-component symlink, because direct writes left truncated files and followed symlinks (lgse/strata#15).
- A malformed entry is salvaged key by key instead of resetting the file, which had silently lost every customization on the next save (lgse/strata#646).
- A syntax error is preserved rather than repaired. No backup or recovery UI was added; saving stops until restart (lgse/strata#721, lgse/strata#728).
- Every new preference must extend an exhaustive fixture with no `..Default` escape, and tests compare changed keys with every serialized field (lgse/strata#518).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-18 | lgse/strata#1109 | refactor | Moved preference storage, notifications, and bindings from `ThemeManager` to `PreferenceManager`. |
| 2026-09-10 | lgse/strata#728 | fix | Logged unreadable or invalid TOML and stopped saving instead of overwriting it with defaults. |
| 2026-09-09 | lgse/strata#671 | fix | Kept valid entries when one entry is malformed or a required key is missing. |
| 2026-09-07 | lgse/strata#518 | fix | Bound every preference at construction and live across windows, so Settings only edits values. |
| 2026-09-01 | lgse/strata#144 | fix | Persisted Reduce motion, Hidden files, and Folders first, which had reset on restart. |
| 2026-08-31 | lgse/strata#39 | fix | Wrote settings and other managed files atomically with private permissions and refused symlink destinations. |

## Known gaps

- A symlinked `settings.toml`, as in dotfile setups, loads but every save is refused with only a log warning, so changes are lost on restart; the fix is unmerged. lgse/strata#1455, lgse/strata#1544
