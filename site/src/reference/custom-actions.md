---
nodes: [integration/custom-actions, operations/progress/jobs, integration/10xer-mode/file-verbs, browser/context-menu, remote/file-providers/external]
reviewed_at: 0a086aa3bdb251842a1e8413e2a6b35970d0b409
---

# Custom actions reference

Custom actions add your own scripts to the file and folder context menus. In
[10xer mode](10xer-mode.md), **;** then **1**–**9** / **0** runs the first
ten matching actions that can run on the focused item or filled selection;
actions whose interpreter or program is missing are skipped.

They are ordinary programs running with your permissions. There is no sandbox and
no install step beyond enabling an action. Strata validates the definition and the
files around it, prepares private invocation files, and reports progress and
results; it does not restrict what a script may do.

## Where actions live

<!-- node: integration/custom-actions, Definitions -->
<!-- node: integration/custom-actions, Settings → Actions -->

```text
$XDG_CONFIG_HOME/strata/actions/
  checksums/
    action.toml
    run.sh
```

One directory per action, named after its `id`, containing `action.toml` and
optionally one script beside it. Settings → Actions creates, edits, duplicates,
imports, and exports these files. You can also edit them by hand. Context menus
and the 10xer **;** list reread the manifests each time they open, so hand edits
apply the next time you open one. Once **Settings → Actions** has been opened in
a window, every window keeps the manifests loaded at that moment until each
window where it was opened closes; closing Settings does not release them. In
that time Strata rereads them only after Settings → Actions creates, saves,
duplicates, imports, or deletes an action, and **Save changes** or the enable
switch writes the loaded values back over your manifest edits. Restarting Strata
always picks up hand edits. The editor reads the script itself from disk each
time it opens.

Actions are ordinary, user-owned folders under
`${XDG_CONFIG_HOME:-$HOME/.config}/strata/actions/`. The folder name and manifest
`id` must match. Use a new lowercase kebab-case id; do not overwrite an existing
action. Create directories with mode `0700` and manifest/script files with mode
`0600`. Entry points are regular files with plain filenames, not symlinks or
paths. Scripts need no executable bit: Strata invokes the interpreter. Command
actions have only a manifest. Import/export transfers the manifest and declared
entrypoint, not arbitrary helper files. After hand-writing files, restart Strata
if Settings → Actions has been opened since it started, then review and enable
the action in Settings → Actions.

## Creating an action

<!-- node: integration/custom-actions, Settings → Actions -->
<!-- node: integration/custom-actions, Script library -->
<!-- node: integration/10xer-mode/file-verbs, Open With and actions -->

Choose **Settings → Actions → New action…**. The editor has three tabs:

- **General**: name, directory id, description, bundled icon, and enabled state.
  Leave the id blank to derive it from the name.
- **Script**: choose Python, Bash, or Command. Scripts have a line-numbered editor;
  commands take an installed program and one argument per line. Switching runtimes
  keeps each script draft until you close the dialog; only the runtime selected
  when you save is written. For Python and Bash, a runtime
  indicator checks the declared shebang (or default interpreter) against the same executable lookup
  used when loading actions. Python uses the script's shebang, or `python3` when
  there is none. Availability is checked automatically when the
  dialog opens; reopen it after installing a runtime.
  Bash/Command do not require Python. This does not execute anything or validate
  script syntax, dependencies such as ImageMagick, FFmpeg, or ExifTool, or
  behavior; missing runtimes do not prevent saving a draft.
- **Behavior**: execution mode, per-item failure policy, working folder, menu
  placement, file/folder filters, selection limit, and confirmation. **On
  failure** (**Continue** or **Stop**) can be changed only when **Run** is set to
  **Per item**.

The editor opens with Name focused, nothing selected, and the caret at the end.
**Create action** saves all three tabs together. Invalid fields bring you back to
that tab without discarding your edits. Clicking outside the dialog leaves it open;
**Cancel**, the close button, or **Escape** discards the draft.
Existing actions use the same editor with **Save changes**; their id stays fixed.
Creating or duplicating an action never replaces an existing action directory.
Manifest-only MIME filters and minimum selection counts survive editor saves.
Command arguments preserve literal whitespace and empty lines; unchanged arguments
containing embedded newlines are also retained.

### Managing actions

Each action row in **Settings → Actions** has an enable switch and **Edit**,
**Duplicate**, **Export…**, and **Delete** buttons.

- **Duplicate** creates `<id>-copy` named “<name> copy”, then tries `<id>-copy-1`,
  `<id>-copy-2`, and so on.
- **Export…** asks for a folder and writes the action to `<chosen folder>/<id>`.
  It refuses if that folder already exists.
- **Import…** asks for an action folder and copies its `action.toml` and
  entrypoint. It saves the action disabled under a free id (`<id>`, then
  `<id>-1`, `<id>-2`, …) and tells you to review its script before enabling it.
- **Delete** asks **Delete this action?**, with **Delete** focused. Confirming
  removes the action folder and its script from your actions directory.

### Script examples

Open **Library** on the Script tab to browse bundled Python and Bash recipes in a
dropdown attached to the editor. Search names, descriptions, requirements, input
scope, category, or runtime; every word you type must match. Narrow the list
with **All**, **Files**, or **Media**. Each template shows its language, purpose,
run mode/input scope, and required tools:

| Example | Extra requirements | Result |
| --- | --- | --- |
| Log selected paths | None | Log paths and report progress without changing files |
| Convert images to WebP | ImageMagick (`magick` or `convert`) | First frame, quality 85, in `strata-webp-*/converted.webp` |
| Resize images to 1024px | ImageMagick (`magick` or `convert`) | First frame, aspect-preserving PNG, never enlarged, in `strata-resize-*/resized.png` |
| Convert videos to MP4 | FFmpeg with `libx264` and AAC | H.264/AAC copy in `strata-mp4-*/converted.mp4` |
| Extract MP3 audio | FFmpeg with `libmp3lame` | First audio stream in `strata-mp3-*/audio.mp3`; fails if there is no audio |
| SHA-256 checksums | None | Adjacent `<original-name>.sha256`, compatible with `sha256sum --check` from the original folder |
| Batch rename | Python 3 + Linux `renameat2` support | Rename regular files in place with a numbered pattern; never overwrite another name |
| Strip EXIF metadata | Bash + ExifTool + coreutils | Remove writable metadata in place after copying the original into a fresh adjacent `strata-original-*` folder |
| Lowercase file names | Python 3 + Linux `renameat2` support | Lowercase names and replace spaces with dashes, using the same collision-safe engine as Batch rename |
| Count lines | Bash + `wc` (coreutils) | Log each file's newline count and the total, without changing files |

Python recipes need Python 3 but no pip packages; Bash recipes do not need
Python. Strata does not install tools. A recipe whose ImageMagick, FFmpeg, or
ExifTool command is not on your `PATH` fails before it creates or changes any
file.
Conversion outputs go into fresh, private folders **beside each original**;
conversions never overwrite originals. EXIF stripping instead edits the working
photo after making a private backup, as described below. Existing checksum files
and symlinks are refused, not
replaced. A failed or cancelled conversion may leave a partial output folder.
Review scripts and use trusted input files: media tools and actions are not
sandboxed.

Applying a recipe selects its runtime and sets suitable file filters and run mode.
Conversions, checksums, and EXIF stripping select **Per item**; the starter,
rename/lowercase, and line-count recipes select **Whole selection**, even if the
previous draft used the opposite mode. A blank Name or Description, or one still
showing the previously applied recipe's text, takes the recipe's name and
description; a name or description you typed, the id, and other settings are
kept. Choose a template to load it into the editor for review; the editor then
shows the Script tab with the recipe loaded. If the target runtime's script is
not blank and differs from the starter template (your edits, an earlier recipe,
or an existing action's script), the dropdown first asks you to **Replace
script** or **Keep draft**, without opening another dialog.
Code replacement can be undone in the editor; drafts for the other runtimes are retained.
**Escape** or clicking outside closes only the dropdown, leaving the editor open.
Searching, browsing, or applying a template never saves or executes it. Review
and save the action, then launch it from its file/folder context menu or, in
10xer mode, **;** then a digit. The digits follow context-menu order. A vacant
digit flashes `No action N` and runs nothing. A digit pressed after the targets
or the action list changed flashes `Selection changed` or `Actions changed` and
runs nothing; see [10xer mode](10xer-mode.md).

The documented Python starter and every Python recipe include the same maintained
[`context()` reference](https://github.com/lgse/strata/blob/0a086aa3bdb251842a1e8413e2a6b35970d0b409/data/actions/context-api.txt) as a module docstring.
Examples are starting points: edit the output format, quality, resize limit,
FFmpeg flags, or filters before saving. Shared rename-recipe code is embedded
into the inserted script, so saved recipes do not depend on files in Strata's
source checkout.

**EXIF stripping:** only regular, non-symlink photos are accepted. Each original
is copied completely into a new private folder before ExifTool replaces the
working photo; repeated runs keep separate backups. If the backup copy fails,
that photo's metadata is left untouched. Failed or cancelled copies may leave
partial backup folders, and cancellation does not restore earlier changes. Removing writable metadata can remove orientation/color profiles and
is not a guarantee that every format is anonymized. Review results before
removing backups.

**Count lines:** `wc -l` counts newline characters; an unterminated final line is
not counted. Whole-selection mode gives a total across the supplied selection.

### Batch rename

The **Batch rename** recipe defaults to `PATTERN = "{index:03d}_{filename}"`,
producing names such as `001_photo.jpg`. Edit the pattern, or replace
`new_name(context)` with your own Python logic returning a single filename.
Its per-file context provides:

- `filename`: original name including its extension.
- `stem` and `suffix`: name without its last extension, and that extension with
  its leading dot (empty if absent).
- `index`: **1-based** position in Strata's supplied selection order, not click
  order; `total`: number of files in the job.
- `path`: original absolute `pathlib.Path`.
- `batch`: the full Strata `context()` object documented below, including logging
  and progress methods. These per-file fields belong to this recipe, not the
  general helper.

Patterns accept `filename`, `stem`, `suffix`, `index`, and `total`. For example,
`"photo_{index:04d}{suffix}"` produces `photo_0001.jpg`. The default whole-selection
mode checks the entire plan before renaming anything. Changing to per-item mode
keeps the job-wide index but can only preflight one file at a time.

Names cannot contain directory separators or be empty, `.` or `..`. Duplicate
inputs/destinations, existing destinations (including symlinks), folders, and
symlink inputs are refused. Unchanged names are skipped; swaps into other selected
names are not supported. Every move uses Linux's atomic no-replace operation,
including if another process creates the destination after preflight. Missing
support fails rather than falling back to an overwriting rename. Some filesystems
may refuse case-only changes. **Lowercase file names** uses the same engine and
safety rules, with an editable `new_name(context)` transformation instead of a
numbering pattern.

File contents are unchanged, but original **names** change. This is not an atomic
batch or an undo feature: cancellation, concurrent filesystem changes, or an I/O
error can leave earlier files renamed. Review the script and try it on copies first.

## Manifest

<!-- node: integration/custom-actions, Definitions -->
<!-- node: integration/custom-actions, Invocation -->

```toml
schema_version = 1
id = "checksums"
name = "Generate checksums"
description = "Writes a sha256 file next to each selection."
icon = "file-code"
enabled = true
menu = "submenu"

[when]
kinds = ["file"]
extensions = ["zip", "tar"]
min_items = 1

[run]
runtime = "bash"
entrypoint = "run.sh"
mode = "whole-selection"
on_error = "continue"
working_directory = "parent"
confirm = false
```

| Field | Meaning |
| --- | --- |
| `schema_version` | Must be `1`. A newer version is refused with an explanation. |
| `id` | Directory name, up to 64 characters: lowercase letters, digits, `.`, `-`, `_`, starting with a letter or digit. It must equal the folder name, or the action fails to load. Cannot change later. |
| `name` | Menu label, 1–64 characters. |
| `description` | Optional accessible description, 1–240 characters. |
| `icon` | Bundled Lucide icon slug, for example `play`, `terminal`, `image`. |
| `enabled` | `false` keeps the action in Settings but out of menus. |
| `menu` | `submenu` (default) groups the action under **Actions**; `top` puts it in the menu body. |
| `[when].kinds` | `file`, `folder`, or both. Empty means either. |
| `[when].extensions` | Extensions without dots, matched regardless of case. Empty means any. |
| `[when].mime_types` | Guessed content types such as `image/*` or `image/png`. |
| `[when].min_items` / `max_items` | Selection size bounds. `min_items` defaults to 1 and `max_items` to no limit; both lie between 1 and 10,000, and `max_items` cannot be smaller than `min_items`. |
| `[run].runtime` | `python`, `bash`, or `command`. |
| `[run].entrypoint` | Script file name beside `action.toml` (Python and Bash only). |
| `[run].program` / `[run].args` | Program and arguments (command actions only). |
| `[run].mode` | `whole-selection` (default) invokes once with every path; `per-item` invokes once per path. |
| `[run].on_error` | `continue` (default) or `stop`, used by `per-item` runs. |
| `[run].working_directory` | Where the process starts (**Working folder** in the editor). `parent` (default, **Invoking**) is the invoking folder, which for a folder-background run is that folder itself; `home` (**Home**) is your home folder; `action` (**Action**) is the action's own directory. |
| `[run].confirm` | Ask once before queuing the entire job (see [Confirmation](#confirmation)). |

Validation is strict: unknown keys, unsupported versions, invalid ids, entrypoints
that are not a plain file name, and argument tokens that do not match the execution
mode are all refused with a message rather than being ignored. A manifest lists
at most 64 extensions, 64 content types, and 32 command arguments. An extension
is at most 24 characters, with no leading dot, `/`, `\`, `*`, or whitespace.

## Matching

<!-- node: integration/custom-actions, Matching and menus -->
<!-- node: browser/context-menu -->

An action appears when **every** currently selected entry satisfies `[when]`, and
the selection size is within `min_items`/`max_items`. A mixed selection therefore
never runs an action on a subset the author did not intend to accept.
Extensions match regardless of case, so `jpg` matches `photo.JPG`. Content types
are guessed from the file name alone; Strata never reads file contents to match
an action. `image/*` matches every `image/` type.

Opening the folder background menu offers the same rules with the folder itself as
the single input. Actions are only offered for native paths: Trash, GVfs, and other
non-native locations are excluded in this release.

Custom actions occupy a separate section after the opening, printing, and extract
commands and before Cut/Copy. Actions with `menu = "top"` are listed first in that
section of the menu body, followed by the **Actions** submenu row, with a play
icon, holding the rest. Both groups are sorted by name, ignoring case. The context menu uses GTK's native nested menu model: hover over
**Actions** to open its submenu, then move onto an action to highlight it.
Hovering another menu item closes the submenu. Clicking or keyboard activation
also opens it. On the **Actions** row, **Right**, **Space**, or **Enter** opens
the submenu with its first action focused; **Left** closes only the submenu and
refocuses its row. An outside click or **Escape** dismisses the menu. Long filenames and
paths use middle ellipsis, preserving their beginning and extension.

## How an invocation runs

<!-- node: integration/custom-actions, Invocation -->

Nothing is ever passed through a shell. Programs and interpreters receive argv
entries directly, and every path is absolute, so a selected file name can never be
read as a command or as an option such as `-rf`.

| Environment variable | Contents |
| --- | --- |
| `STRATA_ACTION_VERSION` | Protocol version, currently `1`. |
| `STRATA_ACTION_ID` | Definition identity; the display name is in context JSON. |
| `STRATA_ACTION_MODE` | `per-item` or `whole-selection`. |
| `STRATA_ACTION_SOURCE` | `selection` or `background`. |
| `STRATA_ACTION_COUNT`, `STRATA_ACTION_POSITION` | Input count, and 1-based position for per-item runs. |
| `STRATA_ACTION_PATHS` | File containing every input path, NUL-delimited and byte-exact. |
| `STRATA_ACTION_PARENT` | File containing the invoking folder. |
| `STRATA_ACTION_PROGRESS` | File to append progress events to (see below). |
| `STRATA_ACTION_CONTEXT`, `STRATA_ACTION_RUN_DIR` | JSON context and private scratch directory, mode 0700. |
| `STRATA_ACTION_DIR` | The action's own directory. |

Paths travel in files rather than in the environment so unusual names — spaces,
newlines, and bytes that are not valid UTF-8 — survive exactly.

For a Bash script, the manifest's `[run]` section uses `runtime = "bash"`,
`entrypoint = "run.sh"`, and `mode = "whole-selection"`. Example `run.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail
while IFS= read -r -d '' path; do
    printf 'Selected: %q\n' "$path"
done < "$STRATA_ACTION_PATHS"
```

`STRATA_ACTION_PATHS` is the **name of a file containing NUL-delimited paths**,
not a whitespace-separated list. Always quote paths; never use `for path in
$(cat ...)` or `eval`. `STRATA_ACTION_COUNT` is invocation-local;
`STRATA_ACTION_POSITION` is the 1-based per-item position. The invoking folder is
stored byte-exactly in the file named by `STRATA_ACTION_PARENT`.

`whole-selection` runs the action once with every selected path. `per-item` runs it
once per path and tracks succeeded, failed, and remaining counts itself; with
`on_error = "stop"` the first failure ends the job.

### Confirmation

With `confirm = true`, choosing the action opens **Run this action?** with the
action's name and icon. It reads “This runs “<name>” on <n> selected items.”, then
the action's description, with **Run** focused. **Cancel** or the close button
runs nothing.

### Command argument tokens

`args` entries are either literal text without `{` or `}`, or exactly one of:

- `{path}` — the single input of a per-item run.
- `{paths}` — every input of a whole-selection run, as separate arguments.
- `{parent}` — the invoking folder.

Any other argument containing a brace, such as `prefix-{path}` or `{}`, is
refused, so nothing is ever interpolated into a command line. Use a Bash action
if a program needs literal braces.

For an installed executable, `[run]` looks like this—no script file:

```toml
[run]
runtime = "command"
program = "sha256sum"
args = ["--", "{paths}"]
mode = "whole-selection"
```

Programs receive direct argv, not shell source: pipes, redirection, `$VARIABLE`,
and globbing are not expanded. Use Bash if shell syntax is needed.

## Progress and results

<!-- node: integration/custom-actions, Invocation -->
<!-- node: operations/progress/jobs, Queue -->
<!-- node: operations/progress/jobs, Dashboard -->

Process exit status decides success: `0` means the invocation succeeded and any
other status means it failed. Reported percentages are presentational only.

A script may optionally report measurable progress by appending one JSON object per
line to `$STRATA_ACTION_PROGRESS`:

```json
{"event": "progress", "processed": 42, "total": 100, "message": "Converting images"}
{"event": "output", "path": "/home/you/Pictures/out.webp"}
```

- `processed` is required and bounded; `total` and `message` are optional.
- `output` records a created location: absolute paths only, which is why a relative
  path is ignored rather than guessed.
- Malformed or unknown lines are ignored, the file is read incrementally, and both
  the file and the number of events per invocation are bounded.

Whole-selection scripts that never report a total still appear as **Running**
with elapsed time and an indeterminate indicator. A per-item job's bar fills by
completed items, plus the current item's reported fraction. stdout and stderr are captured as bounded output
for the Jobs dashboard; they are not the progress channel.

## Python helper

<!-- node: integration/custom-actions, Invocation -->

Python actions can use the bundled standard-library helper, which is importable
inside a run and needs no `pip install`. In this sketch, `convert` stands for your
own function that writes `<path>.webp`:

```python
#!/usr/bin/env python3
from strata_actions import context

ctx = context()
for index, path in enumerate(ctx.paths, start=1):
    convert(path)
    ctx.progress(index, len(ctx.paths), "Converting images")
    ctx.output(f"{path}.webp")
```

`ctx.paths` are `str` values decoded with `surrogateescape`, so use
`ctx.paths_bytes()` when a tool needs the original bytes. `ctx.single` returns
the sole path for a one-item invocation, or `None`. `ctx.count` counts inputs in
this invocation, not the entire per-item job. `ctx.position` and `ctx.total` are
the 1-based job position and job size in **Per item** mode, otherwise `None`;
whole-selection scripts enumerate `ctx.paths` themselves.

A script that only logs the selection, as `main.py` with `runtime = "python"` and
`entrypoint = "main.py"`:

```python
#!/usr/bin/env python3
from pathlib import Path
from strata_actions import context

ctx = context()
for index, path in enumerate(ctx.paths, start=1):
    ctx.log(f"{index}: {Path(path).name}")
    ctx.progress(index, ctx.count, "Logging selected files")
```

Other properties are `parent` (invoking folder, not necessarily the working
directory), `directory` (action directory), `run_directory` (private scratch,
removed after the invocation), `action_id`, `version`, `metadata` (raw JSON),
`mode`, `source`, and the optional 1-based per-item `position` and `total`.
`ctx.log(message)` writes to captured stdout. Bytes that are not Unicode
are escaped, so logging a native path still succeeds when the locale uses a
strict UTF-8 stdout. `ctx.progress(processed,
total=None, message=None)` reports invocation-local work; `ctx.output(path)`
reports an absolute output path, but does not create a file. Output reporting is
best-effort: names containing non-UTF-8 bytes cannot be represented by the JSON
progress channel and produce a warning rather than failing the action.

Import `find_tool(name)` to look up an executable (returns its path or `None`), or
`require_tool(name)` to raise `ContextError` when a dependency is missing.

Any other language can follow the same contract: read the paths file, write the
progress file, and exit with a status.

## Jobs and cancellation

<!-- node: operations/progress/jobs, Queue -->
<!-- node: operations/progress/jobs, Dashboard -->
<!-- node: operations/progress/jobs, Cancellation -->

Each invocation runs in the background. Queuing an action automatically opens
Jobs in the **launching window**, with that new job first, showing its
queued/running state, progress, and elapsed time; **Details** shows its output.
Confirmation actions open Jobs only after you choose **Run**. This presentation does not change queue execution order
or open dashboards in other windows. A **Jobs** button appears in the footer only
while jobs exist. It reads, for example, “2 jobs running · 1 queued”, or “3 jobs
finished” when none are active, with “ · failures” added when any job failed.
Clicking it reopens the dashboard.

Minimizing, pressing **Escape**, or clicking away only hides the dashboard. Progress
and completion updates do not reopen it; launching another action does.
**Remove** on a queued job ends it as Cancelled (“Removed before starting”)
without running it. **Cancel** on a running job shows “Cancelling…” and sends
SIGTERM to its whole process group, then SIGKILL after 2 seconds. A job still
cancelling after 10 seconds is marked Cancelled (“Cancelled; the action did not
stop cleanly”) and frees its slot. Closing the last application window while jobs
are queued, running, or cancelling shows **Background jobs are still active** and
keeps the window open; finish or cancel them in Jobs first. Other windows may
close without interrupting work.

An invocation ends when its direct process exits. Output capture and scratch
files are then closed without waiting for background descendants. Scripts should
wait for subprocesses that need the invocation's context or captured output.

Up to 20 finished jobs (successes, failures, and cancellations) stay for the
current session. The oldest finished jobs are dropped first; active jobs never
are. The dashboard lists at most 12 jobs, then shows “<n> older jobs are hidden”.
**Details** expands captured output and **Hide** collapses it; a queued job has no
**Details** yet. Details shows “No output yet.” until output arrives. On a running
job it streams new output and follows the bottom until you scroll up, then follows
again once you scroll back down. The header summarizes running, queued, and
finished jobs. Each row shows the action's name and icon, a theme-accent status
(“Queued”, “Cancelling…”, or “Running for”, “Done in”, “Failed after”, or
“Cancelled after” with the elapsed time), and a check or X for finished results.
Below it, the row lists the script's latest message, progress counts such as
`3/10` (plus “<n> failed” in a per-item job), and the invoking folder, shown as
Home or `~/…` under your home folder. Failure
output appears only in Details, not a separate banner.
The dashboard opens above the footer without covering it.
Icon-only buttons retain tooltips; controls retain accessible names. **Minimize** keeps history;
**Dismiss** removes one finished job,
and **Clear finished** removes finished history without disturbing active work.

Cancelling stops the work that has not happened yet. It does not roll back changes
already written to disk, and Strata does not retry a failed or cancelled action.

## Trust model

<!-- node: integration/custom-actions, Definitions -->
<!-- node: integration/custom-actions, Settings → Actions -->
<!-- node: operations/progress/jobs, Queue -->
<!-- node: operations/progress/jobs, Dashboard -->

- Actions are trusted local programs. Out-of-process execution is not a filesystem
  or network boundary; a script can do anything you can do.
- Imported actions arrive **disabled**. Review the script before enabling it.
  Import copies only `action.toml` and its entrypoint.
- Strata never discovers or runs scripts found in browsed folders, and never
  installs runtimes, interpreters, or packages. A missing interpreter or program
  leaves the action visible but disabled, with the reason in its accessible description.
- Interpreters and programs are looked up on your `PATH`. A script without a
  shebang runs with `python3` or `bash`. A shebang outside the runtime's family,
  such as `#!/bin/bash` in a Python action, makes the action fail to load and
  appear under **PROBLEMS**. A `program` written as a relative path containing `/`
  counts as unavailable; use a bare name or an absolute path.
- Manifests and generated scripts are written owner-only (0600) inside an
  owner-only directory, and entrypoints are read as regular files: a symlinked
  manifest, entrypoint, action directory, or scratch directory is refused rather
  than followed.
- Each invocation keeps the newest 8 KiB of stdout and stderr, starting with “…”
  when trimmed, and a job keeps the newest 64 KiB across invocations. Terminal
  colour and control sequences are stripped, and the rest is shown as plain text.

## Limitations

<!-- node: integration/custom-actions -->
<!-- node: operations/progress/jobs, Queue -->

- Local native locations only; Trash, remote mounts, and the file chooser are out.
- `per-item` runs are sequential, and at most two jobs run at once.
- Whole-selection commands that cannot report progress show no percentage.
- There is no sandbox, no restart/resume, and no built-in parameter form; a script
  that needs options reads them from its own file or environment.
- Editing an action's script from Settings replaces the whole file; keep large
  scripts in version control if you edit them outside Strata.

## Testing an action

<!-- node: integration/custom-actions, Definitions -->
<!-- node: integration/custom-actions, Settings → Actions -->
<!-- node: operations/progress/jobs, Dashboard -->

Enable it, then right-click a file that matches `[when]` and choose it. The Jobs
dashboard shows the invocation, its output, and its exit status. A definition that
cannot load appears under **Settings → Actions → PROBLEMS** as
`<folder>: <reason>`, and never silently disappears from the menus; the other
actions still load. **PROBLEMS** carries the note “These files could not be loaded.
Fix them in the actions folder, or remove them.” Settings search finds the action
list and **PROBLEMS** as “Custom actions”, **New action…** as “New custom action”,
and **Import…** as “Import custom action”.

When a coding agent writes an action for you: choose a fresh id, write the
matching manifest and entrypoint, declare required tools, preserve
originals/refuse overwrites, and keep the action disabled for review. Test on
disposable copies through Strata's context menu, then inspect Jobs output.

## Service-dependent actions and badges

<!-- node: remote/file-providers/external -->
<!-- node: integration/custom-actions, Matching and menus -->

For asynchronous eligibility based on external state and live file decorations,
see [External file providers](file-providers.md). Static action matching remains
limited to the file/selection filters described above; a provider can keep its
menu entirely absent outside the locations it supports.
