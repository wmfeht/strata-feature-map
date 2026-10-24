---
title: Integrations catalog
status: shipped
origin: {issue: lgse/strata#1741, pr: lgse/strata#1748}
branch: null
reviewed_at: c94eeb0020fa1154e11c741888f1b56d92ce70d6
review: draft
code: [src/services/integration_catalog.rs, src/ui/settings/integrations.rs, data/icons/scalable/actions/strata-blocks.svg, data/icons/scalable/actions/strata-cloud.svg, data/icons/scalable/actions/strata-git-branch.svg, data/icons/scalable/actions/strata-smartphone.svg]
tests: [src/services/integration_catalog/tests.rs, src/ui/settings/integrations/tests.rs]
docs: [docs/file-providers.md, integrations/README.md]
related: [remote/file-providers/external, remote/file-providers/kde-connect, remote/file-providers/localsend, settings/preferences, app/infrastructure]
---

## Summary

Settings → Integrations, a catalog of opt-in provider programs bundled with Strata under `integrations/`. It installs an entry as an external file provider, updates it when the bundled copy changes, turns it off, and removes it. It also lists hand-made registrations beside catalog installs. For users who want KDE Connect or LocalSend in the context menu without copying files by hand.

## Behavior

### Page

- Settings → Integrations shows the intro "Optional integrations bundled with Strata connect the context menu to other apps and services…" with Refresh and Open folder buttons. lgse/strata#1748
- Open folder closes Settings and opens the providers directory, default `~/.config/strata/providers`, in the browser. lgse/strata#1748
- Each visit to the page rescans the catalog and the providers directory. lgse/strata#1748 (unverified)
- Refresh reloads the providers (see `remote/file-providers/external`), discards cached requirement results, checks them again, and rescans the page. lgse/strata#1748
- A catalog with no valid entries shows "No integrations are bundled with this build." lgse/strata#1748

### Catalog

- The CATALOG heading shows the entry count. Each card shows the entry's PNG or its category icon, its name, a description cut to two lines, and Install or an "Installed" check; the maintainer is not shown. lgse/strata#1748, lgse/strata#1704
- Category chips, All first, each with a count, appear only when the entries span two or more categories. Choosing a chip shows only that category's cards. lgse/strata#1704
- A selected category with no entries left after a rescan returns to All. lgse/strata#1704 (unverified)
- With two visible cards each card takes half the row, one card fills the row, and the grid never shows more than three columns. lgse/strata#1761
- Choosing a category chip resizes the columns to the cards it leaves visible. lgse/strata#1761

### Requirements

- A card's footer reads "Requirements" with a check when every requirement is met, a red X when any is missing, and no mark while the check runs. lgse/strata#1748, lgse/strata#1704
- Selecting the footer expands it to "Requires:" with one Available or Missing chip per requirement, the runtime first, and relabels it "Hide requirements". It shows "Checking…" until results arrive. lgse/strata#1748, lgse/strata#1704
- For each missing requirement with a package for the detected pacman, apt, dnf, or zypper, the expanded footer shows "Install missing dependencies with:" and the copyable command. lgse/strata#1748
- Each install command has a Run in terminal button. After the terminal opens, the page says "The command opened in your terminal. Select Refresh when it finishes." lgse/strata#1704, lgse/strata#1729
- When no terminal emulator resolves, selecting Run in terminal shows "No terminal emulator was found." under the command. It suggests `xdg-terminal-exec` with `~/.config/xdg-terminals.list`, setting `$TERMINAL`, or a listed terminal. lgse/strata#1729 (unverified)
- A `command` requirement is met when its name or one of its `alternatives` resolves in a trusted system directory. lgse/strata#1748, lgse/strata#1756
- A `command` requirement is also met through a link in a search directory, such as `/usr/bin/localsend` → `/opt/localsend/localsend`. lgse/strata#1756
- That link counts only when root owns the target and every directory above it, and none is group- or world-writable. lgse/strata#1756
- A `module` requirement is checked with the resolved interpreter's `-I` and `importlib.util.find_spec`, never by importing it, and counts as missing after 5 seconds. lgse/strata#1748
- Expanded footers stay expanded across rescans, and revisiting the page reuses requirement results until Refresh. lgse/strata#1748

### Install, update, and remove

- Install fails with "<runtime> is not installed in a system directory" when the entry's runtime does not resolve in a trusted system directory. lgse/strata#1748
- Install creates the providers directory and `<id>/` with mode 0700, refuses a symlinked or group- or world-writable directory, and writes each file with mode 0600. lgse/strata#1748
- The installed `provider.json` runs the resolved interpreter on the absolute entry path and carries the entry's name, icons, and category. `catalog-install.json` records the catalog hash and each file's SHA-256. lgse/strata#1748, lgse/strata#1704
- After an install, update, removal, or switch change succeeds, the page reloads the providers and rescans, with no restart notice. lgse/strata#1748
- A catalog install's row reads "Installed via catalog" and shows Update only when the bundled files differ from the recorded hash; nothing updates automatically. lgse/strata#1748, lgse/strata#1704
- Update on a copy whose files differ from the record asks "The installed copy has local changes. Updating replaces them with the bundled files." with Cancel and Replace; files change only on Replace. lgse/strata#1748
- An update deletes files the previous install recorded that the new entry lacks, and keeps the `disabled` marker. lgse/strata#1748
- Remove deletes an unedited catalog install at once; an edited one first asks "The installed copy has local changes that are deleted with it." lgse/strata#1748
- A failed change shows "The change failed: <error>" under its row or card and enables its controls again. lgse/strata#1748 (unverified)

### Installed list

- INSTALLED, with a count, lists catalog installs and every other slug-named entry in the providers directory, sorted by name, and is hidden when there are none. lgse/strata#1748, lgse/strata#1704
- A registration under an id the catalog does not list reads "Manually installed" and shows its manifest `name`, or its id. Its icon shows only when it loads as a trusted provider. lgse/strata#1748, lgse/strata#1704
- Remove on a manually installed row asks "This copy was not installed from the catalog. Its folder is deleted." first. lgse/strata#1748
- A catalog id's directory without a valid `catalog-install.json` reads "Manually installed" with no Update, and keeps the catalog entry's name and icon. lgse/strata#1748 (unverified)
- Each installed row has a switch labelled Enabled or Disabled. Off writes an empty `disabled` file beside `provider.json`; on deletes it. lgse/strata#1748

### Catalog format

- `STRATA_INTEGRATION_CATALOG=<dir>` replaces the bundled catalog. Directories starting with `.` or `_` are skipped, and an invalid entry logs `Strata integration <dir>: <error>` and is left out. lgse/strata#1748
- An entry is rejected unless `schema_version` is 1, `id` matches its directory slug, and `entry` is one of its files. lgse/strata#1748
- An entry is rejected unless `name` is plain text of at most 64 bytes, `description` at most 400 bytes, and `maintainer` a GitHub username. lgse/strata#1748
- An entry is rejected with more than 32 files or a file over 1 MiB. lgse/strata#1748
- An entry is rejected with more than 16 icons, or an icon that is not a PNG of at most 256×256. lgse/strata#1748
- An entry is rejected when it bundles a file named `provider.json`, `catalog-install.json`, or `disabled`. lgse/strata#1748
- An entry is rejected with more than 8 requirements, or a requirement naming both or neither of `command` and `module`. lgse/strata#1748
- An entry is rejected for a dotted `module`, or a package manager other than pacman, apt, dnf, and zypper. lgse/strata#1748
- An entry is rejected for `alternatives` on a `module` requirement, more than 4 alternatives, or an alternative that is not an executable basename. lgse/strata#1756 (unverified)

## Design

`integrations/README.md` describes the catalog layout, `catalog.toml`, and the maintenance policy; `docs/file-providers.md` covers bundled integrations beside the provider protocol.

- Entries ship in Strata's repository rather than in external repositories pinned by hash: users can find them, reviewers read code instead of hashes, and contributors need no release process (lgse/strata#1741).
- Integrations stay opt-in. Shipping them enabled was rejected (lgse/strata#1741).
- Each entry names a maintainer. A broken, unmaintained entry is marked and removed after a release cycle (lgse/strata#1741).
- Updates follow the content hash, with no version field. Nothing updates automatically, and local edits are confirmed before they are replaced (lgse/strata#1741, lgse/strata#1748).
- The interpreter and script paths are resolved at install time and written into `provider.json`; nothing runs through a PATH lookup (lgse/strata#1741, lgse/strata#1748).
- Module requirements must be top-level, so the check never imports a parent package (lgse/strata#1748).
- Changes reload the providers instead of asking for a restart (lgse/strata#1748).
- The catalog is named after what users see, integrations. The install directory and protocol keep "providers" because the directory also holds hand-made registrations (lgse/strata#1748).
- Every LocalSend package installs a `/usr/bin` link into `/opt` or `/usr/lib`, which the trusted-command rule rejected. The relaxed rule applies only to integration requirement checks (lgse/strata#1756).
- A GTK `FlowBox` keeps space for empty columns, so the column count is capped at the cards shown (lgse/strata#1761).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-18 | lgse/strata#1761 | fix | Capped the catalog grid's columns at the visible card count, so two cards fill the row without an empty third column. |
| 2026-10-18 | lgse/strata#1748 | feat | Added Settings → Integrations, a bundled opt-in catalog that installs, updates, turns off, and removes provider registrations. |

## Known gaps

- When turning an integration's switch on or off fails, the error shows but the switch keeps its new position until Refresh. lgse/strata#1748
- With more than one row of cards, expanding one card's requirements leaves empty space below the cards in other rows, because every row takes the tallest card's height. lgse/strata#1761
