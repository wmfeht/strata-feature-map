---
title: Chooser window size and placement
status: shipped
origin: {issue: lgse/strata#535, pr: lgse/strata#538}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: reviewed
code: [src/portal/window_geometry.rs]
tests: [src/portal/window_geometry/tests.rs, src/portal/window_geometry/tests/centering.rs]
related: []
---

## Summary

The chooser window's initial size and position. Size follows the monitor and a parent window: the requesting application's window on Hyprland, or the originating Strata window for destination choosers. Floating choosers are centered on their monitor.

## Behavior

### Size

- The chooser opens at 80% of the bound's width and 78% of its height, at most the bound minus 120 px and 100 px. lgse/strata#405
- That size is clamped between 640×460 and 1000×680 px. lgse/strata#405
- On a bound under 760 px wide or 560 px tall, the 640×460 minimum overrides the clearance; a bound below 640×460 caps the minimum at the bound. lgse/strata#405 (unverified)
- The bound is the monitor size; without monitor geometry it is the parent size, and without either the chooser opens at 920×580. lgse/strata#405, lgse/strata#538 (unverified)
- On Hyprland, a request with a Wayland parent and an app ID uses the requesting window's size when exactly one window's class or initial class matches. lgse/strata#538
- With both sizes known, the bound is the smaller of the monitor and parent size in each dimension. lgse/strata#538
- A sole matching window that is unmapped, hidden, or has a zero size gives no size hint. lgse/strata#538 (unverified)
- Matching ignores case and keyboard focus; several matches, a missing app ID, X11, or other compositors keep monitor-based sizing. lgse/strata#538
- The Hyprland size query is read-only and gives up after 100 ms or a reply over 1 MiB. lgse/strata#538
- Moving the chooser to another monitor keeps a manual resize. lgse/strata#538
- A destination chooser for Move to, Copy to, Extract to, or Send to uses its originating window's current size as the parent size, on any compositor. lgse/strata#1384 (unverified)

### Placement

- On Hyprland, floating choosers open centered on their monitor, not over the calling window, and keep their parent and modal relationship. lgse/strata#538
- Before each chooser, Strata registers the runtime window rule `strata-file-chooser-center` for the class `io.github.lgse.Strata.FileChooser` and sets only `center`. lgse/strata#538
- The rule is refreshed before every chooser, so centering survives a Hyprland config reload without accumulating rules. lgse/strata#538
- Lua and legacy configurations with named window-rule support both get the rule; unsupported rules, missing IPC, or a 100 ms timeout keep compositor placement. lgse/strata#538
- Regular Strata windows keep their usual placement. lgse/strata#538
- Destination choosers also register the rule and take the chooser identity, so they open centered too. lgse/strata#1384

## Design

- Hard-coded 1050×720 overflowed 1152×720 logical displays with a bar, hiding the action row (lgse/strata#399).
- Wayland exported parent handles give transiency but no geometry, and GTK already honors compositor bounds. For portal requests, a Hyprland query is the only parent-size source, used only for an unambiguous app ID (lgse/strata#535).
- The reporter asked for monitor centering after the sizing fix. Strata adds a runtime rule matching only the chooser identity instead of editing Hyprland configuration files (lgse/strata#535).
- The portal process identifies as `io.github.lgse.Strata.FileChooser`, separate from `io.github.lgse.Strata`, so the rule never affects file-manager windows (lgse/strata#538).
- Named-rule support is probed without effect, then match and `center` are set in one IPC batch so a reload cannot split them (lgse/strata#538).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-07 | lgse/strata#538 | fix | Sized choosers from a single matching Hyprland window and centered them on the monitor with a runtime rule. |
| 2026-09-06 | lgse/strata#405 | fix | Sized the chooser from the monitor instead of a fixed 1050×720, fitting small and scaled screens. |

## Known gaps

None known.
