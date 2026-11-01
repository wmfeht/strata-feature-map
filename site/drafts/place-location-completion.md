---
proposed: {page: reference/keyboard-navigation.md, section: "Arrows, the header, and the sidebar"}
nodes: [browser/navigation/location-bar/completion]
reason: 'Folder suggestions under the location entry, and the keys that pick and complete them, are user-visible and no page names the node. The location entry sits in the header, and this section already covers header keys; add the node to the page''s nodes in site/pagemap.yaml and merge the text below as a `###` subsection. Its parent''s text lives on the Installation and SFTP pages, neither of which has a keyboard section.'
release: v1.1.1
---

### Path suggestions in the location entry

While you edit the location (**Ctrl+L**), a popover under the entry, as wide as
the entry, lists child folders whose names start with the typed text, ignoring
case. Absolute paths, `~/` paths and relative paths all complete; a relative path
completes against the current folder and inserts that folder's absolute path.
Typing only `~` suggests `~/`. When the typed text names an existing folder and at
most one sibling matches it, the popover lists that folder's children instead.
The popover does not appear while the breadcrumbs show.

Each suggestion shows a folder icon, the name with the typed part highlighted,
and its parent folder, with your home folder shortened to `~`. Hidden folders are
suggested only when hidden files are shown or the typed name starts with `.`. At
most 50 folders are listed, from the first 10,000 entries.

| Key | Effect |
| --- | --- |
| **Down** / **Up** | Move through suggestions, wrapping at the ends. **Down** also reopens a closed popover. |
| **Page Down** / **Page Up** | Move by 5 suggestions. |
| **Tab** | Insert the highlighted suggestion, the only suggestion, or a longer common prefix, and close the popover. With nothing longer to insert, highlight the next suggestion. |
| **Enter** | Open the highlighted folder. |
| **Escape** | Close the popover while it shows, keeping the typed path and location editing. |

Folders are listed in the background, so a slow or dead mount never blocks
typing. While a listing runs, the previous suggestions stay. **Tab** pressed
during a listing waits for it, as do the arrow and page keys while suggestions
show and an **Enter** after them; they then run in order.
