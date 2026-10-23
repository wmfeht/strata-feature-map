---
title: Portal-free service activation
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

When D-Bus activates Strata to answer a FileManager1 call, Strata runs without GTK desktop portals so the call cannot stall on the portal that made it. Programs Strata launches from that process get the original `GDK_DEBUG` back. It is for anyone whose browser or app opens "Show in folder" through xdg-desktop-portal.

## Behavior

- Started with `--gapplication-service` before any `--`, Strata re-execs before GTK starts, with `no-portals` appended to `GDK_DEBUG`, such as `misc:no-portals`. lgse/strata#1811
- A FileManager1 `ShowItems` call while Strata is not running, such as Chromium's "Show in folder", gets its reply without the 25 s portal timeout. lgse/strata#1810, lgse/strata#1811
- `strata`, `strata /tmp`, `strata -- --gapplication-service`, `--portal`, and `--preview-helper` launches add no override and do not re-exec for it. lgse/strata#1811
- A `GDK_DEBUG` that already holds `no-portals`, in any case and after `:`, `;`, `,`, a space, or a tab, adds nothing and does not re-exec for it. lgse/strata#1811
- Later `strata` launches open in the activated process, so GTK portals stay off until that process exits. lgse/strata#1811
- From the activated process, default-app opens, Open With, the context-menu default app, Open in Terminal, and Omarchy presentation see the original `GDK_DEBUG`, or none when it was unset. lgse/strata#1811
- Executables and `.sh` files, custom actions, file providers, document-preview web links, the AUR page, and Restart now in Settings get the same restore. lgse/strata#1811
- None of those programs see `STRATA_ORIGINAL_GDK_DEBUG`. lgse/strata#1811
- In a process Strata did not re-exec, launched programs inherit `GDK_DEBUG` unchanged. lgse/strata#1811 (unverified)

## Design

- xdg-desktop-portal 1.22.1 waits in `OpenDirectory` for the `ShowItems` reply, while GTK's startup queries that portal before FileManager1 is exported. Replying earlier in the handler cannot break that wait (lgse/strata#1810, lgse/strata#1811).
- The override is set by re-exec before GTK starts, not by changing the environment after threads may run. It shares the Cairo renderer and `GTK_THEME` restart path (lgse/strata#1811).
- The re-exec decision lives in `src/main.rs`, a shared module `app/infrastructure` owns; this node owns the restore for launched programs (lgse/strata#1811).
- The override is scoped to service activation and is not a substitute for asynchronous dispatch in the portal. Packagers keep `--gapplication-service` in activation commands and do not set `no-portals` globally (lgse/strata#1811, docs/packaging.md).
- Launched programs get the original `GDK_DEBUG` back, because GDK's `no-portals` overrides its sandbox check and broke portals in Flatpak apps (https://github.com/lgse/strata/pull/1811#issuecomment-6350215206).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-23 | lgse/strata#1811 | fix | Re-exec'd service-activated Strata without GTK portals to stop a 25 s FileManager1 stall, and restored `GDK_DEBUG` for launched programs. |

## Known gaps

- No maintained test reproduces a cold FileManager1 activation against the portal; only the environment policy is tested. lgse/strata#1811
