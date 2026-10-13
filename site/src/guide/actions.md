---
nodes: [integration/custom-actions]
reviewed_at: 0a086aa3bdb251842a1e8413e2a6b35970d0b409
---

# Custom actions

Add your own scripts to the right-click menu. An action is a folder with a
small `action.toml` and, usually, one script. Strata runs it in the background
and shows its progress and output in the Jobs dashboard.

## Your first action

<!-- node: integration/custom-actions, Settings → Actions -->
<!-- node: integration/custom-actions, Script library -->

1. Open **Settings → Actions** and click **New action…**.
2. On **General**, type `Count lines` in **Name**. Leave **Id** blank; Strata
   derives `count-lines` from the name.
3. On **Script**, click **Library** and pick **Count lines**. This Bash
   recipe needs only `wc` and offers the action only for text files such as
   `.txt` and `.md`.
4. Click **Create action**.
5. Select a few `.txt` or `.md` files, right-click, and choose
   **Actions → Count lines**.

The Jobs dashboard opens with the new job. Click the eye button (**Details**)
on the job to read each file's count and the total.

## What is on disk

<!-- node: integration/custom-actions, Definitions -->
<!-- node: integration/custom-actions, Matching and menus -->

Settings wrote this, and you can edit it by hand:

```text
~/.config/strata/actions/count-lines/
  action.toml
  run.sh
```

The folder name must match the `id`. A short working manifest is:

```toml
schema_version = 1
id = "count-lines"
name = "Count lines"
icon = "file-code"

[when]
kinds = ["file"]

[run]
runtime = "bash"
entrypoint = "run.sh"
```

The `[when]` table decides when the action shows up. Add
`extensions = ["md", "txt"]` to limit it to those files, or set
`kinds = ["folder"]` for folders. The action appears only when every selected
item matches. The menu rereads your files each time it opens, so a hand edit
shows up on your next right-click. If you opened **Settings → Actions** since
Strata started, restart Strata first.

## Writing a script in Python

<!-- node: integration/custom-actions, Invocation -->

Python actions can import a helper with no `pip install`. This script converts
each selected image to WebP beside the original:

```python
#!/usr/bin/env python3
import subprocess
from strata_actions import context, require_tool

ctx = context()
magick = require_tool("magick")
for index, path in enumerate(ctx.paths, start=1):
    target = f"{path}.webp"
    subprocess.run([magick, path, target], check=True)
    ctx.progress(index, ctx.count, "Converting images")
    ctx.output(target)
```

A new action starts as **Python** with `main.py` and a starter script;
replace the starter with this one. On **Behavior**, clear **Folders** and set
**Extensions** to `png, jpg, jpeg`. In the manifest that is `runtime = "python"`
and `entrypoint = "main.py"`.

`ctx.paths` holds the selected absolute paths, `ctx.progress` fills the
progress bar, and `ctx.output` records where a result went. `require_tool`
stops the run when a program is missing, and any non-zero exit marks the job
failed.

## Running an existing program instead

<!-- node: integration/custom-actions, Invocation -->

Choose **Command** under **Runtime**, name the **Program**, and enter one
argument per line under **Arguments**. On **Behavior**, clear **Folders** and
set **Extensions** to `jpg, jpeg, png`. In the manifest:

```toml
[when]
kinds = ["file"]
extensions = ["jpg", "jpeg", "png"]

[run]
runtime = "command"
program = "magick"
args = ["mogrify", "-resize", "1024x1024>", "{paths}"]
confirm = true
```

`{paths}` expands to every selected file, one argument each, and nothing goes
through a shell.
`mogrify` overwrites the originals, so `confirm = true` asks before running.
In Settings that is the **Confirm** switch on **Behavior**.

## Good to know

<!-- node: integration/custom-actions, Definitions -->
<!-- node: integration/custom-actions, Matching and menus -->
<!-- node: integration/custom-actions, Settings → Actions -->

- Actions run with your permissions and no sandbox. Read a recipe before you
  save it. Actions you add with **Import…** arrive disabled.
- `mode = "per-item"` runs the action once per file. Use `{path}` there
  instead of `{paths}`.
- In [10xer mode](10xer.md), press `;` then `1`–`9` or `0` to run one of the
  first ten matching actions.
- Actions are not offered in Trash or on remote locations.
- A manifest that fails to load is listed under **PROBLEMS** in
  **Settings → Actions** with the reason. Your other actions still load.

**Full detail:** the [Custom actions reference](../reference/custom-actions.md)
covers every manifest field, environment variable, and recipe.
