---
nodes: [integration/10xer-mode, integration/10xer-mode/file-verbs, integration/10xer-mode/places, integration/10xer-mode/search, integration/10xer-mode/preview-keys, integration/10xer-mode/file-chooser]
reviewed_at: 0a086aa3bdb251842a1e8413e2a6b35970d0b409
---

# 10xer mode

Press Ctrl+Shift+M for a Yazi-style keymap: letters become commands and `j`
and `k` move. Press it again to go back.

## What 10xer mode changes

<!-- node: integration/10xer-mode, Chrome and Settings -->
<!-- node: integration/10xer-mode, Keymap ownership -->

- **Letters are commands.** Typing `d` asks to trash the item; it no longer
  starts a filter.
- **Less chrome.** The window's Search button, each pane's close, filter,
  refresh, and sort controls, and the List and Icons pane header hide.
- **The footer is the command line.** Prompts such as `filter:` and `go ›`
  open there, and a chord such as `g` lists its next keys above it.
- **F1 lists only 10xer keys.** Press F1 or `~` to see what runs now.
- **Some default keys change.** Space selects instead of previewing, Ctrl+R
  inverts the selection, Ctrl+B and Ctrl+F page up and down, and Ctrl+N shows
  or hides the sidebar.

Ctrl+C, Ctrl+X, Ctrl+V, Ctrl+Z, Ctrl+K, and Ctrl+L work as in the
[default map](keyboard.md).

## Turn it on and off

<!-- node: integration/10xer-mode, Entering and leaving -->
<!-- node: integration/10xer-mode, Leaving the mode -->
<!-- node: integration/10xer-mode/file-chooser, Following the mode -->

1. Press Ctrl+Shift+M, or press Ctrl+, and turn on **10xer mode** under
   **BROWSING** in **General**.
2. Check for the **10X** pill at the far right of the footer.
3. Press Ctrl+Shift+M again, or turn the switch off in Settings, to leave.
   Ctrl+Shift+M is the only key that leaves: `q` and Escape never do.

The choice is saved for every window and the next launch. Strata's system file
chooser follows it too.

Leaving the mode closes prompts and clears `f` filters, `s` searches, and find
highlights. Your selection stays.

## Keys to learn first

<!-- node: integration/10xer-mode, Movement -->
<!-- node: integration/10xer-mode, Selection -->
<!-- node: integration/10xer-mode, Escape -->
<!-- node: integration/10xer-mode, Entering and leaving -->
<!-- node: integration/10xer-mode/file-verbs, Targets -->
<!-- node: integration/10xer-mode/file-verbs, Clipboard -->
<!-- node: integration/10xer-mode/file-verbs, Delete and restore -->
<!-- node: integration/10xer-mode/file-verbs, Create and rename -->
<!-- node: integration/10xer-mode/places, The `g` chord -->
<!-- node: integration/10xer-mode/places, `go ›` -->
<!-- node: integration/10xer-mode/places, `z` and `Z` -->
<!-- node: integration/10xer-mode/search, Find -->
<!-- node: integration/10xer-mode/search, Filter -->
<!-- node: integration/10xer-mode/search, Search -->
<!-- node: integration/10xer-mode/preview-keys, Opening and leaving -->

These work in List and Columns. In Icons, `h`, `j`, `k`, and `l` move between
tiles; press Enter to open one. Capitals mean Shift: `G` is Shift+G.

| Keys | What it does |
| --- | --- |
| `j` / `k` | Next / previous item |
| `h` / `l` | Parent folder / open the folder |
| Enter or `o` | Open the item, including files |
| `g g` / `G` | First / last item |
| `H` / `L` | Back / forward in history |
| `i` | Preview a file while you keep moving |
| Space | Select or unselect, then move down |
| `v` | Select a range as you move |
| `y` / `x` / `p` | Copy / cut / paste |
| `d` | Move to Trash; `d` again confirms |
| `a` | Create a file; end with `/` for a folder |
| `r` | Rename |
| `/`, a name, Enter; then `n` / `N` | Find a name, then next / previous match |
| `f` | Filter this folder |
| `s` | Search this folder and its subfolders |
| `z` | Jump to a visited folder |
| `g h` / `g d` | Home / Downloads |
| `g` Space | Type a path to go to |
| Escape | End one thing: prompt, filter, range, preview, then selection |
| `Q` | Close the window |

Try it: press `s`, type `readme`, and press Enter. The cursor lands on the
first hit; Enter again opens it.

`y`, `x`, and `d` act on the selection, or on the focused item when nothing is
selected. Press `l` on a file to move the keys into its preview, and `h` to
hand them back.

## Who it is for

<!-- node: integration/10xer-mode, Chrome and Settings -->

Turn it on if you use Yazi, Ranger, or Vim, or want your hands on the keyboard
and fewer buttons on screen.

Leave it off if you browse with the mouse or find files by typing their name.
In 10xer mode, **Type to search**, **Keep arrows in file list**, and
**Include subfolders** read **Not used in 10xer mode.**

While the mode is on, its Settings row reads **(experimental feature, under
active development)**: expect keys to change between releases.

**Full detail:** the [10xer mode reference](../reference/10xer-mode.md) lists
every key, chord, prompt, and file chooser rule.
