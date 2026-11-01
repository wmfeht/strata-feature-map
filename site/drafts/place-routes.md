---
proposed: {page: reference/preview-sandbox.md, section: Offline route previews}
nodes: [preview/preview-panel/routes]
reason: 'Offline GPX, FIT, and KML route previews are user-visible, and the node is on no page. The Preview sandbox page''s "Providers" section now covers the route sandbox, its limits and messages, and the Units choice, but not the header, elevation profile, supported geometry, or playback. Upstream docs/preview-sandbox.md has an "Offline route previews" `##` section between "Local 3D model previews" and "Browser worker pool"; proposed as that new section, with the node added to the page''s nodes. Limits and error messages are already in the Providers section of the same page; the new section should link there rather than repeat them. A person must add the `##` section to site/pagemap.yaml.'
release: v1.1.1
---

Quick preview on a local `.gpx`, `.fit`, or `.kml` file shows the route in an
image named "Route preview", drawn in the sandbox with no map tiles or network
access, in the drawer and the file chooser. The header shows "N of M in folder",
counting route files, the file name, and badges for the format, such as "GPX",
and the distance, such as "0.6 km". A route with two distinct timestamps adds a
duration badge: elapsed time including pauses, such as "10:17:50".

With recorded altitude on a connected pair of points, an "Elevation profile"
shows below, headed "Elevation" and its range, such as "10–30 m"; otherwise that
section is left out. Zero and negative altitudes count. KML altitude counts only
in `absolute` altitude mode.

GPX tracks, route points and waypoints render, as do KML Points, LineStrings,
and `gx:Track`, also inside MultiGeometry and MultiTrack. Distance never bridges
separate segments, such as GPX track segments or a FIT timer stop. FIT enhanced
altitude wins over legacy altitude, and invalid GPS fixes break the route. KML
polygon outlines, KMZ, NetworkLinks, and external assets are not rendered.

### Playback

The play button, or the media play key (**Ctrl+Alt+Space** by default), moves a
marker along the route and the profile together over 15 s, at a steady
ground-distance pace. During playback, hover, and seeking, the elevation heading
also shows the marker's height. Hovering either image pauses and moves both
markers to that point; playback resumes only on play. The media seek keys, such
as **Ctrl+Alt+Left** and **Ctrl+Alt+Right**, pause and move the marker a third of
the route. Playback stops at the end; play then restarts it. Selecting another
file, closing the preview, or hiding it stops playback.

### Units

Changing **Settings → General → Units** updates open route previews in every
window, including the chooser, without resetting playback. The preview has no
unit selector of its own.

### Errors and limits

Besides the cases in the Providers section, a FITS astronomy image named `.fit`
shows the invalid-route message.
