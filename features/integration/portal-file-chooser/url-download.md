---
title: Name field filenames and URL downloads
status: shipped
origin: {issue: lgse/strata#1279, pr: lgse/strata#1285}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: reviewed
code: [src/services/remote_download.rs, src/ui/chooser/download.rs]
tests: [src/services/remote_download/tests.rs]
related: []
---

## Summary

The Name field in file-open choosers. Typing an existing filename opens it, and pasting a direct `http://` or `https://` file URL downloads the file to a temporary local path returned to the caller.

## Behavior

### Filenames

- File-open requests show a Name field; typing an existing filename in the displayed folder and pressing Enter or Open returns that file. lgse/strata#1285
- Typing a folder's name and pressing Enter navigates into that folder and clears Name. lgse/strata#1285 (unverified)
- A missing name shows "Choose an existing, accessible file" in the action bar, and the request stays open for another try. lgse/strata#1285
- A name the selected filter rejects shows "The file does not match the selected filter", and the request stays open. lgse/strata#1285
- A name typed before the folder finishes loading survives the automatic first-row selection. lgse/strata#1285

### URLs

- Pasting a direct `http://` or `https://` URL in Name and pressing Enter or Open downloads it and returns a local `file://` URI. lgse/strata#1285
- Downloads land in a new `strata-download-*` folder in the temporary directory and remain after the chooser closes. lgse/strata#1285
- The file is named from `Content-Disposition` `filename*` or `filename`, else the last URL path segment, else `download`. lgse/strata#1285
- While downloading, the bottom-left of the action bar shows a circular progress ring and a cancel button; unknown sizes show a spinner and bytes downloaded. lgse/strata#1285
- Escape or the cancel button stops the download and leaves the chooser open for another name or URL. lgse/strata#1285
- A URL that answers with a redirect fails with "The URL redirects elsewhere; paste the direct file URL instead". lgse/strata#1285
- A URL with credentials before the host is not downloaded. lgse/strata#1285
- A network or HTTP failure, such as a 404, shows "Could not download the file: %{error}" in the action bar, and the request stays open. lgse/strata#1285
- A download whose name the selected filter rejects shows "The file does not match the selected filter" and is not returned. lgse/strata#1285
- Submitting the same URL again in the same chooser reuses the earlier download, while its file still exists, instead of fetching again. lgse/strata#1387
- `strata-download-*` folders older than 24 hours are deleted when the portal starts and when a download begins. lgse/strata#1285
- Folder, SaveFile, and SaveFiles requests do not download URLs, and the address bar and Ctrl+V never start a download. lgse/strata#1285

## Design

The Windows common dialog accepts a pasted file URL and hands the application a local path; this mirrors that behavior (lgse/strata#1279).

- GVfs `http://` mounts were rejected: the backend is often absent and cannot map to a native path (lgse/strata#1279).
- Each download gets its own temporary folder, so names never collide. A shared cache was rejected for simpler cleanup (lgse/strata#1279).
- Files outlive the chooser because the caller opens them after the request completes. A one-day sweep removes them instead (lgse/strata#1285).
- Redirects are refused so a remote server cannot point the portal at host-only services (lgse/strata#1285).
- Server-provided names are reduced to a single safe component of at most 255 bytes, keeping an extension of up to 20 bytes (lgse/strata#1285).
- URLs enter only through Name. The address bar stays navigation-only, and the interaction was moved there at the owner's request (lgse/strata#1285).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-01 | lgse/strata#1285 | feat | Added a Name field to file-open choosers that opens typed filenames and downloads pasted HTTP(S) URLs. |

## Known gaps

None known.
