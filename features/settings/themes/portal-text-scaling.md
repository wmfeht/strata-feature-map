---
title: Desktop text scaling without GTK portals
status: shipped
origin: {issue: lgse/strata#2042, pr: lgse/strata#2045}
branch: null
reviewed_at: 1d2e244b55aac2fabad2a7b2a108ebf5969df59e
review: draft
code: [src/ui/theme/portal_text_scale.rs]
tests: [src/ui/theme/portal_text_scale/tests.rs]
related: [browser/view-modes/text-size, integration/file-manager-interface/service-activation, integration/portal-file-chooser, app/infrastructure]
---

## Summary

Reads the desktop's text-scaling factor from the settings portal in a Strata process restarted with GTK portals disabled. It is for users with a non-1 text-scaling factor whose Strata starts through D-Bus activation, so its text matches a window started with `strata`.

## Behavior

- With `text-scaling-factor` 1.25 and text size 12, a window cold-started by a FileManager1 `ShowFolders` call draws text at the same size as one started with `strata`. lgse/strata#2045
- In that process, changing `text-scaling-factor` while the window is open rescales its text and interface icons without a restart. lgse/strata#2045
- A window activated with `GDK_DEBUG=no-portals` already set keeps GTK's 96 DPI text. lgse/strata#2045
- A `strata --portal` process restarted with `no-portals` also reads the factor at startup and follows `SettingChanged`. lgse/strata#2045, lgse/strata#2024 (unverified)
- Only `text-scaling-factor` in `org.gnome.desktop.interface` with a floating-point value is applied; other keys and namespaces change nothing. lgse/strata#2045 (unverified)
- The factor sets `gtk-xft-dpi` to factor × 96 × 1024, rounded, so 1.1818 gives 116176. lgse/strata#2045 (unverified)
- A factor of 0, below 0, NaN, or infinite leaves `gtk-xft-dpi` unchanged. lgse/strata#2045 (unverified)
- Without a session bus, or when the portal `ReadAll` call fails, `gtk-xft-dpi` stays at GTK's value and a debug log records it. lgse/strata#2045 (unverified)
- A reply without a floating-point `text-scaling-factor` leaves `gtk-xft-dpi` unchanged, without a log. lgse/strata#2045 (unverified)

## Design

- Strata restarts a D-Bus-activated process with `GDK_DEBUG=no-portals` so GTK cannot deadlock on the portal waiting for Strata (lgse/strata#1811, lgse/strata#2024).
- GTK's Wayland backend has no settings source but the portal, so `gtk-xft-dpi` fell back to 96 DPI. With factor 1.18, 12 px text rendered at 12 px, not 14 px (lgse/strata#2045).
- The portal is read asynchronously, so the activating call can never block on it (lgse/strata#2045).
- Strata sets only `gtk-xft-dpi`. Its existing `gtk-xft-dpi` listeners rescale the CSS root font and interface icons (lgse/strata#2045).
- A user who sets `no-portals` themselves chose to keep GTK off the portal, so Strata leaves it alone (lgse/strata#2045).
- The bug needed activation to start a new process; a running, normally launched Strata takes the request and already has the factor (lgse/strata#2045).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |

## Known gaps

None known.
