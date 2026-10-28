---
title: Offline route previews
status: shipped
origin: {issue: lgse/strata#1841, pr: lgse/strata#1842}
branch: null
reviewed_at: 86df474dc0e8352e0e2098637a017cc4c77a8c44
review: draft
code: [src/services/route_preview.rs, src/sandbox_helper/route.rs, src/sandbox_helper/route/fit.rs, src/sandbox_helper/route/geometry.rs, src/sandbox_helper/route/render.rs, src/sandbox_helper/route/xml.rs, src/ui/preview/route.rs, src/ui/preview/route/player.rs, src/ui/preview/route/plot.rs, src/ui/preview/route/position.rs]
tests: [src/sandbox_helper/route/tests.rs, src/ui/preview/route/position/tests.rs, src/ui/preview/tests/route.rs, src/adapters/local_preview/tests/route_preview.rs, tests/qa/scenarios/quick_preview/route-preview-shows-offline-track-and-elevation.jsonl]
related: [preview/preview-panel/media, preview/preview-panel/sandbox, settings/preferences]
---

## Summary

Offline previews of GPS activity and route files (GPX, FIT, and KML) in the drawer and the file chooser, for checking a recorded track without a mapping app. A sandboxed helper draws the route line and an elevation profile, and a media-style player animates a marker along both.

## Behavior

### Showing a route

- Space on a local `.gpx`, `.fit`, or `.kml` file shows the route in an image named "Route preview", with no map tiles or network access. lgse/strata#1842
- Its header shows "N of M in folder", counting the GPX, FIT, and KML files in listing order. lgse/strata#1842
- Its header also shows the file name, with badges for the format, such as "GPX", and the route distance, such as "0.6 km". lgse/strata#1842
- A route with two distinct timestamps adds a duration badge: elapsed time including pauses, with hours on long activities, such as "10:17:50". lgse/strata#1842
- An untimed route shows no duration badge. lgse/strata#1842
- With recorded altitude on a connected pair of points, an "Elevation profile" image shows, headed "Elevation" and its range, such as "10–30 m". lgse/strata#1842
- A route without recorded altitude shows no elevation section. lgse/strata#1842
- Zero and negative altitudes count: a KML from −5 m to 20 m shows "-5–20 m". lgse/strata#1842
- KML altitude counts only with `absolute` altitude mode; clamped and terrain-relative tracks show no elevation section. lgse/strata#1842
- GPX tracks, route points, and waypoints render, as do KML Points, LineStrings, and `gx:Track`, including inside MultiGeometry and MultiTrack. lgse/strata#1842
- Distance never bridges disconnected segments, such as separate GPX track segments or a FIT timer stop. lgse/strata#1842
- In FIT files, enhanced altitude wins over legacy altitude, and invalid GPS fixes break the route. lgse/strata#1842
- KML polygon outlines, KMZ, NetworkLinks, and external assets are not rendered. lgse/strata#1842

### Playback

- The play button or the media play key, Ctrl+Alt+Space by default, moves a marker along the route and the profile together over 15 s. lgse/strata#1842
- The marker moves at a steady ground-distance pace, not by screen length or recorded time. lgse/strata#1842
- During playback, hover, and seeking, the elevation heading also shows the marker's height, such as "29 m". lgse/strata#1842
- The control row shows the marker's distance on the left and the total on the right. lgse/strata#1842 (unverified)
- Both images' accessible description is the marker's distance, such as "0.3 km". lgse/strata#1842
- The play button's tooltip reads "Play/Pause" followed by its shortcut in parentheses; its accessible name is "Play or pause". lgse/strata#1842 (unverified)
- Hovering either image pauses playback and moves both markers to the hovered point. lgse/strata#1842
- Playback resumes only on an explicit play; moving the pointer between the images leaves it paused. lgse/strata#1842
- Where route passes overlap, hovering keeps the pass nearest the current distance among lines within 2 px of the closest. lgse/strata#1842
- Playback stops at the route end; play then restarts from the start. lgse/strata#1842
- The media seek keys, such as Ctrl+Alt+Left and Ctrl+Alt+Right, pause and move the marker a third of the route. lgse/strata#1842 (unverified)
- Mute and volume keys do nothing on a route. lgse/strata#1842 (unverified)
- A route of zero length has an inactive play button. lgse/strata#1842 (unverified)
- Selecting another file, closing the preview, or hiding it in a narrow window stops playback. lgse/strata#1842

### Units

- Distances show in kilometres and heights in metres by default. With Settings → General → Units on Imperial, they show in miles and feet. lgse/strata#1842
- Changing Units updates open route previews in every window, including the chooser, without resetting playback. lgse/strata#1842
- The Units choice applies to later files. lgse/strata#1842
- The route preview has no unit selector of its own. lgse/strata#1842

### Errors and limits

- A malformed or coordinate-free file, such as `<gpx><trk>`, shows "This route file is invalid or contains no supported coordinates." lgse/strata#1842
- A route over 250,000 valid points shows "This route exceeds the 250,000 point preview limit." lgse/strata#1842
- GPX or KML with a DOCTYPE, custom entities, or nesting deeper than 64 levels shows the invalid-route message. lgse/strata#1842
- A FIT file with a bad or missing CRC, or a truncated sequence, shows the invalid-route message. lgse/strata#1842
- Helper output whose images, samples, or distances fail validation shows "The preview renderer produced invalid image data". lgse/strata#1842 (unverified)

## Design

[docs/preview-sandbox.md](https://github.com/lgse/strata/blob/d6c74746cdb27e506a08e8cdefa3bc8cef7d10f9/docs/preview-sandbox.md) "Offline route previews" is the maintained contract: formats, playback, limits, and output validation.

- No basemap or explore slider. Online basemaps and a bar chart were rejected; a route line and elevation line keep the first pass simple (lgse/strata#1841).
- The one-shot `preview-route` helper parses and draws the route. Coordinates and document data stay in the sandbox; only two bounded PNGs, small metadata, and at most 250,000 projected samples return (lgse/strata#1842).
- One projected trace drives both images, hover, and playback. The plot owns transforms, picking, and markers; the player owns position and the timer (lgse/strata#1842).
- The host checks image sizes (800×600 route, 800×70 profile), sample bounds, monotonic distances, segment starts, and profile consistency before showing anything (lgse/strata#1842).
- Distances use a spherical Earth. Longitude wrapping keeps date-line crossings together, and the drawing clamps Web Mercator latitude near 85° (lgse/strata#1842).
- Clamped and terrain-relative KML altitudes need terrain data the sandbox lacks, so only `absolute` mode feeds the profile (lgse/strata#1842).
- Routes reuse the media player layout, details header, and badges. Units are one saved preference shared with Settings; an in-preview selector was removed (lgse/strata#1842).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |

## Known gaps

- `<` and `>` do not step between route files, though the header shows the folder position. lgse/strata#1842
- A FITS astronomy image named `.fit` shows the invalid-route message instead of an unsupported preview. lgse/strata#1842
- A KML holding only polygons, once shown as XML text, shows the invalid-route message. lgse/strata#1842
- Every playback frame resets both images' accessible description, adding AT-SPI traffic. lgse/strata#1842
- After a long frame-clock stall that does not unmap the plot, such as a minimised window, playback jumps to the route end. lgse/strata#1842
