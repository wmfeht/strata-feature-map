---
title: Send to removable devices
status: shipped
origin: {issue: lgse/strata#1153, pr: lgse/strata#1278}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: reviewed
code: [src/ui/browser/destination.rs]
tests: [src/ui/browser/context_menu/actions/tests.rs]
related: [devices/volumes]
---

## Summary

A Send to… submenu in the item menu that copies the selection to a mounted removable device without leaving the current folder. It is for people who copy to USB drives often.

## Behavior

- The item menu shows Send to… only when items are selected and a mounted, writable, local removable device exists. lgse/strata#1278, lgse/strata#1393
- Device rows are sorted by name, ignoring case; devices sharing one identity are left out. lgse/strata#1278 (unverified)
- Each device submenu offers Drive root, up to 3 recent folders labeled "<folder> (recent)", and Choose folder…. lgse/strata#1278
- A recent folder that no longer exists on the device is left out of its submenu. lgse/strata#1278 (unverified)
- Sending copies the selection, never moves it, and leaves the browser in its current folder. lgse/strata#1278
- Choose folder… opens a floating chooser titled "Send to folder" whose navigation stays inside the device. lgse/strata#1384
- The Send to folder chooser hides the sidebar, confirms with "Copy here", and offers no New Folder. lgse/strata#1384 (unverified)
- A subfolder chosen there becomes a recent destination for that device. lgse/strata#1278
- Sending to a folder moves it to the top of the recent list; the drive root never becomes a recent entry. lgse/strata#1278 (unverified)
- If the device is gone when a destination is activated or the chooser confirms, "Destination unavailable" appears and nothing is copied. lgse/strata#1278, lgse/strata#1384
- A send that finishes before progress appears shows "Copied to <device>" or "N items copied to <device>" for 2 seconds. lgse/strata#1278 (unverified)
- An open Send to… menu updates as devices mount and unmount. lgse/strata#1393

## Design

Windows Explorer's Send to was the model: pick a drive and the copy starts without leaving the current folder (lgse/strata#1153).

- Drive root is an explicit first row because a `GMenuModel` item carries either an action or a submenu, never both (lgse/strata#1153).
- Device targets are resolved again when a destination is activated and when the chooser confirms, so a stale or remounted device fails closed (lgse/strata#1278, lgse/strata#1384).
- Stopping Strata's writes does not make earlier writes safe to unplug; only a confirmed safe eject does (lgse/strata#1278).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-27 | lgse/strata#1278 | feat | Added a Send to… submenu that copies to removable devices without navigating. |

## Known gaps

None known.
