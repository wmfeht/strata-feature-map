---
proposed: {page: reference/file-providers.md, section: Bundled integrations}
nodes: [remote/file-providers/integrations, remote/file-providers/kde-connect, remote/file-providers/localsend]
reason: 'Settings → Integrations and the bundled KDE Connect and LocalSend providers are user-visible, and no page names their nodes. The External file providers page only mentions the Integrations page''s Refresh and switch in passing; none of its sections covers the catalog or the two integrations. Upstream docs/file-providers.md has a "Bundled integrations" `##` section between "Registration and artwork" and "Transport"; proposed as that new section, with the three nodes added to the page''s nodes. A person must add the `##` section to site/pagemap.yaml.'
release: v1.1.1
---

Raw material for a "Bundled integrations" section.

### Settings → Integrations

**Settings → Integrations** lists the opt-in provider programs bundled with
Strata. **Open folder** closes Settings and opens the providers directory,
`~/.config/strata/providers` by default. **Refresh** reloads the providers,
checks requirements again, and rescans the page. A build with no valid entries
shows "No integrations are bundled with this build."

Under **CATALOG**, with the entry count, each card shows the entry's icon, name,
a two-line description, and **Install** or an "Installed" check. When entries span
two or more categories, chips (**All** first, each with a count) filter the
cards. The grid shows at most three columns, and fewer cards fill the row.

A card's footer reads **Requirements**, with a check when all are met and a red X
when any is missing. Select it to list each requirement as Available or Missing.
For a missing one with a package for the detected pacman, apt, dnf or zypper, it
shows "Install missing dependencies with:" and a command you can copy or start
with **Run in terminal**. Afterwards the page says "The command opened in your
terminal. Select Refresh when it finishes." A command counts only when it
resolves in a trusted system directory, or through a link there to a root-owned
target, such as `/usr/bin/localsend` → `/opt/localsend/localsend`.

**Install** fails with "\<runtime> is not installed in a system directory" when
the entry's interpreter is not in a trusted system directory. Otherwise it writes
the entry into `<providers>/<id>/` (mode 0700, files 0600) with a `provider.json`
whose interpreter and script paths are resolved on this machine. It records a
content hash in `catalog-install.json`, then reloads the providers; no restart is
needed.

**INSTALLED**, with a count, lists catalog installs and every hand-made
registration, sorted by name.

- A catalog install reads "Installed via catalog" and shows **Update** only when
  the bundled files changed. Nothing updates on its own. Updating a copy you
  edited asks first, with **Replace**.
- A registration the catalog does not list reads "Manually installed".
- Each row's switch turns the provider off by writing an empty `disabled` file
  beside `provider.json`, and back on by deleting it.
- **Remove** deletes an unedited catalog install at once. An edited copy, or a
  manually installed one, asks first.
- A failed change shows "The change failed: \<error>" under its row or card.

`STRATA_INTEGRATION_CATALOG=<dir>` replaces the bundled catalog with a directory
in the same layout.

### KDE Connect

Requires `kdeconnect-cli` and the Python module `gi`. With the integration
installed, every paired, reachable device with file sharing on appears by name
under **Send to… ▸ KDE Connect**, sorted by name and updated live while the menu
is open. Two devices with the same name get a short id suffix. More than 63
devices show no entry.

Choosing a device sends the whole selection to it at once, with no picker window,
and shows "Files submitted to \<device>: \<N>. KDE Connect handles transfer
progress and results." KDE Connect confirms submission, not delivery.

- Folders, symbolic links and other non-regular files are never sent: a
  selection containing one shows no KDE Connect entry, and neither does the
  folder background menu.
- A file edited or replaced after the menu opened: "The selected files changed.
  Reopen the right-click menu." Nothing is sent.
- A menu older than 120 seconds, or reused: "This device menu expired. Reopen
  the right-click menu."
- A device that disconnected or turned off sharing rejects the send; it is never
  redirected to another device. An unexpected D-Bus error reports "KDE Connect
  did not confirm the submission. Check your device before retrying." and is not
  retried.

### LocalSend

Requires `localsend` or `localsend_app` in a trusted system directory; Flatpak,
Snap and AppImage installs are not found. With it installed, the item menu on
files, folders, or both shows one **Send to… ▸ LocalSend** entry, with no
submenu. A selection with a symbolic link shows none.

Choosing it opens LocalSend's Send tab with the selected items, added to anything
already there, and shows no notice; LocalSend then picks the device and sends. A
running LocalSend, including one in the tray, takes the items over. LocalSend
started from the menu keeps running after Strata quits.

- An item changed after the menu opened: "The selected items changed. Reopen the
  right-click menu."
- A menu older than 120 seconds, or reused: "This LocalSend menu expired. Reopen
  the right-click menu."
- LocalSend exiting with an error within 1.5 s: "LocalSend closed before it
  opened the selection."

### Messages

Both integrations show their messages in the language of `LC_ALL`, then
`LC_MESSAGES`, then `LANG`, not Strata's language setting, with English as the
fallback.
