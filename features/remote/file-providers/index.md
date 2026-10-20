---
title: Remote locations and file providers
status: shipped
origin: {issue: lgse/strata#20, pr: lgse/strata#31}
branch: null
reviewed_at: e0f73973926ff67e77c2c56cf288b7b7617bb2e5
review: draft
code: []
tests: []
docs: []
related: []
---

## Summary

How files that do not live on a local disk reach Strata. `remote/file-providers/network-locations` covers SMB, SFTP, and other GIO/GVfs locations, with mounting and sign-in. `remote/file-providers/external` covers opt-in provider programs that add live badges, context actions, and Send to… destinations. `remote/file-providers/integrations` is the Settings → Integrations catalog that installs bundled providers. `remote/file-providers/kde-connect` and `remote/file-providers/localsend` are the two bundled providers.

## Behavior

## Design

Strata delegates remote access instead of implementing protocols, accounts, or credential storage itself.

- Network locations go through GIO/GVfs and a GTK mount operation, not `ssh`, `smbclient`, or `mount`. Permanent secrets are left to the backend and the desktop keyring (lgse/strata#20).
- Cloud services stay outside Strata. A provider program keeps authentication and cloud operations in its own service, and Strata has no dependency on any one provider (lgse/strata#1356, lgse/strata#1385).
- Integrations such as KDE Connect and LocalSend ship in Strata's repository but stay separate, opt-in provider programs that the user installs from Settings (lgse/strata#1741, lgse/strata#1748).
- HTTP(S) URL downloads in the file chooser belong to `integration/portal-file-chooser/url-download`, and remote preview staging to `preview/preview-panel`.

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |

## Known gaps

None known.
