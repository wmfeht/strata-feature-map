---
title: Document preview scrollbar
status: shipped
origin: {issue: lgse/strata#1749, pr: lgse/strata#1752}
branch: null
reviewed_at: 86df474dc0e8352e0e2098637a017cc4c77a8c44
review: reviewed
code: [src/ui/virtual_preview/scrollbar.rs, src/ui/virtual_preview/scrollbar/position.rs]
tests: [src/ui/virtual_preview/scrollbar/tests.rs]
related: [preview/preview-panel/find, integration/portal-file-chooser]
---

## Summary

The vertical scrollbar of rendered documents and large plain-text Source previews, in the browser and the file chooser. Its thumb follows a document position rather than GTK's estimated pixel heights, so held, dragged, and touchpad-scrolled thumbs stop jumping.

## Behavior

- In a rendered document or a large plain-text Source preview, holding the scrollbar thumb still keeps the content at one position. lgse/strata#1752, lgse/strata#1749
- Dragging the thumb downward never moves the content backward, and the content passes through interior positions on the way. lgse/strata#1752
- Dragging the thumb to the top or bottom of the track shows the document's first or last line, even while new rows are measured. lgse/strata#1752
- Releasing the thumb, even with the pointer over the content, leaves the content in place. The next wheel input scrolls it and the thumb follows. lgse/strata#1752
- Closing the preview while holding the thumb ends the drag; after reopening, the thumb follows scrolling again. lgse/strata#1752 (unverified)
- Setting the scrollbar to its minimum or maximum from the keyboard or an accessibility tool shows the document's exact start or end. lgse/strata#1752
- Wheel or touchpad scrolling forward over the content never moves the thumb backward; scrolling backward never moves it forward; stopping leaves it still. lgse/strata#1752
- With the first row's top in view, the thumb sits at the top of the track. With the last row's end in view, it sits at the bottom. lgse/strata#1752 (unverified)
- Touchpad momentum stops when the scroll range changes or the content origin shifts by 2 px or more. lgse/strata#1752
- Document previews in the Open and Save file chooser scroll the same way as in the browser. lgse/strata#1752
- The vertical scrollbar sits beside the content instead of overlaying it, and hides when the whole document fits. lgse/strata#1752 (unverified)

## Design

- GTK estimates unmeasured row heights and re-anchors its pixel value, so a thumb mirroring those pixels jumped. The thumb now follows a separate document position, rows plus a text-offset fraction, while GTK's pixel adjustment still drives native input and kinetic scrolling (lgse/strata#1749, lgse/strata#1752).
- GTK's kinetic trajectory stores an absolute pixel origin, so stale momentum is cancelled rather than corrected. A 2 px tolerance absorbs GTK's integer rounding. A second scroll engine, disabled momentum, and two-frame `scroll_to` corrections were rejected (lgse/strata#1752).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |

## Known gaps

- A touchpad flick can end early when newly measured rows change the scroll range or content origin. lgse/strata#1752
