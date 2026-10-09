---
title: Remote locations and file providers
status: shipped
origin: {issue: lgse/strata#20, pr: lgse/strata#31}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: reviewed
code: []
tests: []
docs: []
related: []
---

## Summary

How files that do not live on a local disk reach Strata. Children: `remote/file-providers/network-locations` (SMB, SFTP, and other GIO/GVfs locations, with mounting and sign-in) and `remote/file-providers/external` (opt-in provider programs that add live badges and context actions, such as cloud availability).

## Behavior

## Design

Strata delegates remote access instead of implementing protocols, accounts, or credential storage itself.

- Network locations go through GIO/GVfs and a GTK mount operation, not `ssh`, `smbclient`, or `mount`. Permanent secrets are left to the backend and the desktop keyring (lgse/strata#20).
- Cloud services stay outside Strata. A provider program keeps authentication and cloud operations in its own service, and Strata has no dependency on any one provider (lgse/strata#1356, lgse/strata#1385).
- HTTP(S) URL downloads in the file chooser belong to `integration/portal-file-chooser/url-download`, and remote preview staging to `preview/preview-panel`.

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |

## Known gaps

None known.
