---
title: Custom actions
status: shipped
origin: {issue: lgse/strata#36, pr: lgse/strata#1085}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [src/model/action.rs, src/model/action/**, src/services/actions.rs, src/services/actions/**, src/adapters/local_actions.rs, src/adapters/local_actions/**, src/ui/actions.rs, src/ui/settings/actions.rs, src/ui/settings/actions/**, data/actions]
tests: [src/model/action/tests.rs, src/services/actions/tests.rs, src/adapters/local_actions/tests.rs, src/ui/settings/actions/tests.rs, src/ui/settings/actions/tests/readiness.rs, src/adapters/local_jobs/tests/examples.rs, src/adapters/local_jobs/tests/examples/**, tests/e2e/scenarios/test_custom_actions.py]
docs: [docs/custom-actions.md]
related: [operations/progress/jobs, integration/10xer-mode, remote/file-providers]
---

## Summary

User-defined Python, Bash, or command actions in the file and folder context menus. Each action is a folder holding an `action.toml` manifest and an optional script. Users create and manage actions in Settings → Actions, which includes a library of bundled recipes. Runs are queued as background jobs (`operations/progress/jobs`). In 10xer mode, `;` then a digit runs the first ten matching actions (`integration/10xer-mode`).

## Behavior

### Definitions

- Each action loads from `$XDG_CONFIG_HOME/strata/actions/<id>/action.toml`, plus one entrypoint script beside it for Python and Bash. lgse/strata#1085
- A manifest is refused with a message if its `schema_version` is not 1, it has an unknown key, or its entrypoint is not a plain file name. lgse/strata#1085
- An `id` must start with a lowercase letter or digit and use only lowercase letters, digits, `.`, `-`, or `_`, up to 64 characters. It must match its folder name, or the action fails to load. lgse/strata#1085
- A symlinked manifest, entrypoint, or action folder is refused rather than followed. lgse/strata#1085
- An action that fails to load is listed under Problems in Settings → Actions as `<folder>: <reason>`, and the other actions still load. lgse/strata#1085
- A script whose shebang names an interpreter outside its runtime's family, such as `#!/bin/bash` for a Python action, fails to load. lgse/strata#1085 (unverified)
- A script without a shebang runs with `python3` or `bash`, looked up on the user's `PATH`. lgse/strata#1085
- If the interpreter or command program is not on `PATH`, the action's menu item is shown but insensitive, and its accessible description gives the reason. lgse/strata#1085, lgse/strata#1359
- A command `program` given as a relative path containing `/` is treated as unavailable. lgse/strata#1085 (unverified)

### Matching and menus

- An action appears only when every selected entry matches its `kinds`, `extensions`, and `mime_types`, and the selection size is between `min_items` and `max_items`. lgse/strata#1085
- Extensions match case-insensitively. Content types are guessed from the file name without reading contents, and `image/*` matches every `image/` type. lgse/strata#1085 (unverified)
- An action with `enabled = false` stays in Settings but is left out of menus. lgse/strata#1085
- The folder background menu matches actions against the open folder as a single folder input. lgse/strata#1085
- A selection that includes Trash or a non-native GVfs item shows no custom actions. lgse/strata#1085
- Actions with `menu = "top"` appear in the menu body. Others appear under an Actions submenu. Both groups are sorted by name, ignoring case. lgse/strata#1085 (unverified)
- Custom actions sit in their own section after the open, print, and extract commands and before Cut and Copy. lgse/strata#1085

### Invocation

- An action with `confirm = true` opens "Run this action?" with the action name and item count, and Run focused. Cancel runs nothing. lgse/strata#1085, lgse/strata#1206
- Programs and interpreters get argv entries directly, never through a shell. lgse/strata#1085
- A command argument that is exactly `{path}`, `{paths}`, or `{parent}` expands to absolute paths, one argument each. Other arguments pass through literally. lgse/strata#1085
- An argument with a token inside other text, such as `prefix-{path}`, is refused on save. So is `{path}` in whole-selection mode or `{paths}` in per-item mode. lgse/strata#1085
- Each invocation gets `STRATA_ACTION_*` variables for version, id, mode, source (`selection` or `background`), count, and 1-based per-item position. lgse/strata#1085
- Input paths go in a NUL-delimited, byte-exact file named by `STRATA_ACTION_PATHS`, so names with newlines or invalid UTF-8 arrive intact. lgse/strata#1085
- Each invocation gets a private 0700 scratch folder in `STRATA_ACTION_RUN_DIR`, which is removed afterwards. lgse/strata#1085
- The working directory is the invoking folder by default. Users can choose Home or the action's own folder instead. lgse/strata#1085
- A script that appends `{"event": "progress", "processed": N, "total": M}` lines to `$STRATA_ACTION_PROGRESS` updates its job's progress. lgse/strata#1085
- `{"event": "output", "path": …}` lines record an absolute output path. Relative paths, malformed lines, and unknown lines are ignored. lgse/strata#1085
- Python actions can call `from strata_actions import context` with nothing installed through pip. lgse/strata#1085
- `ctx.log` escapes non-UTF-8 bytes, so logging a native path succeeds when the locale's stdout is strict UTF-8. lgse/strata#1267

### Settings → Actions

- Each action row has an enable switch and Edit, Duplicate, Export…, and Delete buttons. lgse/strata#1085
- New action… opens an editor with General, Script, and Behavior tabs, and Create action saves all three. lgse/strata#1085
- If a field is invalid, the editor switches to that field's tab, keeps the edits, and writes nothing. lgse/strata#1085
- If Id is left blank, it is derived from Name: "Batch rename" becomes `batch-rename`. When an existing action is edited, Id is read-only. lgse/strata#1085
- Cancel, the close button, or Escape discards the draft. A click outside the dialog leaves it open. lgse/strata#1085
- Edit opens with Name focused, nothing selected, and the caret at the end. lgse/strata#1085
- Switching among Python, Bash, and Command keeps each runtime's draft until the dialog closes. Only the active runtime is saved. lgse/strata#1085
- For Python and Bash, the Script tab reports whether the interpreter is found, without running anything. A missing interpreter does not block saving. lgse/strata#1085
- The On failure choice, Continue or Stop, is insensitive until Run is set to Per item. lgse/strata#1085 (unverified)
- Duplicate creates `<id>-copy` named "<name> copy", trying `-copy-1` and so on, and never replaces an existing folder. lgse/strata#1085
- Import… copies only `action.toml` and its entrypoint. It saves the action disabled under a free id and asks the user to review the script. lgse/strata#1085
- Export… writes the action to `<chosen folder>/<id>` and refuses if that folder exists. lgse/strata#1085

### Script library

- Library on the Script tab offers 10 Python and Bash recipes. They can be searched by name, description, requirements, or input scope, and filtered by All, Files, or Media. lgse/strata#1085
- Applying a recipe sets its runtime, filters, and mode. It fills Name and Description only when they are blank, and keeps the id. lgse/strata#1085
- If the target runtime's draft has been edited, the dropdown asks Replace script or Keep draft. lgse/strata#1085
- Browsing or applying a recipe never saves or runs it. lgse/strata#1085
- Batch rename defaults to `{index:03d}_{filename}`, such as `001_photo.jpg`, numbered in Strata's selection order. lgse/strata#1085
- Rename recipes refuse empty, `.`, `..`, duplicate, or existing target names and names containing `/`. In whole-selection mode, they check every name before renaming. lgse/strata#1085
- Rename recipes use `renameat2` no-replace, so a target created after the check is not overwritten. lgse/strata#1085
- SHA-256 checksums writes `<name>.sha256` beside each file and refuses when it already exists. lgse/strata#1085
- Conversion recipes write into a new `strata-<kind>-*` folder beside each original and never overwrite the original. lgse/strata#1085
- Strip EXIF copies each original into a new `strata-original-*` folder before editing. If that copy fails, metadata is not removed. lgse/strata#1085
- A recipe whose tool, such as ImageMagick, FFmpeg, or ExifTool, is missing fails before creating or changing files. lgse/strata#1085 (unverified)

## Design

[docs/custom-actions.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/custom-actions.md) holds the manifest, invocation, and trust contract. The design was agreed in comments on lgse/strata#36.

- Actions are external processes defined by portable folders, not an in-process plugin framework. This needs no Strata SDK, no particular language, and no rebuild (lgse/strata#36).
- Settings generates and edits the same TOML manifest that users can edit by hand. There is no separate GUI-only format (lgse/strata#36).
- Python is the main runtime, with an optional standard-library helper. Bash and plain commands cover CLI tools. There is no JavaScript preset, and runtimes are never bundled or installed (lgse/strata#36).
- Actions are trusted and not sandboxed in v1. Imports start disabled. Scripts in browsed folders are never found or run (lgse/strata#36).
- Matching is declarative, so opening a menu never runs user code. Content types are guessed from names only (lgse/strata#36).
- Every selected item must match, so an image-only action never runs on part of a mixed selection (lgse/strata#36).
- Paths go in files rather than argv or the environment. This keeps bytes exact and avoids command-line limits, so a whole-selection run is never split (lgse/strata#36).
- Action interpreters resolve on the user's `PATH`, including shims. Strata's own helpers use only fixed trusted roots (lgse/strata#1055, lgse/strata#1085).
- A broken definition is reported under Problems and never hides other actions (lgse/strata#1085).
- Rename recipes are not transactions and offer no undo. Cancelling or an I/O error can leave earlier files renamed (lgse/strata#1085).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-20 | lgse/strata#1085 | feat | Added manifest-defined Python, Bash, and command actions with a Settings editor and recipe library, as agreed in lgse/strata#36. |

## Known gaps

- Actions accept only native local paths. Trash, remote mounts, and the file chooser are excluded. lgse/strata#36, lgse/strata#1085
- Built-in parameter forms and enforced sandboxing were deferred from the first release. lgse/strata#36
