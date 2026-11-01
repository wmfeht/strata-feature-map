---
proposed: {page: reference/install.md, section: Release channels}
nodes: [app/updates/release-picker]
reason: 'The "### Install a specific release" subsection under "Release channels" already covers which releases the menu lists and the dialog a chosen release opens, but not the row''s description, its loading and error states, the check mark, or the disabled button. Add the node to the page''s nodes in site/pagemap.yaml and merge the facts below into that subsection, with no second heading.'
release: v1.1.1
---

Facts to merge into the existing subsection:

- The row reads "Roll back or switch to another release your channel offers."
  Its menu button shows the installed version, such as `v1.1.1`. With automatic
  checks off, the menu still works while the **Release channel** menu is
  locked.
- Opening **Settings → Updates** requests no list. Opening the menu shows
  "Loading releases…", then the list. Reopening it on the same channel reuses the
  list. After a failed load, the next opening asks again. Changing the channel
  discards the list: an open menu reloads at once, a closed one when next opened.
- A channel with nothing to install shows "No releases are available on this
  channel." A failed request shows "Couldn't load releases: \<reason>".
- Each entry shows `vX` above its build kind and date, such as "Stable ·
  \<date>", or the build kind alone when the release has no date. The installed
  release has a check mark, and choosing it closes the menu and does nothing
  else.
- The menu button is disabled while the chosen release's commit is resolved.
