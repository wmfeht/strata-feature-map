---
title: Camera photos
status: shipped
origin: {issue: lgse/strata#833, pr: lgse/strata#834}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: reviewed
code: [src/adapters/local_files/camera_photos.rs, src/services/camera_preview.rs, src/ui/browser/camera_scroll.rs, src/ui/thumbnail/camera.rs]
tests: [src/adapters/local_files/camera_photos/tests.rs, src/services/camera_preview/tests.rs, src/app/browser/tests/camera_photos.rs]
docs: [docs/preview-sandbox.md]
related: [preview/preview-panel, browser/thumbnails, browser/view-modes]
---

## Summary

Opening a phone or camera's gphoto2 entry in Devices as one flat, progressive Photos view instead of backend date folders. For iPhone users copying or previewing camera-roll photos over USB.

## Behavior

### Photos view

- Opening a `gphoto2://` camera root shows a flat listing titled "Photos" of every JPEG, HEIC/HEIF, MOV, MP4, and recognized RAW file below it. lgse/strata#834
- `.AAE` sidecars and other formats are hidden from Photos and left untouched on the device. lgse/strata#834
- Files with the same name stay separate rows, each with its original URI. lgse/strata#834
- Discovery skips symlinks and visits newer date-named folders first. lgse/strata#834
- Files inside a hidden folder count as hidden and follow the show-hidden-files setting. lgse/strata#834 (unverified)
- Rows appear in batches; the scan has no deadline or entry limit and runs until it finishes, the user navigates away or refreshes, or the device errors. lgse/strata#834
- Android MTP and iPhone AFC entries keep normal folder browsing. lgse/strata#834
- Deleting a photo removes only that row; a same-named photo from another folder stays listed. lgse/strata#834 (unverified)

### Order

- Photos sorts by Device order by default: batches append in discovery order with no final re-sort. lgse/strata#1029
- Choosing Name or Modified sorts the listing; choosing Device order again reloads it in discovery order. lgse/strata#1029
- Device order is offered in the sort menu only at a camera root. lgse/strata#1029 (unverified)
- In Device order the sort-direction button is disabled, with the tooltip "Device order follows discovery; choose a sort field to reverse its direction". lgse/strata#1029 (unverified)
- The selected photo stays selected while new batches arrive. lgse/strata#1029
- In List view, file-type grouping stays off while loading and in Device order; the saved grouping setting is kept. lgse/strata#834, lgse/strata#1029

### Thumbnails and scrolling

- Thumbnails come from the camera's own preview, limited to 1 MiB and 15 seconds; on failure the file icon stays and the original is not downloaded. lgse/strata#834
- Camera thumbnails are cached only in memory. lgse/strata#834
- Thumbnails appear during the scan: after each batch the scan waits 200 ms, then up to 2 seconds for visible thumbnails. lgse/strata#1021
- Visible thumbnails load top-to-bottom, left-to-right, and are reprioritized after scrolling. lgse/strata#1021
- An untouched viewport at the top stays at the top as batches arrive; after the user scrolls, normal anchoring applies. lgse/strata#1021
- During loading, background selection updates do not scroll List, Icons, or Columns view to the selected photo. lgse/strata#1021

## Design

The README section "Connecting phones" covers backends and setup. [docs/preview-sandbox.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/preview-sandbox.md#camera-file-list-thumbnails) carries the thumbnail and scheduling rules.

- Photos is a virtual listing of the USB-exposed collection, not iOS albums; the backend provides no album membership (lgse/strata#834).
- Each row keeps its real URI, so preview, copy, and delete act on the originals (lgse/strata#834).
- Thumbnails use GVfs `preview::icon`, which requests `GP_FILE_TYPE_PREVIEW`. The preview is decoded in the image sandbox and never falls back to a full download (lgse/strata#834).
- GVfs gphoto2 serves enumeration and previews on one worker, so a continuous scan starved thumbnails. Each batch yields 200 ms for row binding, then up to 2 seconds for the visible wave. This trades total scan speed for early previews (lgse/strata#1013).
- Sorted insertion moved photos under the user while batches arrived, so discovery order became the default. It is not guaranteed chronological (lgse/strata#1026).
- Previewing camera photos without a manual copy is part of the preview panel's remote previews (lgse/strata#834).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-09-15 | lgse/strata#1029 | fix | Defaulted Photos to discovery order so batches append without reshuffling. |
| 2026-09-15 | lgse/strata#1021 | perf | Yielded the camera scan to visible thumbnail waves and kept an untouched viewport at the top. |
| 2026-09-14 | lgse/strata#834 | feat | Opened camera/PTP devices as a flat, progressive Photos view with camera-provided thumbnails. |

## Known gaps

- GVfs publishes a folder's entries only after enumerating that folder, so the first rows wait for the first folder. lgse/strata#1021
- Some iPhones expose an empty photo store with libgphoto2 2.5.34 until an upstream libgphoto2 fix is installed. lgse/strata#834
