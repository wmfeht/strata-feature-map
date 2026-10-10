---
title: Preference storage and synchronization
status: shipped
origin: {issue: lgse/strata#212, pr: lgse/strata#518}
branch: null
reviewed_at: 72b840e69d6f0df9d33fb5583e62a3a2944886a1
review: draft
code: [src/ui/preferences/bindings.rs, src/ui/preferences/save_notice.rs, src/storage.rs]
tests: [src/ui/preferences/tests.rs, src/ui/preferences/tests/preferences.rs, src/ui/preferences/bindings/tests.rs, src/ui/preferences/fixtures.rs, src/storage/tests.rs, tests/e2e/scenarios/test_preferences.py]
related: []
---

## Summary

How application-wide preferences are loaded, saved to `settings.toml`, recovered from damaged files, and kept in step across every window of one Strata process. Every Settings row and every preference consumer goes through this store.

## Behavior

### Saving

- Each preference change is saved to `$XDG_CONFIG_HOME/strata/settings.toml`, normally `~/.config/strata/settings.toml`. lgse/strata#518
- A save writes a temporary file in the destination's directory, syncs it, and renames it into place. lgse/strata#39, lgse/strata#1544
- A failed write leaves the previous `settings.toml` intact and removes the temporary file. lgse/strata#39
- An existing `settings.toml` keeps its permission bits, so a 0644 file stays 0644; a missing one is created 0600. lgse/strata#1544
- A failed save logs a warning naming the `settings.toml` path and the reason. lgse/strata#1544 (unverified)
- A change whose save fails still applies in memory and is retried on the next save. lgse/strata#518
- Setting a preference to its current value notifies no consumer, and writes nothing unless an earlier save failed. lgse/strata#518
- Opening Settings writes nothing to `settings.toml`. lgse/strata#518

### Symlinked settings file

- When `settings.toml` is a user-owned symlink to a user-owned regular file, a change writes the target and leaves the link in place. lgse/strata#1455, lgse/strata#1544
- A relative link resolves against the link's own directory, and a chain of links resolves to its final file. lgse/strata#1544 (unverified)
- A chain of up to 8 links is written through; a 9th link is refused and nothing is written. lgse/strata#1544
- A link loop is refused like a chain longer than 8 links, and nothing is written. lgse/strata#1544 (unverified)
- A `settings.toml` that is a directory or other non-regular file, not a link, is refused, and nothing is written. lgse/strata#39, lgse/strata#1544
- A dangling link or a link to a directory is refused, and nothing is written. lgse/strata#1544
- A link owned by another user, or a target file another user owns, is refused. lgse/strata#1544
- A plain, unlinked `settings.toml` owned by another user, in a writable folder, is replaced by a user-owned file with the same permission bits. lgse/strata#1544 (unverified)
- When the target's directory is not writable, the save fails and its reason names the target, not the link. lgse/strata#1544 (unverified)
- The "Settings can't be saved" detail gives the refusal reason, such as "The symlink “<link>” points to a missing target “<target>”" or "The symlink “<path>” belongs to another user". lgse/strata#1544 (unverified)

### Save notices

- A save that fails while a browser window is active opens one dialog there: "Settings can't be saved", summary "Changes last only until Strata closes". lgse/strata#1455, lgse/strata#1544
- Its detail reads "Strata couldn't write “<path>”: <reason>. It tries again with each change." lgse/strata#1544
- Further failed saves show no dialog until a save succeeds; the next failure after a success shows the dialog again. lgse/strata#1544
- A save that fails with no active browser window, such as during an Omarchy theme update, is only logged. The next failure can still show the dialog. lgse/strata#1544
- A save that fails from a portal file chooser window is only logged. lgse/strata#1544
- When `settings.toml` could not be read at startup, the first change in a browser window opens one "Settings file can't be read" dialog per session. lgse/strata#721, lgse/strata#1544
- Its detail reads "Strata couldn't read “<path>” when it started: <reason>. To keep the file as it is, Strata won't save over it. Fix or remove the file, then restart Strata." lgse/strata#1544
- Startup with an unreadable `settings.toml` shows no dialog before the first change. lgse/strata#1544

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

[docs/preferences.md](https://github.com/lgse/strata/blob/72b840e69d6f0df9d33fb5583e62a3a2944886a1/docs/preferences.md) carries the lifecycle, the consumer table, and the steps for adding a preference.

- One binding call applies the current value at once and then each change, so there is no separate startup initializer to drift from the change handler (lgse/strata#518).
- Settings only edits preferences. Folder peeking once applied only when the General page was built, so a saved choice was ignored until Settings opened (lgse/strata#515).
- One general notification mechanism replaced per-preference broadcasts such as the release-channel one. Per-preference broadcasts duplicate listener lifecycle and loop prevention (lgse/strata#212).
- Bindings hold weak widget anchors and drop their listeners when the anchor is destroyed. Reentrant changes are delivered in a second pass without holding borrows across callbacks (lgse/strata#518).
- Settings controls ignore programmatic synchronization instead of writing it back, so two open windows cannot loop (lgse/strata#518).
- Synchronization covers windows of one process only. Separate processes and external edits while Strata runs are read on the next launch (lgse/strata#212).
- `PreferenceManager` owns the schema, persistence, and notifications; `ThemeManager` only applies themes and CSS. This leaves one writer of `settings.toml` (lgse/strata#1107).
- Writes are atomic and refuse a substituted final-component symlink, because direct writes left truncated files and followed symlinks (lgse/strata#15).
- lgse/strata#15 forbade only a substituted symlink, not one the user made. Dotfiles setups symlink `settings.toml`, so config writes follow user-owned links (lgse/strata#1455, lgse/strata#1544).
- Following links is opt-in, through `atomic_write_config`: `settings.toml`, `gtk-3.0/bookmarks`, custom themes, and the Hyprland bindings. Caches and state keep the strict `atomic_write` (lgse/strata#1455, lgse/strata#1544).
- The temporary file is created in the target's directory, so the rename never crosses filesystems. The regular-file check repeats on the target before the rename, which never follows a link (lgse/strata#1455).
- Existing permission bits are kept because replacing a 0644 dotfile would silently make it 0600 (lgse/strata#1455).
- A malformed entry is salvaged key by key instead of resetting the file, which had silently lost every customization on the next save (lgse/strata#646).
- A syntax error is preserved rather than repaired; saving stops until restart (lgse/strata#721, lgse/strata#728). No backup or recovery UI exists; a dialog at the first change says saving is off until restart (lgse/strata#1455, lgse/strata#1544).
- A failed save was only logged, so changes were lost without notice. One notice per failure streak covers write failures; the unreadable file gets one notice per session (lgse/strata#1455, lgse/strata#1544).
- The notice opens after the failing setter returns, and only in the active browser window, because the change came from the user there. Timers and the chooser only log ([docs/preferences.md](https://github.com/lgse/strata/blob/72b840e69d6f0df9d33fb5583e62a3a2944886a1/docs/preferences.md), lgse/strata#1544).
- Every new preference must extend an exhaustive fixture with no `..Default` escape, and tests compare changed keys with every serialized field (lgse/strata#518).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-10 | lgse/strata#1544 | fix | Wrote config files through user-owned symlinks, kept file modes, and showed a notice when settings cannot be saved. |
| 2026-09-18 | lgse/strata#1109 | refactor | Moved preference storage, notifications, and bindings from `ThemeManager` to `PreferenceManager`. |
| 2026-09-10 | lgse/strata#728 | fix | Logged unreadable or invalid TOML and stopped saving instead of overwriting it with defaults. |
| 2026-09-09 | lgse/strata#671 | fix | Kept valid entries when one entry is malformed or a required key is missing. |
| 2026-09-07 | lgse/strata#518 | fix | Bound every preference at construction and live across windows, so Settings only edits values. |
| 2026-09-01 | lgse/strata#144 | fix | Persisted Reduce motion, Hidden files, and Folders first, which had reset on restart. |
| 2026-08-31 | lgse/strata#39 | fix | Wrote settings and other managed files atomically with private permissions and refused symlink destinations. |

## Known gaps

- With an unreadable `settings.toml`, the load warning is logged twice at startup. lgse/strata#1544
