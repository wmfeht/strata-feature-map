---
title: Launched-program GDK_DEBUG restore
status: shipped
origin: {issue: lgse/strata#1810, pr: lgse/strata#1811}
branch: null
reviewed_at: bf26829b4fd74c1f25ac170aad9521a633234a30
review: draft
code: [src/child_environment.rs]
tests: [src/child_environment/tests.rs]
related: [app/infrastructure, integration/open-with, integration/open-with/terminal, browser/context-menu, operations/progress/jobs, remote/file-providers/external, settings/preferences, preview/preview-panel/documents]
---

## Summary

A Strata that D-Bus activated for FileManager1 runs with `no-portals` added to `GDK_DEBUG` (see `app/infrastructure`). This node gives programs launched from that process the original `GDK_DEBUG` back, so their own portals keep working.

## Behavior

- From the activated process, default-app opens, Open With, the context-menu default app, Open in Terminal, and Omarchy maintenance commands from Settings see the original `GDK_DEBUG`, or none when it was unset. lgse/strata#1811
- Executables and `.sh` files, custom actions, file providers, document-preview web links, the AUR package page opened by Settings' update action, and Restart now in Settings get the same restore. lgse/strata#1811
- None of those programs see `STRATA_ORIGINAL_GDK_DEBUG`. lgse/strata#1811
- In a process Strata did not re-exec, launched programs inherit `GDK_DEBUG` unchanged. lgse/strata#1811 (unverified)

## Design

- Launched programs get the original `GDK_DEBUG` back, because GDK's `no-portals` overrides its sandbox check and broke portals in Flatpak apps (https://github.com/lgse/strata/pull/1811#issuecomment-6350215206).
- The re-exec that adds `no-portals` lives in `src/main.rs` and is described on `app/infrastructure`; this node owns only the restore (lgse/strata#1811).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-23 | lgse/strata#1811 | fix | Re-exec'd service-activated Strata without GTK portals to stop a 25 s FileManager1 stall, and restored `GDK_DEBUG` for launched programs. |

## Known gaps

None known.
