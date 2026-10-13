---
nodes: [browser/search, browser/search/filter, browser/search/exclusions]
reviewed_at: 0a086aa3bdb251842a1e8413e2a6b35970d0b409
---

# Find files

Press Ctrl+F to narrow the folder you are looking at. Press Ctrl+K to search
Home and every mounted local drive, from any folder.

## Filter the current folder

<!-- node: browser/search/filter, Opening and closing -->
<!-- node: browser/search/filter, Matching -->
<!-- node: browser/search/filter, Scope -->
<!-- node: browser/search/filter, Results -->

1. Open a folder and press Ctrl+F, or click the funnel button in the pane.
2. Type part of a name, such as `invoice`.
3. Press Down to reach the results, then Enter to open one.
4. Press Escape to get the full listing back.

You can skip Ctrl+F. With **Type to search** on, the default, start typing in
a file view and the filter opens with what you typed. Press `/` to open an
empty filter.

The filter searches the current folder and its subfolders, showing each
subfolder result's path below its name. Queries match names only, ignoring
case.

| Query | Finds |
| --- | --- |
| `invoice` | Any name containing `invoice`. |
| `trahs` | `strata-trash.svg`. Queries of 4 or more letters and digits forgive one typo. |
| `*.pdf` | Names ending in `.pdf`. |
| `IMG*.MOV` | Names starting with `IMG` and ending in `.MOV`. |

`*` is the only wildcard; `?` and `[]` match themselves.

Results act like normal items: drag them, copy them, or right-click for the
item menu. Space previews the selected file.

## Search everywhere

<!-- node: browser/search, Opening and scope -->
<!-- node: browser/search, Matching and results -->
<!-- node: browser/search, Keyboard and activation -->

1. Press Ctrl+K, or click the search button in the header.
2. Type a name or a piece of a path, such as `cat-01`.
3. Press Up and Down to pick a result, then Enter, or click it, to open it.

Matching is fuzzy: the characters you type must appear in order, in the name or
the path. `cat-01` lists `cat-01-photo.jpg` first, and
`bucket-cat/file-01-noise.jpg` below it.

- Opening a folder goes into that folder.
- Opening a file shows it selected in its folder, with quick preview open.
- Alt+Enter, or right-click → **Open containing folder**, opens the result's
  parent folder with the result selected.

Press Escape, or Ctrl+K again, to close search.

Search indexes Home and every mounted local drive, but skips:

- hidden files and folders, unless hidden files are shown (Ctrl+H);
- generated trees such as `node_modules/`, `target/`, `.venv/`, `.cache/`,
  `__pycache__/`, and `go/pkg/mod/`;
- anything a `.gitignore` or `.ignore` file excludes;
- folders you exclude yourself.

## Choose what search skips

<!-- node: browser/search/exclusions, Editing -->
<!-- node: browser/search/exclusions, Validation -->
<!-- node: browser/search/exclusions, Effect on search -->

Keep a large or private folder out of Ctrl+K results:

1. Press Ctrl+, to open Settings, and choose **General**.
2. Under **Search & filtering**, find **Global search exclusions**.
3. Type a rule, or click **Browse…** to pick a folder.
4. Press Enter or click **Add**.

A rule is a folder name or a directory path:

| Rule | Skips |
| --- | --- |
| `build` | Every folder named `build`, in any case, and everything inside it. |
| `~/LargeData` | That one folder and everything below it. |

A rule containing `/` is a path and must start with `/` or `~/`, so
`project/build` is refused. A folder name is matched literally, with no
wildcards. Changes apply the next time you open Ctrl+K. To delete a rule,
click the remove button beside it.

## Good to know

<!-- node: browser/search, Opening and scope -->
<!-- node: browser/search, Matching and results -->
<!-- node: browser/search/filter, Scope -->
<!-- node: browser/search/exclusions, Effect on search -->

- Exclusions apply to Ctrl+K only. The Ctrl+F filter still finds files inside
  excluded folders.
- Ctrl+K does not search remote shares. Inside a share, Ctrl+F narrows the
  loaded listing without searching subfolders.
- Ctrl+K shows at most 100 results. On a very large disk, indexing stops early
  and the footer shows **Partial results**; excluding big folders helps.
- In **Settings → General**, turn off **Include subfolders** to filter only
  the current folder, or turn on **Open search results directly** to launch
  files from Ctrl+K instead of previewing them.
- In [10xer mode](10xer.md), press F to filter and S to search
  subfolders instead of Ctrl+F.
